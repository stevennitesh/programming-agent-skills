---
name: handoff
description: Compact the live thread into a resumable handoff for a fresh Codex session or agent thread.
---

# Handoff

**Trace -> Snapshot -> Compact -> Redact -> Save -> Verify -> Return**

**Trace.** Resolve `<work-root>` as the Git root when present, otherwise the current directory. Target `<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>.md`. In a Git repo, confirm the target is ignored before writing; otherwise recommend `$repo-bootstrap` and stop. Read the live thread and named artifacts.

**Snapshot.** Verify volatile repo and workflow state. Verify every pointer or mark it explicitly unverified. Label facts, inferences, and unknowns; leave new evidence and task work to the receiving session.

**Compact.** Preserve only state expensive to recover from the Source Trace, using the active workflow's vocabulary. A supplied focus sets Purpose and Next Step without hiding any blocker, risk, unresolved decision, or state needed to resume safely.

```markdown
# Handoff

## Purpose
Continuation, decision, or proof target.

## Current State
Complete, in-progress, intentionally unchanged, and blocked state; active workflow and exact phase or gate. For repo work: cwd/worktree, branch or detached HEAD, relevant commit, staged/unstaged scope, material untracked files, and unrelated-dirty-work ownership.

## Key Decisions
Confirmed and rejected decisions, constraints, scope boundaries, and commitments awaiting approval.

## Source Trace
Exact pointers to durable truth and intentionally preserved `.tmp/` or tracked `.scratch/` artifacts. Reference; do not copy.

## Validation
Commands/checks, outcomes, proof, skips, gaps, and residual risk.

## Open Questions
Question, known evidence, and decision unlocked.

## Next Step
One executable, workflow-native action with target and stopping point.

## Suggested Skills
Receiving-session skills with one-line reasons, or `None`.
```

**Redact.** Remove secrets, credentials, and personally identifiable information.

**Save.** Create `.tmp/` when absent and write exactly the target artifact. The invocation authorizes only those changes. Keep the file outside the index and commits; leave tracked files, tracker state, Git state, the active workflow, and Codex tasks unchanged. Suggested skills remain unexecuted.

**Verify.** Reread until the file is source-traced, redacted, actionable, current, pointer-exact or explicitly unverified, ignored when Git applies, and the only authorized state change.

**Return.** Report the absolute path and:

> Continue from `<absolute-path>`. Read the handoff first, then execute its Next Step.

Append a redacted one-line form of any supplied focus to the pickup prompt.
