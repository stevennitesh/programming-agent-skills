# Upper-Bound Engineering Language

Status: answered

Supports: language and method selection while authoring documents under
docs/synthesis/skills/

Scope: cross-packet distillation of the Matt Pocock, Superpowers, and Ponytail
vocabulary packets, compared with the two existing local language documents
named below and corrected only for the five slicing, readiness, and migration
claims validated by UBL-01 and decided by UBL-24

Freshness: source packets, local comparison owners, and completed UBL
validation evidence inspected or applied 2026-07-22

## Purpose And Boundary

This document answers: across the three inspected skill-pack vocabulary
packets, which concepts, methods, techniques, and steering terms create the
strongest useful pressure for designing or improving coding-agent skills?

This is synthesis intake. It is not canonical vocabulary, a universal
engineering sequence, a runtime instruction, or authority to change a skill.
The three generated vocabulary packets are the only source evidence about the
upstream packs. UBL-01 adds bounded semantic and professional evidence only for
the five admitted slicing, readiness, and migration claims; UBL-24 owns their
correction decision. Engineering Steering Vocabulary and Agentic Bridge
Vocabulary are comparison-only local terminology owners: they help deduplicate
language and expose collisions, but they do not turn an upstream claim into a
local decision.

Evidence keys used throughout:

- M: [Matt Pocock Skills vocabulary packet](matt-pocock-skills-vocabulary.md)
- S: [Superpowers vocabulary packet](superpowers-skill-pack-vocabulary.md)
- P: [Ponytail vocabulary packet](ponytail-skill-pack-vocabulary.md)
- L-Steer: [Engineering Steering Vocabulary](03-high-signal-steering-words.md)
- L-Bridge: [Agentic Bridge Vocabulary](04-agentic-bridge-vocabulary.md)
- V-00: [UBL-00 claim ledger](validation/UBL-00-claim-ledger.md)
- V-01: [UBL-01 slicing and migration source packet](validation/UBL-01-slicing-and-migration.md)
- V-24: [UBL-24 final correction decision](validation/UBL-24-final-correction-decision.md)

The labels direct and corroborated retain the source packets' claim labels.
Synthesis marks a comparison, merge, or proposed local use. Inference marks an
application that needs downstream validation. Provenance cells use two locator
forms: M, S, or P plus a semantic-owner suffix points into an upstream packet,
whose linked record preserves the exact repository path, line locator, claim
label, conditions, and limits; V-01 plus an S-number points to an externally
inspected source record, while UBL01-C1 through UBL01-C5 identify its validated
claim dispositions. V-00 owns admission and status, and V-24 owns only the
bounded correction decision. This pass did not reopen upstream repositories.
Cross-pack repetition establishes shared skill-pack usage only. It does not
establish professional correctness, behavioral effectiveness, or local
suitability. V-01 establishes bounded source fidelity for UBL01-C1 through
UBL01-C5; it and V-24 explicitly leave behavioral effect, transfer, and local
suitability `untested`.

## Source Registry

| Evidence Key | Inspected Revision And Coverage | Completion Status | Authority | Material Limitations |
| --- | --- | --- | --- | --- |
| M | Matt Pocock Skills, ed37663cc5fbef691ddfecd080dff42f7e7e350d; 167 tracked files accounted for; checkout verified 2026-07-22 | source-packet-complete | Primary evidence for that revision's instructions, metadata, references, scripts, examples, and status buckets | No network fetch; package versions conflict; no behavioral tests; in-progress, personal, miscellaneous, and deprecated terms do not establish promoted behavior; external term origins were not verified |
| S | Superpowers, d884ae04edebef577e82ff7c4e143debd0bbec99; 172 tracked files accounted for; checkout verified 2026-07-22 | source-packet-complete | Primary evidence for that revision's runtime skills, disclosed material, tests, integrations, plans, and specs | No network fetch; external superpowers-evals checkout absent; several tests prove recall or negative shape rather than full behavior; integration docs drift; current and historical authoring guidance conflict |
| P | Ponytail, 16f29800fd2681bdf24f3eb4ccffe38be3baec6b; 156 tracked files accounted for; checkout verified 2026-07-22 | source-packet-complete | Primary evidence for that revision's canonical skills, adapters, commands, tests, benchmarks, examples, and docs | No network fetch; host adapters disagree on lifecycle terms; short copies omit ladder rungs; benchmark evidence is task-, model-, scorer-, and sample-bound; several checks are structural proxies; six PNGs had no inspectable textual contract |
| V-00 | UBL-00 claim ledger; reconciled 2026-07-22 | source-packet-complete | Owns admission, claim IDs, active/deferred state, and revisit triggers | Routes evidence and preserves status; does not prove source meaning or behavior |
| V-01 | UBL-01 source packet; 16 source records / 22 directly inspected pages checked 2026-07-22 | source-packet-complete | Registry and synthesis of primary or canonical semantic evidence plus bounded professional counterpressure for UBL01-C1 through UBL01-C5 | Full current tracer-bullet chapter access was partial; frontier lacks a stable general definition; expand-contract/product-slice separation is inference; behavior remains untested |
| V-24 | UBL-24 correction decision; completed 2026-07-22 | source-packet-complete | Owns the bounded split, narrow, demote, and row-level application decisions | Source-synthesis judgment only; does not authorize or establish downstream behavioral, transfer, or local results |

The three upstream packets report complete accounting of their supplied
revisions. That completeness supports vocabulary distillation, not claims that
the instructions work well. The validation records add only the bounded source
decisions and limitations stated in their rows.

## Fast Lookup

| Desired Behavior | Preferred Steering Language | Operational Companion | Evidence Or Completion Gate | Avoid / Misuse Risk | Best Provenance |
| --- | --- | --- | --- | --- | --- |
| **Invocation and routing** | - | - | - | - | - |
| Choose the method owner before implementation | Router skill; process skills come first | Resolve an explicit request or triggering condition, load the owning method, and keep a router route-only | The selected owner is named or loaded before substantive action; a router performs no downstream work | Superpowers' 1% threshold can over-trigger; Matt's router cannot invoke another user-invoked skill | synthesis; M corroborated: writing-great-skills/GLOSSARY.md:19-59 and ask-matt/SKILL.md:7-13; S corroborated: using-superpowers/SKILL.md:10-31 |
| Make an installed skill reachable | Model-invoked or user-invoked; triggering conditions | Separate discovery metadata from procedural body and test discovery in a fresh context | The intended prompt loads the skill and the body, not a metadata shortcut, controls the response | Installed does not mean active; S conflicts internally on description as when-only versus what-and-when | synthesis; M corroborated: .agents/invocation.md:1-16; S corroborated: writing-skills/SKILL.md:93-103,140-213 |
| **Context and information loading** | - | - | - | - | - |
| Recruit a strong prior without restating a procedure | Leading word | Use one established, compact term, then supply the action and gate it must recruit | A no-guidance comparison shows the term changes the target behavior without hiding required mechanics | Invented or decorative terms become no-ops and add definition cost | synthesis; M corroborated: writing-great-skills/GLOSSARY.md:129-135; L-Steer and L-Bridge own the local comparison |
| Keep the common path visible and conditional detail available | Context pointer plus progressive disclosure | Put common-path action inline; name the condition and target for branch-specific material | Retrieval or application probes show required material is loaded in the branch that needs it | A bare link is not a reliable pointer; required material must return inline if retrieval still misses | synthesis; M direct: writing-great-skills/SKILL.md:30-44 and GLOSSARY.md:37-41,101-105 |
| Preserve one semantic owner across contexts | Single source of truth; file-backed handoff; thin adapter | Point to settled artifacts, carry bulky evidence by path, and adapt transport rather than duplicate behavior | A fresh context recovers state from the path; parity or drift checks prove adapters preserve the owner | File existence does not prove loading; fallback copies and malformed briefs can drift | synthesis; M corroborated: writing-great-skills/SKILL.md:53-83 and handoff/SKILL.md:7-17; S corroborated: subagent-driven-development/SKILL.md:181-265; P corroborated: docs/agent-portability.md:3-38 |
| **Intent, requirements, and decisions** | - | - | - | - | - |
| Resolve dependent human decisions | Shared understanding; one question at a time | Look up facts independently, walk one decision branch at a time, recommend, and leave judgment with the human | The human confirms the resulting understanding before action | Bulk questionnaires lose dependency order; a mandatory interview adds ceremony when no judgment is open | synthesis; M corroborated: grilling/SKILL.md:6-12; S direct: brainstorming/SKILL.md:20-32,63-72 |
| Keep product meaning stable | Active domain modeling; canonical term; domain model | Challenge ambiguity with concrete scenarios, check existing use, and update the owning glossary when authorized | Examples agree with the term and its invariants; durable decisions meet the stated ADR bar | A glossary is not a full specification; routine choices create decision sediment | synthesis; M corroborated: domain-modeling/SKILL.md:44-74; L-Steer owns ubiquitous language and domain model locally |
| **Planning, slicing, and dependency control** | - | - | - | - | - |
| Prove one real path early | Tracer bullet | Build a skeletally thin path through the real components needed for selected feedback, observe it, and adjust from the proven base | The named path runs through real components and yields executable or inspectable evidence | It need not be customer-complete or final architecture and does not define task size or diff volume | synthesis; M corroborated: to-tickets/SKILL.md:25-40; V-01 S01-S03 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| Deliver one behavior end to end | Vertical slice | Organize the relevant concerns around one request or valuable behavior | The behavior is usable or testable through its claimed boundary under the local completion policy | It need not touch every named architectural layer and does not establish concurrency, task size, or diff volume | synthesis; V-01 S04-S07 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| Expose what can start now | Predecessor edges; dependency-ready set | Record actual dependencies; define frontier only locally as open, unclaimed work whose named predecessors are satisfied | Every eligible item has its named predecessors satisfied and its own proof condition; state, resource, ownership, write, and conflict constraints are checked before concurrency | Readiness is domain-relative; a list or frontier alone does not justify parallelism | synthesis; M corroborated: to-tickets/SKILL.md:38-65; V-01 S08-S11 and UBL01-C4; behavioral effect untested |
| **Implementation and test-first proof** | - | - | - | - | - |
| Prove behavior before general implementation | RED-GREEN-REFACTOR | Observe the intended failure, make the smallest passing change, then simplify while green | The test is seen red for the right reason and green after the minimal change; refactoring retains green | M's runtime body moves refactoring to review while its metadata uses the three-part phrase | synthesis; S corroborated: test-driven-development/SKILL.md:31-71,113-192; M corroborated but conflicted: tdd/SKILL.md:8,34-36 |
| Minimize new machinery without under-delivery | Existing owner before new code; shortest working diff | Understand and trace first; check local reuse, standard or platform capability, and installed dependencies before adding code | All explicit behavior and safety floors hold; any new dependency or abstraction has a concrete insufficiency case | Shortest can become code golf or a patch at the wrong semantic owner | synthesis; P corroborated: ponytail/SKILL.md:32-64 and docs/platform-native.md:197-211 |
| **Debugging and uncertainty reduction** | - | - | - | - | - |
| Anchor diagnosis in the exact symptom | Tight, red-capable feedback loop | Build and run one deterministic, fast, agent-runnable reproducer before theorizing | The exact symptom is red before repair and the same loop is green afterward | A nearby failure or never-run command creates evidence for the wrong problem | synthesis; M corroborated: diagnosing-bugs/SKILL.md:12-60; S direct: systematic-debugging/SKILL.md:46-213 |
| Repair the shared cause, not the visible path | Root cause, not symptom; caller trace | Enumerate affected callers, trace backward, and place the repair at their shared semantic owner | All affected paths are covered and a regression check locks the real failure | Root cause as rhetoric is generic; assuming a shared owner without tracing callers can broaden damage | synthesis; P corroborated: ponytail/SKILL.md:50-54; S corroborated: systematic-debugging/root-cause-tracing.md:32-65,130-154 |
| **Design, interfaces, and simplification** | - | - | - | - | - |
| Hide substantial behavior behind a small caller surface | Deep module; interface; seam | Apply the deletion test, keep internal seams private, and test through the public interface | Removing the module would recreate meaningful behavior; caller-facing tests do not couple to internals | A pass-through module or hypothetical seam adds indirection; seam is not automatically boundary | synthesis; M corroborated: codebase-design/SKILL.md:10-28,60-67,97-109 |
| **Review, evidence, and completion** | - | - | - | - | - |
| Stabilize the review target and keep judgments independent | Fixed point; two-axis review; Spec and Standards | Resolve the comparison baseline, then judge requested behavior and engineering quality separately | Findings cite the immutable target and retain their axis; an absent spec is reported, not invented | Blended verdicts let one axis mask the other; S's task protocol is narrower than M's review model | synthesis; M corroborated: code-review/SKILL.md:6-23,74-87; S corroborated: subagent-driven-development/task-reviewer-prompt.md:78-165 |
| Prevent success claims from outrunning proof | Evidence before claims; fresh verification evidence | Identify the proving command, run it now, read all output, and limit the claim to its scope | Current output supports the exact claim; residual uncertainty remains visible | Memory, partial checks, or another agent's report are not fresh proof; one command proves only its scope | synthesis; S corroborated: verification-before-completion/SKILL.md:8-48,76-106; M corroborated: completion criterion and legwork |
| Make done demanding and distinguishable | Completion criterion plus legwork | Define the observable end state and the work required inside it before exposing later steps | Every criterion is checked; skipped proof or limitation is named | Vague done invites premature completion; visible later steps can pull attention forward | synthesis; M corroborated: writing-great-skills/GLOSSARY.md:137-159 |
| **Collaboration, handoffs, and fresh-context work** | - | - | - | - | - |
| Transfer state without transferring conversational noise | File-backed handoff; handoff versus compact | Put requirements, diffs, evidence, status, and recovery pointers in owned artifacts | A fresh context can resume without redispatch or copying settled source material | Helpers can depend on fragile heading conventions; shared worktrees can collide | synthesis; S corroborated: subagent-driven-development/SKILL.md:181-265; M corroborated: handoff/SKILL.md:7-17 |
| Parallelize only semantic independence | Independent problem domain; explicit blocking edges | Prove no shared state, dependency, write surface, or ordering need; otherwise keep fresh ownership serial | Dispatch map shows disjoint obligations and an integration or review owner | Independent in SDD still means serial; the same adjective licenses parallelism elsewhere | synthesis; S direct: dispatching-parallel-agents/SKILL.md:10-46,129-175; S corroborated: subagent-driven-development/SKILL.md:367-389; M corroborated: blocking edges |
| **Skill authoring, evaluation, and pruning** | - | - | - | - | - |
| Make wording answer an observed behavior gap | Pressure testing; documentation TDD | Run a no-guidance control, capture failures and rationalizations, add the smallest guidance, and repeat under pressure | Repeated fresh-context samples improve against an explicit rubric and variance is recorded | Bounded samples do not justify bulletproof or universal-compliance claims | synthesis; S corroborated: writing-skills/SKILL.md:10-45,459-585,633-655 |
| Test behavior rather than word presence | Behavior gate | Use behavior-present and behavior-absent probes around one operational distinction | The evaluator accepts known-good behavior and rejects a lazy-plausible bad case | Selected probes do not establish the whole skill; structural checks can be proxies | synthesis; P corroborated: benchmarks/behavior.yaml:1-13 and behavior.js:1-44 |
| Remove words that do not change execution | No-op; duplication; sediment; sprawl; single source of truth | Merge repeated meanings, delete inert explanation, retain intentional leading tokens, and keep one owner | Behavioral probes or retrieval tests remain equal or improve after the cut | Raw brevity can remove a needed gate; repeated tokens are not always duplicated meaning | synthesis; M corroborated: writing-great-skills/SKILL.md:53-83 and GLOSSARY.md:161-201 |

## Tier 1: Strong Steering Anchors

Tier 1 is intentionally small. These terms are broadly transferable and create
meaningful execution or judgment pressure when paired with mechanics. Inclusion
does not canonize them locally.

| Term | Concise Meaning | Behavior Recruited | Use When | Operational Companion | Misuse Risk | Source Support |
| --- | --- | --- | --- | --- | --- | --- |
| Leading word | Compact established concept that recruits a distributed prior | Compresses a meaningful practice without re-explaining it | A known professional term accurately names the desired behavior | Name the observable action and gate after the term | Invented, decorative, or ambiguous words become no-ops | synthesis; M corroborated: writing-great-skills/GLOSSARY.md:129-135; compared with L-Steer and L-Bridge |
| Completion criterion | Observable, demanding done condition | Resists premature completion and vague confidence | A skill has a bounded outcome | Enumerate required evidence and residual limitation | A cosmetic checklist can still under-specify legwork | synthesis; M corroborated: writing-great-skills/GLOSSARY.md:137-159 |
| Evidence before claims | Success claim follows current inspectable support | Replaces memory and confidence with verification | Reporting completion, repair, review, or delegation results | Run the proving check, read all output, qualify scope | Fresh but partial evidence can still be overclaimed | synthesis; S corroborated: verification-before-completion/SKILL.md:8-48,76-106 |
| Tracer bullet | Skeletally thin real path for early feedback | Makes one real path observable so design can adjust from a proven base | Learning across real components is needed before broader implementation | Name the selected feedback and real components; attach executable or inspectable proof | Can be skeletal, non-customer-complete, and non-final; does not define task size or diff volume | synthesis; M corroborated: to-tickets/SKILL.md:25-40; V-01 S01-S03 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| Vertical slice | One request or behavior organized across its relevant concerns | Produces a usable or testable end-to-end increment | Work can land as one value or behavior slice | State the claimed boundary and local completion proof; declare blockers separately | Does not require every named layer or establish concurrency; compatibility-sensitive staged work can be a safer shape | synthesis; V-01 S04-S07 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| RED-GREEN-REFACTOR | Observed failure, smallest pass, simplification while green | Constrains implementation and proves the test can fail | Expected behavior and a red-capable seam are known | Watch the intended red, implement minimal green, retain green during refactor | M's current runtime moves refactoring to review; name the chosen loop | synthesis; S corroborated: test-driven-development/SKILL.md:31-71,113-192; M corroborated but conflicted: tdd/SKILL.md:8,34-36 |
| Tight, red-capable feedback loop | Fast exact-symptom signal that can fail and pass | Makes debugging consume evidence | The symptom or performance failure is uncertain | Run before hypothesizing; reuse for regression proof | A nearby or nondeterministic proxy can misdirect diagnosis | synthesis; M corroborated: diagnosing-bugs/SKILL.md:12-60; S direct: systematic-debugging/SKILL.md:46-213 |
| Falsifiable hypothesis | Explanation with a discriminating prediction | Replaces guess-and-check with uncertainty reduction | More than one cause remains plausible | Instrument one signal and change one variable | Vague hypotheses merely rename intuition | synthesis; M corroborated: diagnosing-bugs/SKILL.md:62-122; S direct: systematic-debugging/SKILL.md:46-213 |
| Root cause, not symptom | Repair the shared semantic cause | Prevents repeated surface patches | Multiple paths express the same failure | Trace callers and lock the repair with regression evidence | Root-cause rhetoric without a trace can justify oversized changes | synthesis; P corroborated: ponytail/SKILL.md:50-54; S corroborated: root-cause-tracing.md:32-65,130-154 |
| Deep module, interface, and seam | Substantial behavior hidden behind a small caller-facing surface | Creates leverage, locality, and stable test surfaces | A real variation or behavior cluster merits ownership | Apply deletion test and test through the interface | Shallow wrappers and speculative seams add indirection | synthesis; M corroborated: codebase-design/SKILL.md:10-28,60-67 |
| Fixed point and two-axis review | Stable comparison target plus separate right-thing and built-right judgments | Prevents moving baselines and blended verdicts | Reviewing a bounded diff, task, or branch | Pin target; keep Spec and Standards findings separate | Review scopes differ; S's task verdicts are not a universal review protocol | synthesis; M corroborated: code-review/SKILL.md:6-23,74-87; S corroborated: task-reviewer-prompt.md:78-165 |
| Active domain model | Canonical language tested against concrete scenarios and code | Preserves product meaning across artifacts | Ambiguity or a domain decision affects implementation | Update the owning glossary when authorized; reserve ADRs for consequential decisions | A glossary can be mistaken for a specification | synthesis; M corroborated: domain-modeling/SKILL.md:44-74; compared with L-Steer |
| Context pointer and progressive disclosure | Conditional, explicit route to branch-specific material | Preserves attention without hiding required rules | Reference material is needed only on a branch | Keep common path inline and test retrieval/application | Links without conditions create hidden loading variance | synthesis; M direct: writing-great-skills/SKILL.md:30-44 and GLOSSARY.md:37-41 |
| Single source of truth | One semantic owner with downstream pointers or thin transport adapters | Prevents instruction drift and stale handoffs | Behavior appears across skills, hosts, or contexts | Prove parity and fresh-context recovery | Duplicated fallbacks can falsify the single-owner claim | synthesis; M corroborated: writing-great-skills/SKILL.md:53-83; P corroborated: docs/agent-portability.md:3-38; S corroborated: file-backed handoff |

## Tier 2: Methods And Techniques

Tier 2 retains mechanics that can transfer even when the originating pack's
name should not. Applicable skill types are proposed local uses and therefore
labeled synthesis or inference in the provenance cell.

| Method Or Technique | Purpose | Essential Mechanics | Entry Condition | Evidence Gate | Failure Prevented | Applicable Skill Types | Provenance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Invocation economics and route-only routing | Allocate discovery cost between model and human without making the router an executor | Classify model-invoked versus user-invoked reach; expose one map; return the next owner or flow and stop | More than one skill exists and users or models need a stable selection surface | Fresh prompts reach the right owner; router runs leave downstream state untouched | Unreachable skills, overloaded descriptions, and routers that silently do the work | Routers, skill-pack entrypoints, invocation metadata | synthesis; M corroborated: .agents/invocation.md:1-16 and ask-matt/SKILL.md:7-13 |
| Information hierarchy with conditional loading | Put immediate action above reference while preserving required branches | Inline common path; place local reference next; disclose external or branch material through sharpened conditions | A skill contains both always-needed and conditional material | Retrieval, application, and gap probes show the correct branch loads the correct material | Context bloat, buried steps, and invisible must-have rules | Any multi-branch skill or large reference skill | synthesis; M corroborated: writing-great-skills/SKILL.md:30-44 and GLOSSARY.md:67-111 |
| Sequential decision elicitation | Resolve human-owned choices without losing dependencies | Ask one question, offer a recommendation and tradeoff, look up facts, follow the chosen branch, and require confirmation | Open decisions materially change scope or design | Shared understanding is confirmed and the decision artifact records settled terms | Autonomous invention of user intent and bulk-question overload | Grilling, brainstorming, domain modeling, planning | synthesis; M corroborated: grilling/SKILL.md:6-12; S direct: brainstorming/SKILL.md:20-72 |
| End-to-end behavior slicing with explicit blockers | Turn a plan into proof-bearing behavior slices | Shape one request or behavior across its relevant concerns, size it separately for a fresh context, and declare predecessor edges | Work can be decomposed into behavior slices | Each slice has explicit proof through its claimed boundary and no hidden predecessor; a dependency-ready set is derivable, while concurrency is proved separately | Unjustified horizontal batches that defer behavior proof, imagined integration, and false parallelism | Ticket shaping, implementation planning, TDD | synthesis; M corroborated: to-tickets/SKILL.md:25-65 and tdd/SKILL.md:28-35; V-01 S04-S11 and UBL01-C1, UBL01-C2, UBL01-C3, UBL01-C4; behavioral effect untested |
| Expand-migrate-contract compatibility change | Change an incompatible interface or schema while old and new forms coexist | Add the new form while preserving the old, migrate callers or data through releasable backward-compatible stages, remove the old form after its use ends, and record dependencies or required stops | Clients, versions, or data cannot switch atomically | Every stage remains operational or releasable and compatible; dependencies and required stops are explicit | Flag-day replacement, premature contraction, and labeling a technical migration stage as a product slice | Refactor planning, schema or API migrations | synthesis; V-01 S12-S15 and UBL01-C5; separating progressive-exposure blast-radius control and product-slice shape is inference from S16 and their distinct gates; behavioral effect untested |
| Test-first behavioral proof | Constrain code with an independently sourced behavioral failure | Write or select the public-seam test, observe the intended red, make minimal green, simplify under green | Expected behavior, exact symptom, and red-capable seam are known | Red reason is correct; green proves the behavior; refactor does not add behavior | Tests that only confirm existing behavior or mirror implementation | TDD, feature work, understood bugs | synthesis; S direct: test-driven-development/SKILL.md:47-192; M corroborated with refactor-location conflict |
| Systematic diagnostic loop | Reduce causal uncertainty before repair | Reproduce, collect evidence, compare patterns, state one falsifiable hypothesis, change one variable, trace backward, then regression-test | Symptom, cause, or reproduction is uncertain | Exact symptom is reproduced; hypothesis is discriminated; same loop and regression proof pass after repair | Guess-and-check patches and plausible storytelling | Bug diagnosis, flake investigation, performance diagnosis | synthesis; S direct: systematic-debugging/SKILL.md:46-213; M direct: diagnosing-bugs/SKILL.md:12-124 |
| Deep-module deletion and interface test | Decide whether an abstraction earns its surface | Apply deletion test, classify dependencies, require a real variation seam, hide internals, replace internal-coupled tests with interface tests | A module, adapter, or seam is proposed or under review | Deleting it would recreate meaningful behavior; callers and tests depend on the interface only | Pass-through abstraction and premature seams | Design, architecture improvement, TDD seam choice | synthesis; M corroborated: codebase-design/SKILL.md:60-67 and DEEPENING.md:1-36 |
| Ordered sufficiency search | Find the least new machinery that safely satisfies the commitment | Understand and trace; test non-existence, local reuse, standard or platform capability, installed dependency, trivial direct form, then minimum new code; stop at the first sufficient option | The requested behavior is understood and solution choice remains open | Selected owner meets compatibility, correctness, safety, accessibility, and explicit requirements; new machinery has a concrete justification | Reinvention, speculative dependency, and code-golf under-delivery | Implementation, simplification, dependency choice | inference; P corroborated: ponytail/SKILL.md:32-64. Preferred phrase is synthesis; ladder remains P's pack-specific name |
| Fixed-point dual-axis review | Judge both requested behavior and implementation quality without moving the target | Resolve baseline, read standards and spec, inspect one immutable diff, retain separate verdicts and severities | A bounded review target and comparison point exist | Every finding cites target evidence and its axis; absent spec remains explicit | Moving-memory review and one axis masking the other | Branch review, task review, release review | synthesis; M direct: code-review/SKILL.md:6-23,74-87; S corroborated: task-reviewer-prompt.md:78-165 |
| Serial fresh-context implementation with task review | Reduce context pollution while retaining one integration owner | Curate a task brief, dispatch one fresh implementer, collect evidence, issue separate compliance and quality verdicts, repair and re-review, update recovery state, then review whole branch | An approved multi-task plan has serially integrable units and review capacity | Each task closes its repair loop; ledger prevents redispatch; whole-branch review checks integration | Context accumulation, implementer self-certification, and lost recovery state | Multi-task implementation campaigns | inference; S corroborated: subagent-driven-development/SKILL.md:45-82,159-265. S explicitly does not license parallel implementers |
| Qualified parallel investigation | Convert genuine independence into concurrency | Partition by unrelated problem domain with no shared state or dependencies, give each a bounded contract, then synthesize centrally | Two or more investigations are semantically independent | Disjoint scopes and evidence packages are visible; one owner verifies integration | Parallel work on coupled tasks and ambiguous independent wording | Research, diagnosis lanes, read-only review | synthesis; S direct: dispatching-parallel-agents/SKILL.md:10-46,129-175; M corroborated: blockers and frontier |
| Skill pressure testing | Make instruction changes answer observed agent failures | Establish no-guidance baseline, capture outputs and rationalizations, classify failure, add minimal guidance, repeat fresh samples under competing pressures, record variance | A skill is intended to change discipline or judgment | Rubric-scored treatment improves over control across repeated fresh contexts; residual gap is explicit | Intuition-only wording and one-shot success claims | Skill authoring, behavior repair, pruning validation | synthesis; S corroborated: writing-skills/SKILL.md:459-585,633-655 |
| Behavior-gate and evaluator self-test | Prove the measurement discriminates before trusting results | Define behavior-present and behavior-absent probes; run known-good and lazy-plausible bad references; constrain any model judge with fixed rubric and settings | Behavior cannot be established by deterministic assertions alone | Known-good passes, bad fails, live evaluation starts only after self-test; proxy limits stay visible | Text-presence tests, broken scorers, and unearned judge trust | Skill evaluation, benchmark harnesses, authoring experiments | synthesis; P corroborated: benchmarks/behavior.js:1-44 and benchmarks/agentic/README.md:63-104 |
| Failure-shaped instruction and pruning pass | Use the least instruction form that repairs the observed failure | Distinguish discipline, shape, omission, and conditional failures; choose prohibition, positive recipe, structural slot, or observable conditional; remove no-ops and duplicated meanings | Baseline evidence identifies a wording failure or pruning candidate | Fresh controls show repair or parity; required retrieval and completion gates remain | Reflexive negation, decorative prose, sediment, and behavior-losing brevity | Skill authoring, review, pruning | inference; S corroborated: writing-skills/SKILL.md:459-480,575-585; M corroborated: writing-great-skills/SKILL.md:53-83 |
| Portable semantic core with verified adapters | Keep behavior stable across harnesses without pretending tools are identical | One canonical behavior owner; thin adapters translate lifecycle and actions; generated-copy, invariant-phrase, version, and live-action checks catch drift | A skill ships to more than one host | Parity checks and host acceptance tests pass; host-specific exceptions are documented | Duplicated runtime meaning, unavailable tools, and silent adapter drift | Cross-harness skills, plugin packaging, installation | inference; S corroborated: docs/porting-to-a-new-harness.md:33-63; P corroborated: docs/agent-portability.md:3-38 |

## Tier 3: Situational Language

These terms name useful distinctions only inside a narrower workflow, artifact,
risk level, or host contract. Their local use remains synthesis or inference,
not adoption.

| Term | Specific Context | Meaning | Required Companion | Do Not Generalize To | Provenance |
| --- | --- | --- | --- | --- | --- |
| Skill-first invocation and 1% chance | Superpowers-style compulsory routing | Invoke a possibly relevant skill before clarification or action | Explicit precedence, user-instruction override, and over-trigger evaluation | A universal threshold for every pack or harness | inference; S corroborated: using-superpowers/SKILL.md:10-31 |
| Bootstrap | Harness activation | Automatically inject or re-inject a control skill so installation is not inert | Discovery-versus-injection model plus live reachability test | Repo primer, ordinary skill metadata, or every native-discovery host | synthesis; S corroborated: docs/porting-to-a-new-harness.md:43-55,81-106; current Codex path is a documented tension |
| Unique-marker test | Startup or context-delivery mechanism | Empirical proof that one marker reached a fresh session | Behavior-level acceptance prompt | Proof that the delivered instructions changed behavior | synthesis; S corroborated: docs/porting-to-a-new-harness.md:174-205 |
| Iron Law or hard gate | High-risk, temptation-prone precondition | Bright-line stop or restart branch with named rationalizations | Qualified gate name, entry condition, observable pass condition, and justified exceptions | Generic emphasis, low-risk steps, or an unqualified word gate | inference; S corroborated: test-driven-development/SKILL.md:31-45,272-287 and verification-before-completion/SKILL.md:16-75 |
| Destination, decision ticket, fog, and frontier | Very large, uncertain efforts | Keep imprecise in-scope uncertainty as fog until it can become a precise decision question; expose resolved runnable frontier | Scoped destination, map as index, decision-not-deliverable rule, and exit to specification | A well-scoped feature, ordinary task list, or implementation from the map | inference; M corroborated: wayfinder/SKILL.md:7-126 |
| Known ceiling and debt ledger | Intentional simplification with a future limit | Record the limit, revisit condition, and upgrade action; optionally harvest owned markers | Explicit commitment and safety check; discoverable trigger; ledger ownership | General uncertainty or residual risk, which is not an intentional design limit | synthesis; P corroborated: ponytail-debt/SKILL.md:11-38 |
| One runnable check | Minimum proof floor for small non-trivial logic | One executable assertion, demo, self-check, or test fails when the logic breaks | Scope statement and escalation to broader semantic proof where risk demands | A universal completion gate or exhaustive test strategy | synthesis; P corroborated: ponytail/SKILL.md:107-112 |
| Subagent-Driven Development | Superpowers serial multi-task execution | Controller-managed fresh implementer and reviewer contexts with file handoffs and final branch review | Approved plan, serial integration, task briefs, evidence-backed status-to-action protocol, repair budget, and recovery ledger | Parallel implementation or the common software-design-document expansion of SDD | inference; S corroborated: subagent-driven-development/SKILL.md:6-17,45-82,132-265 |
| Native-tool-first isolation | Harness-owned worktree lifecycle | Detect existing isolation, prefer native tool, use Git fallback deliberately, and clean by provenance | Concrete host capabilities, baseline verification, and cleanup ownership | A claim that native tools are always present or superior | synthesis; S corroborated: using-git-worktrees/SKILL.md:8-61,121-202 |
| Best-effort and never-block | Optional lifecycle support | Optional helpers fail quietly and preserve unrelated state | Observability for lost support, safe input or path gates, and owned cleanup | Correctness-critical behavior, security enforcement, or silent core failure | inference; P corroborated: hooks/ponytail-mode-tracker.js:114-130 |
| Technical correctness over social comfort | Receiving review feedback | Treat feedback as a claim to inspect, clarify, accept, or rebut with evidence | Respectful evidence, code inspection, and explicit disagreement | Pack-voice bans on gratitude or ordinary collaboration norms | synthesis; S direct: receiving-code-review/SKILL.md:8-38,59-98,203-213 |
| Prototype as primary source | Off-main design evidence | Runnable throwaway artifact remains inspectable after its validated decision moves into production | One-question scope and explicit production exclusion | A reason to retain every experiment or merge prototype structure | synthesis; M corroborated: prototype/SKILL.md:8-26 |

## Steering Formulations

These are synthesis-writing aids, not candidate runtime instructions. Each
formula deliberately combines a leading or professional term with an
observable action and a gate. Every proposed use is labeled.

| Steering Term | Action It Should Recruit | Gate That Makes It Operational | Suitable Synthesis Context | Claim Label |
| --- | --- | --- | --- | --- |
| Leading word | Select one established term that accurately compresses the target practice, then state the required action | A no-guidance comparison and fresh treatment samples show a behavior change rather than word echo | Skill invocation, descriptions, body pruning | synthesis |
| Context pointer plus progressive disclosure | Keep common-path action inline and load branch material only under a named condition | Retrieval and application probes show the branch receives all required material | Large or multi-branch skills | synthesis |
| Shared understanding plus active domain model | Resolve one dependent decision at a time and test canonical terms with concrete scenarios | Human confirmation and scenario consistency precede action; authorized glossary change records the result | Requirements, domain work, design | synthesis |
| Tracer bullet | Build a skeletally thin path through the real components needed for selected feedback, observe it, and adjust from the proven base | The named real path produces executable or inspectable evidence for only its claimed feedback boundary | Early learning and architecture steering | synthesis; V-01 S01-S03 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| Vertical slice | Organize one request or valuable behavior across its relevant concerns | The behavior is usable or testable through its claimed boundary under the local completion policy | Ticket shaping and end-to-end delivery | synthesis; V-01 S04-S07 and UBL01-C1, UBL01-C2, UBL01-C3; behavioral effect untested |
| RED-GREEN-REFACTOR | Observe the intended failure, make the smallest passing change, then simplify without new behavior | Correct red is witnessed; green follows; refactor remains green | Red-testable implementation; explicitly qualify M's refactor-location conflict | synthesis |
| Tight, red-capable feedback loop | Reproduce the exact symptom with one fast, deterministic command before forming a repair theory | The same command is red before repair and green after it; nondeterminism uses a pinned reproduction-rate substitute | Bug and performance diagnosis | synthesis |
| Root cause, not symptom | Trace all affected callers and repair their shared semantic owner | Caller coverage and a regression check prove the shared failure is closed | Multi-path defects and duplicated validation | synthesis |
| Deep module at a real seam | Hide substantial behavior behind a small caller interface and keep internal seams private | Deletion test shows leverage; caller-facing tests prove behavior through the interface | Module, adapter, and API-shape synthesis | synthesis |
| Existing owner before new code | Search local reuse, standard or platform capability, and installed dependencies before invention | Every rejected owner has a concrete insufficiency; selected solution meets commitments and safety floors | Simplification and dependency choice | inference |
| Fixed-point two-axis review | Pin one comparison target and judge Spec and Standards separately | Every finding cites immutable evidence and one axis; missing spec stays explicit | Review-skill synthesis | synthesis |
| Evidence before claims | Run the current proving command, read all output, and state only the supported claim | Evidence is fresh, scope-matched, and accompanied by remaining uncertainty | Completion and delivery language | synthesis |
| Completion criterion plus legwork | Define a demanding observable end state and the work required inside it | Every criterion is checked before later-step pull; skipped proof is disclosed | Any bounded procedural step or terminal skill | synthesis |
| Fresh-context file handoff | Put requirements, diff, proof, status, and recovery state in owned artifacts | A fresh receiver reconstructs the task and next action without conversation memory | Delegation, compaction recovery, session handoff | synthesis |
| Qualified independence | Prove disjoint state, dependencies, write surfaces, and ordering before concurrent dispatch | The dispatch map and integration owner make independence inspectable | Parallel research, diagnosis, or review | synthesis |
| Pressure-tested skill wording | Capture no-guidance failure and rationalization, add the smallest targeted guidance, then repeat under pressure | Repeated fresh samples improve against a rubric and variance or residual failure is reported | Skill authoring and behavior repair | synthesis |
| Instrument first | Make known-good behavior pass and a lazy-plausible bad case fail before live evaluation | Evaluator self-test passes under fixed rubric and disclosed judge settings | Evaluation-harness synthesis | synthesis |
| No-op pruning | Remove duplicated or inert wording while retaining the action, owner, and gate | Behavior and retrieval probes remain equal or improve after the cut | Skill cleanup and compression | synthesis |

## Aliases And Collisions

Every usage recommendation in this table is synthesis. M, S, and P identify the
source packets that expose the alias or collision.

| Preferred Semantic Owner | Aliases | Collision Or Difference | Usage Guidance |
| --- | --- | --- | --- |
| Route-only router (M) | Router skill, ask-matt, flow map | S skill-first invocation loads a method; it is not a router, and M's router cannot execute another user-invoked skill | Use router for selection and stop; use invocation for loading the chosen owner |
| Context pointer (M) | Disclosed-file pointer, branch pointer | S file-backed handoff moves state across owners or contexts; P thin adapter transports behavior across hosts | Use pointer for conditional loading, handoff for transfer, adapter for portability |
| Tracer bullet (V-01; M usage) | Thin real path, skeletal end-to-end feedback | A vertical slice can overlap but organizes delivery around a behavior; S bite-sized task governs dispatch size and P shortest working diff governs solution volume | Use for learning and steering; name delivery shape, work-unit size, and diff volume separately |
| Vertical slice (V-01; M usage) | End-to-end behavior slice, one slice at a time | A tracer bullet can be skeletal and learning-oriented; S bite-sized task governs dispatch size and P shortest working diff governs solution volume | Use for delivery shape; name learning purpose, work-unit size, and diff volume separately |
| Qualified gate | Iron Law, hard gate, Gate Function, Red Flags - STOP | S gate also means design approval, proof, task review, and output-shape check | Always qualify gate by subject, entry condition, pass evidence, and exception policy |
| Interface and seam (M) | API, boundary, adapter | M explicitly rejects boundary as a synonym for its module-interface location; adapter is a role, implementation is substance | Preserve the qualifier; do not silently replace seam with boundary |
| RED-GREEN-REFACTOR (S) | Red-green, documentation TDD | M's runtime ends implementation at green and moves refactoring to review while metadata and docs still use the three-part phrase | State whether the loop targets code or agent behavior and where refactoring occurs |
| Fixed point | Review baseline, immutable target | S fresh evidence concerns timing of proof; P honesty boundary qualifies a measurement baseline and counterfactual | Do not use fresh, fixed, and fair baseline as synonyms |
| Spec, plan, task, and decision ticket | Agent brief, bite-sized task, issue, ticket | S spec is approved design, plan is durable implementation artifact, task is dispatch unit; M decision ticket answers a question and is not a build slice | Define artifact scope and owner before using the generic noun |
| Independent problem domain (S) | Independent task, isolated context, locally defined dependency-ready work | S SDD calls tasks independent but executes them serially; parallel-dispatch independence licenses concurrency | State independence dimensions and scheduling consequence explicitly |
| Completion criterion (M) | Done condition, evidence floor, one runnable check | P one runnable check is a minimum for small logic; S fresh evidence gates a claim; none alone guarantees semantic completeness | Pair the criterion with proportionate proof and claim scope |
| Known ceiling (P) | Upgrade path, trigger to revisit, Skipped / Add when | Upgrade action and revisit condition are different; a deliberate limit is not generic uncertainty or residual risk | Record limit, condition, and action separately; keep uncertainty under its own owner |
| Platform-native capability (P) | Native, stdlib, installed dependency | S native-tool-first means harness-owned tooling, not a code-level platform primitive | Qualify native by platform, harness, compatibility, and ownership |

## Failure Modes And Weak Language

The replacements below are proposed synthesis, not adopted runtime wording.

| Weak Or Risky Language | Why It Fails | Stronger Replacement | Required Qualification |
| --- | --- | --- | --- |
| Do your best; be careful; high quality | Generic encouragement supplies no action or stop condition | Named professional term plus observable action plus evidence gate | Choose a term that actually changes judgment for this context |
| Simple, minimal, shortest, or do less | Optimizes volume without locating the right owner or protecting commitments | First sufficient owner; shortest working diff after comprehension and correctness | Preserve explicit behavior, trust boundaries, data loss, security, accessibility, and proof |
| Iron Law, hard gate, or no exceptions without a subject | Categorical rhetoric hides what is gated and contradicts source exceptions | Qualified design gate, red-test gate, or claim gate | State entry condition, pass evidence, restart behavior, and legitimate exceptions |
| The skill is installed | Installation does not prove discovery, injection, or behavior | Fresh-context reachability test plus behavior acceptance prompt | Distinguish marker delivery from behavior change |
| Write tests | Does not require a meaningful seam, observed failure, or claim scope | RED-GREEN-REFACTOR at a pre-agreed public seam | Use only when expected behavior and a trusted red-capable test are known |
| Looks good; should pass; done | Confidence and intention are not evidence | Evidence before claims plus completion criterion | Run current proof, read full output, and qualify residual uncertainty |
| One runnable check proves completion | P defines it as a minimum floor, not exhaustive proof | Proportionate semantic proof through the caller-facing seam | Name the check's scope and add gates for risk, safety, and completeness |
| Fix the root cause | Without a reproducer or caller trace it can rationalize an oversized change | Tight red-capable loop plus falsifiable caller-trace hypothesis | Establish exact symptom, affected paths, and regression seam |
| Independent | The word has opposite scheduling consequences inside S | Disjoint problem domain with explicit state, dependency, write, and ordering analysis | State whether independence permits parallelism or only fresh serial ownership |
| Review the code | Target, baseline, axes, and terminal state are missing | Fixed-point Spec and Standards review | Name immutable target, requested behavior source, standards source, and finding contract |
| Make it native | Native can mean language library, platform feature, or harness tool | Platform-native capability or harness-native tool | Verify availability, compatibility, capability, and ownership |
| Fresh | Recency, isolation, and startup loading are conflated | Fresh evidence, fresh context, or fresh session | Anchor freshness to a specific event or baseline |
| Bulletproof or 100% compliant | Bounded historical samples cannot establish universal behavior | Passed named scenarios with sample count, rubric, variance, and residual gap | Keep external eval absence and model/task bounds visible |
| Delete, YAGNI, or boring over clever | Simplicity pressure can erase required behavior or design leverage | Ordered sufficiency search plus commitment and safety floors | Deep modules, tests, and necessary adapters are not bloat by default |
| Prohibit the failure | Negation may not teach the desired output shape and can worsen it | Match instruction form to observed failure | Use a fresh no-guidance control to classify discipline, shape, omission, or conditional failure |

## Cross-Pack Agreements And Disagreements

The following comparisons are synthesis. Agreement means shared language or
mechanics in the inspected packs, not proof that the practice is professionally
correct.

### Agreements

| Shared Pressure | Matt Pocock | Superpowers | Ponytail | Context And Limit |
| --- | --- | --- | --- | --- |
| Observable evidence should control action and completion | Completion criteria, tight red-capable loops, fixed-point review (M corroborated) | Observed RED, root-cause evidence, and fresh verification before claims (S corroborated) | Runnable-check floor, behavior gates, and evaluator self-tests (P corroborated) | Strong three-pack usage agreement; proof scopes differ and no packet establishes universal sufficiency |
| Smallness must remain connected to something complete | Tracer-bullet vertical slice and deep module (M corroborated) | Bite-sized task and minimal GREEN (S corroborated) | First sufficient rung and shortest working diff after correctness (P corroborated) | The object differs: delivery path, dispatch unit, implementation step, module surface, or solution volume |
| Diagnose causes rather than patch symptoms | Exact-symptom loop, minimisation, falsifiable hypotheses (M corroborated) | Systematic debugging and backward root-cause tracing (S corroborated) | Trace every caller and fix the shared function once (P corroborated) | P supplies a placement heuristic; M and S supply the fuller uncertainty-reduction sequence |
| Explicit information ownership reduces drift | Information hierarchy, context pointer, single source, and handoff (M corroborated) | File-backed briefs, reports, review packages, and recovery ledger (S corroborated) | Canonical core, thin adapters, parity gates, and owned cleanup (P corroborated) | These address conditional loading, cross-context transfer, and cross-host transport respectively; they are not aliases |
| Right thing and built right should not collapse into one confident verdict | Fixed point with separate Spec and Standards (M corroborated) | Task review with separate Spec Compliance and Task quality (S corroborated) | Correct, safe, and complete gates prevent low-volume under-delivery (P corroborated) | P's gates are benchmark-scoped rather than the same review axes; the shared pressure is separation of judgments |
| Existing evidence should constrain invention | Inspect code and semantic owners before diagnosis, design, or domain change (M corroborated) | Process skill, approved spec, and current proof precede implementation claims (S corroborated) | Understand and trace before running the ladder; search existing owners before new code (P corroborated) | S uniquely requires skill invocation before code inspection; sequence and ceremony are not agreed |
| Skills should be evaluated by recruited behavior, not attractive prose | Leading words and no-op pruning define the authoring target, but M has no behavioral tests (M corroborated with gap) | No-guidance controls, pressure scenarios, rationalizations, repeated micro-tests (S corroborated) | Behavior-present and behavior-absent gates plus instrument-first scorer checks (P corroborated) | Only S and P provide evaluation mechanics; no combined method has been tested in this pack |
| Human judgment and agent legwork should be separated | Facts are researched; dependent decisions remain with the human during grilling (M corroborated) | Brainstorming obtains user approval before implementation (S corroborated) | Skipped / Add when favors a safe sufficient delivery without stalling (P corroborated) | P supplies a different response-boundary technique, not consensus on mandatory approval |

### Disagreements And Contextual Conflicts

| Issue | Source Positions | Distillation Result |
| --- | --- | --- |
| Invocation aggressiveness | S requires invocation at a 1% chance before clarification or inspection; M models user and model invocation as a context-versus-recall cost and uses a route-only map; P exposes persistent or one-shot modes | No universal threshold. Preserve reach, route, and duration as separate decisions and require local invocation evaluation |
| Refactoring inside TDD | S defines RED-GREEN-REFACTOR with cleanup while green; M's TDD runtime stops the implementation loop at green and moves refactoring to review while its metadata still says red-green-refactor | Genuine current conflict. Any synthesis must state where refactoring occurs rather than borrowing the phrase alone |
| Mandatory design ceremony | S's brainstorming gate applies even when work appears simple; P calls its ladder a reflex, not a research project; M routes well-scoped and foggy work to different methods | Do not manufacture one process. Gate proportionality and routing need downstream design evidence |
| Meaning of independent | S SDD uses fresh independent task owners but serial execution; S parallel dispatch uses independent problem domains to license concurrency; M frontier means open, unblocked, and unclaimed work | Independence must name state, dependency, write, context, and scheduling dimensions |
| Skill description content | S runtime says description is triggering conditions rather than workflow; its bundled reference says what and when; M treats description as invocation surface and possible context pointer | Internal S conflict plus cross-pack variation. Do not adopt a when-only formula without harness-specific tests |
| Simplest solution versus designed leverage | P prefers the first sufficient existing owner and shortest correct diff; M may introduce a deep module or seam when it creates leverage and locality | Contextual tension, not contradiction. Reuse and deletion precede invention, but a real deep owner can be the simpler semantic design |
| Hard gates and exceptions | S uses no-exceptions rhetoric while its own packet records exceptions and overloaded gate meanings; P explicitly preserves safety and requirement floors under reduction; M uses completion criteria without one global Iron Law dialect | Retain only qualified gates with subject, evidence, and exception policy |
| Minimum proof | P's one runnable check is a floor; S fresh evidence gates only the claim it supports; M's interface tests and fixed-point review can demand broader semantic proof | Never promote the minimum check into a universal completion criterion |
| Native | P means standard library or platform capability in solution selection; S native-tool-first means the harness-owned isolation mechanism | Same word, different owner. Always qualify platform-native versus harness-native |
| Prototype disposition | M calls the code throwaway but retains the runnable artifact off-main as a primary source; P's general reduction pressure favors deletion and less machinery | Preserve the evidence-versus-production distinction; no general rule to retain or delete every prototype follows |
| Completion rhetoric | S demands immediate current proof; M separates criterion, legwork, and later-step pull; P uses terse terminals such as Lean already. Ship. but lacks an estimation method for reduction totals | Prefer explicit criterion and scoped proof; terse terminals do not establish completion |

## Synthesis Application Index

Every row below is synthesis. It is an intake index for an author editing one
docs/synthesis/skills/<skill>.md document, not an instruction to include every
listed concept.

| Synthesis Need | Concepts To Consider | Techniques To Consider | Evidence Needed Before Adoption |
| --- | --- | --- | --- |
| Invocation and routing | synthesis: invocation reach, route-only router, method precedence, runtime duration | Trigger evaluation, fresh-context reachability, router no-op check | Prompts that should and should not invoke; harness delivery proof; evidence that the router stops |
| Context and loading | synthesis: leading word, context pointer, progressive disclosure, single semantic owner | Information hierarchy, retrieval/application/gap probes, file-backed recovery, adapter parity | Fresh contexts load required branches; removed or deferred text does not reduce behavior; duplicates are detected |
| Intent and requirements | synthesis: shared understanding, active domain model, qualified approval gate | One-question decision walk, fact lookup, scenario testing, durable brief | Open decisions are real and human-owned; terms survive examples; acceptance and exclusions are observable |
| Planning and dependencies | synthesis: tracer bullet, vertical slice, bite-sized unit, predecessor edge, dependency-ready set, locally defined frontier, expand-migrate-contract compatibility change, progressive-exposure blast-radius control | Thin real feedback paths, end-to-end behavior slicing, explicit dependency graphs, compatibility staging, and separate exposure control | Purpose-scoped path or slice proof is explicit; blockers are factual; readiness is separate from concurrency safety; migration stages remain releasable and backward-compatible; blast radius is assessed separately; behavioral effect remains untested |
| Implementation and TDD | synthesis: RED-GREEN-REFACTOR, public seam, minimum new machinery | Observed red, minimal green, green refactor, ordered sufficiency search | Expected behavior and red-capable test are known; correctness and safety floors hold; M/S refactor conflict is resolved |
| Debugging | synthesis: tight red-capable loop, falsifiable hypothesis, root cause, caller trace | Exact reproduction, minimisation, one-variable probe, backward trace, regression test | Symptom is exact; hypothesis discriminates; affected callers and correct proof seam are established |
| Design and simplification | synthesis: deep module, interface, seam, existing owner, known ceiling | Deletion test, interface test, reuse/native search, bounded deferral, question-driven prototype | Abstraction has leverage; dependency insufficiency is concrete; shortcut trigger is observable; prototype yields a verdict |
| Review and completion | synthesis: fixed point, Spec and Standards, completion criterion, evidence before claims | Immutable snapshot, dual-axis review, current claim gate, separate correct/safe/complete checks | Every finding and claim cites scope-matched evidence; missing spec and residual uncertainty stay visible |
| Collaboration and handoff | synthesis: fresh context, file-backed handoff, qualified independence, ownership-aware isolation | Task brief, status-to-action protocol, recovery ledger, disjoint dispatch, owned cleanup | Receiver recovers state; independence dimensions are proved; integration and cleanup owners are explicit |
| Skill authoring and pruning | synthesis: leading word, no-op, failure shape, behavior gate, evaluator trust | No-guidance control, pressure tests, repeated fresh samples, known-good/bad scorer test, behavior-preserving prune | Rubric, sample count, variance, retrieval, and residual gap are recorded; wording changes behavior rather than recall |

## Prune Log

| Removed, Merged, Or Bounded Material | Disposition And Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |
| Lazy, simplest, minimal, shortest path, do less | Merged as aliases; volume language alone is unsafe | Ordered sufficiency search with commitment and safety floors | One phrase demonstrates distinct behavior in a controlled local test |
| Ladder and first rung that holds | Mechanics retained in Tier 2; pack-specific name not promoted broadly | Ordered sufficiency search | A synthesis needs Ponytail-compatible vocabulary or the metaphor outperforms the neutral formulation |
| 1% chance | Bounded to Tier 3; frequency does not justify a universal invocation threshold | Tested triggering conditions and method precedence | Local precision and recall evidence supports that threshold |
| Iron Law, HARD-GATE, Gate Function, Red Flags - STOP, no exceptions | Collapsed into qualified gate; rhetoric and meanings are overloaded | Subject-specific gate with observable pass condition | A pressure test shows categorical wording is necessary for one failure |
| Wayfinder destination, fog, graduate, frontier, decision ticket | Kept in Tier 3 only; coherent but designed for very large foggy work | Precise question, blocker edge, and uncertainty-aware planning mechanics | The target synthesis owns that scale and validates the metaphor |
| SDD acronym and exact role/status strings | Mechanics retained; acronym collides and statuses are protocol-local | Serial fresh-context implementation, two-axis task review, evidence-backed status-to-action map | Interoperability with Superpowers is an explicit goal |
| Bulletproof and 100% compliance | Rejected as unsupported universal outcome language | Named scenarios, rubric, sample count, variance, residual gap | Replicated external evidence supports the claimed population |
| Skill Discovery Optimization acronym | Merged into reachability and triggering-condition mechanics; the source conflicts on description content | Tested invocation metadata and full-body loading | The acronym itself improves shared understanding without hiding the conflict |
| Visual companion, screens, tombstones, and event vocabulary | Feature name and protocol pruned as too source-specific for this cross-packet reference | None | A visual-elicitation synthesis needs the exact Superpowers protocol |
| Ponytail brand, ponytail marker syntax, and command names | Brand and syntax pruned; semantic distinction retained | Known ceiling, revisit trigger, upgrade action, owned ledger | Compatibility with Ponytail source markers is required |
| Lite, full, and ultra | Rejected as private intensity labels with source inconsistencies | Explicit reduction behavior and floors | A local mode system needs tested intensity semantics |
| Persistent, live, default, active, off, one-shot command behavior | No general taxonomy admitted because hosts disagree | Host-scoped reach, duration, mutation, and deactivation contract | A specific host lifecycle is being synthesized |
| Lean already. Ship. and net line or dependency estimates | Decorative terminal and false-precision risk; no estimation method | Evidence-backed no-finding result and scoped completion criterion | A repeatable estimator and bounded complexity-only report are defined |
| Generic TDD, DRY, YAGNI, error handling, type safety, coverage, scalability | Generic names do not survive without distinctive mechanics | RED-GREEN-REFACTOR, safety floors, completion and proof gates | The synthesis question narrows to one practice's meaning |
| Generic verbs: read, write, ask, run, check, fix, commit | Rejected; they do not compress judgment | Named technique plus observable action and gate | A verb participates in a defined state transition |
| Teaching and in-progress workflow language: mission, storage or fluency strength, explore or exploit, fragments, beats, grounding, push right, grill the send | Off-question, draft, or isolated Matt vocabulary with weak transfer to coding-skill engineering | General decision, context, and checkpoint mechanics already retained | The synthesis targets teaching, writing, or the owning workflow is promoted |
| Exact harness APIs, tool names, host commands, manifest fields, and protocol primitives | Source-specific implementation detail | Tool mapping, thin adapters, live acceptance, owned cleanup | A harness-integration synthesis needs the exact interface |
| Historical command/skill taxonomy, decision map, Negative Space, old reviewer split, old worktree paths | Superseded, changelog-only, or dormant | Current packet semantic owners | Historical evolution becomes the question |
| Raw benchmark percentages, model names, LOC medians, and speed or cost claims | Revision-sensitive results and unsupported transfer | Honesty boundary, named scorer, baseline, and limitations | A separate evidence review verifies generalization |
| Frequency-only terms and repeated slogans | Frequency is discovery evidence, not admission | Semantic owner that changes action or judgment | The term gains a defined contrast, action, or completion gate |
| Agent-ready, ready-for-agent, Codex-ready brief | Workflow labels merged; readiness is not self-proving | Durable bounded brief with acceptance, blockers, and proof | A local lifecycle owner defines and validates the state |

## Evidence Gaps

- The three upstream packets establish what their supplied revisions instruct,
  name, test, or report. Repetition alone cannot establish professional
  correctness. V-01 supplies bounded semantic and professional evidence only
  for UBL01-C1 through UBL01-C5.
- External semantic validation was completed only for tracer bullets, vertical
  slices, dependency readiness, and expand-migrate-contract within V-01's
  stated scope. No external-origin study verified the intellectual history or
  other attributed engineering traditions such as TDD, deep modules, DDD,
  debugging practices, or YAGNI.
- Full current-edition tracer-bullet text was inaccessible beyond a licensed
  preview; exact later-edition drift remains unknown.
- No inspected source establishes frontier as general professional planning
  vocabulary. General rows use dependency-ready set; the Wayfinder-scoped
  metaphor remains local.
- No source directly compares expand-contract phases with vertical product
  slices. Their separation remains `inference` from distinct goals and gates.
- Live official documentation underlying V-01 can change after 2026-07-22.
- No controlled comparison shows which retained term, formulation, or
  combination changes behavior in this skill pack. Every proposed local use
  still needs skill-specific controls and acceptance criteria.
- No packet proves that one universal sequence, invocation threshold, gate
  density, evidence burden, or completion formula fits every skill.
- None of the three upstream checkouts was network-refreshed for this pass.
  Their exact local revisions are known; live-remote equality is not.
- M contains no behavioral tests and includes status-qualified draft,
  miscellaneous, personal, and deprecated vocabulary. Its package manifests
  also disagree on version, and its runtime and metadata disagree on
  red-green-refactor.
- S's external eval repository was unavailable. Several tests establish
  description recall or negative shape rather than full workflow behavior.
  Its authoring references conflict, and harness documentation has current
  integration drift.
- P's strongest behavioral evidence is bounded by task set, model, scorer,
  sample size, nondeterminism, proxy checks, and historical contamination.
  Host adapters disagree on persistence, review, commands, and absent state.
- Cross-pack agreement on evidence, smallness, or root-cause language does not
  establish the appropriate proof scope, solution size, or diagnostic depth for
  a particular local skill.
- The source packets do not establish whether a pack-specific metaphor such as
  fog, ladder, Iron Law, SDD, or lazy senior developer recruits better behavior
  than the neutral or professional formulation retained here.
- No combined evaluation tests the proposed three-part bridge of steering term,
  observable action, and evidence gate. The formulations remain synthesis aids.
- The two local language documents remain comparison owners only. This bounded
  application updates no local comparison owner, canonical ownership decision,
  or downstream synthesis conflict.
- Applicability to any individual docs/synthesis/skills/<skill>.md remains
  unknown until that skill's invocation, ownership, risk, artifact, and
  completion contract are inspected.

## Final Decision

source-packet-complete
