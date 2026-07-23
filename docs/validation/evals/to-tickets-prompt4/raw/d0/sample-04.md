# ordinary-feature

## Return: proposal awaiting approval

Proposal revision: `OF-R1`.

Source Trace: Owner A is the settled-source owner and publication authority. The
bounded outcome is that a user can submit an order through the API and observe
the saved order, and an operations user can observe that same new order in the
existing dashboard. The accepted production surfaces are the API, domain
service, database, and existing dashboard. No implementation technique, new
dashboard, or unrelated order workflow is authorized. Proof must cross each
user-visible boundary. No source gaps or conflicts are present.

Coverage map:

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | `T1` |
| Apply order-domain behavior | `T1` |
| Persist the order | `T1` |
| API caller can observe the saved order | `T1` |
| Operations user sees the new order in the existing dashboard | `T2` |
| Existing dashboard, not a replacement UI | `T2` scope fence |
| Unrelated order, reporting, and operations behavior | Explicitly excluded |

Ordered graph: `T1 -> T2`. Predicted initial ready frontier: `T1`. Intended
mutations, after approval and a freshness check, are to create `T1` and `T2`,
attach both to the bounded parent/source, add the blocking edge `T1 -> T2`, set
their roles and ready states, and write packet metadata for `OF-R1`. No
mutation occurs while this proposal awaits approval.

### T1 — Submit and persist an order through the API

- Form and roles: vertical production slice; implementation owner unassigned,
  source owner and publication authority `Owner A`.
- Blockers: `none`. Consumed outcome: none.
- Covered commitments: API submission, domain-service handling, database
  persistence, and caller-visible saved-order observation.
- Acceptance: given valid order input and no corresponding saved order, the
  supported API accepts the submission, applies the settled domain behavior,
  persists exactly one order, and returns or exposes the saved order through
  the supported API boundary. Existing persisted orders remain readable.
  Invalid input follows the existing API failure contract and does not create a
  partial order.
- Proof lane: an API-level production-path test exercises the real domain and
  persistence boundary and reads the order back through the supported API;
  focused domain/persistence tests may localize failures but do not replace
  that proof.
- Rationale: API, service, and database work form one caller-observable outcome;
  splitting them by layer would create tickets with no independent meaningful
  proof.
- Expected write scope: order API adapter, order domain/application service,
  order persistence mapping/schema as required, and their focused/API tests.
- Semantic ownership and parallel safety: owns the order-write and saved-order
  API contract. Its persisted-order contract is consumed by `T2`, so that seam
  is a blocker rather than a concurrency promise.
- Execution profile and state boundary: standard production profile; cover
  absent order to saved order, valid and invalid submission, and an already
  populated database. No alternate CLI or strict profile is evidenced.
- Scope fence: no dashboard work, unrelated order lifecycle features,
  reporting redesign, or speculative database cleanup.

### T2 — Show the new order in the existing operations dashboard

- Form and roles: vertical presentation/read slice; implementation owner
  unassigned, source owner and publication authority `Owner A`.
- Blockers: `T1`. Consumed outcome: the persisted-order identity and supported
  read contract established by `T1`.
- Covered commitments: an operations user can see the newly saved order in the
  existing dashboard.
- Acceptance: after an order has been saved through the supported order
  boundary, an authorized operations user opening or refreshing the existing
  dashboard sees that order with its stable identifying information; an empty
  data set remains operable, and pre-existing orders continue to render.
- Proof lane: a dashboard-boundary test using a persisted order proves the
  operations-visible result; a focused read-adapter/component test may support
  diagnosis but does not replace the dashboard proof.
- Rationale: this has a distinct user, production surface, proof boundary, and
  rollback from order creation, so separate completion is valuable.
- Expected write scope: the existing dashboard order query/adapter and display
  path plus focused dashboard tests.
- Semantic ownership and parallel safety: owns only operations visibility.
  Although fixture-led preparation is possible, production integration is
  blocked by `T1`; shared persisted-order contracts are a serial tripwire.
- Execution profile and state boundary: standard operations-dashboard profile;
  cover empty, one newly saved order, and existing populated order sets. No
  alternate access mode or profile is evidenced.
- Scope fence: do not create a replacement dashboard, change order-write
  semantics, or add unrelated operations/reporting features.

Safe continuation: obtain explicit approval from Owner A for exact revision
`OF-R1`; any material change requires a reconciled revision and fresh approval.

# source-conflict

## Return: source-gap packet

Evidence conflicts on a behavior-defining invariant: the settled source permits
refunds for 30 days, while the approved ADR permits 14 days, and neither owner
supersedes the other. This changes acceptance, supported behavior, and likely
proof, so no slicing or mutation is safe.

Tracker state: unchanged.

Required resolution: the source and ADR authorities must reconcile the refund
window, identify the controlling durable source, and explicitly settle whether
the losing rule is superseded or retained in a distinct scope. Safe
continuation: return the reconciled decision as bounded settled source, then
restart Trace.

# setup-gap

## Return: setup precondition

Evidence: the target repository has neither a tracker contract nor a provider
mapping, so readiness, transport, relationships, and mutation read-back cannot
be established. Tracker state: unchanged.

Exact safe continuation: run `$repo-bootstrap` to establish a compatible
tracker contract and provider mapping, then rerun To Tickets against the same
settled source. No proposal or publication is attempted.

# economics

## Case A

Size judgment: a two-line documentation correction with a ten-minute proof is
too small to repay parallel coordination overhead.

Next recommendation: run `$implement` for the single ready documentation
ticket.

## Case B

Size judgment: both tickets are substantial enough to occupy a focused
session, and their distinct semantic owners, production scopes, public proof
seams, fixtures, resources, and tripwires provide evidence of economic and
semantic independence.

Next recommendation: run `$parallel-implement` with the parent.

# graph-distinctions

- Blockers: `T1` has none; `T2` has none; `T3` is blocked by `T1` because it
  consumes the schema created by `T1`.
- Tracker ordering: `T2`, `T1`, `T3`. The dependency edge constrains `T3`
  without rewriting that stable tracker order.
- Overlap: `T2` and `T3` both predict writes to `registry.py`, but their
  semantic ownership is distinct. File overlap alone is not a dependency.
- Serial tripwire: `T2` and `T3` both require the single-writer test database,
  so their database proof runs must not overlap once both are eligible.
- Ready frontier: `T2`, `T1`. `T3` is not ready until `T1` completes.
- Execution judgment: the current frontier lacks enough size and complete
  resource-isolation evidence to justify parallel delivery merely from two
  ready tickets.

Next recommendation: run `$implement` for `T2`, the first ready ticket in
tracker order.

# incomplete-independence

Disjoint predicted files do not establish independence. Semantic ownership,
public proof seams, fixture sharing, resource constraints, and the economics of
parallel work remain unknown, so parallel execution is unproved. The tickets
may remain separately ready, but no concurrency claim follows.

Next recommendation: run `$implement` for the first ticket in tracker order.

# state-matrix

## Proposed acceptance

| Initial state | Access/profile | Required observable behavior |
| --- | --- | --- |
| Cache absent | CLI and API; default and strict | Create valid current cache state and return the same supported result through each access path. |
| Current cache reusable | CLI and API; default and strict | Reuse the cache without unnecessary rebuild while preserving the supported result. |
| Legacy cache incompatible | CLI and API; default | Detect incompatibility, invalidate safely, rebuild current state, and return a supported result without consuming stale data. |
| Legacy cache incompatible | CLI and API; strict | Detect incompatibility and follow the settled strict-profile failure/recovery contract; never silently consume legacy state. |

Across both access paths and profiles, reuse preserves valid current state;
invalidation cannot leave a partially current cache; and restart after creation
or invalidation observes a valid current cache and produces the same supported
result. If the settled strict contract does not specify fail-versus-rebuild,
that is a source gap requiring resolution before approval.

## Proposed proof

Use a boundary matrix test at both the CLI and public API seams. For every
applicable row, seed the exact initial cache state, exercise default and strict
profiles, assert the caller-visible result or specified strict failure, and
inspect whether the cache was reused, invalidated, or rebuilt as required.
Then restart the process and repeat the supported read to prove durable current
state. Add transition assertions for absent-to-current,
current-to-reused-current, legacy-to-invalidated-to-current, and
post-transition restart. Focused cache-unit tests may diagnose detection and
invalidation but do not replace CLI/API boundary proof.

# migration

## Proposed work units and edges

1. `T1 — Introduce additive protocol compatibility`: make deployed services
   accept old and new clients while preserving operability and rollback.
2. `T2 — Migrate records under dual compatibility`: migrate records in
   restartable bounded batches while old and new clients coexist.
3. `T3 — Prove old-use exhaustion and compatibility`: establish from
   authoritative evidence that no old clients or old-format records remain and
   that the new-only path is compatible.
4. `T4 — Remove old protocol support`: remove the old path only after the
   exhaustion and compatibility gate passes.

Blocking edges: `T1 -> T2 -> T3 -> T4`. `T1` also directly blocks `T3` and
`T4`; `T2` directly blocks `T4`. Initial ready frontier: `T1`.

## Acceptance and proof

- `T1`: old and new clients both complete supported operations against every
  deployed mixed-version stage; additive deployment and rollback remain
  releasable. Prove with public protocol contract tests for old/new clients
  against pre-change, mixed, and upgraded service states, including rollback.
- `T2`: records migrate without denying supported old/new operations; batches
  are idempotent or safely resumable, interruption leaves an operable state,
  and every intermediate stage is releasable. Prove with migration-boundary
  tests covering old, mixed, and new records; old/new clients; interruption,
  retry, restart, and rollback at batch boundaries.
- `T3`: authoritative inventory shows zero remaining old client use and zero
  old-format records, while new clients pass the public compatibility suite.
  Prove with the production-authoritative usage/inventory check plus the
  versioned public contract suite; elapsed time or migration completion alone
  is insufficient.
- `T4`: only after `T3`, old protocol requests are rejected by the settled
  new-only contract, new clients and migrated records remain fully operable,
  and rollback/release policy is satisfied. Prove with new-only public contract
  and release tests plus a negative old-client test.

Each ticket is fenced to its migration phase. In particular, `T1` cannot remove
old support, `T2` cannot declare old use exhausted, and `T4` cannot begin on an
assumption or schedule alone.

# stale-approval

## Return: proposal awaiting approval

Revision `R7` is stale because the parent's acceptance changed materially after
approval. The freshness gate fails, so approval of `R7` does not authorize the
changed proposal.

Mutation occurs: **no**. Tracker state remains unchanged.

Safe continuation: reconcile the new parent acceptance into a new identified
proposal revision, regenerate affected coverage, tickets, edges, acceptance,
proof, and frontier, and obtain explicit approval of that exact revision before
publication.

# partial-mutation

## Return: partial-publication recovery

Approved intent included parent `P`, blocker `T1`, and dependent `T2`.
Observed read-back shows `P` and `T1`; it cannot find `T2`. The provider timed
out while creating `T2`, so its remote state remains unknown despite the
negative read. Existing unrelated `T9` is observed unchanged. Applied
operations: creation of `P` and `T1`. Failed or unknown operation: creation and
relationship publication for `T2`. The intended graph is not verified and must
not be reported as published.

Frontier risk: exposing `T1` as the final ready frontier could start work from
an incomplete graph, while blindly recreating `T2` could duplicate a
late-applied provider mutation or lose its blocker relationship.

Safest non-duplicating recovery: stop mutation and dispatch; reconcile `T2`
using the original stable mutation/idempotency identity and provider search,
then either adopt and read back the discovered ticket or create it once only
after absence is authoritative. Reapply only missing relationships/metadata,
and read back `P`, ordered children, bodies, roles, states, blocking edges,
affected dependents, and frontier. Do not alter `T9`.

# route-table

## (a) Empty frontier

Next action: resolve blocker `B7`.

## (b) Singleton frontier

Next action: run `$implement` for `T1`.

## (c) Explicit parent-delivery run

Next action: run `$parallel-implement` with the parent.

## (d) Semantic-ownership overlap

Next action: run `$implement` for `T1`, the first ticket in tracker order.

## (e) Substantial isolated tickets

Next action: run `$parallel-implement` with the parent.

## (f) Uncertain independence

Next action: run `$implement` for `T1`, the first ticket in tracker order.

# Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
