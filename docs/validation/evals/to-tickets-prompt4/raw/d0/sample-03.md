# 1. ordinary-feature

## Proposal R1 — awaiting approval

**Typed Return:** proposal awaiting approval. No tracker mutation has occurred. Publication authority is `Owner A`; publication requires `Owner A` to approve this exact R1.

### Source Trace

- Source owner/publication authority: `Owner A`.
- Settled outcome: an end user submits an order through the API and can observe the saved order; an operations user can observe that same new order in the existing dashboard.
- Accepted scope: API, domain service, database persistence, and existing dashboard read/display behavior.
- Exclusions: no new order-management features, dashboard redesign, alternate submission channel, or implementation technique was authorized.
- Proof expectation: observable caller-facing API persistence proof and observable operations-dashboard proof.
- Material gaps: none stated.

### Coverage map

| Source commitment or boundary | Disposition |
|---|---|
| Submit an order through the API | T1 |
| Apply the domain operation and save the order | T1 |
| Submitter can see the saved order | T1 |
| Operations user sees the new order in the existing dashboard | T2 |
| API, domain service, and database participation | T1 expected production scope; implementation details remain with delivery |
| Dashboard participation | T2 expected production scope |
| No unrelated order-management or dashboard redesign | Scope fence on T1 and T2 |

### Ordered graph and predicted frontier

`T1 → T2`. T1 produces the persisted, API-observable order outcome consumed by T2. The predicted initial ready frontier is `{T1}`.

Intended mutations after approval and freshness reconciliation: create T1 and T2 under the approved parent, assign the roles and states below, add the blocking edge `T1 blocks T2`, and read back the parent, both ticket bodies, roles, state, relationship, edge, affected dependents, and resulting frontier.

### T1 — Submit and observe a persisted order through the API

- Work-unit form: vertical behavior slice; no migration phase.
- Roles/state: publication owner `Owner A`; delivery owner unassigned; open, unclaimed, ready-for-agent after publication.
- Bounded source: Proposal R1 Source Trace; commitments: API submission, domain operation, database persistence, and submitter-visible saved order.
- Why this slice / what to build: it establishes one caller-visible API-to-persistence outcome that can be completed and proved without dashboard completion.
- Blockers / consumed outcome: none / none.
- Acceptance:
  - Given a valid order request, the API accepts it through the supported public endpoint.
  - The domain operation persists exactly the resulting order in the supported database path.
  - The API caller can retrieve or otherwise observe the saved order through the supported public API boundary, with its stable identity and submitted values.
  - Rejected or invalid input does not appear as a saved order.
- Highest proof seam and proof lane: a public API integration test against the supported persistence boundary that submits, observes, and checks invalid-input non-persistence.
- Expected production scope: order API boundary, order domain service, and order persistence seam; exact files and helpers are implementation-owned.
- Semantic ownership: creation and API observation of a persisted order.
- Parallel safety: independent of T2 for completion; its persistence contract is consumed by T2, so the edge remains serial. Shared resources beyond the stated database path are not evidenced.
- Execution profile/state matrix: serial predecessor profile. Creation from absent order to persisted current order and API observation apply; legacy/reuse/restart or migration branches are not evidenced and are non-applicable to this source.
- Scope fence: do not add dashboard behavior, redesign order APIs, add alternate channels, or expand order-management behavior.

### T2 — Show newly persisted orders in the existing operations dashboard

- Work-unit form: consumer-facing vertical behavior slice; no migration phase.
- Roles/state: publication owner `Owner A`; delivery owner unassigned; open, unclaimed, blocked by T1 until its consumed outcome is complete.
- Bounded source: Proposal R1 Source Trace; commitment: an operations user sees the new order in the existing dashboard.
- Why this slice / what to build: it owns the distinct operations-user proof seam and consumes, rather than redefines, the persisted-order outcome.
- Blockers / consumed outcome: T1 / a newly submitted order is durably stored with the fields and identity exposed by the supported order contract.
- Acceptance:
  - Given an order created through the supported API and persisted under T1's contract, an operations user can see that order in the existing dashboard.
  - The displayed order corresponds to the persisted identity and required operational values.
  - Existing dashboard behavior remains available; no new dashboard workflow is introduced.
- Highest proof seam and proof lane: dashboard boundary test using a real supported persisted order, proving operations-visible rendering and identity/value correspondence.
- Expected production scope: existing dashboard order query/read model and display seam; exact files and helpers are implementation-owned.
- Semantic ownership: operations visibility of persisted orders.
- Parallel safety: locally provable, but it consumes T1's outcome and must not complete against an invented persistence contract. No concurrency before T1.
- Execution profile/state matrix: dependent consumer profile. Current persisted-order read/display applies; absent, legacy, invalidation, restart, and migration branches are not evidenced and are non-applicable to this source.
- Scope fence: do not change submission semantics, persistence schema without a newly approved need, dashboard architecture, or unrelated dashboard presentation.

**Safe continuation:** `Owner A` approves or rejects Proposal R1 exactly as written; any material change requires a new revision and fresh approval.

# 2. source-conflict

**Typed Return:** source-gap packet.

- Evidence: the settled source authorizes refunds for 30 days; the approved ADR authorizes 14 days; neither authority supersedes the other.
- Material gap: the valid refund window is unresolved. It changes supported behavior, acceptance, proof, and likely compatibility obligations, so implementation-owned technique cannot resolve it.
- Coverage/slicing/publication state: no slicing or tracker mutation occurred; tracker state is unchanged.
- Required decision: the relevant source and ADR owners must establish one authoritative refund window and record whether one source supersedes or amends the other.
- Exact safe continuation: reconcile the two authorities, then rerun ticket formation from the newly settled source.

# 3. setup-gap

**Typed Return:** setup precondition.

- Evidence: the target repository has neither a tracker contract nor a provider mapping, so Ready-for-agent fields, transport, relationships, and Mutation read-back cannot be established.
- Tracker state: unchanged; no proposal or mutation was attempted.
- Exact precondition and safe continuation: run `$repo-bootstrap` for the target repository to establish a compatible tracker contract and provider mapping, approve and apply that setup through its owner, then return to ticket formation.

# 4. economics

## Case A

- Size judgment: this is one very small ready work unit—a two-line documentation correction with a ten-minute proof. Dispatch coordination would exceed the likely delivery cost.
- Exactly one next recommendation: run `$implement` for the documentation ticket.

## Case B

- Size judgment: these are two substantial, full-session work units with distinct semantic ownership, production scope, public proof seams, and fixtures, with no shared scarce resource or serial tripwire. The independence and economics gates both support parallel delivery.
- Exactly one next recommendation: run `$parallel-implement` with their parent.

# 5. graph-distinctions

- Blockers: T1 has none; T2 has none; T3 is blocked by T1 because it consumes the schema T1 creates.
- Tracker order: `T2`, `T1`, `T3`. Dependency order additionally requires `T1 → T3`; tracker order does not erase that edge.
- Overlap: T2 and T3 both predict writes to `registry.py`, but they own different semantics. This is file overlap, not evidence of shared semantic ownership.
- Serial tripwire: T2 and T3 both require the single-writer test database, so they must not use that proof resource concurrently even after T3 becomes ready.
- Ready frontier: `{T2, T1}`. T3 is not ready.
- Exactly one next recommendation: run `$implement` for T2, the first ready ticket in tracker order, because the graph contains a known serial proof-resource tripwire.

# 6. incomplete-independence

- Execution/parallel judgment: disjoint predicted files do not establish independence. Semantic ownership, public proof seams, fixture isolation, and resource/tripwire isolation remain unknown, so parallel safety and favorable parallel economics are unproved. No parent-delivery override applies.
- Ready frontier: both tickets may be ready in dependency terms, but their concurrent execution is not approved by this evidence.
- Exactly one next recommendation: run `$implement` for T1, the first ticket in tracker order.

# 7. state-matrix

## Proposed acceptance

- **Initial-state branches**
  - Absent: first CLI and API access creates or obtains the supported cache state and returns the correct result without assuming a pre-existing cache.
  - Reusable current: CLI and API access reuse a compatible current cache and return behavior equivalent to a fresh result without unnecessary replacement.
  - Legacy incompatible: CLI and API access detect that the legacy cache is incompatible, do not treat it as current, and follow the approved safe invalidation/rebuild behavior.
- **Access surfaces**
  - CLI and API each expose the same supported cache semantics for absent, reusable-current, and legacy-incompatible states.
  - Surface-specific errors remain observable through the supported CLI and API contracts.
- **Profiles**
  - Default profile performs the approved automatic reuse or safe invalidation/rebuild behavior.
  - Strict profile rejects or stops on an incompatible state rather than silently accepting or replacing it, while still reusing a compatible current state.
- **Transitions**
  - Reuse preserves compatible current state across repeated access.
  - Invalidation prevents subsequent reads from observing the invalidated legacy/current entry as reusable.
  - Restart preserves only the state promised as durable; after restart, both CLI and API classify it consistently as absent, reusable current, or incompatible and take the profile-appropriate action.
- No branch may return stale legacy content as a valid current result, and a failed transition must not advertise a reusable current cache.

## Proposed proof lanes

The highest meaningful seam is a parameterized public-boundary integration matrix, not isolated helper tests:

| Starting state | Surface | Profile | Required observable proof |
|---|---|---|---|
| Absent | CLI, API | Default, strict | correct result and supported cache creation/obtainment; no pre-existence assumption |
| Reusable current | CLI, API | Default, strict | compatible state is reused and result is correct |
| Legacy incompatible | CLI, API | Default | incompatibility is detected; approved invalidation/rebuild occurs; legacy result is never returned as current |
| Legacy incompatible | CLI, API | Strict | incompatibility is reported through the public contract; no silent acceptance/replacement |

Transition sequences must additionally prove `current → reuse → restart → reuse`, `legacy → invalidate → rebuild → restart → current`, and strict-profile rejection followed by a fresh process observing the correct unchanged or explicitly invalidated state. Proof records cache identity/version and public result/error so reuse, replacement, and restart behavior are distinguishable.

# 8. migration

## Proposed work units and edges

`T1 Expand compatibility → T2 Migrate records and usage → T3 Contract old support`.

### T1 — Expand: deploy coexistence support

- Migration phase: expand.
- Acceptance: a deployed stage accepts both old and new clients; old and new protocol records remain readable/writable as required; mixed-version operation is supported; rollback to the preceding release does not strand records written during the stage; the stage is independently operable and releasable.
- Proof: public protocol compatibility matrix covering old client/old record, old client/newly written compatible record, new client/old record, and new client/new record, plus upgrade and rollback across adjacent deployed versions.
- Blockers: none. Scope fence: add compatibility only; do not remove old support or declare migration complete.

### T2 — Migrate: move records and active usage

- Migration phase: migrate.
- Acceptance: records migrate resumably and idempotently while old and new clients coexist; interruption/restart neither loses nor duplicates records; progress and residual old use are observable; every intermediate deployment remains operable and releasable; rollback remains safe under T1's compatibility contract.
- Proof: production-like migration test over mixed records with pause/restart/retry, concurrent old/new client access, reconciliation counts, residual-old-use reporting, and adjacent-stage upgrade/rollback.
- Blocker/consumed outcome: T1 / deployed coexistence contract.
- Scope fence: migrate records and observe use; do not remove compatibility.

### T3 — Contract: remove old support after proved completion

- Migration phase: contract.
- Acceptance: removal is permitted only when authoritative observation shows no old clients or old-format use remains, all records satisfy the new contract, and compatibility proof passes; after removal, new clients and migrated records operate correctly; the resulting stage is releasable; an unmet gate leaves old support intact.
- Proof: pre-removal gate test using authoritative usage and record scans, negative test showing removal is blocked while any old use remains, post-removal public protocol test for new clients/records, and release/rollback proof for the approved contract-stage strategy.
- Blocker/consumed outcome: T2 / completed records migration plus proved end of all old use; also consumes T1's compatibility evidence.
- Scope fence: remove only the explicitly retired protocol path; no unrelated client or record redesign.

The edges are true completion blockers, not merely preferred scheduling: T2 cannot safely start its migration contract without T1 coexistence, and T3 cannot remove old support until T2's migration and zero-old-use gates are proved.

# 9. stale-approval

**Typed Return:** proposal awaiting approval.

- Evidence: `R7` was approved, but the parent acceptance changed materially before publication. The approved revision is therefore stale because its coverage, ticket acceptance, or proof may no longer preserve current parent intent.
- Tracker state: unchanged by this run.
- Mutation: none occurs.
- Exact safe continuation: reconcile the changed parent into a new identified proposal revision, present its complete coverage and graph, and obtain fresh explicit approval before any publication.

# 10. partial-mutation

**Typed Return:** partial-publication recovery.

- Approved target: parent P with blocker T1 and dependent T2.
- Observed applied operations: read-back confirms P and T1 exist.
- Failed/unknown operation: T2 creation timed out. Read-back cannot find T2, but the timeout leaves provider state unknown; absence from this read does not prove that no delayed or idempotent creation exists.
- Unrelated state: existing T9 is confirmed unchanged and must remain untouched.
- Resulting frontier risk: the intended graph and its ready frontier are unverified. T1 may appear ready while its dependent/relationship is missing or delayed, and retrying creation blindly could duplicate T2. No implementation dispatch is safe from this partial graph.
- Safest non-duplicating recovery: stop all further graph mutation and dispatch; use the original operation's stable idempotency key/provider request identity to perform authoritative lookup and repeated read-back for T2 and its parent/edge. If T2 is found, reconcile its exact body, roles, state, and edge before verifying the whole frontier. If authoritative provider evidence proves it was never created, retry that one approved T2 creation with the same idempotency identity, then read back P, T1, T2, relationships, blockers, affected dependents, T9 unchanged, and the frontier. Any mismatch returns for reconciliation rather than creating another ticket.

# 11. route-table

| Frontier | Exactly one next action |
|---|---|
| (a) Empty because B7 is open | Resolve blocker B7. |
| (b) Singleton T1 | Run `$implement` for T1. |
| (c) Non-empty and a parent-delivery run was explicitly requested | Run `$parallel-implement` with the parent. |
| (d) T1/T2 overlap on semantic ownership | Run `$implement` for T1, the first ticket in tracker order. |
| (e) T1/T2 are substantial and isolated across semantics, production, proof, resources, and tripwires | Run `$parallel-implement` with the parent. |
| (f) Independence is uncertain | Run `$implement` for T1, the first ticket in tracker order. |

Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
