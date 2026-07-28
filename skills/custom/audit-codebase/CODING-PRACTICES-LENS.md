# Coding Practices Lens

Apply repository, language, framework, formatter, linter, type checker, and
test conventions before generic advice. These concepts are cross-language
questions, not universal syntax mandates.

## Concepts

- **Descriptive Naming:** names reveal domain meaning, units, state, and
  intent; vague aliases and misleading booleans increase caller burden.
- **Type Safety:** types represent valid states and preserve contracts across
  interfaces; unchecked escape hatches need evidence.
- **Immutability Default:** prefer values and updates that make state changes
  explicit; mutation is valid when locally owned, required, or measurably
  beneficial.
- **Explicit Error Handling:** failures preserve cause, useful context,
  cleanup, and the promised caller contract; neither swallowing nor
  indiscriminate wrapping is acceptable.
- **Input Validation:** validate at the Trust Boundary with rules derived from
  the contract, not duplicated arbitrary checks.
- **Clear Control Flow:** prefer visible happy, edge, and failure paths;
  guard clauses may reduce nesting when they preserve cleanup and ordering.
- **Why Comments:** explain surprising constraints, trade-offs, or policy;
  comments that narrate obvious syntax create drift.
- **Behavior Tests:** names and assertions describe observable behavior through
  the Proof Seam, including meaningful edge and failure branches.
- **Behavior-Owned Test Portfolio:** tests form the smallest diagnosable set of
  distinct responsibilities mapped to supported behavior, Invariants,
  branches, or risks. Ticket history, test count, and duplicate coverage do
  not earn retention.
- **Focused Concurrency:** independent work may run concurrently when ordering,
  resource pressure, cancellation, and failure semantics permit it; sequential
  code is not automatically a defect.

## Examples

Descriptive Naming:

```text
q, flag, x                  -> search_query, is_authenticated, total_revenue
```

The rename is a candidate only when the current names obscure supported
behavior or increase caller/test burden.

Why Comments:

```text
Weak:  "increment retry count"
Strong: "cap exponential backoff at 30s to preserve the partner timeout budget"
```

Explicit Error Handling:

```text
Weak:  catch every error, log "failed", throw an unrelated generic error
Strong: preserve the cause and caller-facing failure while performing required cleanup
```

Behavior Tests:

```text
Weak:  "works"
Strong: "rejects an overdraft through every debit entry path"
```

Behavior-Owned Test Portfolio:

```text
Weak:  one new test per ticket repeats the same setup, seam, and oracle
Strong: one behavior test or case table owns equivalent variants; distinct
        failure and lifecycle behavior stays independently diagnosable
```

## Smell Boundaries

Function length, nesting, magic values, comments, mutable state, broad types,
test count, and suite time are discovery hints. Admit a finding only when
direct evidence ties the practice to ambiguity, invalid states, duplicated
policy, failure exposure, change spread, proof friction, or avoidable
maintenance or execution cost.

For suspected test sprawl, map each relevant test to its supported behavior or
branch, Proof Seam, oracle, distinct risk, and observed cost. Admit
consolidation only when overlap has no distinct responsibility and the
surviving portfolio preserves coverage and diagnostic clarity. Retain
deliberate overlap when different layers prove different risks. Use
[PERFORMANCE-LENS.md](PERFORMANCE-LENS.md) for measured runtime or resource
claims.

Framework-specific examples from an upstream source do not override repository
authority. For example, copying a value is not an unconditional replacement
for locally owned mutation, and concurrent execution is not correct when
ordering, cancellation, resource pressure, or failure isolation matters.
