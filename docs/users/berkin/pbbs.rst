==========================================================================
Notes on PBBS
==========================================================================

--------------------------------------------------------------------------
Compiling natively
--------------------------------------------------------------------------

Compiling on Mac doesn't seem to work (with the default LLVM compiler,
didn't try gcc), so I have focused on the brg-0X machines.

Top level contains some scripts to make things, such as makeAll,
makeRelease, runall and clean. To make everything, just run::

  % ./makeAll

Out of the box, this fails in suffixArray, where
suffixArray/sequenceData/data makefile cannot file the data dir. Needed to
change line 13 of Makefile to following::

  % cp ../../../testData/data/$@ .

Note that makeAll actually deletes the binaries, so to run things, you
actually need to go to the benchmark, then implementation and call make.
To run them, it seems the general syntax is ``./bnchmrk -r nrounds -o out
in``, but I think all of the benchmarks have testInputs script to run
bunch of different experiments::

  % cd suffixArray/serialKS
  % make
  % ./testInputs

--------------------------------------------------------------------------
Intel Compiler
--------------------------------------------------------------------------

I've gotten a non-commercial academic license for the intel compiler and
the registration code is: ``N3S8-3LM2RWVP``. It's very easy to get the
non-commercial license.

To install, after we untar the file, we run ``./install.sh``. We select
``(3), non-root installation``. The rest is straightforward. In my
installation, I chose icc-only installation.

--------------------------------------------------------------------------
Running PBBS on cilk+
--------------------------------------------------------------------------

It seems that parallelDefs file checks for different environment variables
to use various parallel compilations. For Intel's cilk+, it checks for
``MKLROOT``. ``MKLROOT`` can't be empty string, but any other value works.
So, we can compile the benchmark the following way::

  % cd suffixArray/parallelKS
  % MKLROOT="test" make

The compiled binaries check for libclkrts.so.5 so file, and the correct
one is in the composer_xe... dir (not the top level lib/mic)::

  % LD_LIBRARY_PATH=/home/graduate/bi45/install/stow-pkgs/x86_64-centos6/pkgs/icc-2013-sp1/composer_xe_2013_sp1/lib/intel64/ ./testInputs 

--------------------------------------------------------------------------
icc installation notes
--------------------------------------------------------------------------

NOTE: icc doesn't let you install it to multiple places. I doesn't let you
to change the directory if it detects it is installed somewhere. To
prevent this, make sure you run the uninstall script in the composer. Had
to revert from backup so that I could uninstall it.

The rest was straightforward. Here are some instructions on how to use ICC
on the BRG machines:

I installed the Intel compiler (more specifically Intel Composer XE which
includes icc, tbb, cilk+, mkl etc.) on the BRG machines. To start using
it, you can source the setup script::

  % source ${BARE_PKGS_GLOBAL_PREFIX}/intel-composerxe/setup.sh

One good way to see cilk+ in action is to run the PBBS benchmarks. After
you have sourced the above script, you can go to any PBBS benchmark and
compile and run::

  % cd pbbs/benchmarks/comparisonSort/quickSort
  % make
  % ./testInputs

You can see that icpc was used to compile the benchmark. The default build
system of PBBS checks a couple of environment variables to determine which
compiler to build with. For cilk+ in particular, it checks if ${MKLROOT}
is defined. The setup script defines that variable, so we can compile the
benchmark the following way for sequential compilation using g++::

  % make clean
  % MKLROOT="" make
  % ./testInputs

You should be able to see the cilk+ parallel code is a lot faster than the
sequential one. Let me know if you guys have any problems with this
installation.

--------------------------------------------------------------------------
General steps to port the apps
--------------------------------------------------------------------------

We need to fix comment styles etc. In particular we want to add ``//====``
style block indicators. All throughout the process, make sure we run
./testInputs to ensure we haven't broken anything.

The first thing to do is change the ``intT`` and ``uintT`` declarations.
Note we want to replace ``uintT`` first to prevent ``intT`` matching with
``uintT`` as well::

  :%s/uintT/unsigned int/
  :%s/intT/int/

Usually in the descriptions of some obnoxiously short class/variable
names, it will describe what they are. Substitute the short names with a
more descriptive name, following code conventions. For example, ``struct
Qs`` -> ``struct Queues``. Before doing the substitution, search for the
name in the entire directory (including symlinked stuff) as well as the
old name to ensure we don't have name collisions and if we need to change
the name elsewhere.

When renaming things, start with class/struct names, then variable names,
and finally function names.

``using`` is considered harmful. Remove them. Note that since the header
files are symlinked at this point, using a perl script to automatically do
this for us wouldn't work. It's easier to do this one by one in each file.

Start commenting out using in a couple headers, and it will break code. 

--------------------------------------------------------------------------
PBBS Cleaning
--------------------------------------------------------------------------

Issues:

* PBBS uses a lot of ``using namespace`` s, and we should convert them to
  explicit ``namespace::``
* PBBS buildsystem symlinks stuff into local directory. This is not very
  good, and it's even worse because all these symlinks show up as
  untracked files in git
* Some of the stuff are not symlinked. Especially data generation and
  graphData sort of stuff are just replicated in some places.
* The coding and naming conventions are pretty bad. The use a lot of
  camelCase, space/tab intermixing, extremely dense coding style, and
  often poor choice for variable names.


--------------------------------------------------------------------------
Generating small datasets
--------------------------------------------------------------------------

I think most datasets can be generated to be small the following way.
These directions are for delaunay refine, but I think it applies to others
as well. By default, the ``testInputs`` script uses the datasets
``2DinCubeDelaunay_2000000`` and ``2DkuzminDelaunay_2000000``. These are
fairly large datasets. To compile smaller datasets, we need to use
geometryData scripts. These scripts generate the pre-triangulated versions
of these datasets of a given size. For the triangulated versions that
delaunay refine actually uses, it uses the delaunay triangulation
benchmark itself to triangulate these::

  % cd ../geometryData/data
  % make 2DinCube_500
  % make 2DinCubeDelaunay_500

And to run a specific dataset, you can use the following::

  % cd -
  % ./refine ../geometryData/data/2DinCubeDelaunay_500

Note that too small datasets do not finish. By trying out some sizes, it
seems that 5000 manages to finish.

To verify, we need to write the output to a file::

  % ./refine ../geometryData/data/2DinCubeDelaunay_5000 2DinCubeDelaunayRefine_5000
  % ../common/refineCheck ../geometryData/data/2DinCubeDelaunay_5000 2DinCubeDelaunayRefine_5000

This doesn't output anything if it passes verification, otherwise, gives
an error message like the following::

  Delaunay refine check: 4865 skinny triangles

I also wrote a basic python script to find the smallest dataset that
finishes::

  2DkuzminDelaunay_1468
  2DinCubeDelaunay_2566

--------------------------------------------------------------------------
Building with maven cross-compilers
--------------------------------------------------------------------------

I modified ``delaunayRefine/incrementalRefine/parallelDefs`` to allow
compiling with maven-clang or maven-gcc compilers if the environment
variables ``MAVEN_CLANG`` or ``MAVEN_GCC`` is set respectively. Here is an
example::

  % make clean
  % MAVEN_GCC="yes" make
  % maven-isa-run ./refine ../geometryData/data/2DinCubeDelaunay_500

--------------------------------------------------------------------------
Driver
--------------------------------------------------------------------------

At least in the case of ``delaunayRefine``, the driver contains set up
code that should be included in the timing loop. The file I/O that
shouldn't be counted is in ``refineTime.C``. 

--------------------------------------------------------------------------
Porting issues
--------------------------------------------------------------------------

The first issue compiling the app with clang was an error with the
includes::

  /research/brg/install/stow-pkgs/x86_64-centos6/bin/../maven/include/c++/4.4.1/maven/bits/gthr-default.h:40:3: error:
      couldn't allocate output register for constraint '{$2}'
  MAVEN_SYSCALL_ARG0(NUMCORES, numcores, error_flag);
  ^
  /research/brg/install/stow-pkgs/x86_64-centos6/bin/../maven/include/machine/syscall.h:46:5: note: expanded from macro 'MAVEN_SYSCALL_ARG0'
  ( "li $v0, %2; syscall"

After digging down, I figured out that this was a bug in LLVM that seems
to be fixed in the recent release
(http://llvm.org/bugs/show_bug.cgi?id=13795). The issue is when specifying
a register variable to a specific variable and then using it as an
output::

  register int foo asm("v0");
  asm( "li %0, 0" : "=r" (foo) : );

For some reason, it cannot force ``foo`` to be constrained to this
register. A temporary workaround is to use a non-constrained variable and
use that to set value of ``foo``::

  int bar;
  register int foo asm("v0") = bar;
  asm( "li %0, 0" : "=r" (bar) : );

I fixed this issue using such a fix so we should probably correct it to
original once we upgrade our llvm.

To ensure it is correct, I checked the function that calls this macro,
``__bthread_threading`` in ``mriq``, and the dump is as following before
the change::

  00001170 <__bthread_threading>:
      1170:       24020fa0        li      v0,4000
      1174:       0000000c        syscall
      1178:       28420002        slti    v0,v0,2
      117c:       38420001        xori    v0,v0,0x1
      1180:       03e00008        jr      ra


Another issue is doubles. PBBS contains doubles and we want to use floats
instead in our architectures. We need to change these doubles into
floats::

  % cd pbbs-dr/
  % perl -pi -e "s/double/float/g" `find *`

Even after converting all the doubles to floats, there were still some
doubles remaining. The compiler complains about instructions like
``cvt.s.d`` where it tries to use the floating point registers of standard
MIPS as opposed to general purpose registers. It turns out that this was
due to some functions in ``math.h``, such as ``acos``. C/C++ standard
library versions of these math functions overload the operand and return
type to both ``double`` and ``float``, but LLVM was doing an optimization
where it was replacing these with builtin functions, which only uses
``double`` as the argument and return type. The fix turned out to use
remove ``math.h`` import and replace it with ``cmath``, and explicitly use
``std::`` namespace::

  // import <math.h>
  import <cmath>

  // foo = acos( bar );
  foo = std::acos( bar );

Turns out this is due to ``math.h`` explicitly using ``cosf``, ``cos`` etc
variants for different data types as opposed to ``cmath`` achieving the
same using overloading (http://stackoverflow.com/questions/8734230/math-interface-vs-cmath-in-c/8734292#8734292)

Timing related stuff should be commented out...

In addition, I was getting a null-pointer dereferencing in the ISA
simulator. Tracing back to the root cause, it turns out it was due to the
function calls from GCC to LLVM. It was specifically due to a function
call that had a structure argument, and LLVM was expecting the structure
to be expanded into argument registers. On the other hand, GCC was passing
this as a pointer to the structure. The way to fix this is to explicitly
pass this argument as a structure pointer as opposed to structure.


--------------------------------------------------------------------------
Syscalls
--------------------------------------------------------------------------

To support file IO, I have to implement the following syscalls in the
cycle-level simulator::

  4
  5
  8
  2
  9

Note that other apps currently do the ``9`` syscall, and it works fine
without it. Also note that the syscall numbers are defined in xcc the
following file::

  libgloss/maven/machine/syscfg.h

Here are the definitions of each syscall number::

  1  exit
  2  read
  3  write
  4  open
  5  close
  6  link
  7  unlink
  8  lseek
  9  fstat
  10 stat
  11 brk (ctorng's addition)

In addition, there are maven-specific stuff::

  4000 numcores
  4001 sendam
  4002 bthread_once
  4003 bthread_key_create
  4004 bthread_key_delete
  4005 bthread_key_setspecific
  4006 bthread_key_getspecific
  4007 yield


--------------------------------------------------------------------------
Naming
--------------------------------------------------------------------------

Note that each application should start with a name such as ``pbbs-dr``
while the common stuff are located in ``pbbs-common``. In addition, each
file there should start with the subproject name. Here is a quick script
to rename the includes to correct version::

  % perl -pi -e 's/include\s*"blockRadixSort.h"/include "pbbs-common-blockRadixSort.h"/g; s/include\s*"dataGen.h"/include "pbbs-common-dataGen.h"/g; s/include\s*"delaunayDefs.h"/include "pbbs-common-delaunayDefs.h"/g; s/include\s*"deterministicHash.h"/include "pbbs-common-deterministicHash.h"/g; s/include\s*"geometry.h"/include "pbbs-common-geometry.h"/g; s/include\s*"geometryIO.h"/include "pbbs-common-geometryIO.h"/g; s/include\s*"gettime.h"/include "pbbs-common-gettime.h"/g; s/include\s*"graph.h"/include "pbbs-common-graph.h"/g; s/include\s*"graphIO.h"/include "pbbs-common-graphIO.h"/g; s/include\s*"graphUtils.h"/include "pbbs-common-graphUtils.h"/g; s/include\s*"IO.h"/include "pbbs-common-IO.h"/g; s/include\s*"merge.h"/include "pbbs-common-merge.h"/g; s/include\s*"nearestNeighbors.h"/include "pbbs-common-nearestNeighbors.h"/g; s/include\s*"octTree.h"/include "pbbs-common-octTree.h"/g; s/include\s*"parallel.h"/include "pbbs-common-parallel.h"/g; s/include\s*"parseCommandLine.h"/include "pbbs-common-parseCommandLine.h"/g; s/include\s*"quickSort.h"/include "pbbs-common-quickSort.h"/g; s/include\s*"randPerm.h"/include "pbbs-common-randPerm.h"/g; s/include\s*"rangeMin.h"/include "pbbs-common-rangeMin.h"/g; s/include\s*"sampleSort.h"/include "pbbs-common-sampleSort.h"/g; s/include\s*"sequence.h"/include "pbbs-common-sequence.h"/g; s/include\s*"sequenceIO.h"/include "pbbs-common-sequenceIO.h"/g; s/include\s*"serialHash.h"/include "pbbs-common-serialHash.h"/g; s/include\s*"serialSort.h"/include "pbbs-common-serialSort.h"/g; s/include\s*"speculative_for.h"/include "pbbs-common-speculative_for.h"/g; s/include\s*"stlParallelSort.h"/include "pbbs-common-stlParallelSort.h"/g; s/include\s*"topology.h"/include "pbbs-common-topology.h"/g; s/include\s*"transpose.h"/include "pbbs-common-transpose.h"/g; s/include\s*"unionFind.h"/include "pbbs-common-unionFind.h"/g; s/include\s*"utils.h"/include "pbbs-common-utils.h"/g; ' `find *`

To rename the files::

  % mv blockRadixSort.h pbbs-common-blockRadixSort.h; mv dataGen.h pbbs-common-dataGen.h; mv delaunayDefs.h pbbs-common-delaunayDefs.h; mv deterministicHash.h pbbs-common-deterministicHash.h; mv geometry.h pbbs-common-geometry.h; mv geometryIO.h pbbs-common-geometryIO.h; mv gettime.h pbbs-common-gettime.h; mv graph.h pbbs-common-graph.h; mv graphIO.h pbbs-common-graphIO.h; mv graphUtils.h pbbs-common-graphUtils.h; mv IO.h pbbs-common-IO.h; mv merge.h pbbs-common-merge.h; mv nearestNeighbors.h pbbs-common-nearestNeighbors.h; mv octTree.h pbbs-common-octTree.h; mv parallel.h pbbs-common-parallel.h; mv parseCommandLine.h pbbs-common-parseCommandLine.h; mv quickSort.h pbbs-common-quickSort.h; mv randPerm.h pbbs-common-randPerm.h; mv rangeMin.h pbbs-common-rangeMin.h; mv sampleSort.h pbbs-common-sampleSort.h; mv sequence.h pbbs-common-sequence.h; mv sequenceIO.h pbbs-common-sequenceIO.h; mv serialHash.h pbbs-common-serialHash.h; mv serialSort.h pbbs-common-serialSort.h; mv speculative_for.h pbbs-common-speculative_for.h; mv stlParallelSort.h pbbs-common-stlParallelSort.h; mv topology.h pbbs-common-topology.h; mv transpose.h pbbs-common-transpose.h; mv unionFind.h pbbs-common-unionFind.h; mv utils.h pbbs-common-utils.h;

--------------------------------------------------------------------------
Multiple definitions
--------------------------------------------------------------------------

The checker source could both be compiled standalone natively, or could be
linked with the main program. This creates multiple definition issues when
linking. First of all, both of these source files have ``main`` function,
so I modified the native compilation to add ``-DNATIVE_COMPILE`` flag to
``g++``. So we can check for ``NATIVE_COMPILE`` and guard the ``main``
function in the checker not to be included if ``NATIVE_COMPILE`` is not
defined.

The more serious issue was with the other pbbs common headers. When they
are included from both ``.cc`` files, they create duplicate symbols in
both object file, so we cannot link them because of the multiple
definition problem. Searching online suggests there are multiple ways to
fix it. One way is to add ``-Xlinker -zmuldefs`` to the ``LDFLAGS``. This
is not the prettiest solution and might still fail.

Better solutions require changing the header file so that the functions
are local to the object file. One way is to add ``inline`` to the
functions, the other is ``static``. However, turns out that the best way
to do this in C++ is to use unnamed namespaces in these headers. For
example, I had to change ``pbbs-common-IO.h`` the following way::

  // stuff
  namespace benchIO {
  // the following is new
  namespace {

    // stuff

  }
  }

--------------------------------------------------------------------------
Step-by-step guide
--------------------------------------------------------------------------

To illustrate the full porting process, I will walk through the
``maximalMatching`` benchmark. This assumes we have commented out the code
and refactored the necessary parts. We first compile natively and run
``testInputs``::

  % cd maximalMatching/serialMatching
  % make
  % ./testInputs

This tells us the datasets it uses. These take a long time, so we want to
generate smaller datasets::

  % cd ../graphData/data
  % make randLocalGraph_E_5_1000
  % make rMatGraph_E_5_1000
  % make 2Dgrid_E_1000

We want to make sure that these datasets are meaningful so we run them and
verify the output::

  % cd -
  % ./matching -o randLocalGraph_E_5_1000.out randLocalGraph_E_5_1000
  % ./matching -o rMatGraph_E_5_1000.out rMatGraph_E_5_1000
  % ./matching -o 2Dgrid_E_1000.out 2Dgrid_E_1000
  % cd ../common
  % make matchingCheck
  % ./matchingCheck randLocalGraph_E_5_1000 randLocalGraph_E_5_1000.out
  % ./matchingCheck rMatGraph_E_5_1000 rMatGraph_E_5_1000.out
  % ./matchingCheck 2Dgrid_E_1000 2Dgrid_E_1000.out

If the verification passes, it doesn't print out anything. If it failed,
it displays a messages indicating what went wrong. Now that we have
smaller dataset, we can port it over to ``maven-app-misc``.

In the ``maven-app-misc`` project, we create a new subproject called
``pbbs-mm`` and copy ``pbbs-dr.ac``, ``pbbs-dr.mk.in`` and ``pbbs-dr.cc``
to this new directory and rename them accordingly. Within each file, we
replace the references to ``dr`` and ``DR`` to ``mm`` and ``MM``
respectively::

  :%s/dr/mm/gc
  :%s/DR/MM/gc

We want to copy ``matching.C`` in ``serialMatching`` as
``pbbs-mm-scalar.cc`` in ``maven-app-misc``. We want to change the
function signatures to match the style of other apps and create a header
file.

When changing the top level function signature, we want to avoid return
types and have outputs in the argument as pointers if possible. In
addition, PBBS often passes large structures in the argument, however this
creates problems when using GCC/Clang linking. So instead, we should
explicitly use pointers to structures. So in ``matching.C``, the original
function signature changes the following way::

  std::pair<int*, int> maximalMatching(edgeArray<int> edge_array)
                                |
                                V
  void matching_scalar( int *out, int *size, edgeArray<int> *edge_array )

We also want to remove all of the ``using`` statements, create a header
file and change the ``include`` s to include ``pbbs-common-`` prefix for
the common headers.

In the top level C++ source (``pbbs-mm.cc``), we need to incorporate the
functionality of the timing code (originally in ``matchingTime.C``). In
particular, we want to see how input file is loaded and add this code to
``pbbs-mm.cc``. Instead of loading triangles, I had to load the edge
array, and the code I ended up using was::

  edgeArray<int> edge_array = readEdgeArrayFromFile<int>( input_filename );

  // this is the output array big enough for number of edges (nonZeros)
  int maximal_matching[ edge_array.nonZeros ];
  int num_maximal_matching;

And the function signature looked like::

  impl_ptr->func_ptr( maximal_matching,
                      &num_maximal_matching, &edge_array );

And to write the result to file::

  benchIO::writeIntArrayToFile( maximal_matching, num_maximal_matching,
                                output_filename );


Add some checking info

I copied a small and an original data file as following::

  2Dgrid_E_1000           -> pbbs-mm-2dgrid-e-1000.dat
  randLocalGraph_E_5_1000 -> pbbs-mm-randlocalgraph-e-5-1000.dat
  rMatGraph_E_5_1000      -> pbbs-mm-rmatgraph-e-5-1000.dat

Also need to copy the check code to ``maven-app-misc``
(``matchingCheck.C`` to ``pbbs-mm-check.cc``). We need to modify a couple
of things in the checker code. We want to be able to compile the checker
standalone natively, so it would need a main function. We also want to be
able to verify the output directly from the main program, so we want to be
able to link it with ``pbbs-mm.cc``. However, there can only be a single
``main`` function, so we need to add a guard to check for
``NATIVE_COMPILE`` preprocessor definition, which is only defined when
compiling the checker standalone and natively::

  #ifdef NATIVE_COMPILE
  int main( ... ) {
    // stuff
  }
  #endif

In the checker, we also want to change the pass/fail messages consistent
with other apps. You can see ``pbbs-mm-check.cc`` how these messages look
like. By default, the checker doesn't print out anything when the
verification passes, but we want to change that to print ``[ passed ]``
when it passes. Create a header for the checker and make sure you include
this in ``pbbs-mm.cc``.

In the makefile fragment, things should similar to ``pbbs-mm.mk.in``. You
can see that there is a new ``_native_`` list of sources as well and
``pbbs-mm-check.cc`` is under both ``pbbs_mm_srcs`` for maven compilation
and ``pbbs_mm_native_prog_srcs`` for native compilation as the top level
source.


