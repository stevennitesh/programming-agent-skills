# Prompt 02: Implement Facet Map And Research Plan

Durable upstream source and reconstruction: [`UPSTREAM-SOURCE.md`](../../language/UPSTREAM-SOURCE.md).

This executes
[`docs/synthesis/methods/prompts/02-facet-map-and-research-plan.md`](../../../synthesis/methods/prompts/02-facet-map-and-research-plan.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Step 1 output:
[`docs/research/skill-facets/implement/01-intent-and-keywords.md`](01-intent-and-keywords.md)

User goal for this skill: run Prompt 02 for the refreshed `implement` Prompt 01
output, including the `.tmp/mattpocock-skills` source contrast, so the next
source-search pass starts from a clean facet map with current owner boundaries.

Revision feedback:

- Use the new Prompt 01 output that analyzed both the current repo-local skill
  and `.tmp/mattpocock-skills/skills/engineering/implement/SKILL.md`.
- Use three subagents to stress-test facet shape, owner boundaries, and source
  planning.

Subagent inputs used:

- Facet-map challenge: considered merging `Bounded Slice Control` with
  `Commitment Boundary`, recommended merging proof/seams, and deferred
  invocation shape.
- Boundary stress test: confirmed `implement` must not take over `to-issues`,
  `triage`, `$tdd`, `$review`, `codebase-design`, repo docs, or the engineering
  contract.
- Source/search planning: confirmed `Ready Issue Selection` as the first
  source-search facet and supplied source lanes, vocabulary, evidence gates, and
  noisy lanes.

Constraints:

- Do not research online yet.
- Do not rewrite `skills/custom/implement/SKILL.md`.
- Do not propose final runtime wording yet.
- Choose the research structure before source search.

## 1. Skill Research Objective

Research should make `implement` more predictable at taking exactly one ready
issue through a bounded, proven, reviewed, committed implementation slice. The
`.tmp/mattpocock-skills` source skill is useful source pressure for the minimum
TDD/check/review/commit spine, but this research must preserve the current
repo-local executor shape: one ready issue, repo docs, baseline, context intake,
slice control, proof, review, commit, and note.

The quality bar is source pressure that can become agent behavior, evidence
gates, and stop/ask rules without duplicating `to-issues`, `triage`, `$tdd`,
`$review`, `codebase-design`, or the engineering contract.

The one-issue WIP limit, explicit-only invocation, tracker/domain routing,
dirty-work preservation, downstream `$tdd` / `$review` ownership, and issue
state restraint must not regress. Over-research means collecting generic Agile,
testing, Git, or review advice that does not change how the agent selects,
orients, bounds, proves, simplifies, locks, or stops during one implementation
run.

## 2. Step 1 Carry-Forward Audit

| Step 1 Input | Used / Revised / Deferred / Blocked | Where It Shows Up | Notes |
| --- | --- | --- | --- |
| Skill intent and current behavior surface | Used | Final facet map and research order | The map follows the actual `implement` execution surface: select one ready issue, baseline, intake, slice control, commitment boundary, proof, simplification, lock. |
| Upstream `.tmp` source contrast | Used | Skill objective, source lanes, merge ledger, and cross-facet risks | The compact source skill keeps the proof/check/review/commit spine visible, but does not replace current ready-issue selection, tracker routing, baseline, context, note, or state-restraint behavior. |
| Owner map | Used | Facet boundaries and collision map | `to-issues`, `triage`, `$tdd`, `$review`, `codebase-design`, tracker docs, domain docs, and the engineering contract are treated as owner boundaries. |
| Preserve inventory | Used | Evidence gates and final facet boundaries | Explicit-only invocation, one-issue limit, dirty-tree baseline, domain routing, TDD handoff, fixed-point review, commit/note, and issue-state restraint are all preserve constraints. |
| Rough facet candidates | Revised | Final facet map | `Ready Issue Selection` stays first. `Semantic Proof` and `Seams And Load-Bearing Internals` are merged because both shape one runtime behavior: proving correctness through the right seam. `Invocation And Skill Shape` is deferred to final compression instead of source research. |
| Facet collision risks | Used | Cross-facet collision map | Prompt 02 resolves the major collisions instead of leaving them implicit: readiness vs context, baseline vs lock, proof vs seam, and commitment boundary as a cross-cutting stop rule. |
| Source search seeds and noisy lanes | Used / Revised | Source lanes and vocabulary by facet | Seeds were regrouped by final ownership. Generic Agile, Git tutorials, unit-test taxonomy, and style-only review material remain demoted. |
| Questions for Prompt 02 | Used | Merge / split / retire ledger | Questions are answered explicitly: ready issue selection stays separate; baseline and lock stay separate; context stops at implementation readiness; commitment boundary stays separate; proof and seam guidance merge; invocation shape is deferred. |

## 3. Final Facet Map

| Order | Facet | Behavior Surface | Research Question | Why It Matters | Output Artifact |
| --- | --- | --- | --- | --- | --- |
| 1 | Ready Issue Selection | invocation, named issue precedence, PRD/spec handoff, ready-label selection, blocker/ambiguity/no-issue stop | How should `implement` select exactly one ready issue or stop when no safe issue is available? | The skill cannot do the rest of the loop safely until it has one concrete issue-equivalent slice, not a PRD, queue, or ambiguous set. | `docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md` |
| 2 | Baseline And Fixed Point | dirty work, starting ref, staging boundary, change isolation | What must the agent establish before editing so unrelated work is preserved and review/commit remain trustworthy? | A weak baseline poisons `$review`, commit scope, and implementation notes. | `docs/research/skill-facets/implement/FACET-2-BASELINE-AND-FIXED-POINT-sources.md` |
| 3 | Context Intake | issue/spec reading, comments, parent source, domain vocabulary, acceptance criteria, blockers, non-goals | What must the agent understand before editing so implementation is not guesswork? | `implement` should not redo triage, but it must verify that the chosen ready issue has enough actionable context to execute. | `docs/research/skill-facets/implement/FACET-3-CONTEXT-INTAKE-sources.md` |
| 4 | Bounded Slice Control | scope boundary, tracer-bullet/support distinction, adjacent work, failed proof, follow-ups | How should one implementation run stay small, valuable, independently provable, and reviewable? | This prevents a ready issue from becoming broad cleanup, adjacent behavior, or several implementation slices at once. | `docs/research/skill-facets/implement/FACET-4-BOUNDED-SLICE-CONTROL-sources.md` |
| 5 | Commitment Boundary | ask/stop rules, autonomous technique, user-owned decisions, changed commitments | Which decisions can the agent make inside the slice, and which changes require stopping or asking? | The agent needs room to choose technique without silently changing product intent, contracts, data/security semantics, or the slice itself. | `docs/research/skill-facets/implement/FACET-5-COMMITMENT-BOUNDARY-sources.md` |
| 6 | Semantic Proof And Seams | semantic correctness, proof surface, `$tdd` handoff, seam choice, load-bearing internals, skipped checks | What proves the selected issue is correct, and how should `implement` choose a meaningful seam without duplicating `$tdd` or `codebase-design`? | Proof and seam choice are one behavior in this skill: demonstrate the right semantics through the highest useful boundary. | `docs/research/skill-facets/implement/FACET-6-SEMANTIC-PROOF-AND-SEAMS-sources.md` |
| 7 | Protected Simplification | simplification, refactor, cleanup, scratch disposal, behavior protection | How should the agent simplify after proof without widening the issue or changing behavior? | `implement` should allow useful cleanup while behavior is protected, not convert one issue into a cleanup campaign. | `docs/research/skill-facets/implement/FACET-7-PROTECTED-SIMPLIFICATION-sources.md` |
| 8 | Review And Lock | `$review`, in-scope findings, commit, implementation note, validation record, skipped checks, residual risk, issue-state restraint | What makes the result ready to hand off after implementation: reviewed, committed, noted, and honest about residual risk? | The final phase is where agents often overclaim, skip evidence, commit too broadly, or change issue state casually. | `docs/research/skill-facets/implement/FACET-8-REVIEW-AND-LOCK-sources.md` |

## 4. Facet Boundaries

### Facet 1: Ready Issue Selection

Owns:

- How `implement` chooses exactly one issue when the user names an issue, path,
  URL, PRD, spec, or nothing.
- How to treat `ready-for-agent`, blockers, dependency order, ambiguity, and no
  available issue.
- The local readiness recheck needed before taking ownership of a selected
  issue.

Does not own:

- Creating issues from PRDs/specs; `to-issues` owns that.
- Moving issues into `ready-for-agent`; `triage` owns that.
- Tracker commands and label strings; repo tracker docs own those.
- Reading full implementation context after selection; Context Intake owns
  that.

Research should answer:

- What source pressure supports one-at-a-time pull discipline?
- What is the smallest readiness check `implement` should run before taking an
  issue?
- When should the agent ask, skip, or stop instead of selecting automatically?

Research should not answer:

- How to write Codex-ready briefs.
- How to triage raw issues.
- How to implement the selected issue.

### Facet 2: Baseline And Fixed Point

Owns:

- What the agent must inspect before editing.
- How to preserve unrelated dirty work.
- How to capture a starting ref for `$review`.
- How to keep staging and commit scope tied to the selected issue.

Does not own:

- The full `$review` procedure.
- PR publication, merge, or release workflows.
- General Git tutorials that do not affect agent behavior.
- Final implementation-note content beyond baseline/fixed-point evidence.

Research should answer:

- What baseline facts must be known before edits start?
- How do teams keep diffs reviewable when worktrees are dirty?
- What wording makes the fixed point feel load-bearing rather than optional?

Research should not answer:

- How to run every possible Git workflow.
- How to resolve unrelated dirty changes.
- How to implement `$review`.

### Facet 3: Context Intake

Owns:

- What issue/spec/comment/parent/context the agent must read before coding.
- How to detect missing acceptance criteria, blockers, non-goals, or proof
  surface.
- How domain vocabulary should carry into code, tests, notes, and commits.
- When a supposedly ready issue is not executable enough for `implement`.

Does not own:

- Writing or rewriting the Codex-ready brief; `triage` owns that.
- Splitting a PRD/spec into issues; `to-issues` owns that.
- Creating glossary terms or ADRs; `domain-modeling` owns durable domain
  memory.
- User-owned commitment changes; Commitment Boundary owns the stop rule.

Research should answer:

- What context does an implementation agent need to avoid guesswork?
- What makes acceptance criteria and validation notes executable enough?
- When should `implement` return to triage or ask for clarification?

Research should not answer:

- How to run product discovery.
- How to author every issue-template field.
- How to research external sources for the feature being implemented.

### Facet 4: Bounded Slice Control

Owns:

- What makes one selected issue a bounded implementation slice.
- How to distinguish tracer-bullet issues from support issues during execution.
- How to keep adjacent behavior, cleanup, docs, config, or refactor work from
  joining the diff accidentally.
- What to do when failed proof reveals work outside the selected slice.

Does not own:

- Selecting the ready issue; Ready Issue Selection owns that.
- User-owned commitment changes; Commitment Boundary owns that.
- Proof mechanics and seam depth; Semantic Proof And Seams owns that.
- Broad architecture or cleanup campaigns.

Research should answer:

- What source language best teaches "one useful proof-carrying slice"?
- How should the agent decide whether a discovered branch is in scope or a
  follow-up?
- What gates prevent broadening the diff after failed proof?

Research should not answer:

- How to split the original PRD into issues.
- How to implement all support work discovered during the slice.
- How to run every Agile story-splitting method.

### Facet 5: Commitment Boundary

Owns:

- Which changes require user confirmation before proceeding.
- Which implementation choices the agent can make autonomously.
- How to phrase stop/ask rules without making the agent timid.
- How to identify when the best local approach changes the selected slice.

Does not own:

- The engineering contract's repo-wide commitment definitions.
- ADR writing mechanics.
- Product-management theory beyond behavior-changing stop rules.
- Generic "ask when unsure" advice.

Research should answer:

- Which commitments are unsafe for an agent to change silently?
- Which technical choices should remain agent-owned inside the slice?
- What evidence tells the agent it crossed from technique into commitment?

Research should not answer:

- How to run a grilling session.
- How to produce a PRD.
- How to negotiate product scope outside the selected issue.

### Facet 6: Semantic Proof And Seams

Owns:

- What counts as proof that the selected issue's behavior is semantically
  correct.
- When `$tdd` should be invoked or followed.
- How to choose the highest useful proof seam.
- How to treat load-bearing internals that determine correctness.
- How to report skipped checks and residual risk.

Does not own:

- The full red-green-refactor procedure; `$tdd` owns it.
- Full module/interface design guidance; `codebase-design` owns it.
- Full test examples, mocking taxonomy, or repo-specific test frameworks.
- Fixed-point review findings; `$review` owns them.

Research should answer:

- How do sources distinguish output existence from semantic correctness?
- What proof shapes work for behavior, data, config, docs, and support slices?
- What makes a seam useful enough for one implementation slice?
- What handoff language keeps `implement` from weakening `$tdd` or duplicating
  `codebase-design`?

Research should not answer:

- How to write all possible tests.
- How to redesign the module graph.
- How to test private helpers by default.

### Facet 7: Protected Simplification

Owns:

- When simplification is allowed inside one implementation issue.
- What proof must protect cleanup/refactor moves.
- How to distinguish in-scope simplification from a separate support slice.
- How to dispose of exploration scaffolding and scratch artifacts.

Does not own:

- Broad codebase cleanup campaigns.
- Architecture review or deepening candidate discovery.
- Behavior changes not required by the selected issue.
- Full refactoring catalogs.

Research should answer:

- When does cleanup help the slice versus widen it?
- What gates keep refactoring behavior-preserving?
- What should happen to scratch/prototype artifacts before lock?

Research should not answer:

- How to clean an entire repository.
- Which refactoring pattern to use in every case.
- How to rewrite architecture-review or cleanup skills.

### Facet 8: Review And Lock

Owns:

- What must be true before the agent can commit and call the issue
  implemented.
- How to use `$review` as a gate without duplicating its body.
- What an implementation note must preserve for maintainers and future agents.
- How to record validation, skipped checks, residual risk, and issue-state
  restraint.

Does not own:

- Full Standards/Spec review mechanics.
- PR publication, merge, or release workflows.
- Issue-closing rules unless repo docs explicitly define them.
- Commit-message standards beyond one implementation issue.

Research should answer:

- What handoff evidence makes an implementation trustworthy?
- What should be fixed before lock versus recorded as out-of-scope follow-up?
- What wording prevents overclaiming and unauthorized issue-state changes?

Research should not answer:

- How to run every CI or release process.
- How to resolve PR review threads.
- How to close issues in all trackers.

## 5. Research Order

| Order | Facet | Why Now | Later Dependencies | Independent? | Skip / Merge Signal |
| --- | --- | --- | --- | --- | --- |
| 1 | Ready Issue Selection | It is the first branch in `implement`; everything else depends on one selected issue-equivalent slice. | Context Intake and Bounded Slice Control need a selected issue to reason about. | Mostly independent. | Merge into Context Intake only if source search shows selection adds no behavior beyond readiness context. |
| 2 | Baseline And Fixed Point | It is the first pre-edit safety gate and protects later review/commit truth. | Review And Lock depends on a real fixed point; Protected Simplification depends on knowing what changed. | Mostly independent. | Merge into Review And Lock only if no distinct baseline/change-isolation sources emerge. |
| 3 | Context Intake | It decides whether the selected issue is executable before coding begins. | Bounded Slice Control, Commitment Boundary, and Semantic Proof need intent, acceptance criteria, blockers, and non-goals. | Mostly independent. | Merge with Ready Issue Selection only if readiness recheck cannot be separated from selection. |
| 4 | Bounded Slice Control | Once issue and context are known, this facet defines what remains in the active slice. | Commitment Boundary and Semantic Proof need a stable slice boundary. | Mostly independent. | Merge with Semantic Proof only if research shows every slice rule is really a proof rule. |
| 5 | Commitment Boundary | After context and slice are explicit, the skill needs clear ask/act rules. | Proof, simplification, and lock need to know when local changes become user-owned changes. | Cross-cutting but source-distinct. | Treat as a cross-cutting rule, not a runtime section, if sources only restate the engineering contract. |
| 6 | Semantic Proof And Seams | Proof is the core implementation quality bar, and seam choice is part of the same behavior. | Protected Simplification and Review And Lock depend on proof quality and skipped-check honesty. | Independent enough to research alone. | Split only if source search yields distinct source sets for proof standards versus seam/interface discipline. |
| 7 | Protected Simplification | Cleanup/refactor gates should be shaped after proof and seam choices are clear. | Review And Lock needs to know whether simplification stayed in scope. | Mostly independent after proof/seams. | Merge into Semantic Proof if research finds only "refactor while green" and no distinct implementation behavior. |
| 8 | Review And Lock | This is the final handoff facet and should consume prior decisions. | None; it is the convergence artifact. | Best researched last. | Split only if implementation note / issue-state restraint and commit/review evidence diverge into separate behaviors. |

This is a research order, not a safe runtime integration order. Runtime
integration should wait for at least Facets 1-6 because selection, context,
slice boundary, commitment boundary, and proof wording collide in the core
`implement` process. Facet-only integration is safe only for a narrow local
gate whose later facets cannot reasonably change it.

## 6. Source Lanes By Facet

| Facet | Primary Source Lanes | Secondary Source Lanes | Avoided Source Lanes |
| --- | --- | --- | --- |
| Ready Issue Selection | delivery/operations sources; Kanban/WIP sources; issue-readiness practice; agentic coding / LLM task-selection sources | prompt/skill-writing for stop gates; tracker docs for local mapping | generic project-management advice; raw issue-template catalogs; triage-state-machine sources unless they affect pickup behavior |
| Baseline And Fixed Point | version-control practice; professional software engineering books; code-review practice; delivery/operations sources | official Git docs for mechanics; agentic coding sources on diff/commit safety | Git tutorials that only teach commands; PR-size folklore without reviewability evidence |
| Context Intake | requirements/product sources; specification-by-example sources; issue-brief practice; domain-driven design; agent context-engineering sources | prompt/skill-writing for context gates | broad discovery methods; PRD-writing methods; generic meeting/interview advice |
| Bounded Slice Control | professional software engineering books; story-slicing sources; delivery/small-batch sources; code-review size/comprehension sources | agentic coding sources on bounded tasks and trajectory control | generic Agile taxonomies; "small PR" numerology; framework-specific task runners |
| Commitment Boundary | requirements ownership sources; product ownership sources; ADR/public-contract sources; human-in-the-loop agent sources | security/privacy/data-contract sources when tied to stop rules | authority charts; generic "ask the user" advice; product discovery frameworks |
| Semantic Proof And Seams | TDD/proof sources; specification-by-example sources; legacy-code seam sources; architecture/design sources; empirical software testing papers | codebase-design vocabulary; agentic coding validation/eval sources | tool-specific unit-test tutorials; architecture pattern advocacy not tied to proof; mocking taxonomy without agent behavior |
| Protected Simplification | refactoring books; TDD green-refactor sources; simple-design sources; safe-change practice | prompt/skill-writing pruning sources; delivery sources on safe cleanup | broad cleanup manifestos; style-only clean-code advice; architecture-review sources |
| Review And Lock | code-review sources; Definition of Done / delivery sources; traceability and handoff sources; commit hygiene sources | agentic coding validation loops; tracker note conventions | release-management depth; style-only review checklists; PR-thread workflows |

## 7. Search Vocabulary By Facet

### Facet 1: Ready Issue Selection

Strong search terms:

- ready for development
- ready for agent
- WIP limit
- pull system
- blocked work
- dependency order
- task readiness
- one piece flow

Exact phrase queries:

- `"ready for development" software issue`
- `"definition of ready" software development`
- `"blocked work" Kanban software`
- `"WIP limit" "pull system" software`
- `"one piece flow" software development`
- `"task readiness" "coding agent"`

Book/source anchors:

- `"WIP limits" "Kanban"`
- `"pull system" "Lean Software Development"`
- `"definition of ready" "Scrum"`
- `"work in progress" "The Phoenix Project"`

Agentic bridge queries:

- `"coding agent" "ready for agent"`
- `"AI coding assistant" "task selection"`
- `"LLM coding agent" "acceptance criteria"`

Noise filters:

- avoid issue-template examples unless they produce pickup gates.
- avoid project-management advice that does not constrain agent selection.

### Facet 2: Baseline And Fixed Point

Strong search terms:

- baseline
- fixed point
- dirty working tree
- change isolation
- reviewable diff
- atomic commit
- logical commit
- revertability
- bisectability

Exact phrase queries:

- `"dirty working tree" preserve changes`
- `"atomic commits" code review`
- `"logical commits" software engineering`
- `"reviewable diff" code review`
- `"change isolation" software engineering`
- `"git bisect" "small commits"`

Book/source anchors:

- `"small changes" "Google Engineering Practices"`
- `"atomic commits" "Version Control with Git"`
- `"small batches" "Continuous Delivery"`
- `"modern code review" "Google"`

Agentic bridge queries:

- `"coding agent" "dirty working tree"`
- `"AI coding assistant" "git diff"`
- `"LLM coding agent" "commit"`

Noise filters:

- avoid Git command tutorials without review or preservation guidance.
- avoid numeric PR-size claims unless tied to comprehension, rollback, or
  validation behavior.

### Facet 3: Context Intake

Strong search terms:

- acceptance criteria
- specification by example
- executable specification
- issue brief
- product intent
- non-goals
- blockers
- ubiquitous language
- context engineering

Exact phrase queries:

- `"acceptance criteria" implementation`
- `"specification by example" acceptance criteria`
- `"executable specification" software`
- `"issue brief" software development`
- `"non-goals" software requirements`
- `"ubiquitous language" implementation`
- `"context engineering" coding agent`

Book/source anchors:

- `"Specification by Example" acceptance criteria`
- `"User Story Mapping" acceptance criteria`
- `"Domain-Driven Design" ubiquitous language`
- `"Writing Effective Use Cases" preconditions`

Agentic bridge queries:

- `"coding agent" "acceptance criteria"`
- `"AI coding assistant" "context"`
- `"LLM coding" "issue context"`

Noise filters:

- avoid broad requirements-gathering sources unless they produce implementation
  readiness gates.
- avoid product-discovery sources that belong upstream.

### Facet 4: Bounded Slice Control

Strong search terms:

- tracer bullet
- vertical slice
- walking skeleton
- thin slice
- small batch
- one self-contained change
- story splitting
- scope creep
- follow-up

Exact phrase queries:

- `"tracer bullet" software development`
- `"vertical slice" software development`
- `"walking skeleton" agile architecture`
- `"story splitting" acceptance criteria`
- `"small batch" software delivery`
- `"one self-contained change" code review`
- `"avoid scope creep" software implementation`

Book/source anchors:

- `"tracer bullets" "The Pragmatic Programmer"`
- `"vertical slice" "Growing Object-Oriented Software"`
- `"walking skeleton" "Alistair Cockburn"`
- `"story splitting" "User Story Mapping"`
- `"small changes" "Google Engineering Practices"`

Agentic bridge queries:

- `"coding agent" "bounded task"`
- `"AI coding assistant" "scope creep"`
- `"LLM software engineering" "small changes"`

Noise filters:

- avoid generic Agile slicing catalogs unless they produce agent gates.
- avoid "small means fewer lines" claims without proof, review, or recovery
  behavior.

### Facet 5: Commitment Boundary

Strong search terms:

- commitment boundary
- requirements ownership
- product owner
- public contract
- data contract
- backward compatibility
- ADR
- human-in-the-loop

Exact phrase queries:

- `"requirements ownership" implementation`
- `"product owner" acceptance criteria implementation`
- `"public API contract" compatibility`
- `"data contract" software change`
- `"architecture decision record" implementation decision`
- `"human in the loop" AI agent software engineering`

Book/source anchors:

- `"Product Ownership" acceptance criteria`
- `"Architecture Decision Records" public contract`
- `"Release It" compatibility`
- `"Domain-Driven Design" bounded context`

Agentic bridge queries:

- `"coding agent" "human in the loop"`
- `"AI agent" "approval" "software change"`
- `"LLM coding" "public API"`

Noise filters:

- avoid generic "communicate with stakeholders" advice.
- avoid authority-model sources that do not produce concrete stop rules.

### Facet 6: Semantic Proof And Seams

Strong search terms:

- semantic correctness
- red-green-refactor
- test oracle
- characterization test
- executable specification
- seam
- contract test
- public interface
- load-bearing internal
- ports and adapters

Exact phrase queries:

- `"semantic correctness" software testing`
- `"test oracle" software testing`
- `"characterization test" legacy code`
- `"red green refactor" TDD`
- `"contract test" public interface`
- `"seam" "Working Effectively with Legacy Code"`
- `"load-bearing" internal behavior software`

Book/source anchors:

- `"Test Driven Development" "Kent Beck"`
- `"Working Effectively with Legacy Code" seams`
- `"Growing Object-Oriented Software" interface tests`
- `"Specification by Example" executable specification`
- `"xUnit Test Patterns" test oracle`

Agentic bridge queries:

- `"coding agent" "test oracle"`
- `"AI coding assistant" "validation" tests`
- `"LLM coding agent" "semantic correctness"`

Noise filters:

- avoid unit-testing tutorials unless they discuss behavior proof.
- avoid architecture pattern advocacy unless it changes proof-seam choice.

### Facet 7: Protected Simplification

Strong search terms:

- refactoring
- behavior preserving
- green refactor
- preparatory refactoring
- simple design
- cleanup boundary
- scratch artifacts
- safe change

Exact phrase queries:

- `"behavior preserving" refactoring`
- `"refactor while green"`
- `"preparatory refactoring" software`
- `"simple design" test driven development`
- `"code cleanup" scope creep`
- `"safe refactoring" tests`

Book/source anchors:

- `"Refactoring" "Martin Fowler"`
- `"TDD by Example" refactor`
- `"Working Effectively with Legacy Code" refactoring`
- `"Growing Object-Oriented Software" refactoring`

Agentic bridge queries:

- `"coding agent" "refactor" "tests"`
- `"AI coding assistant" "cleanup" "scope creep"`
- `"LLM coding" "scratch files"`

Noise filters:

- avoid style-only clean-code advice.
- avoid repository cleanup plans that are separate from one issue.

### Facet 8: Review And Lock

Strong search terms:

- fixed-point review
- code review
- Definition of Done
- implementation note
- residual risk
- traceability
- skipped checks
- commit SHA
- issue state

Exact phrase queries:

- `"code review" "small changes"`
- `"code review checklist" software`
- `"definition of done" validation evidence`
- `"implementation note" software issue`
- `"residual risk" software delivery`
- `"commit message" issue reference`
- `"traceability" commit issue`

Book/source anchors:

- `"Google Engineering Practices" "code review"`
- `"Continuous Delivery" deployment pipeline`
- `"Accelerate" change failure recovery`
- `"SmartBear" code review`

Agentic bridge queries:

- `"coding agent" "implementation note"`
- `"AI coding assistant" "residual risk"`
- `"LLM coding agent" "code review"`

Noise filters:

- avoid style-only review checklists.
- avoid release-management depth unless it sharpens one-issue lock evidence.

## 8. Evidence Gates By Facet

### Ready Issue Selection

A good research packet must produce:

- leading words for one-at-a-time pull, readiness, blockers, and dependency
  order;
- concrete agent behaviors for named issue, PRD/spec, queue selection,
  ambiguity, and no-ready-issue cases;
- evidence gates for selected issue source, readiness, blocker status, and
  selection reason;
- stop/ask rules for ambiguous readiness or no available issue;
- weak/no-op language to avoid, especially broad "pick next task" phrasing;
- source quality notes separating pickup behavior from triage behavior.

### Baseline And Fixed Point

A good research packet must produce:

- leading words for baseline, fixed point, change isolation, and reviewable
  diff;
- concrete agent behaviors for dirty-tree inventory, starting ref, staging
  boundary, and unrelated-change preservation;
- evidence gates for fixed point and in-scope file set;
- stop/ask rules for unsafe dirty-tree overlap;
- weak/no-op language to avoid, especially generic "check git status."

### Context Intake

A good research packet must produce:

- leading words for product intent, acceptance criteria, executable context,
  blockers, and non-goals;
- concrete agent behaviors for reading issue bodies, comments, parent sources,
  linked context, and domain docs;
- evidence gates for enough context to implement without guesswork;
- stop/ask rules for missing acceptance criteria, blockers, or proof surface;
- source quality notes distinguishing implementation context from product
  discovery.

### Bounded Slice Control

A good research packet must produce:

- leading words for tracer bullet, vertical slice, small batch, support slice,
  and follow-up;
- concrete agent behaviors for active slice statement, adjacent-work triage, and
  failed-proof response;
- evidence gates that keep work inside one behavior/support proof;
- stop/ask rules for mixed concepts, adjacent behavior, or needed support work;
- weak/no-op language to avoid, especially "stay focused."

### Commitment Boundary

A good research packet must produce:

- leading words for commitments, technique, public/data/security contracts, and
  user-owned decisions;
- concrete agent behaviors for asking only at commitment boundaries;
- evidence gates for detecting changed product intent, acceptance criteria,
  public contracts, data semantics, security/privacy posture, dependency or
  tooling commitments, or slice boundary;
- stop/ask rules that prevent both under-asking and over-asking;
- source quality notes separating implementation autonomy from product
  authority.

### Semantic Proof And Seams

A good research packet must produce:

- leading words for semantic correctness, red-green-refactor, test oracle,
  executable specification, seam, interface, and load-bearing internal;
- concrete agent behaviors for proof choice, `$tdd` handoff, focused checks,
  skipped validation, and seam selection;
- evidence gates for behavior, data, docs/config, support work, and internal
  semantics;
- stop/ask rules for unclear behavior, impossible proof, or seam changes beyond
  the slice;
- source quality notes separating proof guidance from full `$tdd` or
  `codebase-design` procedures.

### Protected Simplification

A good research packet must produce:

- leading words for green refactor, behavior-preserving change, preparatory
  refactoring, simple design, and cleanup boundary;
- concrete agent behaviors for simplifying only while protected, deleting
  scratch, and recording separate cleanup;
- evidence gates for behavior-preserving cleanup;
- stop/ask rules for cleanup that changes behavior or becomes a support slice;
- weak/no-op language to avoid, especially broad "clean up as you go."

### Review And Lock

A good research packet must produce:

- leading words for fixed-point review, Definition of Done, traceability,
  residual risk, implementation note, and issue-state restraint;
- concrete agent behaviors for running `$review`, fixing in-scope findings,
  committing in-scope files, and noting evidence;
- evidence gates for commit scope, validation record, skipped checks, residual
  risk, and issue-note completeness;
- stop/ask rules for unresolved in-scope findings or unauthorized issue-state
  changes;
- source quality notes separating lock behavior from full review/PR workflows.

## 9. Merge / Split / Retire Ledger

| Step 1 Candidate | Decision | Final Facet(s) | Why | Risk To Watch |
| --- | --- | --- | --- | --- |
| Ready Issue Selection | Kept and promoted | Ready Issue Selection | It is the first concrete behavior and has distinct stop/ask rules from later context intake. | Could drift into `triage` or `to-issues`; keep it to pickup/readiness only. |
| Baseline And Fixed Point | Kept | Baseline And Fixed Point | It has distinct pre-edit safety and fixed-point research needs. | Could become generic Git hygiene; require reviewability/change-isolation gates. |
| Context Intake Before Editing | Kept and renamed | Context Intake | It owns executable context after selection. | Could become product discovery or brief authoring; keep upstream owner boundaries visible. |
| Bounded Slice Control | Kept and renamed | Bounded Slice Control | It owns active-slice and adjacent-work behavior. A subagent suggested merging it with Commitment Boundary, but the source lanes and failure modes are distinct enough to research separately. | Could duplicate Semantic Proof or Commitment Boundary; keep it about scope boundaries, not proof mechanics or user authority. |
| Commitment Boundary | Kept | Commitment Boundary | It has distinct authority/ask/act source lanes and cross-cuts later facets. It should stay separate from Bounded Slice Control because changing the slice is only one kind of commitment change. | Could restate the engineering contract; require implement-specific decisions. |
| Semantic Proof And TDD Handoff | Merged | Semantic Proof And Seams | Proof and seam choice are one implement behavior: prove the right semantics through the right boundary. | Could duplicate `$tdd`; keep full red-green-refactor mechanics out. |
| Seams And Load-Bearing Internals | Merged | Semantic Proof And Seams | The source lanes overlap with proof, and separate research would likely duplicate runtime wording. | Split later only if source search finds distinct seam-only behavior. |
| Protected Simplification | Kept | Protected Simplification | It owns post-proof cleanup and scratch disposal. | Could become broad refactoring advice; keep it slice-bound. |
| Review And Lock | Kept | Review And Lock | It owns final handoff after `$review`, not `$review` itself. | Could duplicate review or PR workflows; keep lock evidence central. |
| Invocation And Skill Shape | Deferred / retired from source research | Final compression and runtime patching, not an active source-search facet | Explicit-only invocation and compact skill shape matter, but they are final synthesis constraints after behavior research, not a separate research surface for Prompt 03. | Later runtime wording could accidentally make `implement` an implicit general coding router; Prompt 12 should re-check description/config compatibility. |

## 10. Cross-Facet Collision Map

| Collision | Primary Owner | Secondary Facet / Owner | Risk If Ignored | Later Prompt Watchpoint |
| --- | --- | --- | --- | --- |
| Ready issue selection vs upstream readiness | Ready Issue Selection | `triage`, `to-issues`, tracker docs | `implement` could start triaging or writing issues instead of picking one. | Prompt 03 must search for pickup/readiness gates, not full issue lifecycle. |
| Ready issue selection vs context intake | Ready Issue Selection | Context Intake | Selection could absorb all issue reading, or context intake could redo selection. | Keep selection to "which issue and can it be safely picked"; context owns "what must be understood before coding." |
| Baseline vs review/lock | Baseline And Fixed Point | Review And Lock, `$review` | Lock could rely on a fixed point that was never captured, or baseline research could duplicate review. | Prompt 06/08 should preserve the fixed-point handoff into `$review`. |
| Context intake vs product discovery | Context Intake | `triage`, `grilling`, `to-prd` | `implement` could ask product-discovery questions instead of stopping or returning upstream. | Search should favor implementation-readiness gates and non-goal recognition. |
| Bounded slice vs semantic proof | Bounded Slice Control | Semantic Proof And Seams | Proof gaps can widen scope or slice language can swallow proof mechanics. | Keep slice gates about scope; keep proof gates about correctness evidence. |
| Commitment boundary vs all implementation steps | Commitment Boundary | Engineering contract and every later facet | The agent may over-ask about technique or under-ask about commitments. | Treat as cross-cutting runtime guard; audit later wording for duplicate contract prose. |
| Semantic proof vs `$tdd` | Semantic Proof And Seams | `$tdd` | `implement` could copy TDD procedure or weaken it into after-the-fact checks. | Source extraction must identify handoff gates and forbidden shortcuts. |
| Semantic proof vs `codebase-design` | Semantic Proof And Seams | `codebase-design` | Seam guidance could turn into architecture design. | Keep only proof-seam selection needed for one implementation slice. |
| Protected simplification vs broad cleanup | Protected Simplification | Bounded Slice Control, architecture-review skills | Cleanup could become a second issue hidden inside implementation. | Require behavior protection and slice value for every simplification rule. |
| Review/lock vs issue-state workflow | Review And Lock | Tracker docs, `triage` | Agent could close/relabel or omit evidence. | Prompt 05/09 should preserve issue-state restraint and implementation-note evidence. |

## 11. First Facet Recommendation

Research `Ready Issue Selection` first.

Why:

- It is the first runtime decision `implement` makes.
- A wrong or ambiguous selection invalidates every later facet.
- Prompt 01 promoted this from a rough concern into a distinct owner boundary:
  `implement` may pick up one ready issue, but must not become `triage` or
  `to-issues`.
- This facet is small enough to search well and should produce clear stop/ask
  gates for Prompt 04 extraction.

Source lanes to start with:

- delivery/operations sources on pull systems, WIP limits, and blocked work;
- issue-readiness / Definition of Ready sources;
- professional sources on one-piece flow or small-batch work;
- agentic coding sources only when they discuss task selection or readiness;
- prompt/skill-writing sources for explicit stop/ask gates.

Five strongest search queries:

- `"ready for development" software issue`
- `"definition of ready" software development`
- `"blocked work" Kanban software`
- `"WIP limit" "pull system" software`
- `"coding agent" "task selection" "acceptance criteria"`

Output file to create:

`docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md`

Early facet integration is not safe yet. The first facet touches invocation and
the first runtime branch, but final runtime wording should wait for at least
Context Intake and Bounded Slice Control so "ready issue", "selected slice",
and "enough context" do not drift into separate meanings.

Research is good enough to proceed when the source-search packet has:

- at least one strong delivery/WIP/readiness source;
- at least one source that distinguishes ready selection from upstream triage;
- at least one source that gives an operational stop/ask gate;
- rejected-source notes for broad project-management or issue-template lanes;
- extraction targets for selection behavior, ambiguity, blockers, and no-ready
  issue outcomes.

## 12. Output Summary

- facet-map decision: `ready-for-source-search`
- final facet count: 8 active facets
- first facet to research: `Ready Issue Selection`
- next artifact path:
  `docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md`
- strongest cross-facet terms:
  - ready issue
  - blocked work
  - fixed point
  - context intake
  - bounded slice
  - commitment boundary
  - semantic correctness
  - proof seam
  - protected simplification
  - residual risk
- biggest risk in the research plan:
  - The facets are close to existing skill and contract ownership. Each prompt
    must keep asking whether source pressure changes `implement` behavior, or
    merely restates `to-issues`, `triage`, `$tdd`, `$review`, `codebase-design`,
    tracker docs, or the engineering contract.

The facet-map decision label is explicit: `ready-for-source-search`.
