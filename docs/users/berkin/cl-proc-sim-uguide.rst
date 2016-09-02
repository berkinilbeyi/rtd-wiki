==========================================================================
Running cycle-level model
==========================================================================

These instructions walk through the necessary steps in running the PyMTL
cycle-level model that is used for the XLOOPS project. For any questions,
contact Berkin Ilbeyi (bi45@cornell.edu).

--------------------------------------------------------------------------
Prerequisites
--------------------------------------------------------------------------

The PyMTL cycle level model requires the pkernel and the applications
available in these two repos::

  micro2012/maven-app-misc
  micro2012/maven-sys-pkernel

The cycle-level model assumes the application binaries and pkernel at a
particular locations, that looks like the following::

  vc/
    git-maven/
      maven-app-misc/
      maven-sys-pkernel/
    git-parc/
      pymtl/

I recommend the same directory structure so that you don't have any issues
with running the scripts. It is possible to override these default
directory structure, however it's easier if you don't have to.

For both of the maven-related projects we clone, build, and run the
convert cache script::

  % cd vc/
  % mkdir git-maven
  % cd git-maven/
  % git clone git@github.com:cornell-brg/maven-sys-pkernel.git
  % git clone git@github.com:cornell-brg/maven-app-misc.git
  % cd maven-sys-pkernel
  % mkdir build-maven
  % cd build-maven
  % ../configure --host=maven
  % make
  % ../convert-cache.py
  % cd ../../maven-app-misc
  % mkdir build-maven
  % cd build-maven
  % ../configure --host=maven
  % make
  % ../convert-cache.py

--------------------------------------------------------------------------
PyMTL
--------------------------------------------------------------------------

After these, we need to pull PyMTL, which is in the pymtl repo. Currently,
the cycle-level model is in a separate branch called ``cl-mt`` in the
``pymtl`` repo. We need to clone the ``cl-mt`` branch of the ``pymtl``
repo::

  % cd vc/
  % mkdir git-parc
  % cd git-parc/
  % git clone -b cl-mt git@github.com:cornell-brg/pymtl.git

To be able to run PyMTL, the pymtl directory needs to be added to the
``$PYTHONPATH`` environment variable. You might want to add this to your
``.bashrc``::

  % cd pymtl
  % export PYTHONPATH=`pwd`:$PYTHONPATH
  % cd cl

All of the cycle-level related stuff are in the ``cl/`` directory in the
pymtl project. In the ``cl/`` directory, we can run the simulation in
isolation like the following::

  % ./cl-proc-sim --stats --num-lanes 4 --share-fus --enable-assert ubmark-vvadd --impl tloops --verify

This runs and verifies tloops version of vector-vector add that we just
compiled on a processor model with 4 tloops lanes with 1 data cache bank,
shared long-latency functional units. To see all of the options, you can
run::

  % ./cl-proc-sim --help

Note that if you didn't use the same folder structure, then you need to
tell the simulator which directory to look for for apps and pkernel. By
default, relative to the directory of cl-proc-sim, it expects the maven
directory to be at ``../../../git-maven``. If you have cloned pkernel and
apps to ``~/foo/bar/maven-sys-pkernel`` and ``~/foo/bar/maven-app-misc``,
you need to add the following flag to ``cl-proc-sim``: ``--maven-dir
~/foo/bar``. You will need to change the scripts as well to pick up the
correct maven directory.

--------------------------------------------------------------------------
Stats
--------------------------------------------------------------------------

The typical output of ``cl-proc-sim`` with stats enabled might something
like::

  ...
  /home/graduate/bi45/vc/git-parc/pymtl/new_pymtl/SimulationTool.py:440: Warning: Cannot add variable 'REFILL' to sensitivity list.
    "".format( name ), Warning )
  /home/graduate/bi45/vc/git-parc/pymtl/new_pymtl/SimulationTool.py:440: Warning: Cannot add variable 'REFILL_WAIT' to sensitivity list.
    "".format( name ), Warning )
  Unknown opcode encountered! 0x481d1008
  Unknown opcode encountered! 0xd0400001
  Unknown opcode encountered! 0x481ce008
  Unsupported SYSCALL: 5
  Unsupported SYSCALL: 5
  Unsupported SYSCALL: 5
  SYSCALL_exit
  status: 0
  Status message received 0
  num_cycles          = 60328
  num_insts           = 47155
  sim_cycles          = 261001
  elapsed_time        = 40.7136819363
  sim_cycles_per_sec  = 6410.64594474
  stats.core0.branch_res = 7012
  stats.core0.fu_use_muldiv = 0

  stats.core0.no_inst = 0
  stats.core0.num_cycles = 60328
  stats.core0.num_insts = 47155
  stats.core0.stall = 6161
  stats.core0.stall_amo = 0
  stats.core0.stall_dmem_load_full = 0
  stats.core0.stall_dmem_store_full = 27
  stats.core0.stall_dx_to_w_full = 11
  stats.core0.stall_raw = 6123
  stats.core0.stall_raw_fu = 0
  stats.core0.stall_raw_ld = 6123
  stats.core0.stall_waw = 0

  stats.dcache0.hits = 9262
  stats.dcache0.misses = 2

  stats.icache0.hits = 54165
  stats.icache0.misses = 2

It is normal to see the warnings and errors as above. The stats are
reported starting with the line ``num_cycles = ...``. The ``num_cycles``
stat is arguably the most important and shows the total number of cycles
in the timing region. ``num_insts`` similarly shows the _dynamic_
instruction count (on the control processor) in the timing region. The
next three lines are about the simulator itself and not relevant for
application/ microarchitecture performance. After these, there are more
stats with each line starting with ``stats.``. These are hierarchical
stats, broken down by the component, and it is printed deeper down the
hierarchy.  For example, lane 2 on processor 1 would be printed as
``stats.core1.lane2``. Within each leaf component, the breakdown of stats
are similar, and it has num_cycles and num_insts that show the number of
cycles and dynamic instructions respectively. In addition, thee are stats
for the number of cycles stalled represented as ``stall``, and further
broken down as the type of stall, such as stall due to a RAW dependency in
``stall_raw``.

--------------------------------------------------------------------------
Line tracing
--------------------------------------------------------------------------

Another feature of the cycle-level model is to print the line trace, which
can be turned on using the ``-v`` flag. There are two levels of line
tracing.  The first level, turned on using ``-v 1``, displays the
instructions in the pipeline and the messages in the memory system. The
second level, turned on using ``-v 2`` displays the actual variables read
and written in addition to first level line tracing.
