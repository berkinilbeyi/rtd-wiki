==========================================================================
PyMTL embedding
==========================================================================

--------------------------------------------------------------------------
Embedding pypy
--------------------------------------------------------------------------

There is a website dedicated to embedding pypy in C
(http://doc.pypy.org/en/latest/embedding.html). Apparently, for it to
work, you need to compile pypy with ``--shared`` flag. You can see if it
is enabled in the default pypy installation::

  % pypy --info | grep shared

The default pypy installed on the servers doesn't support it, so I went
ahead to compile pypy from source.

--------------------------------------------------------------------------
Compiling pypy
--------------------------------------------------------------------------

::

  % wget https://bitbucket.org/pypy/pypy/downloads/pypy-2.2.1-src.tar.bz2
  % tar xjf pypy-2.2.1-src.tar.bz2
  % cd pypy-2.2.1-src
  % ./rpython/bin/rpython --opt=jit --shared pypy/goal/targetpypystandalone.py

This draws some mandelbrot fractals in ascii art :)

This unfortunately failed due to a compilation error in ``compile_c``
step::

  [platform:Error] AssertionError: conflicting entries for
  [platform:Error] InsnCall(99, pypy_g_ASTBuilder_handle_expr, {<-32;esp>: '%r12', <-48;esp>: '%rbx', '%r14': None, '%r15': None, '%r13': None, <-24;esp>: '%r13', <-16;esp>: '%r14', <-8;esp>: '%r15', <-40;esp>: '%rbp'}) --- None.gcroots[%r14]:
  [platform:Error] None and '%r14'

To fix this, I tried installing a pre-compiled version of pypy to compile
it, after talking to Derek::

  % wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.2.1-linux_x86_64-portable.tar.bz2
  % tar xjf pypy-2.2.1-linux_x86_64-portable.tar.bz2
  % cd pypy-2.2.1-linux_x86_64-portable/bin
  % ./virtualenv-pypy ~/venvs/pypy2.2.1
  % source ~/venvs/pypy2.2.1/bin/activate

Newer pypy did not help. I'm trying with Derek's version that works
(revision 69762:3f9e48c7b04c). For some reason, I could not clone this on
the servers directly, it might be due to older version of mercurial up
there. Building mercurial itself looked like a pain, so I had to pull this
on my macbook, switch the revision, tar it and upload it::

  % hg clone http://bitbucket.org/pypy/pypy mercurial-pypy
  % cd mercurial-pypy
  % hg up -r 69762:3f9e48c7b04c

This worked. It created pypy-c and libpypy-c.so in the top level. We'll
use virtualenv to create a virtualenv for this pypy::

  % LD_LIBRARY_PATH=/work/bits0/bi45/misc/pypy/mercurial-pypy ./virtualenv-pypy -p ../../mercurial-pypy/pypy-c ~/venvs/pypy69762-shared

In addition, I copied ``libpypy-c.so`` to ``~/venvs/pypy69762-shared/lib`` and
modified ``bin/activate`` script to add the library to
``$LD_LIBRARY_PATH``.

--------------------------------------------------------------------------
New notes
--------------------------------------------------------------------------

It seems that ``virtualenv`` symlinks the library when the interpreter is
``pypy``. This could be bad because the global installation would depend
on personal files. Instead, we should first install ``pypy`` on global
stow.

I also wanted to update the ``pypy`` version to the most recent (2.5.1). I
translated from source::

  % cd pypy-2.5.1-src/pypy/goal
  % pypy ../../rpython/bin/rpython --shared --opt=jit targetpypystandalone.py

To create a clean directory from this, we need to run the ``release``
tool::

  % cd pypy/tool/release
  % ./package.py pypy-2.5.1

Note that ``pypy-2.5.1`` there could be anything. The instructions suggest
to use ``pypy-VER-PLATFORM``. This will create the ``.tar.bz2`` and the
file hierarchy somewhere in ``/tmp``. For me, it created it at
``/tmp/usession-release-2.5.1-2/build``. You can just copy this to the
necessary folder::

  % cp -r /tmp/usession-release-2.5.1-2/build/pypy-nightly \
          $STOW_PKGS_GLOBAL_PREFIX/pkgs/pypy-shared-2.5.1

I did not stow install this yet because I'm not sure if this will work for
everybody.

Now, we need to create a ``virtualenv`` with this::

  % virtualenv -p $STOW_PKGS_GLOBAL_PREFIX/pkgs/pypy-shared-2.5.1/bin/pypy \
                  /research/brg/install/venv-pkgs/pypy2.5.1-shared

You can test that this works::

  % . /research/brg/install/venv-pkgs/pypy2.5.1-shared/bin/activate
  % pypy

With this, we can ``pip install`` PyMTL::

  % pip install git+git://github.com/cornell-brg/pymtl.git

This is the URL formatting that seems to work. Basically this is the HTTPS
URL with ``https://`` replaced with ``git+git://``. Also note that you can
re-run the above command with ``pip install -U`` to update to latest
version of PyMTL.


