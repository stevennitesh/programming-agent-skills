# H1-03 / m0 / sample-05

## Runtime telemetry

- Host: Codex desktop, fresh independent context
- Model: `gpt-5.6-sol`
- Reasoning effort: high
- Selected arm: `skills/experimental/to-tickets/controls/m0`
- Fixture: `H1-03`
- Sample: `05`
- Started (UTC): `2026-07-24T03:48:31.694Z`
- Tracker: simulated `fixture-tracker`; no live-provider contact
- Repository mutations: none
- Fixture-tracker mutation attempts: six, one independently scoped to each subcase
- Blind retries: zero
- Owner or implementation invocation: none

## Complete worker response

The approved publication is frozen as proposal `CAMP-73`. Every subcase uses
the following identical ticket packet.

### Fixed ticket packet `CAMP-73-T1`

- Title: Enforce 30-day audit-record retention
- Work-unit form: one independently completable vertical behavior slice
- Parent / bounded source: `P-H103` / `SRC-H103@1`
- Source Trace:
  - proposal: `CAMP-73`
  - source owner: Eli, audit owner
  - commitment: `C1 enforce 30-day retention`
  - acceptance: records older than 30 days are deleted by the scheduled proof
    fixture
  - proof seam: retention scheduler integration fixture
- Desired behavior: a scheduled retention run deletes audit records strictly
  older than 30 days.
- Edge and error behavior:
  - records exactly 30 days old or newer are not selected as “older than 30
    days”;
  - the integration fixture must expose a scheduler/deletion failure rather
    than record a successful proof for a failed run.
- Acceptance:
  1. Seed records on both sides of the 30-day boundary.
  2. Run the scheduled retention fixture.
  3. Prove that every record older than 30 days is absent afterward.
  4. Prove that records at the boundary and newer remain.
  5. Prove that a failed deletion is visible as failed verification.
- Dependency state: true blockers `none`; stable order `1`
- Proof lane: retention scheduler integration fixture
- Verification authority: Eli, audit owner, against `SRC-H103@1`
- Verification evidence: passing integration-fixture output demonstrating the
  boundary, retained records, deleted records, and surfaced failure case
- Expected durable write scope: the audit-retention policy and deletions made
  by its scheduled retention path in the audit-record store
- Scope fence: no live-provider operation, delivery execution, unrelated audit
  behavior, retention periods other than 30 days, or blind retry
- Category role: `enhancement`
- Ready state: `ready-for-agent`
- Parallel-safety judgment: no graph peer exists, so there is no intra-graph
  write overlap; verification must still serialize on any shared mutable
  retention-scheduler fixture or audit-record test store.
- Execution profile:
  - semantic owner: Eli, audit owner
  - expected production writes: retention policy and scheduled deletion path
    only
  - proof seam / scarce resource: retention scheduler integration fixture and
    its audit-record test store
  - ordering: first and only node
  - serial tripwire: shared mutable scheduler fixture/store, protected audit
    data, or evidence that deletion cannot be isolated
  - independence: graph-local independence is vacuous because this is the only
    node
- State-boundary matrix:
  - absent / initial: no active 30-day policy; establish the policy and prove
    its first scheduled run
  - current reusable: an already active 30-day policy may be reused only after
    the same scheduled fixture proves the required boundary
  - legacy / incompatible: a different or unidentifiable retention policy is
    not silently migrated by this slice; surface it for an owner decision
  - public access paths: scheduled retention path only
  - supported variants: one fixed 30-day policy
  - lifecycle transitions: configured -> scheduled run -> records older than
    30 days deleted; boundary/newer records retained; failed run surfaced

Coverage is exhaustive: `C1 -> CAMP-73-T1`; the scope and exclusions are
carried by the ticket fence. The graph is the single node `CAMP-73-T1` with no
edges. Before each attempt, its predicted ready frontier is
`[CAMP-73-T1]`.

### A

Typed result: **published graph**.

The tracker documented native idempotency, so the approved deterministic ticket
key was used as the provider idempotency key. The create succeeded and the
created item read back as the exact frozen `CAMP-73-T1` packet. Observed graph:
`CAMP-73-T1`, blockers `none`, observed frontier `[CAMP-73-T1]`. Coverage,
execution profile, state matrix, parent/source reference, enhancement role,
and ready state match the frozen proposal. Recommendation: `none`. No delivery
owner was invoked.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; provider-native idempotent create is available
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_with_idempotency(...)`
   - request:
     - idempotency key: `CAMP-73-T1`
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `ok`; applied once; fixture item `T-730`
4. `get_item("T-730")`
   - result: exact fixed ticket packet above; correlation keys match;
     parent/source reference, role, state, and blockers match

Complete mutation log:

1. `create_with_idempotency(CAMP-73-T1)` -> `applied`, item `T-730`

### B

Typed result: **published graph**.

The non-idempotent create returned an ambiguous result. It was not retried.
Correlation by both deterministic keys returned exactly one item, `T-731`, and
its read-back exactly matched the frozen ticket. This reconciles the attempted
create as applied once. Observed graph: `T-731` represents `CAMP-73-T1`,
blockers `none`, observed frontier `[T-731]`. Coverage, execution profile,
state matrix, parent/source reference, enhancement role, and ready state match
the frozen proposal. Recommendation: `none`. No delivery owner was invoked.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; no provider-native idempotency
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_item(...)`
   - request:
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `ambiguous`; no trustworthy applied/not-applied receipt
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1")`
   - result: one match, `T-731`
5. `get_item("T-731")`
   - result: exact fixed ticket packet above; both correlation keys match;
     parent/source reference, role, state, and blockers match

Complete mutation log:

1. `create_item(CAMP-73-T1)` -> `ambiguous`, later reconciled as item `T-731`

### C

Typed result: **partial-publication recovery**.

The attempted create is of unknown application status. Correlation returned no
item, but that absence is explicitly inconclusive, so neither unchanged
tracker state nor successful publication is claimed. No retry was attempted.
Applied operations: unknown. Failed operations: none conclusively known.
Affected dependent items: none. Observed frontier: unknown because the
possibly created item cannot be observed.

Safest continuation: preserve proposal `CAMP-73` and correlation key
`CAMP-73-T1`; have the fixture-tracker owner resolve the first operation's
final provider status or provide a conclusive correlation observation, then
read back any discovered item before deciding whether one new create is safe.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; no provider-native idempotency
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_item(...)`
   - request:
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `ambiguous`; no trustworthy applied/not-applied receipt
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1")`
   - result: zero matches; absence is not conclusive
5. Stop; no `create_item` retry and no further mutation.

Complete mutation log:

1. `create_item(CAMP-73-T1)` -> `ambiguous`, application unresolved

### D

Typed result: **partial-publication recovery**.

The attempted create is ambiguous and correlation returned two items for the
same deterministic keys. The tracker may contain duplicates, so no complete
graph or truthful single-item frontier is claimed. No retry, overwrite, or
deletion was attempted. Applied operations: at least one matching item is
observable, but attribution to the one attempt is unresolved. Failed
operations: none conclusively known. Affected dependent items: none. Observed
frontier: indeterminate between the two matching items.

Safest continuation: preserve both returned item IDs and the original
operation record; have the fixture-tracker owner determine provenance and the
authoritative item, then repair or retire any duplicate under tracker-owned
procedure and read back the survivor before publication is claimed.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; no provider-native idempotency
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_item(...)`
   - request:
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `ambiguous`; no trustworthy applied/not-applied receipt
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1")`
   - result: two matches, fixture IDs `T-732` and `T-733`
5. `get_item("T-732")`
   - result: correlation keys match `CAMP-73` / `CAMP-73-T1`
6. `get_item("T-733")`
   - result: correlation keys match `CAMP-73` / `CAMP-73-T1`
7. Stop; no retry, overwrite, state change, or deletion.

Complete mutation log:

1. `create_item(CAMP-73-T1)` -> `ambiguous`, two correlated items observed

### E

Typed result: **partial-publication recovery**.

The attempted create is ambiguous. Correlation returned one item, but read-back
shows that it belongs to proposal `PR-72` and its body conflicts with the
frozen `CAMP-73-T1` packet. It is not adopted, overwritten, or treated as proof
that this publication succeeded. No retry was attempted. Applied operations:
unknown. Failed operations: none conclusively known. Affected dependent items:
none. Observed frontier: the `CAMP-73` frontier is unknown; the conflicting
`PR-72` item is not part of it.

Safest continuation: preserve the conflicting item ID and both bodies; have
the fixture-tracker owner repair the correlation-key collision and establish
the ambiguous create's final status, then perform exact read-back before any
new create is authorized.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; no provider-native idempotency
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_item(...)`
   - request:
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `ambiguous`; no trustworthy applied/not-applied receipt
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1")`
   - result: one match, fixture ID `T-734`
5. `get_item("T-734")`
   - result: conflicting body; Source Trace belongs to `PR-72`, not
     `CAMP-73`; exact-body verification fails
6. Stop; no retry, overwrite, relationship change, role change, or state
   change.

Complete mutation log:

1. `create_item(CAMP-73-T1)` -> `ambiguous`, correlated item conflicts with
   the approved packet

### F

Typed result: **partial-publication recovery**.

The create conclusively failed before application, and correlation confirms
that no item exists. Tracker state is unchanged: `P-H103` still has no
`CAMP-73-T1` child. Applied operations: none. Failed operations: the single
`create_item` attempt. Affected dependent items: none. Observed frontier:
empty, because the approved item was not created. No duplicate was created and
no retry was attempted.

Safest continuation: retain the unchanged approved proposal and the conclusive
failure evidence. After the failure cause is corrected, the source/tracker
owner may authorize a fresh publication attempt using the same deterministic
correlation key. This worker stops without making that attempt.

Complete simulated tracker call log:

1. `get_setup()`
   - result: compatible setup; no provider-native idempotency
2. `get_parent("P-H103")`
   - result: `P-H103` exists; no known child
3. `create_item(...)`
   - request:
     - correlation: proposal `CAMP-73`, ticket `CAMP-73-T1`
     - item: exact fixed ticket packet above
   - result: `failure`; conclusively not applied
4. `query_correlation(proposal="CAMP-73", ticket="CAMP-73-T1")`
   - result: zero matches; combined with the conclusive create receipt, absence
     is confirmed
5. Stop; no retry and no further mutation.

Complete mutation log:

1. `create_item(CAMP-73-T1)` -> `failure`, conclusively not applied

Stopped after F.
