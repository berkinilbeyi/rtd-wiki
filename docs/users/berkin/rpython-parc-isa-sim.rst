==========================================================================
rpython isa sim notes
==========================================================================

--------------------------------------------------------------------------
observations
--------------------------------------------------------------------------

- a lot of ir insts! (3360 ops), only a single loop. seems like the
  unrolled loop is correctly jitted
- decoding turns into int_eq(iX, 10) guard .. etc, but within the loop
  portion, it should be more efficient?
- 1848 - 18d4
- Even within the loop, it's still doing a lot of decoding
- There are some non-JITed function calls, which might be difficult for
  the accelerator. By default, the heuristic is to not trace (simply leave
  them as function calls) when the function call contains loops.
  Apparently @unroll_safe can be used to indicate that it is ok to unroll
  and inline the contents of these function calls

--------------------------------------------------------------------------
versions
--------------------------------------------------------------------------

+---+--------------------------------------------------------+--------+
| v | description                                            | time   |
+===+========================================================+========+
| 1 | original, spends a lot of time decoding insts          | ~5s    |
+---+--------------------------------------------------------+--------+
| 2 | marked decode() as an elidable function                | ~5.8s  |
+---+--------------------------------------------------------+--------+
| 3 | 2 + memoization in decode()                            | ~13.6s |
+---+--------------------------------------------------------+--------+
| 4 | 2 + elidable iread()                                   | ~2.4s  |
|   |   skips decoding altogether                            |        |
|   |   each lw: getarrayitem_gc, call( Memory.read ),       |        |
|   |   setarrayitem_gc                                      |        |
+---+--------------------------------------------------------+--------+
| 5 | 4 + unroll_safe for Memory.read, iread, write          | ~1.8s  |
| 6 | 5 + virtualizable for rf (not sure if this is working) | ~1.6s  |
+---+--------------------------------------------------------+--------+
+---+--------------------------------------------------------+--------+
| 2 | word addressable memory                                | 1.1s   |
+---+--------------------------------------------------------+--------+
| 3 | constant fold pc                                       | 1.1s   |
+---+--------------------------------------------------------+--------+
| 4 | virtualizable rf                                       | 0.9s   |
+---+--------------------------------------------------------+--------+
| 9 | constant folding mem                                   | 0.18s  |
+---+--------------------------------------------------------+--------+

--------------------------------------------------------------------------
other optimizations
--------------------------------------------------------------------------

- Use machine word size (64-bit) memory operations (represent data as
  numbers, not characters)

--------------------------------------------------------------------------
ubmark
--------------------------------------------------------------------------

========= ========== ========== ============ ===========
version   vvadd      cmpx-mult  masked-filt  bin-search
insts     239000779  887001237  543800779    641800074
========= ========== ========== ============ ===========
1         1.16       3.41       27.13        13.52
4         0.89       2.58       16.14        12.87
9         0.18       0.50        0.54         0.45
10        0.17       0.47        0.41         0.50
========= ========== ========== ============ ===========

