==========================================================================
IEEE Micro notes
==========================================================================

Here are the guidelines:

Submitted by Lieven Eeckhout
http://www.computer.org/portal/web/computingnow/micro
Call for Papers: IEEE Micro Special Issue on Heterogeneous Computing
Guest Co-Editors:
Dean Tullsen (UCSD)
Ravishankar Iyer (Intel)
Submissions due:	Jan 16, 2015
Publication date:	July-August 2015
Heterogeneity is widely accepted as a fruitful avenue to improve
performance and power/energy/thermal-efficiency in the face of continued
technology miniaturization (Moore’s Law) and slowed supply voltage
reduction (end of Dennard scaling). Heterogeneity comes in many flavors
ranging from Systems-on-Chip (SoCs) with specialized hardware
accelerators, to hybrid CPU/GPU architectures, to single-ISA heterogeneous
multi-cores with different core types, to multi-ISA heterogeneous
multi-cores in which different core types implement different
Instruction-Set Architectures (ISA).  Architects have explored and built
heterogeneous architectures across a broad spectrum of computing devices
including embedded systems, mobile devices, datacenters, and
High-Performance Computing (HPC) supercomputers. While the performance and
power/energy opportunities have been outlined, important challenges are
yet to be studied regarding architecture, accelerators, hardware/software
interface, run-time support, compilation, programming models, and
performance evaluation. The goal of this Special Issue is to present the
latest state-of-the-art results in the broad area of heterogeneous
computing systems.

Areas of interest include, but are not limited to:
- Heterogeneous architectures, including:
  o System-on-Chip (SoC) with accelerators
  o CPU/GPU systems
  o Single-ISA heterogeneous multi-cores
  o Multi-ISA heterogeneous multi-cores
- Roadmaps and commercial trends in heterogeneous architectures
- Trade-offs in performance, power, energy, thermal, reliability, code
  portability and programmability due to heterogeneity
- Case studies of heterogeneous architectures in embedded system design,
  mobile computing, HPC, data centers, etc.
- Accelerator architectures and interfaces
- Platform support for heterogeneous and accelerator architectures
- Hardware/software interactions on heterogeneous architectures, including
  OS scheduling and compilation
- Programming models and runtime support for heterogeneous architectures
- Workloads particularly suited for heterogeneity
- Performance evaluation of heterogeneous architectures
- Experiences with real heterogeneous platforms

Submission procedure:
Log onto IEEE CS Manuscript Central
(https://mc.manuscriptcentral.com/micro-cs) and submit your manuscript.
Please direct questions to the IEEE Micro magazine assistant
(micro-ma@computer.org) regarding the submission site. For the
manuscript submission, acceptable file formats include Microsoft Word and
PDF. Manuscripts should not exceed 5,000 words including references, with
each average-size figure counting as 150 words toward this limit.
Please include all figures and tables, as well as a cover page with author
contact information (name, postal address, phone, fax, and e-mail address)
and a 200-word abstract. Submitted manuscripts must not have been
previously published or currently submitted for publication elsewhere, and
all manuscripts must be cleared for publication. All previously published
papers must have at least 30% new content compared to any conference (or
other) publication. Accepted articles will be edited for structure, style,
clarity, and readability. For more information, please visit
the IEEE Micro Author Center
(http://www2.computer.org/portal/web/peerreviewmagazines/acmicro).
Important dates:
Initial submissions due:	Jan 16, 2015
Author notification:	March 2, 2015
Revised papers due:	March 20, 2015
Final version due:	April 23, 2015
Publication timeframe:	July-August 2015
Questions?
Contact the Guest Co-Editors Dean Tullsen (tullsen@ucsd.edu) and
Ravi Iyer (ravishankar.iyer@intel.com), or the Editor-in-Chief
Lieven Eeckhout (lieven.eeckhout@ugent.be).

--------------------------------------------------------------------------
Word count
--------------------------------------------------------------------------

The limit is 5000 words. Here is the current breakdown::

  % texcount -inc paper-xloops.tex

  File(s) total: paper-xloops.tex
  Words in text: 8132
  Words in headers: 69
  Words outside text (captions, etc.): 520
  Number of headers: 25
  Number of floats/tables/figures: 15
  Number of math inlines: 13
  Number of math displayed: 0

References are not included in this. We can assume ~20 words per reference

Assuming average size images (150 words): 8132 + (15figs*150) + 36*20 = 11102

--------------------------------------------------------------------------
Current outline
--------------------------------------------------------------------------

Abstract 151

1. Intro 832

  - intra-iteration loop dependence patterns and prior work
  - efficiency vs flexibility, case for abstraction
  - inter-iteration loop dependence patterns
  - xloops
  - rest of the paper
  - contributions

2. Explicit Loop Specialization 3446

  2.1 XLOOPS ISA 1155

    - overview
    - xi instruction
    - xloop.uc instruction
    - xloop.or instruction
    - xloop.om instruction
    - xloop.ua instruction
    - xloop.*.db instruction
    - exceptions
    - isa as a clean abstraction

    Fig 1: ISA examples
    Table 1: ISA extensions

  2.2 XLOOPS Compiler 375

    - annotations
    - modified compiler passes
    - additional optimizations

    Fig 2: C code for war (#pragma xloops unordered/ordered) example
    Fig 3: C code for mm (#pragma xloops ordered) example

  2.3 XLOOPS Traditional execution 89

  2.4 XLOOPS Specialized execution 1394

    - uarch overview
    - scan phase
    - specialized execution phase
    - xi execution
    - xloop.uc execution
    - xloop.or execution
    - xloop.om execution
    - xloop.ua execution
    - xloop.*.db execution

    Fig 4: XLOOPS microarchitecture

  2.5 XLOOPS Adaptive execution 406

    - motivation
    - profiling phases
    - migration of execution
    - memorizing the outcomes of profiling

3. XLOOPS application kernels 425

  - diverse applications, suites
  - custom kernel descriptions
  - compiler framework

  Table 2: Application kernels and cycle-level results

4. XLOOPS cycle-level evaluation 2016

  4.1 Cycle-level methodology 346

    - methodology
    - mcpat / energy modeling methodology
    - lane / o3 configurations

    Table 3: cycle-level configurations

  4.2 Traditional execution 233
    
    - explain results for traditional execution

  4.3 Specialized execution 547

    - explain different columns for specialized execution
    - xloop.uc analysis
    - xloop.or analysis
    - xloop.om, orm, ua analysis
    - xloop.uc.db analysis

    Fig 5: cycle-level speedups
    Fig 6: Stall/squash breakdowns

  4.4 Adaptive execution 128

    - explanation

    Fig 7: Adaptive execution speedups

  4.5 Energy efficiency vs performance 191

    - explanation

    Fig 8: Energy efficiency vs performance

  4.6 Microarchitectural design space exploration 320

    - multi threading
    - scaling lanes
    - more llfus and memory ports

    Fig 9: Microarchitecture design space

  4.7 Application case studies 216

    - hand optimized xloop.or
    - loop transformations

    Table 4: Case study results

5. VLSI Evaluation 543

  5.1 VLSI Methodology 146

    - methodology

  5.2 VLSI Area Results 186

    - explanation

    Table 5: VLSI area and cycle time results

  5.3 VLSI Energy efficiency vs Performance 174

    - explanation

    Fig 10: VLSI energy efficiency vs performance

6. Related work 499

  - intra-iteration: ASIPS, DySER etc
  - xloop.uc: dsps, simd, gpus, subword simd etc
  - xloop.ua: TM
  - xloop.or: multiscalar, helix-rc etc
  - xloop.om: multiscalar, tls
  - xloop.*.db: carbon

7. Conclusions 105

Acknowledgments 89

References ~ 20*36 = 720

--------------------------------------------------------------------------
proposed outline for IEEE Micro
--------------------------------------------------------------------------

Abstract 151

1. Intro 832 -> ~800

  Will be similar to current one but will contrast less in inter- vs.
  intra-iteration dependences. Instead, try to motivate a case for
  single-ISA architecture.

2. Explicit Loop Specialization 3446 -> ~3300

  2.1 XLOOPS ISA 1155 -> ~1000

    mostly the same as the current paper

    Fig 1: ISA examples (might reduce the number of examples in this)
    Table 1: ISA extensions

  (remove compiler section, was 375)

  2.2 XLOOPS Traditional execution 89 -> ~100

    similar to current one, emphasize here that code that can run on a
    dataflow engine can run on a GPP with negligible performance overheads

  2.3 XLOOPS Specialized execution on Loosely-Coupled Lanes (LCLs) 1394 -> ~1000

    similar, but try to cut some content and refer to paper

    - uarch overview
    - scan phase
    - specialized execution phase
    - xi execution
    - xloop.uc execution
    - xloop.or execution
    - xloop.om execution (reduce or cut)
    - xloop.ua execution (cut totally)
    - xloop.*.db execution (reduce)

    Fig 2: XLOOPS microarchitecture + dataflow engine

  2.4 XLOOPS Specialized execution on Dataflow Engine (DFE) ~700

    new section

    - sketch of a possible microarchitecture. maybe also talk about the
      vast design space
    - configuration logic which is quite sophisticated

    (maybe) Fig: a detailed view of the dataflow engine
    Fig 3: simplified configuration algorithm

  2.5 XLOOPS Adaptive execution 406 -> ~500

    in addition to the older section, also need to talk about three-way
    adaptive execution

    - motivation
    - profiling phases
    - migration of execution
    - memorizing the outcomes of profiling

3. XLOOPS application kernels 425 -> ~300

  try to make this section more compact

  - diverse applications, suites
  - custom kernel descriptions
  - compiler framework

  Table 2: Application kernels and cycle-level results (make the table
  simpler, add data about dataflow execution)

4. XLOOPS cycle-level evaluation 2016 -> ~1750

  4.1 Cycle-level methodology 346 -> ~300
    mostly same, try to make it a little more concise

    - methodology
    - mcpat / energy modeling methodology
    - lane / o3 configurations

    Table 3: cycle-level configurations

  4.2 Traditional execution 233 -> ~250

    mostly the same
    
    - explain results for traditional execution

  4.3 Specialized execution 547 -> ~700

    also explain DFE performance

    - explain different columns for specialized execution
    - xloop.uc analysis
    - xloop.or analysis
    - xloop.om, orm, ua analysis
    - xloop.uc.db analysis

    Fig 5: cycle-level speedups
    Fig 6: Stall/squash breakdowns (maybe not include this?)
    Fig 7: 2D LCL vs DFE performance

  4.4 Adaptive execution 128 -> ~250

    evaluation of 3-way adaptive execution

    - explanation

    Fig 8: Adaptive execution speedups

  4.5 Energy efficiency vs performance 191 -> ~250

    hopefully we can get some energy modelling here for DFE

    - explanation

    Fig 9: Energy efficiency vs performance

  (remove uarch design space and app case studies, 320 and 216 words each)

(remove vlsi evaluation, 543 words)

5. Related work 499 -> ~600

  also give related work regarding the dataflow execution and other
  single-isa proposals

  - intra-iteration: ASIPS, DySER etc
  - xloop.uc: dsps, simd, gpus, subword simd etc
  - xloop.ua: TM
  - xloop.or: multiscalar, helix-rc etc
  - xloop.om: multiscalar, tls
  - xloop.*.db: carbon

7. Conclusions 105 -> ~150

(not sure if we have acknowledgments)

References ~ 20*36 = 720

total word count: 800 + 3300 + 300 + 1750 + 600 + 720 + (12 fig/tbls * 150)
                  = 9270

We're still 4000+ words off the 5000 word limit. We need to cut much more
content...

