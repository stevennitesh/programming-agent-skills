# Proposed coding skill pack for GPT-6 Astra

Date: 2026-09-05. Status: read-only assessment and proposed design.

This note does not change the accepted pack composition, active instructions,
installed skills, or historical source pins. The user authorized the assessment,
three initial assessors, a subsequent debate with three agents, and this note.
No coding experiments or behavioral comparisons were run.

## Decision

I would build a smaller default pack around four on-demand methods:
`codebase-design`, `diagnosing-bugs`, `research`, and `change-review`.
Ordinary implementation would proceed directly under a short engineering
contract, repository facts, and precise pointers to relevant proof methods.

I would keep the useful specialized workflows separately available. Domain
modeling and writing instructions are particularly valuable for the projects
that need them, including this repository. Their value does not require loading
their procedures during every coding task.

The largest change should be to the instruction structure and activation rules,
not the amount of professional knowledge available. Remove repeated procedure,
unnecessary setup dependencies, and automatic ceremony. Preserve intended
meaning, evidence discipline, effect ownership, and recovery guarantees.

Four is a proposed starting configuration, not a proven optimum. The strongest
alternative is the same repository facts and short contract with no additional
default skills. That alternative must be included in a later comparison.

## Evidence and scope

| Source | Inspected identity | Coverage |
| --- | --- | --- |
| This repository | `9733d619d9d1104a1791b2e2392aeb1a3b189da1` | All 27 active skill entrypoints, relevant references, engineering/setup context, selected lane and installation mechanisms; both extras assessed for separation |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | 37 entrypoints inventoried; substantive engineering and selected productivity methods and references inspected |
| Pstack in cursor/plugins | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | 45 main entrypoints, including 21 principle skills, inventoried; three Benny automation entrypoints also catalogued; engineering, verification, evidence and selected orchestration methods inspected |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | 14 entrypoints inventoried; substantial planning, delegation, review, verification and isolation methods inspected |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | All six entrypoints and benchmark-method disclosures inspected |

The [refresh note](upstream-refresh-2026-09-05.md) records clone locations,
before/after commits, older research pins, and the distinction between changes
fetched today and changes already present in the clones.

The initial independent assignments were:

- `upstream_methods`: Matt Pocock and Pstack methods, with inventory and exclusions.
- `local_pack`: 21 active local skills and two extras.
- `orchestration`: six remaining local skills, Superpowers and Ponytail.

The root assessed current runtime guidance, repository context and enforcement,
and integrated the findings. Three fresh agents then challenged the proposal
through minimalism, reliability and usability lenses. Each received the peer
objections and the revised proposal for a rebuttal. The debate is recorded below.

This was a source-based design assessment. It was not an exhaustive security
audit of upstream hooks, installers, every supporting script, specialist course
tooling, bot integrations, or every historical evaluation. Excluded specialist
material is not classified as low quality. No upstream benchmark was rerun.

## What Astra changes, and what it does not establish

Official guidance describes Astra as more sensitive to instructions and calls
out possible over-clarification, overly broad testing, verbose responses, and
less delegation than a workflow expects. That supports calibrating instructions
to the task. It does not prove that any particular local skill is unnecessary.
[Astra guidance](https://developers.openai.com/api/docs/guides/latest-model#gpt-6-astra-behavior)

This session supplies native tools for delegated agents, event waits, task
continuation, worktrees, shell operations and other applications. Their
availability is observed. Reliable use under every condition is not established.
In particular, this session already contains extensive developer and user
instructions. My apparent default behavior is not an uncontaminated measurement
of the model without the pack.

Installed skills, visible descriptions, implicit invocation and explicit
invocation are different. Codex initially exposes skill metadata and loads a
selected body later. Explicit-only invocation does not imply that metadata has
zero discovery cost. The local assertion in
[Skill mechanics](../../skills/custom/writing-for-agents/references/SKILL-MECHANICS.md)
that explicit-only spends no automatic context load needs runtime-specific
correction. [Current skills documentation](https://learn.chatgpt.com/docs/build-skills)

For this proposal, a default skill is installed and discoverable, with a narrow
task trigger. It is not always loaded and not a mandatory pipeline stage.
An optional module is installed for a project or working profile. Once installed,
its invocation policy depends on the method: relevant knowledge can be selected
from the task, while a costly campaign or a special interaction mode requires
the user's selection or an applicable repository contract.

## The professional knowledge worth retaining

Keep methods that change a consequential decision, expose a plausible mistake,
or preserve a project-specific commitment. General expertise alone does not
supply the user's meaning, the actual environment, or the evidence for a result.

| Knowledge | When it matters | What to keep |
| --- | --- | --- |
| Caller-first design | An interface, ownership or failure policy is unsettled | Sketch real usage, including errors and ordering; compare materially different choices; prefer a module that hides meaningful policy over forwarding layers |
| Domain meaning | Code, tests or participants disagree about a term or invariant | Intended meaning, authority, inclusion/exclusion examples, units, state transitions and relationships; distinguish observed behavior from desired behavior |
| Test discrimination | A normal example could also pass a plausible wrong implementation | Independent expected values, hand-checked examples, a reference oracle or a counterexample that distinguishes the accepted rule |
| End-to-end meaning | A changed boundary could drop accepted data, identity, availability or evidence | Pass actual produced output through the affected public transformations to an ordinary consumer; a reconstructed object does not prove the handoff |
| Success semantics | Termination and success conditions can disagree | Exercise a state where they disagree; exhausting a budget is not proof of the requested result |
| Causal diagnosis | The cause is uncertain or intermittent | A faithful reproducer, falsifiable explanations, discriminating probes, rates and relevant conditions; retain uncertainty when alternatives remain viable |
| Trust and valid representations | Input or state can violate a relied-on invariant | Validate at the boundary that owns the risk, derive types from existing schemas, and avoid duplicate validation inside a trustworthy representation |
| Migration | Consumers cannot all change atomically, or old behavior is displaced | Identify real compatibility commitments; use staged migration when necessary, otherwise migrate owned callers and remove displaced paths together |
| Effects and recovery | A retry, interruption or failure can leave partial effects | Identity, idempotency, read-back, partial-success handling, cancellation and cleanup at the actual effect boundary |
| Shared-state reasoning | Concurrent work can affect shared schemas, databases, ports, packages or fixtures | Exclusive ownership or serialization, lifecycle ordering, resource isolation and integrated proof; separate files alone are insufficient |
| Performance evidence | The result claims an improvement in time, cost, capacity or resources | Comparable workload and environment, a baseline, independently chosen acceptance threshold, uncertainty, and equivalent work |
| Historical rationale | A change depends on why a rule or safeguard exists | Contemporary decisions, incidents and commits; label inference rather than assigning intent from current code |
| Review judgment | A candidate needs independent assessment | A real obligation, reachable scenario, decisive evidence, consequence and proportionate correction; agreement is not evidence |

The local sources already contain much of this knowledge:
[engineering contract](../agents/engineering-contract.md),
[Implement proof guidance](../../skills/custom/implement/SKILL.md),
[finding contract](../../skills/custom/change-review/FINDING-CONTRACT.md),
[design](../../skills/custom/codebase-design/SKILL.md), and
[measured improvement](../../skills/custom/hillclimb/SKILL.md).
The detailed examples should remain available at one owner. Repetition across
skills should not be mistaken for additional protection.

Keep professional tradeoffs, not universal slogans. Internal types can be
invalidated by unsafe casts, mutation, concurrency or old persisted data.
Small diffs can hide wrong behavior. Higher-level tests do not automatically
make lower-level tests redundant. An abstraction can reduce total complexity
even when it adds lines. Apply each rule where its assumptions hold.

## Proposed pack structure

### Common context

The common contract should be short enough to read as guidance, not a checklist.
Its proposed content is:

> Complete the authorized outcome in the current behavior owner. Consult the
> repository's intended meaning and real callers before changing a contract.
> Ask only when a consequential choice remains unresolved; make routine
> implementation choices from available evidence.
>
> Prefer the smallest integrated design. Reuse existing mechanisms, model data
> clearly, and remove displaced paths when compatibility permits. Preserve
> unrelated work and the user's authority over external effects.
>
> Match proof to the claim. Use a counterexample when the ordinary case also
> fits a plausible wrong rule. Exercise actual output across a changed boundary
> that can lose accepted meaning. Check competing success conditions and
> material partial-effect recovery when those conditions apply.
>
> Run required and relevant checks. Reuse evidence while the code, inputs,
> dependencies, configuration and environment relevant to its claim remain
> valid. Broaden verification for demonstrated impact or unresolved risk.
>
> Report the result, decisive evidence and material limits. Do not turn an
> inactive concern into another workflow.

This is proposed wording, not newly applicable repository policy. It would need
precise local pointers at the proof and domain triggers. The complete reference
should not be copied into every worker prompt or ticket.

Missing guidance should trigger bounded investigation. Stop dependent work only
when missing information leaves a consequential decision unresolved. The absence
of a preferred document alone should not force repository bootstrap.

### Four candidate default skills

| Entry | Trigger | Unique result and limits |
| --- | --- | --- |
| `codebase-design` | A consequential module, interface, ownership, data or failure-policy choice is unresolved | A grounded design recommendation with caller examples and meaningful alternatives. Routine implementation does not need an architecture interview. |
| `diagnosing-bugs` | A requested investigation or repair has a causally uncertain failure | A supported cause or precise uncertainty, using faithful observations. Provisional hypotheses may guide reproduction; a perfect minimized repro is not a prerequisite for thinking. |
| `research` | A bounded question needs claim-owning sources and evidence judgment | A cited answer separating definitions, observed behavior, intent and empirical effects. A simple lookup should stay simple. |
| `change-review` | The user or repository requests judgment of an identified change | Verified findings or a bounded no-findings result against a fixed candidate. No automatic repair, new scope or universal reviewer ceremony. |

Keep research and diagnosis separate initially. Source authority and causal
experimentation need different evidence and completion conditions. An early
assessor suggested a single investigate skill; the root rejected that broader
merger because fewer names alone do not justify combining these modes.

### Optional profiles

The proposed complete library has 22 entrypoints: the four defaults and 18
optional entries below. This is a preservation-oriented catalog, not a
recommendation to install every entry. The small default and shorter shared
procedures are the main simplification; most specialized user intents remain
legitimate.

| Profile | Optional entries | Intended use |
| --- | --- | --- |
| Deliberate methods | `grilling`, `prototype`, `simplify-code`, `tdd`, `hillclimb` | A chosen interview, disposable experiment, behavior-preserving simplification, test-first cycle, or sustained measurement campaign |
| Domain | `domain-modeling` | Conflicting project meaning, invariants or durable domain capture; live-domain reconciliation includes the useful grill-with-docs ordering rule |
| Delivery | `durable-planning`, `parallel-implement`, `triage`, `wayfinder` | Durable specifications or graphs, accepted parallel delivery, tracker intake, or interdependent decisions spanning sessions |
| Assurance and Git | `high-assurance-review`, `audit-codebase`, `resolving-merge-conflicts` | Explicit independent review, a bounded baseline audit, or an active conflicted Git operation |
| Agent maintenance | `writing-for-agents`, `context-hygiene`, `repo-bootstrap` | Agent-consumed artifacts, context admission/pruning, and bounded repository setup including verification recipes |
| Human artifacts | `wizard`, `to-questionnaire` | A genuinely human-only secure procedure or a questionnaire for an external stakeholder |

For this skill-authoring repository, install the agent-maintenance profile.
For a domain-heavy application, install the domain profile. A team using issue
graphs installs the delivery components it actually uses. Preserve short
catalog descriptions so profiles can be found by ordinary language. An absent
optional module does not prevent competent direct work within the user's scope.

`durable-planning` would select the requested artifact first: specification,
ticket graph, or both. A specification records accepted intent. A graph also
allocates implementation ownership and dependencies. Each retains its own
admission and completion conditions. A draft does not authorize publication;
publication does not authorize implementation. Share only genuinely identical
publication mechanics. This is a conditional merger proposal, not an adopted
rename.

### Complete disposition of the 27 active skills

"Optional" retains a useful invocation and its professional content while
removing it from the generic default. It is not a recommendation to preserve
every line unchanged. "Reference" removes a standalone command while giving its
useful obligations a named owner.

| Current skill | Disposition | Keep or change |
| --- | --- | --- |
| `audit-codebase` | Optional, trim | Keep coverage and systemic-cause reasoning; make HTML and multi-stage report mechanics conditional on the requested artifact |
| `change-review` | Default, trim | Keep candidate identity and finding admission; remove repeated generic process and authority narration |
| `codebase-design` | Default, trim | Keep caller-first choices, information hiding and earned seams; remove duplicate simplicity instructions and obligatory presentation formats |
| `context-hygiene` | Optional | Keep semantic destinations and verified persistence; add information-access and tool-economy questions when session evidence warrants them |
| `diagnosing-bugs` | Default, trim | Keep discriminating investigation and honest uncertainty; avoid repeated route exclusions and extra admission conversations |
| `domain-modeling` | Optional, change | Keep meaning authority and durable records; allow bounded read-only investigation without a setup document, never infer intended meaning from code alone |
| `grill-with-docs` | Merge into domain reference | Preserve reconciliation after each settled answer and before dependent questioning; remove a wrapper-only entrypoint |
| `grilling` | Optional | Preserve a deliberately chosen decision interview; do not impose it on ordinary implementation choices |
| `handoff` | Reference/export recipe | Keep objective, decisions, identities, proof and next-action packet; use native continuation when sufficient and export when continuity requires it |
| `high-assurance-review` | Optional, trim | Preserve author-independent reviewers, fixed context, root adjudication and drift rejection; share the ordinary finding contract |
| `hillclimb` | Optional | Preserve comparable measurement, frozen acceptance, equivalent work and uncertainty; activate only for a bounded sustained optimization method |
| `implement` | Reference plus native direct work | Keep counterexample and handoff proof in shared references; keep necessary worker/delivery obligations with delivery; remove generic default execution wrapper |
| `parallel-implement` | Optional, trim | Preserve behavioral independence, custody, serial integration and complete cleanup; place command mechanics with their helpers |
| `prototype` | Optional | Preserve disposable scope and the distinction between a design answer and production proof; do not merge away this user-selected completion mode |
| `repo-bootstrap` | Optional, change | Prefer bounded repository setup and executable verification recipes; tracker/domain setup is a branch, not the price of entry to coding |
| `research` | Default, trim | Preserve evidence classes and citation entailment; reduce protocol labels and direct/caller duplication |
| `resolving-merge-conflicts` | Optional | Keep operation-specific stage semantics, generated-file and rename handling, state preservation and authorized continuation |
| `simplify-code` | Optional | Keep an explicit behavior-preserving cleanup mode; preserve real safeguards and measure complexity rather than lines |
| `skill-router` | Retire entrypoint in proposed pack | Use a short human catalog and precise descriptions; do not maintain a second procedural route graph |
| `tdd` | Optional | Keep meaningful observed RED and independent expectations; no universal test-first requirement or extra approval for ordinary test seams |
| `to-questionnaire` | Optional | Keep neutral stakeholder questions and downstream coverage; no implicit sending |
| `to-spec` | Merge into durable-planning specification branch | Preserve accepted meaning and independent draft completion; do not automatically slice tickets |
| `to-tickets` | Merge into durable-planning graph branch | Preserve cohesive outcomes, dependency edges, distinguishing acceptance and publication recovery |
| `triage` | Optional | Keep readiness and duplicate-cause judgment plus effect read-back; use the repository's tracker representation |
| `wayfinder` | Optional, trim | Keep decision dependencies and external waits; remove arbitrary one-transition limits where no invariant requires them |
| `wizard` | Optional | Keep secure human secret entry, exact targets and partial-effect recovery; retain narrow human-only scope |
| `writing-for-agents` | Optional, trim | Keep context entry, discoverable pointers and completion criteria; load for a requested instruction artifact, not every incidental worker assignment |

The two existing extras stay separate. `mle-workflow` contains important ML
knowledge about decision-time information, label maturity, split dependence,
preprocessing ownership and protected evaluation. `value-stock` contains
financial-method and evidence contracts. Neither belongs in a generic coding
default. Their references and implementation were not fully audited here.

## What to take from each upstream

### Matt Pocock

Keep caller-first design, runnable diagnosis, independent test expectations,
and the distinction between facts, experiments and user decisions. Its
retrospective adds useful questions about information access, tool expense and
navigation. Put those questions into context maintenance rather than adding
another always-available command.

Avoid requiring user-approved test seams for ordinary engineering, a perfect
fast repro before considering hypotheses, fixed hypothesis counts, prescribed
HTML designs, forced vocabulary, or automatic removal of lower-level tests.
These are specific upstream choices, not prerequisites for high-quality code.

Sources:
[design](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/codebase-design/SKILL.md),
[diagnosis](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/diagnosing-bugs/SKILL.md),
[TDD](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/tdd/SKILL.md),
[retrospective](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/retro/SKILL.md).

### Pstack

Keep impact analysis beyond symbol references, evidence for historical rationale,
existing-schema reuse, and turning repeated mechanical work into a checked
script when it is cheaper and safer than repeated agent edits. Its complementary
migration guidance is useful when conditioned on actual consumer compatibility.

The best addition is executable project-verification setup. Run the actual
launch, readiness, interaction, observation and cleanup path before presenting
it as demonstrated. Separate a stale recipe from a harness problem and a product
regression. This gives future agents information the model cannot know in advance.

Do not copy generation and maintenance wholesale. Creation seeds several
feature descriptions but exercises one. Record exactly which recipe was run
and with what environment and evidence. Other recipes remain source-derived
candidates. An old successful run does not establish current validity after
dependencies or commands change. Repair affected recipes by default; a full-map
verification audit needs that explicit scope. No new provenance registry is
needed merely to hold an evidence pointer.

Reject compulsory principle recitation, model rosters, architecture fanout for
any function-boundary edit, all-PR ten-lane verification and automatic external
communication. Its plan validator verifies shape and strings, not the truth of
the evidence. Unchanged patch IDs also do not establish unchanged surrounding
behavior after a base change.

Sources:
[impact analysis](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/blast-radius/SKILL.md),
[verification creation](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/create-verification-skill/SKILL.md),
[verification maintenance](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/maintain-verification-skill/SKILL.md),
[workflow controller](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/poteto-mode/SKILL.md),
[shipping](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/poteto-mode/playbooks/shipping.md).

### Superpowers

Keep native-first isolation, detecting an existing worktree before making
another, fresh bounded worker context, source-bound review packages, resuming
the implementer for fixes, scoped re-review and independent test expectations.
These are useful despite the larger default workflow around them.

Keep its recent movement toward proportionate brainstorming, plan-scoped scratch
state and safer cleanup. Remove universal approval loops, mandatory per-task
reviews, detailed code transcription into plans, fixed review-round limits and
test reruns required solely because evidence is from an earlier message.
Coordinator initiative must still respect unresolved user-owned decisions.

Superpowers reports that one prose deletion degraded behavior in its tests.
That is a warning against deleting by appearance, not a reproduced result for
Astra or this pack. Preserve a failure-shaped check for an important rule before
replacing its owner.

Sources:
[worktrees](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/using-git-worktrees/SKILL.md),
[delegated development](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md),
[verification](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/verification-before-completion/SKILL.md),
[test quality](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/writing-good-tests.md),
[release notes](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/RELEASE-NOTES.md).

### Ponytail

Keep its ladder after understanding the problem: do not build an unnecessary
feature, reuse code, use the standard library or native platform, then add the
minimum complete solution. Preserve its explicit protection of requested
behavior and consequential safeguards.

Reject smallest-diff or LOC scoring as the governing quality objective. Reject
a universal single-check ceiling and blanket restrictions on introducing a
framework. A small patch can be wrong; some changes require several different
checks; a justified existing framework can reduce total maintenance.

The core skill has not changed since the older recorded research pin. Recent
updates mostly concern platform compatibility and packaging. Its benchmark
disclosures distinguish structural checks from stronger evidence and constrain
transfer across workloads. They establish no Astra benefit here.

Sources:
[core method](https://github.com/DietrichGebert/ponytail/blob/974d940a1c5344210874150b98ff0d2c861fab6a/skills/ponytail/SKILL.md),
[review](https://github.com/DietrichGebert/ponytail/blob/974d940a1c5344210874150b98ff0d2c861fab6a/skills/ponytail-review/SKILL.md),
[benchmark scope](https://github.com/DietrichGebert/ponytail/blob/974d940a1c5344210874150b98ff0d2c861fab6a/benchmarks/README.md).

## Orchestration worth retaining

The user's delegation gate remains intact: use subagents when requested or
required by an applicable skill or repository instruction. Once authorized,
delegate a bounded independent result only when useful local work can proceed
alongside it. Do not optimize for the number of agents.

1. Fix the outcome, accepted behavior, proof and stopping boundary. Establish
   actual behavioral and resource independence before concurrent writes.
2. Give each worker one owned outcome, exact checkout/base, allowed effects,
   source pointers, neighboring owners, completion evidence and stopping condition.
3. Use existing native isolation when it establishes the required base, exclusive
   writable resources and recoverable identity. Supply helper enforcement for
   missing properties. A separate worktree alone is not sufficient.
4. Use completion, failure and attention events. A timeout prompts inspection.
   Resume the same worker for an actionable gap. Replace it only after its writes
   and command sessions have stopped; a cancellation request is not proof.
5. Integrate one accepted change at a time. Inspect the actual result. Recheck
   evidence affected by code, inputs, callers, dependencies, configuration or
   runtime changes. Checkout normalization can invalidate byte-identity proof.
6. Prove the integrated caller-visible result and reconcile all resources created
   by the run. Preserve unfinished work and give the next safe action if blocked.

| Owner | State or judgment |
| --- | --- |
| Native runtime | Actor identities, current status, messages, waits and cancellation observations |
| Operation records and helpers | Exact paths/base/HEAD, retained lane inventory, relevant runtime resources, ancestry, partial effects, receipts and cleanup read-back |
| Root | Independence, accepted meaning, authorization, evidence sufficiency, integration and unresolved choices |

Do not create a second general task tracker. Do retain durable operation records
when interruption, partial effects or cleanup require facts native state does
not preserve. For runs creating writable lanes, every created lane must remain
accounted for through verified cleanup. A bounded read-only assessor need not
produce a lane ledger. The local helper explicitly cannot prove actor quiescence;
its successful inspection is also distinct from action eligibility.
[Lane contract](../../skills/custom/parallel-implement/references/AGENT-LANES.md)

High-assurance review remains an optional promise with real obligations. Keep
the fixed candidate and relevant context, fresh author-independent reviewers,
independent initial findings, root adjudication, coverage limits and final drift
check. Do not replace that with two agents agreeing about a moving branch.
Ordinary review does not need the same machinery.
[High-assurance review](../../skills/custom/high-assurance-review/SKILL.md)

## Where future context belongs

| Material | Destination | Maintenance rule |
| --- | --- | --- |
| User preferences and authority | Small user guidance | Preserve explicit preferences; do not infer new permissions from a skill |
| Project meaning and accepted commitments | Domain records and focused decisions | Capture only non-obvious distinctions; reconcile conflicting current owners |
| Commands, topology and dependencies | Current configuration, scripts and targeted pointers | Avoid copying easy lookups; record non-obvious launch/readiness knowledge when discovery is costly |
| Verification recipes | Repository-owned instructions or scripts | Separate intended procedure from version-bound execution evidence; update affected recipes after drift |
| Professional methods | Selected skills and conditional examples | One owner, clear trigger, realistic failure and completion condition |
| Active task and decision state | Native task state or the actual tracker | Record owner, decision, dependency and return condition; do not duplicate every event |
| Recovery-critical state | Operation-owned durable records | Preserve the identities and receipts needed to resume or clean up safely |
| Repeated mechanical invariants | Types, schemas, lint, tests or checked helpers | Prefer enforcement to repeated prose where the condition is machine-checkable |
| Research, incidents and prior evaluations | Searchable history | Evidence for later judgment, not automatically active instructions |

The existing installer, lane helper and validators should not be discarded just
because native tools exist. Preserve the guarantees they provide until a
replacement demonstrates equivalent behavior. Conversely, composition-epoch
registries, authoring runbooks and historical campaign vocabulary should not
become context for ordinary coding in a target repository. A syntax or identity
validator can establish a mechanical contract; it cannot prove agent judgment.

## Debate and final adjudication

The fresh debate agents were `debate_minimalism`, `debate_reliability`, and
`debate_usability`. All returned qualified support after seeing peer objections
and the revised proposal. Their agreement is advisory, not behavioral proof.

| Disputed point | Challenge | Root decision |
| --- | --- | --- |
| Six defaults | Minimalism and usability questioned default domain and instruction-authoring procedures | Reduce to four candidate defaults; use project profiles for the other two. This repository naturally uses the authoring profile. |
| Fewer names as success | Minimalism noted that design/research/review also overlap model capabilities | Keep the short-contract-only alternative in evaluation; no claim that four is necessary or optimal. |
| Hidden proof examples | Reliability warned direct implementation might never load relocated guidance | Keep precise visible triggers with a consequence threshold; detailed examples remain conditional. |
| Native task state | Reliability identified loss of lane receipts and process state after interruption | Native scheduling/status, operation-owned recovery records, and actual quiescence checks. No universal extra ledger for read-only work. |
| Planning merger | Minimalism and usability distinguished parent intent from implementation slicing | Select specification, graph or both before loading procedures; preserve separate completion and publication authority. |
| Verification setup | Usability found only one seeded recipe is exercised upstream | Candidate versus demonstrated scope must be explicit and evidence version-bound; bounded maintenance rather than automatic whole-product auditing. |
| Missing optional guidance | Usability warned the thin pack could reproduce setup stalls | Investigate with available evidence; stop dependent work only for a consequential unresolved requirement, not a missing preferred file. |
| Deletion safety | Reliability rejected moving a rule by topic alone | Identify the trigger, required behavior and destination owner for every removed safeguard; verify important failure cases before migration. |

The root also declined two aggressive simplifications from the initial pass:
merging research and diagnosis into one general investigate skill, and removing
the distinct prototype/simplify commands. Their different accepted outcomes are
useful user choices. They can be optional without being collapsed.

Unresolved disagreement is empirical: whether four defaults, the current pack,
or only the short contract produces the best results on actual work. No agent
claimed this debate resolves it. The final recommendation is to compare the
candidate before authorizing broad removal.

## Proposed adoption checks, not performed

Compare the current pack, the proposed default/profile arrangement, and the
short contract with the same repository facts and ordinary runtime instructions.
If a no-pack baseline is added, preserve user authority and project invariants.
Hold model, reasoning setting, tools, inputs and acceptance constant. Keep
candidate wording and earlier answers out of control contexts. Model changes
and pack changes must not be attributed to each other.

| Representative task | What must be observed |
| --- | --- |
| Routine bounded fix | Correct completion without an unnecessary interview, plan, reviewer or broad repeated suite |
| Producer/consumer change | Real output survives the changed boundary; a plausible wrong rule fails the check |
| Intermittent defect | Observations discriminate causes rather than merely confirming a favored explanation |
| Resumable importer | Interrupted writes, retries and competing stop conditions preserve accepted behavior |
| Parallel work with shared external resource | Independence is assessed beyond file paths; unsafe overlap is prevented |
| Interrupted lane cleanup | Every created lane and owned process/resource is reconciled against the correct integration state |
| Domain ambiguity | Observed behavior is distinguished from intended meaning; only the necessary user decision is requested |
| Fresh or stale verification recipe | The actual requested path is exercised; generated but untested recipes are not presented as proven |
| Spec or ticket draft | The requested artifact is complete without unrequested publication, slicing or implementation |
| Change review | Concrete defects are found with low false-positive burden; stale evidence and candidate drift are recognized |

Score completion correctness, material omissions, retrieval/invocation errors,
unnecessary questions, unnecessary work, maintainability of the result and total
effort. Token count and skill count explain cost; neither is the quality target.
Use fresh paired samples and add repetitions where variance can change the
decision. A single successful run cannot establish broad reliability.

Before any later migration, give every retained obligation a destination and
working trigger, preserve important negative cases, and keep a recoverable
baseline. Migrate one bounded method at a time. No rollout, installation,
deletion or accepted composition change is authorized by this note.
