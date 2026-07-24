# Published graph

## Evidence and tracker state

- Result type: `published graph`
- Source: `SRC-N02@1`
- Source owner: Dae, jobs owner
- Parent: `P-N02`
- Authorized design: `R52`
- Setup evidence: `get_setup` observed a compatible `fixture-tracker` setup and the stated Ready-for-agent contract.
- Parent evidence: `get_parent(P-N02)` observed the existing parent with no children before publication.
- Publication authority: Dae authorized the complete derived design R52; the source authorizes the `enhancement` role.
- Observed tracker state after publication: `P-N02` has the two ordered children below. Both have role `enhancement`, state `ready-for-agent`, no assignee, and no blocker edges. No other tracker state changed.
- Gaps: none.

## Ordered ticket references

1. `FT-N02-1` — Migrate scheduled jobs to restart-safe schema v2
2. `FT-N02-2` — Display the configured retry limit

## Exact stored item bodies

### `FT-N02-1`

```markdown
# Migrate scheduled jobs to restart-safe schema v2

Parent: P-N02
Source Trace: SRC-N02@1; owner Dae, jobs owner; commitment C1; acceptance “prove absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior”; proof seam job_migration_matrix; authorized derived design R52.

Work-unit form: migration slice using expand-migrate-contract.

Desired behavior: Migrate scheduled-job records from schema v1 to valid schema v2 while supported reads remain operable. First expand compatible reads and v2 writes, then migrate records with durable restart progress, and contract old v1 reads only after migration completion, rollback proof, and compatibility proof establish that old usage has ended.

Acceptance:
- Absent/initial state: with no job record, the migration performs no record conversion, produces no malformed record, and remains safely repeatable.
- Current reusable state: a valid v2 record retains its timezone and retry count unchanged and is not remigrated destructively.
- Legacy/incompatible state: a v1 record with no timezone remains readable during expansion and migration, and conversion writes a valid v2 record with the R52-authorized compatible value rather than an invalid partial form.
- Interruption and restart: interruption at each durable migration boundary leaves supported reads operable; restart resumes from durable progress, does not duplicate or corrupt conversion, and converges on one valid v2 record.
- Rollback: before any old-read removal, job_migration_matrix demonstrates the authorized rollback path from each migrated stage and shows supported reads remain operable.
- Guarded removal: v1 reads are removed only after all old usage has ended and migration, rollback, and compatibility evidence passes; otherwise contraction is prevented.
- Error behavior: incompatible or invalid state that cannot be converted under R52 is reported without contracting old reads or writing a falsely valid v2 record.

State-boundary matrix:
| Branch | Required behavior and transition |
| --- | --- |
| Absent/initial | absent → unchanged absent; repeatable no-op |
| Current reusable | valid v2 → unchanged valid v2 |
| Legacy/incompatible | readable v1 without timezone → valid v2 through compatible expansion and migration |
| Interrupted migration | durable partial progress → operable supported read → resumed valid v2 |
| Rollback | expanded or migrated stage → authorized operable rollback, proven before contraction |
| Public access paths | every supported scheduled-job read stays operable during expansion and migration; old v1 read is removed only by the guarded contraction |
| Supported variants | absent, valid v2, v1 without timezone, interrupted migration, restart, rollback, and post-proof contraction |
| High-risk interactions | interruption during conversion, restart after a durable boundary, rollback before contraction, and attempted contraction while old usage or proof is incomplete |

Expected durable write scope: scheduled-job compatibility read/write path, durable migration progress, conversion of v1 job records to valid v2 records, and eventual removal of the old v1 read path after its guard passes.

Scope fence: Only scheduled-job schema-v2 compatibility, migration, restart progress, rollback proof, and guarded removal. Do not change retry-display behavior, introduce unsettled product behavior, rename unrelated helpers, revive abandoned mockups, or use appendix example tracker commands as implementation requirements.

Dependency state: true blockers: none. Stable tracker order: 1.

Proof lane: job_migration_matrix covers absent, current v2, v1 without timezone, interruption at durable boundaries, restart, rollback, incompatible/error state, and guarded old-read removal.

Verification authority: Dae’s accepted SRC-N02@1 behavior and authorized design R52.

Verification evidence: passing job_migration_matrix evidence for every matrix branch, including operable reads, valid v2 writes, restart convergence, rollback proof, and refusal to contract before the guard passes.

Parallel safety: Serial within this ticket across expand → migrate → contract. The contract stage is a serial tripwire because it removes a public compatibility path and must wait for old-usage, rollback, and compatibility evidence. It is independent of FT-N02-2 at the durable-write and proof-resource seams, so the two tickets may run in parallel.
```

### `FT-N02-2`

```markdown
# Display the configured retry limit

Parent: P-N02
Source Trace: SRC-N02@1; owner Dae, jobs owner; commitment C2; acceptance “display is a pure current read of the configured retry limit”; proof seam retry_display fixtures; authorized derived design R52.

Work-unit form: independently completable vertical behavior slice.

Desired behavior: Display the current configured retry limit by reading the existing configured retry-count value without mutating job or configuration state.

Acceptance:
- For every supported current configured retry-limit fixture, the displayed value exactly matches the configured retry count.
- Repeated display reads leave scheduled-job records, retry configuration, and migration progress unchanged.
- Edge/error behavior: when the current retry limit cannot be read as a valid configured value, the display path exposes the existing read failure and does not invent, persist, or derive a fallback value.

State-boundary matrix: not applicable. This is a stateless pure read of current configuration and creates no lifecycle transition.

Expected durable write scope: none.

Scope fence: Only read and display the configured retry limit. Do not migrate job records, mutate configuration, add fallback policy, make unsettled product changes, rename unrelated helpers, or revive abandoned mockups.

Dependency state: true blockers: none. Stable tracker order: 2.

Proof lane: retry_display fixtures cover exact current-value display, repeated-read purity, and invalid/unavailable current-read error behavior.

Verification authority: Dae’s accepted SRC-N02@1 behavior and authorized design R52.

Verification evidence: passing retry_display fixture evidence showing exact displayed values, no durable writes, and no invented fallback on read failure.

Parallel safety: Safe to run in parallel with FT-N02-1. It has no expected durable writes, uses the separate retry_display proof resource, consumes the already-current configured retry count rather than a migration outcome, and does not cross the migration trust boundary.
```

## Coverage map

| Source material | Disposition |
| --- | --- |
| Outcome: migrate scheduled jobs to schema v2 | `FT-N02-1` desired behavior and acceptance |
| Outcome: display retry limit | `FT-N02-2` desired behavior and acceptance |
| C1 restart-safe v1→v2 migration with rollback proof | `FT-N02-1` |
| C2 configured retry-limit display | `FT-N02-2` |
| Absent, current, incompatible, interruption, restart, rollback, guarded-removal acceptance | `FT-N02-1` state matrix, acceptance, and job_migration_matrix proof |
| Pure current retry-limit read | `FT-N02-2` acceptance and retry_display proof |
| Scope: job migration and retry-limit display | Exhausted by `FT-N02-1` and `FT-N02-2` |
| Exclusion: unsettled product changes | Explicit scope fence on both tickets; no ticket |
| Team formed in 2019 | Background fact with no implementation commitment; no ticket |
| Three abandoned UI mockups | Abandoned material, not a commitment; no ticket |
| Suggested renaming of every helper | Unaccepted suggestion and outside scope; no ticket |
| Meeting greetings | Non-decision conversational material; no ticket |
| Appendix example tracker HTTP commands | Example transport material, not product work; no ticket |

All source-visible commitments and boundaries have a ticket acceptance, exclusion, or no-ticket reason.

## Dependency graph and ready frontier

```text
P-N02
├── FT-N02-1  blockers: none
└── FT-N02-2  blockers: none
```

There is no blocker edge: `FT-N02-2` reads the retry count already present in current schema v2 and does not consume a result of `FT-N02-1`. The stable ready frontier is:

1. `FT-N02-1`
2. `FT-N02-2`

Both are open, ready-for-agent, and unclaimed. The internal expand → migrate → contract order in `FT-N02-1` is a serial constraint, not a tracker blocker edge.

## Execution profiles

| Ticket | Semantic ownership | Production writes | Proof seam / scarce resource | Ordering and serial tripwires | Independence |
| --- | --- | --- | --- | --- | --- |
| `FT-N02-1` | Scheduled-job schema compatibility and migration under Dae/R52 | Compatibility paths, migration progress, v1→v2 records, guarded old-read removal | job_migration_matrix; migration state and rollback/compatibility evidence are scarce | Strict internal expand → migrate → contract; contraction waits for old-usage end plus rollback and compatibility proof | Parallel with `FT-N02-2`; serialize all stages inside this ticket |
| `FT-N02-2` | Retry-limit current-read display under Dae/R52 | none | retry_display fixtures | Tracker order 2 only; no serial tripwire | Parallel with `FT-N02-1`; separate proof seam and no writes |

## Mutation read-back

- `get_item(FT-N02-1)` returned the exact first stored body above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, and blockers `[]`.
- `get_item(FT-N02-2)` returned the exact second stored body above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, assignee `none`, and blockers `[]`.
- `get_dependents(FT-N02-1)` returned `[]`.
- `get_dependents(FT-N02-2)` returned `[]`.
- Read-back therefore matches the frozen design, roles, states, relationships, graph, and predicted frontier exactly.

## Complete simulated operation log

1. `get_setup()` → compatible `fixture-tracker`; required Ready-for-agent fields, role mapping `enhancement`, and state mapping `ready-for-agent` available.
2. `get_parent("P-N02")` → existing parent `P-N02`, children `[]`, source design authorization `R52`.
3. `create_item(title="Migrate scheduled jobs to restart-safe schema v2", body=<exact FT-N02-1 body reproduced above>)` → created `FT-N02-1`; receipt only.
4. `create_item(title="Display the configured retry limit", body=<exact FT-N02-2 body reproduced above>)` → created `FT-N02-2`; receipt only.
5. `set_parent("FT-N02-1", "P-N02")` → success.
6. `set_parent("FT-N02-2", "P-N02")` → success.
7. No `set_blocker` operation: the audited graph has no true blocker edge.
8. `set_role("FT-N02-1", "enhancement")` → success.
9. `set_role("FT-N02-2", "enhancement")` → success.
10. `set_state("FT-N02-1", "ready-for-agent")` → success.
11. `set_state("FT-N02-2", "ready-for-agent")` → success.
12. `get_item("FT-N02-1")` → exact stored FT-N02-1 body reproduced above; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; blockers `[]`.
13. `get_item("FT-N02-2")` → exact stored FT-N02-2 body reproduced above; parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `none`; blockers `[]`.
14. `get_dependents("FT-N02-1")` → `[]`.
15. `get_dependents("FT-N02-2")` → `[]`.

No unavailable operation was called, and no live external mutation occurred.

## Stopped recommendation

`$implement` — start with `FT-N02-1`, the first ready item in tracker order. Although the two tickets are evidenced as mutually parallel-safe, top-level delivery of the verified parent was not explicitly requested, and the migration ticket contains an internal serial contract tripwire. Stop without invoking the owner.
