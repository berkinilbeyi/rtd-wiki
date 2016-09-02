==========================================================================
scm apps
==========================================================================

--------- ---- ------------------------------------------------------------
benchmark #it  notes
--------- ---- ------------------------------------------------------------
ack       1?   should work
array1    1?   requires vector stuff
boyer     20   req cond/else, lists etc. but quite large
browse    600  req conversions, type checks. large
cat       1?   req inport, outport
conform   40   req vectors, type convs. large
cpstak    1000 should work
ctak      100  req call-with-current-continuation
deriv     2M   req eq?, map, list
dderiv    2M   req eq?, set-cdr!, list, map
destruc   500  req set-car/cdr, do, cond/else, quotient
diviter   1M   req cddr, null?. should be easy
divrec    1M   req cddr, null?. should be easy
dynamic   20   req many things, would be tough
earley    200  req many things, would be tough
fft       2000 req FLOAT ops, vectors
fib       5    works
fibc      500  req call-with-current-continuation
fibfp     5    req FLOAT ops, should be easy
gcbench   1    req vectors, display stuff. large
gcold     1    req many things, vectors etc
graphs    1    req vector and other stuff. quite large
lattice   1    req letrec, let*, case, might not be too bad
matrix    1    req list, let*, case. large
maze      4000 req cond, set-rec!, vector, other stuff
mazefun   1000 req map, remainder, might not be too bad. large
mbrot     100  req vectors, float ops, exact->inexact. not too bad
nboyer    100  req string, vectors
nqueens   2000 req write, newline. not bad
nucleic   5    req floats, let*, trig, #() syntax, might not be bad
paraffins 1000 req vectors, let*
parsing   1000 req strings, file parsing, let*
perm9     10   req lists, might not be bad
peval     200  req list, let*, bunch of other stuff
pnpoly    100k req vectors, floats, not bad
primes    100k req letrec, modulo, not bad
puzzle    100  req list, vectors, other stuff
ray       5    req floats, vector, display, write etc.
sboyer    100  req string, vectors, bunch of stuff
scheme    20k  req everything, very difficult
simplex   100k req float, vector
slatex    20   req cond, display, char=?, memv, file io, might not be bad
string    1    req string-append, string-length, substring etc, not bad
sum       10k  works
sum1      1    req float, file io, not bad
sumfp     10k  req float, not bad
sumloop   1    should work
tail      1    req file io, not bad
tak       2000 works
takl      300  req null?, not bad
triangl   10   req list, vector, cond
wc        1    req file io, char=? not bad
--------- ---- ------------------------------------------------------------


ack     -- need to impl cond
cpstak  -- doesn't work, returns a lambda expr instead
           had an issue with implied begin statement, fixed
           complains now regarding an attribute not found (a)
sumloop -- returns 0


