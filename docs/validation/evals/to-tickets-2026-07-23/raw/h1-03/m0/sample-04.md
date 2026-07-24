# Runtime telemetry

- Fixture: `H1-03`
- Arm: `m0`
- Sample: `04`
- Runtime: Codex desktop, fresh independent context
- Model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Generated at: `2026-07-23T22:48:20.7697796-05:00`
- External tracker: none; all calls below are simulated against `fixture-tracker`
- Repository mutations: this evaluation record only

# Complete worker response

The approved publication proposal is frozen as follows and is identical in
subcases A through F.

## Frozen ticket `CAMP-73-T1`

- Title: Enforce 30-day audit-record retention
- Work-unit form: one enhancement behavior slice
- Parent: `P-H103`
- Source Trace: `SRC-H103@1`, owned by Eli (audit owner); commitment `C1`
- Desired behavior: the retention scheduler enforces the settled 30-day
  retention policy for audit records.
- Observable acceptance:
  - the retention scheduler integration fixture proves that records older than
    30 days are deleted;
  - the boundary case proves that records not older than 30 days are not
    selected by this policy; and
  - a simulated deletion failure makes the fixture fail rather than reporting
    successful retention enforcement.
- Dependency state: no true blockers.
- Proof lane: retention scheduler integration fixture.
- Verification authority: the source-owned acceptance in `SRC-H103@1`, with the
  repository integration-fixture result as verification evidence.
- Required evidence: a passing fixture result for the older-than-30-day case,
  the boundary case, and the deletion-failure case.
- Expected durable write scope: retention-policy configuration or policy logic
  and the retention scheduler integration fixture needed to prove it.
- Scope fence: retention policy only. Do not change unrelated audit-record
  production or storage behavior, retry an uncertain tracker creation, contact
  a live provider, or begin implementation.
- Category role: `enhancement`, authorized by the source.
- Intended tracker state: `ready-for-agent`.
- Parallel-safety judgment: this single-item graph has no peer ticket with
  which to parallelize. Work that shares the retention policy or scheduler
  fixture is serial; work proven not to touch those seams is independent.
- Execution profile:
  - semantic owner: Eli, audit owner;
  - production write seam: the audit-retention policy;
  - proof seam and scarce resource: the retention scheduler integration
    fixture;
  - ordering: first and only ticket;
  - serial tripwire: concurrent changes to retention policy semantics or the
    scheduler fixture;
  - independence: no graph-level parallelism is claimed.
- State-boundary matrix:
  - absent/initial: no enforced 30-day policy; establish and prove the policy;
  - current reusable: an already compatible 30-day rule may be retained only
    if the full integration fixture passes;
  - legacy/incompatible: any rule that retains records beyond the settled
    boundary must not be treated as compatible;
  - public access path: scheduled retention execution;
  - supported variant: the single settled 30-day policy;
  - lifecycle transition: on a scheduled run, records move from retained to
    deleted only after they become older than 30 days;
  - high-risk interaction: deletion failure must remain observable and must not
    be reported as a passing enforcement run.

Coverage is exhaustive: `C1`, the source acceptance, the retention-policy
scope, the live-provider exclusion, and the blind-retry exclusion are all
carried by `CAMP-73-T1`; there are no deferrals and no uncovered commitments.
The graph is the single node `CAMP-73-T1`, with no blocker edges and stable
order `[CAMP-73-T1]`. Exact runtime approval `PR-73` authorizes the one
publication attempt in each clean subcase. Correlation uses proposal
`CAMP-73`, ticket key `CAMP-73-T1`, source `SRC-H103@1`, and approval `PR-73`.

## A — published graph

The tracker documents provider-native idempotency, so the native idempotent
creation operation is used. Creation succeeds and exact read-back verifies the
frozen body, parent, role, state, source correlation, and unclaimed assignee.

- Source/parent: `SRC-H103@1` / `P-H103`
- Ordered tickets: `[CAMP-73-T1]`
- Dependency graph: `CAMP-73-T1 -> none`
- Verified frontier: `[CAMP-73-T1]`
- Mutation read-back: exact
- Gaps: none
- Next owner: `$implement` for the single first ready item; not invoked.

### Simulated tracker operation log — A

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotent creation is
     documented and available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_with_idempotency(idempotency_key="CAMP-73-T1", correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: success; one item keyed `CAMP-73-T1` created.
4. `get_item("CAMP-73-T1")`
   - Result: exact match for body, `P-H103` parent, `enhancement` role,
     `ready-for-agent` state, unclaimed assignee, and correlation.

No other operation or mutation occurred.

## B — published graph

The provider has no native idempotency. The single authorized `create_item`
call returns ambiguous, so it is not retried. Exact correlation finds one item,
`T-731`, and read-back proves that it is the approved `CAMP-73-T1` publication.
The ambiguous receipt is therefore reconciled as applied.

- Source/parent: `SRC-H103@1` / `P-H103`
- Ordered tickets: `[T-731 (CAMP-73-T1)]`
- Dependency graph: `T-731 -> none`
- Verified frontier: `[T-731]`
- Mutation read-back: exact
- Gaps: none
- Next owner: `$implement` for the single first ready item; not invoked.

### Simulated tracker operation log — B

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotency is unavailable;
     correlation reconciliation is available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_item(correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: ambiguous; application is unknown.
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1", source="SRC-H103@1", approval="PR-73")`
   - Result: exactly one matching item, `T-731`.
5. `get_item("T-731")`
   - Result: exact match for the frozen ticket body, `P-H103` parent,
     `enhancement` role, `ready-for-agent` state, unclaimed assignee, and all
     correlation fields.

No retry and no other operation or mutation occurred.

## C — partial-publication recovery

The only creation attempt is ambiguous. Correlation returns zero matches, but
the fixture states that absence is not conclusive, so neither non-application
nor successful publication can be claimed.

- Applied operations: unknown; the one `create_item` call may have applied.
- Failed operations: none conclusively established.
- Affected dependents: none in the frozen graph.
- Observed frontier: indeterminate; do not dispatch `CAMP-73-T1`.
- Preserved state: no further tracker mutation.
- Gap: the creation outcome is unresolved.
- Safest continuation: the tracker owner must resolve the provider-side
  receipt or obtain conclusive correlation evidence for the exact frozen
  identity. Retry only after proving non-application and receiving new
  publication authority.
- Next owner: `none`.

### Simulated tracker operation log — C

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotency is unavailable;
     correlation reconciliation is available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_item(correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: ambiguous; application is unknown.
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1", source="SRC-H103@1", approval="PR-73")`
   - Result: zero matches; absence is inconclusive.

No retry, read-back, or other mutation occurred.

## D — partial-publication recovery

The only creation attempt is ambiguous. Correlation returns two matching
items, so uniqueness cannot be established and neither candidate may be
declared the verified publication.

- Applied operations: unknown; the one `create_item` call may have applied.
- Failed operations: none conclusively established.
- Affected dependents: none in the frozen graph.
- Observed frontier: indeterminate; do not dispatch either candidate.
- Preserved state: both observed candidates are left unchanged.
- Gap: duplicate or colliding correlation must be resolved.
- Safest continuation: the tracker owner must identify the authoritative item,
  quarantine or repair the other candidate under tracker policy, and then
  obtain exact read-back. Do not retry creation.
- Next owner: `none`.

### Simulated tracker operation log — D

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotency is unavailable;
     correlation reconciliation is available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_item(correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: ambiguous; application is unknown.
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1", source="SRC-H103@1", approval="PR-73")`
   - Result: two matching items; the fixture supplies no unique authoritative
     match.

No retry, candidate mutation, or other operation occurred.

## E — partial-publication recovery

The only creation attempt is ambiguous. Correlation returns one item, but its
body belongs to approval `PR-72`, not the frozen `PR-73` proposal. It is a
conflict, not proof that `CAMP-73-T1` was applied.

- Applied operations: unknown; the one `create_item` call may have applied.
- Failed operations: none conclusively established.
- Affected dependents: none in the frozen graph.
- Observed frontier: indeterminate; the `PR-72` item is not dispatchable as
  `CAMP-73-T1`.
- Preserved state: the conflicting item is left unchanged.
- Gap: correlation collision or stale provider data prevents exact read-back.
- Safest continuation: the tracker owner must repair or disambiguate the
  correlation and conclusively resolve the `PR-73` attempt. Do not overwrite
  the `PR-72` item and do not retry creation.
- Next owner: `none`.

### Simulated tracker operation log — E

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotency is unavailable;
     correlation reconciliation is available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_item(correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: ambiguous; application is unknown.
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1", source="SRC-H103@1", approval="PR-73")`
   - Result: one item, but its body and authority belong to `PR-72`; it is not
     an exact match for the frozen publication.

No retry, overwrite, or other mutation occurred.

## F — partial-publication recovery

The single creation call fails conclusively before application. Correlation
then confirms absence, so no duplicate exists and no unknown applied mutation
remains. The requested ticket was not published.

- Applied operations: none.
- Failed operations: the one `create_item` call, conclusively not applied.
- Affected dependents: none.
- Observed frontier: empty.
- Preserved state: `P-H103` remains without a child from this proposal.
- Gap: publication failed before application.
- Safest continuation: return the conclusive failure to the tracker owner. A
  later attempt requires correction of the failure and fresh publication
  authority; this run does not retry.
- Next owner: `none`.

### Simulated tracker operation log — F

1. `get_setup()`
   - Result: compatible `fixture-tracker`; native idempotency is unavailable;
     correlation reconciliation is available; approval `PR-73` is accepted.
2. `get_parent("P-H103")`
   - Result: parent exists and matches the frozen source parent.
3. `create_item(correlation={proposal:"CAMP-73", ticket:"CAMP-73-T1", source:"SRC-H103@1", approval:"PR-73"}, item=<frozen ticket including explicit parent P-H103, role enhancement, state ready-for-agent, assignee unclaimed>)`
   - Mutation result: conclusive failure before application.
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1", source="SRC-H103@1", approval="PR-73")`
   - Result: zero matches; absence is conclusive.

No retry or other mutation occurred. Processing stops after F.
