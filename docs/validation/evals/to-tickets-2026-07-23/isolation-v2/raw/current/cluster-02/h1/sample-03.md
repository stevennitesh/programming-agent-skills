# Published graph

## Publication identity

- Result type: `published graph`
- Source: `SRC-N02@1`
- Source owner: `Dae, jobs owner`
- Parent: `P-N02`
- Approved proposal revision: `R52`
- Tracker: `fixture-tracker`
- Setup evidence: compatible setup returned by `get_setup`
- Parent evidence: `get_parent(P-N02)` returned the existing parent with no children
- Publication authority: Dae authorized complete derived design `R52`; publication was limited to the complete source-justified graph
- Mutation boundary: only the exact simulated tracker graph changed
- Initial tracker state: `P-N02` existed with no children
- Final tracker state: `P-N02` has children `FT-N02-01` and `FT-N02-02`; both have role `enhancement`, state `ready-for-agent`, no assignee, and no blockers

## Source Trace summary

`SRC-N02@1`, owned by Dae, requires scheduled jobs to migrate to schema v2 and the configured retry limit to be displayed. The accepted commitments are C1, restart-safe v1-to-v2 migration with rollback proof, and C2, a pure current read that displays the configured retry limit. The authorized proof seams are `job_migration_matrix` and `retry_display` fixtures. Scope is job migration and retry-limit display. Unsettled product changes are excluded. The exact source-authorized proposal is `R52`.

## Complete coverage map

| Source material | Disposition |
|---|---|
| C1: migrate v1 jobs to restart-safe v2 with rollback proof | `FT-N02-01` |
| C1 acceptance: absent state | `FT-N02-01` acceptance and state matrix |
| C1 acceptance: current reusable state | `FT-N02-01` acceptance and state matrix |
| C1 acceptance: incompatible state | `FT-N02-01` acceptance and state matrix |
| C1 acceptance: interruption and restart | `FT-N02-01` acceptance and state matrix |
| C1 acceptance: rollback | `FT-N02-01` acceptance and state matrix |
| C1 acceptance: guarded removal of old reads | `FT-N02-01` acceptance and state matrix |
| C2: display configured retry limit | `FT-N02-02` |
| C2 acceptance: pure current read | `FT-N02-02` acceptance |
| Scope boundary: job migration and retry-limit display | Enforced by both ticket scope fences |
| Exclusion: unsettled product changes | Explicitly excluded by both ticket scope fences |
| Team formed in 2019 | No ticket: historical context does not express an implementation commitment |
| Three abandoned UI mockups | No ticket: abandoned material is not accepted design or scope |
| Suggestion to rename every helper | No ticket: participant suggestion is unsettled and excluded |
| Meeting greetings | No ticket: no implementation commitment |
| Appendix example tracker HTTP commands | No ticket: transport examples are not product scope and do not authorize live operations |

Every source-visible commitment and scope boundary has a ticket, exclusion, or no-ticket reason. There are no unresolved commitment-changing decisions.

## Exact stored item bodies

### `FT-N02-01`

```markdown
# Migrate scheduled jobs from schema v1 to v2

Work-unit form: migration behavior slice using expand-migrate-contract.

Source Trace: SRC-N02@1 (owner: Dae, jobs owner), commitment C1, authorized derived design R52, parent P-N02. Proof seam: job_migration_matrix.

Desired behavior: Keep supported v1 and v2 job reads operable while new writes produce valid v2 records, migrate legacy v1 jobs to valid v2 using R52's source-authorized conversion rule, resume safely after interruption, prove rollback, and remove old-read compatibility only after migration and rollback proof satisfy the guard.

Acceptance:
- Absent/initial: with no scheduled-job record, migration is a successful no-op and creates no phantom record.
- Current reusable: a valid v2 record, including timezone and retry count, remains valid and is not destructively rewritten when the migration is rerun.
- Legacy: a supported v1 record with no timezone remains readable during expansion and is converted once to a valid v2 record under R52's authorized conversion rule.
- Incompatible: an unsupported or malformed record is reported without being partially rewritten, and supported reads remain operable.
- Interruption: interruption at every durable migration boundary leaves a recoverable state and does not authorize contraction.
- Restart: restarting from each interrupted state resumes from durable progress, does not duplicate or corrupt a job, and reaches the same valid v2 result as an uninterrupted run.
- Rollback: before contraction, rollback proof restores or preserves an operable supported-read state for every migrated case.
- Guarded removal: old v1 reads cannot be removed until all supported records are migrated, restart proof passes, and rollback proof passes; once those conditions hold, contraction removes only the obsolete v1-read path and v2 reads and writes remain operable.

Edge/error behavior: Empty input is a no-op; already-current v2 input is idempotent; malformed or unsupported input fails closed without partial conversion; interrupted runs remain restartable; a failed migration or rollback check keeps compatibility reads and blocks contraction.

State-boundary matrix:
| Branch | Required behavior |
|---|---|
| Absent/initial | No record is created; no-op succeeds. |
| Current reusable v2 | Reuse the valid v2 state without destructive rewrite; rerun is idempotent. |
| Legacy v1 | Expansion reads v1 and v2 while writers emit valid v2; migration converts by R52's authorized rule. |
| Incompatible/malformed | Report the incompatibility, preserve the record, and do not contract. |
| Interrupted migration | Preserve durable progress and resume without duplicate or corrupt writes. |
| Rollback | Retain compatibility reads and prove an operable recovery before contraction. |
| Contracted | Permit only after migration, restart, and rollback guards pass; v2 remains operable. |
Public access paths: scheduled-job read path, scheduled-job write path, and authorized migration entry point. Supported variants: schema v1 during expansion/migration and schema v2 throughout and after contraction. Lifecycle: absent or v1 -> expanded compatibility -> migrating/interrupted/restarted -> migrated v2 -> rollback-proven -> contracted v2.

Dependency state: no true blockers.

Proof lane: Run the job_migration_matrix fixture across absent, valid v2, legacy v1, incompatible, interruption, restart, rollback, pre-guard contraction refusal, and post-guard contraction cases.

Verification authority: SRC-N02@1 acceptance and authorized design R52, as exercised by job_migration_matrix.

Verification evidence: Passing fixture results for every matrix branch, including durable-boundary interruption/restart equivalence, rollback operability, and contraction guard refusal/success.

Expected durable write scope: schema compatibility reader, v2 job writer, migration/checkpoint logic, contraction guard, and scheduled-job records transformed by the migration. No UI or retry-display writes.

Parallel-safety judgment: Serial within this ticket. Expansion must precede migration, and contraction must follow complete migration plus restart and rollback proof. Migration checkpoints, job records, compatibility reads, rollback, and cutover are shared scarce state/proof resources.

Scope fence: Only schema-v2 compatibility, migration, restart, rollback, and guarded old-read removal for scheduled jobs. Do not change retry-limit display, invent product behavior, redesign scheduling, rename unrelated helpers, revive abandoned mockups, or perform unrelated cleanup.
```

Stored metadata:

- Correlation identity: `R52:SRC-N02@1:T01`
- Parent: `P-N02`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: `none`
- Blockers: `none`
- Tracker order: `1`

### `FT-N02-02`

```markdown
# Display the configured retry limit

Work-unit form: independently completable vertical behavior slice.

Source Trace: SRC-N02@1 (owner: Dae, jobs owner), commitment C2, authorized derived design R52, parent P-N02. Proof seam: retry_display.

Desired behavior: Display the configured retry limit by performing a pure current read of the configured retry-count value.

Acceptance:
- Given a current valid configured retry limit, the displayed value exactly matches the current configured value.
- Refreshing or rendering again reads the current value and does not retain or display a stale prior value.
- The display path performs no write, migration, normalization, defaulting, or other mutation.
- A missing, malformed, or failed current read follows the existing read-error path and does not fabricate a limit or mutate configuration.

Edge/error behavior: Zero and other valid configured boundary values are displayed exactly; repeated reads remain pure; missing, malformed, or failed reads expose the existing error behavior without a write or invented fallback.

State-boundary matrix: not applicable. This slice is a stateless presentation of a pure current read and owns no durable state transition.

Dependency state: no true blockers. Current schema v2 already stores retry count, and this slice does not consume the migration outcome.

Proof lane: Run the retry_display fixture for current value, refresh/change, valid boundaries, missing value, malformed value, and read failure while asserting zero durable writes.

Verification authority: SRC-N02@1 acceptance and authorized design R52, as exercised by retry_display.

Verification evidence: Passing retry_display fixture results showing exact current values, no stale values, existing error behavior, and no writes.

Expected durable write scope: retry-limit display/presentation code and its fixture only. No schema, migration, scheduled-job record, configuration, or persistence writes.

Parallel-safety judgment: Safe to execute in parallel with FT-N02-01. Its expected production writes and retry_display proof resource are disjoint from migration state, compatibility reads, migration checkpoints, rollback, cutover, and job_migration_matrix.

Scope fence: Only display the configured retry limit through the existing current read. Do not change retry semantics or configuration, add product behavior, choose new UI designs, revive abandoned mockups, rename unrelated helpers, or modify migration behavior.
```

Stored metadata:

- Correlation identity: `R52:SRC-N02@1:T02`
- Parent: `P-N02`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: `none`
- Blockers: `none`
- Tracker order: `2`

## Dependency graph and observed frontier

There are no blocker edges: neither ticket consumes an outcome of the other. Tracker order is `FT-N02-01`, then `FT-N02-02`, but order is not a blocker.

```text
P-N02
├── FT-N02-01  (no blockers)
└── FT-N02-02  (no blockers)
```

Predicted frontier before publication: `FT-N02-01`, `FT-N02-02`.

Observed frontier after read-back: `FT-N02-01`, `FT-N02-02`. Both are open in `ready-for-agent`, unclaimed, and have no blockers.

## Execution profiles

| Order | Ticket | Semantic ownership | Expected production writes | Proof seams / scarce resources | Ordering and serial tripwires | Independence |
|---|---|---|---|---|---|---|
| 1 | `FT-N02-01` | Scheduled-job schema compatibility and migration behavior | Compatibility reader, v2 writer, migration/checkpoint logic, contraction guard, migrated job records | `job_migration_matrix`; job records, checkpoints, rollback and cutover are scarce shared resources | Expand -> migrate/restart -> rollback proof -> contract. Internally serial; contraction guard is a hard tripwire. | No blocker relative to `FT-N02-02`, but do not parallelize this ticket's internal migration stages. |
| 2 | `FT-N02-02` | Retry-limit current-read presentation | Display/presentation code only | `retry_display`; no shared migration proof resource | No migration ordering requirement; any discovered persistence write is a scope violation and serial-safety failure. | Evidenced parallel-safe with `FT-N02-01` through disjoint production writes and proof fixtures. |

The applicable migration state matrix is stored verbatim in `FT-N02-01`. `FT-N02-02` is stateless for this work and records why no state matrix applies.

## Correlation identities and creation safety

The fixture exposes neither provider-native `create_with_idempotency` nor `query_correlation`. Creation therefore used deterministic identities `R52:SRC-N02@1:T01` and `R52:SRC-N02@1:T02` in the exact item metadata. Both creates returned definite success, so no ambiguous-creation recovery or retry was needed.

## Mutation read-back

| Item | Exact body | Parent | Role | Assignee | State | Blockers | Dependents |
|---|---|---|---|---|---|---|---|
| `FT-N02-01` | Exactly matches the stored body reproduced above | `P-N02` | `enhancement` | `none` | `ready-for-agent` | `none` | `none` |
| `FT-N02-02` | Exactly matches the stored body reproduced above | `P-N02` | `enhancement` | `none` | `ready-for-agent` | `none` | `none` |

Every authorized mutation and affected relationship read back exactly. No operation failed, was unknown, or mismatched.

## Complete simulated operation log

1. `get_setup()` -> compatible `fixture-tracker` setup; Ready-for-agent contract, `enhancement` role, and `ready-for-agent` state available.
2. `get_parent("P-N02")` -> parent exists; source `SRC-N02@1`; no children.
3. `create_item(correlation="R52:SRC-N02@1:T01", body=<exact FT-N02-01 body above>, order=1)` -> success; created `FT-N02-01`; exact body and correlation stored.
4. `create_item(correlation="R52:SRC-N02@1:T02", body=<exact FT-N02-02 body above>, order=2)` -> success; created `FT-N02-02`; exact body and correlation stored.
5. `set_parent("FT-N02-01", "P-N02")` -> success.
6. `set_parent("FT-N02-02", "P-N02")` -> success.
7. `set_role("FT-N02-01", "enhancement")` -> success.
8. `set_role("FT-N02-02", "enhancement")` -> success.
9. `set_state("FT-N02-01", "ready-for-agent")` -> success.
10. `set_state("FT-N02-02", "ready-for-agent")` -> success.
11. `get_item("FT-N02-01")` -> exact stored body and metadata reproduced above; parent `P-N02`; role `enhancement`; assignee `none`; state `ready-for-agent`; blockers `none`; correlation `R52:SRC-N02@1:T01`; order `1`.
12. `get_dependents("FT-N02-01")` -> `none`.
13. `get_item("FT-N02-02")` -> exact stored body and metadata reproduced above; parent `P-N02`; role `enhancement`; assignee `none`; state `ready-for-agent`; blockers `none`; correlation `R52:SRC-N02@1:T02`; order `2`.
14. `get_dependents("FT-N02-02")` -> `none`.

## Stopped recommendation

Recommend exactly one next owner: `$implement` for first ready item `FT-N02-01`, because its expand-migrate-contract sequence contains migration, rollback, and cutover serial tripwires. Do not invoke it.
