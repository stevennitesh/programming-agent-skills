# H1-03 / m0 / sample-02

## Runtime telemetry

- Runtime: Codex desktop, fresh independent context
- Model: gpt-5.6-sol
- Reasoning effort: high
- Selected arm: `skills/experimental/to-tickets/controls/m0/SKILL.md`
- Arm policy: implicit invocation disabled; this run is an explicit invocation
- Fixture source: `SRC-H103@1`
- Proposal correlation key: `CAMP-73`
- Deterministic ticket key: `CAMP-73-T1`
- Tracker: `fixture-tracker`
- Live-provider contact: none
- Repository mutation during worker execution: none
- Fixture mutation boundary: one authorized creation attempt per subcase, followed only by the documented reconciliation reads

## Frozen publication payload

The payload below is identical in subcases A through F.

### CAMP-73-T1 — Enforce 30-day audit-record retention

- **Bounded slice / work-unit form:** one vertical behavior slice that enforces the settled 30-day audit-record retention policy through the scheduled retention path.
- **Parent:** `P-H103`
- **Category role:** `enhancement`, authorized by `SRC-H103@1`
- **Intended tracker state:** `ready-for-agent`
- **Source Trace:** `SRC-H103@1`, owner Eli (audit owner), commitment C1, outcome “Create one audit-retention policy ticket,” acceptance “records older than 30 days are deleted by the scheduled proof fixture,” proof seam “retention scheduler integration fixture.”
- **Desired behavior:** when the scheduled retention path runs, audit records strictly older than 30 days are deleted.
- **Edge behavior:** audit records exactly 30 days old and newer are not in the source-authorized deletion set.
- **Error behavior:** a scheduler or deletion failure must be observable in the integration fixture and must not be reported as passing retention proof.
- **Observable acceptance:** a retention-scheduler integration fixture seeds eligible and ineligible audit records, runs the scheduled path, proves that all records strictly older than 30 days were deleted, proves that records at the 30-day boundary and newer remain, and fails visibly if scheduling or deletion fails.
- **Dependency state:** true blockers `none`. This is the only slice and therefore the first stable tracker item.
- **Proof lane:** retention scheduler integration fixture.
- **Verification authority:** Eli, audit owner, against the source acceptance.
- **Verification evidence required:** passing integration-fixture result with the fixed time boundary plus before/after record identities showing eligible deletion and ineligible retention.
- **Expected durable production write scope:** the audit-retention policy and its scheduled enforcement seam; at runtime, deletion is limited to audit records strictly older than 30 days.
- **Scope fence:** no unrelated retention policy, no live-provider operation, no blind retry, no implementation work outside the retention-policy slice.
- **Parallel-safety judgment:** serialize work that mutates the shared retention scheduler fixture or its audit-record test state. This is a serial constraint, not a blocker edge.
- **Execution profile:** semantic owner Eli; production writes limited to the retention policy and scheduled enforcement seam; proof uses the retention scheduler integration fixture; order 1 of 1; serial tripwire is shared scheduler-fixture or audit-data state; no independent sibling slice exists.
- **State-boundary matrix:**
  - absent/initial policy: establish the 30-day rule and prove scheduled deletion;
  - current reusable 30-day policy: preserve it and prove the same scheduled behavior;
  - legacy/incompatible policy: replace the incompatible retention value through the bounded policy seam and prove the 30-day result;
  - public access path: the scheduled retention execution path;
  - supported variants: the source-authorized audit-record retention policy only;
  - lifecycle: scheduled evaluation identifies records strictly older than 30 days, deletes that eligible set, and preserves boundary/newer records.

The frozen graph is one node, `P-H103 -> CAMP-73-T1`, with no blocker edges and predicted ready frontier `[CAMP-73-T1]` after parent, role, and ready-state mutations read back exactly. The fixture exposes no `set_parent`, `set_role`, `set_state`, or `get_dependents` operation, so a successful creation can be reconciled and body-verified but cannot be claimed as a completely published graph. No missing relationship, role, or state is treated as implicit.

## Worker response

### A

**Typed result: partial-publication recovery.**

Provider-native idempotency was preferred. The single `create_with_idempotency` call succeeded and returned the deterministic item. `get_item` read back the frozen ticket body exactly. The creation is therefore known and must not be repeated. The graph is not claimed complete because the available fixture surface cannot apply or read back the parent relationship, `enhancement` role, or `ready-for-agent` state.

- Applied operation: idempotent creation of `CAMP-73-T1`.
- Failed operation: none.
- Unavailable completion operations: `set_parent`, `set_role`, `set_state`, and relationship/frontier read-back.
- Affected dependent items: none.
- Observed frontier: unknown; the item cannot be treated as ready without state and relationship read-back.
- Safest recovery: retain `CAMP-73` as the idempotency key, do not recreate the item, expose the missing tracker operations, apply the intended parent/role/state once, and refetch the item and affected relationships.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — A

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_with_idempotency(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: success, applied once; native idempotency accepted; returned item key `CAMP-73-T1`.
4. `get_item("CAMP-73-T1")`
   - Result: success; item key and complete frozen ticket body match exactly.

No correlation query or second create was issued.

### B

**Typed result: partial-publication recovery.**

The single non-idempotent `create_item` call returned an ambiguous result. No retry was made. Correlation reconciliation found exactly one item, `T-731`, for `CAMP-73`; `get_item` proved that its ticket key and complete body match the frozen publication payload. `T-731` is the created item to retain, and creation must not be retried. Parent, role, state, and resulting frontier remain unverified because their mutation/read-back operations are unavailable.

- Applied operation: creation is reconciled as applied to `T-731`.
- Failed operation: none conclusively observed.
- Unavailable completion operations: `set_parent`, `set_role`, `set_state`, and relationship/frontier read-back.
- Affected dependent items: none.
- Observed frontier: unknown; `T-731` cannot be treated as ready without state and relationship read-back.
- Safest recovery: adopt `T-731`, do not recreate, expose the missing tracker operations, apply the intended parent/role/state once, and refetch the item and affected relationships.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — B

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_item(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: ambiguous; application status unknown.
4. `query_correlation("CAMP-73")`
   - Result: success; exactly one exact correlation match, item `T-731`.
5. `get_item("T-731")`
   - Result: success; deterministic ticket key and complete frozen ticket body match exactly.

No second create was issued.

### C

**Typed result: partial-publication recovery.**

The single `create_item` call returned an ambiguous result. Correlation reconciliation returned zero items, but the fixture states that this absence is not conclusive. The creation may still have applied and must not be retried.

- Applied operations: unknown.
- Failed operations: none conclusively observed.
- Affected dependent items: potentially the not-yet-observable `CAMP-73-T1`; no known dependents.
- Observed frontier: unknown.
- Safest recovery: preserve `CAMP-73`, perform a later authoritative reconciliation capable of proving application or non-application, and create nothing until that result is conclusive. If an exact item appears, verify its complete body and continue it; only a conclusive not-applied result permits a new controlled attempt.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — C

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_item(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: ambiguous; application status unknown.
4. `query_correlation("CAMP-73")`
   - Result: success; zero matches, with absence explicitly inconclusive.

No `get_item` target existed, and no second create was issued.

### D

**Typed result: partial-publication recovery.**

The single `create_item` call returned an ambiguous result. Correlation reconciliation returned two matching items, so neither item can be selected as the authoritative publication and no retry is safe.

- Applied operations: at least one possible creation, exact application count unresolved.
- Failed operations: none conclusively observed.
- Affected dependent items: both correlation matches; no known dependents.
- Observed frontier: unknown and potentially duplicated.
- Safest recovery: freeze mutation, inspect both provider records under `CAMP-73`, identify the authoritative exact-body item, quarantine or resolve the duplicate through tracker-owned recovery, and only then finish missing relationships/state and refetch. Do not create another item.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — D

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_item(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: ambiguous; application status unknown.
4. `query_correlation("CAMP-73")`
   - Result: success; two matching items returned.

No item was adopted, no second create was issued, and no further mutation occurred.

### E

**Typed result: partial-publication recovery.**

The single `create_item` call returned an ambiguous result. Correlation reconciliation found one item, but its body belongs to `PR-72`, not the authorized `PR-73` / `SRC-H103@1` publication. It is not adopted as `CAMP-73-T1`, and the mismatch does not prove that the attempted creation failed. No retry is safe.

- Applied operations: unknown.
- Failed operations: no conclusive failure; the correlation match is conflicting.
- Affected items: the single conflicting `PR-72` item and any still-unobserved result of the ambiguous create.
- Observed frontier: unknown.
- Safest recovery: freeze mutation, investigate the correlation-key collision or stale provider record, obtain conclusive disposition of the ambiguous `PR-73` attempt, and do not modify the `PR-72` item or issue another create.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — E

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_item(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: ambiguous; application status unknown.
4. `query_correlation("CAMP-73")`
   - Result: success; exactly one item returned.
5. `get_item(match[0].id)`
   - Result: success; body Source Trace belongs to `PR-72` and conflicts with the frozen `PR-73` / `SRC-H103@1` payload.

The conflicting item was not adopted or mutated, and no second create was issued.

### F

**Typed result: partial-publication recovery.**

The single `create_item` call failed conclusively before application. Correlation reconciliation confirmed absence, so no duplicate was created. The tracker remains without the child item.

- Applied operations: none.
- Failed operation: creation of `CAMP-73-T1`, conclusively not applied.
- Affected dependent items: none.
- Observed frontier: empty for this proposed graph.
- Safest recovery: preserve the frozen payload and failure evidence. A later publication owner may make a new controlled attempt only after the reported failure cause is repaired and the complete required tracker mutation/read-back surface is available; this run performs no retry.
- Next owner recommendation: `none`.

#### Simulated tracker operation log — F

1. `get_setup()`
   - Result: success; configured tracker is `fixture-tracker`; setup and source surfaces are complete.
2. `get_parent("P-H103")`
   - Result: success; parent `P-H103` exists.
3. `create_item(correlation_key="CAMP-73", item_key="CAMP-73-T1", body=<frozen publication payload>)`
   - Result: failure; conclusively not applied.
4. `query_correlation("CAMP-73")`
   - Result: success; zero matches and absence is confirmed.

No second create was issued.

Execution stopped after subcase F.
