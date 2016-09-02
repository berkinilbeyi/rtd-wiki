==========================================================================
Python Benchmarks
==========================================================================

There seems to be two main benchmark suites for Python. The first is the
"Unladen Swallow" family of benchmarks.

- The original Unladen Swallow benchmarks developed by Google are at https://code.google.com/p/unladen-swallow/wiki/Benchmarks
  * Use ``svn checkout http://unladen-swallow.googlecode.com/svn/tests unladen-bmarks`` to pull.
- PyPy flavor of Unladen, with a few additions of their own, used in
  http://speed.pypy.org , available at https://bitbucket.org/pypy/benchmarks/src
- Grand Unified Python Benchmark at http://speed.python.org which is not
  up yet. Benchmarks are at https://hg.python.org/benchmarks/

The other family of benchmarks are Computer Languages Benchmarks Game,
available at https://alioth.debian.org/snapshots.php?group_id=100815

--------------------------------------------------------------------------
Unladen Swallow
--------------------------------------------------------------------------

The following need external libs:

- ``bm_django.py``
- ``bm_html5lib.py``
- ``bm_rietveld.py``: needs django
- ``bm_spambayes.py``: needs spambayes
- ``bm_spitfire.py``: needs spitfire

I skipped ``bm_threading.py`` because it benchmarks threading.

Works: ``ai``, ``bm_mdp``, ``chaos``, ``crypto_pyaes``, ``deltablue``,
``django``, ``eparse``, ``fannkuch``, ``float``, ``go``, ``hexiom2``,
``html5lib``, ``json_bench``, ``meteor-contest``, ``nbody_modified``,
``pidigits``, ``pyflate-fast``, ``raytrace-simple``, ``richards``,
``slowspitfire``, ``spectral-norm``, ``spitfire``, ``spitfire_cstringio``,
``telco``, 

Fails: ``chameleon``: ``'/lib/libc.so.6' is not an ELF executable for
ARM`` and PyPy crashes. Manually tracing back the problem using pdb::

  chameleon/zpt/template:21 from ..template import BaseTemplate
  chameleon/template:8      import shutil
  ...
  lib_pypy/_ctypes/builtin.py:13 _rawffi.get_libc().getaddressindll('memmove')

  % LD_LIBRARY_PATH=/work/bits0/bi45/misc/arm-progs/rpython/xcc-root/lib PYTHONPATH=/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/lib/chameleon/src /research/brg/install/stow-pkgs/x86_64-centos6/bin/qemu-arm /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-full /work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/own/bm_chameleon.py -n 3

- ``bm_chameleon``: ``DLOpenError``
- ``bm_dulwich_log``: ``ImportError: No module named zlib``
- ``bm_icbd``: Uses ``subprocess`` so the kicked off execution doesn't run
  under qemu anymore
- ``bm_krakatau``: ``DLOpenError``
- ``bm_mako``: ``DLOpenError``
- ``cpython_doc``: seems to stall -- the program uses ``subprocess``
  (``poller.poll()``) and tries to do interprocess communication which is not
  available
- ``genshi_text``: ``ImportError: No module named pyexpat``
- ``genshi_xml``: ``ImportError: No module named pyexpat``
- ``pypy_interp``: ``subprocess`` failure
- ``rietveld``: ``ImportError: No module named zlib``
- ``scimark_*``: for some reason, the ``runner.py`` script doesn't attempt
  to run the comparison ``pypy-qemu``.
- ``spambayes``: ``DLOpenError``
- ``sympy_*``: ``DLOpenError``
- ``translate``: only runs the baseline for some reason
- ``twisted_*``: ``DLOpenError``

After addressing the ``DLOpenError``, these all turned into
``MemoryError`` s::

  % LD_LIBRARY_PATH=/research/brg/install/stow-pkgs/x86_64-centos6/pkgs/arm-unknown-linux-uclibcgnueabi/arm-unknown-linux-uclibcgnueabi/sysroot/lib PYTHONPATH=/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/lib/chameleon/src /research/brg/install/stow-pkgs/x86_64-centos6/bin/qemu-arm /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-c /work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/own/bm_chameleon.py -n 1

  Traceback (most recent call last):
    File "app_main.py", line 75, in run_toplevel
    File "/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/own/bm_chameleon.py", line 3, in <module>
      from chameleon import PageTemplate
    File "/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/lib/chameleon/src/chameleon/__init__.py", line 1, in <module>
      from .zpt.template import PageTemplate
    File "/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/lib/chameleon/src/chameleon/zpt/template.py", line 21, in <module>
      from ..template import BaseTemplate
    File "/work/bits0/bi45/misc/pyxcel/benchmarks/pypy-benchmarks/lib/chameleon/src/chameleon/template.py", line 8, in <module>
      import shutil
    File "/work/bits0/bi45/vc/hg-misc/pypy-cross/lib-python/2.7/shutil.py", line 21, in <module>
      from grp import getgrnam
    File "/work/bits0/bi45/vc/hg-misc/pypy-cross/lib_pypy/grp.py", line 9, in <module>
      from ctypes import Structure, c_char_p, c_int, POINTER
    File "/work/bits0/bi45/vc/hg-misc/pypy-cross/lib-python/2.7/ctypes/__init__.py", line 556, in <module>
      _reset_cache()
    File "/work/bits0/bi45/vc/hg-misc/pypy-cross/lib-python/2.7/ctypes/__init__.py", line 280, in _reset_cache
      CFUNCTYPE(c_int)(lambda: None)
    File "/work/bits0/bi45/vc/hg-misc/pypy-cross/lib_pypy/_ctypes/function.py", line 237, in __init__
      ffiargs, ffires, self._flags_)
  MemoryError

After digging deep down, this seems to happen in ``rpython.rlib.clibffi``
line 495. The problematic line is::

  self.ll_argtypes = lltype.malloc(FFITYPE_PP.TO, argnum, flavor='raw',
                                   track_allocation=False)

For some reason, when cross-translated to ARM, this raises a
``MemoryError`` when ``argnum`` is 0. I looked into malloc and tried
different things but none of these fixed this issue. I also looked into
what native execution does, and it doesn't raise ``MemoryError`` when
``argnum`` is 0. I added a hacky logic there to make ``argnum`` 1 if it
was supposed to be 0. This is probably fine because all it will do is to
``malloc`` one additional element, and ``free``-ing should work fine.

After fixing the ``DLOpenError``/``MemoryError`` issue, here are
problematic benchmarks:


- ``bm_chameleon``: works
- ``bm_krakatau``: Missing ``zlib`` (``zlib.decompressobj(-15)`` :
  ``AttributeError: 'NoneType' object has no attribute 'decompressobj'``
- ``bm_mako``: works
- ``spambayes``: ``userhome = pwd.getpwuid(os.getuid()).pw_dir`` :
  ``KeyError: 'getpwuid(): uid not found: 10088'``
- ``sympy_expand``: works
- ``sympy_integrate``: works
- ``sympy_str``: works
- ``sympy_sum``: works
- ``twisted_iteration``: works
- ``twisted_names``: works
- ``twisted_pb``: works
- ``twisted_tcp``: works

Working benchmarks: 34 out of 49.

Cmd::

  % ./runner.py --fast -c "/research/brg/install/stow-pkgs/x86_64-centos6/bin/qemu-arm /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-full" -b <app_name>

  % /work/bits0/bi45/vc/hg-misc/pypy/pypy/goal/pypy-ref runner.py --fast -c "/research/brg/install/stow-pkgs/x86_64-centos6/bin/qemu-arm /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-full" -b ai,bm_mdp,chaos,crypto_pyaes,deltablue,django,eparse,fannkuch,float,go,hexiom2,html5lib,json_bench,meteor-contest,nbody_modified,pidigits,pyflate-fast,raytrace-simple,richards,slowspitfire,spectral-norm,spitfire,spitfire_cstringio,telco,bm_chameleon,bm_mako,sympy_expand,sympy_integrate,sympy_str,sympy_sum,twisted_iteration,twisted_names,twisted_pb,twisted_tcp


--------------------------------------------------------------------------
IPython analysis
--------------------------------------------------------------------------

I've had bringing up ipython notebook + matplotlib + numpy et al on the
servers. PyPy-based venv couldn't install numpy, CPython didn't work
because ``_sqlite3`` module is missing on the CPython on the servers. I'll
rebuild CPython that has it. First install sqlite::

  % wget https://sqlite.org/2015/sqlite-autoconf-3080803.tar.gz
  % tar xzf sqlite-autoconf-3080803.tar.gz
  % cd sqlite-autoconf-3080803
  % mkdir build
  % cd build
  % ../configure --prefix=$BITS/stowdir/sqlite-3.8.8.3
  % make -j 8
  % make install
  % cd $STOW_PKGS_PREFIX/pkgs
  % ln -s $BITS/stowdir/sqlite-3.8.8.3
  % stow sqlite-3.8.8.3

Now rebuild python::

  % cd Python-2.7.9
  % mkdir build
  % cd build
  % ../configure --prefix=$BITS/stowdir/python-2.7.9
  % make -j 16
  % make install

At the end of the build, it report which modules failed to build. If it
doesn't report ``sqlite``, then it's a success. Create a virtual env with
this new python::

  % virtualenv -p $BITS/stowdir/python-2.7.9/bin/python ~/venvs/python2.7.9

Activate and install stuff::

  % . ~/venvs/python2.7.9/bin/activate
  % pip install matplotlib pandas ipython
  % pip install "ipython[notebook]"

Start notebook (without the browser)::

  % ipython notebook --no-browser

In the notebook, these lines are useful::

  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  %matplotlib inline

Something simple::

  ts = pd.Series( [1,3,5,2,3])
  ts.plot()

--------------------------------------------------------------------------
Vim keybindings in IPython notebook
--------------------------------------------------------------------------

This is a pain to set up. There are some useful links, but none of them
worked for me because my IPython is 3.0:

- http://www.borsuk.org/2014/07/20/ipython-notebook-vim-keys/
- https://github.com/ivanov/ipython-vimception/blob/master/README.md
- http://undefd.kaihola.fi/2013/10/25/emacs-keybindings-for-ipython-notebook-and-firefox.html
- http://nbviewer.ipython.org/github/ivanov/scipy2014/blob/master/v%20in%20IPython.ipynb
- https://www.pfenninger.org/posts/ipython-notebook-extensions-to-ease-day-to-day-work/

The bottom line is that IPython Notebook uses a JavaScript library called
CodeMirror, which supports vim keybindings
(http://codemirror.net/demo/vim.html).

The first thing I had to do was to update CodeMirror in IPython::

  % cd ~/venvs/python2.7.9/lib/python2.7/site-packages/IPython/html/static/components
  % mv codemirror codemirror-bak
  % git clone git@github.com:codemirror/CodeMirror.git codemirror

I also had to hack the vim scipt there (``codemirror/keymap/vim.js``) to
comment out loading dependencies::

  62 (function(mod) {
  63   //if (typeof exports == "object" && typeof module == "object") // CommonJS
  64   //  mod(require("../lib/codemirror"), require("../addon/search/searchcursor"), require("../addon/dialog/dialog"), require("../addon/edit/matchbrackets.js"));
  65   //else if (typeof define == "function" && define.amd) // AMD
  66   //  define(["../lib/codemirror", "../addon/search/searchcursor", "../addon/dialog/dialog", "../addon/edit/matchbrackets"], mod);
  67   //else // Plain browser env
  68     mod(CodeMirror);
  69 })(function(CodeMirror) {
  70 ...

After this, it works if you load the script properly. Here's a code
snippet that seems to work if you do in notebook directly.  Note that you
have to use two different ``%%javascript`` prompts::

  %%javascript
  require(["/static/components/codemirror/keymap/vim.js"]);

  %%javascript
  IPython.CodeCell.options_default.cm_config["keyMap"] = "vim";

To get this working automatically, had to wait until the notebook loaded
and had to wait until ``vim.js`` was loaded. This is in
``~/.ipython/profile_default/static/custom/custom.js``::

  $([IPython.events]).on("app_initialized.NotebookApp", function() {
    require(["/static/components/codemirror/keymap/vim.js"],
      function() {
        IPython.CodeCell.options_default.cm_config["keyMap"] = "vim";
      }
    )
  });
