==========================================================================
``jitviewer`` notes
==========================================================================

Some useful notes are here:
https://bitbucket.org/pypy/pypy/wiki/how%20to%20run%20the%20jitviewer%20using%20a%20nightly%20build.
Also Derek has useful notes: http://brg.csl.cornell.edu/wiki/lockhart-2013-06-24#jitviewer

First, need to create a virtual environment with pypy::

  % cd ~/work/venvs
  % virtualenv --python=/opt/local/bin/pypy --no-site-packages pypy-2.2.1
  % . pypy-2.2.1/bin/activate

Note, on Mac, ``virtualenv`` might have to include the version such as
``virtualenv-2.7``.

Clone the repo::

  % cd ~/work/experiment/pypy/
  % hg clone https://bitbucket.org/pypy/jitviewer

Install the requirements::

  % cd jitviewer
  % pip install -r requirements.txt

For Mac, also install ``binutils`` for ``objdump`` (installs under the
name ``gobjdump``)::

  % sudo port install binutils

Download and untar the pypy source::

  % cd ~/work/experiment/pypy
  % wget <pypy src>
  % tar xjf <pypy src>

Add pypy source to ``PYTHONPATH``::

  % cd pypy-2.2.1-src
  % export PYTHONPATH=`pwd`:$PYTHONPATH

Run the trace::

  % cd ~/work/experiment/pypy/test-pypy
  % PYPYLOG=jit-log-opt,jit-backend-counts:test-loop.pypylog2 python test-loop.py
  
Run jitviewer::

  % jitviewer.py -l test-loop.pypylog2

On mac, after these steps, the assembly didn't show up. For that, I had to
create a symlink to ``gobjdump``, which is MacPorts' name for
``objdump``::

  % cd ~/work/venvs/pypy-2.2.1/bin
  % ln -s `which gobjdump` objdump

Even then it didn't show, using the trace+jitviewer appoach, but the
combined command to run both finally showed the disassembly::

  % jitviewer -c test-loop.py


