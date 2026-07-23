# tracer-positive

**Work unit form:** one tracer-bullet vertical slice for provider webhook
ingress. Send one representative provider-signed event through the real HTTP
route and adapter, call the production verification library, and hand the
verified event to the real event-boundary contract. Limit the slice to the
smallest event type and success/failure outcomes needed to test that path;
provider-wide event handling, retries, persistence, and downstream business
behavior remain outside this ticket.

**Acceptance:**

- A correctly signed representative request entering through the real HTTP
  route reaches the event boundary as the expected normalized event.
- A request with an invalid signature is rejected before the event boundary.
- The test uses the production adapter and verification library rather than
  test substitutes for the load-bearing path.
- The result records whether the integration assumption held and identifies
  any boundary mismatch discovered.

**Proof:** an integration test at the HTTP boundary using fixed signed request
fixtures and the production verification path, asserting both the accepted
event delivered at the event boundary and the invalid-signature rejection.

**Edges or gates:** blockers: none. This work does not block on the complete
payment integration. Any later provider-delivery ticket that relies on this
path consumes the proven adapter/verification/event-boundary outcome and is
blocked by this ticket.

**Rationale:** the named value is early evidence about one load-bearing
integration risk. A thin real-path tracer gives that evidence sooner than a
full provider feature while retaining observable proof through the uncertain
boundary.

# tracer-negative

**Work unit form:** one independently valuable vertical behavior slice:
“Save notification preferences,” spanning the UI interaction, API request,
validation, persistence, and returned/displayed saved state.

**Acceptance:**

- A user can select supported notification preferences and save them in the
  UI.
- The API validates and persists the submitted preferences for that user.
- Reloading the UI returns and displays the persisted values.
- Invalid preference values receive the defined validation response and do not
  alter the previously saved state.

**Proof:** a caller-facing end-to-end or highest-available application test
that saves preferences through the UI/API boundary and verifies them after a
fresh read, plus an invalid-input case proving state is unchanged.

**Edges or gates:** blockers: none. No learning gate or follow-on tracer edge
is introduced.

**Rationale:** this is already a normal, independently valuable vertical
slice. With no named uncertainty or early-learning purpose, recasting it as a
tracer would add no useful slicing distinction.

# support-positive

**Work unit form:** create a separate durable support ticket,
“Provide the reusable test-harness adapter,” followed by delivery tickets D1
and the other approved delivery.

**Adapter acceptance:**

- The harness exposes the stable adapter behavior required by both approved
  deliveries.
- Existing harness consumers retain their current behavior.
- Both deliveries can consume the adapter without delivery-specific branching
  or private copies.
- The adapter's supported inputs, outputs, and failure behavior are explicit.

**Proof:** focused adapter contract tests for supported inputs, outputs, and
failure behavior, plus the existing harness regression suite proving
behavior preservation.

**Edges or gates:** the adapter ticket has no blocker. D1 and the other
approved delivery each have a blocking edge from the adapter ticket because
each consumes its durable adapter outcome. D1 still owns export behavior and
its caller-facing export proof; the adapter ticket does not absorb that
delivery scope.

**Rationale:** the adapter has durable reusable behavior and independent proof,
and the supplied economics favor separation: one session unlocks two approved
deliveries instead of adding three sessions inside D1 and delaying the other
delivery. This is a dependency-unlocking support slice, not a split by file or
layer.

# support-cleanup

**Work unit form:** no ticket.

**Acceptance and proof:** not applicable because there is no admitted delivery
commitment to accept or prove. Record the cleanup and speculative prefactoring
in the coverage map as excluded: it is unrelated to a named delivery outcome
and has no source justification for publication.

**Edges or gates:** none; it must not become an invented blocker for approved
delivery.

**Rationale:** generic cleanup and speculative prefactoring do not become
ticketable merely because they may be technically desirable. Without a
settled delivery purpose, distinct proof value, or dependency unlock, a
separate support ticket would expand scope.

# support-inline

**Work unit form:** keep the six-line durable helper inside D2. D2 remains one
vertical delivery ticket; its expected write scope and covered commitments
explicitly include the helper.

**Acceptance:**

- D2's caller-visible behavior is complete through its highest meaningful
  boundary.
- The helper provides the narrowly required behavior for D2, including its
  defined edge or failure case.
- No duplicate helper path is introduced.

**Proof:** D2's public-seam test proves the delivered behavior, and a focused
helper test proves the durable helper contract and edge case.

**Edges or gates:** no separate helper ticket and therefore no new blocking
edge. D2 retains its original true blockers, if any.

**Rationale:** although the helper is durable and testable, it is tiny and the
supplied estimates show that separation costs more coordination than inline
delivery. It does not provide a valuable independent completion or unlock.

# exposure-positive

## E1 — Expand with a compatible, controllable backfill path

**Work unit form:** an expand-phase technical slice that introduces the
tenant-batched backfill mechanism, health observations, mixed old/new
compatibility, checkpointing, and the tested rollback path without requiring
all records to migrate.

**Acceptance:**

- Before any production widening, an operator can select a bounded tenant
  batch, preview its scope, execute it, inspect health, and invoke rollback.
- Not-started, running, completed, failed, rolled-back, and resumed batches
  have explicit, observable states.
- Re-running or resuming a batch cannot silently double-apply the data change.
- Old and new representations remain operable for unmigrated, migrated, and
  mixed-state tenants.

**Proof:** integration tests over representative tenant data for successful,
failed, resumed, and rolled-back batches; compatibility tests covering old,
new, and mixed states; and an operator-path test proving health and checkpoint
visibility.

**Edges or gates:** blockers: none. E2 consumes E1's compatible batch,
observation, and rollback capability and is blocked by E1.

## E2 — Migrate through bounded exposure stages

**Work unit form:** one migrate-phase delivery ticket operated as a sequence of
tenant-batch exposure stages: a canary batch, limited widening, and progressive
widening to the remaining population. Individual routine batches are gates
within this ticket, not separate tickets.

**Acceptance:**

- The canary begins only after E1 proof passes and records its exact tenant and
  record scope.
- Before every widening, operators verify the completed batch, health
  indicators, old/new compatibility, checkpoint integrity, and rollback
  readiness.
- A failed gate stops widening and leaves the last known completed checkpoint;
  rollback returns the affected batch to its proved compatible state.
- Widening completes only when all intended tenants and all ten million
  records are reconciled, with no unexplained skipped or duplicate records.
- During partial migration, both migrated and unmigrated tenants remain
  operable.

**Proof:** production-equivalent rehearsal of canary, failure, rollback, and
resume; per-stage reconciliation totals and health evidence; compatibility
checks before each widening decision; and final full-population reconciliation
against the intended ten-million-record scope.

**Edges or gates:** E1 blocks E2. Within E2 the serial gates are:
canary health and compatibility pass → limited widening; limited widening
health and compatibility pass → progressive widening; every subsequent batch
requires the same read-back before the next begins. These are exposure gates,
not concurrency candidates.

## E3 — Contract only after migration is proven complete

**Work unit form:** a contract-phase slice that removes the old compatibility
path only after it is no longer used.

**Acceptance:**

- E2's reconciliation proves the entire intended population migrated.
- Telemetry or an equivalent observation proves old-form usage has ended.
- Removing the old path leaves new-form reads and writes operable.
- The rollback boundary is explicitly moved or retired only according to the
  approved migration contract.

**Proof:** compatibility and caller-facing regression tests against the fully
migrated state, evidence of zero old-path usage, and a rehearsal showing the
post-contract recovery procedure.

**Edges or gates:** E2 blocks E3 because E3 consumes the completed migration
and zero-old-usage outcomes. The old path remains until both gates pass.

**Rationale:** expand-migrate-contract keeps every intermediate state operable.
Tenant batches bound exposure, while health, compatibility, reconciliation,
and tested rollback provide an evidence gate before each increase in blast
radius.

# exposure-negative

**Work unit form:** one atomic vertical behavior ticket for the validation
message change, including the production validation response and every
caller-visible rendering that is part of that behavior.

**Acceptance:**

- The triggering invalid input returns the approved validation message at the
  public boundary.
- Valid input behavior is unchanged.
- Other validation cases are unchanged.
- The change is applied atomically with no mixed old/new compatibility state.

**Proof:** a focused public-boundary test for the changed invalid case plus
regression cases for valid input and unchanged validation failures.

**Edges or gates:** blockers: none. Use the ordinary test-and-review completion
gate; do not create exposure stages, batch gates, rollback tickets, or
expand-migrate-contract edges.

**Rationale:** the change has neither a widening exposure boundary nor a
compatibility migration. Additional staged work units would add coordination
without reducing a material risk.

Actions actually performed:

- Wrote this no-mutation evaluation artifact.
- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
