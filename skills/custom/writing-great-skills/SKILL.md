---
name: writing-great-skills
description: Predictability lens for creating, editing, or reviewing Codex skills. Use when deciding invocation, ownership, composition, descriptions, information hierarchy, context pointers, leading words, gates, completion criteria, or pruning.
---

# Writing Great Skills

Make skill behavior **predictable**: the same process every run, with outputs free to vary.

## Load The Right Reference

Trace the declared source of truth, disclosed files, `agents/openai.yaml`, installed mirror, upstream counterpart, callers, routers, composers, owned outputs, and mutation boundary.

Read [GLOSSARY.md](GLOSSARY.md) completely for a full audit. For a bounded edit, read only the owning sections:

- invocation or description: `Invocation` and `Leading Word`;
- structure or splitting: `Information Hierarchy`;
- pruning: `Pruning` and the relevant failure mode;
- completion drift: `Completion Criterion`, `Legwork`, and `Premature Completion`.

## Audit Spine

1. **Invoke.** Decide implicit or explicit-only reach. Make the policy explicit in `agents/openai.yaml`. For implicit reach, front-load the description with one trigger per real branch. For explicit-only reach, keep the description human-facing and route discoverability through a router.
2. **Own.** Give every behavior one owner. The owner keeps its rules, gates, output, mutation boundary, and completion criterion. Compose by invoking an owner whose policy permits caller composition; route an explicit-only owner by naming one next skill and stopping.
3. **Arrange.** Keep universal steps in `SKILL.md`. Keep compact universal reference beside them. Move branch-only reference behind a sharp context pointer. Split a sequence only when visible later steps cause observed premature completion after its criterion is already sharp.
4. **Lead.** Prefer pretrained leading words that recruit the intended behavior. Repeat the word, not its explanation. Keep explicit wording wherever a leading word would merely imply an owner, gate, output, completion criterion, or handoff.
5. **Gate.** End every meaningful step with a checkable bound. Demand enough evidence to prevent plausible-but-unproven completion. Name failure, blocked, and partial-mutation outcomes.
6. **Prune.** Keep one source of truth. Delete duplication, sediment, and true no-ops. Move live branch detail; preserve behavior-bearing detail. State the positive target first and retain negation only for a hard guardrail.
7. **Verify.** Recheck every active surface and relationship. Confirm that pruning left behavior explicit, referenced files resolve, invocation policy matches the description, and the installed mirror matches when sync is in scope.

## Mode Gate

Honor review-only as read-only. When edits are authorized, change the declared source of truth first, validate it, then sync the installed mirror when that surface is in scope.

Own skill-authoring judgment. The caller owns task mode, product decisions, and mutation scope.

## Audit Output

Return:

1. Verdict and concise ratings
2. Behavior and leading words to keep
3. Findings ordered by impact
4. Exact replacement wording
5. Deliberate non-changes
6. Behavior at risk from pruning

## Completion Criteria

Complete only when every active invocation surface, owner, composition edge, context pointer, gate, output, mutation boundary, handoff, and completion criterion is accounted for; every upstream/custom difference is deliberate; each meaning has one owner; and pruning preserves behavior explicitly rather than by implication.
