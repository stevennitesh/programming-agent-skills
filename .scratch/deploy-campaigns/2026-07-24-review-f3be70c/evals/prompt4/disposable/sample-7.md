# M0 control sample 7

## V-01

Route: Review; the target is an ordinary committed branch diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: all applicable committed-target tuple cells captured and stable
Target: ordinary committed branch diff C1
Sources: Standards: readable supplied Standards. Spec: required S1, readable.
Covered work: all changed units, context, and required proof closed.
Standards findings: none (supplied judgment is clean)
Spec findings: none (supplied judgment is clean)
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02

Route: Review; the target is an ordinary staged-only diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: HEAD, index tree, staged identity, normalized status, and all applicable cells captured and stable
Target: ordinary staged-only diff
Sources: Standards: readable supplied Standards. Spec: optional supplied S1.
Covered work: all coverage entries closed.
Standards findings:

ID: F1
Axis: Standards
Severity: P1
Location: src/a.py:8
Anchor: governing Standard A1
Supported scenario: R1
Evidence: direct evidence E1
Impact: concrete impact I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_a

Spec findings: none (supplied judgment is clean)
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03

Route: Review; the target is an ordinary live WIP diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: all applicable WIP tuple cells captured and stable
Target: ordinary live WIP diff
Sources: Standards: readable supplied Standards. Spec: required S1, readable.
Covered work: all coverage entries closed.
Standards findings: none (supplied judgment is clean)
Spec findings:

ID: F1
Axis: Spec
Severity: P1
Location: src/b.py:12
Anchor: governing requirement A1
Supported scenario: R1
Evidence: direct evidence E1
Impact: concrete impact I1
Blocking: yes
Remediation: decision-required
Required proof: acceptance_b

Axis summary: Standards: 0, worst none. Spec: 1, worst P1.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-04

Route: Review; the target is an ordinary mixed WIP diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: resolved endpoints, HEAD, index tree, staged and unstaged identities, normalized status and untracked inventory, and sorted path/mode/content identities for both untracked files
Target: ordinary mixed staged, unstaged, and untracked WIP
Sources: Standards: readable supplied Standards. Spec: skipped because Spec is optional and absent.
Covered work: every changed unit, contextual read, and applicable proof closed.
Standards findings: none (supplied judgment is clean)
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none; every applicable tuple cell recomputed equal
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05

Route: Review; the target is an ordinary review-since diff.
Review status: complete
Review mode: initial
Fixed point: M1, the sole applicable best merge base with topic after refs/remotes/origin/main resolved to D1
Snapshot identity: resolved endpoints and all applicable committed-target cells captured and stable
Target: ordinary review since topic
Sources: Standards: readable supplied Standards. Spec: skipped because Spec is optional and absent.
Covered work: all coverage entries closed.
Standards findings: none (supplied judgment is clean)
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06

Route: Review; routing closes, but Pin cannot select exactly one fixed point.
Review status: incomplete
Review mode: initial
Fixed point: unresolved; M1 and M2 are both applicable best merge bases after refs/remotes/origin/main resolved to D1
Snapshot identity: unavailable; capture cannot begin without one fixed point
Target: ordinary review since topic
Sources: Standards: unresolved. Spec: unresolved.
Covered work: Route and default-branch resolution; merge-base enumeration found two applicable bases.
Verified findings: none; judgment did not begin
Blocker: Pin requires exactly one applicable best merge base, but the supplied observation has M1 and M2.
Skipped work: snapshot capture, Trace, Judge, Admit, and read-back
Residual risk: no clean inference is possible for either axis
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07

Route: Review; the target is an ordinary committed diff.
Review status: incomplete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured; no more specific identity or stable read-back is supplied
Target: ordinary committed diff
Sources: Standards: readable. Spec: unresolved because required S1 is unavailable.
Covered work: Route, supplied fixed point and capture, and Standards source trace.
Verified findings: none; required Spec judgment cannot begin
Blocker: the Charter requires Spec S1, and the supplied fact says S1 is unavailable.
Skipped work: required Spec trace and judgment; terminal read-back stability is not supplied
Residual risk: no clean inference is possible for uncovered judgment
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08

Route: Review; the target is an ordinary committed diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: skipped because it is not required and no Spec is supplied.
Covered work: all entries closed; the naming preference was tested against the admission gates.
Standards findings: none; the supplied candidate has neither a governing Standard nor concrete maintainability impact
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09

Route: Review; the target is an ordinary committed diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable. Spec: readable.
Covered work: all required entries closed; optional platform-Z verification is unavailable.
Standards findings: none; the platform-Z candidate lacks direct evidence for reach or impact
Spec findings: none; no Spec violation is supplied
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: platform-Z check
Residual risk: an unverified platform-Z defect remains possible; this is not an admitted finding
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10

Route: Review; the target is an ordinary staged diff. The repair and successor request is outside Review authority.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured and stable
Target: ordinary staged diff
Sources: Standards: readable. Spec: readable.
Covered work: all entries closed.
Standards findings:

ID: F1
Axis: Standards
Severity: P1
Location: src/c.py:4
Anchor: governing anchor A1
Supported scenario: R1
Evidence: direct evidence E1
Impact: concrete impact I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_c

Spec findings: none (supplied judgment is clean)
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11

Route: Review; the target is an ordinary committed diff.
Review status: complete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable. Spec: readable.
Covered work: all entries closed.
Standards findings: none (supplied judgment is clean)
Spec findings:

ID: F2
Axis: Spec
Severity: P1
Location: src/d.py:20
Anchor: governing acceptance criterion A2
Supported scenario: R2
Evidence: direct evidence E2
Impact: concrete impact I2
Blocking: yes
Remediation: decision-required
Required proof: acceptance_d

Axis summary: Standards: 0, worst none. Spec: 1, worst P1.
Skipped optional checks: none supplied
Residual risk: resolution requires caller decision because the proposed resolution changes A2
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12

Route: Review; the target is an ordinary multi-file WIP.
Review status: incomplete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: captured and stable
Target: ordinary multi-file WIP
Sources: Standards: readable. Spec: readable.
Covered work: all entries except material src/hidden.py are inspected or proved.
Verified findings: none supplied; make no clean inference for uncovered axes
Blocker: the material coverage entry for inaccessible src/hidden.py is blocked.
Skipped work: judgment requiring src/hidden.py
Residual risk: effects in the inaccessible material file remain unjudged
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13

Route: Review; the target is an ordinary mixed WIP. The request to continue on changed state is rejected.
Review status: incomplete
Review mode: initial
Fixed point: B0 (caller supplied)
Snapshot identity: original tuple captured; its unstaged-diff content identity fails read-back
Target: ordinary mixed WIP
Sources: Standards: not supplied. Spec: not supplied.
Covered work: all entries closed on the original snapshot; F1 was admitted before read-back.
Verified findings:

ID: F1
Axis: not supplied by the fixture
Severity: not supplied by the fixture
Location: not supplied by the fixture
Anchor: admission is supplied; the underlying anchor is not supplied
Supported scenario: admission is supplied; the scenario is not supplied
Evidence: F1 was admitted against the original snapshot; its detailed evidence is not supplied
Impact: admission is supplied; the impact is not supplied
Blocking: not supplied by the fixture
Remediation: not supplied by the fixture
Required proof: not supplied by the fixture

Blocker: the recomputed unstaged-diff content identity differs from the pinned identity.
Skipped work: no recapture or judgment of the changed state
Residual risk: F1 is preserved only as evidence bound to the original snapshot
Drift: detected in unstaged-diff content identity; every other tuple cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14

Selected owner: `$convergent-pr-review`
Route: hand the complete caller packet for the bounded high-risk local PR release candidate to `$convergent-pr-review`, then stop.
Fixed point and snapshot tuple: not reached because Route selects another owner before capture.
Covered work: routing classification from target, risk, and complete caller-packet facts.
Skipped work: Review Pin, Trace, Judge, Admit, and Return judgment.
Standards result: not judged by Review.
Spec result: not judged by Review.
Drift: not reached.
Terminal status: routed and stopped.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-15

Selected owner: `$audit-codebase`
Route: recommend `$audit-codebase` for the immutable whole-repository baseline and open-ended audit, then stop.
Fixed point and snapshot tuple: not reached because Route selects another owner before capture.
Covered work: routing classification from immutable baseline and open-ended audit facts.
Skipped work: Review Pin, Trace, Judge, Admit, and Return judgment.
Standards result: not judged by Review.
Spec result: not judged by Review.
Drift: not reached.
Terminal status: routed and stopped.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-16

Route: Review owns the ordinary committed diff; the ready terminal report is returned without mutation.
Terminal status: the supplied ready report with one admitted P1 finding remains terminal.
Fixed point: preserved from the ready report; value not supplied by the fixture.
Snapshot identity: preserved from the ready report; tuple values not supplied by the fixture.
Target: ordinary committed diff
Sources: Standards and Spec results are preserved from the ready report; values are not supplied.
Covered work: supplied review state says one P1 finding is admitted and the terminal report is ready.
Admitted finding:

ID: not supplied by the fixture
Axis: not supplied by the fixture
Severity: P1
Location: not supplied by the fixture
Anchor: admission is supplied; the underlying anchor is not supplied
Supported scenario: admission is supplied; the scenario is not supplied
Evidence: the supplied review state says the P1 finding is admitted
Impact: admission is supplied; the detailed impact is not supplied
Blocking: yes
Remediation: not supplied by the fixture
Required proof: not supplied by the fixture

Skipped work: edit, stage, commit, tracker update, and successor review are not authorized.
Drift: preserved from the ready report; value not supplied by the fixture.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17

Route: Review; render both terminal interfaces. The complete interface explicitly separates Standards and Spec; the incomplete interface preserves the runtime field order.

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

Route: Review; the target is an ordinary three-file diff.
Review status: complete
Review mode: initial
Fixed point: resolved under the supplied passing gates; exact value not supplied
Snapshot identity: tuple captured and stable under the supplied passing gates
Target: ordinary three-file diff with five hunks
Sources: Standards: passed under supplied other gates. Spec: passed under supplied other gates.
Covered work: all three paths and five hunks or semantic units inspected; necessary context inspected; required proof proved; no skips.
Standards findings: none supplied under passing gates
Spec findings: none supplied under passing gates
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: none
Residual risk: none supplied
Drift: none; tuple is stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02

Route: Review; the target is an ordinary two-file diff.
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied otherwise-passing gates; exact value not supplied
Snapshot identity: tuple captured and stable
Target: ordinary two-file diff
Sources: Standards: available gates pass. Spec: available gates pass.
Covered work: changed units inspected; necessary caller-context coverage is blocked.
Verified findings: none supplied; make no clean inference for uncovered axes
Blocker: a necessary caller-context read is blocked, so a material coverage entry cannot close.
Skipped work: judgment that depends on the blocked caller context
Residual risk: effects visible only through the blocked caller seam remain unjudged
Drift: none; tuple is stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03

Route: Review; the target is an ordinary one-file diff.
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied otherwise-passing gates; exact value not supplied
Snapshot identity: tuple captured and stable
Target: ordinary one-file diff
Sources: Standards: available gates pass. Spec: available gates pass.
Covered work: changed unit and context inspected; contract-required proof is blocked.
Verified findings: none supplied; reviewer inability to obtain required evidence is not a finding
Blocker: contract-required proof is blocked, so required coverage cannot close.
Skipped work: judgment requiring the blocked proof
Residual risk: the required behavior remains unproved
Drift: none; tuple is stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04

Route: Review; the target is an ordinary generated-and-source diff.
Review status: complete
Review mode: initial
Fixed point: resolved under the supplied passing gates; exact value not supplied
Snapshot identity: tuple captured and stable
Target: ordinary generated and source diff
Sources: Standards: repository authority proves the generated artifact is ignored and reproducible. Spec: passed under supplied other gates.
Covered work: source inspected; generated artifact closed as skipped-nonmaterial under repository authority.
Standards findings: none supplied under passing gates
Spec findings: none supplied under passing gates
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: ignored reproducible generated artifact, nonmaterial
Residual risk: none supplied
Drift: none; tuple is stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05

Route: Review; the target is an ordinary generated-and-source diff.
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied otherwise-passing gates; exact value not supplied
Snapshot identity: tuple captured and stable
Target: ordinary generated and source diff
Sources: Standards: available gates pass. Spec: available gates pass.
Covered work: source inspected; required shipped generated artifact is materially skipped.
Verified findings: none supplied; majority code coverage cannot establish a clean result
Blocker: the skipped shipped generated artifact is required and material.
Skipped work: inspection and proof of the required shipped generated artifact
Residual risk: behavior of the shipped artifact remains unjudged
Drift: none; tuple is stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT

Route: Review; the target is an ordinary committed diff.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; resolved target endpoint fails read-back
Target: ordinary committed diff
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the endpoint mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: the resolved target endpoint differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in resolved target endpoint
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD

Route: Review; the target is an ordinary WIP.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; HEAD fails read-back
Target: ordinary WIP
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the HEAD mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: HEAD differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in HEAD
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX

Route: Review; the target is an ordinary staged diff.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; index tree fails read-back
Target: ordinary staged diff
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the index-tree mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: the index tree differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in index tree
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED

Route: Review; the target is an ordinary staged diff.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; staged-diff content identity fails read-back
Target: ordinary staged diff
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the staged-content mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: staged-diff content identity differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in staged-diff content identity
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED

Route: Review; the target is an ordinary WIP.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; unstaged-diff content identity fails read-back
Target: ordinary WIP
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the unstaged-content mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: unstaged-diff content identity differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in unstaged-diff content identity
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS

Route: Review; the target is an ordinary mixed WIP.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; normalized status fails read-back
Target: ordinary mixed WIP
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the normalized-status mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: normalized status differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in normalized status
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

Route: Review; the target is an ordinary WIP with untracked files.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; untracked path inventory fails read-back
Target: ordinary WIP with untracked files
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the inventory mismatch; every other cell matches.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: untracked path inventory differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in untracked path inventory
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

Route: Review; the target is an ordinary WIP with one untracked file.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; deterministic untracked path identity fails read-back while mode and content match
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the untracked-path mismatch.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: deterministic untracked path identity differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in deterministic untracked path identity
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

Route: Review; the target is an ordinary WIP with one untracked file.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; untracked mode identity fails read-back while path and content match
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the untracked-mode mismatch.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: untracked mode identity differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in untracked mode identity
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

Route: Review; the target is an ordinary WIP with one untracked file.
Review status: incomplete
Review mode: initial
Fixed point: not supplied; no value inferred
Snapshot identity: original applicable tuple captured; untracked content identity fails read-back while path and mode match
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: not supplied.
Covered work: snapshot read-back found the untracked-content mismatch.
Verified findings: none supplied; make no clean inference for unreported axes
Blocker: untracked content identity differs on read-back.
Skipped work: no recapture or continuation on the changed state
Residual risk: judgment results are not supplied
Drift: detected in untracked content identity
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
