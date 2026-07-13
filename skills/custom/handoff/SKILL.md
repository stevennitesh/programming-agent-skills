---
name: handoff
description: Compact the live thread into a resumable handoff for a fresh Codex session or agent thread.
---

# Handoff

Create a **compaction**: preserve the live thread's resumable core while durable artifacts remain the source of truth.

## Boundary

Write exactly one artifact at `<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>.md`. Resolve `<work-root>` as the Git root when present, otherwise the current working directory. Create `.tmp/` when absent. In a Git repo, confirm the target is ignored before writing; otherwise stop and recommend `$repo-bootstrap`.

The invocation authorizes only that handoff artifact. Keep it outside the Git index and commits. Leave tracked workspace files, the tracker, Git state, the active workflow, and Codex tasks unchanged. Suggested skills remain instructions for the receiving session.

When the invocation includes a focus, make it the receiving session's Purpose and Next Step. The **focus gate** preserves every blocker, risk, unresolved decision, and state fact required to resume safely.

## Build The Handoff

Trace the live thread and its named artifacts. **Snapshot:** verify volatile state and pointer exactness; mark unknowns, and leave new evidence trails and task work to the receiving session.

Use this structure:

```markdown
# Handoff

## Purpose

What the receiving session must continue, decide, or prove.

## Current State

What is complete, in progress, intentionally unchanged, and currently blocked.

Name the active workflow and its exact phase or gate.

For repo work, include the cwd or worktree, branch or detached HEAD, relevant commit, staged and unstaged scope, material untracked files, and ownership of unrelated dirty work.

## Key Decisions

Confirmed decisions, rejected options, constraints, scope boundaries, and commitments still requiring user approval.

## Source Trace

Exact paths, URLs, issue numbers, specs, plans, ADRs, commits, diffs, prototypes, intentionally preserved `.tmp/` artifacts, and tracked `.scratch/` artifacts the receiving session must read.

## Validation

Commands and checks run, their outcomes, proof gathered, skipped validation, missing proof, and residual risk.

## Open Questions

Unresolved questions, partial answers, evidence gaps, and the decision each answer would unlock.

## Next Step

One executable next action in the active workflow vocabulary, including its target and stopping point.

## Suggested Skills

Only the skills the receiving session should invoke, each with a one-line reason. Write `None` when no skill is needed.
```

## Compaction Rules

- **References, not copies:** Point to specs, plans, ADRs, issues, commits, diffs, and other durable truth instead of restating them.
- **Workflow-native:** Preserve the workflow actually in progress rather than translating every handoff into implementation.
- **Facts / Inferences / Unknowns:** Label confirmed state, interpretation, and uncertainty distinctly.
- **Redaction gate:** Remove API keys, passwords, tokens, private keys, credentials, secrets, and personally identifiable information.
- **Resumable core:** Carry only state the receiving session cannot recover cheaply from the Source Trace.

## Read Back And Return

Reread the saved file and verify:

- every load-bearing live-state fact is captured or source-traced;
- the output is under `<work-root>/.tmp/` and ignored when `<work-root>` is a Git repo;
- local paths, issue numbers, URLs, and commit identifiers are exact or marked unverified;
- repo and workflow state are current;
- durable truth was referenced rather than copied;
- secrets and personal data are absent;
- the Next Step is executable;
- Suggested Skills are justified.

Report the absolute path and this pickup prompt:

> Continue from `<absolute-path>`. Read the handoff first, then execute its Next Step.

When a focus was supplied, append it to the pickup prompt.

## Completion Criteria

Complete only when exactly one handoff file is saved under `<work-root>/.tmp/`, ignored when the work root is a Git repo, reread, redacted, and source-traced; the current workflow and conditional repo state are accurate; the Next Step and Suggested Skills are actionable; the absolute path and pickup prompt are returned; and no other state changed.
