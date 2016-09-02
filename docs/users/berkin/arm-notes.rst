==========================================================================
ARM notes
==========================================================================

packages installed::

  protobuf-compiler.x86_64 (not very necessary...)
  libtool.x86_64 (required for ArchC (and qemu?))
  glibc-static.x86_64 (required for building certain cross-compile
  toolchains)
  

--------------------------------------------------------------------------
Installing qemu
--------------------------------------------------------------------------

Download and untar::

  % wget http://wiki.qemu-project.org/download/qemu-2.1.0.tar.bz2
  % tar xjf qemu-2.1.0.tar.bz2

Configure::

  % cd qemu-2.1.0
  % mkdir build
  % cd build/
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/qemu-2.1.0

If getting an error message ``error: possibly undefined macro:
AC_PROG_LIBTOOL``, then need to install libtool. Need to do this through
``yum`` though, not like below.

The rest is straightforward. Beware though, compiling takes a while, so
``-j 16`` it::

  % make -j 16
  % make install
  % cd $STOW_PKGS_PREFIX/pkgs
  % stow qemu-2.1.0

Running was very straighforward. This managed to run non-OS as well OS
binaries. Note though, we need to change the ``uname`` string, similar to
what I've done in gem5::

  % qemu-arm hello-arm-baremetal
  % qemu-arm -r "3.12" hello-arm-linux

--------------------------------------------------------------------------
Installing libtool (deprecated)
--------------------------------------------------------------------------

Note: this section is not needed.

Pretty straightforward::

  % wget http://ftp.wayne.edu/gnu/libtool/libtool-2.4.2.tar.gz
  % tar xzf libtool-2.4.2
  % cd libtool-2.4.2
  % mkdir build
  % cd build/
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/libtool-2.4.2
  % make
  % make install

...

--------------------------------------------------------------------------
SPEC benchmarks
--------------------------------------------------------------------------

Cluster has the spec benchmarks, in ``/ufs/cluster/benchmarks``. Copy
these over::

  % scp berkin@cluster.csl.cornell.edu:/ufs/cluster/benchmarks/SPEC2006/install_archives/cpu2006.tar.xz .
  % mkdir cpu2006
  % cd cpu2006
  % tar xf ../cpu2006.tar.xz

After this we need to "install" the benchmarks. Installation is simple,
and it just installs it in the same directory as the default untarred
directory::

  % ./install.sh

To be able to use the benchmarks, you need to source ``shrc``. The
documentation `here`__ is pretty good.

__ http://www.spec.org/cpu2006/Docs/install-guide-unix.html

I used the ``linux64-amd64-gcc43+`` configuration. It should be possible
to add a new configuration for the arm platform relatively easily::

  % cd config/
  % cp Example-linux64-amd64-gcc43+.cfg brg-linux.cfg
  % cd ..

After this building and running a benchmark was pretty easy::

  % runspec --config=brg-linux.cfg --action=build --tune=base bzip2
  % runspec --config=brg-linux.cfg --size=test --noreportable --tune=base bzip2

And to run the benchmarks officially for the entire suite::

  % runspec --config=brg-linux.cfg --tune=base int

To compile spec benchmarks with arm, we need to copy a configuration and
set the compiler accordingly::

  % cd configs/
  % cp Example-linux64-amd64-gcc43+.cfg brg-arm.cfg

In this, we want to change the compilers to respective compilers from
``arm-unknown-linux-gnueabi`` toolchain. We also want to change the
extension, so that we can identify the arm binaries. Also, we need to pass
``-static`` to the linker::

  # berkin:
  ext           = arm-gcc43
  #ext           = gcc43-64bit

  # berkin:
  CC  = /work/bits0/bi45/misc/arm-toolchain/arm-unknown-linux-gnueabi/x-tools/arm-unknown-linux-gnueabi/bin/arm-unknown-linux-gnueabi-gcc
  CXX = /work/bits0/bi45/misc/arm-toolchain/arm-unknown-linux-gnueabi/x-tools/arm-unknown-linux-gnueabi/bin/arm-unknown-linux-gnueabi-g++
  FC  = /work/bits0/bi45/misc/arm-toolchain/arm-unknown-linux-gnueabi/x-tools/arm-unknown-linux-gnueabi/bin/arm-unknown-linux-gnueabi-gfortran
  #CC                 = /usr/bin/gcc
  #CXX                = /usr/bin/g++
  #FC                 = /usr/bin/gfortran

  # berkin: we need to pass -static to the linker for arm
  LDCFLAGS = -static
  LDCXXFLAGS = -static
  LDFFLAGS = -static

We want to build and run the entire suite natively first so that we can
check the command line args etc. (this uses ``test`` size, but larger
sizes should be similar)::

  % runspec --loose --size test --tune base --config brg-linux --iterations=1 int

``470.lbm`` is apparently fairly small so we can try porting it::

  % runspec --loose --size test --tune base --config brg-arm --iterations=1 lbm

This creates ``benchspec/CPU2006/470.lbm``. The executables are in the
``exe/`` directory with the appropriate suffix. To see the running args,
go to the appropriate run::

  % cd benchspec/CPU2006/470.lbm/run/run_base_test_arm-gcc43.0000
  % specinvoke -n
  # specinvoke r6392
  #  Invoked as: specinvoke -n
  # timer ticks over every 1000 ns
  # Use another -n on the command line to see chdir commands and env dump
  # Starting run for copy #0
  ../run_base_test_arm-gcc43.0000/lbm_base.arm-gcc43 20 reference.dat 0 1 100_100_130_cf_a.of > lbm.out 2>> lbm.err

``specinvoke -n`` just does a dry run, so it doesn't actually run it. It
might be a good idea to run this for real on the host to see the expected
outputs. Now, we can try running this on gem5::

  % cd <gem5 dir>
  % mkdir eval
  % cd eval
  % mkdir spec
  % cd spec
  % ln -s /work/bits0/bi45/misc/spec/cpu2006/benchspec/CPU2006/470.lbm/run/run_base_test_arm-gcc43.0000/ 470.lbm
  % ./build/ARM/gem5.opt configs/example/se.py -c eval/spec/470.lbm/lbm_base.arm-gcc43 -o "-h"
  % ./build/ARM/gem5.opt configs/example/se.py -c eval/spec/470.lbm/lbm_base.arm-gcc43 -o "20 reference.dat 0 1 eval/spec/470.lbm/100_100_130_cf_a.of"


To recompile, you can simply use ``--rebuild`` flag in ``specinvoke``::

  % runspec --loose --size test --tune base --config brg-arm-newlib --iterations --rebuild hmmer

If you hack the source for debugging, it will refuse to build unless you
add ``strict_rundir_verify = 0`` in the config file.


--------------------------------------------------------------------------
Gem5
--------------------------------------------------------------------------

Compile gem5 for arm::

  % cd <gem5 dir>
  % scons build/ARM/gem5.opt -j 15

This didn't work. I pulled the latest stable gem5::

  % hg clone http://repo.gem5.org/gem5-stable

This required protoc buffer compiler (protoc)::

  % sudo yum install protobuf-compiler.x86_64

Also needed a new version of swig. Download and untar::

  % cd swig-3.0.2
  % mkdir build
  % cd build
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/swig-3.0.2 --without-pcre

The ``--without-pcre`` flag is required because it otherwise fails to find
PCRE, which is a regular expressions library::

  % make
  % make install
  % cd ~/install/stow-pkgs/x86_64-centos6/pkgs
  % stow swig-3.0.2

After this, I was able to compile gem5. I had to use a newer version on
GCC (4.8.2).

When running it, because it depends on the newer compiler's c++ libraries,
I had to override the ``LD_LIBRARY_PATH``::

  % LD_LIBRARY_PATH="$STOW_PKGS_PREFIX/pkgs/gcc-4.8.2/lib64" ./build/ARM/gem5.opt

This failed with an error message::

  Traceback (most recent call last):
    File "/work/bits0/bi45/misc/gem5/gem5-stable/src/python/importer.py", line 93, in <module>
      sys.meta_path.append(importer)
  TypeError: 'dict' object is not callable
  Segmentation fault

I couldn't get this fixed. I found only this about this problem:
https://www.mail-archive.com/gem5-dev@gem5.org/msg09861.html , which
suggests it might be a python issue. I rolled back multiple times, and the
version that worked was r9703 (ctorng's original port from march 2013)::

  % hg clone -r 9703 http://repo.gem5.org/gem5 gem5-9703
  % cd gem5-9703
  % scons build/ARM/gem5.opt -j 15
  % ./build/ARM/gem5.opt -h

This gem5 couldn't run the non-OS version of the ARM binaries either,
complaining it encountered an unknown syscall. It could run the
linux-compiled ARM binary, but initially failed saying ``FATAL: kernel too
old``. This is because the kernel version reported by the simulator (e.g.
with ``uname -r``) is too old, and the binary rejects to run. This error
is not coming from gem5. The fix is simple, just change the reported Linux
version at line 69 in ``src/arch/arm/linux/process.cc``::

  //strcpy(name->release, "3.0.0");
  strcpy(name->release, "3.10.2");

The exact version doesn't matter as long as newer than the
cross-compiler's Linux version (3.10.2). With this, I could run::

  % ./build/ARM/gem5.opt configs/example/se.py -c /work/bits0/bi45/misc/arm-progs/hello/hello-arm

--------------------------------------------------------------------------
Crosstool-ng
--------------------------------------------------------------------------

Experimenting with crosstool-ng, which is a tool that makes it easy to
create cross-platform toolchains. Download, untar, configure, make. Note
that creating a ``build/`` dir doesn't work::

  % wget http://crosstool-ng.org/download/crosstool-ng/crosstool-ng-1.9.3.tar.bz2
  % tar xjf crosstool-ng-1.9.3.tar.bz2
  % cd crosstool-ng-1.9.3
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/crosstool-ng-1.9.3
  % make
  % make install
  % cd $STOW_PKGS_PREFIX/pkgs/
  % stow crosstool-ng-1.9.3

Create a new dir and run ``ct-ng`` for a target. For the list of targets,
use::

  % ct-ng list-samples
  % ct-ng arm-unknown-linux-gnueabi

Crosstool-ng doesn't like ``LD_LIBRARY_PATH`` to be set. Unset and run
build::

  % export LD_LIBRARY_PATH=""
  % ct-ng build

This downloaded a bunch of tarballs. However, it failed when it tried to
get ``duma_2_5_15``. I manually downloaded that::

  % cd targets/tarballs
  % wget http://downloads.sourceforge.net/project/duma/duma/2.5.15/duma_2_5_15.tar.gz
  % wget http://downloads.sourceforge.net/project/expat/expat/2.0.1/expat-2.0.1.tar.gz
  % wget http://downloads.sourceforge.net/project/strace/strace/4.5.19/strace-4.5.19.tar.bz2

Actually, cross the top. I used the wrong crosstool version by mistake.
The most recent version is 1.19.0. There are a couple different things
with this new version. After installing the same way, create a target. I
tried ``arm-unknown-eabi`` which uses ``newlib``. Once the stuff is
created, the configuration is in ``.config`` file. I changed a couple
stuff regarding the directories. Most importantly, there was an issue with
mpc not being found (because ``LD_LIBRARY_PATH`` is not allowed). I could
successfully compile the cross compiler by using the
``CT_TARGET_LDFLAGS``. Here are the options I changed in ``.config``::

  CT_LOCAL_TARBALLS_DIR="${CT_TOP_DIR}/tarballs"
  CT_PREFIX_DIR="${CT_TOP_DIR}/x-tools/${CT_TARGET}"

  CT_TARGET_LDFLAGS="-L$STOW_PKGS_PREFIX/lib"

The most successful target has been ``arm-unknown-linux-gnueabi`` so far.
In addition to above changes, this initially failed because it couldn't
find ``gcj`` related stuff on the host machine. This is only necessary if
we want to compile from Java, which we won't do. We need to disable
java-related stuff in the config file::

  CT_CC_SUPPORT_JAVA=n
  CT_CC_LANG_JAVA=n

With this compiler, now we can compile a simple hello world program::

  % arm-unknown-linux-gnueabi-gcc -o hello-arm -static -march=armv5 hello.c

The ``-static`` flag statically links dependent libraries (like the linux
library). ``-march`` specifies the version of the ISA.

I was trying to build ``arm-bare_newlib_cortex_m3_nommu-eabi``, but this
failed because gcc with option ``-lc`` failed when it tried to statically
link the c library (using ``-static`` flag). Had to yum install
``glibc-static.x86_64``.

--------------------------------------------------------------------------
ArchC
--------------------------------------------------------------------------

Instructions from http://www.archc.org/doc.quickstart.html. First need to
install SystemC::

  % wget http://www.accellera.org/downloads/standards/systemc/accept_license/accepted_download/systemc-2.3.0.tgz
  % tar xzf systemc-2.3.0.tgz
  % cd systemc-2.3.0
  % mkdir build
  % cd build/
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/systemc-2.3.0
  % make
  % make install prefix=$STOW_PKGS_PREFIX/pkgs/systemc-2.3.0
  % cd $STOW_PKGS_PREFIX/pkgs
  % stow systemc-2.3.0

Note, I also had to provide the ``prefix`` for ``make install`` as well. 

Install binutils (2.15 as suggested by the documentation had a bug, so I
installed 2.16.1)::

  % wget http://ftp.gnu.org/gnu/binutils/binutils-2.16.1a.tar.bz2
  % tar xjf binutils-2.16.1a.tar.bz2
  % cp binutils-2.16.1
  % mkdir build
  % cd build
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/binutils-2.16.1

Now archc installation. Had to install ``libtool.x86_64``. Download,
untar::

  % cd archc-2.2
  % ./boot.sh

``boot.sh`` generates ``configure`` script. For the configure script, we
need to supply bunch of stuff with ``--with-*`` flags. I did all of these
except for ``gdb``. Note that some say the source, and other the compiled
code. According to their website::

  --with-binutils=<binutils SOURCE>
  --with-gdb=<gdb SOURCE>
  --with-systemc=<systemC BUILD>
  --with-tlm=< /include dir in systemC BUILD>

So I used the following to configure::

  % mkdir build
  % cd build/
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/archc-2.2 --with-binutils=$BITS/misc/binutils/binutils-2.16.1 --with-systemc=$STOW_PKGS_PREFIX/pkgs/systemc-2.3.0 --with-tlm=$STOW_PKGS_PREFIX/pkgs/systemc-2.3.0/include
  % make
  % make install

Now, we can use an architecture description and run a simulation::

  % wget http://downloads.sourceforge.net/project/archc/ARMv5/1.0.1/arm-v1.0.1.tar.bz2
  % tar xjf arm-v1.0.1.tar.bz2
  % cd arm
  % acsim arm.ac -abi
  % make -f Makefile.archc

This will create ``arm.x``, which is the simulator. This requires
``libsystemc-2.3.0.so``, so for the time being, need to also provide a
``LD_LIBRARY_PATH``::

  % LD_LIBRARY_PATH=$STOW_PKGS_PREFIX/pkgs/systemc-2.3.0/lib-linux64 ./arm.x --load=/work/bits0/bi45/misc/arm-progs/hello/hello-armv5-c

However, this failed with error message::

  Warning: A syscall not implemented in this model was called.
          Caller address: 0x80CC
          SWI number: 0x123456    (1193046)
  ArchC Error: Segmentation fault.

--------------------------------------------------------------------------
Running maven apps on ARM
--------------------------------------------------------------------------

With some difficulty, I managed to compile ``maven-apps-misc`` for arm
target, but couldn't figure out how to run these yet (getting an error
message). Make sure you have up-to-date ``maven-app-misc`` and
``maven-sys-common``. You need to modify line 157 of ``aclocal.ac`` of
``maven-sys-common`` to be like the following::

  AS_IF([ test "${build}" != "${host}" && test "${host}" != "arm-unknown-linux-gnueabi" ],

This basically skips the ISA simulator check for the arm target. I already
pushed this change for ``maven-app-misc`` but not for
``maven-sys-common``. You need to compile the common libraries for the arm
target first::

  % autoconf && autoheader
  % mkdir build-arm
  % cd build-arm
  % ../configure --host=arm-unknown-linux-gnueabi
  % make

Instead of installing the libraries, we'll copy them to the build
directory of ``maven-app-misc``. We will configure apps similarly, but we
need to pass additional flags to the linker::

  % cd <maven-app-misc>
  % mkdir build-arm
  % cd build-arm
  % ../configure --host=arm-unknown-linux-gnueabi LDFLAGS="-static -pthread"

We need to copy the libraries::

  % cp <maven-sys-common>/build-arm/lib* .
  % make ubmark-vvadd

We can run the binary with ``qemu``::

  % qemu-arm -r "3.12" ubmark-vvadd

However, I'm currently getting the following error from ``qemu``::

  terminate called after throwing an instance of '__gnu_cxx::__concurrence_broadcast_error'
    what():  __gnu_cxx::__concurrence_broadcast_error
  qemu: uncaught target signal 6 (Aborted) - core dumped
  Aborted

--------------------------------------------------------------------------
Running no-syscall maven apps on ARM
--------------------------------------------------------------------------

This was more successful than running the whole suite. I'm using
no-syscall version of ``ubmark`` s in the ``pymtl`` repo. Make sure you
pull the latest version of this repo because I made some changes to allow
cross-compilation to arm. The first change is to remove the isa simulator
check in the configure script as described above. The second change is to
map the success/failure messages to print statements. So there actually
are syscalls in this version, but should be very minimal. Create a build
directory, and configure::

  % cd pymtl/ubmark
  % mkdir build-arm
  % cd build-arm
  % LDFLAGS="-static" ../configure --host=arm-unknown-linux-gnueabi

As explained earlier, we need to statically link the linux libraries into
the binary. We can just build it now::

  % make ubmark-vvadd

and run::

  % qemu-arm -r "3.12" ubmark-vvadd
  Test passed

dump the assembly::

  % arm-unknown-linux-gnueabi-objdump -dC ubmark-vvadd > ubmark-vvadd.dump

--------------------------------------------------------------------------
SimIt-ARM
--------------------------------------------------------------------------

Download tarballs::

  % wget http://downloads.sourceforge.net/project/simit-arm/simit-arm/release%203.0/SimIt-ARM-3.0.tar.gz
  % wget wget http://downloads.sourceforge.net/project/simit-arm/simit-arm/release%203.0/linux_images.tar.bz2

Not sure if I'll need the linux images, but I downloaded it anyway::

  % tar xzf SimIt-ARM-3.0.tar.gz
  % cd SimIt-ARM-3.0/
  % mkdir build
  % cd build/

Modern compilers seem to detect bunch of weird errors that are hard to
fix. I tried 4.4.7, 4.8.2 and Clang 3.2, and all failed in compilation.
This is probably due to the last version of SimIt being released in 2007.
But ``gcc34`` which is installed on the servers seem to work. Also can add
``--enable-jit`` flag to ``configure`` to enable jit::

  % CC=gcc34 CXX=g++34 ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/SimIt-ARM-3.0
  % make
  % make install

Couldn't get this working so far. When running a hello world program it
hangs. When I run it verbose, I get the following::

  % ema -v hello-armv5-l-c
  Loading .init (24 bytes) at address 0x00008154
  Loading .text (381048 bytes) at address 0x00008170
  Loading __libc_freeres_fn (3304 bytes) at address 0x000651e8
  Loading .fini (20 bytes) at address 0x00065ed0
  Loading .rodata (83328 bytes) at address 0x00065ee8
  Loading __libc_atexit (4 bytes) at address 0x0007a468
  Loading __libc_subfreeres (44 bytes) at address 0x0007a46c
  Loading .ARM.extab (800 bytes) at address 0x0007a498
  Loading .eh_frame (128 bytes) at address 0x0007af30
  Loading .tdata (16 bytes) at address 0x00082fb4
  Loading .tbss (24 bytes) at address 0x00082fc4
  Loading .jcr (4 bytes) at address 0x00082fd0
  Loading .data.rel.ro (44 bytes) at address 0x00082fd4
  Loading .got (112 bytes) at address 0x00083000
  Loading .data (1764 bytes) at address 0x00083070
  Loading .bss (6280 bytes) at address 0x00083758
  Loading __libc_freeres_ptrs (20 bytes) at address 0x00084fe0
  ema: Simulation starts ...
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)
  got a system call (number : 0, name : ?)
  Warning : system call returns an error (number : 0, name : ?)

They have some test binaries (``wc`` and  ``grep``), but even a simplest
``wc`` hangs (complains about unimplemented instructions::

  % echo "test" > test.in
  % ema wc test.in
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  Warning: Unimplemented instruction 0x000080d9:0x0de49d10 ignored.
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  Warning: Unimplemented instruction 0x000080d9:0x0de49d10 ignored.
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  Warning: Unimplemented instruction 0x000080d9:0x0de49d10 ignored.
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  Warning: Unimplemented instruction 0x000080d9:0x0de49d10 ignored.
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  Warning: Unimplemented instruction 0x000080d9:0x0de49d10 ignored.
  Warning: Unimplemented instruction 0x000080c5:0x00e49df0 ignored.
  ...

Same thing for ``grep``, it hangs forever::

  % ema grep "test" test.in
  ema: Simulation starts ...
  Warning: Unimplemented instruction 0xbfffbcf0:0x00010af4 ignored.
  Warning: Unimplemented instruction 0xbfffbcf8:0x00014cb8 ignored.
  Warning: Unimplemented instruction 0xbfffbd04:0x000143fc ignored.
  Warning: Unimplemented instruction 0xbfffbd20:0x000081b4 ignored.
  Warning: Unimplemented instruction 0xbfffbfa8:0x365f3638 ignored.
  Warning: Unimplemented instruction 0xbfffc168:0x73657400 ignored.
  Warning: Unimplemented instruction 0xbfffc174:0x414d006e ignored.
  Warning: Unimplemented instruction 0xbfffc180:0x3d4c4c41 ignored.
  Warning: Unimplemented instruction 0xbfffc184:0x7365722f ignored.
  Warning: Unimplemented instruction 0xbfffc1c8:0x46455250 ignored.
  Warning: Unimplemented instruction 0xbfffc1dc:0x736e692f ignored.
  Warning: Unimplemented instruction 0xbfffc1f8:0x736f746e ignored.
  Warning: Unimplemented instruction 0xbfffc200:0x414e5453 ignored.

However, their full system simulation seems to work fine. You need to get
``linux_images`` package from SimIt website::

  % ema -s linux_images/sa1100/sa1100.cfg
  <boots linux>
  bash-3.2#

You need to use ``poweroff`` command to exit simulation.

When this didn't work, I tried ``simit-arm`` from somebody called
Volodymyr Medvid. They use a CMake-based build system. This initially
didn't work, so I had to install a more recent version of bison::

  % wget http://ftp.gnu.org/gnu/bison/bison-3.0.2.tar.gz
  % tar xzf bison-3.0.2.tar.gz
  % cd bison-3.0.2/
  % mkdir build
  % cd build
  % ../configure --prefix=$STOW_PKGS_PREFIX/pkgs/bison-3.0.2
  % make
  % make install
  % cd $STOW_PKGS_PREFIX/pkgs
  % stow bison-3.0.2

Then clone and build. In CMake, the prefix specification is pretty weird,
you need to use a flag like ``-DCMAKE_INSTALL_PREFIX:PATH=<prefix>``::

  % git clone https://github.com/medvid/simit-arm.git medvid-simit-arm
  % cd medvid-simit-arm
  % cmake -DCMAKE_INSTALL_PREFIX:PATH=$STOW_PKGS_PREFIX/pkgs/SimIt-ARM-medvid ..
  % make
  % make install

This version also kept giving the same errors about unimplemented
instructions. Then I thought it might be because the program was never
tested on a 64-bit machine, and they were probably using generic ``int``
s which are compiled to 64-bit words. So I tried again with the ``-m32``
flag::

  % cd build
  % CFLAGS="-m32" CXXFLAGS="-m32" LDFLAGS="-m32" cmake -DCMAKE_INSTALL_PREFIX:PATH=$STOW_PKGS_PREFIX/pkgs/SimIt-ARM-medvid ..
  % make

This failed somewhere in the linking stage::

  Linking CXX executable ema
  cd /work/bits0/bi45/misc/simit-arm/medvid-simit-arm/build/emulator && /home/graduate/bi45/install/stow-pkgs/x86_64-centos6/pkgs/cmake-2.8.12.2/bin/cmake -E cmake_link_script CMakeFiles/ema.dir/link.txt --verbose=1
  /usr/bin/c++   -m32    -m32 CMakeFiles/ema.dir/main.cpp.o  -o ema -rdynamic libarmemu .a
  libarmemu.a: could not read symbols: File in wrong format
  collect2: ld returned 1 exit status

Looking at detailed logs with ``make VERBOSE=1``, it seemed like one of
the compilation stages did not get the ``-m32`` flag. I re-executed that
with the flag::

  % cd emulator/
  % /usr/bin/c++ -m32 -c -I/work/bits0/bi45/misc/simit-arm/medvid-simit-arm -I/work/bits0/bi45/misc/simit-arm/medvid-simit-arm/emulator -DSIMIT_SYSTEM_LEVEL -o /work/bits0/bi45/misc/simit-arm/medvid-simit-arm/build/emulator/arm_iss_sys.o /work/bits0/bi45/misc/simit-arm/medvid-simit-arm/emulator/arm_iss.cpp
  % cd ..
  % make
  % make install

This worked and I could correctly run their test programs::

  % cd test/
  % ema wc ../README.md

--------------------------------------------------------------------------
Pydgin multiple PyPy versions
--------------------------------------------------------------------------

Ver 2.2 <, indexing with brackets don't work::

  :%s/rf\[\(.*\)\] *= *\(.*\)/rf.__setitem__(\1, \2)/gc
  :%s/rf\[\([^\]]*\)\]/rf.__getitem__(\1)/gc

Needed to do these changes for ``isa.py``, ``syscalls.py``, ``utils.py``.

Version 2.0 complained about file open. Not bothering to fix::

  exe_file = open( filename, 'rb' )

  AttributeError: ("'FrozenDesc' object has no attribute 'rowkey'", <

2.1 has the same issue

--------------------------------------------------------------------------
Using properties
--------------------------------------------------------------------------

To access the instruction fields without function call, I added
``@property`` decorator in ``instruction.py``::

  @property
  def rn( self ):
    return (self.bits >> 16) & 0xF

To change the declarations in ``isa.py``, I used the following regex::

  :%s/inst\.\([^(]*\)()/inst.\1/gc


