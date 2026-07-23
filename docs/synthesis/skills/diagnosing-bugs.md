# Diagnosing Bugs Runtime Synthesis

Status: decision-complete; Deploy Prompt 2 result is `no-change`.

This synthesis records the confirmed Deploy Prompt 1 decision for
`$diagnosing-bugs`. It is design and provenance authority, not runtime
instructions. Runtime authority remains in:

- `skills/custom/diagnosing-bugs/SKILL.md`;
- `skills/custom/diagnosing-bugs/agents/openai.yaml`;
- the caller's scope, mode, and mutation authority;
- `docs/agents/engineering-contract.md` and routed domain contracts;
- `docs/synthesis/skill-context-relationships.md`; and
- current pack tests and evaluation definitions.

The decision is intentionally small:

```text
B0 = the exact current canonical package
C1 = B0 + no additions
```

No experimental candidate, runtime rewrite, new reference, relationship
change, evaluation campaign, promotion, installation, or delivery is admitted.

## Confirmed Outcome And Viability Floor

Diagnosing Bugs turns one uncertain existing-behavior failure into an
evidence-backed causal explanation and the smallest safe next action. It may
retain a production fix only when the user or caller supplied implementation
authority.

The minimum viable runtime must preserve:

| Concern | Viability floor |
| --- | --- |
| Outcome | Prove the cause of the exact reported symptom before recommending or applying a fix |
| Invocation | Admit broken, failing, flaky, slow, environment-only, or production-only behavior when expected behavior, exact symptom, cause, or trusted red-capable reproduction is uncertain |
| Authority | Distinguish diagnosis from fix mode; retain caller ownership of scope, review, Git, tracker, external, release, Lock, and architecture work |
| Causal sequence | `Trace -> Loop -> Minimise -> Hypothesise -> Probe -> Prove -> Return` |
| Safe failure | Return decision-needed when expected behavior is unsettled; return blocked when no evidence-capable Loop or required authority exists; make no unsupported causal claim |
| Irreversible order | Evidence-capable Loop before causal hypothesis; Cause Gate before fix; fix proof before completion |
| Safety | Preserve unrelated work; separately approve live instrumentation, persisted telemetry, external writes, sensitive capture, and durable evidence |
| Return | Return the causal and regression packet to the original caller; a standalone diagnosis recommends `$implement` and stops |
| Completion | Cause Gate and cleanup for diagnosis; additionally authorized causal fix, applicable regression proof, original-scenario proof, and relevant comparison for fix mode |

## Evidence Registry And Freshness

Prompt 1 inspected the complete current synthesis, canonical package, runtime
pointers, affected caller surfaces, relationship map, current structural tests,
evaluation definitions and relevant transcripts, all three required upstream
checkouts, and the applicable engineering-language rows.

| Evidence | Identity or access depth | Role | Freshness limit |
| --- | --- | --- | --- |
| Canonical `SKILL.md` | SHA-256 `d289f553a633be8d5ab4de2e6d2031d045ef023f29cb9f3ad537565c493d1b7b` | Exact B0 runtime | Read from repository `98c628c686f4e63c021a725b4805b9a4873ae4a0` on 2026-07-22 |
| Canonical `agents/openai.yaml` | SHA-256 `d9ef3372e04c488b227009cd14ef0ed84fa4335056d48219bc6cbf8a80a970bd` | Exact B0 invocation policy | Same repository snapshot |
| Engineering and domain docs | Complete `engineering-contract.md` and `domain.md` | Shared language, proof, work-state, and domain routing | Current checkout only |
| Relationships and callers | Complete relationship map; relevant complete canonical caller packages and supporting surfaces | Trigger, authority, and Return ownership | Current checkout only |
| Structural proof | Relevant rows in `tests/test_skill_pack_contracts.py` | Ordered spine, policy, routing, Return, and relationship contracts | Inspected source; not rerun in Prompt 1 or 2 |
| Behavioral definitions | Diagnosis Return Ownership and Disjoint Bug Routing in `core-workflows.md` | Required positive and critical-failure cases | Definitions only, not fresh behavior samples |
| Historical evaluation | 2026-07-12 and 2026-07-13 cohesion/whole-pack transcripts | Historical routing and Return evidence | Reduced-confidence or contract-simulation evidence; not current live difficult-branch proof |
| Matt Pocock | Clean `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; complete matching package, metadata, HITL template, docs, and relevant changelog | Credible upstream baseline candidate | Checkout commit dated 2026-07-21; matched recorded upstream; no remote refresh |
| Superpowers | Clean `d884ae04edebef577e82ff7c4e143debd0bbec99`; complete `systematic-debugging` package and all disclosed files plus relevant release records | Credible upstream baseline candidate and source pressure | Checkout commit dated 2026-07-02; matched recorded upstream; no remote refresh |
| Ponytail | Clean `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; complete skill inventory and main `ponytail` package | No matching debugging package; corroborating root-cause placement only | Checkout commit dated 2026-07-15; matched recorded upstream; no remote refresh |
| Engineering-language synthesis | Applicable debugging, falsifiable-hypothesis, root-cause, completion, and skill-evaluation rows plus their local source pointers | Research pressure and claim labels | Local synthesis; not professional authority or behavioral proof |

Prompt 1 prohibited browsing, remote refresh, and new behavioral evaluation.
These identities therefore prove what was inspected, not that upstream has not
changed since its recorded commit.

## Simplest Credible Baseline Comparison

| Candidate | Core strengths | Missing or excess relative to the local floor | Decision |
| --- | --- | --- | --- |
| Current canonical runtime | Compact exact-symptom Loop, minimisation, falsifiable hypotheses, Cause Gate, modes, local mutation boundaries, failed-fix recovery, caller Return | No demonstrated viability-floor omission | **Select as B0** |
| Matt Pocock `diagnosing-bugs` | Strong tight-loop emphasis, broad harness ladder, minimisation, regression seam, tagged cleanup | Requires local mode, caller, four-fact, authority, dirty-work, and Return adaptation; carries a mandatory hypothesis count, human checkpoint, helper template, and architecture handoff not required locally | Keep as provenance; reject as executable B0 |
| Superpowers `systematic-debugging` | Root-cause investigation, evidence gathering, pattern comparison, one-variable hypothesis tests, backward tracing | Broader 296-line core plus disclosed catalog; categorical rhetoric, fixed failure-count architecture escalation, defense-in-depth mandate, and implementation coupling exceed the local floor | Keep source pressure; reject as executable B0 |
| Ponytail | Trace callers and repair a shared semantic cause with a small diff | No matching diagnosis lifecycle, evidence loop, authority, blocked Return, or cleanup contract | Supporting rationale only |
| Scratch outline | Could be shorter conceptually | Unnecessary because the current canonical package is already credible, executable, locally compatible, and smaller than the matching upstream package | Not used |

The current runtime wins by behavior and semantic density, not raw word count.
Choosing an upstream would require adding the same mandatory local contracts
that the current runtime already expresses while also removing upstream
machinery.

## Current Runtime Behavior Dispositions

Every distinct current-runtime behavior has one disposition. `Protect` means
protect the behavior in B0, not freeze every sentence as universally optimal.
Because B0 is the exact current package, no byte change is authorized by this
decision.

| Current behavior | Disposition | Basis and owner |
| --- | --- | --- |
| Implicit trigger for broken, failing, flaky, slow, environment-only, or production-only behavior with an uncertain bug fact | `protect` | Core outcome; description and invocation policy own reach |
| Fix only with implementation authority | `protect` | Required local authority contract |
| Seven-stage causal spine and two causal laws | `protect` | Core outcome and irreversible order |
| Diagnosis mode versus fix mode | `protect` | Required local mutation boundary |
| Caller owns scope, review, staging, commit, tracker/external mutation, push, release, Lock, and architecture follow-up | `owned elsewhere` | Caller contract; Diagnosis retains only causal work and an authorized causal fix |
| Return to original caller; standalone diagnosis recommends `$implement` | `protect` | Required local Return contract |
| Four-fact pre-Trace handoff to `$tdd` with non-bounce rule | `protect` | Required local caller relationship |
| Engineering and domain document pointers | `protect` | Minimum context pointers to shared owners |
| `.tmp` disposable boundary and separately approved live, persisted, external, sensitive, and `.scratch` behavior | `protect` | Non-intuitive safety and authority boundary |
| Source Trace, independent expected-behavior oracle, fixed point, worktree, and prior evidence qualification | `protect` | Exact-symptom and state-preservation contract |
| Decision-needed Return when expected behavior remains unresolved | `protect` | Safe failure before causal judgment |
| Evidence-capable, exact-symptom, repeatable, tight, agent-runnable Loop | `protect` | Core outcome |
| Escalation from nearby automation through replay, harness, fuzz/bisection/differential evidence to structured HITL | `protect` | Cheapest current expression of difficult reproduction branches |
| Flake exposure fields and performance baseline/constraint | `protect` | Existing minimum support for explicitly invoked failure classes |
| Blocked Return when no red-capable Loop can be built | `protect` | Core causal safety boundary |
| One-factor-at-a-time minimisation with load-bearing or unremovable stop | `protect` | Core uncertainty reduction |
| Ranked falsifiable hypotheses, competing explanation, and hypothesis ledger | `protect` | Core causal discrimination; no mandatory count |
| One-variable probe, targeted instrumentation, and tagged cleanup | `protect` | Core causal discrimination plus reversible mutation safety |
| Cause Gate: prediction, symptom coverage, discrimination, and alternative disposition | `protect` | Core causal-claim boundary |
| Diagnosis-mode recommendation without retained production change | `protect` | Required authority contract |
| Correct-seam RED/GREEN, smallest causal fix, original unminimised Loop, and branch comparison in fix mode | `protect` | Core fix proof |
| Honest seam gap without false durable regression coverage | `protect` | Non-intuitive proof boundary |
| Failed-fix removal limited to authored changes, exact-state stop when isolation is unsafe, then return to hypotheses | `protect` | Non-intuitive work-preservation boundary |
| Removal and verification of temporary instrumentation and artifacts | `protect` | Cleanup and completion safety |
| Complete diagnosis packet with proof, cleanup, residual risk, and skipped checks | `protect` | Required Return evidence |
| Completion differs for diagnosis and fix modes | `protect` | Required completion and authority boundary |

No current behavior is classified `replace`, `remove`, or `disclose`. The old
synthesis proposed those changes, but they were never promoted into current
runtime and did not acquire authority through documentation alone.

## Research Intake And Local Dispositions

The engineering-language file labels these rows as synthesis, direct, or
corroborated evidence from the inspected packs. None is independent local
behavioral proof.

| Research pressure and original claim label | Local disposition | Reason |
| --- | --- | --- |
| Tight, red-capable feedback loop; `synthesis`, Matt corroborated, Superpowers direct | `supporting rationale only` | Already expressed in B0; no semantic or behavioral delta |
| Falsifiable hypothesis; `synthesis`, Matt corroborated, Superpowers direct | `supporting rationale only` | Already expressed through prediction, competitor, probe, and ledger |
| Systematic diagnostic loop; `synthesis`, Matt and Superpowers direct | `supporting rationale only` | B0 already implements the locally bounded causal sequence |
| Root cause, not symptom, plus caller trace; `synthesis`, Ponytail and Superpowers corroborated | `candidate mechanism` then `defer` | Enumerating every caller can help multi-path defects but is an added universal action without an observed B0 failure |
| Observable evidence controls action and completion; `synthesis`, cross-pack corroborated | `supporting rationale only` | Already owned by B0 and the engineering contract |
| Qualified parallel investigation; `synthesis` | `reject` | One bounded symptom has one causal owner; no demonstrated benefit justifies dispatch or recombination machinery |
| Pressure-tested skill wording; `synthesis`, Superpowers corroborated | `owned elsewhere` | Proof method belongs to Writing Great Skills and Prompt 4, not diagnosis runtime |
| Behavior-gate/evaluator self-test; `synthesis`, Ponytail corroborated | `owned elsewhere` | Evaluation-harness concern, not runtime behavior |

No item qualifies as a semantic substitution: B0 contains no identified
misleading source term that can be corrected at equal or lower runtime load.
No source question can change an admitted ledger row, so there is no Research
Interlude.

## Unified Baseline-Delta Ledger

| Mechanism | Baseline state | Current disposition | Research pressure and claim label | Admission basis | Owner | Cheaper expression | Runtime destination | Required proof | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Exact-symptom evidence Loop | Present | Protect | Tight loop; synthesis with direct/corroborated pack evidence | `core outcome` | Diagnosing Bugs | Current Loop contract | B0 `SKILL.md` | Current-contract preservation plus representative exact/lookalike cases | B0 |
| Four-fact TDD boundary and caller Return | Present | Protect | Local contract evidence | `required local contract` | Diagnosis, TDD, callers, relationship map | Current shared predicate | Existing owner surfaces | Relationship trace and routing cases | B0 |
| Diagnosis/fix modes and separate mutation authorities | Present | Protect | Local contract and engineering contract | `required local contract`; `non-intuitive safety or authority boundary` | Caller plus Diagnosing Bugs | Current mode boundary | B0 `SKILL.md` | Authority-pressure and no-mutation cases | B0 |
| Minimisation, falsifiable competitor, one-variable probe, Cause Gate | Present | Protect | Systematic loop and falsifiable hypothesis; synthesis/direct/corroborated | `core outcome` | Diagnosing Bugs | Current causal spine | B0 `SKILL.md` | Causal discrimination and overclaim controls | B0 |
| Flake/performance/HITL minimum fields | Present compactly | Protect | Tight-loop and systematic-loop rationale | `core outcome` for named invocation branches | Diagnosing Bugs | Current inline branch clauses | B0 `SKILL.md` | Branch-matched cases only when a claim changes | B0 |
| Correct-seam regression, honest seam gap, original scenario | Present | Protect | Root-cause and evidence-before-claims rationale | `core outcome`; `non-intuitive safety or authority boundary` | Diagnosing Bugs | Current Prove contract | B0 `SKILL.md` | Regression-seam, no-seam, and original-scenario cases | B0 |
| Failed-fix isolation and cleanup reconciliation | Present | Protect | Local work-state contract | `non-intuitive safety or authority boundary` | Diagnosing Bugs | Current Prove/Return clauses | B0 `SKILL.md` | Dirty-work and failed-fix preservation cases | B0 |
| Evidence-state transition table | Absent | Defer | Old synthesis inference | None | Would be Diagnosing Bugs | Existing ordered stages and explicit gates | None | Control must first show wrong-operation selection | Deferred |
| Per-operation completion table | Absent | Defer | Old synthesis inference | None | Would be Diagnosing Bugs | Existing stage and final completion criteria | None | Control must first show premature stage completion | Deferred |
| `EVIDENCE-BRANCHES.md` | Absent | Defer | Old synthesis inference | None | Would be Diagnosing Bugs | Current inline branch minimums | None | Control must show a specific branch omission; retrieval must then be proved | Deferred |
| Four typed outcome schemas | Absent | Defer | Old synthesis inference | None | Would be Diagnosing Bugs | Current decision-needed, blocked, diagnosis, fix, and packet language | None | Control must show ambiguous Return or ownership | Deferred |
| Expanded Diagnostic Mutation Envelope | Absent as named machinery; essential rules already present | Defer | Old synthesis inference | None beyond rules already in B0 | Would be Diagnosing Bugs plus caller | Current authority, starting-state, tagging, cleanup, and exact-state rules | None | Control must show a concrete mutation-safety failure not covered by B0 | Deferred |
| Mandatory affected-caller enumeration | Absent | Defer | Root-cause caller trace; synthesis with Ponytail/Superpowers corroboration | None | Would be Diagnosing Bugs | Inspect callers only when the causal hypothesis requires it | None | Multi-path control must show a missed shared cause | Deferred |
| Independent hypothesis scouts | Absent | Reject | Qualified parallel investigation; synthesis | None | Foreign orchestration owner | Single causal owner | None | Not applicable until a bounded need exists | Rejected |

No ledger row enters C1.

## Executable B0 Specification

B0 is not a conceptual rewrite. It is the exact two-file canonical package
identified in the evidence registry. A reproducible B0 copy requires those
exact bytes and no additional files.

Its semantic surface is:

```text
implicit uncertain-bug admission
  -> diagnosis | explicitly authorized fix mode
  -> Trace independent oracle, exact evidence, and starting state
  -> Loop on the exact symptom or return blocked
  -> Minimise while preserving the real failure
  -> Hypothesise with falsifiable competing predictions
  -> Probe one discriminating variable under reversible authority
  -> pass Cause Gate before recommendation or fix
  -> diagnosis recommendation | authorized causal fix and regression proof
  -> reconcile instrumentation, artifacts, worktree, proof, and residual risk
  -> Return to original caller | recommend Implement for standalone diagnosis
```

B0 includes the complete protected behavior set above. It requires no invented
reference, helper, schema, candidate file, caller change, or relationship
change.

## C1 Delta Set

C1 is exactly B0. The admitted-addition set is empty.

Therefore there is no C1 entry condition, failure Return, destination, or
mechanism-contribution claim to implement or test. Creating a candidate that
only recopies B0 would manufacture lifecycle state without a behavioral
question and would not satisfy Prompt 3's purpose.

## Ownership, Relationships, And Loading

| Surface or behavior | Owner and preserved relationship |
| --- | --- |
| Direct request | Diagnosing Bugs; diagnosis mode unless implementation is explicit |
| Route selection | `$skill-router` recommends Diagnosing Bugs and stops for an uncertain bug fact |
| Interview gap | `$grilling` recommends Diagnosing Bugs and stops; no fix authority |
| Source mismatch | `$research` recommends Diagnosing Bugs and stops when the missing authority is causal reproduction rather than source evidence |
| Audit finding | Audit finding contract may suggest Diagnosing Bugs; Audit starts nothing |
| Selected implementation | `$implement` invokes Diagnosing Bugs in fix mode inside its Charter, then resumes review and closeout |
| Parallel lane | The lane worker invokes fix mode inside its assignment and returns to the same lane |
| Conflict proof | `$resolving-merge-conflicts` invokes diagnosis mode, receives a causal packet, and retains reconciliation/Finish authority |
| TDD boundary | `$tdd` hands uncertain bug facts to Diagnosis; Diagnosis hands off only when all four facts were already known before Trace |
| Standalone proved diagnosis | Diagnosing Bugs recommends explicit `$implement` and stops |
| Shared engineering and domain behavior | `engineering-contract.md` and `domain.md`; Diagnosis points rather than copying |
| Runtime context | Universal behavior remains in the existing `SKILL.md`; no branch reference is admitted |

The prior synthesis's direct Wayfinder-to-Diagnosis edge and reference to
`skills/custom/wayfinder/OPERATIONS.md` are drift, not current canonical
contracts. The canonical Wayfinder package has no such surface. No Wayfinder
relationship is admitted here; any future coordinated Wayfinder candidate must
establish and prove its own caller contract before this synthesis changes.

## Runtime And Affected-Surface Map

| Surface | Prompt 2 disposition | Future change condition |
| --- | --- | --- |
| `skills/custom/diagnosing-bugs/SKILL.md` | Preserve exact B0 | Only a later confirmed non-empty C1 packet |
| `skills/custom/diagnosing-bugs/agents/openai.yaml` | Preserve implicit policy | Only invocation evidence admitting a metadata delta |
| Caller skills and worker briefs | Preserve | Only a confirmed relationship or authority delta |
| `docs/synthesis/skill-context-relationships.md` | Preserve current canonical edges | Only a coordinated accepted runtime relationship change |
| Structural tests and behavior definitions | Preserve | Only proof directly affected by admitted candidate bytes |
| Experimental manifest and candidates | Not applicable | Prompt 3 with a non-empty C1 only |
| Installed mirror | Owned by Prompt 5 installation | Never edit as canonical source |

Common-path behavior stays inline in B0. No disclosed branch is selected.
Caller-owned review, Git, tracker, release, Lock, architecture, evaluator,
installer, worker topology, and delivery procedures stay outside Diagnosis.

## Rejected And Deferred Design

Rejected:

- mandatory three-to-five hypothesis counts;
- mandatory user checkpoints before probes;
- automatic architecture escalation after an arbitrary fix count;
- defense-in-depth changes as part of every causal fix;
- persisted diagnostic state, event ledgers, generated packet schemas, or helper CLIs;
- independent hypothesis scouts for one bounded symptom;
- automatic live instrumentation, telemetry, dependency, service, or external mutation; and
- review, commit, tracker closeout, deployment, or downstream execution inside Diagnosis.

Deferred until an observed B0 failure supplies an admission basis:

- evidence-state and per-operation completion tables;
- a disclosed evidence-branches reference;
- stricter typed outcome schemas;
- a named expanded Diagnostic Mutation Envelope;
- mandatory affected-caller enumeration;
- statistical, minimisation, or HITL helpers; and
- a separate production-diagnosis skill.

Deferral is not a queued recommendation. Each idea returns to Prompt 1 only
after exact new evidence can change its ledger decision.

## Claim-To-Proof Matrix

| Claim lane | Current claim | Available evidence | Required future proof or limit |
| --- | --- | --- | --- |
| Semantic fidelity | B0 uses exact-symptom, falsifiable-hypothesis, root-cause, and evidence-before-claims concepts consistently with inspected source pressure | Complete source read and local comparison | Source pressure supports meaning, not behavioral efficacy |
| Mechanism contribution | No C1 mechanism improves on B0 | No contribution claim is made | A future mechanism needs a realistic B0 control failure before a candidate arm |
| Invocation and context loading | Current implicit predicate, policy, four-fact boundary, and no-extra-reference shape are preserved | Metadata read-back, relationship trace, structural tests, historical routing evidence | No fresh invocation samples in Prompt 2; required only if metadata or loading changes |
| Current-contract preservation | Exact B0 bytes preserve current behavior and caller relationships by identity | SHA-256 identities, complete read-back, caller and relationship trace | Existing structural checks were inspected but not rerun; no runtime byte changed |
| Pruning equivalence | No runtime pruning occurred | Not applicable | No pre-prune fixture or equivalence claim should be created |
| Deterministic proof | Two-file package identity, implicit policy, ordered headings, relationship edges, and packet surface are structurally checkable | Existing pack tests and current hashes | Prompt 2 validates synthesis only; runtime tests remain unchanged |

Historical evaluation supports only its recorded snapshot and protocol. The
2026-07-12 pass scored Diagnosis Return Ownership `5/5` but lacked an
independent runner. The 2026-07-13 evidence was primarily contract simulation
plus executable structural regressions. Neither proves live intermittent,
performance, environment-only, production-instrumentation, sensitive-data, or
failed-cleanup behavior for the current model and host.

## Candidate Lifecycle And Residual Gaps

Candidate lifecycle state: none.

- No `diagnosing-bugs` entry exists in `skills/experimental/manifest.json`.
- No executable B0 fixture was created because the canonical package itself is
  the confirmed exact B0.
- No C1 package, pre-prune fixture, validation record, promotion record, or
  accepted candidate hash exists.
- Prompt 2 does not manufacture historical minimality, contribution, pruning,
  or behavioral proof.

Residual gaps:

- no fresh behavior evaluation of current difficult branches;
- no live intermittent, performance, environment-only, or production-only run;
- no injected cleanup, sensitive-data, or external-state failure campaign; and
- upstream freshness is bounded by the inspected checkout commits.

These gaps do not admit a candidate because no C1 claim depends on them. They
become decision-bearing only if new evidence identifies a B0 failure or a
required caller, platform, safety, or completion contract changes.

## Dry Read As Prompt 3 Input

Prompt 3 has no work to perform:

- B0 is exact, executable, locally compatible, and fully identified;
- every current runtime behavior and applicable research item has one
  disposition;
- the protected behavior set is explicit;
- every foreign behavior points to its owner;
- competing future-rewrite prose has been removed;
- C1 contains zero admitted additions; and
- no candidate or proof claim should be manufactured.

The terminal Prompt 2 decision is therefore `no-change`, not
`ready-for-prompt-3`. A future campaign begins again at Deploy Prompt 1 only
when new evidence can change the unified ledger.
