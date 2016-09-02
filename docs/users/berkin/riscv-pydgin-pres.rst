==========================================================================
RISC-V Pydgin Presentation/Abstract Outline
==========================================================================

Abstract we had submitted:

Instruction-set simulators (ISSs) are indispensable tools for software
development on new ISAs.  Proprietary ISAs have very stable interfaces
that evolve slowly, and as a result frequent changes to the ISSs were not
required. Recently, RISC-V recognized the increasing need for
instruction-set specialization by providing a very extensible ISA.
Extensible ISAs require the ISS to be extensible as well. An extensible
ISS should enable productively experimenting with new instructions while
maintaining high simulator performance.  We believe Pydgin [1] is the
right tool for this job with its excellent productivity and performance,
made possible by its pseudo-code-like architecture description and the
automatic insertion of a state-of-the-art just-in-time compiler. In this
talk, I will introduce Pydgin and its unique development flow, which makes
use of contemporary work on dynamic language interpreters. I will also
talk about our development effort to add RISC-V support to Pydgin, which
we achieved in only 2 person-weeks, giving a 3X performance boost over
Spike, the reference RISC-V ISS. I will argue that Pydgin is an excellent
framework for experimenting with new RISC-V extensions, as well as adding
instrumentation for early design-space exploration.

Note that I would prefer a 12-minute presentation slot for this. But if
there are no slots left, I would be happy to do a poster instead.

[1] D. Lockhart, B. Ilbeyi, and C. Batten. Pydgin: Generating Fast
Instruction Set Simulators from Simple Architecture Descriptions with
Meta-Tracing JIT Compilers. Int'l Symp. on Performance Analysis of Systems
and Software (ISPASS), Mar 2015.

--------------------------------------------------------------------------
Talk outline
--------------------------------------------------------------------------

- Motivation:
  * Proprietary ISAs have relatively stable interfaces (e.g. x86 and some
    obscure extension)
  * Traditional instruction-set simulators focused on simulation
    performance
  * As a result, these ISSs have less-than-friendly architectural
    descriptions (show example)
  * RISC-V breaks this trend and makes extensibility and architectural
    specialization an important goal
  * RISC-V makes extensibility feasible, but traditional ISSs make it hard

- Introduce Pydgin
  * Pydgin is an ISS that is written in Python
  * Not arbitrary Python: a typed subset of Python with a few limitations:
    - One type per variable (like C++ auto type)
    - No lambdas or closures
    - Integers are bounded to native word width unless otherwise specified
      (Python integers are unbounded)
    - Not all Python standard library supported (there are RPython
      equivalents of the most useful parts of the library (e.g., struct,
      re))
    - Full support for Python OO features

- RPython translation and execution flow

- RISC-V state and ADL example

- Mini RISC-V extensibility example

- Performance comparison against SPIKE (and Qemu?)

- Development anecdotes to illustrate productivity
  * It took two people a total of three person-months to develop Pydgin
    for PARC (a MIPS-like ISA) and ARMv5
  * It took two people (with the help and convincing of Yunsup Lee) a
    total of three person-weeks to develop Pydgin for RISC-V

- Current state of Pydgin-RISC-V and conclusion
  * ISA subsets supported
  * Currently bare-metal-only
  * Currently 64-bit on 64-bit only
  * (We have ideas on implementing full-system with I/O modeling?)
  * Link to the github link, directions on how to use it
  * Conclusions
  * Acknowledgements

--------------------------------------------------------------------------
git coloring command
--------------------------------------------------------------------------

::

  git log --format="%C(white)%cd %C(blue)%an    %x09%C(yellow)%s" --date=short | less

--------------------------------------------------------------------------
extended abstract outline
--------------------------------------------------------------------------

- Introduction
  * How instruction sets simulators are used
  * Typical performance of various kinds simulators
  * Productivity
  * Proprietary ISAs
  * RISC-V

  * Traditionally, productivity through high-level ADLs, performance
    through low-level C with a custom DBT
  * There has been previous research on automatically translating the
    high-level descriptions into low-level DBT-enabled interpreter.
  * These custom translation approaches usually suffer because they are
    either not free or not maintained.
  * A similar trend exists in the PL community, where interpreters of
    dynamic languages are traditionally written in low-level C/C++ with
    sophisticated custom JIT.
  * A notable exception is the PyPy project
  * Pydgin uses that flow
