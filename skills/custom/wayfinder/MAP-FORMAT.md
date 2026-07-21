# Wayfinder Map Format

Read when creating, validating, or reconciling a map.

Open work lives in child tickets. Resolution detail lives in the ticket that owns it. The map keeps orientation and pointers. The Scope Boundary fixes the charted effort; Out Of Scope indexes linked tickets or discoveries later excluded from that boundary.

`Not Yet Specified` is the sole fog container. Keep every unresolved fog item there rather than adding a parallel heading.

## Map

```markdown
## Destination

<the decision, artifact, or readiness state that closes this map>

## Scope Boundary

<what is inside this map and what destination delivery remains outside>

## Notes

<source and domain pointers, skills, constraints, and standing preferences>

## Decisions So Far

- [<resolved ticket title>](link) - <one-line gist>

## Not Yet Specified

<in-scope fog whose question is not yet sharp; when empty, write exactly: None — all remaining in-scope questions are ticket-owned.>

## Out Of Scope

- [<future-work owner, governing resolution, or map pointer>](link) - <why it lies beyond the destination>
```

Prefer the ticket that owns future work. When none exists, link the resolution or map pointer that governs the exclusion. Do not create a ticket solely to supply a link.

## Ticket

```markdown
## Question

<one sharp decision or investigation, sized for one session>
```

Record type, HITL/AFK mode, parent relationship, blocking edges, claim state, and resolution state through the repo's `Wayfinding operations` convention.
For Research tickets, also record the caller-approved repo-local note path.
For Prototype tickets, put `Claim level: shape/feel | design evidence` and either `Human judge: <who>` or `Verdict criteria: <objective caller-locked criteria>` near `Participation`.
