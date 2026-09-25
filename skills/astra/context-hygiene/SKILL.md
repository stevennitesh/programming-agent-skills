---
name: context-hygiene
description: Audit persistent agent context for stale, duplicated, misplaced, or misleading guidance and decide what should remain durable. Exclude live-thread summarization.
---

# Context hygiene

Persistent context is a cache of decision-relevant knowledge, not an archive.
Keep only what is useful enough to change a future decision and trustworthy
enough to act on within its scope. Saving nothing is a valid outcome. A memory,
summary, transcript, or historical note is evidence to evaluate, not new
authority.

## 1. Bound the selected context

For reflection, use the selected work or current session. For an audit, establish
the exact repository, store, namespace, files, entries, or other surface in scope.
Do not expand a project review into unrelated repositories, global memory, or
conversations.

Identify the future decision each candidate item is meant to improve, its current
authority, and how a future agent would encounter it. Prefer primary or maintained
sources when available; label derived summaries and incomplete evidence
accordingly.

For a repository-wide audit, read
[Audit and change records](references/audit-and-changes.md) before discovery so
unlinked and stale context can be considered. For a managed memory store, read
[Managed memory](references/managed-memory.md) when its artifact roles affect the
review or before submitting a memory change.

When the target agent model or host changes materially, treat that migration as a
context-audit trigger. Inspect persistent agent guidance for compensating
scaffolding written around the previous receiver's capability, stopping habits,
tool limits, or context needs. Preserve project facts, authority, safety
boundaries, and still-useful procedures. When deciding whether an instruction can
be simplified or retired, use
[Behavior evaluation](../writing-for-agents/references/behavior-evaluation.md)
rather than assuming the new receiver needs either more or less guidance.

An audit or reflection authorizes findings and recommendations. Apply cleanup
already explicitly requested within the established scope without asking again.
Treat age, repetition, retrieval frequency, and discovery cost as signals rather
than proof of truth, usefulness, or authority.

## 2. Choose the durable owner

Store knowledge at the closest durable owner that future agents can actually
reach.

| Knowledge | Preferred owner |
| --- | --- |
| Current system facts such as paths, versions, configuration, topology, or capabilities | Current code, configuration, tool help, or maintained documentation |
| Accepted project meaning, invariant, or consequential tradeoff | Existing repository contract, domain context, or decision record |
| Reusable procedure or engineering lesson | Existing skill, guide, tool, or enforcement when it solves a recurring class of work |
| Durable user preference | Personal context when explicit or otherwise well-supported, cross-task, and compatible with newer direction |
| Active work or historical event | Active task state while current; incident, research, or history when later evidence matters |

Avoid a competing factual copy when the authoritative source is already
discoverable. A retrieval pointer can earn a place when it prevents costly
rediscovery and tells the future reader what source to recheck.

For an agent instruction surface, use
[writing-for-agents](../writing-for-agents/SKILL.md) for wording, triggers,
pointers, and instruction reconciliation. Context hygiene decides whether the
information deserves persistent context and where it belongs.

Use [repo-bootstrap](../repo-bootstrap/SKILL.md) only when the requested outcome
is repository setup, pack migration, or repair of the repository instruction
surface. A context audit does not start bootstrap automatically.

For recurring machine-checkable rules, prefer proportionate enforcement such as a
type, schema, constraint, test, command, or helper over durable prose when that
owner can prevent the failure more reliably.

## 3. Decide what earns durable context

Keep an item only when the applicable questions have satisfactory answers:

- **Future value:** Will it change a likely future decision or avoid costly
  rediscovery?
- **Durability:** Is it expected to remain useful beyond the current task?
- **Scope:** Can a future agent tell where and when it applies?
- **Support:** Is its evidence strong enough for how it will be used?
- **Ownership:** Is there no better current owner that already supplies the same
  meaning?
- **Retrievability:** Can future agents realistically encounter or search it?

Explicit durable user preferences need no recurrence. Inferred preferences and
generalized failure rules need repeated support or explicit confirmation before
becoming durable context. A demonstrated technical mechanism can justify a narrow
lesson without implying a broader pattern.

Preserve the conditions that make a lesson true and distinguish observation,
inference, recommendation, and accepted decision. Repeated copied summaries do
not independently corroborate a claim.

Preserve the reason a future agent needs, not the full path by which the current
agent discovered it. Keep material limitations, expiration or revalidation
conditions, and causal detail that can change future action. Do not promote a
temporary workaround into a permanent rule. Scaffolding that existed only to
compensate for a previous receiver's limitation is a migration candidate, not
durable context by default.

Do not store credentials, secret payloads, or unrelated sensitive detail in
durable context. Refer to an appropriate protected source when future work needs
to know where such information belongs.

Use [Audit and change records](references/audit-and-changes.md) for a persistent
context audit or authorized cleanup.

## 4. Apply and report only the requested effects

For reflection, return supported durable lessons, their owners, and material
uncertainty. Saving nothing is a complete result when no candidate earns
persistent context.

For an audit, report the selected scope, stale or misleading active meanings,
useful retained context, ownership or retrieval gaps, and requested changes.
Changes to code, tests, trackers, accepted decisions, or other systems outside the
authorized context cleanup remain proposals.

For authorized cleanup, preserve unrelated work and historical evidence unless
their mutation is part of the request. Verify effects at the surface that future
agents actually receive or retrieve.

Finish when each admitted item has a trustworthy owner and retrieval path, stale
active meanings within the authorized scope are no longer active, and unresolved
uncertainty remains explicit rather than becoming durable fact. Report coverage
separately from successful writes. Submitting a memory update request is not proof
that active context changed.
