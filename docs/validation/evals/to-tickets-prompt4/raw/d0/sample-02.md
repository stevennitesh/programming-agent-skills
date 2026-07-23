# Case 1: ordinary-feature

## Proposal R1 awaiting approval

**Typed Return:** proposal awaiting approval. No tracker mutation occurs unless
Owner A explicitly approves this exact revision.

### Source Trace

- Source owner and publication authority: Owner A.
- Settled outcome: an API user can submit an order and observe the saved order;
  an operations user can observe that new order in the existing dashboard.
- In scope: API submission and response, domain order creation, persistence,
  and dashboard visibility.
- Excluded: redesigning the dashboard, adding unrelated order operations, and
  implementation-specific helpers or file choices.
- Proof expectation: caller-visible API proof through persistence and
  operator-visible dashboard proof.
- Material source gaps: none stated.

### Coverage map

| Source commitment or boundary | Disposition |
|---|---|
| Submit an order through the API | T1 |
| Create the order through the domain service | T1 |
| Save and return the order | T1 |
| Show the new saved order in the existing dashboard | T2 |
| Dashboard redesign and unrelated order operations | Explicitly excluded |

### Ordered graph and predicted frontier

`T1 -> T2`. T2 consumes the persisted-order outcome established by T1.
The predicted initial ready frontier is `T1`.

### Intended tracker mutations

After approval and a freshness check: create T1 and T2 under the bounded source,
assign Owner A's approved roles and open ready state, create the blocking edge
T1 blocks T2, and record packet metadata for proposal R1. No parent-body change
is proposed beyond tracker-required child and ordering metadata.

### T1 — Submit and persist an order through the API

- **Form and roles:** vertical behavior slice; delivery owner unclaimed,
  publication authority Owner A.
- **Blockers / consumed outcome:** none.
- **Why this slice:** it establishes one independently observable public
  capability and the persisted-order contract consumed by the dashboard.
- **Build and covered commitments:** accept a valid order submission at the
  existing API boundary, create it through the domain service, persist it, and
  return an observable representation of the saved order.
- **Acceptance:** a valid API request succeeds; the response identifies the
  created order; a read through the supported persistence-facing/public read
  seam observes matching saved data; invalid input follows the existing API
  error contract and does not persist an order.
- **Proof lane:** API-level behavior test using the supported database boundary,
  proving request-to-domain-to-persistence behavior rather than isolated layer
  mocks.
- **Expected write scope:** order API, order-domain behavior, persistence
  integration, and their focused tests; exact files remain implementation-owned.
- **Semantic ownership / shared resources / parallel safety:** owns order
  creation and persistence semantics. It may share order representations and
  the test database with T2, so it is not proposed for concurrent execution
  with T2.
- **Execution profile / state matrix:** ordinary focused implementation. The
  source supplies no migration or supported-state branches; migration and
  legacy-state axes are evidenced non-applicable to this proposal.
- **Scope fence:** no dashboard work, unrelated order lifecycle operations,
  schema redesign beyond what the settled order requires, or implementation
  dispatch.

### T2 — Display a newly persisted order in the existing dashboard

- **Form and roles:** dependent vertical behavior slice; delivery owner
  unclaimed, publication authority Owner A.
- **Blockers / consumed outcome:** blocked by T1; consumes T1's persisted-order
  contract.
- **Why this slice:** operator visibility has a distinct user, public proof
  seam, and independently judged outcome after persistence exists.
- **Build and covered commitments:** make the existing dashboard's supported
  order view include an order created through the API.
- **Acceptance:** after an order is created through the supported API, an
  operations user opening or refreshing the existing dashboard sees that order
  with the source-required identifying data; existing order display remains
  operable.
- **Proof lane:** dashboard boundary test seeded through the public API or its
  committed persisted-order contract, plus focused regression proof for the
  existing view.
- **Expected write scope:** dashboard order query/presentation seam and focused
  tests; exact files remain implementation-owned.
- **Semantic ownership / shared resources / parallel safety:** owns operator
  order-visibility semantics. It shares the persisted-order contract and may
  share the test database with T1; the dependency and shared proof resource
  require serial execution.
- **Execution profile / state matrix:** dependent focused implementation after
  T1. No migration or legacy-state behavior is present in the settled source.
- **Scope fence:** no order-creation changes, dashboard redesign, unrelated
  operational views, or implementation dispatch.

**Safe continuation:** Owner A approves R1 exactly, or supplies changes for a
new revision. Publication must then recheck source, parent, target, and
relationships before any mutation.

# Case 2: source-conflict

**Typed Return:** source-gap packet.

- **Evidence:** the settled source permits refunds for 30 days; an approved ADR
  permits them for 14 days; neither authority supersedes the other.
- **Material gap:** the refund eligibility contract is conflicting, and either
  choice changes acceptance, implementation scope, and proof.
- **Tracker state:** unchanged.
- **Safe continuation:** the source owner and ADR authority must reconcile the
  refund window and identify the superseding durable decision. Resume Trace
  only after that decision; do not slice tickets from either value.

# Case 3: setup-gap

**Typed Return:** setup precondition.

- **Evidence:** the target repository has neither a tracker contract nor a
  provider mapping, so readiness, roles, relationships, and mutation read-back
  cannot be established.
- **Tracker state:** unchanged.
- **Safe continuation:** run `$repo-bootstrap` to establish a compatible tracker
  contract and provider mapping, then restart source tracing. This simulation
  does not invoke that skill.

# Case 4: economics

## Case A

The two-line documentation correction is small, with only a ten-minute proof;
dispatch overhead would dominate and there is no substantial parallel graph.
**Exactly one next recommendation:** `$implement` the ready documentation
ticket.

## Case B

Both tickets are substantial enough to occupy full focused sessions, and the
given evidence establishes separation across semantic ownership, production
scope, public proof seams, fixtures, resources, and tripwires. Parallel work
has credible economic value.
**Exactly one next recommendation:** `$parallel-implement` with their parent.

# Case 5: graph-distinctions

- **True blockers:** T1 blocks T3 because T3 consumes the schema created by T1.
  T1 and T2 have no blockers.
- **Tracker order:** T2, T1, T3. Dependency order constrains T3 to follow T1;
  it does not require T1 to precede independent T2.
- **Overlap:** T2 and T3 both predict writes to `registry.py`, but their stated
  semantic ownership is distinct. Filename overlap alone is not a dependency
  or proof of semantic conflict.
- **Serial tripwire:** T2 and T3 both require the one-writer test database and
  therefore may not execute their database-writing proof concurrently.
- **Initial ready frontier:** T2 and T1. T3 is blocked on T1.
- **Execution judgment:** the graph is not globally parallel-safe merely because
  its initial frontier has two tickets; its later T2/T3 proof lanes require
  serialization.
- **Exactly one next recommendation:** `$implement` T2, the first ticket in
  tracker order.

# Case 6: incomplete-independence

Disjoint predicted files do not establish semantic, production, proof, fixture,
or resource independence. Parallel safety and economics therefore remain
uncertain, and no explicit parent-delivery run overrides that uncertainty.
**Exactly one next recommendation:** `$implement` T1, the first ticket in
tracker order.

# Case 7: state-matrix

## Proposed acceptance

| Initial state | Access/profile | Required observable behavior |
|---|---|---|
| Cache absent | CLI and API; default and strict | Create a valid current cache, return the requested result, and leave it reusable. |
| Reusable current cache | CLI and API; default and strict | Reuse the cache without unnecessary invalidation or rebuild and return an equivalent result. |
| Legacy incompatible cache | CLI and API; default | Detect incompatibility, invalidate safely, rebuild current state, and return the result without consuming stale data. |
| Legacy incompatible cache | CLI and API; strict | Detect and reject or stop according to the strict-profile contract; never silently consume or overwrite incompatible state. |

Across all applicable rows, a reuse transition preserves current valid state,
an invalidation transition cannot expose stale results as current, and a
restart after successful creation or rebuild observes reusable current state.
A restart after an interrupted invalidation/rebuild must resolve to a supported
absent or current state, not a partially valid cache.

## Proposed proof content

- A parameterized public-boundary suite exercises CLI and API against absent,
  reusable-current, and legacy-incompatible fixtures under both profiles.
- Proof observes result equivalence, whether reuse or rebuild occurred, and the
  final durable cache state; it does not infer behavior solely from helper
  calls.
- Transition tests cover create-to-restart, current-reuse-to-restart,
  legacy-invalidation-to-rebuild-to-restart, and interruption followed by
  restart.
- Strict-profile proof establishes its explicit incompatible-state failure
  behavior and absence of silent mutation; default-profile proof establishes
  safe invalidation and recovery.
- Regression proof confirms repeated CLI/API access converges on the same
  supported current representation.

# Case 8: migration

## Proposed work units and edges

1. **T1 — Expand for protocol coexistence.** Add the backward-compatible
   protocol/record capability needed for old and new clients to operate
   together. No destructive switch.
2. **T2 — Migrate records under coexistence.** Incrementally migrate records
   while both client generations remain supported. **Edge:** T1 blocks T2.
3. **T3 — Prove completion and contract old support.** Establish that all
   records and all active/deployed clients have left old use, prove new-only
   compatibility and rollback/release safety, then remove old support.
   **Edge:** T2 blocks T3. T1's coexistence capability remains in force until
   T3's gates pass.

The ordered graph is `T1 -> T2 -> T3`; each unit is separately releasable and
rollback-safe.

## Acceptance and proof

### T1

- Old client + old record, old client + compatible expanded record, new client
  + old record, and new client + expanded record remain operable wherever the
  protocol permits them during coexistence.
- Deployment of the expansion alone is releasable and does not force migration
  or strand old clients.
- Public protocol compatibility tests cover both client generations and record
  representations; staged-deployment and rollback proof demonstrates a mixed
  fleet remains operable.

### T2

- Migration is resumable and idempotent; mixed migrated/unmigrated records stay
  readable and writable by every client generation promised for this phase.
- Each batch leaves a deployable, releasable state; interruption and restart do
  not corrupt records, duplicate effects, or require an atomic cutover.
- Proof covers empty, partially migrated, fully migrated, interrupted, resumed,
  and rolled-back stage boundaries through supported client/protocol seams,
  with migration counts and record integrity observed.

### T3

- Removal is forbidden until authoritative evidence shows zero remaining old
  records and zero active or deployed old-client use.
- After removal, new clients operate over fully migrated records; old protocol
  use fails only according to the approved retirement contract.
- Proof includes the completion audit, new-only public compatibility suite,
  deployment and rollback/release proof, and a negative check that the removal
  gate refuses contraction while any old use remains.

# Case 9: stale-approval

**Typed Return:** proposal awaiting approval.

- **Evidence:** Owner A approved R7, but the parent's acceptance changed
  materially before publication. R7 is no longer fresh because its coverage,
  ticket acceptance, or proof may no longer match the parent.
- **Tracker state and mutation:** unchanged; no mutation occurs.
- **Safe continuation:** reconcile the changed parent into a new identified
  proposal revision, rerun coverage and graph checks, and obtain explicit
  approval of that exact revision before publication.

# Case 10: partial-mutation

**Typed Return:** partial-publication recovery.

- **Approved revision:** the previously approved graph containing parent P,
  blocker T1, and dependent T2.
- **Observed applied operations:** read-back confirms P and T1.
- **Failed or unknown operations:** T2 creation timed out. Read-back cannot find
  T2, but the provider outcome remains unknown; absence from the read surface
  does not safely prove that creation never committed.
- **Unrelated state:** existing T9 is observed unchanged.
- **Graph/frontier risk:** the intended graph is unverified and incomplete. If
  T2 committed but is not yet visible, retrying could duplicate it or its
  relationships. If it did not commit, T1 may appear as a misleading singleton
  frontier while the approved dependent and edge are missing. No ticket should
  be dispatched from this frontier.
- **Tracker state:** partially changed; do not roll back P or T1 automatically
  and do not alter T9.
- **Safest non-duplicating recovery:** reconcile the original mutation's stable
  operation/idempotency identity and provider state, repeat authoritative
  read-back for T2 and its relationships, create T2 only after absence is
  conclusively established using the same non-duplicating identity, then
  read back P, T1, T2, their edge, roles, states, and resulting frontier. Return
  for fresh approval if recovery would materially change the approved graph.

# Case 11: route-table

| Frontier | Exactly one next action |
|---|---|
| (a) Empty because B7 is open | Resolve blocker B7. |
| (b) Singleton T1 | Recommend `$implement` for T1. |
| (c) Non-empty; parent-delivery run explicitly requested | Recommend `$parallel-implement` with the parent. |
| (d) T1/T2 overlap on semantic ownership | Recommend `$implement` for T1, first in tracker order. |
| (e) T1/T2 are substantial and isolated across semantics, production, proof, resources, and tripwires | Recommend `$parallel-implement` with the parent. |
| (f) Independence is uncertain | Recommend `$implement` for T1, first in tracker order. |

# Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
