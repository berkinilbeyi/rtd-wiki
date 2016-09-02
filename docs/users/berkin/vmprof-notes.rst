==========================================================================
vmprof notes
==========================================================================

yum packages installed:

  - libunwind                         for vmprof
  - libunwind-devel                   for vmprof
  - libdwarf                          for vmprof on cpython
  - libdwarf-devel                    for vmprof on cpython
  - elfutils-libelf-devel             for vmprof on cpython

Initialize a virtualenv::

  % cd /work/bits1/bi45/vc/hg-misc/pypy-upstream/pypy/goal/
  % virtualenv -p ./pypy-c ~/venvs/pypy-4.0-alpha
  % . ~/venvs/pypy-4.0-alpha/bin/activate

Install pymtl::

  % cd $BITS/vc/git-brg
  % git clone git@github.com/cornell-brg/pymtl.git pymtl-ece4750
  % cd pymtl-ece4750
  % git checkout ece4750
  % pip install --editable .

This works to run the processor::

  % cd $BITS/vc/git-brg/pymtl-research/proc
  % pypy ./research-proc-sim ../../ece4750-labs/apps/ubmark/build-maven/ubmark-cmplx-mult

Can dump pypylog, but doesn't look too useful. Trying vmprof::

  % pip install vmprof

This installed, but running  with vmprof didn't work, complaining about
missing ``libunwind.so``::

  % pypy -m vmprof -o cmplx-mult.out ./research-proc-sim ../../ece4750-labs/apps/ubmark/build-maven/ubmark-cmplx-mult

Searching for the missing package::

  % yum whatprovides */libunwind.so
  % yum list installed | grep libunwind
  % sudo yum install libunwind-devel

The output can be viewed like following::

  % vmprofshow cmplx-mult.out

Get top ones::
 
 % cat vmprof-cmplx-mult.out | sed 's/\x1b\[[0-9;]*m//g' | sort -r -n | head -n 40 > vmprof-cmplx-mult-top40.out
  

--------------------------------------------------------------------------
Installation on CPython
--------------------------------------------------------------------------

There were some errors preventing it to be installed on cpython like
above. The error messages indicated that headers ``dwarf.h`` and
``gelf.h`` couldn't be found. For those, I had to install
``libdwarf-devel`` and ``elfutils-libelf-devel`` respectively.
