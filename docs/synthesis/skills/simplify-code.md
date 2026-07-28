# Simplify Code Runtime Synthesis

## Current Decision

Status: Author-reconciled on 2026-07-27 after the historical Deploy Campaign.
The canonical runtime remains explicit-only. It accepts only a user-selected
Audit candidate or user-named target, makes one unstaged behavior-preserving
cut by default, and returns exactly `simplified`, `no-safe-simplification`, or
`blocked`. An explicit `until-clean` mode may run a finite serial campaign
inside one named region.

Canonical package identity:

- package: `skills/custom/simplify-code`;
- inventory: `SKILL.md`, `agents/openai.yaml`;
- tree SHA-256:
  `16d5a9b617150aef3fa3a9b443b1ec35ce0f6a972bcf4903968b84d94cdad208`;
- `SKILL.md` SHA-256:
  `1b8bb83eb2355d6a476b5ca7e31710e9bd5de8bd4ecab9142940f51f740a45db`;
- `agents/openai.yaml` SHA-256:
  `961e1d3de8909b6eff7d2f9bd4a94936c6206cb5e9354632595867a43608d3f9`.

The hashes and evaluations below are historical evidence for earlier bytes;
they do not prove the current wording. No installed synchronization is
claimed for this Author pass.

## Current Runtime Contract

The common path has five units:

1. **Bound.** Accept only the exact selected target, trace its commitments and
   Proof Seam, and return missing, invalid, stale, or foreign work as
   `blocked`.
2. **Baseline.** Record work state and run the smallest trusted before proof.
   Inadequate proof blocks mutation and cannot support a no-safe verdict.
3. **Reduce.** Inspect the selected Audit direction in default mode or
   `Delete -> Reuse -> Standardize, native-first -> Collapse -> Shrink` for
   other targets and `until-clean`; take the first safe cut and preserve the
   Engineering Contract safety floor.
4. **Prove.** Rerun the seam and proportionate checks, establish a strict
   reduction in maintenance obligations, and preserve the index and unrelated
   work.
5. **Return.** Reconcile evidence under one typed outcome and leave the result
   unstaged.

The irreversible order is:

```text
Bound -> Baseline -> Reduce -> Prove -> Return
```

Campaign mode repeats only `Baseline -> Reduce -> Prove` under one named
region, invariant contract, Proof Seam, finite budget, monotonic ledger, and
the six established terminal classifications.

## Historical Source And Decision Basis

The source-first checkpoint was frozen before the previous canonical runtime
or synthesis conclusions were opened:

```text
checkpoint SHA-256:
76300e21e94700b0a702be25a1f0a36071188380da3e51ef814152b6239028e8

intent manifest SHA-256:
ee19da0dc1117e4b096f0de7c53fa7ec819a440c52f4472412f760065ddc62a8

source manifest SHA-256:
3477ae076ceef1f527e9c1162da2172ead4f07603582ecdd9c2353d35e16bd74
```

| Source | Exact identity | Accepted pressure and limit |
| --- | --- | --- |
| Matt Pocock Skills | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | Bounded engineering and proof vocabulary only; no direct simplification executor or efficacy claim. |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99` | Before/after verification pressure only; it does not set the local runtime contract. |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` | Ordered elimination, reuse, native capability, deletion, and safety floors; persistent modes, scoring, volume pressure, and wholesale package behavior were not adopted. |
| Local intent authorities | Intent manifest above | Invocation, outcome, authority, mutation, Return, completion, routes, and protected safety behavior. |
| Previous canonical runtime | Tree `030c31bf4f880f1d0c66005482ff6aa7b4382bd301dd491563491fd195964054` | Compatibility inventory and C1 origins only; presence did not establish protection or efficacy. |

No network refresh was performed. These identities describe the inspected
local revisions, not later remote state.

## Historical Candidate Decisions

| Unit | Origin | Registered B0 failure | Decision and promoted effect |
| --- | --- | --- | --- |
| `C1-01` ordered selection | source mechanism | A later local move can beat an admissible deletion or existing owner. | `accepted`; B0 complied 3/5 with two later-rung choices, while C1 complied 5/5 with one observed choice. |
| `C1-02` characterization support | current retention | B0 might refuse a cut despite an independent observable oracle. | `rejected-no-control-failure`; B0 licensed the valid oracle and refused the wrong condition 10/10. |
| `C1-03` exact index identity wording | current retention and safety | B0 might accept equal status shape despite changed staged bytes. | `rejected-no-control-failure`; B0 refused equal-status drift and inadequate late snapshots 10/10. The work-state outcome remains protected. |
| `C1-04` default budget and terminals | intent counterexample | Omitted budget and terminal distinctions vary or permit unbounded continuation. | `accepted`; B0 failed the omitted-budget claim 5/5, while C1 used default three and all six terminals correctly 5/5. |
| `C1-05` attempt-owned recovery | intent counterexample | Failure recovery might overwrite pre-existing or concurrent work. | `rejected-no-control-failure`; B0 handled the isolated and refusal cases 25/25. The non-destructive outcome remains protected. |

Prompt 4 also removed an unproven B0 sentence preferring source-supported
deletion or an already-sufficient owner/native capability: D0 and rebuilt B0
both selected deletion 5/5, with no variance benefit. The independently
required coherence, proof, safety, strict-reduction, and work-state gates
remain.

The Pruning Pass classified every instruction-bearing passage exactly once.
No passage qualified for collapse, disclosure, or deletion without removing
protected meaning or changing exact accepted behavior. Its disposition was
`pruning-not-needed`.

## Current Relationships And Ownership

| Caller or owner | Relationship | Trigger and Return |
| --- | --- | --- |
| Human | Invoke | Explicitly names Simplify Code and an exact target; names `until-clean` and optionally a finite budget for campaign mode; receives an unstaged typed result. |
| `$skill-router` | Recommend and stop | Selects one bounded behavior-preserving simplification. |
| `$tdd` | Recommend and stop | Settled GREEN work exposes separate bounded cleanup. |
| `$audit-codebase` | Recommend and stop | A user selects an analyzed bounded behavior-preserving reduction with current report identity, supported behavior, Source Trace, and Proof Seam. |
| Simplify Code | Recommend and stop | Repository mapping, wide discovery, or multi-subsystem audit coverage goes to Audit Codebase. |
| Simplify Code | Return and stop | Uncertain bug facts go to Diagnosing Bugs; feature, public-contract, review, Git, tracker, installation, and external work return to their owners. |

Relationship topology is unchanged by this Author pass. A required new
Interface, dependency direction, Proof Seam, or ownership decision returns to
the caller as a design gap; Simplify Code does not add a design-workflow step.
The provider prompt now requires an explicitly selected target; the
explicit-only policy is unchanged.

## Historical Exact Proof

The accepted behavior record is
[2026-07-23-simplify-code-behavior-eval.md](../../validation/skills/simplify-code/evals/EV-simplify-code-behavior-eval-20260723-01/evidence/2026-07-23-simplify-code-behavior-eval.md).
It owns the fixed protocol, raw-output pointers, sample judgments, variance,
worst results, deviations, and telemetry limits. The pruning record is
[2026-07-23-simplify-code-pruning.md](../../validation/skills/simplify-code/evals/EV-simplify-code-pruning-20260723-01/evidence/2026-07-23-simplify-code-pruning.md).

Exact identities:

| Package | Tree SHA-256 | Role |
| --- | --- | --- |
| Previous canonical | `030c31bf4f880f1d0c66005482ff6aa7b4382bd301dd491563491fd195964054` | Compatibility inventory |
| Final B0 and D0 | `54aac31397e2a5ab10daf78420906a24459622f144631e0c61e8e02888acd434` | Viable minimum and no-guidance control |
| Promoted canonical C1 | `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06` | Accepted final runtime |
| Current Author bytes | `16d5a9b617150aef3fa3a9b443b1ec35ce0f6a972bcf4903968b84d94cdad208` | Current canonical runtime; structural proof only |

Five fresh integrated C1 samples passed all protected B0 families, ordered
selection, default and explicit budgets, all six terminals, work-state and
dependency boundaries, and explicit-only invocation. Aggregate: 5/5; zero
outcome variance; worst result passed; zero protected-behavior regressions or
critical failures.

This lane used read-only synthetic action decisions. It does not prove live
source mutation, real concurrent interleaving, arbitrary tasks or hosts, or
later model/runtime builds.

## Current Deliberate Non-Changes And Residuals

Deliberately unchanged: explicit-only and unstaged operation; relationship
topology; the five-rung ladder; safety and dependency-removal floors; the
finite serial campaign; and the absence of automation, scoring, parallel cuts,
whole-tree cleanup, downstream execution, Git delivery, or tracker mutation.

Residual evidence gaps are a fresh wording-efficacy evaluation, live
filesystem mutation and concurrent-interleaving proof, generalization beyond
the historical fixed packets, and installed-package parity for the current
bytes.

## Historical Lifecycle

| Unit | Current epoch state |
| --- | --- |
| Prompt 1 | Passed; source-first checkpoint frozen. |
| Prompt 2 | Passed; decision-complete synthesis recorded. |
| Prompt 3 | Passed; B0, D0, and C1 constructed with exact identities. |
| Prompt 4 | Accepted; B0 viable, `C1-01` and `C1-04` accepted, three hypotheses rejected without control failure. |
| Pruning Pass | Complete; `pruning-not-needed`; exact C1 retained byte-identically. |
| Prompt 5 canonical phase | Passed; exact C1 promoted and canonical proof completed. |
| Prompt 5 installation phase | Recorded in the promotion/install transcript after managed parity proof. |
| Git delivery | Bare mode; pending and outside Prompt 5. |
