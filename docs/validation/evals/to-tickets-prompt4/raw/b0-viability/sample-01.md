# To Tickets Prompt 4 Evaluation

## 1. ordinary-feature

**Return: proposal awaiting approval — revision OF-R1**

### Source Trace

- Bounded source: the settled `ordinary-feature` case in the fixed packet.
- Publication authority: Owner A.
- Outcome: a user can submit an order through the API and observe the saved
  order; an operations user can observe that same new order in the existing
  dashboard.
- Accepted scope: API request/response, domain order creation, durable database
  storage, and existing-dashboard visibility.
- Exclusions: unrelated order workflows, dashboard redesign, and
  implementation technique not required by the settled behavior.
- Proof expectation: observable proof through the public API and existing
  operations dashboard, including persistence across the intervening read.
- Material source gaps: none stated.

### Coverage map

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | T1 acceptance and API proof |
| Save the order through the domain service and database | T1 acceptance and persistence proof |
| Return/allow observation of the saved order | T1 acceptance and API read-back proof |
| Show the new order in the existing operations dashboard | T1 acceptance and dashboard proof |
| API, domain service, database, and dashboard are involved | T1 expected production scope |
| Unrelated order workflows and dashboard redesign | Explicitly excluded by T1 scope fence |

### Ordered graph and predicted frontier

- Tracker order: T1.
- Blocking edges: none.
- Predicted ready frontier after publication: T1, because it is intended to be
  open, ready-for-agent, unclaimed, and has no true blocker.

### Proposed ticket T1 — Submit and observe a persisted order

- Form: one vertical behavior slice.
- Parent/source: `ordinary-feature` fixed-packet case, proposal OF-R1.
- Roles: Owner A holds publication authority; implementation is unclaimed.
- Why this slice: API submission and dashboard visibility are two observations
  of one persisted-order behavior. Splitting by API, service, database, or UI
  would leave tickets whose user-visible completion depended on sibling work.
- What to build: carry a valid order submission through the public API and
  domain service into durable storage, expose the saved result to the submitting
  user, and make the same order visible in the existing operations dashboard.
- Covered commitments: all four rows assigned to T1 in the coverage map.
- Observable acceptance:
  1. Given a valid order request, submitting through the public API succeeds and
     returns an identity or representation that identifies the saved order.
  2. Reading through the supported API observation path shows the persisted
     order with the submitted business values.
  3. An operations user using the existing dashboard can find that same order
     and distinguish it by the returned identity and material submitted values.
  4. The behavior crosses the real API, domain service, database, and dashboard
     boundaries rather than replacing any of them with a ticket-local stub.
- Highest meaningful proof seam: a focused end-to-end acceptance test that
  submits through the public API against the supported database, reads the
  saved order through the supported API path, and exercises the dashboard's
  production query/view boundary for the same identity.
- Dependency state: blockers `none`; consumes no predecessor outcome.
- Expected write scope: production behavior in the order API path, order-domain
  service, order persistence mapping/schema only if required, and the existing
  dashboard order query/view; focused acceptance/integration tests and their
  bounded fixtures.
- Semantic ownership: end-to-end creation and operations visibility of a newly
  persisted order.
- Parallel-safety note: this ticket owns one cross-component semantic seam.
  Work inside it should remain serial unless an implementation route later
  proves smaller scopes independently safe; filename separation alone is not
  evidence of independence.
- Shared resources and serial tripwires: the order persistence contract and the
  public order representation are shared seams; database-backed proof may be a
  serial resource. No sibling ticket is proposed.
- Scope fence: do not redesign the dashboard, alter unrelated order lifecycle
  behavior, introduce unrelated schema work, or choose implementation details
  beyond what this observable slice requires.

### Intended tracker mutations

After explicit approval of exactly OF-R1: create T1 under the approved parent,
set its ready-for-agent fields and roles, preserve the parent body except for
tracker-required child/order metadata, and create no blocking relationship.
Read back the parent, T1 body, roles, state, relationships, and resulting
frontier. No mutation is authorized yet.

**Safe continuation:** Owner A must explicitly approve revision OF-R1 exactly
as presented, or request a revised proposal.

## 2. source-conflict

**Return: source-gap packet**

- Evidence: the settled source permits refunds for 30 days; the approved ADR
  permits refunds for 14 days; neither authority supersedes the other.
- Material gap: the supported refund window is conflicting and determines
  acceptance, business behavior, and proof.
- Tracker state: unchanged; no slicing or mutation occurs.
- Required resolution: the responsible source/ADR authorities must reconcile
  the conflict and identify the controlling refund-window decision.
- Exact safe continuation: provide the reconciled, authoritative duration and
  any required ADR/source update, then rerun Trace before slicing.

## 3. setup-gap

**Return: setup precondition**

- Evidence: the target repository has neither a tracker contract nor a provider
  mapping, so compatibility and tracker-owned publication/read-back behavior
  cannot be established.
- Tracker state: unchanged; no proposal or mutation occurs.
- Exact safe continuation: run `$repo-bootstrap` to establish a compatible
  tracker contract and provider mapping, then rerun To Tickets from Trace.

## 4. economics

### Case A

- Size judgment: the single ready documentation correction is tiny
  (approximately two lines with a ten-minute proof), not substantial parallel
  work; coordination would cost more than it could save.
- Exactly one next recommendation: run `$implement` for the sole ready ticket.

### Case B

- Size judgment: both ready multi-module features are substantial, each
  requiring a full focused session, and the supplied evidence establishes
  semantic, production-scope, public-proof, fixture, resource, and tripwire
  isolation.
- Exactly one next recommendation: run `$parallel-implement` with their parent.

## 5. graph-distinctions

- Blockers: T1 has none; T2 has none; T3 is blocked by T1 because T3 consumes
  the schema outcome created by T1.
- Blocking edge: T1 -> T3.
- Tracker order: T2, T1, T3. This order is presentation/selection order, not an
  additional dependency.
- Overlap: T2 and T3 both predict writes to `registry.py`, but they own
  different semantics. The shared filename is overlap evidence, not a blocking
  edge and not proof that their behavior is semantically coupled.
- Serial tripwire: T2 and T3 both require the test database, which permits only
  one writer. They must not use that proof resource concurrently when T3
  becomes unblocked.
- Ready frontier: T2, T1. T3 is excluded because T1's required schema outcome
  is not yet satisfied.
- Exactly one next recommendation: run `$implement` for T2, the first ticket in
  tracker order; the stated economics/independence of the two current frontier
  tickets are insufficient to justify a parallel route.

## 6. incomplete-independence

- Execution judgment: both tickets are substantial, but disjoint predicted
  files establish neither semantic independence nor production/proof
  isolation. Public proof seams, shared fixtures, and scarce-resource or
  tripwire constraints remain unknown, so parallel eligibility is unproved and
  defaults to serial. No parent-delivery request overrides route selection.
- Exactly one next recommendation: run `$implement` for the first ticket in
  tracker order.

## 7. state-matrix

### Proposed acceptance

| Initial state | Access/profile coverage | Required observable behavior |
| --- | --- | --- |
| Absent | CLI and API; default and strict | The first request creates a valid cache through each access path. The result is usable immediately and remains usable after restart. |
| Reusable current | CLI and API; default and strict | A compatible current cache is reused without unnecessary replacement; both access paths observe equivalent current data before and after restart. |
| Legacy incompatible | CLI and API; default and strict | The legacy cache is never silently treated as current. The applicable profile produces its settled invalidation/rejection behavior, and any successful rebuild yields current data that remains valid after restart. |

For every initial-state row:

1. Reuse preserves a compatible cache and its observable identity/freshness
   signal where the product exposes one.
2. Invalidation prevents subsequent reads from returning the invalidated
   content and allows or requires a supported rebuild according to the
   profile's settled behavior.
3. Restart preserves reusable current state and does not resurrect absent,
   invalidated, or incompatible legacy state.
4. CLI and API agree on cache validity and resulting data under both default
   and strict profiles; any intentional profile-specific difference is
   asserted explicitly rather than omitted.

No listed axis is treated as non-applicable: all three initial states, both
access paths, both profiles, and reuse/invalidation/restart transitions are in
scope.

### Proposed proof

- Highest meaningful seam: parameterized acceptance tests through the real CLI
  command and public API, backed by the supported persistent cache.
- Seed three fixtures representing absent, reusable-current, and
  legacy-incompatible initial state.
- Cross each fixture with default and strict profiles and both access paths,
  asserting the observable result and persisted cache state.
- For each applicable combination, exercise reuse, explicit or
  behavior-triggered invalidation, and process restart; after restart, read
  again through both CLI and API.
- Inspect the persistent boundary to prove current data is retained when
  reusable, invalidated data is not resurrected, and legacy-incompatible data
  is not consumed as current.
- Keep focused unit/contract proof for cache-format classification and profile
  policy, but do not substitute it for the public CLI/API and restart
  acceptance seam.

## 8. migration

### Proposed work units

1. **T1 — Expand compatible protocol support.** Add the new protocol and record
   form beside the old forms. Old and new clients can operate concurrently,
   and existing records remain readable. This is a releasable expansion.
2. **T2 — Migrate records while both protocols remain supported.** Move records
   through an idempotent, resumable migration while old and new clients remain
   operable. This is a releasable migration phase, not permission to remove old
   support.
3. **T3 — Contract old protocol support.** Only after authoritative evidence
   shows all old client use has ended and compatibility/migration proof passes,
   remove old protocol and record handling.

### Edges

- T1 -> T2: migration consumes the compatible dual-protocol/dual-record
  capability.
- T2 -> T3: contraction consumes completed migration plus its evidence.
- T3 also has an external removal gate: confirmed end of all old-client use and
  passing compatibility proof. Mere tracker order or predicted file overlap is
  not a blocking edge.

### Acceptance and proof

**T1 acceptance**

- Old clients continue all supported operations against old and newly written
  compatible records.
- New clients complete the supported operations through the new protocol.
- Mixed old/new client traffic is supported without corrupting or hiding
  records.
- Deployment and rollback of the expansion leave the system operable.

**T1 proof:** protocol contract suites for old and new clients plus a
database-backed mixed-client acceptance test, including expand deployment and
rollback compatibility.

**T2 acceptance**

- Migration is resumable and idempotent; interruption and rerun do not lose,
  duplicate, or corrupt records.
- Old and new clients remain operable before, during, and after each migration
  batch.
- Every intermediate deployed stage is releasable and backward-compatible.
- Progress and residual old-form records are observable.

**T2 proof:** representative old/new/mixed record fixtures; interrupted,
resumed, and repeated migration tests; old/new client contract suites at each
intermediate checkpoint; count/content reconciliation and rollback/restart
proof.

**T3 acceptance**

- Authoritative usage evidence reports no remaining old clients.
- Migration reconciliation reports no records requiring old-only support.
- The full compatibility proof passes before removal.
- After removal, new clients and migrated records retain all supported
  behavior, and old-only code/schema is absent without leaving an inoperable
  rollback or deployment sequence.

**T3 proof:** archived zero-old-use evidence, migration reconciliation,
pre-contraction compatibility suite, post-contraction new-client acceptance
suite, and deployment/restart proof. T3 cannot be considered ready merely
because T2's code completed; both removal gates must be observed.

## 9. stale-approval

**Return: proposal awaiting approval**

- Evidence: R7 was approved, but the parent acceptance changed materially
  before publication. The approved source/proposal is therefore stale.
- Tracker state: unchanged.
- Mutation: none occurs.
- Exact safe continuation: reconcile the changed parent acceptance into a new
  identified proposal revision, regenerate affected coverage, tickets, graph,
  frontier, and intended mutations, then obtain explicit approval of that
  exact revision before publication.

## 10. partial-mutation

**Return: partial-publication recovery**

- Approved graph context: parent P, blocker T1, and dependent T2.
- Observed applied operations: read-back confirms P and T1 exist.
- Failed/unknown operation: T2 creation timed out; read-back cannot find T2,
  but the provider outcome remains unknown rather than safely assumed absent.
- Unrelated state: existing T9 is observed unchanged and is outside recovery
  scope.
- Graph mismatch: the intended dependent and its relationship are not
  verifiably present, so publication is not complete.
- Frontier risk: no ready frontier can be safely advertised from this partial
  graph. T1 may appear actionable in isolation, while a delayed/hidden T2 or a
  retry-created duplicate could produce inconsistent dependencies and packet
  state.
- Safest non-duplicating recovery: stop mutation; query the provider using the
  original idempotency key/external identity and reconcile T2 across direct
  lookup, parent children, and relationship reads. If T2 is found, verify and
  repair only the approved missing metadata/edge. If authoritative
  reconciliation proves it was never created, retry the same approved T2
  operation with the same idempotency identity, then read back P, T1, T2,
  roles, states, relationships, affected dependents, and frontier. Do not
  modify T9.
- Exact safe continuation: perform that bounded reconciliation and recovery
  before any implementation recommendation.

## 11. route-table

### (a) Empty frontier because blocker B7 is open

Exactly one next action: resolve blocker B7.

### (b) Singleton T1

Exactly one next action: run `$implement` for T1.

### (c) Non-empty frontier with parent-delivery explicitly requested

Exactly one next action: run `$parallel-implement` with the parent.

### (d) T1/T2 overlap on semantic ownership

Exactly one next action: run `$implement` for the first of T1/T2 in tracker
order.

### (e) T1/T2 are substantial and isolated

Exactly one next action: run `$parallel-implement` with the parent.

### (f) Independence is uncertain

Exactly one next action: run `$implement` for the first of T1/T2 in tracker
order.

## Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
