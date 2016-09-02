==========================================================================
Pyxcel
==========================================================================

--------------------------------------------------------------------------
Benchmarks
--------------------------------------------------------------------------

bmark
us-ai           -n 20   7.8B
us-django       -n 10   3.4B
us-html5lib     -n 2   38.8B
us-nbody        -n 3    8.1B
us-pickle       -n 16   9.1B
us-regex_effbot -n 20   7.3B
us-regex_v8     -n 10   8.5B
us-richards     -n 200  8.4B
us-spitfire     -n 6    9.0B


us-regex_compile    Python exception
us-rietvelt         uses zlib module
us-spambayes        tries to dynamically load libc.so.0

--------------------------------------------------------------------------
Hooks
--------------------------------------------------------------------------

Current hooks::

  2 - JIT Region begin
  3 - Guard fail (no bridge)
  4 - Guard fail (w/ bridge)
  5 - Load
  6 - Store
  7 - Finish
  8 - Function call



export SB2=/srv/chroot/precise_arm
export SB2OPT="-t ARM"

To translate a simple interpreter::

  % ../../rpython/bin/rpython --platform=arm --opt=2 hellointerp.py

To try::

  % sb2 -t ARM
  [ARM] % ./hellointerp-c

RLisPy w/o JIT::

  % ~/work/vc/hg-misc/pypy/rpython/bin/rpython --platfrom=arm --opt=2 rlispy/interp.py

RLisPy w/ JIT::

  % ~/work/vc/hg-misc/pypy/rpython/bin/rpython --platfrom=arm --jit-backend=arm --opt=jit --gcrootfinder=shadowstack rlispy/interp.py

PyPy w/o JIT::

  % ../../rpython/bin/rpython --platform=arm  --opt=2  targetpypystandalone.py

  [platform:execute] sb2 -t ARM gcc -c -O3 -pthread -fomit-frame-pointer -Wall -Wno-unused /tmp/usession-default-22/platcheck_43.c -o /tmp/usession-default-22/platcheck_43.o
  [translation:info] Error:
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/goal/translate.py", line 284, in main
  [translation:info]     default_goal='compile')
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/driver.py", line 552, in from_targetspec
  [translation:info]     spec = target(driver, args)
  [translation:info]    File "targetpypystandalone.py", line 291, in target
  [translation:info]     return self.get_entry_point(config)
  [translation:info]    File "targetpypystandalone.py", line 303, in get_entry_point
  [translation:info]     space = make_objspace(config)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/tool/option.py", line 35, in make_objspace
  [translation:info]     return Space(config)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/interpreter/baseobjspace.py", line 394, in __init__
  [translation:info]     self.initialize()
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/objspace/std/objspace.py", line 99, in initialize
  [translation:info]     self.make_builtins()
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/interpreter/baseobjspace.py", line 585, in make_builtins
  [translation:info]     self.install_mixedmodule(mixedname, installed_builtin_modules)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/interpreter/baseobjspace.py", line 616, in install_mixedmodule
  [translation:info]     modname = self.setbuiltinmodule(mixedname)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/interpreter/baseobjspace.py", line 462, in setbuiltinmodule
  [translation:info]     mod = Module(self, self.wrap(name))
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/interpreter/mixedmodule.py", line 22, in __init__
  [translation:info]     self.__class__.buildloaders()
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/module/fcntl/__init__.py", line 17, in buildloaders
  [translation:info]     from pypy.module.fcntl import interp_fcntl
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/pypy/module/fcntl/interp_fcntl.py", line 41, in <module>
  [translation:info]     for k, v in platform.configure(CConfig).items():
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/rtyper/tool/rffi_platform.py", line 226, in configure
  [translation:info]     ignore_errors=ignore_errors))
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/rtyper/tool/rffi_platform.py", line 733, in run_example_code
  [translation:info]     output = build_executable_cache(files, eci, ignore_errors=ignore_errors)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/tool/gcc_cache.py", line 28, in build_executable_cache
  [translation:info]     result = platform.execute(platform.compile(c_files, eci))
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/platform/__init__.py", line 53, in compile
  [translation:info]     ofiles = self._compile_o_files(cfiles, eci, standalone)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/platform/__init__.py", line 75, in _compile_o_files
  [translation:info]     ofiles.append(self._compile_c_file(self.cc, cfile, compile_args))
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/platform/posix.py", line 40, in _compile_c_file
  [translation:info]     cwd=str(cfile.dirpath()))
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/platform/arm.py", line 44, in _execute_c_compiler
  [translation:info]     self._handle_error(returncode, stderr, stdout, outname)
  [translation:info]    File "/home/berkin/work/vc/hg-misc/pypy/rpython/translator/platform/__init__.py", line 151, in _handle_error
  [translation:info]     raise CompilationError(stdout, stderr)
  [translation:ERROR] CompilationError: CompilationError(out="""
  [translation:ERROR]     In file included from /usr/include/fcntl.h:34:0,
  [translation:ERROR]                      from /tmp/usession-default-22/platcheck_43.c:79:
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:36:5: error: unknown type name ‘__off64_t’
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:37:5: error: unknown type name ‘__off64_t’
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:39:5: error: unknown type name ‘__pid_t’
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:47:5: error: unknown type name ‘__off64_t’
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:48:5: error: unknown type name ‘__off64_t’
  [translation:ERROR]     /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:49:5: error: unknown type name ‘__pid_t’
  [translation:ERROR]     """)

This was in revision ``75741:80ab83e0a2f3``. Trying the tip. Still the
same problem. Looking at includes, it seems that the root cause seems to
be at including ``fcntl.h``. I tried a simple ``bug.c`` file::

  #include <fcntl.h>

And tried compiling it::

  % gcc -c bug.c
  (works)
  % arm-linux-gnueabi-gcc -c bug.c
  (works)
  % sb2 -t ARM gcc -c bug.c
  In file included from /usr/include/fcntl.h:34:0,
                   from bug.c:3:
  /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:33:5: error: unknown type name ‘__off_t’
  /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:34:5: error: unknown type name ‘__off_t’
  /usr/lib/gcc-cross/arm-linux-gnueabi/4.7/../../../../arm-linux-gnueabi/include/bits/fcntl.h:39:5: error: unknown type name ‘__pid_t’

As a hack I added the following line to
``/usr/arm-linux-gnueabi/include/bits/fcntl.h:29``::

  #include <unistd.h>

I tried minimal pypy::

  % ../../rpython/bin/rpython --platform=arm  --opt=2 targetpypystandalone.py --no-allworkingmodules
 
This seem to translate without issue... Minimal PyPy w/o JIT::

  % ../../rpython/bin/rpython --platform=arm --jit-backend=arm --gcrootfinder=shadowstack --opt=jit targetpypystandalone.py --no-allworkingmodules

