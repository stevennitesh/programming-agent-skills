---
name: review
description: "Review one ordinary branch, WIP, staged, or \"review since X\" diff read-only from a fixed snapshot. Judge Standards (\"built right?\") and Spec (\"right thing?\") separately, then return one terminal report. Hand local PRs or high-risk local diffs to $convergent-pr-review; immutable repository-baseline audits belong to $audit-codebase."
---

# Review

**Route -> Pin -> Trace -> Judge -> Admit -> Return**

Read-only constrains the whole sequence. Inspect and safely verify; leave files,
Git, dependencies, trackers, PR state, external systems, and successor
snapshots unchanged.

## Route

Select exactly one owner before capture. Review owns bounded ordinary diffs.
Hand a local PR or high-risk local diff and its complete caller packet to
`$convergent-pr-review`, then stop. Recommend `$audit-codebase` for an immutable
repository-baseline audit, then stop. Run no competing ordinary pass.

Carry every caller-supplied Charter field, `Spec required`, review mode, Source
Trace, fixed point and target, required proof, and carried finding ID.

## Pin

Use the caller-supplied fixed point. Otherwise resolve the repository default
branch and merge base. Select exactly one target in this precedence:

1. supplied review tree;
2. explicitly staged-only;
3. supplied committed target;
4. live WIP.

Capture the complete target content, including in-scope untracked bytes, and
the refs, commands, status, content identities, and other identities needed to
prove exactly what was judged. Return `incomplete` when the fixed point or
target cannot be resolved, the target is empty, or any required capture
surface is missing. Judge this captured snapshot, never later live reads.

Record `Review mode: initial | remediation`; standalone Review defaults to
`initial`.

For remediation, require the original Charter, prior snapshot identity,
carried IDs, caller-owned Repair delta, remaining acceptance, fixed point, and
successor target. Judge only each carried outcome and proof, the Repair delta
and affected seams, and remaining acceptance exercised by those surfaces.
Keep IDs stable and dispose each as `resolved`, `still admitted`, `disproved`,
or `incomplete`. Leave untouched scope closed.

## Trace

Trace Spec in this precedence:

1. caller-supplied source;
2. decision-bearing material referenced by captured commits;
3. one matching repository source.

The caller supplies `Spec required: yes | no`; standalone Review defaults to
`no`. A missing, unreadable, conflicting, or unresolved required Spec makes
the review `incomplete`. When optional Spec is absent, record it as skipped;
do not infer intent from tests or implementation.

Trace Standards from repository instructions, routed guidance, test and tool
configuration, and meaningful nearby conventions. Load
[SMELL-BASELINE.md](SMELL-BASELINE.md) only when these Standards are thin.
Repository Standards override the fallback.

## Judge

Judge Standards first. Then return attention to the pinned snapshot and Spec
sources; discard the prior axis's conclusions, severity, counts, and ranking
pressure. Judge applicable Spec. Preserve each axis's own coverage and
findings.

Generate candidate observations during judgment.

## Admit

Load [FINDING-CONTRACT.md](FINDING-CONTRACT.md). Verify every candidate and
report only admitted findings.

A target's omission of contract-required proof is a potential finding under
the normal gates. Review's inability to obtain evidence required to decide a
candidate or required axis makes that coverage `incomplete`; it is not a
finding. Name unavailable optional verification as residual risk; it never
turns an unverified candidate into a finding.

## Return

Recompute every live-target identity and captured surface required to detect
drift. Drift makes the report `incomplete`; do not recapture.

Return exactly one complete or incomplete report, then stop. `complete` means
review coverage closed; it is not release acceptance.

A complete report records:

```text
Review status: complete
Review mode: initial | remediation
Fixed point:
Snapshot identity:
Target:
Sources: Standards: <sources>. Spec: <source or skipped>.
Standards findings: <admitted findings or none>
Spec findings: <admitted findings, none, or skipped>
Carried dispositions: <when applicable>
Axis summary: Standards: <count>, worst <severity or none>. Spec: <count or skipped>, worst <severity or none>.
Skipped optional checks:
Residual risk:
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

An incomplete report records:

```text
Review status: incomplete
Review mode: initial | remediation
Fixed point: <resolved or unresolved>
Snapshot identity: <identity or unavailable>
Target: <resolved target or unresolved>
Sources: Standards: <sources or unresolved>. Spec: <source, skipped, or unresolved>.
Covered work:
Verified findings: <findings already admitted; make no clean inference for uncovered axes>
Carried dispositions: <when applicable>
Blocker: <exact routing, ref, capture, source, evidence, drift, or report blocker>
Skipped work:
Residual risk:
Drift: <none, detected, or not reached>
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires Route, Pin, Trace, Judge, Admit, and Return to close for
every applicable axis; the Standards-to-Spec lens reset occurred; every
candidate and carried ID is disposed; drift passes; and the terminal report
truthfully returns control to the caller.
