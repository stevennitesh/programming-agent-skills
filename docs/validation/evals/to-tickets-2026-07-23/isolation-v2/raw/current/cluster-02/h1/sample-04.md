# Published graph

Type: `published graph`

## Evidence and publication authority

- Source: `SRC-N02@1`
- Source owner: Dae, jobs owner
- Parent: `P-N02`
- Approved proposal revision: `R52`
- Approval: Dae reviewed and authorized the complete derived design `R52`.
- Setup evidence: `fixture-tracker` reported a compatible setup.
- Prepublication reconciliation: `SRC-N02@1`, `R52`, `fixture-tracker`, and parent `P-N02` matched the authorized publication scope; `P-N02` existed with no children.
- Mutation boundary: only the exact two-item simulated graph below changed.
- Unchanged source scope: job migration and retry-limit display.
- Exclusion preserved: unsettled product changes.

## Complete coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `I-N02-01`, including compatible expansion, restart-safe migration, rollback proof, and guarded contraction |
| Outcome: display retry limit | `I-N02-02`, as a pure current read |
| C1: migrate v1 jobs to restart-safe v2 with rollback proof | `I-N02-01` |
| C2: display the configured retry limit | `I-N02-02` |
| Absent/initial, current, incompatible, interruption, restart, rollback, and guarded-removal acceptance | `I-N02-01` acceptance and state-boundary matrix |
| Pure current retry-limit read | `I-N02-02` acceptance |
| `job_migration_matrix` proof | `I-N02-01` |
| `retry_display` proof | `I-N02-02` |
| Unsettled product changes | Explicitly excluded from both items |
| Team formed in 2019 | No ticket: historical note with no implementation commitment |
| Three abandoned UI mockups | No ticket: abandoned material |
| Suggested renaming of every helper | No ticket: unsettled suggestion and outside the settled outcome |
| Meeting greetings | No ticket: non-decision conversational content |
| Example tracker HTTP commands | No ticket: illustrative transport material; tracker procedure remains tracker-owned |

Every source-visible commitment and boundary has a disposition.

## Ordered stored item bodies

### `I-N02-01`

```markdown
# Migrate scheduled jobs from schema v1 to v2 with restart and rollback safety

Work-unit form: migration behavior slice using expand-migrate-contract.

Source Trace:
- Source: SRC-N02@1
- Owner: Dae, jobs owner
- Parent: P-N02
- Approved design: R52
- Commitment: C1
- Acceptance/proof pointers: migration acceptance in SRC-N02@1; job_migration_matrix

Desired behavior:
Expand supported job reads so v1 records without timezone and current v2 records remain operable; migrate each v1 record to a schema-valid v2 record containing timezone and retry count; preserve durable progress so an interrupted run resumes safely; retain the old-read path until rollback proof passes and old usage has ended; then permit guarded removal of the old-read path.

Observable acceptance:
1. Absent/initial state is a successful no-op and creates no job or migration residue.
2. A current valid v2 job remains readable and reusable without destructive conversion or semantic change.
3. A legacy v1 job remains readable during expansion and is converted into a schema-valid v2 job with timezone and retry count.
4. An interruption cannot expose a partially valid job; durable progress identifies completed work.
5. Restart resumes safely, is idempotent for already-completed work, and completes without duplicate jobs, lost jobs, or repeated semantic changes.
6. Rollback proof demonstrates that the supported pre-contraction read path remains operable and that rollback does not lose or corrupt jobs.
7. Old reads cannot be removed while old usage remains or compatibility/rollback proof is absent or failing; the system stays in the compatible expanded state.
8. Contraction is permitted only after old usage is absent and compatibility plus rollback proof passes.
9. job_migration_matrix proves the absent, current, incompatible, interruption, restart, rollback, and guarded-removal branches.

Edge/error behavior:
- Invalid or unconvertible legacy input fails safely, remains recoverable through the supported read/rollback path, and is not marked complete.
- A failed checkpoint or durable write cannot advance migration progress.
- A repeated migration or restart does not duplicate or remigrate a completed valid v2 record.
- A failing guard refuses contraction rather than removing compatibility.

Dependency state:
- True blockers: none.
- Tracker order: 1.
- No blocker edge is inferred from serial execution constraints.

Proof lane:
- Verification authority: Dae owns source meaning; executable job_migration_matrix assertions are the completion authority for the named behavior branches.
- Verification evidence: passing job_migration_matrix cases for absent, current v2 reuse, legacy v1 conversion, interruption, restart/idempotence, rollback, invalid input, and guarded removal.

Expected durable write scope:
- Production behavior: scheduled-job v1/v2 compatible reads, v1-to-v2 migration, progress/checkpoint, rollback, and contraction guard seams.
- Durable runtime data: only migrated schema-valid v2 job records and the progress/rollback state required for safe resume and proof.
- Proof: job_migration_matrix fixtures.

Scope fence:
- In scope: scheduled-job schema v1/v2 compatibility, conversion, restart safety, rollback proof, and guarded removal.
- Out of scope: retry-limit presentation, unrelated job behavior, unsettled product changes, broad helper renames, and tracker transport.

Parallel safety:
- Not safe to execute concurrently with I-N02-02 until the delivery owner proves disjoint production-write and proof-resource seams. Both touch the scheduled-job schema trust boundary; this is a serial constraint, not a blocker edge.

State-boundary matrix:
| Branch | Required behavior |
|---|---|
| Absent/initial | No-op; no synthetic job or migration residue |
| Current reusable | Valid v2 with timezone and retry count remains readable and reusable without destructive rewrite |
| Legacy/incompatible | v1 without timezone remains readable during expansion and converts to schema-valid v2 |
| Public access paths | Supported reads remain operable throughout expansion and migration; old reads are removed only after the guard passes |
| Supported variants | v1 and v2 during expansion/migration; v2 after guarded contraction |
| Interruption transition | No partial validity; completed progress is durable and incomplete work remains resumable |
| Restart transition | Resume from durable progress; repeated work is idempotent |
| Rollback transition | Preserve an operable supported read path and prove no job loss/corruption before contraction |
| Contract transition | Refuse removal until old usage is absent and compatibility/rollback proof passes |

Correlation identity: to-tickets:SRC-N02@1:R52:I-N02-01
Role: enhancement
Target state: ready-for-agent
```

### `I-N02-02`

```markdown
# Display the configured retry limit from current job state

Work-unit form: independently observable vertical behavior slice.

Source Trace:
- Source: SRC-N02@1
- Owner: Dae, jobs owner
- Parent: P-N02
- Approved design: R52
- Commitment: C2
- Acceptance/proof pointers: pure-current-read acceptance in SRC-N02@1; retry_display

Desired behavior:
Display the configured retry limit by reading the current configured retry-count value without deriving, defaulting, migrating, or mutating job state.

Observable acceptance:
1. For a current valid configured retry count, the displayed retry limit equals that value exactly.
2. Repeated display reads return the current configured value and perform no durable write.
3. A missing, invalid, or incompatible current value follows the existing read/validation error path and does not invent a value or mutate state.
4. retry_display proves the successful current read, repeated read, and error/no-write behavior.

Edge/error behavior:
- Zero and other schema-valid boundary values display exactly as configured.
- Missing, invalid, or incompatible input is not silently defaulted or coerced.
- Display failure leaves durable state unchanged.

Dependency state:
- True blockers: none.
- Tracker order: 2.
- The slice does not consume the migration outcome; no blocker edge is created.

Proof lane:
- Verification authority: Dae owns source meaning; executable retry_display assertions are the completion authority for the display behavior.
- Verification evidence: passing retry_display cases for exact current value, valid boundaries, repeated reads, missing/invalid/incompatible input, and absence of writes.

Expected durable write scope:
- Production behavior: current retry-count read and retry-limit presentation seam.
- Durable runtime data: none.
- Proof: retry_display fixtures.

Scope fence:
- In scope: presentation of the current configured retry count as the retry limit.
- Out of scope: schema migration, changing or defaulting retry configuration, unrelated UI changes, unsettled product changes, broad helper renames, and tracker transport.

Parallel safety:
- Not safe to execute concurrently with I-N02-01 until the delivery owner proves disjoint production-write and proof-resource seams. Both touch the scheduled-job schema trust boundary; this is a serial constraint, not a blocker edge.

State-boundary matrix:
Not applicable: this is a stateless pure-read presentation slice and performs no lifecycle transition or durable state mutation. Its supported input and error branches are captured in acceptance and proof.

Correlation identity: to-tickets:SRC-N02@1:R52:I-N02-02
Role: enhancement
Target state: ready-for-agent
```

## Dependency graph and observed frontier

```text
P-N02
├── I-N02-01  blockers: none
└── I-N02-02  blockers: none
```

- Blocking edges: none. Neither item consumes a required predecessor outcome.
- Cycle/missing-edge/contradictory-order check: none found.
- Stable tracker order: `I-N02-01`, then `I-N02-02`.
- Observed ready frontier: `I-N02-01`, `I-N02-02`.
- Both items are open, `ready-for-agent`, unclaimed, and have satisfied true blockers.
- Execution ordering: serialize at the shared scheduled-job schema trust boundary unless the delivery owner first proves the two write/proof-resource seams independent. This serialization does not change the frontier or create a blocker.

## Execution profiles

| Item | Semantic ownership | Expected production writes | Proof seam / scarce resource | Ordering and serial tripwire | Independence judgment |
|---|---|---|---|---|---|
| `I-N02-01` | Dae; scheduled-job migration semantics | Compatible reads, migration, durable progress/rollback, contraction guard; v2 job and progress state | `job_migration_matrix`; shared job-schema trust boundary | Tracker order 1; interruption, rollback, and contraction are serial tripwires | Ready independently, but serialize against `I-N02-02` until disjoint seams are proved |
| `I-N02-02` | Dae; retry-limit display semantics | Current-read/display behavior only; no durable runtime write | `retry_display`; shared job-schema trust boundary | Tracker order 2; pure-read/no-write invariant | Ready independently, but serialize against `I-N02-01` until disjoint seams are proved |

## Correlation identities

- `I-N02-01`: `to-tickets:SRC-N02@1:R52:I-N02-01`
- `I-N02-02`: `to-tickets:SRC-N02@1:R52:I-N02-02`

Preflight by the bounded parent read found no existing children, so neither deterministic identity was already represented under `P-N02`. No ambiguous creation occurred and no retry was attempted.

## Mutation read-back

| Item | Body | Parent | Blockers | Role | State | Assignee | Dependents |
|---|---|---|---|---|---|---|---|
| `I-N02-01` | Exact byte-for-byte body reproduced above | `P-N02` | none | `enhancement` | `ready-for-agent` | unclaimed | none |
| `I-N02-02` | Exact byte-for-byte body reproduced above | `P-N02` | none | `enhancement` | `ready-for-agent` | unclaimed | none |

Read-back matched the approved `R52` bodies, parent relationships, absence of blocker relationships, authorized roles, unclaimed assignees, and ready states. The observed frontier therefore matches the predicted frontier.

## Complete simulated operation log

1. `get_setup()` → compatible setup for `fixture-tracker`; ready state `ready-for-agent`; authorized role `enhancement`.
2. `get_parent("P-N02")` → parent exists; source `SRC-N02@1`; children `[]`.
3. `create_item(correlation="to-tickets:SRC-N02@1:R52:I-N02-01", body=<exact I-N02-01 body above>)` → created `I-N02-01`.
4. `create_item(correlation="to-tickets:SRC-N02@1:R52:I-N02-02", body=<exact I-N02-02 body above>)` → created `I-N02-02`.
5. `set_parent("I-N02-01", "P-N02")` → success.
6. `set_parent("I-N02-02", "P-N02")` → success.
7. `set_role("I-N02-01", "enhancement")` → success.
8. `set_role("I-N02-02", "enhancement")` → success.
9. `set_state("I-N02-01", "ready-for-agent")` → success.
10. `set_state("I-N02-02", "ready-for-agent")` → success.
11. `get_item("I-N02-01")` → exact stored body reproduced above; parent `P-N02`; blockers `[]`; role `enhancement`; state `ready-for-agent`; assignee unclaimed.
12. `get_item("I-N02-02")` → exact stored body reproduced above; parent `P-N02`; blockers `[]`; role `enhancement`; state `ready-for-agent`; assignee unclaimed.
13. `get_dependents("I-N02-01")` → `[]`.
14. `get_dependents("I-N02-02")` → `[]`.

No `set_blocker` operation was issued because the approved graph has no true dependency edge. All authorized mutations succeeded; there were no failed, ambiguous, retried, or unapplied operations.

## Safe continuation

- Gaps: none.
- Tracker state: the parent now has exactly the two verified children above; no other simulated tracker state changed.
- Recommendation: `$implement` for `I-N02-01`, the first ready item in tracker order, because the shared scheduled-job schema trust boundary is a serial tripwire until independence is proved.
- Stopped without invoking implementation or dispatching work.
