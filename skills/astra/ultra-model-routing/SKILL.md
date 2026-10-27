---
name: ultra-model-routing
description: Route subagent models alongside native Ultra delegation, including final review before PR delivery. Exclude changing the lead or installing runtime configuration.
---

# Ultra model routing

Preserve the user's selected lead model, effort, and native delegation mode.
Use this policy alongside a Sol 6.1 Ultra lead when that is the user's selection.
Let native orchestration choose useful assignments, parallelism, communication,
and integration within the task's authority and repository constraints.

Keep model allocation with this skill for the selected task. The
[cost-aware-coding](../cost-aware-coding/SKILL.md) execution workflow is a separate
choice; do not apply its competing routes and worker pipeline to the same work.

Apply the routes below to newly scoped subagent assignments. Keep planning and
final acceptance with the lead; give workers freedom over methods within their
assignments. Keep a small task direct when delegation would add more work than
it saves. This skill does not select Ultra or change the active session.

## Assign model and effort together

| Delegated assignment | Model | Effort |
| --- | --- | --- |
| Substantive coding, debugging, investigation, and reasoning | `gpt-6.1-sol` | `high` |
| Routine execution and defined bulk work with settled rules and observable acceptance | `gpt-6.1-terra` | `medium` |
| Interim review and final review | `gpt-6.1-sol` | `xhigh` |
| A specifically identified hard reasoning or review problem | `gpt-6.1-sol` | `max`, by deliberate escalation |

Use no Astra or Luna subagent routes or fallback routes under this policy.
Explicit user model instructions take precedence. Preserve the chosen model
versions; report an unavailable route instead of silently substituting another
family, version, or effort.

Read [Model policy](references/model-policy.md) when classification or escalation
needs judgment. Classify the assignment being delegated, not the size of the
parent project. Large, settled work can remain routine; a small unresolved
correctness question can require substantive reasoning.

## Delegate through the native tools

Read [Native spawning](references/native-spawning.md) before the first routed
spawn on a host, or when its tool contract or configuration changes. Use exposed
model and effort controls together. For the current Codex V2 contract, create
routed children with `fork_turns="none"` and a self-contained assignment.

Carry scope, accepted decisions, relevant source and candidate identities, write
ownership, verification obligations, and expected return into the assignment.
Give enough context for correct work; omit unrelated conversation history.
Preserve repository custody and concurrency requirements.

Reuse a suitable worker for coherent follow-ups and repairs. Reassess the route
for materially different work or a demonstrated reasoning limitation. If a
child delegates under applicable instructions, carry this routing policy and
the assignment's authority into its children.

Keep the native delegation policy active. This skill supplies no fixed worker
roster, single-writer execution pipeline, mandatory idle-lead period, or blanket
prohibition on further delegation. Select additional execution workflows only
when the task calls for the responsibility they own.

## Review and deliver

Use the review route for useful interim assessments; do not add a review after
every routine edit. Use [change-review](../change-review/SKILL.md) for candidate
identity, finding standards, evidence, and correction review.

Before an authorized PR is opened, complete **three sequential final-review
rounds**, unless the user explicitly changes that requirement. Read
[Final review](references/final-review.md) for independence, repairs between
rounds, and the final candidate condition. Parallel reviewers in one round do
not count as multiple sequential rounds.

Keep the lead's acceptance, required checks, and remaining material limits
visible in the final handoff. Review completion does not grant publication,
merge, or deployment authority; use [pr-delivery](../pr-delivery/SKILL.md) when
that delivery endpoint is requested. A task without requested PR delivery does
not acquire a PR workflow merely by using this routing policy.

Report material routing or verification limits accurately. Instructions and
package validation do not establish actual runtime enforcement, lower cost, or
quality parity with stock Ultra.
