# Upper-Bound Engineering Language Validation Roadmap

Status: planned, budget-gated

Supports:
[Upper-Bound Engineering Language](../language/upper-bound-engineering-language.md)
and later synthesis decisions under `docs/synthesis/skills/`

Authority: research backlog only; this document does not establish canonical
vocabulary, validate a runtime skill, authorize a correction, or require every
listed research lane

Default next packet: UBL-00 Claim And Assumption Ledger

Future source-evidence-note convention:
`docs/research/language/validation/UBL-XX-<slug>.md`

UBL-16 through UBL-23 are downstream candidate-validation module labels.
Their evidence belongs to the exact synthesis or runtime candidate's
authorized validation owner, not automatically under language research.

## Purpose And Boundary

This roadmap separates two questions that should not share one budget:

1. **Source validation:** Does the language reference represent its sources,
   professional meanings, conditions, disagreements, and pack intent
   responsibly?
2. **Candidate validation:** Does one exact wording change improve one owned
   agent behavior against a realistic control?

The source campaign validates the reference. It may confirm, narrow, split,
demote, rewrite, reject, or leave a claim unresolved. It does not prove that
an abstract term changes agent behavior. Behavioral proof follows an exact
candidate path and wording, fixed tasks, and a candidate-owned evidence
record.

The listed UBL identifiers are a research menu, not a batch. UBL-00 activates
only the smallest high-leverage claim cohort. Unselected claims remain
conditional or deferred with visible evidence gaps. Detailed packet or
evaluation design is written only after its admission gate fires.

This roadmap does not itself browse, reopen upstream repositories, contact
people, run evaluations, edit the language reference, change synthesis, or
modify runtime skills. Each action requires separate authorization. The source
campaign may finish at UBL-24 without any downstream candidate evaluation.

## Lean Campaign Spine

```text
UBL-00 claim ledger
  -> if admitted: one selected UBL-01-through-UBL-08 source packet
  -> only a decision-blocking UBL-09-through-UBL-15 lane
  -> UBL-24 correction decision
  -> stop source campaign

later exact candidate
  -> smallest applicable UBL-16-through-UBL-23 module set
  -> candidate-owned decision
```

The default source campaign is therefore UBL-00, at most one source packet,
and UBL-24. When no source claim passes admission, skip the source packet and
proceed directly to UBL-24. A second concept cluster or contextual lane is
admitted only when the first result cannot support an honest bounded
correction.

Packet IDs preserve the original taxonomy. They identify available research
pressure and allow one-by-one tracking; they do not imply separate artifacts,
fixed execution order, or an obligation to run the full inventory.

## Proof Layers

| Proof Layer | Question | Strong Evidence | Insufficient By Itself |
| --- | --- | --- | --- |
| Semantic fidelity | Does the term mean what the reference says? | Exact inspected sections of original books, papers, standards, specifications, canonical documentation, or source repositories | Titles, snippets, summaries, isolated quotations, or pack repetition |
| Professional validity | Do credible engineers use the concept with comparable mechanics and limits? | Original definition plus independent professional, empirical, or field evidence and counterpressure | Popularity, one famous author, frequency, or slogans |
| Pack intent | Why did a pack introduce, change, or remove the wording? | Bounded commit lineage, diffs, issues, tests, deleted wording, design notes, or maintainer explanation | Current file text or author recollection alone |
| Behavioral effect | Does exact wording improve agent behavior? | A realistic failing control and repeated fresh-context comparison against the exact candidate | Plausible prose, one success, description recall, or an uncalibrated judge |
| Transfer | Does the effect survive a changed model, harness, context, or task? | Candidate-preserving replication with configuration and variance reported | One model, harness, prompt, or task family |
| Local suitability | Does the candidate help this pack without breaking ownership, invocation, proof, or completion? | Frozen local tasks and candidate-owned shadow evidence | External authority or upstream adoption |

Match proof to the claim:

- semantic claims need exact source meaning and enough context to prevent
  distortion;
- professional-validity claims need independent evidence; semantic claims do
  not acquire this burden merely because the concept is useful;
- pack-intent claims need only the bounded history capable of deciding them;
- behavioral claims need an exact candidate and a red-capable control;
- broad transfer claims need replication, while local claims may remain
  explicitly environment-specific;
- removing or demoting a claim does not require promotion-level proof.

For the language reference, semantic fidelity, professional validity where
claimed, and pack intent are the default layers. Behavioral effect, transfer,
and local suitability remain `unverified`, `upstream-reported`, or linked to
exact reusable candidate evidence.

## Default Resource Envelope

These are admission defaults, not targets to consume.

### Source Campaign

| Resource | Default Bound | Expansion Gate |
| --- | --- | --- |
| Active cohort | Only claims that pass admission, up to five; zero is valid | An omitted high-consequence claim blocks the same correction |
| Concept clusters | One UBL-01-through-UBL-08 cluster | The first packet leaves UBL-24 unable to decide a material correction |
| Semantic source work | One canonical or original source plus a bounded countersearch | Source conflict, inadequate access, or an undecidable semantic claim |
| Independent corroboration | Required only when the wording asserts professional validity or the decision is high-consequence and disputed | A second independent source can resolve the remaining decision |
| Repository history | Introducing, materially changing, superseding, or removing lineage for selected claim IDs only | Bounded lineage exposes a decision-relevant contradiction |
| Field cases | Zero by default | Canonical sources conflict and one professional-transfer claim remains material |
| External conversations | Zero by default | Stronger reproducible evidence leaves a high-impact intent or terminology question unresolved |
| Behavioral agent runs | Zero | A later exact candidate separately authorizes evaluation |
| Endpoint | UBL-24 after admitted source work, if any | A named source gap blocks an honest bounded decision |

A bounded countersearch is required; finding a second source is not. If no
credible limiting evidence is found within the declared search boundary,
record that result and its limitations. Do not manufacture corroboration or
continue searching to fill a quota.

### Downstream Candidate Validation

This budget is outside source-campaign completion.

| Stage | Default Bound | Expansion Gate |
| --- | --- | --- |
| Candidate | One exact wording change in one named synthesis or runtime skill | Multiple changes are behaviorally inseparable and jointly owned |
| Initial task | One fixed representative task | The candidate claims broader behavior or has a material adjacent-negative risk |
| Control admission | Five fresh control runs; stop if the claimed failure does not appear | Configuration drift invalidates an otherwise reusable control |
| Initial screen | Five admitted control runs and five exact-candidate runs: 10 total | The control fails and the result can change the candidate |
| Scoped expansion | Add a second or third task, or an F/G term-contribution arm; normally 20 to 30 total runs | Breadth, wrong-condition risk, or term attribution is part of the candidate's claim |
| Exceptional initial ceiling | 45 total runs | Separately authorized precision need and decision value |
| Transfer | One changed model-or-harness factor, one to three tasks, and 10 to 30 runs | The surviving candidate explicitly promises broader transfer |
| Local shadow | One frozen historical task first; at most three | Local adoption remains plausible and risk justifies broader coverage |

Five samples per arm are a behavioral screening floor, not confirmatory proof.
Narrow the claim or return `needs-more-evidence` when the bounded result cannot
support it. Unused budget expires.

## Admission And Economy Gates

Apply these gates in order:

1. **Decision:** open work only when its result can change an exact row, tier,
   alias, condition, gate, or completion rule.
2. **Cohort:** activate only high-consequence, uncertain, reusable source
   claims that pass admission, up to five in one concept cluster. Zero active
   claims is valid and proceeds directly to UBL-24.
3. **Cheapest decisive evidence:** use source meaning for semantics, independent
   evidence only for professional validity, and targeted history for intent.
4. **Reference completion:** proceed to UBL-24 with behavior explicitly
   unverified; do not run an abstract term experiment.
5. **Blocker:** open another source lane only when the current evidence cannot
   support an honest bounded UBL-24 decision.
6. **Candidate:** behavioral work requires one exact path, wording, owned
   failure, fixed task, proof output, and finite budget.
7. **Control:** if the incumbent or no-guidance control does not exhibit the
   claimed failure, return `reject-no-control-failure`.
8. **Survivor:** add tasks, diagnostics, transfer, pruning, or local trials only
   after the exact candidate improves without a critical regression.
9. **Budget:** stop at the admitted cap and preserve the residual gap unless a
   separately authorized expansion can change the decision.

## Evidence Ownership

The
[Source Distillation Flow](../../synthesis/methods/source-distillation-flow.md)
owns source selection, access-depth reporting, claim labels, source meaning,
counterevidence, prune logs, evidence gaps, and the terminal source-packet
decision. Use its
[Prompt 05](../../synthesis/methods/prompts/05-distill-source-packet.md)
output rather than restating that contract in every UBL item.

The current canonical
[Behavioral Skill Evaluation](../../../skills/custom/writing-great-skills/BEHAVIOR-EVALS.md)
contract owns failure diagnosis, uncontaminated controls, fresh samples,
rubrics, judgment, recording, and candidate outcomes. UBL-16 through UBL-23
add only candidate-specific admission and optional research pressure.

One campaign ledger owns claim state, evidence pointers, resource use, and
revisit triggers. An evidence packet owns its inspected source registry and
findings. A candidate record owns behavioral evidence. Do not copy any of
these into a second authority.

Store each raw source or run corpus once and reference it by stable path,
revision, or hash. Reuse an evaluator, frozen task, source, or control only
when its evidence contract and configuration still match.

## Coverage Lock

Compression routes research; it does not replace the language reference as
the claim inventory. UBL-00 must map every decision-bearing Fast Lookup row,
Tier 1 anchor, Tier 2 method, Tier 3 situational term, steering formulation,
alias or collision, weak-language row, agreement or disagreement, application
index row, prune decision, and evidence gap to a ledger claim or an explicit
deferred group.

An admitted packet reads the exact current rows it owns, not only the compact
menu summary. It carries forward their meaning, recruited behavior, entry
condition, mechanics, evidence gate, misuse risk, claim label, provenance,
limitations, and disagreement. Group rows only when one evidence decision can
responsibly decide them together.

## Campaign Ledger

UBL-00 creates one ledger at:
`docs/research/language/validation/UBL-00-claim-ledger.md`

Later source packets append evidence pointers and dispositions. UBL-24
reconciles the ledger. Packet notes do not duplicate its queue or resource
tables.

### Claim Ledger

| Field | Purpose |
| --- | --- |
| Claim ID and exact location | Stable reference to one decision unit in the language document |
| Exact claim and class | Independently testable semantic, professional, intent, behavioral, transfer, local, or collision statement |
| Current evidence and label | Source pointer plus `direct`, `corroborated`, `synthesis`, `inference`, or `thin` |
| Hidden assumption and falsifier | What the wording presumes and what would narrow or overturn it |
| Required proof and owner | Smallest proof layer and one source packet or future exact-candidate trigger |
| Consequence and risk | Exact decision affected and impact if wrong |
| Queue state and revisit trigger | `active`, `conditional`, or `deferred` plus the observation that changes it |
| Result | `confirm`, `narrow`, `split`, `demote`, `rewrite`, `reject`, or `unresolved` |
| Behavioral status | `untested`, `upstream-reported`, `candidate-accepted`, `candidate-rejected`, or `environment-specific` |

### Evidence Pointer

| Evidence ID | Claim IDs | Artifact And Locator | Revision Or Check Date | Access And Authority | Supports / Limits |
| --- | --- | --- | --- | --- | --- |
| stable ID | owned claims | one source packet, repository lineage, conversation record, or candidate record | immutable revision or live check | exact inspected depth and source role | bounded claim contribution and explicit limitation |

### Resource Ledger

| Work Unit | Planned Cap | Used | Decision Gained | Stop Or Expansion Reason |
| --- | ---: | ---: | --- | --- |
| one admitted source packet or candidate record | finite source, history, contact, review, or run budget | actual use | claim IDs advanced | terminal stop or separately authorized expansion |

## Claim Dispositions

Research completion, source disposition, and behavioral status remain
separate.

| Disposition | Meaning | Evidence Threshold |
| --- | --- | --- |
| Confirm | Current bounded source wording survives | Required source layers agree at the claimed strength |
| Narrow | The idea survives only under tighter conditions | Counterevidence identifies a stable boundary |
| Split | One owner hides materially different meanings | Sources or exact behaviors require separate claims |
| Demote | A useful distinction is situational rather than broad | Evidence depends on workflow, risk, model, harness, or artifact |
| Rewrite | Mechanics matter but the current owner or wording misleads | Stronger source language or candidate evidence supports the replacement |
| Reject | The claim is unsupported, harmful, or behaviorally inert | Stronger evidence contradicts it or a valid candidate test rejects it |
| Unresolved | Evidence remains conflicted or inaccessible | A named gap prevents a responsible decision |

Cross-pack repetition is evidence of shared skill-pack usage only. Source
confirmation never promotes an untested behavioral claim.

## UBL-00: Claim And Assumption Ledger

Research question: Which load-bearing source claims should this finite campaign
test, and which behavioral or transfer claims must remain downstream?

Inputs:

- Upper-Bound Engineering Language;
- the Matt Pocock, Superpowers, and Ponytail vocabulary packets;
- Engineering Steering Vocabulary;
- Agentic Bridge Vocabulary.

Method:

1. Inventory every decision-bearing section named by the Coverage Lock at a
   coarse decision-unit level.
2. Split only high-leverage compound statements into falsifiable semantic,
   professional, intent, behavioral, transfer, local, or collision claims.
3. Record current evidence, its original label, the hidden assumption, and a
   falsifier.
4. Score consequence if wrong, uncertainty, downstream leverage, and expected
   verification cost.
5. Activate only source claims that pass admission, up to five in one
   UBL-01-through-UBL-08 cluster. Mark every other claim conditional or
   deferred with a revisit trigger. If none pass, proceed directly to UBL-24.
6. Assign the single selected source packet to every active claim it can
   decide. Defer a claim that requires a different packet unless it blocks the
   same correction. Give behavioral and transfer claims only an exact
   future-candidate trigger.
7. For any active cohort, project a zero-agent-run source budget and the
   smallest source or history work capable of deciding it.

Completion gate:

- every decision-bearing reference row has a ledger owner, an explicit grouped
  owner, or a deferred state with a coarse semantic status;
- every steering formulation separates term, action, and gate claims;
- behavioral and transfer claims are explicitly untested unless exact reusable
  candidate evidence exists;
- the active cohort contains only admitted claims in one concept cluster,
  never more than five, and may be empty;
- no claim is justified only by cross-pack repetition;
- every deferred item has a reason and revisit trigger;
- the source campaign can proceed without rereading the entire reference to
  rediscover scope.

UBL-00 routes evidence. It does not browse, decide wording, run evaluations,
or edit the language reference.

## Source Verification Menu

UBL-01 through UBL-15 are selectable research lanes. An admitted packet owns
only its chosen claim IDs and the exact decision they can change. Candidate
sources below are discovery targets, not pre-approved authorities. Before
packet admission, verify the edition or revision, current status, and access
depth needed to inspect the decision-bearing material. Treat excerpts,
summaries, and secondary descriptions as scoped evidence rather than silent
substitutes for an inaccessible canonical source. Record inadequate access as
an evidence gap; a separately admitted alternative may support a narrower
claim but does not inherit canonical authority.

### Canonical Meaning And Professional Validity

| ID | Decision Question | Strongest Starting Lanes | Required Counterpressure | Likely Correction |
| --- | --- | --- | --- | --- |
| UBL-01 | Are tracer bullet and vertical slice distinct learning and delivery shapes? Do bite-sized, frontier, blocking edge, blast radius, and expand-contract preserve completeness, readiness, independence, and migration exceptions? | Exact tracer-bullet passages in `The Pragmatic Programmer`; original vertical-slice, XP, agile, parallel-change, and expand-contract sources; mature API and schema migration guidance | Horizontal or staged work that is safer; green intermediate state without independent parallelism; mechanical migration versus product slice | Split tracer bullet from vertical slice; narrow vertical-slice default or frontier; replace or qualify expand-contract |
| UBL-02 | What does RED-GREEN-REFACTOR require, including observed intended RED, minimal GREEN, refactoring while green, and a valid public or pre-agreed seam? When does TDD fit, and does the analogy transfer to skill wording? | `Test-Driven Development by Example`; original test-first and refactoring sources; systematic or empirical TDD research; relevant Matt and Superpowers lineage | Legacy, exploratory, nondeterministic, UI, data, and integration work; behavioral versus implementation-coupled seams; test-first versus test-after | Add entry conditions; separate code TDD from skill evaluation; preserve a real Matt/Superpowers disagreement |
| UBL-03 | Which diagnostic mechanics reduce uncertainty, and where do deterministic reproduction, one-variable hypotheses, minimal reproducers, caller repair, root cause, and condition waits overstate certainty? | `Why Programs Fail` and scientific-debugging sources; SRE, incident, distributed-systems, and empirical debugging evidence | Statistical reproduction; exploratory instrumentation; multi-causal, flaky, concurrent, performance, environmental, and socio-technical failures; containment and defense in depth | Prefer causal explanation or contributing conditions where needed; narrow sequence absolutes; separate diagnosis from repair placement |
| UBL-04 | How do deep module, interface versus API, seam versus boundary, adapter role versus implementation substance, information hiding, leverage, locality, and deletion test differ? | `A Philosophy of Software Design`; `Working Effectively with Legacy Code`; Parnas; original ports-and-adapters material; modularity and change-locality research | Small interfaces that hide harmful coupling; structural proxy versus observed locality; retain, merge, inline, or no-new-seam cases | Split colliding owners; qualify deep-module and deletion-test claims; add an explicit no-new-seam control |
| UBL-05 | What do ubiquitous language, active domain model, cross-artifact synchronization, scenario testing, shared understanding, sequential elicitation, fact discovery, and ADR thresholds establish? | `Domain-Driven Design` and authoritative DDD material; original decision-record guidance; requirements-elicitation and decision research | Multiple bounded contexts, regulated or contested terms, exploratory domains, batched versus sequential decisions, routine logs versus durable records | Bound language by context; separate understanding from specification; demote one-question cadence if it remains procedural |
| UBL-06 | When do reuse, native-first search, sufficiency, shortest working diff, deletion, YAGNI, dependency restraint, and known ceilings reduce total complexity rather than cause under-delivery? | Original XP, YAGNI, lean, simplicity, reuse, technical-debt, and design-option sources; dependency, maintenance, security, accessibility, performance, and operability evidence | Reuse that creates coupling; native options with portability or edge-case costs; new modules or dependencies that simplify the total system; shortest diff in the wrong owner | Replace a universal ladder with conditions; demote shortest-diff language; separate ceiling, residual risk, debt, trigger, action, and owner |
| UBL-07 | Which distinctions should govern fixed review baselines, Spec and Standards, verification, validation, semantic proof versus artifact existence, proof scope, freshness, completion versus legwork, and correct, safe, and complete judgments? | Verification and validation standards; mature review, release, testing, assurance, safety, and empirical code-review sources | Missing or moving specifications; probabilistic and visual work; human acceptance; immutable targets; proof whose command covers only one layer | Split evidence, proof, verification, and validation; qualify freshness and fixed-point language; preserve scorer-specific and completion-demand limits |
| UBL-08 | Are leading words and intentional token repetition distinct from duplication? Do context pointers, progressive disclosure, information hierarchy, discovery metadata, route-only routing, fresh-context handoff, and one semantic owner with thin adapters work as claimed? | Current primary research on instruction following, prompt sensitivity, retrieval, long context, tool use, agents, information architecture, schemas, and cognitive priming; official platform documentation | Invented versus established terms; term alone versus action plus gate; pointer versus actual retrieval; metadata versus procedural body; file existence versus fresh-context recovery; human-interface evidence versus LLM evidence | Label coined or adapted terms honestly; narrow harness-specific claims; split reachability, routing, injection, and duration; leave behavior unverified |

One canonical source and bounded countersearch are enough for a semantic
decision when access is strong and the wording makes no professional-validity
claim. Add independent corroboration only under the resource gate.

### Conditional Intent, Field, And Conversation Lanes

| ID | Open Only When | Bounded Method | What It Can Establish | Stop Or Limitation |
| --- | --- | --- | --- | --- |
| UBL-09 | A selected Matt Pocock claim has unresolved provenance or intent | Pin the repository revision; trace only introducing, materially changing, superseding, or removing lineage; inspect associated diffs, tests, issues, deleted wording, and status | Current versus draft or superseded ownership; the failure pressure behind selected terms; unresolved migrations such as TDD placement, seam language, routers, prototypes, or Wayfinder | Do not audit the whole repository; changelog-only or inactive vocabulary remains historical, not current authority |
| UBL-10 | A selected Superpowers claim depends on history or evaluation lineage | Pin the canonical revision; trace only admitted wording; inspect actual scenarios, prompts, models, repetitions, rubrics, outputs, and external evaluation artifacts when required | What hard gates, invocation thresholds, RED-GREEN-REFACTOR, review protocols, SDD, bootstrap, or description rules were designed and tested to do | Historical bounded evaluations do not prove universal behavior; classify structural proxies and harness exceptions |
| UBL-11 | A selected Ponytail claim depends on benchmark, adapter, or lifecycle lineage | Pin the revision; reconstruct only the required benchmark generation, baseline, scorer, task, mode, or host surface; run deterministic scorer self-tests only when feasible | Whether ladder, shortest-diff, safety-floor, ceiling, lifecycle, behavior-gate, instrument-first, or savings claims survive contamination and adapter drift | Reduced code volume does not establish correctness, safety, completeness, maintainability, or real savings |
| UBL-12 | An active agent-specific claim cannot be decided from inspected packets and local terminology owners | Search current primary papers and official documentation only for the selected claim; separate human-interface findings from LLM findings; inspect benchmark and judge limits | Current support for context retrieval, prompt sensitivity, skill discovery, tool use, agent evaluation, memory, compaction, or benchmark transfer | Vendor-, model-, length-, harness-, and task-specific results remain scoped; this lane does not open behavioral evaluation |
| UBL-13 | Canonical sources conflict and one professional-transfer claim remains material | Select one behavior family; inspect one positive operational case and one limiting, bypass, or negative case; add a second pair only if the decision remains blocked | Observable field mechanics, gates, outcomes, and contexts; differences between book language and mature practice | Prestige, convention, popularity, and term frequency are not outcome evidence |
| UBL-14 | Bounded repository history leaves one high-impact pack-intent question unresolved | Contact the directly responsible author or maintainer once with one reasonable follow-up; ask about failure, observable effect, non-applicability, rejected alternatives, and revision criteria before showing this roadmap's interpretation | Intended meaning, tacit exceptions, and disagreement with repository history | Intent is not efficacy; recollection does not erase contemporaneous repository evidence; non-response is an evidence gap |
| UBL-15 | A decision-critical terminology-prior or collision claim survives stronger evidence | Run a scenario-first pilot with three relevant senior practitioners and one or two scenario families; capture natural mechanics and terms before showing candidate vocabulary | Ambiguity, natural professional priors, counterexamples, and whether a term clarifies or distorts mechanics | Three participants cannot establish consensus or saturation; broader outreach requires separate authorization |

For conversations, obtain consent, record role and date, separate verbatim
statements from synthesis, protect sensitive material, and preserve
non-response as a gap. Conversations never establish agent efficacy.

### Just-In-Time Source Packet

When a menu gate fires, create only this admission header and then use the
canonical source-distillation flow:

| Field | Required Value |
| --- | --- |
| Menu ID and claim IDs | One lane and the active cohort claims it owns |
| Decision | Exact language row, tier, alias, condition, or gate that can change |
| Boundary | Included question, explicit exclusions, and freshness need |
| Source plan | Canonical lane, bounded countersearch, and conditional corroboration or history |
| Budget | Finite sources, lineage, contacts, and human-review allowance |
| Stop | Evidence sufficient for a bounded disposition, cap reached, or named blocker |
| Output | One `docs/research/language/validation/UBL-XX-<slug>.md` packet and one ledger pointer |

Start with
[Prompt 01](../../synthesis/methods/prompts/01-scope-source-question.md).
Use a facet map only for genuinely independent questions. End with exactly
`source-packet-complete`, `evidence-gap`, or `blocked`.

## UBL-24: Final Correction Decision

Research question: Given the admitted source evidence, deferred claims,
behavioral statuses, and residual gaps, what bounded correction decision
follows for Upper-Bound Engineering Language?

UBL-24 owns source-synthesis judgment. It does not run missing behavioral work,
edit the reference, or authorize runtime changes.

Required matrix:

| Claim ID | Current Wording And Location | Source Evidence | Source Disposition | Behavioral Status | Proposed Correction Or No-Change | Residual Gap Or Candidate Trigger |
| --- | --- | --- | --- | --- | --- | --- |
| from UBL-00 | exact section or row | evidence pointers and scope | confirm, narrow, split, demote, rewrite, reject, or unresolved | untested, upstream-reported, candidate-accepted, candidate-rejected, or environment-specific | bounded wording or structural change, or no-change | honest unknown or exact future-candidate condition |

Required outputs:

- permission to propose no wording changes when evidence confirms the current
  wording; unresolved claims remain gaps rather than reasons to manufacture a
  correction;
- reconciled active and deferred claim ledger;
- source-backed correction or no-change decision for exact rows;
- preserved disagreements, counterevidence, and access limits;
- Tier, alias, collision, failure-mode, and prune-log changes only where the
  admitted evidence reaches them;
- explicit behavioral-status register;
- exact future-candidate triggers where behavioral proof still matters;
- exact rows that remain unchanged;
- statement that application, synthesis, and runtime work require separate
  authorization.

Completion:

- every active source claim has a disposition or named blocker;
- deferred claims remain visibly unvalidated with revisit triggers;
- no behavioral or transfer claim is promoted from source plausibility;
- proposed wording stays inside the inspected evidence;
- an independent reader can trace each correction or no-change decision to one
  evidence pointer without reopening conversation context.

Return exactly:

- `source-packet-complete` when a bounded correction matrix is ready;
- `evidence-gap` when useful work exists but a material source decision remains
  unresolved;
- `blocked` when the ledger cannot be responsibly reconciled.

After UBL-24, stop the source campaign. Applying its proposal is separate work.

## Downstream Candidate-Validation Handoff

Do not open this section for a vocabulary row or abstract formulation. Admit
it only when one named synthesis or runtime skill contains exact candidate
wording and owns a behavioral claim.

### Admission Record

| Field | Requirement |
| --- | --- |
| Candidate owner | One synthesis or runtime skill and its canonical path |
| Candidate | Immutable exact wording, placement, version, and diff |
| Failure | Observable incumbent failure the candidate claims to change |
| Control | Realistic no-guidance or incumbent wording capable of exhibiting that failure |
| Task | One fixed representative task first, with positive or adjacent-negative cases when the failure type requires them |
| Harness | Fixed model, reasoning, tools, authority, context, runtime, and rubric |
| Output | Candidate-owned validation record; language research stores only a pointer |
| Budget | Ten-run initial screen and any separately gated expansion |

If any field is missing, return `blocked` or keep the behavioral claim
`untested`. Do not design a generic vocabulary experiment as a substitute.

### Behavioral Proof Floor

Use the current canonical Behavioral Skill Evaluation contract at execution
time. The non-negotiable floor is:

1. Diagnose the exact failure before choosing instruction form.
2. Freeze task, context, configuration, rubric, control, and candidate.
3. Run five fresh control samples. Stop when the claimed failure does not
   appear.
4. Run five fresh candidate samples only for an admitted control.
5. Inspect outputs with an explicit rubric; preserve variance, worst result,
   critical failures, deviations, and unavailable telemetry.
6. Accept only material improvement without a critical regression.
7. Return `accept`, `reject-no-control-failure`, `reject-regression`,
   `needs-more-evidence`, or `blocked` without extrapolation.

Use deterministic checks where possible and blind human review where judgment
is necessary. A model judge may supplement but never replace those controls
for a load-bearing claim. Score the target behavior plus semantic correctness,
scope and authority, evidence, completion, proportionality, safety and
preservation, and cost where applicable. A wording revision starts a new
immutable candidate record; do not pool results across versions.

Term contribution is optional and separate. Compare F, plain action plus gate,
with G, the term plus identical action and gate, only when choosing the term
can change the candidate. If F and G are equivalent, prefer plain mechanics
unless the term earns another demonstrated invocation, context, or maintenance
benefit.

### Optional Module Menu

| ID | Module | Admission Gate | Smallest Useful Work | Evidence Or Stop |
| --- | --- | --- | --- | --- |
| UBL-16 | Evaluation-method review | One candidate has material scorer, contamination, or isolation risk | One independent review of the exact candidate, control, task, rubric, and smallest comparison | Revise or stop if the design cannot isolate the claimed contribution |
| UBL-17 | Evaluator calibration | No reusable evaluator is red-capable for the selected behavior | Known-good and lazy-plausible known-bad cases; deterministic clean-fail-restored proof where applicable; judge calibration only for used criteria | Stop when the evaluator distinguishes admitted good and bad work and its limits are recorded |
| UBL-18 | Candidate screen | Exact candidate, realistic control, frozen task, and evaluator are ready | One task, five control runs, then five candidate runs; add tasks only under the budget ladder | Candidate outcome plus variance, worst result, side effects, and residual gap |
| UBL-19A-J | Behavior-family pressure | The candidate promises one named family not covered by UBL-18 | Select one family and one scenario class first; add wrong-application or broader classes only when claimed | Never generalize beyond tested family and scenarios |
| UBL-20 | Cross-model or cross-harness transfer | A reproducible survivor explicitly promises transfer | Change one model-or-harness factor; preserve task, candidate, control, and rubric; map tool differences explicitly; record context, retrieval, and invocation changes | Classify broad, model-specific, harness-specific, task-specific, or unresolved |
| UBL-21 | Side effects and process cost | Existing runs expose an unresolved material tradeoff | Measure cost and harms in existing arms; add one missing decision-critical scenario only if necessary | Retain, add entry condition, demote, or reject based on benefit-cost evidence |
| UBL-22 | Candidate pruning regression | A surviving candidate has one removable semantic unit | Remove one unit, rerun the same calibrated controls, and stop a dependency chain at the first failed cut | Mark the unit load-bearing, useful compression, redundant, or unresolved |
| UBL-23 | Local historical shadow | A surviving candidate is still being considered for local adoption | One leakage-audited frozen historical task and two arms first; use blind review where feasible; expand to at most three tasks for material local risk | Local accept, narrow, reject, or unresolved without live skill mutation |

UBL-16, UBL-20, standalone UBL-21, UBL-22, and UBL-23 are survivor-only.
UBL-17 may be reused when task behavior, rubric, and configuration remain
equivalent. Optional modules do not inherit unused budget from earlier work.

Across modules, monitor adjacent costs that can reverse an apparent win:
false invocation, unnecessary questions or ceremony, tokens and tool calls,
elapsed time and user turns, scope expansion or under-delivery, abstraction or
TDD bias, premature stopping, context loss, review burden, and damage to
unrelated state or safety boundaries. Add runs only for a missing
decision-critical side effect.

### UBL-19 Behavior-Family Pressure Menu

This is a scenario library, not ten packets.

| ID | Behavior Family | Representative Positive And Negative Pressure | Primary Measures |
| --- | --- | --- | --- |
| UBL-19A | Invocation and routing | Explicit and implicit triggers, tempting false positive, route-only request, overlapping skills | Invocation precision and recall, pre-action compliance, false-trigger cost |
| UBL-19B | Context and information loading | Common path, branch-only reference, missing or stale pointer, misleading link, long context | Required retrieval, missed rule, irrelevant load, stale-source use |
| UBL-19C | Intent, requirements, and decisions | Discoverable fact, human preference, ambiguous term, irreversible decision, trivial choice | Correct authority, question count, shared understanding, scope and latency |
| UBL-19D | Planning, slicing, and dependencies | End-to-end feature, horizontal temptation, genuine migration, hidden blocker, false parallelism | Slice completeness, blocker accuracy, independent proof, green intermediate state |
| UBL-19E | Implementation and test-first proof | Clear behavior, understood and uncertain bugs, legacy seam, nondeterminism, trivial change | Correct red, red reason, behavioral seam, minimal green, refactor safety, fit |
| UBL-19F | Debugging and uncertainty reduction | Exact and intermittent failures, multi-causal incident, performance regression, misleading nearby symptom | Reproduction quality, hypothesis discrimination, causal evidence, repair placement |
| UBL-19G | Design, interfaces, and simplification | Real abstraction, pass-through wrapper, reusable owner, native feature, dependency, no-new-seam case | Interface leverage, locality, coupling, unnecessary machinery, preserved requirements |
| UBL-19H | Review, evidence, and completion | Stable and moving baselines, missing spec, polished wrong output, partial or probabilistic proof | Finding validity, Spec and Standards, proof scope, completion accuracy |
| UBL-19I | Collaboration and handoffs | Warm and fresh owners, incomplete brief, shared state, independent work, compaction recovery | Handoff fidelity, rediscovery, duplicate work, conflicts, cleanup preservation |
| UBL-19J | Skill authoring and pruning | Discipline failure, shape error, omission, conditional choice, duplicated prose, removed term, stale pointer | Behavioral improvement, retrieval, variance, no-op detection, pruning parity |

One scenario class supports only that scenario. A family-wide claim requires
meaningfully different ordinary, failure-revealing, and wrong-application
classes and their separately admitted run budget.

### Candidate Record

The candidate owner records:

- exact control and candidate hashes or immutable text;
- task and starting-state provenance;
- model, harness, tools, authority, context construction, and runtime;
- rubric, deterministic checks, and judge calibration;
- sample counts and order;
- complete trajectories, tool outputs, diffs, tests, and review artifacts;
- per-sample result, aggregate, variance, worst result, and critical failures;
- process cost and side effects;
- deviations, contamination risk, unavailable telemetry, and raw-artifact
  pointers;
- terminal decision and residual gap.

The language reference may link to this record only for the exact tested
wording and scope. It must not generalize or duplicate the result.

## Stop And Completion Rules

Stop a source packet when its bounded claim is decided, the next evidence unit
cannot resolve a named falsifier, disagreement, or disposition, searches
repeat existing evidence, its cap is reached, or a precise access or evidence
gap can be returned honestly.

Stop candidate work when the control does not fail, the candidate regresses,
the admitted decision is supported, the budget expires, or the residual
uncertainty requires separate authorization.

Do not continue because:

- a packet or module has an ID;
- unused budget remains;
- a famous source agrees;
- several repositories repeat a term;
- one model output looks good;
- a participant or author is confident;
- a result is convenient for current synthesis.

The source campaign is complete when:

- every active source claim has its required evidence or an explicit gap;
- each selected collision or disagreement has a bounded disposition;
- deferred work and revisit triggers remain visible;
- behavioral, transfer, and local claims retain their actual status;
- UBL-24 can reach correction or no-change decisions without inventing
  consensus;
- no UBL-16-through-UBL-23 module is required for source completion.

## Anti-Expansion Rules

- Add packet detail to the admitted evidence note, not this roadmap.
- Add a new roadmap rule only when it governs more than one likely packet.
- Keep menu IDs even when no packet is executed; do not create placeholder
  files.
- Do not convert source inventories into required coverage.
- Do not recalibrate or rerun unchanged evidence under a new ID.
- Narrow a claim before expanding evidence when both yield the same honest
  decision.
- Preserve contract-bearing proof and completion mechanics; prune explanatory
  repetition around them.

## Start Here

Run UBL-00 only.

It should inventory claims without browsing, contacting people, running
evaluations, or editing the language reference. Activate only claims that pass
admission, up to five in one concept cluster, and project the zero-agent-run
source budget. If none pass, proceed directly to UBL-24.

Otherwise, after review, run one selected UBL-01-through-UBL-08 source packet.
Open one conditional UBL-09-through-UBL-15 lane only if that packet leaves the
same bounded correction undecidable. Then proceed to UBL-24 and stop.
