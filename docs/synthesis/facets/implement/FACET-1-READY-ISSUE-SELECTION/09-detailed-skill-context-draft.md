# Prompt 09: Detailed Skill-Context Draft For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/09-detailed-skill-context-draft.md`](../../../methods/prompts/09-detailed-skill-context-draft.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet or scope: `1 - Ready Issue Selection`

Candidate runtime draft:
[`08-candidate-runtime-draft.md`](08-candidate-runtime-draft.md)

Candidate-draft decision: `ready-for-detailed-skill-context-draft`

Existing skill text: `skills/current/implement/SKILL.md`, especially the
existing description, intro, `### 1. Select The Issue`, later Context Intake,
bounded slice, proof, review, commit, implementation note, and issue-state
guard.

Relevant owners to preserve:

- Engineering contract: `docs/agents/engineering-contract.md`
- Tracker docs: `docs/agents/issue-tracker.md`
- Triage labels: `docs/agents/triage-labels.md`
- Related skills: `skills/current/triage/SKILL.md`,
  `skills/current/to-issues/SKILL.md`, `skills/current/implement/SKILL.md`
- Support docs: none created

Revision feedback:

- Rerun Prompt 09 from the refreshed Prompt 08 candidate runtime draft.
- Use current 10-section Prompt 09 schema.
- Add the missing Owner Boundary Check.
- Preserve exact Prompt 08 runtime weights and core classes.
- Restore `A4` as runtime behavior, not merely a tracker pointer.
- Preserve explicit issue/path/URL behavior, next-unblocked tracker selection,
  `H1` tracker eligibility, and all validation IDs.
- Use three subagents to check schema, placement, and owner/scenario risks.

Subagent inputs used:

- Schema pass: fix candidate-draft decision input, add Owner Boundary Check,
  use exact Prompt 08 weights/classes, and end at `## 10. Draft Decision`.
- Placement pass: replace only `### 1. Select The Issue`; preserve explicit
  path/URL targets, no-input next-unblocked behavior, `A4`, `L6`, and `H1`.
- Owner/scenario pass: keep `O3` out of runtime, keep `O2` ask/handoff only,
  preserve support placeholders, and carry all validation IDs into the final
  handoff.

Do not edit `SKILL.md` in this prompt.

## 1. Draft Scope

This draft assembles Facet 1, `Ready Issue Selection`, into a skill-shaped
detailed skill-context draft for the existing `implement` skill.

Candidate runtime draft used:

- [`08-candidate-runtime-draft.md`](08-candidate-runtime-draft.md)

Existing `SKILL.md` text used as the base:

- `skills/current/implement/SKILL.md`, especially `### 1. Select The Issue`.

Prompt 08 candidate-draft decision used:

- `ready-for-detailed-skill-context-draft`

This draft must preserve:

- `implement` picks up one ready-for-agent issue and stops after one issue;
- explicit issue, path, or URL targets still work when they are one
  issue-equivalent item;
- a PRD/spec can be used to identify one ready issue, but not to implement the
  whole source document;
- if no issue is provided, the agent uses repo tracker docs and ready labels to
  select the next unblocked ready item in repo-visible order;
- tracker-state eligibility and explicit-target no-substitution remain runtime
  behavior;
- dependency order, ambiguous-order ask, and no-ready stop still exist;
- Context Intake, baseline capture, bounded implementation, proof, review,
  commit, and implementation note remain later steps;
- issue-state changes remain forbidden unless requested or repo-defined.

This draft will not decide final controlled wording, edit `SKILL.md`, validate
against real tasks, add support docs, final-prune the skill, or introduce new
runtime behavior beyond Prompt 08 candidate lines and existing behavior
preservation. Prompt 10 owns the plain-language candidate that Prompt 11 will
validate.

## 2. Revision Feedback Disposition

| Feedback Item | Affected Line IDs Or Sections | Step 9 Action | Remaining Risk |
| --- | --- | --- | --- |
| Current Prompt 09 schema requires 10 sections and an Owner Boundary Check. | Whole artifact, Section 3 | Rebuilt artifact around current schema and added the owner table. | Prompt 10 should consume current section names only. |
| Prompt 08 decision was stale in existing Prompt 09. | Prompt Inputs, Section 1 | Replaced with `ready-for-detailed-skill-context-draft`. | None if final decision remains separate. |
| Candidate Input table used loose labels. | Section 4 | Added exact Prompt 08 runtime weights and core classes. | Future reruns should keep weights/classes exact. |
| `A4` was weakened into a tracker pointer. | `A4`, Sections 4-10 | Assembled tracker-state eligibility and explicit-target no-substitution as runtime behavior. | Prompt 10 may compress too far unless V4 preserves the ineligible-target case. |
| Existing draft weakened no-input next-unblocked behavior. | `A1`, `A3`, `A4`, V11 | Detailed draft says no-input selection uses repo-visible ready/order/dependency policy. | Prompt 10 should avoid reducing this to generic ready-label lookup. |
| Existing draft risked overblocking explicit paths/URLs. | `R2`, `R3`, `R5`, V3 | Detailed draft distinguishes explicit path/URL or path-backed ready slice from bare source path. | Prompt 10 must keep both acceptance and rejection paths. |
| `L6` ambiguity wording was awkward. | `L6`, V8 | Rephrased as unresolved result-defining ambiguity. | Prompt 10 should not overblock ordinary implementation unknowns. |
| `H1` dropped tracker eligibility. | `H1`, V10 | Restored tracker eligibility when relevant in the selection record. | Prompt 10 should keep this or merge it visibly into readiness facts. |
| Final validation list omitted trace-map IDs. | Sections 8 and 10 | Final handoff lists all V1-V12 IDs. | Prompt 10 should preserve all IDs for Prompt 11. |

## 3. Owner Boundary Check

| Owner | Owned Behavior | Prompt 09 May Use | Prompt 09 Must Not Inline | Draft Action |
| --- | --- | --- | --- | --- |
| Existing `implement` selection section | One issue, no-input next unblocked issue, ambiguous-order ask, no-ready stop, blocker skip. | Replace `### 1. Select The Issue` with a detailed selection draft. | Change invocation scope or later implementation process. | Replace selection section only. |
| Existing `implement` later steps | Baseline, Context Intake, bounded implementation, proof, review, commit, note. | Mention that selection facts precede later phases. | File discovery, planning, proof strategy, review, commit, or issue-note procedure. | Keep later sections unchanged. |
| Engineering contract | Commitment boundaries, high-risk/security/privacy posture, proof and convergence discipline. | Keep high-risk policy as a support placeholder. | Inline universal risk thresholds or proof policy. | `O3` not assembled into runtime. |
| Tracker docs | GitHub operations, ready labels, ordering, state, dependency syntax. | Point to tracker docs for exact mechanics. | Inline `gh` commands, label tables, or tracker mutation procedure. | `A4` includes behavior plus pointer, not commands. |
| Triage labels | Local role-to-label mapping and ready/ineligible state roles. | Use eligible tracker-state concept. | Reproduce or edit state-label tables. | Keep exact label semantics in docs. |
| `triage` | Make issues ready, repair briefs, request info, classify labels/state. | Detect unready work and route/stop. | Repair, relabel, promote, or rewrite issue briefs. | `O1` blocks repair inside `implement`. |
| `to-issues` | Decompose PRDs/specs/plans into ready issue slices. | Route source docs that lack one ready item. | Decompose or author issues inside `implement`. | `R3` is route-only. |
| Later bounded-slice control | Detailed scope/slice management after selection. | Detect obvious many-item scope before pickup. | Split or plan the work in this facet. | `O2` stays ask/handoff only. |
| Semantic Proof / `$tdd` | Proof strategy and red-green-refactor after selection. | Require a done signal before pickup. | Demand a proof plan or test design during selection. | `L3` says no proof plan yet. |
| User / product owner | Product priority, explicit target choice, result-defining missing facts. | Ask on unordered candidates, ambiguity, blocker order, or ineligible named target. | Invent priority or silently substitute another item. | `A1`, `A2`, `A4`, and `L5` preserve authority. |

## 4. Candidate Input

| Line ID | Prompt 08 Runtime Weight | Prompt 08 Core Class | Prompt 08 Placement | Candidate Line Or Decision | Step 9 Treatment |
| --- | --- | --- | --- | --- | --- |
| R1 | must-runtime | Runtime Core | replace/merge with selection opening | Before Context Intake, select exactly one issue-equivalent item. | Assemble into opening gate. |
| R2 | must-runtime | Runtime Core | insert near selection opening | Broad source surfaces are not implementation scope until one ready issue-equivalent item is named. | Assemble with explicit path/URL caveat. |
| R3 | must-runtime | Runtime Core | merge with existing PRD/spec sentence | PRD/spec/source/path without one ready item asks for target item or routes to `to-issues`. | Assemble route-only; no decomposition. |
| R4 | must-runtime | Runtime Core | insert | No one issue-equivalent item, no implementation. | Assemble as blunt consequence. |
| R5 | candidate-runtime | Validation Detail | insert or merge with R1/R4 | Done when one concrete issue, URL, tracker item, path-backed ready slice, or explicit user-selected work item is named. | Assemble as issue-equivalent definition. |
| A1 | must-runtime | Runtime Core | replace broad choose-next wording | Use explicit user target or repo-visible ready/order policy; do not invent priority or readiness. | Assemble in authority paragraph. |
| A2 | must-runtime | Runtime Core | keep/strengthen ambiguous-order line | Multiple unordered eligible items ask user/order source. | Assemble as ask rule. |
| A3 | must-runtime | Runtime Core | keep/strengthen no-ready line | No ready item stops and reports checked surface. | Assemble as stop rule. |
| A4 | must-runtime | Runtime Core | replace tracker-doc pointer and strengthen preconditions | Tracker items need eligible state; explicit ineligible targets stop without substitution or metadata edits. | Assemble as runtime gate plus tracker-doc pointer. |
| L1 | must-runtime | Runtime Core | insert after authority | Run local readiness recheck with four named facts. | Assemble in readiness paragraph. |
| L2 | must-runtime | Validation Detail | insert under readiness | Agent-prompt adequacy guides a fresh coding agent into Context Intake. | Assemble as compact definition. |
| L3 | must-runtime | Validation Detail | insert under readiness | Observable done signal exists without proof plan. | Assemble as compact definition. |
| L4 | must-runtime | Runtime Core | replace/strengthen blockers line | Blocked work waits unless selected item is blocker/order confirmed. | Assemble as blocker gate. |
| L5 | must-runtime | Runtime Core | merge with ask/commitment boundary | Ask only after naming missing fact and result effect. | Assemble as ambiguity ask rule. |
| L6 | must-runtime | Validation Detail | insert or merge with L1-L5 | No readiness facts, no pickup. | Assemble as validation-visible consequence. |
| L7 | support-only | Support | defer to support | Readiness facts recorded without Context Intake/proof/repair. | Not assembled; duplicates H1/H2. |
| O1 | must-runtime | Runtime Core | insert near selection/readiness | Detect unready work; do not make it ready inside `implement`. | Assemble as owner-boundary rule. |
| O2 | candidate-runtime | Validation Detail | insert if kept | Multiple independent outcomes/items/surfaces ask or hand off; do not split here. | Assemble as ask/handoff smell. |
| O3 | support-only | Support | defer to support | High-risk pickup boundaries belong to repo docs / engineering contract. | Not assembled; support placeholder only. |
| O4 | support-only | Support | defer to support / owner scan | Neighbor owner handoff checklist. | Not assembled; covered by owner table. |
| O5 | likely-prune | Cut | cut | Owner-owned work not repaired inside selection. | Not assembled; duplicate meta line. |
| H1 | must-runtime | Runtime Core | insert before Context Intake handoff | Record selected item identity, checked surface, authority, eligibility/readiness facts, and branch outcomes. | Assemble with tracker eligibility when relevant and "selection outcomes" wording. |
| H2 | must-runtime | Runtime Core | insert | Select first, plan later. | Assemble as phase boundary. |
| H3 | candidate-runtime | Validation Detail | insert/merge | Start Context Intake only after H1 selection facts are recorded. | Assemble as validation-visible handoff gate. |
| H4 | likely-prune | Cut | cut | Context Intake has one selected item and recorded facts. | Not assembled; redundant wrapper. |
| S1 | support-only | Support | support placeholder | Future prompt-adequacy and done-signal examples. | Not assembled; support placeholder. |
| S2 | likely-prune | Cut | cut | Source-process rationale. | Not assembled; rationale bloat. |

## 5. Placement And Merge Map

| Line ID | Existing Location | Draft Action | Why This Placement Preserves Behavior |
| --- | --- | --- | --- |
| R1, R4, R5 | `### 1. Select The Issue` opening | replace | Preserves one-issue pickup while defining issue-equivalent targets that keep current issue/path/URL behavior testable. |
| R2, R3 | Existing source-target sentence in selection prose | merge | Prevents broad PRD/spec/path implementation while preserving use of a source document to identify one ready item. |
| A1, A2, A3, A4 | Existing no-issue, ambiguous-order, no-ready lines | replace | Keeps user/repo selection authority, next-unblocked tracker selection, dependency order, ambiguous ask, no-ready stop, tracker eligibility, and no substitution. |
| L1, L2, L3, L4, L5, L6 | New readiness paragraph inside `### 1. Select The Issue` | insert | Adds local pickup readiness without entering full triage, Context Intake, or proof planning. |
| O1, O2 | New owner-boundary paragraph inside `### 1. Select The Issue` | insert | Blocks issue repair, tracker mutation, and splitting inside selection while preserving handoff to owning workflows. |
| H1, H2, H3 | End of `### 1. Select The Issue`, before `### 2. Capture Baseline` | insert | Makes selection facts the handoff into later phases without moving baseline, Context Intake, proof, review, or commit behavior. |
| O3 | None | support placeholder | Exact risk policy is owned by repo docs / engineering contract and should not become inline runtime policy now. |
| L7, O4, S1 | None | not assembled | Support material is deferred until validation shows a need. |
| O5, H4, S2 | None | not assembled | Cut as duplicate, meta, or rationale lines. |

## 6. Preserved Existing Behavior

| Existing Behavior | Preserved By Draft Location / Line ID | Regression Risk |
| --- | --- | --- |
| Pick up one ready-for-agent issue. | Selection opening; `R1`, `R4`, `R5` | "Issue-equivalent" could accidentally broaden to source docs unless `R2` remains visible. |
| Stop after one issue. | Opening gate and final handoff; `R1`, `R4`, `H1`, `H2`, `H3` | Draft could become a multi-item selection workflow if `O2` is weakened. |
| Explicit issue/path/URL targets still work. | Issue-equivalent definition and source caveat; `R2`, `R5` | Path/URL behavior could be overblocked by bare-source-path rejection. |
| PRD/spec can find or choose one ready issue. | Source-document paragraph; `R2`, `R3` | Draft could reject useful PRD/spec references instead of using them to identify one item. |
| PRD/spec is not implemented wholesale. | Source-document paragraph; `R2`, `R3`, `O1` | Draft could let a source document become scope without a ready item. |
| No issue provided means use tracker docs and ready labels. | Selection authority paragraph; `A1`, `A3`, `A4`, V11 | Prompt 10 must keep "next unblocked ready item in repo-visible order." |
| Dependency order and blocker skip remain. | Authority/readiness paragraph and tracker pointer; `A4`, `L4` | Draft could require tracker metadata edits instead of respecting visible state. |
| Ambiguous order asks user. | Selection authority paragraph; `A2` | Agent could invent priority from convenience. |
| No ready issue available stops. | Selection authority paragraph; `A3` | Agent could create, repair, or promote work in `implement`. |
| Explicit named tracker item may still be ineligible. | Tracker eligibility gate; `A4` | Agent could silently substitute another issue or mutate tracker state. |
| Context Intake remains later. | Final handoff; `H1`, `H2`, `H3` | Selection could collapse into file discovery or issue-context reading too early. |
| Bounded slice behavior remains later. | Owner-boundary paragraph; `O2` | Draft could turn into slicing instructions instead of ask/handoff. |
| Proof strategy remains later. | Readiness and handoff paragraphs; `L3`, `H2` | Done-signal check could become a proof-plan requirement. |
| Review, commit, and note remain later. | Existing later sections unchanged; `H2` | Selection could start review/commit planning too early if wording drifts. |
| Issue state changes only when requested or repo-defined. | Tracker pointer and owner boundary; `A4`, `O1` | Draft could duplicate tracker procedure or authorize relabeling. |

## 7. Detailed Skill-Context Draft

Replacement draft for `skills/current/implement/SKILL.md`,
`### 1. Select The Issue`:

```markdown
### 1. Select The Issue

Before Context Intake, select exactly one issue-equivalent item. An
issue-equivalent item is one concrete issue, URL, tracker item, path-backed
ready slice, or explicit user-selected work item. A queue, project, PRD, spec,
batch, list, or bare source path is not implementation scope until one ready
item is named. If the user provides a PRD, spec, source document, or bare source
path, use it only to identify one ready item; if it does not name one, ask for
the target item or route to `to-issues`. Do not treat an explicit path/URL
target or path-backed ready slice as a broad source path when it is already one
issue-equivalent item. No one issue-equivalent item, no implementation.

Use an explicit user target or repo-visible ready/order source; do not invent
priority or readiness. If no item is provided, use repo tracker docs, ready
labels, and dependency/order policy to select the next unblocked ready item. If
multiple eligible items remain unordered, ask for the user choice or repo order.
If no ready item exists on the checked surface, stop and report that surface.
For tracker items, confirm tracker-state eligibility through repo tracker docs.
If an explicit tracker target is not eligible, stop on that target without
silent substitution or tracker metadata edits.

Run a local readiness recheck before pickup: agent-prompt adequacy, observable
done signal, blocker/dependency state, and result-defining ambiguity.
Agent-prompt adequacy means the item can guide a fresh coding agent into
Context Intake without issue repair. Observable done signal means the item
names an expected behavior, repro, doc target, validation hint, or done
condition; it does not require a proof plan yet. Blocked work waits unless the
selected item is the blocker or repo-visible order confirms this item should be
worked now. Ask only after naming the missing fact and how it would change the
expected result. If the item lacks prompt adequacy, lacks a done signal, lacks
clear blocker state, or has unresolved result-defining ambiguity, do not pick
it up.

Detect unready work; do not make it ready inside `implement`. If the candidate
contains multiple independent outcomes, items, or unrelated surfaces, ask for
one ready item or hand off upstream; do not split it here.

Record selected item identity, checked surface, selection authority, tracker
eligibility when relevant, readiness facts, and selection outcomes before file
discovery, implementation planning, proof strategy, or edits. Select first,
plan later. Start Context Intake only after those selection facts are recorded.
```

## 8. Traceability Map

| Draft Location / Heading | Line IDs | Validation IDs | What Prompt 10 Must Preserve For Prompt 11 |
| --- | --- | --- | --- |
| Selection opening: exactly one issue-equivalent item | R1, R4, R5 | V1-single-item, V3-path-backed-slice | Broad multi-item inputs are rejected; one issue/URL/tracker item/path-backed ready slice is accepted when ready. |
| Source document/source path handling | R2, R3, R5 | V2-prd-source-handoff, V3-path-backed-slice, V12-prd-identifies-one-ready-item | PRD/spec/bare source path without one ready item asks/routes; PRD/spec/path that identifies one ready item can proceed. |
| Selection authority and tracker eligibility | A1, A2, A3, A4 | V4-authority, V5-no-ready, V7-blocker, V11-next-ready-from-tracker | Agent uses user target or repo-visible order, asks on unordered multiples, stops on no-ready, selects the one next ready item, and stops on ineligible explicit tracker targets without substitution. |
| Local readiness recheck | L1, L2, L3, L4, L5, L6 | V6-readiness, V7-blocker, V8-ambiguity | Ready label is not enough; prompt-poor, unverifiable, blocked, or result-ambiguous work is not picked up. |
| Owner-boundary stop/handoff | O1, O2 | V2-prd-source-handoff, V5-no-ready, V9-owner-boundary | `implement` does not repair, promote, split, relabel, rewrite, reprioritize, or mutate tracker state. |
| Selection-to-Context-Intake handoff | H1, H2, H3 | V10-selection-boundary, V11-next-ready-from-tracker | Selection facts, including tracker eligibility when relevant, are recorded before file discovery, implementation planning, proof strategy, edits, or Context Intake. |

Prompt 09-created validation IDs for Prompt 10 to preserve:

- `V11-next-ready-from-tracker`: no issue/path/URL is provided, tracker docs
  expose exactly one next unblocked `ready-for-agent` item in dependency order,
  and the agent selects it using repo-visible authority before Context Intake.
- `V12-prd-identifies-one-ready-item`: a PRD/spec/source document identifies
  exactly one ready issue-equivalent item, and the agent may select that item
  without implementing the whole source document.

These are not new runtime behaviors. They preserve existing `implement`
behavior that Prompt 08 did not explicitly scenario-test.

## 9. Support Pointer Placeholders

| Pointer Or Placeholder | Draft Location | Target If Validated | Why It Is Not Created Yet |
| --- | --- | --- | --- |
| Tracker docs pointer | Selection authority paragraph | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, repo-local tracker docs | Existing docs own exact labels, ordering, state, commands, and dependency syntax. |
| High-risk pickup pointer | Not assembled in runtime draft | `docs/agents/engineering-contract.md`, repo policy docs | Prompt 09 marked `O3` owned elsewhere; validation must prove a pointer is needed before adding it. |
| Prompt adequacy / done-signal examples | Not assembled in runtime draft | Future implement support/examples doc | Examples would add load before Prompt 11 proves the readiness checks are misread. |
| Neighbor-owner checklist | Not assembled in runtime draft | Future support doc if validation proves it useful | `O4` bundles too many owners for runtime and is useful only as support. |

## 10. Draft Decision

Draft decision: `ready-for-plain-language-candidate`

Draft artifact path:

`docs/synthesis/facets/implement/FACET-1-READY-ISSUE-SELECTION/09-detailed-skill-context-draft.md`

Line IDs assembled:

- `R1`, `R2`, `R3`, `R4`, `R5`;
- `A1`, `A2`, `A3`, `A4`;
- `L1`, `L2`, `L3`, `L4`, `L5`, `L6`;
- `O1`, `O2`;
- `H1`, `H2`, `H3`.

Line IDs not assembled and why:

- `O3`: owned by engineering contract / repo docs; do not inline risk policy
  yet.
- `L7`, `O4`, `S1`: support material; defer until validation proves a support
  pointer is useful.
- `O5`, `H4`, `S2`: cut as duplicate, meta, or source-rationale bloat.

Owner boundaries preserved:

- `to-issues` owns PRD/spec decomposition and issue authoring.
- `triage` owns issue repair, ready-state promotion, and relabeling.
- tracker docs own exact labels, commands, state roles, ordering fields, and
  dependency syntax.
- engineering contract / repo docs own high-risk policy.
- later `implement` steps own Context Intake, bounded slicing, proof, review,
  commit, and issue notes.

Validation scenarios Prompt 10 must preserve for Prompt 11:

- `V1-single-item`
- `V2-prd-source-handoff`
- `V3-path-backed-slice`
- `V4-authority`, including explicit named tracker item is ineligible and
  stops without substitution or metadata edits
- `V5-no-ready`
- `V6-readiness`
- `V7-blocker`
- `V8-ambiguity`
- `V9-owner-boundary`
- `V10-selection-boundary`
- `V11-next-ready-from-tracker`
- `V12-prd-identifies-one-ready-item`

Placement conflicts or residual risks:

- `R5` may be pruned later, but it should stay validation-visible to protect
  issue/path/URL behavior.
- `A4` may duplicate preconditions, but Prompt 10 must preserve tracker-state
  eligibility and explicit-target no-substitution.
- `L6` is dense but gives Prompt 10 a clear no-pickup consequence to preserve
  for validation.
- `O1` may be shortened during final prune if "do not make it ready" proves
  strong enough.
- `O2` must remain ask/handoff only and must not become a slicing workflow.
- `H3` may merge with `H1`/`H2` during final prune if the handoff remains
  observable.
