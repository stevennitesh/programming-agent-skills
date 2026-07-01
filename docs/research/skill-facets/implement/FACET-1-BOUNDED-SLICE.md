# Facet 1 Research: Bounded Slice

Research question:

> How do strong teams keep implementation work small, valuable, independently provable, and reviewable?

This facet should improve `implement` around issue selection, slice boundaries, proof, adjacent-work restraint, and the stop condition.

## Decision Summary

Research completeness: **8/10**.

Skill-edit readiness: **8.5/10**.

Decision: the packet is ready to propose a compressed `implement` edit. Apply
it only after explicit runtime-skill approval, and do not copy the research
into the skill.

The first-pass payload was right but a little under-specified. The second pass sharpened four things:

- story mapping sharpened `issue` into `one user/caller/operator activity or path`;
- review research sharpened `reviewable change` into `one self-contained change`;
- delivery research sharpened `small batch` into `reviewable, validated, recoverable as one unit`;
- agentic research sharpened `proof` into a `stop condition` after failed validation.

Runtime payload:

```text
pre-edit lock on one activity/path
  -> outside proof
  -> one self-contained reviewable change
  -> related proof travels with the diff
  -> validation failure stays inside the locked slice
  -> follow-ups in note, not diff
```

## Third-Pass Rating

Four review agents rated the packet for this goal:

> higher quality programming by encoding strong signal language for upper-bound behavior, not average behavior.

Ratings: **8/10**, **8/10**, **8/10**, and **8.2/10**.

Consensus:

- The packet is strong enough to propose an `implement` edit.
- The source research is useful, but the runtime wording must be much smaller.
- The strongest leading words are `tracer bullet`, `outside proof`, `one self-contained reviewable change`, `related proof travels with the diff`, `stop, split, or ask`, and `No proof, no done`.
- `one activity/path is the WIP limit` is conceptually right but too awkward for runtime; use `Before editing, lock one user-, caller-, or operator-visible activity/path`.
- The pre-edit lock must be concrete: activity/path, outside proof, likely in-scope areas, explicit non-goals, and the stop/split trigger.
- Add one compact good/bad slice contrast so the research stays practical.

Promoted synthesis target: see
[`../../../synthesis/skills/implement.md`](../../../synthesis/skills/implement.md).
This research packet preserves the evidence, rejected alternatives, gates, and
remaining gaps behind that wording.

## Second-Pass Triage

Four subagents researched the remaining gaps: story mapping, code-review size, batch risk, and agentic coding behavior.

Accepted suggestions:

- Lock the slice by `one user/caller/operator activity or path`, not only by issue title.
- Add a batch boundary: what will change, what will not, and how the result can be reviewed, validated, and recovered as one unit.
- Use `one self-contained change`, `one concept`, and `related proof travels with the diff` as reviewability handles.
- Add a proof-failure rule: if validation fails, iterate inside the locked slice; if the needed fix changes the slice, stop, split, or ask.
- Promote agentic coding evidence from deferred gap to active support, but keep agent-framework jargon out of runtime wording.

Rejected suggestions:

- Do not add a story-mapping section to `SKILL.md`.
- Do not encode hard LOC thresholds or claim that small PRs automatically merge faster.
- Do not import trunk-based delivery, DORA metrics, ReAct, Reflexion, or multi-agent taxonomy into the runtime skill.
- Do not make `walking skeleton` the default path for every issue.
- Do not turn bounded slicing into "as small as possible"; the target is the smallest useful proof-carrying batch.

Deferred suggestions:

- Add exact book chapter/page citations later if this research becomes public-facing.
- Extend the shared agentic bridge/source docs if multiple facets reuse the
  same AI-agent sources.
- Add deeper source treatment for feature flags / branch by abstraction if future facets cover long-running change.

## Source Tiers

Use these tiers when deciding what survives into the skill.

### Core Engineering Canon

These sources donate the main runtime vocabulary.

| Source | Attention Handles | What It Should Make The Agent Do |
| --- | --- | --- |
| *The Pragmatic Programmer*, Hunt and Thomas, `Tracer Bullets`; Artima interview | `tracer bullet`, `under real conditions`, `adjust aim` | Build one small real path through the system before adding breadth. |
| Jeff Patton, *User Story Mapping*; `The New User Story Backlog is a Map` | `user activity`, `backbone`, `release slice`, `thin slice` | Slice by a user/caller/operator activity or path, not by folder, layer, or nearby work. |
| *Growing Object-Oriented Software, Guided by Tests*, Freeman and Pryce | `outside proof`, `acceptance test`, `walking skeleton`, `feedback` | Start where done is visible; identify the outer proof, then drive inward until it passes. |
| Google Engineering Practices and *Software Engineering at Google*, small CLs | `one self-contained change`, `addresses one thing`, `reviewable change`, `code health` | Shape the diff as one coherent issue with related proof and reviewer-needed context. |
| Kent Beck, *Extreme Programming Explained* and *Test-Driven Development by Example* | `small releases`, `customer tests`, `simple design`, `red-green-refactor` | Keep the slice small, proved, and simple while behavior is protected. |
| Michael Feathers, *Working Effectively with Legacy Code* | `characterization test`, `seam`, `sprout`, `wrap` | For support or legacy work, create a safe proving seam before changing behavior. |
| Gojko Adzic, *Specification by Example* and example mapping | `examples`, `business rules`, `acceptance tests`, `pass/fail proof` | Translate activity/path into concrete examples and observable proof. |

### Empirical Review Support

These strengthen the skill's confidence but should donate only compact runtime language.

| Source | Attention Handles | What It Should Make The Agent Do |
| --- | --- | --- |
| Sadowski et al., `Modern Code Review: A Case Study at Google` | `small changes`, `lightweight review`, `few files` | Treat broad file spread and mixed concepts as reviewability smells. |
| Bosu, Greiler, and Bird, `Characteristics of Useful Code Reviews` | `useful review comments`, `file count`, `review usefulness` | Prefer coherent changes; file spread can reduce reviewer usefulness even when LOC is modest. |
| di Biase et al., `The effects of change decomposition on code review` | `change decomposition`, `separate concepts`, `wrongly reported issues` | Split concepts before coding; do not mechanically split work that still belongs together. |
| Rigby/Bird and Bacchelli code-review work | `modern code review`, `review comprehension`, `review purpose` | Treat reviewability as comprehension and maintainability, not only defect finding. |

### Delivery Economics

These support batch-size, validation, and recoverability.

| Source | Attention Handles | What It Should Make The Agent Do |
| --- | --- | --- |
| Humble and Farley, *Continuous Delivery* | `release candidate`, `green build`, `deployment pipeline`, `fast feedback` | Leave the repo in a validated state; do not finish in a broken middle state. |
| *Accelerate* and DORA small-batch writing | `small batches`, `fast feedback`, `easy remediation`, `delivery performance` | Treat the slice as a batch that should be quick to verify and recover from. |
| Reinertsen, *The Principles of Product Development Flow* | `batch size`, `queues`, `WIP`, `cost of delay`, `feedback` | Prevent tiny-for-tiny's-sake; optimize for learning, proof, review, and recovery. |

### Agentic Translation

These justify constrained workflows and validation loops, not software-engineering taste by themselves.

| Source | Attention Handles | What It Should Make The Agent Do |
| --- | --- | --- |
| Anthropic, `Building Effective Agents` | `simple agents`, `clear interfaces`, `success criteria`, `feedback loops` | Keep the workflow constrained and test-verifiable; use tools and tests to converge. |
| OpenAI Codex prompting and best practices docs | `focused tasks`, `test expectations`, `acceptance criteria`, `diff review` | Give Codex a bounded task, explicit success criteria, and concrete verification. |
| SWE-agent and Agentless | `agent-computer interface`, `localize-repair-validate`, `constrained workflow` | Favor tight localization, repair, and validation over freeform autonomy. |
| SWE-bench, ReAct, and Reflexion | `real issue`, `tool feedback`, `feedback loop` | Use tool/test feedback to converge inside the slice; keep the jargon out of `SKILL.md`. |

### Supporting Sources

These reinforce the behavior but should rarely donate final wording directly.

| Source | Useful Support | Use Carefully |
| --- | --- | --- |
| Humanizing Work, `Guide to Splitting User Stories` | Strong practical guard against horizontal layer slicing. | Good for rejecting layer work; avoid importing too much Agile slicing taxonomy. |
| Agile Alliance, `Story Splitting`, `User Stories`, and `Given-When-Then` | Functional increment; observable consequence; vertical slices. | Good for proof shape; generic if not tied to a real seam. |
| Mountain Goat / Mike Cohn story mapping and SPIDR writing | Practical splitting heuristics. | Useful in research; too much taxonomy for runtime skill wording. |
| Scrum Guide / Scrum Alliance DoD and DoR | Ready vs done; usable and verified. | Can become ceremonial; translate into concrete evidence gates. |
| Kanban Method / product-flow writing | WIP limits; finish before pulling more. | Strong only when concretized as `one issue is the WIP limit`. |
| Lean Software Development and Lean Product and Process Development | Eliminate waste; partially done work is waste; rapid learning. | Useful for pruning extras; avoid generic lean slogans. |
| SmartBear / Cisco lightweight review case study | Numeric intuition about review size and inspection rate. | Keep numbers out of runtime skill text. |
| Alistair Cockburn, `Walking Skeleton` | Connect the main components with the smallest end-to-end function. | Conditional only: use for new or uncertain system shape, not every issue. |

### Counterweights

These prevent overclaiming.

| Source | What It Prevents |
| --- | --- |
| Kudrjavets, Nagappan, and Rastogi, `Do Small Code Changes Merge Faster?` | Do not claim small changes automatically merge faster. |
| Reinertsen batch-size economics | Do not make `small` mean tiny-for-tiny's-sake; optimize for learning, proof, review, and recovery. |
| Agentless | Do not assume more autonomy or more agent framework improves coding behavior. |
| Support-slice reality | Do not imply every slice is user-visible; support slices may be maintainer-visible or operator-visible when they are explicit and observable. |

## High-Signal Language

This is the part that should survive into skill wording if space is tight.

```text
lock one activity/path before editing
  -> tracer bullet
  -> outside proof
  -> best practical seam
  -> one self-contained reviewable change
  -> related proof travels with the diff
```

### Strong Terms

| Term | Why It Moves Behavior |
| --- | --- |
| `lock one activity/path before editing` | Stops scope creep better than anchoring only to an issue title. |
| `tracer bullet` | Pushes the agent to build one real path through the system, not isolated pieces. |
| `outside proof` | Makes the agent start from the visible acceptance check instead of implementation internals. |
| `best practical seam` | Sharpens where to test: outside-facing enough to catch the promised behavior, without needless end-to-end cost. |
| `one self-contained change` | Shapes the diff around one concept, not several adjacent discoveries. |
| `related proof travels with the diff` | Prevents code-only changes that rely on future validation. |
| `file spread is review size` | Catches broad, hard-to-review diffs that may not have many lines. |
| `do not broaden after failed proof` | Converts validation failure into a stop/split/ask gate. |
| `not a spike` / `production-shaped` | Prevents the agent from counting exploration code as implementation. |

### Weak Or Generic Terms

These terms are useful as background, but weak alone. Sharpen them or leave them out of final skill wording.

| Term | Better Shape |
| --- | --- |
| `small` | `small enough to prove, review, validate, and recover as one unit` |
| `valuable` | `observable user/caller/operator behavior` |
| `testable` | `outside proof through the highest useful seam` |
| `acceptance criteria` | `pass/fail commitments` |
| `Definition of Done` | `No proof, no done` |
| `vertical slice` | `one activity/path through the real system` |
| `small batch` | `one locked activity/path with proof` |
| `flow` | Usually omit from skill wording. |
| `done means usable and verified` | `usable for its promised purpose, with validation evidence` |

### Good/Bad Slice Contrast

Bad slice:

```text
Add parser behavior, update config plumbing, clean old docs, fix nearby lint, and adjust an unrelated edge case.
```

Good slice:

```text
Add one parser behavior, prove it with a fixture through the parser's public seam, and note config/docs cleanup as follow-up.
```

## Agent Behavior And Gates

### Behavior To Encode

The improved skill should make the agent:

- treat the selected activity/path as the active WIP limit;
- confirm the issue is ready enough to implement without guessing;
- name the outside proof before editing;
- name the pre-edit lock: activity/path, outside proof, likely in-scope areas, explicit non-goals, and stop/split trigger;
- prefer one tracer bullet through the real system for behavior work;
- use `walking skeleton` only for new or uncertain system shape;
- use a support slice only when it clearly unblocks or de-risks the behavior;
- avoid horizontal layer delivery unless the layer work is explicitly the support slice;
- keep related tests/proof with the diff;
- keep the diff explainable as one concept and one issue;
- iterate inside the locked slice when proof fails;
- stop, split, or ask when the needed fix changes the slice;
- record adjacent work as follow-up instead of widening the diff.

### Start Gate

A bounded slice is ready to start when:

- the issue has clear intent;
- the one user-visible, caller-visible, or operator-visible activity/path is identifiable;
- acceptance criteria or equivalent confirmation are testable;
- the outside proof is named;
- explicit non-goals and the stop/split trigger are named;
- hard blockers are absent, known, or addressable inside the slice;
- adjacent work can be named and left out of the diff.

### Done Gate

A bounded slice is done when:

- the promised behavior or support change is usable for its purpose;
- proof runs through the highest useful interface or seam;
- related proof travels with the diff;
- the diff is one self-contained reviewable change;
- repo-standard validation, or the strongest practical substitute, is recorded;
- the repo is not left in a broken middle state;
- adjacent improvements are left as follow-ups, not implemented in the slice.

### Split Or Ask Gate

Stop, split, or ask when:

- the slice cannot be proved from an outside check;
- the change spreads across unrelated files or concepts;
- behavior, broad cleanup, config, docs, and refactor work are mixing without necessity;
- validation failure requires work outside the locked slice;
- the implementation note would need multiple unrelated explanations.

### Plain-Language Gates

- Lock one activity/path before editing.
- Build one real path first.
- Slice by behavior, not by folder, layer, or component.
- No proof, no done.
- Related proof travels with the diff.
- If it cannot be proved, reviewed, validated, and recovered as one unit, split before coding.
- If proof fails, iterate inside the slice; if the slice changes, stop, split, or ask.
- Follow-ups go in the note, not the diff.
- Do not finish in a broken middle state.

## Synthesis Promotion

The chosen runtime-facing synthesis wording now lives in
[`../../../synthesis/skills/implement.md`](../../../synthesis/skills/implement.md).

This packet preserves source evidence, ratings, alternatives, rejected
suggestions, behavior gates, and gaps. Do not copy this research packet into
`SKILL.md`; promote through synthesis first.

## Prune Notes

Do not duplicate:

- detailed TDD mechanics from `tdd`;
- full review procedure from `review`;
- the whole convergence loop from `docs/agents/engineering-contract.md`;
- tracker publishing rules from `docs/agents/issue-tracker.md`;
- generic Agile glossary language that does not change agent behavior;
- agent-framework taxonomy that does not change coding behavior.

The `implement` skill should own:

- the decision to keep work to one bounded slice;
- the pre-edit lock on activity/path, proof, and out-of-scope work;
- the gate that proof must travel with the diff;
- the rule that adjacent work becomes follow-up, not scope expansion;
- the stop condition when failed proof would require a different slice.

## Remaining Research Gaps

These gaps should not block the first `implement` edit.

- Add exact bibliographic detail for book sources if the research becomes public-facing.
- Decide whether repeated agentic-bridge sources deserve a shared research document for multiple facets.
- Research feature flags / branch by abstraction only if later facets need long-running-change guidance.
- Gather repo-local transcript examples of scope creep, failed proof, and over-broad diffs to test the wording against real agent behavior.
