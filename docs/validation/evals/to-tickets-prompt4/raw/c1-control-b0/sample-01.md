# `tracer-positive`

## Work unit

Create one thin, fresh-session-sized tracer ticket: **“Prove signed provider
webhook traversal at the real event boundary.”** Its source is the settled
payment-provider integration decision owned by Owner A. The ticket implements
only the minimum production path needed to accept one representative signed
webhook through the real HTTP adapter, call the real verification library, and
emit the expected event-boundary representation. It excludes broad provider
event coverage, retry policy, persistence, downstream business handling, and
production rollout.

Blockers: none. Expected production scope is the webhook route/adapter,
verification-library integration seam, and event-boundary mapping. Semantic
owner: signed-webhook ingress. The public proof seam is an HTTP request at the
real adapter boundary observed as an event at the real event boundary.

## Acceptance and proof

- A correctly signed representative payload submitted through the real HTTP
  adapter reaches the real verifier and produces the specified normalized
  event, preserving the provider event identity and required payload fields.
- A payload with an invalid signature is rejected before the event boundary
  and emits no normalized event.
- A focused integration test exercises the actual HTTP adapter, verification
  library, and event-boundary adapter together; mocks may replace downstream
  consumers but not any of those three risk-bearing seams.
- The test records enough diagnostics to distinguish routing, signature
  verification, and mapping failures.

This is the thinnest useful vertical tracer because it crosses every seam named
in the load-bearing uncertainty while deliberately omitting unrelated product
behavior. Its result is observable and complete without sibling tickets, so it
can provide the requested early integration-risk feedback.

# `tracer-negative`

## Work unit

Create one vertical behavior ticket: **“Let a user save notification
preferences through the UI and API.”** The ticket owns the complete request
from the preferences UI through the API and supported persistence boundary,
including redisplaying the saved supported values. It is not labeled or split
as a tracer: the source names independently valuable behavior, not an
uncertainty-reduction experiment.

Blockers: none. Semantic owner: notification-preference update behavior.
Expected production scope is the preference UI, its API contract, validation,
and persistence path; unrelated notification delivery and preference redesign
are outside the fence.

## Acceptance and proof

- A user can select each supported notification preference, save it, refresh
  or revisit the UI, and observe the saved values.
- Invalid or unsupported values receive the settled validation response and do
  not partially update stored preferences.
- An end-to-end or highest-available caller-facing test drives the UI action
  through the real API boundary and verifies the persisted values through a
  subsequent read.
- Focused API tests cover accepted and rejected state branches without relying
  on unrelated notification-delivery completion.

There are no predecessor edges or staged gates. The single ticket is locally
provable and independently valuable; splitting it by UI, API, or storage layer
would create component tickets without a distinct proof or authority reason.

# `support-positive`

## Decision and work units

Create a separate enabling ticket **S1: “Add the reusable test-harness
adapter”**, followed by delivery tickets **D1: “Add exports”** and the other
approved delivery that consumes the same adapter. S1 is a durable,
behavior-preserving support slice with a distinct proof seam, and the supplied
economics make separation valuable: one session unlocks both deliveries,
whereas embedding it in D1 takes three sessions and delays the other delivery.

S1 owns only the reusable adapter and its contract. It excludes export
behavior, the other delivery's product behavior, generic harness cleanup, and
speculative abstractions. Semantic owner: test-harness adapter contract.
Expected production scope is none unless the settled adapter is itself shipped
runtime code; its write scope is the harness adapter and focused adapter tests.

## Acceptance and proof

- S1 exposes the settled reusable interface required by both D1 and the other
  approved delivery.
- Existing harness behavior remains unchanged for existing callers.
- A focused contract test proves representative existing and new callers use
  the adapter with equivalent setup, observation, and teardown behavior.
- D1's own acceptance remains observable export behavior through its public
  export seam; the other delivery retains its own independent product proof.

## Edges and rationale

Add blocking edges `S1 -> D1` and `S1 -> other approved delivery`, because each
delivery consumes S1's required adapter outcome. S1 has no blocker. After S1
passes its contract proof, both delivery tickets may enter the ready frontier;
their concurrency still depends on semantic, production-scope, proof-resource,
and serial-tripwire isolation and is not established merely by these edges.

# `support-cleanup`

## Decision

Create no ticket for the generic cleanup or speculative prefactoring. Map it as
an explicit exclusion/no-ticket disposition because it is unrelated to a
named delivery, has no settled independently valuable outcome, and has no
delivery-unlocking proof or authority boundary.

There is therefore no acceptance contract, proof lane, or blocker edge to
publish. If a later settled delivery demonstrates a concrete need, that
delivery should either include the necessary bounded change or justify a
separate enabling ticket with its own observable proof and favorable
coordination economics.

# `support-inline`

## Work unit

Keep the six-line durable helper inside **D2**. D2's scope explicitly includes
the helper, its focused proof, and the delivery behavior that consumes it.
Do not create a separate helper ticket or blocking edge: the supplied estimate
shows separation adds coordination cost, while the helper has no independently
valuable unlock or authority boundary.

## Acceptance and proof

- The helper satisfies the narrow input/output and error behavior required by
  D2 and does not broaden into a generic utility.
- A focused unit test covers the helper's supported branches.
- D2's highest meaningful caller-facing proof exercises the helper through
  D2's delivered behavior, so local helper proof cannot substitute for D2's
  public-seam proof.
- D2 completes without depending on an unrelated sibling.

The scope fence excludes opportunistic helper generalization, unrelated
call-site migration, and cleanup outside D2.

# `exposure-positive`

## Work units and graph

Use an expand-migrate-contract sequence whose intermediate states remain
operable:

1. **E1 — Expand compatibility and prove rollback controls.** Add the
   backward-compatible new record form/read path, batch checkpointing,
   old/new health comparisons, and the tested rollback mechanism. No records
   are widened beyond a bounded rehearsal cohort.
2. **E2 — Migrate through tenant batches.** Run the backfill as resumable,
   explicitly sized tenant batches. Each batch is an exposure increment, not
   an automatic new ticket; the ticket cannot advance to the next increment
   until the current gate passes.
3. **E3 — Contract the old form.** Remove old-form compatibility only after all
   ten million records are accounted for, old usage has ended, compatibility
   proof passes, and the final observation window is healthy.

Blocking edges are `E1 -> E2 -> E3`, because E2 consumes the compatibility and
rollback controls established by E1, and E3 consumes verified migration
completion from E2. Semantic ownership is respectively compatibility/control,
backfill progression, and old-form retirement. The shared schema, migration
checkpoint store, and production health dashboard are serial tripwires; only
one migration writer may advance exposure at a time.

## Gates, acceptance, and proof

E1 acceptance:

- Old records and newly written records remain readable and behaviorally
  compatible during migration.
- A bounded rehearsal batch can be applied, health-inspected, rolled back, and
  safely reapplied without duplicate or lost effects.
- Focused compatibility tests exercise old-only, new-only, and mixed old/new
  states; a rollback test verifies restoration from a partially completed
  batch.

E2 acceptance for every tenant batch:

- The batch has a durable identity, before/after counts, checkpoint, and
  idempotent resume behavior.
- Pre-widen gate: the prior batch has completed; error rate, latency, resource
  pressure, and old/new result comparison are within the settled thresholds;
  no unresolved compatibility signal exists; rollback remains available and
  has not exceeded its safe window.
- On a failed or unknown gate, widening stops. Operators either roll back the
  current batch or hold at the last verified checkpoint; they do not proceed
  on a provider receipt alone.
- A production-shaped rehearsal proves resume after interruption, a
  representative mixed-state read verifies compatibility, and per-batch
  read-back reconciles selected, changed, skipped, failed, and remaining
  records.
- Completion reconciles all ten million records with no unknown tenant or
  record state.

E3 acceptance:

- No old-form usage remains according to authoritative read-back.
- Full-corpus reconciliation and a final mixed-version compatibility test pass
  before contraction.
- After contraction, caller-facing regression proof passes and rollback or a
  documented safe forward-recovery route remains valid for the settled
  operational window.

The batch ladder bounds blast radius and makes every widening decision
observable and reversible. Separate expand, migration, and contract tickets are
warranted because they have distinct state, rollback, and proof gates; the
system remains releasable between them.

# `exposure-negative`

## Work unit

Create one atomic vertical ticket: **“Change the validation message.”** It
updates the settled caller-visible message at its real validation boundary and
all directly owned expectations. There is no expand-migrate-contract sequence,
batch ladder, canary ticket, or exposure edge because the change has neither an
expanding exposure boundary nor a compatibility migration.

## Acceptance and proof

- The triggering invalid input returns the exact settled new message through
  the public caller-facing validation seam.
- Valid inputs and other validation branches retain their existing behavior.
- A focused boundary test proves the changed branch and representative
  unchanged branches.
- The normal completion gate is one passing focused proof plus the repository's
  required regression checks; no staged widening gate is invented.

Blockers: none. Semantic owner: the validation-message behavior. The scope
fence excludes validation redesign, unrelated copy cleanup, and compatibility
machinery. The ticket is independently complete when the atomic behavior and
its regression proof pass.

Actions actually performed:

- None. No tracker mutation, skill invocation, implementation, or dispatch was
  performed.
