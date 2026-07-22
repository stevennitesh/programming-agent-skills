# Superpowers Skill-Pack Vocabulary

Status: answered

Supports: Later vocabulary synthesis or engineering-practice comparison only

Scope: The complete tracked Superpowers checkout at `.tmp/superpowers`

Freshness: Checked-out revision verified 2026-07-22; network freshness intentionally not checked

## Question And Boundary

**Question:** What distinctive, operationally meaningful language and vocabulary
does the Superpowers skill pack use?

This packet extracts terms that change how Superpowers routes, acts, decides,
communicates, or finishes. It covers skill descriptions, every `SKILL.md`, all
disclosed files under `skills/`, tests, hooks, integration code, commands,
metadata, templates, examples, human-facing docs, and dated plans/specs. Scripts
were interpreted only where their names, interfaces, output, or comments define
pack vocabulary.

The intended use is provenance-backed input to later synthesis. This packet
does not select canonical local language, establish that upstream advice is
correct, edit a vocabulary owner, draft skill wording, or modify a runtime
skill. Superpowers terminology was extracted before the local comparison.
Every local comparison below is labeled `synthesis` or `inference`.

Upstream paths in this packet are relative to `.tmp/superpowers/` unless shown
otherwise. Raw token lists, concordances, frequency reports, and copied corpus
material were not persisted.

## Source Identity

| Pack | Origin | Revision | Worktree State | Verified | Authority | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Superpowers | `https://github.com/obra/superpowers.git` | `d884ae04edebef577e82ff7c4e143debd0bbec99` on `main`; commit time 2026-07-02; subject `Release v6.1.1: fix Codex SessionStart hook re-registration, add Codex portal packaging` | Clean, including untracked-file check; `HEAD` equals the checkout's existing `origin/main` tracking ref (`0` ahead, `0` behind) | 2026-07-22 | The checkout is primary evidence for its own language, interfaces, and tracked history | No fetch or network comparison was performed. Equality with the local tracking ref does not prove equality with the current remote repository. |

## Coverage

The authoritative inventory is `git ls-files`, not a visibility-filtered file
walk. All 172 tracked files were accounted for.

| Surface | Inspected / Skipped / Not Applicable | Files Or Count | Consequence |
| --- | --- | --- | --- |
| Skill descriptions and runtime bodies | Inspected | 14 `SKILL.md` files | Current skill routing and procedure are the strongest semantic authority. |
| Disclosed skill references, prompts, templates, examples, and scripts | Inspected | 34 files; 48 total under `skills/` | Current supporting contracts were retained; creation logs and pressure fixtures were status-qualified as historical/evaluation evidence. |
| Tests and evaluation-facing fixtures | Inspected | 52 files; 42 semantic-bearing, 10 support/boilerplate | Assertions and interfaces corroborate some meanings. Descriptive recall tests were not upgraded to behavioral proof. |
| Dated plans and specs | Inspected | 29 files: 4 root plans, 11 Superpowers plans, 14 specs; 12,508 lines | These are point-in-time evidence. They corroborate term history, experiments, and supersession, not current runtime authority by themselves. |
| Human docs, routing, governance, and release history | Inspected | Included in 43 integration/top-level files | Current README, contributor, testing, and porting language was retained; release-note-only terms were treated as historical. |
| Hooks, manifests, harness integrations, metadata, and maintenance/distribution scripts | Inspected | Included in the same 43 files | Names, interfaces, output states, and comments establish bootstrap, tool-mapping, packaging, and integration vocabulary. |
| Binary and vector assets | Inspected; not applicable to semantic extraction | 2 files | Branding was corroborated elsewhere; icon geometry supplied no operational vocabulary. |
| Disclosed external `superpowers-evals` checkout | Skipped: not present in the supplied checkout | 1 external repository referenced by `CLAUDE.md` and `docs/testing.md` | This packet can report the pack's eval vocabulary, but cannot verify current external scenarios, results, or efficacy claims. |

## Vocabulary Clusters

### Skill-First Routing And Harness Activation

Superpowers treats skill use as a compulsory control layer, not an optional
reference lookup. A `1% chance` that a skill applies triggers invocation before
clarification, exploration, or action; `process skills come first` and choose
the approach before implementation skills. Harnesses make this reliable through
a `bootstrap`, `tool mapping`, and `skill discovery + invocation`, with skill
bodies naming actions rather than platform-specific tools.

### Hard Gates And Rationalization Resistance

`Iron Law`, `HARD-GATE`, `Gate Function`, `Red Flags - STOP`, `no exceptions`,
and `rationalization table` form a recurring enforcement dialect. These terms
turn tempting shortcuts into explicit stop, restart, or escalation branches.
`Gate` is overloaded, however: it can mean design approval, proof, task review,
or an output-shape check.

### Spec-To-Finish Delivery And Fresh-Context Roles

The public workflow is brainstorming -> approved spec -> worktree -> plan ->
execution -> review -> branch finish. Planning produces `bite-sized tasks` with
exact paths and proof. `Subagent-Driven Development (SDD)` gives a `controller`
fresh `implementer` and `task reviewer` contexts, serializes tasks, uses two
review verdicts, and ends with broad whole-branch review. Files, not conversation
memory, carry bulky handoffs and recovery state.

### Test-First Proof, Debugging, And Completion

The pack uses `RED-GREEN-REFACTOR` both for production behavior and, by analogy,
for skill wording. Debugging insists on root-cause evidence before a fix.
Completion insists on `fresh verification evidence` immediately before a
claim. Together these phrases recruit an observed-failure -> smallest change ->
fresh proof discipline.

### Skill Authoring And Behavioral Pressure

`Skill Discovery Optimization (SDO)` makes descriptions name triggering
conditions rather than summarize workflow. Skill wording is tested with a
no-guidance baseline, pressure scenarios, captured rationalizations, repeated
micro-tests, and failure-shaped guidance. `Bulletproof` is the pack's aspirational
word for surviving bounded pressure tests, not evidence of universal compliance.

### Worktree And Visual-Companion Ownership

Worktree language is harness-aware: detect existing isolation, prefer native
tools, fall back to Git, avoid `phantom state`, and clean up only what the flow
owns. Brainstorming's optional `visual companion` is a tool rather than a mode;
it communicates through `screens`, `choices`, and an event stream while the
terminal remains the primary conversation channel.

## Retained Vocabulary

| Term | Variants | Class | Meaning In This Pack | Behavior Or Distinction Recruited | Spread | Claim Label | Best Provenance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Skill-first invocation | `1% chance`; invoke before any response/action; explicit skill request | candidate-leading-word; invocation-routing; pack-specific | Skill selection precedes clarification, code inspection, and substantive tool use. | Load a possibly relevant skill first; an explicitly named skill must be invoked. | Runtime body plus explicit-request tests and bootstrap docs | corroborated | `skills/using-superpowers/SKILL.md:10-31`; `tests/explicit-skill-requests/run-test.sh:81-110` | The threshold is intentionally aggressive and can over-trigger; user instructions still take precedence. |
| Process skills come first | skill priority; required sub-skill | invocation-routing; relationship-handoff | Approach-owning skills precede implementation skills. | Resolve method before execution. | `using-superpowers` plus planning/execution dependencies | corroborated | `skills/using-superpowers/SKILL.md:24-31`; `skills/executing-plans/SKILL.md:65-69` | `Process skill` is not defined in a pack glossary. |
| Bootstrap | session-start injection; compaction re-injection | invocation-routing; artifact-state; pack-specific | The full `using-superpowers` control context is made present automatically. | Prevent skills from remaining installed but inert. | Porting guide, hooks, OpenCode/Pi integrations, tests | corroborated | `docs/porting-to-a-new-harness.md:43-55,81-106`; `tests/pi/test-pi-extension.mjs:54-119` | Current Codex packaging appears to rely on native discovery without the guide's stated non-negotiable injection, creating an exception or contradiction. |
| Tool mapping | actions, not tools; platform adaptation | invocation-routing; relationship-handoff | Harness-neutral actions are translated to real platform tool names and payload shapes. | Preserve behavior across tool APIs without inventing unavailable tools. | Porting guide, three skill references, harness implementations/tests | corroborated | `docs/porting-to-a-new-harness.md:33-63,108-122`; `skills/using-superpowers/references/codex-tools.md:1-36` | Some guide-listed mappings are absent or retired. |
| Harness shape | Shape A shell-hook; Shape B in-process plugin/extension; Shape C instructions-file | invocation-routing; pack-specific | Classifies how bootstrap content reaches the model; discovery and injection are separate axes. | Select an integration architecture and its proof. | Porting guide and concrete integrations | direct | `docs/porting-to-a-new-harness.md:167-298` | Shapes may compose; current docs contain platform drift. |
| Unique-marker test | startup/context mechanism test | evidence-completion; pack-specific | A unique string empirically tests whether an assumed injection path actually reaches a fresh session. | Replace documentation inference with an observable acceptance check. | Porting guide and contribution gate | corroborated | `docs/porting-to-a-new-harness.md:174-205,277-286`; `CLAUDE.md:72-91` | Proves delivery of the marker, not every runtime behavior. |
| Brainstorming hard gate | design before implementation; user design approval; terminal state | workflow-control; relationship-handoff | No implementation action occurs until a design is presented and approved; brainstorming ends by invoking `writing-plans`. | Separate creative decision authority from implementation. | Brainstorming body, README workflow, acceptance prompt | corroborated | `skills/brainstorming/SKILL.md:12-18,20-61,121-131`; `README.md:188-204` | The gate is broader than ordinary brainstorming and applies regardless of perceived simplicity. |
| One question at a time | 2-3 approaches; design sections; spec self-review | workflow-control; domain-design | Elicit intent sequentially, compare alternatives, validate design in pieces, then self-check the spec. | Reduce decision overload and expose tradeoffs before commitment. | Brainstorming body | direct | `skills/brainstorming/SKILL.md:20-32,63-72,111-138` | One-message cadence is a pack procedure, not proof of better outcomes. |
| Visual companion | tool, not a mode; screen; choice; event stream; tombstone | artifact-state; pack-specific | Optional browser display for questions better seen than described; structured events return selections to the conversation. | Make visual design options inspectable without moving the whole conversation into the browser. | Skill guide, server/helper code, tests, historical specs | corroborated | `skills/brainstorming/visual-companion.md:5-31,98-160,250-286`; `tests/brainstorm-server/server.test.js:340-383` | Large implementation/security vocabulary is local to this feature; `screen` means HTML artifact. |
| Bite-sized task | task right-sizing; exact steps; no placeholders | workflow-control; artifact-state | A plan unit small enough to implement and verify with exact files, code, and commands. | Turn an approved spec into executable, checkable work. | Writing-plans body and dated plan templates | corroborated | `skills/writing-plans/SKILL.md:10-14,36-154`; `docs/superpowers/specs/2026-06-10-strict-cost-sdd-design.md:66-117` | Historical `chunk` is a document-review boundary, not a concurrency wave. |
| Subagent-Driven Development (SDD) | fresh subagent per task; controller; implementer; task reviewer; whole-branch review | workflow-control; relationship-handoff; pack-specific | Serial controller-managed implementation with curated fresh task context, per-task review, repair, and final broad review. | Limit context pollution while preserving task fidelity and review. | Runtime skill, prompts, helper scripts, tests, dated redesign docs | corroborated | `skills/subagent-driven-development/SKILL.md:6-17,45-82,159-218`; `tests/claude-code/test-subagent-driven-development-integration.sh:138-156` | `Independent` here permits fresh ownership but explicitly does not license parallel implementers. SDD can collide with “software design document.” |
| File-backed handoff | task brief; report file; review package; progress ledger; recovery map | artifact-state; relationship-handoff; pack-specific | Requirements, claims, diffs, and completion state move by path; the ledger owns recovery after compaction. | Keep bulk evidence stable and prevent redispatch after context loss. | SDD body plus executable helpers and release history | corroborated | `skills/subagent-driven-development/SKILL.md:181-265`; `skills/subagent-driven-development/scripts/task-brief:1-40` | Helpers depend on plan-heading conventions; shared worktree runs can collide. |
| Two-verdict task review | Spec Compliance; Task quality; `Cannot verify from diff`; Critical/Important/Minor | evidence-completion; relationship-handoff; pack-specific | One reviewer reads the task diff once and separately judges requirement fidelity and implementation quality. | Prevent “right thing” and “built right” from masking each other. | Reviewer prompt, SDD body, dated supersession spec | corroborated | `skills/subagent-driven-development/task-reviewer-prompt.md:78-165`; `docs/superpowers/specs/2026-06-09-sdd-task-scoped-review-dispatch-design.md:28-34,123-147` | Current tests strongly assert workflow shape but do not fully prove review ordering or repair loops from transcripts. |
| Implementation status protocol | `DONE`; `DONE_WITH_CONCERNS`; `NEEDS_CONTEXT`; `BLOCKED` | artifact-state; relationship-handoff; pack-specific | Implementer status determines whether the controller reviews, supplies context, redispatches, or stops. | Make uncertainty and partial completion actionable. | SDD body and implementer prompt | corroborated | `skills/subagent-driven-development/SKILL.md:132-157`; `skills/subagent-driven-development/implementer-prompt.md:113-138` | Similar words have broader meanings outside SDD; interpret within the role protocol. |
| Independent problem domain | focused; self-contained; isolated context; no shared state | invocation-routing; workflow-control | Parallel dispatch is allowed only for unrelated investigations that do not share state or dependencies. | Convert true independence into concurrent legwork. | Parallel-dispatch body | direct | `skills/dispatching-parallel-agents/SKILL.md:10-46,49-91,129-175` | Collides with SDD's “independent tasks,” which are executed serially. |
| Iron Law / hard gate | Gate Function; Red Flags - STOP; start over; no exceptions | workflow-control; failure-exclusion; pack-specific | Bright-line wording marks a non-negotiable precondition and names shortcut rationalizations. | Stop an agent at predictable failure branches. | Brainstorming, TDD, debugging, verification, writing-skills | corroborated | `skills/test-driven-development/SKILL.md:31-45,272-287`; `skills/verification-before-completion/SKILL.md:16-38,52-75` | `Gate` has several meanings; exceptions exist despite categorical rhetoric. |
| RED-GREEN-REFACTOR | watch RED fail; minimal GREEN; stay green | workflow-control; evidence-completion; domain-design | Observe the intended failure, make the smallest passing change, then clean up without adding behavior. | Prove the test can fail and constrain implementation. | TDD body, README, planning, writing-skills analogy, tests | corroborated | `skills/test-driven-development/SKILL.md:31-71,113-192`; `README.md:194-200` | Established professional language, not pack-invented; Superpowers applies it unusually broadly to skill authoring. |
| Systematic debugging | root cause; symptom fix; pattern analysis; single hypothesis; trace backward | workflow-control; evidence-completion | Four phases gather evidence, compare working patterns, test one hypothesis minimally, then fix the root cause. | Replace guess-and-check with a falsifiable investigation. | Debugging body and disclosed techniques | corroborated | `skills/systematic-debugging/SKILL.md:46-213`; `skills/systematic-debugging/root-cause-tracing.md:32-65,130-154` | The `3+ failed fixes` architecture heuristic is pack-specific and qualified by context. |
| Defense-in-depth / condition-based waiting | fix at source; layered validation; condition polling; test polluter | domain-design; failure-exclusion | After root cause, add validation at meaningful layers; replace arbitrary delays with polling on the real condition; isolate order-dependent pollution. | Prevent recurrence and remove timing guesses. | Debugging references and helper script | corroborated | `skills/systematic-debugging/defense-in-depth.md:20-94`; `skills/systematic-debugging/condition-based-waiting.md:1-82` | Mostly established professional techniques; impact numbers in the docs are not substantiated here. |
| Evidence before claims | fresh verification evidence; full command; full output; actual status | evidence-completion; candidate-leading-word | A success claim is allowed only after a current proving command has been run and read. | Block completion based on memory, expectation, partial checks, or another agent's report. | Verification body, README philosophy, implementer/reviewer prompts | corroborated | `skills/verification-before-completion/SKILL.md:8-38,40-106`; `README.md:232-238` | “In this message” is harness/session-model dependent; one command proves only its scope. |
| Technical correctness over social comfort | verify before implementing; performative agreement; reasoned pushback | failure-exclusion; relationship-handoff; pack-specific | Review feedback is a claim to evaluate against code, not an order or social-performance prompt. | Ask, verify, and push back when evidence conflicts. | Review-reception body | direct | `skills/receiving-code-review/SKILL.md:8-38,59-98,113-174,203-213` | The absolute ban on gratitude is pack voice, not necessary evidence of technical rigor. |
| Skill Discovery Optimization (SDO) | triggering conditions; description is when, not workflow; violation symptoms | candidate-leading-word; invocation-routing; pack-specific | Metadata should recruit loading conditions without giving a workflow shortcut that displaces the body. | Improve skill discovery and force full instruction loading. | Writing-skills body and platform-neutral rename spec | corroborated | `skills/writing-skills/SKILL.md:93-103,140-213,544-550,668-679`; `docs/superpowers/specs/2026-05-05-platform-neutral-prose-design.md:17,49-52` | Bundled Anthropic guidance in the checkout says descriptions include what and when, so the local reference conflicts with Superpowers' rule. |
| Pressure testing for skills | baseline behavior; pressure scenario; no-guidance control; rationalization table; micro-test; variance | evidence-completion; workflow-control; pack-specific | Run the scenario without guidance, capture failures and excuses, add the smallest guidance, then retest under competing pressures. | Make wording answer observed failure rather than intuition. | Writing-skills body/reference, fixtures, contributor docs, eval plans | corroborated | `skills/writing-skills/SKILL.md:10-45,459-585,633-655`; `skills/writing-skills/testing-skills-with-subagents.md:43-176` | Current external eval results are unavailable; historical “100%” and “bulletproof” claims remain thin. |
| Match the form to the failure | prohibition; positive recipe; structural slot; observable conditional | domain-design; failure-exclusion; pack-specific | Guidance form depends on whether the baseline failure is discipline, wrong shape, omission, or a conditional decision. | Avoid using prohibition reflexively when it worsens output. | Current authoring body plus dated micro-test spec | corroborated | `skills/writing-skills/SKILL.md:459-480,575-585`; `docs/superpowers/specs/2026-06-10-positive-instruction-redesign-design.md:6-34,96-144` | Transfer requires a fresh control for the new wording problem. |
| Native-tool-first isolation | detect-and-defer; consent bridge; Git fallback; never fight the harness; phantom state | workflow-control; artifact-state; pack-specific | Detect existing isolation, prefer harness-native worktree support, and clean only workspaces the workflow owns. | Preserve harness state and establish a clean baseline before implementation. | Worktree/finish skills, tests, dated rototill design | corroborated | `skills/using-git-worktrees/SKILL.md:8-61,121-202`; `skills/finishing-a-development-branch/SKILL.md:161-182,211-232` | Tests prove absence of manual Git in some cases more strongly than positive native-tool use; directory provenance is heuristic. |

## Techniques Encoded By The Language

| Vocabulary | Technique | Essential Mechanics | Use Context In The Pack | Failure / Misuse Risk | Claim Label | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| Skill-first invocation + bootstrap | Automatic method routing | Inject the bootstrap; inspect metadata; invoke before substantive response; order process before implementation | Every session and explicit skill request | Over-triggering or inert installed skills when injection/discovery fails | corroborated | `skills/using-superpowers/SKILL.md:10-31`; `docs/porting-to-a-new-harness.md:43-55` |
| Unique-marker test + acceptance prompt | Verify a harness integration live | Put a unique marker through the claimed startup path, then start a fresh session and require brainstorming before code for a fixed prompt | New harness port | Marker delivery alone can pass while downstream behavior is wrong | corroborated | `docs/porting-to-a-new-harness.md:134-205` |
| Brainstorming hard gate | Design before implementation | Ask one question at a time, compare 2-3 approaches, present design sections, self-review, obtain approval, hand off to planning | Creative work | Can add ceremony to trivial changes; pack intentionally accepts that cost | direct | `skills/brainstorming/SKILL.md:12-72,102-138` |
| Bite-sized tasks + SDD | Serial fresh-context implementation | Curate one task brief, dispatch implementer, collect proof, run dual-verdict task review, repair/re-review, update ledger, finish with broad review | Approved multi-task implementation plans | Parallel implementation conflicts; stale or malformed briefs damage fidelity | corroborated | `skills/subagent-driven-development/SKILL.md:45-82,181-265` |
| RED-GREEN-REFACTOR | Test-first behavioral proof | Observe correct failure, write minimal code, observe pass, refactor while green | Features and bug fixes | A test that never went red may only confirm existing behavior | direct | `skills/test-driven-development/SKILL.md:47-192` |
| Systematic debugging | Root-cause investigation | Reproduce/gather evidence, analyze patterns, form one hypothesis, change one variable, implement only after confirmation | Bugs, test failures, unexpected behavior | Rigid numerical heuristics or calling incomplete investigation “no root cause” | direct | `skills/systematic-debugging/SKILL.md:46-213,245-276` |
| Fresh verification evidence | Claim gate | Identify the proving command, run it now, read all output, confirm scope, state claim with evidence | Completion, fixes, commits, PRs, delegation | A partial command can be overclaimed; freshness is tied to message semantics | corroborated | `skills/verification-before-completion/SKILL.md:16-48,76-106` |
| Skill pressure testing | Documentation TDD | Establish no-guidance failure, classify it, author minimal guidance, repeat under pressure, manually inspect matches and variance | Discipline- and behavior-shaping skills | Bounded samples cannot justify “bulletproof”; prohibition can backfire on shape failures | corroborated | `skills/writing-skills/SKILL.md:459-585,633-655` |
| Native-tool-first worktrees | Ownership-aware isolation | Detect existing isolation, ask/consume consent, prefer native tool, fall back to Git, verify baseline, clean by provenance | Feature work and plan execution | Manual fallback can create phantom harness state; cleanup provenance is imperfect | corroborated | `skills/using-git-worktrees/SKILL.md:16-100,121-202`; `skills/finishing-a-development-branch/SKILL.md:161-182` |
| Visual companion event loop | Mixed visual/text elicitation | Offer just in time, render a screen, collect structured choice/event, continue in terminal, unload or tombstone on stop | Visually clearer brainstorming questions | Stale events, auth failures, or treating the browser as the whole conversation | corroborated | `skills/brainstorming/visual-companion.md:98-160,250-286`; `tests/brainstorm-server/auth.test.js:148-286` |

## Aliases, Collisions, And Inconsistencies

| Terms | Relationship | Evidence | Consequence For Interpretation |
| --- | --- | --- | --- |
| `independent tasks` in SDD vs `independent problem domains` in parallel dispatch | Same adjective, opposite scheduling consequence | `skills/subagent-driven-development/SKILL.md:367-389`; `skills/dispatching-parallel-agents/SKILL.md:14-46` | SDD independence permits isolated fresh ownership but remains serial; parallel skill independence licenses concurrency. |
| `gate` | Overloaded | Design `skills/brainstorming/SKILL.md:12-18`; proof `skills/verification-before-completion/SKILL.md:24-38`; task review `skills/subagent-driven-development/task-reviewer-prompt.md:78-165`; authoring `skills/test-driven-development/testing-anti-patterns.md:51-61` | Preserve the qualifier; unqualified `gate` has no single pack-wide meaning. |
| `spec` / `plan` / `task` / `review` | Scope family, not aliases | `skills/brainstorming/SKILL.md:102-131`; `skills/writing-plans/SKILL.md:36-174`; `skills/subagent-driven-development/task-reviewer-prompt.md:18-23` | A spec is the approved design, a plan is the durable implementation artifact, and a task is the dispatch/review unit; reviews exist at document, task, and branch scope. |
| Spec Compliance / Task quality vs local Spec / Standards | Partial conceptual overlap | Upstream `skills/subagent-driven-development/task-reviewer-prompt.md:78-165`; local `docs/agents/engineering-contract.md:29` | `synthesis`: both separate “right thing” from “built right,” but upstream's task verdict protocol is narrower than the local review axes. |
| RED/GREEN | Deliberate analogy | Code `skills/test-driven-development/SKILL.md:47-192`; skills `skills/writing-skills/SKILL.md:10-45` | Always name whether the observed failure is program behavior or agent behavior. |
| SDD | Pack abbreviation with external collision | `skills/subagent-driven-development/SKILL.md:1-12` | In this pack it means Subagent-Driven Development, not software/system design document. |
| Skill description: “when only” vs bundled external guidance: “what and when” | Internal source conflict | `skills/writing-skills/SKILL.md:140-180`; `skills/writing-skills/anthropic-best-practices.md:185-219` | Superpowers' runtime authoring rule and its bundled reference disagree; the packet does not choose which is correct. |
| Reference-skill testing | Internal procedure conflict | `skills/writing-skills/testing-skills-with-subagents.md:25-28`; `skills/writing-skills/SKILL.md:433-442` | The older disclosed reference says not to test pure references; the current body prescribes retrieval/application/gap tests. |
| Bootstrap is non-negotiable vs Codex native discovery | Current integration tension | `docs/porting-to-a-new-harness.md:49-55,86-106`; `.codex-plugin/plugin.json:23-24`; `RELEASE-NOTES.md:3-12` | Either Codex is an unstated native-discovery exception or the porting doctrine is stale. |
| Gemini support | Current/historical drift | `RELEASE-NOTES.md:28-30`; `README.md:14`; `GEMINI.md:1-2`; `docs/porting-to-a-new-harness.md:791` | Removed-support prose coexists with shipped files and a missing `gemini-tools.md` reference; do not infer a coherent current Gemini contract. |
| Visual `screen` / `terminal` | Pack-specific senses | `docs/superpowers/specs/2026-02-19-visual-brainstorming-refactor-design.md:13-30` | `Screen` is generated HTML and `terminal` is the text conversation channel, not necessarily a monitor and shell. |
| `bulletproof` / `100% compliance` | Aspirational outcome language | `skills/writing-skills/testing-skills-with-subagents.md:267-306`; `skills/writing-skills/SKILL.md:575-585` | Treat as bounded historical test results, not external or universal validity. |

## Inferred Applications And Local Comparison

All statements in this section are downstream comparisons, not Superpowers
source claims.

- **Synthesis:** Superpowers' `Evidence before claims` strongly overlaps the
  local engineering contract's `Evidence: inspectable support for a claim` and
  the local research preference for `evidence` and `proof`. Superpowers adds an
  immediate message-scoped claim gate; the local contract adds proportionality,
  semantic proof, proof seams/lanes, and residual-risk reporting.
  (`skills/verification-before-completion/SKILL.md:8-38`;
  `docs/agents/engineering-contract.md:20-32,83-92`;
  `docs/research/language/03-high-signal-steering-words.md:45-50`)

- **Synthesis:** Upstream two-verdict review and local `Spec / Standards` share
  the same high-level separation. They are not aliases: upstream judges one
  task's spec compliance and task quality, while the local owner defines review
  axes across an immutable review snapshot.
  (`skills/subagent-driven-development/task-reviewer-prompt.md:78-165`;
  `docs/agents/engineering-contract.md:24-32`)

- **Synthesis:** Superpowers' `RED-GREEN-REFACTOR` matches the local professional
  steering term, including observed failure and minimal passing change. The
  distinctive upstream addition is its direct analogy to skill/documentation
  behavior testing.
  (`skills/test-driven-development/SKILL.md:47-192`;
  `skills/writing-skills/SKILL.md:10-45`;
  `docs/research/language/03-high-signal-steering-words.md:33-36`)

- **Synthesis:** Upstream debugging's repro/evidence/single-hypothesis language
  aligns with the local `repro`, `hypothesis`, and `probe` cluster. Upstream's
  `Iron Law` rhetoric and exact `3+ fixes` architecture stop are pack-specific
  control mechanisms, not local professional terms.
  (`skills/systematic-debugging/SKILL.md:46-213`;
  `docs/research/language/03-high-signal-steering-words.md:45-47`)

- **Synthesis:** Upstream `bootstrap` is materially different from the local
  `Global AGENTS template` and `agent primer`. Upstream means automatic runtime
  injection of a complete control skill; locally, the global template exposes
  route/setup and the short repo primer points to owning contracts. Treating
  these as aliases would erase ownership and loading differences.
  (`docs/porting-to-a-new-harness.md:43-55`;
  `CONTEXT.md:100-124`)

- **Synthesis:** Superpowers' file-backed `task brief`, `review package`, and
  `progress ledger` are concrete context-engineering artifacts. The local bridge
  vocabulary names the broader concerns as `context engineering`, `context
  budget`, `trajectory`, and `observability` without prescribing these exact
  artifact names.
  (`skills/subagent-driven-development/SKILL.md:181-265`;
  `docs/research/language/04-agentic-bridge-vocabulary.md:66-82`)

- **Synthesis:** Superpowers' skill pressure testing overlaps the local
  `evaluation harness`, `feedback signal`, and `completion criterion` bridge.
  Upstream contributes operational terms for no-guidance controls, pressure
  scenarios, captured rationalizations, and variance; this packet does not
  establish that those should become canonical local vocabulary.
  (`skills/writing-skills/SKILL.md:575-585,633-655`;
  `docs/research/language/04-agentic-bridge-vocabulary.md:76-87`)

- **Inference:** `Match the form to the failure` may be useful evidence for
  later local skill-authoring synthesis because it distinguishes discipline,
  output-shape, omission, and conditional failures. Adoption would require
  fresh local controls showing the taxonomy improves behavior rather than
  merely adding terminology.

- **Inference:** `Actions, not tools` may help later harness-portability work,
  but local use would need to preserve concrete tool availability and proof
  seams; an overly abstract action vocabulary could hide capability differences.

## Prune Log

| Removed Or Merged Material | Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |
| Generic engineering words: TDD alone, DRY, YAGNI, error handling, type safety, coverage, scalability | Established terms without distinctive pack meaning | RED-GREEN-REFACTOR, task review, and explicit workflow gates | A narrower study examines how the pack redefines one term |
| Generic headings: Overview, Core Principle, When to Use, Quick Reference, Common Mistakes | Structural boilerplate | Named semantic clusters | A document-structure study is requested |
| Exact harness API/tool names | Platform mechanics, not semantic owners | Tool mapping and harness shape | A harness-specific integration packet is requested |
| Browser/server protocol primitives, CSS, RFC 6455, HTTP details | Implementation mechanics | Visual companion event loop and fail-closed session concept | Visual companion architecture becomes the question |
| Contributor rhetoric, hiring, commercial services, funding, telemetry, community, conduct, license | Human/governance context without reusable workflow semantics | One-problem-per-PR and eval requirements were considered but not retained as core vocabulary | Repository governance voice becomes the question |
| `Prime Radiant` branding and icon geometry | Branding does not recruit an engineering behavior | Visual companion | Product-brand language becomes in scope |
| Unsupported impact numbers and session anecdotes | Thin, unreplicated evidence | Traceable techniques | Current replicated results become available |
| Historical `Description Trap`, `SUBAGENT-STOP`, slash commands, named reviewer agent, old global worktree path, old symlink install | Retired or superseded surfaces | Current SDO, SDD, worktree, and integration owners | Historical evolution becomes the question |
| Historical two separate task reviewers | Explicitly superseded by one reviewer/two verdicts | Two-verdict task review | A version-history comparison is requested |
| Historical document-review `chunk` and loops | Dated and apparently dormant in current parent skills | Bite-sized task and current handoff pipeline | Current runtime references the review prompts again |
| Cheap-controller/reviewer tiers and cost experiment rungs | Failed experiments, not recommendations | Judgment remains controller/reviewer owned | A cost-model experiment history is requested |
| `Worktree Rototill` | Memorable historical project name, not current runtime vocabulary | Native-tool-first isolation | The design's evolution becomes the question |
| Frequency-only words and raw event/status strings | Frequency or interface presence alone is not semantic admission | Cluster owner that explains the behavior | A term gains a defined decision or cross-surface role |

## Evidence Gaps

- The checkout was not fetched. The exact inspected revision and clean equality
  with its existing `origin/main` ref are verified; current network-remote
  equality is not.
- The disclosed external `superpowers-evals` repository is absent. This packet
  cannot verify current LLM scenarios, actor/verifier judgments, repeated-run
  results, or claims that wording is `bulletproof`.
- Several tests are description-recall or negative assertions. In particular,
  current tests do not fully prove SDD self-review, review ordering, repair-loop
  closure, or positive native-worktree-tool invocation.
- Current integration documentation has material drift: Gemini is both removed
  and shipped; Antigravity mechanisms conflict; multiple tool-mapping references
  are missing; and Codex appears to be an unnamed exception to bootstrap
  doctrine.
- The current writing-skills body conflicts with its bundled Anthropic reference
  on description content and with an older disclosed reference on testing pure
  reference skills.
- Dormant spec/plan reviewer prompt files are disclosed but not invoked by the
  current parent skills. Dated plans/specs prove historical meaning only.
- No external-origin study was performed. The packet distinguishes established
  professional terms from pack-specific language based on ordinary provenance,
  but does not independently verify intellectual history or external efficacy.
- No pack-level glossary resolves overloaded words such as `gate`, `review`,
  `independent`, `fresh`, `task`, or `spec`.

These gaps limit claims about effectiveness, current remote freshness, and
local suitability. They do not prevent a provenance-backed answer about the
language present in the supplied checked-out revision.

## Source Trace

| Source | Authority | Version Or Date | Supports |
| --- | --- | --- | --- |
| `skills/using-superpowers/` and explicit-request tests | Runtime owner plus routing checks | `d884ae04` | Compulsory invocation, process precedence, platform references |
| `skills/brainstorming/` and brainstorm-server tests | Runtime owner plus executable feature contracts | `d884ae04` | Design gate, elicitation, visual companion, screen/event vocabulary |
| `skills/writing-plans/` | Runtime planning owner | `d884ae04` | Bite-sized tasks, exact plans, handoff choices |
| `skills/subagent-driven-development/` and Claude Code tests | Runtime role/protocol owner plus partial workflow checks | `d884ae04` | Fresh-context roles, file handoffs, statuses, two-verdict review, recovery |
| `skills/test-driven-development/` | Runtime TDD owner | `d884ae04` | Iron Law and RED-GREEN-REFACTOR |
| `skills/systematic-debugging/` | Runtime debugging owner and disclosed techniques | `d884ae04` | Root cause, hypothesis, tracing, layered validation, condition waiting |
| `skills/verification-before-completion/` | Runtime completion-claim owner | `d884ae04` | Fresh evidence and claim gate |
| `skills/writing-skills/` | Runtime skill-authoring owner plus references/evaluation fixtures | `d884ae04` | SDO, skill types, pressure testing, failure-shaped guidance |
| `skills/using-git-worktrees/` and `skills/finishing-a-development-branch/` | Runtime isolation and cleanup owners | `d884ae04` | Native-first isolation, baseline, provenance-aware cleanup and options |
| `docs/porting-to-a-new-harness.md`, hooks, manifests, integrations, and packaging tests | Cross-harness design and executable interface authority | `d884ae04` | Bootstrap, tool mapping, harness shapes, injection, distribution and drift |
| `docs/plans/` and `docs/superpowers/{plans,specs}/` | Dated point-in-time design, plan, and experiment evidence | 2025-11-22 through 2026-06-11 | Historical definitions, measured experiments, supersessions, and limitations |
| Local `CONTEXT.md`, `docs/agents/engineering-contract.md`, and language research owners | Current local vocabulary owners | Inspected 2026-07-22 | Synthesis/inference-only overlap and collision analysis |

## Final Decision

`source-packet-complete`

The supplied revision is fully accounted for; retained terms have semantic
meaning, exact provenance, claim strength, limitations, and one cluster;
historical and current sources are distinguished; aliases and collisions are
visible; generic and retired material is pruned; and local comparisons remain
explicitly downstream synthesis or inference.
