# Published graph

## Result identity

- Type: `published graph`
- Source: `SRC-N02@1`
- Source owner: `Dae, jobs owner`
- Parent: `P-N02`
- Approved proposal revision: `R52`
- Tracker: `fixture-tracker`
- Tracker state before publication: setup compatible; `P-N02` existed with no children
- Publication scope: the complete source-justified graph only
- Correlation identities:
  - Proposal: `to-tickets:SRC-N02@1:R52`
  - Ticket 1: `to-tickets:SRC-N02@1:R52:01`
  - Ticket 2: `to-tickets:SRC-N02@1:R52:02`
- Tracker state after publication: `P-N02` has two exact, ready-for-agent enhancement children; no blocker relationships
- Gaps: none

## Source Trace summary

`SRC-N02@1`, owned by Dae, commits to migrating scheduled jobs to schema v2 and displaying the configured retry limit. The accepted proof must cover absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior, while the display remains a pure current read. The proof seams are `job_migration_matrix` and `retry_display` fixtures. Derived design `R52` is the complete design explicitly reviewed and authorized by the source owner. Scope is job migration and retry-limit display; unsettled product changes remain excluded.

The notes about the team's formation year, abandoned mockups, greetings, a suggested wholesale helper rename, and example tracker HTTP commands create no implementation commitment and are omitted from ticket scope.

## Coverage map

| Source element | Disposition |
|---|---|
| C1: restart-safe v1-to-v2 migration with rollback proof | `FI-N02-01` |
| C2: display configured retry limit | `FI-N02-02` |
| Absent, current, incompatible, interruption, restart, rollback, guarded-removal acceptance | `FI-N02-01` acceptance and state matrix |
| Pure current read acceptance | `FI-N02-02` acceptance |
| `job_migration_matrix` proof seam | `FI-N02-01` |
| `retry_display` proof seam | `FI-N02-02` |
| Unsettled product changes | Explicitly excluded from both tickets |
| Team history, abandoned mockups, greetings, helper-renaming suggestion, example HTTP commands | No ticket: non-decision-bearing context |

Every source-visible commitment and scope boundary has a disposition.

## Ordered items and exact stored bodies

### `FI-N02-01`

```text
Title: Migrate scheduled jobs from schema v1 to restart-safe schema v2
Correlation: to-tickets:SRC-N02@1:R52:01
Work-unit form: stateful migration behavior slice using expand-migrate-contract
Source Trace: SRC-N02@1; owner Dae; commitment C1; acceptance for absent, current, incompatible, interruption, restart, rollback, and guarded removal; proof seam job_migration_matrix; approved derived design R52; parent P-N02.
Desired behavior: Expand supported job handling so v1 records without timezone remain readable while migration writes valid v2 records containing timezone and retry count. Migrate through an operable, releasable, restart-safe stage. A rerun after interruption resumes without corrupting or duplicating completed work. Preserve a proven rollback path. Remove old-read support only after migration completion, rollback proof, and compatibility proof establish that old usage has ended.
Acceptance:
- Absent/initial: no scheduled-job record is a successful no-op and creates no malformed state.
- Current reusable: an already-valid v2 record remains valid and is not destructively rewritten.
- Legacy/incompatible: a v1 record with no timezone stays readable during expansion and is converted to a valid v2 record with the required timezone and retry-count fields.
- Interruption: a failure after a partial batch leaves previously completed records valid and remaining records recoverable.
- Restart: rerunning from interrupted state resumes safely and converges on the same valid v2 result without duplicate effects.
- Rollback: fixture evidence demonstrates an operable rollback path before contraction is eligible.
- Guarded removal: old-read support cannot be removed until no v1 usage remains and migration, compatibility, and rollback proof all pass.
- Error behavior: an invalid or nonconvertible record is reported without silently fabricating v2 values or corrupting other records.
Relevant seams: scheduled-job schema reader/writer and migration runner; job_migration_matrix fixture.
Expected durable write scope: scheduled-job schema/migration production code and persisted scheduled-job records converted from v1 to v2; no UI writes.
Scope fence: Includes only compatibility expansion, migration/resume behavior, rollback proof, and guarded contraction required by C1. Excludes retry-limit display, unrelated schema or product changes, wholesale helper renaming, abandoned UI mockups, and tracker HTTP examples.
Dependency state: blockers none.
Stable tracker order: 1.
Proof lane: job_migration_matrix exercises each supported state branch, interruption/restart convergence, invalid-record isolation, rollback, and the contraction guard.
Verification authority: Dae's accepted SRC-N02@1 acceptance and authorized design R52.
Verification evidence: passing job_migration_matrix fixture results for absent, current-v2, v1-without-timezone, invalid, partial/interrupted, restarted, rollback, and old-read-removal-guard cases, including persisted-record assertions.
Parallel safety: Serial tripwire. This slice mutates persisted scheduled-job state, crosses a compatibility boundary, and owns migration/cutover/rollback proof. Run it serially with any other work that writes the job schema, migration state, or job_migration_matrix proof resource. It is independent of FI-N02-02 because that item only reads current retry-limit state and uses a separate proof fixture.
Role: enhancement
State: ready-for-agent
Parent: P-N02
```

### `FI-N02-02`

```text
Title: Display the configured retry limit for a scheduled job
Correlation: to-tickets:SRC-N02@1:R52:02
Work-unit form: stateless vertical display behavior slice
Source Trace: SRC-N02@1; owner Dae; commitment C2; acceptance requiring a pure current read of the configured retry limit; proof seam retry_display; approved derived design R52; parent P-N02.
Desired behavior: Display the scheduled job's currently configured retry limit by reading the current value without mutating job configuration or persisted job state.
Acceptance:
- A current configured retry limit is rendered exactly as supplied by the current read.
- A zero retry limit is displayed as zero rather than treated as absent.
- If the current read supplies no retry limit or returns an error, the display follows the existing non-mutating unavailable/error path and does not invent a value.
- Reading or rendering the display performs no durable write and does not trigger migration.
Relevant seams: current scheduled-job retry-limit read model and display renderer; retry_display fixture.
Expected durable write scope: display/read-model production code only; no persisted data, schema, migration, or configuration writes.
Scope fence: Includes only the current retry-limit read and display behavior required by C2. Excludes job migration, changing the retry limit, new product behavior, unrelated UI redesign, abandoned mockups, and wholesale helper renaming.
Dependency state: blockers none.
Stable tracker order: 2.
Proof lane: retry_display fixtures cover a configured positive value, zero, missing value, and read error while asserting no mutation.
Verification authority: Dae's accepted SRC-N02@1 acceptance and authorized design R52.
Verification evidence: passing retry_display fixture results with exact rendered-value assertions and no-write/no-migration assertions for positive, zero, missing, and error cases.
Parallel safety: Safe to run in parallel with FI-N02-01 when the worker confines writes to the display/read-model seam and uses only retry_display. It neither writes migration state nor consumes a migration outcome. Serialize if implementation discovery reveals writes to the job schema, migration state, or job_migration_matrix resource.
Role: enhancement
State: ready-for-agent
Parent: P-N02
```

## Dependency graph and frontier

```text
FI-N02-01   blockers: none
FI-N02-02   blockers: none
```

No blocker edge is justified: the display consumes the current configured retry-limit read, not a migration outcome. Tracker order is not a blocker.

Predicted frontier before mutation: none, because the items did not yet exist.

Observed ready frontier after read-back, in tracker order:

1. `FI-N02-01`
2. `FI-N02-02`

Both items are open, `ready-for-agent`, unclaimed, and have satisfied true blockers.

## Execution profiles

| Item | Semantic ownership | Production writes | Proof seam / scarce resource | Ordering and serial tripwires | Independence judgment |
|---|---|---|---|---|---|
| `FI-N02-01` | Scheduled-job schema migration semantics under Dae's source authority | Migration/schema code and persisted scheduled-job records | `job_migration_matrix`; migration/cutover/rollback state | First in stable tracker order. Serial with job-schema writers, migration operators, cutover, rollback, or the same matrix resource. | Independent of `FI-N02-02`; no blocker edge. |
| `FI-N02-02` | Retry-limit current-read display semantics under Dae's source authority | Display/read-model code only; no durable state | `retry_display` | Second in stable tracker order. No inherent serial constraint; stop and serialize if schema or migration writes are discovered. | Evidenced parallel-safe with `FI-N02-01` under its scope fence; no blocker edge. |

## State-boundary matrices

### `FI-N02-01` — stateful

| Supported branch / interaction | Required behavior | Proof |
|---|---|---|
| Absent/initial | Successful no-op; no malformed record created | `job_migration_matrix`: absent |
| Current reusable v2 | Preserve valid v2 state without destructive rewrite | `job_migration_matrix`: current-v2 |
| Legacy/incompatible v1 without timezone | Keep reads operable during expansion; convert to valid v2 with timezone and retry count | `job_migration_matrix`: legacy-v1 |
| Invalid/nonconvertible legacy state | Report the record; do not fabricate values or corrupt unrelated records | `job_migration_matrix`: invalid |
| Public access during migration | Supported reads handle v1 and v2 until guarded contraction | `job_migration_matrix`: mixed-read compatibility |
| Partial/interrupted migration | Completed records remain valid; remaining records remain recoverable | `job_migration_matrix`: interrupted |
| Restart after interruption | Resume idempotently and converge without duplicate effects | `job_migration_matrix`: restart |
| Rollback transition | Demonstrate an operable rollback before contraction | `job_migration_matrix`: rollback |
| Contract/removal transition | Remove v1 reads only after no old usage remains and migration, compatibility, and rollback proof pass | `job_migration_matrix`: guarded removal |

Lifecycle: compatible expansion → mixed v1/v2 operable migration → interruption/restart as needed → completed v2 plus rollback proof → guarded contraction after old usage ends.

### `FI-N02-02` — stateless

Not applicable. The slice is a pure current read and render, performs no durable write, and has no lifecycle transition. Its distinct input branches—positive configured value, zero, missing value, and read error—are covered in acceptance and `retry_display` evidence.

## Mutation read-back

- `get_item(FI-N02-01)` returned the exact `FI-N02-01` stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, blockers `[]`, and correlation `to-tickets:SRC-N02@1:R52:01`.
- `get_item(FI-N02-02)` returned the exact `FI-N02-02` stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, blockers `[]`, and correlation `to-tickets:SRC-N02@1:R52:02`.
- `get_dependents(FI-N02-01)` returned `[]`.
- `get_dependents(FI-N02-02)` returned `[]`.
- Exact body, parent, authorized role, state, assignee, blocker state, correlation identity, and resulting frontier all matched approved revision `R52`.
- Failed or unknown operations: none.
- Affected dependents: none.

## Complete simulated operation log

| # | Operation | Arguments | Observation |
|---:|---|---|---|
| 1 | `get_setup` | tracker `fixture-tracker` | Compatible setup; Ready-for-agent contract, `enhancement` role, and `ready-for-agent` state available. |
| 2 | `get_parent` | `P-N02` | Parent exists with no children; source identity `SRC-N02@1` and publication authority are consistent with approved revision `R52`. |
| 3 | `create_item` | correlation `to-tickets:SRC-N02@1:R52:01`; exact `FI-N02-01` body reproduced above | Success; returned `FI-N02-01`. |
| 4 | `create_item` | correlation `to-tickets:SRC-N02@1:R52:02`; exact `FI-N02-02` body reproduced above | Success; returned `FI-N02-02`. |
| 5 | `set_parent` | item `FI-N02-01`; parent `P-N02` | Success. |
| 6 | `set_parent` | item `FI-N02-02`; parent `P-N02` | Success. |
| 7 | `set_role` | item `FI-N02-01`; role `enhancement` | Success. |
| 8 | `set_role` | item `FI-N02-02`; role `enhancement` | Success. |
| 9 | `set_state` | item `FI-N02-01`; state `ready-for-agent` | Success. |
| 10 | `set_state` | item `FI-N02-02`; state `ready-for-agent` | Success. |
| 11 | `get_item` | `FI-N02-01` | Exact stored body and metadata matched; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; blockers `[]`. |
| 12 | `get_item` | `FI-N02-02` | Exact stored body and metadata matched; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; blockers `[]`. |
| 13 | `get_dependents` | `FI-N02-01` | `[]`. |
| 14 | `get_dependents` | `FI-N02-02` | `[]`. |

No `set_blocker` operation was issued because no true dependency exists. No unavailable operation was invoked. The source, revision, tracker target, and parent were reconciled immediately before the first mutation.

## Safe continuation

Recommendation: `$parallel-implement`

Stop without invoking it.
