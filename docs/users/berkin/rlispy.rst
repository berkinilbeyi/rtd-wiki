==========================================================================
Cross-compiling rlispy
==========================================================================

Yum installs (brg-05):
  fakeroot.x86_64 -- for rpython cross-translation (scratchbox2)

General directions are here: http://pypy.readthedocs.org/en/latest/arm.html

Scratchbox2::

  % git clone https://gitorious.org/scratchbox2/scratchbox2.git
  % cd scratchbox2
  % ./autogen.sh
  % make install prefix=$STOW_PKGS_PREFIX/pkgs/scratchbox2

This also requires ``fakeroot`` (yum install) and ``realpath`` (?)::

  % sudo yum install fakeroot.x86_64

--------------------------------------------------------------------------
Running rpython-compiled things on gem5
--------------------------------------------------------------------------

::

  % cd $BITS/misc/gem5/gem5-9703
  % scons build/X86/gem5.opt -j 15
  % ./build/X86/gem5.opt configs/example/se.py -c /work/bits0/bi45/vc/git-brg/lispy/rlispy-nojit-native

This fails because the executable is not compiled with ``--static`` flag.

::

  % cd $BITS/vc/hg-misc/pypy-accel
  % export PYTHONPATH=`pwd`:$PYTHONPATH
  % cd ../../git-brg/lispy/
  % export PYTHONPATH=`pwd`:$PYTHONPATH
  % pypy ../../hg-misc/pypy-accel/rpython/bin/rpython rlispy/interp.py


--------------------------------------------------------------------------
fixing bug
--------------------------------------------------------------------------

::

    File "rpython_jit_metainterp_pyjitpl.c", line 6480, in MIFrame_run_one_step
    File "rpython_jit_metainterp_pyjitpl.c", line 12915, in handler_getarrayitem_vable_r
    File "rpython_jit_metainterp_pyjitpl.c", line 30375, in MIFrame__opimpl_getarrayitem_vable
    File "rpython_jit_metainterp_pyjitpl.c", line 29031, in MIFrame__nonstandard_virtualizable
    File "rpython_jit_metainterp_pyjitpl.c", line 36313, in MetaInterp_replace_box
    File "rpython_jit_metainterp_pyjitpl.c", line 49361, in MIFrame_replace_active_box_in_frame
  Fatal RPython error: AssertionError
  Abort trap: 6

note had to change some stuff in rpython itself


``tak`` is currently having this issue::

    RPython traceback:
    File "rpython_jit_metainterp_warmspot.c", line 129, in ll_portal_runner__Signed_Bool_rlispy_bytecode_By
    File "rlispy_eval.c", line 1266, in portal
    File "rlispy_bytecode.c", line 12323, in CallBCInst_execute
  Fatal RPython error: NotImplementedError
  Abort trap: 6



