---
name: writing-great-skills
description: Create, review, or edit Codex skills for predictable invocation, single ownership, composition, context disclosure, leading words, gates, and pruning.
---

# Writing Great Skills

**Predictability:** same process, variable output.

## Reference

Read [GLOSSARY.md](GLOSSARY.md) completely for a full audit. For bounded work, load the owning headings: `Invocation` and `Leading Word`; `Information Hierarchy`; `Pruning` and its failure mode; or `Completion Criterion`, `Legwork`, and `Premature Completion`.

## Delegation

**Delegate legwork:** For pack-wide audits, invocation authorizes direct subagents without separate confirmation. Give each one bounded, read-only evidence lane. Use `fork_turns="none"` when independent judgment matters; direct children do not spawn. Subagents return evidence; the root owns required source reading, judgment, synthesis, edits, verification, and completion.

## Audit Spine

1. **Trace.** Trace only affected surfaces. A full audit covers canonical source, `agents/openai.yaml`, disclosed files, current upstream, callers, routers, composers, handoffs, outputs, mutation boundaries, tests, evaluations, relationship maps, and installed mirrors. Review-only stays read-only.

2. **Choose.** Choose implicit or explicit-only reach in `agents/openai.yaml`. For implicit reach, front-load one trigger per branch. For explicit-only reach, keep the description human-facing and route it through a router.

3. **Own.** Give each behavior one owner for its rules, gates, output, mutation boundary, and completion criterion. Compose only when the owner permits it. Callers name the callee, trigger, and return boundary; routers name one next skill and stop.

4. **Arrange.** Keep common-path steps and compact universal reference in `SKILL.md`. Give each step a checkable, proportional result. Co-locate each concept. Disclose branch-only reference through a sharp context pointer. Split only for distinct invocation or observed premature completion after a sharp criterion.

5. **Prune.** Collapse repeated meaning into a pretrained leading word; repeat the word, not its explanation. Test no-ops sentence by sentence and delete failures. Keep only non-intuitive mechanics; semantic and safety contracts; scope, approval, ownership, and mutation boundaries; required outputs and proof; irreversible sequencing; and completion criteria. Keep a failure branch inline only when it changes the safe next action.

6. **Verify.** Recheck affected surfaces and representative workflows. Confirm references resolve, invocation matches policy, and each affected relationship verifies once. For authorized edits, change the declared source first, validate it, then synchronize in-scope installed mirrors.

## Output

A full audit returns the verdict, impact-ordered findings, exact fixes, deliberate non-changes, and behavior at risk. Bounded work returns only applicable findings.

## Completion

Complete when invocation, ownership, composition, mutation boundaries, outputs, proof, and completion criteria are unambiguous, and affected surfaces verify.
