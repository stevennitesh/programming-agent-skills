# Selected Improvement Candidate

Use this branch only when the invocation explicitly names `Candidate N` and its verified improvement report. [`SKILL.md`](SKILL.md) owns the survey vocabulary and mutation boundary.

**Reopen -> Verify -> Resolve -> Reclassify -> Route -> Reconcile -> Return.**

## Reopen

Read the named report and locate exactly one stable candidate. Reuse its Source Trace, survey bound, disposition, proof seam, uncertainty, and sequence relationship. When the report or candidate is ambiguous, return the exact missing pointer and stop. Do not repeat the Survey.

## Verify

Refresh repo and work state, then verify the candidate's load-bearing evidence against current source, callers, tests, history, domain context, and constraints. Record material drift. Continue only when the candidate remains inside the surveyed bound; otherwise return a stale-candidate packet and recommend a new `$improve-codebase` survey.

## Resolve

Resolve at most one decision-blocking uncertainty at a time:

- **Repository trace:** inspect the missing source, caller, test, history, or configuration evidence directly.
- **Source:** invoke `$research` with one source question, the decision it supports, scope, freshness, and `authorized note path: none` unless the user approved exactly one path. Receive cited inline evidence, one authorized note pointer, or a blocker.
- **Runnable:** invoke `$prototype` with one terminal question, judgment authority, objective criteria when applicable, and a disposable path under `.tmp/improvement-prototypes/`. App-tree or durable prototype paths require explicit authority. Receive its reconciled verdict and cleanup state; treat it as design evidence, never production proof.
- **User decision:** invoke `$grill-with-docs` only when a public commitment, accepted trade-off, domain term, or ADR question requires the user's judgment. Receive its complete exit packet and stop on `Evidence gap`.
- **Design:** invoke `$codebase-design` only when a supported `Concentrate` candidate still needs dependency, seam, ownership, interface, migration, or replacement design. Receive its design packet.

## Reclassify

Apply the deletion test again with the returned evidence or decision. Set the final disposition to `Eliminate`, `Concentrate`, `Retain`, or `Investigate`. A design recommendation to merge, inline, or keep the current shape may change the original disposition. Preserve unresolved conflict as `Investigate`; do not force a route.

## Route

Choose one terminal route:

- **Eliminate:** recommend `$simplify-code Candidate N from <absolute-report-path>` and stop before edits.
- **Concentrate, single-slice:** recommend `$implement` when the direction, commitment boundary, and proof are ready for one bounded slice.
- **Concentrate, multi-slice:** recommend `$to-tickets` when a settled direction needs dependency-ordered slices.
- **Concentrate, underspecified:** recommend `$to-spec` when intent, acceptance, architecture, migration, or validation remains unresolved.
- **Retain:** return a no-change verdict with the evidence that the current boundary earns its cost.
- **Investigate:** return the exact evidence gap, attempted resolver, result, and next evidence action; start no downstream skill.

Account for `Preparatory`, `Absorbed`, and `Residual` relationships before routing so the recommendation does not duplicate another candidate's work.

## Reconcile

Update the same report's selected card and Resolution section with the resolver, returned evidence or decision, final disposition, route, and resolution time. Preserve candidate IDs and omit stale prototype paths. Reread and verify the report under [HTML-REPORT.md](HTML-REPORT.md).

## Return

Return one improvement packet containing:

- absolute report path, candidate ID, survey bound, and Source Trace;
- original and final dispositions with deletion-test result;
- resolver packet or direct evidence, including uncertainty and limits;
- sequence relationship and overlap decision;
- recommended route and exact pickup, or no-change/evidence-gap verdict;
- report verification and confirmation that downstream work remains unstarted.

## Completion

Complete only when the named candidate was reopened without resurveying; current evidence was verified; each invoked resolver stayed within its authority and returned to this caller; the candidate was reclassified; sequencing was honored; the report was reconciled and reverified; exactly one terminal route or verdict was returned; and product, tracker, index, commit, external, and unrelated state remained unchanged.
