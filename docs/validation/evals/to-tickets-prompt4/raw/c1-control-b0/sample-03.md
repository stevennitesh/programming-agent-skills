# tracer-positive

**Work unit form:** One thin vertical risk-probe ticket: accept a signed provider webhook at the real HTTP endpoint, pass its unmodified signing inputs through the production verification library, and emit one representative event through the real event boundary. Scope is limited to the minimum happy path and one invalid-signature rejection needed to test this integration risk; broader provider feature coverage, retries, persistence, and operational hardening are excluded.

**Acceptance:**

- A correctly signed representative provider payload received by the real HTTP adapter is verified with the production verification library and becomes the expected boundary event.
- An incorrectly signed or tampered payload is rejected and emits no boundary event.
- The probe records whether the signing inputs survive HTTP parsing without a representation change that invalidates verification.

**Proof:** An integration test drives the real HTTP adapter with provider-representative signed bytes, observes the event-boundary output, and repeats with a tampered signature to observe rejection. This is the highest meaningful seam for the named uncertainty; a unit test of the verifier alone is insufficient.

**Edges or gates:** Blockers: none. This ticket must complete before tickets that assume the provider's signed-webhook path is viable. Passing proof is the gate for broadening the integration; failure returns the observed incompatibility for a design decision rather than starting full delivery.

**Rationale:** The slice is intentionally thinner than an independently valuable provider feature because its settled purpose is early learning about one load-bearing end-to-end integration risk.

# tracer-negative

**Work unit form:** One independently valuable vertical behavior ticket: let a user view, change, save, and subsequently retrieve notification preferences through the UI and API. Include the persistence and validation needed for that behavior; exclude unrelated notification delivery behavior and preference redesign.

**Acceptance:**

- A user can edit supported notification preferences in the UI and save them through the public API.
- A successful save persists the new values, and a fresh read or page load shows those values.
- Invalid values receive the established validation response and do not overwrite the last valid preferences.
- Existing preferences remain unchanged for users who do not submit an update.

**Proof:** A caller-facing end-to-end or browser/API integration test changes preferences through the UI, observes the API result, and verifies the persisted values on a fresh read. A focused API integration test proves invalid-input preservation.

**Edges or gates:** Blockers: none. No learning gate is introduced. Completion is judged entirely through this ticket's public behavior, without sibling work.

**Rationale:** There is no named uncertainty that justifies a risk-only probe. The smallest useful slice is the normal vertical user outcome.

# support-positive

**Decision and work unit form:** Create a separate enabling ticket S1 for the reusable test-harness adapter, followed by delivery ticket D1 for exports. S1 owns the durable adapter behavior and its reusable contract; D1 owns export behavior and consumes that contract. S1 excludes export implementation, while D1 excludes redesigning the adapter.

**S1 acceptance:**

- The adapter exposes the agreed reusable harness boundary for both approved deliveries.
- Existing harness behavior remains unchanged for current callers.
- Each approved delivery can substitute its test input through the adapter without delivery-specific branching in the shared contract.

**S1 proof:** Focused contract tests exercise current and new adapter paths and demonstrate behavior preservation for existing callers. A minimal consuming fixture for each approved delivery proves that the reusable seam is usable without implementing either delivery.

**D1 acceptance:** Export behavior meets its settled caller-visible acceptance through the production export seam and uses the proven adapter for its harness setup.

**D1 proof:** Focused export integration tests through the public export boundary, independent of the other approved delivery.

**Edges or gates:** S1 blocks D1 and the other approved delivery because both consume S1's required adapter outcome. S1's contract proof must pass before either dependent starts. The dependency graph is `S1 -> D1` and `S1 -> other approved delivery`.

**Rationale:** The adapter is durable, independently provable enabling work. The supplied economics favor separation: one session unlocks two deliveries, whereas embedding it in D1 takes three sessions and blocks the other delivery. This is a dependency-based split, not a split by file or team.

# support-cleanup

**Decision and work unit form:** No ticket. Record generic cleanup and speculative prefactoring as explicitly excluded from this bounded delivery graph.

**Acceptance:** Not applicable because no settled delivery outcome, consumer, or proof expectation has been supplied.

**Proof:** No delivery proof is warranted. Any future proposal must identify a concrete consuming outcome, bounded scope, owner, and behavior-preserving proof before admission.

**Edges or gates:** No nodes or edges are added, and no approved delivery is blocked on this cleanup.

**Rationale:** Unrelated cleanup is not justified by a named delivery, dependency unlock, or independently valuable outcome. Publishing it would turn speculation into ready work without settled source authority.

# support-inline

**Decision and work unit form:** Keep the six-line durable helper inside delivery ticket D2. D2 remains one vertical delivery slice and explicitly includes implementing the helper plus its focused behavior-preserving proof. The helper is not a separate node.

**Acceptance:**

- D2 delivers its settled caller-visible behavior.
- The helper provides the narrow behavior D2 requires and preserves the relevant existing behavior.
- The helper remains limited to the demonstrated D2 use; speculative generalization is excluded.

**Proof:** D2's caller-facing integration proof demonstrates the delivered behavior, and a focused helper test covers its durable contract and relevant edge case.

**Edges or gates:** Blockers: none beyond D2's existing true blockers. The focused helper test is an internal completion gate for D2, not a tracker edge.

**Rationale:** Although the helper is durable and provable, a separate ticket has greater coordination cost than inline implementation. It does not provide a valuable independent completion or unlock, so splitting would reduce delivery efficiency.

# exposure-positive

**Work unit form:** Use an expand-migrate-contract sequence with bounded exposure stages:

1. **E1 — Expand compatibility and controls:** establish backward-compatible old/new handling, tenant-batch selection, health checks, progress accounting, and tested rollback without changing all records.
2. **E2 — Pilot batch:** backfill a small named tenant cohort while old and new forms remain operable.
3. **E3 — Progressive batches:** widen through explicitly bounded tenant cohorts, retaining compatibility and rollback at every boundary.
4. **E4 — Complete migration and contract:** after all records are migrated and old usage is proven absent, remove the old form in a separate contraction ticket.

**Acceptance:**

- E1 proves old-only, new-only, mixed-state, retry/resume, and rollback branches; batches are idempotent and progress is observable.
- E2 changes only the pilot cohort, exposes batch health and compatibility status to operators, and can restore the pilot to its pre-batch state with the tested rollback.
- Each E3 batch changes only its declared tenants; operators can inspect error rate, throughput, old/new read compatibility, remaining population, and rollback readiness before widening.
- Failed or ambiguous health checks stop widening without corrupting completed or untouched tenants.
- E4 begins only when all ten million records are accounted for, no old-form usage remains, compatibility proof passes, and rollback or recovery obligations for contraction are met.

**Proof:**

- E1 uses integration tests against representative old, new, and mixed records, including interrupted-run resume and rollback.
- E2 runs the real migration on a production-like pilot dataset and records before/after counts, compatibility reads, health signals, and a rollback rehearsal.
- Every E3 batch produces reconciled record counts, compatibility-test results, operational-health evidence, and rollback verification before the next batch.
- E4 runs full compatibility/regression proof and verifies that no old-form reads or writes remain before removing support.

**Edges or gates:** `E1 -> E2 -> E3 -> E4`. Within E3, each tenant batch is a release gate rather than an automatically separate ticket: observe and reconcile health, old/new compatibility, counts, and rollback readiness; widen only on pass. On failure, stop exposure and execute or prepare the tested rollback according to the approved threshold. No stage requires the next stage to keep the system operable.

**Rationale:** Ten million records create material exposure risk, while tenant batching provides observable, reversible boundaries. Separating compatible expansion, controlled migration, and final contraction keeps every intermediate state releasable and prevents calendar order from replacing evidence-based gates.

# exposure-negative

**Work unit form:** One atomic vertical ticket for the validation-message change through the public validation boundary. Include the message source and caller-visible rendering needed for the change; exclude unrelated validation refactoring.

**Acceptance:**

- The triggering invalid input returns and displays the new approved message.
- Valid input behavior and other validation messages remain unchanged.
- The change is applied atomically through the supported path.

**Proof:** A focused caller-facing validation test submits the triggering invalid input and asserts the exact approved message; regression cases cover valid input and one unaffected validation condition.

**Edges or gates:** Blockers: none. The only completion gate is passing focused and relevant regression proof before the atomic release. No exposure-widening, compatibility, migration, or rollback stages are created.

**Rationale:** There is no expanding exposure boundary or non-atomic compatibility transition, so staged rollout tickets would add ceremony without isolating a distinct risk or independently valuable outcome.

Actions actually performed:

- None. No tracker mutation, skill invocation, implementation, or dispatch was performed.
