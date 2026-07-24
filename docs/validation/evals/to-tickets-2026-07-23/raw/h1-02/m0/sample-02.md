# Runtime telemetry

- Fixture: `H1-02`
- Selected arm: `skills/experimental/to-tickets/controls/m0`
- Host: Codex desktop, fresh independent context
- Model: `gpt-5.6-sol`
- Reasoning effort: high
- Tracker: `fixture-tracker` (simulated; no live provider contacted)
- Source revision: `SRC-H102@1`
- Approved publication revision: `PR-52`
- Mutations: limited to the two approved fixture items and their settled metadata

# Complete worker response

## Published graph

**Typed result:** `published graph`

**Source / parent:** `SRC-H102@1` / `P-H102`

**Publication revision:** `PR-52`

**Stable order:**

1. `T-H102-1` — Migrate scheduled jobs from schema v1 to restart-safe schema v2
2. `T-H102-2` — Display the configured retry limit

### Exact read-back body: T-H102-1

```markdown
# Migrate scheduled jobs from schema v1 to restart-safe schema v2

## Bounded slice

Migrate persisted scheduled-job records from schema v1, which has no timezone field, to schema v2, which stores timezone and retry count. The migration must remain operable when restarted, retain a proved rollback path, and contract legacy support only after old usage has ended and compatibility proof passes.

Work-unit form: migration stage using expand-migrate-contract.

## Source Trace

- Source: SRC-H102@1
- Parent: P-H102
- Approved proposal: PR-52
- Commitment: C1 — migrate v1 jobs to restart-safe v2 with rollback proof
- Acceptance: v1 absent/current/incompatible/restart branches are proved
- Proof seam: job_migration_matrix

## Desired behavior and acceptance

- Expand: readers accept both v1 records without timezone and current v2 records with timezone and retry count while migration is active.
- Migrate: each valid v1 record is durably rewritten as v2 without losing its existing job behavior; the v2 result contains timezone and retry count.
- Initial or absent state: when no persisted job record exists, migration performs no write and succeeds without fabricating a job.
- Current reusable state: an already-valid v2 record is reused without destructive rewriting or data loss.
- Legacy state: a valid v1 record without timezone is converted to v2 and remains readable through the supported scheduled-job access path.
- Incompatible state: a record that is neither supported v1 nor valid v2 fails safely, is not partially rewritten, and produces observable migration failure evidence.
- Restart behavior: interruption before completion can be followed by rerun; completed records are not duplicated or corrupted and remaining supported records can finish.
- Rollback: rollback of the expanded/migrated form is proved before any contraction begins.
- Contract: legacy v1 support is removed only after old v1 usage has ended and compatibility plus rollback proof has passed.
- Error behavior: a failed durable write leaves no record falsely presented as successfully migrated.

## State-boundary matrix

| Boundary | Supported behavior | Required proof |
|---|---|---|
| Absent / initial | No record means no migration write and no fabricated job | Matrix case observes no-op success |
| Current reusable | Valid v2 with timezone and retry count is reused without destructive rewrite | Matrix case preserves the v2 record |
| Legacy | Valid v1 without timezone is read and written as valid v2 | Matrix case proves conversion and subsequent read |
| Incompatible | Neither valid v1 nor valid v2 fails safely with no partial durable conversion | Matrix case proves failure and unchanged durable state |
| Restart after interruption | Rerun resumes safely; completed work is not duplicated or corrupted | Restart case interrupts and reruns |
| Public access path | Supported scheduled-job readers continue to read jobs during expand and after migration | Compatibility case exercises the scheduled-job read path |
| Lifecycle transition | expand -> migrate/restart -> rollback proof -> end old usage -> contract | Ordered evidence records every gate before contraction |

Supported variants are v1 without timezone during the compatibility window and v2 with timezone and retry count. No other record shape is accepted.

## Expected durable write scope

- Scheduled-job schema v2 representation
- Scheduled-job migration and compatibility reader
- Migration checkpoint or equivalent restart-safety state, if the existing seam requires it
- Migration proof fixtures for the state matrix and rollback

No retry-limit display changes, unrelated helper renames, UI mockup work, or tracker-procedure changes.

## Dependency state

True blockers: none.

Stable tracker order: 1.

## Proof lane

- Lane: `job_migration_matrix`
- Verification authority: the settled scheduled-job migration integration fixture owned by the jobs domain
- Verification evidence: passing cases for absent, valid current v2, legacy v1, incompatible record, interrupted/restarted migration, supported access during compatibility, and rollback before contraction

## Parallel safety

Safe to run in parallel with T-H102-2 because this slice owns persistence compatibility and migration proof, while T-H102-2 is a stateless display-only read with a separate proof fixture. This ticket is serial within itself across expand, migrate/restart proof, rollback proof, old-usage exhaustion, and contract. Contraction before those gates is a serial tripwire.

## Scope fence

In scope: scheduled-job v1/v2 compatibility, durable migration, restart safety, rollback proof, and gated contraction.

Out of scope: retry-limit display, historical narrative, UI mockups, speculative helper renaming, copied tracker procedures, meeting pleasantries, implementation dispatch, and delivery execution.
```

Read-back metadata:

- Parent: `P-H102`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: none
- Blockers: none
- Dependents: none

### Exact read-back body: T-H102-2

```markdown
# Display the configured retry limit

## Bounded slice

Display the configured retry limit as a pure read of the existing configuration.

Work-unit form: independently completable stateless behavior slice.

## Source Trace

- Source: SRC-H102@1
- Parent: P-H102
- Approved proposal: PR-52
- Commitment: C2 — display the configured retry limit
- Acceptance: display is a pure read of configured retry limit
- Proof seam: retry_display unit fixture

## Desired behavior and acceptance

- The displayed retry limit equals the value supplied by the existing configuration seam.
- Reading and displaying the value does not mutate configuration, scheduled-job persistence, retry counters, or migration state.
- Edge behavior: supported boundary values supplied by the configuration seam are displayed without substitution.
- Error behavior: if the configuration seam cannot supply a valid retry limit, the existing error path is preserved and no value or state is fabricated.

## State-boundary matrix

Not applicable: this slice is stateless and only reads the configured retry limit.

## Expected durable write scope

- Retry-limit display/view code
- `retry_display` unit fixture

No durable data, schema, migration, configuration, or retry-counter writes.

## Dependency state

True blockers: none.

Stable tracker order: 2.

## Proof lane

- Lane: `retry_display` unit fixture
- Verification authority: the settled unit fixture at the configured retry-limit read seam
- Verification evidence: passing cases for the configured value, supported boundary values, purity/no mutation, and the existing invalid-or-unavailable configuration error path

## Parallel safety

Safe to run in parallel with T-H102-1. It has no expected production-write overlap, shared durable state, migration ordering, or shared scarce proof resource with the migration slice.

## Scope fence

In scope: pure read and display of the configured retry limit plus its focused unit proof.

Out of scope: job-schema migration, configuration mutation, retry-counter mutation, historical narrative, UI mockups, speculative helper renaming, copied tracker procedures, meeting pleasantries, implementation dispatch, and delivery execution.
```

Read-back metadata:

- Parent: `P-H102`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: none
- Blockers: none
- Dependents: none

## Coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `T-H102-1` |
| Outcome: display retry limit | `T-H102-2` |
| C1: restart-safe v1-to-v2 migration with rollback proof | `T-H102-1` acceptance, state matrix, proof lane, and serial gates |
| C2: display configured retry limit | `T-H102-2` acceptance and proof lane |
| v1 records have no timezone | `T-H102-1` legacy branch |
| v2 stores timezone and retry count | `T-H102-1` current and migration target branches |
| absent/current/incompatible/restart proof | `T-H102-1` state-boundary matrix |
| rollback before contraction | `T-H102-1` lifecycle gate and proof lane |
| pure configuration read | `T-H102-2` acceptance and stateless classification |
| Historical narrative, abandoned mockups, helper-renaming speculation, copied tracker procedure, and pleasantries | Explicitly excluded; no ticket |
| Delivery execution | Source exclusion; no ticket |

## Dependency graph and ready frontier

- `T-H102-1`: blockers `none`
- `T-H102-2`: blockers `none`
- Blocking edges: none
- Cycles or contradictory order: none
- Ready frontier, in tracker order: `T-H102-1`, `T-H102-2`

## Execution profiles

| Ticket | Semantic ownership | Production writes | Proof resources | Ordering / tripwires | Independence |
|---|---|---|---|---|---|
| `T-H102-1` | Scheduled-job schema compatibility and migration | v2 representation, compatibility/migration path, restart checkpoint if required | `job_migration_matrix`, rollback evidence | Internally serial: expand, migrate/restart proof, rollback proof, old-usage exhaustion, contract | Independent of display slice |
| `T-H102-2` | Retry-limit presentation | Display/view code only; no durable state | `retry_display` unit fixture | No migration ordering; purity is the tripwire | Independent of migration slice |

## Mutation read-back

Both created tickets read back with the exact bodies shown above. Parent, authorized `enhancement` role, `ready-for-agent` state, unassigned status, blocker-free graph, and ready frontier match the frozen PR-52 publication design.

**Gaps:** none.

**Observed tracker state:** `P-H102` has exactly `T-H102-1` and `T-H102-2`; both are open, unclaimed, `ready-for-agent`, and blocker-free.

**Exact safe continuation:** publication is complete; retain the verified graph unchanged.

**Recommended next owner:** `none`.

# Complete simulated tracker operation log

1. `get_setup()`
   - Result: `ok`
   - Observed tracker: `fixture-tracker`
   - Observed Ready contract: bounded slice, Source Trace, observable acceptance with edge/error behavior, dependency state, proof lane, expected durable write scope, parallel-safety judgment, scope fence, work-unit form, verification authority, and verification evidence
   - Ready state: `ready-for-agent`
   - Authorized role: `enhancement`

2. `get_parent("P-H102")`
   - Result: `ok`
   - Observed: parent `P-H102` exists; source reference `SRC-H102@1`; children `[]`

3. `create_item({ proposal: "PR-52", order: 1, body: <T-H102-1 body below> })`
   - Mutation result: `ok`
   - Created fixture ID: `T-H102-1`
   - Exact submitted body:

```markdown
# Migrate scheduled jobs from schema v1 to restart-safe schema v2

## Bounded slice

Migrate persisted scheduled-job records from schema v1, which has no timezone field, to schema v2, which stores timezone and retry count. The migration must remain operable when restarted, retain a proved rollback path, and contract legacy support only after old usage has ended and compatibility proof passes.

Work-unit form: migration stage using expand-migrate-contract.

## Source Trace

- Source: SRC-H102@1
- Parent: P-H102
- Approved proposal: PR-52
- Commitment: C1 — migrate v1 jobs to restart-safe v2 with rollback proof
- Acceptance: v1 absent/current/incompatible/restart branches are proved
- Proof seam: job_migration_matrix

## Desired behavior and acceptance

- Expand: readers accept both v1 records without timezone and current v2 records with timezone and retry count while migration is active.
- Migrate: each valid v1 record is durably rewritten as v2 without losing its existing job behavior; the v2 result contains timezone and retry count.
- Initial or absent state: when no persisted job record exists, migration performs no write and succeeds without fabricating a job.
- Current reusable state: an already-valid v2 record is reused without destructive rewriting or data loss.
- Legacy state: a valid v1 record without timezone is converted to v2 and remains readable through the supported scheduled-job access path.
- Incompatible state: a record that is neither supported v1 nor valid v2 fails safely, is not partially rewritten, and produces observable migration failure evidence.
- Restart behavior: interruption before completion can be followed by rerun; completed records are not duplicated or corrupted and remaining supported records can finish.
- Rollback: rollback of the expanded/migrated form is proved before any contraction begins.
- Contract: legacy v1 support is removed only after old v1 usage has ended and compatibility plus rollback proof has passed.
- Error behavior: a failed durable write leaves no record falsely presented as successfully migrated.

## State-boundary matrix

| Boundary | Supported behavior | Required proof |
|---|---|---|
| Absent / initial | No record means no migration write and no fabricated job | Matrix case observes no-op success |
| Current reusable | Valid v2 with timezone and retry count is reused without destructive rewrite | Matrix case preserves the v2 record |
| Legacy | Valid v1 without timezone is read and written as valid v2 | Matrix case proves conversion and subsequent read |
| Incompatible | Neither valid v1 nor valid v2 fails safely with no partial durable conversion | Matrix case proves failure and unchanged durable state |
| Restart after interruption | Rerun resumes safely; completed work is not duplicated or corrupted | Restart case interrupts and reruns |
| Public access path | Supported scheduled-job readers continue to read jobs during expand and after migration | Compatibility case exercises the scheduled-job read path |
| Lifecycle transition | expand -> migrate/restart -> rollback proof -> end old usage -> contract | Ordered evidence records every gate before contraction |

Supported variants are v1 without timezone during the compatibility window and v2 with timezone and retry count. No other record shape is accepted.

## Expected durable write scope

- Scheduled-job schema v2 representation
- Scheduled-job migration and compatibility reader
- Migration checkpoint or equivalent restart-safety state, if the existing seam requires it
- Migration proof fixtures for the state matrix and rollback

No retry-limit display changes, unrelated helper renames, UI mockup work, or tracker-procedure changes.

## Dependency state

True blockers: none.

Stable tracker order: 1.

## Proof lane

- Lane: `job_migration_matrix`
- Verification authority: the settled scheduled-job migration integration fixture owned by the jobs domain
- Verification evidence: passing cases for absent, valid current v2, legacy v1, incompatible record, interrupted/restarted migration, supported access during compatibility, and rollback before contraction

## Parallel safety

Safe to run in parallel with T-H102-2 because this slice owns persistence compatibility and migration proof, while T-H102-2 is a stateless display-only read with a separate proof fixture. This ticket is serial within itself across expand, migrate/restart proof, rollback proof, old-usage exhaustion, and contract. Contraction before those gates is a serial tripwire.

## Scope fence

In scope: scheduled-job v1/v2 compatibility, durable migration, restart safety, rollback proof, and gated contraction.

Out of scope: retry-limit display, historical narrative, UI mockups, speculative helper renaming, copied tracker procedures, meeting pleasantries, implementation dispatch, and delivery execution.
```

4. `create_item({ proposal: "PR-52", order: 2, body: <T-H102-2 body below> })`
   - Mutation result: `ok`
   - Created fixture ID: `T-H102-2`
   - Exact submitted body:

```markdown
# Display the configured retry limit

## Bounded slice

Display the configured retry limit as a pure read of the existing configuration.

Work-unit form: independently completable stateless behavior slice.

## Source Trace

- Source: SRC-H102@1
- Parent: P-H102
- Approved proposal: PR-52
- Commitment: C2 — display the configured retry limit
- Acceptance: display is a pure read of configured retry limit
- Proof seam: retry_display unit fixture

## Desired behavior and acceptance

- The displayed retry limit equals the value supplied by the existing configuration seam.
- Reading and displaying the value does not mutate configuration, scheduled-job persistence, retry counters, or migration state.
- Edge behavior: supported boundary values supplied by the configuration seam are displayed without substitution.
- Error behavior: if the configuration seam cannot supply a valid retry limit, the existing error path is preserved and no value or state is fabricated.

## State-boundary matrix

Not applicable: this slice is stateless and only reads the configured retry limit.

## Expected durable write scope

- Retry-limit display/view code
- `retry_display` unit fixture

No durable data, schema, migration, configuration, or retry-counter writes.

## Dependency state

True blockers: none.

Stable tracker order: 2.

## Proof lane

- Lane: `retry_display` unit fixture
- Verification authority: the settled unit fixture at the configured retry-limit read seam
- Verification evidence: passing cases for the configured value, supported boundary values, purity/no mutation, and the existing invalid-or-unavailable configuration error path

## Parallel safety

Safe to run in parallel with T-H102-1. It has no expected production-write overlap, shared durable state, migration ordering, or shared scarce proof resource with the migration slice.

## Scope fence

In scope: pure read and display of the configured retry limit plus its focused unit proof.

Out of scope: job-schema migration, configuration mutation, retry-counter mutation, historical narrative, UI mockups, speculative helper renaming, copied tracker procedures, meeting pleasantries, implementation dispatch, and delivery execution.
```

5. `set_parent("T-H102-1", "P-H102")`
   - Mutation result: `ok`

6. `set_parent("T-H102-2", "P-H102")`
   - Mutation result: `ok`

7. No `set_blocker` call.
   - Frozen graph contains no true blocking edge.

8. `set_role("T-H102-1", "enhancement")`
   - Mutation result: `ok`

9. `set_role("T-H102-2", "enhancement")`
   - Mutation result: `ok`

10. `set_state("T-H102-1", "ready-for-agent")`
    - Mutation result: `ok`

11. `set_state("T-H102-2", "ready-for-agent")`
    - Mutation result: `ok`

12. `get_item("T-H102-1")`
    - Result: `ok`
    - Body: exact match to the complete submitted `T-H102-1` body in operation 3
    - Parent: `P-H102`
    - Role: `enhancement`
    - State: `ready-for-agent`
    - Assignee: none
    - Blockers: none

13. `get_item("T-H102-2")`
    - Result: `ok`
    - Body: exact match to the complete submitted `T-H102-2` body in operation 4
    - Parent: `P-H102`
    - Role: `enhancement`
    - State: `ready-for-agent`
    - Assignee: none
    - Blockers: none

14. `get_dependents("T-H102-1")`
    - Result: `ok`
    - Dependents: `[]`

15. `get_dependents("T-H102-2")`
    - Result: `ok`
    - Dependents: `[]`

16. `get_parent("P-H102")`
    - Result: `ok`
    - Children in stable tracker order: `["T-H102-1", "T-H102-2"]`

Final simulated mutation log:

```text
create_item(PR-52, order=1) -> ok, T-H102-1
create_item(PR-52, order=2) -> ok, T-H102-2
set_parent(T-H102-1, P-H102) -> ok
set_parent(T-H102-2, P-H102) -> ok
set_role(T-H102-1, enhancement) -> ok
set_role(T-H102-2, enhancement) -> ok
set_state(T-H102-1, ready-for-agent) -> ok
set_state(T-H102-2, ready-for-agent) -> ok
```
