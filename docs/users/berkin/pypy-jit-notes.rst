==========================================================================
PyPy JIT notes
==========================================================================

This shows notes on how to get the JIT out of PyPy programs.

--------------------------------------------------------------------------
Hooks
--------------------------------------------------------------------------

There are three different JIT hooks as described in
http://pypy.readthedocs.org/en/latest/jit-hooks.html .
``set_optimize_hook`` is called when a code block is optimized, and
``set_compile_hook`` is called when that code block is compiled into
machine instructions. I'm not sure if these are called _before_ or _after_
these events. You can provide a function as an argument to these, and the
argument to these functions would be a loopinfo object (some more info on
the source code
https://bitbucket.org/pypy/pypy/src/2eef95188f80711ca41ed621c8ba07c16cfd1750/pypy/module/pypyjit/interp_resop.py?at=default).
The following example prints the (IR) operations within optimized (or
compiled) code::

  import pypyjit

  def optimize_hook( loopinfo ):
    print loopinfo
    print "Operations:"
    for op in loopinfo.operations:
      print op
    print ""

  pypyjit.set_optimize_hook( optimize_hook )

--------------------------------------------------------------------------
Debugger
--------------------------------------------------------------------------

Along with checking the source code (due to lack of documentation),
experimenting with the attributes is useful. You can set up a debugger and
see the available attributes for quick exploration::

  def optimize_hook( loopinfo ):
    import pdb; pdb.set_trace()
    ...

Then in the debugger, we can see the available attributes::

  (Pdb) p dir( loopinfo )

--------------------------------------------------------------------------
Translation
--------------------------------------------------------------------------

To translate pypy on mac (with poor optimization), need to install
``libgc`` (Boehm GC)::

  % sudo port install boehmgc-devel

This would probably fix that issue, but it complained on me saying it
conficts with ``boehmgc``. I couldn't uninstall ``boehmgc`` because
``inkscape`` depended on it.

I then decided to translate pypy wit JIT optimization anyway, which
doesn't need that garbage collector::

  % cd pypy/goal
  % pypy ../../rpython/bin/rpyhton --opt=jit targetpypystandalone.py

Also can specify a different compiler (from default clang on Mac) with
``--cc=gcc-mp-4.7``. This failed after couple hours (with both compilers)::

  Undefined symbols for architecture x86_64:
    "_libintl_bind_textdomain_codeset", referenced from:
    ...
    "_libintl_bindtextdomain", referenced from:
    ...

Turns out this was an issue with the translator not being able to find the
libraries as explained https://trac.macports.org/ticket/34131#no1 and
http://stackoverflow.com/questions/5287050/specifying-installed-native-library-paths-during-pypy-translate
. The solution is to use ``PYPY_LOCALBASE`` environment variable to point
to the library (prefix) directory::

  % PYPY_LOCALBASE=/opt/local pypy ../../rpython/bin/rpython --opt=jit targetpypystandalone.py

--------------------------------------------------------------------------
Example interpreter
--------------------------------------------------------------------------

There is a tutorial online that is extremely useful to implement an
interpreter in RPython and have code JIT-ed and look at this code.
https://bitbucket.org/brownan/pypy-tutorial/src/42135b18f387137aea4048d280357d69b753a633/tutorial.rst?at=default
. To translate these examples, need to use ``rpython`` which does the
translation::

  % pypy ../pypy-hg/rpython/bin/rpython --opt=jit example4.py

And IR info can be generated with ``PYPYLOG`` environment variable::

  % PYPYLOG=jit-log-opt:test.pypylog ./example4-c test.b

One thing I changed was to add ``can_enter_jit``, which is supposed to be
at the end of the user level loop, which was omitted at the examples. The
catch is that ``can_enter_jit`` can appear right before the
``jit_merge_point`` call. However, having a few statements didn't break
anything, and gave rougly the same results. Here are the summary of
results for ``mandel.b``, which prints a mandelbrot fractal image::

  example2 (rpython translated, no jit):              36s
  example4 (w/ jit):                                  13s
  example5 (jit w/ optimizations to the map lookups): 5.5s
  bf-berkin (jit w/ can_enter_jit):                   5.1s

This version seems to identify one fewer loop in my simple ``test.b``, but
the other loops they identify seem to be very similar.

Looking at the IR, there seems to be some sources of inefficiency. We're
looking at a code like ``[>+ >+ <<-]``, which copies the value of a cell
to two other cells. The jit has an entry level code, which figures out all
the pointer values etc. There is a loop in the IR, which uses these
pointers. However, it still loads the values from the memory and writes it
back for every operation. These should be optimizable further by skipping
these intermediate memory operations. Furthermore, the single value
additions and subtractions should be optimized to a value copy.


Another source of inefficiency seems to 

TODO: continue

--------------------------------------------------------------------------
Logging
--------------------------------------------------------------------------

It's possible to print logs other than IR, and it turns out I did not use
the correct dumping settings earlier to view the assembly in jitviewer.
There are different categories of logs, as shown here:
https://ep2013.europython.eu/media/conference/slides/pypy-hands-on.pdf .
These are ``gc-minor``, ``gc-major``, ``jit-log-noopt``, ``jit-log-opt``,
``jit-backend``, ``jit-backend-counts``. To view the assembly and the IR
in the jitviewer, you need to generate the log the following way::

  PYPYLOG=jit-log-opt,jit-backend:vvadd.pypylog pypy vvadd.py
  jitviewer.py -l vvadd.pypylog

Unfortunately, the log itself doesn't do the object dump, but shows
everything in post-assembly encoded version.

It turns out these different options were flags in code marked with
``debug_start`` and ``debug_stop``. For example, this is from
``rpython/jit/backend/x86/assembler.py``::

  from rpython.rlib.debug import debug_start, debug_print, debug_stop

  debug_start("jit-backend-addr")
  debug_print("Loop ... ")
  debug_stop("jit-backend-addr")



sed -n '/^digraph/,/^\}$/p' test.pypylogB1 > test.dot

Here are some useful logs::

  jit-log-opt-loop: the IR of the jitted loops
  jit-backend-counts: the counts of entering various jitted loops
  jit-summary: shows the times and stats for various things about the jit
               (emitted from rpython/jit/metainterp/jitprof.py)
  gc-minor: pretty verbose, but shows the total memory used


--------------------------------------------------------------------------
Testing
--------------------------------------------------------------------------

--------------------------------------------------------------------------
pygame flowgraph viewer
--------------------------------------------------------------------------

PyPy has a flow graph viewer written using PyGame. This seems to be
specifically for the translation, not for JIT IR. I couldn't get pip to
install pygame because of an issue finding the SDL header files, but there
is a port of it on macports. To use it, need to use he macports python,
which is named something like ``python2.7``. You can use the pygame viewer
standalone to inspect a dot file, or alternatively use the interactive
pygame session post-translation using ``--view`` flag to rpython::

  % python2.7 ../pypy-hg/rpython/bin/rpython --view rlis.py

