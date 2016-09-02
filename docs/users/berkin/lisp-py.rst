==========================================================================
lisp interpreter notes
==========================================================================




--------------------------------------------------------------------------
Benchmarking results
--------------------------------------------------------------------------

To run the benchmarks, just pipe the program::

  % pypy lispy.py < benchmarks/sum2.scm
  % scheme < sum2.scm

For ``sum`` kernel, we sum the values from 0 to m, for n times. For m =
10000, n = 10000, here are the results so far::

  ikarus       0.4s
  mit          1m21s
  pypy lispy   6m5s

To make times a little more reasonable, we set m = 1000, n = 10000::

  ikarus        0.01s
  mit           8.5s
  pypy lispy    41.4s
  cpython lispy 5m4s

Working on another kernel now, just does a sum for 10000000::

  mit           8.5s
  pypy rlis.py  55.8s
  lis-nojit-c   5.5s
  lis-jit-c     6.5s
  ikarus        0.1s

Timing again:

  rlis-jit18-c    0.15s
  rlis-nojit18-c  4.6s
  mit             8.3s
  ikarus          0.09s
  pypy rlis.py    1m16s
  cpython rlis.py 13m40s

--------------------------------------------------------------------------
JIT optimizations
--------------------------------------------------------------------------

I first tried having separate functions for each keyword. This is useful
because the tokens are statically linked to a unique, non-changing
function. This gave a very short JIT trace, however, very poor
performance, around 30-10s.

One observation was the high memory usage with this approach. One reason
is the ``TailCallValue`` object, which a new one is created in every
function call. Instead of this, I am now using a global ``TailCallValue``
object, and update its fields. Getting rid of this improved the
performance sligtly.

Another observation was that the trace contained ``call_may_force`` tags,
and only one of the entry bridges were being directly called from the main
loop. This was despite all 10 bridges showing being called 10000000 times.
So it seems that all these different function calls are turned into
interpreted calls, and not part of the trace. Within these interpreted
traces, it eventually went into being traced into entry bridges, but going
in and out of python domain hurt the performance. 

For these eval functions, I used ``@unroll_safe`` annotations, which made
sure these function calls are incorporated into the tracing. The timing is
around 5.5s.

Proper tail recursion (not creating a new env on each function call)
lowers this 4.8s. The way to have a proper tail recursion is to have a
boolean variable ``tail_call``, that is passed to the eval functions. For
calls to ``eval`` (no tail call), ``tail_call`` is reset to False. Only
function calls turn this value to True. The remaining eval functions
simply return this. 

Implemented maps for env, similar to
http://morepypy.blogspot.com/2011/03/controlling-tracing-of-interpreter-with_21.html
This improved performance to 4.2s.

It turns out marking the ``can_enter_jit`` is _extremely_ important.
Otherwise, there tends to be multiple trace snippets connected through
``call_assembler``. I added a ``can_enter_jit`` tag to the ``eval_tuple``
block which does a (tail (maybe not always?)) recursion. After this, this
creates a single trace and timing is down to 1.2s.

After this, could add virtualizable, with performance at 1.1s.

Removing unnecessary list ops -> 0.85s.

After some constant folding on eval_tuple -> 0.7s.

In ``eval_tuple``, delayed the evaluation of exps (function call
arguments) until the type of the function is determined (builtin python
function, user-defined lambda expression etc.). Refactored this eval to
its own function -> 0.15s.

8/27: I implemented bunch of new features and now can run more realistic
programs. This gave a very poor performance. Looking at the traces
revealed that there are a lot bridges that were being created. They were
failing on guards where they were checking the env map against a constant
pointer. This is due to constant folding on the env map when getting a
variable. It's efficient the first time the program is running, but when
the same function is called from outside, it creates a new environment,
hence a new map instance. Actually the contents of the map is identical,
so a global list of maps, and reusing the same instance should fix it.

Implemented memoization for the environments, like the reference
implementation. However, the performance didn't improve by much. Looking
at the traces again, this time the compiled bridge is for the next guard
failure, which checks the outer env. I guess outer env is not the same
because the JIT'ed code is in a let statement inside a function def, so
the outer function env changes.

I removed the constant folding on outer, which improved the timing from
.8s to .4s. It actually improved the sum_simple slightly .17 -> .16.

Removed constant folding from proc. Increased the time sum_simpl slightly
.16 -> .18 but reduced the time for 100-top-it .4 -> .05. For 1000-top-it,
it's .183s (vs ikarus .086). For 10000-top-it, it throws an error saying
"Add doesn't support the given types". Something funky going on with the
env...

--------------------------------------------------------------------------
Issues
--------------------------------------------------------------------------

* need to allow translated testing
* virtualizables might have issues with other code
* currently the environment has a limit of 10 elements, need to figure out
  a way to grow this
* need to add bunch of language features, syntactic sugar, and library
  components to be able to run the benchmark code




