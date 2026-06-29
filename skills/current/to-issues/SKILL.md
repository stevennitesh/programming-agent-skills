---
name: to-issues
description: Break a PRD, spec, plan, or issue into dependency-ordered, independently pick-up-able bounded slices, preferring tracer-bullet vertical slices for product behavior.
---

# To Issues

Turn source material into implementation issues that an unattended Codex session can pick up one at a time.

Prefer **tracer bullets** for product behavior: narrow vertical slices through the real system that prove one observable behavior end to end. A tracer bullet earns its place by reducing uncertainty about behavior, a seam, or a risk.

A support issue is allowed only when it clearly unblocks or de-risks later tracer bullets. It must be bounded, independently verifiable, and have observable validation. Examples: behavior-preserving prefactoring, migration checkpoints, test harness work, compatibility proof, or operational wiring.

Prefer tracer bullets over support issues. Avoid horizontal slices like "add schema", "build API", or "make UI" unless they are support issues that clearly unblock later tracer bullets.

## Preconditions

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either is missing, run `$setup-matt-pocock-skills`.

When exploring code, read `docs/agents/domain.md` if present so issue titles, behavior descriptions, and acceptance criteria use the repo's domain glossary and respect relevant ADRs.

## Process

### 1. Resolve The Source

Use the current conversation unless the user passed a PRD, spec, issue number, URL, or file path.

If the user passed a source reference, fetch and read the full source, including comments, linked context, and prior decisions.

Identify the parent source, user-facing outcome, accepted decisions, out-of-scope boundaries, and prototype findings worth preserving.

### 2. Map The Work

Explore only enough code to understand the current shape, existing seams, likely test surface, and useful prefactoring.

If prefactoring or other support work is needed, make it its own first issue only when it is independently verifiable and clearly unblocks or de-risks later tracer bullets. Behavior-preserving support work must say so explicitly.

### 3. Draft Bounded Slices

Split the work into dependency-ordered issues.

Each issue must be bounded, complete, independently verifiable, include specific observable acceptance criteria, name blockers explicitly, and avoid stale file paths unless the path is itself the durable contract.

Tracer-bullet issues must deliver one narrow behavior and cross every layer needed for that behavior. Support issues must identify what they unblock or de-risk and what observable validation proves they are complete.

Every issue should let a fresh Codex session understand the slice and its acceptance criteria without rereading the whole PRD. Link or reference the parent instead of duplicating its full context.

Prefer fewer strong tracer bullets over many weak variations. Start with the happy path when nothing works end to end yet. Add another tracer-bullet issue only when it proves a materially distinct behavior, branch, failure mode, permission boundary, state transition, integration seam, or migration risk.

Stop splitting when remaining cases are data variations of the same behavior.

Each issue should include:

- Parent reference
- Why this slice
- What to build: the end-to-end behavior or support change, not layer-by-layer steps
- Acceptance criteria: specific, observable proof
- Blocked by

Use domain glossary vocabulary. Avoid file paths and code snippets unless they are durable contracts or prototype findings; trim prototype material to the decision-rich part and say it came from the prototype.

### 4. Review With The User

Show the proposed breakdown before publishing:

```markdown
1. <Issue title>
   Blocked by: <none / issue title>
   Covers: <user stories or behavior>
   Why this slice: <one sentence>
```

Ask whether the granularity, order, and dependencies are right. Iterate until the user approves the breakdown. Do not publish before approval.

### 5. Publish

Publish approved issues in dependency order, blockers first.

Default to the configured issue tracker from `docs/agents/issue-tracker.md`. Use that file's documented commands and apply the label mapped from `ready-for-agent` in `docs/agents/triage-labels.md`, unless the user says otherwise.

If the configured issue tracker is local markdown, or the user asks for local issues, create a local issue packet using the repo's existing convention. If none exists, use:

```text
docs/<feature>/issues/<workstream-slug>-<YYYY-MM-DD>/
  README.md
  01-short-issue-slug.md
  02-short-issue-slug.md
```

The local packet README records the parent source, readiness, issue order, and dependency shape. Add a pointer from the relevant docs index when one exists.

Do not close, relabel, or otherwise modify the parent source unless the user explicitly asks.

End by naming `$implement` as the next skill to run when the user wants an agent to pick up one ready issue.

## Completion Criteria

Done means approved issues are published in dependency order, blockers are explicit, and the parent source is unchanged unless the user asked otherwise.
