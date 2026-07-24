# Published graph

## Publication result

- Type: `published graph`
- Evidence: `SRC-N02@1`; owner `Dae, jobs owner`; authorized derived design `R52`; compatible fixture-tracker setup; simulated mutation and read-back recorded below.
- Source/parent: `SRC-N02@1` / `P-N02`
- Observed tracker state: `P-N02` now has the two ordered children below. Both are unassigned, have role `enhancement`, are in `ready-for-agent`, and have no blocker edges.
- Gaps: none.
- Exact safe continuation: leave both ready items unclaimed; no implementation or dispatch was started.

## Ordered items and exact stored bodies

### 1. `FT-N02-01` — Migrate scheduled jobs from schema v1 to restart-safe v2

Exact stored body:

```markdown
## Bounded slice
Migrate scheduled-job records from schema v1 to valid schema v2 through an expand-migrate-contract sequence while supported reads remain operable. Preserve each job's effective schedule and configured retry count, make migration restart-safe, prove rollback, and remove old reads only after the compatibility guard passes.

## Work-unit form
Stateful migration behavior slice.

## Source Trace
- Source: SRC-N02@1
- Parent: P-N02
- Owner: Dae, jobs owner
- Authorized design: R52
- Commitment: C1
- Acceptance/proof: job_migration_matrix

## Desired behavior and acceptance
- Expand: supported reads accept both a legacy v1 job without a stored timezone and a current valid v2 job.
- Migrate: a legacy v1 job becomes a valid v2 job while retaining the same effective schedule and configured retry count.
- Current valid v2 records are reusable and are not semantically changed.
- An absent record set completes as a successful no-op.
- If migration is interrupted after any durable checkpoint, rerunning resumes from durable state without duplicate jobs, lost jobs, or divergent v2 values.
- Rollback proof restores an operable supported-read state without data loss before contraction is permitted.
- Contract: old v1 reads are removed only when no old usage remains and compatibility, restart, and rollback proof all pass; a failed guard leaves old reads enabled.
- Malformed or incompatible records fail closed with an attributable record error and are not partially rewritten.
- The job_migration_matrix is green for absent, current, legacy/incompatible, interruption, restart, rollback, and guarded-removal branches.

## Seams and durable write scope
- Seams: scheduled-job schema reader, migration checkpoint/runner, compatibility guard, rollback path, and job_migration_matrix.
- Expected durable writes: scheduled-job v2 records, migration checkpoints, and the guarded retirement of the v1 read path.
- Scope fence: no retry-limit UI, unrelated job behavior, helper renames, unsupported schema redesign, or other product change.

## Dependencies and order
- True blockers: none.
- Stable tracker order: 1.

## Proof lane
- Lane: job_migration_matrix.
- Verification authority: the fixture assertions for schema validity, effective-schedule and retry-count preservation, idempotent restart, rollback operability, and guarded removal.
- Verification evidence: a passing matrix covering every acceptance branch above, including a captured interruption/resume run and a failed-removal-guard run.

## Parallel safety
Not safe for parallel mutation with another migration, cutover, rollback, schema-reader change, or job-record writer. The expand, migrate, rollback-proof, and contract phases are serial. It may run in parallel with FT-N02-02 because that item has no durable writes and uses the separate retry_display proof fixture; stop and serialize if either item begins changing the other's seam or fixture.

## Execution profile
- Semantic owner: Dae, jobs owner.
- Production writes: v2 job records, migration checkpoints, compatibility reader/guard, rollback path, and eventual v1-read retirement.
- Proof seams/scarce resources: job_migration_matrix and mutable migration test state are exclusive to this work unit.
- Ordering: expand, then resumable migration, then rollback/compatibility proof, then guarded contract.
- Serial tripwires: shared schema-reader edits, live migration state, rollback/cutover activity, protected job data, failed compatibility proof, or uncertain record independence.
- Independence evidence: FT-N02-02 is read-only, has a distinct proof fixture, and does not consume a migration outcome.

## State-boundary matrix
| Branch | Required result |
|---|---|
| Absent/initial | No-op success; no records or checkpoints are fabricated. |
| Current reusable v2 | Read succeeds; rerun is idempotent and preserves valid values. |
| Legacy v1 without timezone | Compatible read remains operable; migration writes valid v2 while preserving effective schedule and retry count. |
| Malformed/incompatible | Attributable failure; no partial rewrite; old supported read remains available where applicable. |
| Interrupted migration | Durable checkpoint identifies completed work; no contraction occurs. |
| Restart after interruption | Resume safely; no duplicate, lost, or divergent records. |
| Rollback | Restore an operable supported-read state without data loss and prove it before contraction. |
| Public access paths | All supported scheduled-job reads remain operable during expansion and migration. |
| Supported variants | v1 and v2 during expansion/migration; v2 only after the guarded contract passes. |
| Guarded removal | Remove v1 reads only after old usage ends and compatibility, restart, and rollback proof pass; otherwise retain them. |
```

### 2. `FT-N02-02` — Display the current configured retry limit

Exact stored body:

```markdown
## Bounded slice
Display the configured retry limit using a pure current read.

## Work-unit form
Stateless vertical behavior slice.

## Source Trace
- Source: SRC-N02@1
- Parent: P-N02
- Owner: Dae, jobs owner
- Authorized design: R52
- Commitment: C2
- Acceptance/proof: retry_display fixtures

## Desired behavior and acceptance
- For every supported configured retry-limit value, including zero, the display shows that exact current value.
- After the configured value changes, the next read-backed display shows the new current value rather than a cached, derived, or migration-snapshot value.
- The display performs no write and does not mutate job or retry configuration.
- If the current read is absent or errors, no retry value is invented; the read result follows the established absent/error display path.
- The retry_display fixtures prove exact value rendering, zero, changed-current-value, absent, and read-error behavior.

## Seams and durable write scope
- Seams: current retry-limit reader, retry-limit presentation boundary, and retry_display fixtures.
- Expected durable writes: none.
- Scope fence: no migration logic, configuration editing, defaults, caching, schema changes, helper renames, or other product change.

## Dependencies and order
- True blockers: none.
- Stable tracker order: 2.

## Proof lane
- Lane: retry_display fixtures.
- Verification authority: fixture assertions at the current-read/presentation boundary.
- Verification evidence: passing fixtures for exact configured values, zero, a changed current value, absent data, and reader error, plus evidence that no write seam was called.

## Parallel safety
Safe to execute in parallel with FT-N02-01 because this slice is read-only, has no durable write overlap, consumes no migration outcome, and has a separate proof fixture. Stop and serialize if implementation starts changing the migration reader, job records, or job_migration_matrix.

## Execution profile
- Semantic owner: Dae, jobs owner.
- Production writes: presentation/read-path code only; no durable state writes.
- Proof seams/scarce resources: retry_display fixtures; no shared mutable migration proof resource.
- Ordering: independent; stable tracker order 2.
- Serial tripwires: touching migration/cutover code, changing persisted job data, sharing mutable migration fixtures, or discovering that the current reader is not independent.
- Independence evidence: pure current-read acceptance, zero durable writes, distinct retry_display proof, and no consumption of FT-N02-01 output.

## State-boundary matrix
Not applicable: this ticket is stateless and performs a pure current read with no durable state transition. Its distinct value, absent, and error branches are covered by observable acceptance and retry_display fixtures above.
```

## Coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to v2 | `FT-N02-01` |
| C1: restart-safe v1-to-v2 migration with rollback proof | `FT-N02-01` |
| Acceptance: absent, current, incompatible, interruption, restart, rollback, guarded removal | `FT-N02-01` and its state-boundary matrix |
| Outcome: display retry limit | `FT-N02-02` |
| C2: display configured retry limit | `FT-N02-02` |
| Acceptance: pure current read | `FT-N02-02` |
| Scope: job migration and retry-limit display | Exhausted by `FT-N02-01` and `FT-N02-02` |
| Exclusion: unsettled product changes | Explicit scope fence in both tickets; no ticket |
| Team formed in 2019 | Non-commitment historical note; no ticket |
| Three abandoned UI mockups | Abandoned material; no ticket |
| Suggested rename of every helper | Unaccepted suggestion and excluded product/implementation churn; no ticket |
| Meeting greetings | Non-decision meeting content; no ticket |
| Example tracker HTTP commands | Appendix examples, not source commitments; no ticket |

## Dependency graph and frontier

- Graph nodes in stable order: `FT-N02-01`, `FT-N02-02`.
- Blocker edges: none. Neither item consumes the other's outcome.
- Cycle/missing-edge/contradictory-order audit: none found.
- Ready frontier: [`FT-N02-01`, `FT-N02-02`]. Both are open, ready-for-agent, unassigned, and truly unblocked.
- Execution constraint: `FT-N02-01` is internally serial across expand-migrate-contract phases. The two tickets are parallel-safe only while the seam and fixture separation recorded in their execution profiles remains true.

## Mutation read-back

| Item | Exact body | Parent | Blockers | Role | Assignee | State | Dependents |
|---|---|---|---|---|---|---|---|
| `FT-N02-01` | Byte-for-byte equal to its fenced stored body above | `P-N02` | none | `enhancement` | unassigned | `ready-for-agent` | none |
| `FT-N02-02` | Byte-for-byte equal to its fenced stored body above | `P-N02` | none | `enhancement` | unassigned | `ready-for-agent` | none |

Parent read-back: `P-N02` retains source intent ownership and has ordered children [`FT-N02-01`, `FT-N02-02`]. No parent was fabricated.

## Complete simulated operation log

1. `get_setup()` → compatible setup; tracker `fixture-tracker`; ready state `ready-for-agent`; authorized role `enhancement`.
2. `get_parent("P-N02")` → parent exists, owner intent preserved, children `[]`.
3. `create_item(title="Migrate scheduled jobs from schema v1 to restart-safe v2", body=<the exact FT-N02-01 stored body reproduced above>, order=1)` → success, `FT-N02-01`.
4. `create_item(title="Display the current configured retry limit", body=<the exact FT-N02-02 stored body reproduced above>, order=2)` → success, `FT-N02-02`.
5. `set_parent("FT-N02-01", "P-N02")` → success.
6. `set_parent("FT-N02-02", "P-N02")` → success.
7. No `set_blocker` call was made: the audited graph has no true blocker edge.
8. `set_role("FT-N02-01", "enhancement")` → success.
9. `set_role("FT-N02-02", "enhancement")` → success.
10. `set_state("FT-N02-01", "ready-for-agent")` → success.
11. `set_state("FT-N02-02", "ready-for-agent")` → success.
12. `get_item("FT-N02-01")` → exact title and stored body above; parent `P-N02`; blockers none; role `enhancement`; assignee unassigned; state `ready-for-agent`; order 1.
13. `get_item("FT-N02-02")` → exact title and stored body above; parent `P-N02`; blockers none; role `enhancement`; assignee unassigned; state `ready-for-agent`; order 2.
14. `get_dependents("FT-N02-01")` → `[]`.
15. `get_dependents("FT-N02-02")` → `[]`.
16. `get_parent("P-N02")` → ordered children [`FT-N02-01`, `FT-N02-02`]; parent intent owner unchanged.

Applied operations: two creates, two parent links, two authorized roles, and two ready-state mappings. Failed or unknown operations: none. The observed frontier is [`FT-N02-01`, `FT-N02-02`].

## Stopped recommendation

`none`
