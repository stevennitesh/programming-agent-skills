# To Tickets Runtime Design Synthesis

Status: promoted active design.

The canonical runtime is `skills/custom/to-tickets` at package hash
`f652f1fb12787a482dcde59771e7b50f8dd5f7a890981df6acede35dc8a47758`.
It is the exact final C1 accepted by the 2026-07-23 Deploy Campaign. The
installed mirror must match that identity after managed synchronization.

Runtime authority remains in the canonical package. This synthesis records the
selected behavior, ownership, evidence boundary, rejected alternatives, and
residual gaps without restaging campaign chronology or tracker procedure.

## Selected Runtime

To Tickets converts one bounded body of settled implementation source into one
approved, exhaustive, dependency-ordered graph of independently grabbable
Ready-for-agent tickets. It verifies tracker state, recommends exactly one
implementation owner, and stops.

The runtime is explicit-only. It admits source only when outcome, decisions,
scope, exclusions, proof expectations, owner, and publication authority are
settled. Missing or incompatible tracker setup returns the exact
`$repo-bootstrap` precondition. A material source gap returns one complete gap
packet before slicing or mutation.

Its five leading words implement this semantic order:

```text
Trace -> Map -> Slice -> Approve -> Publish
      -> Mutation read-back -> recommend exactly one owner -> stop
```

- **Trace** covers the complete source and records decisions, scope, evidence,
  proof expectations, deferrals, rejections, and material gaps.
- **Map** inspects repository reality only far enough to identify stable seams,
  supported state, proof lanes, expected production scope, overlap, migration
  constraints, and durable pointers. Patch design remains with delivery.
- **Slice** covers every source-visible commitment exactly once, defaults to a
  fresh-session-sized vertical behavior slice, builds factual predecessor
  edges, and makes each ticket independently provable.
- **Approve** presents one identified complete revision and requires explicit
  approval of that exact revision.
- **Publish** reconciles freshness, publishes blockers first through the
  tracker owner, reads every affected surface back, and returns one safe result.

Successful publication requires every source commitment and scope boundary to
map to one ticket, explicit deferral or exclusion, or no-ticket reason. Every
ticket satisfies the tracker-owned Ready-for-agent contract and also carries
its source, work-unit form, applicable migration phase, rationale, covered
commitments, durable pointers, observable acceptance, highest meaningful proof
seam, blockers, expected write scope, semantic ownership, shared resources,
serial tripwires, and scope fence.

A blocking edge exists only when a dependent consumes a required predecessor
outcome. Tracker order, predicted overlap, readiness, shared resources, and
serial tripwires remain distinct. The local ready frontier is open,
Ready-for-agent, unclaimed work whose true blockers are satisfied, in tracker
order.

Stateful tickets apply the engineering contract's state-boundary matrix. A
parent-delivery request or plausible substantial independence adds the
conditional execution profile required by Parallel Implement: blockers,
semantic owner, production scope and exclusions, public proof seam and focused
proof, size, shared seam or scarce resource, and serial tripwire. To Tickets
records these facts; Parallel Implement alone decides runtime width.

Non-atomic compatibility work uses operable, releasable, backward-compatible
expand-migrate-contract stages. Contract waits until old usage ends and
compatibility proof passes. Migration phases are not automatically vertical
product slices.

Mutation read-back covers the parent, ordered children, bodies, roles, state,
relationships, blocking edges, affected dependents, and resulting frontier.
A failed, unknown, or mismatched mutation returns the approved revision,
observed operations, unknown state, frontier risk, and safest nonduplicating
recovery. Provider receipts alone do not establish completion.

After a completely verified graph, To Tickets selects exactly one next action:

- resolve a named blocker when the frontier is empty;
- recommend `$parallel-implement` for an explicitly requested parent-delivery
  run;
- recommend `$implement` for one ready ticket;
- recommend tracker-ordered `$implement` when ownership, scope, seam, fixture,
  proof resource, or tripwire overlaps;
- recommend `$parallel-implement` for at least two substantial, semantically
  independent, production-isolated, proof-isolated tickets; or
- default uncertain independence or economics to tracker-ordered `$implement`.

The skill recommends and stops. It does not implement, dispatch, review, claim,
or close tickets.

## Typed Returns And Completion

The runtime returns exactly one of:

- setup precondition;
- source-gap packet;
- no-ticket result;
- proposal awaiting approval;
- partial-publication recovery; or
- published graph.

Each result names its evidence, unchanged or observed tracker state, and exact
safe continuation. Only the published-graph branch is successful publication;
the other typed results are bounded stops.

## Ownership

| Surface | Owns | Excludes |
| --- | --- | --- |
| `skills/custom/to-tickets/SKILL.md` | Admission, complete source coverage, slicing, graph facts, approval, publication scope, typed Return, completion, and one next-owner decision | Tracker transport, implementation, runtime dispatch, review, claim, and closeout |
| `skills/custom/to-tickets/agents/openai.yaml` | Explicit-only invocation policy | Runtime procedure |
| Tracker docs and Repo Bootstrap-owned templates | Common Ready contract, roles, representation, queries, transport, and Mutation read-back procedure | Coverage judgment, slicing, approval, and execution economics |
| Engineering contract | Source Trace, proof, state-boundary matrix, evidence, and Lock vocabulary | Ticket procedure |
| Source owner and `$to-spec` | Settled intent, parent completeness, decisions, and proof expectations | Ticket graph design and tracker mutation |
| `$triage` | Equivalent Ready-contract production from raw incoming work | To Tickets coverage and parent decomposition |
| `$implement` | Delivery of one selected Ready item | Ticket repair, graph mutation, and parent campaign execution |
| `$parallel-implement` | Parent-graph admission, serial or parallel execution, landing, review, Lock, and release | To Tickets approval, source decisions, and publication |
| Relationship index and routing docs | Caller-callee edges and public routing | Skill-local procedure |
| Contract tests and validation records | Structural and bounded behavioral evidence | Runtime rules or generalized efficacy claims |
| Installed mirror | Managed copy at canonical parity | Independent edits |

The 2026-07-23 campaign found no relationship delta. The existing edges remain:
Repo Bootstrap owns setup repair; tracker docs own transport and read-back;
engineering owns shared proof and state semantics; To Tickets recommends
exactly one implementation owner and stops.

## 2026-07-23 Runtime Decision

The campaign shape was `pruning-only`: the prior canonical runtime differed
from exact `B0 = C1`. Exact B0 package hash
`f652f1fb12787a482dcde59771e7b50f8dd5f7a890981df6acede35dc8a47758`
passed all `55/55` minimum-runtime judgments. B01-B11 remain independently
required by intent, compatibility, authority, safety, proof, caller, or
completion contracts. No behavioral-efficacy claim is made for a B0 unit whose
no-guidance control also passed.

Three beyond-minimum mechanisms were rejected independently because exact B0
did not exhibit their registered failure:

| Unit | Proposed addition | Decision |
| --- | --- | --- |
| C101 | Tracer-purpose and tracer-learning-role clauses | `rejected-no-control-failure`; B0 passed five positive and five wrong-condition judgments |
| C102 | Conditional support-slice clause | `rejected-no-control-failure`; B0 passed five positive and ten wrong-condition judgments |
| C103 | Blast-radius and progressive-exposure clause | `rejected-no-control-failure`; B0 passed five positive and five wrong-condition judgments |

Exact B0 passed all `35/35` registered C1-control judgments, so no candidate arm
was opened and no mechanism-contribution claim survives. The mandatory Pruning
Pass audited every runtime passage, found no material behavior-preserving cut,
and retained the exact bytes with disposition `pruning-not-needed`.

## Evidence

| Record | Authority |
| --- | --- |
| [Prompt 4 evaluation](../../validation/transcripts/2026-07-23-to-tickets-prompt4-eval.md) | Original exact tasks, packets, rubric, raw-output identities, samples, and terminal observations |
| [Prompt 4 reconciliation](../../validation/transcripts/2026-07-23-to-tickets-prompt4-reconciliation.md) | Accepted exact B0 as behavior-complete C1 and recorded individual C101-C103 rejection |
| [Pruning Pass](../../validation/transcripts/2026-07-23-to-tickets-pruning.md) | Complete cut audit and byte-identical no-cut decision |
| [Prompt 5 promotion and install](../../validation/transcripts/2026-07-23-to-tickets-promotion-install.md) | Canonical promotion, current mechanical proof, managed synchronization, and installed parity |
| [Earlier I3 promotion](../../validation/transcripts/2026-07-22-to-tickets-i3-promotion-eval.md) | Historical prior-runtime evidence only |

The current campaign reuses exact behavioral evidence because final bytes,
tasks, claims, authority, and evidence contracts did not change between Prompt
4 acceptance, pruning, and promotion. Structural proof demonstrates the
canonical contract and relationships; it does not independently prove slicing
quality or behavioral efficacy.

## Deliberate Non-Changes

- Invocation remains explicit-only.
- The runtime remains one linear five-verb skill with no disclosed helper.
- Tracker procedure and shared engineering rules remain with their owners.
- Relationship surfaces remain byte-unchanged because the relationship delta
  is none.
- No mandatory proposal file, graph renderer, ticket generator, numeric sizing
  score, story-point quota, mechanical coverage validator, or direct
  implementation dispatch is added.
- C101-C103 remain outside the runtime and receive no efficacy claim.
- Raw and chronological validation records remain historical evidence and are
  not rewritten as active instructions.

## Residual Gaps

- live-provider publication, read-back, idempotency, and recovery;
- support-work comparative economics without supplied facts;
- generalization beyond the exact fixtures, runtime, and local harness; and
- unavailable model and configuration telemetry recorded by Prompt 4.

Any material runtime or claim change creates a new candidate identity and a
proportionate proof obligation. Installation and Git delivery remain separate
from canonical semantic authority.
