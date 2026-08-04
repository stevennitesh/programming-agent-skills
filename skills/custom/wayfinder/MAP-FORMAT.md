# Wayfinder Map Format

Persist these shapes. `SKILL.md` owns behavior; tracker docs own representation.

## Map

```markdown
## Destination

Destination owner: <owner>
Outcome: <decision, settled source, or readiness>
Route-closing condition: <observable condition>
Terminal kind: settled source | terminal decision
Return owner: <closure recipient>
Predecessor: <closed map link or none>
Post-Chart ticket allowance: <finite integer>
Post-Chart tickets used: <integer and calculation>

## Scope Boundary

In: <scope>
Out: <delivery and exclusions>

## Notes

<source, domain, constraint, skill, or standing-decision pointers; or None>

## Decisions So Far

- [<resolved ticket title>](link) - <one-line gist>

## Not Yet Specified

- Uncertainty: <unsharp in-scope uncertainty>
  Owner: <who owns sharpening>
  Sharpening source: <finite source>
  Observable trigger: <evidence that permits reconsideration>
  Fallback: <exclude, terminate, successor, or named blocker>
  Affecting tickets: <links or none>

When empty, write exactly:
None - all remaining in-scope questions are ticket-owned.

## Out Of Scope

- [<governing resolution, ticket, map, or successor>](link) - <reason>
```

## Ticket

```markdown
Type: Research | Prototype | Diagnosis | Grilling | Questionnaire | Task
Participation: HITL | AFK | external
Resolution owner: <who settles it>
Resolver: <resolver locked by SKILL.md>
Expected return: <evidence or return permitting normalization>
Mutation boundary: <allowed artifact or none>
Re-entry owner: $wayfinder

## Question

<one sharp one-session question>
```

Append only applicable resolver fields:

```text
Research note path and write mode: <approved repo-local path; create | update | none>

Decision owner: <Prototype decision owner>
Result recipient: <Prototype return recipient>
Claim level: shape/feel | design evidence
Judgment mode: human | rule-based
Human judge: <who> | Verdict criteria: <objective caller-locked criteria>
Prototype evidence surface and representative cases: <selected surface; cases, variants, workload, or interactions>
Prototype paths and final disposition: <authorized roots; cleanup or preservation>
Prototype effects, entry, bound, and limits: <authorized effects; entry point or recipe; finite bound; known limits>

Questionnaire packet and approval: <exact packet or durable pointer; approval evidence; authorized durable path; retention owner; answer-return destination>
```

## Resolution Comment

```markdown
Status: resolved | blocked | waiting | out of scope
Answer, blocker, wait, or scope condition: <normalized result>
Condition owner: <owner or none>
Observable trigger or intervention: <exact condition or none>
Required return evidence: <evidence or none>
Supersedes: <prior condition pointer or none>
Authority: <owner or governing source>
Evidence or assets: <links>
Map implications: <pointers, edges, fog, allowance, or none>
Residual: <uncertainty or none>
```

## Closing Packet

```markdown
Disposition: delivered | cancelled | superseded | out of scope
Map/source owner: <link; owner>
Destination/bound: <outcome; scope; exclusions>
Closing route: <condition; terminal kind; return owner>
Route-closing satisfaction: <cited evidence>
Snapshot identity: <map, ticket, resolver-return, and tracker identities>
Decisive resolutions: <links; owners>
Coherence: <destination, dependency, contract, decision, and evidence result>
Evidence: <links>
Growth allowance: <total; used; remaining; calculation>
Residual: <exclusions; deferrals; uncertainty; or none>
Proof/acceptance objectives: <items>
Domain Delta: <intact packet or not applicable>
Recovery or successor boundary: <pointer or none>
```
