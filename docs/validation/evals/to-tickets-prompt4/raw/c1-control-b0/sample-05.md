# tracer-positive

**Work unit form:** One thin, vertical integration-risk tracer: accept a single
signed webhook request at the real HTTP endpoint, pass its untouched body and
signature through the production verification library, and emit one canonical
event at the real event boundary. Limit supported behavior to one representative
event type and the valid-signature and invalid-signature branches; exclude
provider-wide event coverage, retries, persistence, and downstream business
handling.

**Acceptance:**

- A correctly signed representative provider payload sent through the real HTTP
  adapter is verified and crosses the production event boundary once as the
  expected canonical event.
- A tampered payload or invalid signature is rejected before the event boundary,
  with no event emitted.
- The test uses the provider library's real signing/verification behavior rather
  than replacing verification with a mock.

**Proof:** A focused integration test drives an HTTP request through the
production adapter and verification library and observes the event-boundary
output; its negative branch observes rejection and absence of output. This is
the highest meaningful seam for the named uncertainty.

**Edges or gates:** True blockers: none. The tracer is complete only when both
signature branches pass at the public HTTP-to-event seam. Broader integration
work may consume the proven adapter/verification/event path and therefore is
blocked by this outcome if it relies on that path.

**Rationale:** The slice is intentionally narrower than a user-complete provider
integration because its named value is early evidence about the one
load-bearing end-to-end path, not delivery of the full feature.

# tracer-negative

**Work unit form:** One independently valuable vertical behavior slice: let a
user edit notification preferences in the UI, persist them through the real API,
and see the saved values after reload. Include validation and authorization
needed for that behavior; exclude unrelated notification delivery changes.

**Acceptance:**

- An authorized user can select supported notification preferences, save them,
  reload the page, and see the persisted selections.
- Invalid preference values are rejected without changing stored preferences.
- A user cannot change another user's preferences.

**Proof:** A focused browser or full-stack acceptance test exercises the UI,
real API boundary, and persistence read-back. API-level negative tests prove
validation and authorization at their public boundary.

**Edges or gates:** True blockers: none. Completion is gated by observable
save-and-reload behavior plus the two negative branches. There is no separate
tracer dependency or learning gate.

**Rationale:** With no named uncertainty or risk-learning purpose, the useful
unit is the normal user-valued vertical slice rather than an artificially thin
technical probe.

# support-positive

**Work unit form:** Split out one durable enabling/support ticket, S1, for the
reusable test-harness adapter, followed by delivery ticket D1 for exports. S1
owns only the stable adapter contract and behavior-preserving integration with
the harness; D1 owns export behavior and consumes that contract.

**Acceptance:**

- S1 exposes the agreed reusable harness adapter and preserves existing harness
  behavior for current callers.
- Both D1's export tests and the other approved delivery can use the adapter
  without delivery-specific branches in S1.
- D1 produces the required exports through its public delivery seam using the
  adapter, without expanding S1 into export implementation.

**Proof:** S1 has focused contract tests for adapter inputs, outputs, and
behavior preservation, plus an integration test using one representative
current harness consumer. D1 has its own export acceptance test at the public
export seam.

**Edges or gates:** `S1 -> D1` is a blocking edge because D1 consumes S1's
adapter outcome. The other approved delivery also depends on S1 if it consumes
the adapter. S1 must pass its behavior-preservation proof before either
dependent begins using the contract.

**Rationale:** S1 is a durable, independently provable enabling change; the
supplied estimates make the split economically meaningful because one session
unlocks two deliveries while inlining it into D1 would take three sessions and
hold up the other delivery.

# support-cleanup

**Work unit form:** No ticket. Record the generic cleanup and speculative
prefactoring as excluded from this bounded delivery graph.

**Acceptance:** Not applicable because no implementation work unit is admitted.
The coverage map explicitly records: generic cleanup — excluded, no settled
delivery commitment; speculative prefactoring — excluded, no demonstrated
consumer or proof obligation.

**Proof:** Source-to-coverage review confirms neither item is required by a
named delivery outcome, acceptance criterion, migration, or proof lane.

**Edges or gates:** No edges and no readiness gate are created.

**Rationale:** Cleanup alone does not justify a separately grabbable ticket.
Creating one would add speculative scope without an independently approved
outcome.

# support-inline

**Work unit form:** Keep the six-line durable helper inside delivery ticket D2.
D2 remains one vertical delivery slice and names the helper as internal scope,
not as a separate ticket.

**Acceptance:**

- D2's externally observable delivery behavior passes through its public seam.
- The helper satisfies its small, stable input/output contract and handles its
  relevant boundary case.
- The helper introduces no behavior change outside D2's stated scope.

**Proof:** D2 has its normal public-seam acceptance test, accompanied by a
focused unit test for the helper's contract and boundary case.

**Edges or gates:** No inter-ticket edge. D2 completion is locally gated on both
the public delivery proof and the helper's focused proof.

**Rationale:** The helper is required and durable, but its tiny scope and
supplied coordination estimate make separate completion less valuable than
including it in D2.

# exposure-positive

**Work unit form:** Use an expand-migrate-contract sequence with operable
exposure stages:

1. E1 expands the system to support old and new record forms concurrently,
   adds health/compatibility telemetry, implements tested rollback, and proves
   one tenant batch can be migrated safely.
2. E2 migrates successive bounded tenant batches, widening exposure only after
   the prior batch's gate passes.
3. E3 contracts the compatibility path only after all records are migrated and
   evidence shows old-form usage has ended.

Each batch in E2 is an exposure checkpoint within the migration ticket rather
than an arbitrary layer split. If a later batch has distinct authority,
rollback, or operational ownership, make that batch a separate ordered
migration ticket with the same gate.

**Acceptance:**

- E1 leaves the system operable with old-only, new-only, and mixed old/new
  records; readers and writers remain compatible in each applicable branch.
- E1 exposes per-batch health and progress, proves a tenant-scoped rollback
  restores the prior form, and migrates a canary tenant without data loss.
- For every E2 batch, record counts and invariants reconcile, application
  health remains within the settled threshold, old and new forms remain
  readable during the observation window, and rollback remains available
  before the next batch widens exposure.
- E2 completes only when all ten million records are accounted for and no
  failed or unknown tenant batch remains.
- E3 removes old-form support only after telemetry and reconciliation prove no
  old usage remains; the new-only path then passes compatibility and behavior
  acceptance.

**Proof:** E1 uses compatibility tests covering old-only, new-only, and mixed
states; a production-like canary migration test; telemetry assertions; and a
rollback rehearsal. Each E2 batch produces read-back evidence for counts,
invariants, error/latency health, compatibility, and rollback readiness.
E3 runs the full compatibility/behavior suite in new-only state and verifies
that no old-form reads or writes remain.

**Edges or gates:** `E1 -> E2 -> E3` are blocking edges because migration
consumes the compatible expanded form and contraction consumes verified
completion of migration. Within E2, batch `n+1` may start only after batch `n`
meets reconciliation, health, compatibility, observation-window, and rollback
gates. A failed or unknown gate stops widening and triggers the tested rollback
or an explicit recovery decision.

**Rationale:** Tenant batches create meaningful exposure boundaries with
observable health and rollback. Expand-migrate-contract preserves operability
through intermediate states and prevents the irreversible contraction from
preceding verified migration.

# exposure-negative

**Work unit form:** One atomic vertical ticket for the validation-message
change, including the production message and its caller-visible behavior.

**Acceptance:**

- The applicable invalid input returns the approved new validation message at
  the public validation boundary.
- Valid input behavior and unrelated validation messages remain unchanged.

**Proof:** A focused public-boundary test asserts the new message for the
target invalid input and regression cases for valid input and one unaffected
validation branch.

**Edges or gates:** True blockers: none. The only completion gate is passing
the focused behavior and regression proof before the atomic release. There are
no batch-widening, compatibility, migration, or rollback stages.

**Rationale:** With no expanding exposure boundary and no compatibility
migration, additional staged tickets or operational gates would add ceremony
without independent value.

Actions actually performed:

- Tracker mutation: none.
- Skill invocation: none.
- Implementation: none.
- Dispatch: none.
