# M0 control sample 3

## V-01

Route: Review (ordinary committed branch diff C1).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: all applicable committed-target tuple cells captured and stable.
Target: ordinary committed branch diff C1.
Covered work: all changed units, context, and required proof closed. Skipped work: none.
Standards result: clean; findings none. Spec result: required S1 readable and clean; findings none.
Drift: none.
Basis: `target`, `fixed_point`, `snapshot`, `sources`, `coverage`, `judgment`, and `drift` supplied for V-01.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02

Route: Review (ordinary staged-only diff).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: HEAD, index tree, staged identity, normalized status, and all applicable cells captured and stable.
Target: ordinary staged-only diff.
Covered work: all entries closed. Skipped work: none.
Standards result: one admitted P1 finding. Spec result: supplied optional S1 is clean; findings none.

ID: F1
Axis: Standards
Severity: P1
Location: src/a.py:8
Anchor: governing Standard A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_a

Drift: none.
Basis: V-02 supplies the complete stable staged tuple, closed coverage, all five finding gates for F1, its classification, clean Spec judgment, and no drift.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03

Route: Review (ordinary live WIP diff).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: all applicable WIP tuple cells captured and stable.
Target: ordinary live WIP diff.
Covered work: all entries closed. Skipped work: none.
Standards result: clean; findings none. Spec result: one admitted P1 finding.

ID: F1
Axis: Spec
Severity: P1
Location: src/b.py:12
Anchor: governing requirement A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: decision-required
Required proof: acceptance_b

Drift: none.
Basis: V-03 supplies the stable WIP tuple, readable required sources, closed coverage, clean Standards judgment, all five finding gates and classification for Spec F1, and no drift.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-04

Route: Review (ordinary mixed WIP).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: resolved endpoints, HEAD, index tree, staged identity, unstaged identity, normalized status, untracked inventory, and sorted path/mode/content identities for both untracked files; every applicable cell recomputed equal.
Target: ordinary mixed staged, unstaged, and untracked WIP.
Covered work: every changed unit, contextual read, and applicable proof closed. Skipped work: Spec, because it is not required and absent.
Standards result: clean; findings none. Spec result: skipped.
Drift: none.
Basis: V-04 supplies the fixed point, complete tuple and equal read-back, optional absent Spec, closed coverage, and clean Standards judgment.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05

Route: Review (ordinary review since topic).
Review status: complete. Review mode: initial.
Fixed point: M1, the sole applicable best merge base after `refs/remotes/origin/main` resolves to D1.
Snapshot identity: resolved endpoints and all applicable committed-target cells captured and stable.
Target: ordinary review since topic.
Covered work: all entries closed. Skipped work: Spec, because it is not required and absent.
Standards result: clean; findings none. Spec result: skipped.
Drift: none.
Basis: V-05 supplies default-branch resolution D1, exactly one merge base M1, a stable committed tuple, closed coverage, clean Standards judgment, and optional absent Spec.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06

Route: Review, stopped in Pin.
Review status: incomplete. Review mode: initial.
Fixed point: unresolved.
Snapshot identity: unavailable.
Target: ordinary review since topic.
Covered work: default branch resolved to D1 and applicable best merge bases were enumerated. Skipped work: snapshot capture, Trace, both judgments, admission, and drift read-back.
Standards result: no clean inference. Spec result: no clean inference.
Blocker: two applicable best merge bases, M1 and M2; Review requires exactly one.
Drift: not reached.
Basis: V-06 supplies `fixed_point: not supplied`, default-branch resolution D1, merge bases M1 and M2, and the pre-judgment observation that both apply.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07

Route: Review, stopped in Trace.
Review status: incomplete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured.
Target: ordinary committed diff.
Covered work: snapshot captured; Standards source is readable. Skipped work: required Spec judgment, final Standards/Spec conclusions, admission, and drift read-back.
Standards result: no clean inference. Spec result: unresolved.
Blocker: Charter-required Spec S1 is unavailable.
Drift: not reached.
Basis: V-07 supplies the fixed point and captured snapshot, says Spec is required, says S1 is unavailable, and only establishes that Standards is readable.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08

Route: Review (ordinary committed diff).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured and stable.
Target: ordinary committed diff.
Covered work: all entries closed. Skipped work: Spec, because it is not required.
Standards result: findings none; the variable-name preference is rejected because it lacks a governing Standard and concrete maintainability impact. Spec result: skipped.
Drift: none.
Basis: V-08 supplies closed coverage, a stable tuple, optional Spec, and a preference-only candidate with neither an anchor nor impact.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09

Route: Review (ordinary committed diff).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured and stable.
Target: ordinary committed diff.
Covered work: all required entries closed. Skipped work: optional platform-Z check.
Standards result: no admitted findings. Spec result: no admitted findings.
Skipped optional checks: platform-Z verification.
Residual risk: the platform-Z defect remains possible but unverified.
Drift: none.
Basis: V-09 supplies closed required coverage and no drift; its only candidate lacks direct evidence of reach or impact, and the unavailable check is explicitly optional.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10

Route: Review (ordinary staged diff); the repair and successor-snapshot request remains with the caller.
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured and stable.
Target: ordinary staged diff.
Covered work: all entries closed. Skipped work: none.
Standards result: one admitted P1 finding. Spec result: clean; findings none.

ID: F1
Axis: Standards
Severity: P1
Location: src/c.py:4
Anchor: governing anchor A1
Supported scenario: R1
Evidence: E1
Impact: I1
Blocking: yes
Remediation: automatic-in-scope
Required proof: test_c

Drift: none.
Basis: V-10 supplies a stable tuple, closed coverage, all five gates and classification for F1, clean Spec, no drift, and caller pressure to mutate; the Review contract grants no mutation or successor authority.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11

Route: Review (ordinary committed diff).
Review status: complete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured and stable.
Target: ordinary committed diff.
Covered work: all entries closed. Skipped work: none.
Standards result: clean; findings none. Spec result: one admitted P1 finding.

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

Drift: none.
Basis: V-11 supplies closed coverage, all five gates and classification for F2, clean Standards, no drift, and the fact that the proposed resolution changes A2, requiring caller decision authority.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12

Route: Review (ordinary multi-file WIP), stopped at coverage.
Review status: incomplete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: captured and stable.
Target: ordinary multi-file WIP.
Covered work: every entry other than src/hidden.py was inspected or proved. Skipped work: material inaccessible src/hidden.py is blocked.
Standards result: no clean inference. Spec result: no clean inference.
Verified findings: none supplied.
Blocker: a material changed unit, src/hidden.py, is inaccessible.
Drift: none.
Basis: V-12 supplies readable sources and a stable tuple but explicitly marks material src/hidden.py blocked; material blocked coverage prevents completion.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13

Route: Review (ordinary mixed WIP), stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: caller-supplied B0.
Snapshot identity: the originally captured tuple; its unstaged-diff content identity no longer matches.
Target: ordinary mixed WIP.
Covered work: all entries closed on the original snapshot and F1 was admitted. Skipped work: no continued judgment on the changed state.
Standards result: no clean inference beyond supplied F1, whose axis is not supplied. Spec result: no clean inference.
Verified findings: F1, preserved only as evidence bound to the original snapshot.
Blocker: unstaged-diff content identity drift; do not recapture or continue despite caller pressure.
Drift: detected in unstaged-diff content identity; every other cell matches.
Basis: V-13 supplies the original fixed point and tuple, closed coverage, admitted F1, the exact unequal tuple cell, equality of all others, and pressure to continue.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14

Route: `$convergent-pr-review`; stop without an ordinary Review pass.
Terminal status: owner selected.
Fixed point and snapshot tuple: not captured by Review; the complete caller packet transfers to the selected owner.
Covered work: routing only. Skipped work: Pin, Trace, Judge, Admit, and Return under Review.
Standards result: not judged. Spec result: not judged. Admitted findings: none.
Drift: not reached.
Basis: V-14 identifies a local PR release candidate, bounded high risk, and a complete caller packet, which exactly matches the handoff route.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-15

Route: recommend `$audit-codebase`; stop without an ordinary Review pass.
Terminal status: owner selected.
Fixed point and snapshot tuple: not captured by Review.
Covered work: routing only. Skipped work: Pin, Trace, Judge, Admit, and Return under Review.
Standards result: not judged. Spec result: not judged. Admitted findings: none.
Drift: not reached.
Basis: V-15 identifies an immutable whole-repository baseline and an open-ended correctness, methodology, leakage, validation, analytics, and performance audit.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-16

Route: Review performs Return only; the requested edits, staging, commit, tracker update, and successor review are returned to the caller.
Terminal status: return the already-ready terminal report unchanged; its `complete`/`incomplete` value is not supplied and must not be invented.
Fixed point and snapshot tuple: not supplied in V-16.
Covered work: the supplied review state has one admitted P1 finding and a ready terminal report. Skipped work: every requested mutation and successor-snapshot operation.
Standards result: not supplied. Spec result: not supplied. Admitted findings: one P1 finding, with axis and record fields not supplied.
Drift: not supplied.
Basis: V-16 supplies only the admitted P1, ready-report state, and mutation pressure; the Review contract is read-only and reserves repair, tracker, Git, and successor authority to the caller.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17

Route: Review machine interface.
Fixed point and snapshot tuple or blocker: represented by the exact ordered fields below.
Covered and skipped work, separate axis results, findings, and drift: represented by the exact ordered fields below.
Basis: V-17 requests both exact interfaces and observes that complete names Standards and Spec, incomplete preserves field order, and both terminate at caller.

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

Route: Review (ordinary three-file diff).
Review status: complete on the supplied coverage facts. Review mode: initial.
Fixed point: resolved by the supplied statement that all other gates pass; value not supplied.
Snapshot identity: tuple captured and stable; cell values not supplied.
Target: ordinary three-file diff with five hunks.
Covered work: every path and hunk or semantic unit, necessary context read, and required proof. Skipped work: none.
Standards result: closed under `all pass`; no finding detail supplied. Spec result: closed under `all pass`; no finding detail supplied. Admitted findings: none supplied.
Drift: none.
Basis: COV-01 says every coverage entry closes, there are no skips, all other gates pass, and the tuple is stable.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02

Route: Review (ordinary two-file diff), stopped at coverage.
Review status: incomplete. Review mode: initial.
Fixed point: resolved under the supplied available gates; value not supplied.
Snapshot identity: tuple captured and stable; cell values not supplied.
Target: ordinary two-file diff.
Covered work: changed units inspected. Skipped work: necessary caller-context read is blocked.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: blocked necessary contextual read.
Drift: none.
Basis: COV-02 explicitly says a necessary caller-context read is blocked; blocked material coverage prevents completion even though available gates pass and the tuple is stable.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03

Route: Review (ordinary one-file diff), stopped at coverage.
Review status: incomplete. Review mode: initial.
Fixed point: resolved under the supplied available gates; value not supplied.
Snapshot identity: tuple captured and stable; cell values not supplied.
Target: ordinary one-file diff.
Covered work: changed unit and context inspected. Skipped work: contract-required proof is blocked.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: blocked contract-required proof; reviewer inability to obtain it is incomplete coverage, not an invented finding.
Drift: none.
Basis: COV-03 explicitly marks contract-required proof blocked while available gates pass and the tuple remains stable.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04

Route: Review (ordinary generated and source diff).
Review status: complete on the supplied coverage facts. Review mode: initial.
Fixed point: resolved by the supplied statement that all gates pass; value not supplied.
Snapshot identity: tuple captured and stable; cell values not supplied.
Target: ordinary generated and source diff.
Covered work: source inspected; repository authority proves the generated artifact ignored and reproducible. Skipped work: generated artifact, closed as skipped-nonmaterial.
Standards result: closed under `all pass`; no finding detail supplied. Spec result: closed under `all pass`; no finding detail supplied. Admitted findings: none supplied.
Drift: none.
Basis: COV-04 explicitly proves the skip nonmaterial and says all other gates pass with a stable tuple.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05

Route: Review (ordinary generated and source diff), stopped at coverage.
Review status: incomplete. Review mode: initial.
Fixed point: resolved under the supplied available gates; value not supplied.
Snapshot identity: tuple captured and stable; cell values not supplied.
Target: ordinary generated and source diff.
Covered work: source inspected. Skipped work: required shipped generated artifact is material and skipped.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: material shipped artifact remains skipped; inspecting most code cannot make coverage complete.
Drift: none.
Basis: COV-05 explicitly identifies the skipped artifact as required, shipped, and material, notwithstanding caller pressure and stable available gates.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; resolved target endpoint no longer matches.
Target: ordinary committed diff.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: resolved target endpoint drift.
Drift: detected in resolved target endpoint; every other cell matches.
Basis: DRIFT-ENDPOINT supplies the complete initial tuple and exact unequal endpoint on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; HEAD no longer matches.
Target: ordinary WIP.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: HEAD drift.
Drift: detected in HEAD; every other cell matches.
Basis: DRIFT-HEAD supplies the complete initial tuple and exact unequal HEAD cell on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; index tree no longer matches.
Target: ordinary staged diff.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: index-tree drift.
Drift: detected in index tree; every other cell matches.
Basis: DRIFT-INDEX supplies the complete initial tuple and exact unequal index-tree cell on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; staged-diff content identity no longer matches.
Target: ordinary staged diff.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: staged-diff content identity drift.
Drift: detected in staged-diff content identity; every other cell matches.
Basis: DRIFT-STAGED supplies the complete initial tuple and exact unequal staged-diff identity on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; unstaged-diff content identity no longer matches.
Target: ordinary WIP.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: unstaged-diff content identity drift.
Drift: detected in unstaged-diff content identity; every other cell matches.
Basis: DRIFT-UNSTAGED supplies the complete initial tuple and exact unequal unstaged-diff identity on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; normalized status no longer matches.
Target: ordinary mixed WIP.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: normalized-status drift.
Drift: detected in normalized status; every other cell matches.
Basis: DRIFT-STATUS supplies the complete initial tuple and exact unequal normalized-status cell on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; untracked path inventory no longer matches.
Target: ordinary WIP with untracked files.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: untracked-inventory drift.
Drift: detected in untracked path inventory; every other cell matches.
Basis: DRIFT-UNTRACKED-INVENTORY supplies the complete initial tuple and exact unequal inventory cell on read-back.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; deterministic untracked path identity no longer matches.
Target: ordinary WIP with one untracked file.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: deterministic untracked-path identity drift.
Drift: detected in untracked path identity; mode and content match.
Basis: DRIFT-UNTRACKED-PATH supplies the complete initial tuple, exact unequal path identity, and matching mode and content.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; untracked mode identity no longer matches.
Target: ordinary WIP with one untracked file.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: untracked-mode identity drift.
Drift: detected in untracked mode identity; path and content match.
Basis: DRIFT-UNTRACKED-MODE supplies the complete initial tuple, exact unequal mode identity, and matching path and content.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

Route: Review, stopped at Return read-back.
Review status: incomplete. Review mode: initial.
Fixed point: not supplied.
Snapshot identity: originally captured tuple; untracked content identity no longer matches.
Target: ordinary WIP with one untracked file.
Covered work: not supplied. Skipped work: no continued judgment on changed state.
Standards result: no clean inference. Spec result: no clean inference. Verified findings: none supplied.
Blocker: untracked-content identity drift.
Drift: detected in untracked content identity; path and mode match.
Basis: DRIFT-UNTRACKED-CONTENT supplies the complete initial tuple, exact unequal content identity, and matching path and mode.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
