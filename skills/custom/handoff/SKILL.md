---
name: handoff
description: Compact the live thread into one verified local continuation packet for a fresh Codex context that can access the same work root.
---

# Handoff

**Trace -> Snapshot -> Compact -> Redact -> Save -> Verify -> Return**

**Trace.** Admit only an intended fresh session or agent thread whose receiver
can read the same work root and required local sources. For same-conversation
compaction or an ordinary live-workflow Return, report `not-created` with
`/compact` or the active owner; when receiver access cannot be established,
report `not-created` with the transport mismatch. Resolve `<work-root>` as the
Git root when present, otherwise the current directory. Select the first unused
`<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>[-<NN>].md`; never overwrite. In a
Git repo, confirm the exact target is ignored before writing; otherwise
recommend `$repo-bootstrap`, report `not-created`, and stop. Read the live
thread, active workflow, and named sources as evidence, not new authority.

**Snapshot.** Refresh volatile repo and workflow state, including the active
owner, exact phase or gate, selected work identity, authority, and unrelated
dirty-work ownership. Verify every pointer and material identity or mark it
explicitly unverified. Label facts, inferences, unknowns, and unstable state;
leave new evidence and task work to the receiver.

**Compact.** Preserve only state expensive to recover from the Source Trace,
using the active workflow's vocabulary. A supplied focus sets Purpose and Next
Step without hiding any blocker, risk, unresolved decision, or state needed to
resume safely.

```markdown
# Handoff

## Purpose
Continuation, decision, or proof target; completion and stopping boundaries.

## Current State
Complete, in-progress, intentionally unchanged, and blocked state; active owner, workflow, exact phase or gate, and selected work identity. For repo work: cwd/worktree, branch or detached HEAD, relevant commit, staged/unstaged scope, material untracked files, and unrelated-dirty-work ownership.

## Key Decisions
Confirmed and rejected decisions, constraints, commitment and scope boundaries, approvals, and authority still required.

## Source Trace
Exact pointers to durable truth and intentionally preserved `.tmp/` or tracked `.scratch/` artifacts, with owner, identity or revision, verification status, and `read first` or `conditional` priority. Reference; do not copy.

## Validation
Commands/checks, outcomes, proof identity, skips, gaps, residual risk, and the exact condition that requires proof to rerun.

## Open Questions
Question, owner, known evidence, and decision unlocked, or `None`.

## Next Step
Exactly one workflow-native re-entry action with owner, target, refresh preconditions, expected evidence, and stopping point. Do not execute it in Handoff.

## Suggested Skills
Only the active owner or an already-selected supporting skill with a one-line reason, or `None`. Do not route here.
```

**Redact.** Remove secrets, credentials, and personally identifiable information
while preserving the dependency type and operational impact.

**Save.** Create `.tmp/` when absent and write exactly the unused target
artifact. The invocation authorizes only those changes. Keep the file outside
the index and commits; leave tracked files, tracker state, Git state, the active
workflow, and Codex tasks unchanged. Suggested skills remain unexecuted.

**Verify.** Reread the artifact and refresh material volatile state. Reconcile
drift into the same file or mark it unstable with a receiver precondition.
Finish only when the file is source-traced, redacted, actionable, pointer-exact
or explicitly unverified, ignored when Git applies, and the only authorized
state change. If safe completion fails, remove only incomplete Handoff-authored
state and return `not-created` or `blocked` without a pickup.

**Return.** Report the absolute path and:

> Continue from `<absolute-path>`. Read the handoff and current repo instructions, refresh its volatile Current State, then execute its Next Step only if its authority and preconditions still hold.

Append a redacted one-line form of any supplied focus to the pickup prompt. Do
not create or message the receiving task, invoke a suggested skill, or execute
the Next Step.
