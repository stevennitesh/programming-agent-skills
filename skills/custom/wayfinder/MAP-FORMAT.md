# Wayfinder map format

Persist only decision state. `SKILL.md` owns behavior; the configured tracker
guide owns provider representation.

## Map

```markdown
## Destination

Owner: <destination owner>
Outcome: <decision or settled source>
In scope: <bounded scope>
Out of scope: <delivery and exclusions>
Close when: <observable condition>
Return to: <owner of the settled result>

## Notes

<only pointers or standing constraints every session needs; or None>

## Decisions so far

- [<ticket title>](link) - <one-line answer gist>

## Not yet specified

- <unsharp in-scope uncertainty> - sharpens when <evidence or decision>

When empty, write `None`.

## Out of scope

- [<ticket or decision>](link) - <reason>
```

## Ticket

```markdown
Type: Research | Prototype | Grilling | Questionnaire | Task
Decision owner: <who can settle the question>
Accept when: <evidence or attributable decision that answers the question>
Mutation boundary: <allowed durable artifact or none, only when applicable>

## Question

<one sharp one-session question>

## Why this matters

<how the answer changes the destination or route>
```

Represent dependencies through the configured tracker relationship mode, not a
second body field.

Append only fields that change authority or safe continuation:

```text
Research note: <approved repo-local path and create | update | none>
Prototype judgment: <named human judge or predeclared objective rule>
Prototype evidence and run: <representative cases; bounded entry point; cleanup or custody>
Questionnaire packet: <recipient; downstream decision; needed-back items; authorized path; answer-return destination; exact user re-entry>
```

## Resolution

```markdown
Condition: resolved | waiting | blocked | out of scope
Answer or condition: <answer, wait, blocker, or scope decision>
Owner and return condition: <owner; observable trigger or intervention; or none>
Evidence: <links>
Direct map consequences: <decision gist, dependencies, new question, fog, or none>
Supersedes: <prior resolution pointer or none>
```

## Closing record

```markdown
Disposition: delivered
Destination: <outcome and scope>
Closing evidence: <cited evidence satisfying Close when>
Decisions: <ticket links>
Exclusions and residuals: <items or none>
Return to: <owner>
```

## Termination record

```markdown
Disposition: cancelled | superseded | out of scope
Confirmed by: <destination owner and evidence>
Unresolved and preserved work: <ticket or evidence links>
Recovery or successor: <pointer or none>
Return to: <owner>
```
