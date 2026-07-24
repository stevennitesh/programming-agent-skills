# M0 control sample 6

## V-01

Route: Review (supplied target is an ordinary committed branch diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: all applicable committed-target tuple cells captured and stable
Target: ordinary committed branch diff C1
Sources: Standards: readable supplied Standards. Spec: required Spec S1, readable.
Covered work: all changed units, context, and required proof closed.
Standards findings: none (supplied judgment: clean)
Spec findings: none (supplied judgment: clean)
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02

Route: Review (supplied target is an ordinary staged-only diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: supplied HEAD, index tree, staged identity, normalized status, and applicable cells captured and stable
Target: ordinary staged-only diff
Sources: Standards: readable supplied Standards. Spec: optional supplied Spec S1.
Covered work: all entries closed.
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
Spec findings: none (supplied judgment: clean)
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03

Route: Review (supplied target is an ordinary live WIP diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: all applicable WIP tuple cells captured and stable
Target: ordinary live WIP diff
Sources: Standards: readable supplied Standards. Spec: required Spec S1, readable.
Covered work: all entries closed.
Standards findings: none (supplied judgment: clean)
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

Route: Review (supplied target is ordinary mixed WIP).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: supplied resolved endpoints, HEAD, index tree, staged identity, unstaged identity, normalized status and inventory, plus sorted path/mode/content identities for both untracked files
Target: ordinary mixed staged, unstaged, and untracked WIP
Sources: Standards: readable supplied Standards. Spec: skipped because Spec required no and absent.
Covered work: every changed unit, contextual read, and applicable proof closed.
Standards findings: none (supplied judgment: clean)
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none; every applicable tuple cell recomputed equal
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05

Route: Review (supplied target is an ordinary review-since diff).
Review status: complete
Review mode: initial
Fixed point: sole applicable best merge base M1; refs/remotes/origin/main resolved to D1
Snapshot identity: resolved endpoints and all applicable committed-target cells captured and stable
Target: ordinary review since topic
Sources: Standards: readable supplied Standards. Spec: skipped because Spec required no and absent.
Covered work: all entries closed.
Standards findings: none (supplied judgment: clean)
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06

Route: Review (ordinary review-since target reaches Pin).
Review status: incomplete
Review mode: initial
Fixed point: unresolved
Snapshot identity: unavailable
Target: ordinary review since topic
Sources: Standards: unresolved. Spec: unresolved.
Covered work: default branch refs/remotes/origin/main resolved to D1; best-merge-base enumeration returned M1 and M2.
Verified findings: none; judgment did not begin.
Blocker: two applicable best merge bases exist, so Pin cannot select exactly one fixed point.
Skipped work: snapshot capture, source trace, Standards judgment, Spec judgment, admission, and read-back
Residual risk: merits unreviewed
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07

Route: Review (supplied target is an ordinary committed diff).
Review status: incomplete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured
Target: ordinary committed diff
Sources: Standards: readable supplied Standards source. Spec: unresolved; required S1 is unavailable.
Covered work: fixed point and snapshot captured; Standards source traced.
Verified findings: none; make no clean inference for either uncovered axis.
Blocker: caller-required Spec S1 is unavailable.
Skipped work: Standards and Spec judgment, admission, and read-back were not supplied as closed.
Residual risk: candidate merits remain unreviewed.
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08

Route: Review (supplied target is an ordinary committed diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: skipped; Spec required no and no Spec source is supplied.
Covered work: all entries closed; preference-only naming candidate verified and rejected.
Standards findings: none; the variable-name preference lacks an Anchor and concrete Impact.
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: optional Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09

Route: Review (supplied target is an ordinary committed diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all required entries closed; unsupported platform-Z candidate rejected.
Standards findings: none; no direct evidence supports Reach or Impact.
Spec findings: none; no direct evidence supports Reach or Impact.
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: optional platform-Z check unavailable
Residual risk: platform-Z behavior remains unverified; this does not admit the candidate.
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10

Route: Review (supplied target is an ordinary staged diff); repair and successor-snapshot pressure is outside Review authority.
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured and stable
Target: ordinary staged diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
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
Spec findings: none (supplied fact: Spec is clean)
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11

Route: Review (supplied target is an ordinary committed diff).
Review status: complete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all entries closed.
Standards findings: none (supplied fact: Standards is clean)
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
Residual risk: proposed resolution changes A2 and therefore remains caller-owned.
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12

Route: Review (supplied target is ordinary multi-file WIP).
Review status: incomplete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: captured and stable
Target: ordinary multi-file WIP
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all entries except material src/hidden.py are inspected or proved.
Verified findings: none; make no clean inference for either axis.
Blocker: material coverage entry src/hidden.py is inaccessible and blocked.
Skipped work: src/hidden.py and any Standards or Spec judgment depending on it
Residual risk: hidden material may affect either axis.
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13

Route: Review (supplied target is ordinary mixed WIP).
Review status: incomplete
Review mode: initial
Fixed point: caller-supplied B0
Snapshot identity: original snapshot with all applicable tuple cells captured
Target: ordinary mixed WIP
Sources: Standards: not exposed by the assigned fact. Spec: not exposed by the assigned fact.
Covered work: all entries closed and F1 admitted against the original snapshot.
Verified findings:
ID: F1
Axis: not exposed by the assigned fact
Severity: not exposed by the assigned fact
Location: not exposed by the assigned fact
Anchor: admission is supplied; anchor detail is not exposed
Supported scenario: admission is supplied; scenario detail is not exposed
Evidence: supplied fact says F1 was admitted against the original snapshot
Impact: admission is supplied; impact detail is not exposed
Blocking: not exposed by the assigned fact
Remediation: not exposed by the assigned fact
Required proof: not exposed by the assigned fact
Blocker: recomputed unstaged-diff content identity differs from the pinned identity.
Skipped work: no continuation or recapture on the new state
Residual risk: F1 remains evidence bound only to the original snapshot.
Drift: detected; unstaged-diff content identity differs while every other tuple cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14

Selected owner: $convergent-pr-review
Basis: the supplied target is a local PR release candidate, its risk is bounded high-risk, and the caller packet is complete.

## V-15

Selected owner: recommend $audit-codebase
Basis: the supplied target is an immutable whole-repository baseline and the request is an open-ended correctness, methodology, leakage, validation, analytics, and performance audit.

## V-16

Route: Review only for the already-ready terminal report; the requested edit, stage, commit, tracker update, and successor review are returned to the caller.
Review status: complete
Review mode: initial
Fixed point: closed in the supplied ready terminal report; value not exposed
Snapshot identity: closed in the supplied ready terminal report; value not exposed
Target: ordinary committed diff
Sources: Standards: closed in the supplied ready terminal report; identity not exposed. Spec: closed or skipped in that report; identity not exposed.
Covered work: supplied review state says one P1 finding is admitted and the terminal report is ready.
Standards findings: axis not exposed by the assigned fact
Spec findings: axis not exposed by the assigned fact
Verified admitted finding:
ID: not exposed by the assigned fact
Axis: not exposed by the assigned fact
Severity: P1
Location: not exposed by the assigned fact
Anchor: admission is supplied; anchor detail is not exposed
Supported scenario: admission is supplied; scenario detail is not exposed
Evidence: supplied review state says one P1 finding is admitted
Impact: admission is supplied; impact detail is not exposed
Blocking: yes
Remediation: not exposed by the assigned fact
Required proof: not exposed by the assigned fact
Axis summary: one P1 finding; per-axis count is not exposed.
Skipped optional checks: not exposed by the assigned fact
Residual risk: not exposed by the assigned fact
Drift: none, as implied by the supplied fact that the terminal report is ready
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17

Route: Review (supplied target is an ordinary committed diff).
Review status: incomplete
Review mode: initial
Fixed point: unresolved
Snapshot identity: unavailable
Target: ordinary committed diff
Sources: Standards: unresolved. Spec: unresolved.
Covered work: the supplied request and observation were traced.
Verified findings: none; no merits facts were supplied.
Blocker: the request asks for both terminal interfaces, but Review must return exactly one terminal report, and no fixed point, snapshot tuple, sources, coverage, or judgment facts are supplied for this target.
Skipped work: Pin, source trace, Standards judgment, Spec judgment, admission, and read-back
Residual risk: target merits unreviewed
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-01

Route: Review (supplied target is an ordinary three-file diff).
Review status: complete
Review mode: initial
Fixed point: resolved under the supplied fact that all other gates pass; value not exposed
Snapshot identity: captured and stable under the supplied all-other-gates fact
Target: ordinary three-file diff with five hunks
Sources: Standards: resolved under the supplied all-other-gates fact. Spec: resolved or skipped under that same fact; identity not exposed.
Covered work: every path and hunk or semantic unit inspected; necessary context inspected; required proof proved; no skips.
Standards findings: none supplied
Spec findings: none supplied or skipped under the all-other-gates fact
Axis summary: no admitted finding is supplied for either axis.
Skipped optional checks: none
Residual risk: none supplied
Drift: none; tuple stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02

Route: Review (supplied target is an ordinary two-file diff).
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied all-available-gates fact; value not exposed
Snapshot identity: captured and stable
Target: ordinary two-file diff
Sources: Standards: unresolved for the blocked caller context. Spec: unresolved for the blocked caller context.
Covered work: changed units inspected; necessary caller-context read blocked.
Verified findings: none; make no clean inference for either axis.
Blocker: a necessary caller-context read is blocked, so its material coverage entry cannot close.
Skipped work: blocked caller context and dependent judgment
Residual risk: dependent Standards or Spec behavior remains unreviewed.
Drift: none; tuple stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03

Route: Review (supplied target is an ordinary one-file diff).
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied all-available-gates fact; value not exposed
Snapshot identity: captured and stable
Target: ordinary one-file diff
Sources: Standards: resolved under the supplied all-available-gates fact. Spec: resolved or skipped there; identity not exposed.
Covered work: changed unit and context inspected; contract-required proof blocked.
Verified findings: none; reviewer inability to obtain required evidence is incomplete coverage, not a finding.
Blocker: contract-required proof is blocked.
Skipped work: blocked required proof and any dependent judgment
Residual risk: required behavior remains unproved.
Drift: none; tuple stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04

Route: Review (supplied target is an ordinary generated-and-source diff).
Review status: complete
Review mode: initial
Fixed point: resolved under the supplied all-gates-pass fact; value not exposed
Snapshot identity: captured and stable
Target: ordinary generated and source diff
Sources: Standards: includes supplied repository authority proving the artifact ignored and reproducible. Spec: resolved or skipped under the supplied all-gates-pass fact.
Covered work: source inspected; generated artifact closed as skipped-nonmaterial because repository authority proves it ignored and reproducible.
Standards findings: none supplied
Spec findings: none supplied or skipped under the all-gates-pass fact
Axis summary: no admitted finding is supplied for either axis.
Skipped optional checks: ignored reproducible generated artifact, skipped-nonmaterial
Residual risk: none supplied
Drift: none; tuple stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05

Route: Review (supplied target is an ordinary generated-and-source diff).
Review status: incomplete
Review mode: initial
Fixed point: resolved under the supplied all-available-gates fact; value not exposed
Snapshot identity: captured and stable
Target: ordinary generated and source diff
Sources: Standards: resolved under the supplied all-available-gates fact. Spec: unresolved for the required shipped artifact.
Covered work: source inspected; required shipped generated artifact skipped and material.
Verified findings: none; majority coverage cannot support a clean inference.
Blocker: the required shipped generated artifact is materially skipped.
Skipped work: required shipped generated artifact and dependent judgment
Residual risk: shipped output is unreviewed.
Drift: none; tuple stable
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT

Route: Review (supplied target is an ordinary committed diff).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary committed diff
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: resolved target endpoint differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; resolved target endpoint differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD

Route: Review (supplied target is ordinary WIP).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: HEAD differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; HEAD differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX

Route: Review (supplied target is an ordinary staged diff).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary staged diff
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: index tree differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; index tree differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED

Route: Review (supplied target is an ordinary staged diff).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary staged diff
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: staged-diff content identity differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; staged-diff content identity differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED

Route: Review (supplied target is ordinary WIP).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: unstaged-diff content identity differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; unstaged-diff content identity differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS

Route: Review (supplied target is ordinary mixed WIP).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary mixed WIP
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: normalized status differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; normalized status differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

Route: Review (supplied target is ordinary WIP with untracked files).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP with untracked files
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: untracked path inventory differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; untracked path inventory differs while every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

Route: Review (supplied target is ordinary WIP with one untracked file).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP with one untracked file
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: deterministic untracked path identity differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; untracked path identity differs while mode and content match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

Route: Review (supplied target is ordinary WIP with one untracked file).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP with one untracked file
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: untracked mode identity differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; untracked mode identity differs while path and content match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

Route: Review (supplied target is ordinary WIP with one untracked file).
Review status: incomplete
Review mode: initial
Fixed point: unresolved because no fixed point fact is supplied
Snapshot identity: original snapshot with all applicable cells captured
Target: ordinary WIP with one untracked file
Sources: Standards: unresolved. Spec: unresolved.
Covered work: snapshot capture and tuple read-back
Verified findings: none supplied; make no clean inference for uncovered axes.
Blocker: untracked content identity differs on read-back.
Skipped work: no continuation or recapture after drift
Residual risk: merits are not supplied and remain unreviewed.
Drift: detected; untracked content identity differs while path and mode match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
