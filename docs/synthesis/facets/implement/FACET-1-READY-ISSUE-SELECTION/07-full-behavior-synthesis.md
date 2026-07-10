# Prompt 07: Full Behavior Synthesis For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/07-full-behavior-synthesis.md`](../../../methods/prompts/07-full-behavior-synthesis.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Facet research question: How should `implement` select exactly one ready issue
or stop when no safe issue is available?

Facet boundaries:

- Owns: source/candidate resolution, one issue-equivalent selection, selection
  authority, tracker-state eligibility, compact readiness recheck,
  blocker/dependency stop, result-defining ambiguity stop, no-ready stop,
  PRD/spec-without-issue handoff, generic risk confirmation, obvious
  multi-issue smell, explicit-target no-substitution, and the handoff boundary
  to Context Intake.
- Does not own: issue creation, issue repair, issue splitting, ready-state
  promotion, tracker metadata mutation, exact tracker syntax, product priority,
  full Context Intake, implementation planning, proof strategy, review, commit,
  issue notes, or exact sensitive-domain policy.
- Should answer: what the agent does before coding to select one ready
  issue-equivalent item or stop safely.
- Should not answer: how to author the issue, make it ready, decompose a source
  document, design implementation, prove the change, or close the work.

Agent bridge:
[`06-agent-bridge.md`](06-agent-bridge.md)

Agent-bridge decision: `ready-for-full-behavior-synthesis`

Typed gates and branch exits:

- Hard gates: candidate surface can produce one item; exactly one selected
  issue-equivalent item; visible selection authority; tracker-state
  eligibility; local readiness recheck; agent-prompt adequacy; observable done
  signal; blocker/dependency state; no result-defining ambiguity; owner
  boundaries preserved.
- Rechecks: risk-domain confirmation; obvious multi-issue smell.
- Handoff: selection facts recorded before Context Intake.
- Branch exits: multiple candidates ask user; no ready item blocks; PRD/spec
  without one issue hands off to `to-tickets`; readiness repair/tracker mutation
  hands off; blocked candidate asks/stops; result-defining ambiguity asks;
  prompt-poor/no done signal hands off; risk asks; premature planning rejoins
  after recording facts; explicit ineligible target blocks without silent
  substitution.

Priority preservation:

- Must: one selected issue-equivalent item; repo-visible ordering or explicit
  user target; tracker-state eligibility; local readiness recheck;
  agent-prompt adequacy; observable done signal; blocker/dependency check;
  multiple-candidate order stop; no-ready stop; PRD/spec without one issue
  stop; result-defining ambiguity stop; owner-boundary stop; explicit-target
  no-substitution stop.
- Should: select first, plan later; risk-domain confirmation.
- Could: obvious multi-issue smell; report checked surface when stopping.

Duplicate-term choices:

- Primary terms: one selected issue-equivalent item; repo-visible ordering or
  explicit user target; tracker-state eligibility; local readiness recheck;
  agent-prompt adequacy; observable done signal; result-defining ambiguity;
  blocker/dependency check; select first, plan later.
- Support terms: pull, WIP, ready marker, ready for selection, issue as prompt,
  acceptance criteria, testable, underspecified, blocked by / blocking,
  sensitive, self-contained.
- Avoid runtime terms: full Definition of Ready, INVEST, Scrum ceremony,
  tracker-specific syntax, full proof plan, ask if unsure, suitable issue.

Owner-severity decisions:

- Hard-boundary: `to-tickets` owns PRD/spec decomposition; `triage` owns
  ready-state promotion and issue-brief repair; tracker docs own exact syntax,
  commands, labels, ordering fields, and metadata mutation; user/repo-visible
  policy owns priority.
- Later-facet-watchpoint: Context Intake owns full understanding and file
  discovery; Bounded Slice Control owns detailed size/slice management;
  Semantic Proof owns proof strategy; Review And Lock owns output review.
- Soft-reference: engineering contract / repo docs own exact high-risk policy.
- Support-only/research-only: Kanban, Scrum, DoR, INVEST, Small CL, and
  benchmark rationale.

Relevant research packets:

- Source search:
  [`docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md`](../../../../research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md)
- Source extraction:
  [`docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-extraction.md`](../../../../research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-extraction.md)
- Source triage:
  [`docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-triage.md`](../../../../research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-triage.md)

Revision feedback:

- Rerun Prompt 07 from the refreshed Prompt 06 agent-bridge packet.
- Use three subagents to check schema/section compliance, behavior synthesis,
  and runtime/support/owner placement.

Subagent inputs used:

- Schema pass: replace the legacy flow-oriented template shape with current
  Prompt 07 sections.
- Behavior synthesis pass: preserve one-item selection, visible authority,
  tracker-state eligibility, compact readiness facts, named branch exits, and
  Context Intake handoff.
- Owner/prune pass: demote source-method jargon to support and keep issue
  repair, splitting, planning, proof, review, tracker mutation, and exact risk
  policy out of this facet.

## 1. Purpose

This facet makes `implement` predictable at the moment before coding starts.
The agent should begin from one selectable work item, not from momentum, queue
browsing, a broad source document, a path-shaped hint, or a hunch about what
seems useful.

The behavior matters when the user invokes `implement` with one issue, several
possible issues, a queue, a source document, a path, a URL, or no explicit
item. It is the gate that decides whether the session has one legitimate
implementation item to own, or whether it must stop, ask, narrow, or hand off
before Context Intake begins.

Average-agent behavior to prevent:

- grabbing a batch of work because several items are visible;
- treating a PRD, spec, project, queue, or bare path as implementation scope;
- trusting a ready label without checking whether the item can guide an agent;
- bypassing ready-state checks because the user named an issue;
- silently substituting another issue when an explicit target is ineligible;
- inventing priority among multiple ready items;
- starting work that is blocked, unverifiable, or result-defining ambiguous;
- repairing, relabeling, splitting, or promoting issues inside `implement`;
- sliding from selection into file discovery, planning, proof design, or code
  edits.

Upper-bound engineering taste to recruit:

- disciplined pull: one selected issue-equivalent item enters the active run;
- visible authority: priority and readiness come from the user or repo-visible
  order, not agent preference;
- issue commitment: a named item still has to be eligible before the agent
  enters implementation;
- compact readiness: enough local recheck to avoid unsafe pickup, not a full
  triage ceremony;
- owner-boundary respect: unready work goes to the owner that can make it
  ready;
- stable handoff: Context Intake starts from selected identity and readiness
  facts, not from an improvised plan.

This facet does not make work ready. It only selects or stops. Issue creation,
issue repair, PRD decomposition, detailed slicing, implementation planning,
proof strategy, review, commit behavior, and exact risk policy all belong
elsewhere.

## 2. Prompt 06 Handoff Check

| Prompt 06 Input | Used / Revised / Deferred / Rejected | Synthesis Consequence | Notes |
| --- | --- | --- | --- |
| agent-bridge decision: `ready-for-full-behavior-synthesis` | Used | Continue to full behavior synthesis. | No agent-bridge loop needed. |
| Final behavior sequence | Used | Prose explains six steps: resolve surface, lock one item, apply authority, recheck readiness, check risk/size, record boundary. | Sequence is preserved. |
| Typed gates | Used | Hard gates stay hard; risk/size stays recheck; selection boundary stays handoff. | Prompt 08 must preserve gate strength. |
| Branch exits | Used | Branches remain ask-user, handoff-skill, blocked, or rejoin-flow. | No generic "ask if unsure" branch is introduced. |
| Priority preservation | Used | Must candidates remain runtime candidates. | Should/Could items become compact branches or support pressure. |
| Duplicate-term choices | Used | Primary terms are kept; source terms are demoted. | WIP, DoR, INVEST, Scrum, and Small CLs do not become runtime anchors. |
| Owner-severity decisions | Used | Hard-boundary conflicts become stop/handoff explanations. | `triage`, `to-tickets`, tracker docs, Context Intake, Semantic Proof, Review And Lock, and engineering contract remain owners. |
| Support/reference pointers | Used | Support keeps rationale and examples. | Runtime should point to repo tracker docs for exact syntax. |
| Explicit-target no-substitution branch | Used | Named ineligible target stops on that item instead of silently replacing it. | This is a hard eligibility behavior for Prompt 08. |
| Unresolved design questions | Resolved or deferred | `agent-prompt adequacy` remains visible; risk and multi-issue branches are short; PRD/spec route remains explicit. | Prompt 08 may decide whether risk/size survive inline after compression. |

## 3. Revision Feedback Disposition

| Feedback Item | Affected Sections | Step 7 Action | Remaining Risk |
| --- | --- | --- | --- |
| Current Prompt 07 schema requires `Agent bridge`, `Agent-bridge decision`, revision feedback, bridge traceability, candidate draft contract, and candidate runtime draft handoff. | Prompt Inputs, Sections 2, 3, 6, 16, 17 | Rebuilt artifact around current schema. | Prompt 08 should consume current section names, not legacy handoff labels. |
| Prompt 06 added tracker-state eligibility and explicit-target no-substitution. | Purpose, chosen behavior, traceability, gates, stop/ask logic, budget, contract | Promoted both into runtime-preserve behavior. | Prompt 08 may be tempted to collapse this into generic readiness. |
| User requested three subagents. | Prompt Inputs and synthesis choices | Incorporated schema, behavior, and owner/pruning passes. | None for Prompt 07; subagent outputs were advisory, not separate source truth. |

## 4. Source Pressure

| Source / Prior | Pressure It Adds | Behavior It Supports | Runtime Or Support? |
| --- | --- | --- | --- |
| GitHub Copilot task guidance | Assigned work should be scoped enough to guide an agent and include a success shape. | Agent-prompt adequacy and observable done signal. | Runtime with support examples. |
| Kanban pull / WIP rationale | Work should enter the active system only under a pull rule and WIP discipline. | One selected issue-equivalent item. | Support rationale; behavior is runtime. |
| DORA WIP limits | Do not start extra work to stay busy; visible priority and blockers matter. | No-ready stop, multiple-candidate order stop, blocker discipline. | Runtime pressure plus support. |
| Scrum ready-for-selection language | Selection is not full planning; item must be selectable enough, ordered, and transparent. | Select first, plan later; selection authority. | Support rationale; behavior is runtime. |
| GitHub issue dependencies | Blocked-by/blocking semantics are visible dependency evidence. | Blocker/dependency check. | Runtime behavior; tracker syntax support. |
| SWE-bench Verified underspecification | Missing result-defining information makes agent work unreliable. | Result-defining ambiguity stop. | Support rationale; behavior is runtime. |
| VS Code AI task guidance | Good agent tasks need specific input, output, constraints, and expected result. | Agent-prompt adequacy and done signal. | Runtime pressure. |
| Copilot Agents responsible-use guidance | Sensitive or consequential autonomous work needs oversight. | Risk-domain confirmation. | Short runtime branch; exact policy elsewhere. |
| Definition of Ready / stage-gate contrast | A small readiness check helps; a full checklist can become a gate owned upstream. | Local readiness recheck, not issue repair. | Support only. |
| Google Small CL reviewability | One coherent change is easier to review than broad mixed work. | Obvious multi-issue smell. | Optional runtime branch / support. |

## 5. Chosen Behavior

The agent first identifies the candidate surface. It asks: did the user name
one issue-equivalent item, point at a ready queue, provide a PRD/spec/path, or
give no item at all? This prevents a source document, queue, or broad request
from quietly becoming implementation scope.

The agent then locks exactly one issue-equivalent item. The selected thing can
be an issue, URL, tracker item, path-backed ready slice, or explicit
user-selected work item. It cannot be a list, queue, project, PRD, broad spec,
or batch. If more than one eligible item exists and no repo-visible order
selects one, the agent asks. If no ready item exists, it stops and reports the
checked surface.

Selection authority comes next. The agent may own the selected item only when
the authority is visible: the user selected it, or repo-visible ready/order
policy selected it. For tracker items, visible authority includes state
eligibility: the item must not be closed, waiting for information, human-owned,
rejected, or otherwise blocked by tracker state. If a user explicitly names an
ineligible target, the agent stops on that target and reports the missing
eligibility fact. It does not quietly replace the target with another issue.

The local readiness recheck is deliberately small. It proves that the item can
guide a fresh coding agent, that at least one observable done signal exists,
that visible blockers or dependencies do not prevent pickup, and that no
result-defining ambiguity remains. This is not Context Intake, proof strategy,
or triage. It is a small pre-ownership check that catches false-ready work.

The agent also checks risk and size smells. Sensitive, critical, regulated,
security, PII, auth, incident, production-critical, consequential, or deep
business-logic work needs explicit boundaries before autonomous pickup. An item
that is plainly many issues should be narrowed or routed upstream, not sliced
inside this facet.

The handoff is a selection boundary, not a plan. The agent records the selected
item identity, why it was the one selected item, selection authority, tracker
eligibility facts when relevant, readiness facts, and any branch resolved or
handed off. Then it moves to Context Intake.

## 6. Bridge Traceability

| Agent Bridge Step / Gate | Synthesis Explanation | Candidate Behavior Fragment Or Gate Consequence | Must Preserve? |
| --- | --- | --- | --- |
| Step 1: Resolve candidate surface | Identify whether the user gave one item, a ready surface, a source document, or no source. | Candidate surface must be able to produce one issue-equivalent item. | yes |
| Step 2: Lock one issue-equivalent item | Selection succeeds only with one concrete item, not a batch, project, queue, or document. | Exactly one selected issue-equivalent item is named. | yes |
| Step 3: Apply selection authority | The agent may not choose by taste; authority comes from repo-visible order or explicit user target. | Selection authority is visible. | yes |
| Tracker-state eligibility | Named tracker item must be eligible before implementation; explicit target does not bypass readiness. | Ineligible explicit target stops on that item; no silent substitution. | yes |
| Step 4: Local readiness recheck | Check prompt adequacy, done signal, blocker/dependency state, and result-defining ambiguity. | Readiness facts recorded; no full triage. | yes |
| Step 5: Risk and size smells | Risk is a confirmation branch; obvious multi-issue work is a narrow/route branch. | Ask on risk; narrow on obvious multi-issue smell. | optional |
| Step 6: Selection boundary | Record identity, authority, eligibility/readiness facts, and branch outcomes before planning. | Selection facts complete before Context Intake. | yes |
| B1: Multiple candidates | Priority is user/repo-owned. | Ask: user or repo order selects one. | yes |
| B2: No ready item | `implement` must not create work to stay busy. | Stop: checked surface has no ready item. | yes |
| B3: PRD/spec without issue | Source docs need one ready issue or upstream issue creation. | Handoff: one ready item must be named. | yes |
| B4: Obvious multi-issue smell | Selection may reject unsafe scope but must not decompose it. | Narrow: one coherent item required. | optional |
| B5: Readiness repair / tracker mutation | Repair and tracker mutation belong elsewhere. | Handoff: upstream owner makes item ready. | yes |
| B6: Blocked candidate | Dependency order matters unless working the blocker. | Gate: blocker resolved, selected, or order confirmed. | yes |
| B7: Result-defining ambiguity | Ask only when missing detail changes expected result. | Ask: missing result detail supplied. | yes |
| B8: Prompt-poor / no done signal | Agent must not invent issue brief or proof target. | Handoff: prompt and done signal exist. | yes |
| B9: Risk-domain confirmation | High-risk autonomous pickup needs boundaries. | Ask: user confirms guardrails. | optional |
| B10: Premature planning | Context Intake owns discovery and planning. | Stop: record selection facts first. | yes |
| B11: Explicit target is not eligible | Named work is not automatically implementable. | Block: report missing eligibility; no substitute unless asked. | yes |

## 7. Leading Words

| Leading Word | Primary / Support / Avoid | Why It Recruits Useful Priors | Behavior It Anchors | Risk If Misused |
| --- | --- | --- | --- | --- |
| one selected issue-equivalent item | Primary | Makes selection singular and concrete while allowing non-GitHub issue forms. | Step 2 hard gate. | Compressing to "issue" may exclude path-backed or user-selected work. |
| repo-visible ordering or explicit user target | Primary | Keeps priority and readiness authority visible. | Step 3 authority gate. | Compressing to "ready issue" hides authority. |
| tracker-state eligibility | Primary | Makes issue state a selection gate without teaching tracker mechanics. | Named tracker item eligibility. | Can drift into label editing or exact syntax. |
| local readiness recheck | Primary | Allows a small safety check without importing full triage. | Step 4 pre-context gate. | Can bloat into DoR or issue repair. |
| agent-prompt adequacy | Primary | Tests whether a fresh coding agent can begin from the item. | Prompt-quality sub-gate. | "Clear enough" is too vague. |
| observable done signal | Primary | Keeps pickup from becoming unverifiable work. | Success-shape sub-gate. | "Acceptance criteria" may imply full proof planning. |
| blocker/dependency check | Primary | Recruits work-order and dependency discipline. | Dependency stop branch. | Tracker syntax or metadata edits may leak inline. |
| result-defining ambiguity | Primary | Distinguishes correctness-changing gaps from ordinary unknowns. | Specific ask branch. | "Ask if unsure" causes timid over-asking. |
| risk-domain confirmation | Support / optional runtime | Reminds agent not to silently enter high-impact work. | High-risk pickup ask branch. | Can become an inline policy document. |
| obvious multi-issue smell | Support / optional runtime | Catches plainly non-singular scope. | Narrow or upstream route branch. | Can become a slicing workflow. |
| select first, plan later | Primary | Protects phase order and Context Intake boundary. | Handoff boundary. | Easy to lose during compacting. |
| pull / WIP | Support | Explains why one active item matters. | Rationale for singular selection. | Imports Kanban ceremony if inline. |
| Definition of Ready / INVEST / Scrum terms | Avoid runtime | Source rationale only. | Support for readiness restraint. | Pulls `implement` into process or triage. |

## 8. Agent Execution Surface

| Execution Surface | Agent Action | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- |
| read | Read the user request and repo tracker docs only enough to identify candidate surface and authority. | Source type and authority source are known. | Treating broad inputs as scope. |
| inspect | Inspect ready labels/order/blockers semantically, using repo docs for syntax. | Candidate has visible authority and no contradiction. | Invented priority or tracker mutation. |
| search | Search the ready surface only enough to find one eligible candidate when no explicit item is named. | Exactly one candidate or a no/multiple branch is reached. | Queue browsing and batch pickup. |
| compare | Compare candidate facts against eligibility/readiness gates: tracker state, prompt adequacy, done signal, blockers, ambiguity. | Eligibility and readiness facts are recorded. | Label-only readiness. |
| stop | Stop when no ready item exists, source doc lacks one issue, target is ineligible, readiness repair is needed, or tracker mutation would be required. | Branch exit is recorded. | Upstream takeover. |
| ask | Ask on user-owned choices or missing result-defining detail, risk boundaries, blockers, or narrowing. | User supplies selection, missing detail, boundary, or narrower item. | Timid generic asking and invented requirements. |
| report | Record checked surface, selected item, authority, eligibility/readiness facts, and handoffs. | Context Intake receives stable selection facts. | Selection-as-planning. |
| validate | Validate only the selection gates, not code behavior. | All hard gates pass or a branch exits. | Premature proof design. |

## 9. Evidence Gates

| Gate | Gate Type | Why It Matters | Too Weak If | Too Heavy If | Candidate Consequence Shape |
| --- | --- | --- | --- | --- | --- |
| Candidate surface can produce one item | hard gate | Prevents source documents, queues, and vague requests from becoming scope. | It accepts a PRD/spec as scope. | It decomposes the PRD inTo Tickets. | "No one issue-equivalent item, no implementation." |
| Exactly one selected issue-equivalent item | hard gate | Bounds the run to one item. | It names a list or project. | It rejects valid user-selected path-backed work. | "Name one issue-equivalent item." |
| Selection authority is visible | hard gate | Prevents invented priority/readiness. | It says "looks ready." | It edits labels, state, or priority. | "Use repo-visible order or explicit user target." |
| Tracker-state eligibility is visible | hard gate | Keeps named tracker work from bypassing readiness. | Closed, needs-info, ready-for-human, wontfix, or other ineligible state passes. | Agent edits state or inlines exact tracker syntax. | "Named target must be eligible; do not substitute silently." |
| Local readiness recheck | hard gate | Catches false-ready work before ownership. | It checks only a label. | It performs full Context Intake or issue repair. | "Recheck prompt, done signal, blockers, ambiguity." |
| Agent-prompt adequacy | hard gate | Ensures a fresh agent can begin intake. | A title-only nontrivial issue passes. | Exact files/design are required. | "Issue can guide a fresh coding agent." |
| Observable done signal | hard gate | Keeps pickup from being unverifiable. | "Make better" passes. | A full proof plan is required. | "At least one expected result or proof hint exists." |
| Blocker/dependency state clear | hard gate | Prevents starting in the wrong order. | Text blockers are ignored. | Agent edits dependency metadata. | "No blocker, or this item is the blocker." |
| No result-defining ambiguity | hard gate | Prevents invented requirements. | Missing expected behavior passes. | Ordinary implementation unknowns block. | "Ask only if the missing fact changes the result." |
| Risk-domain confirmation | recheck | Avoids silent high-risk pickup. | Sensitive signals are ignored. | Runtime defines full policy. | "Ask for boundaries on high-risk work." |
| Obvious multi-issue smell | recheck | Stops obviously non-singular work. | Broad multi-slice work passes. | Agent starts slicing here. | "If plainly many issues, narrow or route upstream." |
| Owner boundary preserved | hard gate | Keeps selection from taking over other skills. | Issue repair happens silently. | Normal selection is blocked for missing full context. | "Detect unready; do not make ready." |
| Selection facts recorded before planning | handoff | Gives Context Intake a stable starting point. | Only a title is recorded. | A full plan is drafted. | "Record selection facts, then hand off." |

## 10. Stop / Ask / Continue Logic

| Situation | Agent Should | Why | Resume / Continue When |
| --- | --- | --- | --- |
| Multiple eligible items with no repo-visible order | Ask | Priority is user/repo-owned. | User or repo order selects one. |
| No ready issue-equivalent item exists | Stop | `implement` must not create work to stay busy. | User provides a ready item or upstream workflow creates one. |
| User gives PRD/spec/path without one ready item | Stop / ask / handoff | A source document is not automatic implementation scope. | One ready issue-equivalent item is named. |
| User names an ineligible tracker item | Stop | An explicit target does not grant permission to bypass readiness. | Named item becomes eligible or user explicitly selects another ready item. |
| Selection requires issue repair, relabeling, promotion, splitting, or tracker metadata edit | Stop / handoff | Making work ready belongs upstream. | `triage`, `to-tickets`, or tracker owner makes it ready. |
| Candidate is blocked | Stop / ask | Dependency order matters. | Blocker is resolved, selected, or order is confirmed. |
| Candidate is prompt-poor or has no done signal | Stop / handoff | Agent would invent the brief or do unverifiable work. | Issue brief or done signal is repaired upstream. |
| Result-defining ambiguity exists | Ask | Missing detail changes what should be built. | Missing result detail is supplied. |
| Sensitive or critical domain signal appears | Ask | User-owned risk/commitment boundary may be involved. | User confirms boundaries or chooses another item. |
| Obvious multi-issue smell appears | Narrow / handoff | Selection can reject broad scope, not split it. | One coherent issue-equivalent item exists. |
| Ordinary code technique is unknown but selection gates pass | Continue | Technique belongs to later Context Intake / implementation. | No user input needed at this facet. |
| Selection starts becoming planning | Stop, then continue after correction | Context Intake owns planning and file discovery. | Selection facts are recorded. |
| One candidate passes all gates | Continue | Facet is complete. | Handoff to Context Intake. |

## 11. Runtime vs Support Placement

| Material | Runtime / Support / Research / Elsewhere | Pointer Shape | Why |
| --- | --- | --- | --- |
| One selected issue-equivalent item | Runtime | inline runtime | Core success condition. |
| Repo-visible ordering or explicit user target | Runtime | inline runtime | Selection authority must be visible. |
| Tracker-state eligibility | Runtime | inline runtime plus short tracker-doc pointer | Eligibility matters; exact label/state syntax is repo-owned. |
| Local readiness recheck | Runtime | inline runtime | Needed before Context Intake. |
| Agent-prompt adequacy | Runtime | inline runtime or compact sub-gate | Avoids prompt-poor pickup. |
| Observable done signal | Runtime | inline runtime or compact sub-gate | Avoids unverifiable pickup. |
| Blocker/dependency check | Runtime | inline runtime plus short tracker-doc pointer | Dependency semantics are runtime; syntax is local. |
| Result-defining ambiguity | Runtime | inline runtime | Prevents invented requirements without generic asking. |
| Explicit-target no-substitution | Runtime | inline runtime | Prevents named-but-unready work from being silently replaced. |
| Risk-domain confirmation | Runtime / Support | short runtime pointer | Runtime asks; repo docs/contract own policy. |
| Obvious multi-issue smell | Runtime / Support | short runtime pointer or support/reference section | Useful early smell; detailed slicing elsewhere. |
| Select first, plan later | Runtime | inline runtime | Preserves phase order. |
| Kanban/WIP rationale | Support | support/reference section | Explains one-item discipline. |
| DoR / stage-gate contrast | Support | support/reference section | Explains why readiness check stays small. |
| Issue-as-prompt examples | Support | support/reference section | Helps examples without bloating runtime. |
| Tracker labels, commands, ordering fields, dependency syntax | Elsewhere | other skill/contract | Repo tracker docs own exact details. |
| Issue repair, promotion, splitting, relabeling | Elsewhere | other skill/contract | `triage` / `to-tickets` own readiness repair. |
| Full proof strategy | Elsewhere | later facet | Semantic Proof owns proof. |
| Context reading, file discovery, implementation planning | Elsewhere | later facet | Context Intake owns this after selection. |
| Review and lock behavior | Elsewhere | later facet | Review And Lock owns output review. |
| Exact sensitive-domain policy | Elsewhere | other skill/contract | Engineering contract / repo docs own policy. |
| Kanban metrics, Scrum ceremony, benchmark scoring, platform setup | Research | research-only | No runtime behavior. |

## 12. Rejected Or Deferred Options

| Option | Reject / Defer | Why | Revive Only If |
| --- | --- | --- | --- |
| "Pick a ready issue" without authority and eligibility gates | Reject | Hides priority, readiness, and explicit-target eligibility. | It preserves repo-visible order, explicit user target, and tracker-state eligibility. |
| Silent substitution when named item is ineligible | Reject | Violates explicit user target and hides readiness failure. | User explicitly asks for another ready issue. |
| Whole PRD/spec as implementation scope | Reject | Violates one issue-equivalent boundary. | A ready issue-equivalent slice is named. |
| Full DoR checklist | Reject | Turns selection into triage/process ceremony. | Working on `triage` or repo process docs. |
| Full INVEST matrix | Reject | Issue authoring and slicing are upstream. | Working on `to-tickets` or `triage`. |
| Runtime tracker command syntax | Defer | Repo docs own exact syntax and change over time. | Editing repo tracker docs. |
| Issue repair during selection | Reject | `implement` detects unready work but must not make it ready. | User explicitly asks for tracker/triage maintenance. |
| Agent chooses priority among unordered candidates | Reject | Product priority is not agent-owned. | User or repo order selects one. |
| Full risk policy | Defer | Runtime should ask; repo docs define thresholds. | Working on engineering contract or repo policy. |
| Full proof plan before selection | Reject | Semantic Proof owns proof strategy. | Later facet starts after selection. |
| Detailed slicing of broad work | Reject here | Bounded Slice Control or `to-tickets` owns slicing. | A later facet or skill is invoked. |
| Generic "ask if unsure" | Reject | Causes timid over-asking. | It becomes named gates: order, ambiguity, blockers, risk, missing target, or ineligible explicit target. |
| Planning/file discovery before selection facts | Reject | Collapses into Context Intake. | Selection facts are recorded first. |

## 13. Design Questions

| Question | Why It Matters | Disposition | Suggested Resolution |
| --- | --- | --- | --- |
| Should `agent-prompt adequacy` remain visible? | It is the clearest agent-specific gate, but a candidate runtime draft may want to fold it into local readiness. | resolved-for-candidate-draft | Keep it visible unless `local readiness recheck` explicitly includes "fresh coding agent can begin." |
| Should `tracker-state eligibility` stay separate from selection authority? | It protects explicit-target cases and keeps tracker state visible. | resolved-for-candidate-draft | Keep it as its own candidate line or sub-gate; point exact syntax to tracker docs. |
| Should `risk-domain confirmation` be inline? | It protects high-risk pickup but can become policy text. | defer-to-Prompt-08 | Keep as a short ask gate plus repo-policy pointer if budget allows. |
| Should the obvious multi-issue smell survive runtime? | It catches unsafe scope but can drift into slicing. | defer-to-Prompt-08 | Keep only if compressed as "ask/narrow; do not split here." |
| How explicit should PRD/spec routing be? | Users may give source documents while implying a narrow slice. | resolved-for-candidate-draft | Say source docs require one ready issue-equivalent item or `to-tickets` handoff. |
| Should Prompt 08 use "pull" as a leading word? | It is useful taste but less concrete than the selected-item gate. | defer-to-Prompt-08 | Prefer one selected issue-equivalent item; keep pull as support if needed. |

## 14. Verbose Draft Notes

The agent should think of selection as a disciplined pull into one concrete
implementation item. It is not looking for work in general. It is deciding
whether this run has exactly one issue-equivalent item that the agent is allowed
to own.

The first check is the candidate surface. A user may name one issue, point at a
queue, paste a PRD, provide a path, or simply ask to implement. Those inputs do
not have the same meaning. A PRD, spec, queue, or project is not automatically
one implementation item. If the input cannot yield one concrete candidate, the
agent should stop, ask for the target, or route upstream.

The second check is authority and eligibility. The agent can act on an explicit
user target or on repo-visible ordering/readiness. It should not choose by
taste, convenience, or perceived importance. For tracker items, the agent must
also confirm the named item is eligible. A closed, needs-info, ready-for-human,
wontfix, or otherwise ineligible item does not become implementable just
because it was named. The agent stops on that item and reports the missing
eligibility fact rather than silently substituting another issue.

The local readiness recheck is intentionally small. It asks whether the item can
guide a fresh coding agent, whether there is at least one observable done
signal, whether blockers are clear, and whether any missing information would
change the expected result. It does not gather all context, choose files, design
proof, or repair the issue. Those are later or upstream responsibilities.

The stop/ask behavior should be specific. The agent asks when the user owns the
choice or missing fact: unordered candidates, result-defining ambiguity,
blocker order, risk boundaries, or narrowing an obvious multi-issue item. It
continues when ordinary implementation technique is merely unknown, because
that belongs to Context Intake and implementation.

Risk and size checks are smells, not full workflows. Sensitive or critical work
needs user boundaries or repo-policy guidance. Obviously broad or multi-issue
work needs narrowing or upstream handling. The agent should not write a risk
policy, and it should not decompose broad work inside this selection facet.

The facet ends by recording selection facts: selected item identity, why this
is the one item, authority source, eligibility facts when relevant, readiness
facts, and any branch that was resolved or handed off. That record is the
handoff into Context Intake. If the agent begins planning, searching files,
designing proof, or editing code before recording the selection boundary, it
has rushed past the facet.

## 15. Candidate Runtime Budget

| Candidate | Must Include / Optional / Support-Only / Avoid | Why | Drop Or Demote If |
| --- | --- | --- | --- |
| One selected issue-equivalent item | Must Include | Core output of the facet. | Never for this facet. |
| Repo-visible ordering or explicit user target | Must Include | Prevents invented priority/readiness. | Never; exact syntax can move to docs. |
| Tracker-state eligibility | Must Include | Prevents explicit targets from bypassing readiness. | Only if merged into selection authority without losing no-substitution behavior. |
| Explicit-target no-substitution | Must Include | Keeps named-but-ineligible work from being silently replaced. | Never unless `implement` stops supporting explicit targets. |
| Local readiness recheck | Must Include | Prevents label-only pickup. | Only if all sub-gates stay visible elsewhere. |
| Agent-prompt adequacy | Must Include | Strongest agent-specific clarity gate. | Only if local readiness explicitly includes fresh-agent usability. |
| Observable done signal | Must Include | Prevents unverifiable pickup. | Only if merged into prompt adequacy without loss. |
| Blocker/dependency check | Must Include | Prevents starting in the wrong order. | Never; syntax can move to repo docs. |
| Result-defining ambiguity | Must Include | Prevents invented requirements without timid asking. | Only if explicitly covered by prompt adequacy. |
| No-ready stop | Must Include | Stops `implement` from creating work. | Never for this facet. |
| PRD/spec without one issue route | Must Include | Prevents whole-document implementation. | Only if another branch handles source documents. |
| Owner-boundary stop | Must Include | Prevents issue repair, splitting, planning, and tracker mutation. | Never; this protects workflow boundaries. |
| Select first, plan later | Must Include | Handoff boundary to Context Intake. | Only if flow order makes it impossible to miss. |
| Risk-domain confirmation | Optional | Useful high-risk pickup guard. | If engineering contract reliably handles it earlier. |
| Obvious multi-issue smell | Optional | Useful early scope rejection. | If candidate runtime draft gets crowded or Bounded Slice Control absorbs it. |
| Kanban/WIP/DoR/INVEST/Scrum source terms | Support-Only | Useful rationale but too heavy for runtime. | Always demote from runtime unless needed as support pointer. |
| Tracker command syntax | Avoid | Repo docs own exact syntax. | Revive only in tracker docs. |
| Full proof strategy | Avoid | Semantic Proof owns this. | Revive in proof facet. |
| Issue repair/splitting/promotion steps | Avoid | `triage` / `to-tickets` own this. | Revive in those skills. |

## 16. Candidate Draft Contract

| Preserve | May Compress | Must Not Carry Forward | Why |
| --- | --- | --- | --- |
| One selected issue-equivalent item | Support terms like pull/WIP | Batch, queue, project as valid selected item | Core selection must stay singular. |
| Repo-visible ordering or explicit user target | Exact ready/order syntax into tracker-doc pointer | "Looks ready", "most important", agent-chosen priority | Selection authority is not agent preference. |
| Tracker-state eligibility | Exact state names into tracker-doc pointer | Label editing, state mutation, or implicit substitution | Eligibility is runtime; syntax and mutation are not. |
| Explicit-target no-substitution | Short stop gate | Quietly choosing another issue after named item fails | Explicit targets must fail visibly if not eligible. |
| Local readiness recheck | DoR rationale into support | Full DoR / INVEST checklist | Recheck must stay small and selection-owned. |
| Agent-prompt adequacy and observable done signal | Fold under readiness if both facts remain visible | Full proof plan or file-design requirement | Selection needs startability and success shape only. |
| Blocker/dependency check | Tracker-specific terms into support | Dependency metadata edits | Detecting blockers is runtime; mutation is not. |
| Result-defining ambiguity | Underspecification rationale into support | Generic "ask if unsure" | Ask only when correctness would change. |
| Risk-domain confirmation | Repo-policy pointer | Inline risk policy | Exact thresholds belong to contract/docs. |
| Obvious multi-issue smell | Demote to support if too crowded | Slicing or decomposition procedure | Selection can reject broad work, not split it. |
| Select first, plan later | Short handoff phrase | File discovery, planning, proof strategy, edits | Context Intake owns the next phase. |
| Owner boundaries | Short owner-handoff notes | Issue creation, issue repair, splitting, promotion, relabeling | Prevents `implement` from taking over neighboring skills. |

## 17. Candidate Runtime Draft Handoff

Synthesis decision: `ready-for-candidate-runtime-draft`

Chosen behavior:

- Resolve the candidate surface.
- Lock exactly one issue-equivalent item.
- Apply selection authority from repo-visible order or explicit user target.
- Check tracker-state eligibility when the item is a tracker item.
- Run a compact local readiness recheck.
- Ask/stop/handoff on named branch conditions.
- Record selection facts before Context Intake.

Strongest leading words:

- one selected issue-equivalent item;
- repo-visible ordering or explicit user target;
- tracker-state eligibility;
- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity;
- select first, plan later.

Candidate behavior fragments:

- "Select exactly one issue-equivalent item before Context Intake."
- "Use repo-visible ordering or an explicit user target; do not invent
  priority."
- "For tracker items, check eligible ready state; do not mutate tracker state."
- "If an explicit target is not eligible, stop on that target; do not silently
  substitute another issue."
- "Run a local readiness recheck: prompt adequacy, done signal, blockers, and
  result-defining ambiguity."
- "A PRD/spec/path is not implementation scope until one ready item is named."
- "Detect unready work; do not repair, relabel, split, promote, or mutate it."
- "Ask only on named gates: order, blocker, result-defining ambiguity, risk, or
  missing target item."
- "Record selected item, authority, eligibility/readiness facts, and branch
  outcomes before planning."

Candidate runtime budget:

- Must include: one item, selection authority, tracker-state eligibility,
  explicit-target no-substitution, readiness recheck, agent-prompt adequacy,
  done signal, blocker/dependency, result-defining ambiguity, no-ready stop,
  PRD/spec stop, owner-boundary stop, select first / plan later.
- Optional: risk-domain confirmation, obvious multi-issue smell, checked-surface
  reporting.
- Support-only: pull/WIP, DoR, INVEST, Scrum, Small CLs, source examples.
- Avoid: tracker syntax, tracker mutation, issue repair, issue splitting, proof
  strategy, planning, review behavior.

Traceability from fragments to agent-bridge steps or gates:

- one item -> Steps 1-2 and hard gate;
- selection authority -> Step 3 and hard gate;
- tracker-state eligibility and no-substitution -> Step 3 / Branch B11;
- readiness recheck -> Step 4 and hard gate;
- risk/size smells -> Step 5 and recheck branches;
- selection facts before planning -> Step 6 and handoff;
- named asks -> Branches B1-B11.

Gate consequences to preserve:

- No one issue-equivalent item, no implementation.
- No visible authority, no selection.
- No eligible tracker state, no pickup.
- Named but ineligible target stops on that target.
- No prompt adequacy or done signal, no pickup.
- Blocked work waits unless the selected item is the blocker.
- Result-defining ambiguity requires a user/upstream answer.
- Detect unready work; do not make it ready.
- Record selection facts before planning.

Support/reference pointers needed:

- repo tracker docs for ready labels, ordering fields, state semantics, and
  dependency syntax;
- support examples for agent-prompt adequacy and blocker/dependency checks;
- support rationale for pull/WIP and DoR/stage-gate contrast;
- engineering contract or repo docs for exact high-risk policy.

Support pointer shapes:

- short runtime pointer for tracker docs;
- short runtime pointer or support reference for risk policy;
- support/reference section for source rationale and examples;
- later-facet pointer for Context Intake and Semantic Proof.

What stays research-only:

- Kanban metrics and cadences;
- Scrum ceremonies and roles;
- full DoR / INVEST checklist mechanics;
- SWE-bench scoring methodology;
- Copilot platform setup;
- detailed Small CL splitting tactics.

Repeated meanings Prompt 08 should collapse:

- pull / WIP / capacity -> one selected issue-equivalent item;
- ready marker / explicit policies -> repo-visible ordering or explicit user
  target;
- ready-for-agent / needs-info / closed examples -> tracker-state eligibility
  plus tracker-doc pointer;
- issue as prompt / well-scoped / clear enough -> agent-prompt adequacy;
- acceptance criteria / testable / done when -> observable done signal;
- underspecified / vague / unclear -> result-defining ambiguity;
- blocked by / blocking / unresolved dependency -> blocker/dependency check.

Validation scenario seeds to remember:

- explicit named issue is eligible and proceeds;
- explicit named issue is ineligible and stops without substitution;
- no issue provided and exactly one next unblocked `ready-for-agent` item exists;
- multiple eligible items exist with no visible order;
- PRD/spec/path lacks one ready issue-equivalent item;
- ready-labeled item is prompt-poor or lacks done signal;
- candidate has an unresolved blocker;
- candidate has result-defining ambiguity;
- candidate is obviously multi-issue or high risk;
- selection facts are recorded before Context Intake or planning.

Biggest candidate-drafting risk:

- Compressing this to "pick a ready issue" would erase the useful behavior.
  Prompt 08 must preserve one selected issue-equivalent item, visible selection
  authority, tracker-state eligibility, explicit-target no-substitution,
  compact readiness facts, named stop/ask gates, and the select-first /
  plan-later boundary.
