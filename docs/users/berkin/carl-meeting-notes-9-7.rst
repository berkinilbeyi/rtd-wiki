==========================================================================
Meeting notes with Carl
==========================================================================

Cache flushes: Carl says cache flushes should be rare (on the order of one
per each trace compilation). This roughly matches what we have observed.
He says cache flushes should be rare for other languages too, which sort
of conflicts with [1], which claims Java benchmarks have cache
invalidations for every 1000 to 10000 instructions.

[1] A. Gutierrez, J. Pusdesris, R. Dreslinski, T. Mudge. Lazy Cache
Invalidation for Self-Modifying Codes. CASES 2012.

We talked about the nature of blackhole execution, which is necessary
because there are multiple side exits from JIT-ed code. The blackhole
interpreter interprets PyPy (double interpreter) to continue execution of
the JIT-ed code (which might be executing code multiple "virtual" frames
deep) until reaching a safe point. At this point, the execution is
represented only with "interpreter frames". Other JIT interpreters usually
(JIT) compile code for all side exits, but this would create a lot of
redundant code that never gets called (most guards don't fail).

Pre-execution to predict the start of blackhole execution: Chris had the
idea to predict (or run-ahead execute) and pre-execute the blackhole on a
second processor. Carl said predicting guard failures would be hard. But a
run-ahead execution might work.

Another idea is to use hardware transactions in the JIT between safe
points. When there is a guard failure that no bridge has been compiled
for, the transaction aborts itself, and falls back to the safe point in
the interpreter. This would get rid of the need for a blackhole
interpreter or JIT side exit code. This would require many stores per
transaction (on the order of 100) which is not feasible with HTM currently
available. This technique would be useful for other tracing JITs too.

We talked about HotSpot JVM and PyPy, and whether there is a fundamental
difference in Python language that prevents it to reach absolute
performance levels of HotSpot. Carl says he doesn't think there is a
reason; given enough development time, PyPy can be as fast as HotSpot.
Dynamic typing in Python should not be an issue; even in Java at the JIT
level, the type information is erased and looks like dynamic typing.
However, Carl says Python is a much bigger language than Java, and it
might not be practical to put in as much development time as HotSpot.

A better way to motivate hardware acceleration of PyPy is that it is not
feasible to put as much engineering effort towards the interpreters of new
languages. Here, hardware can help writing fast interpreters much easier
than software. 

Carl confirmed that there are many calls from JIT to statically compiled
functions, for things such as dictionary lookups. One relatively easy
hardware specialization would be to accelerate these functions. Dictionary
lookups etc. are probably more common than statically compiled code
because dictionaries are well supported at a language level in (R)Python.

Regarding my attempt at implementing hardware watches, Carl had the good
observation that these are similar to quasi-immutables. Quasi-immutable
variables get rid of guards by invalidating compiled traces if they are
changed. They need to use constant addresses, and whenever
quasi-immutables are written over, there is additional code that
invalidates the JIT traces that the quasi-immutables are tied to. My
vision of watches did not require the invalidation of traces, but simply
using a less-optimized version of the trace in case of a watch failure,
and use the more-optimized version back again if watches didn't fail.
Carl raised the observation that an invalidation might be necessary for
watches too when there is a failure.

A "crazy idea" is to have hardware support for meta-information on the
heap, such as types etc. This heap can get rid of certain guards and load
chains by using memoization. 
