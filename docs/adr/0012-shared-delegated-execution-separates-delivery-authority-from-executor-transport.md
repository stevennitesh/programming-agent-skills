# Shared Delegated Execution Uses A Plain Worker Handoff

## Status

Superseded in part by ADR-0017.

## Context


`$implement` directly delivers one selected item while `$parallel-implement`
coordinates independent graph workers. A worker needs resolved intent, bounded
scope, relevant repository context, validation, and stop conditions, but it does
not need the coordinator's planning transcript or a second execution authority.

The earlier design introduced a versioned Execution Assignment, content-addressed
Executor Capsule, Grounding Manifest, runtime receipts, and proof-gated cutover.
Those mechanisms duplicated authority already held by the ticket, repository,
coordinator, Git, and formal review. They delayed implementation without making
the worker's first action more reliable.

Concurrent writers still need mechanically safe checkout isolation. A new
worktree can also be slower or unusable when its test environment and temporary
paths have not been prepared.

## Decision

`$implement` owns one plain delegated implementation handoff containing the
ticket outcome, fixed decisions and relevant references, acceptance criteria,
owned scope and exclusions, exact base and working directory, required
validation, stop and escalation conditions, and expected evidence return.

The handoff is fresh ordinary task context. The worker starts when it receives
the information and performs no schema, capsule, hash, transcript, provenance,
profile-receipt, or content-classifier validation. It implements only its
assigned scope and returns observed evidence. The coordinator independently
verifies the diff, task commit when requested, and proof before accepting
completion.

One small helper prepares worktrees only for concurrent writers. It creates or
safely reuses an exact-base clean worktree, creates reusable pytest temp,
basetemp, and cache paths outside the tracked checkout, and runs a quick pytest
collection smoke when the checkout declares pytest through configuration or a
supported Python test layout. A newly created lane that fails preflight is
removed only after its exact base and cleanliness are reverified; reused,
changed, dirty, and uncertain lanes are preserved.

The same helper removes safe completed lanes at graph end or the oldest safe
completed lane under the existing runtime capacity limit. It considers only
lanes explicitly named completed and preserves omitted, dirty, unintegrated,
and uncertain lanes. Cleanup removes only the helper-owned released-lane state
under the configured root and its registered worktree. It never forces removal
or reports a lane removed when that bounded cleanup failed.

`$parallel-implement` composes the same handoff while retaining dependency and
independence judgment, claims, serial landing, recombined proof, formal review,
Repair, Lock, tracker closeout, and parent completion. Workers are direct
children of the coordinator and never spawn another worker.

## Considered Options

- Keep the capsule and assignment validator. Rejected because it duplicated
  existing authority and required the worker to validate context before doing
  the work.
- Keep the run ledger and provider-receipt platform. Rejected because normal
  coordinator task state, Git, and the tracker already own the necessary facts.
- Create worktrees for every delegated worker. Rejected because serial work
  needs no additional checkout automation.
- Hardcode a community-derived worker limit. Rejected because the runtime
  already owns capacity and the coordinator must still qualify independence and
  expected benefit.

## Consequences

- The strict assignment validator, capsule compiler, manifests, fixtures, and
  schema-oriented tests are removed rather than retained as compatibility paths.
- The existing worktree helper is simplified in place around `prepare` and
  `cleanup`; it is not a worker launcher or orchestration engine.
- Worker evidence is concise and useful but provisional. Formal review remains
  independent and evaluates the integrated candidate.
- `$implement` and `$parallel-implement` share handoff meaning without sharing
  their delivery lifecycles.
