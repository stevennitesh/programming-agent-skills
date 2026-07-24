# M0 control sample 8

Each decision below is based only on the named fixture facts or simulated observation.

## V-01

Route: Review (basis: ordinary committed branch diff C1).
Fixed point and snapshot: caller-supplied B0; all applicable committed-target tuple cells are captured and stable.
Covered/skipped: all changed units, context, and required proof closed; no skips supplied.
Standards: clean. Spec: required S1 readable and clean.
Admitted findings: none.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02

Route: Review (basis: ordinary staged-only diff).
Fixed point and snapshot: caller-supplied B0; HEAD, index tree, staged identity, normalized status, and all applicable cells are captured and stable.
Covered/skipped: all entries closed; no skips supplied.
Standards: one admitted finding:

```text
ID: F1
Axis: Standards
Severity: P1
Location: src/a.py:8
Anchor: Standard A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_a
```

Spec: optional S1 supplied and clean.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03

Route: Review (basis: ordinary live WIP diff).
Fixed point and snapshot: caller-supplied B0; all applicable WIP tuple cells are captured and stable.
Covered/skipped: all entries closed; no skips supplied.
Standards: clean. Spec: one admitted finding:

```text
ID: F1
Axis: Spec
Severity: P1
Location: src/b.py:12
Anchor: requirement A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: decision-required
Required proof: acceptance_b
```

Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-04

Route: Review (basis: ordinary mixed staged, unstaged, and untracked WIP).
Fixed point and snapshot: caller-supplied B0; resolved endpoints, HEAD, index tree, staged and unstaged identities, normalized status, untracked inventory, and sorted path/mode/content identities for both untracked files are captured.
Covered/skipped: every changed unit, contextual read, and applicable proof closed; Spec explicitly skipped because it is not required and is absent.
Standards: clean. Spec: skipped.
Admitted findings: none.
Drift: every applicable tuple cell recomputed equal.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05

Route: Review (basis: ordinary review since topic).
Fixed point and snapshot: absent a supplied fixed point, origin/main resolves to D1 and the sole applicable best merge base M1 becomes the fixed point; resolved endpoints and all applicable committed-target cells are captured and stable.
Covered/skipped: all entries closed; optional absent Spec skipped.
Standards: clean. Spec: skipped.
Admitted findings: none.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06

Route: Review (basis: ordinary review since topic).
Fixed point and snapshot blocker: no fixed point was supplied, origin/main resolves to D1, and the simulated observation finds two applicable best merge bases, M1 and M2; exactly one is required, so capture and judgment must not begin.
Covered/skipped: no judgment coverage reached; all review work skipped after the Pin blocker.
Standards: not judged. Spec: not judged.
Verified findings: none.
Drift: not reached.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: caller-supplied B0; snapshot captured.
Covered/skipped: Standards source is readable; required Spec judgment is blocked because Charter-required S1 is unavailable.
Standards: no clean inference made. Spec: unresolved.
Verified findings: none.
Blocker: missing required Spec S1.
Drift: not reached.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: caller-supplied B0; captured and stable.
Covered/skipped: all entries closed; Spec skipped because it is not required.
Standards: no finding—the preferred variable name has neither a documented Standard anchor nor concrete maintainability impact, so it fails admission. Spec: skipped.
Admitted findings: none.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: caller-supplied B0; captured and stable.
Covered/skipped: all required entries closed; the optional platform-Z check is skipped because unavailable.
Standards: no admitted finding from the platform-Z candidate. Spec: no admitted finding from the candidate. The possible defect lacks direct evidence of reach or impact and therefore fails admission.
Admitted findings: none.
Residual risk: platform-Z behavior remains unverified because its optional check is unavailable.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10

Route: Review (basis: ordinary staged diff).
Fixed point and snapshot: caller-supplied B0; captured and stable.
Covered/skipped: all entries closed; no skips supplied.
Standards: one admitted finding:

```text
ID: F1
Axis: Standards
Severity: P1
Location: src/c.py:4
Anchor: A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_c
```

Spec: clean.
Drift: none.
Review status: complete.
The caller's pressure to repair F1 and open a successor snapshot is rejected because classification grants no mutation.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: caller-supplied B0; captured and stable.
Covered/skipped: all entries closed; no skips supplied.
Standards: clean. Spec: one admitted finding:

```text
ID: F2
Axis: Spec
Severity: P1
Location: src/d.py:20
Anchor: acceptance criterion A2
Supported scenario: R2
Evidence: E2
Impact: I2
Blocking: yes
Remediation: decision-required
Required proof: acceptance_d
```

The remediation is decision-required because the proposed resolution changes A2.
Drift: none.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12

Route: Review (basis: ordinary multi-file WIP).
Fixed point and snapshot: caller-supplied B0; captured and stable.
Covered/skipped: all other entries are inspected or proved, but material src/hidden.py is inaccessible and blocked.
Standards: no clean inference for the uncovered axis. Spec: no clean inference for the uncovered axis.
Verified findings: none supplied.
Blocker: material coverage entry src/hidden.py is blocked.
Drift: none.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13

Route: Review (basis: ordinary mixed WIP).
Fixed point and snapshot: caller-supplied B0; all applicable tuple cells captured.
Covered/skipped: all entries closed; no skips supplied.
Standards/Spec: fixture does not supply F1's axis or the axes' clean results, so none are invented.
Verified findings: F1 remains admitted evidence bound only to the original pinned snapshot; no additional finding fields are supplied.
Blocker: read-back shows the unstaged-diff content identity changed. Pressure to continue on the new state is rejected.
Drift: detected in unstaged-diff content identity; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14

Route: `$convergent-pr-review` (basis: the target is a local PR release candidate, risk is bounded high-risk, and the caller packet is complete). Review stops before Pin and runs no competing pass.
Fixed point and snapshot: not reached because ownership routes before capture.
Covered/skipped: routing only; ordinary Review judgment skipped.
Standards: not judged. Spec: not judged.
Admitted findings: none.
Drift: not reached.
Terminal status: handoff to the selected owner and stop.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-15

Route: recommend `$audit-codebase` (basis: the target is an immutable whole-repository baseline and the request is an open-ended audit of correctness, methodology, leakage, validation, analytics, and performance). Review stops before Pin.
Fixed point and snapshot: not reached because ownership routes before capture.
Covered/skipped: routing only; ordinary Review judgment skipped.
Standards: not judged. Spec: not judged.
Admitted findings: none.
Drift: not reached.
Terminal status: recommendation to the selected owner and stop.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-16

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: the ready terminal report owns these details; the fixture does not expose them, so none are invented.
Covered/skipped: the fixture states that one P1 finding is admitted and the terminal report is ready; other coverage and axis details are not exposed.
Standards/Spec: the P1 finding's axis is not supplied.
Admitted findings: one P1 finding, with all unsupplied fields left to the already-ready report.
Drift: as recorded in the ready report; not exposed by the fixture.
Terminal status: return the already-ready terminal report unchanged, then stop. Do not edit, stage, commit, update tracker state, or start a successor review.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17

Route: Review machine interface (basis: the request explicitly asks to render both terminal interfaces, and the simulated observation requires complete to name Standards and Spec, incomplete to preserve ordered fields, and both to terminate at caller).
Fixed point, snapshot, coverage, Standards/Spec results, findings, and drift are interface fields rather than case facts; no values are invented.

Complete interface:

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

Incomplete interface:

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

## COV-01

Route: Review (basis: ordinary three-file diff with five hunks).
Fixed point and snapshot: the fixture does not name the identities; it states all other gates pass and the tuple is stable.
Covered/skipped: every path and hunk or semantic unit, necessary context read, and required proof is inspected or proved; no skips.
Standards: no admitted finding supplied. Spec: no admitted finding supplied.
Admitted findings: none supplied.
Drift: none; tuple stable.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02

Route: Review (basis: ordinary two-file diff).
Fixed point and snapshot: identities are not named; all available gates pass and the tuple is stable.
Covered/skipped: changed units inspected; necessary caller-context read blocked.
Standards: no clean inference for uncovered judgment. Spec: no clean inference for uncovered judgment.
Verified findings: none supplied.
Blocker: a necessary contextual read is blocked.
Drift: none; tuple stable.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03

Route: Review (basis: ordinary one-file diff).
Fixed point and snapshot: identities are not named; all available gates pass and the tuple is stable.
Covered/skipped: changed unit and context inspected; contract-required proof blocked.
Standards: no clean inference for the proof-blocked judgment. Spec: no clean inference for the proof-blocked judgment.
Verified findings: none—the reviewer's inability to obtain required evidence is incomplete coverage, not a finding.
Blocker: contract-required proof is blocked.
Drift: none; tuple stable.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04

Route: Review (basis: ordinary generated and source diff).
Fixed point and snapshot: identities are not named; all gates pass and the tuple is stable.
Covered/skipped: source inspected; generated artifact skipped-nonmaterial because repository authority proves it is ignored and reproducible.
Standards: no admitted finding supplied. Spec: no admitted finding supplied.
Admitted findings: none supplied.
Drift: none; tuple stable.
Review status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05

Route: Review (basis: ordinary generated and source diff).
Fixed point and snapshot: identities are not named; all available gates pass and the tuple is stable.
Covered/skipped: source inspected; required shipped generated artifact explicitly skipped and material.
Standards: no clean inference for uncovered judgment. Spec: no clean inference for uncovered judgment.
Verified findings: none supplied.
Blocker: material required shipped artifact is skipped; inspecting most code cannot close coverage.
Drift: none; tuple stable.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT

Route: Review (basis: ordinary committed diff).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: resolved target endpoint differs on read-back.
Drift: detected in resolved target endpoint; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD

Route: Review (basis: ordinary WIP).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: HEAD differs on read-back.
Drift: detected in HEAD; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX

Route: Review (basis: ordinary staged diff).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: index tree differs on read-back.
Drift: detected in index tree; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED

Route: Review (basis: ordinary staged diff).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: staged-diff content identity differs on read-back.
Drift: detected in staged-diff content identity; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED

Route: Review (basis: ordinary WIP).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: unstaged-diff content identity differs on read-back.
Drift: detected in unstaged-diff content identity; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS

Route: Review (basis: ordinary mixed WIP).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: normalized status differs on read-back.
Drift: detected in normalized status; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

Route: Review (basis: ordinary WIP with untracked files).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: untracked path inventory differs on read-back.
Drift: detected in untracked path inventory; every other cell matches.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

Route: Review (basis: ordinary WIP with one untracked file).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: deterministic untracked path identity differs on read-back.
Drift: detected in untracked path identity; mode and content match.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

Route: Review (basis: ordinary WIP with one untracked file).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: untracked mode identity differs on read-back.
Drift: detected in untracked mode identity; path and content match.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

Route: Review (basis: ordinary WIP with one untracked file).
Fixed point and snapshot: fixed point is not named; all applicable tuple cells were captured.
Covered/skipped: not supplied; make no clean inference.
Standards: not supplied. Spec: not supplied.
Verified findings: none supplied.
Blocker: untracked content identity differs on read-back.
Drift: detected in untracked content identity; path and mode match.
Review status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
