==========================================================================
SimPoint notes
==========================================================================

Useful links: http://gem5.org/Simpoints and
http://cseweb.ucsd.edu/~calder/simpoint/simpoint-3-0.htm


../build/ARM/gem5.fast --outdir=libquantum-simpoint ../configs/brg/pyxcel.py --simpoint-profile --fastmem -c /work/bits0/bi45/misc/spec/cpu2006/benchspec/CPU2006/462.libquantum/run/run_base_test_arm-newlib-gcc43.0000/libquantum_base.arm-newlib-gcc43 -o " 30 "

note: --simpoint-profile collects simpoint BBV profile, and saves it to
simpoint.bb.gz. This requires the --fastmem argument


get simpoint:

wget http://cseweb.ucsd.edu/~calder/simpoint/releases/SimPoint.3.2.tar.gz

add to CmdLineParser.cpp:
#include <cstring>

add to Utilities.h:
#include <cstdlib>
#include <climits>

add to Datapoint.h:
#include <iostream>

add to FVParser.cpp:
#include <cstring>

make


/work/bits0/bi45/misc/simpoint/SimPoint.3.2/bin/simpoint -loadFVFile simpoint.bb.gz -maxK 30 -saveSimpoints simpoints.out -saveSimpointWeights weights.out -inputVectorsGzipped

