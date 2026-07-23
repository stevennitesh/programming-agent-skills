# Case 1: `ordinary-feature`

## Return: proposal awaiting approval

**Proposal revision:** `ordinary-feature-R1`

**Source Trace**

- Source owner and publication authority: `Owner A`.
- Stable outcome: a submitted API order is saved and visible both to the submitting user and to an operations user in the existing dashboard.
- Accepted scope: API request/response, domain-service behavior, database persistence, and dashboard presentation of the newly saved order.
- Exclusions: no new order-management behavior, dashboard redesign, alternate submission channel, or unrelated schema cleanup.
- Proof expectation: demonstrate the behavior across the public API and the existing operations dashboard, including persisted data rather than a mocked handoff.
- Material gaps: none identified from the supplied settled source.

**Coverage map**

| Source commitment or boundary | Disposition |
| --- | --- |
| User submits an order through the API | `T1` acceptance and API proof |
| Submitted order is saved | `T1` acceptance and persistence proof |
| Submitting user can see the saved order | `T1` acceptance and API response/read-back proof |
| Operations user sees the new order in the existing dashboard | `T1` acceptance and dashboard proof |
| API, domain service, database, and dashboard participate | `T1` expected production scope |
| Unrelated order behavior and dashboard redesign | Explicitly excluded by `T1` scope fence |

**Ordered graph and predicted frontier**

- `T1 — Submit, persist, and surface a new order`
- True blockers: `none`.
- Blocking edges: `none`.
- Predicted ready frontier after publication: `T1`, provided it remains open, unclaimed, and ready-for-agent.

## Proposed ticket `T1`

- **Form:** one vertical behavior slice.
- **Roles:** source owner and publication authority `Owner A`; implementation owner unassigned and available for claim.
- **Parent/bounded source:** `ordinary-feature`, proposal `ordinary-feature-R1`.
- **Why this slice:** the saved order and dashboard visibility are one end-to-end outcome. Splitting by API, service, database, or dashboard would create layer tickets whose useful behavior and proof depend on siblings.
- **What to build:** accept a valid order through the public API, pass it through the domain service, persist it in the database, return or expose the saved order to the submitting user, and make that same order visible in the existing operations dashboard.
- **Covered commitments:** all four implementation commitments in the coverage map.
- **Acceptance:**
  1. Given a valid order submission, the public API accepts it and identifies the resulting saved order.
  2. A read through the supported user-facing API path returns the persisted order with the submitted values and stable identity.
  3. The existing operations dashboard displays that same newly persisted order to an authorized operations user.
  4. A failed persistence operation does not report a successfully saved order or display a phantom order.
- **Highest meaningful proof seam:** a caller-facing integration or system test that submits through the public API against the real test persistence boundary, reads the saved order back, and observes the same identity and values through the dashboard-facing behavior.
- **Focused proof:** exercise one successful valid submission and one persistence-failure path; verify API result, durable record, user read-back, and operations display.
- **Expected write scope:** production behavior spanning the order API adapter, order domain-service seam, order persistence mapping/schema only if required, and the existing dashboard order query/presentation seam; focused tests and fixtures for this behavior.
- **Semantic ownership:** creation and visibility lifecycle of a newly submitted order.
- **Shared resources:** the order persistence model and the API/dashboard representation of order identity.
- **Parallel-safety note:** this slice is internally cross-component and should have one semantic owner. Any concurrent work touching order identity, persistence, or dashboard order projection requires reconciliation.
- **Serial tripwires:** order schema or identity changes, shared database migrations, and shared end-to-end order fixtures.
- **Scope fence:** do not add cancellation, refunds, fulfillment, bulk entry, a new dashboard, or general refactors unrelated to making a newly submitted order durable and visible.
- **Local completion:** completion is observable through `T1`'s public API-to-dashboard proof and does not require an unrelated sibling ticket.

**Intended tracker mutations after approval:** create `T1` under the identified parent/source, set its Ready-for-agent fields and roles, leave blockers empty, record no blocking edges, and preserve the parent body except for tracker-required child metadata.

**Approval state:** `ordinary-feature-R1` has not been explicitly approved. Tracker state is unchanged. Safe continuation: `Owner A` approves this exact revision or supplies changes for a new revision; no publication occurs before that approval.

# Case 2: `source-conflict`

## Return: source-gap packet

- **Conflicting sources:** settled source permits refunds for 30 days; the approved ADR permits refunds for 14 days.
- **Authority finding:** both are decision-bearing and neither is identified as superseding the other.
- **Material effect:** the conflict changes supported refund behavior, acceptance criteria, implementation scope, and proof.
- **Required resolution:** the responsible authorities must select 14 days or 30 days, or issue a superseding durable decision that states the governing window and the fate of the other source.
- **Evidence still usable:** refunds are supported for some bounded period, but the period itself is unresolved.
- **Tracker state:** unchanged.
- **Safe continuation:** reconcile the two authorities and provide the superseding decision, then restart Source Trace. Slicing and publication stop now.

# Case 3: `setup-gap`

## Return: setup precondition

- **Missing setup:** the target repository has neither a tracker contract nor a provider mapping, so Ready-for-agent state, roles, relationships, and mutation/read-back behavior cannot be interpreted safely.
- **Tracker state:** unchanged.
- **Exact precondition:** run `$repo-bootstrap` for the target repository to establish a compatible tracker contract and provider mapping, then return the reconciled setup evidence to To Tickets.
- **Safe continuation:** resume Source Trace only after that precondition is satisfied. No proposal or mutation is attempted.

# Case 4: `economics`

## Case A

- **Size judgment:** the ready two-line documentation correction with ten-minute proof is not substantial enough to justify parallel orchestration.
- **Next recommendation:** `$implement` the documentation-correction ticket.

## Case B

- **Size judgment:** both multi-module features are substantial because each is expected to occupy a full focused session; their distinct semantic owners, production scopes, public proof seams, and fixtures, plus the absence of shared scarce resources and tripwires, establish parallel eligibility.
- **Next recommendation:** `$parallel-implement` with their parent.

# Case 5: `graph-distinctions`

- **True blockers:** `T1: none`; `T2: none`; `T3: T1`, because `T3` consumes the schema created by `T1`.
- **Blocking edges:** `T1 -> T3` only.
- **Tracker order:** `T2`, `T1`, `T3`. This ordering does not itself create a blocker.
- **Predicted overlap:** `T2` and `T3` both write `registry.py`, but they own different semantics. Filename overlap alone is not a blocking edge or proof of semantic conflict.
- **Serial tripwire:** `T2` and `T3` must not run database-writing proof concurrently because the test database allows only one writer. This scheduling constraint is not a blocker.
- **Ready frontier:** `T2`, then `T1`. `T3` is excluded until `T1` is complete.
- **Next recommendation:** `$implement` `T2`, the first ready ticket in tracker order, because the graph contains a shared scarce proof resource/serial tripwire.

# Case 6: `incomplete-independence`

- **Execution judgment:** both tickets are substantial, but disjoint predicted files do not establish semantic, production-scope, or proof isolation.
- **Parallel judgment:** parallel eligibility is unproved because semantic ownership, public proof seams, shared fixtures, and resource constraints are unknown. Uncertainty defaults to serial, and no parent-delivery run overrides that judgment.
- **Next recommendation:** `$implement` `T1`, the first ticket in tracker order.

# Case 7: `state-matrix`

## Proposed acceptance content

The cache ticket accepts only when all applicable state, access, profile, and transition branches are observable:

| State or transition | CLI, default | CLI, strict | API, default | API, strict |
| --- | --- | --- | --- | --- |
| Absent initial state | Creates a valid cache and returns the requested result | Creates a valid cache only under strict validation and returns the requested result | Same supported initialization through the API | Same strict initialization through the API |
| Reusable current state | Reuses the current compatible cache without unnecessary rebuild | Reuses only after strict validation succeeds | Reuses the same compatible state through the API | Reuses only after strict API-path validation succeeds |
| Legacy incompatible state | Invalidates or replaces it safely; never treats it as current | Rejects or invalidates it according to strict policy with an actionable result | Applies the same safe incompatibility boundary through the API | Applies strict rejection/invalidation through the API |
| Reuse transition | A second access reuses the valid state | A second access revalidates and reuses valid state | Equivalent reuse is observable through the API | Equivalent strict reuse is observable through the API |
| Invalidation transition | An invalidating change prevents stale reuse and produces valid replacement state | Strict mode detects the invalid condition before reuse | API access observes invalidation and no stale result | Strict API access detects invalidity and does not reuse stale state |
| Restart transition | A process restart can load and reuse valid durable cache state | Restarted strict access revalidates before reuse | A restarted service can reuse valid durable state through the API | A restarted service revalidates before strict reuse |

Additional acceptance boundaries:

- CLI and API behavior agree on cache identity, compatibility, and freshness for equivalent requests.
- Default and strict profiles differ only where the approved validation policy requires it; neither profile silently returns stale or incompatible data.
- Failed creation, validation, invalidation, or restart recovery does not publish partial state as reusable.
- Evidence demonstrates each branch above; no listed axis is silently omitted.

## Proposed proof content

- **Highest meaningful seam:** caller-facing CLI and API integration tests against the real cache persistence/serialization boundary.
- **State fixtures:** absent storage, reusable current cache, and an explicitly versioned legacy incompatible cache.
- **Transition proof:** for each access/profile combination, run create-from-absent, reuse-current, invalidate-then-access, and persist-restart-access sequences; assert returned result, cache identity/version, freshness, and whether reuse or rebuild occurred.
- **Failure proof:** interrupt or fail creation/invalidation and verify no partial state is subsequently accepted.
- **Cross-surface proof:** issue equivalent CLI and API requests against the same prepared states and verify consistent compatibility and freshness decisions.
- **Strict-profile proof:** corrupt or otherwise invalidate a state condition checked only by strict validation and verify strict access refuses reuse while producing the defined actionable result.

# Case 8: `migration`

## Proposed work units and edges

1. **`T1 — Expand protocol compatibility`**
   - Add the new protocol form beside the old form.
   - Keep old clients fully supported.
   - **Blockers:** none.
2. **`T2 — Migrate records and client use`**
   - Move records through the compatible path and transition client use while old and new clients coexist.
   - **Blocker:** `T1`; consumes the dual-protocol compatibility surface.
3. **`T3 — Contract old protocol support`**
   - Remove the old protocol only after all old use has ended and compatibility proof passes.
   - **Blocker:** `T2`; consumes the verified completion signal that records and clients no longer require the old form.

Blocking edges are `T1 -> T2 -> T3`. Each phase is an operable, releasable technical work unit; the phases are not claimed to be separate product-value slices merely because they are separate migration stages.

## Acceptance and proof

### `T1` acceptance

- New clients can use the new form while old clients continue to use the old form.
- Mixed old/new traffic preserves equivalent supported behavior and records remain readable through the required compatibility boundary.
- Deployment of `T1` alone is operable, releasable, and backward compatible.

**Proof:** compatibility tests run old-only, new-only, and mixed client traffic against the expanded protocol and persistence boundary; rollback to the pre-migration client population remains supported.

### `T2` acceptance

- Records migrate through resumable, idempotent batches or an equivalently safe bounded mechanism.
- During partial migration, both old and new clients remain operable and records in old and new forms remain correctly accessible.
- Failed or interrupted migration can resume without duplication, loss, or an unreadable intermediate state.
- Deployment at every migration checkpoint is operable, releasable, and backward compatible.
- Completion produces verifiable evidence of remaining old records and old-client use.

**Proof:** exercise unmigrated, partially migrated, completed, interrupted, resumed, and rollback-compatible states with concurrent old/new client compatibility tests; reconcile counts and identities before and after migration.

### `T3` acceptance

- Old protocol support is removed only when authoritative evidence reports zero old-client use and zero records requiring the old form.
- The new-only system preserves supported behavior and data access.
- The contracted deployment is operable and releasable, and the compatibility proof required by the settled source passes before removal.

**Proof:** gate contraction on read-back of zero old use, rerun the old/new compatibility evidence to prove migration completion, verify new-only caller-facing behavior and all migrated records, and prove an old client is rejected in the defined way rather than being silently misinterpreted.

# Case 9: `stale-approval`

## Return: proposal awaiting approval

- **Approved artifact:** revision `R7`.
- **Freshness finding:** the parent acceptance changed materially after approval, so `R7` no longer describes the current source and cannot authorize publication.
- **Required reconciliation:** trace the changed parent acceptance, update coverage, tickets, edges, acceptance, proof, and scope wherever affected, and assign a new identified revision.
- **Approval required:** explicit approval of that complete new revision.
- **Mutation:** none occurs.
- **Tracker state:** unchanged.
- **Safe continuation:** return to Approve with the reconciled proposal; publish only after fresh approval.

# Case 10: `partial-mutation`

## Return: partial-publication recovery

- **Intended graph:** parent `P`, blocker `T1`, and dependent `T2`.
- **Observed applied operations:** read-back confirms `P` and `T1`.
- **Failed or unknown operation:** creation of `T2` timed out. Current read-back cannot find `T2`, but the provider result remains unknown, so absence is not yet safe evidence that a duplicate-creating retry is harmless.
- **Unrelated state:** existing `T9` is observed unchanged and must remain untouched.
- **Graph status:** publication is incomplete and is not a successfully published graph.
- **Frontier risk:** the intended ready frontier and dependent relationship cannot be verified while `T2` may be absent, delayed, or created under an unobserved provider identity. `T1` may appear ready in observed state, but acting from that apparent frontier could proceed from an incomplete parent graph.
- **Safest non-duplicating recovery:**
  1. Do not recreate `P`, `T1`, or `T2`, and do not mutate `T9`.
  2. Reconcile the timed-out request using its stable idempotency key, correlation identifier, and provider search/read interfaces until `T2` is conclusively found or conclusively absent.
  3. If found, verify `T2`'s body, roles, state, parent, blocker relationship to `T1`, and affected dependents.
  4. If conclusively absent, resume only the missing `T2` operation with the same safe idempotency identity.
  5. Read back `P`, ordered children, bodies, roles, states, relationships, blocking edge, affected dependents, and the resulting frontier before returning success.
- **Safe continuation:** perform the bounded reconciliation above; do not implement or dispatch from the unverified frontier.

# Case 11: `route-table`

| Frontier | Exactly one next action |
| --- | --- |
| (a) Empty because blocker `B7` is open | Resolve blocker `B7`. |
| (b) Singleton `T1` | Run `$implement` for `T1`. |
| (c) Non-empty and a parent-delivery run was explicitly requested | Run `$parallel-implement` with the parent. |
| (d) `T1`/`T2` overlap on semantic ownership | Run `$implement` for `T1`, the first ticket in tracker order. |
| (e) `T1`/`T2` are substantial and isolated across semantics, production, proof, resources, and tripwires | Run `$parallel-implement` with the parent. |
| (f) Independence is uncertain | Run `$implement` for `T1`, the first ticket in tracker order. |

Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
