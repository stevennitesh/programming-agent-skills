# Published graph

**Result type:** `published graph`

**Evidence:** `SRC-N02@1`, owned by Dae (jobs owner); authorized derived design `R52`; compatible `fixture-tracker` setup; parent `P-N02`; proof seams `job_migration_matrix` and `retry_display`; exact simulated mutation read-back below.

**Tracker state:** Before publication, `P-N02` existed with no children. After publication, it has the two ordered, unassigned, `enhancement`, `ready-for-agent` children below. No other simulated tracker state changed.

## Ordered item 1

**Reference:** `FT-N02-01`
**Title:** Migrate scheduled jobs to restart-safe schema v2

Exact stored body:

```text
Bounded slice
Migrate supported scheduled-job records from schema v1 to valid schema v2 through an expand-migrate-contract sequence while keeping supported reads operable, making restart safe, and retaining rollback until guarded removal is proven safe.

Work-unit form
Migration work unit: expand compatible v2 handling, migrate through operable and releasable restart-safe stages, prove rollback, then contract old-read support only after old usage has ended and the compatibility guard passes.

Source Trace
Parent: P-N02
Source: SRC-N02@1
Owner: Dae, jobs owner
Authorized design: R52
Commitment: C1 migrate v1 jobs to restart-safe v2 with rollback proof
Acceptance pointer: absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior
Proof pointer: job_migration_matrix

Desired behavior and acceptance
- An absent job remains absent; migration is a no-op and does not fabricate state.
- A current valid v2 job remains usable and is not remigrated or duplicated.
- A supported v1 job, which lacks timezone, is transformed according to authorized design R52 into a valid v2 job containing the required timezone and retry-count fields.
- An incompatible or unrecognized record is detected and left intact; the migration reports the failure instead of partially or destructively rewriting it.
- Supported reads remain operable throughout the expand and migration stages, and writes produced during migration are valid v2.
- If migration is interrupted, completed durable work remains identifiable and a restart resumes safely without duplicate effects or corruption.
- Rollback restores the last supported pre-contract state and is proven before removal of old-read support.
- Old-read support is removed only after the guard proves old usage has ended and compatibility and rollback evidence pass.
- job_migration_matrix passes every distinct state and lifecycle branch listed below.

Edge and error behavior
Absent, already-current, legacy, incompatible, interrupted, restarted, rollback, and premature-contract paths must be observable. Detection or proof failure must preserve the last operable state, report failure, and keep old-read support in place.

Relevant seams
Scheduled-job schema-version detection; v1/v2 read compatibility; v2 encoder and durable job write; migration progress/checkpoint boundary; rollback path; old-read removal guard; job_migration_matrix.

Expected durable write scope
Production writes are limited to scheduled-job schema-v2 records and the migration progress or checkpoint state required for restart safety. The guarded contract stage may remove only the old-read compatibility path after its acceptance guard passes. No UI, unrelated job behavior, or tracker state is written by implementation.

Scope fence
In scope: scheduled-job schema v1-to-v2 compatibility, restart-safe migration, valid-v2 writes, rollback proof, and guarded removal of old reads. Out of scope: retry-limit display, unsettled product changes, unrelated schema changes, broad helper renames, abandoned UI mockups, and tracker transport examples.

Dependency state
True blockers: none.
Stable tracker order: 1.

Proof lane
Run job_migration_matrix across the complete state-boundary matrix, inject an interruption after a durable partial step, restart, exercise rollback, and attempt guarded removal both before and after compatibility proof.

Verification authority
Dae, as jobs owner and source-meaning authority for SRC-N02@1 and R52, verifies the fixture evidence against the stated acceptance.

Verification evidence
A passing job_migration_matrix result identifying each tested branch and showing: no fabricated absent state; unchanged reusable v2; valid migrated v2; intact incompatible state with reported failure; safe interruption and idempotent restart; successful rollback; rejected premature removal; and successful removal only after old usage ends and compatibility proof passes.

Parallel-safety judgment
Serial-constrained. The ticket crosses durable migration, compatibility, rollback, and contract-removal boundaries and uses the migration fixture and job-state proof resource. Run its own expand, migrate, rollback, and contract stages serially. This serial constraint is not a blocker edge for the independent retry-limit display ticket.

State-boundary matrix
| Branch or interaction | Required behavior |
| --- | --- |
| Absent / initial | No job is created; no migration progress is fabricated. |
| Current reusable state | Valid v2 remains readable and writable, with no duplicate migration. |
| Legacy state | Supported v1 stays readable during expansion and becomes valid v2 through restart-safe migration. |
| Legacy interruption and restart | Durable progress is recognized; restart resumes without duplicate effects, partial invalid v2, or corruption. |
| Legacy rollback | The last supported pre-contract state is restored and remains readable. |
| Incompatible state | Record is preserved, failure is reported, and contract is blocked. |
| Public access paths | Scheduled-job readers remain operable during expand and migrate; scheduled-job writers emit valid v2. |
| Supported variants | v1 during compatibility and migration; v2 as current and migrated form. |
| Contract transition | Old-read removal is rejected before old usage ends or proof passes and allowed only after both conditions hold. |
| High-risk interaction | Interruption, restart, and rollback before contract must not strand an unreadable or partially rewritten job. |
```

## Ordered item 2

**Reference:** `FT-N02-02`
**Title:** Display the configured retry limit

Exact stored body:

```text
Bounded slice
Display the configured retry limit by performing a pure current read of the configured value.

Work-unit form
Vertical read-only behavior slice from the current retry-limit read seam to the display output.

Source Trace
Parent: P-N02
Source: SRC-N02@1
Owner: Dae, jobs owner
Authorized design: R52
Commitment: C2 display the configured retry limit
Acceptance pointer: display is a pure current read of the configured retry limit
Proof pointer: retry_display fixtures

Desired behavior and acceptance
- For every supported configured retry-limit value in retry_display, the display shows that current value exactly.
- Each display read observes the current configured value rather than a cached, migrated, inferred, or hard-coded value.
- Rendering the value performs no durable write and does not change the configured retry limit or scheduled-job state.
- If the current read reports that no supported value is available or returns an error, the display path preserves that read outcome and does not invent or persist a fallback value.
- retry_display passes the normal, changed-current-value, unavailable-value, and read-error fixtures.

Edge and error behavior
Zero and other supported boundary values are displayed as configured. A changed value is visible on the next read. Unavailable or failed current reads do not surface a stale or fabricated value and do not write state.

Relevant seams
Current retry-limit read interface; display formatting/render seam; retry_display fixtures.

Expected durable write scope
None. This slice is a pure read and display path.

Scope fence
In scope: reading and displaying the current configured retry limit and preserving unavailable/error outcomes. Out of scope: job migration, configuration editing, defaults or new product policy, caching, unrelated UI mockups, broad helper renames, and tracker transport examples.

Dependency state
True blockers: none.
Stable tracker order: 2.

Proof lane
Run retry_display fixtures with a normal value, supported boundary values, a changed current value, an unavailable value, and a read error; observe display output and assert no durable writes.

Verification authority
Dae, as jobs owner and source-meaning authority for SRC-N02@1 and R52, verifies the fixture evidence against the stated acceptance.

Verification evidence
A passing retry_display result showing exact current values, next-read visibility after a value change, preserved unavailable/error outcomes, and a zero-write assertion for every case.

Parallel-safety judgment
Parallel-safe with FT-N02-01. This ticket has no production writes, uses the distinct retry_display proof resource, does not consume a migration outcome, and shares no scarce proof resource. Its read-only implementation must retain the stated scope fence.

State-boundary matrix
Not applicable: this is a stateless pure-current-read display slice with no persistent state or lifecycle transition. Supported current values and unavailable/error read outcomes are covered as read fixtures rather than state transitions.
```

## Coverage map

| Source element | Disposition |
| --- | --- |
| Outcome: migrate scheduled jobs to schema v2 | `FT-N02-01` |
| Outcome: display retry limit | `FT-N02-02` |
| C1 restart-safe v1-to-v2 migration with rollback proof | `FT-N02-01` |
| C2 retry-limit display | `FT-N02-02` |
| Absent, current, incompatible, interruption, restart, rollback, and guarded-removal acceptance | `FT-N02-01` acceptance, proof lane, and state matrix |
| Pure current-read display acceptance | `FT-N02-02` acceptance and proof lane |
| Job migration scope | `FT-N02-01` |
| Retry-limit display scope | `FT-N02-02` |
| Unsettled product changes | Explicitly excluded from both tickets |
| Team formed in 2019 | No ticket: historical context creates no implementation commitment |
| Three abandoned UI mockups | No ticket: explicitly abandoned material creates no commitment |
| Suggestion to rename every helper | No ticket: participant suggestion is unsettled and outside source scope |
| Meeting greetings | No ticket: non-decision conversational material |
| Example tracker HTTP commands | No ticket: appendix transport examples do not change source commitments or tracker contract |

Every source-visible commitment and boundary has a ticket, exclusion, or no-ticket reason. No commitment is deferred.

## Dependency graph and ready frontier

```text
P-N02
├── 1. FT-N02-01  blockers: none
└── 2. FT-N02-02  blockers: none
```

There is no blocker edge: neither ticket consumes an outcome of the other. Migration serialization is an execution constraint, not a dependency. The observed ready frontier, in tracker order, is `[FT-N02-01, FT-N02-02]`; both items are open, ready-for-agent, unassigned, and have satisfied true blockers.

## Execution profiles

| Item | Semantic owner | Production writes | Proof seam / scarce resource | Ordering and serial tripwires | Independence |
| --- | --- | --- | --- | --- | --- |
| `FT-N02-01` | Dae / scheduled-job migration semantics | Job v2 records and restart checkpoint; guarded removal of old-read compatibility | `job_migration_matrix`; durable migration state, rollback, compatibility guard | Tracker order 1. Serial within expand-migrate-contract due migration, interruption, rollback, and removal boundaries. | Independent of the display slice, but serial-constrained internally. |
| `FT-N02-02` | Dae / retry-limit display semantics | None | `retry_display`; no scarce resource shared with migration proof | Tracker order 2. No serial tripwire while scope remains read-only. | Evidenced independent of migration; safe to run concurrently. |

## Frozen prepublication audit

The commitment ledger, both exact bodies, stable order, empty blocker graph, predicted frontier `[FT-N02-01, FT-N02-02]`, authorized `enhancement` roles, ready states, execution profiles, matrices, and intended mutations were complete and non-contradictory before the first create. Both bodies satisfied every fixture-tracker Ready-for-agent field. Publication scope was exactly the complete source-justified graph under `P-N02`.

## Mutation read-back

| Item | Exact body | Parent | Blockers / dependents | Role | Assignee | State |
| --- | --- | --- | --- | --- | --- | --- |
| `FT-N02-01` | Exact byte-for-byte body reproduced above | `P-N02` | none / none | `enhancement` | unassigned | `ready-for-agent` |
| `FT-N02-02` | Exact byte-for-byte body reproduced above | `P-N02` | none / none | `enhancement` | unassigned | `ready-for-agent` |

Read-back matched both stored titles and bodies exactly, both parent relationships, both roles, both unassigned values, both states, and the empty dependent sets. The resulting frontier matched the frozen prediction. There were no failed, unknown, ambiguous, or mismatched operations.

## Complete simulated operation log

1. `get_setup()` → compatible setup; tracker `fixture-tracker`; ready state `ready-for-agent`; authorized role `enhancement`.
2. `get_parent("P-N02")` → parent exists; source `SRC-N02@1`; no children.
3. `create_item(title="Migrate scheduled jobs to restart-safe schema v2", body=<exact FT-N02-01 body above>)` → success, `FT-N02-01`.
4. `create_item(title="Display the configured retry limit", body=<exact FT-N02-02 body above>)` → success, `FT-N02-02`.
5. `set_parent("FT-N02-01", "P-N02")` → success.
6. `set_parent("FT-N02-02", "P-N02")` → success.
7. `set_role("FT-N02-01", "enhancement")` → success.
8. `set_role("FT-N02-02", "enhancement")` → success.
9. `set_state("FT-N02-01", "ready-for-agent")` → success.
10. `set_state("FT-N02-02", "ready-for-agent")` → success.
11. `get_item("FT-N02-01")` → exact stored title and body above; parent `P-N02`; blockers none; role `enhancement`; assignee unassigned; state `ready-for-agent`.
12. `get_dependents("FT-N02-01")` → none.
13. `get_item("FT-N02-02")` → exact stored title and body above; parent `P-N02`; blockers none; role `enhancement`; assignee unassigned; state `ready-for-agent`.
14. `get_dependents("FT-N02-02")` → none.

No `set_blocker` operation was issued because the audited graph has no true blocker edge.

**Gaps:** none.

**Exact safe continuation:** Implement only a ready item under its stored scope and proof contract; begin with the first ready item in tracker order.

**Stopped recommendation:** `$implement`
