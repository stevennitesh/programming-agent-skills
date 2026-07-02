# Prompt 09: Detailed Skill-Context Draft For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/09-detailed-skill-context-draft.md`](../../../methods/prompts/09-detailed-skill-context-draft.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Candidate runtime draft:
[`08-candidate-runtime-draft.md`](08-candidate-runtime-draft.md)

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

Revision feedback: none.

Subagent inputs used:

- Scenario/traceability pass: assemble `R1` through `H3` from Prompt 08, keep
  `O3` out of runtime, and add a positive no-issue-provided tracker path
  scenario for Prompt 10 to preserve and Prompt 11 to validate because
  existing `implement` already owns that behavior.
- Owner-placement pass: replace only `### 1. Select The Issue`; keep
  `to-issues`, `triage`, tracker docs, Context Intake, proof, review, and
  commit ownership intact.
- Skill-prose/prune pass: keep `R5`, `L6`, and `H3` validation-visible; avoid
  weak phrases like "pick a ready issue", "choose the best issue", and "ask if
  unsure".

## 1. Draft Scope

This draft assembles Facet 1, `Ready Issue Selection`, into a skill-shaped
detailed skill-context draft for the existing `implement` skill.

Inputs used:

- candidate runtime draft: `08-candidate-runtime-draft.md`;
- existing skill base: `skills/current/implement/SKILL.md`.

Prompt 08 decision used:

- `ready-for-plain-language-candidate`.

This draft must preserve:

- `implement` picks up one ready-for-agent issue and stops after one issue;
- explicit issue, path, or URL targets still work when they are one
  issue-equivalent item;
- a PRD/spec can be used to find or choose one ready issue, but not to
  implement the whole source document;
- if no issue is provided, the agent uses repo tracker docs and ready labels;
- dependency order, ambiguous-order ask, and no-ready stop still exist;
- Context Intake, baseline capture, bounded implementation, proof, review,
  commit, and implementation note remain later steps;
- issue-state changes remain forbidden unless requested or repo-defined.

This draft will not decide final controlled wording, edit `SKILL.md`, validate
against real tasks, add support docs, final-prune the skill, or introduce new
runtime behavior beyond Prompt 08 candidate lines and existing behavior
preservation. Prompt 10 owns the plain-language candidate that Prompt 11
will validate.

## 2. Revision Feedback Disposition

No revision feedback to disposition.

## 3. Candidate Input

| Line ID | Prompt 08 Runtime Weight / Placement | Candidate Line Or Decision | Step 9 Treatment |
| --- | --- | --- | --- |
| R1 | runtime core | Before Context Intake, select exactly one issue-equivalent item. | Assemble into the opening gate for `### 1. Select The Issue`. |
| R2 | runtime core | Broad source surfaces are not implementation scope until one ready issue-equivalent item is named. | Assemble into the opening gate with source-scope rejection. |
| R3 | runtime core | PRD/spec/source/path without one ready item asks for the target item or routes to `to-issues`. | Assemble route-only; preserve existing PRD/spec can identify one ready issue. |
| R4 | runtime core | No one issue-equivalent item, no implementation. | Assemble as the blunt selection consequence. |
| R5 | validation-useful detail | Keep concrete examples of issue, URL, tracker item, path-backed ready slice, and explicit user-selected work item. | Assemble as the definition of issue-equivalent item for validation. |
| A1 | runtime core | Use an explicit user target or repo-visible ready/order source; do not invent priority or readiness. | Assemble in selection authority paragraph. |
| A2 | runtime core | Multiple unordered eligible items require user choice or repo order. | Assemble in selection authority paragraph. |
| A3 | runtime core | No ready item on the checked surface stops and reports that surface. | Assemble in selection authority paragraph. |
| A4 | validation-useful pointer | Keep as short tracker-doc pointer and metadata-mutation guard. | Assemble as a short pointer only. |
| L1 | runtime core | Run local readiness recheck over prompt adequacy, done signal, blocker/dependency state, and result-defining ambiguity. | Assemble in readiness paragraph. |
| L2 | runtime core | Agent-prompt adequacy means the item can guide a fresh coding agent into Context Intake without issue repair. | Assemble as a compact definition. |
| L3 | runtime core | Observable done signal names behavior, repro, doc target, validation hint, or done condition without a proof plan yet. | Assemble as a compact definition. |
| L4 | runtime core | Blocked work waits unless selected item is the blocker or repo-visible order confirms work now. | Assemble in readiness paragraph. |
| L5 | runtime core | Ask only after naming the missing fact and how it changes the expected result. | Assemble in readiness paragraph. |
| L6 | validation-useful detail | No prompt adequacy, done signal, clear blocker state, or ambiguity result, no pickup. | Assemble as a validation-visible readiness consequence. |
| O1 | runtime core | Detect unready work; do not make it ready inside `implement`. | Assemble as compressed owner-boundary rule. |
| O2 | validation-useful detail | Multiple independent outcomes/items/surfaces ask for one ready item or hand off upstream; do not split here. | Assemble as prune-watch stop/handoff smell. |
| H1 | runtime core | Record selected item identity, checked surface, selection authority, readiness facts, and branch outcomes. | Assemble in final selection handoff. |
| H2 | runtime core | Select first, plan later; no file discovery, implementation planning, proof strategy, or edits until selection facts are recorded. | Assemble in final selection handoff. |
| H3 | validation-useful detail | Start Context Intake only after `H1` selection facts are recorded. | Assemble as validation-visible handoff gate. |
| L7 | move-to-support | Readiness facts recorded without Context Intake/proof/repair. | Not assembled; duplicates `H1`/`H2`. |
| O3 | owned-elsewhere | High-risk pickup boundaries belong to repo docs / engineering contract. | Not assembled; record as support pointer placeholder. |
| O4 | move-to-support | Stop/handoff for neighboring owners. | Not assembled; useful support checklist only. |
| O5 | cut | Owner-owned work not repaired inside selection. | Not assembled; duplicate meta line. |
| H4 | cut | Context Intake has one selected item plus recorded facts. | Not assembled; redundant wrapper. |
| S1 | not-runtime-line | Future examples for prompt adequacy and done-signal checks. | Not assembled; defer until validation shows need. |
| S2 | cut | Source-process rationale. | Not assembled; rationale bloat. |

## 4. Placement And Merge Map

| Line ID | Existing Location | Draft Action | Why This Placement Preserves Behavior |
| --- | --- | --- | --- |
| R1, R4, R5 | `### 1. Select The Issue` opening | replace/merge | Preserves one-issue pickup while defining issue-equivalent targets that keep current issue/path/URL behavior testable. |
| R2, R3 | `### 1. Select The Issue` opening and existing PRD/spec sentence | replace/merge | Prevents broad PRD/spec/path implementation while preserving use of a source document to find one ready item. |
| A1, A2, A3, A4 | Existing no-issue, ambiguous-order, no-ready lines | replace/merge | Keeps repo/user selection authority, dependency order, ambiguous ask, and no-ready stop. |
| L1, L2, L3, L4, L5, L6 | New readiness paragraph inside `### 1. Select The Issue` | insert | Adds local pickup readiness without entering full triage, Context Intake, or proof planning. |
| O1, O2 | New owner-boundary paragraph inside `### 1. Select The Issue` | insert | Blocks issue repair, tracker mutation, and splitting inside selection while preserving handoff to owning workflows. |
| H1, H2, H3 | End of `### 1. Select The Issue`, before `### 2. Capture Baseline` | insert | Makes selection facts the handoff into later phases without moving baseline, Context Intake, proof, review, or commit behavior. |
| O3 | None | support placeholder | Exact risk policy is owned by repo docs / engineering contract and should not become inline runtime policy now. |
| L7, O4, S1 | None | not assembled | Support material is deferred until validation shows a need. |
| O5, H4, S2 | None | not assembled | Cut as duplicate/meta/rationale lines. |

## 5. Preserved Existing Behavior

| Existing Behavior | Preserved By Draft Location / Line ID | Regression Risk |
| --- | --- | --- |
| Pick up one ready-for-agent issue. | `### 1. Select The Issue`; `R1`, `R4`, `R5` | "Issue-equivalent" could accidentally broaden to source docs unless `R2` remains visible. |
| Stop after one issue. | Opening gate and final handoff; `R1`, `R4`, `H1`, `H2`, `H3` | Draft could become a multi-item selection workflow if `O2` is weakened. |
| Explicit issue/path/URL targets still work. | Issue-equivalent definition; `R5` | Path/URL behavior could be overblocked by source-path rejection. |
| PRD/spec can find or choose one ready issue. | Source-document paragraph; `R2`, `R3` | Draft could reject useful PRD/spec references instead of using them to identify one item. |
| PRD/spec is not implemented wholesale. | Source-document paragraph; `R2`, `R3`, `O1` | Draft could let a source document become scope without a ready item. |
| No issue provided means use tracker docs and ready labels. | Selection authority paragraph; `A1`, `A3`, `A4` | Prompt 08 lacked a positive happy-path scenario; Prompt 09 adds one for Prompt 10 to preserve and Prompt 11 to validate. |
| Dependency order and blocker skip remain. | Readiness paragraph and tracker pointer; `L4`, `A4` | Draft could require tracker metadata edits instead of respecting visible state. |
| Ambiguous order asks user. | Selection authority paragraph; `A2` | Agent could invent priority from convenience. |
| No ready issue available stops. | Selection authority paragraph; `A3` | Agent could create, repair, or promote work in `implement`. |
| Context Intake remains later. | Final handoff; `H1`, `H2`, `H3` | Selection could collapse into file discovery or issue-context reading too early. |
| Bounded slice behavior remains later. | Owner-boundary paragraph; `O2` | Draft could turn into slicing instructions instead of ask/handoff. |
| Proof strategy remains later. | Readiness and handoff paragraphs; `L3`, `H2` | Done-signal check could become a proof-plan requirement. |
| Review, commit, and note remain later. | Existing later sections unchanged; `H2` | Selection could start review/commit planning too early if wording drifts. |
| Issue state changes only when requested or repo-defined. | Tracker pointer and owner boundary; `A4`, `O1` | Draft could duplicate tracker procedure or authorize relabeling. |

## 6. Detailed Skill-Context Draft

Replacement draft for `skills/current/implement/SKILL.md`,
`### 1. Select The Issue`:

```markdown
### 1. Select The Issue

Before Context Intake, select exactly one issue-equivalent item. An
issue-equivalent item is one concrete issue, URL, tracker item, path-backed
ready slice, or explicit user-selected work item. A queue, project, PRD, spec,
batch, list, or bare source path is not implementation scope until one ready
item is named. If the user provides a PRD, spec, source document, or path, use
it only to identify one ready item; if it does not name or lead to one, ask for
the target item or route to `to-issues`. No one issue-equivalent item, no
implementation.

Use an explicit user target or repo-visible ready/order source; do not invent
priority or readiness. If no item is provided, use repo tracker docs and ready
labels. If multiple eligible items remain unordered, ask for the user choice or
repo order. If no ready item exists on the checked surface, stop and report
that surface. Use tracker docs for ready labels, ordering, state, and
dependency syntax; do not edit tracker metadata here.

Run a local readiness recheck before pickup: agent-prompt adequacy, observable
done signal, blocker/dependency state, and result-defining ambiguity.
Agent-prompt adequacy means the item can guide a fresh coding agent into
Context Intake without issue repair. Observable done signal means the item
names an expected behavior, repro, doc target, validation hint, or done
condition; it does not require a proof plan yet. Blocked work waits unless the
selected item is the blocker or repo-visible order confirms this item should be
worked now. Ask only after naming the missing fact and how it would change the
expected result. If the item lacks prompt adequacy, a done signal, clear
blocker state, or a resolved result-defining ambiguity, do not pick it up.

Detect unready work; do not make it ready inside `implement`. If the candidate
contains multiple independent outcomes, items, or unrelated surfaces, ask for
one ready item or hand off upstream; do not split it here.

Record selected item identity, checked surface, selection authority, readiness
facts, and branch outcomes before file discovery, implementation planning,
proof strategy, or edits. Select first, plan later. Start Context Intake only
after those selection facts are recorded.
```

## 7. Traceability Map

| Draft Location / Heading | Line IDs | Prompt 09 Validation IDs | What Prompt 10 Must Preserve For Prompt 11 |
| --- | --- | --- | --- |
| Selection opening: exactly one issue-equivalent item | R1, R4, R5 | V1-single-item, V3-path-backed-slice | Broad multi-item inputs are rejected; one issue/URL/tracker item/path-backed ready slice is accepted when ready. |
| Source document/source path handling | R2, R3, R5 | V2-prd-source-handoff, V3-path-backed-slice | PRD/spec/bare source path without one ready item asks/routes; PRD/spec/path that identifies one ready item can proceed. |
| Selection authority and tracker pointer | A1, A2, A3, A4 | V4-authority, V5-no-ready, V7-blocker, V11-next-ready-from-tracker | Agent uses user target or repo-visible order, asks on unordered multiples, stops on no-ready, and can select the one next ready item from tracker docs. |
| Local readiness recheck | L1, L2, L3, L4, L5, L6 | V6-readiness, V7-blocker, V8-ambiguity | Ready label is not enough; prompt-poor, unverifiable, blocked, or result-ambiguous work is not picked up. |
| Owner-boundary stop/handoff | O1, O2 | V2-prd-source-handoff, V5-no-ready, V9-owner-boundary | `implement` does not repair, promote, split, relabel, rewrite, reprioritize, or mutate tracker state. |
| Selection-to-Context-Intake handoff | H1, H2, H3 | V10-selection-boundary, V11-next-ready-from-tracker | Selection facts are recorded before file discovery, implementation planning, proof strategy, edits, or Context Intake. |

Prompt 09-created validation IDs for Prompt 10 to preserve:

- `V11-next-ready-from-tracker`: no issue/path/URL is provided, tracker docs
  expose exactly one next unblocked `ready-for-agent` item in dependency
  order, and the agent selects it using repo-visible authority before Context
  Intake.
- `V12-prd-identifies-one-ready-item`: a PRD/spec/source document identifies
  exactly one ready issue-equivalent item, and the agent may select that item
  without implementing the whole source document.

These are not new runtime behaviors. They preserve existing `implement`
behavior that Prompt 08 did not explicitly scenario-test.

## 8. Support Pointer Placeholders

| Pointer Or Placeholder | Draft Location | Target If Validated | Why It Is Not Created Yet |
| --- | --- | --- | --- |
| Tracker docs pointer | Selection authority paragraph | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, repo-local tracker docs | Existing docs own exact labels, ordering, state, commands, and dependency syntax. |
| High-risk pickup pointer | Not assembled in runtime draft | `docs/agents/engineering-contract.md`, repo policy docs | Prompt 09 marked `O3` owned elsewhere; validation must prove a pointer is needed before adding it. |
| Prompt adequacy / done-signal examples | Not assembled in runtime draft | Future implement support/examples doc | Examples would add load before Prompt 11 proves the readiness checks are misread. |
| Neighbor-owner checklist | Not assembled in runtime draft | Future support doc if validation proves it useful | `O4` bundles too many owners for runtime and is useful only as support. |

## 9. Draft Decision

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
- `L7`, `O4`, `S1`: support material; defer until validation proves a
  support pointer is useful.
- `O5`, `H4`, `S2`: cut as duplicate, meta, or source-rationale bloat.

Validation scenarios Prompt 10 must preserve and Prompt 11 should run first:

1. `V1` / `V2` / `V3`: compare broad source-surface rejection with valid
   issue/URL/path-backed ready target acceptance.
2. `V11`: no issue provided and exactly one next unblocked ready tracker item
   exists.
3. `V12`: PRD/spec identifies exactly one ready issue-equivalent item without
   becoming implementation scope.
4. `V6`: ready-labeled but prompt-poor or no-done-signal item is not picked
   up.
5. `V9`: repair/splitting/relabeling/promoting remains outside `implement`.
6. `V10`: selection facts are recorded before file discovery, proof strategy,
   edits, or Context Intake.

Placement conflicts or residual risks:

- `R5` may be pruned later, but it should stay validation-visible to protect
  issue/path/URL behavior.
- `A4` may duplicate preconditions, but Prompt 10 should preserve the tracker
  pointer unless it can keep the same behavior with less wording.
- `L6` is dense but gives Prompt 10 a clear no-pickup consequence to preserve
  for validation.
- `O1` may be shortened during final prune if "do not make it ready" proves
  strong enough.
- `O2` must remain ask/handoff only and must not become a slicing workflow.
- `H3` may merge with `H1`/`H2` during final prune if the handoff remains
  observable.
