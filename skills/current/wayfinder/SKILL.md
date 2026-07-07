---
name: wayfinder
description: Plan a large, foggy effort as a tracker-backed map of investigation tickets, then resolve one frontier ticket at a time until the route to the destination is clear.
---

# Wayfinder

A loose idea has arrived: too large for one agent session, and wrapped in fog. The way from here to the **destination** is not visible yet.

Wayfinding charts the route as a **shared map** on the repo's issue tracker, then works one ticket at a time until the destination is clear enough for a PRD, implementation issues, or one bounded implementation slice.

## Destination

Name the destination first. It shapes every ticket and fixes scope.

The destination can be:

- a spec or PRD ready to turn into implementation issues
- a decision that must be locked before planning starts
- a change made in place, such as a migration or large refactor

Anything past the destination is **out of scope**, not fog.

## Refer By Name

Every map and ticket has a readable title. In narration, map updates, and decision summaries, refer to tickets by linked name, not bare id, number, or slug.

Use ids only inside links, tracker operations, or dependency wiring.

## Map

The map is a single tracker item labelled `wayfinder:map`. Tickets are child items of that map.

The map is an index, not a store. It lists the destination, standing notes, decisions so far, fog that is not yet ticketable, and out-of-scope work. The detail for each resolved decision lives in exactly one place: the ticket resolution.

Tracker mechanics are repo-local. Read `docs/agents/issue-tracker.md`, section `Wayfinding operations`, before creating or updating a map. If that section is absent, recommend `$setup-matt-pocock-skills`; for local-only work, use `.scratch/<feature-slug>/wayfinder/`.

### Map Body

```markdown
## Destination

<what reaching the end of this map looks like: the spec, decision, or change this effort is finding its way to>

## Notes

<domain docs, skills every session should consult, standing preferences for this effort>

## Decisions So Far

<!-- one line per closed ticket: enough to judge relevance, with a link to the ticket that owns the detail -->

- [<closed ticket title>](link) - <one-line gist>

## Not Yet Specified

<!-- in-scope fog you cannot ticket yet; graduates as the frontier advances -->

## Out Of Scope

<!-- work ruled beyond this destination; closed, never graduates -->
```

### Tickets

Each ticket is a child tracker item of the map. Its body is the question, sized to one agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries one type label:

- `wayfinder:research`
- `wayfinder:prototype`
- `wayfinder:grilling`
- `wayfinder:task`

A session claims a ticket before working by assigning it to the driver or marking it `In Progress` in the repo-local tracker convention. That claim is the concurrency guard.

The answer is recorded on resolution, not prefilled in the ticket body. Link assets from the resolution; do not paste full research, prototypes, logs, or transcripts into the map.

## Ticket Types

- **Research**: Use `$research` when source legwork needs a durable, cited note. Link the note from the ticket resolution.
- **Prototype**: Raise fidelity with a cheap concrete artifact: outline, stub, UI/logic spike, or `$prototype`. Link the artifact or captured answer.
- **Grilling**: Resolve through conversation. Run `$grilling` and `$domain-modeling`; ask one question at a time. This is the default.
- **Task**: Manual or mechanical work that must happen before the discussion can move forward. Automate where possible; otherwise hand the user a precise checklist. Resolve with what was done and any facts later tickets depend on.

## Fog Of War

The map is deliberately incomplete. Beyond the live tickets lies **fog of war**: in-scope questions you can tell are coming but cannot yet phrase sharply because they depend on open answers.

Write that fog in `Not Yet Specified`. It is a signpost for collaborators, not a backlog.

Fog graduates only when the frontier reaches it. Resolving a ticket may turn one fog patch into several tickets, one ticket, or nothing.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you can answer it now.

- Ticket when the question is sharp, even if blocked.
- Keep as fog when the question is still too vague to ask.

`Not Yet Specified` excludes decisions already made, live tickets, and out-of-scope work.

## Out Of Scope

Out-of-scope work is beyond the destination. It is not fog and never graduates into tickets unless the destination changes.

If an existing ticket turns out to sit beyond the destination, close it or mark it out of scope, then add one line to `Out Of Scope`: gist, reason, and link. Do not add it to `Decisions So Far`; a scope boundary is not a step on the route.

## Invocation

Two modes. Either way, never resolve more than one ticket per session.

### Chart The Map

Use this when the user brings a loose idea.

1. **Name the destination.** Run `$grilling` and `$domain-modeling` to pin down what this map is finding its way to: spec, decision, or change.
2. **Map the frontier.** Grill breadth-first across the space, not deep on one thread, surfacing open decisions and the first takeable tickets.
3. **Create the map.** Fill Destination and Notes, leave Decisions So Far empty, and sketch non-ticketable fog into Not Yet Specified.
4. **Create ticketable children.** Create every sharp ticket, then wire blocking edges in a second pass after ticket ids exist.
5. Stop. Charting the map does not resolve tickets or implement product code.

If there is no fog of war after the initial grilling, recommend `$to-prd` for multi-session work or `$implement` for one ready issue.

### Work Through The Map

Use this when the user provides a map URL, number, or path. A ticket is optional; without one, choose the next frontier ticket.

1. Load the map low-resolution view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in map order.
3. Claim the ticket before work.
4. Resolve it. Zoom into related or closed tickets only as needed; follow the map Notes; when in doubt, run `$grilling` and `$domain-modeling`.
5. Record the resolution: post the answer, close or mark the ticket resolved, and append one context pointer to Decisions So Far.
6. Add newly surfaced tickets and wire blocking edges. Graduate any fog made specifiable, removing each graduated patch from Not Yet Specified. Update or close tickets invalidated by the answer. Rule out-of-scope discoveries out of scope instead of resolving them on the route.
7. Stop. Do not implement product code.

Expect other sessions to edit the tracker concurrently. Preserve other sessions' updates and touch only the selected ticket, directly affected dependency edges, and map sections affected by the resolution.

## Completion Criteria

For charting, done means the map exists, the first frontier is ticketed and wired, fog is recorded only where it is not yet ticketable, and no ticket has been resolved.

For working, done means exactly one ticket is resolved or marked blocked/out of scope, the map has one new context pointer or scope note, newly ticketable fog has been graduated, and the next frontier is visible.

When the destination is clear, recommend `$to-prd` if the work needs a parent PRD and implementation issues, or `$implement` if exactly one ready issue remains.
