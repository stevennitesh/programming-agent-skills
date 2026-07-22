# Prompt 08: Candidate Runtime Draft For Implement Facet 1

Historical source-to-skill Prompt 08 artifact for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet or scope: `1 - Ready Issue Selection`

Full behavior synthesis artifact(s):
[`07-full-behavior-synthesis.md`](07-full-behavior-synthesis.md)

Synthesis decision: `ready-for-candidate-runtime-draft`

Behavior flow artifact(s):
[`06-agent-bridge.md`](06-agent-bridge.md)

Existing skill text to preserve: `skills/custom/implement/SKILL.md`,
especially the current description, "Implement one ready-for-agent issue. Stop
after one issue.", issue selection, preconditions, Context Intake, bounded
slice behavior, proof/review/commit/note flow, and the rule against issue state
changes unless requested or repo-defined.

Relevant owners to preserve:

- Engineering contract: `docs/agents/engineering-contract.md`
- Tracker docs: `docs/agents/issue-tracker.md`,
  `docs/agents/triage-labels.md`
- Related skills: `to-tickets`, `triage`, `review`,
  `convergent-pr-review`, `tdd`
- Later `implement` steps: Capture Baseline, Context Intake, Choose And
  Implement, Prove And Simplify, Converge, Lock
- Support docs: future examples/rationale only; no support doc is created here

Revision feedback:

- Rerun Prompt 08 from the refreshed Prompt 07 synthesis.
- Use current 14-section Prompt 08 schema.
- Keep stable R/A/L/O/H line IDs where possible.
- Add the missing owner-boundary scan.
- Replace old audit labels with current draft labels.
- Preserve Prompt 07's tracker-state eligibility and explicit-target
  no-substitution gate.
- Use three subagents to check schema, runtime line quality, and owner/context
  pointer risks.

Subagent inputs used:

- Schema pass: rename sections to current Prompt 08 terms, add Owner Boundary
  Scan, use `Draft Risk`, `Validation Detail`, and current handoff labels.
- Runtime line pass: keep most R/A/L/O/H IDs stable, preserve `L6`, and make
  tracker eligibility/no-substitution explicit in `A4`.
- Owner/context pass: keep source decomposition in `to-tickets`, tracker syntax
  in tracker docs, risk policy in the engineering contract, and Context Intake
  after selection facts are recorded.

Do not edit `SKILL.md` in this prompt.

## 1. Candidate Draft Scope

This draft covers Facet 1, `Ready Issue Selection`, for the `implement` skill.

Full behavior synthesis input used:

- [`07-full-behavior-synthesis.md`](07-full-behavior-synthesis.md)
- [`06-agent-bridge.md`](06-agent-bridge.md)
- existing `skills/custom/implement/SKILL.md`
- repo owner docs listed in Prompt Inputs

Prompt 07 synthesis decision used:

- `ready-for-candidate-runtime-draft`

Existing skill text that must be preserved:

- `implement` invokes on one ready-for-agent issue;
- the agent stops after one issue;
- if no issue is provided, it uses repo-visible tracker docs and ready labels;
- ambiguous ready ordering asks the user;
- unavailable ready work stops;
- baseline capture, Context Intake, bounded implementation, proof, review,
  commit, and issue note remain later steps;
- issue state changes happen only when requested or repo-defined.

Behavior this draft must make predictable:

- before Context Intake, select exactly one issue-equivalent item with visible
  authority, tracker eligibility when relevant, compact readiness facts, and a
  recorded selection boundary; otherwise stop, ask, narrow, or hand off.

This draft must not decide:

- final runtime prose;
- `SKILL.md` edits;
- support-doc creation;
- source-document decomposition;
- issue creation, repair, splitting, promotion, relabeling, or state mutation;
- exact tracker command syntax;
- exact high-risk policy;
- implementation planning, proof strategy, review, commit, or issue notes.

## 2. Prompt 07 Handoff Check

| Handoff Item | Prompt 07 Direction | Step 08 Disposition | Risk For Prompt 09 |
| --- | --- | --- | --- |
| Synthesis decision | `ready-for-candidate-runtime-draft` | Continue to candidate runtime drafting. | None if this label remains explicit. |
| One selected issue-equivalent item | Preserve as the core selection output. | `R1`, `R4`, and `R5` make it the opening hard gate. | "Ready issue" could erase non-GitHub issue forms or source-surface checks. |
| Source documents and paths | A PRD/spec/path is not implementation scope until one ready item is named. | `R2` and `R3` block bare source surfaces while preserving path-backed ready slices in `R5`. | Prompt 09 must not overblock explicit path targets. |
| Selection authority | Use repo-visible ordering or explicit user target; do not invent priority. | `A1` through `A3` keep priority user/repo-owned. | "Best" or "suitable" would hide invented priority. |
| Tracker-state eligibility | Tracker items need eligible ready state before pickup. | `A4` makes eligibility a runtime gate and points exact syntax to tracker docs. | If folded into generic readiness, explicit targets may bypass tracker state. |
| Explicit-target no-substitution | Named but ineligible target stops on that target. | `A4` says no silent substitution and no tracker metadata edits. | Agent may quietly choose another issue after a named item fails. |
| Local readiness recheck | Preserve prompt adequacy, done signal, blocker/dependency state, and result-defining ambiguity. | `L1` through `L6` keep all four sub-gates visible. | "Confirm readiness" would hide the real checks. |
| Agent-prompt adequacy | Keep fresh-agent usability visible. | `L2` preserves the meaning without requiring full context. | Could drift into Context Intake if it asks for files/design. |
| Observable done signal | Preserve without becoming proof strategy. | `L3` keeps this as a selection gate, not a proof plan. | Could duplicate Semantic Proof if expanded. |
| Blocker/dependency check | Detect blockers; tracker docs own syntax and mutation. | `L4` handles dependency order; `A4` handles tracker pointer. | Could drift into tracker metadata editing. |
| Result-defining ambiguity | Ask only when missing information changes expected result. | `L5` requires naming the missing fact and result effect. | Generic "ask if unsure" would create timid over-asking. |
| No-ready stop | Stop and report checked surface. | `A3` preserves no-ready behavior. | Could silently route into issue creation. |
| PRD/spec stop | Ask for target or route upstream. | `R3` routes without decomposing. | Could duplicate `to-tickets` if it starts authoring issues. |
| Owner-boundary stop | Detect unready work; do not repair it. | `O1` is the runtime guard; owner details are in Section 4. | Could duplicate `triage`, `to-tickets`, or tracker docs if expanded. |
| Risk-domain confirmation | Keep short; repo docs own exact policy. | `O3` stays support/pointer-only. | Inline risk policy would bloat runtime. |
| Obvious multi-issue smell | Optional narrow/handoff branch; do not slice here. | `O2` remains validation-visible detail. | Could duplicate Bounded Slice Control or `to-tickets`. |
| Select first, plan later | Record selection facts before Context Intake. | `H1` through `H3` preserve the handoff boundary. | Could collapse into planning, file discovery, proof, or edits. |
| Support-only material | WIP, DoR, INVEST, Scrum, Small CLs, and source examples move out of runtime. | Cut or support-only in Sections 10-12. | Source vocabulary could bloat runtime. |
| Research-only material | Kanban metrics, Scrum ceremonies, SWE-bench scoring, platform setup, detailed splitting stay out. | Cut in Section 12. | Runtime could become a research summary. |
| Design questions | Risk and multi-issue branches are short; exact tracker/risk policy deferred. | `O2` is candidate runtime; `O3` is support-only. | Prompt 09 must decide if either line is still too heavy. |

## 3. Revision Feedback Disposition

| Feedback Item | Affected Line IDs Or Sections | Step 08 Action | Remaining Draft Risk |
| --- | --- | --- | --- |
| Current Prompt 08 schema requires 14 named sections. | Whole artifact | Rebuilt around current section names, including `Owner Boundary Scan`, `Candidate Runtime Draft`, and `Detailed Draft Handoff`. | Prompt 09 should consume current section names only. |
| Add Owner Boundary Scan. | Section 4 | Added owner table before candidate drafting principles. | Owner scan is lightweight; Prompt 09 still owns placement assembly. |
| Replace old audit terminology. | Sections 8 and 11 | Used `Draft Risk` and `Validation Detail`. | None if future prompts keep current labels. |
| Preserve stable runtime IDs. | Sections 7-13 | Kept R/A/L/O/H IDs. `A4` was revised in place instead of adding a new ID. | `A4` is denser than before; Prompt 09 may split it only if stable-ID feedback records the change. |
| `R2` overblocked valid path targets in earlier feedback. | `R2`, `R3`, `R5` | Kept "bare source path" nuance and `R5` path-backed ready slice example. | Prompt 09 should verify valid explicit path targets still pass. |
| `L5` needed non-generic ask wording. | `L5` | Kept missing-fact plus result-effect requirement. | Could become too heavy if applied to ordinary implementation unknowns. |
| `O2` must not become slicing. | `O2` | Kept multiple independent outcomes/items/surfaces wording and upstream handoff. | Prompt 09 should keep it validation-visible rather than a slicing procedure. |
| `L6` was previously missing from assembled candidate block. | `L6`, Section 13 | Included `L6` in candidate runtime steps, inventory, gate consequences, minimal runtime core, and assembled draft. | Prompt 09 should confirm it remains checkable if merged. |
| Prompt 07 added tracker-state eligibility and explicit-target no-substitution. | `A4`, Sections 8-13 | Revised `A4` to explicitly preserve both. | This is the highest-risk line if compressed too far. |

Line ID changes: none. Existing IDs were preserved, revised, demoted, or cut in
place.

## 4. Owner Boundary Scan

| Owner | Owned Behavior | Step 08 May Draft | Step 08 Must Not Draft | Candidate Impact |
| --- | --- | --- | --- | --- |
| Existing `implement` selection section | One issue, ambiguous ordering ask, no-ready stop, dependency order. | Stronger candidate selection gates before Context Intake. | Change invocation scope or final `SKILL.md` wording here. | Preserve current one-issue behavior while making false-ready stops explicit. |
| Existing `implement` later steps | Baseline, Context Intake, bounded implementation, proof, review, commit, note. | Handoff line that says selection facts precede Context Intake. | File discovery, implementation planning, proof strategy, review, commit, or issue-note behavior. | `H1`-`H3` stop at selection facts. |
| Engineering contract | Commitment boundaries, high-risk/security/privacy posture, proof and convergence discipline. | Short pointer for risk boundaries if validation needs it. | Define universal risk thresholds or proof strategy. | `O3` stays support-only. |
| Tracker docs | GitHub issue operations, ready labels, ordering, state, dependency syntax. | Point to tracker docs for exact labels, state, order, and dependency syntax. | Inline `gh` commands, mutate labels/state, or define tracker-specific semantics here. | `A4` is runtime behavior plus pointer, not a tracker procedure. |
| Triage labels | Actual state-role labels such as `ready-for-agent`, `needs-info`, `ready-for-human`, and `wontfix`. | Use the idea of eligible tracker state. | Reproduce or edit label tables. | `A4` keeps syntax repo-owned. |
| `triage` | Make issues ready, request info, classify labels/state. | Detect unready work and hand off. | Repair prompts, promote readiness, relabel, or rewrite issue briefs. | `O1` blocks repair inside `implement`. |
| `to-tickets` | Turn PRDs/specs/plans into ready issue slices. | Route source documents that lack one ready item. | Decompose PRDs/specs or author new issues. | `R3` is route-only. |
| Bounded Slice Control / later implement scope control | Detailed size/slice management after selection. | Detect obvious multi-issue smell before pickup. | Split or plan the work here. | `O2` remains validation detail. |
| Semantic Proof / `$tdd` | Proof strategy and red-green-refactor once behavior is selected. | Require a done signal before pickup. | Demand proof plan or test design during selection. | `L3` avoids proof planning. |
| User / product owner | Product priority, result-defining missing facts, explicit target choice. | Ask on unordered candidates, ambiguity, blocker order, or ineligible named target. | Invent priority or silently replace explicit targets. | `A1`, `A2`, `A4`, and `L5` keep authority visible. |

## 5. Candidate Drafting Principles

Strong leading words to preserve:

- `one selected issue-equivalent item`;
- `repo-visible ordering or explicit user target`;
- `tracker-state eligibility`;
- `explicit-target no-substitution`;
- `selection authority`;
- `local readiness recheck`;
- `agent-prompt adequacy`;
- `observable done signal`;
- `blocker/dependency state`;
- `result-defining ambiguity`;
- `detect unready work; do not make it ready`;
- `select first, plan later`.

Explanatory prose to cut:

- why one active item improves flow;
- why source documents can be too broad;
- why issue quality matters for agents;
- detailed rationale for WIP, DoR, INVEST, Scrum, SWE-bench, or Small CLs;
- examples of every possible tracker shape.

Belongs behind context pointers:

- exact ready labels, state names, ordering fields, dependency syntax, and local
  tracker mappings;
- repo-specific sensitive or high-risk policy;
- support examples for borderline agent-prompt adequacy and done-signal checks;
- source-process rationale, if future maintainers need it.

Gates and consequences must remain checkable:

- No one issue-equivalent item, no implementation.
- No visible authority, no selection.
- No eligible tracker state, no pickup.
- Named but ineligible target stops on that target.
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

Do not convert this wording to final plain language here. Prompt 10 owns that
pass.

## 6. Candidate Invocation / Description Wording

No invocation wording change proposed.

The existing description already says `implement` picks up one ready-for-agent
issue, implements it, verifies it, reviews it, commits it, and leaves a note.
This facet changes runtime selection behavior after invocation, not the trigger
surface.

Risk to preserve: the current description says "one ready-for-agent issue"
rather than "one issue-equivalent item." Prompt 09 should check whether runtime
lines are enough to cover URLs, tracker items, and path-backed ready slices
without broadening invocation.

## 7. Candidate Runtime Steps

### Select One Item

[R1] Before Context Intake, select exactly one issue-equivalent item.

[R2] A queue, project, PRD, spec, batch, list, or bare source path is not
implementation scope until one ready issue-equivalent item is named.

[R3] If the user provides a PRD, spec, source document, or path without one
ready item, ask for the target item or route to `to-tickets`.

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

[A4] For tracker items, confirm tracker-state eligibility through repo tracker
docs; if an explicit target is not eligible, stop on that target without silent
substitution or tracker metadata edits.

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
tracker eligibility when relevant, readiness facts, and branch outcomes.

[H2] Select first, plan later: no file discovery, implementation planning,
proof strategy, or edits until selection facts are recorded.

[H3] Start Context Intake only after the `H1` selection facts are recorded.

## 8. Candidate Line Inventory And Placement

| Line ID | Candidate Line | Function | Placement / Merge Target | Prompt 07 Source | Runtime Weight | Draft Risk |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Before Context Intake, select exactly one issue-equivalent item. | step | replace/merge with `### 1. Select The Issue` opening | one selected issue-equivalent item | must-runtime | Could be too abstract without R5 examples. |
| R2 | A queue, project, PRD, spec, batch, list, or bare source path is not implementation scope until one ready issue-equivalent item is named. | hard gate | insert near selection opening | PRD/spec/path not scope | must-runtime | Must not overblock explicit path targets or path-backed ready slices. |
| R3 | If source document/path lacks one ready item, ask or route to `to-tickets`. | stop/ask rule | merge with existing PRD/spec sentence | PRD/spec stop | must-runtime | Could duplicate `to-tickets` if it says how to decompose. |
| R4 | No one issue-equivalent item, no implementation. | hard gate | insert | blunt gate | must-runtime | Could sound harsh but useful. |
| R5 | Done when one concrete issue-equivalent item is named. | completion criterion | insert or merge with R1/R4 | selection completion | candidate-runtime | Examples must not widen into a batch. |
| A1 | Use explicit user target or repo-visible ready/order policy. | hard gate | replace broad "choose next" wording | selection authority | must-runtime | Weak if "repo-visible" is not tied to tracker docs. |
| A2 | Multiple unordered eligible items ask user/order source. | stop/ask rule | keep/strengthen existing ambiguous order line | multiple-candidate branch | must-runtime | Good as-is; check duplicate risk against current text. |
| A3 | No ready item stops and reports checked surface. | stop/ask rule | keep/strengthen existing no issue line | no-ready stop | must-runtime | Could become too much reporting if verbose. |
| A4 | Tracker items need eligible state; explicit ineligible targets stop without substitution or metadata edits. | hard gate / context pointer | replace tracker-doc pointer and strengthen preconditions | tracker-state eligibility, explicit-target no-substitution | must-runtime | Densest line; Prompt 09 may split behavior from pointer if needed. |
| L1 | Run local readiness recheck with four named facts. | recheck | insert after authority | local readiness recheck | must-runtime | Must not become full triage checklist. |
| L2 | Agent-prompt adequacy guides fresh coding agent into Context Intake. | recheck | insert under readiness | agent-prompt adequacy | must-runtime | Could require full context if phrased poorly. |
| L3 | Observable done signal exists without proof plan. | recheck | insert under readiness | observable done signal | must-runtime | Could duplicate Semantic Proof if expanded. |
| L4 | Blocked work waits unless selected item is blocker/order confirmed. | hard gate | replace/strengthen existing blockers line | blocker/dependency check | must-runtime | Needs tracker syntax pointer elsewhere. |
| L5 | Ask only after naming the missing fact and how it would change the expected result. | stop/ask rule | merge with later ask/commitment boundary | result-defining ambiguity | must-runtime | Could become too heavy if ordinary implementation unknowns block selection. |
| L6 | No readiness facts, no pickup. | hard gate | insert or merge with L1-L5 | blunt readiness gate | must-runtime | Slightly dense; Prompt 09 should check readability. |
| L7 | Readiness facts recorded without Context Intake/proof/repair. | completion criterion | defer to support | select first, plan later | support-only | Duplicates H1/H2. |
| O1 | Detect unready work; do not make it ready inside `implement`. | ownership guard | insert near selection/readiness | owner-boundary stop | must-runtime | Forbidden-operation examples may bloat final runtime. |
| O2 | Multiple independent outcomes, items, or unrelated surfaces ask or hand off; do not split here. | stop/ask rule | insert if kept | obvious multi-issue smell | candidate-runtime | Could duplicate Bounded Slice Control if expanded. |
| O3 | Use repo docs or engineering contract for high-risk pickup boundaries. | context pointer | defer to support | risk-domain confirmation | support-only | Could duplicate engineering contract if kept inline. |
| O4 | Stop/handoff for neighboring owners. | ownership guard | defer to support / owner scan | owner conflicts | support-only | Useful support checklist, too broad for runtime. |
| O5 | Done when owner-owned work was not repaired inside selection. | completion criterion | cut | owner-boundary completion | likely-prune | Meta duplicate. |
| H1 | Record selected item identity, checked surface, authority, eligibility/readiness facts, and branch outcomes. | handoff | insert before Context Intake handoff | selection facts | must-runtime | Must remain selection facts, not plan. |
| H2 | Select first, plan later. | hard gate | insert | select first, plan later | must-runtime | Strong; check duplication with Context Intake. |
| H3 | Start Context Intake only after the `H1` selection facts are recorded. | handoff | insert/merge | Context Intake handoff | candidate-runtime | Could duplicate H1/H2 if overexplained. |
| H4 | Done when Context Intake has one selected item and recorded facts. | completion criterion | cut | handoff completion | likely-prune | Redundant wrapper. |

## 9. Candidate Gate Consequences

| Line ID | Candidate Line | Purpose | Failure Prevented |
| --- | --- | --- | --- |
| R4 | No one issue-equivalent item, no implementation. | Keep the run singular. | Batch, queue, PRD, project, or vague request becomes scope. |
| A1 | Use explicit user target or repo-visible ready/order policy; do not invent priority or readiness. | Preserve authority. | Agent chooses by taste or convenience. |
| A2 | If multiple eligible items remain unordered, ask for the user choice or repo order. | Keep priority user/repo-owned. | Hidden prioritization. |
| A3 | If no ready item exists on the checked surface, stop and report that surface. | Stop busywork. | Agent creates or repairs work inside `implement`. |
| A4 | For tracker items, confirm tracker-state eligibility; if explicit target is not eligible, stop on that target without silent substitution. | Preserve ready state and explicit target authority. | Closed, needs-info, human-owned, rejected, or otherwise ineligible work starts, or the agent silently chooses another item. |
| L1 | Run a local readiness recheck with four named facts. | Prevent label-only pickup. | Work starts from an unusable issue. |
| L4 | Blocked work waits unless selected item is the blocker or repo-visible order confirms this item should be worked now. | Preserve dependency order. | Work starts behind an unresolved blocker. |
| L5 | Ask only after naming the missing fact and how it would change the expected result. | Avoid invented requirements without timid asking. | Generic uncertainty blocks ordinary implementation. |
| L6 | No prompt adequacy, done signal, clear blocker state, or ambiguity result, no pickup. | Make readiness blunt. | Prompt-poor or unverifiable work starts. |
| O1 | Detect unready work; do not make it ready inside `implement`. | Preserve owner boundaries. | `implement` becomes `triage` or `to-tickets`. |
| O2 | If the candidate has multiple independent outcomes/items/surfaces, ask or hand off; do not split here. | Catch non-singular scope. | Selection becomes decomposition or broad implementation. |
| H2 | Select first, plan later: no file discovery, implementation planning, proof strategy, or edits until selection facts are recorded. | Preserve phase boundary. | Selection collapses into Context Intake or coding. |

## 10. Context Pointer Candidates

| Line ID | Pointer Text | Target Support Doc | Why It Should Be Disclosed | When Agent Should Open It |
| --- | --- | --- | --- | --- |
| A4 | Use repo tracker docs for ready labels, ordering, state, and dependency syntax. | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, repo-local tracker docs | Exact tracker semantics are repo-owned and changeable. | When selection depends on ready labels, ordering, blockers, state roles, or local tracker mappings. |
| O3 | Use repo docs or the engineering contract for high-risk pickup boundaries. | `docs/agents/engineering-contract.md`, repo policy docs | Runtime should not define a universal risk policy. | When validation shows high-risk pickup is otherwise missed. |
| S1 | See support examples for agent-prompt adequacy and done-signal checks. | Future implement support/examples doc | Borderline readiness examples may help without bloating runtime. | When an item is not clearly prompt-poor but the readiness check is uncertain. |
| S2 | Source rationale for pull/WIP and DoR contrast lives in support. | Future synthesis/support rationale, if created | Explains why the gate exists without turning runtime into process theory. | Maintainer context only, not normal runtime. |

## 11. Minimal Runtime Core

| Line ID | Runtime Core / Validation Detail / Support / Cut | Why |
| --- | --- | --- |
| R1 | Runtime Core | Names the first phase output. |
| R2 | Runtime Core | Blocks broad source surfaces without rejecting path-backed ready work. |
| R3 | Runtime Core | Keeps PRD/spec/path handoff explicit. |
| R4 | Runtime Core | Blunt singularity gate. |
| R5 | Validation Detail | Useful completion criterion; may compress into R1/R4. |
| A1 | Runtime Core | Prevents invented priority/readiness. |
| A2 | Runtime Core | Preserves user/repo priority owner. |
| A3 | Runtime Core | Prevents busywork when no ready item exists. |
| A4 | Runtime Core | Preserves tracker-state eligibility, no-substitution, tracker-doc pointer, and no metadata mutation. |
| L1 | Runtime Core | Names compact readiness facts. |
| L2 | Validation Detail | Preserves agent-prompt adequacy; may merge under L1. |
| L3 | Validation Detail | Preserves done signal without proof plan; may merge under L1. |
| L4 | Runtime Core | Preserves dependency discipline. |
| L5 | Runtime Core | Preserves result-defining ambiguity branch. |
| L6 | Validation Detail | Blunt gate; may merge with L1-L5. |
| L7 | Support | Handoff check duplicates H1-H2. |
| O1 | Runtime Core | Hard owner boundary; final prune should compress examples. |
| O2 | Validation Detail | Useful optional smell; Prompt 09 should check duplication with Bounded Slice Control. |
| O3 | Support | Risk policy belongs to repo docs / engineering contract. |
| O4 | Support | Good support checklist, too broad for final runtime. |
| O5 | Cut | Meta completion line likely unnecessary. |
| H1 | Runtime Core | Records handoff facts. |
| H2 | Runtime Core | Prevents premature planning. |
| H3 | Validation Detail | Names the Context Intake handoff gate; may merge into H1/H2. |
| H4 | Cut | Redundant with H1-H3. |
| S1 | Support | Future examples only. |
| S2 | Cut | Rationale is not needed in runtime. |

## 12. Cut / Preserve Log

| Material | Cut / Preserve / Move | Why |
| --- | --- | --- |
| One selected issue-equivalent item | Preserve | Core facet output. |
| Queue/project/PRD/spec/bare source path not scope until one item named | Preserve | Prevents broad-source drift without blocking path-backed ready work. |
| Repo-visible order or explicit user target | Preserve | Selection authority is user/repo-owned. |
| Tracker-state eligibility | Preserve | Explicit target does not bypass ready state. |
| Explicit-target no-substitution | Preserve | Named-but-ineligible work must fail visibly. |
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
| Issue repair/relabel/split/promote/rewrite | Preserve as prohibited behavior | Protects `triage`, `to-tickets`, and tracker owners. |
| Risk-domain confirmation | Move | Useful guard, but exact policy belongs elsewhere. |
| Obvious multi-issue smell | Preserve as validation detail | Useful rejection when tied to multiple independent outcomes/items/surfaces; slicing belongs elsewhere. |
| Select first, plan later | Preserve | Protects Context Intake boundary. |
| File discovery/planning/proof/editing | Preserve as prohibited behavior before handoff | Prevents phase collapse. |
| Kanban/WIP/DoR/INVEST/Scrum/Small CL source terms | Move or cut | Support rationale only. |
| SWE-bench methodology and platform setup | Cut | Research-only. |

## 13. Candidate Runtime Draft

```markdown
### 1. Select The Issue

[R1] Before Context Intake, select exactly one issue-equivalent item.

[R2] A queue, project, PRD, spec, batch, list, or bare source path is not
implementation scope until one ready issue-equivalent item is named.

[R3] If the user provides a PRD, spec, source document, or path without one
ready item, ask for the target item or route to `to-tickets`.

[R4] No one issue-equivalent item, no implementation.

[A1] Use an explicit user target or repo-visible ready/order policy; do not
invent priority or readiness.

[A2] If multiple eligible items remain unordered, ask for the user choice or
repo order.

[A3] If no ready item exists on the checked surface, stop and report that
surface.

[A4] For tracker items, confirm tracker-state eligibility through repo tracker
docs; if an explicit target is not eligible, stop on that target without silent
substitution or tracker metadata edits.

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
tracker eligibility when relevant, readiness facts, and branch outcomes.

[H2] Select first, plan later: no file discovery, implementation planning,
proof strategy, or edits until selection facts are recorded.

[H3] Start Context Intake only after the `H1` selection facts are recorded.
```

## 14. Detailed Draft Handoff

candidate-draft decision: `ready-for-detailed-skill-context-draft`

Lines most likely to be no-ops:

- `R4`, if Prompt 09 preserves the same consequence clearly in `R1`;
- `L6`, if all four `L1` readiness sub-gates keep explicit failure
  consequences;
- `H3`, if `H1` and `H2` already make the Context Intake boundary checkable.

Lines most likely to duplicate another skill or contract:

- `R3`, if it starts decomposing PRDs/specs instead of routing to `to-tickets`;
- `A4`, if it reproduces tracker label tables or command syntax;
- `O1`, if it teaches issue repair by listing too many forbidden operations;
- `O2`, if it becomes a slicing workflow instead of a narrow/handoff smell;
- `O3`, if Prompt 09 tries to bring it back inline as risk policy;
- `H2`, if it restates Context Intake too broadly.

Line IDs whose placement or runtime weight is most uncertain:

- `R5`, because it may merge into `R1`/`R4`;
- `A4`, because it carries both runtime eligibility and tracker-doc pointer
  behavior;
- `L6`, because the blunt readiness gate may be redundant after `L1` through
  `L5`;
- `O2`, because Bounded Slice Control may own most size behavior;
- `O3`, because validation may show a tiny pointer is useful or unnecessary;
- `H3`, because it may merge into the selection-boundary lines.

Owner conflicts or owner-boundary risks:

- `R3` must route to `to-tickets` without decomposing source documents.
- `A4` must check eligibility without editing tracker metadata or inlining
  tracker commands.
- `O1` must detect unready work without becoming `triage`.
- `O2` must reject broad work without slicing it.
- `L2`/`L3` must stay before Context Intake and Semantic Proof.
- `H1`-`H3` must record selection facts, not a plan.

Gates most likely to be too weak:

- `R1` without `R2` through `R4`;
- `A1` if "repo-visible ready/order policy" is not tied to tracker docs;
- `A4` if tracker-state eligibility or no-substitution is compressed away;
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

- preserve `A4` as the tracker-doc pointer unless Prompt 09 finds the existing
  preconditions already cover syntax;
- defer a future support/examples doc for agent-prompt adequacy and done-signal
  examples;
- keep high-risk pickup policy in the engineering contract or repo docs unless
  validation proves a tiny pointer is necessary;
- keep source-process rationale out of runtime.

Existing skill behavior that must not regress:

- `implement` still selects and implements one ready-for-agent issue;
- it still stops after one issue;
- it still respects existing tracker docs and local tracker mappings;
- it still asks when ready order is ambiguous;
- it still stops when no issue is available;
- it still proceeds to baseline, Context Intake, implementation, proof,
  review, commit, and issue note after selection;
- it still avoids changing issue state unless requested or repo-defined.

Validation scenario seeds to remember:

- explicit named issue is eligible and proceeds;
- explicit named issue is ineligible and stops without substitution;
- no issue provided and exactly one next unblocked `ready-for-agent` item
  exists;
- multiple eligible items exist with no visible order;
- PRD/spec/path lacks one ready issue-equivalent item;
- explicit path target or path-backed ready slice is valid and should pass;
- ready-labeled item is prompt-poor or lacks a done signal;
- candidate has an unresolved blocker;
- candidate has result-defining ambiguity;
- candidate is obviously multi-issue or high risk;
- selection facts are recorded before Context Intake or planning.
