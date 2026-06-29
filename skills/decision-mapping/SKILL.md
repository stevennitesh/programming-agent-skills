---
name: decision-mapping
description: Turn a loose idea into a compact, git-tracked decision map of investigation tickets, then resolve one frontier ticket at a time.
---

# Decision Mapping

Use this when a loose idea has too much fog of war to become a PRD or implementation plan in one session.

Create a compact decision map: one Markdown file, git-tracked alongside the project, that records the open questions blocking a clear path to implementation. The whole map is loaded into every resume session, so keep it small and link to assets instead of duplicating them.

## Decision Map

Save maps under the repo's existing decision-map or planning convention. If none exists, use `docs/decision-maps/<slug>.md`.

Each ticket is sized to one Codex session:

```markdown
## #1: Relational Or Non-Relational Database?

Status: Pending | In Progress | Resolved | Blocked
Blocked by: #<ticket-number>, #<ticket-number>
Type: Research | Prototype | Grilling

### Question

<question>

### Answer

<resolved answer, or why blocked>

### Assets

- <path/link to research summary, prototype, notes>
```

Assets created during tickets should be linked from the map, not duplicated inside it.

## Ticket Types

- **Research**: Read documentation, third-party APIs, or local resources like knowledge bases. Create a concise markdown summary as an asset.
- **Prototype**: Use `$prototype` to test a UI, logic, state, or behavior hypothesis. Link the prototype or its captured answer as an asset.
- **Grilling**: Use `$grilling` and `$domain-modeling` to resolve a decision through conversation. Ask one question at a time. This is the default.

## Frontier

The map is deliberately incomplete beyond the frontier. The frontier is the set of `Pending` tickets whose blockers are `Resolved`.

Push back the fog of war one node at a time. Resume only one frontier ticket per session.

If a ticket cannot be resolved, mark it `Blocked`, record why, and add the smallest follow-up ticket or user input needed to unblock it.

The map is done when no `Pending` frontier tickets remain and the path to implementation is clear.

## Invocation

### Bootstrap

Use bootstrap when the user brings a loose idea.

1. Run `$grilling` and `$domain-modeling` to surface open decisions. Ask one question at a time.
2. Write the decision map with the current frontier identified and trivially-decidable entries resolved inline.
3. Stop. Bootstrap creates the map; it does not resolve tickets or implement product code.

If the initial grilling leaves no fog of war, offer to skip the map and recommend `$to-prd` for multi-session implementation or `$implement` for one ready issue.

### Resume

Use resume when the user provides a decision map path and a ticket number.

1. Reread the whole map from disk before editing.
2. Mark the selected ticket `In Progress` before working, unless it is already `In Progress` from another active session.
3. Resolve or block exactly one frontier ticket, invoking Research, `$prototype`, or `$grilling` + `$domain-modeling` as needed.
4. Update that ticket's status, answer, assets, and directly affected dependency edges.
5. Add newly discovered tickets with correct `Blocked by` edges.
6. Stop. Do not implement product code.

If the decision invalidates other parts of the map, update or delete only the affected nodes.

## Parallelism

Multiple sessions may work from the same map. Preserve other sessions' updates. If the selected ticket is already `In Progress`, ask before taking it over. On resume, change only the ticket being resolved plus directly affected dependency edges or invalidated nodes.

## Completion Handoff

When the map is done, recommend `$to-prd` if the work needs a parent PRD and implementation issues, or `$implement` if exactly one ready issue remains.
