---
name: wayfinder
description: Chart a tracker-backed route through a large, foggy effort, then advance one frontier ticket per session until the route to the destination is clear.
---

# Wayfinder

Wayfinder charts the route before delivery begins. Name the **destination**, chart the first **frontier**, then advance exactly one ticket per session.

Tickets resolve uncertainty. Delivery begins after the map closes.

## Navigation Model

- **Destination** - the state where the route is clear enough to stop wayfinding: a settled decision, source ready for `$to-spec`, settled work ready for `$to-tickets`, or one ready slice for `$implement`. Anything beyond it is **out of scope**.
- **Map** - an **index**, not a store. Child tickets own questions and resolutions; the map holds orientation and context pointers.
- **Takeable** - an open child of the map that is unblocked and unclaimed.
- **Frontier** - the takeable child tickets in map order: the edge of the known.
- **Fog of war** - in-scope uncertainty that cannot yet be stated as a sharp question. Record it under `Not Yet Specified`.
- **Graduate** - move fog into one or more tickets once its questions become sharp.
- **Claim** - the concurrency guard. Work starts only after the tracker records ownership.
- **Name** - use linked map and ticket titles in human-facing text. Reserve ids for tracker operations and dependency wiring.

**Fog or ticket?** Ticket a question when it is precise, even if blocked. Keep it as fog while the question itself remains unclear.

Read `docs/agents/issue-tracker.md`, section `Wayfinding operations`, before any tracker mutation. If the section is absent or its required operations are unavailable, stop and recommend `$repo-bootstrap`. For local-only work, use `.scratch/<feature-slug>/wayfinder/`.

## Ticket Types

Every ticket declares a method and a participation mode:

- **Research - AFK:** Run `$research`; link its cited note from the resolution.
- **Prototype - HITL:** Create the cheapest concrete artifact the human can react to: outline, stub, UI/logic spike, or `$prototype`. Link the artifact and capture the verdict.
- **Grilling - HITL:** Run `$grill-with-docs`. This is the default for decision questions.
- **Task - HITL or AFK:** Complete a prerequisite that exposes a later decision. Automate AFK work; otherwise provide a precise HITL checklist. Record what changed and the facts later tickets depend on.

A **HITL** ticket completes only through live human participation. An **AFK** ticket may be driven autonomously.

The ticket body owns the question. Its resolution owns the answer and linked assets.

## Modes

Choose exactly one mode per session.

### Chart

Use this mode for a loose idea without an existing map.

1. **Name the destination.** Run `$grill-with-docs` with a **charting bound**: settle only the outcome, scope, and route-closing condition.
2. **Sweep breadth-first.** Surface each material child decision as a sharp question. Defer it explicitly to a named Wayfinder ticket instead of resolving it inside the charting interview.
3. **Gate on fog.** If the route is already clear, skip the map and use the closing routes below.
4. **Chart the map.** Read [MAP-FORMAT.md](MAP-FORMAT.md), then create the map with its destination, notes, empty resolution index, visible fog, and scope boundary.
5. **Create-then-wire.** Create every sharp child ticket, then add blocking edges after ticket identities exist.

Apply the tracker's **Mutation read-back** rule to the map, every child, and every blocking edge before declaring the chart complete.

Charting is complete when either:

- no map is needed and the next route is named; or
- the map exists, every sharp question is ticketed, all known blocking edges are wired, remaining fog cannot yet be stated as a sharp question, and zero tickets have recorded outcomes.

### Advance One Frontier Ticket

Use this mode when the user supplies a map. A named ticket wins only when it is takeable. Otherwise reject the selection: report its current state, expose the frontier, and stop before claim. Without a named ticket, choose the first frontier ticket in map order.

1. **Orient low-resolution.** Load the destination, notes, resolution pointers, fog, scope boundary, and ticket headers. Load full ticket bodies only as needed.
2. **Claim.** Refresh the selected ticket, then record this driver's claim through the tracker convention. If its state changed or another session owns it, report the current state and refresh the frontier.
3. **Zoom.** Follow the map Notes. Load the selected ticket and only the related context needed to resolve it. Follow its type and HITL/AFK mode.
4. **Record one outcome:**
   - **Resolved:** record the answer, close or resolve the ticket, and append one context pointer to `Decisions So Far`.
   - **Blocked:** record the blocker. Create-then-wire a sharp blocker; return an unaskable blocker to fog. Apply the tracker's blocked convention and release the active claim.
   - **Out of scope:** close or mark the ticket out of scope and append one linked scope note under `Out Of Scope`.
5. **Reconcile.** Graduate sharpened fog, create-then-wire newly visible tickets, update invalidated dependencies, and close or revise tickets made obsolete by the outcome.
6. **Read back.** Apply the tracker's Mutation read-back rule to the ticket, claim, outcome, map pointers, and changed edges.
7. **Expose the edge.** Show the next frontier or close the map.

Other sessions may update the tracker concurrently. Preserve their work and touch only the selected ticket, directly affected edges, and map sections changed by its outcome.

Advancing is complete when exactly one ticket has one recorded outcome, its claim state is reconciled, every direct map consequence is updated, and the next frontier or closing route is visible.

## Close The Map

The map closes when:

- the destination is reached;
- no unresolved child ticket remains;
- no in-scope fog remains; and
- the next durable artifact or action is clear.

Close or mark the map complete through the tracker convention.

Recommend exactly one next route and end the session:

- **Settled decision:** report it; recommend `$domain-modeling` when it changes durable language or warrants an ADR.
- **Settled idea needing a parent spec:** recommend `$to-spec`.
- **Settled source containing multiple implementation slices:** recommend `$to-tickets`.
- **Exactly one bounded ready slice:** recommend `$implement`.

## Handoff

End every session with the map link when one exists, the chart result or one ticket outcome, linked evidence, direct map changes, and the next frontier or closing route. A closing handoff also reports the destination and decisive resolutions.
