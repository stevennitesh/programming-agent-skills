# Prompt 06: Agent Bridge For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/06-agent-bridge.md`](../../../methods/prompts/06-agent-bridge.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Facet research question: How should `implement` select exactly one ready issue
or stop when no safe issue is available?

Facet boundaries:

- Owns: source/candidate resolution, one issue-equivalent selection, selection
  authority, compact readiness recheck, blocker/dependency stop, ambiguity
  stop, no-ready stop, PRD/spec-without-issue handoff, risk confirmation smell,
  and the handoff boundary to Context Intake.
- Does not own: issue creation, issue repair, issue splitting, ready-state
  promotion, tracker metadata mutation, exact tracker syntax, product priority,
  full context intake, implementation planning, proof strategy, review, commit,
  issue notes, or exact sensitive-domain policy.
- Should answer: what the agent does before coding to select one ready
  issue-equivalent item or stop safely.
- Should not answer: how to author the issue, make it ready, decompose a source
  document, design the implementation, prove the change, or close the work.

Source triage packet:
[`docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-triage.md`](../../../../research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-triage.md)

Triage decision: `ready-for-behavior-flow`

Revision feedback:

- Rerun Prompt 06 from the refreshed Prompt 05 triage packet.
- Use three subagents to check behavior sequence, branches / stop rules, and
  duplicate-term / owner-boundary compression.

Subagent inputs used:

- Sequence pass: split the execution chain into source resolution, one-item
  selection, authority check, compact readiness recheck, blocker/dependency,
  prompt adequacy, done signal, ambiguity, risk/size, and selection boundary.
- Branch pass: keep branches specific to no-ready, multiple candidates,
  PRD/spec without issue, readiness repair, blocker/dependency, ambiguity,
  prompt-poor/no-done-signal, risk, multi-issue smell, and premature planning.
- Boundary/compression pass: use primary behavior terms from Prompt 05 and keep
  source vocabulary such as WIP, DoR, INVEST, Scrum, and Small CLs in support.

## 1. Agent Bridge Scope

This behavior flow converts the `Ready Issue Selection` triage into an
execution skeleton for the first part of `implement`: selecting exactly one
ready issue-equivalent item or stopping before implementation starts.

Surviving material in scope:

- one selected issue-equivalent item;
- repo-visible ordering or explicit user target;
- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity stop;
- no-ready stop;
- PRD/spec-without-one-issue stop;
- owner-boundary stop;
- risk-domain confirmation;
- obvious multi-issue smell;
- select first, plan later.

Material intentionally left for support/reference:

- Kanban pull/WIP rationale;
- Scrum ready-for-selection rationale;
- Definition of Ready / stage-gate contrast;
- issue-as-prompt examples;
- SWE-bench underspecification rationale;
- tracker dependency examples;
- Small CL reviewability rationale;
- exact tracker commands, state names, labels, and dependency syntax.

This behavior flow must not decide final runtime `SKILL.md` wording, write
generous synthesis prose, create or triage issues, mutate tracker state, perform
Context Intake, plan implementation, design proof, review output, or define
repo-specific high-risk policy.

## 2. Prompt 05 Handoff Check

| Prompt 05 Input | Used / Revised / Deferred / Rejected | Flow Consequence | Notes |
| --- | --- | --- | --- |
| Triage decision: `ready-for-behavior-flow` | Used | Build the ordered execution skeleton. | No return to triage needed. |
| Runtime priority / budget | Used | Must candidates become hard gates or stop branches. | Should/Could items become rechecks, support cues, or optional branches. |
| Bridge resolution plan | Used | Raw source terms become plain behavior terms. | Avoid carrying Kanban, Scrum, DoR, INVEST, or benchmark language into the core flow. |
| Duplicate / synonym collapse choices | Used | Primary terms are one selected issue-equivalent item, repo-visible ordering or explicit user target, local readiness recheck, agent-prompt adequacy, observable done signal, result-defining ambiguity, blocker/dependency check, and select first, plan later. | Source phrases remain support terms. |
| Owner-conflict severities | Used | Hard boundaries become stop/handoff branches. | Especially `to-issues`, `triage`, tracker docs, Context Intake, Bounded Slice Control, Semantic Proof, Review And Lock, and engineering contract. |
| Rejected temptation: full DoR / INVEST | Rejected | Flow does not build a readiness checklist. | Only a compact local readiness recheck survives. |
| Watchpoint: exact tracker semantics | Deferred | Runtime checks blocker/order semantics only. | Repo docs own commands, labels, and metadata edits. |
| Watchpoint: risk-domain confirmation | Revised | Keep as generic confirmation branch. | Engineering contract / repo docs own exact policy. |
| Watchpoint: obvious multi-issue smell | Revised | Keep only as an early stop/narrow branch. | Bounded Slice Control owns detailed sizing and slicing. |

## 3. Priority Preservation Check

| Candidate | Must / Should / Could | Flow Placement | Preserved / Demoted / Dropped | Why |
| --- | --- | --- | --- | --- |
| One selected issue-equivalent item | Must | Steps 1-2 hard gates | Preserved | Core facet output. |
| Repo-visible ordering or explicit user target | Must | Step 3 hard gate | Preserved | Prevents invented priority/readiness authority. |
| Local readiness recheck | Must | Step 4 hard gate | Preserved | Prevents label-only pickup. |
| Agent-prompt adequacy | Must | Step 5 hard gate | Preserved | Tests whether a fresh agent can begin Context Intake. |
| Observable done signal | Must | Step 6 hard gate | Preserved | Prevents unverifiable pickup without designing proof. |
| Blocker/dependency check | Must | Step 7 hard gate | Preserved | Prevents starting blocked work. |
| Multiple-candidate order stop | Must | Branch B1 | Preserved | Priority is not agent-owned. |
| No-ready stop | Must | Branch B2 | Preserved | Preserves `triage` / `to-issues` ownership. |
| PRD/spec without one issue stop | Must | Branch B3 | Preserved | Prevents whole-document implementation scope. |
| Result-defining ambiguity stop | Must | Step 8 and Branch B7 | Preserved | Prevents invented requirements. |
| Owner-boundary stop | Must | Step 10 and Branch B10 | Preserved | Prevents readiness repair, tracker mutation, splitting, or planning. |
| Select first, plan later | Should | Step 10 handoff gate | Preserved | Keeps Context Intake separate. |
| Risk-domain confirmation | Should | Step 9 and Branch B8 | Preserved as recheck | Avoids silent high-risk pickup without defining policy. |
| Obvious multi-issue smell | Could | Branch B4 / Step 9 support recheck | Demoted | Selection catches obvious scope explosions only. |
| Report searched surface when stopping | Could | Branch B2 and completion criteria | Preserved as support behavior | Useful evidence without bloating main path. |

## 4. Runtime Candidate Inventory

| Candidate | Type | Why It Survived | Behavior Role |
| --- | --- | --- | --- |
| One selected issue-equivalent item | behavior rule / evidence gate | Defines the facet's success condition. | Bound the run to one candidate. |
| Repo-visible ordering or explicit user target | evidence gate | Establishes selection authority. | Prevent invented priority or readiness. |
| Local readiness recheck | evidence gate / bridge translation | Catches false readiness without owning `triage`. | Check small pre-context facts. |
| Agent-prompt adequacy | evidence gate / bridge translation | Directly tests agent-task fit. | Reject prompt-poor issues. |
| Observable done signal | evidence gate / bridge translation | Gives later proof a target without designing proof now. | Reject unverifiable pickup. |
| Blocker/dependency check | stop/ask rule / evidence gate | Keeps dependency order intact. | Stop or ask on blocked work. |
| Result-defining ambiguity | stop/ask rule | Prevents invented requirements. | Ask only on missing details that change the result. |
| No-ready stop | stop rule | Keeps `implement` from creating its own work. | Stop when no ready item exists. |
| PRD/spec without one issue | stop/handoff rule | Prevents treating source documents as implementation scope. | Route to `to-issues` or ask for target issue. |
| Owner-boundary stop | stop/handoff rule | Protects neighboring skills/facets. | Route issue repair, splitting, planning, and tracker mutation to owners. |
| Risk-domain confirmation | stop/ask rule | Prevents silent high-risk autonomous pickup. | Ask for explicit boundaries. |
| Obvious multi-issue smell | stop/narrow rule | Catches plainly unsafe scope early. | Ask to narrow or route upstream without slicing. |
| Select first, plan later | behavior rule / handoff | Protects Context Intake boundary. | Record selection facts before planning. |

## 5. Duplicate-Term Resolution

| Behavior Role | Primary Term | Support Terms | Demote / Avoid | Why |
| --- | --- | --- | --- | --- |
| Single-item discipline | One selected issue-equivalent item | pull, WIP, capacity | queue grabbing, start next task | Plain behavior is stronger than process jargon. |
| Selection authority | Repo-visible ordering or explicit user target | ready marker, explicit policies, pull criteria | highest priority, suitable issue | Agent must not invent priority. |
| Readiness | Local readiness recheck | ready for selection, Definition of Ready | full DoR checklist, READY-ready | Runtime needs a small gate. |
| Issue quality | Agent-prompt adequacy | issue as prompt, well-scoped | clear enough, well-defined | Agentic term makes the gate checkable. |
| Success signal | Observable done signal | acceptance criteria, testable, done when | full proof plan | Selection needs a signal, not proof design. |
| Ambiguity | Result-defining ambiguity | underspecified, vague, unclear | ask if unsure | Specific branch avoids timidity. |
| Dependency | Blocker/dependency check | blocked by, blocking, unresolved dependency | tracker-specific syntax, dependency edits | Keeps behavior tracker-neutral. |
| Risk | Risk-domain confirmation | sensitive, consequential, human oversight | full risk policy | Exact policy belongs elsewhere. |
| Size | Obvious multi-issue smell | self-contained, Small CL, INVEST small | slicing strategy | Selection can reject obvious non-issues only. |
| Boundary | Select first, plan later | selectable vs understood, selection-as-planning | implementation planning | Context Intake owns the next phase. |

## 6. Support / Reference Inventory

| Candidate | Why It Belongs In Support | Runtime Pointer Needed? |
| --- | --- | --- |
| Kanban pull/WIP rationale | Explains why one active item matters without importing process ceremony. | Maybe, if support docs are created. |
| Scrum ready-for-selection rationale | Explains selectable versus fully understood. | Maybe, behind selection-boundary support. |
| DoR / stage-gate contrast | Explains why local readiness exists and why it must stay small. | Maybe, behind readiness support. |
| Issue-as-prompt examples | Helps explain agent-prompt adequacy. | Maybe, as examples only. |
| SWE-bench underspecification rationale | Supports result-defining ambiguity as a no-pick condition. | No inline pointer needed. |
| Tracker dependency examples | Help explain blocker/dependency semantics. | Yes, runtime should point to repo tracker docs for exact syntax. |
| Small CL reviewability rationale | Supports obvious multi-issue smell but belongs mostly to Bounded Slice Control. | No for this facet. |
| Exact tracker labels, commands, and dependency fields | Repo-local and changeable. | Yes, use repo tracker docs rather than inline syntax. |

## 7. Behavior Sequence

### Step 1: Resolve Candidate Surface

Trigger / situation:

- `implement` starts and the user may have provided one issue, a URL, a path,
  a PRD/spec, a queue, or no explicit work item.

Agent action:

- Identify the selection surface implied by the request.
- Prefer an explicit user target when it already names one issue-equivalent
  item.
- If no single target is named, inspect only the repo/user-visible ready surface
  needed to find candidates.
- If the input is only a PRD/spec/source document, branch before treating it as
  implementation scope.

Leading words:

- one selected issue-equivalent item;
- repo-visible ordering or explicit user target.

Primary term:

- candidate surface.

Supporting terms:

- pull;
- ready surface.

Evidence gate:

- The run has one candidate source type: explicit user target, repo-visible
  ready/order surface, PRD/spec without one issue, or no ready source.

Gate type:

- hard gate.

Stop / ask / continue rule:

- Continue only when the source can produce one issue-equivalent candidate.
- Branch to PRD/spec handoff when the input is a source document without one
  ready issue-equivalent item.

Failure prevented:

- Treating a whole document, queue, project, or vague request as automatic
  implementation scope.

Source pressure:

- repo-visible ordering or explicit user target;
- PRD/spec without one issue stop.

Ownership severity:

- hard-boundary for source-document decomposition.

Next:

- Step 2, Branch B2, or Branch B3.

### Step 2: Lock One Issue-Equivalent Item

Trigger / situation:

- Candidate surface can yield zero, one, or multiple candidate items.

Agent action:

- Select exactly one candidate when the user named exactly one or repo-visible
  ordering clearly yields one.
- If multiple candidates are eligible and no clear order exists, ask the user
  to choose or provide the ordering source.
- If no ready issue-equivalent item exists, stop and report the checked surface.

Leading words:

- one selected issue-equivalent item;
- repo-visible ordering.

Primary term:

- one selected issue-equivalent item.

Supporting terms:

- pull;
- WIP.

Evidence gate:

- Exactly one issue, URL, tracker item, path-backed ready slice, or explicit
  user-selected work item is named.

Gate type:

- hard gate.

Stop / ask / continue rule:

- Ask on multiple eligible candidates without clear order.
- Stop when no ready issue-equivalent candidate exists.
- Continue only with exactly one concrete candidate.

Failure prevented:

- Batch pickup, queue grabbing, hidden priority decisions, and whole-project
  implementation.

Source pressure:

- one selected issue-equivalent item;
- multiple-candidate order stop;
- no-ready stop.

Ownership severity:

- hard-boundary if no ready work would require issue creation or triage.

Next:

- Step 3, Branch B1, or Branch B2.

### Step 3: Apply Selection Authority

Trigger / situation:

- Exactly one issue-equivalent candidate is named.

Agent action:

- Confirm the candidate is eligible by repo-visible ready/order policy or by
  explicit user target.
- Use repo tracker docs for exact ready labels, ordering fields, state names,
  or dependency syntax.
- Do not promote, relabel, reorder, rewrite, or edit tracker metadata.

Leading words:

- repo-visible ordering or explicit user target.

Primary term:

- selection authority.

Supporting terms:

- ready marker;
- explicit policy.

Evidence gate:

- Candidate has explicit user selection or repo-visible readiness/ordering
  authority with no obvious contradiction.

Gate type:

- hard gate.

Stop / ask / continue rule:

- Continue when authority is clear.
- Stop or hand off if selection would require ready-state promotion, issue
  rewrite, relabeling, priority invention, or tracker mutation.

Failure prevented:

- Invented readiness, invented priority, and upstream takeover.

Source pressure:

- repo-visible ordering or explicit user target;
- owner-boundary stop.

Ownership severity:

- soft-reference to tracker docs;
- hard-boundary for `triage` / tracker mutation.

Next:

- Step 4 or Branch B5.

### Step 4: Run Local Readiness Recheck

Trigger / situation:

- Candidate has selection authority.

Agent action:

- Recheck only the pre-context facts needed before ownership:
  - requested work is visible enough to name;
  - the issue can plausibly guide a fresh coding agent;
  - at least one observable done signal exists;
  - no obvious blocker/dependency prevents pickup;
  - no result-defining ambiguity remains.

Leading words:

- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity.

Primary term:

- local readiness recheck.

Supporting terms:

- ready for selection;
- issue as prompt.

Evidence gate:

- Readiness facts are recorded: prompt adequacy, done signal,
  blocker/dependency state, and ambiguity result.

Gate type:

- hard gate.

Stop / ask / continue rule:

- Continue when all readiness facts pass.
- Ask only when missing detail changes the expected result.
- Stop/skip if blocked unless the selected item is the blocker itself.
- Hand off if the issue needs repair, rewriting, acceptance-criteria repair, or
  ready-state changes.

Failure prevented:

- Label-only readiness, prompt-poor pickup, unverifiable work, dependency-order
  violations, and invented requirements.

Source pressure:

- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity stop.

Ownership severity:

- hard-boundary for `triage` on issue repair;
- later-facet-watchpoint for Context Intake and Semantic Proof.

Next:

- Step 5, Branch B5, Branch B6, Branch B7, or Branch B8.

### Step 5: Check Risk And Size Smells

Trigger / situation:

- Candidate passes the compact local readiness recheck.

Agent action:

- Check for sensitive, critical, consequential, regulated, production-critical,
  security, PII, auth, incident, or deep business-logic signals.
- Check whether the candidate is plainly too broad or multi-issue to be one
  coherent implementation item.
- Do not define risk policy or slice the work here.

Leading words:

- risk-domain confirmation;
- obvious multi-issue smell.

Primary term:

- risk and size recheck.

Supporting terms:

- human oversight;
- self-contained change.

Evidence gate:

- Either no risk confirmation is needed, or user boundaries are explicit.
- Candidate does not plainly require several independent implementation issues.

Gate type:

- recheck.

Stop / ask / continue rule:

- Ask for confirmation and guardrails before high-risk autonomous pickup.
- Ask to narrow or route upstream when the candidate is plainly multi-issue.
- Continue when no risk/size branch is triggered or the branch is resolved.

Failure prevented:

- Silent high-risk pickup and whole-spec implementation.

Source pressure:

- risk-domain confirmation;
- obvious multi-issue smell.

Ownership severity:

- soft-reference for engineering contract / repo docs;
- later-facet-watchpoint for Bounded Slice Control.

Next:

- Step 6, Branch B4, or Branch B9.

### Step 6: Record Selection Boundary

Trigger / situation:

- Exactly one candidate has passed selection authority, local readiness, and
  risk/size rechecks.

Agent action:

- Record only the selection facts:
  - selected issue-equivalent item identity;
  - why it is the one selected item;
  - selection authority;
  - readiness facts checked;
  - any branch resolved or intentionally deferred to the next owner.
- Do not begin implementation planning, file discovery, proof strategy, or code
  edits inside this facet.

Leading words:

- select first, plan later.

Primary term:

- selection boundary.

Supporting terms:

- Context Intake handoff.

Evidence gate:

- The selected item and readiness facts are recorded, and no implementation
  plan or code edit has started.

Gate type:

- handoff.

Stop / ask / continue rule:

- If planning or Context Intake starts before selection facts are recorded,
  stop and complete this boundary first.
- Continue by handing off to Context Intake.

Failure prevented:

- Selection-as-planning, premature Context Intake, and phase collapse.

Source pressure:

- select first, plan later;
- owner-boundary stop.

Ownership severity:

- later-facet-watchpoint for Context Intake.

Next:

- Handoff to Context Intake.

## 8. Branches

| Branch | Trigger | Behavior | Gate | Exit Type | Rejoin / Exit |
| --- | --- | --- | --- | --- | --- |
| B1: Multiple eligible candidates | More than one eligible item and no repo-visible order | Ask user to choose or provide ordering source. | One candidate selected. | ask-user | Rejoin Step 2. |
| B2: No ready item | Checked surface has no ready issue-equivalent item | Stop and report checked surface plus no-ready reason. | Surface named; no item selected. | blocked | Exit facet; route to `triage` / `to-issues` if appropriate. |
| B3: PRD/spec without one issue | User provides source doc, PRD, spec, or path but no ready issue-equivalent item | Ask for target issue or route to `to-issues`. | One ready issue-equivalent item is named. | handoff-skill | Rejoin Step 2 after upstream slice exists. |
| B4: Obvious multi-issue smell | Candidate is broad, multi-slice, or many unrelated areas | Ask to narrow or route upstream; do not slice here. | One coherent issue-equivalent item exists. | ask-user | Rejoin Step 2 or exit to `to-issues` / `triage`. |
| B5: Readiness repair or tracker mutation needed | Selection would require issue rewrite, acceptance-criteria repair, ready-state promotion, relabeling, ordering changes, or dependency metadata edits | Stop and hand off to owner. | Upstream owner makes item ready. | handoff-skill | Exit to `triage`, `to-issues`, or tracker owner; rejoin only after ready issue exists. |
| B6: Blocked candidate | Candidate has an unresolved blocker/dependency and the candidate is not itself the blocker | Stop, skip if repo order clearly identifies an unblocked ready item, or ask whether to work the blocker. | Blocker resolved, order confirmed, or blocker selected. | ask-user | Rejoin Step 2 or Step 4. |
| B7: Result-defining ambiguity | Missing detail would change the expected result | Ask for that specific missing result detail or route upstream. | Missing detail supplied. | ask-user | Rejoin Step 4 or exit to `triage`. |
| B8: Prompt-poor or no done signal | Candidate lacks work/outcome shape or any observable done signal | Stop or route upstream; do not invent the issue brief. | Adequate prompt/done signal exists. | handoff-skill | Exit to `triage`; rejoin only after repair. |
| B9: Risk-domain confirmation | Candidate touches sensitive, critical, regulated, consequential, security, PII, auth, incident, production-critical, or deep business-logic work | Ask for explicit confirmation and boundaries; consult repo policy if available. | User confirms guardrails or selects another issue. | ask-user | Rejoin Step 5 or exit blocked. |
| B10: Premature planning | Agent starts design, file discovery, proof strategy, or code edits before selection facts are recorded | Stop planning and record selection facts only. | Identity/readiness facts complete. | rejoin-flow | Rejoin Step 6 or hand off to Context Intake. |

## 9. Completion Criteria

| Criterion | Gate Type | What It Proves | How Agent Checks It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- |
| Exactly one selected issue-equivalent item is named | hard gate | The facet did not pick a batch, queue, project, or whole document. | Check selected item is singular and concrete. | It names a list, project, PRD, or source document. | It decomposes the source into issues. |
| Selection authority is visible | hard gate | Agent did not invent priority or readiness. | Check explicit user target or repo-visible ready/order source is named. | It says "looks ready." | It edits tracker policy or labels. |
| Local readiness recheck is complete | hard gate | Candidate is safe enough to own before Context Intake. | Check prompt adequacy, done signal, blocker/dependency state, and ambiguity result. | It checks only a label. | It performs full Context Intake or issue repair. |
| Agent-prompt adequacy exists | hard gate | A fresh coding agent can start from the issue plus repo-local context. | Check candidate states requested work and success shape enough to begin intake. | A title-only nontrivial issue passes. | Exact files or complete design are required. |
| Observable done signal exists | hard gate | Later proof has a target. | Check for expected behavior, repro, proof hint, doc target, or done condition. | "Make better" passes. | A full proof plan is required now. |
| Blocker/dependency state is clear | hard gate | Work will not start in the wrong order. | Check no visible blocker exists, or selected item is the blocker. | Textual blockers are ignored. | Agent edits dependency metadata. |
| No result-defining ambiguity remains | hard gate | Agent will not invent product intent. | Check missing details would not change expected result. | Vague result-changing gaps pass. | Every ordinary implementation unknown blocks selection. |
| Owner boundaries are preserved | hard gate | `implement` stayed selection-only. | Check no issue creation, repair, relabeling, splitting, planning, proof design, or tracker mutation occurred. | Mutation happens silently. | Normal selection is refused due to missing full context. |
| Selection boundary is ready for Context Intake | handoff | Next facet has stable identity and readiness facts. | Check selected item and readiness facts are recorded before planning. | Only a title is recorded. | A full implementation plan is drafted. |

## 10. Stop / Ask Rules

| Rule | Stop / Ask / Narrow / Continue | Why | Resume Condition |
| --- | --- | --- | --- |
| Multiple eligible candidates with no visible order | Ask | Priority is user/repo-owned. | User or repo ordering selects one. |
| No ready issue-equivalent item exists | Stop | `implement` must not create its own work to stay busy. | User provides a ready item or upstream workflow creates/triages one. |
| PRD/spec/path without one ready issue | Stop / ask / handoff | A source document is not automatic implementation scope. | One ready issue-equivalent item is named. |
| Candidate requires readiness repair or tracker mutation | Stop / handoff | Repair belongs to `triage`, `to-issues`, or tracker owner. | Item is made ready upstream. |
| Candidate is blocked | Stop / ask | Dependency order matters. | Blocker is resolved, selected, or order is confirmed. |
| Result-defining ambiguity exists | Ask | Prevents invented requirements. | Missing result detail is supplied. |
| Prompt-poor issue or no done signal | Stop / handoff | Implementation would be unverifiable or invented. | Issue brief or done signal is repaired upstream. |
| Sensitive or critical domain signal | Ask | Avoids silent high-risk autonomous pickup. | User confirms boundaries/guardrails. |
| Obvious multi-issue smell | Narrow / handoff | Selection can reject unsafe scope, not split it. | One coherent issue-equivalent item exists. |
| Selection starts becoming planning | Stop / continue after correction | Context Intake owns understanding and planning. | Identity/readiness facts are recorded. |
| One candidate passes all gates | Continue | Facet is complete. | Handoff to Context Intake. |

## 11. Ownership And Pointer Decisions

| Item | Runtime Skill | Support Doc | Research Only | Owned Elsewhere | Conflict Severity | Why |
| --- | --- | --- | --- | --- | --- | --- |
| One selected issue-equivalent item | Yes | Maybe | No | No | none | Core facet behavior. |
| Repo-visible ordering or explicit user target | Yes | Maybe | No | Repo tracker docs for exact syntax | soft-reference | Runtime needs authority; docs own details. |
| Local readiness recheck | Yes | Maybe | No | `triage` owns repair | hard-boundary | Runtime checks; upstream fixes. |
| Agent-prompt adequacy | Yes | Maybe | No | Context Intake owns deeper context | later-facet-watchpoint | Selection needs only adequacy. |
| Observable done signal | Yes | Maybe | No | Semantic Proof owns proof strategy | later-facet-watchpoint | Selection needs a target, not proof design. |
| Blocker/dependency check | Yes | Maybe | No | Tracker docs own syntax and metadata edits | hard-boundary | Runtime detects; tracker owner mutates. |
| Result-defining ambiguity stop | Yes | Maybe | No | `triage` / user may supply missing result detail | hard-boundary | Runtime must not invent requirements. |
| Multiple/no-ready stop branches | Yes | No | No | User / `triage` / `to-issues` | hard-boundary | Prevents silent ownership change. |
| PRD/spec without issue branch | Yes | No | No | `to-issues` | hard-boundary | Prevents whole-spec implementation. |
| Risk-domain confirmation | Yes | Maybe | No | Engineering contract / repo docs | soft-reference | Runtime asks; policy owns thresholds. |
| Obvious multi-issue smell | Maybe | Yes | No | Bounded Slice Control / `to-issues` | later-facet-watchpoint | Selection catches only obvious unsafe scope. |
| Select first, plan later | Yes | No | No | Context Intake owns next phase | later-facet-watchpoint | Keeps phase boundary clear. |
| Kanban/DoR/Small CL rationale | No | Yes | Maybe | No | support-only | Useful rationale, not inline behavior. |
| Full DoR/INVEST/story splitting | No | No | Yes | `to-issues` / `triage` | hard-boundary | Not source selection behavior. |

## 12. Agent Bridge Risks

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |
| Flow becomes polished runtime wording too early | Prompt 06 should produce a skeleton, not final `SKILL.md` prose. | Keep action/gate/branch language and defer prose to Prompt 07. |
| Local readiness recheck becomes full triage | Would make `implement` repair or promote issues. | Limit recheck to prompt adequacy, done signal, blockers, and ambiguity. |
| Gate terms are too vague | "Ready" and "clear" can pass without evidence. | Use named gates with concrete facts. |
| Generic ask behavior returns | Would make the agent timid. | Ask only on named gates: priority, result-defining ambiguity, blocker, risk, or missing target issue. |
| Selection becomes planning | Would collapse into Context Intake. | Require selection facts only before handoff. |
| Agent invents priority | Would violate user/repo ownership. | Require repo-visible order or explicit user target. |
| `implement` repairs issues | Would take over `triage` / `to-issues`. | Add hard owner-boundary stop. |
| Size smell becomes slicing workflow | Would steal Bounded Slice Control. | Only reject obviously multi-issue candidates; do not decompose. |
| Risk gate becomes policy doc | Could conflict with repo policy. | Keep as confirmation branch and point to repo docs / engineering contract. |
| Source support terms leak inline | DoR, INVEST, WIP, and Scrum terms can bloat runtime. | Keep them in support/reference inventory. |

## 13. Handoff To Full Behavior Synthesis

Behavior-flow decision: `ready-for-full-behavior-synthesis`

Final behavior sequence:

1. Resolve candidate surface.
2. Lock one issue-equivalent item.
3. Apply selection authority.
4. Run local readiness recheck.
5. Check risk and size smells.
6. Record selection boundary and hand off to Context Intake.

Strongest leading words:

- one selected issue-equivalent item;
- repo-visible ordering or explicit user target;
- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity;
- risk-domain confirmation;
- obvious multi-issue smell;
- select first, plan later.

Strongest gates:

- exactly one selected issue-equivalent item;
- selection authority by repo-visible order or explicit user target;
- prompt adequacy;
- observable done signal;
- blocker/dependency state;
- no result-defining ambiguity;
- owner boundary preserved;
- selection boundary before planning.

Support/reference pointers needed:

- repo tracker docs for exact ready labels, ordering, commands, state semantics,
  and dependency syntax;
- support rationale for Kanban pull/WIP and DoR/stage-gate contrast if final
  runtime needs a reference note;
- support examples for agent-prompt adequacy, blocker/dependency checks, and
  obvious multi-issue smell;
- engineering contract or repo docs for exact high-risk policy.

Unresolved design questions:

- Whether Prompt 07 should keep `agent-prompt adequacy` as a visible phrase or
  fold it under `local readiness recheck`.
- Whether `risk-domain confirmation` belongs inline in final runtime or stays
  mostly as a commitment-boundary pointer.
- Whether the obvious multi-issue smell survives runtime compression or is
  left to Bounded Slice Control.
- How explicit the PRD/spec route should be when the user names a source
  document and implies a narrow issue-equivalent slice.

Ownership conflicts:

- `to-issues` owns PRD/spec decomposition.
- `triage` owns ready-state promotion and issue-brief repair.
- Repo tracker docs own exact labels, commands, ordering fields, state names,
  and dependency metadata.
- Context Intake owns full understanding, file discovery, and planning after
  selection.
- Bounded Slice Control owns detailed size and slice management.
- Semantic Proof owns proof strategy.
- Review And Lock owns output review.
- Engineering contract / repo docs own exact sensitive/critical policy.

What Prompt 07 should explain in prose:

- Why the first behavior is selecting one issue-equivalent item, not looking
  for general work.
- How repo-visible ordering or explicit user target gives selection authority.
- How local readiness recheck is intentionally smaller than `triage` or
  Context Intake.
- How named stop/ask branches protect owner boundaries.
- Why the handoff after this facet is Context Intake, not implementation.
