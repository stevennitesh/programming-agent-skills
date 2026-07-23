# Case 1: `ordinary-feature`

## Proposal R1 — awaiting approval

**Typed Return:** proposal awaiting approval.

**Source Trace.** Owner A has publication authority. The settled source requires
one end-to-end order behavior: a user submits an order through the API and can
observe the saved order, and an operations user can observe that same new order
in the existing dashboard. The named production surfaces are the API, domain
service, database, and dashboard. No exclusion, deferral, migration, or
additional supported-state branch is stated. The proof expectation is
caller-visible API persistence plus dashboard visibility.

**Coverage map**

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | T1 acceptance and API proof |
| Persist the submitted order | T1 acceptance and database-backed proof |
| Let the submitting user see the saved order | T1 acceptance and API read-back proof |
| Show the same new order to an operations user | T1 acceptance and dashboard proof |
| API, domain service, database, and dashboard are involved | T1 expected production scope |
| Work outside this order flow | T1 scope fence |

Every source-visible commitment has exactly one disposition. None is deferred,
excluded, or left without a ticket.

**Ordered graph and predicted frontier.** The graph is the singleton `T1`;
`T1` has no blockers or blocking edges. The predicted ready frontier after
verified publication is `[T1]`.

### T1 — Submit, persist, and surface a new order

- **Form:** one vertical behavior slice.
- **Roles:** publication authority `Owner A`; implementation owner unassigned;
  ticket open, unclaimed, ready-for-agent after verified publication.
- **Parent/source:** the bounded `ordinary-feature` settled source in this
  packet; Source Trace is the R1 summary above.
- **Why this slice:** the saved order and dashboard row are two observations of
  one submitted order. Completing them together proves the behavior through
  its highest meaningful user-facing boundaries without requiring a sibling.
- **What to build / covered commitments:** accept an order through the API,
  carry it through the domain service, persist it in the database, return or
  expose the saved order to the submitting user, and make that order visible
  in the existing operations dashboard.
- **Acceptance:** given a valid order submission, the API accepts it and
  identifies the saved order; a subsequent caller-visible read observes the
  persisted order with the submitted business data; an operations user opening
  or refreshing the existing dashboard sees that same order; the observations
  identify one persisted order rather than separate API and dashboard records.
- **Proof lane:** an integration or end-to-end test drives the public API
  submission against the supported persistence boundary, reads the saved order
  back through the public caller-facing seam, and exercises the existing
  operations dashboard boundary to verify the same order is displayed.
- **Blockers / consumed outcome:** none.
- **Expected write scope:** order API handling, order domain behavior, order
  persistence/mapping, dashboard order query/view, and focused proof for this
  flow.
- **Semantic ownership:** the create-and-observe order behavior.
- **Parallel safety:** this is the only slice. It spans shared order seams and
  supplies no basis for parallel subdivision; treat its internal work as
  serially owned.
- **Shared resources / serial tripwires:** shared order schema and persisted
  order representation across API, service, database, and dashboard; changes
  affecting that representation must remain under T1's single owner.
- **Scope fence:** no unrelated order workflows, dashboard redesign, API
  redesign, database cleanup, implementation of other operations features, or
  speculative migration.

**Intended tracker mutations after approval:** create T1 under the approved
parent with the body and metadata above, set its roles and ready state, record
that it has no blockers, and preserve the parent body except for required child
and ordering metadata. Read back the parent, T1 body, roles, state,
relationships, blockers, and resulting frontier.

**Observed tracker state:** unchanged; this is a no-mutation simulation and R1
has not been approved. **Safe continuation:** Owner A explicitly approves this
exact R1, or supplies a material correction that produces a new revision for
fresh approval.

# Case 2: `source-conflict`

## Source-gap packet

**Typed Return:** source-gap packet.

- **Evidence:** the settled source authorizes refunds for 30 days; the approved
  ADR authorizes refunds for 14 days; neither authority supersedes the other.
- **Material gap:** the allowed refund window changes product behavior,
  acceptance, proof, and scope. Choosing either value while slicing would
  silently override one settled authority.
- **Required resolution:** the source owner and ADR owner must reconcile the
  conflict and identify the controlling refund-window decision, including
  supersession or an explicit contextual distinction if both rules remain.
- **Observed tracker state:** unchanged. No tickets, edges, or proposal were
  created.
- **Exact safe continuation:** obtain the authoritative reconciliation, update
  the durable source trace, then restart Trace before any slicing.

# Case 3: `setup-gap`

## Setup precondition

**Typed Return:** setup precondition.

The repository lacks both the tracker contract and provider mapping, so ticket
readiness, transport, relationships, and mutation read-back cannot be defined.
The exact precondition is: run `$repo-bootstrap` to establish a compatible
tracker contract and provider mapping, then return to `$to-tickets` with that
setup surface identified.

**Observed tracker state:** unchanged; no provider mutation was attempted.
**Exact safe continuation:** satisfy the `$repo-bootstrap` precondition and
restart the setup gate.

# Case 4: `economics`

## Case A

The two-line documentation correction with a ten-minute proof is a small,
non-substantial work unit. Parallel coordination would cost more than the work
it could isolate.

**Exactly one next recommendation:** run `$implement` for the documentation
ticket.

## Case B

Each multi-module feature is substantial because each is expected to occupy a
full focused session. The two tickets are eligible for parallel execution:
they have distinct semantic owners, production scopes, public proof seams, and
fixtures, with no shared scarce resource or serial tripwire.

**Exactly one next recommendation:** run `$parallel-implement` with the parent.

# Case 5: `graph-distinctions`

- **True blockers:** `T1: none`; `T2: none`; `T3: T1`, because T3 consumes the
  schema created by T1. The required blocking edge is `T1 -> T3`.
- **Tracker order:** `T2`, `T1`, `T3`. This display/order fact creates no
  dependency.
- **Predicted overlap:** T2 and T3 both write `registry.py`, but their semantic
  ownership differs. Filename overlap is a coordination signal, not a blocker
  and not proof of semantic dependence.
- **Serial tripwire:** T2 and T3 both require the test database, which permits
  only one writer. They must not use that proof resource concurrently; this is
  a serial constraint, not a blocking edge.
- **Ready frontier:** `[T2, T1]` in tracker order. T3 is not on the frontier
  until T1's schema outcome is complete.

**Exactly one next recommendation:** run `$implement` for T2, the first ticket
in tracker order, because the graph contains a named serial proof-resource
tripwire.

# Case 6: `incomplete-independence`

Both tickets are substantial, but disjoint predicted files establish only
syntactic separation. Semantic ownership, public proof isolation, fixture
sharing, and scarce-resource constraints are unknown, so parallel eligibility
is not proved. No parent-delivery request overrides the route priority.

**Exactly one next recommendation:** run `$implement` for the first ticket in
tracker order.

# Case 7: `state-matrix`

## Proposed acceptance

The ticket is not complete merely because a happy-path cache hit works. Its
acceptance matrix is:

| Initial state | Access surface | Profile | Observable acceptance |
| --- | --- | --- | --- |
| Absent | CLI and API | Default and strict | The first access handles absence through the supported initialization path and returns a valid result; a subsequent access observes reusable current state. |
| Reusable current | CLI and API | Default and strict | Access returns the current cached result and demonstrably reuses the existing valid state without an unnecessary invalidation or restart. |
| Legacy incompatible | CLI and API | Default | The legacy state is never treated as current; it is invalidated and replaced through the supported path, after which access succeeds with current state. |
| Legacy incompatible | CLI and API | Strict | The legacy state is never silently reused or rewritten; access fails through the documented strict-profile incompatibility boundary, identifies the incompatible state, and leaves it recoverable. |

Transitions are also acceptance obligations:

- **Reuse:** reusable current state remains reusable across a second CLI call,
  a second API call, and a cross-surface CLI-to-API or API-to-CLI access.
- **Invalidation:** an explicit invalidation prevents the invalidated entry from
  being reused; the next supported default-profile access creates current
  state, while strict behavior remains consistent with its documented policy.
- **Restart:** after process restart, valid reusable state is reused and
  invalid or incompatible state is not silently promoted to current.
- Results exposed through CLI and API remain semantically consistent for the
  same profile and state branch.

## Proposed proof lane

Use a table-driven boundary suite over every row above, running the same state
fixtures through the public CLI and API seams under both profiles. Inspect
observable cache identity/version or hit/miss telemetry to distinguish reuse
from reconstruction. Add transition sequences for reuse, invalidation, and
restart, including cross-surface access. Prove strict-profile failure at its
public error boundary and prove that it does not mutate incompatible state.
The suite must isolate persisted state between rows and include a
restart-capable integration fixture; unit-only cache-method tests do not satisfy
the public proof seam.

# Case 8: `migration`

## Proposed expand-migrate-contract work units

### T1 — Expand with a backward-compatible protocol

- Add the new protocol form beside the old form while retaining old-client
  reads and writes.
- **Acceptance:** old clients continue to operate unchanged; new clients can
  use the new form; records produced by either supported path remain readable
  as required by both forms; the expanded deployment is independently operable
  and releasable.
- **Proof:** compatibility integration matrix for old/new client against the
  expanded service and both old/new record forms, plus rollback proof to the
  prior deployable state.

### T2 — Migrate records through the compatible form

- Migrate records while both client protocols remain supported, with resumable
  and observable progress.
- **Acceptance:** each migration stage is operable, releasable, restartable,
  and backward-compatible; old and new clients continue to work during partial
  migration; repeated or resumed migration does not corrupt or duplicate
  records; completion evidence accounts for all in-scope records.
- **Proof:** staged migration integration tests with mixed old/new records and
  clients, interruption/resume and idempotency checks, per-stage deployment
  smoke proof, and a completion audit.

### T3 — Contract old protocol support

- Remove the old form only after old use has ended and compatibility evidence
  has passed.
- **Acceptance:** observed old-client usage is zero under the approved
  completion criterion; T2's record audit is complete; the final compatibility
  suite proves supported new clients and migrated records; old protocol code
  is then removed without breaking the new public seam; the contracted stage
  is operable and releasable.
- **Proof:** usage/consumer inventory read-back, completed-record audit, final
  new-client integration and release proof, and a negative test showing the
  retired old protocol is no longer accepted.

## Edges

`T1 -> T2` because migration consumes the compatible expanded protocol.
`T2 -> T3` because contraction consumes completed migration evidence. T3 also
consumes the verified end of old usage. These are true blocking edges, yielding
the acyclic order T1, T2, T3; no phase may rely on a temporarily inoperable
deployment.

# Case 9: `stale-approval`

## Proposal awaiting fresh approval

**Typed Return:** proposal awaiting approval. R7 is stale because the parent's
acceptance changed materially after approval. Reconcile the changed parent
acceptance into a new identified revision, regenerate affected coverage,
tickets, acceptance, proof, graph, and frontier, and present that complete
revision for explicit approval.

**Mutation occurs:** no. **Observed tracker state:** unchanged by this attempt.
**Exact safe continuation:** approve the reconciled replacement revision
explicitly before publication.

# Case 10: `partial-mutation`

## Partial-publication recovery

**Typed Return:** partial-publication recovery.

- **Approved intent:** publish parent P, blocker T1, dependent T2, and their
  approved relationship/state.
- **Observed applied operations:** read-back proves P and T1 exist.
- **Failed or unknown operations:** T2 creation timed out. Read-back cannot find
  T2, but the provider outcome remains unknown; absence from this read is not
  proof that the create never committed.
- **Unrelated state:** existing T9 is observed unchanged and is outside the
  recovery scope.
- **Frontier risk:** the approved graph is incomplete and T2 may be absent,
  delayed, duplicated under a provider-generated identity, or missing its
  relationship to T1. Therefore no complete ready frontier can be asserted,
  and P/T1 must not be handed off as though publication succeeded.
- **Recovery:** stop further mutation. Reconcile the timed-out request using
  its idempotency key, correlation data, exact parent, and exhaustive provider
  lookup/read-back. If T2 is found, verify and repair only the approved missing
  relationship or metadata, then read back the entire graph. If authoritative
  reconciliation proves T2 was not created, retry the same approved T2 create
  with the original idempotency identity, not a fresh duplicate-producing
  request. Leave T9 untouched. If authoritative state cannot be established,
  remain blocked and escalate to the tracker owner.

**Exact safe continuation:** perform the non-duplicating T2 reconciliation and
full graph read-back before declaring any frontier or dispatching work.

# Case 11: `route-table`

## (a) Empty frontier because B7 is open

**Exactly one next action:** resolve blocker B7.

## (b) Singleton T1

**Exactly one next action:** run `$implement` for T1.

## (c) Non-empty frontier with an explicitly requested parent-delivery run

**Exactly one next action:** run `$parallel-implement` with the parent.

## (d) T1/T2 overlap on semantic ownership

**Exactly one next action:** run `$implement` for the first ticket in tracker
order.

## (e) T1/T2 are substantial and isolated

Their semantics, production scopes, proof seams, resources, and tripwires are
isolated.

**Exactly one next action:** run `$parallel-implement` with the parent.

## (f) Independence is uncertain

**Exactly one next action:** run `$implement` for the first ticket in tracker
order.

# Actions actually performed:

- No tracker mutation, skill invocation, implementation, or dispatch was
  performed.
