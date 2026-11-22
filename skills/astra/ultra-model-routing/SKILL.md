---
name: ultra-model-routing
description: Route subagent models alongside native Ultra delegation, including final review before PR delivery. Exclude changing the lead or installing runtime configuration.
---

# Ultra model routing

Preserve the user's selected lead model, effort, and native delegation mode.
Native orchestration chooses how to assign and coordinate work within task
authority and repository constraints. This skill supplies child model routes
and the pre-PR review sequence. Use
[controlled-delegation](../controlled-delegation/SKILL.md) when the user wants
one primary worker and a waiting lead.

## Route assignments

Use [Shared model routing](../controlled-delegation/references/model-policy.md)
to select model and effort for each coherent assignment when dispatching it.
Keep small work direct when the handoff adds more work than it saves. Keep
routine steps and verification with the worker when the routing policy supports
it. Reuse workers while their route still fits. Resolve missing inputs or tooling
at the source. Seek Astra design advice before implementation when independent
judgment could change a decision with substantial rework at stake.

Follow [Native spawning](../controlled-delegation/references/native-spawning.md)
for host controls, worker context, and selection evidence. Pass the relevant
authority and routing rules to authorized descendants, and preserve repository
custody and concurrency requirements.

## Review and deliver

Use [change-review](../change-review/SKILL.md) for candidate assessment and
repairs. Add interim review when its answer can affect the work. Before opening
an authorized PR, complete one independent Sol review by default. Use
[Final review](references/final-review.md) for this gate or when the user
requests that review method. Honor the user's requested review arrangement.

The lead owns final acceptance. Report the candidate, evidence, and material
limits. Use [pr-delivery](../pr-delivery/SKILL.md) when PR delivery is authorized.
Publication, merge, and deployment require authority for those effects.
