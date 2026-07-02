# Prompt 09: Behavior Audit For Implement Facet 1

This reruns
[`docs/synthesis/methods/prompts/09-behavior-audit.md`](../../../methods/prompts/09-behavior-audit.md)
for `implement` after the narrow Prompt 08 repair restored `L6` to the
assembled compact draft block.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Compact draft:
[`08-compact-draft.md`](08-compact-draft.md)

Generous synthesis:
[`07-generous-synthesis.md`](07-generous-synthesis.md)

Existing skill text to preserve: `skills/current/implement/SKILL.md`,
especially the current description, one-issue stop, explicit issue/path/URL
pickup, PRD/spec-to-one-issue behavior, tracker-doc preconditions, Context
Intake, bounded slice, proof, review, commit, implementation note, and
issue-state guard.

Relevant owners checked:

- Engineering contract: `docs/agents/engineering-contract.md`
- Tracker docs: `docs/agents/issue-tracker.md`
- Triage labels: `docs/agents/triage-labels.md`
- Related skills: `skills/current/triage/SKILL.md`,
  `skills/current/to-issues/SKILL.md`, `skills/current/implement/SKILL.md`
- Support docs: none created

Revision feedback: prior Prompt 09 decision was `revise-before-draft` only
because the assembled compact draft block omitted `L6`. Prompt 08 restored
`L6` in the compact block while preserving stable line IDs.

Subagent inputs used:

- Gate-strength pass: found `L6` closed; recommended
  `ready-for-validation-draft`, with `R5`, `A4`, `L6`, `O2`, and `H3` on
  prune-watch.
- Ownership pass: found no ownership blocker; keep `A4` pointer-only, `O1`
  as prohibited behavior only, and `O2` as a selection smell rather than a
  slicing workflow.
- Validation-readiness pass: found no Prompt 08 blocker; Prompt 10 should
  preserve path/URL acceptance, source-document rejection, readiness failure,
  owner boundaries, and selection-before-context handoff.

## 1. Audit Scope

This audit covers Facet 1, `Ready Issue Selection`, for `implement`.

Compact draft used:

- revised `08-compact-draft.md`, including Prompt 08 line inventory, placement
  targets, runtime weights, minimal runtime core, context-pointer candidates,
  and candidate compact draft block.

Prompt 08 inventory and runtime weights used:

- runtime core: `R1`, `R2`, `R3`, `R4`, `A1`, `A2`, `A3`, `A4`, `L1`, `L2`,
  `L3`, `L4`, `L5`, `L6`, `O1`, `H1`, `H2`, `H3`;
- audit expansion / prune-watch: `R5`, `O2`;
- support / pointer / cut: `L7`, `O3`, `O4`, `O5`, `H4`, `S1`, `S2`.

Existing skill behavior that must not regress:

- `implement` still picks up one ready-for-agent issue and stops after one
  issue;
- explicit issue, path, or URL targets still work when they are one
  issue-equivalent item;
- a PRD/spec can still be used to find or choose one ready-for-agent issue,
  but not to implement a whole source document;
- no provided issue means the agent uses repo tracker docs and ready labels;
- dependency order, ambiguous-order ask, and no-ready stop still exist;
- baseline capture, Context Intake, bounded implementation, proof, review,
  commit, and implementation note remain later steps;
- issue-state changes remain forbidden unless requested or repo-defined.

Related owners checked:

- `triage` owns issue repair, ready-state promotion, label/state application,
  Codex-ready brief writing, and maintainer-approved tracker updates.
- `to-issues` owns PRD/spec/source decomposition, issue splitting, dependency
  ordering, approval, and publishing approved bounded slices.
- Tracker docs own exact labels, commands, state names, ordering fields, and
  dependency syntax.
- Context Intake owns full issue/context reading, acceptance criteria intake,
  approach choice, and codebase exploration after selection.
- Bounded Slice Control owns detailed scope pressure after selection.
- Semantic Proof owns proof design and correctness evidence.
- Review/Lock owns fixed-point review, commit, and implementation note.
- Engineering contract / repo docs own exact high-risk policy.

This audit will not decide final runtime wording, edit `SKILL.md`, validate
against real scenarios, add support docs, write examples, or final-prune the
skill.

## 2. Revision Feedback Closure

| Feedback Item | Affected Line IDs | Closed / Still Risky / Not Closed | Evidence In Draft | Next Action |
| --- | --- | --- | --- | --- |
| `R2` overblocked valid path targets | `R2`, `R5` | Closed, validation risk remains | `R2` blocks a "bare source path" rather than all paths; `R5` preserves issue, URL, tracker item, path-backed ready slice, and explicit user-selected work item. | Validate bare-source-path rejection and path-backed/URL acceptance. |
| `L5` was too hand-wavy | `L5` | Closed | `L5` requires naming the missing fact and how it would change the expected result. | Validate against generic "ask if unsure" and ordinary implementation unknowns. |
| `O2` used subjective "plainly many issues" | `O2` | Closed wording, still prune-watch | `O2` now names multiple independent outcomes, items, or unrelated surfaces. | Validate as a stop/handoff smell only; do not let it become slicing. |
| `H3` used soft "facts are stable" wording | `H3`, `H1`, `H2` | Closed, prune-watch | `H3` starts Context Intake only after `H1` selection facts are recorded. | Validate phase boundary, then likely merge with `H1`/`H2` during final prune. |
| Duplicate/meta lines should be demoted or cut | `A5`, `L7`, `O3`, `O4`, `O5`, `H4`, `S1`, `S2` | Closed | `A5`, `O5`, `H4`, and `S2` are cut; `L7`, `O3`, `O4`, and `S1` are support/pointer/audit-only. | Keep non-runtime in audit; do not reintroduce without validation evidence. |
| Readiness failure consequence must survive | `L1`, `L2`, `L3`, `L6` | Closed | `L6` appears in both the runtime-step inventory and the assembled candidate compact draft block. | Proceed to Prompt 10 with `L6` validation-visible and prune-watch. |

All revision feedback is closed. Remaining risks are validation/prune-watch
risks, not Prompt 08 blockers.

## 3. Candidate Line Inventory

| Line ID | Candidate Line | Section | Function | Prompt 08 Placement | Prompt 08 Runtime Weight |
| --- | --- | --- | --- | --- | --- |
| R1 | Before Context Intake, select exactly one issue-equivalent item. | Select One Item | step | replace/merge with `### 1. Select The Issue` opening | must-runtime |
| R2 | A queue, project, PRD, spec, batch, list, or bare source path is not implementation scope until one ready issue-equivalent item is named. | Select One Item | hard gate | insert near selection opening | must-runtime |
| R3 | If the user provides a PRD, spec, source document, or path without one ready item, ask for the target item or route to `to-issues`. | Select One Item | stop/ask rule | merge with existing PRD/spec sentence | must-runtime |
| R4 | No one issue-equivalent item, no implementation. | Select One Item | hard gate | insert | must-runtime |
| R5 | Done when exactly one issue, URL, tracker item, path-backed ready slice, or explicit user-selected work item is named. | Select One Item | completion criterion | insert / fold into selection gate | audit expansion |
| A1 | Use an explicit user target or repo-visible ready/order policy; do not invent priority or readiness. | Apply Selection Authority | hard gate | replace broad choose-next wording | must-runtime |
| A2 | If multiple eligible items remain unordered, ask for the user choice or repo order. | Apply Selection Authority | stop/ask rule | keep/strengthen ambiguous-order line | must-runtime |
| A3 | If no ready item exists on the checked surface, stop and report that surface. | Apply Selection Authority | stop/ask rule | keep/strengthen no-issue line | must-runtime |
| A4 | Use repo tracker docs for ready labels, ordering, state, and dependency syntax; do not edit tracker metadata here. | Apply Selection Authority | context pointer | merge with tracker-doc mention | candidate-runtime |
| L1 | Run a local readiness recheck: agent-prompt adequacy, observable done signal, blocker/dependency state, and result-defining ambiguity. | Run Local Readiness Recheck | recheck | insert after authority | must-runtime |
| L2 | Agent-prompt adequacy means the item can guide a fresh coding agent into Context Intake without issue repair. | Run Local Readiness Recheck | recheck | insert under readiness | must-runtime |
| L3 | Observable done signal means the item names an expected behavior, repro, doc target, validation hint, or done condition; it does not require a proof plan yet. | Run Local Readiness Recheck | recheck | insert under readiness | must-runtime |
| L4 | Blocked work waits unless the selected item is the blocker or repo-visible order confirms this item should be worked now. | Run Local Readiness Recheck | hard gate | replace/strengthen blocker line | must-runtime |
| L5 | Ask only after naming the missing fact and how it would change the expected result. | Run Local Readiness Recheck | stop/ask rule | merge with ask/commitment boundary | must-runtime |
| L6 | No prompt adequacy, done signal, clear blocker state, or ambiguity result, no pickup. | Run Local Readiness Recheck | hard gate | insert / merge with readiness recheck | must-runtime / prune-watch |
| L7 | Readiness facts recorded without Context Intake/proof/repair. | Run Local Readiness Recheck | completion criterion | defer to support | support-only |
| O1 | Detect unready work; do not make it ready inside `implement`: no repair, relabeling, splitting, promotion, reprioritization, rewriting, or tracker-state mutation. | Preserve Owner Boundaries | ownership guard | insert near selection/readiness | must-runtime |
| O2 | If the candidate contains multiple independent outcomes, items, or unrelated surfaces, ask for one coherent ready item or hand off upstream; do not split it here. | Preserve Owner Boundaries | stop/ask rule | insert if kept | candidate-runtime |
| O3 | Use repo docs or the engineering contract for high-risk pickup boundaries. | Context Pointer Candidates | context pointer | defer to support | support-only |
| O4 | Stop/handoff for neighboring owners. | Preserve Owner Boundaries | ownership guard | defer to support | support-only |
| O5 | Done when owner-owned work was not repaired inside selection. | Preserve Owner Boundaries | completion criterion | cut | likely-prune |
| H1 | Record selected item identity, checked surface, selection authority, readiness facts, and branch outcomes. | Record Selection Boundary | handoff | insert before Context Intake handoff | must-runtime |
| H2 | Select first, plan later: no file discovery, implementation planning, proof strategy, or edits until selection facts are recorded. | Record Selection Boundary | hard gate | insert | must-runtime |
| H3 | Start Context Intake only after the `H1` selection facts are recorded. | Record Selection Boundary | handoff | insert/merge | must-runtime |
| H4 | Done when Context Intake has one selected item plus recorded selection facts. | Record Selection Boundary | completion criterion | cut | likely-prune |
| S1 | See support examples for agent-prompt adequacy and done-signal checks. | Context Pointer Candidates | support/reference | future support/examples doc | support-only |
| S2 | Source rationale for pull/WIP and DoR contrast lives in support. | Context Pointer Candidates | support/reference | cut | cut |

## 4. Line-By-Line Behavior Audit

| Line ID | Behavior Changed? | Failure Prevented | Evidence Required | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| R1 | Yes | Starts from one selected item before Context Intake. | One named issue-equivalent item. | keep-for-validation | Core singular selection gate. |
| R2 | Yes | Broad source surface becomes implementation scope. | Input is not a queue/project/source surface, or one ready item is named. | keep-for-validation | Prior path regression is closed; validate bare path versus path-backed ready slice. |
| R3 | Yes | PRD/spec/source decomposition inside `implement`. | Source input lacks one ready item; target item or handoff named. | keep-for-validation | Safe because it is route-only and names no decomposition steps. |
| R4 | Yes | Batch or vague request starts implementation. | Absence/presence of one issue-equivalent item. | keep-for-validation | Strong blunt gate. |
| R5 | Yes | Existing path/URL target behavior regresses. | One concrete item type is named. | keep-but-prune-watch | Protects explicit issue/path/URL and path-backed ready slice behavior during validation. |
| A1 | Yes | Invented priority or readiness. | Explicit user target or repo-visible ready/order source. | keep-for-validation | Strong authority gate. |
| A2 | Preserves and sharpens existing behavior | Hidden priority decision among unordered candidates. | Multiple eligible items with no order. | keep-for-validation | Observable ask branch. |
| A3 | Preserves and sharpens existing behavior | Busywork when no ready item exists. | Checked surface and no-ready reason. | keep-for-validation | Strong stop if checked surface is reported. |
| A4 | Yes | Inline tracker semantics or metadata mutation. | Tracker docs consulted when syntax/order/dependencies matter. | keep-but-prune-watch | Useful pointer; may merge with existing preconditions. |
| L1 | Yes | Label-only pickup. | Four readiness facts checked. | keep-for-validation | Names the local recheck without becoming full triage. |
| L2 | Yes | Title-only or prompt-poor issue starts Context Intake. | Item can guide a fresh coding agent. | keep-for-validation | Keeps agent-prompt adequacy visible. |
| L3 | Yes | Unverifiable work starts. | Expected behavior, repro, doc target, validation hint, or done condition. | keep-for-validation | Explicitly avoids proof-plan ownership. |
| L4 | Yes | Starts blocked work or ignores dependency order. | Blocker state or repo-visible order confirmation. | keep-for-validation | Strong dependency gate. |
| L5 | Yes | Generic "ask if unsure" or invented requirements. | Missing fact named and tied to changed expected result. | keep-for-validation | Prior feedback is closed. |
| L6 | Yes | Prompt-poor or unverifiable pickup. | Readiness facts all pass, or pickup stops. | keep-but-prune-watch | Now validation-visible; dense enough to merge later. |
| L7 | Little | Phase bleed during readiness recheck. | Readiness facts recorded without later-owner work. | move-to-support | Duplicates H1/H2 and reads like process meta. |
| O1 | Yes | `implement` repairs or mutates unready work. | No repair/relabel/split/promote/rewrite/tracker mutation occurred. | keep-for-validation | Runtime-worthy prohibition; final wording may compress examples. |
| O2 | Yes | Multi-outcome work gets sliced inside selection. | Multiple independent outcomes/items/surfaces or one coherent item. | keep-but-prune-watch | Checkable enough for validation; do not expand into slicing. |
| O3 | Some | Silent high-risk pickup. | High-risk signal and repo/user boundaries. | owned-elsewhere | Exact policy belongs to engineering contract / repo docs. |
| O4 | Some | Owner-boundary drift. | Selection did not perform neighboring-owner work. | move-to-support | Useful audit checklist, too broad for runtime. |
| O5 | No meaningful runtime behavior | Meta assurance of owner handoff. | Owner-owned work left upstream. | cut | Duplicates O1/O4. |
| H1 | Yes | Context Intake starts without stable selected identity/facts. | Identity, checked surface, authority, readiness facts, branch outcomes recorded. | keep-for-validation | Strong handoff evidence. |
| H2 | Yes | File discovery, planning, proof, or edits begin before selection boundary. | No forbidden action before H1 facts. | keep-for-validation | Strong phase gate. |
| H3 | Yes | Handoff before selection facts are recorded. | H1 facts recorded. | keep-but-prune-watch | Valid handoff gate; likely merge with H1/H2 later. |
| H4 | Little | Completion wrapper around H1-H3. | Context Intake has selected item and facts. | cut | Redundant. |
| S1 | No runtime line | Examples needed only if validation exposes ambiguity. | Validation failure or borderline examples. | not-runtime-line | Audit in context-pointer section. |
| S2 | No runtime line | Runtime bloat from process rationale. | None for normal runtime. | cut | Rationale does not belong in runtime. |

## 5. Placement And Runtime Weight Audit

| Line ID | Prompt 08 Placement / Weight | Audit Verdict | Reason | Revision Direction |
| --- | --- | --- | --- | --- |
| R1 | Replace/merge selection opening; must-runtime | inline runtime | Core behavior. | Keep. |
| R2 | Insert near selection opening; must-runtime | inline runtime | Prior path wording fixed. | Keep; validate path split. |
| R3 | Merge with PRD/spec sentence; must-runtime | inline runtime | Needed route-only source handoff. | Keep route-only; no decomposition. |
| R4 | Insert; must-runtime | inline runtime | Blunt gate. | Keep. |
| R5 | Insert/fold; audit expansion | inline for validation / prune-watch | Protects current issue/path/URL behavior. | Keep for validation; final prune may fold examples. |
| A1 | Replace broad choose-next wording; must-runtime | inline runtime | Prevents invented priority/readiness. | Keep. |
| A2 | Strengthen ambiguous-order line; must-runtime | inline runtime | Preserves existing ask behavior. | Keep. |
| A3 | Strengthen no-issue line; must-runtime | inline runtime | Adds checked-surface evidence. | Keep concise. |
| A4 | Merge with tracker-doc mention; runtime core | inline pointer / prune-watch | Selection needs pointer; docs own syntax. | Keep short. |
| L1 | Insert after authority; must-runtime | inline runtime | Recheck is small and now has L6 consequence. | Keep. |
| L2 | Insert under readiness; must-runtime | inline runtime | Good definition; stays below full Context Intake. | Keep. |
| L3 | Insert under readiness; must-runtime | inline runtime | Good done-signal definition; avoids proof plan. | Keep. |
| L4 | Strengthen blockers line; must-runtime | inline runtime | Preserves dependency discipline. | Keep. |
| L5 | Merge with ask boundary; must-runtime | inline runtime | Prior feedback fixed. | Keep. |
| L6 | Insert/merge; must-runtime / prune-watch | inline for validation / prune-watch | Restored to compact block; required failure consequence. | Keep validation-visible; final prune may merge into L1. |
| L7 | Support-only | support-only | Duplicates handoff facts. | Keep out of runtime. |
| O1 | Insert near selection/readiness; must-runtime | inline runtime / prune-watch | Important owner guard, examples may bloat. | Keep; final prune can compress. |
| O2 | Insert if kept; audit expansion | inline for validation / prune-watch | Revised trigger is checkable enough. | Validate as stop/handoff smell only. |
| O3 | Support/pointer-only | owned elsewhere | Risk policy belongs to repo docs / engineering contract. | Keep out of runtime unless validation proves pointer needed. |
| O4 | Support-only | support-only | Bundles many owners. | Keep as audit checklist only. |
| O5 | Cut | cut | Meta duplicate. | Cut. |
| H1 | Insert before Context Intake; must-runtime | inline runtime | Required handoff evidence. | Keep. |
| H2 | Insert; must-runtime | inline runtime | Strong phase boundary. | Keep. |
| H3 | Insert/merge; must-runtime | inline runtime / prune-watch | Prior feedback fixed. | Keep for validation; final prune may merge. |
| H4 | Cut | cut | Redundant completion wrapper. | Cut. |
| S1 | Support-only | not runtime | Only useful if validation fails. | Defer. |
| S2 | Cut | cut | Process rationale bloat. | Cut. |

The minimal runtime core contains every behavior that must be validated. The
only remaining concerns are density, merge candidates, and owner-boundary
pruning after validation.

## 6. No-Op And Weak Language Check

| Line ID | Weakness | Why It Is Weak | Stronger Direction |
| --- | --- | --- | --- |
| R3 | Route line can grow into decomposition | `to-issues` owns source splitting. | Keep "ask or route"; no decomposition steps. |
| R5 | Example line can become bulky | It may duplicate R1/R4. | Keep through validation to protect path/URL behavior, then fold if safe. |
| A4 | Pointer duplication | Preconditions already mention tracker docs. | Keep only if validation needs line-local pointer. |
| L6 | Dense negative gate | It is clear but compact enough to be hard to read. | Keep validation-visible; final prune may merge with L1. |
| O1 | Long example list | It may overemphasize forbidden operations. | Final prune around "detect unready; do not make it ready." |
| O2 | "Coherent" is soft | Trigger is concrete, but target "coherent" needs validation. | Keep through validation, then prune if Bounded Slice Control covers it. |
| O3 | Risk pointer can become policy | Engineering contract owns policy. | Keep support/pointer-only. |
| H3 | Potential duplicate | H1/H2 already imply the boundary. | Keep through validation; likely merge later. |

No runtime line is a pure no-op. Weaknesses are mostly final-prune and
placement risks.

## 7. Gate Strength Check

| Line ID | Gate | Too Weak If | Too Heavy If | Revision Direction |
| --- | --- | --- | --- | --- |
| R1/R4 | Exactly one issue-equivalent item before Context Intake; no item, no implementation. | It allows a queue, list, or project. | It rejects one valid URL/path-backed ready item. | Keep with R2/R5. |
| R2/R3/R5 | Broad source surfaces are not scope until one ready item is named, while valid path/URL items still pass. | PRD/spec/path becomes implementation scope. | Any explicit path target is rejected. | Keep for validation. |
| A1 | Explicit user target or repo-visible ready/order authority. | Agent chooses "best" or "suitable" item. | It requires tracker mutation or full policy design. | Keep. |
| A2 | Multiple unordered candidates require user choice or repo order. | Agent silently prioritizes. | It asks despite visible order. | Keep. |
| A3 | No ready item stops and reports checked surface. | Agent creates/repairs work. | Reporting checked surface becomes a report workflow. | Keep concise. |
| L1-L6 | Recheck prompt adequacy, done signal, blockers, ambiguity; no failed readiness fact, no pickup. | It says only "confirm readiness." | It becomes full triage/Context Intake. | Keep validation-visible. |
| L4 | Blocked work waits unless this item is blocker/order-confirmed. | Blockers are ignored. | Agent edits dependency metadata. | Keep. |
| L5 | Ask only on named result-changing missing fact. | Generic uncertainty triggers asks, or missing requirements are invented. | Ordinary implementation unknowns block selection. | Keep. |
| O1 | Detect unready work; do not make it ready. | Agent repairs/relabels/splits/promotes. | Normal selection is refused. | Keep; prune later. |
| O2 | Multiple independent outcomes/items/surfaces require narrowing or handoff. | Broad multi-issue work is accepted as one item. | Normal bounded issue is rejected. | Validate as prune-watch. |
| H1-H3 | Record selection facts before Context Intake; no planning/editing before facts. | Handoff happens on vibes. | Full implementation plan is required. | Keep. |

## 8. Ownership / Duplication Check

| Line ID | Possible Duplicate Owner | Conflict Or Duplication | Action |
| --- | --- | --- | --- |
| R1/R4 | runtime skill | Strengthens existing one-issue behavior. | Keep. |
| R2/R5 | runtime skill / existing `implement` | Must preserve issue/path/URL target behavior. | Keep for validation. |
| R3 | `to-issues` | Safe if route-only; duplicate if it decomposes. | Keep route-only. |
| A1/A2/A3 | runtime skill | Strengthens existing selection behavior. | Keep. |
| A4 | tracker docs | Tracker docs own syntax, labels, commands, state, dependencies. | Keep as pointer only. |
| L1-L6 | `triage`, Context Intake | Selection owns small recheck; `triage` owns repair and promotion. | Keep small; no repair/promotion. |
| L3 | Semantic Proof | Selection owns done signal; proof owns proof design. | Keep without proof plan. |
| L4 | tracker docs | Runtime owns blocker decision; docs own syntax/mutation. | Keep. |
| L5 | engineering contract / user | Selection owns result-defining ambiguity; contract owns broader commitment boundary. | Keep narrow. |
| O1 | `triage`, `to-issues`, tracker docs | Keep prohibition; owners perform repair/splitting/mutation. | Keep, prune later. |
| O2 | `to-issues`, Bounded Slice Control | Selection may reject; owners split/control scope. | Keep as prune-watch. |
| O3 | engineering contract / repo docs | Exact risk policy owned elsewhere. | Owned elsewhere / pointer-only. |
| O4 | many owners | Bundles `triage`, `to-issues`, Context Intake, Semantic Proof, Review/Lock. | Support-only. |
| H1-H3 | Context Intake | Handoff facts help Context Intake; do not start planning here. | Keep. |
| S1 | future support doc | Optional examples. | Defer. |
| S2 | support/reference | Rationale-only. | Cut. |

## 9. Context Pointer Check

| Line ID Or Decision | Inline / Pointer / No Pointer / Not Runtime | Target If Pointer | Why | Risk |
| --- | --- | --- | --- | --- |
| A4 | Inline pointer | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, repo-local tracker docs | Selection depends on ready/order/dependency semantics. | Duplicates preconditions if too wordy. |
| L2/L3 examples | No pointer yet | Future implement support/examples doc | Validate before adding examples. | Examples may become support sediment. |
| O3 | Pointer/support only | `docs/agents/engineering-contract.md`, repo policy docs | Risk policy is repo-owned. | Inline policy would duplicate the contract. |
| O2 | No pointer or support-only | Bounded Slice Control / `to-issues` | Selection can reject obvious multi-outcome candidates but should not teach slicing. | Could steal Bounded Slice Control. |
| O4 | Not runtime / support-only | Prompt 09 audit notes | Good ownership checklist but too broad. | Runtime bloat. |
| S1 | Support-only | Future examples doc | Only if validation shows misreadiness. | Premature disclosure. |
| S2 | Cut | None | Source rationale is not needed for runtime. | Process-theory bloat. |

## 10. Leading Word Check

| Line ID | Leading Word | Strong / Weak | Why | Action |
| --- | --- | --- | --- | --- |
| R1/R4 | issue-equivalent item | Strong with examples | Prevents "issue" from excluding URL/tracker/path-backed item. | Keep with R5 through validation. |
| A1 | repo-visible ready/order policy | Strong but formal | Anchors visible authority. | Keep or compress to "repo-visible ready/order source" later. |
| L1 | local readiness recheck | Strong | Names small pre-context gate. | Keep. |
| L2 | agent-prompt adequacy | Strong | Agent-specific readiness gate. | Keep. |
| L3 | observable done signal | Strong | Prevents unverifiable pickup without proof plan. | Keep. |
| L5 | result-defining ambiguity | Strong | Better than "unclear"; now observable. | Keep. |
| L6 | no pickup | Strong gate | Supplies failure consequence. | Keep validation-visible; merge later only if consequence survives. |
| O1 | detect unready work; do not make it ready | Strong | Good owner-boundary phrase. | Keep; prune examples later. |
| O2 | multiple independent outcomes/items/surfaces | Stronger than prior wording | Concrete enough to validate. | Keep as prune-watch. |
| H2 | select first, plan later | Strong | Recruits phase-boundary behavior. | Keep. |
| H3 | H1 facts recorded | Strong enough | Observable handoff condition. | Keep as prune-watch. |

## 11. Regression Check

| Existing Behavior | Preserved? | Candidate Line(s) | Risk |
| --- | --- | --- | --- |
| Pick up one ready-for-agent issue. | Yes | R1, R4, R5 | Could broaden too far if issue-equivalent includes broad PRD/spec/path. |
| Stop after one issue. | Yes | R1, R4, H1-H3 | No major risk. |
| Explicit issue/path/URL target can be implemented. | Yes, must validate | R2, R5 | `R5` must stay visible through validation. |
| PRD/spec is used to find or choose one ready issue, not implement whole spec. | Yes | R2, R3 | Good if route-only. |
| No provided issue means use ready labels/tracker docs. | Yes | A1, A3, A4 | A4 must stay pointer-only. |
| Dependency order and blocker skip remain. | Yes | L4, A4 | Must not mutate dependency metadata. |
| Ambiguous order asks user. | Yes | A2 | No major risk. |
| No issue available stops. | Yes | A3 | Reporting checked surface is a useful addition. |
| Prompt-poor / no done signal work should not start. | Yes | L1-L6 | `L6` is now in the compact block and should stay validation-visible. |
| Context Intake reads issue/context after selection. | Yes | H1-H3 | H2 must not forbid Context Intake after H1 facts. |
| Bounded slice behavior remains later. | Yes | O2 | O2 must not become slicing workflow. |
| Proof strategy remains later. | Yes | L3, H2 | L3 must not require proof plan. |
| Review, commit, and note remain later. | Yes | O4, H2 | O4 should not be runtime. |
| Issue state changes only when requested or repo-defined. | Yes | A4, O1 | O1/A4 should not duplicate tracker procedures. |

## 12. Revised Candidate Line Set

### Keep For Validation

- `R1`: Before Context Intake, select exactly one issue-equivalent item.
- `R2`: A queue, project, PRD, spec, batch, list, or bare source path is not
  implementation scope until one ready issue-equivalent item is named.
- `R3`: If the user provides a PRD, spec, source document, or path without one
  ready item, ask for the target item or route to `to-issues`.
- `R4`: No one issue-equivalent item, no implementation.
- `A1`: Use an explicit user target or repo-visible ready/order source; do not
  invent priority or readiness.
- `A2`: If multiple eligible items remain unordered, ask for the user choice or
  repo order.
- `A3`: If no ready item exists on the checked surface, stop and report that
  surface.
- `L1`: Run a local readiness recheck: agent-prompt adequacy, observable done
  signal, blocker/dependency state, and result-defining ambiguity.
- `L2`: Agent-prompt adequacy means the item can guide a fresh coding agent
  into Context Intake without issue repair.
- `L3`: Observable done signal means the item names an expected behavior,
  repro, doc target, validation hint, or done condition; it does not require a
  proof plan yet.
- `L4`: Blocked work waits unless the selected item is the blocker or
  repo-visible order confirms this item should be worked now.
- `L5`: Ask only after naming the missing fact and how it would change the
  expected result.
- `O1`: Detect unready work; do not make it ready inside `implement`.
- `H1`: Record selected item identity, checked surface, selection authority,
  readiness facts, and branch outcomes.
- `H2`: Select first, plan later: no file discovery, implementation planning,
  proof strategy, or edits until selection facts are recorded.

### Keep But Prune-Watch

- `R5`: Keep concrete examples of issue, URL, tracker item, path-backed ready
  slice, and explicit user-selected work item through validation.
- `A4`: Keep as a short tracker-doc pointer and metadata-mutation guard.
- `L6`: Keep the no-pickup readiness-failure gate validation-visible; final
  prune may merge it into `L1`.
- `O2`: Keep the multiple-outcome/item/surface smell through validation, but
  do not let it become slicing guidance.
- `H3`: Keep as explicit handoff gate; final prune may merge with `H1`/`H2`.

### Revise Before Validation

- None.

### Move To Support

- `L7`: Use only as audit/support guidance because it duplicates the handoff
  boundary.
- `O4`: Keep as an audit ownership checklist, not runtime wording.
- `S1`: Defer examples until validation shows they are needed.

### Owned Elsewhere

- `R3`: `to-issues` owns decomposition; `implement` may only ask or route.
- `A4`: Tracker docs own exact labels, ordering, state, commands, and
  dependency syntax.
- `O1`: `triage`, `to-issues`, and tracker owners own repair, splitting,
  promotion, and mutation; `implement` owns the prohibition.
- `O2`: `to-issues` and Bounded Slice Control own decomposition and detailed
  slicing.
- `O3`: Engineering contract / repo docs own exact risk policy.
- `H2`: Context Intake, Semantic Proof, and implementation phases own the later
  actions; selection owns the prohibition before H1 facts.

### Cut

- `A5`: Duplicates `A1`/`A2`; already removed from runtime.
- `O5`: Meta completion line; duplicates `O1`/`O4`.
- `H4`: Redundant wrapper around `H1`-`H3`.
- `S2`: Source-process rationale is not needed in runtime.

### Not Runtime Lines

- Compact-draft decision: audited as Prompt 08 handoff, not runtime wording.
- Context-pointer rows: audited in Section 9.
- Minimal runtime core rows: audited in Section 5.

## 13. Handoff To Validation Draft

Audit decision: `ready-for-validation-draft`

Reason:

- Prior Prompt 09 feedback is closed: `R2`, `L5`, `O2`, and `H3` now have
  stronger wording; duplicate/meta lines are demoted or cut; and `L6` is now
  present in both the runtime-step inventory and assembled compact draft block.
- No remaining line requires a Prompt 08 revision before Prompt 10.
- Remaining risks are validation and final-prune risks: path/URL acceptance,
  dense readiness wording, tracker pointer duplication, owner-boundary bloat,
  and `O2` overlap with Bounded Slice Control / `to-issues`.

Lines ready for validation-draft assembly:

- `R1`, `R2`, route-only `R3`, `R4`, prune-watch `R5`;
- `A1`, `A2`, `A3`, short pointer `A4`;
- `L1`, `L2`, `L3`, `L4`, `L5`, prune-watch `L6`;
- compressed `O1`, prune-watch `O2`, support/pointer-only `O3`;
- `H1`, `H2`, prune-watch `H3`.

Lines that must be revised before draft assembly:

- None.

Scenario-ready validation tasks tied to line IDs for Prompt 10 to preserve:

| Validation ID | Line IDs | Scenario Or Fixture Needed | Behavior / Gate To Test | Regression Risk |
| --- | --- | --- | --- | --- |
| V1-single-item | R1, R2, R4, R5, H1 | User gives a queue/list/project with several candidates, and separately gives one issue/URL/tracker item/path-backed ready slice. | Agent rejects broad scope but accepts one concrete item when readiness facts pass. | Regresses into "pick a ready issue" or overblocks valid explicit targets. |
| V2-prd-source-handoff | R2, R3, O1 | User gives PRD/spec/bare source path but no ready item. | Agent asks for target item or routes to `to-issues`; no decomposition. | `implement` starts authoring issues. |
| V3-path-backed-slice | R2, R5 | User gives one path-backed ready slice, URL, or explicit path target. | Agent can treat it as the one item when readiness facts pass. | Revised wording overblocks current path/URL behavior. |
| V4-authority | A1, A2, A4 | Multiple ready candidates with no visible order. | Agent asks for user choice or repo order; does not invent priority. | Hidden "best issue" selection. |
| V5-no-ready | A3, O1 | Checked surface has no ready item. | Agent stops and reports checked surface. | Agent creates, repairs, or promotes work. |
| V6-readiness | L1, L2, L3, L6 | Candidate has ready label but weak body or no done signal. | Agent runs local readiness recheck and does not pick up work with failed readiness facts. | Label-only pickup or prompt-poor implementation. |
| V7-blocker | L4, A4 | Candidate has visible unresolved blocker. | Agent waits, selects blocker if appropriate, or asks for order confirmation. | Starts blocked work or edits dependency metadata. |
| V8-ambiguity | L5 | Candidate has a result-defining gap. | Agent asks only after naming the missing fact and expected-result effect. | Generic "ask if unsure" or invented requirements. |
| V9-owner-boundary | O1, O2 | Candidate needs repair or contains multiple independent outcomes. | Agent asks for one coherent ready item or hands off; does not split or repair. | Duplicates `triage`, `to-issues`, or Bounded Slice Control. |
| V10-selection-boundary | H1, H2, H3 | Valid candidate selected. | Agent records identity, checked surface, authority, readiness facts before Context Intake. | Starts file discovery, proof strategy, or edits too early. |

Regression risks to test:

- valid path and URL targets still work when they are one ready
  issue-equivalent item;
- bare source paths and source documents do not become scope without one ready
  item;
- local readiness remains smaller than `triage` and Context Intake;
- failed prompt adequacy or missing done signal blocks pickup;
- result-defining ambiguity does not become generic uncertainty;
- multi-outcome smell does not become a slicing workflow;
- risk pointer does not become inline policy;
- selection boundary does not start planning.

Likely final-prune targets:

- `R5` examples, if validation proves path/URL behavior stays safe without
  inline examples;
- `A4` if existing preconditions can carry the tracker-doc pointer;
- `L6` if merged into `L1`;
- `O1` examples if the compact phrase "do not make it ready" proves enough;
- `O2` if Bounded Slice Control absorbs the size smell;
- `O3`, `L7`, `O4`, `O5`, `H4`, `S1`, and `S2`.
