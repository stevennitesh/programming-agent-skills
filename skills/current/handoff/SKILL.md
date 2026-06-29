---
name: handoff
description: Compact the current conversation into a handoff document for a fresh Codex session or agent thread to pick up.
---

# Handoff

Write a handoff document so a fresh Codex session or agent thread can continue without rediscovering the conversation.

Save it as a timestamped markdown file in the OS temp directory, not the current workspace.

If the user passed arguments, treat them as the focus for the next session and tailor the handoff to that focus.

## What To Include

Use this structure:

```markdown
# Handoff

## Purpose

What the next session is meant to continue or decide.

## Current State

What has happened so far, what is finished, what is in progress, and what is known to be unchanged.

## Key Decisions

Decisions already made, rejected options, constraints, and scope boundaries.

## Artifacts

Paths, URLs, issue numbers, PRDs, plans, ADRs, commits, diffs, prototypes, or temp files the next session should read.

## Validation

Commands run, checks performed, results, skipped validation, and residual risk.

## Open Questions

Questions still unresolved, with any partial answers or relevant context.

## Next Step

The single most useful next action: open a file, run a skill, continue an issue, test a behavior, or ask the user a specific question.

## Suggested Skills

Skills the next session should invoke, with one-line reasons.
```

Do not duplicate content already captured in durable artifacts such as PRDs, plans, ADRs, issues, commits, or diffs. Reference them by path, URL, issue number, or commit SHA.

Redact sensitive information, including API keys, passwords, tokens, private keys, credentials, and personally identifiable information.

Keep the handoff factual. Separate what was confirmed from what is inferred or still uncertain.

## Completion Criteria

Done means the handoff file is saved in the OS temp directory, redactions are applied, durable artifacts are referenced instead of copied, the next step is concrete, suggested skills are included, and the saved path is reported to the user.
