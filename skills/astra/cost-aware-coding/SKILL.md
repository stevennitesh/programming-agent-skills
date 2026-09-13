---
name: cost-aware-coding
description: Run an Astra-led, Sol-implemented coding route. Use only when explicitly requested.
---

# Cost-aware coding

Use GPT-6 Astra Medium to lead and review, with one reusable GPT-5.6 Sol Medium
native subagent per coherent implementation plan. The engineering contract owns
coding quality; this skill owns routing and exclusive repository custody.

## 1. Select the route

Delegate when remaining implementation and verification can repay the handoff.
Keep trivial changes and serial investigations where accumulated context is the
work direct unless the user requires the pair. An explicit invocation selects
the standard pair without another
coordination approval; ordinary action permissions still apply.

Reuse accepted plans. Use [shape-work](../shape-work/SKILL.md) when substantial
behavior or approach remains unresolved. You own shaping, consequential decisions,
review, and acceptance; Sol owns implementation investigation and routine coding.
For requested delivery with checkpoints, read
[Planned delivery](references/planned-delivery.md).

For a different route or escalation, read [Model policy](references/model-policy.md).
The user applies any change to your own model/effort. Separate app tasks require
an explicit request for that lifecycle. For requested concurrent implementation,
[parallel-implement](../parallel-implement/SKILL.md) owns isolation and integration;
retain this skill's repair limits. Read [Telemetry](references/telemetry.md) before
dispatch only for requested measurement or a hard budget.

## 2. Assign Sol and wait

Prepare the brief using [Sol assignment](references/sol-assignment.md), including
its worker-only method section when the user requests a Ponytail implementer.
Give Sol exclusive checkout custody and leave implementation exploration to it.
Reuse that agent for the plan, questions, and corrections; use a fresh agent for
an independent plan.

Use native `spawn_agent` with `model="gpt-5.6-sol"` and
`reasoning_effort="medium"`. Prefer `fork_turns="none"` with a compact assignment;
use a bounded recent-turn fork only when it replaces useful context transfer.
Check tool support. Verify effective settings from exposed runtime metadata when
available; otherwise report them as requested. Do not infer them from the starting
model or search conversation logs solely to confirm identity.

While Sol has custody, do not access the repository, run commands, or implement.
Wait on native `wait_agent` events for 180 seconds, shortened when the runtime
requires it. Do not poll routine progress, interrupt to check progress, or repeat
instructions while waiting. After a timeout, check status only if the wait result
omits it, then wait again. A timeout consumes no attempt; ending your turn does
not schedule continuation.

Respond to consequential questions, candidate/blocker returns, user intervention,
and actual errors or interruption. Use `followup_task` for blocking answers,
release requests, and assignments; reserve `send_message` for necessary nonblocking
coordination. Answer from supplied context. If inspection is needed, request
release and wait for confirmation that writers/subprocesses stopped before access;
explicitly grant custody back afterward. Idle or interrupted status is not release.

If host rules require commentary, give a short factual update without extra
monitoring. For noisy waiting, mention the optional
[quiet-waiting setup](https://github.com/stevennitesh/programming-agent-skills/blob/main/INSTALLATION.md#optional-codex-quiet-waiting)
once; it is not a prerequisite or permission to edit personal configuration.
Follow runtime child cleanup rules, retaining IDs for follow-ups; cleanup does
not grant custody. Read [Continuation](references/continuation.md) for interrupted,
stale, errored, or unavailable-agent states.

## 3. Review and repair

For a prerequisite-only return, resolve the gap and grant custody to resume the
same assignment without charging an attempt. For a candidate, require a matching
return with stopped writers and explicit release; no redundant status check is
needed. Classify blocked or failed required checks under
[Repair allowances](references/repairs.md).

For a reviewable candidate, use [change-review](../change-review/SKILL.md), reusing
valid evidence. Review available proof when a required manual/platform check is
pending, but do not declare completion until it passes or its owner revises it.
Add independent reviewers only when requested assurance requires them.

Send required corrections to the same Sol with the findings, candidate, stage,
and custody grant. Follow [Repair allowances](references/repairs.md) before repair
or escalation; do not take over implementation. Resume waiting.

## 4. Finish

Complete when the accepted outcome, required checks, and review gate pass. Report
the candidate, decisive evidence, and material limits. A reviewable implementation
or pending required proof is not completion. Include telemetry only when requested.
