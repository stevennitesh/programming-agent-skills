# Prototype Description Pruning Evaluation

Date: 2026-07-21

## Decision

**Accept metadata equivalence** for current inactive candidate hash
`4d9ca65a05d5b174b8eefbbc9396f00020ce267932b628415004575e03ff329d`.
The shortened description matched the prior accepted description on every fixed
positive and adjacent-negative invocation decision. This is not promotion or
platform-level auto-discovery proof.

## Fixed Inputs

- Control hash: `efe81189617f7a179d7ba00639c5f64b2e98a606b76049f0131dacaad99e0d85`
- Candidate hash: `4d9ca65a05d5b174b8eefbbc9396f00020ce267932b628415004575e03ff329d`
- Control description: `Answer one bounded design question with a disposable
  runnable probe. Use for logic, state, data, API or interface shape,
  structurally different UI bets, or predeclared comparative measurement. Not
  for production proof, uncertain defect diagnosis, or multi-decision design.`
- Candidate description: `Prototype one bounded design question with a
  disposable runnable probe; exclude production proof, uncertain defects, and
  multi-decision design.`
- Policy in both arms: `allow_implicit_invocation: true`

The nine fixed request families were bounded Logic, structural UI, predeclared
comparative Measure, production implementation, uncertain defect diagnosis,
source research, multi-decision design, ordinary one-number measurement, and
incidental `Prototype` naming.

## Runtime And Rubric

- Runtime: Codex desktop fresh-context direct collaboration agents.
- Context: `fork_turns="none"`; no model or reasoning override.
- Samples: five independent control contexts and five independent candidate
  contexts; each classified all nine requests from metadata only.
- Authority: read-only; no tools, files, procedure body, peer results, or
  opposite-arm wording were available to a sample.
- Pass: invoke all three bounded design-probe positives and reject all six
  adjacent negatives.
- Critical failure: miss a positive or capture an adjacent negative.

## Results

| Arm | Sample 1 | Sample 2 | Sample 3 | Sample 4 | Sample 5 | Aggregate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Prior description | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 45/45 |
| Shortened description | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 45/45 |

Variance was zero, the worst result was 9/9 in both arms, and no critical
failure occurred. Every sample invoked Logic, structural UI, and comparative
Measure, then rejected production work, uncertain diagnosis, research,
multi-decision design, ordinary measurement, and incidental naming.

## Limits

Exact model identifier, reasoning mode, token count, and per-sample timing were
unavailable. This simulation proves equivalence on the fixed metadata-routing
cases; it does not prove host discovery, exhaustive paraphrase robustness, or
any procedure-body behavior.
