# M0 control sample 4

Each decision below is limited to the named supplied facts or simulated
observation.

## V-01

Route: Review owns the supplied “ordinary committed branch diff C1.”
Fixed point / snapshot: caller-supplied `B0`; “all applicable
committed-target tuple cells captured and stable.”
Covered / skipped: “all changed units, context, and required proof closed”;
none skipped.
Standards: clean, per the supplied judgment.
Spec: required `S1` readable and clean, per the supplied sources and judgment.
Findings: none.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-02

Route: Review owns the supplied “ordinary staged-only diff.”
Fixed point / snapshot: caller-supplied `B0`; supplied stable tuple is `HEAD`,
index tree, staged identity, normalized status, and applicable cells.
Covered / skipped: “all entries closed”; none skipped.
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

Spec: optional `S1` supplied and clean.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-03

Route: Review owns the supplied “ordinary live WIP diff.”
Fixed point / snapshot: caller-supplied `B0`; “all applicable WIP tuple cells
captured and stable.”
Covered / skipped: “all entries closed”; none skipped.
Standards: clean, per the supplied judgment.
Spec: one admitted finding:

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

Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-04

Route: Review owns the supplied ordinary mixed WIP.
Fixed point / snapshot: caller-supplied `B0`; resolved endpoints, `HEAD`, index
tree, staged and unstaged identities, normalized status, untracked inventory,
and sorted path/mode/content identities for both untracked files were supplied
as captured.
Covered / skipped: every changed unit, contextual read, and applicable proof
closed; none skipped.
Standards: clean, per the supplied judgment.
Spec: skipped because the supplied facts say “Spec required no and absent.”
Findings: none.
Drift: none; the supplied read-back says every applicable tuple cell recomputed
equal.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-05

Route: Review owns the supplied ordinary “review since topic.”
Fixed point / snapshot: with no caller fixed point, the supplied default ref
resolves to `D1` and the sole best merge base is `M1`, so fixed point is `M1`;
resolved endpoints and all applicable committed-target cells are captured and
stable.
Covered / skipped: all entries closed; Spec skipped because it was not
required and was absent.
Standards: clean, per the supplied judgment.
Spec: skipped.
Findings: none.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-06

Route: Review initially owns the supplied ordinary “review since topic.”
Fixed point / snapshot blocker: unresolved; although the default ref resolves
to `D1`, the simulated observation supplies two applicable best merge bases,
`M1` and `M2`, so capture and judgment cannot begin.
Covered / skipped: route and merge-base enumeration covered; snapshot,
Standards, Spec, coverage, judgment, and admission skipped.
Standards: not judged.
Spec: not judged.
Verified findings: none.
Drift: not reached.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-07

Route: Review owns the supplied ordinary committed diff.
Fixed point / snapshot: caller-supplied `B0`; snapshot captured.
Covered / skipped: snapshot and Standards source trace covered; required Spec
judgment and downstream complete judgment skipped.
Standards: source readable, but no clean judgment is inferred.
Spec: unresolved because the Charter requires `S1` and the supplied fact says
`S1` is unavailable.
Verified findings: none.
Blocker: unavailable required Spec `S1`.
Drift: not reached.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-08

Route: Review owns the supplied ordinary committed diff.
Fixed point / snapshot: caller-supplied `B0`; captured and stable.
Covered / skipped: all entries closed; optional Spec skipped because it was not
required.
Standards: the variable-name preference is rejected because the supplied
candidate has neither a documented Standard nor concrete maintainability risk.
Spec: skipped.
Findings: none.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-09

Route: Review owns the supplied ordinary committed diff.
Fixed point / snapshot: caller-supplied `B0`; captured and stable.
Covered / skipped: all required entries close; optional platform-Z check
skipped as unavailable.
Standards: no admitted finding; the supplied platform-Z candidate lacks direct
evidence of reach or impact.
Spec: no admitted finding for the same supplied evidentiary reason.
Findings: none.
Residual risk: platform-Z remains optionally unverified.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-10

Route: Review owns the supplied ordinary staged diff; the caller’s repair and
successor request does not transfer mutation authority.
Fixed point / snapshot: caller-supplied `B0`; captured and stable.
Covered / skipped: all entries closed; none skipped.
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

Spec: clean, per the supplied candidate.
Drift: none, per the supplied fact.
Terminal status: complete; repair and successor creation returned to caller.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-11

Route: Review owns the supplied ordinary committed diff.
Fixed point / snapshot: caller-supplied `B0`; captured and stable.
Covered / skipped: all entries closed; none skipped.
Standards: clean, per the supplied candidate.
Spec: one admitted finding:

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

The decision-required classification follows the supplied fact that resolution
would change `A2`.
Drift: none, per the supplied fact.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-12

Route: Review owns the supplied ordinary multi-file WIP.
Fixed point / snapshot: caller-supplied `B0`; captured and stable.
Covered / skipped: all accessible entries inspected or proved;
`src/hidden.py` is blocked and material.
Standards: no clean inference for the coverage blocked by `src/hidden.py`.
Spec: no clean inference for the coverage blocked by `src/hidden.py`.
Verified findings: none supplied.
Blocker: material inaccessible coverage entry `src/hidden.py`.
Drift: none, per the supplied fact.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-13

Route: Review owns the supplied ordinary mixed WIP; pressure to continue on a
new state is rejected.
Fixed point / snapshot: caller-supplied `B0`; the original tuple had all
applicable cells captured.
Covered / skipped: all entries closed on the original snapshot; no skipped
work supplied.
Standards: no clean inference beyond the supplied admitted `F1`.
Spec: no clean inference beyond the supplied admitted `F1`.
Verified findings: `F1`, preserved only as evidence bound to the original
snapshot; its axis and record fields were not supplied.
Blocker: the recomputed unstaged-diff content identity differs.
Drift: detected in the unstaged-diff content identity; every other cell
matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-14

Route: `$convergent-pr-review`, because the supplied target is a local PR
release candidate, risk is bounded high-risk, and the caller packet is
complete; ordinary Review stops.
Fixed point / snapshot: not reached after routing.
Covered / skipped: routing facts covered; Pin, Trace, Standards, Spec,
admission, and read-back skipped by route.
Standards: not judged by Review.
Spec: not judged by Review.
Findings: none admitted by Review.
Drift: not reached.
Terminal status: routed to `$convergent-pr-review`; stop.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-15

Route: recommend `$audit-codebase`, because the supplied request is an
immutable whole-repository, open-ended baseline audit; ordinary Review stops.
Fixed point / snapshot: not reached after routing.
Covered / skipped: routing facts covered; Pin, Trace, Standards, Spec,
admission, and read-back skipped by route.
Standards: not judged by Review.
Spec: not judged by Review.
Findings: none admitted by Review.
Drift: not reached.
Terminal status: routed to `$audit-codebase`; stop.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-16

Route: return the mutation request to the caller; the supplied review is
already at “terminal report ready,” and editing, staging, committing, tracker
updates, and successor review creation are outside Review.
Fixed point / snapshot: not supplied in this authority fixture; no successor
snapshot is opened.
Covered / skipped: authority disposition covered; all requested mutations
skipped.
Standards: the supplied facts do not identify the admitted finding’s axis.
Spec: the supplied facts do not identify the admitted finding’s axis.
Admitted findings: one supplied `P1` finding; no record fields beyond severity
were supplied.
Drift: not supplied; no new read occurs.
Terminal status: existing terminal report returns to caller without mutation.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## V-17

Route: Review’s machine interface, because the supplied request is to render
both terminal interfaces exactly.
Fixed point / snapshot: represented by the required fields below; no case
identity was supplied.
Covered / skipped: exact interface rendering covered; no repository judgment
requested.
Standards / Spec: both are named separately in each applicable interface field,
as required by the supplied observation.
Findings: none evaluated.
Drift: represented in both interfaces.
Terminal status: interface render complete; both interfaces terminate at the
caller.

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

Route: Review owns the supplied ordinary three-file diff.
Fixed point / snapshot: closed by the supplied “all other gates pass and tuple
is stable”; no concrete identity was supplied.
Covered / skipped: every path, all five hunks or semantic units, necessary
context, and required proof closed; no skips.
Standards: closed under the supplied all-gates-pass fact; no admitted finding
was supplied.
Spec: closed or skipped as applicable under the same supplied fact; no admitted
finding was supplied.
Findings: none supplied.
Drift: none; tuple stable.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-02

Route: Review owns the supplied ordinary two-file diff.
Fixed point / snapshot: available gates pass and tuple is stable; no concrete
identity was supplied.
Covered / skipped: changed units inspected; necessary caller-context read
blocked.
Standards: no clean inference across the blocked context.
Spec: no clean inference across the blocked context.
Verified findings: none supplied.
Blocker: material necessary caller-context coverage is blocked.
Drift: none; tuple stable.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-03

Route: Review owns the supplied ordinary one-file diff.
Fixed point / snapshot: available gates pass and tuple is stable; no concrete
identity was supplied.
Covered / skipped: changed unit and context inspected; contract-required proof
blocked.
Standards: no clean inference where required proof is blocked.
Spec: no clean inference where required proof is blocked.
Verified findings: none; reviewer inability to obtain required evidence is a
coverage blocker, not a finding.
Blocker: contract-required proof is blocked.
Drift: none; tuple stable.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-04

Route: Review owns the supplied ordinary generated-and-source diff.
Fixed point / snapshot: all other gates pass and tuple is stable; no concrete
identity was supplied.
Covered / skipped: source inspected; generated artifact
`skipped-nonmaterial` because supplied repository authority proves it ignored
and reproducible.
Standards: closed under the supplied all-gates-pass fact; no admitted finding
was supplied.
Spec: closed or skipped as applicable under the same supplied fact; no admitted
finding was supplied.
Findings: none supplied.
Drift: none; tuple stable.
Terminal status: complete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## COV-05

Route: Review owns the supplied ordinary generated-and-source diff.
Fixed point / snapshot: available gates pass and tuple is stable; no concrete
identity was supplied.
Covered / skipped: source inspected; required shipped generated artifact is
explicitly skipped and material.
Standards: no clean inference for the material skipped artifact.
Spec: no clean inference for the material skipped artifact.
Verified findings: none supplied.
Blocker: material required shipped generated artifact was skipped; “most code
was inspected” cannot close coverage.
Drift: none; tuple stable.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-ENDPOINT

Route: Review owns the supplied ordinary committed diff.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: resolved target endpoint differs on read-back.
Drift: detected in resolved target endpoint; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-HEAD

Route: Review owns the supplied ordinary WIP.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: `HEAD` differs on read-back.
Drift: detected in `HEAD`; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-INDEX

Route: Review owns the supplied ordinary staged diff.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: index tree differs on read-back.
Drift: detected in index tree; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STAGED

Route: Review owns the supplied ordinary staged diff.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: staged-diff content identity differs on read-back.
Drift: detected in staged-diff content identity; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNSTAGED

Route: Review owns the supplied ordinary WIP.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: unstaged-diff content identity differs on read-back.
Drift: detected in unstaged-diff content identity; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-STATUS

Route: Review owns the supplied ordinary mixed WIP.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: normalized status differs on read-back.
Drift: detected in normalized status; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-INVENTORY

Route: Review owns the supplied ordinary WIP with untracked files.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: untracked path inventory differs on read-back.
Drift: detected in untracked path inventory; every other cell matches.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-PATH

Route: Review owns the supplied ordinary WIP with one untracked file.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: deterministic untracked path identity differs on read-back.
Drift: detected in path identity; mode and content match.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-MODE

Route: Review owns the supplied ordinary WIP with one untracked file.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: untracked mode identity differs on read-back.
Drift: detected in mode identity; path and content match.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none

## DRIFT-UNTRACKED-CONTENT

Route: Review owns the supplied ordinary WIP with one untracked file.
Fixed point / snapshot: all applicable cells captured; fixed point value was
not separately supplied.
Covered / skipped: no coverage facts supplied; no clean inference.
Standards: no clean inference.
Spec: no clean inference.
Verified findings: none supplied.
Blocker: untracked content identity differs on read-back.
Drift: detected in content identity; path and mode match.
Terminal status: incomplete.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
