# What Distinctive, Operationally Meaningful Language Does the Matt Pocock Skill Pack Use?

Status: answered

Supports: later vocabulary synthesis without selecting canonical local language

Scope: the complete checked-out Matt Pocock Skills pack, including promoted,
in-progress, miscellaneous, personal, and deprecated skills; descriptions and
Codex metadata; disclosed references; routing and relationship docs; templates;
embedded examples; human-facing docs; release metadata; and scripts whose names,
interfaces, output, or comments define vocabulary

Freshness: checkout state verified 2026-07-22; no fetch, update, or checkout
mutation performed

## Question And Boundary

**Question:** What distinctive, operationally meaningful language and vocabulary
does the Matt Pocock skill pack use?

**Intended use:** provide a provenance-backed research packet for later
synthesis. This packet does not adopt terminology, select canonical local
vocabulary, draft skill wording, or edit any runtime skill or vocabulary owner.

The upstream vocabulary was extracted before the local comparison. Upstream
claims describe what this pack says and does, not whether its advice is correct
or universally applicable. Local comparisons are explicitly labeled
`synthesis` or `inference`.

Excluded from admission were generic prose, dependency names, framework syntax,
incidental filenames, unexplained acronyms, and terms supported only by
frequency. No raw corpus, term list, concordance, frequency report, or copied
source material is persisted with this packet.

## Source Identity

| Pack | Origin | Revision | Worktree State | Verified | Authority | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Matt Pocock Skills | `https://github.com/mattpocock/skills.git` | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` (`main`; commit date 2026-07-21) | Clean: `git status --porcelain=v1` empty; tracked diff clean; local `origin/main` resolves to the same commit | 2026-07-22 | Canonical upstream checkout is primary evidence for its own language and instructions | No fetch was performed, so “current” means the supplied checkout and its local remote-tracking ref, not a freshly queried remote. Source text proves instruction content, not behavioral effectiveness. |

Revision identity is commit-first because release metadata disagrees inside the
same checkout: `package.json` says `1.1.0`, the Claude plugin manifest says
`1.2.0`, and the lockfile root says `0.0.0`. Those fields do not supersede the
resolved Git commit.

All upstream locators below are relative to the checkout root at the pinned
commit. Line ranges refer to that revision.

## Coverage

The tracked tree contained 167 files. Every file was accounted for.

| Surface | Inspected / Skipped / Not Applicable | Files Or Count | Consequence |
| --- | --- | --- | --- |
| `SKILL.md` bodies | Inspected | 41: 17 engineering, 5 productivity, 9 in-progress, 4 misc, 2 personal, 4 deprecated | Complete runtime and draft vocabulary coverage; status buckets remain visible. |
| Codex metadata | Inspected | 41 `agents/openai.yaml` files | Confirmed display language and implicit-invocation policy. |
| Disclosed references, templates, and skill-local scripts/config | Inspected | 25 | Covered glossaries, design references, tracker/domain seeds, report formats, prototype branches, teaching formats, triage artifacts, shell templates, and boundary config. |
| Bucket relationship docs | Inspected | 6 bucket `README.md` files | Confirmed promoted, in-progress, miscellaneous, personal, and deprecated status. |
| Human-facing promoted docs | Inspected | 22 files under `docs/engineering/` and `docs/productivity/` | Corroborated leading ideas, routing roles, observable signals, and handoffs. |
| Repository instructions and relationship docs | Inspected | 10: 4 under `.agents/` plus `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, top-level `README.md`, `CHANGELOG.md`, and `LICENSE` | Confirmed invocation taxonomy, docs topology, pack glossary, routing ownership, and historical rename intent. License added no vocabulary. |
| Change, plugin, package, and release metadata | Inspected | 16: 11 changeset files, 2 plugin manifests, 2 package manifests, 1 workflow | Confirmed versioned naming and rationale. Generated dependency records below the lockfile root stanza were skipped as dependency noise. |
| Other repository surfaces | Inspected | 6: 3 `.out-of-scope/` decisions, 2 root scripts, `.gitignore` | Added rejection language and install/link semantics; `.gitignore` added no vocabulary. |
| Dedicated examples directory | Not applicable | 0 | Examples embedded in skills and references were inspected. |
| Dedicated tests | Not applicable | 0 | The checkout contains no pack tests; behavioral effectiveness cannot be inferred from source inspection. |

No vocabulary-bearing surface was inaccessible. Scripts were retained as
evidence only where their interface, output, or comments named concepts such as
HITL loops, wizard stages, dangerous-command guardrails, entry-point boundaries,
or linked skill installation.

## Vocabulary Clusters

### 1. Invocation, Routing, And Context Economics

The pack treats invocation as a two-sided cost model. A **model-invoked** skill
pays **context load** so the agent can discover it; a **user-invoked** skill pays
**cognitive load** because the human must remember it. A **router skill** reduces
the latter without doing downstream work. Routing is described as a **flow**:
one **main flow**, situational **on-ramps**, **standalone** skills, and vocabulary
layers “underneath.” (`skills/productivity/writing-great-skills/GLOSSARY.md:15-65`;
`skills/engineering/ask-matt/SKILL.md:7-76`)

### 2. Skill Steering, Information Placement, And Pruning

The authoring vocabulary is organized around **predictability** of process. It
uses **leading words** to recruit model priors; an **information hierarchy** and
**progressive disclosure** to place steps and reference; **context pointers** to
control loading; and **completion criteria**, **legwork**, and
**post-completion steps** to explain thoroughness and rushing. Its failure-mode
lexicon is unusually explicit: **premature completion**, **duplication**,
**sediment**, **sprawl**, **no-op**, and **negation**.
(`skills/productivity/writing-great-skills/SKILL.md:7-83`;
`skills/productivity/writing-great-skills/GLOSSARY.md:67-201`)

### 3. Deep-Module Design And Test Surfaces

The code-design glossary deliberately standardizes **module**, **interface**,
**implementation**, **depth**, **seam**, **adapter**, **leverage**, and
**locality**, while rejecting substitutes such as “component,” “service,”
“API,” and “boundary.” Depth is leverage at the interface; locality is the
concentration of change and verification. (`skills/engineering/codebase-design/SKILL.md:10-28`)

### 4. Discovery, Delivery, Review, And Diagnosis

Planning uses **tracer-bullet vertical slices**, explicit **blocking edges**, and
a runnable **frontier**. A **wide refactor** is the named exception, decomposed
by **blast radius** through **expand-contract**. Review pins a **fixed point**
and keeps **Standards** and **Spec** as two unmerged axes. Diagnosis refuses to
hypothesize until it has a **tight**, **red-capable** loop for the exact symptom,
then reproduces, minimises, hypothesizes, instruments, fixes, and regression
tests. (`skills/engineering/to-tickets/SKILL.md:25-65`;
`skills/engineering/code-review/SKILL.md:6-23,78-87`;
`skills/engineering/diagnosing-bugs/SKILL.md:12-124`)

### 5. Human Judgment, Domain Language, And Durable Briefs

**Grilling** is a relentless, one-question-at-a-time walk down a **decision
tree** to **shared understanding**. Facts are looked up; decisions remain with
the human. **Domain modeling** is the active act of sharpening canonical terms,
testing concrete scenarios, updating the glossary inline, and offering an ADR
only for a hard-to-reverse, surprising, real trade-off. Triage packages settled
work into an **agent brief** that favors durability, behavior, acceptance, and
explicit scope over file-path precision. (`skills/productivity/grilling/SKILL.md:6-12`;
`skills/engineering/domain-modeling/SKILL.md:44-74`;
`skills/engineering/triage/AGENT-BRIEF.md:1-49`)

### 6. Wayfinding Under Uncertainty

Wayfinder supplies the densest pack-specific frame. A **destination** fixes
scope; a shared **map** is an **index, not a store**; **decision tickets** resolve
questions rather than deliver build slices; **fog of war** holds in-scope work
that cannot yet be phrased precisely; resolving tickets **graduates** fog onto
the **frontier**. **HITL** and **AFK** classify who must participate. The frame’s
core constraint is “decisions, not deliverables.”
(`skills/engineering/wayfinder/SKILL.md:7-126`)

### 7. Prototypes, Learning, And Draft Experiments

A prototype is **throwaway code that answers a question**, yet the runnable
prototype is preserved off-main as a **primary source** after its validated
decision is absorbed. Teaching distinguishes **fluency strength** from
**storage strength**, ties lessons to a **mission** and **zone of proximal
development**, and separates **knowledge**, **skills**, and **wisdom**. The
in-progress writing family distinguishes **explore** from **exploit**, mines
**fragments**, advances through **beats**, and requires concepts to be
**grounded** before later prose can lean on them. These last writing terms are
explicitly draft status, not promoted pack language.
(`skills/engineering/prototype/SKILL.md:8-26`;
`skills/productivity/teach/SKILL.md:24-118`;
`skills/in-progress/writing-fragments/SKILL.md:7-40`;
`skills/in-progress/writing-beats/SKILL.md:7-54`)

## Retained Vocabulary

“Spread” counts distinct skills or supporting surfaces, not raw occurrences.

| Term | Variants | Class | Meaning In This Pack | Behavior Or Distinction Recruited | Spread | Claim Label | Best Provenance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Predictability | predictable process | evidence-completion; pack-specific | Same process across runs, not identical output; the root skill-authoring virtue | Judge every authoring lever by process variance | Authoring skill + glossary + docs | corroborated | `skills/productivity/writing-great-skills/SKILL.md:7`; `skills/productivity/writing-great-skills/GLOSSARY.md:9-13` | A design goal asserted by the pack, not behaviorally tested here |
| Model-invoked / user-invoked | implicit / explicit reach | invocation-routing | Whether the agent may discover a skill or only a human may invoke it | Determines metadata, description style, reachability, and load trade-off | Pack-wide metadata, READMEs, invocation doc, glossary | corroborated | `.agents/invocation.md:1-16`; `skills/productivity/writing-great-skills/GLOSSARY.md:19-29` | Harness mechanics differ; pack requires Claude and Codex metadata parity |
| Context load / cognitive load | agent load / human-index cost | invocation-routing; failure-exclusion | The paired costs of model discovery and human recall | Makes skill granularity an explicit cost allocation | Authoring glossary + docs + router rationale | corroborated | `skills/productivity/writing-great-skills/GLOSSARY.md:43-53`; `.agents/writing-docs.md:3-6` | “Cognitive load” is deliberately not treated as always bad |
| Router skill | router; ask-matt | invocation-routing; relationship-handoff | A user-invoked map that names the next skill or flow and performs none of it | Reduces human recall load while preserving explicit choice | Authoring glossary + ask-matt skill/docs | corroborated | `skills/productivity/writing-great-skills/GLOSSARY.md:55-59`; `skills/engineering/ask-matt/SKILL.md:7-13` | It can point to but cannot fire another user-invoked skill |
| Flow topology | main flow; on-ramp; standalone; vocabulary underneath | invocation-routing; relationship-handoff | A positional map of how skills compose | Routes situations to sequences without treating every skill as a chain step | ask-matt skill/docs + promoted docs | corroborated | `skills/engineering/ask-matt/SKILL.md:11-76` | Pack-specific topology; not a general workflow taxonomy |
| Context pointer | description; disclosed-file pointer | invocation-routing; artifact-state | In-context wording that names and conditions access to out-of-context material | Makes wording, not merely link existence, responsible for reliable loading | Authoring glossary + setup/skill docs | corroborated | `skills/productivity/writing-great-skills/GLOSSARY.md:31-41` | Target existence does not prove the pointer fires reliably |
| Information hierarchy | steps; in-skill reference; disclosed/external reference | workflow-control; artifact-state | A ladder ordered by how immediately the agent needs material | Places action above conditional reference and keeps the top legible | Authoring skill + glossary | corroborated | `skills/productivity/writing-great-skills/SKILL.md:30-44`; `skills/productivity/writing-great-skills/GLOSSARY.md:67-111` | Flat reference can be valid; not every skill needs steps |
| Progressive disclosure | disclose; branch pointer | workflow-control; artifact-state | Move branch-specific reference behind a context pointer | Keeps common-path instructions visible while deferring conditional detail | Authoring skill + many disclosed references | corroborated | `skills/productivity/writing-great-skills/SKILL.md:42-44` | Must-have material returns inline if a sharpened pointer still misses |
| Leading word | Leitwort; leading idea | candidate-leading-word; pack-specific | A compact pretrained concept that accumulates a distributed definition | Anchors execution and invocation with fewer tokens | Authoring glossary + docs conventions + many skills | corroborated | `skills/productivity/writing-great-skills/GLOSSARY.md:129-135`; `.agents/writing-docs.md:46-50` | A coined word recruits fewer priors and must earn definition cost |
| Completion criterion / legwork / post-completion steps | done condition; demand; later-step pull | evidence-completion; workflow-control | The done bar, the work demanded within it, and the visible steps that can pull attention forward | Explains thoroughness and premature stopping as distinct control problems | Authoring glossary + step-based skills | corroborated | `skills/productivity/writing-great-skills/GLOSSARY.md:137-159` | Premature completion requires steps; thin legwork can occur without them |
| Pruning lexicon | single source of truth; relevance; duplication; sediment; sprawl; no-op; negation | failure-exclusion; pack-specific | Named diagnoses for drift, repetition, excess length, inert instructions, and counterproductive prohibition | Gives each editing failure a distinct test and remedy | Authoring skill + glossary + changelog | corroborated | `skills/productivity/writing-great-skills/SKILL.md:53-83`; `skills/productivity/writing-great-skills/GLOSSARY.md:161-201` | Repeated tokens can be intentional leading words; repeated meanings are duplication |
| Deep-module vocabulary | module; interface; implementation; depth; deep/shallow; seam; adapter; leverage; locality | domain-design | One shared language for hiding substantial behavior behind a small caller surface | Standardizes module-shape decisions and forbids blurrier synonyms | codebase-design + TDD + architecture + spec docs | corroborated | `skills/engineering/codebase-design/SKILL.md:10-28,97-109` | Pack definitions narrow or broaden familiar terms; “seam” is not “boundary” here |
| Deletion test | interface is the test surface; one adapter / two adapters | domain-design; evidence-completion | Heuristics for whether a module earns its abstraction and whether a seam is real | Rejects pass-through modules, internal-coupled tests, and hypothetical seams | codebase-design + deepening + architecture | corroborated | `skills/engineering/codebase-design/SKILL.md:60-67`; `skills/engineering/codebase-design/DEEPENING.md:23-36` | Heuristics, not universal laws |
| Grill / shared understanding | relentless; decision tree; one question at a time | candidate-leading-word; workflow-control | Human-led interrogation that resolves dependent decisions sequentially | Separates discoverable facts from human-owned decisions and gates action | grilling + two wrappers + wayfinder/triage | corroborated | `skills/productivity/grilling/SKILL.md:6-12` | The human must confirm shared understanding before action |
| Active domain modeling | canonical term; glossary inline; ADR bar | domain-design; artifact-state | Changing a domain model, not merely consuming its vocabulary | Challenges ambiguity, checks code, records terms immediately, and keeps ADRs rare | domain-modeling + grill-with-docs + architecture/triage | corroborated | `skills/engineering/domain-modeling/SKILL.md:8,44-74` | `CONTEXT.md` is glossary-only; ADR requires all three stated conditions |
| Tracer-bullet vertical slice | vertical slice; one slice at a time | candidate-leading-word; workflow-control; evidence-completion | A narrow complete path through all needed layers, independently verifiable | Prevents horizontal batches and creates agent-sized work | to-tickets + TDD + implement/router/docs | corroborated | `skills/engineering/to-tickets/SKILL.md:25-38`; `skills/engineering/tdd/SKILL.md:28-35` | Wide mechanical refactors are an explicit exception |
| Blocking edges / frontier | blocked by; unblocked; blockers-first | workflow-control; artifact-state | Explicit dependency edges and the set of currently takeable work | Makes the same ticket graph sequential locally or parallel on a tracker | to-tickets + wayfinder + tracker templates | corroborated | `skills/engineering/to-tickets/SKILL.md:38-65`; `skills/engineering/wayfinder/SKILL.md:63-69` | “Frontier” has a narrower wayfinder meaning: open, unblocked, unclaimed children |
| Wide refactor / blast radius / expand-contract | expand; migrate; contract; integrate-and-verify | workflow-control; failure-exclusion | Mechanical cross-codebase change that cannot land as independent vertical slices | Preserves green states while migrating a broad change | to-tickets skill/docs + changelog | corroborated | `skills/engineering/to-tickets/SKILL.md:40` | Only applies when vertical slices cannot land green |
| Fixed point / two-axis review | Standards; Spec; smell baseline | evidence-completion; workflow-control | Resolve one comparison baseline, then review conventions and requested behavior independently | Prevents moving-baseline review and one axis masking the other | code-review skill/docs + router + changelog | corroborated | `skills/engineering/code-review/SKILL.md:6-23,78-87` | The pack asks for a user-supplied fixed point; Spec may explicitly skip if absent |
| Triage state machine | category role; state role; ready-for-agent; ready-for-human; needs-info; wontfix | workflow-control; artifact-state; pack-specific | Exactly one category and one state role per triaged item | Makes issue movement explicit and verification precede promotion | triage + setup + tracker templates + pack CONTEXT | corroborated | `skills/engineering/triage/SKILL.md:23-45,70-90` | Actual label strings may be mapped locally |
| Agent brief | durable; behavioral not procedural; key interfaces | artifact-state; relationship-handoff | Authoritative specification attached when work becomes agent-ready | Preserves behavior and acceptance while avoiding stale paths/lines | triage + AGENT-BRIEF + docs | corroborated | `skills/engineering/triage/AGENT-BRIEF.md:1-49` | “Agent-ready” is a pack workflow state, not proof of implementation readiness outside its checks |
| Tight, red-capable feedback loop | exact symptom; deterministic; fast; agent-runnable | candidate-leading-word; evidence-completion | One already-run command capable of going red on the reported bug and green after repair | Forbids theory-first diagnosis and anchors every later phase | diagnosing-bugs + router/docs + HITL script | corroborated | `skills/engineering/diagnosing-bugs/SKILL.md:12-60` | Nondeterministic bugs substitute a pinned high reproduction rate |
| Minimise / falsifiable hypothesis / correct seam | minimal repro; instrument; regression test | workflow-control; evidence-completion | Shrink the reproducer, rank predictions, change one variable, then lock the real bug at an adequate seam | Turns debugging into evidence consumption instead of plausible storytelling | diagnosing-bugs skill/docs | corroborated | `skills/engineering/diagnosing-bugs/SKILL.md:62-122` | If no correct seam exists, that absence is itself a finding |
| Red-green at pre-agreed seams | implementation-coupled; tautological; horizontal slicing | workflow-control; failure-exclusion | One failing test and minimal implementation per cycle, through a confirmed public interface | Keeps tests behavioral, independently sourced, and responsive to learning | TDD skill + tests/mocking refs + implement/spec docs | corroborated | `skills/engineering/tdd/SKILL.md:8-36`; `skills/engineering/tdd/tests.md:1-73` | Current body explicitly moves refactoring to review; metadata still says red-green-refactor |
| Prototype as primary source | throwaway code that answers a question; logic/UI branch | candidate-leading-word; evidence-completion; artifact-state | Disposable code selects a shape from the question, while runnable exploration is preserved off-main as evidence | Separates validated decision from non-production prototype code | prototype skill + two branch refs + docs + changeset | corroborated | `skills/engineering/prototype/SKILL.md:8-26` | “Throwaway” means excluded from main/production, not necessarily destroyed |
| Destination / decision ticket / map | decisions not deliverables; index not store; low-res/zoom | workflow-control; artifact-state; pack-specific | A map finds the way to a scoped destination through decision-bearing child issues | Keeps planning from silently becoming implementation and detail from duplicating into the map | wayfinder + ask-matt + tracker templates + pack CONTEXT | corroborated | `skills/engineering/wayfinder/SKILL.md:7-69` | Reserved for work larger and foggier than one session |
| Fog of war / graduate / not yet specified | frontier; out of scope | candidate-leading-word; workflow-control; pack-specific | In-scope uncertainty remains fog until its question can be precisely stated, then graduates into a ticket | Prevents premature decomposition and separates unknown-in-scope from ruled-out work | wayfinder skill/docs + changelog | corroborated | `skills/engineering/wayfinder/SKILL.md:82-101,113-126` | Fog is tested by question precision, not answer availability |
| HITL / AFK | human in the loop; agent alone | invocation-routing; workflow-control; pack-specific | Whether resolution requires a live human participant or can be agent-driven | Prevents agents from answering the human side of a decision and enables research parallelism | wayfinder + triage/setup docs | corroborated | `skills/engineering/wayfinder/SKILL.md:73-80` | Task tickets may be either; research is AFK; prototype/grilling are HITL |
| Handoff / compact | fresh session; same conversation | relationship-handoff; artifact-state | Handoff compacts live context into a bridge to a fresh session; compact summarizes within the same conversation | Makes context-boundary choice explicit | handoff + ask-matt + docs | corroborated | `skills/engineering/ask-matt/SKILL.md:61-64`; `skills/productivity/handoff/SKILL.md:7-17` | Handoff references settled artifacts instead of copying them |
| Mission / zone of proximal development | storage strength; fluency strength; learning record | domain-design; evidence-completion | A stateful teaching model that selects the next small lesson from purpose and demonstrated learning | Separates exposure from retained understanding and ties content to a real goal | teach skill + four formats + docs | corroborated | `skills/productivity/teach/SKILL.md:24-118`; `skills/productivity/teach/LEARNING-RECORD-FORMAT.md:1-35` | Established learning terms are operationalized by this pack; external validity was not researched |
| Explore / exploit writing frame | fragment; beat; grounded; prerequisite; introduced; pile/quarry | workflow-control; artifact-state; pack-specific | Draft writing separates divergent material mining from sequential article construction | Prevents premature structure and prevents later prose from leaning on ungrounded concepts | Three in-progress writing skills | corroborated | `skills/in-progress/writing-fragments/SKILL.md:7-40`; `skills/in-progress/writing-beats/SKILL.md:7-54`; `skills/in-progress/writing-shape/SKILL.md:7-73` | In-progress, not promoted; “explore/exploit” is adapted rather than defined as a pack-wide runtime term |
| Loop / workflow / push right | trigger; checkpoint; brief | workflow-control; artifact-state; pack-specific | A recurring life pattern becomes a workflow spec; human review is deferred and receives a decision-ready brief | Makes delegation and human-review placement explicit | in-progress loop-me skill + metadata | direct | `skills/in-progress/loop-me/SKILL.md:10-27` | In-progress and isolated; not corroborated across promoted skills |
| Grill the send, not the subject | questionnaire; gap; discovery questionnaire | workflow-control; relationship-handoff; pack-specific | Interview the sender only about recipient and needed outcome, then ask the recipient for missing knowledge asynchronously | Avoids asking a user to answer the very subject they lack | in-progress questionnaire skill + metadata | direct | `skills/in-progress/to-questionnaire/SKILL.md:7-19` | In-progress; one-off semantic owner |

## Techniques Encoded By The Language

| Vocabulary | Technique | Essential Mechanics | Use Context In The Pack | Failure / Misuse Risk | Claim Label | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| Leading word | Recruit a compact prior instead of restating a behavior | Choose a pretrained term, repeat the token rather than the explanation, place it in body and description when it also routes | Skill authoring and docs | A weak or invented word can become a no-op or cost more definition than it saves | direct | `skills/productivity/writing-great-skills/SKILL.md:61-72` |
| Context pointer + progressive disclosure | Load branch-specific reference only when needed | Inline common-path material; disclose conditional reference; sharpen pointer wording before moving required content back inline | Skill and repo instruction design | A link without a reliable condition creates a hidden variance bug | direct | `skills/productivity/writing-great-skills/GLOSSARY.md:37-41,101-105` |
| Completion criterion + legwork | Bind thoroughness to a checkable, demanding end state | Make done distinguishable and exhaustive; separate within-step effort from across-step rushing | Every bounded step or flat reference body | A vague criterion invites early stopping; visible later steps can worsen it | direct | `skills/productivity/writing-great-skills/GLOSSARY.md:137-159` |
| Grill | Resolve dependent human decisions sequentially | Walk one branch at a time, recommend an answer, look up facts, wait on human decisions, require confirmation | Planning, domain modeling, triage, wayfinder | Bulk questions lose dependency order; autonomous answers violate human authority | corroborated | `skills/productivity/grilling/SKILL.md:6-12`; `skills/engineering/wayfinder/SKILL.md:75-80` |
| Deep module | Deepen behind a small interface and test at that interface | Apply deletion test; classify dependencies; keep internal seams private; replace shallow tests with interface tests | Design, architecture improvement, TDD/spec seams | Premature seams create indirection; testing past the interface couples internals | corroborated | `skills/engineering/codebase-design/SKILL.md:60-67`; `skills/engineering/codebase-design/DEEPENING.md:1-36` |
| Tracer-bullet vertical slice | Deliver one narrow end-to-end behavior at a time | Cross necessary layers, make each slice independently verifiable, size to a fresh context, declare blockers | Ticket shaping and TDD | Horizontal batches verify imagined structure and delay evidence | corroborated | `skills/engineering/to-tickets/SKILL.md:25-40`; `skills/engineering/tdd/SKILL.md:28-35` |
| Wide refactor / expand-contract | Preserve operability through a broad mechanical migration | Add new form, migrate by blast-radius batches, remove old form; use final integration only if batches cannot stay green | Ticket shaping exception | Forcing a broad change into vertical slices or deleting old form early breaks the green invariant | direct | `skills/engineering/to-tickets/SKILL.md:40` |
| Tight red-capable loop | Make diagnosis consume an observable signal | Build and run one exact-symptom command; make it deterministic/fast/unattended; minimise; rank falsifiable hypotheses; instrument one variable | Hard bugs, flakes, performance regressions | A nearby failure or non-red-capable command drives the wrong diagnosis | direct | `skills/engineering/diagnosing-bugs/SKILL.md:12-124` |
| Two-axis review | Keep “built right” and “right thing” independent | Pin fixed point; discover standards and spec; run separate reviewers; never merge or rerank findings | Branch/PR/WIP review | A blended verdict lets one axis mask failure on the other | direct | `skills/engineering/code-review/SKILL.md:6-23,74-87` |
| Wayfinding | Delay decomposition until uncertainty becomes a precise question | Name destination; create index map; ticket only precise questions; keep coarse uncertainty in fog; claim frontier work; resolve at most one non-research ticket | Very large, foggy efforts | Using it for a well-scoped feature adds density; building from the map skips the spec collapse | corroborated | `skills/engineering/wayfinder/SKILL.md:7-126`; `skills/engineering/ask-matt/SKILL.md:44-46` |
| Prototype as primary source | Learn with disposable runnable code without promoting it as production | Pick logic/UI branch from the question; keep state visible; capture verdict; preserve runnable prototype off-main; fold only validated decision into real code | Design questions hard to settle on paper | Hardening the prototype or merging its untested shell confuses evidence with production | corroborated | `skills/engineering/prototype/SKILL.md:8-26`; `skills/engineering/prototype/LOGIC.md:7-91`; `skills/engineering/prototype/UI.md:7-112` |
| Active domain modeling | Keep language and consequential decisions synchronized with discussion and code | Challenge ambiguity, invent edge scenarios, cross-check code, update glossary inline, apply three-part ADR bar | Grilling, architecture, triage, direct domain work | Treating the glossary as a spec or recording routine choices as ADRs creates sediment | corroborated | `skills/engineering/domain-modeling/SKILL.md:44-74` |
| Push right | Delay a human checkpoint until useful work is prepared | Do maximal autonomous preparation, then present a brief linking the asset | In-progress workflow design | Deferring a checkpoint past an irreversible or judgment-heavy decision would be unsafe | direct | `skills/in-progress/loop-me/SKILL.md:20-23` |

## Aliases, Collisions, And Inconsistencies

| Terms | Relationship | Evidence | Consequence For Interpretation |
| --- | --- | --- | --- |
| User-invoked / model-invoked vs command / skill | Historical replacement | `.agents/invocation.md:1-12`; `CHANGELOG.md` 1.0.0 invocation-taxonomy entry | Read current bucket docs by invocation authority, not the older command/skill split. |
| Issue vs ticket vs decision ticket | Deliberate narrowing | `CONTEXT.md:7-18`; `skills/engineering/wayfinder/SKILL.md:7`; `.changeset/wayfinder-decision-tickets.md` | Ordinary tracked work is an issue; `to-tickets` still uses “ticket” operationally; wayfinder’s “decision ticket” is explicitly not an implementation slice. The pack is not fully terminologically uniform. |
| Seam vs boundary | Explicit rejection inside codebase-design | `skills/engineering/codebase-design/SKILL.md:22,105-109` | “Boundary” should not be silently substituted for the pack’s module-interface location. |
| Adapter vs implementation | Role/substance distinction | `skills/engineering/codebase-design/SKILL.md:18-24` | The same concrete object may be discussed by implementation content or adapter role; the nouns are not synonyms. |
| Red-green vs red-green-refactor | Current internal collision | `skills/engineering/tdd/SKILL.md:8,34-36`; `skills/engineering/tdd/agents/openai.yaml:3`; `docs/engineering/tdd.md:15-43` | The runtime body moves refactoring to review, while metadata and docs still recruit the established three-part phrase. Do not infer a single current loop definition without naming the surface. |
| Prototype: throwaway vs primary source | Deliberate semantic refinement | `skills/engineering/prototype/SKILL.md:8-26`; `.changeset/prototype-primary-source.md` | “Throwaway” means non-production/off-main, not necessarily deleted; the runnable artifact is retained as evidence. |
| Map vs decision map | Historical replacement | `CHANGELOG.md` 1.1.0 wayfinder entry; `skills/engineering/wayfinder/SKILL.md:7-23` | Current language uses wayfinding, map, destination, fog, and frontier; “decision map” was rejected as invented and inaccurate. |
| Fog vs not yet specified vs out of scope | Partition, not aliases | `skills/engineering/wayfinder/SKILL.md:82-101` | “Not yet specified” is in-scope fog; out-of-scope work never graduates. |
| HITL / AFK vs ready-for-human / ready-for-agent | Related but different axes | `skills/engineering/wayfinder/SKILL.md:73-80`; `skills/engineering/triage/SKILL.md:31-45` | HITL/AFK says who participates in resolving a decision; triage roles say who can take implementation next. |
| Negative space | Changelog-only current inconsistency | `CHANGELOG.md` 1.1.0 Negation/Negative Space entry; current `skills/productivity/writing-great-skills/SKILL.md:74-83` and `skills/productivity/writing-great-skills/GLOSSARY.md:119-201` omit it | Treat as historical or pending release prose, not retained current runtime vocabulary. |
| Package version | Conflicting metadata | `package.json:3`; `.claude-plugin/plugin.json:3`; `package-lock.json:2-8` | Use commit identity for this packet; version labels cannot identify this tree consistently. |

## Inferred Applications And Local Comparison

All statements in this section are downstream comparisons, not upstream facts.

- **Synthesis:** The local owners already share many upstream professional
  steering terms: `tracer bullet`, `vertical slice`, `deep module`, `interface`,
  `seam`, `feedback loop`, `fixed point`, and separate `Spec / Standards`.
  (`docs/agents/engineering-contract.md:20-30,37-53`;
  `docs/research/language/03-high-signal-steering-words.md:29-66`)

- **Synthesis:** The local authoring bridge already preserves the upstream
  agent-control cluster: `completion criterion`, `context pointer`,
  `progressive disclosure`, `single source of truth`, `no-op`, `leading word`,
  `legwork`, `premature completion`, and `post-completion steps`.
  (`docs/research/language/04-agentic-bridge-vocabulary.md:86-102`)

- **Synthesis:** Local `Router skill` is stricter than upstream’s general
  definition: locally it returns exactly one next route and leaves work
  unstarted, while upstream `ask-matt` can return a flow and ordering. These are
  overlapping concepts, not proven aliases. (`CONTEXT.md:115-120`;
  `skills/engineering/ask-matt/SKILL.md:7-13`)

- **Synthesis:** Upstream `seam` and local `proof seam` collide partially.
  Upstream uses seam for the location where a module interface lives and
  behavior can vary; local `proof seam` is specifically the caller-facing or
  observable boundary where meaning is established. Later synthesis would need
  to preserve the qualifier or validate that one term can safely cover both.
  (`skills/engineering/codebase-design/SKILL.md:22`;
  `docs/agents/engineering-contract.md:20-22`)

- **Synthesis:** Upstream’s current TDD body conflicts with the local steering
  owner’s `red-green-refactor` definition. Upstream ends the implementation loop
  at green and assigns refactoring to review; local research retains the classic
  three-part cycle. This packet does not choose between them.
  (`skills/engineering/tdd/SKILL.md:34-36`;
  `docs/research/language/03-high-signal-steering-words.md:33-36`)

- **Synthesis:** Local `.tmp` / `.scratch` gives a stronger durability contract
  than upstream’s tracker examples: locally `.tmp` is disposable and `.scratch`
  is durable/version-controlled, while upstream uses `.scratch` as a local
  issue/spec medium without establishing repository-wide version-control
  semantics. (`CONTEXT.md:59-60`;
  `skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md:1-27`)

- **Synthesis:** The local engineering contract extends upstream’s fixed-point
  review language with `review snapshot`, `semantic proof`, `proof lane`,
  `residual risk`, and `Lock`. Upstream supplies the two axes and baseline;
  local language supplies a stronger immutable-target and completion envelope.
  (`docs/agents/engineering-contract.md:20-32,83-92`;
  `skills/engineering/code-review/SKILL.md:6-23,74-87`)

- **Inference:** Wayfinder’s destination/fog/frontier frame could be useful
  evidence for later work on uncertainty-aware planning, but the local steering
  owner explicitly de-emphasizes repo-specific operational terms such as
  `decision map`. Any adoption would need behavioral validation showing that the
  metaphor improves routing without displacing clearer professional terms.
  (`docs/research/language/03-high-signal-steering-words.md:74-100`)

- **Inference:** The in-progress writing and workflow terms are the weakest
  adoption candidates because they are coherent only inside inactive drafts.
  They should not be treated as pack-wide vocabulary unless promoted and shown
  to recruit useful behavior outside those narrow skills.

## Prune Log

| Removed Or Merged Material | Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |
| Generic action verbs: read, write, ask, run, check, fix, commit | No pack-specific semantic load | Named workflow terms and completion criteria | A verb gains a defined contrast or state transition |
| Framework/tool nouns: GitHub, GitLab, Claude, Codex, Tailwind, Mermaid, dependency-cruiser, Husky, Prettier | Platforms and implementation mechanisms, not vocabulary owners | Issue tracker, metadata, report, boundary-rule concepts | The question changes to tool integration language |
| Fowler smell names | Established review checklist, not distinctive pack semantics; retained collectively as “smell baseline” | Fixed point / two-axis review | A later packet studies code-review vocabulary specifically |
| Triage label strings individually | Merged into the triage state-machine owner | Triage state machine | A later synthesis designs tracker lifecycle vocabulary |
| Setup file and command names | Incidental mechanics or artifact paths | Setup/config and context-pointer concepts | A setup-contract study needs exact interfaces |
| Wizard helper names and terminal UI phrases | Local template interface, not spread beyond one in-progress skill | Wizard/stage concept was itself not admitted | The wizard is promoted or human-procedure UX becomes the question |
| Shoehorn, exercise, pre-commit, Obsidian terminology | Narrow domain/tool language with no pack-wide semantic role | None | The question narrows to those individual skills |
| Deprecated QA/refactor-plan vocabulary | Historical procedures superseded by triage, to-spec/to-tickets, codebase-design, and domain-modeling | Current promoted owners | Historical evolution becomes the question |
| Negative Space | Mentioned in changelog but absent from current authoring runtime and glossary | Negation plus Branch | The term reappears in current authoritative surfaces |
| Smart zone | One router reference to an external article; not defined by the pack | Context load, handoff, context hygiene | The external source is inspected and the term becomes operational elsewhere |
| Frequency-only candidates | Frequency is discovery evidence, never admission | Semantic owners above | A term acquires a traceable behavior or distinction |

## Evidence Gaps

- The source tree contains no behavioral tests or evaluation transcripts. This
  packet can establish vocabulary and instructed behavior, not that the words
  reliably change model behavior.
- No external-origin study was performed. Where the pack attributes terms to
  Ousterhout, Feathers, Fowler, DDD, TDD, the Pragmatic Programmer, learning
  science, or explore/exploit theory, this packet does not independently verify
  those histories or external definitions.
- Release identity is inconsistent across manifests; the Git commit is the only
  stable identity for the inspected tree.
- `Negative Space` is described in the changelog but absent from the current
  authoring skill and glossary; its current status is unresolved, so it was not
  admitted.
- `red-green-refactor` appears in metadata and human docs while the TDD runtime
  body explicitly defines a red-green loop with refactoring moved to review.
  Both surfaces are recorded; no canonical interpretation is selected.
- In-progress, personal, miscellaneous, and deprecated skills were inspected
  and clearly status-labeled. Their terms do not establish promoted pack
  behavior unless corroborated by promoted surfaces.
- The checkout was not fetched by request. Its clean equality with the local
  `origin/main` ref does not establish equality with the network remote on
  2026-07-22.

These gaps do not prevent answering what language the supplied revision uses;
they limit claims about effectiveness, external provenance, release version,
and local suitability.

## Source Trace

| Source | Authority | Version Or Date | Supports |
| --- | --- | --- | --- |
| `skills/productivity/writing-great-skills/SKILL.md` and `skills/productivity/writing-great-skills/GLOSSARY.md` | Explicit semantic owner for skill-authoring vocabulary | `ed37663` | Predictability, invocation economics, information hierarchy, leading words, completion, pruning, failure modes |
| `skills/engineering/ask-matt/SKILL.md` | Pack router and relationship map | `ed37663` | Main flow, on-ramps, standalone skills, vocabulary layers, cross-session routing |
| `skills/engineering/codebase-design/SKILL.md` and disclosed references | Explicit semantic owner for design vocabulary | `ed37663` | Module/interface/depth/seam/adapter/leverage/locality and design heuristics |
| `skills/engineering/wayfinder/SKILL.md` plus tracker templates | Runtime owner and storage interfaces | `ed37663` | Destination, map, decision tickets, fog, frontier, HITL/AFK, claim/resolve semantics |
| `skills/engineering/diagnosing-bugs/SKILL.md` | Runtime diagnostic procedure | `ed37663` | Tight red-capable loop, minimisation, hypotheses, instrumentation, correct seam |
| `skills/engineering/to-tickets/SKILL.md` and `skills/engineering/tdd/SKILL.md` | Runtime delivery and test procedures | `ed37663` | Tracer bullets, vertical/horizontal slicing, blockers, wide refactors, red-green |
| `skills/engineering/code-review/SKILL.md` | Runtime review procedure | `ed37663` | Fixed point, Standards/Spec axes, smell baseline |
| `skills/productivity/grilling/SKILL.md` and `skills/engineering/domain-modeling/SKILL.md` | Runtime owners for human decision and domain-language work | `ed37663` | Shared understanding, facts/decisions, canonical terms, glossary/ADR discipline |
| `skills/engineering/prototype/SKILL.md`, `skills/engineering/prototype/LOGIC.md`, `skills/engineering/prototype/UI.md` | Runtime owner and branch references | `ed37663` | Throwaway question-answering code and primary-source preservation |
| `skills/productivity/teach/` | Runtime owner and artifact formats | `ed37663` | Mission, learning records, storage/fluency strength, knowledge/skills/wisdom |
| `skills/in-progress/` writing/workflow/questionnaire skills | Direct draft owners | `ed37663` | Explore/exploit, fragment/beat/grounding, push right, send/subject gap |
| `.agents/invocation.md`, `.agents/writing-docs.md`, `CLAUDE.md`, `README.md`, `CHANGELOG.md`, changesets, metadata | Pack governance, human routing, and change rationale | `ed37663` | Status, invocation parity, leading-idea documentation, renames, inconsistencies |
| Local `CONTEXT.md` and `docs/agents/engineering-contract.md` | Current local vocabulary owners | inspected 2026-07-22 | Synthesis-only comparison with repository and runtime terms |
| Local `docs/research/language/03-high-signal-steering-words.md` and `docs/research/language/04-agentic-bridge-vocabulary.md` | Current local research owners | inspected 2026-07-22 | Synthesis/inference-only overlap and collision analysis |

## Final Decision

`source-packet-complete`

The supplied revision is fully accounted for, every retained term has an exact
semantic owner and status-aware provenance, aliases and collisions are visible,
local comparisons are separated from upstream claims, and the remaining gaps
limit effectiveness or external-validity claims rather than the source question.
