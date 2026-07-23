# Case 1: `ordinary-feature`

## Proposal awaiting approval: `ordinary-feature-R1`

**Typed Return:** proposal awaiting approval. No tracker state changes have been
made.

### Source Trace summary

- Bounded source: fixed `ordinary-feature` case supplied by Owner A.
- Source owner and publication authority: Owner A.
- Outcome: a customer submits an order through the API, the order is saved and
  returned observably, and an operations user can see that same new order in
  the existing dashboard.
- Accepted implementation commitments: API submission, domain processing,
  durable database persistence, API visibility of the saved order, and
  visibility in the existing operations dashboard.
- Scope: the API, domain service, database, and existing dashboard behavior
  needed for this one end-to-end order flow.
- Exclusions: dashboard redesign, unrelated order operations, alternate
  submission channels, and implementation-owned choices of helpers, exact
  files, or test layout.
- Proof expectation: exercise the public API through persistence and the
  existing dashboard read path, correlating the displayed order to the API
  result.
- Material gaps: none in the supplied settled behavior. Implementation
  technique remains with the delivery owner.

### Coverage map

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | T1 acceptance and API proof |
| Save the submitted order | T1 acceptance and persistence proof |
| Let the submitting user see the saved order | T1 acceptance and API response/read proof |
| Show the same new order to operations in the existing dashboard | T1 acceptance and dashboard proof |
| API, domain service, database, and dashboard are involved | T1 expected production scope |
| Existing dashboard is the UI boundary | T1 scope fence; dashboard redesign excluded |

Every visible commitment has exactly one disposition. There are no deferrals,
rejections, or no-ticket items.

### Ordered graph and predicted frontier

- Tracker order: T1.
- Blocking edges: none.
- Predicted ready frontier after publication: T1, because it would be open,
  ready-for-agent, unclaimed, and have no blockers.

### Intended tracker mutations

1. Create T1 under the bounded `ordinary-feature` source/parent.
2. Assign Owner A as source owner and publication approver; leave the delivery
   claim unassigned.
3. Mark T1 ready-for-agent and open with no blocker relationships.
4. Record the Source Trace, acceptance, proof lane, write scope,
   parallel-safety note, and scope fence below.

### T1 — Submit, persist, and surface a new order

- **Work-unit form:** one vertical behavior slice.
- **Roles:** Owner A is source owner and publication approver; delivery owner is
  unassigned until claimed.
- **Parent/source reference:** `ordinary-feature`, proposal
  `ordinary-feature-R1`.
- **Why this slice:** the customer submission and operations visibility are one
  observable order lifecycle. Splitting by API, service, database, or
  dashboard would create layer tickets that cannot independently prove the
  settled outcome.
- **What to build / covered commitments:** accept a valid order through the
  public API, process and durably save it through the domain and persistence
  paths, expose the saved order to the submitting user, and make that same
  order visible in the existing operations dashboard.
- **Blockers:** none.
- **Consumed predecessor outcome:** none.
- **Acceptance:**
  - Given a valid order submission, the public API accepts it and returns or
    otherwise exposes a stable identifier and the saved order state.
  - Reading authoritative persistence by that identifier shows one saved order
    whose material values match the accepted submission.
  - The existing operations dashboard shows that same order, correlated by the
    stable identifier and material values.
  - A failed submission does not appear as a successfully saved or displayed
    order.
- **Highest meaningful proof seam:** a focused caller-facing scenario starting
  at the real API boundary and observing both authoritative persistence and the
  existing dashboard read boundary.
- **Proof lane:** submit a representative valid order through the API; assert
  its returned/surfaced identity and saved values; query the authoritative
  persistence path; then load the existing dashboard through its production
  data path and assert the same identity and values. Include the rejected-path
  assertion that no successful order is surfaced after submission failure.
- **Expected production write scope:** the order API handler/contract, order
  domain-service behavior, order persistence schema or repository as required,
  and the existing dashboard's order query/presentation path. Tests and
  fixtures may change only where needed to prove this slice.
- **Semantic ownership:** creation and visibility of a newly submitted order
  across the customer and operations boundaries.
- **Shared resources and serial tripwires:** the order persistence contract and
  public order representation are shared seams; coordinate serially with any
  concurrent work changing either seam. No separate concurrent sibling is
  proposed.
- **Parallel-safety note:** T1 is internally cross-component and should have
  one delivery owner. Disjoint component files would not make its API,
  persistence, and dashboard semantics independent.
- **Execution profile:** not applicable; the proposal has one vertical slice,
  no parent-delivery run was requested, and no sibling parallel decision
  exists.
- **State-boundary matrix:** no legacy/current-state, profile, restart, or
  migration branches are evidenced by this bounded source, so those axes are
  non-applicable. The applicable success and failed-submission branches are
  included in acceptance and proof.
- **Scope fence:** do not redesign the dashboard, add alternate order channels,
  implement unrelated order lifecycle operations, or prescribe exact helpers,
  files, and test implementation beyond what the production outcome and proof
  require.

**Approval gate:** Owner A must explicitly approve exactly
`ordinary-feature-R1` before any listed mutation. The safe continuation is to
approve this revision or return material changes for reconciliation and a new
revision.

# Case 2: `source-conflict`

## Source-gap packet

**Typed Return:** source-gap packet.

- **Evidence:** the settled source permits refunds for 30 days; the approved
  ADR permits refunds for 14 days; neither authority supersedes the other.
- **Material effect:** the conflict changes supported behavior, acceptance,
  and proof, so no ticket can safely choose either period.
- **Missing decision:** an authorized owner must reconcile the two authorities
  and establish the governing refund window, including whether the losing
  statement is superseded or amended.
- **Tracker state:** unchanged; no slicing, approval, or mutation occurred.
- **Exact safe continuation:** Owner A obtains and records the authoritative
  reconciliation, then reruns ticket shaping against that settled source.

# Case 3: `setup-gap`

## Setup precondition

**Typed Return:** setup precondition.

- **Evidence:** the target repository has neither a tracker contract nor a
  provider mapping.
- **Why this blocks:** readiness fields, relationship semantics, publication
  transport, and Mutation read-back cannot be established.
- **Tracker state:** unchanged; no proposal or mutation occurred.
- **Exact safe continuation:** run `$repo-bootstrap` to reconcile and establish
  the repository's tracker contract and provider mapping, approve its bounded
  setup delta, and then rerun `$to-tickets`.

# Case 4: `economics`

## Case A

- **Size judgment:** the two-line documentation correction with a ten-minute
  proof is insubstantial. It does not justify parallel coordination, and its
  ready frontier is a singleton.
- **Exactly one next recommendation:** run `$implement` for that ready
  documentation ticket.

## Case B

- **Size judgment:** both tickets are substantial, each filling a focused
  session, and the supplied evidence establishes semantic, production-scope,
  public-proof, fixture, scarce-resource, and tripwire isolation.
- **Exactly one next recommendation:** run `$parallel-implement` with the
  parent.

# Case 5: `graph-distinctions`

- **Blockers:** T1 has none; T2 has none; T3 is blocked by T1 because T3
  consumes the schema created by T1.
- **Blocking edge:** T1 → T3.
- **Tracker ordering:** T2, T1, T3. This prioritization is not an additional
  blocking edge.
- **Predicted overlap:** T2 and T3 both touch `registry.py`, but they own
  different semantics. Filename overlap alone is neither a blocker nor proof
  of semantic overlap.
- **Serial tripwire:** T2 and T3 both require the single-writer test database,
  so their database-writing proof must not run concurrently. This resource
  constraint is not a blocking edge.
- **Ready frontier:** T2 and T1. T3 is excluded until T1's schema outcome is
  complete.
- **Exactly one next recommendation:** run `$implement` for T2, the first ready
  ticket in tracker order; the graph contains a serial tripwire and does not
  establish a fully isolated parallel frontier.

# Case 6: `incomplete-independence`

- **Execution judgment:** both tickets are substantial, but disjoint predicted
  files do not establish parallel safety. Semantic ownership, public proof
  seams, shared fixtures, and resource constraints are unknown, so production
  and proof isolation are unproved. No parent-delivery override applies.
- **Exactly one next recommendation:** run `$implement` for T1, the first
  ticket in tracker order.

# Case 7: `state-matrix`

## Proposed acceptance

| Initial state | Access/profile | Accepted behavior |
| --- | --- | --- |
| Absent | CLI and API; default and strict | Creates a valid cache through either access path; both paths subsequently observe equivalent current state. |
| Reusable current | CLI and API; default and strict | Reuses the compatible cache without unnecessary invalidation or rebuild and returns profile-correct results. |
| Legacy incompatible | CLI and API; default | Detects incompatibility, invalidates the legacy state safely, rebuilds current state, and never serves legacy contents as current. |
| Legacy incompatible | CLI and API; strict | Rejects or invalidates according to the settled strict-profile contract, with an explicit diagnostic; it never silently reuses incompatible state. |

Additional transition acceptance:

- Reuse preserves a current cache across repeated CLI and API access.
- An evidenced invalidation cause moves current state to invalid and the next
  permitted access reconstructs a valid current cache.
- Restart preserves reusable current state and does not turn legacy
  incompatible state into reusable state.
- CLI and API agree on cache identity, compatibility, and invalidation
  outcomes under each profile.
- Interrupted or failed reconstruction does not expose a partial cache as
  current.

## Proposed proof lane

- At the public CLI and API seams, parameterize proof over absent, reusable
  current, and legacy incompatible fixtures and over default and strict
  profiles.
- For absent state, invoke each access path, assert successful creation and
  equivalent observable results, then inspect authoritative cache metadata and
  contents.
- For reusable current state, record cache identity/version, invoke CLI and
  API repeatedly, and prove reuse without rebuild while results remain
  correct.
- For legacy incompatible state, seed the legacy fixture, invoke each access
  path/profile combination, and prove the specified rebuild or explicit
  strict rejection; assert that legacy contents are never served as current.
- Trigger a real invalidation condition, prove invalid state is not reused,
  and prove a subsequent permitted invocation creates a valid current cache.
- Restart between creation and reuse, and separately with a legacy fixture,
  then prove compatibility classification and observable results remain
  correct.
- Inject a reconstruction failure and prove no partial state is marked or
  served as current.

# Case 8: `migration`

Use three expand-migrate-contract technical work units. They are separate
because each stage has its own compatibility proof and releasable rollback
boundary; they are not treated as layer-based product slices.

## T1 — Expand with the compatible new protocol

- **Acceptance:** servers and storage accept the new protocol/form alongside
  the old one; old clients continue to operate unchanged; new clients can
  operate through the new form; records in either supported form are read
  correctly; deployment of T1 alone is operable, releasable, and backward
  compatible.
- **Proof:** caller-facing compatibility matrix covering old client/old record,
  old client/newly written record where supported, new client/old record, and
  new client/new record; deploy/rollback smoke proof with old support retained.

## T2 — Migrate records while both protocols coexist

- **Blocker / consumed outcome:** blocked by T1 and consumes T1's coexistence
  capability.
- **Acceptance:** records migrate incrementally and resumably to the new form;
  old and new clients remain operable throughout; retries do not duplicate or
  corrupt records; mixed-state reads/writes remain compatible; every partial
  migration checkpoint is releasable and rollback-safe.
- **Proof:** representative mixed-state migration, interruption/resume, retry,
  and rollback scenarios through both client types, plus authoritative counts
  and integrity checks showing no loss or duplication.

## T3 — Contract old protocol support

- **Blocker / consumed outcome:** blocked by T2 and consumes verified completion
  of migration. It additionally requires evidence that all old client use has
  ended and compatibility proof has passed.
- **Acceptance:** contraction is refused while any old use or old-form record
  remains; after both absence conditions and compatibility proof are
  satisfied, old protocol code and compatibility paths are removed; new
  clients and migrated records remain fully operable and releasable.
- **Proof:** precondition checks fail closed with seeded old clients or records;
  authoritative usage and record scans show zero old use; the full new-client
  compatibility suite passes before and after contraction; deploy/rollback
  proof covers the contract release.

## Graph

- Blocking edges: T1 → T2 and T2 → T3.
- Tracker order: T1, T2, T3.
- Initial ready frontier: T1.
- T2 becomes ready only after the compatible expansion is proved; T3 becomes
  ready only after migration, zero-old-use evidence, and compatibility proof.

# Case 9: `stale-approval`

## Proposal awaiting approval

**Typed Return:** proposal awaiting approval.

- **Evidence:** Owner A approved revision R7, but the parent acceptance changed
  materially before publication.
- **Freshness decision:** R7 no longer describes the current source and its
  approval cannot authorize publication.
- **Mutation:** none occurs.
- **Tracker state:** unchanged.
- **Exact safe continuation:** reconcile the changed parent acceptance into a
  fully identified successor proposal, present its complete coverage, graph,
  tickets, and intended mutations, and obtain explicit approval of that exact
  revision before publication.

# Case 10: `partial-mutation`

## Partial-publication recovery

**Typed Return:** partial-publication recovery.

- **Approved graph operations observed:** parent P exists; blocker T1 exists.
- **Failed or unknown operation:** creation of dependent T2 timed out, so the
  provider result is unknown. Current read-back cannot find T2, but that does
  not by itself prove that a delayed or unindexed creation cannot appear.
- **Unrelated state:** existing T9 is observed unchanged and is outside the
  recovery scope.
- **Graph/read-back result:** publication is not complete because the approved
  ordered child set and T1 → T2 relationship cannot be verified exactly.
- **Frontier risk:** T1 may appear to be the only ready work while the approved
  dependent is missing; treating the graph as complete could lose T2, and
  blindly recreating T2 could duplicate it if the timed-out request later
  materializes. No verified final frontier is returned.
- **Safest non-duplicating recovery:** preserve P and T1; do not touch T9 or
  issue an unconditional second create. Reconcile the timed-out operation by
  its original idempotency key/provider request identity and search/read back
  the parent relationship. If T2 is found, verify and repair only its approved
  body, roles, state, and T1 → T2 edge as necessary. If the provider
  authoritatively confirms no T2 exists, retry the approved T2 creation using
  the same idempotency key, then read back P, T1, T2, the edge, affected
  dependents, and the resulting frontier before declaring publication
  complete.

# Case 11: `route-table`

## (a) Empty frontier because B7 is open

Exactly one next action: resolve blocker B7.

## (b) Singleton T1

Exactly one next action: run `$implement` for T1.

## (c) Non-empty frontier with parent-delivery explicitly requested

Exactly one next action: run `$parallel-implement` with the parent.

## (d) T1/T2 overlap on semantic ownership

Exactly one next action: run `$implement` for T1, the first ticket in tracker
order.

## (e) T1/T2 are substantial and isolated

Exactly one next action: run `$parallel-implement` with the parent.

## (f) Independence is uncertain

Exactly one next action: run `$implement` for T1, the first ticket in tracker
order.

# Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
