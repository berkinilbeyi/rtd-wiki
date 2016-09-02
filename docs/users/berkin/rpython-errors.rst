==========================================================================
rpython errors
==========================================================================

Error::

  object with a __call__ is not RPython

Original code::

  foo = raw_input( prompt )

This is not allowed. Need to use ``os.open`` style files. Even
``sys.stdin`` creates a problem. Seems like ``sys`` library is not
supported at all. Use the following::

  stdin = os.fdopen( 0, "r" )

  line = stdin.readline()
  if len( line ) == 0:
    print "EOF encountered, exiting."
    break

Error::

  method_split() takes 2 arguments (1 given)

Original code::

  "foo bar".split()

Apparently need to provide the seperator in RPython. Providing ``None``
for this argument is identical to the default argument (whitespace
delimiting)::

  "foo bar".splot( None )

Error::

  UnionError:

  Offending annotations:
    SomeList(...
    SomeInteger(...

This is because there is no common type. To fix this, need to do boxing,
i.e., create a top level object and use polymorphism.

Error::

  this calls an _elidable_function_, but this contradicts other sources

Something funky inside an elidable function. In my case, it was because of
a print statement. Can't have print statements inside an elidable
function.

