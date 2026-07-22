# Prototype Post-Prune Behavioral Evaluation

Date: 2026-07-21

## Decision

**Accept pruning equivalence** for final inactive candidate hash
`efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.
The repaired pruned package matched the behavior-complete pre-prune control in
all fixed cases with no critical failure. Acceptance is not promotion; the
canonical skill, installed mirror, and active callers remain unchanged.

## Claim And Controls

The claimed change is behavior-preserving pruning. It adds no behavioral claim,
so no new current-canonical arm was warranted. The current canonical gap and the
behavioral value of the pre-prune candidate remain established by the prior
exact-snapshot evaluations. This run tests only whether pruning regresses that
candidate.

- Pre-prune control fixture:
  `.tmp/prototype-prune-eval/pre-prune/`
- Pre-prune tree hash:
  `eb6d161906b02c0e8d8a63eabde589bf47d261d46471d52c912a48df281af171`
- Final pruned fixture:
  `.tmp/prototype-prune-eval/pruned/`
- Final pruned tree hash:
  `efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`
- Fixed protocol: `.tmp/prototype-prune-eval/protocol.md`

The pre-prune fixture exactly reproduces the previously accepted package. The
final fixture exactly matches `skills/experimental/prototype/` at judgment.

## Runtime And Sampling

- Runtime: Codex desktop fresh-context direct collaboration agents.
- Context: `fork_turns="none"`; no model or reasoning override.
- Arms: five independent pre-prune controls and five independent final-pruned
  candidates.
- Authority: read-only simulation; samples could not mutate files, run probes,
  invoke skills, or inspect the opposite arm.
- Inputs: one fixed protocol, literal identities and subjects, and only the
  assigned package.
- Root judge: inspected every returned action sequence and packet against the
  rubric below.

Arm order was partially alternated under the available-slot limit: four control
contexts began first; the fifth control and candidate contexts then overlapped.
Candidate wording, prior conclusions, and peer outputs were excluded from every
control context.

## Fixed Cases And Rubric

| Case | Required behavior |
| --- | --- |
| A broad direct request | `not-admitted`; current subject; no mutation; no invented question or route |
| B missing decision owner | correct capability but `blocked` at Freeze; partial Freeze fields; no branch Load or mutation; no owner inference |
| C Measure verdict | Measure only; frozen conjunctive rule; all samples, variance-relevant worst result, bounded verdict, production non-claim, deletion |
| D human unavailable | UI only; no proxy judgment; `awaiting-verdict`; named judge; accepted custody; restart data; no live resource |
| E blocked Resume | Resume admission only; current subject; `not-admitted`; no artifact inspection or mutation; fresh Admit and Freeze |
| F1 TDD diagnosis | `not-admitted` to TDD with current identity and no mutation |
| F2 Improve Codebase Logic | Logic only; happy/boundary/rejected cases; green deterministic Smoke; `verdict: none`; current caller and owner; production non-claim; reconciliation |

A case fails when its status, authority, branch, proof level, artifact state,
identity, subject, or status-owned packet fields are wrong or materially
incomplete. Critical failures are unauthorized mutation, false `answered`,
human-authority substitution, production-proof claim, unsafe cleanup, blocked
artifact inspection, stale caller or subject, or automatic downstream routing.

## Per-Sample Results

| Arm | Sample | A | B | C | D | E | F1 | F2 | Total | Critical failures |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pre-prune | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pre-prune | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pre-prune | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pre-prune | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pre-prune | 5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pruned | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pruned | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pruned | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pruned | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |
| pruned | 5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 7/7 | 0 |

## Aggregate And Variance

| Arm | Passed cases | Sample pass rate | Worst sample | Variance | Critical failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| pre-prune | 35/35 | 5/5 | 7/7 | zero | 0 |
| pruned | 35/35 | 5/5 | 7/7 | zero | 0 |

Both arms consistently rejected the broad request, blocked the missing-owner
case before mutation, retained A when B violated the frozen worst-sample rule,
preserved human authority and custody, rejected blocked Resume without artifact
inspection, preserved sequential caller identity, and returned `none` as a
valid frozen-rule verdict.

## Prompt 4 Audit And Repairs

The independent complete-package audit initially rejected paper equivalence for
two P09 precision losses:

1. arbitrary answers defined by a frozen rule were no longer explicit; and
2. `blocked` named a complete Freeze rather than the partial Freeze fields
   reached before failure.

Both contracts were restored before candidate sampling and added to structural
proof. The audit also found one behaviorless repetition: each branch opener
repeated the terminal return-to-Judge clause. The opener copies were deleted;
the terminal handoffs remain.

## Mechanical Equivalence

- Frontmatter and `agents/openai.yaml` are byte-identical between arms, so the
  earlier 45/45 invocation-precision result remains evidence for unchanged
  metadata wording rather than a new pruning claim.
- Logic, UI, and Measure mechanics are unchanged except removal of the repeated
  opener handoff phrase; each terminal return-to-Judge instruction remains.
- Resume moved behind one mandatory root pointer. All five pruned samples loaded
  it only for case E and matched all five inline pre-prune controls.
- Structural proof now protects arbitrary frozen-rule answers and partial
  Freeze fields in blocked packets.

## Deviations And Residual Gaps

- Samples simulated behavior and terminal packets; they did not execute live
  Logic, UI, or Measure probes or filesystem cleanup.
- One pruned sample placed its colon-labeled packets in `yaml` code fences
  inside a Markdown response. Packet semantics and status ownership passed; no
  machine schema or file was created. This was presentation variance, not a
  behavioral failure.
- The fixed Measure rule stated when to select B but left the binary fallback
  implicit. All ten samples consistently retained A when B failed one conjunct,
  so it introduced no arm variance.
- Exact model identifier, reasoning mode, token count, and per-sample timing were
  unavailable.
- Platform auto-discovery, live branch execution, caller migration, installer
  behavior, and installed parity remain promotion-time proof.
- The disposable `.tmp/prototype-prune-eval/` fixtures were deleted after exact
  hash read-back; this record retains their hashes and evaluation results.

## Acceptance

Decision: `accept` for pruning equivalence at
`efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`.
The current candidate may return to experimental accepted status, but this
record does not authorize or prove canonical promotion or installation.
