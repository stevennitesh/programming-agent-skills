---
name: ultra-model-routing
description: Route subagent models alongside native Ultra delegation, including final review before PR delivery. Exclude changing the lead or installing runtime configuration.
---

# Ultra model routing

Preserve the user's selected lead model, effort, and native delegation mode.
Native orchestration owns useful assignments, parallelism, communication, and
integration within task authority and repository constraints. Use
[controlled-delegation](../controlled-delegation/SKILL.md) instead when controlled delegation
with a smaller team and waiting lead is wanted. Choose one execution arrangement
for the same work.

## Route assignments

Read [Shared model routing](../controlled-delegation/references/model-policy.md)
before selecting child models and efforts, and follow its classification,
override, and availability rules. Loading shared references does not import
controlled team limits or waiting rules. Keep small work direct when delegation
would add more work than it saves.

Use [Native spawning](../controlled-delegation/references/native-spawning.md) for host
controls, fresh-child context, and selection evidence. Carry the assignment's
authority, routing, and execution rules into authorized descendants. Reuse
suitable workers for coherent follow-ups; preserve repository custody and
concurrency requirements.

## Review and deliver

Use [change-review](../change-review/SKILL.md) for candidate assessment and repairs.
Choose useful interim review rather than adding a review after every edit.

Before opening an authorized PR, complete **three sequential final-review rounds**
unless the user changes that requirement. Read
[Final review](references/final-review.md) for round progression and successor
verification. Concurrent reviewers form one round.

The lead retains final acceptance. Return candidate identity, review coverage,
required checks, and material limits. Review does not grant publication, merge,
or deployment authority; [pr-delivery](../pr-delivery/SKILL.md) owns the requested
delivery endpoint. Work without requested PR delivery acquires no PR-opening task.
