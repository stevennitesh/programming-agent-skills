# Wayfinder Map Format

Read when creating, validating, or reconciling a map.

Open work lives in child tickets. Resolutions live in their owning tickets. The
map keeps orientation and pointers. `Not Yet Specified` is the sole fog
container.

## Map

```markdown
## Destination

Destination owner: <who owns the outcome>
Outcome: <decision, settled source, or readiness state>
Route-closing condition: <observable condition>
Terminal kind: settled source for $to-spec | terminal decision
Return owner: <who receives closure>

## Scope Boundary

In: <charted scope>
Out: <destination delivery and explicit exclusions>

## Notes

Source Trace: <source pointers>
Domain: <domain pointers and current Domain Delta, when any>
Constraints: <governing constraints>
Standing decisions: <applicable durable decisions>

## Decisions So Far

- [<resolved ticket title>](link) - <one-line gist>

## Not Yet Specified

<in-scope fog whose question is not yet sharp; when empty, write exactly:
None - all remaining in-scope questions are ticket-owned.>

## Out Of Scope

- [<future-work owner, governing resolution, or map pointer>](link) -
  <why it lies beyond the destination>
```

Prefer the ticket that owns future work. When none exists, link the governing
resolution or map pointer. Do not create a ticket only to supply a link.

## Ticket

```markdown
Type: research | prototype | diagnosis | grilling | task
Participation: HITL | AFK
Resolution owner: <who can settle the question>
Resolver: $research | $prototype | $diagnosing-bugs | $grilling |
  $grill-with-docs | $to-questionnaire | direct task
Expected return: <evidence packet or human return that permits classification>
Re-entry owner: $wayfinder

## Question

<one sharp decision or investigation, sized for one session>
```

Record parent relationship, blocking edges, claim state, and outcome through
the repo's `Wayfinding operations` convention. For Research, record the
approved repo-local note path. For Prototype, also record:

```text
Decision owner: <who>
Claim level: shape/feel | design evidence
Judgment mode: human | rule-based
Human judge: <who> | Verdict criteria: <objective caller-locked criteria>
```

## Resolution Comment

```markdown
Status: resolved | blocked | waiting | out of scope
Answer or condition: <supported answer, blocker, wait trigger, or scope reason>
Authority: <resolution owner or governing source>
Evidence or assets: <links>
Map implications: <pointers, edges, fog dispositions, or none>
Residual: <remaining uncertainty or none>
```
