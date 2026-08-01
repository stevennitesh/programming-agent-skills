---
name: simplify-code
description: Simplify one explicitly selected existing-code target without changing behavior, or run a finite serial until-clean campaign in one named region. Use only when explicitly invoked; exclude features, uncertain bugs, public-contract changes, wide discovery, and new interface or ownership design.
---

# Simplify Code

Return exactly one outcome: `simplified`, `no-safe-simplification`, or
`blocked`. Default to one unstaged, behavior-preserving cut. Run multiple cuts
only in an explicitly requested finite serial `until-clean` campaign.

**Bound -> Baseline -> Reduce -> Prove -> Return.**

## Bound

Accept only an exact `$audit-codebase` candidate selected by the user or a
user-named target. The user may name the current diff as that target; never
infer or replace the target. Verify an Audit candidate's report digest,
subsystem, current Source Trace, supported behavior, Proof Seam, and selected
behavior-preserving direction against current bytes. An invalid, stale, blocked,
disproved, or incomplete target returns `blocked` unchanged. Without a target,
return `blocked` with the exact target needed; recommend `$audit-codebase` only
when wide discovery or repository mapping is needed.

Return feature work, public-contract decisions, reviews, Git delivery, tracker
mutation, installation, and external-system work to their owners. Return
uncertain symptoms or causes to the caller as `diagnosis-required`. Return a
required new Interface, dependency direction, Proof Seam, or ownership decision
to the caller as a design gap. Stop before copying a foreign owner's procedure.

The user owns the target, mode, budget, and commitment decisions. Simplify Code
owns selection, local edits, proof, and Return only inside the admitted region.

Load the applicable repository instructions, Engineering Contract, domain
commitments, and supported compatibility. Trace the target's operational
callers, callees, entries, configuration, registration paths, work state, and
one caller-facing Proof Seam. For a valid Audit candidate, reuse its trace and
selected direction; refresh only affected evidence. In default mode, do not
repeat wide tracing or reopen the full ladder unless refreshed evidence
invalidates that direction. An `until-clean` request names its region and uses
the full ordered inspection.

## Baseline

Record the starting ref, status, relevant diff, and staged-state shape without
disturbing existing work. Run the smallest trusted proof that can detect a
behavior change against the exact starting state. A failing, ambiguous, or
semantically inadequate baseline returns `blocked` with the exact proof gap and
no production mutation. An adequate baseline is required for a
`no-safe-simplification` verdict.

## Reduce

Prefer source-supported deletion and an already-sufficient owner or native
capability over locally attractive rewriting. For an admitted Audit candidate,
choose the smallest concrete cut inside its selected reduction direction in
default mode. For other targets and each `until-clean` cycle, inspect the region
in this order. The first safe rung wins:

1. **Delete** behavior, configuration, compatibility, or abstraction proved
   unreachable, expired, or unsupported within preserved contracts.
2. **Reuse** an existing project-owned semantic match.
3. **Standardize, native-first** through standard/runtime, platform/framework,
   then already-installed dependency capability.
4. **Collapse** an unearned abstraction or duplicated decision at its
   narrowest existing owner; deepen, merge, or inline only within settled
   existing boundaries.
5. **Shrink** branching or data movement with ordinary readable constructs.

An earlier rung yields when its semantics, compatibility, edge behavior,
coherence, or proof fails. Select one coherent candidate only when:

- preserved behavior and its proof seam are explicit;
- the cut fits the admitted region and needs no new commitment;
- caller and maintainer burden strictly decreases; and
- the proof and work-state boundaries are credible.

Preserve product intent, accepted behavior, public and data contracts, domain
decisions, trust-boundary validation, data-loss controls, security, privacy,
accessibility, concurrency, durability, ordering, timing, and required
compatibility. Simplicity never overrides one of these floors.

Do not add a dependency. Remove one only after repository-wide source,
configuration, and runtime-entry evidence proves no use remains, then reconcile
its manifest, lockfile, and repository-owned installation proof.

If the complete applicable inspection finds no safe cut under an adequate
baseline, return `no-safe-simplification` with candidate rejections. The
applicable inspection is the selected Audit direction in default mode or the
full ladder for other targets and `until-clean`. Name an evidenced **Known
Ceiling** and concrete **Revisit Trigger** when supported; invent neither.

Otherwise make one bounded unstaged cut. Remove only fallout created by that
cut: imports, helpers, files, configuration, dependencies, and
implementation-detail tests displaced by stronger caller-facing proof. Preserve
correct behavior proof, unrelated work, the index, trackers, installed state,
and external state.

## Prove

Rerun the same focused proof, then the nearest relevant tests and proportionate
repository checks. Establish a strict net reduction across concepts, branch
families, coordination, indirection, file responsibilities, dependencies,
callers, tests, configuration, and operations. Counts are receipts, not
correctness or productivity proof; a shorter patch that transfers burden is not
simpler.

Refresh changed paths and work state after proof. Confirm the patch preserves
commitments, changes only the admitted cut and its created fallout, keeps the
index and unrelated state as found, and leaves no invocation-created artifacts.

If proof fails, revert only cut-created bytes that can be isolated without
touching pre-existing or concurrent work; otherwise preserve current state.
Return `blocked` with the failed proof, changed paths, work state, and exact
recovery required.

## Until Clean

Enter only when the user explicitly requests `until-clean`, names one region,
and has a finite positive successful-cut budget; use exactly `3` successful cuts
when omitted. Hold one invariant behavior contract and Proof Seam. Repeat
`Baseline -> Reduce -> Prove` serially, recording removed and introduced
maintenance obligations after each successful cut, decrementing the budget, and
using the proved result as the next baseline. Continue only while the ledger
shows strict monotonic reduction. A failed attempt consumes no successful-cut
budget.

Stop at the first applicable terminal:

1. **Clean:** one complete five-rung inspection finds no admissible cut.
2. **Budget exhausted:** no successful-cut budget remains; report eligible
   residuals.
3. **Diminishing return:** the strongest move lacks a progress unit or changes
   presentation only.
4. **Oscillation:** a move recreates, undoes, or exchanges an earlier
   obligation for an equivalent one.
5. **Failed cut:** an attempted cut fails proof; preserve current state and
   report the failed proof, work state, and owning residual.
6. **Boundary stop:** drift, proof limits, region limits, or foreign ownership
   prevents the next cut.

Do not widen or parallelize the region, renew the budget, or count formatting
and presentation-only changes as progress.

## Return

Return exactly one:

- `simplified`: cut or cuts, net obligation reduction, preserved contract and
  Proof Seam, before and after proof, changed paths, starting and ending work
  state, residuals, and any skipped proof or risk.
- `no-safe-simplification`: target, adequate baseline, complete applicable
  candidate accounting, rejection reasons, and any supported Known Ceiling
  and Revisit Trigger.
- `blocked`: missing or invalid target, drift, proof gap or failure, or foreign
  owner; include exact state, changed paths if any, and recovery or owner.

For `until-clean`, also return the initial budget, successful-cut ledger,
remaining budget, and first applicable campaign terminal. A campaign with any
proved cut returns `simplified`; one with no cut and a `Clean` terminal returns
`no-safe-simplification`; a failed or boundary stop returns `blocked`.

The result remains unstaged. Complete only when the target, commitments, Proof
Seam, candidate accounting, proof, work state, changed paths, preservation
checks, residuals, and selected outcome agree with current evidence. Start no
successor.
