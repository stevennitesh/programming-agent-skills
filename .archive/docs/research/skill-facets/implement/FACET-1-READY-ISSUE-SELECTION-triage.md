# Prompt 05: Source Triage For Implement Facet 1

Historical source-to-skill Prompt 05 artifact for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Facet research question: How should `implement` select exactly one ready issue
or stop when no safe issue is available?

Source search packet:
[`FACET-1-READY-ISSUE-SELECTION-sources.md`](FACET-1-READY-ISSUE-SELECTION-sources.md)

Source extraction packet:
[`FACET-1-READY-ISSUE-SELECTION-extraction.md`](FACET-1-READY-ISSUE-SELECTION-extraction.md)

Extraction decision: `ready-for-triage`

Revision feedback:

- Rerun Prompt 05 from the refreshed Prompt 04 extraction packet.
- Use three subagents to check runtime-priority triage, owner-boundary pruning,
  and bridge / duplicate collapse.

Subagent inputs used:

- Runtime priority pass: keep the facet small; preserve one-item pickup,
  repo-visible ordering, agent-prompt adequacy, blockers, result-defining
  ambiguity, local readiness, and selection-before-planning.
- Owner-boundary pass: keep only selection gates; route issue creation,
  readiness repair, tracker mutation, splitting, proof, review, and policy
  details to their owners.
- Bridge / duplicate pass: collapse source terms into `one selected
  issue-equivalent item`, `local readiness recheck`, `agent-prompt adequacy`,
  `observable done signal`, `result-defining ambiguity`, and
  `blocker/dependency check`.

## 1. Triage Scope

This triage covers the source material for the `Ready Issue Selection` facet:
the pre-implementation decision to select exactly one issue-equivalent work
item or stop before coding begins.

Source lanes represented:

- delivery / WIP / pull-system guidance;
- Scrum ready-for-selection language;
- AI-agent task-fit guidance;
- tracker blocker/dependency semantics;
- readiness contrast material;
- reviewability and sensitive-work cautions.

Out of scope:

- creating, rewriting, splitting, promoting, or relabeling issues;
- exact tracker command syntax, state names, labels, or dependency metadata
  mutation;
- full Context Intake, domain reading, or file discovery after selection;
- implementation planning, proof design, review, commit, or issue-note behavior;
- final runtime `SKILL.md` wording.

Over-keeping would mean carrying source methodology into runtime, making
`implement` perform `triage` or `to-issues`, requiring complete upfront design,
or preserving interesting Agile/Kanban/Copilot theory that does not change the
select / ask / stop decision.

## 2. Prompt 04 Handoff Check

| Prompt 04 Input | Used / Revised / Deferred / Rejected | Triage Consequence | Notes |
| --- | --- | --- | --- |
| Extraction decision: `ready-for-triage` | Used | Continue to Prompt 06 after triage. | The extraction has enough behavior, gates, and misuse risks. |
| Claim-strength labels | Used | Direct and cross-source behavior gets priority; bridge material must be translated. | Thin and cross-facet claims are demoted unless they affect selection. |
| Extraction target coverage | Used | All core families were triaged: one item, repo/user authority, readiness, prompt adequacy, blockers, ambiguity, no-ready stop, and PRD/spec handoff. | No source-search rerun needed. |
| Boundary-drift notes | Used | Owner conflicts are the main pruning pressure. | `triage`, `to-issues`, Context Intake, Bounded Slice Control, Semantic Proof, Review/Lock, tracker docs, and engineering contract stay separate. |
| Extraction gaps: ambiguity papers / Linear source | Deferred | Not needed for this behavior-flow pass. | The current source set is sufficient for pragmatic source triage. |
| File-direction uncertainty | Revised | File hints are optional support for prompt adequacy, not a readiness gate. | Context Intake owns deeper file discovery. |
| Sensitive-work uncertainty | Revised | Keep a generic risk confirmation smell; defer exact policy to repo docs / engineering contract. | Prompt 06 should not define a security or compliance policy. |
| DoR / INVEST uncertainty | Rejected for runtime | Keep only the translated local readiness recheck and obvious size/testability smells. | Named DoR/INVEST language attracts issue-authoring drift. |
| Google Small CL uncertainty | Deferred / support | Keep only an obvious multi-issue smell. | Detailed slicing belongs to Bounded Slice Control. |
| Prompt 05 triage-first suggestions | Used | Runtime candidates are compacted to "issue as prompt" plus observable done signal, blocker/dependency check, and owner-boundary stops. | This is the clean pile for Prompt 06. |

## 3. Keep / Reject Standard

- Keep material only when it changes whether the agent selects one work item,
  asks, stops, or routes to another owner.
- Keep runtime gates only if they are checkable before Context Intake: issue
  identity, eligibility authority, minimal readiness, prompt adequacy,
  observable done signal, blocker/dependency state, result-defining ambiguity,
  and risk smell.
- Demote source vocabulary when the behavior is clearer than the method name:
  keep the gate, not the ceremony.
- Put rationale, methodology, examples, and source-specific terms in support or
  research rather than final runtime flow.
- Treat issue creation, readiness repair, splitting, planning, proof, review,
  tracker syntax, and exact risk policy as owned elsewhere.

## 4. Leading Word Triage

| Term | Source | Category | Why | Behavior It Can Steer | Risk If Kept | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Pull | Kanban Guide | keep-support | Useful rationale for one-item pickup. | Select from the ready surface rather than grabbing a batch. | Could import Kanban ceremony. | move to support |
| WIP limit | Kanban Guide / DORA | keep-support | Explains why one issue matters. | Bound the session to one implementation item. | Adds process jargon. | move to support |
| One selected issue-equivalent item | Extraction bridge | keep-runtime | Plain behavior version of pull/WIP. | Name exactly one issue, URL, path, or ready slice. | None if kept concrete. | keep for behavior flow |
| Explicit policies | Kanban Guide | bridge-needed | Good source pressure, but the runtime term should be repo-visible authority. | Follow repo-owned ready/order/blocker rules. | Could drift into policy editing. | translate before keeping |
| Repo-visible ordering | Scrum Guide / DORA / extraction bridge | keep-runtime | Prevents invented priority. | Use tracker/repo order or ask. | Could be too vague if no source is named. | keep for behavior flow |
| Ready for selection | Scrum Guide | keep-support | Helpful boundary phrase, but runtime should say selectable enough. | Selection proves pickability, not full understanding. | Could import Scrum ceremony. | move to support |
| Local readiness recheck | Extraction bridge | keep-runtime | Compact behavior extracted from readiness sources. | Check clear work, done signal, and no obvious blocker/dependency. | Could become full Context Intake. | keep for behavior flow |
| Issue as prompt | GitHub Copilot docs | keep-support | Strong source phrase, but final behavior should use agent-prompt adequacy. | Judge whether issue text can guide a fresh coding agent. | Could drift into issue rewriting. | move to support |
| Agent-prompt adequacy | Extraction bridge | keep-runtime | Best agent-executable term. | Reject title-only or prompt-poor issues. | Could over-require perfect issue text. | keep for behavior flow |
| Acceptance criteria | GitHub Copilot / VS Code docs | keep-support | Useful source phrase. | Reminds that a success signal is needed. | Formal AC may be too strict. | move to support |
| Observable done signal | Extraction bridge | keep-runtime | Plain runtime gate. | Require at least one expected behavior, proof hint, repro, doc target, or done condition. | Could drift into proof design. | keep for behavior flow |
| Underspecified | SWE-bench Verified | keep-support | Good research word for hidden missing detail. | Warns against invented requirements. | Benchmark framing is too heavy. | move to support |
| Result-defining ambiguity | Extraction bridge | keep-runtime | Precise stop condition. | Ask only when missing detail changes the expected result. | Could be missed if phrased too abstractly. | keep for behavior flow |
| Blocked by / blocking | GitHub issue dependencies | keep-support | Source-specific terms are useful examples. | Detect dependency order problems. | Could become GitHub-only. | move to support |
| Blocker/dependency check | Extraction bridge | keep-runtime | Tracker-neutral behavior. | Do not pick blocked work unless selecting the blocker itself. | Could drift into tracker mutation. | keep for behavior flow |
| Definition of Ready | Agile Alliance / Mountain Goat | keep-support | Useful rationale only. | Supports small pickup-readiness recheck. | Pulls `implement` into `triage`. | move to support |
| Stage gate | Mountain Goat | keep-support | Useful warning against over-checking. | Do not demand complete design before selection. | Too meta for runtime. | move to support |
| Self-contained change | Google Small CLs | keep-support | Helpful size smell. | Flag obviously multi-issue candidates. | Mostly belongs to Bounded Slice Control. | move to support |
| Obvious multi-issue smell | Extraction bridge | keep-runtime | Selection can notice unsafe scope without slicing it. | Stop/route when the candidate cannot plausibly be one issue. | Could become decomposition. | keep for behavior flow |
| Sensitive / consequential | GitHub Copilot docs / Copilot Agents card | bridge-needed | Useful risk cue, but exact policy is repo-owned. | Ask for confirmation before high-risk pickup. | Could define policy in the wrong place. | translate before keeping |

## 5. Behavior Rule Triage

| Rule | Source | Category | Why | Operational Gate | Failure Prevented | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Pull one ready item, not a batch. | Kanban Guide / DORA | keep-runtime | Core facet behavior. | Exactly one issue-equivalent item is named. | Multi-issue drift. | keep for behavior flow |
| Use repo-visible ordering when no issue is named. | Scrum Guide / DORA | keep-runtime | Prevents agent-invented priority. | One candidate is selected by repo/user authority. | Silent prioritization. | keep for behavior flow |
| Treat readiness as policy-backed, not label-only. | Kanban Guide / readiness sources | keep-runtime | Catches false-ready labels. | Ready marker or explicit user target plus no contradiction. | Blind pickup. | keep for behavior flow |
| Recheck whether the issue can function as an agent prompt. | GitHub Copilot docs | keep-runtime | Strongest agentic pickup gate. | Clear requested work plus success shape. | Prompt-poor implementation. | keep for behavior flow |
| Require an observable done signal before pickup. | GitHub Copilot / VS Code / Codex docs | keep-runtime | Later proof needs a target, but full proof is later. | A test hint, expected behavior, repro, docs target, or explicit done condition exists. | Unverifiable work. | keep for behavior flow |
| Treat result-defining underspecification as no-pick. | SWE-bench Verified / VS Code docs | keep-runtime | Prevents invented requirements. | Missing detail would change the expected result. | Guessing product intent. | keep for behavior flow |
| Treat open blockers as selection stops. | GitHub issue dependencies / DJAA | keep-runtime | Prevents dependency-order violations. | No unresolved blocker, or the blocker itself is selected. | Starting blocked work. | keep for behavior flow |
| Do not repair readiness inside `implement`. | Facet boundary / readiness contrast | keep-runtime | Hard owner boundary. | No issue creation, rewrite, promotion, relabel, or dependency edit occurs. | `implement` taking over `triage` / `to-issues`. | keep for behavior flow |
| Separate selection from planning. | Scrum Guide / GitHub Copilot docs | keep-runtime | Prevents facet collapse. | Selection output records identity and readiness facts only. | Context Intake or planning starts too early. | keep for behavior flow |
| Stop on broad, ambiguous, sensitive, or deeply domain-heavy tasks. | GitHub Copilot docs / Copilot Agents card | keep-runtime | Useful poor-task-shape gate. | User narrows, confirms, or selects a different issue. | Unsafe autonomous pickup. | keep for behavior flow |
| Do not hide blocked work by pulling more. | DJAA / DORA | keep-support | Good rationale for active-work discipline, but may need session/tracker context. | Existing active blocked work is surfaced. | Hidden WIP expansion. | move to support |
| Use self-contained/reviewable size only as a smell. | Google Small CLs | keep-runtime | Selection can reject obvious scope explosions. | Candidate plausibly fits one coherent issue-equivalent item. | Whole-spec implementation. | keep for behavior flow |

## 6. Failure Mode Triage

| Failure Mode | Source | Category | Why | Skill Countermeasure | Evidence / Warning Sign | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Queue grabbing | Kanban Guide / DORA | keep-runtime | Selection can directly prevent it. | Enforce exactly one selected issue-equivalent item. | Plural selected work, "also", or queue sweep. | keep for behavior flow |
| Label-only readiness | Scrum / readiness sources | keep-runtime | The facet must catch this before ownership. | Minimal readiness recheck. | Ready marker but unclear work, no done signal, or blocker contradiction. | keep for behavior flow |
| Prompt-poor issue | GitHub Copilot docs | keep-runtime | Directly affects agent pickup safety. | Ask or route upstream. | Vague title, no outcome, no success shape. | keep for behavior flow |
| Underspecified task | SWE-bench Verified | keep-runtime | Agent would invent the intended result. | Stop on result-defining ambiguity. | Expected behavior cannot be inferred. | keep for behavior flow |
| Silent prioritization | Scrum / DORA / Kanban | keep-runtime | The agent does not own priority. | Use repo-visible order or ask. | Multiple eligible candidates and no order. | keep for behavior flow |
| Upstream takeover | Facet boundary / DoR contrast | keep-runtime | Hard boundary with `triage` and `to-issues`. | Stop with owner handoff. | Issue rewrite, relabel, split, or promotion begins. | keep for behavior flow |
| Oversized pickup | GitHub Copilot docs / Google Small CLs | keep-runtime | Selection should catch obvious non-issues. | Ask to narrow, split upstream, or select a smaller issue. | Broad refactor/spec or many unrelated areas. | keep for behavior flow |
| Selection-as-planning | Scrum / GitHub Copilot docs | keep-runtime | Prevents Prompt 06 from merging facets. | Lock issue identity before design. | Code plan appears before issue identity is settled. | keep for behavior flow |
| Hidden WIP | DORA / DJAA | keep-support | Useful, but active-work detection may be repo/session-specific. | Surface existing active or blocked work when visible. | Dirty branch, active issue, or blocked work ignored. | move to support |
| Checklist overreach | Mountain Goat | keep-support | Good warning against stage-gate behavior. | Keep recheck minimal. | Agent demands complete design/file list/proof plan. | move to support |
| Sensitive autonomous pickup | GitHub Copilot docs / Copilot Agents card | keep-runtime | Selection should not silently enter high-risk work. | Ask for explicit boundaries. | Security, PII, auth, incident, production-critical, regulated, or consequential signals. | keep for behavior flow |

## 7. Evidence Gate Triage

| Gate | Source | Category | Why | Too Weak If | Too Heavy If | Action |
| --- | --- | --- | --- | --- | --- | --- |
| One selected work item | Kanban Guide / DORA | keep-runtime | Core completion gate for the facet. | It names a project, queue, PRD, or list. | It decomposes a whole source document. | keep for behavior flow |
| Repo-ready marker or explicit user target | Kanban / Scrum / readiness sources | keep-runtime | Establishes authority without inventing priority. | It relies on "looks ready." | It mutates tracker state. | keep for behavior flow |
| Local readiness recheck | Scrum / DoR / GitHub docs | keep-runtime | Catches false-ready pickup. | It checks only a label. | It performs full Context Intake. | keep for behavior flow |
| Agent-prompt adequacy | GitHub Copilot docs | keep-runtime | Directly tests whether the item can guide an agent. | A title alone is accepted for nontrivial work. | Exact file paths or complete design are required. | keep for behavior flow |
| Observable done signal | GitHub Copilot / VS Code / Codex docs | keep-runtime | Needed for later verification without doing proof design now. | It accepts "make better." | It requires a full test plan before pickup. | keep for behavior flow |
| Result-defining ambiguity check | GitHub Copilot / SWE-bench Verified / VS Code docs | keep-runtime | Prevents invented requirements without blocking ordinary unknowns. | Vague result-changing gaps pass. | Every implementation unknown blocks selection. | keep for behavior flow |
| Blocker/dependency check | GitHub issue dependencies / DJAA | keep-runtime | Prevents starting in the wrong order. | Textual blockers are ignored. | Agent edits dependency metadata. | keep for behavior flow |
| Risk-domain check | GitHub Copilot docs / Copilot Agents card | keep-runtime | Pickup should not be silently high-risk. | Obvious risk terms are missed. | It defines full security/compliance policy. | keep for behavior flow |
| Reviewable-size smell | Google Small CLs | keep-runtime | Useful only for obvious whole-spec or multi-issue candidates. | It ignores clearly oversized scope. | It starts slice planning. | keep for behavior flow |
| Owner-boundary check | Facet map / extraction | keep-runtime | Keeps selection from taking over other skills. | It permits issue creation or planning. | It refuses selectable work due to missing full understanding. | keep for behavior flow |

## 8. Stop / Ask Rule Triage

| Condition | Source | Category | Why | Agent Should | Resume When | Action |
| --- | --- | --- | --- | --- | --- | --- |
| More than one eligible issue and no clear order | Scrum Guide / DORA / Kanban Guide | keep-runtime | Priority is not agent-owned. | Use repo order or ask user to choose. | One issue is selected. | keep for behavior flow |
| No ready issue-equivalent item exists | Kanban Guide / DORA | keep-runtime | `implement` must not relax readiness to stay busy. | Stop and report the checked surface. | User provides a ready issue or invokes upstream workflow. | keep for behavior flow |
| Candidate is blocked by unresolved work | GitHub issue dependencies / DJAA / Mountain Goat | keep-runtime | Starting blocked work violates dependency order. | Skip, stop, or ask whether to work the blocker. | Blocker is resolved or selected. | keep for behavior flow |
| Candidate has result-defining ambiguity | GitHub Copilot docs / SWE-bench Verified / VS Code docs | keep-runtime | Agent would invent requirements. | Ask or route upstream. | Missing result-defining detail is supplied. | keep for behavior flow |
| User supplies PRD/spec without one ready issue | Facet boundary / Scrum Guide | keep-runtime | A source document is not automatically one implementation unit. | Ask for target issue or route to `to-issues`. | One ready issue-equivalent slice is named. | keep for behavior flow |
| Candidate is broad, context-rich, deeply domain-heavy, or multi-slice | GitHub Copilot docs / VS Code docs | keep-runtime | Poor autonomous task shape. | Ask to narrow, split upstream, or confirm route. | Scope is narrowed to one ready issue. | keep for behavior flow |
| Candidate touches sensitive or critical domains | GitHub Copilot docs / Copilot Agents card | keep-runtime | High-risk work needs explicit oversight. | Ask for confirmation and boundaries. | User confirms and provides guardrails. | keep for behavior flow |
| Readiness recheck would require issue state/content changes | Agile Alliance / Mountain Goat / facet boundary | keep-runtime | That is triage or issue creation, not selection. | Stop and route to owner. | Issue is made ready upstream or another issue is selected. | keep for behavior flow |
| Selection starts becoming implementation planning | Scrum Guide / GitHub Copilot docs | keep-runtime | Planning belongs after identity is locked. | Stop planning and record selection facts only. | Issue identity and readiness facts are clear. | keep for behavior flow |

## 9. Agentic Bridge Triage

| Source Concept | Agentic Translation | Category | Why | Agent Bridge Candidate | Action |
| --- | --- | --- | --- | --- | --- |
| WIP limit / pull | The session may own one implementation item. | keep-runtime | Behavior matters more than process acronym. | Select exactly one issue-equivalent item. | translate before keeping |
| Pull criteria / explicit policies | Candidate is eligible by repo-visible policy or explicit user target. | keep-runtime | Avoids invented readiness or priority. | Check authority before ownership. | translate before keeping |
| Ready for selection | Selectable now, fully understood later. | keep-runtime | Crucial facet boundary. | Lock identity before Context Intake. | keep for behavior flow |
| Issue as prompt | Issue text plus repo-local context can guide a fresh agent. | keep-runtime | Strongest task-fit bridge. | Check agent-prompt adequacy. | translate before keeping |
| Acceptance criteria / testable | There is an observable done signal. | keep-runtime | Avoids formal AC overreach. | Require expected behavior, proof hint, repro, doc target, or done condition. | translate before keeping |
| Underspecified problem statement | Missing detail changes the expected result. | keep-runtime | Prevents invented requirements. | Stop on result-defining ambiguity. | translate before keeping |
| Blocked by / blocking | Candidate has unresolved prerequisite work. | keep-runtime | Tracker-neutral dependency behavior. | Do not pick blocked work unless selecting the blocker. | translate before keeping |
| Definition of Ready | Small pickup recheck, not readiness promotion. | keep-support | Good rationale; bad runtime term. | Clear, feasible, unblocked, done-signal enough. | move to support |
| Stage gate | Warning against demanding complete design. | keep-support | Prevents over-checking. | Keep recheck minimal. | move to support |
| Self-contained change | Obvious multi-issue smell. | keep-runtime | Selection can reject obvious non-slices. | Ask to narrow or route upstream. | translate before keeping |
| Human oversight | Risky pickup needs explicit user boundaries. | keep-runtime | Generic caution belongs here; exact policy does not. | Ask before sensitive/critical autonomous work. | translate before keeping |

## 10. Bridge Resolution Plan

| Item | Raw Source / Bridge Term | Plain Behavior Translation | Keep / Support / Drop If | Prompt 06 Input |
| --- | --- | --- | --- | --- |
| One-item selection | Pull / WIP / capacity | Select exactly one issue-equivalent item before doing anything else. | Keep runtime unless duplicated exactly. | First behavior node: identify one candidate or stop. |
| Selection authority | Pull criteria / explicit policies / ordering | Candidate comes from repo-visible ready/order policy or explicit user selection. | Keep runtime; support explains source rationale. | Candidate discovery and eligibility node. |
| Selectable vs understood | Ready for selection / stage-gate contrast | Selection proves pickability; Context Intake proves understanding. | Keep runtime boundary. | Boundary node before context reading. |
| Agent-prompt adequacy | Issue as prompt / well-scoped | The issue can guide a fresh agent without hidden product decisions. | Keep runtime; file paths optional. | Local readiness recheck node. |
| Done signal | Acceptance criteria / testable / what good looks like | At least one success/proof hint exists. | Keep runtime; drop formal AC requirement. | Local readiness recheck node. |
| Result-defining ambiguity | Underspecified / ambiguous task | Stop only when missing detail changes what should be built. | Keep runtime; ordinary unknowns move to Context Intake. | Stop/ask branch. |
| Blocker/dependency | Blocked by / blocking | Do not pick blocked work unless the selected item is the blocker itself. | Keep runtime; support can show tracker examples. | Stop/ask branch. |
| Risk confirmation | Human oversight / sensitive work | Ask before autonomous pickup of sensitive, critical, or consequential work. | Keep runtime as generic smell; defer exact policy. | Stop/ask branch. |
| Obvious size smell | Self-contained / Small CLs / INVEST small | Stop or route if the candidate is plainly multi-issue. | Keep runtime only as smell. | Optional guard after readiness check. |

## 11. Owned-Elsewhere Check

| Item | Better Owner | Conflict Severity | Why | Keep Reference? |
| --- | --- | --- | --- | --- |
| Creating issues from PRDs/specs | `to-issues` | hard-boundary | `implement` needs one issue-equivalent item, not a decomposition workflow. | Yes, as stop/owner note. |
| Rewriting, splitting, promoting, or relabeling issues | `triage` / `to-issues` | hard-boundary | Selection can detect unready work but must not make it ready. | Yes, as stop/owner note. |
| Exact tracker commands, labels, and dependency metadata edits | Repo tracker docs | hard-boundary | Local docs own syntax and mutations. | Yes, semantic reference only. |
| Exact priority choice among several ready issues | User / repo tracker docs | hard-boundary | Product priority is not agent-owned. | Yes, use visible order or ask. |
| Full acceptance-criteria repair | `triage` / Context Intake | hard-boundary | Selection needs only a success signal. | Minimal reference only. |
| File discovery and right-context gathering | Context Intake | later-facet-watchpoint | Helpful after identity is locked. | Optional support only. |
| Implementation design and planning | Context Intake / later `implement` facets | hard-boundary | Planning before selection causes premature scope. | Keep "defer planning" only. |
| Detailed story splitting / INVEST | `to-issues` / `triage` | hard-boundary | Issue authoring and slicing are upstream. | No runtime reference. |
| Detailed size and slice management | Bounded Slice Control | later-facet-watchpoint | Selection only catches obvious multi-issue smell. | Support only. |
| Full proof strategy and tests | Semantic Proof | later-facet-watchpoint | Selection only needs a done signal. | Minimal support only. |
| Review / human evaluation after implementation | Review And Lock / `$review` | later-facet-watchpoint | Output review is not selection. | No runtime reference here. |
| Sensitive-domain policy details | Engineering contract / repo docs | soft-reference | Runtime can detect risk; repo owns exact policy. | Generic ask gate only. |
| Kanban metrics, cadences, board design | Research only | research-only | Process background, not selection behavior. | No. |
| Scrum ceremonies and roles | Research only | research-only | Source language is useful; ceremony is not. | No. |
| Copilot setup, MCP, platform configuration | Research only | research-only | Tool setup is outside ready issue selection. | No. |

## 12. Duplicate / Synonym Collapse Check

| Cluster | Candidates | Preferred Carry-Forward | Demote / Merge | Why |
| --- | --- | --- | --- | --- |
| Single-item discipline | Pull, WIP limit, capacity, queue grabbing, one selected work item | One selected issue-equivalent item | Demote pull/WIP/capacity to support; merge queue grabbing as failure mode. | Plain behavior is stronger than process jargon. |
| Selection authority | Explicit policies, repo ordering, highest priority, ready marker, user target | Repo-visible ordering or explicit user target | Demote "highest priority" unless repo-visible. | Agent must not invent priority. |
| Readiness | Ready for selection, Definition of Ready, local readiness recheck, testable enough | Local readiness recheck | Demote DoR and ready-for-selection to support. | Runtime needs a small gate, not methodology. |
| Issue quality | Issue as prompt, well-scoped, well-defined, clear enough, prompt adequacy | Agent-prompt adequacy | Merge well-scoped and clear into prompt adequacy. | Agentic term best predicts behavior. |
| Success criteria | Acceptance criteria, testable, what good looks like, done when | Observable done signal | Demote formal AC wording. | Selection needs a signal, not a full proof plan. |
| Ambiguity | Underspecified, ambiguous, vague, unclear, ask if unsure | Result-defining ambiguity | Reject generic "ask if unsure." | Prevents timidity while stopping invented requirements. |
| Dependencies | Blocked by, blocking, unresolved dependency, blocked work | Blocker/dependency check | Demote tracker-specific words to support examples. | Keeps behavior tracker-neutral. |
| Risk | Sensitive, consequential, human oversight, critical production | Risk-domain confirmation | Merge into generic ask gate. | Exact policy belongs elsewhere. |
| Size | Self-contained, small, reviewable-size smell, INVEST, oversized pickup | Obvious multi-issue smell | Demote detailed Small CL / INVEST material. | Selection can stop obvious scope explosions only. |
| Boundary | Selection-as-planning, selectable vs understood, owner-boundary check | Select first, plan later | Merge as phase boundary. | Prevents overlap with Context Intake. |

## 13. Rejection Log

| Item | Source | Rejection Reason | Do Not Revive Unless |
| --- | --- | --- | --- |
| Full Definition of Ready checklist | Agile Alliance / Mountain Goat | Pulls `implement` into readiness governance and `triage`. | Working on `triage` or repo process docs. |
| Full INVEST matrix | Agile Alliance | Mostly issue-authoring and slicing. | Working on `to-issues` or `triage`. |
| `Definition of Ready` as runtime leading word | Readiness sources | Attracts process ceremony and stage-gate behavior. | A support doc needs rationale language. |
| File paths as required readiness gate | GitHub Copilot docs | Helpful but too strict; agents can discover code during Context Intake. | Evidence shows repeated failures without file hints. |
| Complete upfront design / all details complete | DoR contrast | Creates stage-gate behavior. | Reframed as "enough to select." |
| Exact tracker command syntax | GitHub issue dependencies | Source-specific and repo-owned. | Editing repo tracker docs. |
| Editing dependency metadata | GitHub issue dependencies | Tracker mutation is not selection. | User explicitly asks for tracker maintenance. |
| Kanban metrics, lead time, cadences, board design | Kanban Guide / DORA | Process-management background only. | Designing workflow docs. |
| Scrum ceremony, roles, Sprint Planning mechanics | Scrum Guide | Not agent-executable selection behavior. | Building team process guidance. |
| SWE-bench scoring and benchmark methodology | SWE-bench Verified | Research rationale only. | Researching benchmark design. |
| Copilot setup, MCP, custom agents, platform configuration | GitHub Copilot docs | Tool setup, not selection behavior. | Researching agent platform setup. |
| Detailed Small CL splitting tactics | Google Small CLs | Bounded Slice Control owns split strategy. | Running the slice-control facet. |
| "Pick a suitable issue" | Weak-language notes | Lets agent choose by preference. | Tied to visible ready/order/blocker gates. |
| "Start on the next task" | Weak-language notes | Hides one-item and ordering discipline. | "Next" is defined by repo-visible order. |
| "Make sure it is ready" | Weak-language notes | Not observable. | Replaced by local readiness recheck. |
| "Ask if unsure" | Weak-language notes | Too timid and generic. | Replaced by named stop/ask gates. |
| "Prioritize the most important" | Weak-language notes | Invites invented priority. | Importance comes from repo-visible order or user choice. |

## 14. Surviving Material

### Runtime Candidates: Must Carry Forward

- One selected issue-equivalent item: the facet fails if selection can produce a
  batch, project, PRD, or queue.
- Repo-visible ordering or explicit user target: establishes selection
  authority without invented priority.
- Local readiness recheck: catches false-ready pickup with a small pre-context
  gate.
- Agent-prompt adequacy: the issue must be able to guide a fresh coding agent.
- Observable done signal: the item needs at least one success/proof hint before
  implementation starts.
- Blocker/dependency check: blocked work is not safe to pick unless the selected
  item is the blocker itself.
- Result-defining ambiguity stop: missing information that changes the expected
  result must be supplied or routed upstream.
- No-ready stop: `implement` must stop rather than create its own work.
- PRD/spec without one issue stop: source documents do not become automatic
  implementation scope.
- Owner-boundary stop: if readiness repair, issue mutation, splitting, or
  planning is required, route to the owner.
- Select first, plan later: Prompt 06 must keep source selection separate from
  Context Intake.

### Runtime Candidates: Optional / Supporting Pressure

- Risk-domain confirmation: ask for explicit user boundaries before sensitive,
  critical, or consequential autonomous pickup.
- Obvious multi-issue smell: if the candidate plainly cannot be one coherent
  issue-equivalent item, ask to narrow or route upstream.
- Report searched surface when no ready issue exists: useful evidence if it can
  fit without bloating the flow.
- Hidden active/blocked work caution: useful when the repo/session makes active
  WIP visible.

### Support Candidates

- Kanban pull/WIP rationale: explains why one item matters.
- Scrum ready-for-selection rationale: explains selectable versus fully
  understood.
- Definition of Ready / stage-gate contrast: explains the local recheck and why
  it must stay small.
- GitHub Copilot issue-as-prompt examples: helps explain prompt adequacy.
- SWE-bench Verified underspecification rationale: supports
  result-defining ambiguity as a no-pick condition.
- GitHub issue dependency examples: support tracker-neutral blocker semantics.
- Google Small CL reviewability rationale: supports the obvious multi-issue
  smell.

### Research-Only Material

- Kanban metrics, cadences, board design, lead time, and flow-management theory.
- Scrum roles, ceremonies, Sprint Planning mechanics, and Product Goal details.
- Full DoR / INVEST history and checklist mechanics.
- SWE-bench scoring and benchmark methodology.
- Copilot platform setup, MCP, custom agents, and dependency preinstallation.
- Detailed Small CL splitting tactics.

### Bridge-Needed Material

- Pull / WIP / capacity -> one selected issue-equivalent item.
- Pull criteria / explicit policies -> repo-visible ordering or explicit user
  target.
- Issue as prompt -> agent-prompt adequacy.
- Acceptance criteria / testable -> observable done signal.
- Underspecified -> result-defining ambiguity.
- Blocked by / blocking -> blocker/dependency check.
- Definition of Ready / stage gate -> local readiness recheck plus "keep it
  small."
- Self-contained / INVEST small -> obvious multi-issue smell.
- Human oversight / sensitive task -> risk-domain confirmation.

## 15. Runtime Priority / Budget

| Priority | Candidate | Must / Should / Could | Why | Drop If |
| --- | --- | --- | --- | --- |
| 1 | One selected issue-equivalent item | Must | Core facet output. | Never for this facet. |
| 2 | Repo-visible ordering or explicit user target | Must | Prevents invented priority and invented readiness authority. | Never; exact syntax can move to tracker docs. |
| 3 | Local readiness recheck | Must | Prevents label-only pickup. | Only if another preselection gate explicitly owns it. |
| 4 | Agent-prompt adequacy | Must | Directly tests whether the issue can guide a fresh coding agent. | Only if merged into local readiness recheck. |
| 5 | Observable done signal | Must | Prevents unverifiable pickup. | Only if merged into agent-prompt adequacy. |
| 6 | Blocker/dependency check | Must | Prevents work starting out of order. | Never; tracker syntax may move to docs. |
| 7 | Multiple-candidate order stop | Must | Priority is not agent-owned. | Only if repo ordering is always explicit. |
| 8 | No-ready stop | Must | Preserves `triage` and `to-issues` ownership. | Never for this facet. |
| 9 | PRD/spec without one issue stop | Must | Prevents whole-document implementation. | Only if a separate explicit branch owns PRD/spec handoff. |
| 10 | Result-defining ambiguity stop | Must | Prevents invented requirements. | Only if fully covered by agent-prompt adequacy. |
| 11 | Owner-boundary stop | Must | Prevents readiness repair, tracker mutation, splitting, or planning. | Never; this protects the workflow. |
| 12 | Select first, plan later | Should | Preserves boundary with Context Intake. | If Prompt 06 structure makes it impossible to miss. |
| 13 | Risk-domain confirmation | Should | Avoids silent high-risk autonomous pickup. | If engineering contract reliably owns it before selection. |
| 14 | Obvious multi-issue smell | Could | Useful early warning, but detailed slicing is elsewhere. | If Prompt 06 gets crowded or Bounded Slice Control absorbs it. |
| 15 | Report searched surface when stopping | Could | Improves handoff evidence. | If final response / review facets own reporting. |

## 16. Handoff To Agent Bridge

Triage decision: `ready-for-behavior-flow`

Strongest runtime candidates:

- one selected issue-equivalent item;
- repo-visible ordering or explicit user target;
- local readiness recheck;
- agent-prompt adequacy;
- observable done signal;
- blocker/dependency check;
- result-defining ambiguity stop;
- no-ready and PRD/spec-without-issue stops;
- owner-boundary stop;
- select first, plan later.

Strongest support/reference candidates:

- Kanban pull/WIP rationale;
- ready-for-selection and DoR/stage-gate rationale;
- issue-as-prompt examples;
- underspecification rationale;
- tracker dependency examples;
- Small CL reviewability rationale.

Material that needs bridge translation:

- pull/WIP into one selected issue-equivalent item;
- issue-as-prompt into agent-prompt adequacy;
- acceptance criteria into observable done signal;
- underspecification into result-defining ambiguity;
- blocked-by/blocking into blocker/dependency check;
- DoR/stage-gate into a small local readiness recheck;
- self-contained/INVEST into obvious multi-issue smell;
- human oversight into risk-domain confirmation.

Biggest rejected temptation:

- Turning DoR, INVEST, Kanban, Scrum, or Small CL material into a runtime
  checklist owned by `implement`.

Ownership conflicts to watch:

- `to-issues` owns PRD/spec decomposition.
- `triage` owns ready-state promotion and issue-brief repair.
- Repo tracker docs own exact commands, labels, order fields, and dependency
  metadata.
- Context Intake owns full understanding and file/domain discovery after
  selection.
- Bounded Slice Control owns detailed size and slice management.
- Semantic Proof owns proof strategy.
- Review And Lock owns output review.
- Engineering contract / repo docs own exact high-risk policy.

What Prompt 06 should turn into an execution chain first:

- Resolve candidate source -> select exactly one candidate or stop -> apply
  repo/user authority -> run compact readiness recheck -> stop/ask on blockers,
  result-defining ambiguity, no-ready, PRD/spec without issue, high-risk pickup,
  or owner-boundary collisions -> hand selected issue identity and readiness
  facts to Context Intake.
