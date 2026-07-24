# Published graph

## Result type

`published graph`

## Evidence and publication boundary

- Source: `SRC-N02@1`, owned by Dae, jobs owner.
- Parent: `P-N02`.
- Authorization: Dae authorized complete derived design `R52`.
- Setup observation: `fixture-tracker` is compatible and exposes every operation required by this publication.
- Pre-publication tracker observation: `P-N02` exists with no children.
- Mutation boundary: only the exact two-item simulated graph below changed.
- Unchanged source meaning: outcome, commitments, acceptance, scope, exclusions, proof seams, and parent ownership remain those of `SRC-N02@1`.

## Frozen commitment ledger

| Source fact | Disposition |
|---|---|
| C1: migrate v1 jobs to restart-safe v2 with rollback proof | Covered by `FT-N02-1`. |
| C2: display the configured retry limit | Covered by `FT-N02-2`. |
| Absent-state proof | Acceptance in `FT-N02-1`. |
| Current-state proof | Acceptance in `FT-N02-1`; pure-current-read behavior in `FT-N02-2`. |
| Incompatible-state proof | Acceptance in `FT-N02-1`. |
| Interruption and restart proof | Acceptance in `FT-N02-1`. |
| Rollback proof | Acceptance in `FT-N02-1`. |
| Guarded removal of old reads | Acceptance in `FT-N02-1`. |
| `job_migration_matrix` proof seam | Verification lane in `FT-N02-1`. |
| `retry_display` proof seam | Verification lane in `FT-N02-2`. |
| Scope: job migration and retry-limit display | Exhausted by the two tickets. |
| Exclusion: unsettled product changes | Enforced by both scope fences. |
| Category: enhancement | Applied to both source-authorized implementation slices. |
| Team formed in 2019 | Context only; no implementation commitment and no ticket. |
| Three abandoned UI mockups | Historical, expressly abandoned; no ticket. |
| Suggestion to rename every helper | Unsettled product/implementation change; excluded and no ticket. |
| Meeting greetings | Non-decision conversational material; no ticket. |
| Example tracker HTTP commands | Appendix examples only; no tracker or implementation commitment and no ticket. |

Coverage is exhaustive: every source-visible commitment and scope boundary has a ticket acceptance, exclusion, or no-ticket reason.

## Ordered stored items

### `FT-N02-1` — Migrate scheduled jobs to restart-safe schema v2

The following is the exact stored body:

```text
Slice
Migrate scheduled-job records from schema v1 to schema v2 through an operable expand-migrate-contract sequence, while preserving supported reads until rollback and compatibility proof permit contraction.

Work-unit form
Stateful enhancement; one end-to-end migration behavior slice with internally ordered expand, migrate, and contract stages.

Parent and Source Trace
Parent: P-N02
Source: SRC-N02@1
Owner: Dae, jobs owner
Derived design: R52
Commitment: C1 migrate v1 jobs to restart-safe v2 with rollback proof
Acceptance source: prove absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior
Proof source: job_migration_matrix

Desired behavior and acceptance
1. Expand: supported reads remain operable for v1 records without timezone and for current valid v2 records; v2 writes include a valid timezone and retry count.
2. Absent/initial: with no job record, migration performs no invalid write and reports a safe no-op result.
3. Current/reusable: a valid v2 record is reused without destructive rewriting and remains readable.
4. Legacy/incompatible: a v1 record with no timezone is converted to valid v2 without losing supported job meaning; an incompatible or malformed record is rejected or quarantined by the settled migration boundary and is never represented as a successful valid-v2 migration.
5. Interruption: an interruption may leave only an operable, identifiable stage; it must not make supported reads fail or claim completion.
6. Restart: rerunning after interruption resumes or safely repeats work without duplicate effects and reaches the same valid v2 result.
7. Rollback: before old reads are removed, job_migration_matrix proves rollback from every released migration stage to an operable supported-read state.
8. Contract: old v1 reads are removed only after no old usage remains and compatibility plus rollback proof passes; otherwise removal is guarded and fails closed without changing the supported read path.
9. Error behavior: write, validation, compatibility, or rollback-proof failure preserves an operable supported state, reports failure, and does not advance the contraction guard.

Relevant seams
Scheduled-job schema reader, v2 writer, migration checkpoint/resume boundary, compatibility guard, rollback path, and job_migration_matrix fixture.

Expected durable write scope
Production writes are limited to scheduled-job schema/migration/checkpoint code and the compatibility/rollback guard required for v1-to-v2 transition. Proof writes are limited to job_migration_matrix fixtures and directly associated migration tests. Runtime data writes are limited to valid v2 job records and migration checkpoint state.

Scope fence
Do not change retry-limit display behavior, unrelated job behavior, product semantics, naming across helpers, abandoned UI work, tracker transport, or any unsettled product choice. Do not remove old reads before the contraction acceptance passes.

Dependency state
True blockers: none.
Stable tracker order: 1.
Internal stage order: expand, migrate, rollback/compatibility proof, contract. This internal order and its serial tripwires are not tracker blocker edges.

Proof lane
Run job_migration_matrix across absent, valid v2, v1-without-timezone, incompatible, interruption, restart, rollback, and guarded-removal branches, including write/validation/proof failures.

Verification authority
The acceptance and proof seams authorized by Dae in SRC-N02@1 and derived design R52.

Verification evidence
Passing job_migration_matrix results that identify each required branch, demonstrate valid v2 output, restart equivalence, operability after interruption and failure, successful rollback before contraction, and refusal to remove old reads while any guard is unsatisfied.

Parallel safety
Serial within this ticket: schema reads/writes, checkpoint state, rollback, and contraction share a state boundary and compatibility trust boundary. It may run in parallel with FT-N02-2 only if delivery preserves FT-N02-2 as a pure current read and coordinates any overlapping job model or fixture writes; uncertain or actual write/proof-resource overlap requires serialization.

State-boundary matrix
- Absent or initial state: no record; safe no-op, no invalid write.
- Current reusable state: valid v2 with timezone and retry count; remain readable and avoid destructive rewrite.
- Legacy state: v1 with no timezone; supported read remains operable and migration produces valid v2.
- Incompatible state: malformed or unsupported record; reject or quarantine, preserve operability, never claim successful migration.
- Public access paths: supported scheduled-job reads throughout expand and migrate; old v1 read path remains until guarded contraction; v2 write path writes only valid v2.
- Supported variants: absent, valid v2, v1 without timezone, and explicitly detected incompatible input.
- Lifecycle transitions: absent→absent; v2→v2; v1→checkpointed migration→valid v2; interrupted migration→restart/resume→valid v2; released migration stage→rollback→operable supported-read state; proven no-old-usage plus compatibility and rollback pass→old-read contraction.
- High-risk interactions: interruption during durable write, repeated restart, rollback after partial progress, incompatible input at migration boundary, and attempted contraction with old usage or failed proof.
```

Stored role: `enhancement`
Stored state: `ready-for-agent`
Stored parent: `P-N02`
Stored assignee/claim: none

### `FT-N02-2` — Display the configured retry limit

The following is the exact stored body:

```text
Slice
Display the configured retry limit for a scheduled job as a pure current read.

Work-unit form
Stateless enhancement; one independently provable display behavior slice.

Parent and Source Trace
Parent: P-N02
Source: SRC-N02@1
Owner: Dae, jobs owner
Derived design: R52
Commitment: C2 display the configured retry limit
Acceptance source: display is a pure current read of the configured retry limit
Proof source: retry_display fixtures

Desired behavior and acceptance
1. For a current job with a configured retry count, the display shows that exact configured retry limit.
2. Rendering is a pure current read: it does not migrate, normalize, default, persist, increment, or otherwise mutate the job or retry value.
3. Supported retry-limit variants represented by retry_display fixtures render their configured value without stale or derived substitution.
4. If the current configured retry limit cannot be read or is invalid under the existing settled contract, the display follows the existing error/empty-state path and does not invent or persist a value.

Relevant seams
Current scheduled-job read model, retry-limit presentation boundary, and retry_display fixtures.

Expected durable write scope
Production writes are limited to retry-limit read/presentation code. Proof writes are limited to retry_display fixtures and directly associated display tests. Runtime durable writes: none.

Scope fence
Do not change schema migration, retry semantics, defaults, configuration writes, unrelated UI, abandoned mockups, helper naming, or any unsettled product behavior.

Dependency state
True blockers: none.
Stable tracker order: 2.

Proof lane
Run retry_display fixtures for configured supported values and the existing unreadable/invalid-value error or empty-state branch; assert rendered output and absence of mutation.

Verification authority
The acceptance and proof seams authorized by Dae in SRC-N02@1 and derived design R52.

Verification evidence
Passing retry_display results showing exact configured values, the settled error/empty-state result for unreadable or invalid current data, and assertions that no job, configuration, migration, or retry state is written.

Parallel safety
Semantically independent from migration because it is a pure current read with no runtime durable writes. Parallel delivery with FT-N02-1 is safe only when production and fixture write sets are disjoint or coordinated; any shared job model or scarce fixture resource is a serial constraint, not a blocker edge.

State-boundary matrix
Not applicable: this ticket is a stateless pure current read and owns no lifecycle transition or durable runtime state. Its supported current-value and error/empty-state variants are covered as input/output proof branches.
```

Stored role: `enhancement`
Stored state: `ready-for-agent`
Stored parent: `P-N02`
Stored assignee/claim: none

## Dependency graph and ready frontier

```text
P-N02
├── FT-N02-1  blockers: none
└── FT-N02-2  blockers: none
```

There is no blocker edge: neither item consumes an outcome produced by the other. The graph is acyclic, has no missing edge, and makes no item falsely ready. Stable tracker order is `FT-N02-1`, then `FT-N02-2`.

Observed ready frontier: [`FT-N02-1`, `FT-N02-2`]. Both items are open in `ready-for-agent`, unclaimed, and have all true blockers satisfied.

## Execution profiles

| Item | Semantic ownership | Production writes | Proof seams / scarce resources | Ordering and serial tripwires | Independence judgment |
|---|---|---|---|---|---|
| `FT-N02-1` | Scheduled-job schema migration, compatibility, checkpoint/resume, rollback, contraction guard | Job schema/migration/checkpoint and compatibility/rollback guard | `job_migration_matrix`; migration state, rollback path, compatibility trust boundary | Expand→migrate→prove rollback/compatibility→contract; all internal stages serial; interruption, cutover, rollback, and old-read removal are serial tripwires | Independent of display semantics, but serialize against actual or uncertain shared job-model/fixture writes. |
| `FT-N02-2` | Retry-limit current-read presentation | Retry-limit read/presentation only; no runtime durable write | `retry_display`; any shared job-model fixture is scarce | No behavioral predecessor; shared file or proof-resource contention is a serial constraint only | Evidenced semantic independence from migration; parallel-safe when write/proof resources are disjoint or coordinated. |

## Mutation read-back

- `get_item(FT-N02-1)` returned the exact stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, no assignee, and no blockers.
- `get_item(FT-N02-2)` returned the exact stored body reproduced above, parent `P-N02`, role `enhancement`, state `ready-for-agent`, no assignee, and no blockers.
- `get_dependents(FT-N02-1)` returned none.
- `get_dependents(FT-N02-2)` returned none.
- `get_dependents(P-N02)` returned the ordered children [`FT-N02-1`, `FT-N02-2`].
- The observed bodies, relationships, roles, assignees, states, and frontier exactly match the frozen publication design.

## Complete simulated operation log

1. `get_setup()` → compatible `fixture-tracker`; ready state `ready-for-agent`; authorized category role `enhancement`; required operations available.
2. `get_parent("P-N02")` → parent exists; source `SRC-N02@1`; no children.
3. `create_item(title="Migrate scheduled jobs to restart-safe schema v2", body=<exact FT-N02-1 stored body reproduced above>)` → created `FT-N02-1`.
4. `create_item(title="Display the configured retry limit", body=<exact FT-N02-2 stored body reproduced above>)` → created `FT-N02-2`.
5. `set_parent("FT-N02-1", "P-N02")` → success.
6. `set_parent("FT-N02-2", "P-N02")` → success.
7. `set_role("FT-N02-1", "enhancement")` → success.
8. `set_role("FT-N02-2", "enhancement")` → success.
9. `set_state("FT-N02-1", "ready-for-agent")` → success.
10. `set_state("FT-N02-2", "ready-for-agent")` → success.
11. `get_item("FT-N02-1")` → exact body and stored fields reported in Mutation read-back.
12. `get_item("FT-N02-2")` → exact body and stored fields reported in Mutation read-back.
13. `get_dependents("FT-N02-1")` → `[]`.
14. `get_dependents("FT-N02-2")` → `[]`.
15. `get_dependents("P-N02")` → [`FT-N02-1`, `FT-N02-2`].

No `set_blocker` operation occurred because the frozen graph has no true blocker edge. No operation failed or was ambiguous. No external mutation occurred.

## Stopped recommendation

`$implement` — start with `FT-N02-1`, the first ready item in tracker order, because its migration trust boundary and serial tripwires make serial delivery the safe recommendation. Stop without invoking it.
