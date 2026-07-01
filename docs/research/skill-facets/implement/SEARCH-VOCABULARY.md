# Implement Search Vocabulary

Use this file as optional search support for `implement` facet research.

The reusable research workflow lives in `../FACET-RESEARCH-PROMPT.md`. The implement-specific facet map lives in `README.md`. This file is only for keywords, exact queries, source anchors, and noise filters that may be reused across multiple implement facets.

Use these terms to find sources. Search by facet, not all at once. Prefer exact phrases first, then broaden.

### 1. Bounded Slice

Seed terms:

- `vertical slice`
- `tracer bullet`
- `walking skeleton`
- `thin slice`
- `small batch`
- `single piece flow`
- `work in progress limit`
- `WIP limit`
- `minimum marketable feature`
- `minimum viable change`
- `user story slicing`
- `story splitting`
- `outside-in development`
- `end-to-end slice`
- `incremental delivery`
- `continuous delivery`
- `lean software development`
- `flow efficiency`
- `batch size`

Exact phrase queries:

- `"vertical slice" software development`
- `"tracer bullet" software development`
- `"walking skeleton" agile architecture`
- `"thin slice" user story`
- `"story splitting" acceptance criteria`
- `"small batch" software delivery`
- `"work in progress limits" software development`
- `"single piece flow" software development`
- `"minimum marketable feature" agile`
- `"end-to-end" "vertical slice"`
- `"continuous delivery" "small batches"`

Search with source anchors:

- `"vertical slice" "Growing Object-Oriented Software"`
- `"walking skeleton" "Alistair Cockburn"`
- `"tracer bullets" "The Pragmatic Programmer"`
- `"story splitting" "INVEST"`
- `"small batches" "Continuous Delivery"`
- `"WIP limits" "Kanban"`

Noise filters:

- Avoid project-management-only sources that never reach implementation behavior.
- Avoid "MVP" sources that discuss product launch strategy but not engineering slice size.

### 2. Baseline And Fixed Point

Seed terms:

- `fixed point`
- `baseline`
- `clean working tree`
- `dirty working tree`
- `change isolation`
- `atomic commit`
- `logical commit`
- `small commit`
- `commit hygiene`
- `branch hygiene`
- `pull request size`
- `reviewable diff`
- `diff review`
- `pre-commit check`
- `continuous integration`
- `CI gate`
- `trunk based development`
- `feature branch`
- `merge discipline`
- `revertability`
- `bisectability`

Exact phrase queries:

- `"atomic commits" software engineering`
- `"logical commits" code review`
- `"small commits" code review`
- `"reviewable diff" code review`
- `"pull request size" code review`
- `"change isolation" software engineering`
- `"clean working tree" git workflow`
- `"git bisect" "small commits"`
- `"trunk based development" "small batches"`
- `"continuous integration" "commit"`

Search with source anchors:

- `"atomic commits" "Version Control with Git"`
- `"trunk based development" "Continuous Delivery"`
- `"small commits" "Google Engineering Practices"`
- `"code review" "Google Engineering Practices"`
- `"revert" "Accelerate" software delivery`

Noise filters:

- Avoid Git tutorials that only explain commands.
- Prefer sources that connect baseline discipline to review, rollback, or debugging.

### 3. Exploration Before Choice

Seed terms:

- `spike solution`
- `technical spike`
- `architectural spike`
- `discovery spike`
- `evolutionary design`
- `last responsible moment`
- `set-based design`
- `option thinking`
- `real options`
- `decision point`
- `uncertainty reduction`
- `exploratory programming`
- `throwaway prototype`
- `prototype to learn`
- `design spike`
- `trade-off analysis`
- `fitness function`
- `local design`
- `simple design`

Exact phrase queries:

- `"spike solution" agile`
- `"technical spike" software development`
- `"evolutionary design" software`
- `"last responsible moment" software`
- `"set-based design" software`
- `"real options" software architecture`
- `"uncertainty reduction" software development`
- `"throwaway prototype" software engineering`
- `"prototype" "answer a question" software`
- `"simple design" "Kent Beck"`

Search with source anchors:

- `"spike solution" "Extreme Programming"`
- `"last responsible moment" "Lean Software Development"`
- `"set-based design" "Lean Software Development"`
- `"evolutionary design" "Martin Fowler"`
- `"simple design" "Extreme Programming Explained"`

Noise filters:

- Avoid broad product-discovery writing unless it gives an implementation gate.
- Avoid architecture astronomy: keep sources tied to choosing the next local change.

### 4. Commitment Boundary

Seed terms:

- `requirements ownership`
- `product owner`
- `acceptance criteria`
- `definition of ready`
- `definition of done`
- `scope creep`
- `change control`
- `decision record`
- `architecture decision record`
- `ADR`
- `user story`
- `out of scope`
- `nonfunctional requirement`
- `quality attribute`
- `public contract`
- `API contract`
- `data contract`
- `semantic contract`
- `security requirement`
- `privacy requirement`
- `migration semantics`

Exact phrase queries:

- `"acceptance criteria" "definition of done"`
- `"definition of ready" user story`
- `"scope creep" software requirements`
- `"architecture decision record" software`
- `"public contract" API design`
- `"data contract" software engineering`
- `"nonfunctional requirements" "quality attributes"`
- `"requirements engineering" "acceptance criteria"`
- `"product owner" "acceptance criteria"`
- `"out of scope" requirements`

Search with source anchors:

- `"architecture decision records" "Michael Nygard"`
- `"quality attribute" "Software Architecture in Practice"`
- `"requirements" "Software Requirements" Wiegers`
- `"acceptance criteria" "Specification by Example"`
- `"definition of done" Scrum Guide`

Noise filters:

- Avoid generic Agile glossaries unless they define a concrete stop/ask rule.
- Prefer sources that separate implementation technique from product commitment.

### 5. Semantic Proof

Seed terms:

- `semantic correctness`
- `correctness`
- `executable specification`
- `specification by example`
- `acceptance test`
- `acceptance testing`
- `example mapping`
- `behavior-driven development`
- `BDD`
- `test-driven development`
- `TDD`
- `red green refactor`
- `characterization test`
- `approval test`
- `golden master test`
- `property-based testing`
- `invariant`
- `oracle`
- `test oracle`
- `fixture`
- `known input output`
- `data validation`
- `metamorphic testing`
- `regression test`

Exact phrase queries:

- `"semantic correctness" software testing`
- `"specification by example" acceptance tests`
- `"executable specification" software`
- `"acceptance test" "business rule"`
- `"example mapping" BDD`
- `"red green refactor" TDD`
- `"characterization tests" legacy code`
- `"approval testing" golden master`
- `"property-based testing" invariants`
- `"test oracle" software testing`
- `"metamorphic testing" software testing`
- `"data validation" "known input output"`

Search with source anchors:

- `"Specification by Example" "Gojko Adzic"`
- `"Test-Driven Development by Example" "Kent Beck"`
- `"Growing Object-Oriented Software" acceptance tests`
- `"Working Effectively with Legacy Code" characterization tests`
- `"xUnit Test Patterns" test oracle`
- `"property-based testing" "Hypothesis"`

Noise filters:

- Avoid test taxonomy sources that do not say how proof changes implementation behavior.
- Prefer examples that connect tests to user-visible behavior or data semantics.

### 6. Seams And Interfaces

Seed terms:

- `seam`
- `software seam`
- `interface`
- `information hiding`
- `deep module`
- `module depth`
- `encapsulation`
- `ports and adapters`
- `hexagonal architecture`
- `adapter`
- `contract test`
- `collaboration test`
- `classicist TDD`
- `mockist TDD`
- `sociable test`
- `solitary test`
- `test surface`
- `public interface`
- `owned dependency`
- `fake`
- `stub`
- `mock`
- `dependency inversion`
- `boundary`

Exact phrase queries:

- `"software seam" "Working Effectively with Legacy Code"`
- `"information hiding" "Parnas"`
- `"deep module" software design`
- `"module depth" software design`
- `"ports and adapters" testing`
- `"hexagonal architecture" "Alistair Cockburn"`
- `"contract tests" ports adapters`
- `"classicist TDD" mockist`
- `"sociable tests" TDD`
- `"test through public interface"`
- `"don't mock what you own"`

Search with source anchors:

- `"A Philosophy of Software Design" "deep modules"`
- `"On the Criteria To Be Used in Decomposing Systems into Modules"`
- `"Working Effectively with Legacy Code" seams`
- `"Growing Object-Oriented Software" mock objects`
- `"xUnit Test Patterns" fake stub mock`
- `"Clean Architecture" boundaries`

Noise filters:

- Avoid interface discussions that only mean programming-language signatures.
- Prefer sources that connect interface choice to testing and change locality.

### 7. Simplification While Protected

Seed terms:

- `refactoring`
- `green refactor`
- `refactor only when green`
- `behavior preserving`
- `behavior-preserving refactor`
- `simple design`
- `YAGNI`
- `remove duplication`
- `dead code removal`
- `deletion`
- `opportunistic refactoring`
- `preparatory refactoring`
- `parallel change`
- `branch by abstraction`
- `strangler fig`
- `characterization test`
- `safe refactoring`
- `code smell`
- `technical debt`
- `locality`
- `cohesion`
- `coupling`

Exact phrase queries:

- `"refactor only when green"`
- `"behavior preserving" refactoring`
- `"preparatory refactoring" software`
- `"opportunistic refactoring" software`
- `"parallel change" refactoring`
- `"branch by abstraction" refactoring`
- `"simple design" "remove duplication"`
- `"YAGNI" software design`
- `"safe refactoring" tests`
- `"code smells" refactoring`

Search with source anchors:

- `"Refactoring" "Martin Fowler"`
- `"Refactoring to Patterns" Kerievsky`
- `"Working Effectively with Legacy Code" "sprout method"`
- `"Extreme Programming Explained" simple design`
- `"Growing Object-Oriented Software" refactoring`

Noise filters:

- Avoid broad cleanup advice that encourages widening the slice.
- Prefer sources that require behavior preservation and a safety net.

### 8. Review And Lock

Seed terms:

- `code review`
- `code review checklist`
- `pull request review`
- `reviewable change`
- `definition of done`
- `done criteria`
- `release readiness`
- `change log`
- `implementation note`
- `handoff`
- `residual risk`
- `risk register`
- `evidence`
- `verification evidence`
- `validation evidence`
- `traceability`
- `requirements traceability`
- `audit trail`
- `commit message`
- `conventional commits`
- `change summary`
- `rollback plan`
- `post-implementation review`

Exact phrase queries:

- `"code review" "small changes"`
- `"code review checklist" software`
- `"reviewable change" software`
- `"definition of done" software development`
- `"implementation note" software`
- `"residual risk" software release`
- `"requirements traceability" software`
- `"verification evidence" software`
- `"commit message" "why"`
- `"pull request description" "testing"`
- `"rollback plan" software release`

Search with source anchors:

- `"Google Engineering Practices" "code review"`
- `"SmartBear" "code review"`
- `"Continuous Delivery" deployment pipeline`
- `"Accelerate" software delivery performance`
- `"Conventional Commits" specification`
- `"Keep a Changelog"`

Noise filters:

- Avoid style-only review checklists.
- Prefer sources that separate Spec correctness from Standards/convention review.

## Cross-Facet Search Terms

Use these when the facet-specific search is too narrow:

- `implementation discipline`
- `engineering discipline`
- `software delivery discipline`
- `working in small steps`
- `incremental software development`
- `evolutionary architecture`
- `agile engineering practices`
- `extreme programming practices`
- `continuous delivery practices`
- `software craftsmanship`
- `high quality software engineering`
- `maintainable software design`
- `evidence-based software engineering`
- `verification and validation software`
- `agentic coding`
- `coding agents`
- `AI coding assistant workflow`
- `LLM coding agent evaluation`
- `LLM software engineering`
- `automated program repair`
- `AI pair programming`
- `human in the loop software engineering`

Use agentic terms only as a bridge. The core behavior should usually come from software engineering sources, then translate into agent gates.

## Query Construction Patterns

Combine terms like this:

```text
"<practice term>" software engineering
"<practice term>" code review
"<practice term>" continuous delivery
"<practice term>" TDD
"<practice term>" acceptance criteria
"<practice term>" site:martinfowler.com
"<practice term>" site:agilealliance.org
"<practice term>" site:google.github.io/eng-practices
"<practice term>" book
"<practice term>" paper
"<practice term>" pdf
```

For LLM/agent bridging:

```text
"coding agent" "code review"
"LLM" "software engineering" "unit tests"
"AI coding assistant" "pull request"
"LLM agents" "software engineering" "benchmark"
"program repair" "test suite"
"agentic coding" "workflow"
```

Do not keep a source merely because it matches a keyword. Keep it only if it can improve `implement` as a compact action, gate, or stop rule.

## Source Quality Bar

Prefer sources that are durable, practical, and respected by working programmers:

- widely used books, papers, manuals, or official docs;
- professional curriculum staples;
- sources with concrete practices rather than vibes;
- sources whose vocabulary can collapse a paragraph into a strong attention handle.

Avoid sources that only say "be careful", "write good code", or "communicate well" without an operational gate.
