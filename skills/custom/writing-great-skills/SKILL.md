---
name: writing-great-skills
description: Create, review, or edit Codex skills for predictable invocation, one owner, deliberate composition, sharp context pointers, strong leading words, proportional gates, and pruning.
---

# Writing Great Skills

**Predictability:** same process, variable output.

## Load The Right Reference

For bounded work, trace only affected surfaces. For a pack-wide audit, trace source, `agents/openai.yaml`, disclosed files, upstream, callers, routers, composers, owned outputs, mutation boundaries, and installed mirrors.

Read [GLOSSARY.md](GLOSSARY.md) completely for a full audit. For bounded work, read only the owning sections:

- invocation or description: `Invocation` and `Leading Word`;
- structure or splitting: `Information Hierarchy`;
- pruning: `Pruning` and the relevant failure mode;
- completion drift: `Completion Criterion`, `Legwork`, and `Premature Completion`.

## Delegation

**Delegate legwork:** For pack-wide audits, invocation authorizes direct subagents without separate confirmation. Give each one bounded, read-only evidence lane. Use `fork_turns="none"` when independent judgment matters; direct children do not spawn. Subagents return evidence; the root owns required source reading, judgment, synthesis, edits, verification, and completion.

## Audit Spine

1. **Choose.** Choose implicit or explicit-only reach and record it in `agents/openai.yaml`. For implicit reach, front-load one trigger per real branch and collapse synonyms. For explicit-only reach, keep the description human-facing and route it through a router.

2. **Own.** Give every behavior one owner. The owner keeps its rules, gates, output, mutation boundary, and completion criterion. Compose only when the owner permits caller composition. Route by naming one next skill and stopping.

3. **Arrange.** Keep common-path steps and compact universal reference in `SKILL.md`. Disclose branch-only reference through a sharp context pointer. Split only when the cut earns its context or cognitive load through distinct invocation or observed premature completion after a sharp criterion.

4. **Collapse.** Collapse repeated meaning into a pretrained leading word. Repeat the word, not its explanation. Keep non-intuitive Codex mechanics, gates, outputs, mutation boundaries, and completion explicit with their owner. Callers name the owner and handoff.

5. **Gate.** Give each common-path step a checkable result. Keep approval and mutation boundaries explicit. Add a failure branch only when it changes the safe next action in a representative workflow.

6. **Hunt.** Hunt duplication, no-ops, defensive narration, hypothetical recovery, and examples that teach no non-default judgment. Delete them or collapse repeated meaning into a leading word. Keep non-intuitive Codex mechanics explicit. Add no status, packet field, file, or skill unless it removes more complexity than it creates.

7. **Verify.** Recheck affected surfaces and representative workflows. For a pack-wide audit, verify each active relationship once. Confirm that references resolve, invocation policy matches the description, and installed mirrors match when synchronization is in scope.

## Mode Gate

Review-only stays read-only. When edits are authorized, change the declared source of truth first, validate it, then synchronize installed mirrors only when that surface is in scope.

The root owns skill-authoring judgment. The caller owns task mode, product decisions, and mutation scope.

## Audit Output

For a full audit, return the verdict, highest-impact findings, exact fixes, deliberate non-changes, and behavior at risk. For bounded work, return only applicable findings.

## Completion Criteria

Complete when common-path invocation, ownership, composition, mutation boundaries, outputs, and completion criteria are unambiguous, and affected surfaces verify. Stop before enumerating hypothetical failures.
