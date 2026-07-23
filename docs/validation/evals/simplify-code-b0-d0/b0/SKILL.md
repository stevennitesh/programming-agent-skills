---
name: simplify-code
description: Simplify one bounded existing-code target without changing behavior, or run a finite serial until-clean campaign in one named region. Use only when explicitly invoked; exclude features, uncertain bugs, public-contract changes, wide discovery, and new interface or ownership design.
---

# Simplify Code

Own one outcome: one unstaged, behavior-preserving reduction in total
maintenance obligations; an explicitly requested finite serial `until-clean`
campaign inside one named region; or a fully accounted **No safe
simplification** result.

**Admit -> Trace -> Baseline -> Choose -> Cut -> Prove -> Lock.**

## Admit

Accept one bounded target by this precedence: a still-valid candidate from a
verified `$improve-codebase` report, the user-named target, then one coherent
current diff. Return a missing, stale, absorbed, or incomplete report to
Improve Codebase unchanged. Without a bounded target, recommend
`$improve-codebase` and stop.

Return feature work, public-contract decisions, reviews, Git delivery, tracker
mutation, installation, and external-system work to their owners. Return
uncertain symptoms or causes to `$diagnosing-bugs`. Return a new interface,
dependency direction, proof seam, or ownership decision to
`$codebase-design`. Stop before copying a foreign owner's procedure.

The user owns the target, mode, budget, and commitment decisions. Simplify Code
owns selection, local edits, proof, and Return only inside the admitted region.

## Trace And Baseline

Read the repository instructions and authoritative behavior, domain, and
compatibility commitments. Trace operational callers, callees, entries,
configuration, registration paths, relevant work state, and one caller-facing
proof seam.

Record the starting ref, status, relevant diff, and staged-state shape without
disturbing existing work. Run the smallest trusted proof that can detect a
behavior change against the exact starting state. A failing, ambiguous, or
semantically inadequate baseline cannot authorize production mutation; return
**No safe simplification** with the exact proof gap.

## Choose

Select one coherent candidate
only when:

- preserved behavior and its proof seam are explicit;
- the cut fits the admitted region and needs no new commitment;
- caller and maintainer burden strictly decreases; and
- the proof and work-state boundaries are credible.

Preserve product intent, accepted behavior, public and data contracts, domain
decisions, trust-boundary validation, data-loss controls, security, privacy,
accessibility, concurrency, durability, ordering, timing, and required
compatibility. Simplicity never overrides one of these floors.

Do not add a dependency. Remove one only after repository-wide source,
configuration, and runtime-entry evidence proves no use remains, then
reconcile its manifest, lockfile, and repository-owned installation proof.

If no candidate passes, return **No safe simplification** with the bounded
region, credible candidates, rejection reasons, work state, proof or proof
gap, and owning residual.

## Cut

Make one bounded unstaged cut. Remove only fallout created by that cut:
imports, helpers, files, configuration, dependencies, and implementation-detail
tests displaced by stronger caller-facing proof. Preserve correct behavior
proof, pre-existing dead work, unrelated work, the index, trackers, installed
state, and external state.

## Prove And Lock

Rerun the same focused proof, then the nearest relevant tests and
proportionate repository checks. Establish a strict net reduction across
concepts, branch families, coordination, indirection, file responsibilities,
dependencies, callers, tests, configuration, and operations. Counts are
receipts, not correctness or productivity proof; a shorter patch that transfers
burden is not simpler.

Refresh changed paths and work state after proof. Confirm the patch preserves
commitments, changes only the admitted cut and its created fallout, keeps the
index and unrelated state as found, and leaves no invocation-created
artifacts.

## Until Clean

Enter only when the user explicitly requests `until-clean`, names one region,
and holds a finite positive successful-cut budget. Hold one invariant behavior
contract and proof seam. Run the complete gate serially for one cut at a time:

`Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`

After each successful Lock, record the removed and introduced maintenance
obligations, decrement the budget, and use the proved result as the next
starting state. Continue only while the ledger shows a strict monotonic
reduction. Stop on budget exhaustion, no admissible cut, proof failure, drift,
oscillation, or a boundary owned elsewhere. Do not widen or parallelize the
region, renew the budget, or count formatting and presentation-only changes as
progress.

## Return And Completion

Return the mode and region; cut or **No safe simplification** result; net
obligation reduction; preserved contract and observable seam; before and after
proof; changed paths; starting and ending work state; campaign budget and
ledger when applicable; rejected or deferred candidates; exact stop reason;
residual owner; and skipped proof or risk. The result remains unstaged.

Complete only when the admitted region, callers, commitments, proof seam,
starting state, candidate accounting, after proof, net reduction, changed
paths, index and unrelated-state preservation, residuals, and selected outcome
all agree with current evidence. A campaign additionally requires its finite
budget, serial successful-cut ledger, and truthful terminal reason.
