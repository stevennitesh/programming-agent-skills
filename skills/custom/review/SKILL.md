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
Hand a local PR, release candidate, or bounded high-risk diff and its complete
caller packet to `$convergent-pr-review`, then stop. Recommend
`$audit-codebase` for an immutable repository-baseline audit, then stop. Return
an implementation, repair, or other mutation request to its caller without
beginning review. Run no competing ordinary pass.

Carry every caller-supplied Charter field, `Spec required`, review mode, Source
Trace, fixed point and target, required proof, skips, risk, and carried finding
ID.

## Pin

Use the caller-supplied fixed point. Otherwise resolve the repository default
branch and its ref, enumerate all applicable best merge bases with the target,
and require exactly one. Return `incomplete` before judgment when none or more
than one applies.

Select exactly one target in this precedence:

1. supplied review tree;
2. explicitly staged-only;
3. supplied committed target;
4. live WIP.

Before inspection, capture one state-location snapshot tuple. Record the target
kind, fixed point, resolved endpoints, and every applicable identity:

- `HEAD`;
- index tree;
- staged-diff content;
- unstaged-diff content;
- normalized status and untracked inventory; and
- for every in-scope untracked byte, a deterministic path, mode, and content
  identity.

Record the commands and ref resolutions that produced every tuple cell. Omit a
cell only when it is inapplicable to the selected immutable target. Return
`incomplete` when any applicable cell is missing, the index cannot yield its
required identity, the target is empty, or capture otherwise cannot identify
the complete target. Judge the captured bytes, never later live reads.

Record `Review mode: initial | remediation`; standalone Review defaults to
`initial`.

For remediation, require the original Charter, prior snapshot identity,
carried IDs, caller-owned Repair delta, remaining acceptance, fixed point, and
successor target. Judge only each carried outcome and proof, the Repair delta
and affected seams, and remaining acceptance exercised by those surfaces.
Keep IDs stable and dispose each as `resolved`, `still admitted`, `disproved`,
or `incomplete`. Leave untouched scope closed.

## Trace

Trace the applicable user request, Charter, Source Trace, repository
instructions, domain decisions, captured diff, tests, required proof, skips,
and risk. Treat narration as a source pointer, not proof.

Trace Spec in this precedence:

1. caller-supplied source;
2. decision-bearing material referenced by captured commits;
3. one matching repository source.

The caller supplies `Spec required: yes | no`; standalone Review defaults to
`no`. A missing, unreadable, conflicting, or unresolved required Spec makes
the review `incomplete`. When optional Spec is absent, record it as skipped;
do not infer intent from tests or implementation.

Trace Standards from repository instructions, the routed
`docs/agents/engineering-contract.md`, test and tool configuration, and
meaningful nearby conventions. Load
[SMELL-BASELINE.md](SMELL-BASELINE.md) only when these Standards are thin.
Repository Standards override the fallback.

Maintain an in-context coverage ledger for every changed path and hunk or
equivalent semantic change unit, necessary contextual read, applicable
required proof, and explicit skip. Close every entry as `inspected`, `proved`,
`skipped-nonmaterial`, or `blocked`. A material skipped or blocked entry
prevents `complete`. Keep this ledger in context only; the terminal report
summarizes covered and skipped work.

When the target supersedes or makes behavior redundant, extend coverage beyond
changed hunks to every displaced implementation, caller, registration, export,
flag, test, configuration, documentation, and migration required by Change
Closure.

## Judge

Judge Standards first: whether the captured candidate is built right under
documented repository Standards, maintainability constraints, and concrete
actionable risk. Apply **Must** rules as floors. Apply **Prefer** rules only
when direct evidence shows violated repository authority or a concrete
supported cost. Omit unsupported preferences.

Then return attention to the pinned snapshot and Spec sources; discard the
prior axis's conclusions, severity, counts, and ranking pressure. Judge
applicable Spec separately: whether the candidate is the right thing against
the originating commitments. Preserve each axis's own coverage and findings.

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

Before Return, recompute every applicable snapshot-tuple cell using its
recorded command and ref resolution, then compare it with the pinned identity.
Any missing or changed cell makes the report `incomplete`; name the exact drift
and preserve admitted findings only as evidence bound to the original
snapshot. Do not recapture or continue on the changed state.

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
Covered work:
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
Blocker: <exact routing, ref, capture, source, evidence, coverage, drift, or report blocker>
Skipped work:
Residual risk:
Drift: <none, detected, or not reached>
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires Route, Pin, Trace, Judge, Admit, and Return to close for
every applicable axis; every coverage-ledger entry is closed and none is
materially skipped or blocked; the Standards-to-Spec reset occurred; every
candidate and carried ID is disposed; every applicable tuple cell passes
read-back; and the terminal report truthfully returns control to the caller.
