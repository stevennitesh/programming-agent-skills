# Codebase Architecture Family Synthesis

This note maps the books and supporting references behind the local `$codebase-design` and `$improve-codebase-architecture` skills:

- `skills/custom/codebase-design/SKILL.md`
- `skills/custom/codebase-design/DIRECT-DESIGN.md`
- `skills/custom/codebase-design/DEEPENING.md`
- `skills/custom/codebase-design/DESIGN-IT-TWICE.md`
- `skills/custom/improve-codebase-architecture/SKILL.md`
- `skills/custom/improve-codebase-architecture/HTML-REPORT.md`

The local skill-pack stance is: design deep modules with small useful interfaces, place seams where behavior genuinely varies, use adapters only when they buy locality or testability, compare interface alternatives before settling, and present architecture friction visually enough that a user can choose the next exploration.

## Primary Sources

### John Ousterhout - A Philosophy of Software Design

Source: https://web.stanford.edu/~ouster/cgi-bin/book.php

Use for:

- deep modules
- shallow modules
- simple interfaces hiding complex implementation
- information hiding
- tactical vs strategic programming
- "design it twice"

Maps to:

- `codebase-design/SKILL.md`: depth, interface, implementation, leverage, locality
- `codebase-design/DEEPENING.md`: deepening shallow clusters
- `codebase-design/DESIGN-IT-TWICE.md`: generating several interface alternatives
- `improve-codebase-architecture/SKILL.md`: finding candidates where shallow modules create friction

Skill-pack takeaway:

Depth is about leverage at the interface, not implementation size. A good recommendation should show how callers learn less while behavior and verification concentrate in one module.

### David Parnas - On the Criteria To Be Used in Decomposing Systems into Modules

Source: https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf

Use for:

- information hiding
- decomposing modules around design decisions
- avoiding modules that simply mirror processing steps
- hiding decisions likely to change

Maps to:

- `codebase-design/SKILL.md`: module, interface, implementation, locality
- `codebase-design/DEEPENING.md`: moving decisions into the module that owns them
- `improve-codebase-architecture/SKILL.md`: spotting behavior spread across callers

Skill-pack takeaway:

A module earns its keep when it hides a decision from callers. If every caller must know the sequence, the decomposition is probably shallow.

### Eric Evans - Domain-Driven Design

Source: https://www.domainlanguage.com/ddd/

Use for:

- ubiquitous language
- domain ownership
- modules around domain concepts
- preserving domain vocabulary in code and reports
- avoiding generic architecture words where real domain terms exist

Maps to:

- `codebase-design/SKILL.md`: prefer repo/domain vocabulary and map it to shared architecture vocabulary
- `codebase-design/DEEPENING.md`: move behavior to the module that owns the domain concept
- `improve-codebase-architecture/SKILL.md`: read domain glossary and ADRs before proposing candidates
- `HTML-REPORT.md`: preserve real repo/domain terms in candidate cards

Skill-pack takeaway:

Deepening is strongest when it clarifies domain ownership, not when it merely rearranges files. Use the project's language first, then explain the architecture with the shared vocabulary.

### Martin Fowler - Refactoring

Source: https://martinfowler.com/books/refactoring.html

Use for:

- behavior-preserving structural change
- small safe design moves
- tests as guardrails
- separating refactoring from feature work

Maps to:

- `codebase-design/DEEPENING.md`: behavior-preserving support slices
- `codebase-design/DESIGN-IT-TWICE.md`: first safe migration step
- `improve-codebase-architecture/SKILL.md`: report candidates but do not implement refactors

Skill-pack takeaway:

Architecture review should discover and choose refactoring opportunities; implementation is a separate pass. A good candidate includes validation and migration, not a speculative rewrite.

### Michael Feathers - Working Effectively with Legacy Code

Source: https://martinfowler.com/bliki/LegacySeam.html

Use for:

- seam vocabulary
- getting hard-to-change code under test
- safely changing legacy code
- identifying places where behavior can vary without editing callers

Maps to:

- `codebase-design/SKILL.md`: seam and adapter definitions
- `codebase-design/DEEPENING.md`: dependency categories and adapter strategy
- `improve-codebase-architecture/SKILL.md`: test surface and seam leakage as candidate signals

Skill-pack takeaway:

A seam is not a decoration or a test hook. A seam is a design point where variation belongs. If the only reason for a seam is patching a test, the design is probably wrong.

### Steve Freeman and Nat Pryce - Growing Object-Oriented Software, Guided by Tests

Source: https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/

Use for:

- growing design through tests
- using interfaces to expose responsibility boundaries
- external dependencies behind adapters
- feedback from painful tests

Maps to:

- `codebase-design/SKILL.md`: interface is the test surface
- `codebase-design/DEEPENING.md`: fake adapters and local substitutes
- `improve-codebase-architecture/SKILL.md`: owned modules mocked in tests as a friction signal

Skill-pack takeaway:

Use test pain as design evidence, but keep this skill pack classicist by default: prefer real behavior through the interface and fakes at real seams, not mocks for owned modules.

### Martin Fowler - Patterns of Enterprise Application Architecture

Source: https://martinfowler.com/books/eaa.html

Use for:

- application boundary patterns
- gateways, mappers, repositories, services, and transaction scripts
- separating domain behavior from infrastructure
- adapter-like structures around external systems

Maps to:

- `codebase-design/DEEPENING.md`: remote-owned and true-external dependency categories
- `codebase-design/SKILL.md`: adapter and seam vocabulary
- `improve-codebase-architecture/SKILL.md`: spotting pass-through adapters vs useful isolation

Skill-pack takeaway:

Patterns are useful only when they buy locality or isolate a real dependency. Do not add pattern-shaped indirection just because the pattern exists.

### Martin Kleppmann - Designing Data-Intensive Applications

Source: https://dataintensive.net/

Use for:

- data systems and distributed boundaries
- storage, streams, transactions, consistency, and failure modes
- understanding when a dependency is not just in-process code
- operational constraints that belong in the interface contract

Maps to:

- `codebase-design/SKILL.md`: interface includes invariants, error modes, performance characteristics, and behavior contracts
- `codebase-design/DEEPENING.md`: local-substitutable, remote-owned, and true-external dependencies
- `improve-codebase-architecture/SKILL.md`: why testability and locality matter around data workflows

Skill-pack takeaway:

Interfaces are more than function signatures. Data and distributed dependencies carry durability, consistency, latency, and failure contracts that callers should not have to rediscover.

### Neal Ford and Mark Richards - Fundamentals of Software Architecture

Source: https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/

Use for:

- architectural trade-offs
- fitness functions
- coupling and cohesion
- architecture characteristics and risk
- explaining decisions in reviewable terms

Maps to:

- `improve-codebase-architecture/SKILL.md`: candidate filtering by real architectural value
- `HTML-REPORT.md`: recommendation strength and trade-off-oriented prose
- `codebase-design/DESIGN-IT-TWICE.md`: compare alternatives by risk, migration cost, test surface, and locality

Skill-pack takeaway:

Architecture is trade-offs. A report should not list generic cleanup; it should show why a candidate improves a named quality and what risk it introduces.

### Neal Ford, Rebecca Parsons, and Patrick Kua - Building Evolutionary Architectures

Source: https://www.oreilly.com/library/view/building-evolutionary-architectures/9781491986356/

Use for:

- incremental architecture change
- fitness functions
- architecture evolution without big rewrites
- validating architecture characteristics continuously

Maps to:

- `codebase-design/DEEPENING.md`: support slices and validation commands
- `codebase-design/DESIGN-IT-TWICE.md`: migration path and validation proof
- `improve-codebase-architecture/SKILL.md`: no implementation during discovery; choose one candidate to explore next

Skill-pack takeaway:

Deepening should be reachable through bounded slices. Favor candidates that can be validated and migrated incrementally.

### Matthew Skelton and Manuel Pais - Team Topologies

Source: https://teamtopologies.com/book

Use for:

- cognitive load
- team ownership boundaries
- Conway's Law and flow
- platform/enabling/stream-aligned responsibilities

Maps to:

- `codebase-design/SKILL.md`: locality and AI-navigability
- `improve-codebase-architecture/SKILL.md`: fresh-agent navigation as an architectural signal
- `HTML-REPORT.md`: explain why scattered ownership costs future work

Skill-pack takeaway:

AI-navigability is a form of cognitive-load management. A deep module with clear ownership makes future human and agent work easier to route.

## Visual And Reporting References

### Simon Brown - Software Architecture for Developers / C4 Model

Source: https://c4model.com/

Use for:

- visualizing architecture at useful levels of abstraction
- choosing diagram scope intentionally
- communicating structure without over-modeling

Maps to:

- `improve-codebase-architecture/HTML-REPORT.md`: before/after diagrams, dependency flow, call-graph collapse
- `improve-codebase-architecture/SKILL.md`: report candidates visually instead of settling final interfaces in prose

Skill-pack takeaway:

Architecture diagrams should answer a question at the right level. The HTML report should make friction visible, not decorate the review.

### Edward Tufte - The Visual Display of Quantitative Information

Source: https://www.edwardtufte.com/tufte/books_vdqi

Use for:

- high signal-to-noise visual explanation
- avoiding chartjunk and decorative complexity
- letting visuals carry the argument

Maps to:

- `HTML-REPORT.md`: lean editorial style, sparse prose, diagrams as centerpiece

Skill-pack takeaway:

The report should make the architecture legible. If a candidate needs a long paragraph, redraw the diagram.

## Concept Map By File

### `codebase-design/SKILL.md`

Primary concepts:

- module, interface, implementation
- depth as leverage
- shallow modules and pass-through helpers
- seam and adapter discipline
- interface as test surface
- deletion test
- locality and testability

Best sources:

- Ousterhout for deep modules and design-it-twice
- Parnas for information hiding
- Feathers for seams
- Evans for domain ownership
- GOOS for tests as design pressure

### `codebase-design/DEEPENING.md`

Primary concepts:

- dependency categories: in-process, local-substitutable, remote-owned, true-external
- seam placement by dependency shape
- adapter/fake/stub/mock strategy
- test migration toward deeper interfaces
- coverage parity without preserving bad shallow tests

Best sources:

- Feathers for seams
- Fowler EAA for gateways and infrastructure boundaries
- Kleppmann for distributed and data-system contracts
- GOOS for test doubles at real boundaries
- Evolutionary Architecture for incremental support slices

### `codebase-design/DESIGN-IT-TWICE.md`

Primary concepts:

- first plausible interface is rarely best
- generate meaningfully different alternatives
- compare by depth, locality, caller ergonomics, seam placement, test surface, migration cost, and risk
- recommend one design and the first safe migration step

Best sources:

- Ousterhout for design-it-twice
- Ford/Richards for trade-offs and architecture characteristics
- Evans for domain-owned alternatives
- Evolutionary Architecture for migration and validation

### `improve-codebase-architecture/SKILL.md`

Primary concepts:

- discover deepening candidates
- filter out generic cleanup
- use domain and architecture vocabulary
- produce a visual HTML report outside the repo
- ask the user which candidate to explore
- grill the chosen candidate before design/implementation

Best sources:

- Ousterhout for shallow/deep module detection
- Parnas for decision-hiding modules
- Team Topologies for cognitive load and navigability
- Ford/Richards for architectural trade-offs
- Simon Brown for visual architecture communication

### `improve-codebase-architecture/HTML-REPORT.md`

Primary concepts:

- diagrams carry the weight
- before/after visual proof
- lean editorial prose
- consistent architecture vocabulary
- recommendation strength and top recommendation
- dark, static, self-contained report

Best sources:

- Simon Brown for architectural visualization
- Tufte for visual clarity and signal-to-noise
- Ousterhout for depth diagrams and interface/implementation comparison

## Practical North Star

The skills are in the right direction when they produce recommendations that:

- identify a real shallow module, leaky seam, scattered decision, or pass-through adapter
- explain the friction with domain terms and shared architecture vocabulary
- show how callers learn less after the change
- move behavior behind a smaller useful interface
- place seams only where behavior genuinely varies
- use adapters, fakes, stubs, or mocks only when the dependency shape justifies them
- prove behavior through the same interface callers use
- preserve bounded slices and avoid speculative rewrites
- make the candidate visible enough that the user can choose what to explore next

The goal is not prettier architecture. The goal is leverage, locality, testability, and navigability through deeper modules.
