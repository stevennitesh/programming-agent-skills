# M0 control sample 5

## V-01

- Route: Review; the supplied target is an ordinary committed branch diff.
- Fixed point / snapshot: `B0`; all applicable committed-target tuple cells were supplied as captured and stable.
- Covered / skipped: all changed units, context, and required proof closed; nothing skipped.
- Standards: none. Spec: none. These results are supplied as “Standards clean; Spec clean.”
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-02

- Route: Review; the supplied target is an ordinary staged-only diff.
- Fixed point / snapshot: `B0`; HEAD, index tree, staged identity, normalized status, and applicable cells were supplied as captured and stable.
- Covered / skipped: all entries closed; nothing skipped.
- Standards: admit F1 — Axis: Standards; Severity: P1; Location: `src/a.py:8`; Anchor: A1; Supported scenario: R1; Evidence: E1; Impact: I1; Blocking: yes; Remediation: automatic-in-scope; Required proof: `test_a`. Every admission gate and the classification are supplied. Spec: none, supplied as clean.
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-03

- Route: Review; the supplied target is an ordinary live WIP diff.
- Fixed point / snapshot: `B0`; all applicable WIP tuple cells were supplied as captured and stable.
- Covered / skipped: all entries closed; nothing skipped.
- Standards: none, supplied as clean. Spec: admit F1 — Axis: Spec; Severity: P1; Location: `src/b.py:12`; Anchor: A1; Supported scenario: R1; Evidence: E1; Impact: I1; Blocking: yes; Remediation: decision-required; Required proof: `acceptance_b`. Every admission gate and the classification are supplied.
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-04

- Route: Review; the supplied target is an ordinary mixed staged, unstaged, and untracked WIP.
- Fixed point / snapshot: `B0`; resolved endpoints, HEAD, index tree, staged identity, unstaged identity, normalized status, untracked inventory, and sorted path/mode/content identities for both untracked files were supplied as captured.
- Covered / skipped: every changed unit, contextual read, and applicable proof closed; Spec was explicitly non-required and absent, so it is skipped.
- Standards: none, supplied as clean. Spec: skipped.
- Drift: none; every applicable tuple cell was supplied as recomputed equal.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-05

- Route: Review; the supplied target is an ordinary “review since topic” diff.
- Fixed point / snapshot: the sole applicable best merge base is `M1`; `refs/remotes/origin/main` resolves to `D1`, and resolved endpoints plus all applicable committed-target cells were supplied as captured and stable.
- Covered / skipped: all entries closed; optional absent Spec skipped.
- Standards: none, supplied as clean. Spec: skipped because it was not required and was absent.
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-06

- Route: Review; the supplied target is an ordinary “review since topic” diff.
- Fixed point / snapshot blocker: unresolved because the supplied observation has two applicable best merge bases, `M1` and `M2`, after the default ref resolved to `D1`; capture and judgment must not begin.
- Covered / skipped: default-ref and merge-base resolution covered; Pin after merge-base selection, Trace, both judgments, admission, and drift read-back skipped.
- Standards: no clean inference. Spec: no clean inference.
- Drift: not reached.
- Terminal status: incomplete — exactly one best merge base is required, but two were observed.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-07

- Route: Review; the supplied target is an ordinary committed diff.
- Fixed point / snapshot: `B0`; snapshot supplied as captured.
- Covered / skipped: Standards source readability and required-Spec tracing covered; both judgments, admission, and drift read-back skipped after the source blocker.
- Standards: no clean inference; readability alone is not judgment. Spec: unresolved because Charter-required S1 is supplied as unavailable.
- Drift: not reached.
- Terminal status: incomplete — required Spec S1 is unavailable.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-08

- Route: Review; the supplied target is an ordinary committed diff.
- Fixed point / snapshot: `B0`; snapshot supplied as captured and stable.
- Covered / skipped: all entries closed; optional Spec skipped because it was not required.
- Standards: none. The only candidate is a variable-name preference with no documented Standard or concrete maintainability risk, so it fails Anchor and Impact and is rejected. Spec: skipped.
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-09

- Route: Review; the supplied target is an ordinary committed diff.
- Fixed point / snapshot: `B0`; snapshot supplied as captured and stable.
- Covered / skipped: all required entries closed; optional platform-Z verification skipped because it is unavailable.
- Standards: none admitted. Spec: none admitted. The platform-Z candidate lacks supplied direct evidence of reach or impact and is rejected; unavailable optional verification is residual risk, not a finding.
- Drift: none, as supplied.
- Terminal status: complete, with residual risk that platform Z was not verified.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-10

- Route: Review; the supplied target is an ordinary staged diff.
- Fixed point / snapshot: `B0`; snapshot supplied as captured and stable.
- Covered / skipped: all entries closed; nothing skipped. The caller’s repair/successor request is outside Review authority.
- Standards: admit F1 — Axis: Standards; Severity: P1; Location: `src/c.py:4`; Anchor: A1; Supported scenario: R1; Evidence: E1; Impact: I1; Blocking: yes; Remediation: automatic-in-scope; Required proof: `test_c`. Every gate and classification are supplied. Spec: none, supplied as clean.
- Drift: none, as supplied.
- Terminal status: complete; report F1 and stop without repair or recapture.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-11

- Route: Review; the supplied target is an ordinary committed diff.
- Fixed point / snapshot: `B0`; snapshot supplied as captured and stable.
- Covered / skipped: all entries closed; nothing skipped.
- Standards: none, supplied as clean. Spec: admit F2 — Axis: Spec; Severity: P1; Location: `src/d.py:20`; Anchor: A2; Supported scenario: R2; Evidence: E2; Impact: I2; Blocking: yes; Remediation: decision-required; Required proof: `acceptance_d`. Every gate and classification are supplied, and the proposed resolution changes A2.
- Drift: none, as supplied.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-12

- Route: Review; the supplied target is an ordinary multi-file WIP.
- Fixed point / snapshot: `B0`; snapshot supplied as captured and stable.
- Covered / skipped: every entry except `src/hidden.py` was inspected or proved; that material path is inaccessible and blocked.
- Standards: no clean inference for uncovered scope. Spec: no clean inference for uncovered scope. No verified finding is supplied.
- Drift: none, as supplied.
- Terminal status: incomplete — material `src/hidden.py` is inaccessible.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-13

- Route: Review; the supplied target is an ordinary mixed WIP.
- Fixed point / snapshot: `B0`; all applicable tuple cells were supplied as captured for the original snapshot.
- Covered / skipped: all entries closed and F1 admitted against the original snapshot; no skipped work is supplied. The pressure to continue on changed state is rejected.
- Standards / Spec: preserve admitted F1 only as evidence bound to the original snapshot; its axis and record fields are not supplied, so no further classification or clean inference is made.
- Drift: detected — the recomputed unstaged-diff content identity differs; all other cells match.
- Terminal status: incomplete; do not recapture or continue on the new state.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-14

- Selected owner: `$convergent-pr-review`.
- Fixed point / snapshot blocker: routing stops before capture because the supplied target is a local PR release candidate with bounded high risk and a complete caller packet.
- Covered / skipped: routing covered; ordinary Review capture, Standards judgment, Spec judgment, admission, and drift read-back skipped.
- Standards: not reached. Spec: not reached.
- Drift: not reached.
- Terminal status: handed off and stopped.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-15

- Selected owner: `$audit-codebase` (recommendation).
- Fixed point / snapshot blocker: routing stops before capture because the supplied request is an open-ended correctness, methodology, leakage, validation, analytics, and performance audit of an immutable whole-repository baseline.
- Covered / skipped: routing covered; ordinary Review capture, Standards judgment, Spec judgment, admission, and drift read-back skipped.
- Standards: not reached. Spec: not reached.
- Drift: not reached.
- Terminal status: routed and stopped.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-16

- Route: Review; the supplied target is an ordinary committed diff and the terminal report is already ready.
- Fixed point / snapshot: retain the ready report’s pinned values; the assigned facts do not enumerate them, so none are invented.
- Covered / skipped: terminal reporting of the supplied admitted P1 is covered; requested editing, staging, committing, tracker mutation, and successor review are skipped as unauthorized.
- Standards / Spec: one P1 is supplied as admitted, but its axis is not supplied; preserve the ready report’s separate axis results without inventing them.
- Drift: retain the ready report’s result; no drift fact is supplied.
- Terminal status: return the ready terminal report and stop.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## V-17

- Route: Review; this is a machine-interface rendering request, not a repository judgment.
- Fixed point / snapshot blocker: no target identity is supplied; render the interfaces with placeholders rather than inventing a snapshot.
- Covered / skipped: both supplied runtime interfaces rendered; repository capture and judgment skipped.
- Standards / Spec: represented separately in both interfaces, as required by the supplied observation.
- Drift: represented by the required field in both interfaces.
- Terminal status: interface rendering complete; both interfaces terminate at caller.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

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

- Route: Review; the supplied target is an ordinary three-file, five-hunk diff.
- Fixed point / snapshot: concrete identities are not enumerated; the fixture supplies that the tuple is stable and all other gates pass.
- Covered / skipped: every path and hunk or semantic unit, necessary context read, and required proof is inspected or proved; no skips.
- Standards: no admitted finding is supplied. Spec: no admitted finding is supplied; applicable axis gates are supplied as passing.
- Drift: none; tuple supplied as stable.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## COV-02

- Route: Review; the supplied target is an ordinary two-file diff.
- Fixed point / snapshot: concrete identities are not enumerated; the fixture supplies that the tuple is stable.
- Covered / skipped: changed units inspected; necessary caller-context read blocked.
- Standards: no clean inference across the blocked context. Spec: no clean inference across the blocked context. No verified finding is supplied.
- Drift: none; tuple supplied as stable.
- Terminal status: incomplete — a necessary caller-context read is blocked.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## COV-03

- Route: Review; the supplied target is an ordinary one-file diff.
- Fixed point / snapshot: concrete identities are not enumerated; the fixture supplies that the tuple is stable.
- Covered / skipped: changed unit and context inspected; contract-required proof blocked.
- Standards: no clean inference because required evidence is unavailable. Spec: no clean inference because required evidence is unavailable. The reviewer’s inability to obtain proof is incomplete coverage, not a finding.
- Drift: none; tuple supplied as stable.
- Terminal status: incomplete — contract-required proof is blocked.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## COV-04

- Route: Review; the supplied target is an ordinary generated-and-source diff.
- Fixed point / snapshot: concrete identities are not enumerated; the fixture supplies that the tuple is stable and all other gates pass.
- Covered / skipped: source inspected; generated artifact explicitly closed as skipped-nonmaterial because supplied repository authority proves it ignored and reproducible.
- Standards: no admitted finding is supplied. Spec: no admitted finding is supplied; applicable axis gates are supplied as passing.
- Drift: none; tuple supplied as stable.
- Terminal status: complete.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## COV-05

- Route: Review; the supplied target is an ordinary generated-and-source diff.
- Fixed point / snapshot: concrete identities are not enumerated; the fixture supplies that the tuple is stable.
- Covered / skipped: source inspected; required shipped generated artifact skipped and material. “Most code” inspected does not close that entry.
- Standards: no clean inference for the uncovered material artifact. Spec: no clean inference for the uncovered material artifact. No verified finding is supplied.
- Drift: none; tuple supplied as stable.
- Terminal status: incomplete — a required shipped generated artifact is materially skipped.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-ENDPOINT

- Route: Review; the supplied target is an ordinary committed diff.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except the resolved target endpoint matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — resolved target endpoint differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-HEAD

- Route: Review; the supplied target is an ordinary WIP.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except HEAD matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — HEAD differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-INDEX

- Route: Review; the supplied target is an ordinary staged diff.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except the index tree matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — index tree differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-STAGED

- Route: Review; the supplied target is an ordinary staged diff.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except staged-diff content identity matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — staged-diff content identity differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-UNSTAGED

- Route: Review; the supplied target is an ordinary WIP.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except unstaged-diff content identity matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — unstaged-diff content identity differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-STATUS

- Route: Review; the supplied target is an ordinary mixed WIP.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except normalized status matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — normalized status differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

- Route: Review; the supplied target is an ordinary WIP with untracked files.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered and every cell except untracked path inventory matched; no additional work is supplied.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — untracked path inventory differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

- Route: Review; the supplied target is an ordinary WIP with one untracked file.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered; untracked mode and content match, but deterministic path identity does not.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — deterministic untracked path identity differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

- Route: Review; the supplied target is an ordinary WIP with one untracked file.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered; untracked path and content match, but mode identity does not.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — untracked mode identity differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

- Route: Review; the supplied target is an ordinary WIP with one untracked file.
- Fixed point / snapshot: fixed point is not enumerated; all applicable original tuple cells were supplied as captured.
- Covered / skipped: read-back covered; untracked path and mode match, but content identity does not.
- Standards: no clean inference supplied. Spec: no clean inference supplied. No verified finding is supplied.
- Drift: detected — untracked content identity differs on read-back.
- Terminal status: incomplete; do not recapture or continue.
- Return boundary: caller
- Mutation authority: none
- Successor snapshot authority: none
