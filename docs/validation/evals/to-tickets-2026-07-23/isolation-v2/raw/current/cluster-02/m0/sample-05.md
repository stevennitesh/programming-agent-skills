# Published graph

## Evidence and publication boundary

- Result type: `published graph`
- Source: `SRC-N02@1`
- Source owner: Dae, jobs owner
- Parent: `P-N02`
- Authorized derived design: `R52`
- Evidence: the complete supplied source packet, compatible fixture setup, initial parent observation, `job_migration_matrix`, `retry_display`, and the mutation read-back below
- Mutation boundary: only the two source-justified fixture items and their parent, role, and state relationships changed
- Initial tracker state: `P-N02` existed with no children
- Observed final tracker state: `P-N02` has children `N02-1` and `N02-2` in that order; both are unassigned, have role `enhancement`, and are `ready-for-agent`
- Gaps: none

## Ordered items and exact stored bodies

### `N02-1` — Migrate scheduled jobs to restart-safe schema v2

```markdown
## Bounded slice
Migrate scheduled-job records from v1 to v2 through one restart-safe expand-migrate-contract work unit while keeping supported reads operable and proving rollback before the legacy read path is removed.

## Work-unit form
Stateful migration slice. Its internal stages are ordered: expand compatible reads and valid-v2 writes; migrate restart-safely; prove rollback and compatibility; contract the old read path only after old usage has ended.

## Source Trace
- Parent: P-N02
- Source: SRC-N02@1
- Owner: Dae, jobs owner
- Authorized design: R52
- Commitment: C1
- Acceptance source: absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior
- Proof seam: job_migration_matrix

## Desired behavior and observable acceptance
- Absent/initial: an absent job remains absent; migration succeeds as a no-op and creates no job or checkpoint residue.
- Current reusable state: a valid v2 job remains valid and readable, is not semantically rewritten, and repeated migration is idempotent.
- Legacy state: a supported v1 job remains readable during expansion and is converted to a schema-valid v2 job carrying the required timezone and retry-count data under R52; supported scheduled-job behavior is preserved as asserted by job_migration_matrix.
- Incompatible state: migration reports the matrix-defined incompatibility, writes no partial or invalid v2 record, and does not make supported reads inoperable.
- Interruption: after interruption at every matrix checkpoint, each committed job is readable as either the supported old form or valid v2, with no torn record.
- Restart: rerunning resumes safely, does not duplicate jobs or transformations, and converges to the same valid v2 result.
- Rollback: the rollback lane restores an operable supported read state from every releasable migration stage and passes before contraction is eligible.
- Guarded removal: the legacy read path is removed only after old usage is shown to have ended and compatibility plus rollback proof has passed; otherwise removal remains blocked.

## Seams and expected durable write scope
- Production seams: scheduled-job schema/version boundary, compatible read path, v2 write path, migration runner, and migration progress boundary.
- Expected durable writes: only selected scheduled-job records transformed to valid v2 and the migration progress needed for restart safety.
- No durable writes to retry-limit display state, unrelated job behavior, or unrelated records.

## Dependency state and tracker order
- True blockers: none.
- Stable tracker order: 1.
- The expand, migrate, proof, and contract stages are serial constraints inside this item, not tracker blocker edges.

## Proof
- Proof lane: job_migration_matrix exercises every supported state branch, interruption point, restart, rollback, and guarded contraction.
- Verification authority: the authorized R52 behavior owned by Dae and the job_migration_matrix fixture.
- Verification evidence required: passing fixture results identifying every matrix branch and interruption point, valid-v2 schema evidence, idempotent restart evidence, rollback evidence, and evidence that old usage ended before legacy-read removal.

## Parallel safety
Parallel-safe with N02-2: this item writes job records and migration progress and uses job_migration_matrix, while N02-2 is read-only and uses retry_display. This item's own expand-migrate-contract stages must remain serial because they share the schema trust boundary and rollback gate.

## Scope fence
In scope: C1, supported-read compatibility, valid-v2 writes, restart safety, rollback proof, and guarded legacy-read removal. Out of scope: retry-limit presentation, unrelated schema or product changes, abandoned mockups, broad helper renames, and implementation work outside scheduled-job migration.

## State-boundary matrix
| Branch | Required behavior | High-risk interaction |
|---|---|---|
| Absent/initial | No-op; create neither job nor residue | Restart after an empty scan remains a no-op |
| Current valid v2 | Reuse without semantic rewrite; remain readable | Repeated runs are idempotent |
| Legacy supported v1 | Remain readable during expansion; convert to valid v2 under R52 | Interruption at every releasable checkpoint and restart |
| Incompatible record | Report the defined incompatibility; no torn or invalid v2 write | Other supported reads remain operable |
| Public access paths | Compatible old/new reads remain operable until contraction | Mixed v1/v2 population during migration |
| Supported variants | Exactly the variants enumerated by job_migration_matrix | Each variant preserves supported behavior |
| Rollback transition | Restore an operable supported read state | Must pass before contraction |
| Contract transition | Remove old reads only after old usage ends and compatibility and rollback proof pass | Premature removal remains blocked |
```

### `N02-2` — Display the configured retry limit

```markdown
## Bounded slice
Display the configured retry limit from the current scheduled-job read model as one pure-read behavior slice.

## Work-unit form
Stateless vertical behavior slice.

## Source Trace
- Parent: P-N02
- Source: SRC-N02@1
- Owner: Dae, jobs owner
- Authorized design: R52
- Commitment: C2
- Acceptance source: display is a pure current read of the configured retry limit
- Proof seam: retry_display

## Desired behavior and observable acceptance
- For every supported current configured retry-limit value, including zero and boundary values represented by retry_display, the displayed value exactly matches the current configured value.
- Reading and rendering the retry limit performs no migration, defaulting write, normalization write, or other durable mutation.
- A missing or invalid current value follows the existing read error behavior asserted by retry_display and never silently substitutes or persists a different value.
- Repeated display reads return the current value and do not accumulate state.

## Seams and expected durable write scope
- Production seams: current scheduled-job retry-limit read boundary and retry-limit display boundary.
- Expected durable writes: none; this item is pure read and presentation.

## Dependency state and tracker order
- True blockers: none.
- Stable tracker order: 2.

## Proof
- Proof lane: retry_display.
- Verification authority: the authorized R52 behavior owned by Dae and the retry_display fixture.
- Verification evidence required: passing fixture results for supported values, zero and represented boundaries, missing/invalid read behavior, exact displayed value, and absence of writes.

## Parallel safety
Parallel-safe with N02-1: this item has no production writes and uses retry_display; N02-1 writes only job migration state and uses job_migration_matrix. No scarce proof resource or true dependency is shared.

## Scope fence
In scope: C2 and current configured retry-limit read and display behavior. Out of scope: job migration, changing retry-limit configuration, adding defaults, abandoned UI mockups, broad helper renames, and unsettled product changes.

## State-boundary matrix
Not applicable: this is a stateless pure-current-read display slice with no durable state or lifecycle transition. Supported value and read-error branches are covered by observable acceptance and retry_display.
```

## Coverage map

| Source material | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `N02-1` |
| C1 restart-safe v1-to-v2 migration with rollback proof | `N02-1` |
| Acceptance: absent, current, incompatible, interruption, restart, rollback, guarded removal | `N02-1` acceptance and state matrix |
| Outcome/C2: display configured retry limit | `N02-2` |
| Acceptance: pure current retry-limit read | `N02-2` |
| Scope: job migration and retry-limit display | Exhausted by `N02-1` and `N02-2` |
| Exclusion: unsettled product changes | Explicit scope fences; no ticket |
| Team formed in 2019 | Historical context with no implementation commitment; no ticket |
| Three abandoned UI mockups | Explicitly abandoned material; no ticket |
| Suggestion to rename every helper | Unsettled suggestion outside authorized outcome; no ticket |
| Meeting greetings | Non-decision conversational material; no ticket |
| Example tracker HTTP commands | Procedural examples, not source behavior; no ticket |

Every source-visible commitment and scope boundary has a ticket, exclusion, or no-ticket reason.

## Dependency graph, readiness, and frontier

- Stable order: `N02-1`, `N02-2`
- Blocker edges: none
- Cycles or contradictory order: none
- Both items pass the fixture Ready-for-agent contract: bounded slice, Source Trace, edge/error acceptance, dependency state, proof lane, durable write scope, parallel-safety judgment, scope fence, work-unit form, verification authority, and verification evidence are present.
- Ready frontier: [`N02-1`, `N02-2`]. Both are open, ready-for-agent, unassigned, and have no unsatisfied true blocker.

## Execution profiles

| Item | Semantic owner | Production writes | Proof seam / scarce resource | Ordering and serial tripwires | Independence judgment |
|---|---|---|---|---|---|
| `N02-1` | Dae / R52 scheduled-job migration semantics | Selected job records to v2 and restart progress | job_migration_matrix; schema trust boundary and rollback gate are scarce inside the item | Expand → migrate → prove rollback/compatibility → contract; interruption, mixed-version reads, rollback, and removal gate force internal serialization | May execute alongside `N02-2`; must serialize its own migration stages |
| `N02-2` | Dae / R52 retry-limit display semantics | None | retry_display; no shared scarce proof resource | Pure current read; no migration or lifecycle ordering | Evidenced independent of `N02-1` |

## Mutation read-back

- `get_item(N02-1)` returned the exact stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, and tracker order 1.
- `get_item(N02-2)` returned the exact stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, and tracker order 2.
- `get_item(P-N02)` returned ordered children [`N02-1`, `N02-2`] and otherwise unchanged parent intent.
- `get_dependents(N02-1)` returned `[]`.
- `get_dependents(N02-2)` returned `[]`.
- The observed frontier matches the predicted frontier: [`N02-1`, `N02-2`].

## Complete simulated operation log

| # | Operation | Input | Observation |
|---:|---|---|---|
| 1 | `get_setup` | fixture-tracker | Compatible setup; Ready-for-agent contract, `enhancement` role, and `ready-for-agent` state available |
| 2 | `get_parent` | `P-N02` | Exists, no children; source `SRC-N02@1`; derived design R52 authorized |
| 3 | `create_item` | Title `Migrate scheduled jobs to restart-safe schema v2`; body = exact `N02-1` stored body above | Success; fixture ID `N02-1`; created unassigned |
| 4 | `create_item` | Title `Display the configured retry limit`; body = exact `N02-2` stored body above | Success; fixture ID `N02-2`; created unassigned |
| 5 | `set_parent` | item `N02-1`, parent `P-N02` | Success |
| 6 | `set_parent` | item `N02-2`, parent `P-N02` | Success |
| 7 | `set_role` | item `N02-1`, role `enhancement` | Success |
| 8 | `set_role` | item `N02-2`, role `enhancement` | Success |
| 9 | `set_state` | item `N02-1`, state `ready-for-agent` | Success |
| 10 | `set_state` | item `N02-2`, state `ready-for-agent` | Success |
| 11 | `get_item` | `N02-1` | Exact body above; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; order 1 |
| 12 | `get_item` | `N02-2` | Exact body above; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; order 2 |
| 13 | `get_item` | `P-N02` | Ordered children [`N02-1`, `N02-2`]; parent intent otherwise unchanged |
| 14 | `get_dependents` | `N02-1` | `[]` |
| 15 | `get_dependents` | `N02-2` | `[]` |

No `set_blocker` operation occurred because no dependent consumes a required predecessor outcome.

## Stopped recommendation

Recommendation: `none`.

The request authorized shaping and simulated publication, not top-level parent delivery. No implementation owner is invoked.
