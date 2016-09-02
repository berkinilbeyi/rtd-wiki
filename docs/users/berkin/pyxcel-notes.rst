==========================================================================
Pyxcel notes
==========================================================================

--------------------------------------------------------------------------
Pydgin
--------------------------------------------------------------------------



--------------------------------------------------------------------------
Tasks
--------------------------------------------------------------------------

* Run PyPy on gem5
  - ARM
  - x86
  - Maybe look into upgrading gem5
* Better ARM flow
  - for testing
  - for translation
* ARM performance evaluation on ARM boards
* ARM backend improvements

--------------------------------------------------------------------------
Observations
--------------------------------------------------------------------------

* Some benchmarks seem to have data-parallel loops (e.g. regex stuff) (in
  html5lib). These show up as a single op in the exec slice and everything
  else in the guard slice (since the exit condition is reached on guard
  failure).
* ``guard_nonnull_class`` seems like a good target to specialize
* Need to do something about function calls...
  - Function calls seem to be just functions in the interp that the trace
    skipped over. They are in RPython just like everything else.
  - do function calls modify the object state

--------------------------------------------------------------------------
Research Ideas
--------------------------------------------------------------------------

* JIT-triggered parallelization.
* Instrument how frequent write barriers fail and how large the overhead
  is, and if it touches other stuff
* Offload write buffer handling to another processor. Garbage collection
  has to empty the write buffer handling queue before the collection.
* Trace-caching the JIT trace. Omit certain instructions such as branches
  from here by offloading guards etc.

--------------------------------------------------------------------------
PyPy Ideas
--------------------------------------------------------------------------

* In the register allocator, use the free registers which already have the
value calculated.

Currently looks like this (from ``html5lib``)::

  p13 = getarrayitem_gc(p11, 0, use_e, descr=<ArrayP 4>) an: 4.0
    b0015658:   e3a0a000        mov     sl, #0  ; 0x0
    b001565c:   e1a0c10a        lsl     ip, sl, #2
    b0015660:   e28cc008        add     ip, ip, #8      ; 0x8
    b0015664:   e799a00c        ldr     sl, [r9, ip]
  p15 = getarrayitem_gc(p11, 1, use_e, descr=<ArrayP 4>) an: 4.0
    b0015668:   e3a01001        mov     r1, #1  ; 0x1
    b001566c:   e1a0c101        lsl     ip, r1, #2
    b0015670:   e28cc008        add     ip, ip, #8      ; 0x8
    b0015674:   e799100c        ldr     r1, [r9, ip]
  p17 = getarrayitem_gc(p11, 2, use_e, descr=<ArrayP 4>) an: 5.0
    b0015678:   e58b20e0        str     r2, [fp, #224]
    b001567c:   e3a02002        mov     r2, #2  ; 0x2
    b0015680:   e1a0c102        lsl     ip, r2, #2
    b0015684:   e28cc008        add     ip, ip, #8      ; 0x8
    b0015688:   e799200c        ldr     r2, [r9, ip]
  p19 = getarrayitem_gc(p11, 3, use_e, descr=<ArrayP 4>) an: 5.0
    b001568c:   e58b50e4        str     r5, [fp, #228]
    b0015690:   e3a05003        mov     r5, #3  ; 0x3
    b0015694:   e1a0c105        lsl     ip, r5, #2
    b0015698:   e28cc008        add     ip, ip, #8      ; 0x8
    b001569c:   e799500c        ldr     r5, [r9, ip]

Improve this to::

  p13 = getarrayitem_gc(p11, 0, use_e, descr=<ArrayP 4>) an: 4.0
    ; set ip 8 directly
    mov     ip, #8
    ldr     sl, [r9, ip]
  p15 = getarrayitem_gc(p11, 1, use_e, descr=<ArrayP 4>) an: 4.0
    ; the next offset is just 8 + 4 -- can even just load this directly
    add     ip, ip, #4
    ldr     r1, [r9, ip]
  p17 = getarrayitem_gc(p11, 2, use_e, descr=<ArrayP 4>) an: 5.0
    ; register pressure -- can't do much about that
    str     r2, [fp, #224]
    ; at least we can make this more efficient, 8 + 8
    add     ip, ip, #4
    ldr     r2, [r9, ip]
  p19 = getarrayitem_gc(p11, 3, use_e, descr=<ArrayP 4>) an: 5.0
    ; register pressure
    str     r5, [fp, #228]
    ; as usual 8 + 12
    add     ip, ip, #4
    ldr     r5, [r9, ip]

Even better, should be able to use ARM's post-increment addressing mode to
remove the adds...

* This::

  i20 = int_eq(60, i18, use_g) an: 4.0
    b0014de8:   e3a0503c        mov     r5, #60 ; 0x3c
    b0014dec:   e1550006        cmp     r5, r6
    b0014df0:   03a05001        moveq   r5, #1  ; 0x1
    b0014df4:   13a05000        movne   r5, #0  ; 0x0

Can be::

  i20 = int_eq(60, i18, use_g) an: 4.0
    b0014dec:   e1550006        cmp     r6, #60
    b0014df0:   03a05001        moveq   r5, #1  ; 0x1
    b0014df4:   13a05000        movne   r5, #0  ; 0x0

* Bridge dispatch table
* Directly patch the bridge address into the jitted code instead of
additional indirection


--------------------------------------------------------------------------
Case study
--------------------------------------------------------------------------

  label(p0, p1, p2, i15, p22, p7, p6, p55, i84, p90, no_res, descr=TargetToken(-1345993096))
ignore                        increment_debug_counter(16609056, no_res)
ignore                        p97 = force_token(unknown)
call 0%, const                cond_call(i15, 7854952, p1, guard, descr=<Callv 0 r EF=2 OS=121>)
achange 12%, vchange 12%      p98 = getarrayitem_gc(p22, 2, use_both, descr=<ArrayP 4>)
call ~0%                      cond_call_gc_wb(p1, guard, descr=<WriteBarrierDescr object at 0xc95548>)
achange 12%                   setfield_gc(p1, p7, no_res, descr=<FieldP pypy.interpreter.pyframe.PyFrame.inst_f_backref 20>)
achange 12%                   setarrayitem_gc(p22, 3, ConstPtr(null), no_res, descr=<ArrayP 4>)
achange 12%                   setfield_gc(p1, 3, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
fail 0%                       guard_class(p98, 11044292, guard, descr=<Guard0xafc54970>)
achange 12%, vchange ~0%      p99 = getfield_gc(p98, use_g, descr=<FieldP pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_w_seq 12>)
fail 0%                       guard_nonnull(p99, guard, descr=<Guard0xafc549a0>)
achange 12%, vchange 100%     i100 = getfield_gc(p98, use_both, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
achange ~0%, vchange 0%       p101 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_strategy 12>)
fail 0%                       guard_class(p101, 13424228, guard, descr=<Guard0xafc549d0>)
achange ~0%, vchange ~0%      p102 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_lstorage 8>)
achange ~0%, vchange 0%       i103 = getfield_gc_pure(p102, use_g, descr=<FieldS tuple1.item0 4>)
                              i104 = int_lt(i100, 0, use_g)
fail 0%                       guard_false(i104, guard, descr=<Guard0xafc54a00>)
                              i105 = int_ge(i100, i103, use_g)
fail 12%                      guard_false(i105, guard, descr=<Guard0xafc54a30>)
                              i106 = int_add(i100, 1, use_e)
achange 14%, vchange ~0%      p107 = getarrayitem_gc(p55, 0, use_both, descr=<ArrayP 4>)
achange ~0%, vchange 14%      p108 = getfield_gc(p107, use_both, descr=<FieldP pypy.interpreter.nestedscope.Cell.inst_w_value 8>)
achange 14%                   setfield_gc(p1, 9, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
achange 14%                   setfield_gc(p98, i106, no_res, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
fail 0%                       guard_nonnull_class(p108, 11043048, guard, descr=<Guard0xafc54a60>)
achange 14%                   setfield_gc(p1, 15, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
achange 14%                   setarrayitem_gc(p22, 4, ConstPtr(null), no_res, descr=<ArrayP 4>)
achange 14%, vchange 14%      p109 = getfield_gc_pure(p108, use_both, descr=<FieldP pypy.objspace.std.tupleobject.W_TupleObject.inst_wrappeditems 8>)
                              i110 = arraylen_gc(p109, use_g, descr=<ArrayP 4>)
                              i111 = uint_ge(i100, i110, use_g)
fail 0%                       guard_false(i111, guard, descr=<Guard0xafc54a90>)
malloc, call ~0%              p113 = call_malloc_nursery(16, use_e)
malloc                        setfield_gc(p113, 245, no_res, descr=<FieldS header.tid 0>)
malloc                        setfield_gc(p113, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
malloc                        setfield_gc(p113, i100, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
call ~0%                      cond_call_gc_wb_array(p22, 1, guard, descr=<WriteBarrierDescr object at 0xc95548>)
achange 14%                   setarrayitem_gc(p22, 1, p113, no_res, descr=<ArrayP 4>)
achange 100%, vchange 100%    p116 = getarrayitem_gc_pure(p109, i100, use_both, descr=<ArrayP 4>)
fail 0%                       guard_nonnull_class(p116, ConstClass(W_IntObject), guard, descr=<Guard0xafc54ac0>)
achange 14%                   setfield_gc(p1, 19, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
achange 100%, vchange 100%    i117 = getfield_gc_pure(p116, use_e, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
                              i118 = int_add_ovf(i117, i100, use_e)
fail 0%                       guard_no_overflow(guard, descr=<Guard0xafc54af0>)
                              i119 = int_add(i84, 1, use_both)
                              i120 = arraylen_gc(p90, use_g, descr=<ArrayP 4>)
                              i121 = int_lt(i120, i119, use_g)
call 12%                      cond_call(i121, ConstClass(_ll_list_resize_hint_really_look_inside_iff__listPtr_Signed_Bool), p2, i119, 1, guard, descr=<Callv 0 rii EF=4>)
achange 14%                   setfield_gc(p1, 20, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
fail 0%                       guard_no_exception(guard, descr=<Guard0xafc54b20>)
achange 14%, vchange 28%      p122 = getfield_gc(p2, use_both, descr=<FieldP list.items 8>)
malloc, call ~0%              p124 = call_malloc_nursery(16, use_e)
malloc                        setfield_gc(p124, 245, no_res, descr=<FieldS header.tid 0>)
malloc                        setfield_gc(p124, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
malloc                        setfield_gc(p124, i118, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
call ~0%                      cond_call_gc_wb_array(p122, i84, guard, descr=<WriteBarrierDescr object at 0xc95548>)
achange 100%                  setarrayitem_gc(p122, i84, p124, no_res, descr=<ArrayP 4>)
achange 14%                   setfield_gc(p2, i119, no_res, descr=<FieldS list.length 4>)
ignore                        i127 = arraylen_gc(p22, unknown, descr=<ArrayP 4>)
ignore                        i128 = arraylen_gc(p55, unknown, descr=<ArrayP 4>)
  jump(p0, p1, p2, i15, p22, p7, p6, p55, i119, p122, no_res, descr=TargetToken(-1345993096))





exec_slice:
  label(p0, p1, p2, i15, p22, p7, p6, p55, i84, p90, no_res, descr=TargetToken(-1345993096))
  increment_debug_counter(16609056, no_res)
  p98 = getarrayitem_gc(p22, 2, use_both, descr=<ArrayP 4>)
  setfield_gc(p1, p7, no_res, descr=<FieldP pypy.interpreter.pyframe.PyFrame.inst_f_backref 20>)
  setarrayitem_gc(p22, 3, ConstPtr(null), no_res, descr=<ArrayP 4>)
  setfield_gc(p1, 3, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
  i100 = getfield_gc(p98, use_both, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
  i106 = int_add(i100, 1, use_e)
  p107 = getarrayitem_gc(p55, 0, use_both, descr=<ArrayP 4>)
  p108 = getfield_gc(p107, use_both, descr=<FieldP pypy.interpreter.nestedscope.Cell.inst_w_value 8>)
  setfield_gc(p1, 9, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
  setfield_gc(p98, i106, no_res, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
  setfield_gc(p1, 15, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
  setarrayitem_gc(p22, 4, ConstPtr(null), no_res, descr=<ArrayP 4>)
  p109 = getfield_gc_pure(p108, use_both, descr=<FieldP pypy.objspace.std.tupleobject.W_TupleObject.inst_wrappeditems 8>)
  p113 = call_malloc_nursery(16, use_e)
  setfield_gc(p113, 245, no_res, descr=<FieldS header.tid 0>)
  setfield_gc(p113, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
  setfield_gc(p113, i100, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
  setarrayitem_gc(p22, 1, p113, no_res, descr=<ArrayP 4>)
  p109 = getfield_gc_pure(p108, use_both, descr=<FieldP pypy.objspace.std.tupleobject.W_TupleObject.inst_wrappeditems 8>)
  p113 = call_malloc_nursery(16, use_e)
  setfield_gc(p113, 245, no_res, descr=<FieldS header.tid 0>)
  setfield_gc(p113, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
  setfield_gc(p113, i100, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
  setarrayitem_gc(p22, 1, p113, no_res, descr=<ArrayP 4>)
  p116 = getarrayitem_gc_pure(p109, i100, use_both, descr=<ArrayP 4>)
  setfield_gc(p1, 19, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
  i117 = getfield_gc_pure(p116, use_e, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
  i118 = int_add_ovf(i117, i100, use_e)
  i119 = int_add(i84, 1, use_both)
  setfield_gc(p1, 20, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
  p122 = getfield_gc(p2, use_both, descr=<FieldP list.items 8>)
  p124 = call_malloc_nursery(16, use_e)
  setfield_gc(p124, 245, no_res, descr=<FieldS header.tid 0>)
  setfield_gc(p124, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
  setfield_gc(p124, i118, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
  setarrayitem_gc(p122, i84, p124, no_res, descr=<ArrayP 4>)
  setfield_gc(p2, i119, no_res, descr=<FieldS list.length 4>)
  jump(p0, p1, p2, i15, p22, p7, p6, p55, i119, p122, no_res, descr=TargetToken(-1345993096))

guard_slice:
  cond_call(i15, 7854952, p1, guard, descr=<Callv 0 r EF=2 OS=121>)
  p98 = getarrayitem_gc(p22, 2, use_both, descr=<ArrayP 4>)
  cond_call_gc_wb(p1, guard, descr=<WriteBarrierDescr object at 0xc95548>)
  guard_class(p98, 11044292, guard, descr=<Guard0xafc54970>)
  p99 = getfield_gc(p98, use_g, descr=<FieldP pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_w_seq 12>)
  guard_nonnull(p99, guard, descr=<Guard0xafc549a0>)
  i100 = getfield_gc(p98, use_both, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
  p101 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_strategy 12>)
  guard_class(p101, 13424228, guard, descr=<Guard0xafc549d0>)
  p102 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_lstorage 8>)
  i103 = getfield_gc_pure(p102, use_g, descr=<FieldS tuple1.item0 4>)
  i104 = int_lt(i100, 0, use_g)
  guard_false(i104, guard, descr=<Guard0xafc54a00>)
  i105 = int_ge(i100, i103, use_g)
  guard_false(i105, guard, descr=<Guard0xafc54a30>)
  p107 = getarrayitem_gc(p55, 0, use_both, descr=<ArrayP 4>)
  p108 = getfield_gc(p107, use_both, descr=<FieldP pypy.interpreter.nestedscope.Cell.inst_w_value 8>)
  guard_nonnull_class(p108, 11043048, guard, descr=<Guard0xafc54a60>)
  p109 = getfield_gc_pure(p108, use_both, descr=<FieldP pypy.objspace.std.tupleobject.W_TupleObject.inst_wrappeditems 8>)
  i110 = arraylen_gc(p109, use_g, descr=<ArrayP 4>)
  i111 = uint_ge(i100, i110, use_g)
  guard_false(i111, guard, descr=<Guard0xafc54a90>)
  cond_call_gc_wb_array(p22, 1, guard, descr=<WriteBarrierDescr object at 0xc95548>)
  p116 = getarrayitem_gc_pure(p109, i100, use_both, descr=<ArrayP 4>)
  guard_nonnull_class(p116, ConstClass(W_IntObject), guard, descr=<Guard0xafc54ac0>)
  guard_no_overflow(guard, descr=<Guard0xafc54af0>)
  i119 = int_add(i84, 1, use_both)
  i120 = arraylen_gc(p90, use_g, descr=<ArrayP 4>)
  i121 = int_lt(i120, i119, use_g)
  cond_call(i121, ConstClass(_ll_list_resize_hint_really_look_inside_iff__listPtr_Signed_Bool), p2, i119, 1, guard, descr=<Callv 0 rii EF=4>)
  guard_no_exception(guard, descr=<Guard0xafc54b20>)
  p122 = getfield_gc(p2, use_both, descr=<FieldP list.items 8>)
  cond_call_gc_wb_array(p122, i84, guard, descr=<WriteBarrierDescr object at 0xc95548>)

--------------------------------------------------------------------------
after transformation
--------------------------------------------------------------------------

achange 12%, vchange 12%      p98 = getarrayitem_gc(p22, 2, use_both, descr=<ArrayP 4>)
achange 12%, vchange ~0%      p99 = getfield_gc(p98, use_g, descr=<FieldP pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_w_seq 12>)
achange 12%, vchange 100%     i100 = getfield_gc(p98, use_both, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
achange ~0%, vchange 0%       p101 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_strategy 12>)
fail 0%                       guard_class(p101, 13424228, guard, descr=<Guard0xafc549d0>)
achange ~0%, vchange ~0%      p102 = getfield_gc(p99, use_g, descr=<FieldP pypy.objspace.std.listobject.W_ListObject.inst_lstorage 8>)
achange ~0%, vchange 0%       i103 = getfield_gc_pure(p102, use_g, descr=<FieldS tuple1.item0 4>)
achange 14%, vchange ~0%      p107 = getarrayitem_gc(p55, 0, use_both, descr=<ArrayP 4>)
achange ~0%, vchange 14%      p108 = getfield_gc(p107, use_both, descr=<FieldP pypy.interpreter.nestedscope.Cell.inst_w_value 8>)
fail 0%                       guard_nonnull_class(p108, 11043048, guard, descr=<Guard0xafc54a60>)
achange 14%, vchange 14%      p109 = getfield_gc_pure(p108, use_both, descr=<FieldP pypy.objspace.std.tupleobject.W_TupleObject.inst_wrappeditems 8>)
call ~0%                      cond_call_gc_wb_array(p22, 1, guard, descr=<WriteBarrierDescr object at 0xc95548>)
achange 14%, vchange 28%      p122 = getfield_gc(p2, use_both, descr=<FieldP list.items 8>)

  label(p0, p1, p2, i15, p22, p7, p6, p55, i84, p90, || p98, p99, i100, p101, i103, p108-d, p109, p122 no_res, descr=TargetToken(-1345993096))

                              will change( i100 )
                              X = did_not_change( p1, i15, p22, p98?, p99?, p101?, i103?, p122?
                              guard_false( X ) [ go to normal jit loop ] (a)

                              i104 = int_lt(i100, 0, use_g)
fail 0%                       guard_false(i104, guard, descr=<Guard0xafc54a00>) (b)
                              i105 = int_ge(i100, i103, use_g)
fail 12%                      guard_false(i105, guard, descr=<Guard0xafc54a30>) (c)
                              i106 = int_add(i100, 1, use_e)

                              i110 = arraylen_gc(p109, use_g, descr=<ArrayP 4>)
                              i111 = uint_ge(i100, i110, use_g)
fail 0%                       guard_false(i111, guard, descr=<Guard0xafc54a90>) (d)

malloc, call ~0%              p113 = call_malloc_nursery(16, use_e)
malloc                        setfield_gc(p113, 245, no_res, descr=<FieldS header.tid 0>)
malloc                        setfield_gc(p113, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
malloc                        setfield_gc(p113, i100, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)

achange 100%, vchange 100%    p116 = getarrayitem_gc_pure(p109, i100, use_both, descr=<ArrayP 4>)
fail 0%                       guard_nonnull_class(p116, ConstClass(W_IntObject), guard, descr=<Guard0xafc54ac0>) (e)

achange 100%, vchange 100%    i117 = getfield_gc_pure(p116, use_e, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)
                              i118 = int_add_ovf(i117, i100, use_e)
fail 0%                       guard_no_overflow(guard, descr=<Guard0xafc54af0>) (f)

                              i119 = int_add(i84, 1, use_both)
                              i120 = arraylen_gc(p90, use_g, descr=<ArrayP 4>)
                              i121 = int_lt(i120, i119, use_g)
call 12%                      cond_call(i121, ConstClass(_ll_list_resize_hint_really_look_inside_iff__listPtr_Signed_Bool), p2, i119, 1, guard, descr=<Callv 0 rii EF=4>)
fail 0%                       guard_no_exception(guard, descr=<Guard0xafc54b20>)

malloc, call ~0%              p124 = call_malloc_nursery(16, use_e)
malloc                        setfield_gc(p124, 245, no_res, descr=<FieldS header.tid 0>)
malloc                        setfield_gc(p124, ConstClass(W_IntObject), no_res, descr=<FieldU object.typeptr 4>)
malloc                        setfield_gc(p124, i118, no_res, descr=<FieldS pypy.objspace.std.intobject.W_IntObject.inst_intval 8>)

call ~0%                      cond_call_gc_wb_array(p122, i84, guard, descr=<WriteBarrierDescr object at 0xc95548>)
achange 100%                  setarrayitem_gc(p122, i84, p124, no_res, descr=<ArrayP 4>)
  jump(p0, p1, p2, i15, p22, p7, p6, p55, i119, p122, no_res, descr=TargetToken(-1345993096))


  guard slowpath b+
achange 12%                   setfield_gc(p1, p7, no_res, descr=<FieldP pypy.interpreter.pyframe.PyFrame.inst_f_backref 20>)
achange 12%                   setarrayitem_gc(p22, 3, ConstPtr(null), no_res, descr=<ArrayP 4>)
achange 12%                   setfield_gc(p1, 3, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)

  guard slowpath d+
achange 14%                   setfield_gc(p1, 9, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
achange 14%                   setfield_gc(p98, i106, no_res, descr=<FieldS pypy.objspace.std.iterobject.W_AbstractSeqIterObject.inst_index 8>)
achange 14%                   setfield_gc(p1, 15, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)
achange 14%                   setarrayitem_gc(p22, 4, ConstPtr(null), no_res, descr=<ArrayP 4>)

  guard slowpath e+
achange 14%                   setarrayitem_gc(p22, 1, p113, no_res, descr=<ArrayP 4>)

  guard slowpath f+
achange 14%                   setfield_gc(p1, 19, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)

  guard slowpath g+
achange 14%                   setfield_gc(p1, 20, no_res, descr=<FieldS pypy.interpreter.pyframe.PyFrame.inst_last_instr 44>)

  guard slowpath rollaround
achange 14%                   setfield_gc(p2, i119, no_res, descr=<FieldS list.length 4>)


go to dir:

  % cd pypy-benchmarks/unladen_swallow/performance

run pydgin to generate pydgin out and pypylog:


generate the pydgin in file:

./jitlog_analyze.py --color --asm --slices --gen-omit safe_guard_slice --use-rw --pydgin-out pypy-benchmarks/unladen_swallow/performance/ai_mini_pydgin_analysis_omit2.out pypy-benchmarks/unladen_swallow/performance/ai_mini-pydgin-arm-omit2-pre.pypylog

re-run with omitting:

/work/bits0/bi45/vc/git-brg/pydgin-pyxcel-perf/arm/pydgin-arm-jit -e PYPYLOG=jit:ai_mini-pydgin-arm-omit2-safe_guards.pypylog -e PYXCEL_IN_FILE=../../../omit_safe_guard_slice.in /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-omit2 bm_ai_mini.py


--------------------------------------------------------------------------
omit file
--------------------------------------------------------------------------

go to dir:

  % cd pypy-benchmarks/unladen_swallow/performance

run pydgin to generate pydgin out and pypylog:

  % /work/bits0/bi45/vc/git-brg/pydgin/arm/stable/pydgin-arm-nojit-debug -e PYPYLOG=jit:outs/bm_ai_mini.stage1.pypylog /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-omit2 bm_ai_mini.py | tee outs/bm_ai_mini.stage1.pydginout

The outputs are <bmark>.stage1.pypylog and <bmark>.stage1.pydginout. Now
generate the omit file:

  % ../../../jitlog_analyze.py --asm --gen-omit safe_guard_slice --use-rw --slices --pydgin-out outs/bm_ai_mini.stage1.pydginout --pydgin-in outs/bm_ai_mini.stage2.pydginin outs/bm_ai_mini.stage1.pypylog

Omit file is <bmark>.stage2.pydginin. Run first without the in file

  % /work/bits0/bi45/vc/git-brg/pydgin-pyxcel-perf/arm/stable/pydgin-arm-jit -e PYPYLOG=jit:bm_ai_mini.stage3.pypylog /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-omit2 bm_ai_mini.py | tee outs/bm_ai_mini.stage3.pydginout

Run with the file:

  % /work/bits0/bi45/vc/git-brg/pydgin-pyxcel-perf/arm/stable/pydgin-arm-jit -e PYPYLOG=jit:bm_ai_mini.stage4.pypylog -e PYXCEL_IN_FILE=outs/bm_ai_mini.stage2.pydginin /work/bits0/bi45/vc/hg-misc/pypy-cross/pypy/goal/pypy-jit-arm-nofp-omit2 bm_ai_mini.py | tee outs/bm_ai_mini.stage4.pydginout

stage1 1773375130
stage3 1491371096
stage4 1339045586


bm_ai             1491371096  1339045586
bm_django    F    1982951551  (crashes)
bm_html5lib full pypy (_struct)
bm_nbody          2910059603  2753467864
bm_pickle   random, _struct
bm_richards       1356793327   743988271 (crash)
bm_regex_compile  EmptyCache object is not scriptable
bm_regex_effbot    540525178   504358270
3791179865

