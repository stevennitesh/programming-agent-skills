# Issue Pipeline Family Synthesis

This note maps the books and supporting references behind the local issue pipeline skills:

- `skills/custom/to-spec/SKILL.md`
- `skills/custom/to-tickets/SKILL.md`
- `skills/custom/triage/SKILL.md`
- `skills/custom/triage/ATTENTION-SCAN.md`
- `skills/custom/triage/SPECIFIC-ITEM.md`
- `skills/custom/triage/QUICK-OVERRIDE.md`
- `skills/custom/triage/AGENT-BRIEF.md`
- `skills/custom/triage/OUT-OF-SCOPE.md`
- `skills/custom/implement/SKILL.md`
- `skills/custom/review/SKILL.md`

The local skill-pack stance is: turn messy intent into durable product understanding, split that understanding into dependency-ordered bounded slices, convert raw outside requests into the same ready-for-agent shape, implement exactly one ready slice at a time, and review the result against both repo standards and the originating spec.

## Primary Sources

### Andrew Hunt and David Thomas - The Pragmatic Programmer

Source: https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/

Use for:

- tracer bullets
- real end-to-end feedback
- avoiding speculative build plans
- learning from thin working paths through the system

Maps to:

- `to-tickets/SKILL.md`: tracer-bullet issues for product behavior
- `implement/SKILL.md`: one bounded slice through existing seams
- `review/SKILL.md`: checking whether the diff completes the intended slice

Skill-pack takeaway:

A good implementation issue should behave like a tracer bullet: one narrow real path through the system that proves behavior, a seam, or a risk.

### Jeff Patton - User Story Mapping

Source: https://jpattonassociates.com/story-mapping/

Use for:

- preserving the whole product story
- turning fuzzy product intent into slices
- slicing by user-visible behavior
- keeping parent context separate from implementation tasks

Maps to:

- `to-spec/SKILL.md`: parent spec as full explored understanding
- `to-tickets/SKILL.md`: dependency-ordered issues with parent references
- `to-tickets/SKILL.md`: fewer strong tracer bullets over many weak variations

Skill-pack takeaway:

The parent spec keeps the whole story visible; issues are slices through that story, not a flat backlog of layers.

### Gojko Adzic - Specification by Example

Source: https://www.manning.com/books/specification-by-example

Use for:

- concrete examples as requirements
- executable behavior specifications
- shared understanding across product and engineering
- acceptance criteria that are observable and testable

Maps to:

- `to-spec/SKILL.md`: testing notes that identify observable behavior
- `to-tickets/SKILL.md`: specific observable acceptance criteria
- `triage/AGENT-BRIEF.md`: complete acceptance criteria and validation notes
- `review/SKILL.md`: Spec axis findings for missing or weak behavior proof

Skill-pack takeaway:

Acceptance criteria are behavior contracts. They should tell a fresh implementation session what observable proof makes the slice done.

### Steve Freeman and Nat Pryce - Growing Object-Oriented Software, Guided by Tests

Source: https://growing-object-oriented-software.com/

Use for:

- walking skeleton
- outside-in development
- growing software through tested behavior
- using interfaces to discover responsibility boundaries

Maps to:

- `implement/SKILL.md`: identify the highest useful interface or seam to test through
- `to-tickets/SKILL.md`: tracer bullets that cross every layer needed for one behavior
- `triage/AGENT-BRIEF.md`: validation notes for proving behavior through the right seam

Skill-pack takeaway:

Implementation should grow from a real behavior path, not from horizontal layer completion. Tests and interfaces expose whether the slice is shaped correctly.

### Jez Humble and David Farley - Continuous Delivery

Source: https://martinfowler.com/books/continuousDelivery.html

Use for:

- keeping software releasable
- automated feedback
- build and test pipelines
- confidence from repeatable validation

Maps to:

- `implement/SKILL.md`: focused checks, full validation when feasible, and recorded skipped checks
- `review/SKILL.md`: fixed-point review of the produced diff
- `triage/AGENT-BRIEF.md`: validation notes as part of the ready-for-agent contract

Skill-pack takeaway:

The issue pipeline is not done when code is written. A slice is done when validation creates enough confidence to commit and hand off.

### Martin Fowler - Refactoring

Source: https://martinfowler.com/books/refactoring.html

Use for:

- behavior-preserving structural change
- small safe design moves
- separating refactoring from feature work
- tests as guardrails

Maps to:

- `to-tickets/SKILL.md`: support issues for behavior-preserving prefactoring
- `implement/SKILL.md`: avoid widening one bounded slice
- `review/SKILL.md`: scope-creep findings when a diff adds unrelated behavior

Skill-pack takeaway:

Support slices are allowed when they unblock or de-risk behavior, but they must stay behavior-preserving and independently verifiable.

### Michael Feathers - Working Effectively with Legacy Code

Source: https://martinfowler.com/bliki/LegacySeam.html

Use for:

- seam vocabulary
- safely changing existing systems
- getting hard-to-test behavior under control
- identifying useful points of variation

Maps to:

- `to-spec/SKILL.md`: seams to test through
- `to-tickets/SKILL.md`: likely test surface and useful prefactoring
- `implement/SKILL.md`: prefer existing seams and avoid guesswork
- `review/SKILL.md`: missing or weak tests when acceptance criteria are not proven through the right seam

Skill-pack takeaway:

Existing code changes need a trustworthy seam. The pipeline should name where behavior can be proved before implementation starts.

### David J. Anderson - Kanban

Source: https://shop.leankanban.com/products/kanban-successful-evolutionary-change-for-your-technology-business-print

Use for:

- explicit work states
- flow management
- limiting work in progress
- service policies and queues

Maps to:

- `triage/SKILL.md`: issue state machine
- `triage/SKILL.md`: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`
- `implement/SKILL.md`: choose the next unblocked ready-for-agent issue

Skill-pack takeaway:

Triage labels are not decoration. They are explicit policies that control when an issue can move through the pipeline.

## Supporting References

### Mark Denne and Jane Cleland-Huang - Software by Numbers

Source: https://www.informit.com/store/software-by-numbers-low-risk-high-return-development-9780131407282

Use for:

- minimum marketable features
- incremental value delivery
- small units of investment
- sequencing work by value and risk

Maps to:

- `to-tickets/SKILL.md`: bounded, independently verifiable slices
- `triage/AGENT-BRIEF.md`: why this slice

Skill-pack takeaway:

Each ready issue should justify why it is the right bounded investment now.

### Mike Cohn - User Stories Applied

Source: https://www.mountaingoatsoftware.com/books/user-stories-applied

Use for:

- user stories
- acceptance criteria
- splitting user-facing functionality
- conversation around requirements

Maps to:

- `to-spec/SKILL.md`: user story format
- `to-tickets/SKILL.md`: issue titles and behavior descriptions
- `triage/SKILL.md`: grilling raw requests until they can move to a state role

Skill-pack takeaway:

User stories are placeholders for shared understanding. The pipeline turns that understanding into bounded, verifiable implementation work.

### Richard Rumelt - The Crux

Source: https://www.publicaffairsbooks.com/titles/richard-p-rumelt/the-crux/9781541701267/

Use for:

- finding the pivotal challenge
- distinguishing important blockers from noise
- focusing effort on the next obstacle

Maps to:

- `to-tickets/SKILL.md`: blockers and dependency order
- `triage/SKILL.md`: recommend the state with reasoning
- `implement/SKILL.md`: stop after one issue

Skill-pack takeaway:

Dependency order should expose the next real constraint. Do not split work into many issues that fail to identify what must happen first.

## Concept Map By File

### `to-spec/SKILL.md`

Primary concepts:

- synthesis, not grilling
- parent spec
- full explored idea
- user-visible desired outcome
- accepted decisions and rejected options
- edge cases and failure modes
- testing notes and seams
- out-of-scope boundaries

Best sources:

- User Story Mapping for preserving the whole story
- User Stories Applied for story shape
- Specification by Example for behavior-oriented testing notes

### `to-tickets/SKILL.md`

Primary concepts:

- dependency-ordered implementation issues
- independently pick-up-able bounded slices
- tracer bullets for product behavior
- support issues only when they unblock or de-risk
- observable acceptance criteria
- blockers
- parent references instead of duplicated spec context

Best sources:

- The Pragmatic Programmer for tracer bullets
- User Story Mapping for slicing the story
- Software by Numbers for small value increments
- Refactoring for support slices

### `triage/SKILL.md`

Primary concepts:

- category roles: `bug`, `enhancement`
- state roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`
- redundancy check
- prior rejection check
- claim verification
- grilling only when needed
- AI triage disclaimer
- out-of-scope knowledge base

Best sources:

- Kanban for explicit workflow states
- User Stories Applied for turning requests into shared understanding
- Specification by Example for actionable acceptance criteria

### `triage/AGENT-BRIEF.md`

Primary concepts:

- Codex-ready brief
- one bounded slice
- durable over procedural
- current behavior and desired behavior
- why this slice
- relevant interfaces or seams
- acceptance criteria
- validation notes
- out of scope

Best sources:

- Specification by Example for behavior contracts
- The Pragmatic Programmer for tracer-bullet thinking
- Working Effectively with Legacy Code for seam-aware validation

### `implement/SKILL.md`

Primary concepts:

- one ready-for-agent issue
- starting ref
- preserve unrelated work
- one bounded slice
- focused checks
- acceptance-criteria verification
- review against starting ref
- implementation note

Best sources:

- Growing Object-Oriented Software for walking skeleton and outside-in implementation
- Continuous Delivery for validation and releasable flow
- Refactoring for not widening the slice

### `review/SKILL.md`

Primary concepts:

- fixed point
- Standards axis
- Spec axis
- actionable findings only
- no merged reranking across axes
- missing requirements
- scope creep
- weak tests against acceptance criteria

Best sources:

- Specification by Example for spec fidelity
- Continuous Delivery for confidence before integration
- Refactoring for behavior-preserving change boundaries

## Practical North Star

The issue pipeline is in the right direction when it:

- preserves intent from spec to issue to brief to implementation note
- slices by observable behavior, not horizontal layers
- prefers tracer bullets over broad support work
- records out-of-scope boundaries before implementation starts
- marks raw work with explicit triage states
- gives Codex-ready issues concrete acceptance criteria and validation notes
- implements one ready slice per session
- reviews against a fixed point and a real spec source

The goal is not more process. The goal is contract preservation across handoffs: every stage should make the next stage easier to execute without rediscovering the problem.
