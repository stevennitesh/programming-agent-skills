# M0 control sample 9

Runtime tree: `37a670dbe0748f5f89d7d8e0b61ff30b0241fffd81b1861da5f5838af6dd98c8`  
Fixture: `b6750ac8c30b3d25c7bb1652e1ff8a1735d5369c5475ba11417e7f987e411074`

## 1. V-01

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: all applicable committed-target tuple cells captured and stable  
Target: ordinary committed branch diff `C1`  
Sources: Standards: readable. Spec: required `S1`, readable.  
Covered work: all changed units, context, and required proof closed  
Standards findings: none  
Spec findings: none  
Axis summary: Standards: 0, worst none. Spec: 0, worst none.  
Skipped optional checks: none supplied  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.snapshot`, `facts.sources`, `facts.coverage`, `facts.judgment`, and `facts.drift`.

## 2. V-02

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: `HEAD`, index tree, staged identity, normalized status, and applicable cells captured and stable  
Target: ordinary staged-only diff  
Sources: Standards: readable. Spec: optional `S1`, supplied.  
Covered work: all entries closed  
Standards findings:

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

Spec findings: none  
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.  
Skipped optional checks: none supplied  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: the supplied `facts.judgment` closes all five admission gates; `facts.classification` supplies axis, severity, blocking, and remediation.

## 3. V-03

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: all applicable WIP tuple cells captured and stable  
Target: ordinary live WIP diff  
Sources: Standards: readable. Spec: required `S1`, readable.  
Covered work: all entries closed  
Standards findings: none  
Spec findings:

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

Axis summary: Standards: 0, worst none. Spec: 1, worst P1.  
Skipped optional checks: none supplied  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: the supplied `facts.judgment` closes all five admission gates; `facts.classification` supplies axis, severity, blocking, and remediation.

## 4. V-04

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: resolved endpoints, `HEAD`, index tree, staged and unstaged identities, normalized status and untracked inventory, plus sorted path/mode/content identities for both untracked files  
Target: ordinary mixed staged, unstaged, and untracked WIP  
Sources: Standards: readable. Spec: skipped because not required and absent.  
Covered work: every changed unit, contextual read, and applicable proof closed  
Standards findings: none  
Spec findings: skipped  
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.  
Skipped optional checks: Spec  
Residual risk: none supplied  
Drift: none; every applicable tuple cell recomputed equal  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.snapshot`, `facts.sources`, `facts.coverage`, `facts.judgment`, and `facts.drift`.

## 5. V-05

Review status: complete  
Review mode: initial  
Fixed point: unique best merge base `M1`  
Snapshot identity: default-branch endpoint `refs/remotes/origin/main` -> `D1`, target endpoint, and all applicable committed-target cells captured and stable  
Target: ordinary review since topic  
Sources: Standards: readable. Spec: skipped because not required and absent.  
Covered work: all entries closed  
Standards findings: none  
Spec findings: skipped  
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.  
Skipped optional checks: Spec  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.default_branch` resolves to `D1`; `facts.merge_bases` contains exactly `M1`; all remaining supplied gates close.

## 6. V-06

Review status: incomplete  
Review mode: initial  
Fixed point: unresolved  
Snapshot identity: unavailable  
Target: ordinary review since topic; default-branch ref resolves to `D1`  
Sources: Standards: unresolved. Spec: unresolved.  
Covered work: route and default-branch ref resolution only  
Verified findings: none; judgment did not begin  
Blocker: fixed point is ambiguous because the simulated observation supplies two applicable best merge bases, `M1` and `M2`  
Skipped work: capture, Trace, both judgment axes, admission, and read-back  
Residual risk: candidate quality is unassessed  
Drift: not reached  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.observation` says two applicable best merge bases exist before judgment.

## 7. V-07

Review status: incomplete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured  
Target: ordinary committed diff  
Sources: Standards: readable. Spec: required `S1`, unavailable.  
Covered work: route, capture, and available source trace  
Verified findings: none; make no clean inference for either axis  
Blocker: required Spec `S1` is unavailable  
Skipped work: Standards-to-Spec judgment, admission, and Return read-back  
Residual risk: both axes remain unassessed  
Drift: not reached  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.spec_required` is yes and `facts.sources` says required `S1` is unavailable.

## 8. V-08

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured and stable  
Target: ordinary committed diff  
Sources: Standards: readable. Spec: skipped because not required.  
Covered work: all entries closed  
Standards findings: none; the naming preference is rejected because no governing Standard or concrete maintainability impact supports it  
Spec findings: skipped  
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.  
Skipped optional checks: Spec  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.candidate` is preference-only and lacks Anchor and Impact; `facts.coverage` and `facts.drift` close.

## 9. V-09

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured and stable  
Target: ordinary committed diff  
Sources: Standards: readable. Spec: readable.  
Covered work: all required entries closed  
Standards findings: none  
Spec findings: none  
Axis summary: Standards: 0, worst none. Spec: 0, worst none.  
Skipped optional checks: platform-Z check unavailable  
Residual risk: a platform-Z defect remains possible but unverified  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.candidate` lacks direct evidence of reach or impact; `facts.coverage` identifies the unavailable check as optional.

## 10. V-10

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured and stable  
Target: ordinary staged diff  
Sources: Standards: readable. Spec: readable.  
Covered work: all entries closed  
Standards findings:

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

Spec findings: none  
Axis summary: Standards: 1, worst P1. Spec: 0, worst none.  
Skipped optional checks: none supplied  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.candidate` closes all admission gates and `facts.classification` classifies F1; `facts.pressure` does not grant repair or successor authority.

## 11. V-11

Review status: complete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured and stable  
Target: ordinary committed diff  
Sources: Standards: readable. Spec: readable.  
Covered work: all entries closed  
Standards findings: none  
Spec findings:

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

Axis summary: Standards: 0, worst none. Spec: 1, worst P1.  
Skipped optional checks: none supplied  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.candidate` closes all admission gates; changing accepted criterion `A2` makes remediation decision-required as supplied by `facts.classification`.

## 12. V-12

Review status: incomplete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: captured and stable  
Target: ordinary multi-file WIP  
Sources: Standards: readable. Spec: readable.  
Covered work: all entries except material `src/hidden.py` are inspected or proved  
Verified findings: none supplied; make no clean inference for either uncovered axis  
Blocker: material coverage entry `src/hidden.py` is inaccessible and blocked  
Skipped work: inspection and any affected context/proof for `src/hidden.py`  
Residual risk: behavior in the inaccessible material file is unassessed  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` explicitly marks a material entry blocked.

## 13. V-13

Review status: incomplete  
Review mode: initial  
Fixed point: `B0`  
Snapshot identity: original mixed-WIP tuple; all applicable cells captured  
Target: ordinary mixed WIP at the original snapshot  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: all entries closed on the original snapshot  
Verified findings: F1 remains admitted evidence bound only to the original snapshot; its axis and record fields are not supplied  
Blocker: recomputed unstaged-diff content identity differs from the pinned identity  
Skipped work: no judgment on the changed state  
Residual risk: the changed state is unreviewed  
Drift: detected in unstaged-diff content identity; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed cell; `facts.coverage` preserves admitted F1 on the original snapshot; `facts.pressure` cannot authorize recapture or continuation.

## 14. V-14

Selected owner: `$convergent-pr-review`  
Route basis: `facts.target` is a local PR release candidate, `facts.risk` is bounded high-risk, and `facts.caller_packet` is complete.  
Covered work: routing only; ordinary Review does not capture or judge.  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none

## 15. V-15

Selected owner: recommend `$audit-codebase`  
Route basis: `facts.target` is an immutable whole-repository baseline and `facts.request` is an open-ended correctness, methodology, leakage, validation, analytics, and performance audit.  
Covered work: routing only; ordinary Review does not capture or judge.  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none

## 16. V-16

Route: Review returns the already-ready terminal report and stops.  
Terminal status: the fixture does not supply whether that ready report is complete or incomplete.  
Fixed point and snapshot identity: preserved from the ready report; values not supplied by the fixture.  
Covered work: terminal report already ready  
Standards result: not supplied  
Spec result: not supplied  
Admitted findings: one P1 finding; axis and record fields not supplied  
Drift: preserved from the ready report; value not supplied  
Rejected operations: edit, stage, commit, tracker update, and successor review  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.review_state` says one P1 is admitted and the report is ready; `facts.pressure` cannot expand Review's read-only authority.

## 17. V-17

Route: Review machine interface rendering.  
Basis: `facts.request` asks for both interfaces exactly; `facts.observation` requires both axis names, ordered incomplete fields, and caller termination.

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

## 18. COV-01

Review status: complete  
Review mode: initial  
Fixed point: resolved; identifier not supplied  
Snapshot identity: applicable tuple captured and stable  
Target: ordinary three-file diff with five hunks  
Sources: Standards: passed under `other_gates`. Spec: skipped under standalone default.  
Covered work: every path and hunk or semantic unit inspected; necessary context inspected; required proof proved; no skips  
Standards findings: none under the supplied passing gates  
Spec findings: skipped  
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.  
Skipped optional checks: Spec  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` closes every ledger entry and `facts.other_gates` says all other gates pass and the tuple is stable.

## 19. COV-02

Review status: incomplete  
Review mode: initial  
Fixed point: resolved; identifier not supplied  
Snapshot identity: applicable tuple captured and stable  
Target: ordinary two-file diff  
Sources: Standards: available gates pass. Spec: skipped under standalone default.  
Covered work: changed units inspected; necessary caller-context read blocked  
Verified findings: none supplied; make no clean inference for affected Standards or Spec judgment  
Blocker: a necessary contextual read is blocked  
Skipped work: blocked caller context and any judgment requiring it  
Residual risk: behavior depending on that context is unassessed  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` marks a necessary context entry blocked; `facts.other_gates` does not override material coverage.

## 20. COV-03

Review status: incomplete  
Review mode: initial  
Fixed point: resolved; identifier not supplied  
Snapshot identity: applicable tuple captured and stable  
Target: ordinary one-file diff  
Sources: Standards: available gates pass. Spec: skipped under standalone default.  
Covered work: changed unit and context inspected; contract-required proof blocked  
Verified findings: none; reviewer inability to obtain required evidence is not a finding  
Blocker: contract-required proof is blocked  
Skipped work: the blocked proof and any conclusion that depends on it  
Residual risk: the required behavior is unproved  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` says required proof is blocked; the Finding Contract distinguishes unavailable reviewer evidence from an admitted omission.

## 21. COV-04

Review status: complete  
Review mode: initial  
Fixed point: resolved; identifier not supplied  
Snapshot identity: applicable tuple captured and stable  
Target: ordinary generated and source diff  
Sources: Standards: passed under `other_gates`. Spec: skipped under standalone default.  
Covered work: source inspected; generated artifact closed as skipped-nonmaterial because repository authority proves it ignored and reproducible  
Standards findings: none under the supplied passing gates  
Spec findings: skipped  
Axis summary: Standards: 0, worst none. Spec: skipped, worst none.  
Skipped optional checks: nonmaterial ignored reproducible generated artifact  
Residual risk: none supplied  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` supplies authoritative nonmateriality; `facts.other_gates` says all other gates pass.

## 22. COV-05

Review status: incomplete  
Review mode: initial  
Fixed point: resolved; identifier not supplied  
Snapshot identity: applicable tuple captured and stable  
Target: ordinary generated and source diff  
Sources: Standards: available gates pass. Spec: skipped under standalone default.  
Covered work: source inspected; required shipped generated artifact skipped and material  
Verified findings: none supplied; make no clean inference for the material gap  
Blocker: material shipped artifact remains skipped  
Skipped work: inspection and applicable proof for the required shipped generated artifact  
Residual risk: shipped generated behavior is unassessed  
Drift: none  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.coverage` calls the skipped artifact required, shipped, and material; `facts.pressure` cannot make majority coverage complete.

## 23. DRIFT-ENDPOINT

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable committed-diff cells captured on the original state  
Target: ordinary committed diff  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: resolved target endpoint differs on read-back  
Skipped work: no judgment on the changed target  
Residual risk: current target endpoint is unreviewed  
Drift: detected in resolved target endpoint; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 24. DRIFT-HEAD

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP cells captured on the original state  
Target: ordinary WIP  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: `HEAD` differs on read-back  
Skipped work: no judgment on the changed state  
Residual risk: current WIP is unreviewed  
Drift: detected in `HEAD`; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 25. DRIFT-INDEX

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable staged-diff cells captured on the original state  
Target: ordinary staged diff  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: index tree differs on read-back  
Skipped work: no judgment on the changed index state  
Residual risk: current staged state is unreviewed  
Drift: detected in index tree; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 26. DRIFT-STAGED

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable staged-diff cells captured on the original state  
Target: ordinary staged diff  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: staged-diff content identity differs on read-back  
Skipped work: no judgment on the changed staged bytes  
Residual risk: current staged bytes are unreviewed  
Drift: detected in staged-diff content identity; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 27. DRIFT-UNSTAGED

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP cells captured on the original state  
Target: ordinary WIP  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: unstaged-diff content identity differs on read-back  
Skipped work: no judgment on the changed unstaged bytes  
Residual risk: current unstaged bytes are unreviewed  
Drift: detected in unstaged-diff content identity; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 28. DRIFT-STATUS

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable mixed-WIP cells captured on the original state  
Target: ordinary mixed WIP  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: normalized status differs on read-back  
Skipped work: no judgment on the changed worktree state  
Residual risk: current mixed WIP is unreviewed  
Drift: detected in normalized status; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 29. DRIFT-UNTRACKED-INVENTORY

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP and untracked cells captured on the original state  
Target: ordinary WIP with untracked files  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: untracked path inventory differs on read-back  
Skipped work: no judgment on the changed untracked inventory  
Residual risk: current untracked scope is unreviewed  
Drift: detected in untracked path inventory; every other cell matches  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell.

## 30. DRIFT-UNTRACKED-PATH

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP cells and deterministic untracked path/mode/content identities captured on the original state  
Target: ordinary WIP with one untracked file  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: deterministic untracked path identity differs on read-back  
Skipped work: no judgment on the changed untracked state  
Residual risk: current untracked file identity is unreviewed  
Drift: detected in untracked path identity; mode and content match  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell and matching cells.

## 31. DRIFT-UNTRACKED-MODE

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP cells and deterministic untracked path/mode/content identities captured on the original state  
Target: ordinary WIP with one untracked file  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: untracked mode identity differs on read-back  
Skipped work: no judgment on the changed untracked state  
Residual risk: current untracked file mode is unreviewed  
Drift: detected in untracked mode identity; path and content match  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell and matching cells.

## 32. DRIFT-UNTRACKED-CONTENT

Review status: incomplete  
Review mode: initial  
Fixed point: resolved for the original capture; identifier not supplied  
Snapshot identity: all applicable WIP cells and deterministic untracked path/mode/content identities captured on the original state  
Target: ordinary WIP with one untracked file  
Sources: Standards: not characterized by fixture. Spec: not characterized by fixture.  
Covered work: work before Return is not characterized; no clean inference for either axis  
Verified findings: none supplied  
Blocker: untracked content identity differs on read-back  
Skipped work: no judgment on the changed untracked bytes  
Residual risk: current untracked file content is unreviewed  
Drift: detected in untracked content identity; path and mode match  
Return boundary: caller  
Mutation authority: none  
Successor snapshot authority: none  
Basis: `facts.drift` names the changed tuple cell and matching cells.
