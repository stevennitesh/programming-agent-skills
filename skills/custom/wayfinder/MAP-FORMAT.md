# Wayfinder Map Format

Read this file only when charting a new map.

Open work lives in child tickets. Resolution detail lives in the ticket that owns it. The map keeps orientation and pointers. The Scope Boundary fixes the charted effort; Out Of Scope indexes linked tickets or discoveries later excluded from that boundary.

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

<in-scope fog whose question is not yet sharp>

## Out Of Scope

- [<ticket or discovery>](link) - <why it lies beyond the destination>
```

## Ticket

```markdown
## Question

<one sharp decision or investigation, sized for one session>
```

Record type, HITL/AFK mode, parent relationship, blocking edges, claim state, and resolution state through the repo's `Wayfinding operations` convention.
For Research tickets, also record the caller-approved repo-local note path.
