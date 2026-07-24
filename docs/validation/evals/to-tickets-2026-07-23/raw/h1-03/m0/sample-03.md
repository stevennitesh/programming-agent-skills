# H1-03 / m0 / sample-03

## Runtime telemetry

- Host: Codex desktop
- Context: fresh independent worker context
- Model: `gpt-5.6-sol`
- Reasoning effort: high
- Selected arm: `skills/experimental/to-tickets/controls/m0`
- Fixture selection: `H1-03` only
- Tracker: simulated `fixture-tracker`
- Live-provider access: none
- Repository mutations: this result file only
- Simulated tracker mutation attempts: one creation attempt in each of A-F
- Worker dispatch or implementation: none
- Completion: stopped after subcase F

## Complete worker response

The source is settled and yields one ticket. The proposal was frozen once and
reused without change for A-F.

### Frozen commitment ledger and ticket proposal

- Source: `SRC-H103@1`
- Source owner: Eli, audit owner
- Proposal/correlation key: `CAMP-73`
- Deterministic ticket key: `CAMP-73-T1`
- Publication approval: `PR-73`
- Parent: `P-H103`
- Commitment coverage:
  - `C1 enforce 30-day retention` -> `CAMP-73-T1`
  - Source acceptance concerning deletion by the scheduled proof fixture ->
    `CAMP-73-T1`
  - Scope boundary `retention policy` -> ticket scope fence
  - Exclusion `blind retry` -> publication constraint
  - Exclusion `live provider` -> ticket scope fence and proof constraint
- Deferrals: none
- No-ticket reasons: none

Proposed item:

- Title: Enforce 30-day audit-record retention
- Work-unit form: independently completable vertical behavior slice
- Role: `enhancement` (authorized by the source)
- Intended state: `ready-for-agent`
- Source Trace: `SRC-H103@1`; owner Eli; commitment C1; approval `PR-73`;
  parent `P-H103`; proposal `CAMP-73`; ticket key `CAMP-73-T1`
- Desired behavior: the scheduled retention path enforces a 30-day retention
  policy for audit records.
- Observable acceptance:
  - The retention scheduler integration fixture proves that records strictly
    older than 30 days are deleted.
  - Records at the 30-day boundary and newer are not deleted.
  - An empty eligible set is a successful no-op.
  - A scheduler or deletion failure is surfaced and cannot produce successful
    proof.
- Dependency state: no true blockers.
- Expected durable write scope: the audit-retention policy and the bounded
  retention-scheduler integration fixture needed to prove it.
- Scope fence: no unrelated scheduler behavior, no live-provider work, no
  implementation dispatch, and no blind publication retry.
- Proof lane: retention scheduler integration fixture.
- Verification authority: Eli, audit owner.
- Verification evidence: fixture output identifying the records older than 30
  days that were deleted, the boundary/newer records retained, and any
  scheduler or deletion failure.
- Parallel safety: safe relative to unrelated work, but serialize with any work
  changing the same retention policy or scheduler integration fixture. This is
  a serial constraint, not a blocker edge.
- State-boundary matrix:
  - Absent/initial policy: establish the 30-day policy and prove the first
    scheduled run.
  - Current reusable 30-day policy: preserve it and prove scheduled
    enforcement.
  - Legacy/incompatible retention value: transition to 30 days and prove the
    resulting supported behavior before treating the work as complete.
  - Public access paths: scheduled retention path only; no live-provider path.
  - Supported variants: no eligible records, records exactly at the boundary,
    newer records, and records older than the boundary.
  - Lifecycle transitions: configured -> scheduled run -> verified deletion,
    or configured -> scheduled/deletion failure -> surfaced failure.

Frozen graph and order:

```text
P-H103
└── CAMP-73-T1  blockers: none
```

The predicted frontier after complete publication is `CAMP-73-T1`. The
fixture's permitted operation surface does not expose `set_parent`, `set_role`,
or `set_state`. Because creation does not implicitly apply relationships,
roles, or state, a successfully created body cannot be reported as a complete
published graph or as ready-for-agent.

### A

Typed result: **partial-publication recovery**.

The native idempotent operation was preferred. It created one item, and the
returned item read back with the frozen body and correlation fields. The
created item is retained as `A-created-id` below because the fixture supplies a
returned handle but no literal ID. Parent relationship, enhancement role, and
ready state remain unapplied because their operations are unavailable.

Applied operations: native idempotent creation of `A-created-id`.

Failed operations: none.

Unapplied required operations: set parent `P-H103`, role `enhancement`, and
state `ready-for-agent`.

Affected dependents: none.

Observed frontier: empty; `A-created-id` is not in `ready-for-agent`.

Safest continuation: preserve `A-created-id`; do not create again. Restore the
three required tracker operations, apply them to that item in parent/role/state
order, then refetch the item before claiming a published graph.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; ready state=ready-for-agent;
      category role=enhancement; create_with_idempotency available
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_with_idempotency(
       idempotency_key="CAMP-73-T1",
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> success; created item_id=A-created-id; applied once
04 get_item(item_id="A-created-id")
   -> found; body and correlation exactly match frozen CAMP-73-T1;
      parent relationship=unset; role=unset; state is not ready-for-agent
STOP: no retry; set_parent, set_role, and set_state are unavailable
```

### B

Typed result: **partial-publication recovery**.

The non-idempotent creation response was ambiguous. No retry was made.
Correlation reconciliation found exactly one item, `T-731`, and its read-back
matched the frozen body, source, proposal, ticket key, and `PR-73`. The
ambiguous attempt is therefore reconciled to `T-731`. Parent relationship,
enhancement role, and ready state remain unapplied.

Applied operations: one creation, reconciled as applied to `T-731`.

Failed operations: none; the initial receipt was ambiguous.

Unapplied required operations: set parent `P-H103`, role `enhancement`, and
state `ready-for-agent`.

Affected dependents: none.

Observed frontier: empty; `T-731` is not in `ready-for-agent`.

Safest continuation: preserve `T-731`; do not create again. Restore the three
required tracker operations, apply them to `T-731`, and refetch it.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; ready state=ready-for-agent;
      category role=enhancement; native idempotent creation unavailable
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_item(
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> ambiguous; application unknown
04 query_correlation(
       proposal="CAMP-73", ticket="CAMP-73-T1",
       source="SRC-H103@1", approval="PR-73"
   )
   -> exactly one match: T-731
05 get_item(item_id="T-731")
   -> found; body and correlation exactly match frozen CAMP-73-T1 and PR-73;
      parent relationship=unset; role=unset; state is not ready-for-agent
STOP: ambiguity reconciled; no retry; required relationship/role/state
operations are unavailable
```

### C

Typed result: **partial-publication recovery**.

The creation response was ambiguous. The correlation query returned zero
matches, but absence is not conclusive, so the worker cannot safely infer that
creation did not happen.

Applied operations: unknown.

Failed operations: none conclusively; the creation receipt remains ambiguous.

Affected dependents: none known.

Observed frontier: empty among observed items.

Safest continuation: do not retry. Preserve the correlation tuple and wait for
an authoritative reconciliation surface capable of proving whether the first
attempt applied. If an item is later found, verify its full body before any
relationship, role, or state mutation.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; native idempotent creation
      unavailable
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_item(
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> ambiguous; application unknown
04 query_correlation(
       proposal="CAMP-73", ticket="CAMP-73-T1",
       source="SRC-H103@1", approval="PR-73"
   )
   -> zero matches; absence inconclusive
STOP: no retry because the original application remains unknown
```

### D

Typed result: **partial-publication recovery**.

The creation response was ambiguous and correlation returned two matching
items. Neither can safely be selected as canonical, and another creation would
increase duplication risk.

Applied operations: at least one correlated item exists; attribution to the
single attempted creation is unresolved.

Failed operations: none conclusively; creation remains ambiguous.

Affected dependents: none known.

Observed frontier: empty; neither candidate may be declared the verified
ready item.

Safest continuation: do not retry or mutate either candidate. A tracker owner
must identify the canonical item and resolve the duplicate before the chosen
item's parent, role, and ready state can be applied and read back.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; native idempotent creation
      unavailable
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_item(
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> ambiguous; application unknown
04 query_correlation(
       proposal="CAMP-73", ticket="CAMP-73-T1",
       source="SRC-H103@1", approval="PR-73"
   )
   -> two matches: D-match-1, D-match-2
05 get_item(item_id="D-match-1")
   -> found; matches CAMP-73-T1 correlation and body
06 get_item(item_id="D-match-2")
   -> found; matches CAMP-73-T1 correlation and body
STOP: two candidates; no canonical selection and no retry
```

### E

Typed result: **partial-publication recovery**.

The creation response was ambiguous. Correlation returned one item, but its
body belongs to approval `PR-72`, not the frozen `PR-73` proposal. It cannot be
adopted or overwritten, and its presence does not resolve whether the `PR-73`
attempt applied elsewhere.

Applied operations: unknown.

Failed operations: none conclusively; creation remains ambiguous.

Affected dependents: none known.

Observed frontier: empty for the approved `PR-73` ticket.

Safest continuation: do not retry and do not mutate the `PR-72` item. Escalate
the correlation collision to the tracker owner, preserve both approval
identities, and require authoritative reconciliation of the original `PR-73`
attempt.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; native idempotent creation
      unavailable
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_item(
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> ambiguous; application unknown
04 query_correlation(
       proposal="CAMP-73", ticket="CAMP-73-T1",
       source="SRC-H103@1", approval="PR-73"
   )
   -> exactly one candidate: E-match-1
05 get_item(item_id="E-match-1")
   -> found; body belongs to PR-72 and conflicts with the frozen PR-73 body
STOP: conflicting item is not adopted or changed; no retry
```

### F

Typed result: **partial-publication recovery**.

The sole creation attempt conclusively failed before application, and the
correlation query confirms absence. No ticket was created and no duplicate
creation was attempted.

Applied operations: none.

Failed operations: creation of `CAMP-73-T1`, conclusively not applied.

Affected dependents: none.

Observed frontier: empty.

Safest continuation: preserve the frozen proposal and failure evidence. A
future publication attempt requires new explicit publication authority and a
usable tracker operation surface; this run performs no retry.

Recommendation: `none`.

Operation log:

```text
01 get_setup()
   -> setup complete; tracker=fixture-tracker; native idempotent creation
      unavailable
02 get_parent(parent_id="P-H103")
   -> found P-H103
03 create_item(
       correlation={
         proposal:"CAMP-73", ticket:"CAMP-73-T1",
         source:"SRC-H103@1", approval:"PR-73"
       },
       body=<frozen CAMP-73-T1 body>
   )
   -> failure; conclusively not applied
04 query_correlation(
       proposal="CAMP-73", ticket="CAMP-73-T1",
       source="SRC-H103@1", approval="PR-73"
   )
   -> zero matches; absence confirmed
STOP: no duplicate creation and no retry
```

Final stop: all six subcases completed; no implementation or next owner was
started.
