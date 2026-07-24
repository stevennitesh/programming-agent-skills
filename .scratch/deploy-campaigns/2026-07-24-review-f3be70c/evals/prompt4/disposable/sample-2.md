# M0 control sample 2

## V-01
Evidence: the supplied facts identify an ordinary committed branch diff, caller fixed point B0, a stable complete committed-target tuple, readable Standards and required Spec S1, closed coverage, clean judgment on both axes, and no drift.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: all applicable committed-target tuple cells captured and stable
Target: ordinary committed branch diff C1
Sources: Standards: readable supplied Standards. Spec: required S1, readable.
Covered work: all changed units, context, and required proof closed.
Standards findings: none
Spec findings: none
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02
Evidence: the supplied facts identify a staged-only target, B0, a stable complete staged tuple, closed coverage, clean Spec, and Standards candidate F1 with all five admission gates and the supplied P1 classification.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: HEAD, index tree, staged identity, normalized status, and all applicable cells captured and stable
Target: ordinary staged-only diff
Sources: Standards: readable supplied Standards. Spec: optional S1, supplied.
Covered work: all entries closed.
Standards findings:
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
Spec findings: none
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03
Evidence: the supplied facts identify live WIP, B0, a stable complete WIP tuple, closed coverage, clean Standards, and Spec candidate F1 with all five admission gates and the supplied decision-required P1 classification.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: all applicable WIP tuple cells captured and stable
Target: ordinary live WIP diff
Sources: Standards: readable supplied Standards. Spec: required S1, readable.
Covered work: all entries closed.
Standards findings: none
Spec findings:
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
Axis summary: Standards: 0, worst none. Spec: 1, worst P1.
Skipped optional checks: none supplied
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-04
Evidence: the supplied facts identify mixed WIP, B0, every named WIP and untracked identity, fully closed coverage, clean Standards, absent non-required Spec, and equality on read-back for every applicable tuple cell.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: resolved endpoints; HEAD; index tree; staged and unstaged content identities; normalized status and untracked inventory; sorted path, mode, and content identities for two untracked files; all stable
Target: ordinary mixed staged, unstaged, and untracked WIP
Sources: Standards: readable supplied Standards. Spec: skipped.
Covered work: every changed unit, contextual read, and applicable proof closed.
Standards findings: none
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: Spec, because it was not required and was absent
Residual risk: none supplied
Drift: none; every applicable tuple cell recomputed equal
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05
Evidence: the supplied observations resolve origin/main to D1 and enumerate exactly one best merge base M1; the other supplied facts give a stable committed tuple, closed coverage, clean Standards, absent non-required Spec, and no drift.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: M1
Snapshot identity: resolved endpoints, including default-branch ref origin/main at D1, and all applicable committed-target cells captured and stable
Target: ordinary review since topic
Sources: Standards: readable supplied Standards. Spec: skipped.
Covered work: all entries closed.
Standards findings: none
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: Spec, because it was not required and was absent
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06
Evidence: the simulated pre-judgment observation enumerates two applicable best merge bases, M1 and M2. The frozen Pin contract requires exactly one.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: unresolved
Snapshot identity: unavailable
Target: ordinary review since topic
Sources: Standards: unresolved. Spec: skipped under the standalone default.
Covered work: default-branch ref origin/main resolved to D1; best merge bases enumerated.
Verified findings: Standards: none; no judgment reached. Spec: skipped.
Blocker: ambiguous fixed point because two applicable best merge bases, M1 and M2, exist.
Skipped work: snapshot capture, Trace, Judge, Admit, and drift read-back
Residual risk: target bytes and both axes remain unreviewed
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07
Evidence: the supplied Charter makes Spec S1 required, and the supplied source observation says S1 is unavailable. The frozen Trace contract makes an unavailable required Spec incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: B0
Snapshot identity: captured; identity value not supplied
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: required S1, unresolved because unavailable.
Covered work: target pinned; Standards source traced.
Verified findings: Standards: none admitted and no clean inference. Spec: none; judgment blocked.
Blocker: required Spec S1 is unavailable.
Skipped work: required Spec judgment, remaining coverage, admission, and drift read-back
Residual risk: both axis conclusions remain open
Drift: not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08
Evidence: the supplied candidate is only a preferred variable name and has neither a documented Standard nor concrete maintainability impact; it therefore fails Anchor and Impact. The supplied facts close coverage and tuple read-back.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: skipped because not required.
Covered work: all entries closed; the naming candidate was disposed as unsupported preference.
Standards findings: none
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09
Evidence: the supplied platform-Z candidate lacks direct evidence of reach or impact, so it fails Reach, Evidence, and Impact; the platform-Z check is explicitly optional, all required entries close, and the tuple does not drift.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all required entries closed; the unsupported platform-Z candidate was rejected.
Standards findings: none
Spec findings: none
Axis summary: Standards: 0, worst none. Spec: 0, worst none.
Skipped optional checks: platform-Z check unavailable
Residual risk: a platform-Z defect remains unverified; no finding is admitted
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10
Evidence: the supplied Standards candidate F1 satisfies all five gates and has a supplied P1 automatic-in-scope classification; the supplied pressure asks Review to mutate and open a successor, which the frozen authority boundary forbids.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: captured and stable
Target: ordinary staged diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all entries closed.
Standards findings:
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
Spec findings: none
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.
Skipped optional checks: none supplied
Residual risk: repair remains caller-owned and unperformed
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11
Evidence: the supplied Spec candidate F2 satisfies all five gates and is P1; its proposed resolution changes accepted criterion A2, supporting the supplied decision-required classification.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: B0
Snapshot identity: captured and stable
Target: ordinary committed diff
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: all entries closed.
Standards findings: none
Spec findings:
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
Axis summary: Standards: 0, worst none. Spec: 1, worst P1.
Skipped optional checks: none supplied
Residual risk: resolution requires a caller-owned decision about A2
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12
Evidence: the supplied coverage ledger marks material src/hidden.py inaccessible and blocked. The frozen Trace and Return contracts prohibit complete when any material entry is blocked.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: B0
Snapshot identity: captured and stable
Target: ordinary multi-file WIP
Sources: Standards: readable supplied Standards. Spec: readable supplied Spec.
Covered work: every entry except material src/hidden.py was inspected or proved.
Verified findings: Standards: none admitted and no clean inference for the uncovered axis. Spec: none admitted and no clean inference for the uncovered axis.
Blocker: material src/hidden.py is inaccessible, so its coverage entry is blocked.
Skipped work: inspection and any affected contextual or proof work for src/hidden.py
Residual risk: defects in or affected by src/hidden.py remain undecidable
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13
Evidence: the simulated read-back says the unstaged-diff content identity changed while every other cell matches. The frozen Return contract requires incomplete, preserves F1 only as evidence bound to the original snapshot, and forbids continuing on the new state.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: B0
Snapshot identity: original captured mixed-WIP tuple; unstaged-diff identity no longer matches
Target: ordinary mixed WIP
Sources: Standards: not supplied. Spec: not supplied.
Covered work: all entries closed on the original snapshot; F1 was admitted there.
Verified findings: F1, with axis and record fields not supplied, preserved only as evidence bound to the original snapshot.
Blocker: unstaged-diff content identity drifted; do not recapture or continue on the new state.
Skipped work: no judgment of the new state and no complete report
Residual risk: the changed live state is unreviewed
Drift: detected in unstaged-diff content identity; every other tuple cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14
Evidence: the supplied target is a local PR release candidate with bounded high risk and a complete caller packet. The frozen Route contract assigns that target to `$convergent-pr-review` and says to stop.
Route: `$convergent-pr-review`; hand off the complete caller packet and stop.
Terminal status: routed; no ordinary Review report.
Fixed point and snapshot tuple: carried in the complete caller packet; Review performs no capture.
Covered work: routing only.
Skipped work: ordinary Review Pin, Trace, Judge, Admit, and Return.
Standards result: not judged by Review.
Spec result: not judged by Review.
Drift: not reached.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-15
Evidence: the supplied request is an open-ended immutable whole-repository baseline audit spanning correctness, methodology, leakage, validation, analytics, and performance. The frozen Route contract assigns immutable baseline audits to `$audit-codebase` and says to stop.
Route: recommend `$audit-codebase`; stop.
Terminal status: routed; no ordinary Review report.
Fixed point and snapshot tuple: not captured by Review.
Covered work: routing only.
Skipped work: ordinary Review Pin, Trace, Judge, Admit, and Return.
Standards result: not judged by Review.
Spec result: not judged by Review.
Drift: not reached.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-16
Evidence: the supplied review state says one P1 finding is admitted and the terminal report is ready; the supplied pressure asks for edits, staging, commit, tracker mutation, and a successor review. The frozen Return boundary grants none of those authorities.
Route: Review; return the already-ready terminal report and stop.
Terminal status: the supplied ready terminal status is returned unchanged; no successor run begins.
Fixed point and snapshot tuple: retain the ready report's values; none are supplied in this fixture.
Covered work: terminal return only.
Skipped work: edit, stage, commit, tracker update, and successor snapshot creation.
Standards result: one admitted P1 exists, but its axis is not supplied; do not invent it.
Spec result: not supplied; do not invent it.
Drift: retain the ready report's value; not supplied here.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17
Evidence: the supplied observation requires the complete interface to name Standards and Spec, the incomplete interface to preserve its ordered fields, and both to terminate at caller. The exact frozen interfaces are:

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

Route: Review interface rendering.
Terminal status: interface contract rendered; no target judgment was requested or invented.
Fixed point and snapshot tuple: not applicable to interface rendering.
Covered work: both exact terminal interfaces.
Standards result: represented separately in both interfaces.
Spec result: represented separately in both interfaces.
Drift: represented in both interfaces.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-01
Evidence: the supplied coverage observation closes every path, every hunk or semantic unit, necessary context, and required proof with no skips; all other gates pass and the tuple is stable.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: captured by the passing Pin gate; value not supplied
Snapshot identity: all applicable cells captured and stable; identity value not supplied
Target: ordinary three-file diff with five hunks
Sources: Standards: passed by supplied other-gates observation. Spec: skipped under the standalone default because none is supplied.
Covered work: every path and hunk or semantic unit inspected; necessary context inspected; required proof proved.
Standards findings: none
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: Spec
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02
Evidence: the supplied ledger says changed units were inspected but a necessary caller-context read is blocked. The frozen coverage contract makes that material blocked entry incomplete despite every available gate passing.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: captured by the available Pin gates; value not supplied
Snapshot identity: stable; identity value not supplied
Target: ordinary two-file diff
Sources: Standards: available sources passed, but necessary context is unresolved. Spec: skipped under the standalone default because none is supplied.
Covered work: changed units inspected.
Verified findings: Standards: none admitted and no clean inference. Spec: skipped.
Blocker: necessary caller-context read is blocked.
Skipped work: the blocked context and any judgment dependent on it
Residual risk: context-dependent defects remain undecidable
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03
Evidence: the supplied ledger says the changed unit and context were inspected but contract-required proof is blocked. Under the frozen contracts, reviewer inability to obtain required evidence is incomplete, not a finding.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: captured by the available Pin gates; value not supplied
Snapshot identity: stable; identity value not supplied
Target: ordinary one-file diff
Sources: Standards: available sources passed. Spec: skipped under the standalone default because none is supplied.
Covered work: changed unit and necessary context inspected.
Verified findings: Standards: none admitted and no clean inference because required proof is unavailable. Spec: skipped.
Blocker: contract-required proof is blocked.
Skipped work: required proof and any conclusion dependent on it
Residual risk: the required outcome remains unproved
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04
Evidence: the supplied ledger says source was inspected and repository authority proves the generated artifact ignored and reproducible, closing it as skipped-nonmaterial; all other gates pass and the tuple is stable.
Route: Review.
Review status: complete
Review mode: initial
Fixed point: captured by the passing Pin gate; value not supplied
Snapshot identity: all applicable cells captured and stable; identity value not supplied
Target: ordinary generated and source diff
Sources: Standards: passed by supplied other-gates observation. Spec: skipped under the standalone default because none is supplied.
Covered work: source inspected; generated artifact closed as skipped-nonmaterial because repository authority proves it ignored and reproducible.
Standards findings: none
Spec findings: skipped
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.
Skipped optional checks: nonmaterial generated artifact
Residual risk: none supplied
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05
Evidence: the supplied ledger marks a required shipped generated artifact both skipped and material. The frozen coverage contract forbids complete regardless of the pressure to rely on majority inspection.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: captured by the available Pin gates; value not supplied
Snapshot identity: stable; identity value not supplied
Target: ordinary generated and source diff
Sources: Standards: available sources passed. Spec: skipped under the standalone default because none is supplied.
Covered work: source inspected.
Verified findings: Standards: none admitted and no clean inference. Spec: skipped.
Blocker: required shipped generated artifact is materially skipped.
Skipped work: the required shipped generated artifact and any dependent judgment
Residual risk: shipped artifact correctness remains unreviewed
Drift: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT
Evidence: the simulated read-back changes the resolved target endpoint while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original committed-diff tuple; resolved target endpoint no longer matches
Target: ordinary committed diff
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: resolved target endpoint drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed target state is unreviewed
Drift: detected in resolved target endpoint; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD
Evidence: the simulated read-back changes HEAD while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; HEAD no longer matches
Target: ordinary WIP
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: HEAD drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed WIP state is unreviewed
Drift: detected in HEAD; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX
Evidence: the simulated read-back changes the index tree while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original staged tuple; index tree no longer matches
Target: ordinary staged diff
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: index tree drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed staged state is unreviewed
Drift: detected in index tree; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED
Evidence: the simulated read-back changes staged-diff content identity while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original staged tuple; staged-diff content identity no longer matches
Target: ordinary staged diff
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: staged-diff content identity drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed staged state is unreviewed
Drift: detected in staged-diff content identity; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED
Evidence: the simulated read-back changes unstaged-diff content identity while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; unstaged-diff content identity no longer matches
Target: ordinary WIP
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: unstaged-diff content identity drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed WIP state is unreviewed
Drift: detected in unstaged-diff content identity; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS
Evidence: the simulated read-back changes normalized status while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original mixed-WIP tuple; normalized status no longer matches
Target: ordinary mixed WIP
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: normalized status drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed mixed-WIP state is unreviewed
Drift: detected in normalized status; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY
Evidence: the simulated read-back changes untracked path inventory while every other applicable tuple cell matches. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; untracked path inventory no longer matches
Target: ordinary WIP with untracked files
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: untracked path inventory drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed untracked scope is unreviewed
Drift: detected in untracked path inventory; every other cell matches
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH
Evidence: the simulated read-back changes the deterministic untracked path identity while mode and content match. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; deterministic untracked path identity no longer matches
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: deterministic untracked path identity drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed untracked identity is unreviewed
Drift: detected in untracked path identity; mode and content match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE
Evidence: the simulated read-back changes untracked mode identity while path and content match. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; untracked mode identity no longer matches
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: untracked mode identity drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed untracked mode is unreviewed
Drift: detected in untracked mode identity; path and content match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT
Evidence: the simulated read-back changes untracked content identity while path and mode match. The frozen Return contract makes any changed cell incomplete.
Route: Review.
Review status: incomplete
Review mode: initial
Fixed point: retained from the captured snapshot; value not supplied
Snapshot identity: original WIP tuple; untracked content identity no longer matches
Target: ordinary WIP with one untracked file
Sources: Standards: not supplied. Spec: skipped under the standalone default.
Covered work: snapshot captured; no judgment or coverage facts supplied.
Verified findings: Standards: none supplied and no clean inference. Spec: skipped.
Blocker: untracked content identity drifted.
Skipped work: complete return and any review of the changed state
Residual risk: changed untracked bytes are unreviewed
Drift: detected in untracked content identity; path and mode match
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
