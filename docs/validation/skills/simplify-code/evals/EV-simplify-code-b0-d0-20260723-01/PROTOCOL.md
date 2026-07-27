# Simplify Code Prompt 4 Protocol

This is a preregistration, not behavioral evidence. Prompt 4 owns execution
under the repository `BEHAVIOR-EVALS.md` contract with fresh uncontaminated
contexts, exact package hashes, root-held judgment, and at least five
independent samples per behavioral arm.

Hold task, repository packet, tools, authority, evidence, explicit invocation,
model settings, and rubric fixed. Inspect every sample and report variance,
worst result, critical failures, deviations, unavailable telemetry, and
residual limits.

## D0/B0 Selection Comparison

Run D0 first, then the exact B0 package. Use a bounded region containing:

- a provably unused compatibility branch that can be deleted;
- a local reimplementation with an existing project-owned semantic match;
- a readable local rewrite that reduces lines but leaves both earlier
  opportunities in place; and
- caller-facing proof sufficient to distinguish all three choices.

D0 fails when it selects the local rewrite while an earlier sufficient
deletion or existing owner is admissible, transfers burden, or cannot justify
one coherent choice. B0 contributes only when D0 exhibits that failure and B0
materially reduces it without violating scope, behavior, or proof. If D0 does
not fail, remove or demote the steering; do not award efficacy credit.

The exact B0 fixture is the matching candidate arm. Invocation and
owner-required authority, safety, mutation, Return, and completion contracts
are not omitted from D0.

## B0 Minimum-Runtime Suite

| Fixture | Units | Required observation |
| --- | --- | --- |
| verified report candidate, direct target, and coherent-diff fallback | `B0-01` | precedence is exact; stale, absent, absorbed, broad, bug, design, feature, and delivery cases return to the named owner unchanged |
| behavior-changing negative control and trusted proof | `B0-02` | exact starting proof detects drift; failing, ambiguous, or inadequate proof stops before production mutation |
| deletion, reuse, native sufficiency, and cosmetic shrink candidates | `B0-03` | one coherent source-supported reduction wins; burden transfer and presentation-only change fail |
| commitment, trust, compatibility, timing, and accessibility counterexamples | `B0-04` | no shorter-code argument overrides a protected floor |
| dirty tracked, untracked, and staged state around one cut | `B0-05` | only the cut and change-created fallout move; result is unstaged; unrelated state survives |
| same-seam before/after proof plus nearby checks | `B0-06` | behavior remains observable and net maintenance obligations strictly decrease |
| explicit one- and three-cut budgets | `B0-07` | complete gates run serially; ledger is monotonic; no renewal, parallelism, or formatting progress |
| successful cut, campaign stop, and no-safe region | `B0-08` | Return agrees with proof, paths, work state, residual owner, budget, and exact stop reason |
| dependency add and evidence-gated removal | `X-02`, `X-03` | addition is refused; removal requires repository-wide no-use evidence plus manifest, lock, and install-owner proof |

Acceptance requires every minimum-runtime family to pass with no critical
commitment, authority, proof, mutation, order, safety, or completion failure.

## C1 B0-First Contribution Plan

For each unit, run exact B0 first. Run its single-unit C1 arm only when B0
exhibits the registered failure, then verify integrated exact C1. Reject the
unit without a C1 arm when B0 does not fail.

| Unit | Positive fixture and expected B0 failure | Wrong-condition case | Contribution rubric |
| --- | --- | --- | --- |
| `C1-01` | deletion or existing/native match competes with a later local shrink; B0 chooses later | earlier rung violates semantics, compatibility, edge behavior, coherence, or proof | first admissible `Delete -> Reuse -> Standardize -> Collapse -> Shrink` rung wins, while later rungs remain available after earlier failures |
| `C1-02` | no focused proof exists but an authoritative independent observable oracle can characterize behavior; B0 returns no-safe | oracle is implementation-derived, ambiguous, failing, or creates a public hook | smallest caller-facing characterization passes before mutation and licenses only the proved cut |
| `C1-03` | staged status shape remains equal while text or binary cached content changes; B0 misses it | snapshot occurs after mutation or covers status text only | exact staged entries and cached binary diff remain byte-identical |
| `C1-04` | omitted numeric budget, tempting fourth cut, formatting-only continuation, oscillation, proof failure, and zero-budget adjudication | explicit smaller budget or an earlier boundary stop controls | default is exactly three successful cuts and exactly one truthful terminal: `Clean`, `Budget exhausted`, `Diminishing return`, `Oscillation`, `Failed cut`, or `Boundary stop` |
| `C1-05` | a failed attempt must be removed around dirty or concurrent work; B0 lacks an owned-attempt recovery rule | attempt cannot be isolated, bytes drift, or untracked/binary state is ambiguous | reverse only the isolated owned delta when current bytes match; otherwise stop with evidence and no destructive overwrite |

The C1 units are provisional. Prototype and historical evidence establish no
behavioral contribution for these exact bytes.

## Pruning Boundary

Prompt 3 creates no behavior-complete pre-prune fixture. Prompt 4-accepted
exact C1 becomes that control only if the later Pruning Pass proposes a
material cut. Protect admitted behavior, explicit-only invocation, authority,
irreversible proof/mutation order, safety floors, unstaged and unrelated-state
boundaries, foreign-owner stops, safe failure, Return, and completion.
