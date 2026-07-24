# H1-03 · m0 · sample-01

## Runtime telemetry

```yaml
surface: Codex desktop
context: fresh independent worker
model: gpt-5.6-sol
reasoning_effort: high
repository: E:\GitHub\code\programming-agent-skills
selected_arm: skills/experimental/to-tickets/controls/m0
fixture: H1-03
tracker: fixture-tracker
execution_mode: closed simulated tracker
subcases_executed: [A, B, C, D, E, F]
live_provider_contacted: false
repository_mutations:
  - docs/validation/evals/to-tickets-2026-07-23/raw/h1-03/m0/sample-01.md
fixture_mutations: recorded independently under each subcase
```

## Frozen publication design

The source is `SRC-H103@1`, owned by Eli, with parent `P-H103`. Approval
`PR-73` authorizes this publication proposal. The deterministic proposal key
is `CAMP-73`, and the deterministic ticket key is `CAMP-73-T1`.

### Commitment ledger

| Source fact | Disposition |
|---|---|
| C1: enforce 30-day retention | Ticket `CAMP-73-T1` |
| Records older than 30 days are deleted by the scheduled proof fixture | Observable acceptance and integration proof in `CAMP-73-T1` |
| Scope: retention policy | Ticket scope |
| Exclusion: blind retry | Scope fence and recovery rule |
| Exclusion: live provider | Scope fence |
| Proof: retention scheduler integration fixture | Ticket proof lane |
| Category: enhancement | Authorized role on the ticket |

There are no uncovered commitments, deferrals, or no-ticket dispositions.

### Exact fixed item payload

```yaml
proposal_key: CAMP-73
ticket_key: CAMP-73-T1
approval: PR-73
title: Enforce 30-day audit-record retention
parent: P-H103
tracker_order: 1
state: ready-for-agent
role: enhancement
assignee: null
work_unit_form: vertical behavior slice
slice: >
  Enforce the settled 30-day audit-record retention policy through the
  scheduled retention path and prove its externally observable age-boundary
  behavior.
source_trace:
  source: SRC-H103@1
  owner: Eli, audit owner
  commitment: C1 enforce 30-day retention
  acceptance: records older than 30 days are deleted by the scheduled proof fixture
  proof: retention scheduler integration fixture
desired_behavior:
  - A scheduled retention run deletes audit records whose age is greater than 30 days.
edge_and_error_behavior:
  - Audit records exactly 30 days old or newer are not eligible under the "older than 30 days" rule.
  - The integration fixture is red if an eligible record remains or an ineligible record is deleted.
  - A scheduler or deletion error is surfaced by the proof fixture; this slice does not authorize a blind provider retry.
acceptance:
  - Given audit records on both sides of the 30-day boundary, the scheduled integration fixture proves that every record older than 30 days is deleted.
  - The same fixture proves that records exactly 30 days old and newer are retained.
  - The fixture exposes a failed scheduled deletion as a failed proof run.
dependencies:
  blockers: none
  stable_order: 1
proof_lane: retention scheduler integration fixture
verification_authority: Eli, audit owner
verification_evidence:
  - Passing integration-fixture output for the older-than-30-day deletion case.
  - Passing integration-fixture output for the exact-boundary and newer-record retention cases.
expected_durable_write_scope:
  - Retention-policy configuration and scheduled retention-path production code required for this policy.
  - Deletion of audit records older than 30 days when the scheduled path runs.
scope_fence:
  include: 30-day audit-retention policy and its scheduled integration proof
  exclude:
    - live-provider work
    - blind retries
    - unrelated audit behavior
    - a broader retention-policy redesign
parallel_safety:
  judgment: independently completable; only one slice exists
  constraints:
    - Serialize any work that shares the retention scheduler, audit-record store, or retention integration fixture.
    - Do not run a migration, cutover, or irreversible live-data operation under this ticket.
execution_profile:
  semantic_owner: Eli, audit owner
  production_writes: retention policy and scheduled deletion path
  proof_seam: retention scheduler integration fixture
  scarce_proof_resource: shared retention scheduler fixture, if the harness is exclusive
  ordering: first and only ticket
  serial_tripwires:
    - shared scheduler or audit-store writes
    - protected or live audit data
    - an incompatible existing retention policy
  independence: no sibling ticket exists
state_boundary_matrix:
  absent_or_initial: No enforced scheduled policy; establish the settled 30-day behavior.
  current_reusable: Reuse an existing scheduler seam only if it can enforce and prove the exact 30-day boundary.
  legacy_or_incompatible: A conflicting policy or schema is not silently migrated; it triggers the serial tripwire and remains outside this slice.
  public_access_paths: Scheduled retention path only.
  supported_variants:
    - age greater than 30 days: delete
    - age equal to or less than 30 days: retain
  lifecycle_transitions:
    - eligible record present -> scheduled run -> record absent
    - ineligible record present -> scheduled run -> record remains
    - scheduled deletion error -> proof run fails visibly
```

The graph is one node, `CAMP-73-T1`, with no blocker edges. Before each
subcase, the predicted ready frontier is that one item after an exact
publication and read-back.

## A — provider-native idempotency

### Typed result: published graph

Native idempotency was available and therefore used. The create completed
once, returning opaque fixture ID `T-A1`. Read-back matched the frozen payload,
including parent `P-H103`, role `enhancement`, state `ready-for-agent`, null
assignee, and no blockers.

```yaml
source: SRC-H103@1
parent: P-H103
ordered_tickets:
  - T-A1 (CAMP-73-T1)
coverage:
  C1: T-A1
dependency_graph:
  T-A1: []
frontier: [T-A1]
execution_profiles: complete in frozen payload
state_matrices: complete in frozen payload
tracker_state: one exact child T-A1 under P-H103
gaps: []
recommendation: $implement
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_with_idempotency
  request:
    idempotency_key: CAMP-73-T1
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: success
    applied: true
    id: T-A1
  mutation: created T-A1 exactly once
- sequence: 4
  operation: get_item
  request: {id: T-A1}
  response:
    outcome: found
    item: exact fixed item payload above
    id: T-A1
    exact_match: true
  mutation: none
```

No blind retry, live-provider access, implementation, or worker dispatch
occurred.

## B — one exact correlation match

### Typed result: published graph

The non-idempotent create returned an ambiguous receipt. It was not retried.
Correlation lookup returned exactly one item, `T-731`, and its read-back
matched the frozen payload in full. The ambiguous operation is therefore
reconciled as an applied create, not a reason to create again.

```yaml
source: SRC-H103@1
parent: P-H103
ordered_tickets:
  - T-731 (CAMP-73-T1)
coverage:
  C1: T-731
dependency_graph:
  T-731: []
frontier: [T-731]
execution_profiles: complete in frozen payload
state_matrices: complete in frozen payload
tracker_state: one exact child T-731 under P-H103
gaps: []
recommendation: $implement
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_item
  request:
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: ambiguous
    applied: unknown
    id: unknown
  mutation: application initially unknown
- sequence: 4
  operation: query_correlation
  request: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
  response:
    outcome: found
    count: 1
    ids: [T-731]
  mutation: none
- sequence: 5
  operation: get_item
  request: {id: T-731}
  response:
    outcome: found
    item: exact fixed item payload above
    id: T-731
    exact_match: true
  mutation: none
```

No second create was attempted. No live-provider access, implementation, or
worker dispatch occurred.

## C — zero matches, absence inconclusive

### Typed result: partial-publication recovery

The create receipt is ambiguous and the correlation query found no item, but
this fixture does not make absence conclusive. The create may or may not have
applied. No graph or ready frontier can safely be claimed.

```yaml
source: SRC-H103@1
parent: P-H103
applied_operations:
  - create_item: unknown
failed_or_unknown_operations:
  - create_item returned ambiguous
affected_dependents: none known
observed_tracker_state: no correlation match observed; actual application remains unknown
observed_frontier: unknown
gaps:
  - no definitive create receipt
  - no conclusive absence
safest_recovery: >
  A tracker owner must resolve the original receipt or obtain a conclusive
  identity/absence result, then read back any resolved item against the frozen
  payload. Do not issue another create while application remains unknown.
recommendation: none
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_item
  request:
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: ambiguous
    applied: unknown
    id: unknown
  mutation: application unknown
- sequence: 4
  operation: query_correlation
  request: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
  response:
    outcome: not_found
    count: 0
    absence_conclusive: false
    ids: []
  mutation: none
```

The worker stopped without a retry, live-provider access, implementation, or
dispatch.

## D — two correlation matches

### Typed result: partial-publication recovery

The create receipt is ambiguous and correlation lookup returned two matching
items. The canonical item and duplicate state cannot be determined from the
authorized observations. Neither item is treated as the published graph, and
no further mutation is safe.

```yaml
source: SRC-H103@1
parent: P-H103
applied_operations:
  - create_item: unknown
failed_or_unknown_operations:
  - create_item returned ambiguous
affected_dependents: none known
observed_tracker_state: two items correlate to CAMP-73-T1
observed_frontier: unknown
gaps:
  - canonical item identity is unresolved
  - duplicate status is unresolved
safest_recovery: >
  A tracker owner must reconcile the two identities against the original
  receipt and full payload, choose the canonical item under tracker policy,
  repair any duplicate through separately authorized tracker operations, and
  read back the resulting item. Do not create again.
recommendation: none
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_item
  request:
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: ambiguous
    applied: unknown
    id: unknown
  mutation: application unknown
- sequence: 4
  operation: query_correlation
  request: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
  response:
    outcome: multiple
    count: 2
    ids: [T-D1, T-D2]
  mutation: none
```

The symbolic IDs `T-D1` and `T-D2` identify the fixture's two opaque matches;
the fixture supplies no canonical choice. The worker stopped without a retry,
live-provider access, implementation, or dispatch.

## E — one conflicting correlation match

### Typed result: partial-publication recovery

The create receipt is ambiguous. Correlation lookup found one item, `T-E1`,
but read-back shows that its body belongs to approval `PR-72`, not the
authorized `PR-73` frozen payload. It is not adopted or modified, and its
existence does not resolve whether the attempted create applied elsewhere.

```yaml
source: SRC-H103@1
parent: P-H103
applied_operations:
  - create_item: unknown
failed_or_unknown_operations:
  - create_item returned ambiguous
affected_dependents: none known
observed_tracker_state: one correlation result T-E1 with a conflicting PR-72 body
observed_frontier: unknown
gaps:
  - attempted PR-73 create remains unresolved
  - correlation collision with PR-72
safest_recovery: >
  Preserve T-E1 unchanged. A tracker owner must investigate the correlation
  collision and the original ambiguous receipt, locate any distinct PR-73
  item if one exists, and perform exact read-back before claiming publication.
  Do not create again while application remains unknown.
recommendation: none
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_item
  request:
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: ambiguous
    applied: unknown
    id: unknown
  mutation: application unknown
- sequence: 4
  operation: query_correlation
  request: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1}
  response:
    outcome: found
    count: 1
    ids: [T-E1]
  mutation: none
- sequence: 5
  operation: get_item
  request: {id: T-E1}
  response:
    outcome: found
    id: T-E1
    approval: PR-72
    exact_match: false
    conflict: body belongs to PR-72
  mutation: none
```

No retry or mutation of `T-E1` was attempted. No live-provider access,
implementation, or worker dispatch occurred.

## F — conclusive not-applied failure

### Typed result: partial-publication recovery

The create failed conclusively before application. Correlation lookup then
confirmed absence. Tracker state is unchanged, there is no child ticket, and
there is no duplicate to reconcile. This run does not attempt a second create.

```yaml
source: SRC-H103@1
parent: P-H103
applied_operations: []
failed_or_unknown_operations:
  - create_item failed before application
affected_dependents: []
observed_tracker_state: P-H103 exists with no CAMP-73-T1 child
observed_frontier: []
gaps:
  - fixed item was not published
safest_recovery: >
  Repair the conclusive creation failure, then obtain fresh publication
  authority for a new run using the same frozen proposal and deterministic
  ticket key. This failed run performs no retry.
recommendation: none
```

### Simulated tracker operation log

```yaml
- sequence: 1
  operation: get_setup
  request: {}
  response:
    tracker: fixture-tracker
    compatible: true
    ready_state: ready-for-agent
    category_roles: [enhancement]
  mutation: none
- sequence: 2
  operation: get_parent
  request: {id: P-H103}
  response:
    id: P-H103
    exists: true
  mutation: none
- sequence: 3
  operation: create_item
  request:
    correlation: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
    item: exact fixed item payload above
  response:
    outcome: failure
    applied: false
    failure_point: before application
    id: null
  mutation: none
- sequence: 4
  operation: query_correlation
  request: {proposal_key: CAMP-73, ticket_key: CAMP-73-T1, approval: PR-73}
  response:
    outcome: not_found
    count: 0
    absence_conclusive: true
    ids: []
  mutation: none
```

The worker stopped after F. It did not retry, contact a live provider, start
implementation, or dispatch another worker.
