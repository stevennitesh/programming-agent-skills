---
name: wayfinder
description: Chart a tracker-backed route through a large, foggy effort, then advance one frontier ticket per session until the route to the destination is clear.
---

# Wayfinder

Wayfinder owns one outcome: a tracker-backed route from fog to a clear destination. Its tickets resolve decisions and prerequisites, not destination delivery.

## Navigation Model

- **Destination** — the decision, settled source, or ready slice that closes wayfinding. It fixes scope.
- **Map** — an index of orientation and context pointers. Tickets own questions, resolutions, and assets.
- **Frontier** — the open, unblocked, unclaimed child tickets in map order.
- **Fog of war** — in-scope uncertainty whose question is not yet sharp. Record it under `Not Yet Specified`; graduate it when the question becomes sharp.
- **Claim** — the tracker-recorded session identity and concurrency guard. Work starts after claim.
- **Name** — use linked map and ticket titles in human-facing text; reserve ids for tracker operations and dependency wiring.

**Fog or ticket?** Ticket a precise question even when blocked. Keep uncertainty as fog while the question itself remains unclear.

Before any tracker mutation, read `docs/agents/issue-tracker.md`, section `Wayfinding operations`. If it or a required operation is unavailable, recommend `$repo-bootstrap` and stop. The tracker document owns transport and state mechanics.

## Tickets

Every ticket declares one type and participation mode:

- **Research — AFK:** Invoke `$research` with one approved note path; return its cited note pointer.
- **Prototype — HITL or AFK:** Invoke `$prototype` when the question needs a runnable probe; pass its decision owner, claim level, judgment mode, and human judge when human, then return its supported result, evidence, limits, and cleanup state.
- **Grilling — HITL:** When the user owns one resolution, return the ticket bound and stop. Recommend explicit `$grilling` for a conversation-only preference or tradeoff; recommend explicit `$grill-with-docs` when the decision may change durable domain terms, Invariants, Context Relationships, or an ADR. Resume the ticket in a later Wayfinder invocation with the intact returned decision.
- **Task — AFK or HITL:** Use AFK when accepted repository contracts and objective proof determine the resolution; return the supported answer, affected boundary, and proof criteria. Use HITL only when completing the prerequisite requires live human action. When an identifiable external stakeholder must answer asynchronously, return the ticket bound, recommend explicit `$to-questionnaire`, and stop. Resume the same ticket with attributable answers.

A HITL ticket resolves only through live human participation. The ticket owns the question; its resolution owns the answer and linked assets.

Classify by resolution authority, not whether the ticket is phrased as a decision. Split a ticket when an independently decidable fact and a material human-owned choice can resolve separately.

For Prototype tickets, participation follows the locked judgment:

- `shape/feel` — HITL with judgment mode `human` and a human judge.
- `design evidence` — AFK with judgment mode `rule-based` and objective verdict criteria.
- `design evidence` — HITL with judgment mode `human` only when the caller explicitly reserves the verdict for a human.

## Modes

Choose exactly one mode per session: Chart, Advance, or Maintain. Closure is the terminal gate of Advance or Maintain, not another mode.

### Chart

Use Chart for a loose idea without a map.

1. **Bound.** Return a **charting bound** that settles only the destination, scope, and route-closing condition. Recommend explicit `$grilling` for a conversation-only decision, or `$grill-with-docs` when it may change durable domain terms, Invariants, Context Relationships, or an ADR, then stop. Resume Chart in a later Wayfinder invocation with the intact returned decision.
2. **Sweep.** Surface material decisions breadth-first. For each material decision: Defer it explicitly to a named Wayfinder ticket rather than resolving it during Chart.
3. **Gate.** If the route is already clear, name the closing route and stop without creating a map.
4. **Approve.** Show the destination, map title, child titles, questions, types, modes, approved research note paths, fog, scope boundary, and blocking edges as one mutation packet. For each Prototype ticket, also show its decision owner, claim level, judgment mode, and either the human judge or objective verdict criteria; reject a packet whose claim level, judgment, and mode disagree with the participation rule. Obtain explicit approval; any changed packet requires fresh approval.
5. **Chart.** Read [MAP-FORMAT.md](MAP-FORMAT.md), then create the map with destination, notes, empty resolution index, fog, and scope boundary.
6. **Wire.** Create every sharp child ticket before adding known blocking edges.
7. **Verify.** Apply the tracker's **Mutation read-back** rule to the map, children, and edges.

Chart completes when no map is needed and one closing route is named, or when every sharp question is ticketed, known edges are wired, remaining fog is not yet askable, and zero tickets have recorded outcomes.

### Advance

Use Advance when a map exists and one frontier ticket needs a substantive outcome. For representation-only drift with no question to answer, use Maintain instead.

1. **Orient.** Load the map and ticket headers at low resolution; load full bodies only as needed. Read [MAP-FORMAT.md](MAP-FORMAT.md) when the selected outcome may change map sections.
2. **Select.** Use a named ticket only when it is on the frontier; otherwise report its state, expose the frontier, and stop. Without a selection, take the first frontier ticket.
3. **Claim.** Refresh the ticket, record the current session's claim identity through the tracker convention, then apply **Mutation read-back before resolution work**. If the ticket changed, the exact session identity or claimed-at value is not verified, or another session owns it, refresh the frontier and stop.
4. **Resolve.** Follow the ticket's type and mode, then record exactly one outcome through the tracker convention:
   - **Resolved:** answer the question and add its context pointer to `Decisions So Far`.
   - **Blocked:** record the blocker; create-then-wire a sharp blocker or return an unaskable blocker to fog.
   - **Out of scope:** record why it lies beyond the destination and add its linked scope note to `Out Of Scope`.
5. **Reconcile.** Account for every fog item affected by the outcome exactly once:
   - **Retain:** keep it under `Not Yet Specified` with the remaining uncertainty stated.
   - **Graduate:** create-then-wire one sharp ticket, then remove the fog item.
   - **Resolve:** remove it after its answer is represented by a linked resolution.
   - **Exclude:** remove it and add the governing pointer defined by [MAP-FORMAT.md](MAP-FORMAT.md) to `Out Of Scope`.
   Then create-then-wire newly visible tickets, update affected dependencies, and mark obsolete tickets through consequence-only state changes without answering them.
6. **Verify.** Apply **Mutation read-back** to the selected ticket, claim, outcome, map pointers, changed edges, and resulting frontier.
7. **Expose.** Show the next frontier or run **Closure** below.

Preserve concurrent work. Touch only the selected ticket, directly affected edges, and map sections changed by its outcome.

Advance completes when exactly one selected ticket has a substantive outcome; every other ticket mutation is consequence-only; its claim and direct map consequences are reconciled; every affected fog item has exactly one disposition; and the next frontier or closing route is visible.

### Maintain

Use Maintain when an existing map's representation has drifted from the current map or tracker contract and no unresolved question needs answering. This specific predicate takes precedence over Advance.

1. **Orient.** Read [MAP-FORMAT.md](MAP-FORMAT.md) and the tracker contract; load the map and only affected tickets.
2. **Bound.** Admit only consequence-only repairs supported by existing resolutions or current contracts: canonical section cleanup, stale fog disposition, broken pointers, evidence-backed scope indexing, and dependency or claim metadata repair. If any answer or decision is required, expose the frontier and stop.
3. **Approve.** Show the exact map and ticket delta, evidence pointer for every change, and resulting frontier or closure state. Obtain explicit approval; any changed packet requires fresh approval.
4. **Claim.** Refresh and claim the map through the tracker convention. Continue only after the exact session token and claimed-at value read back.
5. **Repair.** Apply only the approved consequence-only changes. Give every affected fog item exactly one Advance disposition: Retain, Graduate, Resolve, or Exclude. Before removing it, verify its sharp ticket, linked resolution, or governing exclusion pointer is represented in the map. Record no child outcome.
6. **Verify.** Apply **Mutation read-back** to the map, affected tickets, pointers, canonical headings, claim, and resulting frontier.
7. **Expose.** Run **Closure** while the map claim is held when its conditions are satisfied; otherwise release the claim and return the frontier.

Maintain completes when zero frontier tickets have substantive outcomes, every approved consequence-only repair is applied and read back, the map claim is released, and the next frontier or closing route is visible.

## Closure

At the end of Advance or Maintain, close the map only when the destination is reached, no unresolved child or in-scope fog remains, and the next durable artifact or action is clear. If a settled closing decision changes durable domain language or warrants ADR assessment and no current Domain Delta already accounts for it, invoke `$domain-modeling` once with the settled decision and return owner. Use `persist authorized` only with exact domain-write authority; otherwise use `render only`. Record an ADR only with separate explicit approval; otherwise use `offer only`. Continue only when the returned Domain Delta accounts for the consequence; an exact blocker leaves the map open.

Apply the tracker's **Complete map** and **Mutation read-back** conventions; while maintaining, keep the map claim through close, release it only after the closed state reads back, then read back the absence of that claim. Closure completes only when the closing comment or state, claim release, resulting absence of an in-scope frontier, and any required Domain Delta are verified. Recommend exactly one route and stop:

- settled decision — report it;
- settled parent-spec source or a successfully delivered implementation map — `$to-spec`.

## Return

Return the map link when one exists, the Chart or Maintain result or selected ticket outcome, linked evidence, direct map changes, any Domain Delta produced during Closure, and the next frontier or closing route. When a frontier remains, end with `Next frontier: [<ticket title>](<link>). Invoke $wayfinder to advance it.` On closure, also return the destination and decisive resolutions.
