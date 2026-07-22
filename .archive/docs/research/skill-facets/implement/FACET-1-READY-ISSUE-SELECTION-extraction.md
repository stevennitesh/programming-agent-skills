# Prompt 04: Source Extraction For Implement Facet 1

Historical source-to-skill Prompt 04 artifact for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Facet research question: How should `implement` select exactly one ready issue
or stop when no safe issue is available?

Source search packet:
[`FACET-1-READY-ISSUE-SELECTION-sources.md`](FACET-1-READY-ISSUE-SELECTION-sources.md)

Recommended source set:

- GitHub Docs: Best practices for using GitHub Copilot to work on tasks:
  <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results>
- The Official Guide to the Kanban Method:
  <https://kanban.university/kanban-guide/>
- DORA: Work in Process Limits:
  <https://dora.dev/capabilities/wip-limits/>
- The 2020 Scrum Guide:
  <https://scrumguides.org/scrum-guide.html>
- GitHub Docs: Creating issue dependencies:
  <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies>
- OpenAI: Introducing SWE-bench Verified:
  <https://openai.com/index/introducing-swe-bench-verified/>
- VS Code Docs: Best practices for using AI in VS Code:
  <https://code.visualstudio.com/docs/agents/best-practices>
- Mountain Goat Software: Definition of Ready and Its Dangers:
  <https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready>

Revision feedback:

- Rerun Prompt 04 from the refreshed Prompt 03 source packet.
- Use three subagents to extract delivery/WIP, agentic-task readiness, and
  tracker/readiness-contrast material.

Subagent inputs used:

- Delivery/WIP extraction: pull, WIP, capacity, explicit policies,
  ready-for-selection, and blocked work.
- Agentic-readiness extraction: issue-as-prompt, well-scoped tasks,
  underspecified issue text, acceptance criteria, ambiguity, and sensitive work.
- Tracker/readiness extraction: `blocked by` / `blocking`, Definition of Ready,
  INVEST, stage-gate danger, and self-contained-change drift.

Constraints:

- Do not rewrite `skills/custom/implement/SKILL.md`.
- Do not decide final runtime wording.
- Do not triage what survives; Prompt 05 owns survival decisions.
- Extract only material that could change Codex behavior.

## 1. Extraction Scope

This extraction covers `Ready Issue Selection`: the part of `implement` that
must select exactly one issue-equivalent work item, or stop before coding starts
when no safe item is available.

Sources in scope represent:

- agentic coding / task-readiness docs;
- delivery/WIP and pull-system guidance;
- Scrum ready-for-selection language;
- tracker blocker/dependency semantics;
- ambiguity and underspecification evidence;
- readiness contrast material.

Intentionally out of scope:

- creating, rewriting, splitting, or promoting issues;
- tracker command syntax and exact label names;
- full context intake after selection;
- implementation planning, proof, review, commit, or issue note behavior;
- final `SKILL.md` wording.

## 2. Prompt 03 Handoff Check

| Prompt 03 Input | Used / Revised / Skipped | Extraction Consequence | Notes |
| --- | --- | --- | --- |
| Recommended source set | Used | Extracted from the 8 recommended sources. | Also used Prompt 03 supporting notes from GitHub Copilot Agents, Agile Alliance/INVEST, DJAA blocked-items, Google Small CLs, and OpenAI Codex where they produced boundary or drift signals. |
| Expected extraction targets | Used | Extracted pull/WIP, agent-ready issue criteria, ready-for-selection, blocker/dependency gates, underspecified-task stops, ambiguity ask rules, and DoR stage-gate caution. | No Prompt 05 survival decision is made here. |
| Source access / extractability | Used | Only inspected public source pages are treated as direct sources. | Book-level Kanban/Lean sources remain unverified and are not extracted. |
| Rejected/thin lanes | Used | Generic DoR blogs, raw templates, tracker command references, and broad PM advice remain excluded. | This keeps the facet from becoming `triage` / `to-issues`. |
| Source-search decision | Used | Prompt 04 proceeds from `ready-for-extraction` to `ready-for-triage`. | Source coverage is sufficient. |
| Coverage warning: DoR overreach | Used | Readiness material is framed as pickup recheck and contrast, not issue authoring. | Prompt 05 should triage this first. |
| Coverage warning: empirical ambiguity papers thin | Used | SWE-bench Verified is extracted as bridge/contrast only. | No new source search needed. |

## 3. Source Coverage

| Source | Prompt 03 Status | Access / Claim Depth | Sections / Docs Used | Why This Part Was Used | Extraction Confidence |
| --- | --- | --- | --- | --- | --- |
| GitHub Copilot task best practices | Core / bridge | Official page inspected | Well-scoped issues; task types; research/planning note | Direct source for issue-as-prompt, agent task fit, and poor autonomous task candidates. | High |
| Kanban Guide | Core | Official page inspected | Limit WIP; Make Policies Explicit; WIP Limits and Pull | Direct source for pull, WIP, explicit policies, and capacity-based selection. | High |
| DORA WIP limits | Core / supporting | Official capability page inspected | Implementation guidance; pitfalls; improvement guidance | Operational source for WIP capacity, highest-priority pull, visible blockers, and anti-multitasking. | High |
| Scrum Guide 2020 | Core | Official guide inspected | Sprint Planning; Product Backlog; Sprint Backlog; Definition of Done | Source for ready-for-selection, transparency, ordering, sizing, and separating selection from planning. | High |
| GitHub issue dependencies | Core / supporting | Official docs inspected | Creating issue dependencies; blocked-by/blocking relationships | Source for tracker-grounded blocker/dependency semantics. | High |
| SWE-bench Verified | Bridge / contrast | Official OpenAI report inspected | Background; adapting SWE-bench; underspecified issue examples | Source for issue text as task input and underspecified/impossible task filtering. | Medium-high |
| GitHub Copilot Agents application card | Supporting / contrast | Official page inspected | Overview; limitations; deployment/adoption best practices | Source for oversight and sensitive/consequential task caution. | Medium-high |
| VS Code AI best practices | Bridge | Official docs inspected | Agent type choice; effective prompts; context and ambiguity guidance | Source for specificity, acceptance criteria, breaking down broad tasks, and clarifying questions. | Medium |
| Agile Alliance DoR / INVEST | Supporting | Glossary pages inspected | Definition of Ready; INVEST | Source for explicit criteria and independent/small/testable pickup signals. | Medium |
| Mountain Goat DoR dangers | Contrast | Professional page inspected | DoR prevents problems; stage-gate risk | Source for dependency caution and warning against rigid readiness gates. | Medium |
| DJAA blocked-items article | Supporting | Professional page inspected | Types of blockers; parking lot; WIP limit discussion | Source for blocked work counting as WIP and not being hidden by more pickup. | Medium |
| Google Small CLs | Cross-facet support | Engineering-practice page inspected | What is Small; one self-contained change | Source for reviewable-size smell only. | Medium |
| OpenAI Codex best practices | Cross-facet support | Official docs inspected | Testing/review; skills scope | Source for "what good looks like" and skill-scoped workflow, mostly later-facet material. | Medium |

## 4. Extraction Target Coverage

| Source | Prompt 03 Target | Extracted / Skipped / Thin | Where It Appears | Notes |
| --- | --- | --- | --- | --- |
| GitHub Copilot task best practices | Well-scoped issue, acceptance criteria, issue-as-prompt, unsuitable task classes | Extracted | Leading Words, Behavior Rules, Failure Modes, Stop / Ask, Agentic Bridge | Strongest agent-ready source. |
| Kanban Guide | Pull, WIP, explicit policies, capacity | Extracted | Leading Words, Behavior Rules, Evidence Gates | Strongest one-item pickup source. |
| DORA WIP limits | Capacity, priority pull, blocked work, anti-multitasking | Extracted | Behavior Rules, Failure Modes, Evidence Gates | Adds operational gates and failure modes. |
| Scrum Guide | Ready-for-selection, transparency, detail/order/size | Extracted | Leading Words, Behavior Rules, Evidence Gates, Boundary Drift | Keeps selection distinct from planning/refinement. |
| GitHub issue dependencies | Blocked-by/blocking semantics | Extracted | Leading Words, Behavior Rules, Stop / Ask | Commands are intentionally not extracted. |
| SWE-bench Verified | Issue text as task input; underspecified task filtering | Extracted | Failure Modes, Evidence Gates, Agentic Bridge | Used as bridge/contrast, not benchmark policy. |
| GitHub Copilot Agents card | Oversight, limitations, sensitive work | Extracted | Stop / Ask, Failure Modes, Drift Notes | Supports risk-gated pickup only. |
| VS Code AI best practices | Specific inputs/outputs, acceptance criteria, ambiguity asks | Extracted | Behavior Rules, Evidence Gates, Weak Language | Mostly bridge material. |
| Agile Alliance DoR / INVEST | Explicit criteria, independent/small/testable | Extracted with caution | Leading Words, Evidence Gates, Drift Notes | Keep to minimal pickup recheck. |
| Mountain Goat DoR dangers | Dependency caution; stage-gate overreach | Extracted | Failure Modes, Stop / Ask, Weak Language | Contrast source. |
| DJAA blocked-items article | Blocked work adds to WIP; escalation policy | Extracted | Failure Modes, Stop / Ask, Drift Notes | Supports blocker stop. |
| Google Small CLs | One self-contained reviewable change | Thin / cross-facet | Evidence Gates, Boundary Drift | Mostly belongs to Bounded Slice Control. |
| OpenAI Codex best practices | What good looks like; scoped skills | Thin / cross-facet | Agentic Bridge, Boundary Drift | More useful later. |

## 5. Leading Words

| Term | Source | Claim Strength | Meaning In Source | Possible Skill Use | Behavior It Should Trigger | Risk / Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| Pull | Kanban Guide | direct | Work enters the active system only when capacity and pull criteria allow it. | Pull exactly one ready issue. | Select one eligible item instead of starting every visible task. | Could become Kanban ceremony if over-extracted. |
| WIP limit | Kanban Guide / DORA | direct | Active work is constrained to improve flow and reduce context switching. | One issue in progress. | Refuse multi-issue pickup. | Full WIP metrics are out of scope. |
| Capacity | Kanban Guide / DORA / Scrum Guide | cross-source | Work can be selected only when the system/team can take it on. | Capacity check before ownership. | Check no active implementation issue is already being carried. | Can wrongly block user-directed issue changes if over-applied. |
| Explicit policies | Kanban Guide | direct | Work policies should be visible, simple, well-defined, consistently applied, and changeable. | Follow repo tracker docs. | Use repo-local ready/order/blocker rules instead of inventing criteria. | `implement` must not rewrite policies. |
| Ready for selection | Scrum Guide | direct | A backlog item is transparent and sufficiently refined to be selected. | Selectable issue. | Treat ready as selectable, not fully planned. | Do not import Sprint Planning ceremony. |
| Ordered | Scrum Guide / DORA | cross-source | Work comes from a visible order or priority source. | Dependency/order gate. | If several issues are ready, use repo ordering or ask. | Agent must not invent product priority. |
| Issue as prompt | GitHub Copilot docs | direct | An assigned issue should be judged by whether it can guide an AI agent. | Prompt-quality issue. | Recheck whether the issue text can guide a fresh coding session. | Do not rewrite the issue here. |
| Well-scoped | GitHub Copilot / VS Code docs | cross-source | A task is bounded, clear, and has a success shape. | Agent-ready issue. | Prefer clear bounded issues and stop on broad/open-ended ones. | Hard work is not automatically unready. |
| Acceptance criteria | GitHub Copilot / VS Code docs | cross-source | Criteria or expected outputs help the AI verify work. | Observable done signal. | Require at least one success/proof hint before pickup. | Full proof belongs to later facets. |
| Underspecified | SWE-bench Verified | direct / bridge | Issue text may be too ambiguous to support reliable agent work. | Ambiguity stop. | Stop/ask when the issue lacks expected behavior or success conditions. | Do not require benchmark-grade issue quality. |
| Blocked by | GitHub issue dependencies | direct | An issue may be marked dependent on another issue being completed. | Blocker stop. | Skip/stop on open blockers unless working the blocker itself. | Do not edit dependency metadata. |
| Blocking | GitHub issue dependencies | direct | An issue may prevent other work from completing. | Dependency-order candidate. | A blocking issue may be the next prerequisite if otherwise ready. | Do not infer priority without tracker/user signal. |
| Definition of Ready | Agile Alliance / Mountain Goat | direct | A shared readiness criterion set before work enters execution. | Local readiness recheck. | Check actionable, clear, feasible, unblocked, testable enough. | Creation/promotion of readiness belongs upstream. |
| Stage gate | Mountain Goat | direct | Readiness rules can become rigid handoff gates requiring complete prior work. | Overreach warning. | Avoid demanding full design/context before pickup. | Too little checking starts unsafe work. |
| Self-contained | Google Small CLs | direct / bridge | A change should address one thing and be understandable. | Selection smell. | Flag obviously oversized/non-coherent issue candidates. | Mostly belongs to Bounded Slice Control. |

## 6. Behavior Rules

| Rule | Source | Claim Strength | Agent Behavior | When It Applies | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- | --- | --- | --- |
| Pull one ready item, not a batch. | Kanban Guide / DORA | cross-source | Select exactly one issue-equivalent work item. | User provides no issue or provides a queue/source. | One issue id, path, URL, or ready spec-derived issue is named. | Multi-issue drift. |
| Use repo-visible ordering when no issue is named. | Scrum Guide / DORA | bridge | Select from the repo's ordered ready queue, not convenience. | Several ready issues exist. | Tracker/docs expose dependency order, priority, milestone, or queue order. | Silent prioritization. |
| Treat readiness as policy-backed, not label-only. | Kanban Guide / Agile Alliance | cross-source | Verify candidate matches repo-local ready policy and a small local recheck. | Any candidate is selected from tracker/docs. | Ready marker or explicit user selection plus no obvious blocker/dependency contradiction. | False-ready pickup. |
| Recheck whether the issue can function as an agent prompt. | GitHub Copilot docs | direct | Confirm issue text can guide a fresh agent. | Before accepting the selected issue. | Clear problem/work required, success shape, and useful area/file/proof hints or local inferability. | Prompt-poor issue execution. |
| Stop on broad, ambiguous, sensitive, or deeply domain-heavy tasks. | GitHub Copilot docs / Copilot Agents card | cross-source | Ask, narrow, or route away instead of autonomous pickup. | Candidate has broad scope, open-ended uncertainty, critical production/security/PII/auth/incident risk, or deep domain/business logic. | User confirms narrowed scope and boundaries, or a different ready issue is selected. | Unsafe autonomous work. |
| Treat underspecification as a no-pick condition when it changes the expected result. | SWE-bench Verified / VS Code docs | bridge | Ask or stop when expected behavior cannot be inferred. | Issue lacks expected behavior, repro, acceptance signal, or success test. | Missing result-defining detail is supplied. | Invented requirements. |
| Do not repair readiness inside `implement`. | Agile Alliance / Mountain Goat / facet boundary | bridge | Reject or hand off unready work instead of rewriting/promoting it. | Selection reveals missing readiness, blocker, or issue-quality problem. | No issue creation, rewrite, relabel, or promotion occurs in this facet. | `implement` taking over `triage` / `to-issues`. |
| Treat open blockers as selection stops. | GitHub issue dependencies / DJAA | cross-source | Do not pick an issue blocked by unresolved work. | Candidate has `blocked by`, linked blocker, or textual blocker. | Blocker is closed/resolved, user explicitly selects blocker issue, or repo policy says it is safe. | Work starts out of dependency order. |
| Do not hide blocked work by pulling more. | DJAA / DORA | cross-source | If active selected work is blocked, surface the block instead of starting another issue. | Existing implementation issue is waiting/blocked. | Blocker state and next owner/decision are explicit. | Hidden WIP expansion. |
| Use self-contained/reviewable size only as a smell. | Google Small CLs | bridge | Flag obviously oversized issue candidates but do not fully slice them. | Candidate appears to require multiple independent changes. | Candidate can plausibly become one coherent diff with related proof, or route upstream. | PRD/spec sweep as one issue. |
| Separate selection from planning. | Scrum Guide / GitHub Copilot docs | cross-source | Lock issue identity and readiness facts before design/planning. | After selecting candidate, before Context Intake. | Selection output names issue and readiness facts only. | Selection facet stealing Context Intake. |

## 7. Failure Modes

| Failure Mode | Source | Claim Strength | What Goes Wrong | Agent Warning Sign | Countermeasure | Evidence Gate |
| --- | --- | --- | --- | --- | --- | --- |
| Queue grabbing | Kanban Guide / DORA | bridge | Agent starts a list because several issues are available. | Selected work is plural or says "also." | Enforce one selected item. | Exactly one issue-equivalent item is named. |
| Hidden WIP | DORA / DJAA | cross-source | Agent ignores existing active/blocked work and starts new work. | Dirty branch, active issue, or blocked issue exists but selection proceeds. | Surface WIP and ask/stop. | Active work status is checked and accounted for. |
| Label-only readiness | Scrum Guide / Agile Alliance | cross-source | A ready label masks missing clarity, blockers, or outcome. | Issue has label but no clear work/success signal. | Run minimal readiness recheck. | Ready marker plus clear work/proof/blocker facts. |
| Prompt-poor issue | GitHub Copilot docs | direct | Issue cannot guide an agent to the intended code change. | Vague title, no outcome, no criteria, or no area hint. | Ask or route to triage. | Issue text can function as a usable prompt. |
| Underspecified task | SWE-bench Verified | bridge | Agent must guess hidden expected behavior. | Missing expected result, ambiguous problem, or test expectation not represented in issue. | Ask for expected behavior or stop. | Missing result-defining detail is supplied. |
| Silent prioritization | Scrum Guide / DORA | bridge | Agent chooses among ready issues without authority. | Multiple matches and no ordering signal. | Ask user or use repo order. | User/repo ordering selects one. |
| Upstream takeover | Agile Alliance / Mountain Goat / facet boundary | bridge | `implement` writes, repairs, splits, promotes, or relabels issues. | Agent starts editing issue brief or state. | Stop with handoff to `to-issues` or `triage`. | No issue creation/state mutation. |
| Oversized pickup | GitHub Copilot docs / Google Small CLs | cross-source | Broad spec/refactor becomes one implementation run. | Candidate spans many unrelated areas or independent changes. | Ask to split or select narrower issue. | Candidate is one self-contained issue-equivalent item. |
| Checklist overreach | Mountain Goat | direct / bridge | Readiness rules demand perfect upfront design and stall executable work. | Agent rejects issue because every detail is not complete. | Keep recheck minimal and local. | Unknowns left are bounded and do not change requested outcome. |
| Sensitive autonomous pickup | GitHub Copilot docs / Copilot Agents card | cross-source | Agent proceeds on high-impact work without confirmation. | Security, PII, auth, incident, regulated, consequential, or production-critical signals. | Ask for explicit authorization and boundaries. | User confirms autonomy or selects different issue. |
| Selection-as-planning | Scrum Guide / GitHub Copilot docs | cross-source | The selection step becomes implementation design. | Agent starts enumerating code changes before issue identity is locked. | Defer to Context Intake/later facets. | Selected issue and readiness facts are recorded only. |

## 8. Evidence Gates

| Gate | Source | Claim Strength | What It Proves | How An Agent Can Check It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- | --- |
| One selected work item | Kanban Guide / DORA | bridge | WIP is bounded before implementation. | Name one issue id/path/URL/spec-derived issue. | It names a project, PRD, or list. | It demands full issue decomposition. |
| Repo-ready marker or explicit user target | Kanban Guide / Scrum Guide | cross-source | Work is eligible for pickup. | Check ready label/state/order docs or user-named issue. | It relies on "looks ready." | It mutates tracker state. |
| Local readiness recheck | Scrum Guide / Agile Alliance / GitHub Copilot docs | cross-source | Candidate can be safely taken into `implement`. | Check clear work, observable done signal, no open blocker, no unresolved dependency. | It checks label only. | It performs full Context Intake. |
| Agent-prompt adequacy | GitHub Copilot docs | direct | Issue text can guide autonomous coding. | Look for problem/work statement, success shape, and useful file/area/proof hints or inferability. | A title alone is accepted for nontrivial work. | Exact file list/design plan is required. |
| Observable done signal | GitHub Copilot / VS Code / Codex docs | cross-source | Agent can later tell success from failure. | Find acceptance criterion, test/proof hint, expected behavior, repro fixed, docs update, or explicit done condition. | It accepts "make better." | It requires complete tests before pickup. |
| Ambiguity check | GitHub Copilot docs / SWE-bench Verified / VS Code docs | cross-source | Selection will not invent requirements. | Scan for open-ended, unclear, uncertainty-driven, or underspecified work. | Vague tasks pass. | Every minor unknown blocks selection. |
| Blocker/dependency check | GitHub issue dependencies / DJAA | cross-source | Work can start in dependency order. | Inspect tracker relationship, issue text, comments, or local packet for `blocked by` / dependency signals. | Textual blockers are ignored. | Agent edits dependency metadata. |
| Risk-domain check | GitHub Copilot docs / Copilot Agents card | cross-source | Sensitive work is not picked up silently. | Scan for production-critical, security, PII, auth, incident, regulated, or consequential work. | Obvious risk terms are missed. | Low-risk maintenance is blocked. |
| Reviewable-size smell | Google Small CLs | bridge | Candidate is plausibly one coherent change. | Check whether likely work has one purpose and related proof. | It uses line count alone. | It starts full slicing/planning here. |
| Owner-boundary check | Facet map / DoR contrast | bridge | Selection has not crossed into other skills. | Confirm no issue creation, promotion, relabeling, implementation plan, or code edit happened. | It says "ready enough" without owner check. | It refuses user-named ready issues due to missing full context. |

## 9. Stop / Ask Conditions

| Condition | Source | Claim Strength | Why It Matters | Agent Should | Resume When |
| --- | --- | --- | --- | --- | --- |
| More than one eligible issue and no clear order | Scrum Guide / DORA / Kanban Guide | bridge | Priority is a product/workflow decision. | Ask user or use repo ordering if available. | One issue is selected. |
| No ready issue-equivalent item exists | Kanban Guide / DORA | bridge | `implement` should not broaden criteria to stay busy. | Stop and report the searched surface. | User provides a ready issue or invokes upstream workflow. |
| Candidate is blocked by unresolved work | GitHub issue dependencies / DJAA / Mountain Goat | cross-source | Starting blocked work violates dependency order and hides WIP. | Skip, stop, or ask whether to work the blocker instead. | Blocker is resolved or the blocker is selected. |
| Candidate is ambiguous or underspecified | GitHub Copilot docs / SWE-bench Verified / VS Code docs | cross-source | Agent would invent expected behavior. | Ask for clarification or route to `triage`. | Missing result-defining detail is supplied. |
| User supplies PRD/spec without one ready issue | Facet boundary / Scrum Guide | bridge | A source document is not automatically one implementation unit. | Ask for target issue or route to `to-issues`. | One ready issue-equivalent slice is named. |
| Candidate is broad, context-rich, deeply domain-heavy, or multi-slice | GitHub Copilot docs / VS Code docs | cross-source | Poor autonomous task fit. | Ask to narrow, split, or confirm route. | Scope is narrowed to one ready issue. |
| Candidate touches sensitive or consequential domains | GitHub Copilot docs / Copilot Agents card | cross-source | High-risk work needs oversight. | Ask for confirmation and boundaries. | User confirms autonomy and guardrails. |
| Readiness recheck would require changing issue state or content | Agile Alliance / Mountain Goat / facet boundary | bridge | That is triage or issue creation, not selection. | Stop and route to owner. | Issue is made ready by upstream owner or user selects another. |
| Selection starts becoming implementation plan | Scrum Guide / GitHub Copilot docs | cross-source | Planning belongs after issue identity and context are locked. | Stop planning and record selection facts only. | Selected issue and readiness facts are clear. |

## 10. Agentic Bridge Language

| Source Concept | SWE Meaning | Agentic Meaning | Claim Strength | Skill Behavior It Could Steer | Bridge Confidence |
| --- | --- | --- | --- | --- | --- |
| WIP limit | Limit active work to improve flow. | Keep the agent session bound to one implementation issue. | bridge | Stop after selecting one item. | High |
| Pull criteria | Rule for moving work into the active workflow. | Predicate before `implement` owns the work. | bridge | Check ready marker, order, blocker/dependency, and prompt adequacy. | High |
| Ready for selection | Item is transparent, ordered, and small enough to choose. | Selectable, not fully planned. | bridge | Separate selection from Context Intake. | High |
| Issue as prompt | Issue text should enable an agent to make the right code change. | The issue is the first context packet for a fresh coding session. | direct | Ask whether a fresh session could act without hidden product decisions. | High |
| Acceptance criteria | Success criteria for the work. | Observable done signal for pickup, later proof target. | bridge | Require at least one success/proof hint before pickup. | Medium-high |
| Underspecified problem statement | Issue text does not define what should be solved. | No-pick condition if it changes the result. | bridge | Ask or route upstream instead of guessing. | Medium-high |
| Blocked by | Work depends on another issue being completed. | Selection stop unless working the blocker. | direct | Skip blocked candidates in next-ready selection. | High |
| Human oversight | Humans remain accountable for consequential agent actions. | Sensitive pickup needs confirmation. | bridge | Ask before critical/sensitive work. | Medium |
| Definition of Ready | Shared entry criteria for work. | Small pickup recheck, not issue promotion. | bridge | Confirm actionable/clear/feasible/unblocked/testable enough. | Medium |
| Stage gate | Rigid gate between phases. | Warning against over-checking readiness. | bridge | Do not demand complete upfront design. | Medium |
| Self-contained change | One coherent reviewable change. | Smell that selected item can stay one issue. | bridge | Flag obvious multi-issue candidates. | Medium |

## 11. Weak Or No-Op Language

| Weak Phrase | Source / Context | Why It Is Weak | Stronger Replacement Direction |
| --- | --- | --- | --- |
| "Pick a suitable issue" | Generic project-management phrasing | Lets agent choose by preference. | Tie selection to visible ready/order/blocker gates. |
| "Start on the next task" | Generic queue language | Hides pull/WIP discipline. | Pull one ready issue from repo-visible ordering. |
| "Make sure it is ready" | DoR / readiness phrasing | No observable behavior. | Check ready marker, clear work, done signal, blocker/dependency, ambiguity. |
| "Clear enough" | Agent task guidance | Too subjective. | Require clear problem/work required and observable success shape. |
| "Well-defined" | Agent task guidance | Weak without gate. | Tie to inputs/outputs/constraints, acceptance criteria, or expected behavior. |
| "Use INVEST" | Agile readiness sources | Too broad and authoring-oriented. | Keep only independent/small/testable as pickup smells. |
| "Resolve blockers" | Tracker / blocked-work language | Wrong owner for selection facet. | Stop, skip, or select blocker issue when appropriate. |
| "If blocked, move on" | Common workflow shorthand | Hides blocked WIP and dependency order. | Surface blocker and ask/stop unless next ready work is explicitly allowed. |
| "Ask if unsure" | Generic stop rule | Too broad and timid. | Ask on named conditions: ambiguity, blockers, conflicting order, sensitive work, PRD/spec without issue. |
| "All details complete" | DoR overreach | Creates stage-gate behavior. | Require enough to select; defer full understanding to Context Intake. |
| "Prioritize the most important" | DORA priority language without repo source | Agent may invent priority. | Use repo ordering or ask. |

## 12. Boundary Drift Notes

| Extracted Material | Possible Owner | Why It May Drift | Prompt 05 Triage Question |
| --- | --- | --- | --- |
| Acceptance criteria quality | Context Intake / `triage` | Selection needs an observable signal, not a full issue audit. | What minimum done/proof hint survives in this facet? |
| File directions / right context | Context Intake | Helpful for issue-as-prompt, but full file discovery belongs later. | Should file hints be optional at selection? |
| Issue splitting / broad tasks | `to-issues` / Bounded Slice Control | Selection may notice oversize but should not decompose. | Keep as stop/route rule only? |
| DoR criteria | `triage` / repo process docs | Creating or enforcing DoR is upstream. | Keep local recheck and stage-gate warning, drop process material? |
| INVEST | `to-issues` / `triage` | Mostly issue-authoring and slicing. | Keep only independent/small/testable as smells? |
| Tracker dependency commands | Repo tracker docs | Commands and label names are local policy. | Keep semantics but not syntax? |
| Sensitive work | Engineering contract / repo docs | Risk threshold is repo-specific. | Keep generic stop terms or route to contract? |
| WIP metrics / lead time / cadences | Engineering contract / research-only | They are process management, not selection behavior. | Drop as research-only? |
| Google Small CL splitting | Bounded Slice Control / Review And Lock | Stronger owner is scope/reviewability after selection. | Keep only one self-contained change smell? |
| Human review of agent outputs | Review And Lock | Important after implementation, not selection. | Keep only oversight as pickup caution? |
| OpenAI Codex testing/review loop | Semantic Proof / Review And Lock | Mostly later behavior. | Defer to proof/review facets? |

## 13. Extraction Notes By Source

### GitHub Docs: Best Practices For Using GitHub Copilot To Work On Tasks

Most useful extraction:

- Well-scoped issues, issue-as-prompt, acceptance criteria, and poor
  agent-task classes.

Strongest behavior pressure:

- A ready issue for an agent must be clear enough to function as the first
  prompt for the coding session.

Likely research-only material:

- Copilot setup, PR iteration, custom agents, MCP, dependency preinstallation.

Open question:

- Should file directions be a readiness gate or only a helpful signal?

### The Official Guide To The Kanban Method

Most useful extraction:

- Pull, WIP limits, capacity, explicit policies, pull criteria.

Strongest behavior pressure:

- `implement` should pull one eligible item under visible policy, not start a
  batch of available work.

Likely research-only material:

- Metrics, board design, cadences, and process-improvement theory.

Open question:

- How much of "explicit policies" becomes inline skill text versus repo-doc
  pointer?

### DORA: Work In Process Limits

Most useful extraction:

- Capacity-based limits, highest-priority pull, visible blockers, and
  anti-multitasking warnings.

Strongest behavior pressure:

- If no safe ready issue exists, do not relax readiness just to keep working.

Likely research-only material:

- Stakeholder prioritization meetings, delivery metrics, and flow improvement.

Open question:

- How should Prompt 05 treat "highest priority" without letting the agent invent
  priority?

### The 2020 Scrum Guide

Most useful extraction:

- Ready-for-selection, refinement adding detail/order/size, and developers
  selecting what can be done.

Strongest behavior pressure:

- Selection is not the same as planning; choose the item first, then do Context
  Intake.

Likely research-only material:

- Sprint ceremonies, roles, Product Goal mechanics, and full Definition of Done
  governance.

Open question:

- Should "ready for selection" become a leading phrase or stay behind a more
  direct phrase like "selectable issue"?

### GitHub Docs: Creating Issue Dependencies

Most useful extraction:

- `blocked by` and `blocking` relationships as visible dependency evidence.

Strongest behavior pressure:

- A candidate blocked by unresolved work is not safe to pick unless the selected
  work is the blocker itself.

Likely research-only material:

- GitHub CLI/API syntax for adding and editing dependencies.

Open question:

- How should Prompt 05 phrase blocker semantics without becoming GitHub-only?

### OpenAI: Introducing SWE-bench Verified

Most useful extraction:

- Issue text as task input and underspecified issue descriptions as a known
  problem for evaluating coding agents.

Strongest behavior pressure:

- Do not execute an issue when missing information changes what solution should
  be produced.

Likely research-only material:

- Benchmark scoring methodology and test categories.

Open question:

- How much benchmark language is useful, versus just extracting "underspecified
  issue" as a stop condition?

### GitHub Docs: Application Card For GitHub Copilot Agents

Most useful extraction:

- Human oversight and caution around consequential/sensitive domains.

Strongest behavior pressure:

- Sensitive or consequential tasks require confirmation before autonomous
  pickup.

Likely research-only material:

- Responsible-AI governance and platform-card details.

Open question:

- Should sensitive-work pickup live here or in Commitment Boundary?

### VS Code Docs: Best Practices For Using AI In VS Code

Most useful extraction:

- Specific inputs/outputs/constraints, acceptance criteria, breaking down
  complex tasks, and clarifying questions.

Strongest behavior pressure:

- Vague tasks should not be selected without clarification.

Likely research-only material:

- Model choice, session management, context tools, and plan/implement workflow.

Open question:

- How much "break down complex tasks" belongs here versus `to-issues`?

### Agile Alliance DoR / INVEST

Most useful extraction:

- Explicit visible criteria and independent/small/testable readiness signals.

Strongest behavior pressure:

- Use readiness criteria as a local pickup recheck only.

Likely research-only material:

- Story-writing checklist details and rewrite advice.

Open question:

- Which, if any, INVEST terms should survive Prompt 05?

### Mountain Goat Software: Definition Of Ready And Its Dangers

Most useful extraction:

- Unresolved dependencies can legitimately prevent pickup; overly rigid
  readiness can become a stage gate.

Strongest behavior pressure:

- Stop on real dependencies, but do not demand perfect upstream design before
  selection.

Likely research-only material:

- Broad Scrum coaching and anti-stage-gate argumentation.

Open question:

- How can the final skill keep a readiness gate without sounding bureaucratic?

### DJAA Blocked Items In WIP Limits

Most useful extraction:

- Blocked work stays visible and counts against WIP.

Strongest behavior pressure:

- Do not hide blocked active work by pulling unrelated new work.

Likely research-only material:

- Parking-lot mechanics, service delivery reviews, maturity-model depth.

Open question:

- Is this blocker material redundant with GitHub issue dependencies and DORA?

### Google Engineering Practices: Small CLs

Most useful extraction:

- One self-contained change as a reviewability smell.

Strongest behavior pressure:

- Avoid selecting work that obviously cannot land as one coherent change.

Likely research-only material:

- Splitting strategies and review process details.

Open question:

- Should this source be deferred entirely to Bounded Slice Control?

### OpenAI Developers: Codex Best Practices

Most useful extraction:

- Codex works better when it knows what "good" looks like.

Strongest behavior pressure:

- A ready issue needs at least a success signal before implementation.

Likely research-only material:

- Testing, review, MCP, skills, and setup details that belong to later facets.

Open question:

- Is this redundant with GitHub Copilot and VS Code sources for this facet?

## 14. Handoff To Triage

- extraction decision: `ready-for-triage`
- strongest extracted leading words:
  - pull
  - WIP limit
  - ready for selection
  - issue as prompt
  - well-scoped
  - acceptance criteria
  - underspecified
  - blocked by
  - Definition of Ready
  - stage gate
- strongest behavior rules:
  - Pull one ready item, not a batch.
  - Use repo-visible ordering when no issue is named.
  - Recheck whether the issue can function as an agent prompt.
  - Treat open blockers as selection stops.
  - Stop on broad, ambiguous, sensitive, or deeply domain-heavy tasks.
  - Do not repair readiness inside `implement`.
  - Separate selection from planning.
- strongest evidence gates:
  - one selected work item;
  - repo-ready marker or explicit user target;
  - local readiness recheck;
  - agent-prompt adequacy;
  - observable done signal;
  - blocker/dependency check;
  - owner-boundary check.
- extraction gaps:
  - Ambig-SWE or similar ambiguity-specific papers remain unextracted.
  - Linear Method was not verified from an official source.
  - Exact tracker command mapping remains intentionally deferred to repo docs.
- source material promising but uncertain:
  - Agile Alliance DoR/INVEST may be useful, but may mostly belong to `triage`
    and `to-issues`.
  - Google Small CLs may be better deferred to Bounded Slice Control.
  - OpenAI Codex best practices may be better deferred to Context Intake,
    Semantic Proof, Review And Lock, or final skill shape.
- Prompt 05 should triage first:
  - whether the compact readiness gate should be "issue as prompt" plus
    observable done signal;
  - how much blocker/dependency language survives;
  - how to keep DoR/INVEST as pickup smells without issue-authoring drift;
  - whether sensitive-work stop rules belong here or in Commitment Boundary.
