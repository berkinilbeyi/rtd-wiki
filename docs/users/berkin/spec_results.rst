==========================================================================
SPEC performance
==========================================================================

============== =================================== ==================== ==================== ==================== ==================== ==================== ====================
benchmark      output                              native               gem5                 qemu                 maven-isa-run        pydgin-nojit-parc    pydgin-jit-parc     
============== =================================== ==================== ==================== ==================== ==================== ==================== ====================
400.perlbench  attrs.out                           0m0.008s             0m9.044s             0m0.240s                                                                           
400.perlbench  gv.out                              0m0.005s             0m5.893s             0m0.189s                                                                           
400.perlbench  makerand.out                        0m0.087s             5m31.569s            0m2.117s                                                                           
400.perlbench  pack.out                            0m0.117s             2m56.615s            0m1.355s                                                                           
400.perlbench  redef.out                           0m0.003s             0m2.126s             0m0.061s                                                                           
400.perlbench  ref.out                             0m0.002s             0m3.092s             0m0.076s                                                                           
400.perlbench  regmesg.out                         0m0.006s             0m5.661s             0m0.114s                                                                           
400.perlbench  test.out                            0m0.830s             No unalloc thd ctx   0m13.241s                                                                          
401.bzip2      dryer.jpg.out                       0m4.469s             190m15.556s          0m19.484s            115m16.544s          9m24.203s            1m18.554s           
401.bzip2      input.program.out                   0m2.988s             112m1.325s           0m13.283s            65m17.692s           5m40.775s            1m46.331s           
403.gcc        cccp.out                            No Output            Unknown Syscall      Internal Error                                                                     
429.mcf        inp.out                             0m3.007s             36m50.822s           0m6.307s             17m55.040s*          1m42.459s            0m7.752s            
445.gobmk      capture.out                         0m0.144s             5m24.088s            0m1.072s             3m8.094s             0m16.250s            0m7.543s            
445.gobmk      connect.out                         0m1.423s             46m54.227s           0m9.837s             26m6.086s            2m19.862s            0m47.256s           
445.gobmk      connect_rot.out                     0m0.043s             1m36.723s            0m0.347s             0m53.413s            0m4.953s             0m5.219s            
445.gobmk      connection.out                      0m4.834s             183m30.351s          0m47.574s            99m12.649s           9m23.428s            2m33.356s           
445.gobmk      connection_rot.out                  0m0.050s             1m48.789s            0m0.604s             0m59.291s            0m5.616s             0m6.894s            
445.gobmk      cutstone.out                        0m0.252s             8m42.871s            0m2.460s             4m41.935s            0m26.574s            0m20.167s           
445.gobmk      dniwog.out                          0m13.615s            540m23.249s          2m19.820s            281m37.539s          26m35.217s           6m26.722s           
456.hmmer      bombesin.out                        0m3.558s             446m12.768s          1m50.677s                                                                          
458.sjeng      test.out                            0m4.693s             189m12.038s          0m44.666s            97m44.649s           9m8.707s             1m21.581s           
462.libquantum test.out                            0m0.044s             4m38.490s            0m0.595s                                                                           
464.h264ref    foreman_test_baseline_encodelog.out 0m16.982s            1275m23.622s         2m39.880s                                                                          
471.omnetpp    omnetpp.log                         0m0.447s             32m33.162s           0m16.074s            29m52.579s           2m59.052s            0m19.107s           
473.astar      lake.out                            0m11.491s            270m40.157s          0m47.759s                                                                          
483.xalancbmk  test.out                            0m0.079s             4m18.180s            0m1.940s                                                                           
============== =================================== ==================== ==================== ==================== ==================== ==================== ====================

--------------------------------------------------------------------------
Pydgin MIPS results
--------------------------------------------------------------------------

============================= =============== ================
benchmark/output              nojit           jit
============================= =============== ================
401.bzip2/dryer.jpg.out       38.2244697934   272.368840198
401.bzip2/input.program.out   36.17852955     115.262018816
429.mcf/inp.out               35.4600371912   454.626654505
445.gobmk/capture.out         35.6915958738   74.0896208591
445.gobmk/connection.out      32.9162066545   120.373861863
445.gobmk/connection_rot.out  31.2808796915   24.8873647396
445.gobmk/connect.out         34.8749628239   101.743218454
445.gobmk/connect_rot.out     31.7704229952   29.4328569638
445.gobmk/cutstone.out        32.7745940871   42.5551861671
445.gobmk/dniwog.out          33.1205229268   136.296169525
458.sjeng/test.out            33.4973779313   223.280720698
471.omnetpp/omnetpp.log       32.0170126473   293.304844002
============================= =============== ================

--------------------------------------------------------------------------
ARM Issues
--------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
400.perlbench
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``test.out`` on gem5 is failing with the following error::

  fatal: Called sys_clone, but no unallocated thread contexts found!
   @ cycle 762843500
  [cloneFunc:build/ARM/sim/syscall_emul.cc, line 849]

Works fine on qemu.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
403.gcc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The native doesn't print out anything to the output file.

gem5 is failing with the following error::

  fatal: syscall gettid (#224) unimplemented.
   @ cycle 18342000
  [unimplementedFunc:build/ARM/sim/syscall_emul.cc, line 83]

qemu is failing with more descriptive error::

  gcc_base.arm-gcc43: internal error: 8
  It is possible that you may be trying to use SPEC's version of gcc
  without first defining the appropriate flags.  Please check the flags
  that are in the config files from recently-published results on your
  platform, and check that you are using an up-to-date compiler.  If
  you still need help, please contact SPEC, reporting your hw/os
  platform, your compiler version, and your compilation flags.
  Contact SPEC at <URL:http://www.spec.org/>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
464.h264ref
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

gem5 is producing slightly different results. But the outputs are close.
So it probably is due to floating point precision? qemu is similarly off
by a small amount.

--------------------------------------------------------------------------
SPEC on PARC
--------------------------------------------------------------------------

Compilation status:

============== =============================================================
benchmark      notes
============== =============================================================
400.perlbench  doesn't compile (can't find ``arpa/inet.h``, ``sys/ioctl.h``
401.bzip2      compiles
403.gcc        doesn't link (undefined reference to ``getpagesize``)
429.mcf        compiles
445.gobmk      compiles
456.hmmer      doesn't compile (``memory.h`` no such file or directory)
458.sjeng      compiles
462.libquantum doesn't compile (``complex.h`` no such file or directory)
464.h264ref    doesn't compile (``memory.h`` no such file or directory)
471.omnetpp    compiles
473.astar      doesn't compile (``memory.h`` no such file or directory)
483.xalancbmk  doesn't compile (``strings.h`` no such file or directory)
============== =============================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
429.mcf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pydgin segfaults after doing most of the work. ``maven-isa-run`` also
fails with the following::

  maven-isa-run: ../appsvr/memory.h:113: void
  Memory::write_mem_uint32(addr_t, uint32_t): Assertion `addr < 0x10000000 && "Address is greater than memory size!"' failed.

So this is likely due to an issue with maven compilation or memory
mapping.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
445.gobmk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``dniwog`` and ``connection`` fail due to an assertion error on Pydgin::

  RPython traceback:
    File "rpython_jit_metainterp_optimizeopt_unroll.c", line 15765, in UnrollOptimizer_jump_to_already_compiled_trace
    File "rpython_jit_metainterp_optimizeopt_unroll.c", line 26820, in UnrollOptimizer__inline_short_preamble
    File "rpython_jit_metainterp_optimizeopt_intbounds.c", line 124, in OptIntBounds_optimize_GUARD_TRUE
    File "rpython_jit_metainterp_optimizeopt_rewrite.c", line 2747, in OptRewrite_optimize_guard
    File "rpython_jit_metainterp_optimizeopt_pure.c", line 1243, in OptPure_optimize_default
    File "rpython_jit_metainterp_optimizeopt_optimizer.c", line 13556, in _emit_operation__rpython_jit_metainterp_optimize
    File "rpython_jit_metainterp_optimizeopt_optimizer.c", line 15150, in Optimizer_store_final_boxes_in_guard
  Fatal RPython error: AssertionError

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
458.sjeng
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Segfaults on Pydgin. Works fine on ``maven-sim-run``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
471.omnetpp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Pydgin, it complains that syscall 7 is not currently implemented, and
later on fails with the following message::

  terminate called after throwing an instance of 'cTerminationException*'
  terminate called recursively

This might be due to syscall 7 not being implemented. Note that it seems
to be doing most of the work.

--------------------------------------------------------------------------
Fixing issues on PARC
--------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
471.omnetpp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To isolate the place the code was failing, I ``grep`` ed for the error
message. I think the error message is a c++ internal message, but I could
fine ``cTerminationException``. There were multiple places it was being
thrown, so I added print statements to find out which one. It didn't
matter much though because even the simples exceptions didn't seem to
work. So I was trying out the native version with no input files, and it
threw exception right away, but this again was not shown properly in the
pydgin version. As an aside, you can modify the source of benchmarks in
the respective ``benchspec/<bench>/build`` directory. You can build it the
following way::

  % specmake build
  
I looked ``maven-isa-sim``, which was correct. So I decided to dump out
the instructions for both simulators::

  % maven-isa-run -d 2 omnetpp > omnet-maven.out
  % pydgin-parc-nojit-debug --debug insts,rf,mem,syscalls omnetpp > omnet-pydgin.out

I was printing out something right before the exception was thrown. I
found this syscall on both simulation dumps (line numbers). Then I could
strip out everything else from line traces but the PCs. I also start
printing things out starting at the line number we determined to match::

  % tail --lines=+520932 omnet-maven.out | sed -e 's/^.*-> ...//g;s/:.*$//g' > omnet-maven-2.out
  % tail --lines=+490663 omnet-pydgin.out | sed -e 's/^.//g;s/^\(.\{5\}\).*$/\1/g' > omnet-pydgin-2.out
  % diff omnet-maven-2.out omnet-pydgin-2.out

Now, I found the location where the apps were diverging. It was trying to
access the address 0x00142118, which was never initialized in the program.
It turned out that this was part of the ``.gcc_except_table`` section,
which wasn't being loaded. To see an address is part of a section
``readelf`` is useful::

  % readelf -a omnetpp
  
Adding this section to the loaded sections solved the problem.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
458.sjeng
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This was due to the application using too large a memory address. The
memory size was configured for ``2**27``, and had to increase this to
``2**28``. Added a ``--debug memcheck`` to check for the memory boundary.
Furthermore, the args were being passed incorrectly and the binary name
was not in args0. 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
429.mcf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another memory issue, had to increase the memory to ``2**29`` bytes. We
need to increase ``maven-isa-run`` as well. 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
445.gobmk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This one is one of the hardest one to debug. The fact that this only in
JIT-ed code made it very difficult to debug. From the error message, it
seemed like this was happening in
``rpython.jit.metainterp.optimizeopt.optimizer.py``
``store_final_boxes_in_guard`` function. There are three different places
the assertion error could originate, so I added my ``debug_print``
statements to figure out which one. It turned out it was the last one,
which said::

  raise AssertionError("uh?")

It's not clear what's going on here, but I think this code is trying to
convert guards that have ints, but should have bools instead, into bool
guards. It's checking the constant value (the guard value) if it's 0 or 1,
and assigns them false or true values. If neither, we get our assertion
error. I added some more print statements, and seemed like the ``BoxInt``
object had the value of ``0xfffff``. I'm not really sure what this means,
but I basically commented out the assertion error being thrown. It seems
to work fine now, but we should revisit to see why this is happening. It
could also be a bug in RPython, so maybe we should file a bug? Or try more
recent version? I mapped this condition to ``GUARD_TRUE``. 

--------------------------------------------------------------------------
Fixing compilation issues on PARC
--------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fixing ``memory.h``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As per an older email thread from Chris, CTorng and Wacek, they had
encountered these issues before. One of the most common of problems was
the missing ``memory.h``, encountered by three benchmarks: ``hmmer``,
``h264ref`` and ``astar``. Looking at ``memory.h`` at ``/usr/include`` on
the BRG Linux machine, it seemed that it was fairly straightforward. I
just copied this to newlib with slight modifications so the contents were
like the following::

  #ifndef _MEMORY_H
  #define _MEMORY_H 1
  
  #include <sys/features.h>
  
  
  #ifndef _STRING_H_
  # include <string.h>
  #endif  /* string.h  */
  
  #endif  /* memory.h  */

Indeed, this fixed the compilation issues with all three benchmarks,
``hmmer``, ``h264ref``, and ``astar``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fixing ``strings.h``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``xalancbmk`` benchmark complains because of the lack of
``strings.h``. Again as per the email thread and `this link`__, it seems
that this is a BSD header file with mostly duplicates of ``string.h``
functions. Furthermore, looking at newlib's ``string.h``, these functions
all seem to be defined there.

__ http://stackoverflow.com/questions/4291149/difference-between-string-h-and-strings-h

I defined a minimal ``strings.h`` which simply includes ``string.h``::

  #ifndef _STRINGS_H_
  #define _STRINGS_H_
   
  #include <string.h>
  
  #endif /* _STRINGS_H_ */

This seemed to have fixed that issue, but now this application is
complaining about a missing ``linux/limits.h``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Upgrading newlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  % cd src/newlib
  % git log .
  % git checkout 049cb526
  % git branch upstream-newlib
  % git checkout upstream-newlib

  % cd $BITS/newlib
  % wget ftp://sourceware.org/pub/newlib/newlib-2.1.0.tar.gz
  % tar xzf newlib-2.1.0.tar.gz
  % cd -
  % rm -rf newlib
  % cp -r $BITS/newlib/newlib-2.1.0/newlib .
  % git add -u newlib
  % git commit

  % git checkout master
  % git merge upstream-newlib

This had two conflicts: ``newlib/libc/machine/configure`` and
``newlib/libc/machine/mips/setjmp.S``. For the first one, just had to run
``autoconf``::

  % cd newlib/libc/machine/
  % autoconf

The other one was simply a disabled macro, so I just commented out.

I tried compiling, but the compilation failed saying there were
conflicting definitions of ``psignal``, where it was defined both in
libiberty ``strsignal.c`` and in newlib. This is apparently due to newlib
(relatively) recently adding ``psignal`` and there is more information
about it `here`__ and `here`__. I ended up commenting out the definition
in libiberty.

__ http://www.mailinglistarchive.com/html/gcc-help@gcc.gnu.org/2011-03/msg00209.html
__ https://sourceware.org/ml/newlib/2011/msg00174.html

After this, the cross-compiler compiled fine. I tried compiling simple
programs, however this failed for multiple reasons. I got an error message
like the following::

  /home/graduate/bi45/install/stow-pkgs/x86_64-centos6/pkgs/maven-sys-xcc-0.0-209-g75c3473-dirty/bin/../lib/gcc/maven/4.4.1/../../../../maven/lib/libc.a(lib_a-__atexit.o): In function `__register_exitproc':
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:77: undefined reference to `__atexit_lock'
  /home/graduate/bi45/install/stow-pkgs/x86_64-centos6/pkgs/maven-sys-xcc-0.0-209-g75c3473-dirty/bin/../lib/gcc/maven/4.4.1/../../../../maven/bin/ld: small-data section exceeds 64KB; lower small-data size limit (see option -G)
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:77: relocation truncated to fit: R_MIPS_GPREL16 against `__atexit_lock'
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:144: undefined reference to `__atexit_lock'
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:144: relocation truncated to fit: R_MIPS_GPREL16 against `__atexit_lock'
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:97: undefined reference to `__atexit_lock'
  /work/bits0/bi45/vc/git-maven/maven-sys-xcc/build-new/src/maven/newlib/libc/stdlib/../../../../../../src/newlib/libc/stdlib/__atexit.c:97: relocation truncated to fit: R_MIPS_GPREL16 against `__atexit_lock'
  collect2: ld returned 1 exit status

The first problem is the relocation issue. `This`__ was the best
explanation on this. The ``__atexit_lock`` variable apparently didn't fit
to the container it was assigned to. The way to fix this problem was to
compile it with ``-G4`` flag. This basically means for any data larger
than 4 bytes, use a larger container. As a hacky solution, I modified
``src/maven/newlib/libc/stdlib/Makefile`` in the build directory and added
``-G4`` to ``CFLAGS``.

__ https://sourceware.org/ml/ecos-discuss/2000-04/msg00214.html

The other issue was that ``__call_atexit`` wasn't found. This isn't (I
think) related to the previous issue. This variable is supposed to be
declared in ``newlib/libc/stdlib/__call_atexit.c``, and used in
``__atexit.c`` (same directory). The definition at ``__call_atexit.c``
looked like this::

  __LOCK_INIT_RECURSIVE(, __atexit_lock);

While ``__atexit.c`` ``extern`` defined it::

  extern _LOCK_ERECURSIVE_T __atexit_lock;

In ``sys/lock.h``, this is how ``__LOCK_INIT_RECURSIVE`` was defined::

  #define __LOCK_INIT_RECURSIVE(class,lock) static _LOCK_RECURSIVE_T lock = 0;

The problem was with the ``static`` declaration of ``__atexit_lock``,
causing ``__atexit.c`` not to find the variable. Hackily, I changed it to
proper global variable in ``__call_atexit.c``::

  _LOCK_RECURSIVE_T __atexit_lock;

After all these, ``xalancbmk`` still didn't link properly, because of
``dup``, ``getcwd``, ``realpath`` calls.

``realpath`` seems pretty much isolated, might be able to bring it without
mucking much with Linux stuff. ``dup`` seems to just map to a syscall, we
can implement this.

gcc likewise fails on link for: ``getpagesize`` ``getcwd``.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After fixes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After these fixes, the following worked:

=========== =======
benchmark   MIPS   
=========== =======
hmmer       480
libquantum  190
h264ref     92
astar       302
=========== =======

``h264ref``: unimplemented syscall 65535 if compiling with the new newlib,
old one works fine. However, this initially didn't work on Pydgin. This was
due to incorrect implementation of ``lseek`` syscall.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gem5
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gem5 used to complain that it couldn't find ``tcmalloc``, which should
give 11% performance boost. I had ``gperftools`` installed on my local
stow, but I had to change the ``Sconscript`` for it to use it (line 856)::

  py_lib_path.append( "/home/graduate/bi45/install/stow-pkgs/x86_64-centos6/lib" )
  
Then compile normally::

  % scons build/MIPS/gem5.fast -j 15

Verify that this works

--------------------------------------------------------------------------
ARM uclibc
--------------------------------------------------------------------------


Compilation status:

============== ========== ========== =======================================
benchmark      compiles   qemu       simit
============== ========== ========== =======================================
400.perlbench  no         yes
401.bzip2      yes
403.gcc        yes
429.mcf        yes
445.gobmk      yes
456.hmmer      yes
458.sjeng      yes
462.libquantum yes
464.h264ref    no
471.omnetpp    yes        yes
473.astar      yes
483.xalancbmk  no
============== ========== ========== =======================================

--------------------------------------------------------------------------
Execution estimation
--------------------------------------------------------------------------

Inputs that don't work::

  401.bzip2: text.html input.source input.combined input.program

The total number of instructions::

  grep -r "Instructions Executed" * | sed -e 's/^.*= //g' | paste -sd+ | bc
  23 455 298 471 383
  23 TInsts

--------------------------------------------------------------------------
ARM newlib
--------------------------------------------------------------------------

============== ========== ========== ========= =============================
benchmark      compiles   qemu       simit     pydgin
============== ========== ========== ========= =============================
400.perlbench  no
401.bzip2      yes        yes                  partial (segfault)
403.gcc        no
429.mcf        yes        yes                  partial (rpythonerr shifter)
445.gobmk      yes        yes                  segfault
456.hmmer      no
458.sjeng      yes        yes                  segfault
462.libquantum yes        yes                  partial (rpythonerr shifter)
464.h264ref    no
471.omnetpp    no
473.astar      no
483.xalancbmk  no
999.specrand   yes        yes                  rpythonerr
============== ========== ========== ========= =============================


bzip2:      works
mcf:        works
gobmk:      works
libquantum: works
sjeng:      works
h264ref:    fails (cannot open Annex B bytestream file "foreman_qcif.264" stat stuff?)
hmmer:      works (same output as everywhere else)
omnetpp:    works (cTermination exception (need to load exception headers))
astar:      works

sjeng: 1m8  (1m21)
gobmk connection: qemu: 49s simit: 2m13s 

::

  grep "^ " astar.pydgin.out | sed -e "s/^ *//g;s/ .*$//g"
  grep "^0x0" astar.ema.out | sed -e "s/^0x0*//g;s/ .*$//g"


/work/bits0/bi45/vc/git-brg/rpython-isa-sim/arm/pydgin-arm-nojit-debug --debug insts,rf,mem,regdump,syscalls specrand_base.arm-newlib-gcc43 32342 24239 | grep "^[0-9]" | sed -e "s/[0-9]\( \|[0-9]\)://g" | less
ema -v specrand_base.arm-newlib-gcc43 32342 24239 2>&1 | grep "^  " | sed -e "s/  .. = 0x//g;s/  / /g" | less
