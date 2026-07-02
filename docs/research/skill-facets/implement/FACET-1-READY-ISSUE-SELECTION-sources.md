# Prompt 03: Source Search For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/03-source-search-per-facet.md`](../../../synthesis/methods/prompts/03-source-search-per-facet.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet: `1 - Ready Issue Selection`

Facet research question: How should `implement` select exactly one ready issue
or stop when no safe issue is available?

Facet boundaries:

- Owns how `implement` chooses exactly one issue when the user names an issue,
  path, URL, PRD, spec, or nothing.
- Owns treatment of `ready-for-agent`, blockers, dependency order, ambiguity,
  and no available issue.
- Owns the smallest local readiness recheck before taking ownership of a
  selected issue.
- Does not own issue creation from PRDs/specs; `to-issues` owns that.
- Does not own moving issues into `ready-for-agent`; `triage` owns that.
- Does not own tracker commands or label strings; repo tracker docs own those.
- Does not own full implementation context after selection; Context Intake owns
  that.

Facet source lanes:

- Primary: delivery/operations sources; Kanban/WIP sources; issue-readiness
  practice; agentic coding / LLM task-selection sources.
- Secondary: prompt/skill-writing for stop gates; tracker docs for local
  mapping.
- Avoided: generic project-management advice; raw issue-template catalogs;
  triage-state-machine sources unless they affect pickup behavior.

Facet collision watchpoints:

- Ready Issue Selection vs `triage`, `to-issues`, and tracker docs: keep source
  pressure to pickup/readiness gates, not issue lifecycle ownership.
- Ready Issue Selection vs Context Intake: selection answers "which issue can
  be safely picked"; context intake answers "what must be understood before
  coding."
- First-facet integration risk: do not integrate runtime wording until Context
  Intake and Bounded Slice Control have also been researched.

Prior artifacts:

- Intent and keywords:
  [`01-intent-and-keywords.md`](01-intent-and-keywords.md)
- Facet map:
  [`02-facet-map-and-research-plan.md`](02-facet-map-and-research-plan.md)

Revision feedback:

- Rerun Prompt 03 after the refreshed Prompt 02 map.
- Use three subagents to cover delivery/WIP, agentic coding, and
  requirements/tracker-doc lanes.
- Verify sources through live search where possible.

Subagent inputs used:

- Delivery/WIP pass: recommended Kanban University, DORA WIP limits, Scrum
  Guide, DJAA blocked-items guidance, and caution around DoR/INVEST drift.
- Agentic-coding pass: recommended GitHub Copilot task best practices,
  SWE-bench Verified, VS Code AI best practices, OpenAI Codex best practices,
  and agent-spec sources.
- Requirements/tracker pass: recommended GitHub Copilot task docs, Kanban
  Guide, Scrum Guide, GitHub issue dependencies/labels, and Agile Alliance
  Definition of Ready.

Constraints:

- Do not rewrite `skills/current/implement/SKILL.md`.
- Do not extract detailed lessons yet.
- Do not summarize sources for their own sake.
- Rank sources by usefulness for improving this facet's agent behavior.

## 1. Facet Search Objective

This source search is trying to find high-quality pressure for the first
runtime gate in `implement`: select exactly one executable ready issue, or
stop/ask when the available work is ambiguous, blocked, dependency-ordered, not
ready, or owned by an upstream skill.

Upper-bound source quality for this facet means sources that produce operational
selection gates: pull discipline, WIP limits, explicit pull criteria,
ready-for-selection criteria, well-scoped agent task criteria, blocker/dependency
visibility, and ambiguity stop rules. The best sources should help the skill
choose one issue safely, not teach the agent how to implement it.

Noise includes generic Agile ceremony, broad project-management prioritization,
raw issue-template catalogs, tracker command references, full triage workflows,
or coding/testing/review advice that belongs to later `implement` facets.

## 2. Step 2 Handoff Check

| Facet Map Input | Search Impact | Source / Query Consequence | Notes |
| --- | --- | --- | --- |
| Choose exactly one issue or stop | Prefer sources about pull, WIP, selection, and task fit. | Kanban, DORA, Scrum ready-for-selection, and agentic task docs. | Do not search for implementation tactics. |
| Named issue/path/URL/PRD/spec/nothing precedence | Need sources that justify honoring explicit selection while stopping on ambiguous broader inputs. | Search for issue-as-prompt, well-scoped task, and readiness language. | Local skill owns precedence; sources should improve gates. |
| Ready labels, blockers, dependency order, no available issue | Need operational pickup safety checks. | Search blocker/dependency docs and WIP/pull sources. | Tracker-specific commands stay in repo docs. |
| Smallest local readiness recheck | Need "can this be executed?" criteria without issue repair. | Search acceptance criteria, clear problem, small/testable/independent. | Use only as pickup signals, not issue-writing procedure. |
| Does not own `to-issues` / `triage` | Avoid sources whose value is mostly writing, splitting, or promoting issues. | Demote raw templates, issue authoring, backlog refinement, and state-machine docs. | This is the main collision risk. |
| Does not own full Context Intake | Treat acceptance criteria as a readiness signal, not a full pre-coding context procedure. | Keep agent-task docs scoped to selection fit. | Prompt 04 must not extract all context-intake behaviors here. |
| First-facet integration risk | Do not turn source findings into final runtime wording yet. | Mark `ready-for-extraction`, not ready for skill patch. | Integration should wait for adjacent facets. |

## 3. Search Queries

### Books / Professional Practice

- `"WIP limits" "pull system" software`
  - Worth running because WIP and pull discipline are the main external source
    pressure for one-at-a-time pickup.
- `"ready for selection" "Product Backlog" "Scrum Guide"`
  - Worth running because Scrum has canonical "ready for selection" wording.
- `"definition of ready" software development acceptance criteria dependencies`
  - Worth running to identify readiness-check language and its risks.
- `"INVEST" "small" "testable" "independent" user story`
  - Worth running as a possible local readiness recheck, with drift risk.

### Papers

- `SWE-bench Verified issue description underspecified`
  - Worth running because it can support ambiguity/no-ready stop gates for
    coding agents.
- `SWE-bench real world GitHub issues issue text`
  - Worth running because it treats issue text as the unit of agent task work.
- `software engineering agents issue description acceptance criteria`
  - Worth running to find agent-specific task-readiness papers.

### Manuals / Official Docs

- `GitHub Copilot coding agent best practices well-scoped issues acceptance criteria`
  - Worth running because it is the clearest official agent-ready issue source.
- `OpenAI Codex best practices what good looks like task`
  - Worth running as an official Codex bridge for task specification and
    verification.
- `GitHub issue dependencies blocked by blocking official docs`
  - Worth running for blocker/dependency semantics in the likely tracker.
- `GitLab linked issues blocks is blocked by official docs`
  - Worth running as a cross-tracker blocker corroboration.

### Agentic Coding / LLM Tooling

- `"coding agent" "well-scoped" issue`
  - Worth running to find issue-as-prompt and agent task-fit guidance.
- `"AI coding" "acceptance criteria" "ambiguous" task`
  - Worth running for ambiguity stop/ask rules.
- `"VS Code" "AI" "acceptance criteria" "ambiguous"`
  - Worth running for tool-neutral agent prompt guidance.

### Field Practice

- `DORA work in process limits pull highest priority`
  - Worth running because DORA translates WIP into software-delivery gates.
- `Kanban blocked items WIP limits`
  - Worth running to decide whether blocked work should prevent more pickup.
- `Definition of Ready dangers stage gate`
  - Worth running as contrast so `implement` does not become an upstream
    bureaucratic readiness gate.

## 4. Verified Source List

| Rank | Source | Type | Link / Locator | Verification Basis | Access / Extractability | Why It Matters | Expected Contribution | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | GitHub Docs: Best practices for using GitHub Copilot to work on tasks | Official agentic coding manual | <https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results> | Live official docs verified; relevant sections on well-scoped issues, acceptance criteria, file hints, issue-as-prompt, and unsuitable broad/sensitive tasks found. | Directly extractable from public HTML. | Best direct source for deciding whether an issue is ready for a coding agent. | Agent-ready task criteria, ambiguity/broadness stop rules, and issue-as-prompt framing. | High |
| 2 | The Official Guide to the Kanban Method | Official delivery guide | <https://kanban.university/kanban-guide/> | Live official page verified; relevant sections on WIP, pull, explicit policies, pull criteria, and "stop starting, start finishing" found. | Directly extractable from public HTML. | Best source for one-at-a-time pull discipline and explicit pickup policy. | Leading words around pull, WIP, explicit policies, capacity, and not starting work just because work exists. | High |
| 3 | DORA: Work in Process Limits | Evidence-backed delivery practice | <https://dora.dev/capabilities/wip-limits/> | Live DORA page verified; relevant guidance on prioritizing work, limiting active work, pulling highest-priority waiting work, blockers, and single-piece flow found. | Directly extractable from public HTML. | Turns "one issue at a time" into concrete operational gates and failure modes. | WIP gate, capacity gate, highest-priority pull, blocked-work visibility, and anti-multitasking pressure. | High |
| 4 | The 2020 Scrum Guide | Official Scrum guide | <https://scrumguides.org/scrum-guide.html> | Live official page verified; relevant ready-for-selection, refinement, ordering, size, and capacity/Definition of Done confidence language found. | Directly extractable from public HTML. | Provides canonical "ready for selection" language without making `implement` own backlog refinement. | Ready-for-selection vocabulary and separation of selection from planning/context intake. | High |
| 5 | GitHub Docs: Creating issue dependencies | Official tracker documentation | <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies> | Live official docs verified; blocked-by/blocking relationships, blocked icons, and CLI-visible dependency fields found. | Directly extractable from public HTML, but use lightly. | Gives direct blocker/dependency semantics for the likely tracker. | Blocker/dependency stop gate and local-doc deference for exact tracker commands. | High |
| 6 | OpenAI: Introducing SWE-bench Verified | Official AI evaluation report | <https://openai.com/index/introducing-swe-bench-verified/> | Live OpenAI page verified; relevant issue-description task framing and human filtering of problematic/underspecified samples found. | Directly extractable from public HTML. | Provides empirical pressure for not executing underspecified or impossible issue tasks. | Ambiguity/no-ready stop language and "issue text as task input" bridge. | Medium-high |
| 7 | GitHub Docs: Application card for GitHub Copilot Agents | Official responsible-use documentation | <https://docs.github.com/en/copilot/responsible-use/agents> | Live official docs verified; relevant sections on agent capabilities, limitations, permissions, oversight, and sensitive-domain caution found. | Directly extractable from public HTML. | Adds safety/oversight pressure for autonomous task pickup. | Stop/ask pressure for sensitive, consequential, or permission-bound work. | Medium-high |
| 8 | VS Code Docs: Best practices for using AI in VS Code | Official AI tooling manual | <https://code.visualstudio.com/docs/agents/best-practices> | Live official docs verified; relevant sections on specificity, breaking down complex tasks, acceptance criteria, and clarifying questions found. | Directly extractable from public HTML. | Tool-neutral bridge for well-scoped agent tasks and ambiguity asks. | Ambiguity ask rule and acceptance criteria as verification hook. | Medium |
| 9 | Agile Alliance: Definition of Ready and INVEST glossary | Professional glossary / field practice | <https://agilealliance.org/agile101/agile-glossary/> and <https://agilealliance.org/glossary/invest/> | Live pages verified; relevant lines on explicit criteria before accepting a story and INVEST criteria found. | Directly extractable from public HTML. | Supports a minimal local readiness recheck, but can drift into triage. | Clear/visible criteria, independent/small/testable signals. | Medium |
| 10 | Mountain Goat Software: Definition of Ready and Its Dangers | Professional contrast source | <https://www.mountaingoatsoftware.com/blog/the-dangers-of-a-definition-of-ready> | Live page verified; relevant sections on DoR criteria, dependencies, and stage-gate danger found. | Directly extractable from public HTML. | Good contrast against making readiness a rigid upstream gate owned by `implement`. | Warning language: useful readiness checks can become harmful bureaucracy. | Medium |
| 11 | David J. Anderson School: Blocked Items in WIP Limits | Professional Kanban practice | <https://djaa.com/kanban-evergreen-should-we-include-waiting-or-blocked-items-in-wip-limits/> | Live page verified; relevant sections on blocked work adding to WIP and escalation policies found. | Directly extractable from public HTML. | Strong specific source for blocker behavior. | Blocked work still counts as committed work; do not hide it by pulling more. | Medium |
| 12 | Google Engineering Practices: Small CLs | Professional engineering manual | <https://google.github.io/eng-practices/review/developer/small-cls.html> | Live official/professional page verified; relevant sections on one self-contained change and reviewability found. | Directly extractable from public HTML. | Useful cross-facet support, but stronger for Bounded Slice Control and Review And Lock. | Selection sanity check: avoid work that cannot plausibly stay one reviewable change. | Medium |
| 13 | OpenAI Developers: Codex best practices | Official Codex docs | <https://developers.openai.com/codex/learn/best-practices> | Live official docs verified; relevant sections on what "good" looks like, testing/review, and scoped skills found. | Directly extractable from public HTML. | Useful bridge to Codex skill behavior, but broader than selection. | Supportive wording for prompt/skill gates; likely stronger for later Context/Proof facets. | Medium |

## 5. Expected But Unverified Sources

| Source | Why It Might Matter | How To Verify | Keep Searching? |
| --- | --- | --- | --- |
| David Anderson, *Kanban* or *Essential Kanban Condensed* | Deeper primary-source pull/WIP theory. | Publisher page, library copy, or official excerpts. | Optional; current Kanban/DORA sources are enough for Prompt 04. |
| Mary and Tom Poppendieck, *Lean Software Development* | Pull systems and small-batch lean principles. | Publisher page or library copy. | Low priority for this facet; may be more useful for Bounded Slice Control. |
| Linear Method: Write issues not user stories | Could sharpen "issue as concrete task" language. | Find official Linear Method page; search only found mirrors/social discussion in this pass. | Keep searching only if Prompt 04 needs issue-task contrast. |
| Ambig-SWE / underspecification papers | Could provide direct evidence for ambiguity/clarification behavior. | OpenReview/arXiv page or PDF; one OpenReview page hit browser challenge. | Rerun later if SWE-bench Verified is too indirect. |
| Jira/Azure official dependency docs | Could corroborate cross-tracker blocker semantics. | Official Atlassian/Microsoft docs. | Low; GitHub/GitLab are enough and tracker specifics belong to repo docs. |

## 6. Source Quality Notes

- GitHub Copilot task best practices: `core` and `bridge`. It is the most
  direct source for agent-ready issue pickup.
- Kanban Guide: `core`. It provides the strongest delivery language for pull,
  WIP, explicit policies, and pull criteria.
- DORA WIP limits: `core` and `supporting`. It makes WIP limits practical and
  operational, with clear failure modes.
- Scrum Guide 2020: `core`. It gives "ready for selection" language and keeps
  selection distinct from refinement.
- GitHub issue dependencies: `core` for blocker semantics, but `supporting` for
  source extraction because exact tracker commands belong to repo docs.
- SWE-bench Verified: `bridge` and `contrast`. It supports stopping on
  underspecified or invalid agent tasks.
- GitHub Copilot Agents responsible-use card: `supporting` and `contrast`. It
  adds oversight and limits, but is broader than selection.
- VS Code AI best practices: `bridge`. It supports clear prompts, acceptance
  criteria, task breakdown, and clarifying questions.
- Agile Alliance DoR/INVEST: `supporting`. Useful for minimal readiness checks,
  but risky if extracted as issue-authoring or triage procedure.
- Mountain Goat DoR dangers: `contrast`. Good warning against rigid stage gates.
- DJAA blocked-items article: `supporting`. Strong on blockers and escalation,
  but narrower and more Kanban-specific.
- Google Small CLs: `supporting` and cross-facet. Keep light here; mostly for
  Bounded Slice Control.
- OpenAI Codex best practices: `supporting` and cross-facet. More useful for
  Context Intake, Semantic Proof, Review And Lock, and final skill shape.

Rejected or weak sources:

- Generic Definition of Ready blogs: `reject` unless they add a clear
  operational stop rule; most drift into triage.
- Raw issue-template catalogs: `reject`; they teach issue authoring, owned by
  `to-issues` / `triage`.
- Generic project-management prioritization: `reject`; it does not constrain
  agent pickup.
- Tracker command references: `reject` for extraction; local tracker docs own
  commands and labels.
- Tool-specific blog posts about AI coding: `reject` when official docs give
  stronger source pressure.

## 7. Searched / Rejected / Thin Lanes

| Lane Or Query Family | Result | Keep / Reject / Rerun Later | Reason |
| --- | --- | --- | --- |
| Official Kanban / WIP / pull system | Strong official source found. | Keep | Directly supports one-at-a-time pull and explicit pickup criteria. |
| DORA WIP limits | Strong evidence-backed delivery source found. | Keep | Adds operational gates around capacity, priority, blocked work, and multitasking. |
| Official Scrum ready-for-selection | Strong official source found. | Keep | Gives concise readiness language and preserves the selection/refinement boundary. |
| GitHub Copilot coding-agent task docs | Strong official source found. | Keep | Best direct bridge for agent-ready issue selection. |
| OpenAI Codex docs | Verified, but broad. | Keep as supporting / rerun later | Good for skill behavior and proof, weaker for initial selection. |
| SWE-bench / SWE-bench Verified | Useful bridge source found. | Keep | Supports issue text as task input and underspecification as a real evaluation problem. |
| GitHub issue dependencies | Strong official tracker source found. | Keep lightly | Supports blockers/dependencies while leaving exact commands to repo docs. |
| Cross-tracker blocker docs | GitLab verified; Jira/Azure broadly found. | Keep as support only | Corroborates blocker semantics but can drift into tracker mechanics. |
| Definition of Ready field practice | Useful but risky. | Keep with caution | Helps define minimal readiness recheck, but can invade triage. |
| DoR danger / stage-gate contrast | Strong contrast source found. | Keep as contrast | Prevents over-rigid readiness gate and upstream ownership drift. |
| Google small CL / reviewability | High quality but indirect. | Rerun for Facet 4/8 | More useful for bounded slice and review/lock than selection. |
| Generic Agile/project-management sources | Many results, low signal. | Reject | Mostly vocabulary, templates, or advice owned by upstream readiness/triage. |
| Raw issue templates and ticket checklists | Found but demoted. | Reject | They teach issue authoring, not `implement` pickup behavior. |
| Ambig-SWE / ambiguity papers | Search found a likely paper but page access was blocked. | Rerun later only if needed | SWE-bench Verified is enough for Prompt 04. |

## 8. Extraction Readiness Check

- Recommended sources are verified through live official, primary, or
  professional pages.
- The recommended extraction set is accessible enough for Prompt 04:
  - GitHub Copilot task docs;
  - Kanban Guide;
  - DORA WIP limits;
  - Scrum Guide;
  - GitHub issue dependencies;
  - SWE-bench Verified;
  - VS Code AI best practices;
  - Mountain Goat DoR dangers.
- Each recommended source has a clear extraction target:
  - pull/WIP/explicit policies;
  - agent-ready issue criteria;
  - ready-for-selection criteria;
  - blocker/dependency stop gates;
  - underspecified-task stop rules;
  - ambiguity ask rules;
  - DoR stage-gate caution.
- Sources verified but too indirect or secondary for first extraction:
  - Google Small CLs;
  - OpenAI Codex best practices;
  - Agile Alliance INVEST;
  - GitLab linked issues.
- No recommended extraction source requires user-only access or a library copy.

## 9. Expected Extraction Targets

| Source | Extract For | Watch For | Avoid Extracting |
| --- | --- | --- | --- |
| GitHub Copilot task best practices | Well-scoped issue gates, acceptance criteria, issue-as-prompt, unsuitable task classes, ambiguity/broadness stops. | Translate Copilot-specific guidance into general Codex `implement` behavior. | Copilot setup, PR iteration, custom agents, or environment configuration. |
| Kanban Guide | Pull discipline, WIP limits, explicit policies, pull criteria, and capacity-based selection. | Translate team-board language into a single-agent one-issue pickup gate. | Kanban metrics, full board design, or workflow-management theory. |
| DORA WIP limits | Capacity, highest-priority pull, blocked work, anti-multitasking, and single-piece flow. | Keep "highest priority" subject to repo tracker docs and dependency order. | Team process improvement, stakeholder meetings, or delivery metrics. |
| Scrum Guide 2020 | Ready-for-selection, refinement adding detail/order/size, capacity, and Definition-of-Done confidence. | Treat Scrum as source pressure, not a mandate to emulate Sprint Planning. | Full Scrum framework, ceremonies, team roles, or backlog refinement procedure. |
| GitHub issue dependencies | Blocked-by/blocking semantics and visible dependency evidence. | Use as blocker vocabulary; leave exact CLI/API commands to repo docs. | Creating/editing dependencies or tracker workflow mechanics. |
| SWE-bench Verified | Issue text as task input; underspecified/impossible task filtering; human validation pressure. | Keep evaluation language as bridge, not benchmark policy. | Full benchmark methodology, scoring, or proof/test details. |
| GitHub Copilot Agents application card | Oversight, limitations, permissions, sensitive/consequential work caution. | Extract only pickup safety and stop/ask behavior. | Broad responsible-AI governance unrelated to selecting one issue. |
| VS Code AI best practices | Specific inputs/outputs/constraints, acceptance criteria, break down complex tasks, ask clarifying questions. | Use as bridge for agent task clarity, not a full prompt-writing guide. | General AI prompting setup or model-selection advice. |
| Agile Alliance DoR / INVEST | Explicit visible criteria; independent, small, testable as minimal readiness signals. | Keep to local readiness recheck only. | Rewriting issues, story authoring, or moving work to ready. |
| Mountain Goat DoR dangers | Caution against stage-gate overreach; readiness as team-specific criteria. | Use as contrast so `implement` can reject unready work without owning readiness promotion. | Full anti-DoR debate or Scrum coaching. |
| DJAA blocked-items article | Blocked work counts as WIP; blocked-work policies and escalation. | Keep the implementation rule simple: blocked issue is not safe to pick. | Kanban maturity model depth or organizational escalation design. |

## 10. Boundary Stress Test

- Some strong sources partially belong to other facets:
  - Google Small CLs belongs more to Bounded Slice Control and Review And Lock.
  - OpenAI Codex best practices belongs more to Context Intake, Semantic Proof,
    Review And Lock, and final skill shape.
  - VS Code AI best practices partly belongs to Context Intake and Proof.
  - Agile Alliance INVEST and DoR material can drift into `to-issues` and
    `triage`.
- No source shows the facet is too broad, too narrow, or wrongly named.
  "Ready Issue Selection" still fits: the strongest sources are about pull,
  ready-for-selection, agent-suitable tasks, and blocker/dependency gates.
- The source landscape suggests one addition to Prompt 02's mental model, not
  a facet-map revision: blocker/dependency semantics are strong enough to be a
  first-class extraction target inside Ready Issue Selection.
- Collision watchpoints remain manageable if Prompt 04 extracts only pickup
  gates and leaves issue authoring, issue promotion, full context intake, and
  implementation planning out of scope.
- Next step should continue to extraction.

Decision: `ready-for-extraction`.

## 11. Coverage Check

- Strong professional SWE / delivery source: yes, Kanban Guide, DORA WIP
  limits, and Scrum Guide.
- Agentic coding / LLM behavior source: yes, GitHub Copilot task best practices,
  SWE-bench Verified, GitHub Copilot Agents application card, VS Code AI best
  practices, and OpenAI Codex best practices.
- Operational gates rather than taste words: yes, WIP/pull criteria,
  ready-for-selection, well-scoped task criteria, dependency/blocker visibility,
  and ambiguous/broad/sensitive task stops.
- The set is not over-weighted on one author, school, era, or tool. It spans
  Kanban, DORA, Scrum, GitHub, OpenAI, Microsoft, and field practice.
- Missing lane: directly extractable ambiguity-specific agent papers such as
  Ambig-SWE. Optional rerun later if Prompt 04 needs more than SWE-bench
  Verified.
- Recommended sources do not need stronger verification before Prompt 04.

## 12. Recommended Source Set

| Priority | Source | Why Extract Next |
| --- | --- | --- |
| 1 | GitHub Docs: Best practices for using GitHub Copilot to work on tasks | Best direct source for coding-agent issue readiness, issue-as-prompt framing, and unsuitable task classes. |
| 2 | The Official Guide to the Kanban Method | Best source for pull, WIP, explicit policies, and not starting work merely because work exists. |
| 3 | DORA: Work in Process Limits | Best operational source for one-piece flow, capacity, highest-priority pull, and anti-multitasking gates. |
| 4 | The 2020 Scrum Guide | Best canonical source for "ready for selection" and enough refinement/detail/order/size. |
| 5 | GitHub Docs: Creating issue dependencies | Best tracker-grounded source for blocker/dependency semantics. |
| 6 | OpenAI: Introducing SWE-bench Verified | Best bridge source for underspecified issue/task stop rules. |
| 7 | VS Code Docs: Best practices for using AI in VS Code | Useful bridge for ambiguity asks, acceptance criteria, and decomposing broad tasks. |
| 8 | Mountain Goat Software: Definition of Ready and Its Dangers | Best contrast source to prevent readiness from becoming a rigid upstream triage gate. |

## 13. Output Summary

- source-search decision: `ready-for-extraction`
- output artifact:
  `docs/research/skill-facets/implement/FACET-1-READY-ISSUE-SELECTION-sources.md`
- best source to start extraction from:
  GitHub Docs: Best practices for using GitHub Copilot to work on tasks
- strongest source lane:
  agentic coding official docs plus Kanban/DORA delivery discipline
- weakest source lane:
  generic Definition of Ready / issue-template content
- biggest risk in the source set:
  extracting readiness material as if `implement` owns issue creation,
  promotion, or repair instead of limiting it to a small pickup recheck
- next recommended step:
  run Prompt 04 for `Ready Issue Selection`
