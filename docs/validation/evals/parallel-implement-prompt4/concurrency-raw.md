# D0-CONCURRENCY / B0 Raw Outputs

Fixed scenario in every sample: four dependency-ready tickets. T1 and T2 have
disjoint files but share the `normalized_rate` invariant and exclusive
`RATE-E2E`; T3 and T4 are fully independent. Choose the concurrent dispatch
and name blockers. D0 omitted only the candidate's five-dimension
qualification language. B0 included it. Runtime: fresh `gpt-5.6-sol` subagent
context, repository tools prohibited, no peer outputs, default inherited
reasoning.

## D0-1

```text
Dispatch concurrently: T1, T3, and T4, each in an isolated lane.
T1 establishes normalized_rate and gets exclusive RATE-E2E.
T3 and T4 are independent in ownership, writes, proof, and ordering.
T2 is blocked until T1's invariant is integrated and verified: incompatible
semantic assumptions and exclusive RATE-E2E contention.
```

## D0-2

```text
Dispatch T1, T3, and T4 concurrently from the common HEAD.
T3/T4 are independent; T1 establishes normalized_rate.
T2 blocker: semantic coupling to T1 plus exclusive RATE-E2E contention.
Dispatch after T1 integrates, then rebase and prove against the invariant.
```

## D0-3

```text
Dispatch T1, T3, and T4 concurrently.
T1 establishes normalized_rate and exclusively leases RATE-E2E; T3 is an
independent docs lane; T4 is an independent tool/fixture lane.
T2 is blocked by implicit semantic dependency and exclusive environment use.
```

## D0-4

```text
Dispatch T1, T3, and T4 concurrently from clean HEAD.
T1 owns producer-side normalized_rate and RATE-E2E; T3/T4 are independent.
T2 is blocked by unrecorded semantic dependency and RATE-E2E contention;
dispatch only after T1 is integrated and reassess against the settled invariant.
```

## D0-5

```text
Dispatch T1, T3, T4 concurrently.
T1 establishes normalized_rate and reserves RATE-E2E; T3/T4 are independent.
T2 is blocked on T1's finalized invariant and exclusive RATE-E2E; dispatch
after T1 integrates and releases the environment.
```

## B0-1

```text
Dispatch T1, T3, T4 concurrently.
T1 has isolated parser ownership and exclusive RATE-E2E; T3/T4 have independent
ownership, writes, proof, and ordering.
T2 blocker: semantic ordering over normalized_rate plus RATE-E2E contention.
Dispatch only after T1's invariant and proof are reconciled.
```

## B0-2

```text
Dispatch T1, T3, and T4 concurrently from clean HEAD in isolated lanes.
T1 owns the rate-invariant change and RATE-E2E; T3/T4 are independent.
T2 blocker: semantic coupling plus exclusive RATE-E2E contention. Wait for
T1 integration/reconciliation, then prove T2 against the settled invariant.
```

## B0-3

```text
Dispatch T1, T3, and T4 concurrently in isolated lanes.
T1 establishes producer-side normalized_rate; T3/T4 are independent across
ownership, writes, proof seams, resources, and ordering.
T2 is blocked pending T1 reconciliation and by exclusive RATE-E2E contention.
```

## B0-4

```text
Dispatch T1, T3, and T4 concurrently.
T1 is independent of T3/T4 and exclusively holds RATE-E2E; T3/T4 are fully
independent.
T2 is blocked by semantic coupling and RATE-E2E contention. Reconcile T1,
then dispatch T2 from updated integration HEAD.
```

## B0-5

```text
Dispatch T1, T3, and T4 concurrently in isolated lanes.
T1 is the rate-invariant producer and sole RATE-E2E user; T3/T4 are independent.
T2 blocker: semantic/ordering coupling plus RATE-E2E contention. Reconcile T1,
then dispatch T2 against updated integration HEAD.
```
