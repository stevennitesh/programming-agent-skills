# Published graph

Type: `published graph`

Source: `SRC-N02@1`, owned by Dae, jobs owner. Parent: `P-N02`. Authorized derived design: `R52`.

Evidence:

- `get_setup` observed a compatible `fixture-tracker` setup with the stated Ready-for-agent contract, the `enhancement` role, and the `ready-for-agent` state.
- `get_parent(P-N02)` observed the existing parent with no children and the publication authority for complete derived design `R52`.
- The complete supplied source packet identifies two commitments, their acceptance and proof seams, the job-migration/retry-display scope, and the exclusion of unsettled product changes.

Gaps: none. The tracker changed only by the exact simulated graph below.

## Ordered ticket references and exact stored bodies

### `FT-N02-1`

```markdown
# Migrate scheduled jobs from schema v1 to restart-safe schema v2

Work-unit form: one stateful expand-migrate-contract migration slice.

Source Trace:
- Source: SRC-N02@1
- Parent: P-N02
- Owner: Dae, jobs owner
- Authorized derived design: R52
- Commitment: C1, migrate v1 jobs to restart-safe v2 with rollback proof
- Acceptance: absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior
- Proof seam: job_migration_matrix

Desired behavior:
Expand supported job access so legacy v1 records and current v2 records remain operable while all new or migrated writes are valid v2 records containing timezone and retry count. Migrate v1 jobs through an interruption-safe, resumable stage. Preserve an operable rollback path and legacy reads until rollback proof passes and old usage has ended; only then remove old reads.

Observable acceptance:
- With absent/initial job state, the migration is a safe no-op and supported creation continues to write valid v2.
- A current reusable v2 record remains valid and is not destructively rewritten.
- A supported legacy v1 record with no timezone is converted through the R52-authorized mapping into a valid v2 record containing timezone and retry count while supported reads remain operable.
- An incompatible record is detected without a destructive partial conversion and the migration reports the existing migration error outcome.
- If execution is interrupted after any durable migration step, a restart resumes safely, does not duplicate effects, and reaches the same valid v2 result.
- Rollback is exercised and evidenced while legacy reads are still present.
- Old reads cannot be removed before rollback proof passes and old usage has ended; after that guard passes, supported reads use v2.
- `job_migration_matrix` proves every listed branch and transition.

Seams:
- Production: scheduled-job schema/read compatibility, v2 write path, resumable migration checkpointing, rollback path, and guarded legacy-read removal.
- Proof: job_migration_matrix.

Expected durable write scope:
- Scheduled-job migration code and schema compatibility code.
- Scheduled-job records converted from v1 to v2.
- Migration progress/checkpoint state required for safe restart.
- No retry-limit display writes.

Scope fence:
- In scope: scheduled-job v1/v2 compatibility, migration, restart, rollback, and guarded old-read removal.
- Out of scope: retry-limit display, unrelated job behavior, helper renames, abandoned mockups, and unsettled product changes.

Dependency state: true blockers: none. Stable tracker order: 1.

Proof lane:
- Verification authority: the source acceptance authorized by Dae and the job_migration_matrix fixture.
- Verification evidence: passing matrix evidence for absent, current v2, legacy v1, incompatible, interruption, restart, rollback, and guarded-removal branches, including valid-v2 writes.

Parallel safety:
Safe to run in parallel with FT-N02-2 because this slice owns job persistence/migration seams and job_migration_matrix, while FT-N02-2 owns only the retry-limit presentation seam and retry_display fixtures. Within this ticket, expand, migrate, rollback proof, and contract are serial. Schema/data mutation, checkpoint state, rollback, and cutover are serial tripwires; no second job-migration writer may run concurrently.

State-boundary matrix:
| State or access branch | Required behavior | Evidence |
|---|---|---|
| Absent/initial | No-op safely; supported new writes are valid v2 | job_migration_matrix absent case |
| Current reusable v2 | Preserve the valid record and keep it readable | job_migration_matrix current case |
| Legacy v1, no timezone | Keep supported reads operable; migrate via the R52-authorized mapping to valid v2 | job_migration_matrix legacy case |
| Incompatible record | Detect, avoid destructive partial conversion, and report the migration error outcome | job_migration_matrix incompatible case |
| Interrupted migration | Persist safe progress; restart without duplicate effects and converge on valid v2 | job_migration_matrix interruption/restart cases |
| Public access during expand/migrate | Support legacy and v2 reads; write valid v2 | job_migration_matrix compatibility cases |
| Rollback transition | Roll back while old reads remain available and record proof | job_migration_matrix rollback case |
| Contract transition | Remove old reads only after rollback proof passes and old usage ends | job_migration_matrix guarded-removal case |

Supported variants are v1 legacy records without timezone and v2 records with timezone and retry count. Lifecycle is expand compatible access and v2 writes → migrate resumably → prove restart and rollback → verify old usage ended → contract old reads.
```

Stored metadata: parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee none.

### `FT-N02-2`

```markdown
# Display the configured retry limit

Work-unit form: one stateless vertical presentation slice.

Source Trace:
- Source: SRC-N02@1
- Parent: P-N02
- Owner: Dae, jobs owner
- Authorized derived design: R52
- Commitment: C2, display the configured retry limit
- Acceptance: display is a pure current read of the configured retry limit
- Proof seam: retry_display fixtures

Desired behavior:
Read the current configured retry limit without mutation and display that exact value.

Observable acceptance:
- For each supported configured retry-limit value, including boundary values represented by the fixture, the displayed value exactly matches the current configured value.
- Refreshing or rereading reflects the current configured value and does not retain a stale value.
- A missing or invalid configured value follows the existing current-read error behavior, does not fabricate a default, and performs no write.
- retry_display fixtures prove the successful, boundary, refresh, and read-error cases and prove that the display path is read-only.

Seams:
- Production: configured retry-limit read seam and retry-limit presentation seam.
- Proof: retry_display fixtures.

Expected durable write scope:
- Presentation and current-read integration code for retry-limit display.
- No durable runtime data writes, no job-record writes, and no migration/checkpoint writes.

Scope fence:
- In scope: pure current read and display of the configured retry limit.
- Out of scope: job migration, changing retry configuration, defaults or other product changes, helper renames, and abandoned mockups.

Dependency state: true blockers: none. Stable tracker order: 2.

Proof lane:
- Verification authority: the source acceptance authorized by Dae and the retry_display fixtures.
- Verification evidence: passing fixtures for exact display, supported boundaries, refreshed current reads, existing read-error behavior, and absence of writes.

Parallel safety:
Safe to run in parallel with FT-N02-1. This slice has a disjoint production write scope and proof resource: it changes only presentation/current-read integration and uses retry_display fixtures. It does not consume the migration outcome because schema v2 already stores retry count and the source requires a pure current read.

State-boundary matrix:
Not applicable. This is a stateless, read-only display slice; it neither owns nor transitions persisted state. Supported configured values and read-error behavior are acceptance/proof branches rather than lifecycle states.
```

Stored metadata: parent `P-N02`; role `enhancement`; state `ready-for-agent`; assignee none.

## Coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `FT-N02-1` |
| C1 restart-safe v1→v2 migration with rollback proof | `FT-N02-1` acceptance, proof lane, execution profile, and state matrix |
| C1 expand compatibility and valid-v2 writes | `FT-N02-1` |
| C1 interruption and restart | `FT-N02-1` |
| C1 rollback and guarded old-read removal | `FT-N02-1` |
| Outcome/C2: display retry limit | `FT-N02-2` |
| C2 pure current read | `FT-N02-2` |
| Scope: job migration and retry-limit display | Exhausted by `FT-N02-1` and `FT-N02-2` |
| Exclusion: unsettled product changes | Explicitly fenced from both tickets |
| Team formed in 2019; greetings | Context only; no implementation commitment |
| Three abandoned UI mockups | Explicitly abandoned; no ticket |
| Suggested rename of every helper | Unsettled suggestion and outside scope; no ticket |
| Example tracker HTTP commands | Appendix examples only; no ticket and no live call |

## Dependency graph and ready frontier

```text
P-N02
├── FT-N02-1  blockers: none
└── FT-N02-2  blockers: none
```

There is no blocker edge: neither ticket consumes a required outcome of the other. Stable tracker order is `FT-N02-1`, then `FT-N02-2`. The verified ready frontier is [`FT-N02-1`, `FT-N02-2`]; both are open, ready-for-agent, and unclaimed.

The execution profiles and applicable state matrices are stored verbatim in the ticket bodies above. Their production write scopes and proof resources are disjoint across tickets; only the internal expand-migrate-contract stages of `FT-N02-1` require serialization.

## Mutation read-back

- `get_item(FT-N02-1)` returned the exact first body and stored metadata reproduced above.
- `get_item(FT-N02-2)` returned the exact second body and stored metadata reproduced above.
- `get_dependents(FT-N02-1)` returned none.
- `get_dependents(FT-N02-2)` returned none.
- Parent links, `enhancement` roles, unassigned status, and `ready-for-agent` states all matched the intended graph.
- No mutation failed, was unknown, or mismatched.

## Complete simulated operation log

1. `get_setup()` → compatible setup; Ready-for-agent contract, `enhancement` role, and `ready-for-agent` state available.
2. `get_parent("P-N02")` → parent exists with no children; `SRC-N02@1` and authorized design `R52` govern publication.
3. `create_item(body = <the verbatim FT-N02-1 body above>)` → created `FT-N02-1`.
4. `create_item(body = <the verbatim FT-N02-2 body above>)` → created `FT-N02-2`.
5. `set_parent("FT-N02-1", "P-N02")` → success.
6. `set_parent("FT-N02-2", "P-N02")` → success.
7. No `set_blocker` operation: the audited graph has no true blocker edge.
8. `set_role("FT-N02-1", "enhancement")` → success.
9. `set_role("FT-N02-2", "enhancement")` → success.
10. `set_state("FT-N02-1", "ready-for-agent")` → success.
11. `set_state("FT-N02-2", "ready-for-agent")` → success.
12. `get_item("FT-N02-1")` → exact body and metadata reproduced above.
13. `get_item("FT-N02-2")` → exact body and metadata reproduced above.
14. `get_dependents("FT-N02-1")` → none.
15. `get_dependents("FT-N02-2")` → none.

Recommendation: `none`. Stop without invoking another owner.
