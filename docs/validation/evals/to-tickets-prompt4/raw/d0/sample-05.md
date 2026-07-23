# Case 1: `ordinary-feature`

## Proposal R1 awaiting approval

**Typed Return:** proposal awaiting approval. No tracker state changes have been
made. Safe continuation: `Owner A` approves this exact R1 or supplies changes
for a new revision.

### Source Trace

- Source owner and publication authority: `Owner A`.
- Settled outcome: a user submits an order through the API and can observe the
  saved order; an operations user can observe that new order in the existing
  dashboard.
- Required production seams: API, order domain service, database, and existing
  dashboard.
- Exclusions: no dashboard redesign, unrelated order lifecycle behavior,
  implementation-specific helper or file choices, or tracker mutation before
  approval.
- Proof expectation: observable API-to-persistence behavior and observable
  persisted-order-to-dashboard behavior through public seams.
- Material gaps: none stated.

### Coverage map

| Source commitment or boundary | Disposition |
| --- | --- |
| Submit an order through the API | T1 |
| Apply order-domain behavior and save the order | T1 |
| Let the submitting user observe the saved order | T1 |
| Show the newly saved order in the existing operations dashboard | T2 |
| Preserve the existing dashboard rather than redesign it | T2 scope fence |
| Unrelated lifecycle and UI work | Explicitly excluded from T1 and T2 |

### Ordered graph and predicted frontier

`T1 -> T2`. T1 creates the persisted-order outcome consumed by T2. The
predicted ready frontier after publication is `{T1}`.

Intended mutations, after approval and freshness reconciliation: create T1,
create T2, record T1 as blocking T2, assign the parent/source reference and
roles, leave T1 ready and T2 blocked, then read back the parent, both complete
bodies, roles, states, edge, affected dependents, and frontier.

### T1 — Submit and persist an order through the API

- Form/roles: implementation work unit; source owner and publication authority
  `Owner A`; delivery owner unclaimed.
- Parent/source: `ordinary-feature` settled source, Proposal R1.
- Blockers/consumed outcome: none.
- Why this slice: it has one public API-to-persistence proof boundary and
  unlocks dashboard consumption without slicing by technical layer.
- Build/commitments: accept an order through the supported API, apply the
  domain service behavior, persist it, and return or otherwise expose the
  saved order to the submitting user.
- Acceptance: through the public API, a valid submission produces one saved
  order with the submitted observable values and a stable persisted identity;
  the user-visible response/read path identifies that saved order. Existing
  supported failure behavior remains supported.
- Proof lane/highest seam: an API-level integration test exercising the domain
  service and production persistence adapter, with read-back of the stored
  order.
- Expected write scope/semantic ownership: order-submission API, order-creation
  domain behavior, and order persistence contract; exact files are
  implementation-owned.
- Parallel safety/execution profile: serial relative to T2 because T2 consumes
  this persisted-order contract and both meet at the order representation and
  database proof resource.
- Scope fence: no dashboard work, unrelated order lifecycle changes, schema
  cleanup, or API redesign.

### T2 — Display a newly saved order in the existing dashboard

- Form/roles: dependent implementation work unit; source owner and publication
  authority `Owner A`; delivery owner unclaimed.
- Parent/source: `ordinary-feature` settled source, Proposal R1.
- Blockers/consumed outcome: blocked by T1; consumes T1's persisted-order
  contract and identity.
- Why this slice: operations visibility has a distinct user and public
  dashboard proof seam, while its true persisted-order dependency remains
  explicit.
- Build/commitments: make the existing dashboard surface a newly persisted
  order to an operations user.
- Acceptance: given an order persisted under T1's supported contract, an
  operations user opening or refreshing the existing dashboard can identify
  that order by its stable identity and see the source-required order values.
- Proof lane/highest seam: dashboard-level integration or end-to-end test
  seeded through the supported persistence contract and observed through the
  operations-user dashboard.
- Expected write scope/semantic ownership: dashboard order query/projection and
  existing order presentation; exact files are implementation-owned.
- Parallel safety/execution profile: not concurrently grabbable with T1;
  shared order contract/database are serial tripwires until T1's outcome is
  proved.
- Scope fence: no new dashboard, general UI refresh, unrelated operations
  views, or changes to order creation beyond the consumed T1 contract.

# Case 2: `source-conflict`

**Typed Return:** source-gap packet.

- Evidence: the settled source authorizes refunds for 30 days; an approved ADR
  authorizes 14 days; neither authority supersedes the other.
- Material gap: the refund eligibility contract is conflicting, and choosing
  either value would change acceptance, supported behavior, and scope.
- Tracker state: unchanged; no slicing or mutation occurred.
- Safe continuation: the source owner and ADR authority must reconcile the
  refund window and identify the superseding durable decision, then rerun
  ticket creation against that settled source.

# Case 3: `setup-gap`

**Typed Return:** setup precondition.

- Evidence: the repository has neither a tracker contract nor a provider
  mapping, so readiness fields and publication transport cannot be verified.
- Tracker state: unchanged.
- Exact precondition and continuation: run `$repo-bootstrap` to establish a
  compatible tracker contract and provider mapping, then rerun `$to-tickets`
  against the same bounded settled source.

# Case 4: `economics`

## Case A

The ready work is a two-line documentation correction with a ten-minute proof:
it is too small for parallel-dispatch overhead to be economic, and the
frontier contains one ticket.

**Exactly one next recommendation:** run `$implement` for that ticket.

## Case B

Both tickets are substantial full-session work. Their semantic ownership,
production scope, public proof seams, fixtures, resources, and tripwires are
isolated, so there is enough independent work to repay parallel coordination.

**Exactly one next recommendation:** run `$parallel-implement` with the parent.

# Case 5: `graph-distinctions`

- True blockers: T1 has none; T2 has none; T3 is blocked by T1 because it
  consumes T1's schema.
- Tracker ordering: T2, T1, T3. Dependency ordering additionally requires T1
  before T3; tracker order does not invent a T2-to-T1 dependency.
- Overlap: T2 and T3 both predict edits to `registry.py`, but their semantic
  ownership is distinct. The filename collision is physical overlap, not by
  itself a blocker or proof of shared semantics.
- Serial tripwire: T2 and T3 both require the single-writer test database, so
  their proof runs must not overlap even if their code ownership remains
  distinct.
- Ready frontier: `{T2, T1}`; T3 is not ready.

**Exactly one next recommendation:** run `$implement` for T2, the first ticket
in tracker order, because the graph contains a serial proof-resource tripwire.

# Case 6: `incomplete-independence`

Disjoint predicted files establish neither semantic independence nor
production/proof isolation. With semantic owners, public seams, fixtures, and
resource constraints unknown, parallel safety and economics remain uncertain;
the two tickets must not be presented as a parallel-ready pair.

**Exactly one next recommendation:** run `$implement` for T1, the first ticket
in tracker order.

# Case 7: `state-matrix`

## Proposal acceptance

- **Initial-state axis:** from absent state, first supported access creates a
  valid current cache; from reusable current state, access reuses it without
  needless reconstruction; from legacy incompatible state, access invalidates
  or safely replaces it rather than treating it as current.
- **Access axis:** both CLI and API paths produce the same supported cache
  semantics and observable result for each applicable initial state.
- **Profile axis:** the default profile follows the approved normal
  reuse/invalidation policy; the strict profile rejects or rebuilds state
  wherever strict compatibility requires it and never silently reuses
  incompatible state.
- **Transition axis:** reuse preserves a compatible cache and its observable
  identity/content; invalidation prevents subsequent reads from consuming the
  invalid state and permits creation of current state; restart preserves valid
  reusable state and does not resurrect invalidated or legacy-incompatible
  state.
- **Combined boundary:** each supported CLI/API and default/strict combination
  behaves as specified from absent, current, and legacy-incompatible state
  through each applicable reuse, invalidation, and restart transition.

No stated matrix axis is marked non-applicable.

## Proposal proof lane

Use a public-boundary matrix suite, parameterized across initial state
(`absent`, `current`, `legacy-incompatible`), access (`CLI`, `API`), and profile
(`default`, `strict`). For every applicable cell, assert the public result,
whether state was created/reused/rejected/replaced, and the resulting durable
cache version/content. Exercise reuse, explicit or policy-driven invalidation,
and process restart, inspecting persisted state after each transition. Include
cross-access restart checks (create by CLI/read by API and create by API/read
by CLI) and prove that neither profile consumes invalid legacy state.

# Case 8: `migration`

## Proposed work units and edges

1. **T1 — Expand compatibility:** deploy protocol/storage support that accepts
   old and new clients and preserves old and new record readability.
2. **T2 — Migrate records:** after T1, migrate existing records with resumable,
   observable progress while both client protocols remain operable.
3. **T3 — Prove compatibility and end old use:** after T2, verify migrated and
   newly written records through the new protocol, demonstrate that old-client
   use has reached zero, and authorize removal.
4. **T4 — Contract old support:** after T3, remove the old protocol and its
   compatibility path while retaining new-client and migrated-record support.

Edges: `T1 -> T2 -> T3 -> T4`. Each edge consumes an observable predecessor
outcome; none is merely a preferred scheduling edge.

## Acceptance and proof

### T1

- Acceptance: old and new clients can coexist against the deployed system;
  records needed by either are readable; the expansion is backward compatible
  and independently releasable.
- Proof: compatibility integration matrix for old/new clients against old/new
  record forms, plus deploy/rollback smoke proof showing the expanded stage
  remains operable.

### T2

- Acceptance: records migrate without interrupting either client generation;
  retries are safe; progress and failures are observable; any partial
  migration stage is operable, releasable, and resumable.
- Proof: migration integration tests over unmigrated, partially migrated, and
  fully migrated datasets; interruption/restart and idempotent retry proof;
  old/new client reads and writes at each stage.

### T3

- Acceptance: all required records and workflows succeed through the new
  protocol, compatibility behavior is proved, and measured old-client use is
  zero for the approved observation condition before removal is authorized.
- Proof: production-representative new-client/read-write verification,
  migrated-record checks, compatibility regression suite, and auditable
  telemetry/query evidence that no old use remains.

### T4

- Acceptance: old support is removed only with T3 satisfied; new clients and
  all migrated records remain operable; the contracted deployment is
  independently releasable and has a defined safe rollback boundary.
- Proof: absence/negative tests for the retired protocol, full new-client and
  migrated-record public-seam regression, deployment smoke test, and rollback
  rehearsal or equivalent release proof.

# Case 9: `stale-approval`

**Typed Return:** proposal awaiting approval.

- Evidence: R7 was approved, but the parent acceptance changed materially
  before publication. R7 is stale because its coverage, ticket acceptance, and
  possibly graph no longer prove the current parent intent.
- Tracker state: unchanged.
- Mutation: none occurs.
- Safe continuation: reconcile the changed parent into a newly identified
  revision, regenerate all affected coverage/ticket/graph details, and obtain
  explicit approval of that exact revision before publication.

# Case 10: `partial-mutation`

**Typed Return:** partial-publication recovery.

- Approved revision state: retain the approved proposal unchanged as the
  recovery baseline.
- Observed applied operations: parent P exists; blocker T1 exists.
- Failed/unknown operations: T2 creation timed out. Read-back cannot find T2,
  but the timeout leaves provider state unknown; absence in this read does not
  safely prove that a delayed or deduplicated creation cannot appear.
- Unrelated state: existing T9 was read back unchanged and must remain
  untouched.
- Graph/frontier risk: the approved P -> T1 -> T2 graph is incomplete or
  indeterminate. Any reported ready frontier could omit a latent T2, expose an
  incorrectly unblocked dependent, or lead to a duplicate T2, so no frontier
  or implementation route is verified.
- Tracker state: partially changed exactly as observed above; no claim,
  implementation, or compensating deletion occurs.
- Safest non-duplicating recovery: query the provider using the original
  idempotency key/external correlation and parent relationship until T2 is
  authoritatively found or authoritatively absent. If found, reconcile it to
  the approved body and edge; if authoritatively absent, create it once using
  the same idempotency identity. Then read back P, T1, T2, roles, bodies,
  states, edges, affected dependents, T9's unchanged state, and the resulting
  frontier before recommending any next action.

# Case 11: `route-table`

| Frontier | Exactly one next action |
| --- | --- |
| (a) Empty because B7 is open | Resolve B7. |
| (b) Singleton T1 | Run `$implement` for T1. |
| (c) Non-empty and a parent-delivery run was explicitly requested | Run `$parallel-implement` with the parent. |
| (d) T1/T2 overlap on semantic ownership | Run `$implement` for T1, first in tracker order. |
| (e) T1/T2 are substantial and isolated across semantics, production, proof, resources, and tripwires | Run `$parallel-implement` with the parent. |
| (f) Independence is uncertain | Run `$implement` for T1, first in tracker order. |

Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
