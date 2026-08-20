---
name: to-questionnaire
description: Create one Markdown discovery questionnaire for one external stakeholder who owns facts, judgment, or a decision unavailable from inspectable sources and the user.
---

# To Questionnaire

Turn one gap the user cannot answer into a questionnaire for the one external
person who can. The user owns delivery, answers, and the downstream decision.
Create the file, report its path, and stop. Never contact or answer for the
recipient.

**Grill the send, not the subject.**

## Identify

Keep one recipient and one downstream decision. When materially different gaps
belong to different people, return the proposed split instead of blending them.
When supplied context already answers the gap, explain that no questionnaire is
needed and stop. When claim-owning sources can answer it, recommend `$research`
and stop. When the current user owns the answer, recommend `$grilling` and stop.

Infer from the conversation who the questionnaire is for and what the user
needs back. Ask one compact intake only when missing sender-known information
would change the recipient, questions, tone, effort, or destination. Preserve
a supplied answer-return destination.

## Draft

Give the recipient enough context to answer without reconstructing the
conversation. Order questions by decision value, then dependency. Make each
question neutral, about one idea, and answerable by that recipient. Invite
partial answers and explicit unknowns. Ask for rationale, examples, sources, or
constraints only when the downstream decision needs them.

Every item the user needs back must have a substantive question. A catch-all
does not count as coverage. Remove any question that does not affect the
downstream decision. Do not include or ask for credentials or secrets; ask for
a safe pointer or non-secret description instead.

Use this shape, omitting sections that add nothing:

```markdown
# <Questionnaire title>

**Purpose:** <why this exists and the decision riding on it>
**From:** <sender>
**To:** <recipient>
**How your answers will be used:** <answer use>
**Return answers to:** <destination, when not obvious>

## Context

<Enough context to answer well.>

## How to answer

<Deadline and rough effort when relevant. Partial answers and "I don't know"
are useful.>

## <Theme, when there are more than a handful of questions>

### <One question>

_Why this matters: <only when it prevents misreading>_

>

## Anything else?

<Include only when an open catch-all is useful.>
```

## Write

Write exactly one Markdown file to the requested path. Otherwise use
`to-questionnaire-<slug>.md` in the current directory. Never overwrite an
existing file without explicit authority; when no exact target was requested,
choose a clear unused name instead.

Reread the complete intended file as the recipient. Confirm the path exists and
every needed item has a recipient-answerable question. If the write or reread
failed or was partial, do not claim completion; report whether an incomplete
file remains. Otherwise return the path, what it covers, any unresolved gap,
and `Delivery: not performed`.

Complete when the file exists, every item the user needs back is covered,
nothing outside the downstream decision remains, and the path is reported. Stop
before delivery, answer handling, or the downstream decision.
