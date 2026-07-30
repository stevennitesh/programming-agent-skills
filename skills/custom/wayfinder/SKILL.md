---
name: wayfinder
description: Resolve one bounded, interdependent foggy effort through a tracker-backed decision map, then return a coherent settled source or terminal decision.
---

# Wayfinder

Wayfinder owns one finite route from bounded fog to a coherent settled source
or terminal decision. It owns the map, ticket classification, selected resolver
call, result reconciliation, and closing source packet. Tickets resolve
decisions and prerequisites; they do not deliver the destination.

## Navigation Model

- **Destination** - the owner, outcome, scope, route-closing condition, terminal
  kind, and return owner that fix the route.
- **Map** - an orientation index. Tickets own questions, resolutions, and
  assets.
- **Frontier** - open, unblocked, unclaimed child tickets in map order.
- **Fog of war** - in-scope uncertainty whose question is not yet sharp. Keep
  it under `Not Yet Specified`; graduate it when the question becomes sharp.
- **Claim** - the tracker-recorded invocation identity and concurrency guard.
- **Name** - use linked titles in human-facing text; reserve ids for tracker
  operations and dependency wiring.

Ticket a precise question even when blocked. Keep uncertainty as fog while the
question itself remains unclear.

Before tracker mutation, read `docs/agents/issue-tracker.md`, section
`Wayfinding operations`. Freeze the configured parent/child and dependency
modes, and verify their inspect, create, update, link, claim, and read-back
routes. If the document or a required route is missing, recommend
`$repo-bootstrap` and stop. The tracker owns provider mechanics; Wayfinder owns
map semantics.

## Tickets

Every ticket locks one type, participation mode, resolution owner, resolver,
expected return, and `$wayfinder` as re-entry owner:

- **Research - AFK:** Invoke `$research` with one approved note path. Expect its
  cited answer or truthful evidence boundary.
- **Prototype - HITL or AFK:** Invoke `$prototype` with the decision owner,
  claim level, judgment mode, and human judge or objective verdict criteria.
  Expect its supported answer or truthful residual, supported decision
  implications, evidence, limits, and cleanup state.
- **Diagnosis - AFK:** Return `diagnosis-required` with the facts, evidence,
  environment, exact ticket state, authorities, and Wayfinder as Return owner.
  Record the ticket as Waiting and stop.
- **Grilling - HITL:** Invoke `$grilling` when the current user owns a
  conversation-only decision. Invoke `$grill-with-docs` when the decision may
  change durable domain terms, Invariants, Context Relationships, or an ADR.
  Pass the user as decision owner, the return owner, context action, and
  separate ADR action. Expect the intact Grilling packet and, when applicable,
  Domain Delta.
- **Task - AFK or HITL:** Use AFK when repository contracts and objective proof
  determine the answer. Use HITL only for live human action. When one
  identifiable external stakeholder must answer asynchronously, prepare an
  exact `$to-questionnaire` packet containing recipient, downstream decision,
  origin and return owner, needed-back items, sensitivity, effort, authorized
  path and durability, overwrite authority, and `Delivery: not performed`.
  Invoke `$to-questionnaire` only after the user explicitly approves that exact
  packet. Otherwise return it, recommend explicit `$to-questionnaire`, and stop
  before artifact mutation.

The resolver returns evidence; Wayfinder alone classifies and records the map
outcome. `Questionnaire ready` is `Waiting`, never an answer. Only attributable
answers can resolve its ticket. Missing resolver-specific approval is
`incomplete`, not Waiting: release any ticket claim and record no outcome or
shared mutation.

Classify by resolution authority, not wording. Split independently resolvable
facts and material human-owned choices.

For Prototype tickets:

- `shape/feel` uses HITL, human judgment, and a named human judge.
- `design evidence` uses AFK and rule-based judgment by default.
- `design evidence` uses HITL only when the caller reserves the verdict for a
  named human.

## Modes

Choose exactly one mode per invocation: Chart, Advance, or Maintain. Closure is
the terminal gate of Advance or Maintain.

### Chart

Use Chart for a loose idea without a map.

1. **Bound.** Trace the caller packet. Lock destination owner, outcome, scope,
   exclusions, route-closing condition, terminal kind, and return owner. Invoke
   the applicable conversational resolver only when a material bound decision
   remains unsettled. A missing required bound stops Chart.
2. **Admit.** Search for the exact destination tuple. One matching map returns
   its current state and stops; several conflicting maps stop without mutation.
   Admit a new map only for a bounded destination with several interdependent
   material decisions or prerequisites, at least one non-conversational
   resolver, and tracker-backed multi-session sequencing. Otherwise return
   `Wayfinding not needed` without mutation; recommend `$to-spec` only when the
   source is already ready.
3. **Sweep.** Surface material decisions breadth-first. Defer each sharp
   question to one named ticket; keep unaskable uncertainty as fog.
4. **Approve.** Read [MAP-FORMAT.md](MAP-FORMAT.md), then show one complete
   mutation packet: destination, map title, ordered children, questions, types,
   participation, resolution owners, resolvers, expected returns, approved
   research paths, fog, scope, and blocking edges. Include Prototype judgment
   fields: decision owner, claim level, judgment mode, and human judge or
   objective verdict criteria. Reject incompatible Prototype fields. Obtain
   explicit approval; any changed packet requires fresh approval.
5. **Chart.** Refresh tracker identity and capability. Create the map, create
   no children, then repeat the destination-tuple search. Continue only when
   the new map is the sole canonical match. Create children in approved order,
   read back their exact identities, then wire blocking edges from those
   verified identities.
6. **Verify.** Apply the tracker's **Mutation read-back** rule to the map,
   children, order, fields, and edges.

Chart completes with `not-needed`, or with every sharp question ticketed, known
edges wired, remaining fog unaskable, and zero ticket outcomes.

### Advance

Use Advance when a map exists and one frontier ticket needs an outcome.

1. **Orient.** Load map and ticket headers at low resolution; load full bodies
   only as needed. Read [MAP-FORMAT.md](MAP-FORMAT.md) when the outcome may
   change map sections.
2. **Select.** Use a named ticket when it is on the frontier, or when it is
   Waiting and the supplied attributable evidence matches its exact return
   trigger. Otherwise report its state and the frontier, then stop. Without a
   selection, take the first frontier ticket.
3. **Claim.** Refresh and claim the selected ticket with this invocation's
   token. Continue only after its exact owner, token, and claimed-at value read
   back.
4. **Resolve.** Invoke the locked resolver, or validate the supplied return for
   a selected Waiting ticket, then classify exactly one result:
   - **Resolved:** supported answer.
   - **Blocked:** exact unmet prerequisite or evidence boundary.
   - **Waiting:** exact external return trigger, return owner, and any artifact
     pointer and durability.
   - **Out of scope:** reason the question lies beyond the destination.
5. **Reconcile.** Before any ticket outcome, edge, or map mutation, claim the
   map with the same invocation token; refresh both items and continue only if
   their states remain compatible. While holding the map claim, apply the
   outcome and give each affected fog item exactly one disposition:
   - **Retain:** keep the remaining uncertainty.
   - **Graduate:** create, read back, then wire one sharp ticket.
   - **Resolve:** remove after a linked resolution represents its answer.
   - **Exclude:** remove and add its governing pointer to `Out Of Scope`.
   Create-then-wire newly visible tickets, update affected dependencies, and
   make only consequence-supported state changes to other tickets.
6. **Verify.** Read back the selected outcome, map pointers, changed edges,
   fog dispositions, resulting frontier, and both claim identities. If map
   claim acquisition or compatibility fails, record no outcome or shared
   mutation; release the ticket claim and return resolver evidence plus the
   conflict.
7. **Expose.** Release the ticket claim and read back its absence. Run
   **Closure** while the map claim is still held when its gate applies.
   Otherwise release the map claim, read back its absence, and show the
   frontier, wait, or blocker.

Advance completes after one substantive outcome or one verified Waiting state,
its direct consequences read back, and no claim retained.

### Maintain

Use Maintain only when representation has drifted and no question needs an
answer to determine the repair.

1. **Orient.** Read [MAP-FORMAT.md](MAP-FORMAT.md), the tracker contract, the
   map, and only affected tickets.
2. **Bound.** Admit only consequence-supported cleanup of canonical sections,
   stale fog, pointers, scope indexes, dependencies, or claim metadata. If an
   answer is required, expose the frontier and stop.
3. **Approve.** Show the exact delta, evidence for every change, and resulting
   frontier or closure state. Obtain explicit approval; any changed packet
   requires fresh approval.
4. **Claim.** Refresh and claim the map. Continue only after the exact token and
   claimed-at value read back.
5. **Repair.** Apply only the approved changes. Give affected fog one
   disposition. Record no child outcome.
6. **Verify.** Read back the map, affected tickets, pointers, headings, claim,
   and frontier.
7. **Expose.** Run **Closure** while the map claim is held when eligible;
   otherwise release it, read back its absence, and return the frontier.

Maintain completes with zero substantive ticket outcomes, every approved repair
read back, no retained claim, and the frontier or closing route visible.

## Closure

Close only while holding the map claim and only when no unresolved child,
Waiting state, blocker, or in-scope fog remains and the destination's terminal
kind is reached.

If the settled result changes durable domain language or warrants ADR
assessment and no current Domain Delta accounts for it, invoke
`$domain-modeling` once with the settled decision and return owner. Use
`persist authorized` only with exact domain-write authority and `render only`
otherwise. Use `offer only` for ADRs unless an identified candidate has separate
explicit approval. A material Domain Delta blocker leaves the map open.

Build one compact closing packet containing map identity and source owner;
destination, bound, route-closing condition, terminal kind, and return owner;
decisive resolution links and owners; evidence; exclusions, deferrals, and
residual uncertainty; proof or acceptance objectives; and any Domain Delta.
Apply the tracker's **Complete map** and **Mutation read-back** conventions,
then release the map claim and read back its absence.

- For a terminal decision, report the decision and stop.
- For a settled parent-spec source, recommend `$to-spec` and stop.

Never route a closed map directly to `$to-tickets`, `$implement`, or
`$parallel-implement`.

## Return

Return only applicable fields:

```text
Status: charted | advanced | maintained | waiting | blocked | not-needed | closed | incomplete
Map: <link or none>
Operation: <Chart | Advance | Maintain | Closure>
Destination: <owner, outcome, scope, closing condition, terminal kind, return owner>
Selected ticket: <link or none>
Outcome: <resolved | blocked | waiting | out of scope | none>
Evidence and direct changes: <links and concise summary>
Domain Delta: <intact packet or not applicable>
Claims: <verified release or exact conflict>
Next: <frontier, wait trigger, blocker, or closing route>
Suggested owner: <one uninvoked skill or user action, or none>
```

When a frontier remains, end with `Next frontier: [<ticket title>](<link>).
Invoke $wayfinder to advance it.`
