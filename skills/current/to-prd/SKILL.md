---
name: to-prd
description: Synthesize the current conversation into a comprehensive brain-dump PRD and publish it to the configured issue tracker.
---

# To PRD

Create the parent PRD for an idea before `$to-issues` splits it into tracer-bullet implementation issues.

This is **synthesis**, not grilling. Do not interview for new requirements. Preserve the full explored idea in the PRD: user stories, accepted decisions, rejected options, constraints, edge cases, failure modes, prototype findings, testing notes, and out-of-scope boundaries.

## Preconditions

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`; run `$setup-matt-pocock-skills` if either is missing.

When touching codebase context, read `docs/agents/domain.md` if present so the PRD uses domain glossary vocabulary and respects ADRs.

## Process

### 1. Gather Source

Use the current conversation as source material. If a PRD, spec, issue, path, or URL is provided, read it and its linked context.

Do not ask new requirement questions. Record unresolved product decisions under `Open Questions`. Ask only when publishing requires confirmation or a test seam choice materially changes the PRD.

### 2. Ground In The Codebase

Explore just enough code to understand current modules, existing seams, likely test surface, and relevant prior art.

Use domain glossary vocabulary for product concepts and `$codebase-design` vocabulary for architecture: module, interface, seam, adapter, depth, leverage, locality.

Call out ADR conflicts instead of silently overriding them.

### 3. Write The Brain-Dump PRD

Write a comprehensive PRD with these sections:

- `Problem Statement` - the problem from the user's perspective, including why the current state is painful or limiting.
- `Desired Outcome` - what should be true when the work is done, phrased as user-visible or operator-visible change.
- `User Stories` - an extensive numbered list of actors, capabilities, benefits, primary flows, secondary flows, and edge cases.
- `Accepted Decisions` - decisions already settled in the conversation: product behavior, domain terms, module/interface/seam choices, contracts, UX, operations, integrations, and migration choices.
- `Rejected Or Deferred Options` - options discussed but not chosen, with reasons, so future sessions do not reopen them accidentally.
- `Edge Cases And Failure Modes` - weird cases, invalid inputs, empty states, degraded states, permission boundaries, race conditions, data-quality issues, and other likely-to-be-forgotten behavior.
- `Testing Notes` - behavior to prove, likely tracer bullets, seams to test through, useful fixtures, prior test patterns, and regression risks. Name the happy path, high-risk seams, important failure modes, permission boundaries, state transitions, integration risks, or migration risks that need end-to-end proof. Do not split them into issues here.
- `Out Of Scope` - adjacent behavior, features, refactors, cleanup, or design paths explicitly not included.
- `Open Questions` - unresolved questions already visible from the conversation; do not use this section to start a new interview.
- `Further Notes` - useful context that does not fit above; omit if empty.

Make the PRD verbose on purpose. It should let a fresh Codex session recover the same product understanding without reading the full original conversation. Do not compress away rough edges; preserve messy but relevant context under the closest matching section.

User stories should use:

`As a <actor>, I want <capability>, so that <benefit>.`

Testing notes should identify observable behavior to prove through public interfaces, not implementation details. When naming tracer bullets, prefer proof points that reduce uncertainty about behavior, a seam, or a risk.

Do not include file paths or code snippets unless they are durable contracts or prototype findings that encode a decision more precisely than prose. Trim prototype material to the decision-rich part and say it came from the prototype.

### 4. Publish

Publish the PRD using `docs/agents/issue-tracker.md`.

Apply the label mapped from `ready-for-agent` in `docs/agents/triage-labels.md`, unless the user says otherwise.

Do not split the PRD into implementation issues here. Do not close, relabel, or otherwise modify any parent source unless explicitly asked.

End by naming `$to-issues` as the next skill to run if the user wants implementation issues.

## Completion Criteria

Done means the PRD preserves the full explored idea, uses repo/domain vocabulary, records testing seams and boundaries, calls out ADR conflicts, and is published to the configured issue tracker.
