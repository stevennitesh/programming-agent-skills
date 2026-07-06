---
name: to-prd
description: Synthesize the current conversation into a comprehensive brain-dump PRD and publish it to the configured issue tracker.
---

# To PRD

Create the parent brain-dump PRD for an idea before `$to-issues` splits it into tracer-bullet implementation issues.

This is **synthesis**, not grilling: the alignment work is done, and `$to-prd` preserves shared understanding without interviewing for new requirements. Capture settled decisions, rejected or deferred options, constraints, edge cases, failure modes, prototype findings, proof seams, and out-of-scope boundaries.

## Preconditions

Read the target repo's `AGENTS.md` as the setup router.

For publishing, read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either is missing, stop and recommend `$setup-matt-pocock-skills`; do not recreate tracker or label guidance here.

When grounding in codebase context, follow `docs/agents/domain.md` when present to the relevant glossary and ADRs.

## Process

### 1. Gather Source

Use only the current conversation, explicit source material the user provides, target repo `AGENTS.md`, repo-local agent docs it names, this skill's direct supporting files, and explicit user approvals.

If a PRD, spec, issue, path, or URL is provided, read that source and any directly required context it names. Do not chase optional background or infer unstated commitments.

Do not ask new requirement questions. Record unresolved product decisions under `Open Questions`. Ask only before publishing, mutating trackers, crossing a commitment boundary, or choosing a load-bearing test seam that materially changes the PRD.

### 2. Ground In The Codebase

Explore just enough code to understand current modules, existing seams, proof surfaces, and relevant prior art.

Prefer existing seams to new ones and the highest useful seam possible; ideally the PRD names one durable proof seam for the change. If a new seam looks necessary, describe why it is load-bearing instead of designing the patch.

Use domain glossary vocabulary for product concepts and `$codebase-design` vocabulary for architecture: module, interface, seam, adapter, depth, leverage, locality.

Call out ADR conflicts instead of silently overriding them.

### 3. Write The Brain-Dump PRD

Write a source-traced brain-dump PRD with these sections:

- `Source Trace` - source thread, explicit source files/issues/URLs, repo docs consulted, and user approvals relied on.
- `Problem Statement` - the problem from the user's perspective, including why the current state is painful or limiting.
- `Desired Outcome` - what should be true when the work is done, phrased as user-visible or operator-visible change.
- `User Stories` - distinct actors, flows, benefits, and edge cases that affect acceptance.
- `Accepted Decisions` - decisions already settled in the conversation: product behavior, domain terms, module/interface/seam choices, contracts, UX, operations, integrations, and migration choices.
- `Rejected Or Deferred Options` - options discussed but not chosen, with reasons.
- `Edge Cases And Failure Modes` - invalid inputs, empty states, degraded states, permission boundaries, race conditions, data-quality issues, and likely-to-be-forgotten behavior.
- `Proof Seams And Testing Notes` - proof seams, observable behavior to prove, likely tracer bullets, useful fixtures, prior patterns, and regression risks; do not split them into issues.
- `Out Of Scope` - adjacent behavior, features, refactors, cleanup, or design paths explicitly not included.
- `Open Questions` - unresolved questions already visible from the sources; do not use this section to start a new interview.
- `Further Notes` - decision-rich context that does not fit above; omit if empty.

Write for a fresh Codex session that needs to recover the shared understanding without rereading the source thread. Summarize source material; do not mirror it, and do not produce generic boilerplate.

User stories should use:

`As a <actor>, I want <capability>, so that <benefit>.`

Write only stories that carry acceptance signal: a distinct actor, flow, benefit, edge case, permission boundary, or failure mode.

Proof notes name seams and proof points, not implementation steps.

Avoid file paths and code snippets unless they are durable contracts or prototype findings that encode a decision more precisely than prose.

### 4. Approve And Publish

Prepare the PRD as a draft first. Get explicit user approval before creating an issue, applying labels, mutating a tracker, or treating the PRD as the user's commitment.

After approval, publish the PRD as a parent issue using `docs/agents/issue-tracker.md`.

Apply a category label when the tracker docs define one clearly, usually the label mapped from `enhancement` in `docs/agents/triage-labels.md`. Do not apply the label mapped from `ready-for-agent` to the parent PRD unless the user explicitly asks; `ready-for-agent` is reserved for implementation issues published by `$to-issues` or triage briefs that `$implement` can consume.

Do not split the PRD into implementation issues here. Do not close, relabel, or otherwise modify any parent source unless explicitly asked.

End by recommending `$to-issues` if the user wants implementation issues.

## Completion Criteria

Done means the user-approved PRD is published through the configured tracker; every gathered source item is represented once, marked out of scope, or intentionally omitted as irrelevant; repo vocabulary and ADR conflicts are reflected where applicable; and no implementation issues, unapproved tracker mutations, implementation-ready labels, parent-source changes, or new requirement interviews were introduced.
