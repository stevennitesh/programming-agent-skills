---
name: wayfinder
description: Resolve one bounded, interdependent foggy effort through a tracker-backed decision map, then return a coherent settled source or terminal decision.
---

# Wayfinder

Turn one finite, foggy, multi-session effort into a settled source or terminal
decision. Own its map, routing, reconciliation, and closure; tickets answer
questions and prerequisites but never deliver the destination.

## Model

- **Destination:** owner, outcome, scope, exclusions, route-closing condition,
  terminal kind, and return owner.
- **Map:** orientation index; tickets own detail.
- **Frontier:** open, unblocked, unclaimed tickets in map order.
- **Fog:** in-scope uncertainty without a sharp question. Keep it in
  `Not Yet Specified`; ticket every sharp question, even when blocked.

Use linked titles for people; ids are for tracker operations.

## Authority

Choose Chart, Advance, or Maintain. Closure is their terminal gate.

Before mutation, load the tracker `Wayfinding representation` and, when hosted
labels apply, `Wayfinding Labels`. Freeze parent/child and dependency modes.
Require inspect, create, update, link, close, read-back, release, and exclusive
claim routes. Acquisition must be revision-conditional or an exclusive lock
with an observable losing-race result. Missing setup recommends
`$repo-bootstrap` and stops before mutation. Tracker docs own representation;
Wayfinder owns meaning and workflow.

For each invocation generate fresh `codex/<lowercase UUIDv4>` and
`<YYYY-MM-DDTHH:MM:SSZ>` claim values. Reuse them for its ticket and map, never
across invocations. A different token owns an item even for the same actor.
Elapsed time alone never makes a claim stale.
Replace another token only with explicit approval from an affirmed destination
owner or provider administrator. First record its token, claimed-at value, approver
authority, and reason; then read back the replacement.

Every mutation follows: claim, refresh, authorized change, **Mutation read-back**,
release, then verify its absence. Refresh before retrying an indeterminate result;
report verified, failed, and unknown effects. Unverified is incomplete.
Initial map creation is the exception: approve its exact title, create only that
map, repeat the identity search, then claim the sole canonical match before any
further mutation.

## Tickets

Every ticket locks type, participation, resolution owner, resolver, expected
return, and `$wayfinder` re-entry:

| Type | Participation and resolver |
| --- | --- |
| Research | AFK; `$research` with one approved note path. |
| Prototype | HITL or AFK; `$prototype` with decision owner, claim level, judgment mode, and human judge or objective verdict criteria. |
| Diagnosis | AFK; return `diagnosis-required` with evidence, environment, state, authorities, and Wayfinder as return owner; record Waiting and stop. |
| Grilling | HITL; `$grilling` for a conversation-only decision owned by the current user, or `$grill-with-docs` when durable domain material may change. Pass decision and return owners, context action, and separate ADR action. |
| Task | AFK when contracts and objective proof settle it; HITL for human action. |

Prototype `shape/feel` uses HITL, human judgment, and a named judge. `design evidence`
defaults to AFK/rule-based; use HITL only for a named human verdict owner.

For one asynchronous stakeholder, prepare `$to-questionnaire`'s exact packet,
including `Delivery: not performed`. Invoke only after explicit approval of that
packet; otherwise return it and stop before artifact mutation.

Resolvers return evidence; Wayfinder records `resolved`, `blocked`, `waiting`,
or `out of scope`. `Questionnaire ready` is Waiting, never an answer; only
matching attributable evidence resolves it. Missing resolver approval is
`incomplete`: release the claim and make no shared mutation. Classify by
resolution authority; split independently resolvable facts from human choices.

## Chart

Use Chart when a loose idea has no map.

1. **Bound.** Lock the destination. Resolve a material conversational gap;
   otherwise stop on a missing bound.
2. **Admit.** Search the exact destination tuple. Return one match; stop on
   conflicts. Admit only several interdependent decisions or prerequisites, a
   non-conversational resolver, and multi-session tracker sequencing. Otherwise
   return `not-needed`; recommend `$to-spec` only for an existing settled source.
3. **Sweep.** Surface decisions breadth-first: one ticket per sharp question,
   only unaskable uncertainty as fog.
4. **Approve.** Show one [MAP-FORMAT.md](MAP-FORMAT.md)-conforming packet:
   destination, map title, ordered tickets and fields, fog, scope, edges. Reject
   invalid Prototype fields. Require explicit approval, and fresh approval after
   change.
5. **Chart.** Refresh identity/capability; create only the map; repeat the
   destination search. Continue only for the sole canonical match, acquire its
   exclusive claim, create children in order, read back identities, then wire
   from those identities.
6. **Verify.** Read back the map, children, order, fields, edges, and frontier.
   Complete only when every sharp question is ticketed, every known edge wired,
   remaining fog unaskable, and no outcome recorded.

## Advance

Use Advance for one outcome on an existing map.

1. **Orient.** Load headers; zoom only as needed.
2. **Select.** Accept a named frontier ticket or Waiting ticket with attributable
   evidence matching its trigger. Otherwise show state/frontier and stop.
   Without a selection choose the frontier head.
3. **Claim.** Refresh and exclusively claim the ticket. Continue only after its
   owner, token, and claimed-at value read back exactly.
4. **Resolve.** Run its resolver or validate a Waiting return. Classify one
   answer, blocker, external wait, or out-of-scope reason.
5. **Reconcile.** Before outcome or shared mutation, claim the map with the
   same token; refresh map/ticket and require compatible state. Record the
   outcome; disposition each affected fog item once: **retain**, **graduate**
   by create-read-back-wire, **resolve** through a linked answer, or **exclude**
   with a governing pointer. Make only consequence-supported changes.
6. **Verify.** Read back outcome, pointers, edges, fog, frontier, and claims.
   On map-acquisition or compatibility failure, record no outcome or shared
   mutation; release the ticket and return its evidence with the conflict.
7. **Expose.** Release and verify the ticket claim. If Closure is eligible, run
   it while holding the map claim. Otherwise release and verify the map claim,
   then return the frontier, wait, or blocker.

Complete after one outcome or verified Waiting state, consequence read-back,
and no retained claim.

## Maintain

Use Maintain only for representation drift whose repair needs no new answer.

1. **Orient.** Read the format, tracker contract, map, and affected tickets.
2. **Bound.** Limit repair to evidenced sections, fog, pointers, scope,
   dependencies, or claim metadata. If an answer is needed, expose the frontier
   and stop.
3. **Approve.** Show the exact delta, evidence per change, and resulting
   frontier or closure state. Obtain explicit approval; changed content needs
   fresh approval.
4. **Claim.** Refresh and exclusively claim the map; require exact claim
   read-back.
5. **Repair.** Apply only the approved delta, give affected fog one
   disposition, and record no ticket outcome.
6. **Verify.** Read back affected state, claim, and frontier.
7. **Expose.** Run Closure while holding the map claim when eligible; otherwise
   release and verify it, then return the frontier.

Complete with no substantive ticket outcome, verified repair, no retained
claim, and the frontier or closing route visible.

## Closure

Close only while holding the map claim, after reaching the terminal kind, with
no unresolved ticket, Waiting state, blocker, or in-scope fog.

For an unaccounted durable-language or ADR consequence, invoke
`$domain-modeling` once. Use
`persist authorized` only with exact domain-write authority and `render only`
otherwise. Use `offer only` for ADRs absent separate explicit approval. A
material Domain Delta blocker leaves the map open.

Build the closing packet defined in [MAP-FORMAT.md](MAP-FORMAT.md). While
holding the map claim, post it, close the map, read back its closed state and
empty frontier, release the claim, and read back claim absence.

Return a terminal decision and stop. For a settled parent-spec source,
recommend `$to-spec` and stop. Never route a closed map directly to
`$to-tickets`, `$implement`, or `$parallel-implement`.

## Return

Return applicable status (`charted | advanced | maintained | waiting | blocked |
not-needed | closed | incomplete`), map/operation, destination, ticket/outcome,
evidence/changes, `Domain Delta: <intact packet or not applicable>`, claim
release/conflict, next route, and at most one uninvoked suggested owner.

When a frontier remains, end with `Next frontier: [<ticket title>](<link>).
Invoke $wayfinder to advance it.`
