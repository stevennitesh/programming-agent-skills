---
name: wayfinder
description: Resolve one bounded, interdependent foggy effort through a tracker-backed decision map, then return a coherent settled source or terminal decision.
---

# Wayfinder

Resolve one finite, foggy, multi-session effort. Own its map, resolver routing,
reconciliation, and terminal packet. Tickets answer questions and prerequisites;
they never deliver the destination.

## Model

- **Destination:** owner, outcome, scope, exclusions, route-closing condition,
  terminal kind, and return owner.
- **Map:** orientation index; tickets own detail.
- **Frontier:** `Pending`, dependency-unblocked, unclaimed tickets in map order;
  Waiting and Blocked enter only through their evidence-qualified Orient rows.
- **Fog:** one in-scope uncertainty without a sharp question, tethered to a
  finite sharpening source, owner, trigger, and fallback.
- **Operation result:** what this invocation accomplished.
- **Map condition:** `active | waiting | blocked | closeable | closed`.

Use linked titles for people; use provider IDs only for tracker operations.
Keep every sharp question in a ticket, even when blocked.

## Orient

Load the tracker `Wayfinding representation` and, when hosted labels apply,
`Wayfinding Labels`. Freeze its parent/child and dependency modes. Require
inspect, create, update, link, close, read-back, release, and an exclusive claim
route with an observable losing-race result. Missing or incompatible setup
recommends `$repo-bootstrap` and stops before mutation.

Search open and closed maps for the exact destination tuple. One open match
supplies current state; several open matches return the identity conflict. With
no open match, select exactly one branch: a successor may enter Chart only with
one explicitly selected closed predecessor, one material new gap, explicit
imports, and zero maps matching the destination tuple plus predecessor; one
explicitly selected closed match returns its immutable packet; zero closed
matches may enter initial Chart. Any other ambiguity returns without mutation.
For one map derive:

- **Integrity:** `verified`, `repairable-drift` when accepted evidence permits
  exactly one consequence-only correction, or `incompatible` otherwise.
- **Condition:** use this precedence.

| Evidence | Next operation or return |
| --- | --- |
| Map is closed | Return its immutable closing packet. |
| Integrity is incompatible | Return the exact owner or setup precondition. |
| Integrity is repairable-drift | Maintain. |
| Destination owner confirms cancellation, supersession, or out-of-scope termination | Terminate. |
| A frontier ticket exists | Advance. |
| A Waiting or Blocked ticket has evidence that can answer it | Advance that ticket. |
| A recorded trigger or intervention changes only readiness or fog sharpness | Maintain. |
| Unresolved external triggers remain | Return `waiting` with their owners and required evidence. |
| An authority, capability, growth, or prerequisite blocker remains | Return `blocked` with its intervention. |
| No unresolved ticket, fog, wait, or blocker remains and cited evidence satisfies the route-closing condition | Closure. |
| None applies | Return `incomplete` with the state gap. |

Run exactly one selected operation and return its verified result. A later
invocation re-orients from read-back state and may independently select Closure.

## Mutation Gate

For each invocation generate fresh `codex/<lowercase UUIDv4>` and
`<YYYY-MM-DDTHH:MM:SSZ>` claim values. Reuse them for its ticket and map, never
across invocations. A different token owns an item even for the same actor;
elapsed time alone never makes a claim stale. Replace another token only with
explicit approval from an affirmed destination owner or provider administrator,
after recording the old claim, approver authority, and reason.

**Mutation read-back.** Every mutation follows: verify authority and captured state; acquire and read
back the required claim; refresh; apply only the selected change; read back all
direct effects and frontier; release; verify claim absence; Orient. Refresh an
indeterminate result before any retry. Unverified effects return `incomplete`
with verified, failed, and unknown state.

Chart is the only pre-claim exception: approve the exact packet, confirm zero
matches for its initial or successor identity, create only the map, repeat
identity search, then claim the sole created canonical map before children or
edges.

Advance freezes the map identity and open state, selected ticket contract and
claim, dependency identities, and frontier eligibility before resolver work.
After acquiring the map claim, require those fields unchanged except for this
invocation's ticket claim. Drift records no tracker outcome or map mutation;
release both claims and verify their absence, preserve and report resolver
evidence and effects within the frozen mutation boundary, and return the
conflict.

## Resolver Gate

Each ticket locks one type, participation, resolution owner, resolver, expected
return, mutation boundary, and `$wayfinder` re-entry:

| Type | Participation and resolver |
| --- | --- |
| Research | AFK; `$research` with the question, supported map use, scope, exact state, Source Trace, approved note path and write mode, and Wayfinder return owner. |
| Prototype | HITL or AFK; `$prototype` with [MAP-FORMAT.md](MAP-FORMAT.md)'s complete Prototype packet. |
| Diagnosis | AFK after explicit separate start; return `diagnosis-required` with evidence, environment, exact state, authorities, and Wayfinder as return owner. |
| Grilling | HITL; `$grilling` for a conversation-only user decision, or `$grill-with-docs` while durable domain capture remains active. |
| Questionnaire | External; `$to-questionnaire` only after the user approves its exact caller packet and `Delivery: not performed`. |
| Task | AFK for one bounded objectively provable repository or operational fact; HITL only for required live human action; no durable mutation. |

Prototype `shape/feel` uses HITL, human judgment, and a named judge. Objective
`design evidence` defaults to AFK/rule-based; a named human verdict owner makes
it HITL.

Wayfinder normalizes the intact resolver Return; it never copies callee status
labels blindly:

| Return evidence | Map effect |
| --- | --- |
| Supported answer, confirmed decision, or objective verdict | `resolved` |
| Intact Research `conflicted` | `blocked` with the conflict owner and one observable intervention; never `resolved` or generic `incomplete` |
| Verified questionnaire artifact, human verdict wait, or `diagnosis-required` | `waiting` with owner, trigger, and required evidence |
| Advance receives nested Grilling `Route gap` | Keep the ticket blocked on the admitted replacement graph; never recommend Wayfinder to itself |
| Chart receives a Grilling decision or `Route gap` | Treat it as claim-free proposed Chart input; record no ticket outcome or map mutation, and require exact approval of the resulting packet |
| Exact evidence, authority, setup, or prerequisite gap | `blocked` with one intervention |
| Governing evidence places the question outside the destination | `out of scope` |
| Missing approval, malformed or mismatched return, transport failure, or callee non-admission | `incomplete`; release claims, record no tracker outcome or map mutation, and report any frozen-boundary resolver effects |

`Questionnaire ready` is Waiting, never an answer. Only matching attributable
answers can resolve it. Without exact questionnaire approval, return the packet
and `approve, then re-enter Wayfinder Advance`; do not invoke the callee or
mutate shared state.

## Reconcile

Record one normalized result and only its direct consequences. Give each
affected fog item one disposition: **retain** with its tether, **graduate** into
one or more sharp tickets, **resolve** through linked evidence, or **exclude**
with a governing pointer.

Chart freezes one destination-owner-approved post-Chart ticket allowance,
defaulting to the number of initial fog items. Every later ticket creation
consumes one; other state changes consume none. Add only in-scope obligations
caused by accepted evidence. Exhaustion, destination change, or unsupported
growth returns `blocked` for a new finite approval, Terminate, or successor.
Never invoke another resolver while reconciling.

## Chart

Use only after Orient admits a zero-match initial or successor identity.

1. **Bound.** Lock the destination. Resolve one material conversational gap;
   otherwise stop on a missing bound.
2. **Admit.** Require several interdependent material decisions or
   prerequisites, a non-conversational resolver, tracker-backed multi-session
   sequencing, and finitely tethered fog. Otherwise return `not-needed`;
   recommend `$implement` for one settled bounded implementation or `$to-spec`
   only when a durable parent decision contract remains useful.
3. **Sweep.** Surface decisions breadth-first: one ticket per sharp question,
   only unsharp uncertainty as fog. Set the finite growth allowance.
4. **Approve.** Show one [MAP-FORMAT.md](MAP-FORMAT.md)-conforming packet with
   destination, exact map title, ordered tickets and resolver fields, fog,
   scope, edges, and allowance. Require explicit approval and fresh approval
   after any change.
5. **Create.** Apply the initial-map exception. Create children in approved
   order, read back identities, then wire edges from those identities.
6. **Verify.** Read back the entire graph, fields, allowance, fog tethers, and
   initial map condition.

Chart completes with `not-needed` or one canonical verified map, no ticket
outcome, no retained claim, and an `active | waiting | blocked` condition.

## Advance

Use for one frontier ticket or one Waiting or Blocked ticket whose supplied
evidence can answer its exact condition.

1. **Select.** Use the named eligible ticket or the frontier head. Otherwise
   return its state and the actual frontier.
2. **Claim.** Freeze the commit-point fields, exclusively claim the ticket, and
   require owner, token, and claimed-at read-back.
3. **Resolve.** Invoke its locked resolver or validate the attributable return.
   Missing explicit target approval returns `incomplete` before shared mutation.
4. **Commit.** Acquire the map claim with the same token, apply the commit-point
   comparison, normalize the Return, and Reconcile.
5. **Verify.** Read back outcome or wait, pointers, graph, fog, allowance,
   frontier, and claims; release both and Orient.

Advance completes after one resolver Return is either reconciled into one
outcome, one verified wait, or one bounded replacement graph, with no retained
claim.

## Maintain

Use only for one deterministic change requiring no resolver judgment or ticket
outcome: consequence-only representation repair, a proved wait or blocker
transition, or a fog trigger that now makes its question sharp.

1. **Bound.** Show the exact evidence, delta, fog dispositions, allowance use,
   and resulting condition. Obtain destination-owner approval only to increase
   the allowance or change the approved destination packet.
2. **Claim.** Refresh and exclusively claim the map; require exact read-back.
3. **Apply.** Make only the determined correction or liveness transition and
   Reconcile no substantive outcome.
4. **Verify.** Read back affected state, allowance, frontier, and claim absence;
   Orient.

Maintain completes with the selected deterministic delta verified, no ticket
outcome, no retained claim, and the resulting condition visible.

## Closure

Closure is independently selectable from `closeable` state.

1. **Gather.** Freeze the map, every ticket and resolver return, fog and scope
   disposition, Source Trace, growth calculation, route-closing evidence,
   terminal kind, and proof or acceptance objectives. Hold no claim.
2. **Coherence.** Require every obligation to have one disposition; every
   accepted result to agree with the destination, dependencies, contracts, and
   other decisions; and cited evidence to satisfy the route-closing condition.
   Return each newly sharp gap as exact Maintain input. Maintain creates and
   wires its ticket within the approved allowance; Orient then selects Advance.
   Exhausted allowance returns the approval blocker. Never close an empty but
   unsupported graph.
3. **Durability.** For an unaccounted durable-language or ADR consequence,
   invoke `$domain-modeling` once. Use `persist authorized` only with exact
   domain-write authority, `render only` otherwise, and `offer only` without
   separate ADR approval. A material blocker leaves the map open.
4. **Seal.** Build [MAP-FORMAT.md](MAP-FORMAT.md)'s closing packet. Acquire the
   map claim, refresh every Gather field, and stop on semantic drift. Otherwise
   post the packet, close as `delivered`, read back closed state and empty
   frontier, release, and prove claim absence.

Return the terminal decision and stop. Recommend `$implement` for one settled
bounded implementation whose acceptance and authority are complete. Recommend
`$to-spec` when the settled outcome still benefits from a durable parent
decision contract and several slices or durable coordination are plausible.
Never route directly to `$to-tickets` or `$parallel-implement`.

## Terminate

Use only with destination-owner confirmation and evidence for `cancelled`,
`superseded`, or `out of scope`. Capture unresolved obligations and the recovery
or successor boundary; acquire the map claim; post the terminal closing packet;
close; read back; release; prove claim absence; and stop. Do not run Closure,
Domain Modeling, or To Spec. Closed maps remain immutable.

## Return

Return only applicable fields:

```text
Operation result: oriented | charted | advanced | maintained | closed | terminated | not-needed | incomplete
Map condition: active | waiting | blocked | closeable | closed
Map and operation:
Destination and integrity:
Selected ticket and normalized outcome:
Evidence and direct changes:
Growth allowance: total | used | remaining
Domain Delta: <intact packet or not applicable>
Claims: <verified release or exact conflict>
Next admission: <frontier ticket | trigger | intervention | Closure | successor | none>
Suggested owner: <one uninvoked skill or user action, or none>
```

When a frontier remains, end with `Next frontier: [<ticket title>](<link>).
Invoke $wayfinder to advance it.`
