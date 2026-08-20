---
name: handoff
description: Compact the live thread into one verified local continuation packet for a fresh Codex context that can access the same work root.
---

# Handoff

Create one verified local continuation note without advancing the work.

## 1. Qualify

Use Handoff only for an intended fresh task or context that can read the same
work root and required sources. Use `/compact` within the same conversation;
use the active workflow's Return for ordinary continuation.

Resolve the work root as the Git root when present, otherwise the current
directory. Choose the first unused
`<work-root>/.tmp/handoff-<YYYYMMDD-HHMMSS>[-<NN>].md`; never overwrite it. In
a Git repository, prove the exact target is ignored before writing. If the
disposable-artifact setup is missing, recommend `$repo-bootstrap` and stop
without creating a pickup. Create `.tmp/` when it is absent; in Git, do so only
after proving the target ignored. Stop when receiver access is not credible.

## 2. Gather

Refresh the current workflow and repository state. Preserve only information
whose loss could cause repeated work, a wrong mutation, false evidence, or an
authority mistake: the objective and stopping boundary, completed and pending
work, decisions and constraints, blockers and required authority, material
dirty work, decisive source and proof pointers, and the next already-legal
action or the condition that would make one legal.

When they affect resumption, include the exact selected work and gate,
worktree, branch, and HEAD identities, plus the scope and owner of dirty work.

A supplied focus changes emphasis, not scope or authority. Treat completed,
verified work as inherited evidence. Repeat discovery or proof only when its
identity is missing, relevant state has drifted, evidence conflicts, or an
applicable repository or workflow condition requires a rerun. Mark material
uncertainty instead of filling it with inference.

## 3. Write

Write one concise note using these content groups:

```markdown
# Handoff

## Purpose and boundary
Objective, completion and stopping boundaries, and current owner.

## State, decisions, blockers, and authority
What is done, pending, unchanged, or blocked; accepted constraints and authority still needed.

## Sources and proof
Exact durable pointers, relevant identities, useful checks and outcomes, and material uncertainty.

## Next action and preconditions
One already-legal re-entry action and stopping point, or the condition that must be resolved first.
```

Reference durable truth instead of copying it. Redact secrets and credentials.
Include a personal identifier only when an exact local pointer or active
dependency needs it; otherwise redact it while preserving its operational
impact. Write only the Handoff artifact and its directory when absent. Do not
change tracked files, Git state, tracker state, the active workflow, or Codex
tasks.

## 4. Check

Reread the note as a cold receiver. Confirm that its pointers are usable or
explicitly unverified, its next action does not exceed current authority, and
the artifact is ignored when Git applies and is the only state change apart
from its newly created directory. Make verification a precondition for any
action that depends on an unverified pointer. Refresh material mutable state
once more; reconcile drift in the note or make it a receiver precondition. If
completion fails, remove only incomplete state created by this invocation and
return the reason without a pickup.

## 5. Return

Return the absolute path and tell the receiver to read the note and current
repository instructions, then refresh state and authority before acting. Do
not create or message the receiving task, invoke a skill, or execute the next
action.
