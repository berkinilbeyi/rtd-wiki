==========================================================================
PyPy on Gem5
==========================================================================

Pull gem5 and build as usual:

.. code-block:: bash

  % hg clone http://repo.gem5.org/gem5 gem5-hg
  % scons build/ARM/gem5.fast

This gives an error:

.. code-block:: bash

  % LD_LIBRARY_PATH=$STOW_PKGS_PREFIX/lib64 ./build/ARM/gem5.fast
  Traceback (most recent call last):
    File "/work/bits0/bi45/misc/gem5/gem5-hg/src/python/importer.py", line
    104, in <module>
      sys.meta_path.append(importer)
  TypeError: 'dict' object is not callable

After looking into why this is happening, turns out this is because of
``scons`` picking up a wrong version of ``Python``. If you look at
``/usr/bin/scons``, it has ``#! /usr/bin/python`` at top. `This link`_ was
very useful to figure this out. The solution is to explicitly use
``Python``:

.. code-block:: bash

  % python /usr/bin/scons build/ARM/gem5.fast -j 8

.. _`This link`: https://www.mail-archive.com/search?l=gem5-dev@gem5.org&q=subject:%22Re%3A+%5Bgem5-dev%5D+gem5+on+redhat6%22&o=newest&f=1

--------------------------------------------------------------------------
``swp`` issue
--------------------------------------------------------------------------

Running RLisPy (with JIT; without JIT works fine) has this issue::

  info: Entering event queue @ 0.  Starting simulation...
  warn: ignoring syscall setrlimit(3, ...)
  warn: ignoring syscall rt_sigaction(32, ...)
  panic: Attempted to execute unimplemented instruction 'swp' (inst 0x3e10a3093)
   @ tick 1185500
   [invoke:build/ARM/arch/arm/faults.cc, line 726]

This turned out to be due to a check in
``src/arch/arm/isa/insts/swap.isa``:

.. code-block:: python

  swpPreAccCode = '''
      if (!((SCTLR)Sctlr).sw) {
          return std::make_shared<UndefinedInstruction>(machInst, false,
                                                        mnemonic);
      }
  '''

  SwapInst('swp', 'Swp', 'EA = Base;',
           swpPreAccCode + 'Mem = cSwap(Op1_uw, ((CPSR)Cpsr).e);',
           'Dest = cSwap((uint32_t)memData, ((CPSR)Cpsr).e);',
           ['Request::MEM_SWAP',
            'ArmISA::TLB::AlignWord',
            'ArmISA::TLB::MustBeOne'],
            ['IsStoreConditional']).emit()

This checks for an object called ``Sctlr``. Looking at
``arm/miscregs.hh``, it seems like ``.sw`` is a flag that enables ``swp``
instruction:

.. code-block:: cpp

  Bitfield<10>   sw;      // SWP/SWPB enable (ARMv7 only)

I tried setting the ``sw`` flag in ``arm/isa.cc``, but didn't work:

.. code-block:: cpp

  sctlr.sw = 1;

I ended up commenting it in ``arm/isa/insts/swap.isa`` which fixed the
issue.

--------------------------------------------------------------------------
Syscall issues
--------------------------------------------------------------------------

This went on further, but failed when the JIT tried to access
``/proc/cpuinfo``::

  rlispy> None
  rlispy> warn: Attempting to open special file: /proc/cpuinfo. Ignoring.  Simulation may take un-expected code path or be non-deterministic until proper  handling is implemented.
  RPython traceback:
    File "rlispy_eval.c", line 534, in portal
    File "rpython_jit_metainterp_warmstate.c", line 352, in maybe_compile_and_run__star_5
    File "rpython_jit_metainterp_warmstate.c", line 604, in bound_reached__star_5
    File "rpython_jit_metainterp_pyjitpl.c", line 1829, in compile_and_run_once___rpython_jit_metainterp_ji
    File "rpython_jit_backend_arm_detect.c", line 685, in detect_arch_version
    File "rpython_rtyper_module_ll_os.c", line 1069, in ll_os_ll_os_open
  ~~~ Crash in JIT! <OSError object at 0x401b3010>
  warn: ignoring syscall kill(100, ...)

This error comes from ``kern/linux/linux.cc``, in ``openSpecialFile``. I
hacked the caller at ``sim/syscall_emul.hh`` to special-case
``/proc/cpuinfo``:

.. code-block:: cpp

  // berkin: rpython wants to read /proc/cpuinfo, let it...
  if ( !startswith(path, "/proc/cpuinfo") &&
      (startswith(path, "/proc/") || startswith(path, "/system/") ||
      startswith(path, "/platform/") || startswith(path, "/sys/"))) {
      // It's a proc/sys entry and requires special handling
      fd = OS::openSpecialFile(path, process, tc);
      local_errno = ENOENT;
  } else {
      // open the file
      fd = open(path.c_str(), hostFlags, mode);
      local_errno = errno;
  }

Another issue::

  rlispy> fatal: syscall cacheflush (#983042) unimplemented.
   @ tick 2741266500
  [unimplementedFunc:build/ARM/sim/syscall_emul.cc, line 91]
  Memory Usage: 776832 KBytes

--------------------------------------------------------------------------
32-bit PyPy
--------------------------------------------------------------------------

I created a 32-bit backend for pypy, which uses 32-bit python to build.
This failed because compiled libffi was 64-bit. Had to compile a 32-bit
libffi::

  % cd libffi-3.2.1
  % mkdir build32
  % cd build32
  % ../configure 

32-bit PyPy needs 32-bit version of ``librt.a`` for static linking. I had
to ``yum install glibc-static.i686`` for this. No-jit minimal::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=host-32bit --opt=jit --no-shared targetpypystandalone.py --no-allworkingmodules

Jit minimal::

  % /work/bits0/bi45/stowdir/python32-2.7.9/bin/python ../../rpython/bin/rpython --platform=host-32bit --opt=jit --no-shared targetpypystandalone.py --no-allworkingmodules

--------------------------------------------------------------------------
PyPy x86 on gem5
--------------------------------------------------------------------------

I had to ignore some syscalls. This still didn't work::

  debug: OperationError:
  debug:  operror-type: MemoryError
  debug:  operror-value:




