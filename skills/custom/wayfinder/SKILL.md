---
name: wayfinder
description: Chart or advance one finite tracker-backed route from a bounded foggy destination to coherent settled source for a specification.
---

# Wayfinder

Own one outcome: a finite tracker-backed route from a bounded foggy destination to coherent settled source for `$to-spec`. Tickets resolve decisions and prerequisites; they do not deliver the destination or create implementation tickets.

Wayfinder is explicit-only. The user starts or resumes it by naming `$wayfinder`. Other skills may recommend it and stop; none invokes it automatically.

Before tracker mutation, read `docs/agents/issue-tracker.md`, section `Wayfinder tracker mapping`. The mapping must identify the map, ticket, relationship, claim, revision, and read-back primitives; it grants no process authority. Wayfinder owns Mutation read-back semantics; the mapping supplies only the primitive. When a required mapping is missing, placeholder, `unavailable`, or incompatible, recommend `$repo-bootstrap` with the exact precondition and stop.

## Navigation

- **Destination:** the settled-source readiness state that fixes scope and closes the campaign.
- **Map:** the durable orientation index; tickets own detailed questions, resolutions, and assets.
- **Ticket:** one sharp question or prerequisite with one resolver, authority, and expected return.
- **Frontier:** open, unblocked, unclaimed tickets whose dependencies are satisfied, in map order.
- **Fog:** tethered in-scope uncertainty whose sharp question is not yet known.
- **Campaign claim:** the map-scoped concurrency guard for one mutating operation.
- **Closure snapshot:** the declared map, ticket, evidence, budget, authority, domain, and provider-revision state gathered before Seal.

Use a ticket when the question is sharp, even when blocked. Keep uncertainty as fog only while its question is unclear and its finite sharpening source is recorded.

## Chart Or Orient

Resolve the stable destination identity before choosing an operation. Query every open and closed mapped map object and compare its `Stable destination identity:` field exactly:

- **zero maps:** read [Qualification And Chart](OPERATIONS.md#qualification-and-chart);
- **one map:** read the applicable groups in [MAP-FORMAT.md](MAP-FORMAT.md), derive integrity, and use the state table below; or
- **several plausible maps:** return their identity, lifecycle, disposition, owner, predecessor, and unresolved obligations for destination-owner classification; mutate nothing.

Integrity is derived on every Orient: `verified` when representation and tracker state satisfy current contracts; `repairable-drift` when accepted evidence dictates one consequence-only correction; otherwise `incompatible` with its exact owner or setup precondition.

## State Authority

This table alone selects the next operation.

| Current evidence | Integrity | Additional predicate | Operation or return | Claim purpose |
| --- | --- | --- | --- | --- |
| Zero maps | N/A | Qualification and Admission pass; packet approved; final lookup remains zero | [Chart](OPERATIONS.md#qualification-and-chart) | None after read-back |
| Several plausible maps | N/A | Identity remains ambiguous | Return incompatible identity packet | None |
| `open` + `active` | `verified` | Frontier exists and budgets remain | [Advance](OPERATIONS.md#advance) | Advance + selected ticket |
| `open` + `active` | `verified` | No unresolved obligation, wait, contradiction, blocker, or budget decision remains | [Closeout](OPERATIONS.md#closeout) | Gap mutation or Seal only |
| Open | `repairable-drift` | Every correction is consequence-only | [Maintain](OPERATIONS.md#maintain) | Maintain |
| `open` + `waiting` | `verified` | Recorded trigger is satisfied | [Resume](OPERATIONS.md#resume) Wake | Resume |
| `open` + `waiting` | `verified` | Trigger remains pending | Return waiting | None |
| `open` + `blocked` | `verified` | Recorded intervention is satisfied inside scope and budget | [Resume](OPERATIONS.md#resume) Recover | Resume |
| `open` + `blocked` | `verified` | Intervention remains unsatisfied or exhaustion requires a successor | Return blocker | None |
| Open | `incompatible` | Exact owner or setup precondition is known | Return incompatibility | None |
| Open | `verified` | Terminal evidence exists and destination owner confirms | [Terminate](OPERATIONS.md#terminate) | Terminate |
| `closed` + `delivered` | `verified` | No qualifying To Spec gap | Return immutable closure | None |
| `closed` + `delivered` | `verified` | Approved in-scope correction packet or amendment fits capacity | [Reopen](OPERATIONS.md#reopen) | Reopen |
| `closed` + `superseded` | Any | Successor pointer resolves | Return immutable record and successor | None |
| `closed` + `cancelled` or `out-of-scope` | Any | None | Return immutable terminal record | None |
| Closed | `repairable-drift` or `incompatible` | Representation differs from historical contract | Return migration or Repo Bootstrap precondition | None |

Only `open` + `active|waiting|blocked` and `closed` + `delivered|superseded|cancelled|out-of-scope` are legal lifecycle/disposition pairs. Closed semantic history is immutable except through bounded delivered-map Reopen.

## Completion Authority

This table alone closes a selected operation. Branch files perform the work but cannot weaken these conditions.

| Operation | Complete when | Legal nonterminal return |
| --- | --- | --- |
| **Chart** | Pre-create identity remained zero; exactly the new map became canonical; approved map and graph read back; initial frontier or wait is visible; no outcome or claim remains | Existing, ambiguous, different, or unreadable identity; created-map recovery packet |
| **Orient** | Fresh identity, representation, state, claims, counters, edges, and provider evidence derive one integrity result and one permitted operation or return | Ambiguity, incompatibility, terminal state, pending wait, blocker, setup precondition, or missing authority |
| **Advance** | One ticket has one substantive outcome, or one Questionnaire ticket has a verified external-wait packet with its reservation preserved; direct consequences, counters, claim absence, and next state read back | Questionnaire wait; transient incomplete attempt with recovery evidence and unchanged outcome and counters |
| **Maintain** | Every evidence-determined repair reads back; meaning and ticket outcomes remain unchanged; claim absence and state read back | Incompatible decision, scope, provider, or nondeterministic-repair packet |
| **Resume** | One satisfied trigger or intervention and direct consequences read back; net growth reconciles; no ticket outcome changed; claim absence and state read back | Unsatisfied condition, scope change, exhaustion, or incompatible packet |
| **Closeout** | Gather is complete; Coherence and Durability pass; Seal proves unchanged declared fields; packet, delivered close, revisions, and claim absence read back; To Spec is recommended | Typed gap, blocker, approval wait, amendment or successor need, recovery packet, or semantic-change reorientation |
| **Terminate** | Owner confirmation, terminal evidence, budgets, unresolved obligations, closed state, and claim absence read back | Missing confirmation or incompatible terminal evidence with open state unchanged |
| **Reopen** | Prior generations remain immutable; approved evidence, budget, and frontier read back; state is `open` + `active`; claim absence and next operation are visible | Judgment, amendment, capacity, successor, or recovery packet |

## Mutation Envelope

Every mutation uses one envelope:

1. Verify the selected transition, operation authority, capacity, and absence of another campaign claim.
2. Acquire the mapped exclusive guard against the captured revision, then persist and read back one map-scoped claim containing actor, token, timestamp, operation, and selected ticket only for Advance.
3. Perform only the selected operation and apply Graph Growth when obligations change.
4. **Reconcile** every affected artifact, relationship, state, counter, evidence pointer, and provider revision; read them back.
5. Release the claim, read back its absence, and Orient from fresh state. Return after every operation. The sole same-invocation continuation is from a completed Advance into Closeout when that fresh Orient selects Closeout; never start a second resolver or Advance.

Generate `codex/<lowercase UUIDv4>` claim tokens and UTC timestamps. A configured acquisition must fail when another actor wins or the captured revision changes; ordinary last-write-wins mutation followed by read-back is not acquisition. Elapsed time alone never makes a claim stale. Takeover requires recorded prior evidence, reason, and destination-owner or provider-administrator authority before replacement.

External waits retain no claim. A failed acquisition, mutation, read-back, or release returns applied operations, failed operations, current claim evidence, and the safest mapped recovery action. Never remove a foreign claim without recorded takeover authority. Release removes the guard and claim representation, then proves their absence.

Tracker assignment may transport the campaign claim, but it never grants destination, decision, expansion, or termination authority.

An authority-transfer request is not Maintain. Keep or return the map blocked until explicit outgoing and incoming authority, or tracker-governed higher authority, is observable. Resume: Recover owns the later consequence-only authority-packet update and frontier restoration.

## Budget Authority

- The initial outcome total is one unit per initial ticket plus at most one explicitly justified named contingency. Each unresolved ticket reserves one unit; a substantive `Resolved`, `Blocked`, or `Out Of Scope` outcome converts that reservation to used.
- A Questionnaire wait preserves its reservation and leaves used unchanged. A transient incomplete attempt, Maintain, Resume, and read-only Closeout work consume no outcome or correction unit.
- Expansion charges only a net-new direct-consequence obligation. One-for-one replacement transfers the existing reservation. No hidden reserve or private branch allowance exists.
- `Blocked` is substantive only when it records one durable exact intervention or external prerequisite; transient failures leave the outcome and counters unchanged.
- The first approved correction packet fixes one cumulative correction budget for every later Reopen generation of that delivered map: one unit per first-graph ticket plus at most one explicitly justified named contingency. Each unresolved correction ticket reserves one unit and its substantive outcome converts that reservation to used. A later approved amendment may reserve only uncommitted named contingency; it cannot reset, replenish, replace, or add a second counter.

## Graph Growth

| Campaign state | Net-new obligation | Existing or zero-growth obligation | Missing authority |
| --- | --- | --- | --- |
| Original campaign | Remaining expansion budget plus one uncommitted outcome unit | Reopen without charge; one-for-one replacement transfers its reservation | Return capacity or successor blocker |
| Correction generation | Approved cohesive amendment plus one uncommitted correction unit | Reopen without charge | Return amendment or successor blocker |
| Consequence-only change | Not applicable | Repair representation without increasing obligations | Return incompatible when judgment would change |

Each new obligation records its source outcome, destination impact, in-scope reason, budget effect, and blocking relationship. No operation has a private expansion exception. Exhaustion with unresolved obligations records `open` + `blocked`, resolved and unresolved obligations, why the approved graph underestimated the route, and the exact destination-owner successor decision; it never silently extends the campaign.

## Reconcile

Account for direct consequences without resolving a second ticket. Give each affected fog item exactly one disposition:

- **Retain:** preserve the valid tether and state the remaining uncertainty.
- **Graduate:** create and wire finite sharp tickets under Graph Growth, then remove the fog item.
- **Resolve:** remove it after a linked resolution represents its answer.
- **Exclude:** remove it and add the governing scope pointer to Out Of Scope.

Persist the resulting frontier, wait, blocker, or closeout readiness under the current claim before release.

## Return

Return:

```text
Map:
Operation:
Observed state and derived integrity:
Destination authority and identity status, including Chart pre-create and post-create reads when applicable:
Operation result:
Linked evidence and direct map changes:
Claim acquisition, transition, release, and absence:
Outcome budget total, reserved, used, and uncommitted; expansion used and remaining:
Correction budget total, reserved, used, and uncommitted; closure generation, when applicable:
Closure revisions: Gather | pre-Seal | post-close | post-release, when applicable:
Next frontier | waiting trigger | blocker | terminal record | To Spec route:
Next permitted operation:
```

An incomplete attempt also returns recovery evidence and unchanged outcome and counters. Name the first frontier ticket when one remains, then stop. Every invoked resolver returns to its ticket; it never selects the next graph action. A recommendation starts no explicit-only skill automatically.

## Completion

One invocation completes only under the selected operation's completion row or legal nonterminal return, with required read-back and no retained claim. The campaign completes successfully only as `closed` + `delivered` with a sealed closure packet and To Spec recommendation; unsuccessful completion uses a destination-owner-confirmed terminal disposition. Waiting and blocked maps remain open.
