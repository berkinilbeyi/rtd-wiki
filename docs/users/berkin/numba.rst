==========================================================================
Numba
==========================================================================

Create a new virtuaenv::

  % virtualenv -p /research/brg/install/venv-pkgs/x86_64-centos6/python2.7.10/bin/python ~/venvs/python2.7.10-numba
  % . ~/venvs/python2.7.10-numba/bin/activate

Numba suggest to install anaconde (which in turn requires ``auxlib``)::

  % pip install auxlib
  % pip install conda

I tried installing ``llvmlite`` using ``pip`` in the default virtualenv,
but it didn't work. I resorted to using ``conda`` instead::

  % conda config --add channels numba 
  % conda create -n numbaenv llvmlite numpy

``conda`` creates a virtual environment (under the original virtual
environment, ``/work/bits1/bi45/misc/numba/venv/envs/numbaenv``), but it's
a bit weird because it symlinks ``activate`` to the original virtual
env's. I had to hack a bit by actually copying ``activate`` script to
``/work/bits1/bi45/misc/numba/venv/envs/numbaenv/bin/`` and change the
path in there to point to ``numbaenv``. Then I could activate and build
numba::

  % . /work/bits1/bi45/misc/numba/venv/envs/numbaenv/bin/activate
  % git clone git@github.com:numba/numba.git
  % cd numba
  # build:
  % python setup.py build_ext --inplace
  # I had to pip install these packages
  % pip install funcsigs singledispatch
  # list tests:
  % python -m numba.runtests -l
  # run tests:
  % python -m numba.runtests -m


