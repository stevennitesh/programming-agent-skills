# Wayfinder Map Format

Persist these shapes. `SKILL.md` owns behavior; tracker docs own representation.

## Map

```markdown
## Destination

Destination owner: <owner>
Outcome: <decision, settled source, or readiness>
Route-closing condition: <observable condition>
Terminal kind: settled source for $to-spec | terminal decision
Return owner: <closure recipient>

## Scope Boundary

In: <scope>
Out: <delivery and exclusions>

## Notes

<source, domain, constraint, skill, or standing-decision pointers; or None>

## Decisions So Far

- [<resolved ticket title>](link) - <one-line gist>

## Not Yet Specified

<in-scope fog whose question is not yet sharp; when empty, write exactly:
None - all remaining in-scope questions are ticket-owned.>

## Out Of Scope

- [<governing resolution, ticket, map, or future-work owner>](link) - <reason>
```

## Ticket

```markdown
Type: <type locked by SKILL.md>
Participation: HITL | AFK
Resolution owner: <who settles it>
Resolver: <resolver locked by SKILL.md>
Expected return: <evidence or return permitting classification>
Re-entry owner: $wayfinder

## Question

<one sharp one-session question>
```

Append only applicable resolver fields:

```text
Research note path: <approved repo-local note path>

Decision owner: <Prototype decision owner>
Claim level: shape/feel | design evidence
Judgment mode: human | rule-based
Human judge: <who> | Verdict criteria: <objective caller-locked criteria>
```

## Resolution Comment

```markdown
Status: resolved | blocked | waiting | out of scope
Answer or condition: <answer, blocker, wait trigger, or scope reason>
Authority: <owner or governing source>
Evidence or assets: <links>
Map implications: <pointers, edges, fog, or none>
Residual: <uncertainty or none>
```

## Closing Packet

```markdown
Map/source owner: <link; owner>
Destination/bound: <outcome; scope; exclusions>
Closing route: <condition; terminal kind; return owner>
Decisive resolutions: <links; owners>
Evidence: <links>
Residual: <exclusions; deferrals; uncertainty; or none>
Proof/acceptance objectives: <items>
Domain Delta: <intact packet or not applicable>
```
