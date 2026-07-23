# To Tickets Prompt 4 Evaluation

## 1. `ordinary-feature`

**Typed Return: proposal awaiting approval — revision `OF-R1`.**

### Source Trace summary

- Source owner and publication authority: `Owner A`.
- Settled outcome: a user submits an order through the API, the order is saved, and an operations user can see that new order in the existing dashboard.
- Required production seams: API, domain service, database, and existing dashboard.
- Accepted decisions: use the existing dashboard; make the saved order observable to both the submitting user and operations.
- Deferrals/rejections: none stated.
- Scope exclusion: no new order-editing, cancellation, refund, or dashboard-administration behavior.
- Proof expectation: observable end-to-end behavior through the public API and the existing operations dashboard.
- Material gaps: none.

### Coverage map

| Source commitment or boundary | Disposition |
| --- | --- |
| User can submit an order through the API | `T1` acceptance and API proof |
| Submitted order is durably saved | `T1` acceptance and persistence proof |
| Submitting user sees the saved order | `T1` acceptance and public API proof |
| Operations user sees the new order in the existing dashboard | `T1` acceptance and dashboard proof |
| API, domain service, database, and dashboard participate | `T1` production scope |
| No unrelated order lifecycle or dashboard administration | `T1` scope fence |

### Ordered graph and predicted frontier

- Tracker order: `T1`.
- Blocking edges: none.
- Predicted ready frontier after verified publication: `T1`.
- Rationale: this is one vertical behavior slice with one coherent end-to-end proof; splitting it by API, service, database, or dashboard would create layer tickets that could not independently prove the settled outcome.

### Intended tracker mutations

1. Create `T1` under the bounded source/parent represented by `OF-R1`.
2. Record `Owner A` as publication authority, the Source Trace, acceptance, proof lane, scope, and readiness metadata below.
3. Set `T1` open, unclaimed, and ready-for-agent with no blockers.
4. Add no blocking relationships.

### Ticket `T1` — Submit, persist, and surface a new order

- Form: fresh-session-sized vertical behavior slice.
- Roles: source owner/publication authority `Owner A`; implementation owner unclaimed.
- Blockers and consumed outcome: `none`; consumes no predecessor outcome.
- Why this slice: the API submission and dashboard visibility jointly express the single settled outcome, and their highest meaningful proof is end to end.
- What to build: carry an accepted order submission through the API and domain service into durable storage, return the saved order to the user, and expose that same order in the existing operations dashboard.
- Covered commitments: all commitments in the coverage map.
- Acceptance:
  - Given a valid order request, the public API accepts it and returns the saved order with its stable persisted identity and values.
  - Reading the stored state confirms exactly that order was durably saved through the domain service/database path.
  - An operations user opening the existing dashboard can see that same newly saved order with matching identity and material values.
  - A rejected/invalid request is not represented as a saved order or shown as a newly created order in the dashboard.
- Highest meaningful proof seam: a caller-facing end-to-end scenario through the public API and operations dashboard, with a persistence assertion at the database boundary.
- Proof lane:
  - Focused API scenario submits a valid order and verifies the saved representation.
  - Persistence check verifies the committed record and identity.
  - Dashboard scenario verifies the operations view obtains and renders the same order.
  - Negative scenario verifies an invalid submission produces no persisted/dashboard order.
- Source Trace and durable context: `OF-R1`; target repository API, order-domain, persistence, and existing-dashboard owners.
- Expected production scope: order API boundary, order domain service, order persistence mapping/schema only if required by the settled representation, and existing dashboard order query/view.
- Semantic ownership: creation and cross-surface visibility of a newly submitted order.
- Shared resources and serial tripwires: database-backed proof and the end-to-end environment are shared proof resources; serialize with other work mutating the same order contract or using the exclusive test database.
- Parallel-safety note/execution profile:
  - Size: one substantial focused-session slice.
  - Public proof seam: submit through the API and observe the same saved order in the dashboard.
  - Focused proof: API, persistence, dashboard, and invalid-submission scenarios above.
  - Production exclusions: unrelated order lifecycle and dashboard administration.
  - Parallel eligibility: not established within this one-ticket proposal; it owns a cross-component semantic seam and shared database proof.
- Scope fence: do not add editing, cancellation, refund, payment, generalized dashboard redesign, or unrelated schema cleanup.

No tracker state changes under this simulation. Publication requires explicit approval of exactly `OF-R1`; any material change requires reconciliation and fresh approval.

Safe continuation: `Owner A` approves or rejects proposal revision `OF-R1`.

## 2. `source-conflict`

**Typed Return: source-gap packet.**

- Evidence: settled source specifies a 30-day refund window; the approved ADR specifies 14 days.
- Conflict: both artifacts are decision-bearing authorities, and neither supersedes the other.
- Material effect: choosing either value changes supported refund behavior, acceptance, implementation scope, and proof.
- Tracker state: unchanged; no slicing or mutation occurs.
- Required resolution: the accountable source/ADR owners must establish one authoritative refund window and record which decision supersedes the other.
- Safe continuation: return the reconciled, owner-approved refund decision as settled source, then restart Trace.

## 3. `setup-gap`

**Typed Return: setup precondition.**

- Evidence: the target repository has neither a tracker contract nor a provider mapping.
- Missing prerequisites: the repository-local Ready-for-agent contract, tracker transport/provider mapping, relationship semantics, ready query, packet mechanics, and Mutation read-back procedure.
- Tracker state: unchanged; no proposal, ticket, or mutation is attempted.
- Exact safe continuation: run `$repo-bootstrap` to establish a compatible tracker contract and provider mapping, then rerun To Tickets against the same settled source.

## 4. `economics`

### Case A

- Size judgment: one two-line documentation correction with a ten-minute proof is small, not substantial, and cannot economically justify parallel dispatch.
- Exactly one next recommendation: `$implement` the ready documentation ticket.

### Case B

- Size judgment: both tickets are substantial because each requires a full focused session; their distinct semantic owners, production scopes, public proof seams, and fixtures, plus the absence of a shared scarce resource or serial tripwire, establish production and proof isolation.
- Exactly one next recommendation: `$parallel-implement` with the parent.

## 5. `graph-distinctions`

- Blockers:
  - `T2`: `none`.
  - `T1`: `none`.
  - `T3`: blocked by `T1` because `T3` consumes the schema created by `T1`.
- Blocking edge: `T1 -> T3`.
- Tracker order: `T2`, `T1`, `T3`. This is presentation/pick order, not a blocking relationship.
- Predicted overlap: `T2` and `T3` both touch `registry.py`, but their semantic ownership is different; filename overlap alone creates no blocking edge.
- Serial tripwire: `T2` and `T3` must not execute their database-writing proof concurrently because the test database permits only one writer.
- Ready frontier: `T2`, `T1`. Both are open, ready-for-agent, unclaimed, and have satisfied blockers; `T3` is excluded until `T1` completes.
- Exactly one next recommendation: `$implement` `T2`, the first frontier ticket in tracker order, because the graph contains a serial proof-resource tripwire.

## 6. `incomplete-independence`

- Size judgment: both tickets are substantial.
- Execution judgment: parallel eligibility is not established. Disjoint predicted files do not prove semantic, production-scope, public-proof, fixture, or resource isolation, and uncertainty defaults to serial execution.
- Exactly one next recommendation: `$implement` `T1`, the first ticket in tracker order.

## 7. `state-matrix`

### Proposed acceptance

| Axis | Branch | Observable acceptance |
| --- | --- | --- |
| Initial cache state | Absent | The first access builds the cache from authoritative data and returns the correct result without requiring a prior cache artifact. |
| Initial cache state | Reusable current | Access reuses the current compatible cache, returns the correct result, and does not rebuild it unnecessarily. |
| Initial cache state | Legacy incompatible | Access does not treat legacy data as current; it safely invalidates/rebuilds or performs the settled compatibility path, then returns a current result without exposing mixed state. |
| Access surface | CLI | CLI output and exit status reflect the same cache result and failures as the supported contract. |
| Access surface | API | API response and error behavior reflect the same cache result and failures as the supported contract. |
| Profile | Default | Default-profile policy is applied consistently for absent, reusable-current, and legacy-incompatible state. |
| Profile | Strict | Strict-profile policy is applied consistently for absent, reusable-current, and legacy-incompatible state, including rejecting rather than silently accepting any state forbidden by strict policy. |
| Transition | Reuse | A second eligible access reuses the current artifact and preserves its identity/version evidence where the contract promises reuse. |
| Transition | Invalidation | A relevant source/config/version change marks the old artifact unusable and the next access produces or selects valid current state. |
| Transition | Restart | After process restart, persisted compatible state remains reusable, while persisted incompatible state follows invalidation/compatibility policy. |

Cross-axis acceptance: every supported combination of initial state (absent, reusable current, legacy incompatible), access surface (CLI, API), and profile (default, strict) must produce contract-consistent observable behavior. Reuse, invalidation, and restart transitions must be exercised from every initial-state branch for which the transition is meaningful. No listed axis is evidenced as non-applicable.

### Proposed proof lane

- Use a public CLI harness and a public API harness against the same controlled authoritative data and cache store.
- Seed each initial state explicitly: no artifact, a current compatible artifact with observable identity/version, and a legacy incompatible artifact.
- Run a parameterized matrix across all `3 x 2 x 2` initial-state/access/profile combinations, asserting returned value, surface-specific status/error behavior, cache version/identity, and whether rebuild occurred.
- For reuse, perform a second access and assert compatible state is reused rather than rebuilt.
- For invalidation, change the relevant source/config/version input, access again, and assert the old state is not served and valid current state results.
- For restart, restart the process between accesses and assert compatible persisted state remains reusable while incompatible persisted state follows the appropriate invalidation or strict rejection path.
- Include failure assertions proving CLI and API never expose partially rebuilt or mixed legacy/current cache state.
- Highest meaningful proof seam: caller-visible CLI and API behavior across the complete state/profile/transition matrix, with cache-store observations used only to prove reuse, invalidation, and restart semantics.

## 8. `migration`

Use `expand-migrate-contract`; each unit must leave the deployed system operable, releasable, and backward compatible.

### Proposed work units and edges

1. `T1 — Expand`: add the new protocol form alongside the old form without removing or changing old-client support.
2. `T2 — Migrate`: migrate records and new-client traffic through the compatible dual-protocol system while old clients continue to operate.
3. `T3 — Contract`: remove old protocol support only after all old use has ended and compatibility/completion proof has passed.

Blocking edges:

- `T1 -> T2`: migration consumes the dual-protocol capability introduced by Expand.
- `T2 -> T3`: Contract consumes evidence that records and traffic have migrated and old use has ended.

### `T1 — Expand`

- Acceptance: old clients retain their prior behavior; new clients can use the new protocol; old and new representations coexist without corrupting or hiding records; deployment and rollback remain operable.
- Proof: caller-facing compatibility suite runs old- and new-client scenarios against the same deployed stage, including reads/writes across both representations and rollback/restart checks.

### `T2 — Migrate`

- Acceptance: records migrate incrementally through releasable checkpoints; old and new clients remain operable at every checkpoint; resumed or retried migration is safe; newly written and already migrated records are readable under the applicable compatibility contract; completion evidence accounts for all records and old-client traffic.
- Proof: stage-by-stage migration tests cover unmigrated, partially migrated, and fully migrated populations; old/new client compatibility runs at every checkpoint; interruption/retry and rollback checks prove no inoperable intermediate state; reconciliation evidence identifies residual old records and old use.

### `T3 — Contract`

- Acceptance: entry requires verified zero old-client use, zero residual old-form records where removal requires migration, and passing compatibility proof; only then is old support removed; new clients and migrated records remain fully operable and releasable; no old compatibility path remains accidentally reachable.
- Proof: precondition/read-back evidence establishes all old use has ended and migration is complete; the new-client public suite passes after removal; negative proof shows the old protocol is unavailable; deployment, restart, and rollback policy are verified for the contracted stage.

Each phase has its own operability proof, but these technical migration phases are not claimed to be independent parallel product slices.

## 9. `stale-approval`

**Typed Return: proposal awaiting approval.**

- Evidence: `R7` was approved, but the parent acceptance changed materially before publication.
- Freshness result: `R7` no longer matches the bounded source, so its approval does not authorize publication.
- Tracker state: unchanged.
- Mutation: none occurs.
- Safe continuation: reconcile the changed parent acceptance into a new identified proposal revision and obtain explicit approval of that exact revision before any publication.

## 10. `partial-mutation`

**Typed Return: partial-publication recovery.**

- Approved target graph: parent `P`, blocker `T1`, dependent `T2`, and their approved relationships.
- Observed applied operations: `P` and `T1` exist on read-back.
- Failed/unknown operation: the `T2` create request timed out; provider state is unknown even though current read-back cannot find `T2`.
- Unrelated state: existing `T9` is observed unchanged and is outside the recovery scope.
- Exactness result: the approved graph is not verified; relationship/body/readiness checks involving `T2` cannot pass.
- Frontier risk: any apparent frontier containing `T1` is incomplete and unsafe to present as the verified graph frontier. `T2` might exist under an unobserved/delayed provider state, might later appear without its approved relationship, or might truly be absent. Blindly recreating it risks a duplicate; proceeding as though it is absent risks losing the dependent work.
- Simulation tracker state: unchanged beyond the facts supplied; no recovery mutation is performed.
- Safest non-duplicating recovery: stop publication, reconcile the timed-out request through its stable idempotency key/provider reference and repeated authoritative lookup, and do not issue another create while existence is unknown. Once `T2` is conclusively found or conclusively absent, read back the full affected graph; repair only the missing approved operation if absence is proved, then verify `P`, `T1`, `T2`, bodies, roles, state, relationships, blocking edge, affected dependents, and frontier. Leave `T9` untouched.

## 11. `route-table`

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
