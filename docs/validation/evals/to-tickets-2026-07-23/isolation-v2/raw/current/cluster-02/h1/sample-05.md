# Published graph

## Result identity and evidence

- Type: `published graph`
- Source: `SRC-N02@1`
- Source owner: `Dae, jobs owner`
- Parent: `P-N02`
- Approved proposal revision: `R52`
- Approval evidence: Dae, the source-meaning owner, reviewed and authorized the complete derived design `R52`.
- Setup evidence: `fixture-tracker` reported a compatible setup and the required Ready-for-agent contract.
- Source evidence: the supplied source packet, including commitments `C1` and `C2`, acceptance, scope, exclusions, proof fixtures, category, and parent.
- Pre-publication reconciliation: immediately before creation, setup remained compatible; `SRC-N02@1`, proposal `R52`, tracker `fixture-tracker`, and parent `P-N02` matched the approved publication target; `P-N02` still existed with no children. This parent-scoped empty-child read was the duplicate preflight because provider-native idempotent creation and correlation queries were unavailable.
- Observed tracker state: `P-N02` has exactly the two ordered children below. Both have role `enhancement`, state `ready-for-agent`, no assignee, and no blocker. No other fixture state changed.
- Gaps: none.
- Safe continuation: the graph is fully published and verified; no delivery owner should be invoked from this request.

## Exact stored item bodies

### `FT-N02-01` — Migrate scheduled jobs to restart-safe schema v2

```markdown
Proposal: R52
Correlation: R52:SRC-N02@1:C1
Parent: P-N02
Source Trace: SRC-N02@1; owner Dae, jobs owner; commitment C1; acceptance branch set and proof seam job_migration_matrix.

Bounded slice: Expand, migrate, and contract scheduled-job records from v1 to v2 while supported reads remain operable.
Work-unit form: migration behavior slice using expand-migrate-contract.

Desired behavior and acceptance:
- Absent or initial state: an empty job store completes as a no-op and remains valid.
- Current reusable state: valid v2 records are recognized and preserved without destructive rewriting.
- Legacy state: each v1 record is expanded/migrated to valid v2 with an explicit timezone and retry count while supported old and new reads remain operable.
- Incompatible state: a malformed, unsupported, or partly incompatible record is rejected or quarantined without corrupting valid records or falsely marking migration complete.
- Interruption: durable progress is recorded only after a record is validly written; an interruption leaves the store operable.
- Restart: rerunning resumes from durable progress, safely rechecks already migrated records, and does not duplicate or degrade them.
- Rollback: evidence proves the supported rollback path restores an operable prior-reading state before contraction is permitted.
- Guarded removal: old-read support is removed only after all supported records are v2, restart and rollback proof pass, and no old usage remains; a failed guard leaves old reads enabled.
- Edge and error behavior includes empty input, mixed v1/v2 input, repeated restart, invalid timezone or retry data, write failure, rollback failure, and removal-guard failure.

Relevant seams: scheduled-job record reader/writer, migration progress boundary, compatibility read path, rollback boundary, and job_migration_matrix fixture.
Expected durable write scope: scheduled-job v2 records and migration progress/compatibility metadata required for restart, rollback, and guarded contraction; no unrelated durable data.
Scope fence: includes only scheduled-job schema-v2 expansion, restart-safe migration, rollback proof, and guarded old-read contraction. Excludes retry-limit UI work, unrelated product changes, helper renames, abandoned mockups, and tracker transport examples.

Dependency state: true blockers none.
Proof lane: exercise job_migration_matrix across absent, current v2, v1, incompatible, interrupted, restarted, rollback, and guarded-removal branches, including mixed-state and failure interactions.
Verification authority: the accepted SRC-N02@1 migration acceptance owned by Dae.
Verification evidence: passing job_migration_matrix results for every named branch, with persisted-state observations demonstrating valid v2 writes, resumability, operable rollback, and refusal to contract when a guard fails.

Parallel safety: safe to run in parallel with FT-N02-02 because this slice owns job-record migration writes and migration proof resources, while FT-N02-02 is a stateless current-read display slice. Within this ticket, expand, migrate, rollback proof, and contract are serial; shared migration state, compatibility paths, and rollback/cutover are serial tripwires.
Tracker order: 1
```

### `FT-N02-02` — Display the configured retry limit

```markdown
Proposal: R52
Correlation: R52:SRC-N02@1:C2
Parent: P-N02
Source Trace: SRC-N02@1; owner Dae, jobs owner; commitment C2; pure-current-read acceptance and proof seam retry_display.

Bounded slice: Display the currently configured retry limit for a scheduled job.
Work-unit form: independently completable vertical display behavior slice.

Desired behavior and acceptance:
- The display reads the current configured retry limit without migrating, defaulting, or writing job state.
- For each supported configured retry-limit value, including zero and the supported upper boundary, the rendered value exactly matches the current value.
- A missing, invalid, unreadable, or unsupported current value produces the fixture-defined non-success/error presentation and never invents a retry limit.
- Read or rendering failure does not mutate the job record or migration state.

Relevant seams: current job read seam, retry-limit presentation seam, and retry_display fixture.
Expected durable write scope: none; this is a pure current read and presentation.
Scope fence: includes only reading and displaying the configured retry limit. Excludes schema migration, configuration editing, new defaults, product redesign, helper renames, abandoned mockups, and tracker transport examples.

Dependency state: true blockers none.
Proof lane: exercise retry_display with representative supported values, zero, upper-bound, missing, invalid, unreadable, and render-failure cases, and observe no durable writes.
Verification authority: the accepted SRC-N02@1 display acceptance owned by Dae.
Verification evidence: passing retry_display fixture results showing exact current values, defined error behavior, and an unchanged durable-state snapshot.

Parallel safety: safe to run in parallel with FT-N02-01 because it performs no durable writes and uses the separate retry_display proof resource. If its implementation would alter migration state or compatibility reads, that violates this ticket rather than creating an implicit overlap.
Tracker order: 2
```

## Coverage map

| Source element | Disposition |
|---|---|
| Outcome: migrate scheduled jobs to schema v2 | `FT-N02-01` |
| Outcome: display retry limit | `FT-N02-02` |
| `C1` restart-safe v1-to-v2 migration with rollback proof | `FT-N02-01` acceptance and proof |
| `C2` display configured retry limit | `FT-N02-02` acceptance and proof |
| Absent, current, incompatible, interruption, restart, rollback, guarded-removal proof | `FT-N02-01` acceptance, state matrix, and `job_migration_matrix` proof lane |
| Pure current retry-limit read | `FT-N02-02` acceptance and `retry_display` proof lane |
| Scope: job migration and retry-limit display | Exhausted by the two tickets |
| Exclusion: unsettled product changes | Explicitly fenced out of both tickets |
| Team formed in 2019 | No ticket: historical note with no implementation commitment |
| Three abandoned UI mockups | No ticket: explicitly abandoned context, not accepted design |
| Suggestion to rename every helper | No ticket: participant suggestion, not a settled commitment |
| Meeting greetings | No ticket: conversational material with no implementation commitment |
| Example tracker HTTP commands | No ticket: transport examples belong to the tracker owner and create no product commitment |

Every source-visible commitment and boundary has a ticket, exclusion, or explicit no-ticket reason.

## Dependency graph and frontier

Ordered graph:

1. `FT-N02-01` — blockers: `none`
2. `FT-N02-02` — blockers: `none`

There is no blocker edge: neither ticket consumes an outcome produced by the other. The serial stages inside `FT-N02-01` are execution constraints, not tracker blocker edges. The graph has no cycle, missing edge, contradictory order, or unresolved blocker.

Predicted frontier before publication: `FT-N02-01`, `FT-N02-02`.

Observed frontier after read-back: `FT-N02-01`, `FT-N02-02`, both open, `ready-for-agent`, unclaimed, and ordered as above.

## Execution profiles

### `FT-N02-01`

- Semantic ownership: Dae owns source meaning; the delivery owner may choose implementation details only within the accepted behavior and fence.
- Expected production writes: scheduled-job v2 records plus the minimum migration progress/compatibility metadata needed for safe restart, rollback, and guarded contraction.
- Proof seams and scarce resources: `job_migration_matrix`, durable migration state, compatibility reader, rollback path, and contraction guard.
- Ordering: expand-compatible form, migrate resumably, prove restart and rollback, confirm old usage ended, then contract.
- Serial tripwires: shared migration progress, mixed-version compatibility, rollback/cutover, invalid protected job data, and any irreversible removal.
- Independence: independent of `FT-N02-02`; all internal migration stages remain serial.

### `FT-N02-02`

- Semantic ownership: Dae owns source meaning; the delivery owner owns presentation technique within the pure-read requirement.
- Expected production writes: none.
- Proof seams and scarce resources: `retry_display`; no shared migration proof resource.
- Ordering: none beyond tracker order.
- Serial tripwires: any discovered attempt to mutate job or migration state stops this slice as a scope violation.
- Independence: evidenced by its separate fixture, no durable writes, and no consumption of the migration outcome.

## State-boundary matrices

### `FT-N02-01`

| Boundary or transition | Supported behavior | High-risk interaction / proof |
|---|---|---|
| Absent / initial | No-op; valid operable empty state | Must not fabricate records or completion state |
| Current reusable v2 | Preserve valid v2 and safely recognize prior progress | Repeated runs must not rewrite destructively |
| Legacy v1 | Read remains supported during expansion; write valid v2 | Mixed v1/v2 traversal and value validation |
| Incompatible / malformed | Reject or quarantine without corrupting valid state | Partial record, invalid timezone/retry data, unsupported form |
| Public access paths | Supported old and new reads remain operable until guarded contraction | Concurrent reads during migration |
| Supported variants | Empty, all-v1, all-v2, mixed v1/v2, interrupted partial progress | Cross-product with write failure and restart |
| Initial → expanded | Add compatible v2 form without removing old read support | Expansion must be releasable |
| Expanded → migrating | Persist each valid conversion and progress atomically enough to resume | Interruption between record write and progress update |
| Interrupted → restarted | Recheck durable state, resume, and remain idempotent | Repeated interruption/restart |
| Migrated → rollback proof | Demonstrate operable supported rollback before removal | Rollback failure blocks contraction |
| Proven → contracted | Remove old reads only after no old usage and all guards pass | Guard failure leaves compatibility enabled |

### `FT-N02-02`

State-boundary matrix: `not applicable`. The ticket is stateless because it performs a pure current read and presentation and is forbidden from writing job or migration state. Supported value and read/error variants are covered directly by its acceptance and proof lane.

## Correlation identities

- Proposal: `R52`
- Source: `SRC-N02@1`
- `FT-N02-01`: `R52:SRC-N02@1:C1`
- `FT-N02-02`: `R52:SRC-N02@1:C2`

The exact keys are stored in the corresponding item bodies. Initial parent read-back showed no children, so no existing correlated child could conflict. Both creates returned unique fixture IDs; no ambiguous creation or retry occurred.

## Mutation read-back

| Item | Exact body | Parent | Blockers | Role | Assignee | State | Dependents |
|---|---|---|---|---|---|---|---|
| `FT-N02-01` | Exact byte-for-byte body reproduced above | `P-N02` | none | `enhancement` | none | `ready-for-agent` | none |
| `FT-N02-02` | Exact byte-for-byte body reproduced above | `P-N02` | none | `enhancement` | none | `ready-for-agent` | none |

Parent read-back returned `P-N02` with ordered children `FT-N02-01`, `FT-N02-02`. Item and dependent read-back matched the approved `R52` graph, bodies, relationships, role, assignee, state, and frontier exactly.

## Complete simulated operation log

1. `get_setup()` → compatible `fixture-tracker`; Ready-for-agent contract and state `ready-for-agent`; authorized role `enhancement`.
2. `get_parent("P-N02")` → parent exists; source `SRC-N02@1`; children `[]`.
3. `get_setup()` → unchanged and compatible immediately before mutation.
4. `get_parent("P-N02")` → unchanged; children `[]`; approved parent relationship reconciled.
5. `create_item(title="Migrate scheduled jobs to restart-safe schema v2", body=<exact FT-N02-01 body above>, correlation="R52:SRC-N02@1:C1")` → success, ID `FT-N02-01`.
6. `create_item(title="Display the configured retry limit", body=<exact FT-N02-02 body above>, correlation="R52:SRC-N02@1:C2")` → success, ID `FT-N02-02`.
7. `set_parent("FT-N02-01", "P-N02")` → success.
8. `set_parent("FT-N02-02", "P-N02")` → success.
9. No `set_blocker` operation: the approved graph has no true blocker edge.
10. `set_role("FT-N02-01", "enhancement")` → success.
11. `set_role("FT-N02-02", "enhancement")` → success.
12. `set_state("FT-N02-01", "ready-for-agent")` → success.
13. `set_state("FT-N02-02", "ready-for-agent")` → success.
14. `get_item("FT-N02-01")` → exact stored title and body above; parent `P-N02`; blockers `[]`; role `enhancement`; assignee `none`; state `ready-for-agent`.
15. `get_dependents("FT-N02-01")` → `[]`.
16. `get_item("FT-N02-02")` → exact stored title and body above; parent `P-N02`; blockers `[]`; role `enhancement`; assignee `none`; state `ready-for-agent`.
17. `get_dependents("FT-N02-02")` → `[]`.
18. `get_parent("P-N02")` → ordered children `["FT-N02-01", "FT-N02-02"]`.

Applied operations: both creates, both parent links, both roles, and both ready-state mappings. Failed or unknown operations: none. Affected dependents: none.

## Stopped recommendation

Recommendation: `none`.

Reason: the request authorized shaping and simulated publication, not top-level parent delivery, and no delivery relationship otherwise applies. No implementation owner is invoked.
