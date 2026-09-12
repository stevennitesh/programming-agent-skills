---
name: cost-aware-coding
description: Run an Astra-led, Sol-implemented coding route. Use only when explicitly requested.
---

# Cost-aware coding

Use GPT-6 Astra Medium to lead and review, with one reusable GPT-5.6 Sol Medium
native subagent per coherent implementation plan. The engineering contract owns
coding quality; this skill owns routing and exclusive repository custody.

## 1. Select the route

Delegate when the remaining implementation and verification can repay the handoff.
For trivial changes or serial investigations where accumulated context is the work,
execute directly unless the user requires the pair. A concrete invocation selects
the standard pair; it needs no separate coordination proposal or messaging approval.
Ordinary action permissions still apply.

Reuse accepted requirements and plans. Use [shape-work](../shape-work/SKILL.md)
when substantial feature behavior or approach remains unresolved. You own shaping,
research decisions, consequential choices, and acceptance; Sol owns implementation
investigation and routine coding decisions.

If your setting needs changing, suggest the exact model and effort with the reason;
the user changes your setting. Read [Model policy](references/model-policy.md)
for escalation or a different route. Use a separate app task only when the user
requests its independent lifecycle; agree its transport and recovery then.
For requested concurrent implementation, [parallel-implement](../parallel-implement/SKILL.md)
owns isolation, scheduling, and integration; retain this skill's review and repair limits.
Read [Telemetry](references/telemetry.md) only for requested measurement or a hard
budget, capturing required starting observations before dispatch.

## 2. Assign Sol and wait

Read only enough to settle scope and prepare the brief. Use
[Sol assignment](references/sol-assignment.md) for the initial receiver instructions.
Give Sol exclusive checkout custody, leaving implementation exploration to it.
Reuse the same agent for the plan, questions, and corrections; phases alone do
not justify new agents. Start a fresh agent for an independent plan.

Use native `spawn_agent` with explicit `model="gpt-5.6-sol"` and
`reasoning_effort="medium"`. Prefer `fork_turns="none"` with a compact assignment;
use a bounded recent-turn fork only when it replaces useful context transfer.
Check the current tool schema for supported settings. Use exposed runtime metadata
to verify effective settings when available; otherwise report them as requested,
not verified. Do not infer settings from the conversation's starting model or
search conversation logs solely to confirm identity.

While Sol has custody, be idle by default. Do not read repository files or diffs,
search the codebase, run shell, Git, build, or test commands, or implement.
Use native `wait_agent` with 180-second event-driven waits, shortened only when
required by the runtime. Do not request routine progress, interrupt to check
progress, speculate about implementation, repeat acceptance criteria, or narrate
unchanged waiting. After a timeout, use only a minimal status check if the wait
result does not already establish status, then wait again while Sol is running.
A timeout is not a failed attempt. Do not assume ending your turn schedules continuation.

Act on consequential questions, candidate/blocker returns, user intervention,
or an actual error or interruption. Answer from supplied context; repository
access still requires explicit custody release. If higher-priority instructions
require commentary, give the shortest factual update; this does not justify
additional monitoring or analysis.

Use `followup_task` for blocking-question answers, custody-release requests, and
repair assignments: it handles both running and idle agents. Reserve `send_message` for necessary nonblocking
coordination, not routine progress requests. For a question, answer without repository access.
If you need inspection, request release and wait for confirmation that writers
and subprocesses stopped, then inspect, answer, and explicitly grant custody back.
Idle or interrupted status alone does not release custody. Follow runtime cleanup
requirements after a child finishes, retaining its ID for supported follow-ups;
cleanup is not a custody grant. Read [Continuation](references/continuation.md)
for interruption, errors, stale returns, or unavailable agents.

## 3. Review and repair

A matching return with stopped writers and explicit custody release permits you
to inspect the candidate without a redundant status check. Classify its evidence:
blocked or failed required checks follow [Repair allowances](references/repairs.md).
For a reviewable candidate, take custody and use [change-review](../change-review/SKILL.md),
reusing valid checks rather than repeating exploration. A required manual/platform
check may remain pending: review what is provable, but do not declare overall
completion until that gate passes or its owner explicitly revises it.
Add independent reviewers only when requested assurance requires them.

Send required corrections to the same Sol agent with changed context, the current
candidate, attempt stage, and explicit custody grant; resume waiting. Read
[Repair allowances](references/repairs.md) before repair or escalation. Do not
silently take over implementation. Replacement agents inherit remaining allowances.

## 4. Finish

Complete when the accepted outcome, required checks, and review gate pass.
Report the candidate, decisive evidence, and material limits. Distinguish
implementation ready for review from overall completion or pending manual proof.
Include bounded telemetry only when requested.
