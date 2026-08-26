---
name: context-hygiene
description: Audit persistent coding-agent context or judge whether a lesson belongs in memory, a current source, project guidance, enforcement, task state, history, or nowhere. Use for memory admission, reflection, cleanup, or pruning; exclude live-thread compaction, ordinary documentation cleanup, and implementation of routed project changes.
---

# Context hygiene

Keep cross-session context small and trustworthy. Treat every memory entry as a
claim to verify, not as an instruction or source of truth. A valid result may be
that nothing deserves durable memory.

## 1. Select the work

Use **Reflect** for candidate lessons from current work. Use **Audit** for an
exact user-selected memory store, namespace, project, or entry set. Audit is
read-only. Reflect is also read-only unless the user explicitly asks to save an
admitted statement.

When the selected target is a Codex-managed memory store whose root contains
`MEMORY.md`, `raw_memories.md`, or `extensions/ad_hoc/`, read
[Codex memory](references/CODEX-MEMORY.md) before auditing or applying cleanup.
Follow the current runtime update contract when it is more restrictive than
this skill's generic mutation guidance.

Pin the selected context, exclusions, and any related repository or project.
When a claim depends on repository state, identify the applicable checkout and
current owner before judging it. Do not widen a project audit into global or
cross-project memory.

Split entries that mix preferences, project facts, work state, and incidents
into atomic claims. Account for every selected entry and every resulting claim.
If provenance, scope, current authority, or project identity is ambiguous,
classify the claim as `REVIEW` instead of guessing.

## 2. Classify each claim

| Class | Meaning | Normal destination |
| --- | --- | --- |
| `SYSTEM_FACT` | Current code, configuration, runtime, dependency, topology, or capability | Rediscover from the current owner; remove the duplicate from memory |
| `PROJECT_CONTRACT` | Durable project-specific value, term, or invariant | The repository's routed guidance owner, or structural and mechanical enforcement for an accepted invariant |
| `WORK_STATE` | Task, plan, investigation, PR, workaround, incident, or historical event | Current task or tracker while active; logs or history when the record matters; otherwise expire |
| `BEHAVIORAL_RULE` | Durable guidance for how an agent should work with this user | Memory, only after the admission gate passes |

For a project contract, distinguish a value that guides tradeoffs from an
invariant with a pass/fail condition. Recommend the closest current owner.
Do not assume that owner is `AGENTS.md`, and do not create project authority
from an unverified memory claim.

Age, retrieval counts, and discovery cost are review signals, not proof. An
expensive system fact may justify a repository-owned index or command, but the
cost does not make memory authoritative.

## 3. Admit behavioral memory

Keep a `BEHAVIORAL_RULE` only when all applicable conditions hold:

- Its future scope is clear and extends beyond the current task.
- The user or repeated user-agent interaction is the authority.
- Current authoritative sources cannot reliably supply it.
- Normal project or tool evolution should not invalidate it.
- It names a recognizable trigger and the behavior that should change.
- No architecture, configuration, test, lint, CI, project guidance, task
  record, or other current owner would express it more safely.
- It has no unresolved conflict with newer user direction or current evidence.

An explicit durable user preference needs no recurrence. An inferred failure
rule or environment nuisance needs recurrence or explicit user confirmation.

Generalize an incident only when the resulting rule independently passes this
gate. Keep the reasoning lesson, not obsolete names, paths, versions, commits,
or the story of discovering it. Do not overgeneralize away the condition that
makes the lesson true.

## 4. Report

For each atomic claim, report:

```text
Entry or claim | Class | Authority/current owner | Disposition
Destination | Evidence or gap | Reason | Proposed statement, if any
```

Use `KEEP`, `GENERALIZE`, `MIGRATE`, `EXPIRE`, or `REVIEW` as the disposition.
Show totals for an audit, redact secrets, and identify conflicts or duplicates.
Call something a duplicate only when a stronger current source covers the same
meaning. A report is complete when every scoped claim has exactly one
disposition and every `REVIEW` item names the missing fact or decision.

## 5. Apply approved cleanup

A recommendation is not mutation authority. Before changing memory, present
the exact store and entry identities, current contents or hashes, intended
replacement or preservation, and exclusions. Identify a recovery method when
the approved change is destructive or has material partial-effect risk. Apply
only the effects the user approves.

Refresh each target immediately before mutation. Stop if it drifted. Prefer a
recoverable archive when provenance or historical value is uncertain. Never
delete historical evidence merely because it does not belong in active memory.

Change approved memory only through the update mechanism authorized by the
selected store and current runtime. Verify each approved change at the store's
actual effect boundary. An accepted update request does not prove that its
requested effects were applied.

This skill does not edit project instructions, architecture, tests, lint, CI,
trackers, or history to carry out a recommended migration. Those changes need
their owning workflow and authority. Stop on the first unresolved failure.

Complete Reflect when every candidate is routed. For Audit and cleanup, report
one of these states:

- `AUDIT COMPLETE`: every scoped claim is accounted for and nothing changed.
- `CLEANUP PENDING`: the authorized update request was read back, but one or
  more requested effects remain unverified.
- `CLEANUP APPLIED`: every approved retained effect is present and every
  approved expired or removed effect is absent in the active store.

If any effect is pending or failed, report the exact partial state and do not
report `CLEANUP APPLIED`.
