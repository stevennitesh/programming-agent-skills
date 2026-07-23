# tracer-positive

**Work unit form:** One thin, vertical risk-reduction slice: accept one signed
provider webhook at the real HTTP endpoint, pass its unmodified signing inputs
through the production verification library, and deliver one supported event
through the real event boundary. Limit production behavior to this single event
shape and exclude broader provider coverage, retries, replay handling, and
downstream business workflows.

**Acceptance:**

- A correctly signed representative request entering the real HTTP adapter is
  accepted and produces the expected event-boundary payload.
- A request with a changed body, invalid signature, or stale timestamp is
  rejected before the event boundary.
- The bytes and signature metadata used by verification are the ones received
  by the adapter; parsing does not silently alter the signed material.
- Unsupported event shapes are rejected or explicitly ignored without
  appearing as supported business events.

**Proof:** An adapter-level integration test drives signed requests through the
real HTTP route, production verification library, and event-boundary adapter,
with positive and negative cases. The test observes both the HTTP response and
the emitted or absent boundary event.

**Edges or gates:** No blocker is established by the case. Broader integration
delivery may consume this slice's proven adapter-to-boundary contract and is
therefore blocked on this result; unrelated provider work is not.

**Rationale:** The source names early feedback on one load-bearing integration
risk. A deliberately narrow end-to-end slice tests that risk at the highest
meaningful seam without prematurely building the rest of the integration.

# tracer-negative

**Work unit form:** One independently valuable vertical behavior slice:
notification preferences can be viewed and saved through the UI and API,
including persistence and the supported validation behavior. Do not split UI,
API, or persistence into separate tickets.

**Acceptance:**

- A user opens the preferences UI and sees the currently persisted supported
  preferences.
- Saving valid changes through the UI sends them through the public API,
  persists them, and shows the saved values after reload.
- Invalid or unauthorized changes are rejected with the supported user-visible
  and API behavior and do not alter stored preferences.
- Existing preferences remain unchanged when a save fails.

**Proof:** A caller-facing end-to-end or highest-available application test
drives the UI save path through the real API and persistence boundary, then
reloads the preferences. Focused API tests cover validation and authorization
branches that cannot be observed economically through the UI.

**Edges or gates:** Blockers: none. There is one ticket and therefore no
inter-ticket edge or special learning gate.

**Rationale:** This is a normal vertical product slice with standalone user
value. There is no settled risk-learning purpose that justifies recasting it as
a thinner experimental unit.

# support-positive

**Work unit form:** Create a separate enabling ticket for the reusable
test-harness adapter, followed by delivery ticket D1 for exports. The adapter
ticket owns only the durable adapter contract and its focused
behavior-preserving proof; it does not own export behavior. D1 consumes the
adapter to prove exports through the harness.

**Acceptance:**

- The adapter exposes the minimum reusable harness boundary required by D1 and
  the other approved delivery.
- Existing harness behavior remains unchanged for current callers.
- Both approved delivery callers can bind to the adapter without delivery-
  specific branching inside the adapter.
- D1 remains responsible for export behavior and its caller-facing proof.

**Proof:** Focused contract tests compare existing harness behavior before and
after the adapter and exercise representative bindings for both approved
deliveries. D1 separately proves export behavior through the resulting public
test seam.

**Edges or gates:** The adapter ticket blocks D1 and the other approved delivery
because both consume its durable contract. The two delivery tickets do not
block one another merely because they share that predecessor. The adapter must
pass its focused contract proof before either dependent begins consuming it.

**Rationale:** The enabling change is durable, independently provable, reduces
three sessions of embedded D1 work to one session, and unlocks two approved
deliveries. That distinct dependency unlock and favorable coordination
economics justify a separate ticket.

# support-cleanup

**Work unit form:** No ticket.

**Acceptance:** Not applicable. The coverage disposition is an explicit
no-ticket result for generic cleanup and speculative prefactoring.

**Proof:** Confirm from the bounded source that no approved delivery consumes
the cleanup, no observable delivery behavior or required proof depends on it,
and no settled scope grants it an independent outcome.

**Edges or gates:** None. It must not be introduced as a blocker for approved
delivery.

**Rationale:** Unrelated cleanup has no source-visible implementation
commitment, delivery unlock, independent approved value, or publication
justification. If a future approved delivery demonstrates a concrete need, it
can be reconsidered within that source boundary.

# support-inline

**Work unit form:** Keep the six-line durable helper inside delivery ticket D2.
D2 owns the helper, its focused proof, the behavior that consumes it, and the
caller-facing delivery proof.

**Acceptance:**

- The helper implements only the durable behavior D2 requires.
- Focused cases cover the helper's supported inputs and failure or boundary
  behavior.
- D2's observable behavior passes through the helper and succeeds at D2's
  public proof seam.
- No speculative generalization or unrelated caller migration is added.

**Proof:** A small focused test proves the helper contract, and D2's
caller-facing test proves the helper in the delivered behavior.

**Edges or gates:** No separate ticket and no dependency edge. The focused
helper proof is an internal completion check within D2.

**Rationale:** Although durable and testable, the helper is tiny and has no
separate dependency unlock identified by the source. A separate ticket would
cost more coordination than inline delivery.

# exposure-positive

**Work unit form:** Use an operable staged backfill sequence:

1. **B1 — Backfill mechanism and first bounded tenant batch.** Build the
   resumable tenant-batch mechanism, health observations, old/new compatibility
   checks, and tested rollback; execute only the approved first batch.
2. **B2 — Controlled widening.** Advance through successively approved tenant
   batches, stopping at every exposure boundary for operator review.
3. **B3 — Completion and compatibility closeout.** Process the remaining
   approved population, verify all records and consumers, and retire temporary
   compatibility or rollback support only after old usage has ended.

Each unit must leave the system operable and releasable. Batch definitions and
maximum exposure belong in the approved execution packet rather than being
chosen implicitly during implementation.

**Acceptance:**

- **B1:** Unmigrated, in-progress, successfully migrated, failed, retried, and
  rolled-back tenant states are distinguishable and safe. Old readers and
  writers remain compatible with both old and new record states. A failed batch
  stops widening, preserves a resumable checkpoint, and can be rolled back by
  the tested operator action. Operators can inspect batch identity, counts,
  error rate, latency or resource health, compatibility status, and rollback
  status before approving more exposure.
- **B2:** Each batch starts only from a recorded healthy predecessor gate;
  affects only its approved tenant set; preserves old/new compatibility; stops
  automatically or procedurally on the declared health thresholds; and records
  reconciled attempted, succeeded, failed, skipped, and rolled-back counts.
- **B3:** All in-scope records have exactly one reconciled final disposition;
  no old-format usage remains; post-backfill consumers pass compatibility and
  correctness checks; and rollback or compatibility support is removed only
  after its explicit contraction gate. Out-of-scope records remain untouched.

**Proof:**

- Focused tests cover batching, checkpoint/resume, idempotent retry, partial
  failure, old/new reads and writes, and rollback restoration.
- A production-like integration rehearsal exercises a mixed-state population
  and demonstrates health telemetry and the operator stop/rollback path.
- Every live batch produces read-back evidence for its tenant scope, record
  counts, compatibility checks, health thresholds, and rollback readiness.
- Final reconciliation queries account for the full ten-million-record scope
  and prove that temporary compatibility can be contracted safely.

**Edges or gates:** B2 is blocked by B1 because it consumes the proven mechanism
and first-batch health evidence. B3 is blocked by B2 because it consumes the
successfully widened population and reconciled batch evidence. Within B2, each
exposure increase has a serial operator gate: inspect health, compatibility,
count reconciliation, and tested rollback readiness; approve widening only
when all pass. A failed or unknown gate stops further batches without implying
that already verified batches failed.

**Rationale:** Ten million mutable records create material exposure and mixed-
state risk. Tenant batches provide bounded rollback and observable health.
Separate units are valuable because each exposure phase has a distinct
authority gate, proof result, and safe stopping point.

# exposure-negative

**Work unit form:** One atomic vertical ticket for the validation-message
change, including the message source, its public presentation boundary, and
focused regression coverage.

**Acceptance:**

- The triggering invalid input returns the settled new message at the public
  caller-facing boundary.
- Valid input and other validation branches retain their current behavior.
- The change is applied atomically; there is no supported mixed old/new state
  and no data, client, or schema migration.

**Proof:** A focused caller-facing validation test asserts the new message for
the target condition and regression cases for valid input and adjacent
validation conditions.

**Edges or gates:** Blockers: none. Normal review and proof are sufficient.
There are no batch-widening, compatibility, rollback, or migration gates.

**Rationale:** The change has one low-risk atomic outcome and no expanding
exposure boundary. Splitting it or inventing staged rollout gates would not
create independently valuable completion.

Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
