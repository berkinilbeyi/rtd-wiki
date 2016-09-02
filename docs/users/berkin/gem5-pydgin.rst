==========================================================================
gem5-pydgin
==========================================================================

--------------------------------------------------------------------------
Compiling and running with ``PydginCPU``
--------------------------------------------------------------------------

This link is useful: http://www.m5sim.org/Adding_a_New_CPU_Model

Debug build:

  % scons -j 8 build/ARM/gem5.debug --project-target=xpydgin CPU_MODELS=AtomicSimpleCPU,O3CPU,TimingSimpleCPU,PydginCPU

Performance build:

  % scons -j 8 build/ARM/gem5.fast --project-target=xpydgin-jit CPU_MODELS=AtomicSimpleCPU,O3CPU,TimingSimpleCPU,PydginCPU


  % ./build/ARM/gem5.debug --debug-flags=SimpleCPU,DrainFetch,Event configs/brg/pyxcel.py -c ../test/hello-arm-nl --cpu-type=atomic


--------------------------------------------------------------------------
pydgin compilation
--------------------------------------------------------------------------

  % /work/bits0/bi45/vc/hg-misc/pypy-upstream/rpython/bin/rpython --opt=jit arm-sim.py --shared

--------------------------------------------------------------------------
takeOverFrom requirements
--------------------------------------------------------------------------

getProcessPtr
setStatus
copyArchRegs
setContextId
setThreadId
getSystemPtr
getCpuPtr
getQuiesceEvent
setStatus

--------------------------------------------------------------------------
prelim results
--------------------------------------------------------------------------

                            libquantum 40
                            420M dyn insts
gem5 atomic only            2m52      2.44MIPS
2M pydgin ~20K gem5 atomic  7.958     53MIPS
pydgin only                 2.116     199MIPS

--------------------------------------------------------------------------
simpoint
--------------------------------------------------------------------------

bbv generation: (10 M inst quantum)

../build/ARM/gem5.fast --outdir=libquantum-simpoint ../configs/brg/pyxcel.py --simpoint-profile --fastmem -c /work/bits0/bi45/misc/spec/cpu2006/benchspec/CPU2006/462.libquantum/run/run_base_test_arm-newlib-gcc43.0000/libquantum_base.arm-newlib-gcc43 -o " 33 5 "

simpoint generation:

