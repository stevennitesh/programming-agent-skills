# Published graph

## Result identity

- Type: `published graph`
- Source: `SRC-N02@1`
- Source owner: `Dae, jobs owner`
- Parent: `P-N02`
- Approved proposal revision: `R52`
- Tracker: `fixture-tracker`
- Tracker state before publication: setup compatible; `P-N02` existed with no children.
- Tracker state after publication: `P-N02` has the two ordered children below; both are unclaimed and `ready-for-agent`; no blocker relationships exist.
- Publication boundary: only the complete source-justified graph was changed.
- Gaps: none.

Immediately before mutation, the simulated reconciliation confirmed source
`SRC-N02@1`, owner authorization of exact derived design `R52`, compatible
setup, target `fixture-tracker`, parent `P-N02`, and an empty pre-publication
child set. The empty parent and the deterministic correlation identities below
provided the available duplicate preflight; neither provider-native
idempotency nor correlation query was available. No creation result was
ambiguous.

## Ordered ticket references

1. `FT-N02-001` — Migrate scheduled jobs through restart-safe schema-v2 cutover
2. `FT-N02-002` — Display the configured retry limit from current job state

## Exact stored item bodies

### `FT-N02-001`

```markdown
Title: Migrate scheduled jobs through restart-safe schema-v2 cutover
Correlation identity: R52:T01
Parent / bounded source: P-N02 / SRC-N02@1
Source Trace: SRC-N02@1 outcome; C1; acceptance requirement for absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior; proof seam job_migration_matrix; approved derived design R52.
Role: enhancement
Work-unit form: Stateful expand-migrate-contract behavior slice.

Desired behavior:
- Expand reads compatibly so supported v1 and v2 jobs remain operable while all new or rewritten jobs are valid v2 records containing timezone and retry count.
- Migrate v1 jobs through restart-safe, checkpointed work; interruption leaves an operable state and restart resumes without duplicating or corrupting completed work.
- Preserve a proved rollback path until compatibility evidence passes.
- Contract old-read support only after old usage is absent and the compatibility and rollback guards pass.

Observable acceptance and edge/error behavior:
- job_migration_matrix proves the absent branch is a safe no-op and valid v2 writes remain available.
- It proves a current valid v2 record is reusable and is not degraded by migration.
- It proves a supported v1 record lacking timezone becomes a valid v2 record while supported reads remain operable.
- It proves an incompatible record is reported and isolated without destructive partial conversion or loss of other operable records.
- It proves interruption at a recorded migration boundary leaves a releasable state.
- It proves restart resumes from durable progress and reaches the same valid v2 result without duplicate effects.
- It proves rollback restores the supported pre-contract read path and does not require unproved data reconstruction.
- It proves old-read removal is refused while old usage remains or compatibility/rollback proof is incomplete, and succeeds only after every guard passes.

Dependency state: true blockers: none. Stable tracker order: 1.
Proof lane: job_migration_matrix.
Verification authority: Dae owns source semantics; the approved SRC-N02@1 criteria and job_migration_matrix fixture are authoritative for acceptance.
Verification evidence: passing fixture evidence for every named matrix branch, including operable intermediate stages, valid v2 writes, restart equivalence, rollback, and guarded removal.
Expected durable write scope: scheduled-job v2 fields (including timezone and retry count), migration progress/checkpoint state, and the compatibility/removal gate needed by this cutover.
Scope fence: no retry-limit UI, no unrelated job product behavior, no blanket helper rename, no abandoned mockup work, and no tracker-transport implementation.
Parallel safety: not safe to execute concurrently with work that changes scheduled-job schema/read compatibility, migration checkpoints, cutover guards, or job_migration_matrix. This is a serial constraint, not a blocker edge.
```

Stored tracker fields:

- ID: `FT-N02-001`
- Parent: `P-N02`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: unclaimed
- Blockers: none

### `FT-N02-002`

```markdown
Title: Display the configured retry limit from current job state
Correlation identity: R52:T02
Parent / bounded source: P-N02 / SRC-N02@1
Source Trace: SRC-N02@1 outcome; C2; acceptance requirement that display is a pure current read of the configured retry limit; proof seam retry_display; approved derived design R52.
Role: enhancement
Work-unit form: Stateless vertical display behavior slice.

Desired behavior:
- Display exactly the configured retry limit read from current supported job state.
- Keep the display path pure: it does not migrate, default, recompute, normalize, or persist the retry limit.

Observable acceptance and edge/error behavior:
- retry_display proves the rendered value equals the configured current retry limit.
- Re-reading unchanged current state produces the same display and no durable write.
- Missing or invalid configured input follows the existing validation/error path unchanged; the slice does not invent a fallback value or silently write a repair.

Dependency state: true blockers: none. Stable tracker order: 2.
Proof lane: retry_display.
Verification authority: Dae owns source semantics; the approved SRC-N02@1 criteria and retry_display fixture are authoritative for acceptance.
Verification evidence: passing fixture evidence for exact current-value display, repeat-read purity, zero durable writes, and preservation of the existing invalid-input path.
Expected durable write scope: none.
Scope fence: no schema migration, no configuration editing, no retry policy change, no fallback/default product decision, no blanket helper rename, and no abandoned mockup work.
Parallel safety: not safe to execute concurrently with the migration slice because both cross the scheduled-job current-read/schema-compatibility seam; serialize until that shared seam is stable. This is a serial constraint, not a blocker edge.
```

Stored tracker fields:

- ID: `FT-N02-002`
- Parent: `P-N02`
- Role: `enhancement`
- State: `ready-for-agent`
- Assignee: unclaimed
- Blockers: none

## Coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `FT-N02-001` |
| C1: restart-safe v1-to-v2 migration with rollback proof | `FT-N02-001` |
| Absent, current, incompatible, interruption, restart, rollback, and guarded-removal acceptance | `FT-N02-001` acceptance and state-boundary matrix |
| Outcome: display retry limit | `FT-N02-002` |
| C2: display configured retry limit | `FT-N02-002` |
| Pure current-read acceptance | `FT-N02-002` |
| Scope: job migration and retry-limit display | Exhausted by the two tickets |
| Exclusion: unsettled product changes | Preserved as both scope fences; no ticket |
| Team formed in 2019 | Historical context, not an implementation commitment; no ticket |
| Three abandoned UI mockups | Explicitly abandoned material, not current acceptance; no ticket |
| Participant suggestion to rename every helper | Unsettled suggestion excluded by source authority; no ticket |
| Meeting greetings | Non-decision conversational content; no ticket |
| Example tracker HTTP commands | Foreign tracker-transport examples, not source behavior or a commitment; no ticket |

Every source-visible implementation commitment and boundary therefore has one
ticket, an explicit exclusion, or a no-ticket reason.

## Dependency graph and frontier

```text
P-N02
├── FT-N02-001  blockers: none
└── FT-N02-002  blockers: none
```

- Blocking edges: none. Neither slice consumes a required completed outcome of
  the other.
- Cycles: none.
- Missing or contradictory edges: none.
- Stable tracker order: `FT-N02-001`, then `FT-N02-002`.
- Predicted frontier before mutation: empty.
- Observed frontier after read-back: `FT-N02-001`, `FT-N02-002`.
- Both items are open, ready, unclaimed, and blocker-free. Their shared
  current-read/schema seam is a serial tripwire only and does not falsify the
  frontier.

## Execution profiles

| Ticket | Semantic ownership | Production writes | Proof seam / scarce resource | Ordering and serial tripwires | Independence judgment |
|---|---|---|---|---|---|
| `FT-N02-001` | Dae owns job-schema and migration meaning | v2 job fields, migration checkpoint state, compatibility/removal gate | `job_migration_matrix`; scheduled-job compatibility seam | Tracker order 1; serialize schema/read compatibility, checkpoint, cutover, and matrix changes | Blocker-independent but not parallel-safe across the shared job seam |
| `FT-N02-002` | Dae owns retry-limit display meaning | none | `retry_display`; scheduled-job current-read seam | Tracker order 2; serialize with migration while the shared reader/schema seam changes | Blocker-independent but not parallel-safe with `FT-N02-001` |

## State-boundary matrices

### `FT-N02-001`

| Boundary branch | Required behavior / proof |
|---|---|
| Absent / initial | No migratable v1 job is a safe no-op; valid v2 writes stay operable. |
| Current reusable | A valid v2 job, including timezone and retry count, remains reusable and is not degraded. |
| Legacy supported | A v1 job with no timezone remains readable during expansion and is converted to valid v2. |
| Incompatible | The record is reported and isolated; no destructive partial conversion or collateral loss occurs. |
| Public access paths | Supported scheduler/job reads stay operable through expand and migrate; old-read access is removed only by the guarded contract stage. |
| Supported variants | v1 reads during compatibility, valid v2 reads and writes, and releasable intermediate checkpoint states. |
| Interruption transition | Interruption preserves durable progress and an operable state. |
| Restart transition | Restart resumes safely and converges without duplicate effects. |
| Rollback transition | Rollback proof restores the supported pre-contract read path before any old-read removal. |
| Contract transition | Old reads are removed only when old usage is absent and compatibility plus rollback evidence passes. |
| High-risk interactions | v1/v2 coexistence, writes during migration, checkpoint recovery, rollback before contract, and guard refusal are each exercised by `job_migration_matrix`. |

### `FT-N02-002`

State-boundary matrix: `not applicable`. This slice is a pure current read,
creates no durable state, and owns no lifecycle transition. Its relevant
read-only variants are a valid configured current limit and the existing
missing/invalid-input error path; `retry_display` proves both without a write.

## Correlation identities

| Proposal | Ticket | Correlation identity |
|---|---|---|
| `R52` | `FT-N02-001` | `R52:T01` |
| `R52` | `FT-N02-002` | `R52:T02` |

The identities were included in the exact stored bodies. Pre-publication
`get_parent(P-N02)` observed no children. Creation was unambiguous, so no blind
retry or recovery query was needed.

## Mutation read-back

| Item | Exact body | Parent | Role | Assignee | State | Blockers | Dependents |
|---|---|---|---|---|---|---|---|
| `FT-N02-001` | Exact literal body reproduced above | `P-N02` | `enhancement` | unclaimed | `ready-for-agent` | none | none |
| `FT-N02-002` | Exact literal body reproduced above | `P-N02` | `enhancement` | unclaimed | `ready-for-agent` | none | none |

Both `get_item` observations matched the exact stored bodies and every intended
field. Both `get_dependents` observations were empty, confirming the graph and
frontier. No failed, unknown, mismatched, or partial mutation remained.

## Complete simulated operation log

1. `get_setup()` → compatible `fixture-tracker`; Ready-for-agent contract,
   `enhancement` role, and `ready-for-agent` state available.
2. `get_parent("P-N02")` → parent exists; source `SRC-N02@1`; children `[]`.
3. `create_item(correlation="R52:T01", body=<exact FT-N02-001 body reproduced above>)`
   → success, fixture ID `FT-N02-001`.
4. `create_item(correlation="R52:T02", body=<exact FT-N02-002 body reproduced above>)`
   → success, fixture ID `FT-N02-002`.
5. `set_parent("FT-N02-001", "P-N02")` → success.
6. `set_parent("FT-N02-002", "P-N02")` → success.
7. `set_role("FT-N02-001", "enhancement")` → success.
8. `set_role("FT-N02-002", "enhancement")` → success.
9. `set_state("FT-N02-001", "ready-for-agent")` → success.
10. `set_state("FT-N02-002", "ready-for-agent")` → success.
11. `get_item("FT-N02-001")` → exact stored body reproduced above; parent
    `P-N02`; role `enhancement`; assignee unclaimed; state
    `ready-for-agent`; blockers `[]`.
12. `get_item("FT-N02-002")` → exact stored body reproduced above; parent
    `P-N02`; role `enhancement`; assignee unclaimed; state
    `ready-for-agent`; blockers `[]`.
13. `get_dependents("FT-N02-001")` → `[]`.
14. `get_dependents("FT-N02-002")` → `[]`.

`set_blocker` was not called because the approved graph has no true dependency
edge. No unavailable operation was invoked.

## Safe continuation

Recommendation: `$implement` for `FT-N02-001`, the first ready item in tracker
order. Stop without invoking it. Serial delivery is required because the two
ready items share the scheduled-job current-read/schema-compatibility seam.
