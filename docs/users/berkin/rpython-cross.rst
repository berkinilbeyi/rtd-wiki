==========================================================================
Cross-translating RPython-based interpreters
==========================================================================

There are some directions here: https://pypy.readthedocs.org/en/release-2.4.x/arm.html

Packages installed (to ``brg-05``)::

  debootstrap.noarch (for cross-translation)
  glib2-static-2.28.8-4.el6.x86_64 (for static building of qemu)

--------------------------------------------------------------------------
scratchbox2
--------------------------------------------------------------------------

::

  % git clone git@gitorious.org:scratchbox2/scratchbox2.git

Creating a ``build`` dir doesn't work::

  % cd scratchbox2
  % ./autogen.sh
  % make install prefix=$STOW_PKGS_PREFIX/pkgs/scratchbox2

Stow install as usual.

--------------------------------------------------------------------------
debootstrap
--------------------------------------------------------------------------

Had to install ``debootstrap.noarch`` through yum. ``debootstrap``
requires root privileges. For the target directory, I first tried a
location on ``bits0``, but this didn't work because of permission issues.
So I created a temporary root directory at ``/srv/chroot/precise_arm`` on
``brg-05``::

  % sudo mkdir -p /srv/chroot/precise_arm
  % sudo debootstrap --variant=buildd --arch armel --foreign precise /srv/chroot/precise_arm http://ports.ubuntu.com/ubuntu-ports/

Note that different from the instructions, I used normal ``debootstrap``
instead of ``qemu-debootstrap``. It seems like ``qemu-debootstrap`` isn't
available on Red Hat and I couldn't find the source code. What
``debootstrap`` seems to do is create a minimal Debian-based distribution
at the specified target directory. In addition to fetching packages and
extracting them, it also runs some commands. Becasuse the target is arm,
those commands don't run on x86. ``qemu-debootstrap`` seems to a wrapper
that uses ``qemu`` to run those target binaries. Instead of using this
approach, I'm trying a two-step approach, where specifying ``--foreign``
disables executing those commands for the target platform and stops after
extracting packages. 


::

  % cd qemu-2.1.0
  % mkdir build-static
  % cd build-static
  % ../configure --static --prefix=$BITS/stowdir/qemu-2.1.0-static

This failed: ``ERROR: zlib check failed``.

Needed to install zlib (build dir doesn't work)::

  % wget http://zlib.net/zlib-1.2.8.tar.gz
  % tar xzf zlib-1.2.8.tar.gz
  % cd zlib-1.2.8
  % ./configure --prefix=$BITS/stowdir/zlib-1.2.8
  % make
  % make install

Now qemu configure works::

  % LDFLAGS="-L$BITS/stowdir/zlib-1.2.8/lib" CFLAGS="-I$BITS/stowdir/zlib-1.2.8/include" ../configure --static --prefix=$BITS/stowdir/qemu-2.1.0-static
  % make

This failed when trying to link something: ``usr/bin/ld: cannot find
-lgthrad-2.0``. This ``libgthread-2.0.so`` was definitely installed and it
was in package ``glib2-devel``::

  % repoquery -l glib2-devel | grep libgthread

So digging further in make (``-n`` causes dry run and actually shows the
commands)::

  % make -n

A useful trick turned out to be was adding ``--verbose`` to the command
that failed and go deep down to where is it looking for the libraries.
Turned out that ``ld`` was looking for ``libgthread-2.0.a``, not ``.so``,
because we're statically compiling. To find how to get the ``.a``
version::

  % yum whatprovides */libgthread-2.0.a

So I installed ``glib2-static-2.28.8-4.el6.x86_64``. It built fine after
this::

  % make
  % make install

Now copy the ``qemu-arm`` binary to the ``chroot``. Note that ``su``
can't access bits, so first have to copy the file to ``/tmp`` then to
``chroot``::

  % cp /work/bits0/bi45/stowdir/qemu-2.1.0-static/bin/qemu-arm /tmp/qemu-arm-static
  % sudo cp /tmp/qemu-arm-static /src/chroot/precise_arm/usr/bin/


--------------------------------------------------------------------------
Compiling 32-bit Python
--------------------------------------------------------------------------

It's not too bad once figuring out which flags to use. Download python
(not pypy) source, untar::

  % mkdir build32
  % cd build32
  % CC="gcc -m32" LDFLAGS="-L/lib32 -L/usr/lib32 -L`pwd`/lib32 -Wl,-rpath,/lib32 -Wl,-rpath,/usr/lib32" ../configure --prefix=$BITS/stowdir/python32-2.7.9
  % make
  % make install

Can check if python is compiled 32- or 64-bit using::

  import sys
  sys.maxint

If it's ``9223372036854775807``, it's 64-bit; if ``2147483647``, it's
32-bit.

``binascii``: ``zlib-devel-1.2.3-29.el6.i686``
``hashlib``:  ``openssl-devel-1.0.1e-30.el6_6.5.i686``

--------------------------------------------------------------------------
uclibc/glibc-based cross-translation
--------------------------------------------------------------------------

Was mostly painless. Need a 32-bit python to do this though (see above). A
couple of issues:

* ``__aeabi_read_tp`` could not be found during linking. This is due to
  some thread-local storage stuff missing on ARM. This is related to
  enabling ``__thread``. This can be disabled on line 240 of
  ``rpython/translator/c/genc.py`` by commenting out
  ``defines['USE___THREAD'] = 1``.
* ``__sync_lock_test_and_set_4`` could not be found during compiling. This
  apparently had to do an older version of GCC. To fix this, use 4.4+.
* ``WIFCONTINUED`` not found during linking. This is apparently due to a
  missing Linux utility (?). This can be disabled in line 1876 of
  ``rpython/rtyper/module/ll_os.py``, but I don't know if this has some
  consequences.

::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../../../vc/hg-misc/pypy-cross/rpython/bin/rpython --platform=brg-arm

--------------------------------------------------------------------------
cross-translation with jit
--------------------------------------------------------------------------

This further requires specifying the jit backend (``--jit-backend=arm``).
This caused two problems. One was related to libffi related stuff. So I
had to compile and install libffi (next section).

The other issue was ``sys/timeb.h`` could not be found. I removed the
requirement from line 30 of ``rpython/rtyper/module/ll_time.py``.

One final issue happens in ``translator/c/gcc/trackgcroot.py`` where it
can't find some sections. Apparently, this is a known issue and
``--gcrootfinder=shadowstack`` needs to be added to the command line.
Overall command line::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python \
    $BITS/vc/hg-misc/pypy-cross/rpython/bin/rpython \
    --platform=brg-arm --jit-backend=arm --gcrootfinder=shadowstack \
    --opt=jit rlispy/interp.py

--------------------------------------------------------------------------
PyPy
--------------------------------------------------------------------------

This fails regarding header file ``wchar.h`` not found. Comment out the
requirement from line 33 of ``rlib/rlocale.py``.

Another failure: ``openssl/ssl.h``, ``openssl/err.h``... could not be
found. Fort this, I disabled unnecessary modules using the flag
``--no-allworkingmodules``. Now it's barebones.

::

  TypeError: an integer is required (pypy/interpreter/error.py:461)
  
  (pdb) p e
  OSError('/tmp/usession-stdlib-2.7.9-130/shared_cache/externmod.so: wrong ELF class: ELFCLASS64',)

Turns out the cross-compile flow also needs to compile stuff natively
using the host gcc. The error deep down turned out to be 32-bit python
couldn't open shared object compiled by default gcc (64-bit). I added a
hack in ``rlib/translator/platform/__init__.py`` in line 344 and 345 and
add ``-m32`` to compilation and load flags to host configuration::

  host.cflags = ( "-m32", ) + host.cflags
  host.link_flags = ( "-m32", ) + host.link_flags

Another error::

  [translation:ERROR] CompilationError: CompilationError(err="""
  [translation:ERROR]     In file included from common_header.h:106,
  [translation:ERROR]                      from data_pypy_goal_targetpypystandalone.c:4:
  [translation:ERROR]     /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/module/operator/tscmp.h:2: warning: type defaults to 'int' in declaration of 'wchar_t'In file included from common_header.h:106,
  [translation:ERROR]                      from data_pypy_interpreter_astcompiler_assemble.c:4:
  [translation:ERROR]     /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/module/operator/tscmp.h:2: warning: type defaults to 'int' in declaration of 'wchar_t'
  [translation:ERROR]
  [translation:ERROR]     In file included from common_header.h:106,
  [translation:ERROR]                      from data_pypy_interpreter_argument.c:4:
  [translation:ERROR]     /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/module/operator/tscmp.h:2: warning: type defaults to 'int' in declaration of 'wchar_t'
  [translation:ERROR]     /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/module/operator/tscmp.h:2: error: expected ';', ',' or ')' before '*' token

This is because of the C type ``wchar_t`` which is supposed to be defined
in ``wchar.h``. I tried fixing the header files to ensure it is defined,
but it didn't really work. I had to resort back to renaming ``wchar_t`` to
``int`` in ``pypy/module/operator/tscmp.h`` and ``tscmp.c``.

During linking, there was an error: ``getloadavg couldn't be found``. This
is apparently a syscall that we don't support. Disable this in line 952 of
``rtyper/module/ll_os.py``. Nope, didn't fix it, had to disable in pypy
(line 1309 of ``pypy/module/posix/interp_posix.py``).

The final issue with translating without jit is missing labels on linking.
This seems to be due to linking with ``-shared`` flag. Just add
``--no-shared`` as a flag to ``rpython``.

After all these, cross-translation with the following command works::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=brg-arm --jit-backend=arm  --opt=2  --no-shared targetpypystandalone.py  --no-allworkingmodules

With jit (minimal PyPy)::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=brg-arm --jit-backend=arm  --opt=jit --gcrootfinder=shadowstack  --no-shared targetpypystandalone.py  --no-allworkingmodules

--------------------------------------------------------------------------
libffi
--------------------------------------------------------------------------

Note: created a ``xcc-root`` directory at
``$BITS/misc/arm-progs/rpython/xcc-root``.

::

  % wget ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz
  % cd libffi-3.2.1
  % mkdir build
  % cd build
  % ../configure --prefix=$BITS/misc/arm-progs/rpython/xcc-root/pkgs/libffi-3.2.1 --host=arm-unknown-linux-uclibcgnueabi
  % cd /work/bits0/bi45/misc/arm-progs/rpython/xcc-root/pkgs/libffi-3.2.1
  % ln -s lib/libffi-3.2.1/include/
  % cd ..
  % stow libffi-3.2.1/

--------------------------------------------------------------------------
Racket stuff
--------------------------------------------------------------------------

For racket, first download the source. The normal compilation fails
because it can't find ``libglib-2.0.0.dylib``.

--------------------------------------------------------------------------
Necessary modules for pypy
--------------------------------------------------------------------------

Turns out disabling all the modules wasn't the best idea because some very
useful python builtin stuff uses some of these modules. Here is an
incomplete list::

  random      -> binascii, time

To enable a module, just use ``--withmod-module`` (etc.
``--withmod-binascii``). To disable a module, use ``--withoutmod-module``.

The list of modules are in ``pypy/config/pypyoption.py``. The way to test
if a module is installed or not seems to be to try importing (e.g.
``>>> import binascii``. Looking at this, ``essential_modules`` and
``default_modules`` seem to be installed with ``--no-allworkingmodules``. 

Problematic libraries::

  zlib: ImportError: Could not find a zlib library
  _minimal_curses: Skipped: no _curses or _minimal_curses module
  _hashlib: Compilation error (need openSSL)
  _ssl: Compilation error (need openSSL)
  zipimport: ImportError: Could not find a zlib library (requires zlib...)
  pyexpat: Compilation error (expat.h no file or directory)
  bz2: Compilation error (bzlib.h no file or directory)
  _locale: Compilation error in final linking due to wcscoll not found.
           Searching for this in the source code reveals it's in _locale
           module

More options enabled:: 

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=brg-arm --jit-backend=arm --opt=jit --gcrootfinder=shadowstack --no-shared targetpypystandalone.py --no-allworkingmodules --translationmodules --withoutmod-zlib --withoutmod-_minimal_curses

Most modules enabled as possible (except the ones above). This takes 4635s
to translate::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=brg-arm --jit-backend=arm --opt=jit --gcrootfinder=shadowstack --no-shared targetpypystandalone.py --allworkingmodules --withoutmod-zlib --withoutmod-_minimal_curses --withoutmod-_hashlib --withoutmod-_ssl --withoutmod-zipimport --withoutmod-pyexpat --withoutmod-bz2 --withoutmod-_locale

--------------------------------------------------------------------------
C Library issues
--------------------------------------------------------------------------

As I also wrote in python benchmarks notes, many applications failed on
trying to open ``/lib/libc.so.6`` because of incorrect ELF file. After
digging up a lot, saw that the call was in ``_rawffi`` module in PyPy to
the ``get_libc()`` function. This internally called ``get_libc_name()``
defined in ``rpython.rlib.clibffi``. This used the ``ctypes`` utility to
find the name of the c library. This means that it would find the native c
library name (``libc.so.6``). To get this working, I hacked this line in
line 291 of ``clibffi.py``::

  libc_name = "libc.so.0"
  #libc_name = ctypes.util.find_library('c')

In addition, this also requires to add ``LD_LIBRARY_PATH`` that points to
the compiler ``lib`` path that has the c library files::

  % LD_LIBRARY_PATH=/research/brg/install/stow-pkgs/x86_64-centos6/pkgs/arm-unknown-linux-uclibcgnueabi/arm-unknown-linux-uclibcgnueabi/sysroot/lib qemu-arm <pypy> ...

--------------------------------------------------------------------------
Floating point stuff in the JIT
--------------------------------------------------------------------------

Even though the cross-compiler and Pydgin has floating point support
disabled, the ARM backend still assumes there is floating point support.
This showed itself with the unimplemented ``vstmdb`` instruction,
triggered by ``_push_all_regs_to_jitframe`` in
``rpython.jit.backend.arm.assembler``. It checks on
``cpu.supports_floats`` flag. Disabled this in line 22 of
``backend.arm.runner``.

Also ``VPUSH`` and ``VPULL`` is being called in ``_build_wb_slowpath``. I
made such calls dependent on ``self.cpu.supports_floats``.



tmp::

  /work/bits0/bi45/vc/git-brg/pydgin-pyxcel/arm/pydgin-arm-nojit -e PYPYLOG=jit,gc:ai_mini-pydgin-arm-omit1-post.pypylog -e PYXCEL_IN_FILE=omit1.in /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-omit1 bm_ai_mini.py | tee ai_mini_pydgin_analysis_omit1_post.out
