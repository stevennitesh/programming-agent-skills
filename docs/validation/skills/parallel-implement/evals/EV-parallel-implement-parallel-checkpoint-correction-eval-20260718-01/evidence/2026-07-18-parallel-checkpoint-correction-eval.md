# Parallel Checkpoint And Integration Correction Behavior Eval

## Setup

- Date: 2026-07-18
- Runtime: GPT-5 fresh-context read-only agents; model settings and token telemetry were not exposed
- Candidate skill SHA-256: `057dde9a239a0a5eb5723d5e1d948597f4ac8d16a83ae9305075b9372147bc7d`
- Control: committed `HEAD` versions of `parallel-implement/SKILL.md`, `RUN-LEDGER.md`, and `CODEX-WORKTREE-LAUNCH.md`
- Candidate: current working-tree versions of the same surfaces plus `run_ledger.py`
- Samples: five independent control contexts; five conforming candidate contexts after one candidate sample exposed and triggered repair of the open-regression checkpoint branch
- Mutations by samples: none

## Scenario

All worker commits had landed when broad loop-close proof reproduced a semantic regression before formal review. The caller bounded the current run but expected the same event stream to resume. Retained tracker claims, a shared Python virtualenv capable of importing the main checkout, xdist-sensitive startup, and successful Windows extended-path cleanup were included.

## Rubric

One point per required behavior:

1. Uses a dedicated nonterminal checkpoint rather than terminal partial Release or an improvised event.
2. Records pre-review regression authority and advances canonical integration HEAD through a proved correction.
3. Accounts for retained or released claims with exact recovery evidence.
4. Requires explicit lane-local project resolution and deterministic serial startup.
5. Classifies successful extended-path cleanup as `removed` while preserving fallback diagnostics.

A critical failure is any unmodeled resumable state, mutation without correction authority, stale integration HEAD, resume without reconciliation, or forced correction beyond the caller's bounded stop.

## Control

All five controls recognized that `release: partial` was terminal and avoided it, but the baseline gave them no valid outcome event. They stopped on `frontier`, `wave-validation`, or an open stream and described the campaign as `draining`. None could name an executable correction event that advanced canonical integration HEAD. Claim recovery fields and deterministic serial startup were inconsistent. All five independently protected import provenance and classified successful cleanup as `removed`.

- Score: `10/25`
- Critical failures: `5/5` used an unmodeled resumable outcome and lacked executable integration-correction authority
- Variance: low; every control converged on the same workaround

## Candidate

Four initial candidate samples used runtime-contract-3 checkpoint, explicit correction authority, successor HEAD, claim recovery fields, serial startup, lane-local imports, and normalized cleanup. One sample correctly detected that the first reducer draft rejected a bounded `blocked` checkpoint while its named integration regression remained open. That branch was repaired and covered by a RED/GREEN helper test. A fresh replacement sample then verified the final contract permits:

`integration-regression -> checkpoint(blocked) -> resume -> reconcile -> correct-integration -> integration-correction -> graph-drained -> review-ready`

The other valid branch—correct first, then `checkpoint(partial)`—remained accepted.

- Final score: `25/25`
- Critical failures after repair: `0/5`
- Variance: bounded to the caller's stop location; both allowed branches preserve the same authority model

## Result

The candidate materially removes the observed authority gaps and narrows variance. Static helper tests protect event semantics and output shape. This sample did not demonstrate incremental behavioral value for import-provenance wording because every control already handled the explicitly stated import risk; that wording remains conditional operational reference backed by the real-run failure, not a claimed counterfactual uplift.

Residual gap: the behavior fixture is synthetic and read-only. The next real campaign should retain its rendered checkpoint and correction packets as operational evidence.
