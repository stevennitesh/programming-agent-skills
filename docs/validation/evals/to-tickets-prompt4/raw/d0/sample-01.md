# 1. ordinary-feature

## Proposal R1 awaiting approval

**Typed Return:** proposal awaiting approval. No tracker mutation occurs unless
Owner A explicitly approves this exact revision.

**Source Trace:** Owner A has publication authority. The settled source requires
two observable outcomes: an API user can submit an order and retrieve the saved
order, and an operations user can see that order in the existing dashboard.
The named production seams are the API, domain service, database, and dashboard.
No implementation technique or file-level design is settled by the source.

### Coverage map

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | T1 |
| Save the accepted order through the domain/database boundary | T1 |
| Retrieve and observe the saved order through the API | T1 |
| Show the new order in the existing operations dashboard | T2 |
| API, domain service, and database production scope | T1 |
| Dashboard production scope and its persisted-order read seam | T2 |
| Patch design, helper choice, and exact files | Left to implementation |
| Work outside order submission/retrieval/dashboard visibility | Explicitly excluded |

### Ordered graph and predicted frontier

`T1 -> T2`. T1 has no blocker. T2 consumes T1's persisted-order outcome and is
blocked by T1. The predicted initial ready frontier is `{T1}`.

### T1 — Persist an API-submitted order and expose it through the API

- **Form and roles:** bounded feature slice; implementation owner unassigned;
  Owner A is source/publication authority.
- **Blockers / consumed outcome:** none.
- **Why this slice:** it closes the caller-visible write/read boundary and
  produces the persisted-order contract consumed by dashboard visibility.
- **Build and commitments:** accept a valid order through the supported API,
  apply the domain service behavior, persist it in the database, and make the
  saved order observable through the supported API read behavior.
- **Acceptance:** submitting a valid order returns the contractually supported
  result; a subsequent API read observes the same saved order and its required
  identity/data; the database-backed path, rather than a test-only substitute,
  is exercised; supported failures do not report an unsaved order as saved.
- **Highest proof seam / proof lane:** caller-facing API integration proof
  through the real domain-service and test-database boundary, including
  submit-then-read.
- **Expected write scope:** API order endpoint/contract, order domain service,
  order persistence mapping/repository, and their focused tests.
- **Semantic ownership:** order submission and persisted-order retrieval.
- **Shared resources / serial tripwires:** database schema and order API
  contract are shared seams; schema or public-contract changes serialize with
  consumers until proved stable.
- **Parallel safety:** not safe to execute T2 against an unsettled persisted
  contract; T1 is first.
- **Execution profile:** one focused implementation run with API integration
  proof.
- **Scope fence:** no dashboard work, unrelated order workflows, broad database
  refactor, or new operational features.
- **Source/durable context:** this packet's settled ordinary-feature source and
  the repository's API/domain/database contracts.

### T2 — Display a newly persisted order in the existing operations dashboard

- **Form and roles:** bounded consumer feature slice; implementation owner
  unassigned; Owner A is source/publication authority.
- **Blockers / consumed outcome:** blocked by T1; consumes T1's persisted-order
  read contract.
- **Why this slice:** it owns a separate operations-facing proof seam while
  preserving the dependency on the producer contract.
- **Build and commitments:** make a newly saved order appear in the existing
  dashboard using the supported persisted-order read path.
- **Acceptance:** with a contract-valid persisted order fixture, the existing
  dashboard renders that order with the required identifying information; an
  end-to-end check using an order created through T1's API confirms it becomes
  visible; unrelated dashboard data remains supported.
- **Highest proof seam / proof lane:** dashboard-facing integration proof
  against the stable persisted-order contract, plus submit-to-dashboard
  acceptance after T1 is complete. The fixture-based consumer proof lets T2 be
  judged independently once the consumed contract exists.
- **Expected write scope:** dashboard order query/adapter, existing dashboard
  presentation seam, and focused dashboard/integration tests.
- **Semantic ownership:** operations visibility of persisted orders.
- **Shared resources / serial tripwires:** persisted-order contract is shared
  with T1; changes to it serialize until T1 is complete.
- **Parallel safety:** blocked rather than parallel-ready because its production
  contract is produced by T1.
- **Execution profile:** one focused consumer implementation run followed by
  the submit-to-dashboard proof.
- **Scope fence:** no changes to order submission semantics, unrelated dashboard
  redesign, analytics, or operational actions.
- **Source/durable context:** this packet's settled ordinary-feature source,
  T1's resulting public contract, and existing dashboard conventions.

**Intended tracker mutations after approval:** create T1 and T2 with the fields
above, add the blocking edge `T1 -> T2`, set T1 ready and T2 blocked, and
read back the parent, both ticket bodies/roles/states, the edge, and the ready
frontier. **Safe continuation:** Owner A approves or amends Proposal R1.

# 2. source-conflict

**Typed Return:** source-gap packet.

- **Evidence:** the settled source permits refunds for 30 days; the approved
  ADR permits refunds for 14 days; neither authority supersedes the other.
- **Material gap:** the supported refund window changes acceptance, domain
  behavior, and proof, so slicing would encode an unapproved choice.
- **Tracker state:** unchanged; no proposal or ticket is created.
- **Required resolution:** the source owner and ADR authority must reconcile the
  refund window and identify the superseding durable decision.
- **Safe continuation:** rerun Trace against the reconciled source and ADR.

# 3. setup-gap

**Typed Return:** setup precondition.

- **Evidence:** the target repository has neither a tracker contract nor a
  provider mapping, so readiness fields, transport, relationships, and
  Mutation read-back cannot be established.
- **Tracker state:** unchanged.
- **Exact precondition:** run `$repo-bootstrap` to establish a compatible
  tracker contract and provider mapping, then verify that setup before returning
  to ticket slicing.
- **Safe continuation:** satisfy that precondition; do not draft or publish
  tickets against an undefined tracker surface.

# 4. economics

## Case A

The ready documentation correction is tiny: two lines, about ten minutes, and
one direct proof. Dispatch overhead would dominate the work. **Exactly one next
recommendation:** run `$implement` for the documentation ticket.

## Case B

Both ready features are substantial enough to occupy a focused session, while
semantic ownership, production scope, public proof seam, fixtures, resources,
and tripwires are isolated. The parallel work has enough duration to repay
coordination cost. **Exactly one next recommendation:** run
`$parallel-implement` with their parent.

# 5. graph-distinctions

- **Blockers:** T2 has none; T1 has none; T3 is blocked by T1 because it consumes
  the schema created by T1.
- **Tracker ordering:** T2, T1, T3.
- **Overlap:** T2 and T3 both predict writes to `registry.py`, but they own
  different semantics. The filename overlap is not a dependency and does not
  by itself merge their ownership.
- **Tripwire:** T2 and T3 must not use the test database concurrently because it
  permits only one writer. That serial constraint remains even though their
  semantics differ.
- **Ready frontier:** `{T2, T1}`; T3 is excluded until T1 completes.
- **Exactly one next recommendation:** run `$implement` for T2, the first ticket
  in tracker order, because the graph contains a shared proof resource/serial
  tripwire.

# 6. incomplete-independence

Disjoint predicted files establish neither semantic independence nor safe
parallel execution. Public proof seams, shared fixtures, resource constraints,
and semantic ownership are all unknown, so both the independence judgment and
the economics of dispatch remain uncertain. The tickets must not be labeled
parallel-safe from file predictions alone. **Exactly one next recommendation:**
run `$implement` for T1, the first ticket in tracker order.

# 7. state-matrix

## Acceptance

| Initial state | Access/profile | Required observable behavior |
| --- | --- | --- |
| Absent | CLI and API; default and strict | Create usable current cache state; both access paths return contract-equivalent results for the same input. |
| Reusable current | CLI and API; default and strict | Reuse the current cache without needless invalidation or restart; expose the same supported result through both access paths. |
| Legacy incompatible | CLI and API; default | Invalidate incompatible state, rebuild current state, and complete successfully without treating legacy contents as current. |
| Legacy incompatible | CLI and API; strict | Reject or invalidate according to the settled strict contract, never silently reuse legacy state; after the supported recovery/restart, current state is usable. |

Across the matrix, a reuse transition preserves valid current state, an
invalidation transition makes incompatible state unavailable before rebuild,
and a restart observes only complete supported state rather than a partial
write. CLI and API behavior may differ in presentation but not in cache-state
semantics. Both default and strict profiles must make their legacy-state choice
observable.

## Proof content

- Parameterized boundary tests cover all 12 combinations of three initial
  states, two access paths, and two profiles, recording reuse, invalidation,
  rebuild/rejection, and resulting state.
- Instrumented integration proof distinguishes reuse from rebuild and verifies
  that reusable current state is not rewritten.
- Legacy fixtures prove incompatible state is never consumed as current; each
  profile's required reject-or-rebuild behavior is asserted through both CLI
  and API seams.
- Transition tests interrupt after invalidation/write boundaries and restart,
  proving restart yields a complete current cache or the supported recoverable
  absent state, never partial state.
- Cross-access proof creates or rebuilds through one access path and reuses
  through the other under both profiles.

# 8. migration

## Proposed work units and edges

`T1 -> T2 -> T3`.

### T1 — Expand: deploy coexistence support

- **Acceptance:** old and new clients can operate against the same deployed
  service; both old and new record forms are read safely; new writes follow the
  approved compatibility strategy; the stage is independently operable,
  releasable, and rollback-safe without requiring T2.
- **Proof:** protocol integration tests for old/new clients against old/new
  record fixtures, mixed-operation tests, and release/rollback smoke proof.

### T2 — Migrate: move records and active use to the new protocol

- **Blocker:** T1.
- **Acceptance:** migration is resumable and idempotent; mixed populations
  remain operable throughout; each deployable batch is releasable; counts and
  reconciliation expose migrated, remaining, failed, and retried records; all
  active clients are moved to the new protocol; evidence shows no remaining
  old use while compatibility support is still present.
- **Proof:** staged migration over mixed fixtures, interruption/resume and retry
  tests, per-batch reconciliation, old/new client canaries during migration,
  and production-equivalent evidence for zero remaining old records and calls.

### T3 — Contract: prove compatibility, then remove old support

- **Blocker:** T2, specifically its verified zero-old-use outcome.
- **Acceptance:** before removal, the new client works with every migrated
  record and no old client, old record, or old protocol use remains; removing
  old support preserves new-client behavior; the final stage is operable,
  releasable, and rollback has an explicit safe boundary.
- **Proof:** read-back of zero-old-use evidence, full new-client compatibility
  suite over migrated records, negative proof that old protocol use is rejected
  only after the gate, and final release/rollback smoke proof.

The edges are outcome dependencies, not mere desired ordering: T2 consumes
T1's coexistence capability, and T3 consumes T2's proved absence of old use.
No unit permits an inoperable intermediate deployment.

# 9. stale-approval

**Typed Return:** proposal awaiting approval.

- **Evidence:** Owner A approved R7, but the parent's acceptance changed
  materially afterward. R7 is no longer fresh and therefore cannot authorize
  publication.
- **Mutation:** none occurs.
- **Tracker state:** unchanged.
- **Safe continuation:** reconcile the changed parent into a newly identified
  proposal revision, repeat coverage/graph/acceptance checks, and obtain
  explicit approval of that exact revision before publication.

# 10. partial-mutation

**Typed Return:** partial-publication recovery.

- **Approved revision:** the previously approved graph containing parent P,
  blocker T1, and dependent T2 remains the recovery reference.
- **Observed applied operations:** read-back confirms P and T1 exist.
- **Failed/unknown operation:** T2 creation timed out. The current read-back
  cannot find T2, but the timeout leaves provider state unknown until an
  authoritative identifier/idempotency reconciliation proves absence.
- **Unaffected state:** unrelated T9 is observed unchanged.
- **Frontier risk:** the graph is incomplete, so any apparent readiness of T1
  cannot be treated as the approved graph's verified ready frontier; T2 could
  still exist under an unobserved identifier, and a blind retry could duplicate
  it. No implementation route is recommended.
- **Safest non-duplicating recovery:** stop mutation; query by the original
  provider request identifier, idempotency key, parent relationship, and unique
  approved ticket identity. If T2 is found, reconcile and read back its body,
  state, edge, and affected frontier. Only if authoritative reconciliation
  proves it absent, retry exactly the missing T2 creation with the same
  idempotency identity, then read back P, T1, T2, their relationship, T9, and
  the complete frontier.
- **Safe continuation:** perform that bounded reconciliation; do not recreate P
  or T1 and do not begin implementation.

# 11. route-table

| Frontier | Exactly one next action |
| --- | --- |
| (a) Empty because B7 is open | Resolve blocker B7. |
| (b) Singleton T1 | Run `$implement` for T1. |
| (c) Non-empty and a parent-delivery run was explicitly requested | Run `$parallel-implement` with the parent. |
| (d) T1/T2 overlap on semantic ownership | Run `$implement` for T1, first in tracker order. |
| (e) T1/T2 are substantial and isolated across semantics, production, proof, resources, and tripwires | Run `$parallel-implement` with the parent. |
| (f) Independence is uncertain | Run `$implement` for T1, first in tracker order. |

Actions actually performed:

- No tracker mutation, skill invocation, implementation, or dispatch was
  performed.
