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
- **Claim** — the tracker-recorded concurrency guard. Work starts after claim.
- **Name** — use linked map and ticket titles in human-facing text; reserve ids for tracker operations and dependency wiring.

**Fog or ticket?** Ticket a precise question even when blocked. Keep uncertainty as fog while the question itself remains unclear.

Before any tracker mutation, read `docs/agents/issue-tracker.md`, section `Wayfinding operations`. If it or a required operation is unavailable, recommend `$repo-bootstrap` and stop. The tracker document owns transport and state mechanics.

## Tickets

Every ticket declares one type and participation mode:

- **Research — AFK:** Invoke `$research` with one approved note path; return its cited note pointer.
- **Prototype — HITL:** Invoke `$prototype` when the question needs a runnable artifact; return the artifact and verdict.
- **Grilling — HITL:** Invoke `$grill-with-docs`; return one decision. This is the default decision type.
- **Task — HITL or AFK:** Expose a prerequisite for a later decision; return changed facts or a precise human checklist.

A HITL ticket resolves only through live human participation. The ticket owns the question; its resolution owns the answer and linked assets.

## Modes

Choose exactly one mode per session.

### Chart

Use Chart for a loose idea without a map.

1. **Bound.** Invoke `$grill-with-docs` with a **charting bound**: settle only the destination, scope, and route-closing condition.
2. **Sweep.** Surface material decisions breadth-first. For each material decision: Defer it explicitly to a named Wayfinder ticket rather than resolving it during Chart.
3. **Gate.** If the route is already clear, name the closing route and stop without creating a map.
4. **Chart.** Read [MAP-FORMAT.md](MAP-FORMAT.md), then create the map with destination, notes, empty resolution index, fog, and scope boundary.
5. **Wire.** Create every sharp child ticket before adding known blocking edges.
6. **Verify.** Apply the tracker's **Mutation read-back** rule to the map, children, and edges.

Chart completes when no map is needed and one closing route is named, or when every sharp question is ticketed, known edges are wired, remaining fog is not yet askable, and zero tickets have recorded outcomes.

### Advance

Use Advance when a map exists.

1. **Orient.** Load the map and ticket headers at low resolution; load full bodies only as needed.
2. **Select.** Use a named ticket only when it is on the frontier; otherwise report its state, expose the frontier, and stop. Without a selection, take the first frontier ticket.
3. **Claim.** Refresh the ticket, then record the claim. If its state changed or another session owns it, refresh the frontier and stop.
4. **Resolve.** Follow the ticket's type and mode, then record exactly one outcome through the tracker convention:
   - **Resolved:** answer the question and add its context pointer to `Decisions So Far`.
   - **Blocked:** record the blocker; create-then-wire a sharp blocker or return an unaskable blocker to fog.
   - **Out of scope:** record why it lies beyond the destination and add its linked scope note to `Out Of Scope`.
5. **Reconcile.** Graduate sharpened fog, create-then-wire newly visible tickets, update affected dependencies, and mark obsolete tickets through consequence-only state changes without answering them.
6. **Verify.** Apply **Mutation read-back** to the selected ticket, claim, outcome, map pointers, changed edges, and resulting frontier.
7. **Expose.** Show the next frontier or close the map.

Preserve concurrent work. Touch only the selected ticket, directly affected edges, and map sections changed by its outcome.

Advance completes when exactly one selected ticket has a substantive outcome; every other ticket mutation is consequence-only; its claim and direct map consequences are reconciled; and the next frontier or closing route is visible.

## Close

Close the map only when the destination is reached, no unresolved child or in-scope fog remains, and the next durable artifact or action is clear. Apply the tracker convention, recommend exactly one route, and stop:

- settled decision — report it; recommend `$domain-modeling` only for durable language or an ADR;
- settled parent-spec source — `$to-spec`;
- settled source containing multiple implementation slices — `$to-tickets`;
- exactly one bounded ready slice — `$implement`.

## Return

Return the map link when one exists, the Chart result or selected ticket outcome, linked evidence, direct map changes, and the next frontier or closing route. On closure, also return the destination and decisive resolutions.
