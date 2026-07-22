# Prompt 01: Implement Intent And Keywords

Durable upstream source and reconstruction: [`UPSTREAM-SOURCE.md`](../../language/UPSTREAM-SOURCE.md).

Historical source-to-skill Prompt 01 artifact for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Related files or skills:

- `skills/custom/implement/agents/openai.yaml`
- `.tmp/mattpocock-skills/skills/engineering/implement/SKILL.md`
- `docs/agents/engineering-contract.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `skills/custom/to-issues/SKILL.md`
- `skills/custom/triage/SKILL.md`
- `skills/custom/tdd/SKILL.md`
- `skills/custom/review/SKILL.md`

User goal for this skill: redo Prompt 01 for `implement` while also analyzing
the upstream/minimal `implement` skill in `.tmp/mattpocock-skills`, so the next
facet-map pass starts from the current repo-local skill surface, the upstream
source contrast, and the right owner boundaries.

Revision feedback:

- Account for `.tmp/mattpocock-skills/skills/engineering/implement/SKILL.md`.
- Use five subagents to help.

Subagent inputs used:

- Current skill behavior surface and preserve inventory.
- `.tmp/mattpocock-skills` source-skill behavior surface.
- Current-vs-source delta analysis.
- Adjacent owner-boundary analysis.
- Rough facet, keyword, and search-seed analysis.

Constraints:

- Do not research online yet.
- Do not rewrite `skills/custom/implement/SKILL.md`.
- Do not propose final runtime wording yet.
- Do not choose the final facet map; Prompt 02 owns final merge/split/order.

## 1. Skill Intent

`implement` exists to take one ready implementation unit through a disciplined
repo-local execution loop: select exactly one ready issue-equivalent item,
preserve the baseline, understand the bounded slice, implement narrowly, prove
semantic correctness, review from a fixed point, commit, and leave an evidence
note.

The current repo skill is not just a richer copy of the upstream source skill.
The `.tmp/mattpocock-skills` version is a compact explicit implementation
launcher: implement work described by a PRD or issues, use `/tdd` where
possible, run typecheck/focused tests/full suite, run `/review`, and commit.
That source version preserves the original proof/review/commit spine, but it
does not define one-ready-issue selection, tracker routing, dirty-work
preservation, context intake, bounded-slice control, implementation notes, or
issue-state restraint.

The current skill should be invoked when the user explicitly wants one
ready-for-agent issue implemented, names an issue/path/URL, asks to implement a
PRD/spec by choosing one ready issue from it, or asks the agent to pick up the
next ready issue. It is a heavy explicit workflow skill, not an implicit coding
router.

It should make Codex more predictable about:

- selecting exactly one issue-equivalent item or stopping;
- using repo-owned tracker and label policy instead of invented readiness;
- preserving unrelated work before edits;
- reading enough context to avoid guesswork;
- keeping implementation inside one bounded slice;
- asking only when a user-owned commitment would change;
- using `$tdd` or TDD discipline when behavior is clear enough;
- proving semantic correctness through useful seams;
- running focused and repo-standard checks when feasible;
- running `$review` against a real starting ref;
- committing only in-scope files;
- leaving an implementation note with commit SHA, summary, validation, skipped
  checks, and residual risk;
- avoiding issue-state changes unless the user asks or the repo workflow
  defines them.

It should explicitly not:

- create issues from PRDs/specs; `to-issues` owns that;
- move issues into `ready-for-agent`; `triage` owns that;
- implement multiple issues in one run;
- treat a whole PRD/spec as one implementation scope by default;
- rewrite issue briefs or acceptance criteria during selection;
- duplicate the full engineering contract;
- duplicate `$tdd` mechanics;
- duplicate `$review` procedure;
- turn context intake into product discovery or grilling;
- turn protected simplification into a cleanup campaign;
- close, relabel, or change issue status without user/repo authority;
- claim done from output existence, plausibility, or unreviewed code.

## 2. Current Behavior Surface

| Surface | Current / Source Behavior | Research Need |
| --- | --- | --- |
| Invocation / description | Current `SKILL.md` describes picking up one ready-for-agent issue and carrying it through seams, verification, review, commit, and note. `skills/custom/implement/SKILL.md:1-4` | Preserve explicit-workflow shape without turning the description into an implicit router. |
| Invocation policy | Current OpenAI config disables implicit invocation. `skills/custom/implement/agents/openai.yaml:1-2` | Any later description changes must stay compatible with explicit-only routing. |
| Upstream source shape | `.tmp` source is a compact launcher: implement PRD/issues, use `/tdd`, run checks, `/review`, commit. `.tmp/mattpocock-skills/skills/engineering/implement/SKILL.md:1-15` | Keep the original proof/review/commit spine, but do not regress current ready-issue gates. |
| First action | Current skill starts with one ready-for-agent issue and stops after one issue. `skills/custom/implement/SKILL.md:8-10` | Make one-item selection hard to skip. |
| Issue selection | Named issue/path/URL wins; PRD/spec is used to find/choose one ready issue; otherwise choose next unblocked `ready-for-agent` issue from repo docs. `skills/custom/implement/SKILL.md:8-10`, `:22-26` | Research readiness, dependency order, ambiguity, no-ready stop, and PRD/spec handoff without owning issue creation. |
| Preconditions | Read engineering contract, issue tracker, triage labels, and domain docs when relevant. `skills/custom/implement/SKILL.md:12-16` | Preserve repo-local truth routing; avoid copying all repo-doc content into the skill. |
| Convergence loop | Current skill uses orient, explore, choose, prove, expand, converge, simplify, lock. `skills/custom/implement/SKILL.md:18-20`, `docs/agents/engineering-contract.md:13-30` | Decide later what `implement` must keep inline versus point to the engineering contract. |
| Baseline | Inspect worktree, preserve unrelated changes, capture starting ref, stage only in-scope files. `skills/custom/implement/SKILL.md:28-34` | Research fixed-point and dirty-work gates that make review/commit trustworthy. |
| Context intake | Read full issue, comments/local notes, parent source, linked context, acceptance criteria, blockers, and out-of-scope boundaries. `skills/custom/implement/SKILL.md:36-40` | Define enough pre-edit context without turning selection into triage or product discovery. |
| Bounded slice | Treat selected issue as one bounded tracer-bullet/support slice. `skills/custom/implement/SKILL.md:40-42` | Research one-slice discipline and adjacent-work resistance. |
| Ask/stop rule | Ask only when implementation would be guesswork or the better approach changes a commitment. `skills/custom/implement/SKILL.md:42-44`, `docs/agents/engineering-contract.md:32-40` | Sharpen user-owned commitment boundaries without making the agent timid. |
| Implementation | Choose one approach, make the narrow change, prove load-bearing internals through meaningful seams. `skills/custom/implement/SKILL.md:46-56` | Research local approach choice, load-bearing internals, and semantic proof without duplicating design/TDD skills. |
| Proof / validation | Use red-green-refactor when suitable; prove semantic correctness; run focused checks and full/repo-standard validation when feasible. `skills/custom/implement/SKILL.md:54-62`; `.tmp` preserves typecheck, single tests, and full suite at end. `.tmp/.../implement/SKILL.md:9-12` | Keep source proof cadence while adapting it to current repo-local behavior. |
| Simplification | Simplify only while behavior is protected. `skills/custom/implement/SKILL.md:58-64` | Decide later how much cleanup/refactor guidance belongs in `implement`. |
| Review | Run `$review` against the starting ref; fix in-scope findings; record out-of-scope findings. `skills/custom/implement/SKILL.md:66-70`; `.tmp` says use `/review` once done. `.tmp/.../implement/SKILL.md:13` | Preserve review invocation and fixed point while leaving review procedure to `$review`. |
| Lock | Commit, leave implementation note, and avoid issue-state changes unless requested or repo-defined. `skills/custom/implement/SKILL.md:72-78`; `.tmp` preserves commit. `.tmp/.../implement/SKILL.md:15` | Research final handoff evidence and issue-state restraint. |
| Completion criteria | Done means one issue implemented, reviewed, committed, noted, validation recorded, unrelated work preserved, and issue-state changes controlled. `skills/custom/implement/SKILL.md:80-82` | Keep done checkable and resistant to premature completion. |

## 3. Owner Map

| Behavior / Concept | Current Owner | Keep Here / Point Elsewhere / Unclear | Why |
| --- | --- | --- | --- |
| One ready issue through implementation | `implement` | Keep here | This is the skill's core job. |
| Upstream compact implementation spine | `.tmp` source skill | Keep as source pressure | It preserves TDD/check/review/commit as the original minimum contract. |
| Explicit-only routing | `skills/custom/implement/agents/openai.yaml` and skill config | Keep here / point to config | `implement` is heavy and should not become an implicit general coding router. |
| PRD/spec decomposition into issues | `to-issues` | Point elsewhere | `to-issues` creates dependency-ordered bounded slices and names `$implement` as next step. `skills/custom/to-issues/SKILL.md:38-94` |
| Ready-state promotion and Codex-ready briefs | `triage` | Point elsewhere | `triage` owns state roles, verification, Codex-ready brief comments, and label changes. `skills/custom/triage/SKILL.md:29-50`, `:118-141` |
| Tracker commands and label strings | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` | Point elsewhere | Repo docs own exact GitHub commands, issue/PR distinction, and label mappings. |
| Engineering convergence loop | `docs/agents/engineering-contract.md` | Keep local execution slice / point elsewhere for theory | `implement` executes parts of the loop but should not duplicate the full contract. |
| Domain vocabulary and ADR routing | `docs/agents/domain.md`, root `CONTEXT.md`, `docs/adr/` | Point elsewhere with local read gate | `implement` should consume domain terms when coding/testing/notes/commits, not create missing domain docs. |
| Dirty work and starting ref | `implement` | Keep here | Pre-edit safety and review fixed point must happen before implementation. |
| Fixed-point review procedure | `review` | Point elsewhere with local handoff gate | `implement` captures the fixed point and invokes `$review`; `$review` owns Standards/Spec review. `skills/custom/review/SKILL.md:21-113` |
| Red-green-refactor mechanics | `tdd` | Point elsewhere with proof gate | `implement` decides when TDD is suitable; `$tdd` owns the full workflow. `skills/custom/tdd/SKILL.md:55-120` |
| Bug diagnosis when repro/cause is uncertain | `diagnosing-bugs` | Unclear / Prompt 02 boundary | Current skill does not mention this; Prompt 02 should decide if uncertain bug work needs a handoff gate. |
| Seam/interface design vocabulary | `codebase-design` / engineering contract | Unclear / Prompt 02 boundary | Current skill uses seams and load-bearing internals; Prompt 02 should decide if this is a facet or a pointer. |
| Commitment boundaries | Engineering contract plus `implement` | Keep local operational rule / point elsewhere for definitions | `implement` needs an ask gate, but contract owns broad commitment vocabulary. |
| Protected simplification | `implement` plus engineering contract | Keep here, boundary unclear | Simplification after proof is part of implementation, but broad refactor campaigns belong elsewhere. |
| Commit and implementation note | `implement` plus tracker docs | Keep here | Lock evidence is part of done; issue-state changes remain user/repo controlled. |

## 4. Preserve Inventory

| Current Behavior | Source File / Line Or Section | Why It Must Not Regress |
| --- | --- | --- |
| Explicit-only policy | `skills/custom/implement/agents/openai.yaml:1-2` | Prevents a heavy workflow from firing as a generic coding helper. |
| Upstream minimal proof/review/commit spine | `.tmp/mattpocock-skills/skills/engineering/implement/SKILL.md:7-15` | The current skill should deepen behavior without losing the original closeout contract. |
| One-issue WIP limit | `skills/custom/implement/SKILL.md:8-10` | Prevents broad PRD sweeps and multi-issue sessions. |
| Named issue/path/URL precedence | `skills/custom/implement/SKILL.md:10` | Honors explicit user target before auto-selection. |
| PRD/spec resolves to one ready issue | `skills/custom/implement/SKILL.md:10` | Keeps `implement` downstream of planning/issue creation. |
| Setup docs required before implementation | `skills/custom/implement/SKILL.md:14` | Prevents generic behavior when repo-local contract/tracker truth is missing. |
| Domain docs read when touching codebase context | `skills/custom/implement/SKILL.md:16`, `docs/agents/domain.md:7-28` | Keeps code, tests, notes, and commits aligned with repo language and ADRs. |
| Dependency-order ready issue selection | `skills/custom/implement/SKILL.md:22-26` | Avoids blocked work and arbitrary priority choices. |
| Dirty tree inspection | `skills/custom/implement/SKILL.md:28-34` | Protects unrelated user work. |
| Starting ref capture | `skills/custom/implement/SKILL.md:32` | Makes fixed-point review possible. |
| In-scope staging/commit boundary | `skills/custom/implement/SKILL.md:34` | Prevents unrelated changes entering the final commit. |
| Full issue/context read before implementation | `skills/custom/implement/SKILL.md:36-40` | Preserves product intent, acceptance criteria, blockers, and non-goals. |
| `.tmp/` disposable exploration | `skills/custom/implement/SKILL.md:42`, `docs/agents/engineering-contract.md:75-81` | Reduces uncertainty without leaving scratch behind. |
| Commitment-boundary ask rule | `skills/custom/implement/SKILL.md:44`, `docs/agents/engineering-contract.md:32-40` | Prevents silent changes to user-owned decisions. |
| Agent technique autonomy | `skills/custom/implement/SKILL.md:48` | Avoids unnecessary questions about ordinary implementation technique. |
| No adjacent tracer bullets/support slices | `skills/custom/implement/SKILL.md:50-52` | Keeps one implementation run bounded and reviewable. |
| TDD when suitable | `skills/custom/implement/SKILL.md:54`, `.tmp/.../implement/SKILL.md:9`, `skills/custom/tdd/SKILL.md:8-14` | Prevents after-the-fact checks from replacing red-green-refactor when appropriate. |
| Semantic correctness over output existence | `skills/custom/implement/SKILL.md:54`, `docs/agents/engineering-contract.md:42-65` | Requires evidence that the result means the right thing. |
| Focused checks and full/repo-standard validation when feasible | `skills/custom/implement/SKILL.md:56-62`, `.tmp/.../implement/SKILL.md:11` | Keeps feedback tight while preserving broader confidence. |
| Simplify only while behavior is protected | `skills/custom/implement/SKILL.md:64` | Allows cleanup without hidden scope expansion. |
| `$review` from starting ref | `skills/custom/implement/SKILL.md:68`, `skills/custom/review/SKILL.md:21-31` | Keeps review tied to the actual diff. |
| Fix in-scope review findings, record out-of-scope | `skills/custom/implement/SKILL.md:68-70` | Prevents review from widening the issue. |
| Commit with issue reference | `skills/custom/implement/SKILL.md:74`, `.tmp/.../implement/SKILL.md:15` | Makes the work durable and traceable. |
| Implementation note includes SHA, summary, validation, skipped checks, risk | `skills/custom/implement/SKILL.md:76` | Lets future humans/agents audit the work. |
| Issue state changes are controlled | `skills/custom/implement/SKILL.md:78` | Preserves tracker and user authority. |
| Done is implemented, reviewed, committed, noted, validated, and isolated | `skills/custom/implement/SKILL.md:80-82` | Resists premature completion. |

## 5. Failure Modes To Prevent

- Compacting the current skill back toward the `.tmp` source and losing the
  ready-issue executor shape.
- Letting a broader PRD/spec become implementation scope instead of selecting
  one ready issue.
- Implementing several ready issues because they share files or are nearby.
- Creating, rewriting, or promoting issues instead of routing to `to-issues` or
  `triage`.
- Selecting a blocked issue or silently guessing dependency order.
- Starting edits before reading the engineering contract, tracker docs, label
  mapping, and relevant domain docs.
- Starting edits before dirty-work inventory and starting ref capture.
- Staging or committing unrelated user work.
- Reading only an issue title while missing comments, parent source, blockers,
  acceptance criteria, or non-goals.
- Turning context intake into product discovery or issue repair.
- Asking the user about ordinary technique inside the bounded slice.
- Failing to ask when the better implementation changes product intent,
  acceptance criteria, public contracts, data semantics, security/privacy, or
  slice scope.
- Adding adjacent behavior, extra tracer bullets, or support work because the
  files are already open.
- Treating generated artifacts, smoke output, or command success as semantic
  correctness.
- Duplicating `$tdd` instead of invoking/following it where appropriate.
- Testing brittle internals instead of the highest useful seam.
- Duplicating `$review` instead of preserving its fixed-point handoff.
- Leaving `.tmp` scratch or exploration scaffolding in the final diff.
- Running broad simplification/refactor without behavior protection.
- Fixing out-of-scope review findings inside the implementation slice.
- Ending without a commit, implementation note, validation record, skipped
  checks, residual risk, or commit SHA.
- Closing, relabeling, or changing issue state without user/repo authority.
- Letting the convergence loop become decorative rather than gate-driven.

## 6. Rough Facet Candidates

These are rough candidates only. Prompt 02 owns final facet names, ordering,
merge/split decisions, and artifact paths.

| Facet | Behavior Surface | Research Question | Source Lanes | Evidence Gate | Stop/Ask Rule | Preliminary Keywords |
| --- | --- | --- | --- | --- | --- | --- |
| Ready Issue Selection | invocation, first action, tracker lookup, PRD/spec handoff | How should `implement` select exactly one ready issue-equivalent item, or stop when none is safe? | delivery/WIP, backlog readiness, issue workflows, agent task suitability | One selected issue is named with selection source, ready authority, blocker/dependency status, and reason. | Ask on ambiguous ordering; stop on no ready issue or PRD/spec without one ready slice. | ready-for-agent, definition of ready, pull system, WIP limit, blocked issue, dependency order, issue as prompt |
| Baseline And Fixed Point | worktree inspection, starting ref, staging boundary | What must be captured before editing so unrelated work is preserved and review/commit remain trustworthy? | version control, code review, change isolation, commit hygiene | Dirty-work inventory and starting ref are known before edits; staged files are in-scope. | Stop when baseline cannot be established or unrelated work cannot be preserved safely. | fixed point, baseline, dirty working tree, change isolation, atomic commit, clean diff |
| Context Intake Before Editing | issue/comments/source reading, domain docs | What context must the agent read before coding so implementation is not guesswork? | requirements engineering, issue briefs, specification by example, domain-driven design, agent context engineering | Product intent, acceptance criteria/proof hints, blockers, non-goals, domain terms, and linked source are identified. | Ask or route upstream when expected behavior/proof cannot be defined. | Codex-ready brief, acceptance criteria, linked context, parent PRD, blockers, non-goals, domain vocabulary |
| Bounded Slice Control | scope gates, adjacent work, tracer/support distinction | How should one run stay small, valuable, provable, and reviewable? | vertical slicing, tracer bullets, story slicing, small batches, review size | Active work is one behavior or support proof; adjacent work is recorded as follow-up. | Ask/split/stop when proof requires another slice or mixed commitments. | bounded slice, tracer bullet, vertical slice, support slice, scope creep, follow-up, small batch |
| Commitment Boundary | ask rules, technique autonomy, user-owned decisions | Which decisions can the agent make autonomously, and which require stopping or asking? | product ownership, requirements ownership, ADRs, human-in-the-loop agents, public/data/security contracts | Agent proceeds on technique but stops at commitment changes. | Ask before changing product intent, acceptance criteria, user-visible behavior, public contracts, data semantics, security/privacy, dependencies/tooling, or slice boundary. | commitment boundary, technique belongs to agent, user-owned decision, public contract, data contract, security posture |
| Semantic Proof And TDD Handoff | validation, `$tdd` routing, acceptance proof | What proves the selected issue is semantically correct, and when should `implement` invoke/follow `$tdd`? | TDD, BDD, specification by example, test oracles, data validation, executable specs | Acceptance criteria are proven by tests/checks/examples/invariants or skipped with explicit residual risk. | Stop or ask when no meaningful proof path exists or behavior is too unclear for a red test. | semantic correctness, red-green-refactor, test oracle, executable specification, fixture, invariant, acceptance test |
| Seams And Load-Bearing Internals | seam choice, internal contracts, module boundaries | How should `implement` choose the highest useful seam and prove correctness-critical internals without duplicating design skills? | legacy-code seams, information hiding, contract tests, ports/adapters, deep modules, mocking discipline | Load-bearing internals have a contract and proof through a meaningful seam. | Ask or narrow when the only proof path is brittle or the seam change exceeds the slice. | seam, public interface, contract test, adapter, load-bearing internal, module depth, characterization test |
| Protected Simplification | cleanup, refactor, scratch disposal | How should simplification happen after proof without widening the issue or changing behavior? | refactoring, simple design, behavior-preserving change, preparatory refactoring, green refactor | Cleanup is in-scope, behavior-preserving, and protected by checks. | Stop when cleanup changes behavior, creates new commitments, or becomes a separate support slice. | green refactor, behavior-preserving, simple design, preparatory refactoring, cleanup boundary, scratch artifact |
| Review And Lock | `$review`, commit, implementation note, issue state restraint | What final evidence makes the result ready to hand off: reviewed, committed, noted, and honest about residual risk? | code review, Definition of Done, continuous delivery, commit hygiene, traceability, handoff notes | `$review` ran or skip is explained; commit contains in-scope files; issue note records evidence. | Stop if in-scope review findings remain or lock evidence is missing. | fixed-point review, Standards and Spec, implementation note, commit SHA, validation evidence, residual risk |
| Invocation And Skill Shape | description, explicit-only config, body size | How should the final skill preserve explicit-only invocation while staying compact and predictable? | skill writing, procedural instructions, human factors, agent instruction design | The description/config keep manual invocation; runtime body contains only behavior-changing gates. | Stop if proposed runtime text makes `implement` an implicit general coding router. | explicit-only, description, disable-model-invocation, context load, progressive disclosure, completion criterion |

## 7. Facet Collision Risks

| Candidate Facet | Likely Overlap | Risk If Researched Alone | Prompt 02 Boundary Question |
| --- | --- | --- | --- |
| Ready Issue Selection | `to-issues`, `triage`, Context Intake | Selection research may turn into issue creation, issue repair, or full context reading. | What is the smallest local readiness recheck `implement` owns before routing upstream? |
| Baseline And Fixed Point | Review And Lock, `$review` | Git/review guidance may duplicate final review procedure. | Should baseline and lock be separate facets or one lifecycle facet? |
| Context Intake Before Editing | `triage`, Commitment Boundary, domain docs | Intake may become product discovery, brief repair, or domain-modeling. | Where does "read enough" stop before it becomes triage/grilling/domain-modeling? |
| Bounded Slice Control | Semantic Proof, Protected Simplification, `to-issues` | Slice guidance may duplicate issue splitting or later execution scope control. | Which scope decisions happen during issue creation versus implementation? |
| Commitment Boundary | Engineering contract, Context Intake, Seams | The skill may over-ask about technique or under-ask about user-owned commitments. | Which commitment terms must be inline for `implement`, and which can be contract pointers? |
| Semantic Proof And TDD Handoff | `$tdd`, engineering contract, Seams | Research may copy the full TDD workflow or become a testing manual. | What proof gate should `implement` own before deferring to `$tdd`? |
| Seams And Load-Bearing Internals | `codebase-design`, `$tdd`, engineering contract | Seam research may become module-design advice rather than implementation proof gating. | Does this merge with Semantic Proof, or become a pointer to design/TDD skills? |
| Protected Simplification | Bounded Slice Control, Review And Lock | Cleanup research can license broad refactors or out-of-scope review fixes. | What simplification is allowed inside one issue after behavior is protected? |
| Review And Lock | `$review`, tracker docs, Baseline | Lock research can duplicate review procedure or tracker conventions. | What should `implement` require before/after `$review` without owning `$review`? |
| Invocation And Skill Shape | writing-great-skills, explicit-only config | Final description/body work may become runtime wording too early. | Is invocation-shape a facet or a final compression concern after behavior research? |

## 8. Preliminary Keyword Bank

### Professional Software Engineering Terms

- definition of ready
- definition of done
- backlog refinement
- work item
- dependency order
- blocked issue
- WIP limit
- pull system
- tracer bullet
- vertical slice
- walking skeleton
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
- preparatory refactoring
- green refactor
- simple design
- small batch
- atomic commit
- logical commit
- reviewable diff
- fixed-point review
- traceability
- implementation note
- residual risk

### Agentic / LLM Execution Terms

- ready-for-agent
- Codex-ready brief
- issue as prompt
- bounded slice
- coding agent workflow
- agent-computer interface
- context engineering
- task localization
- tool feedback
- repair-validate loop
- completion criterion
- stop / ask / continue rule
- bounded autonomy
- evidence-backed completion
- scratch artifact
- handoff note
- fixed point
- prompt adequacy
- human oversight
- sensitive task
- ambiguous task

### Skill-Writing Terms

- explicit-only
- invocation policy
- skill description
- leading word
- completion criterion
- context pointer
- progressive disclosure
- branch
- single source of truth
- support reference
- no-op
- sprawl
- sediment
- premature completion
- owner boundary
- router skill
- context load

### Weak Or Noisy Terms

- implement
- agile
- best practices
- clean code
- quality
- done
- coding workflow
- software development lifecycle
- ship
- autonomous development
- agentic coding
- test everything
- be careful
- use judgment
- review code
- keep it simple

## 9. Source Search Seeds

### Ready Issue Selection

Search seeds:

- `definition of ready user story issue readiness`
- `backlog refinement ready for development dependency order`
- `Kanban pull system WIP limit work item selection`
- `GitHub issues workflow ready blocked labels`
- `coding agent issue prompt acceptance criteria`
- `LLM coding agent task specification issue description`
- `agent task selection ambiguity stop condition`

Avoid / demote:

- `agile implementation` because it is broad process fluff.
- raw issue-template catalogs because `triage` / `to-issues` own issue authoring.

### Baseline And Fixed Point

Search seeds:

- `git worktree preserve unrelated changes`
- `code review fixed point diff review`
- `atomic commits software engineering change isolation`
- `clean diff code review small changes`
- `staging only related files git best practices`
- `review from fixed point software`

Avoid / demote:

- generic Git tutorials because syntax is not the research target.

### Context Intake Before Editing

Search seeds:

- `software requirements acceptance criteria implementation issue`
- `specification by example acceptance criteria implementation`
- `coding agent context engineering task instructions`
- `issue brief enough context for implementation`
- `domain driven design ubiquitous language ADR implementation`
- `requirements ambiguity ask before implementation`

Avoid / demote:

- product discovery and PRD-writing material because this facet consumes ready
  context rather than creating it.

### Bounded Slice Control

Search seeds:

- `vertical slice software development thin slice`
- `tracer bullet software development feature slice`
- `small batch software delivery change size`
- `story slicing vertical slice acceptance criteria`
- `scope creep software engineering change request`
- `one self-contained change code review`

Avoid / demote:

- `MVP` alone because it drifts into product strategy.
- architecture-cleanup essays unless tied to one reviewable change.

### Commitment Boundary

Search seeds:

- `human in the loop software agents autonomy boundary`
- `requirements ownership acceptance criteria change control`
- `public API contract breaking change decision`
- `data migration semantics user approval software`
- `security privacy posture change approval engineering`
- `architecture decision record when to write ADR`

Avoid / demote:

- generic "ask the user" prompt-engineering advice because the skill needs
  precise stop/ask gates.

### Semantic Proof And TDD Handoff

Search seeds:

- `test driven development red green refactor seam`
- `semantic correctness software testing invariants fixtures`
- `test oracle software engineering acceptance tests`
- `specification by example executable specification`
- `characterization tests legacy code seams`
- `LLM coding agent validation tests completion criteria`

Avoid / demote:

- generic testing-best-practices lists because `$tdd` owns detailed mechanics.

### Seams And Load-Bearing Internals

Search seeds:

- `working effectively with legacy code seams`
- `contract testing ports adapters interface seam`
- `information hiding deep modules software design`
- `test through public interface not private methods`
- `load bearing internal behavior contract test`
- `mocking at system boundaries testing`

Avoid / demote:

- broad architecture rewrite sources unless they address proof through seams.

### Protected Simplification

Search seeds:

- `refactoring behavior preserving tests green refactor`
- `preparatory refactoring small steps`
- `simple design refactoring tests`
- `cleanup scope creep code review`
- `scratch artifacts cleanup software workflow`

Avoid / demote:

- clean-code advice that is not tied to protected behavior or a bounded slice.

### Review And Lock

Search seeds:

- `code review checklist fixed point standards spec`
- `definition of done validation evidence residual risk`
- `commit message issue traceability validation`
- `pull request description validation skipped tests risk`
- `implementation note commit sha validation`
- `software traceability issue commit`

Avoid / demote:

- full PR publication, merge, release notes, or changelog sources unless Prompt
  02 decides lock should own them.

### Invocation And Skill Shape

Search seeds:

- `procedural instructions completion criteria human factors`
- `LLM tool use workflow instructions trigger conditions`
- `prompt engineering procedural task instructions completion criteria`
- `agent skill explicit invocation context load`
- `progressive disclosure documentation task instructions`

Avoid / demote:

- broad prompt-engineering advice that does not change skill predictability.

## 10. Boundaries Before Research

Research should not put the following directly into `SKILL.md`:

- full agile/Scrum/Kanban theory;
- full Git tutorials;
- full TDD procedure;
- full review procedure;
- full issue-writing or triage templates;
- full domain-modeling or ADR guidance;
- full architecture/design advice;
- source-specific examples that do not change runtime behavior.

Another skill or contract probably owns:

- `to-issues`: PRD/spec decomposition and dependency-ordered issue creation;
- `triage`: readiness verification, Codex-ready briefs, label/state changes;
- `$tdd`: red-green-refactor mechanics and detailed test examples;
- `$review`: fixed-point Standards/Spec review procedure;
- `codebase-design`: broad module/interface/seam design vocabulary;
- `domain-modeling`: durable domain terms and ADR-worthy decisions;
- engineering contract: shared convergence loop and commitment vocabulary;
- repo tracker/domain docs: exact commands, labels, and domain doc locations.

Over-research would look like:

- collecting generic Agile/testing/Git/review advice that does not change agent
  behavior;
- making `implement` a duplicate of the engineering contract;
- researching issue authoring instead of issue pickup;
- treating source prestige as more important than actionable gates;
- expanding from one-issue implementation to general autonomous software
  development.

A source is worth keeping if it can improve:

- a selection gate;
- a stop/ask rule;
- a proof/evidence standard;
- a bounded-slice decision;
- an owner-boundary pointer;
- a completion criterion;
- a leading word that reliably steers Codex behavior.

## 11. Questions For Prompt 02

- Should Ready Issue Selection remain its own first facet, or merge with
  Context Intake / Bounded Slice Control?
- What is the smallest local readiness recheck `implement` owns without
  absorbing `triage`?
- How should Prompt 02 account for the `.tmp` source skill's minimal
  proof/review/commit spine while preserving the current ready-issue executor
  shape?
- Should Invocation And Skill Shape be researched as a facet, or deferred until
  final compaction and runtime patching?
- Does Baseline And Fixed Point deserve a separate pre-edit facet from Review
  And Lock, or are they one lifecycle of diff integrity?
- Where does Context Intake stop before it becomes issue repair, product
  discovery, grilling, or domain modeling?
- Should Semantic Proof and Seams/Load-Bearing Internals be one facet because
  both shape proof, or split because one is validation and one is design?
- How much TDD guidance belongs in `implement` before it should simply invoke
  or follow `$tdd`?
- How much review guidance belongs in `implement` before it should simply hand
  off to `$review`?
- Should bug diagnosis be an explicit owner-boundary question for uncertain
  repro/cause work?
- What final evidence belongs in the implementation note versus tracker docs or
  review output?
- Which current behaviors are contract pointers rather than inline runtime
  steps?

## 12. Output Summary

Intent decision: `ready-for-facet-map`

Top rough facets / facet-map questions Prompt 02 should resolve:

- Ready Issue Selection: what local pickup gate `implement` owns before context
  intake.
- Baseline And Fixed Point: what must happen before editing to protect dirty
  work and review.
- Context Intake / Bounded Slice / Commitment Boundary: how to split "read
  enough," "stay bounded," and "ask on user-owned changes."
- Semantic Proof / Seams / TDD Handoff: how to prove correctness without
  duplicating `$tdd` or `codebase-design`.
- Review And Lock: what closeout evidence `implement` owns without duplicating
  `$review` or tracker policy.

Strongest preliminary search terms:

- ready-for-agent
- definition of ready
- issue as prompt
- WIP limit
- fixed point
- bounded slice
- tracer bullet
- commitment boundary
- semantic correctness
- test oracle
- red-green-refactor
- load-bearing internal
- behavior-preserving refactor
- fixed-point review
- implementation note
- residual risk
- explicit-only
- completion criterion

Highest-risk owner boundaries to preserve:

- `implement` selects one ready issue; `to-issues` creates issues.
- `implement` rechecks local pickup safety; `triage` verifies and promotes
  readiness.
- `implement` captures the fixed point; `$review` owns review procedure.
- `implement` demands proof; `$tdd` owns red-green-refactor mechanics.
- `implement` consumes domain/tracker docs; repo docs own exact terms and
  commands.
- `implement` asks at commitment boundaries; the engineering contract owns the
  shared commitment vocabulary.

Biggest risk if rewritten without research:

- The skill either regresses toward the `.tmp` minimal launcher and loses the
  unattended ready-issue safety gates, or it sprawls into a duplicate of
  `to-issues`, `triage`, `$tdd`, `$review`, and the engineering contract.

Likely shape of the eventual compact skill change:

- Preserve the current ready-issue executor shape.
- Compress the body around checkable gates: select one issue, baseline, intake,
  bounded implementation, proof, protected simplification, review, lock.
- Move rationale and source vocabulary behind support/reference pointers where
  needed.
- Keep exact tracker/domain details in repo docs.
- Keep `$tdd` and `$review` as owner handoffs rather than copied workflows.
