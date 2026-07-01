# Prompt 01: Implement Intent And Keywords

This executes
[`docs/synthesis/methods/prompts/01-intent-and-keywords.md`](../../../synthesis/methods/prompts/01-intent-and-keywords.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Related files or skills:

- `skills/current/implement/agents/openai.yaml`
- `docs/agents/engineering-contract.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `CONTEXT.md`
- `README.md`
- `skills/current/to-issues/SKILL.md`
- `skills/current/triage/SKILL.md`
- `skills/current/triage/AGENT-BRIEF.md`
- `skills/current/tdd/SKILL.md`
- `skills/current/review/SKILL.md`
- `docs/research/skill-facets/implement/README.md`
- `docs/research/skill-facets/implement/SEARCH-VOCABULARY.md`
- `docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE.md`
- `docs/synthesis/families/issue-pipeline.md`
- `docs/synthesis/skills/implement.md`
- `docs/synthesis/target-spine.md`

User goal for this skill: redo the research setup for `implement` by
executing Prompt 01 cleanly, so the next research pass starts from the current
skill, the current issue-pipeline boundaries, and the source-to-skill workflow
rather than from the older facet map alone.

Constraints:

- Do not research online yet.
- Do not rewrite `skills/current/implement/SKILL.md`.
- Do not propose final runtime wording yet.
- Use current repo files to identify intent, behavior surfaces, rough facets,
  and preliminary search vocabulary.

## 1. Skill Intent

`implement` exists to take exactly one ready-for-agent issue through the repo's
implementation loop: select the issue, capture the baseline, understand the
bounded slice, choose and make the local change, prove it, review it, commit it,
and leave an evidence-backed implementation note.

It should be invoked when the user explicitly asks for `$implement`, asks to
implement a named issue/path/URL/spec/PRD through the skill-pack workflow, or
asks an agent to pick up the next ready-for-agent issue. It is explicit-only in
`agents/openai.yaml`, so its description is human-facing routing, not an
always-loaded model trigger.

It should make Codex more predictable about:

- choosing exactly one issue or one issue-equivalent slice;
- preserving unrelated dirty work and capturing a review fixed point before
  editing;
- reading the full issue, parent source, acceptance criteria, blockers, and
  out-of-scope boundaries;
- treating implementation as one bounded slice rather than an open-ended cleanup
  session;
- proving semantic correctness through the best practical seam, using `$tdd`
  when behavior is clear enough for red-green-refactor;
- running focused and repo-standard checks when feasible;
- using `$review` from the captured fixed point before lock;
- committing only in-scope files and leaving an implementation note with
  evidence, skipped checks, and residual risk.

It should explicitly not:

- create or triage issues itself; `to-issues` and `triage` own that upstream
  work;
- implement multiple ready issues in one run;
- treat a PRD/spec as permission to build the whole plan;
- broaden scope when adjacent work appears;
- ask the user for ordinary implementation technique decisions that the agent
  can decide inside the bounded slice;
- cross a commitment boundary without asking;
- replace TDD with after-the-fact checks when the slice is suitable for TDD;
- do the full `review` procedure inline; it should call or run `$review`;
- change issue state unless requested or repo-defined;
- treat output existence as semantic proof.

## 2. Current Behavior Surface

| Surface | Current Behavior | Research Need |
| --- | --- | --- |
| Invocation / description | Explicit-only skill: "Pick up one ready-for-agent issue, implement it through the repo's existing seams, verify it, review it, commit it, and leave an implementation note." | Confirm whether the description is still the right human-facing summary after deepening, without adding implicit-trigger bloat. |
| First action | "Implement one ready-for-agent issue. Stop after one issue." | Preserve the one-issue WIP limit and make the first concrete action harder to skip. |
| Issue selection | Named issue/path/URL wins; PRD/spec is used to find or choose one ready issue; otherwise select next unblocked ready-for-agent issue from configured tracker. | Clarify dependency order, ambiguity, and no-issue stop behavior without duplicating `to-issues` or `triage`. |
| Preconditions | Read engineering contract, issue tracker, triage labels; read domain docs when touching codebase context; run setup skill if required files are missing. | Keep repo contract routing intact; research should not replace setup or domain-modeling behavior. |
| Baseline capture | Inspect worktree, preserve unrelated changes, capture starting ref, stage/commit only issue files. | Strengthen fixed-point and dirty-tree discipline so later review and commit stay trustworthy. |
| Orient/explore | Read issue, comments, parent source, linked context, acceptance criteria, blockers, and out-of-scope boundaries; identify tracer-bullet/support-slice proof. | Improve how the agent decides it has enough context before editing. |
| Ask/stop rules | Ask when implementation would be guesswork or when better approach changes a commitment. | Research commitment-boundary language so the agent acts autonomously inside technique but stops at user-owned commitments. |
| Implementation | Choose one approach; make narrow change; give load-bearing internals a contract and proof through smallest meaningful seam. | Deepen local-approach choice, seam selection, and load-bearing internal proof without duplicating `codebase-design` or `tdd`. |
| Scope gates | Do not expand beyond selected slice; do not add adjacent tracer bullets/support slices; follow-ups go in final note. | Preserve and sharpen bounded-slice behavior, especially after failed proof or tempting cleanup. |
| Proof / validation | Use red-green-refactor where suitable; prove semantic correctness; run focused checks regularly and full/repo-standard validation when feasible. | Deepen evidence standards without importing all TDD mechanics. |
| Simplification | Simplify only while behavior is protected; remove scaffolding, collapse bloat, improve names, deepen modules when it helps the slice. | Research protected cleanup so simplification helps without widening behavior. |
| Converge | Run `$review` against starting ref, fix in-scope findings, record out-of-scope findings. | Keep review as a separate fixed-point gate and avoid duplicating `review`. |
| Lock | Commit to current branch; leave implementation note with SHA, summary, validation, skipped checks, residual risk; do not change issue state unless allowed. | Research lock/readiness evidence and handoff shape. |
| Completion criteria | Done means one issue implemented, reviewed, committed, noted; validation recorded; unrelated work preserved; issue-state changes controlled. | Make done checkable enough to resist premature completion. |

## 3. Failure Modes To Prevent

- Implementing more than one issue because multiple ready items are available.
- Treating a PRD/spec as the selected slice instead of using it to find one
  ready issue.
- Selecting a blocked issue or guessing through missing acceptance criteria.
- Editing before capturing dirty-work state and starting ref.
- Losing unrelated user changes while implementing.
- Reading only the issue title and missing comments, parent source, blockers,
  or explicit non-goals.
- Slicing by folder, layer, nearby cleanup, or convenient files instead of one
  observable behavior/support proof.
- Adding adjacent behavior because the code is already open.
- Asking the user about implementation technique inside the bounded slice.
- Not asking when the better approach changes product intent, public contracts,
  data semantics, security/privacy posture, or the bounded slice.
- Treating runnable output, generated files, or a passing smoke command as
  semantic correctness without examples, fixtures, invariants, or acceptance
  proof.
- Using after-the-fact checks where red-green-refactor would have been practical.
- Testing through brittle internals instead of the highest useful seam.
- Keeping exploration scaffolding, scratch files, or broad cleanup in the final
  diff.
- Running review without a real fixed point, or skipping the Spec axis by losing
  the issue/source connection.
- Committing unrelated files because the worktree was dirty or broad.
- Leaving no implementation note, or leaving a note without validation, skipped
  checks, residual risk, or commit SHA.
- Changing issue status or labels when the user/repo workflow did not authorize
  that change.

## 4. Rough Facet Candidates

These are rough candidates only. Prompt 02 owns the final facet map, order,
merge/split decisions, and artifact paths.

| Facet | Behavior Surface | Research Question | Source Lanes | Evidence Gate | Stop/Ask Rule | Preliminary Keywords |
| --- | --- | --- | --- | --- | --- | --- |
| One Ready Issue | invocation, issue selection, first action | How should `implement` reliably select exactly one ready slice and stop when no safe issue is available? | Kanban/state policies, issue-tracker workflows, agent task selection, repo-local tracker docs | One selected issue is named with source, readiness, blockers, and reason for selection. | Ask only when multiple ready issues are equally eligible or no ready issue exists. | ready-for-agent, WIP limit, explicit policies, blocked by, dependency order, one issue |
| Baseline And Fixed Point | baseline capture, dirty tree, review handoff | What must be captured before editing so unrelated work is preserved and review has a trustworthy fixed point? | version-control practice, code-review practice, CI/release practice, local workspace-safety history | Starting ref and dirty-work inventory are recorded before edits; staged files remain in-scope. | Stop if the baseline cannot be established or preserving unrelated changes is impossible. | fixed point, baseline, dirty working tree, change isolation, atomic commit, reviewable diff |
| Context Intake Before Editing | orient/explore, issue reading, domain docs | How much issue/spec/domain context must be read before implementation can begin without guesswork? | requirements engineering, specification by example, domain-driven design, issue brief writing, agent context engineering | Product intent, acceptance criteria, blockers, non-goals, domain terms, and proof surface are identified before coding. | Ask when the issue lacks enough information to define expected behavior or proof. | product intent, acceptance criteria, Codex-ready brief, domain language, linked context, blockers |
| Bounded Slice Control | scope boundary, adjacent work, failed proof | How do strong teams keep one implementation run small, valuable, provable, and reviewable? | tracer bullets, story slicing, small batches, code review size, delivery economics, agent validation loops | The active slice is one behavior/support proof, and adjacent work is recorded as follow-up. | Stop, split, or ask when validation requires a different slice or mixed concepts. | tracer bullet, vertical slice, one self-contained change, small batch, outside proof, follow-up |
| Commitment Boundary | ask/stop rules, autonomy | Which decisions belong to the user, and which belong to the agent during implementation? | requirements ownership, product ownership, ADRs, public contracts, data/security semantics, human-in-the-loop agents | Agent proceeds on technique but stops at changed commitments. | Ask before changing product intent, acceptance criteria, public contracts, data semantics, security/privacy, or slice boundary. | commitment boundary, requirements ownership, public contract, data contract, ADR-worthy, user-owned decision |
| Semantic Proof And TDD Handoff | proof, validation, TDD routing | What counts as proof that the requested behavior is semantically correct, and when should `implement` hand off to `$tdd`? | TDD, BDD/specification by example, test oracles, characterization tests, property-based testing, data validation | Acceptance criteria are proven through tests/checks/examples or skipped with explicit residual risk. | Stop or ask when no meaningful proof path exists or behavior is too unclear for a red test. | semantic correctness, red-green-refactor, executable specification, test oracle, fixture, invariant, acceptance test |
| Seams And Load-Bearing Internals | seam choice, internal contracts | How should the agent choose the highest useful seam and prove correctness-critical internals without brittle over-testing? | legacy-code seams, information hiding, ports/adapters, contract tests, deep modules, mocking discipline | Load-bearing internals have a contract and proof through a meaningful seam. | Ask or narrow when the only available proof is brittle or the seam requires redesign beyond the slice. | seam, public interface, contract test, adapter, characterization test, load-bearing internal, module depth |
| Protected Simplification | simplify step, cleanup, refactor | How should simplification and refactoring happen after behavior is protected without widening the issue? | refactoring, simple design, behavior-preserving change, preparatory refactoring, code cleanup, green refactor | Cleanup is behavior-preserving, in-scope, and protected by tests/checks. | Stop when cleanup changes behavior, introduces new commitments, or becomes a separate support slice. | green refactor, behavior-preserving, simple design, YAGNI, preparatory refactoring, cleanup boundary |
| Review And Lock | fixed-point review, commit, implementation note | What makes the result ready to hand off: reviewed, committed, noted, and honest about residual risk? | modern code review, Definition of Done, continuous delivery, commit hygiene, traceability, handoff notes | `$review` ran or was explicitly skipped, commit contains only in-scope files, and the issue note records evidence. | Stop if review exposes in-scope findings that are not fixed or if lock evidence is missing. | fixed-point review, Standards and Spec, implementation note, validation evidence, residual risk, commit SHA |

## 5. Preliminary Keyword Bank

### Professional Software Engineering Terms

- tracer bullet
- vertical slice
- walking skeleton
- outside-in development
- acceptance criteria
- specification by example
- executable specification
- semantic correctness
- test oracle
- characterization test
- seam
- public interface
- contract test
- ports and adapters
- information hiding
- load-bearing internal
- behavior-preserving refactor
- simple design
- small batch
- WIP limit
- atomic commit
- logical commit
- reviewable diff
- fixed-point review
- Definition of Done
- residual risk
- traceability
- implementation note

### Agentic / LLM Execution Terms

- ready-for-agent
- Codex-ready brief
- bounded slice
- agent-computer interface
- context engineering
- tool feedback
- repair-validate loop
- acceptance criteria in prompt
- task localization
- scratch / exploration artifact
- completion criterion
- stop / ask / continue rule
- validation lane
- overclaiming
- residual risk reporting
- unrelated dirty work
- fixed point for review
- evidence-backed handoff

### Skill-Writing Terms

- explicit-only
- description
- invocation
- behavior surface
- leading word
- completion criterion
- evidence gate
- stop/ask rule
- context pointer
- branch
- progressive disclosure
- owned elsewhere
- no-op
- duplication
- sediment
- sprawl
- single source of truth
- line-by-line behavior audit
- runtime wording
- support/reference doc

### Weak Or Noisy Terms

- implement safely
- be careful
- write good code
- high quality
- best practices
- clean code
- thorough testing
- robust solution
- fully validate
- comprehensive implementation
- end-to-end when used without a concrete seam
- small when it only means fewer lines
- simple when it means underspecified
- done when it only means code exists
- refactor when it means broad cleanup
- review when it means a vague self-check
- agentic workflow when it does not change a gate

## 6. Source Search Seeds

### One Ready Issue

- `"ready for development" issue workflow`
- `"explicit policies" Kanban software development`
- `"work in progress limit" software development`
- `"blocked by" issue tracker workflow`
- `"dependency order" software backlog`
- `"definition of ready" user story`
- `"unblocked" "ready" issue tracker`
- `"Kanban" "explicit policies" software`

### Baseline And Fixed Point

- `"clean working tree" git workflow`
- `"dirty working tree" preserve changes`
- `"atomic commits" code review`
- `"logical commits" software engineering`
- `"reviewable diff" code review`
- `"pull request size" code review`
- `"change isolation" software engineering`
- `"git bisect" "small commits"`
- `"trunk based development" "small batches"`

### Context Intake Before Editing

- `"acceptance criteria" "Specification by Example"`
- `"requirements engineering" "acceptance criteria"`
- `"user story" "acceptance criteria" "conversation"`
- `"domain-driven design" ubiquitous language requirements`
- `"issue template" "acceptance criteria" software`
- `"coding agent" "context" "acceptance criteria"`
- `"AI coding assistant" "task specification"`
- `"requirements traceability" implementation`

### Bounded Slice Control

- `"tracer bullet" software development`
- `"vertical slice" software development`
- `"walking skeleton" agile architecture`
- `"story splitting" acceptance criteria`
- `"small batch" software delivery`
- `"one self-contained change" code review`
- `"code review" "small changes"`
- `"change decomposition" code review`
- `"continuous delivery" "small batches"`

### Commitment Boundary

- `"requirements ownership" software development`
- `"product owner" "acceptance criteria"`
- `"scope creep" software requirements`
- `"architecture decision record" software`
- `"public contract" API design`
- `"data contract" software engineering`
- `"security requirements" change control`
- `"human in the loop" "software engineering" agents`

### Semantic Proof And TDD Handoff

- `"semantic correctness" software testing`
- `"executable specification" software`
- `"specification by example" acceptance tests`
- `"red green refactor" TDD`
- `"test oracle" software testing`
- `"characterization tests" legacy code`
- `"property-based testing" invariants`
- `"metamorphic testing" software testing`
- `"approval testing" golden master`

### Seams And Load-Bearing Internals

- `"software seam" "Working Effectively with Legacy Code"`
- `"test through public interface"`
- `"information hiding" "Parnas"`
- `"deep module" software design`
- `"ports and adapters" testing`
- `"contract tests" ports adapters`
- `"don't mock what you own"`
- `"classicist TDD" mockist`
- `"hexagonal architecture" testing`

### Protected Simplification

- `"refactor only when green"`
- `"behavior preserving" refactoring`
- `"preparatory refactoring" software`
- `"opportunistic refactoring" software`
- `"simple design" "Kent Beck"`
- `"YAGNI" software design`
- `"safe refactoring" tests`
- `"technical debt" "bounded" refactoring`
- `"code smells" refactoring`

### Review And Lock

- `"fixed point" code review`
- `"code review" "small changes"`
- `"Google Engineering Practices" "code review"`
- `"definition of done" software development`
- `"pull request description" testing validation`
- `"commit message" "why"`
- `"requirements traceability" software`
- `"residual risk" software release`
- `"verification evidence" software`
- `"implementation note" software`

## 7. Boundaries Before Research

Keep out of `SKILL.md` unless later synthesis proves it changes runtime
behavior:

- broad source summaries;
- Agile taxonomy for its own sake;
- numeric LOC/file-count thresholds;
- agent-framework jargon like ReAct, Reflexion, or multi-agent taxonomies unless
  it becomes an operational gate;
- full TDD mechanics owned by `tdd`;
- full review procedure owned by `review`;
- issue-writing rules owned by `to-issues` and `triage/AGENT-BRIEF.md`;
- tracker command details owned by `docs/agents/issue-tracker.md`;
- domain-glossary authoring owned by `domain-modeling`;
- generic "good code" advice.

Another skill or contract probably owns:

- `to-issues`: creating bounded implementation issues from PRDs/specs/plans.
- `triage`: turning incoming requests into category/state labels and
  Codex-ready briefs.
- `triage/AGENT-BRIEF.md`: the ready-for-agent issue contract shape.
- `tdd`: red-green-refactor mechanics and test examples.
- `review`: fixed-point Standards and Spec review procedure.
- `docs/agents/engineering-contract.md`: repo-wide convergence loop,
  commitment boundary, proof expectations, and load-bearing internal concept.
- `docs/agents/issue-tracker.md`: GitHub issue operations.
- `docs/agents/domain.md` and `CONTEXT.md`: domain vocabulary routing.

Over-research would be:

- building a large bibliography before choosing facets;
- researching every software-delivery source for every facet;
- chasing source fame instead of behavior-changing rules, gates, or stop
  conditions;
- redoing already-promoted bounded-slice research without identifying the
  specific gap being reopened;
- researching implementation frameworks or project-management methods that do
  not change `implement` behavior.

A source is worth keeping when it can contribute at least one of:

- a leading word that recruits strong implementation behavior;
- a concrete action the agent should take;
- a checkable evidence gate;
- a stop/ask condition;
- a failure mode `implement` can actually prevent;
- a boundary that keeps ownership in the right skill or contract;
- a contrast against weak/no-op wording.

## 8. Output Summary

Top facets to research first:

1. Baseline And Fixed Point, because `implement` cannot run a trustworthy review
   or commit without preserving the starting state.
2. Context Intake Before Editing, because issue/spec/domain understanding is the
   first guard against guesswork and scope drift.
3. Commitment Boundary, because the skill needs a crisp distinction between
   autonomous technique and user-owned commitments.
4. Semantic Proof And TDD Handoff, because `implement` must prove correctness
   without duplicating `tdd`.
5. Review And Lock, because the final handoff is where overclaiming and missing
   evidence become visible.

Strongest preliminary search terms:

- fixed point
- reviewable diff
- acceptance criteria
- commitment boundary
- semantic correctness
- executable specification
- highest useful seam
- behavior-preserving refactor
- residual risk
- implementation note

Biggest risk if `implement` is rewritten without research:

- The rewrite will duplicate the engineering contract, `tdd`, and `review`
  while weakening `implement`'s unique job: running one ready issue through a
  bounded, proven, reviewed, committed implementation slice.

Likely shape of eventual compact skill change:

- A smaller, sharper `implement` should preserve the one-issue pipeline, make
  baseline/context/proof gates harder to skip, clarify when to ask, and point to
  `tdd` and `review` instead of reimplementing them inline. Final wording should
  come only after facet research, behavior flow, compact drafting, behavior
  audit, and validation.
