---
name: to-issues
description: Create approved, dependency-ordered ready-for-agent issue slices from source material.
---

# To Issues

Default to **tracer bullets**: independently-grabbable vertical slices through the real system, each demoable or verifiable on its own. Use **support issues** only when they clearly unblock or de-risk a named tracer bullet; otherwise reject horizontal slices, speculative prefactoring, and cleanup-only slices.

## Preconditions

Setup gate: read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either is missing, stop and recommend `$setup-matt-pocock-skills`; do not recreate tracker or label guidance here.

## Process

### 1. Resolve The Source

Source trace: use repo `AGENTS.md`, repo-local agent docs it names, direct source material, source-linked comments/documents, and explicit user approvals. If a needed decision is outside that trace, ask.

If the user passed a PRD, spec, issue number, URL, or file path, fetch and read that source plus comments and directly linked context named by the source.

Identify parent source, user-facing outcome, accepted decisions, out-of-scope boundaries, and prototype findings from the source trace.

### 2. Map The Work

Explore only enough traced codebase context to name stable seams, validation surfaces, and support issues that materially de-risk later tracer bullets. Do not design the patch or assign exact files.

### 3. Draft Independently-Grabbable Slices

Split the work into dependency-ordered issues.

Each issue must be independently grabbable: one observable proof, explicit blockers, independent validation, enough context for a fresh session, and a parent link instead of duplicated source.

Tracer-bullet issues deliver one narrow, demoable or verifiable behavior across every needed layer. Support issues name the later tracer bullet they unblock or de-risk and how completion is proven.

Cut issues only for materially distinct behaviors, branches, failure modes, permission boundaries, state transitions, integration seams, migration risks, or support work required by a named tracer bullet. If no end-to-end path exists, start with the happy path. Do not split by layer, file, task type, or data variation alone.

Each issue should include:

- Parent reference
- Why this slice
- What to build: end-to-end behavior or support change, not layer-by-layer steps
- Acceptance criteria: specific, observable proof
- Blocked by
- Expected write scope: durable modules, interfaces, commands, docs, or "discover during implementation" when unknown
- Parallel safety: independent after blocker / overlaps with sibling issues / serialize because...
- Relevant context: glossary terms or ADR pointers when known

Use traced domain vocabulary. Avoid file paths and code snippets unless they are durable contracts or prototype findings; trim prototype material to the decision-rich part and say it came from the prototype.

### 4. Review With The User

Show the proposed breakdown before publishing:

```markdown
1. <Issue title>
   Blocked by: <none / issue title>
   Covers: <user stories or behavior>
   Why this slice: <one sentence>
   Parallel safety: <independent after blocker / serialize because...>
```

Ask the user to approve granularity, order, blockers, and parallel safety. Iterate until approved. Do not publish before approval.

### 5. Publish

Publish approved issues in dependency order, blockers first.

Publish target: use `docs/agents/issue-tracker.md` commands. Apply the mapped `ready-for-agent` state label and required category label from `docs/agents/triage-labels.md`, unless the user says otherwise.

Local packet: follow the repo's documented packet convention. If none exists, stop and ask whether to publish to the configured tracker or add a local tracker convention. Do not invent a packet layout here. The README records parent, child issues, issue order, dependency shape, source trace, and durable context pointers; child files own readiness, blockers, and closeout state.

Boundary: do not modify the parent source, triage existing issues/PRs, or launch implementation, review, or closeout here. Recommend `$triage`, `$implement`, or `$parallel-implement` when that is the next workflow.

## Completion Criteria

Done means approved ready-for-agent issues are published in dependency order, required labels are applied, blockers are explicit, write scope, parallel safety, and relevant-context pointers are recorded when known, packet index pointers are added when applicable, and the parent source is unchanged unless the user asked otherwise.
