# Prompt 08: Compact Draft For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/08-candidate-runtime-draft.md`](../../../methods/prompts/08-candidate-runtime-draft.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Generous synthesis:
[`07-full-behavior-synthesis.md`](07-full-behavior-synthesis.md)

Behavior flow:
[`06-agent-bridge.md`](06-agent-bridge.md)

Existing skill text to preserve: `skills/current/implement/SKILL.md`,
especially the current description, "Implement one ready-for-agent issue. Stop
after one issue.", issue selection, preconditions, Context Intake, bounded
slice behavior, proof/review/commit/note flow, and the rule against issue state
changes unless requested or repo-defined.

Revision feedback: prior review decision was `revise-before-draft`.
First feedback revised `R2`, `L5`, `O2`, and `H3` and demoted or cut
duplicate/meta lines. Second feedback found one remaining compact-block gap:
`L6` existed in the runtime inventory but not the assembled candidate draft.
Restore `L6` there while preserving stable line IDs.

Subagent inputs used:

- Revision wording pass: keep stable IDs and revise `R2`, `L5`, `O2`, and
  `H3` in place.
- Owner placement pass: preserve explicit issue/path/URL behavior, keep
  `R3` route-only, compress `O1`, move `O3`/`O4` to support or pointer-only,
  and cut duplicate meta lines.
- Validation-draft readiness pass: preserve scenario risks while returning this
  revised draft to `ready-for-detailed-skill-context-draft`.
- Narrow compact-block repair: restore `L6` in the assembled candidate compact
  draft so Prompt 09 can validate the no-pickup consequence.

## 1. Compact Draft Scope

This draft compacts Facet 1, `Ready Issue Selection`, into candidate runtime
wording for the existing `implement` skill.

Synthesis input used:

- Prompt 06 behavior flow;
- Prompt 07 generous synthesis;
- existing `skills/current/implement/SKILL.md`;
- prior revision feedback;
- three revised Prompt 08 subagent passes on wording, owner placement, and
  validation-readiness risks.

Existing skill behavior that must be preserved:

- `implement` invokes on one ready-for-agent issue;
- the agent stops after one issue;
- if no issue is provided, it uses repo-visible tracker docs and ready labels;
- ambiguous ready ordering asks the user;
- unavailable ready work stops;
- baseline capture, Context Intake, bounded implementation, proof, review,
  commit, and issue note remain later steps;
- issue state changes happen only when requested or repo-defined.

This draft must make one behavior predictable: before Context Intake, the agent
selects exactly one issue-equivalent item with visible authority and compact
readiness facts, or it stops, asks, narrows, or hands off.

This draft must not decide final runtime text, edit `SKILL.md`, add support
docs, decompose source documents, make issues ready, author risk policy, plan
implementation, design proof, review the diff, commit, or write issue notes.

## 2. Prompt 07 Handoff Check

| Handoff Item | Prompt 07 Direction | Step 08 Disposition | Risk For Prompt 09 |
| --- | --- | --- | --- |
| Compression contract: one item | Preserve one selected issue-equivalent item. | `R1` and `R4` make it the opening hard gate. | "Ready issue" could erase non-issue-equivalent targets and source-surface checks. |
| Compression contract: source documents | A PRD/spec/path is not implementation scope until one ready item is named. | Revised `R2` and `R3` keep the source-document stop/handoff inline while preserving explicit path-backed ready targets. | Wording may still overblock path targets if Prompt 09 does not check `R2`. |
| Selection authority | Use repo-visible ordering or explicit user target; do not invent priority. | `A1` through `A4` make authority visible and checkable. | "Best", "suitable", or "looks ready" would be no-ops. |
| Local readiness recheck | Preserve prompt adequacy, done signal, blocker/dependency, and result-defining ambiguity. | `L1` through `L6` keep all four sub-gates inline. | "Confirm readiness" would hide the real checks. |
| Agent-prompt adequacy | Keep visible or fold only with the exact fresh-agent meaning. | `L2` keeps fresh coding agent language. | Could become too heavy by requiring full context or exact files. |
| Observable done signal | Preserve without becoming proof strategy. | `L3` keeps it as a selection gate. | Could duplicate Semantic Proof if it asks for a proof plan. |
| Blocker/dependency check | Detect blockers; tracker docs own syntax and mutation. | `L4` and `A4` preserve detection and pointer shape. | Could drift into tracker metadata editing. |
| Result-defining ambiguity | Ask only when missing information changes expected result. | Revised `L5` requires naming the missing fact and result effect; `L6` remains prune-watch. | Generic "ask if unsure" would make the agent timid. |
| No-ready stop | Stop and report checked surface. | `A3` keeps no-ready behavior. | Could silently route into issue creation. |
| PRD/spec stop | Ask for target or route upstream. | `R3` keeps the branch. | Could duplicate `to-issues` if it decomposes the document. |
| Owner-boundary stop | Detect unready work; do not repair, relabel, split, promote, or mutate it. | Compressed `O1` is the runtime guard; `O4` moves to support. | Could duplicate `triage`, `to-issues`, or tracker ownership if expanded. |
| Risk-domain confirmation | Keep short; repo docs own exact policy. | `O3` moves to support/pointer-only unless validation proves runtime needs it. | Could become an inline risk policy. |
| Obvious multi-issue smell | Optional short narrow/handoff branch; do not slice here. | Revised `O2` names multiple independent outcomes, items, or unrelated surfaces. | Could duplicate Bounded Slice Control or `to-issues`. |
| Select first, plan later | Record selection facts before Context Intake. | Revised `H3` starts Context Intake only after `H1` facts are recorded. | Could collapse into planning, file discovery, proof, or edits. |
| Support-only material | WIP, DoR, INVEST, Scrum, Small CLs, and source examples move out of runtime. | Cut or pointer-only in Sections 9 and 11. | Source vocabulary could bloat runtime. |
| Research-only material | Kanban metrics, Scrum ceremonies, SWE-bench scoring, platform setup, and detailed splitting stay out. | Cut in Section 11. | Runtime could become a research summary. |
| Design questions | Risk and multi-issue survive as short candidate lines; exact tracker/risk policy deferred. | Marked as candidate-runtime or support pointer. | Prompt 09 must decide whether these are too heavy. |

## 3. Revision Feedback Disposition

| Feedback Item | Affected Line IDs Or Sections | Step 08 Action | Remaining Audit Risk |
| --- | --- | --- | --- |
| `R2` overblocked valid path targets | `R2`, `R3`, `R5`, candidate candidate runtime draft, regression risks | Revised `R2` to block a bare source path/source surface, not a path-backed ready slice or explicit path target. | Prompt 09 should verify `R2` still prevents whole-source implementation without rejecting one ready path target. |
| `L5` was too hand-wavy | `L5`, `L6`, candidate candidate runtime draft, gates | Revised `L5` to require naming the missing fact and how it would change the expected result. | Prompt 09 should check this does not become generic "ask if unsure" or block ordinary implementation unknowns. |
| `O2` used subjective "plainly many issues" wording | `O2`, minimal runtime core, gates, validation tasks | Revised `O2` to name multiple independent outcomes, items, or unrelated surfaces. | Prompt 09 should check this rejects broad work without becoming a slicing workflow. |
| `H3` used soft "facts are stable" wording | `H1`, `H2`, `H3`, candidate candidate runtime draft | Revised `H3` to start Context Intake only after `H1` facts are recorded. | Prompt 09 should check the handoff is not duplicative with `H1`/`H2`. |
| Duplicate/meta lines should be demoted or cut | `A5`, `L7`, `O3`, `O4`, `O5`, `H4`, `S1`, `S2` | Cut `A5`, `O5`, `H4`, and `S2`; moved `L7`, `O3`, `O4`, and `S1` to support/prune-watch. | Prompt 09 should confirm no useful runtime gate was lost. |
| `L6` missing from assembled candidate runtime draft block | `L1`, `L2`, `L3`, `L6`, candidate candidate runtime draft | Restored `L6` to the assembled candidate candidate runtime draft block without changing line IDs. | Prompt 09 should verify the no-pickup consequence is now part of the validation target. |

Line ID changes: none. Existing IDs were revised, demoted, or cut in place;
no new runtime IDs were introduced.

## 4. Compression Principles

Strong leading words to preserve:

- `one selected issue-equivalent item`;
- `repo-visible ordering or explicit user target`;
- `selection authority`;
- `local readiness recheck`;
- `agent-prompt adequacy`;
- `observable done signal`;
- `blocker/dependency state`;
- `result-defining ambiguity`;
- `detect unready work; do not make it ready`;
- `select first, plan later`.

Explanatory prose cut:

- why one active item improves flow;
- why source documents can be too broad;
- why issue quality matters for agents;
- detailed rationale for WIP, DoR, INVEST, Scrum, SWE-bench, or Small CLs;
- examples of every possible tracker shape.

Belongs behind context pointers:

- exact ready labels, state names, ordering fields, dependency syntax, and
  local tracker mappings;
- repo-specific sensitive or high-risk policy;
- support examples for borderline agent-prompt adequacy and done-signal
  checks;
- rationale for pull/WIP and DoR contrast, if later support docs need it.

Blunt gates needed:

- No one issue-equivalent item, no implementation.
- No visible authority, no selection.
- No prompt adequacy or done signal, no pickup.
- Blocked work waits unless the selected item is the blocker.
- Result-defining ambiguity requires a user or upstream answer.
- Detect unready work; do not make it ready.
- Record selection facts before planning.

Research-only material:

- Kanban metrics and cadences;
- Scrum ceremonies and roles;
- full DoR / INVEST mechanics;
- SWE-bench scoring methodology;
- Copilot platform setup;
- detailed Small CL splitting tactics.

## 5. Candidate Invocation / Description Wording

No invocation wording change proposed.

The existing description already says `implement` picks up one ready-for-agent
issue, implements it, verifies it, reviews it, commits it, and leaves a note.
This facet changes the runtime selection behavior after invocation, not the
trigger surface.

Risk to preserve: the current description says "one ready-for-agent issue" rather
than "one issue-equivalent item." Prompt 09 should check whether the runtime
lines are enough to cover URLs, tracker items, and path-backed ready slices
without broadening invocation.

## 6. Candidate Runtime Steps

### Select One Item

[R1] Before Context Intake, select exactly one issue-equivalent item.

[R2] A queue, project, PRD, spec, batch, list, or bare source path is not
implementation scope until one ready issue-equivalent item is named.

[R3] If the user provides a PRD, spec, source document, or path without one
ready item, ask for the target item or route to `to-issues`.

[R4] No one issue-equivalent item, no implementation.

[R5] Done when exactly one issue, URL, tracker item, path-backed ready slice,
or explicit user-selected work item is named.

### Apply Selection Authority

[A1] Use an explicit user target or repo-visible ready/order policy; do not
invent priority or readiness.

[A2] If multiple eligible items remain unordered, ask for the user choice or
repo order.

[A3] If no ready item exists on the checked surface, stop and report that
surface.

[A4] Use repo tracker docs for ready labels, ordering, state, and dependency
syntax; do not edit tracker metadata here.

### Run Local Readiness Recheck

[L1] Run a local readiness recheck: agent-prompt adequacy, observable done
signal, blocker/dependency state, and result-defining ambiguity.

[L2] Agent-prompt adequacy means the item can guide a fresh coding agent into
Context Intake without issue repair.

[L3] Observable done signal means the item names an expected behavior, repro,
doc target, validation hint, or done condition; it does not require a proof
plan yet.

[L4] Blocked work waits unless the selected item is the blocker or repo-visible
order confirms this item should be worked now.

[L5] Ask only after naming the missing fact and how it would change the
expected result.

[L6] No prompt adequacy, done signal, clear blocker state, or ambiguity result,
no pickup.

### Preserve Owner Boundaries

[O1] Detect unready work; do not make it ready inside `implement`: no repair,
relabeling, splitting, promotion, reprioritization, rewriting, or tracker-state
mutation.

[O2] If the candidate contains multiple independent outcomes, items, or
unrelated surfaces, ask for one coherent ready item or hand off upstream; do
not split it here.

### Record Selection Boundary

[H1] Record selected item identity, checked surface, selection authority,
readiness facts, and branch outcomes.

[H2] Select first, plan later: no file discovery, implementation planning,
proof strategy, or edits until selection facts are recorded.

[H3] Start Context Intake only after the `H1` selection facts are recorded.

## 7. Candidate Line Inventory And Placement

| Line ID | Candidate Line | Function | Placement / Merge Target | Prompt 07 Source | Runtime Weight | Audit Risk |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Before Context Intake, select exactly one issue-equivalent item. | step | replace/merge with `### 1. Select The Issue` opening | one selected issue-equivalent item | must-runtime | Could be too abstract without R5 examples. |
| R2 | A queue, project, PRD, spec, batch, list, or bare source path is not implementation scope until one ready issue-equivalent item is named. | hard gate | insert near selection opening | PRD/spec/path not scope | must-runtime | Must not overblock explicit path targets or path-backed ready slices. |
| R3 | If source document/path lacks one ready item, ask or route to `to-issues`. | stop/ask rule | merge with existing PRD/spec sentence | PRD/spec stop | must-runtime | Could duplicate `to-issues` if it says how to decompose. |
| R4 | No one issue-equivalent item, no implementation. | hard gate | insert | blunt gate | must-runtime | Could sound harsh but useful. |
| R5 | Done when one concrete issue-equivalent item is named. | completion criterion | insert | selection completion | must-runtime | Examples must not widen into a batch. |
| A1 | Use explicit user target or repo-visible ready/order policy. | hard gate | replace broad "choose next" wording | selection authority | must-runtime | Weak if "repo-visible" is undefined by pointer. |
| A2 | Multiple unordered eligible items ask user/order source. | stop/ask rule | keep/strengthen existing ambiguous order line | multiple-candidate branch | must-runtime | Good as-is; check duplicate risk against current text. |
| A3 | No ready item stops and reports checked surface. | stop/ask rule | keep/strengthen existing no issue line | no-ready stop | must-runtime | Could become too much reporting if verbose. |
| A4 | Use tracker docs for syntax; do not edit metadata here. | context pointer | merge with existing tracker-doc mention | tracker docs pointer, owner boundary | candidate-runtime | Could duplicate preconditions; Prompt 09 should place carefully. |
| L1 | Run local readiness recheck with four named facts. | recheck | insert after authority | local readiness recheck | must-runtime | Must not become full triage checklist. |
| L2 | Agent-prompt adequacy guides fresh coding agent into Context Intake. | recheck | insert under readiness | agent-prompt adequacy | must-runtime | Could require full context if phrased poorly. |
| L3 | Observable done signal exists without proof plan. | recheck | insert under readiness | observable done signal | must-runtime | Could duplicate Semantic Proof if expanded. |
| L4 | Blocked work waits unless selected item is blocker/order confirmed. | hard gate | replace/strengthen existing blockers line | blocker/dependency check | must-runtime | Needs tracker syntax pointer elsewhere. |
| L5 | Ask only after naming the missing fact and how it would change the expected result. | stop/ask rule | merge with later ask/commitment boundary | result-defining ambiguity | must-runtime | Could become too heavy if ordinary implementation unknowns block selection. |
| L6 | No readiness facts, no pickup. | hard gate | insert | blunt readiness gate | must-runtime | Slightly dense; Prompt 09 should check readability. |
| L7 | Readiness facts recorded without Context Intake/proof/repair. | completion criterion | defer to support | select first, plan later | support-only | Duplicates H1/H2. |
| O1 | Detect unready work; do not make it ready inside `implement`. | ownership guard | insert near selection/readiness | owner-boundary stop | must-runtime | Examples may still bloat final runtime. |
| O2 | Multiple independent outcomes, items, or unrelated surfaces ask or hand off; do not split here. | stop/ask rule | insert if kept | obvious multi-issue smell | candidate-runtime | Could duplicate Bounded Slice Control if expanded. |
| O3 | Use repo docs or engineering contract for high-risk pickup boundaries. | context pointer | defer to support | risk-domain confirmation | support-only | Could duplicate engineering contract if kept inline. |
| O4 | Stop/handoff for neighboring owners. | ownership guard | defer to support | owner conflicts | support-only | Useful support checklist, too broad for runtime. |
| O5 | Done when owner-owned work was not repaired inside selection. | completion criterion | cut | owner-boundary completion | likely-prune | Meta duplicate. |
| H1 | Record selected item identity, checked surface, authority, readiness facts, and branch outcomes. | handoff | insert before Context Intake handoff | selection facts | must-runtime | Must remain selection facts, not plan. |
| H2 | Select first, plan later. | hard gate | insert | select first, plan later | must-runtime | Strong; check duplication with Context Intake. |
| H3 | Start Context Intake only after the `H1` selection facts are recorded. | handoff | insert/merge | Context Intake handoff | must-runtime | Could duplicate H1/H2 if overexplained. |
| H4 | Done when Context Intake has one selected item and recorded facts. | completion criterion | cut | handoff completion | likely-prune | Redundant wrapper. |

## 8. Candidate Rules / Gates

| Line ID | Candidate Line | Purpose | Failure Prevented |
| --- | --- | --- | --- |
| R4 | No one issue-equivalent item, no implementation. | Keep the run singular. | Batch, queue, PRD, project, or vague request becomes scope. |
| A1 | Use explicit user target or repo-visible ready/order policy; do not invent priority or readiness. | Preserve authority. | Agent chooses by taste or convenience. |
| A2 | If multiple eligible items remain unordered, ask for the user choice or repo order. | Keep priority user/repo-owned. | Hidden prioritization. |
| A3 | If no ready item exists on the checked surface, stop and report that surface. | Stop busywork. | Agent creates or repairs work inside `implement`. |
| L1 | Run a local readiness recheck with four named facts. | Prevent label-only pickup. | Work starts from an unusable issue. |
| L4 | Blocked work waits unless selected item is the blocker or repo-visible order confirms this item should be worked now. | Preserve dependency order. | Work starts behind an unresolved blocker. |
| L5 | Ask only after naming the missing fact and how it would change the expected result. | Avoid invented requirements without timid asking. | Generic uncertainty blocks ordinary implementation. |
| L6 | No prompt adequacy, done signal, clear blocker state, or ambiguity result, no pickup. | Make readiness blunt. | Prompt-poor or unverifiable work starts. |
| O1 | Detect unready work; do not make it ready inside `implement`. | Preserve owner boundaries. | `implement` becomes `triage` or `to-issues`. |
| H2 | Select first, plan later: no file discovery, implementation planning, proof strategy, or edits until selection facts are recorded. | Preserve phase boundary. | Selection collapses into Context Intake or coding. |

## 9. Context Pointer Candidates

| Line ID | Pointer Text | Target Support Doc | Why It Should Be Disclosed | When Agent Should Open It |
| --- | --- | --- | --- | --- |
| A4 | Use repo tracker docs for ready labels, ordering, state, and dependency syntax. | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, repo-local tracker docs | Exact tracker semantics are repo-owned and changeable. | When selection depends on ready labels, ordering, blockers, or local tracker mappings. |
| O3 | Use repo docs or the engineering contract for high-risk pickup boundaries. | `docs/agents/engineering-contract.md`, repo policy docs | Runtime should not define a universal risk policy. | When validation shows high-risk pickup is otherwise missed. |
| S1 | See support examples for agent-prompt adequacy and done-signal checks. | Future implement support/examples doc | Borderline readiness examples may help without bloating runtime. | When an item is not clearly prompt-poor but the readiness check is uncertain. |
| S2 | Source rationale for pull/WIP and DoR contrast lives in support. | Future synthesis/support rationale, if created | Explains why the gate exists without turning runtime into process theory. | Maintainer context only, not normal runtime. |

## 10. Minimal Runtime Core

| Line ID | Runtime Core / Audit Expansion / Support / Cut | Why |
| --- | --- | --- |
| R1 | Runtime Core | Names the first phase output. |
| R2 | Runtime Core | Blocks broad source surfaces without rejecting path-backed ready work. |
| R3 | Runtime Core | Keeps PRD/spec/path handoff explicit. |
| R4 | Runtime Core | Blunt singularity gate. |
| R5 | Audit Expansion | Useful completion criterion; may compress into R1/R4. |
| A1 | Runtime Core | Prevents invented priority/readiness. |
| A2 | Runtime Core | Preserves user/repo priority owner. |
| A3 | Runtime Core | Prevents busywork when no ready item exists. |
| A4 | Runtime Core | Keeps tracker specifics behind repo docs and blocks metadata mutation. |
| L1 | Runtime Core | Names compact readiness facts. |
| L2 | Runtime Core | Preserves agent-prompt adequacy. |
| L3 | Runtime Core | Preserves done signal without proof plan. |
| L4 | Runtime Core | Preserves dependency discipline. |
| L5 | Runtime Core | Preserves result-defining ambiguity branch. |
| L6 | Audit Expansion | Blunt gate; may merge with L1-L5. |
| L7 | Support | Handoff check duplicates H1-H2. |
| O1 | Runtime Core | Hard owner boundary; final prune should compress examples. |
| O2 | Audit Expansion | Useful optional smell; Prompt 09 should check duplication with Bounded Slice Control. |
| O3 | Support | Risk policy belongs to repo docs / engineering contract. |
| O4 | Support | Good support checklist, too broad for final runtime. |
| O5 | Cut | Meta completion line likely unnecessary. |
| H1 | Runtime Core | Records handoff facts. |
| H2 | Runtime Core | Prevents premature planning. |
| H3 | Runtime Core | Names the Context Intake handoff gate. |
| H4 | Cut | Redundant with H1-H3. |
| S1 | Support | Future examples only. |
| S2 | Cut | Rationale is not needed in runtime. |

## 11. Cut / Preserve Log

| Material | Cut / Preserve / Move | Why |
| --- | --- | --- |
| One selected issue-equivalent item | Preserve | Core facet output. |
| Queue/project/PRD/spec/bare source path not scope until one item named | Preserve | Prevents broad-source drift without blocking path-backed ready work. |
| Repo-visible order or explicit user target | Preserve | Selection authority is user/repo-owned. |
| "Pick a ready issue" wording | Cut | Too weak; loses issue-equivalent and authority gates. |
| "Choose the best/suitable/highest-priority issue" wording | Cut | Invites invented priority. |
| Local readiness recheck | Preserve | Prevents label-only pickup. |
| Agent-prompt adequacy | Preserve | Agent-specific readiness criterion. |
| Observable done signal | Preserve | Prevents unverifiable work. |
| Full acceptance/proof plan | Cut | Semantic Proof owns proof strategy. |
| Blocker/dependency check | Preserve | Prevents wrong-order work. |
| Exact dependency syntax | Move | Repo tracker docs own exact syntax. |
| Result-defining ambiguity | Preserve | Prevents invented product intent. |
| Generic "ask if unsure" | Cut | Too timid and not checkable. |
| Issue repair/relabel/split/promote/rewrite | Preserve as prohibited behavior | Protects `triage`, `to-issues`, and tracker owners. |
| Risk-domain confirmation | Move | Useful guard, but exact policy belongs elsewhere. |
| Obvious multi-issue smell | Preserve as validation detail | Useful rejection when tied to multiple independent outcomes/items/surfaces; slicing belongs elsewhere. |
| Select first, plan later | Preserve | Protects Context Intake boundary. |
| File discovery/planning/proof/editing | Preserve as prohibited behavior before handoff | Prevents phase collapse. |
| Kanban/WIP/DoR/INVEST/Scrum/Small CL source terms | Move or cut | Support rationale only. |
| SWE-bench methodology and platform setup | Cut | Research-only. |

## 12. Candidate Compact Draft

```markdown
### 1. Select The Issue

[R1] Before Context Intake, select exactly one issue-equivalent item.

[R2] A queue, project, PRD, spec, batch, list, or bare source path is not
implementation scope until one ready issue-equivalent item is named.

[R3] If the user provides a PRD, spec, source document, or path without one
ready item, ask for the target item or route to `to-issues`.

[R4] No one issue-equivalent item, no implementation.

[A1] Use an explicit user target or repo-visible ready/order policy; do not
invent priority or readiness.

[A2] If multiple eligible items remain unordered, ask for the user choice or
repo order.

[A3] If no ready item exists on the checked surface, stop and report that
surface.

[A4] Use repo tracker docs for ready labels, ordering, state, and dependency
syntax; do not edit tracker metadata here.

[L1] Run a local readiness recheck: agent-prompt adequacy, observable done
signal, blocker/dependency state, and result-defining ambiguity.

[L2] Agent-prompt adequacy means the item can guide a fresh coding agent into
Context Intake without issue repair.

[L3] Observable done signal means the item names an expected behavior, repro,
doc target, validation hint, or done condition; it does not require a proof
plan yet.

[L4] Blocked work waits unless the selected item is the blocker or repo-visible
order confirms this item should be worked now.

[L5] Ask only after naming the missing fact and how it would change the
expected result.

[L6] No prompt adequacy, done signal, clear blocker state, or ambiguity result,
no pickup.

[O1] Detect unready work; do not make it ready inside `implement`: no repair,
relabeling, splitting, promotion, reprioritization, rewriting, or tracker-state
mutation.

[O2] If the candidate contains multiple independent outcomes, items, or
unrelated surfaces, ask for one coherent ready item or hand off upstream; do
not split it here.

[H1] Record selected item identity, checked surface, selection authority,
readiness facts, and branch outcomes.

[H2] Select first, plan later: no file discovery, implementation planning,
proof strategy, or edits until selection facts are recorded.

[H3] Start Context Intake only after the `H1` selection facts are recorded.
```

## 13. Detailed Skill-Context Draft Handoff

Candidate-draft decision: `ready-for-detailed-skill-context-draft`

Lines already cut or moved out of runtime:

- `A5`, `O5`, `H4`, and `S2` are cut because they were duplicate/meta lines.
- `L7` and `O4` move to support because they duplicate the handoff or
  bundle neighboring owners.
- `O3` moves to support/pointer-only because repo docs and the engineering
  contract own high-risk policy.

Lines most likely to duplicate another skill or contract:

- `R3`, if it starts decomposing PRDs/specs instead of routing to `to-issues`;
- `O1`, if it teaches issue repair by listing too many forbidden operations;
- `O2`, if it becomes a slicing workflow instead of a narrow/handoff smell;
- `O3`, if Prompt 09 tries to bring it back inline as risk policy instead of a
  pointer/support line;
- `H2`, if it restates Context Intake too broadly.

Line IDs whose placement or runtime weight is most uncertain:

- `A4`, because tracker-doc references already appear in preconditions and
  existing selection text;
- `L6`, because the blunt readiness gate may be redundant after `L1` through
  `L5`;
- `O2`, because Bounded Slice Control may own most size behavior;
- `O3`, because validation may show a tiny pointer is useful or unnecessary;
- `O4`, because it is useful as support but too broad for runtime.

Gates most likely to be too weak:

- `R1` without revised `R2` through `R4`;
- `A1` if "repo-visible ready/order policy" is not tied to tracker docs;
- `L1` if the four readiness facts are not kept visible;
- `L5` if it stops naming the missing fact and result effect;
- `H1` if it records only a title instead of authority and readiness facts.

Gates most likely to be too heavy:

- `L2`, if it requires exact files or design before Context Intake;
- `L3`, if it requires a proof plan;
- `O1`, if the forbidden-operation list bloats runtime;
- `O2`, if it rejects normal bounded implementation questions;
- `O3`, if it returns inline and creates universal risk thresholds.

Context-pointer decisions to preserve or defer:

- whether `A4` should stay inline or be absorbed into existing preconditions;
- whether a future support/examples doc is needed for `agent-prompt adequacy`
  and done-signal examples;
- whether high-risk pickup needs a pointer at all after validation;
- whether source-process rationale should stay entirely out of runtime.

Existing skill behavior that must not regress:

- `implement` still selects and implements one ready-for-agent issue;
- it still stops after one issue;
- it still respects existing tracker docs and local tracker mappings;
- it still asks when ready order is ambiguous;
- it still stops when no issue is available;
- it still proceeds to baseline, Context Intake, implementation, proof,
  review, commit, and issue note after selection;
- it still avoids changing issue state unless requested or repo-defined.

Validation-draft tasks to remember:

- Prompt 09 should verify every must-runtime gate remains checkable.
- Prompt 09 should reject any collapse into "pick a ready issue" or "ask if
  unsure".
- Prompt 09 should verify valid explicit path targets and path-backed ready
  slices still pass `R2`.
- Prompt 09 should verify `L6` is present in both the runtime-step inventory
  and assembled candidate runtime draft block.
- Prompt 09 should preserve enough detail to check duplication against
  `triage`, `to-issues`, Context
  Intake, Bounded Slice Control, Semantic Proof, Review And Lock, tracker docs,
  and the engineering contract.
- Prompt 09 should carry revised `O2` as validation-visible detail and keep
  `O3` support/pointer-only unless placement requires it.
- Prompt 09 should check whether line IDs remain stable enough for a feedback
  loop.
