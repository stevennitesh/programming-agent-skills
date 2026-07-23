# Prototype Skill Synthesis

Status: promoted and closed. The canonical and installed Prototype package is
exact accepted C1
`ed5832972cbd1a093656087a7efc61e679f4068b3bea330204ba6559fb78ce33`.
The experimental package and manifest entry are retired. This document records
the final design; the canonical runtime owns executable behavior, and the
validation record owns campaign evidence and chronology.

## Final Decision

Prototype is an implicitly invocable leaf that answers one bounded design
question with a disposable runnable probe. Its durable output is supported
design evidence with stated limits, not production implementation or proof.

The final lifecycle is:

```text
Fit -> Freeze -> Branch -> Probe -> Smoke and Judge -> Reconcile -> Return
```

- **Fit** admits only one material design decision answerable by one bounded
  runnable-evidence question and mutates nothing on mismatch.
- **Freeze** establishes the question, decision, evidence surface, authorities,
  verdict basis, representatives, mutation boundary, artifact disposition,
  run recipe, finite bound, and known limits before mutation.
- **Branch** loads only the decision-bearing Logic, UI, or Measure contract.
- **Probe** builds the smallest artifact capable of changing the verdict.
- **Smoke and Judge** separates runnable, judgeable evidence from a supported
  result and from unsupported production claims.
- **Reconcile** accounts for every effect and leaves no live resource.
- **Return** reports the truthful result or residual directly to the current
  caller or user and starts no downstream route.

Executable authority lives in:

- [`SKILL.md`](../../../skills/custom/prototype/SKILL.md) for Fit, Freeze,
  mutation authority, lifecycle, reconciliation, Return, and completion;
- [`LOGIC.md`](../../../skills/custom/prototype/LOGIC.md) for deterministic
  state, rule, data, API, and interface-behavior probes;
- [`UI.md`](../../../skills/custom/prototype/UI.md) for structural visual and
  interaction probes; and
- [`MEASURE.md`](../../../skills/custom/prototype/MEASURE.md) for predeclared
  comparative measurement.

## Identity And Campaign Shape

| Role | Exact identity | Final disposition |
| --- | --- | --- |
| Frozen executable B0 | `c1a79fa3a144e1cac39be80233e1a3a2756c2f5130af14d3bc20c53418c6d307` | Preserved at [`prototype-b0/`](../../validation/evals/prototype-b0/). |
| Exact accepted C1 | `ed5832972cbd1a093656087a7efc61e679f4068b3bea330204ba6559fb78ce33` | Promoted byte-for-byte. |
| Current canonical runtime | `ed5832972cbd1a093656087a7efc61e679f4068b3bea330204ba6559fb78ce33` | Identical to accepted C1. |
| Installed runtime | `ed5832972cbd1a093656087a7efc61e679f4068b3bea330204ba6559fb78ce33` | Canonical parity proved at promotion. |
| Description pre-prune control | `22614fe625ec8ecbb176ef8af07cb4c0b186e92dee1348f9efb85be10120f668` | Frozen at [`prototype-description-pre-prune/`](../../validation/evals/prototype-description-pre-prune/). |

The closed campaign shape is `behavioral-candidate`: frozen B0 differs from
accepted C1, and current canonical runtime equals C1. Description shortening is
a separately proved pruning-equivalence change, not a C1 behavioral mechanism.

The historical aggregate `1/25` versus `25/25` result is
`historical-admission-only`. It motivated inspection but is not an exact B0
control or exact C1 contribution result.

## Sole Demonstrated Contribution

**Measure is the only behavior-changing mechanism admitted beyond B0.**

Exact B0 selected Logic for variable comparative evidence in all five controls
and never selected the required measurement branch. Exact accepted C1 selected
Measure and applied the frozen comparison rule in all five candidate samples.
`MEASURE.md` therefore owns the added behavior:

- compare predeclared directions under one frozen workload;
- record the metric, unit, environment, warmup and sample rules, threshold,
  confounders, variance, and worst observation when material;
- keep conditions equivalent across directions;
- apply only the frozen verdict rule; and
- return a bounded design result without claiming a production baseline, SLO,
  or diagnosis.

All other retained differences are B0-equivalent wording, mandatory local
authority or safety contracts, or pruning. They receive no contribution
credit.

## Ownership And Relationships

| Concern | Owner |
| --- | --- |
| Question, Freeze, authorized probe effects, branch Smoke, supported result, reconciliation, and truthful Return | Prototype |
| Material thresholds, priorities, adoption, later routing, durable truth, production implementation, and production proof | Current caller or user |
| Decision authority | Named decision owner supplied at Freeze |
| Human-reserved judgment | Named human judge; never inferred from decision ownership or replaced by a proxy |
| Logic, UI, and Measure mechanics | Their disclosed branch files |
| Wayfinder participation | Wayfinder passes decision owner, claim level, judgment mode, and human judge when applicable, then receives the supported result, evidence, limits, and cleanup state |
| Improve Codebase participation | Improve Codebase supplies the complete Freeze authority and receives design evidence without treating it as production proof |

The canonical relationship map is
[`skill-context-relationships.md`](../skill-context-relationships.md).
Prototype has no outbound Handoff or Domain Modeling recommendation. It
returns directly to its current caller or the user and never selects or invokes
a downstream route.

## Protected Contracts

These contracts are part of the promoted minimum and remain protected even
though most were not behavior-changing C1 mechanisms:

| Contract | Protected meaning |
| --- | --- |
| One-question fit | One bounded runnable-evidence question may compare alternatives; multiple independent evidence needs return as separate questions. |
| Mutation-before-Freeze guard | Prototype does not mutate until every material authority, evidence, path, effect, and finite-bound fact is known. |
| Claim and judgment authority | `claim level: shape/feel | design evidence` and `judgment mode: human | rule-based` remain compatible with callers; `shape/feel` requires human judgment. |
| Independent roles | Decision owner and human judge are separate authorities and are never inferred from one another. |
| Branch isolation | One decision-bearing Logic, UI, or Measure contract loads; branch files do not own Reconcile or Return. |
| Evidence boundary | Smoke proves that the probe runs and is judgeable; the verdict answers only the frozen question; production proof remains elsewhere. |
| Artifact authority | Disposable work defaults to one invocation-owned `.tmp/prototype/<question-slug>/`; app-tree and durable paths require explicit authority and positive isolation. |
| Safe reconciliation | Every artifact receives `delete`, `restore`, `preserve-for-verdict`, or `authorized-durable-evidence`; concurrent work is preserved and no terminal Return leaves a live resource. |
| Fresh continuation | A retained artifact is re-frozen as a current invocation with current identity and authority; stale packet state is not trusted. |
| Direct Return | Every result or residual goes to the current caller or user without inherited caller identity or downstream execution. |
| Production separation | Prototype code, tests, metrics, visual acceptance, and successful startup are never promoted into production authority. |

The protected behavior set was exercised across representative Logic, UI,
Measure, cleanup, continuation, and caller-return cases. Exact outcomes and
limits live in the acceptance record rather than here.

## Rejected And Demoted Mechanisms

The following campaign mechanisms were rejected after exact B0 showed no
failure. They are not latent future work:

| Mechanism | Final disposition |
| --- | --- |
| Four-predicate Admit expansion | Removed; compact Fit preserves the required distinction. |
| Five-lock Freeze presentation | Removed; flat minimum Freeze is sufficient. |
| Exact four-packet schema | Removed; Return includes only applicable truthful facts. |
| Three named proof levels | Removed; the Smoke, verdict, and production boundary remains without the taxonomy. |
| Awaiting-only packet-backed Resume and `RESUME.md` | Removed; continued evidence is safely re-frozen as a current invocation. |
| Strong exactly-one wording | Demoted to compact branch context control. |
| Claim, mode, and role labels as a contribution claim | Retained only as deterministic caller-compatibility and authority contracts. |
| Four artifact dispositions as a contribution claim | Retained only as a mandatory deterministic safety contract. |
| Outbound `$handoff` and `$domain-modeling` recommendations | Removed; direct current-caller Return is authoritative. |

The design also rejects multi-question campaigns, automatic downstream
continuation, promotion of the winning probe, a generic all-purpose branch,
default tracked application mutation, production-proof claims, and
Wayfinder-style ledgers or correction generations. Disposable assertions and
case drivers remain allowed when they improve prototype evidence; production
test mutation remains outside Prototype authority.

## Proof

The authoritative closeout is
[`2026-07-22-prototype-b0-first-acceptance.md`](../../validation/transcripts/2026-07-22-prototype-b0-first-acceptance.md).
It records exact hashes, B0-first contribution controls, accepted C1 behavior,
description-pruning equivalence, deterministic and live probes, caller and
relationship checks, promotion, installation scope, and installed parity.

Supporting immutable evidence:

- [`prototype-b0/`](../../validation/evals/prototype-b0/) — executable B0;
- [`prototype-description-pre-prune/`](../../validation/evals/prototype-description-pre-prune/)
  — behavior-complete longer-description control;
- [`prototype-prompt4/`](../../validation/evals/prototype-prompt4/) — fixed
  protocols and live Logic, UI, Measure, and cleanup probes; and
- [`2026-07-22-prototype-b0-c1-construction-evidence.md`](../../validation/transcripts/2026-07-22-prototype-b0-c1-construction-evidence.md)
  — package provenance and the pre-evaluation construction ledger. Its
  superseded candidate identity and future Prompt 4 instructions are
  historical only; the acceptance record governs final decisions.

Accepted proof established:

- exact B0-first contribution for Measure;
- `45/45` representative final-package cases with no observed critical failure;
- `5/5` exact Measure contribution cases;
- `45/45` in both description pre-prune and shortened-description arms;
- live Logic, UI, Measure, cleanup, continuation, and caller-return behavior;
- deterministic authority, safety, inventory, relationship, and absence
  contracts; and
- exact canonical-to-installed parity for the affected cohort.

## Residual Gaps And Limits

No residual gap blocks the promoted design.

- Behavioral evidence is bounded to the recorded tasks, package bytes,
  protocols, runtime, and rubrics; it does not establish universal behavior.
- Measure evidence is design evidence under a frozen local workload, not a
  production performance baseline, SLO, or diagnosis.
- Description testing proves equivalence across the registered request
  families, not host-level discovery telemetry or universal invocation recall.
- Human-reserved shape and feel remains unresolved when the named judge is
  unavailable; truthful Return and safe artifact reconciliation are the
  supported result in that case.
- Promotion and installed parity are historical closeout facts from the linked
  record. A future runtime change requires fresh proportionate proof and normal
  installation ownership.

Prototype has no open extraction, evaluation, promotion, installation, or Git
delivery unit. Future work begins only from a new decision-changing request.
