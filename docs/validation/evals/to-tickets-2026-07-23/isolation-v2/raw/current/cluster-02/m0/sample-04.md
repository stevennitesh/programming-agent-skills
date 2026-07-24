# Published graph

## Evidence and tracker state

- Result type: `published graph`
- Source: `SRC-N02@1`
- Source owner: Dae, jobs owner
- Parent: `P-N02`
- Authorized design: `R52`
- Setup evidence: `get_setup` reported a compatible `fixture-tracker` setup with the stated Ready-for-agent contract and operations.
- Source evidence: the complete supplied packet settles C1, C2, their acceptance, scope, exclusions, proof fixtures, category, and parent. Dae authorized the complete derived design R52.
- Initial tracker state: `P-N02` existed with no children.
- Observed tracker state: `P-N02` has exactly `FT-N02-01` and `FT-N02-02` as children. Both are open, unassigned, categorized `enhancement`, and in `ready-for-agent`. There are no blocker edges.
- Gaps: none.

## Frozen commitment ledger and coverage

| Source fact | Disposition |
|---|---|
| C1: migrate v1 jobs to restart-safe v2 with rollback proof | `FT-N02-01` |
| C1 acceptance: absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior | `FT-N02-01` acceptance and state-boundary matrix |
| C1 proof: `job_migration_matrix` | `FT-N02-01` proof lane |
| C2: display the configured retry limit | `FT-N02-02` |
| C2 acceptance: pure current read of the configured retry limit | `FT-N02-02` acceptance |
| C2 proof: `retry_display` | `FT-N02-02` proof lane |
| Scope: job migration and retry-limit display | Enforced by both ticket scope fences |
| Exclusion: unsettled product changes | Explicitly excluded from both tickets |
| Category: enhancement | Applied to both source-authorized implementation items |
| Team formed in 2019 | No ticket: historical context, not a commitment |
| Three abandoned UI mockups | No ticket: explicitly abandoned material |
| Suggested renaming of every helper | No ticket: unsettled suggestion and excluded product-independent cleanup |
| Meeting greetings | No ticket: conversational noise |
| Example tracker HTTP commands | No ticket: illustrative appendix, not source authority or an implementation commitment |

Coverage is exhaustive: every source-visible commitment and boundary has a ticket, exclusion, or no-ticket reason.

## Ordered stored items

### 1. `FT-N02-01` — Migrate scheduled jobs to restart-safe schema v2

Exact stored body:

```markdown
Work unit: migration — one bounded expand-migrate-contract slice that keeps supported job reads operable, migrates legacy jobs restart-safely, proves rollback, and guards removal of old reads.

Source Trace:
- Source: SRC-N02@1
- Parent: P-N02
- Authorized design: R52
- Commitment: C1
- Acceptance/proof: absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior through job_migration_matrix

Desired behavior and acceptance:
- Expand: supported reads remain operable for both legacy v1 jobs and current v2 jobs while all newly written or migrated records are valid v2 records.
- A legacy v1 job, including one with no timezone field, migrates to a schema-valid v2 record while preserving the job's observable scheduling behavior and configured retry count.
- A current valid v2 job is reused without semantic change or destructive rewrite.
- An absent job produces no record and no migration side effect.
- Migration can be interrupted after any durable step; rerunning it resumes safely, neither duplicates a job nor loses or double-applies job state, and converges on the same valid v2 result.
- Rollback to the supported pre-contract reader is proven against the expanded/migrated state before removal of legacy-read support is allowed.
- Contract: legacy-read removal is rejected while any supported v1 record remains, while migration completion is unproven, or while rollback proof is absent; it is permitted only after those guards pass.
- Invalid or incompatible records fail observably without being silently converted or discarded.

State-boundary matrix:
| Boundary | Required behavior |
|---|---|
| Absent/initial | No-op; create no job and report no migration failure. |
| Current reusable | Preserve a valid v2 record and its timezone/retry semantics. |
| Legacy/incompatible | Read supported v1, produce valid v2, preserve observable scheduling and retry semantics; reject unsupported or invalid input without destructive writes. |
| Public access paths | Supported job readers remain operable throughout expand and migrate; old-read removal stays guarded during contract. |
| Supported variants | Valid v1 without timezone and valid v2 with timezone/retry count are distinct supported branches; invalid/unsupported records are an error branch. |
| Lifecycle transitions | v1 -> expanded compatibility -> restart-safe migrated v2 -> rollback-proven state -> guarded removal of v1 reads. Interruption/restart is exercised at durable migration boundaries. |

Dependencies:
- True blockers: none. Current schema v2 and the authorized R52 behavior are supplied facts.
- Stable tracker order: 1.

Proof lane:
- Verification authority: the source-authorized job_migration_matrix fixture.
- Verification evidence required: passing rows for absent, current v2, legacy v1 without timezone, incompatible input, interruption at each durable boundary, restart convergence, rollback, and both rejected and permitted legacy-read removal.
- Completion evidence must identify the expand, migrate, rollback, and contract assertions; a create or migration receipt alone is insufficient.

Expected durable write scope:
- Production code/configuration: scheduled-job schema compatibility, v2 writing, migration/resume bookkeeping, rollback support, and the guarded legacy-reader removal seam only.
- Runtime state: only scheduled-job records and migration metadata required for idempotent resume.
- Tests/fixtures: job_migration_matrix coverage for the listed branches.

Parallel safety:
- Judgment: serial with FT-N02-02 despite no blocker edge.
- Reason: both slices touch or consume the scheduled-job representation/read seam; unverified concurrent changes could obscure which slice changed retry-count read semantics.
- Serial tripwire: any change to the shared job model, reader contract, retry-count meaning, or fixture setup requires sequencing and re-verification of both proof lanes.

Scope fence:
- In scope: scheduled-job v1/v2 compatibility, restart-safe migration, rollback proof, and guarded legacy-read removal.
- Out of scope: retry-limit presentation, unrelated schema changes, helper renames, abandoned UI work, and any unsettled product change.
```

Stored fields: parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `unassigned`; blockers `none`.

### 2. `FT-N02-02` — Display the current configured retry limit

Exact stored body:

```markdown
Work unit: behavior — one bounded display slice that reads and presents the configured retry limit from current job state without mutating it.

Source Trace:
- Source: SRC-N02@1
- Parent: P-N02
- Authorized design: R52
- Commitment: C2
- Acceptance/proof: pure current read of the configured retry limit through retry_display

Desired behavior and acceptance:
- The display shows exactly the retry limit in the current supported job state.
- Each display read reflects the current configured value, including zero and supported boundary values; it does not substitute a default for a present value or present stale cached state as current.
- Reading and displaying the value performs no scheduled-job or configuration write.
- Missing, invalid, incompatible, or failed current reads follow the existing observable read-error behavior and do not fabricate a retry limit.

State-boundary matrix:
- Not applicable: this ticket is a stateless, pure current read. It neither owns persistence nor causes lifecycle transitions. Supported, missing, invalid, and failed read results are covered as input/error cases in retry_display rather than as durable-state branches.

Dependencies:
- True blockers: none. Current schema v2 already stores retry count, so this slice does not consume the migration outcome.
- Stable tracker order: 2.

Proof lane:
- Verification authority: the source-authorized retry_display fixture.
- Verification evidence required: passing cases for an ordinary configured value, zero, supported boundaries, a value changed before the next read, missing/invalid/incompatible state, read failure, and proof that the display path makes no durable write.

Expected durable write scope:
- Production code/configuration: the retry-limit display and its current-read adapter only.
- Runtime state: none.
- Tests/fixtures: retry_display coverage for the listed value, freshness, error, and no-write cases.

Parallel safety:
- Judgment: serial with FT-N02-01 despite no blocker edge.
- Reason: this slice consumes the scheduled-job representation/read seam that the migration slice may change.
- Serial tripwire: any shared job-model, reader-contract, retry-count semantic, or fixture-setup change requires sequencing and re-verification of both proof lanes.

Scope fence:
- In scope: current retry-limit read and display.
- Out of scope: job migration, configuration editing, caching policy changes, unrelated UI redesign, helper renames, abandoned mockups, and any unsettled product change.
```

Stored fields: parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee `unassigned`; blockers `none`.

## Dependency graph and frontier

```text
P-N02
├── FT-N02-01  (no blockers; tracker order 1)
└── FT-N02-02  (no blockers; tracker order 2)
```

- Blocking edges: none.
- Cycle/missing-edge/contradictory-order audit: no cycles, no missing required edge, and no contradictory order. FT-N02-02 does not depend on FT-N02-01 because current schema v2 already supplies retry count; shared seams create a serial constraint, not a blocker.
- Predicted and observed ready frontier, in tracker order: `FT-N02-01`, `FT-N02-02`.
- Both items are open, ready-for-agent, and unclaimed. The execution profiles require serial implementation while the shared read/model seam remains uncertain.

## Mutation read-back

Read-back returned these exact stored values:

| Item | Title | Parent | Role | State | Assignee | Blockers |
|---|---|---|---|---|---|---|
| `FT-N02-01` | Migrate scheduled jobs to restart-safe schema v2 | `P-N02` | `enhancement` | `ready-for-agent` | unassigned | none |
| `FT-N02-02` | Display the current configured retry limit | `P-N02` | `enhancement` | `ready-for-agent` | unassigned | none |

- `get_item(FT-N02-01)` returned the first exact body above and the listed stored fields.
- `get_item(FT-N02-02)` returned the second exact body above and the listed stored fields.
- `get_parent(P-N02)` returned children `[FT-N02-01, FT-N02-02]` in that order.
- `get_dependents(FT-N02-01)` returned `[]`.
- `get_dependents(FT-N02-02)` returned `[]`.
- Intended mutations and observed state match. No operation failed or remained unknown.

## Complete simulated operation log

| # | Operation | Observation |
|---:|---|---|
| 1 | `get_setup()` | Compatible fixture-tracker setup and Ready-for-agent contract returned. |
| 2 | `get_parent(P-N02)` | Existing parent returned with no children; source `SRC-N02@1` and authorized design `R52` matched. |
| 3 | `create_item(title="Migrate scheduled jobs to restart-safe schema v2", body=<first exact body above>)` | Success; returned `FT-N02-01`. |
| 4 | `create_item(title="Display the current configured retry limit", body=<second exact body above>)` | Success; returned `FT-N02-02`. |
| 5 | `set_parent(FT-N02-01, P-N02)` | Success. |
| 6 | `set_parent(FT-N02-02, P-N02)` | Success. |
| 7 | `set_role(FT-N02-01, enhancement)` | Success. |
| 8 | `set_role(FT-N02-02, enhancement)` | Success. |
| 9 | `set_state(FT-N02-01, ready-for-agent)` | Success. |
| 10 | `set_state(FT-N02-02, ready-for-agent)` | Success. |
| 11 | `get_item(FT-N02-01)` | Returned the first exact body and stored fields shown above. |
| 12 | `get_item(FT-N02-02)` | Returned the second exact body and stored fields shown above. |
| 13 | `get_parent(P-N02)` | Returned children `[FT-N02-01, FT-N02-02]` in stable order. |
| 14 | `get_dependents(FT-N02-01)` | Returned `[]`. |
| 15 | `get_dependents(FT-N02-02)` | Returned `[]`. |

No `set_blocker` operation was issued because the frozen graph contains no true blocker edge.

## Stopped recommendation

`$implement` for `FT-N02-01`, the first ready item in tracker order. The two ready items share a scheduled-job representation/read seam and have an explicit serial tripwire, so serial delivery is required. Recommendation only; no owner was invoked.
