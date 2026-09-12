---
name: cost-aware-coding
description: Run an Astra-led, Sol-implemented coding route. Use only when explicitly requested.
---

# Cost-aware coding

Use GPT-6 Astra Medium to lead and review while one persistent GPT-5.6 Sol
Medium task implements. The engineering contract owns coding quality; this skill
owns routing and exclusive repository custody.

## 1. Select the route

Before requesting a model switch or creating a task, check whether the remaining
implementation, test, or debug loop is large enough to repay the handoff and
review. For a trivial change or serial investigation where accumulated context is
the work, execute directly unless the user explicitly requires the pair.

Otherwise, a concrete implementation request that invokes this skill selects the
standard route without a separate proposal. Before first dispatch, reuse any
existing authorization for task creation and communication. If either is missing,
ask once for the missing scope; the user need not supply special prompt wording:

> May I create the Sol implementation task and let both tasks exchange
> task-relevant information and local file contents or references throughout
> implementation, review, and recovery?

Adapt this question when reusing an existing task or when part is already
authorized. This permission covers the named pair and repository; repository
custody and runtime approval requirements still apply.

Propose first when the user requests a proposal, substantial shaping remains unresolved,
you determine that a different lead model or effort is needed, or a requested constraint
requires another route.

Reuse accepted requirements, decisions, plans, and tickets. If substantial
feature behavior or approach remains unresolved, use
[shape-work](../shape-work/SKILL.md). Sol owns routine implementation choices.

The standard route is:

- **Astra Medium lead:** requirements, consequential decisions, assignment,
  escalation, review, and acceptance.
- **One persistent Sol Medium app task:** repository investigation,
  implementation, checks, debugging, and corrections.
- **One shared checkout with alternating custody:** only the current owner may
  access it.

Read [Model policy](references/model-policy.md) only for a different model,
escalation, or policy comparison. If the user requests concurrent implementation,
use [parallel-implement](../parallel-implement/SKILL.md), which owns isolation,
integration, and concurrent recovery. Agree the concurrent worker transport and
recovery route before dispatch; the single-task arrangement below is for serial
execution. Retain your integrated change-review gate and the shared repair limits.

If the user requests usage measurement or sets a hard budget, read
[Telemetry](references/telemetry.md) before dispatch. Capture any required start
observation then, and resolve an unenforceable hard-budget constraint before
execution. Ordinary runs do not load telemetry.

## 2. Give Sol custody

If your current setting does not match the accepted route or appears insufficient,
suggest the exact model and effort with the reason. The user applies that change;
you cannot change your own setting. Resume execution after the user switches.
Create or reuse one user-visible Sol Medium app task in the
same local project and checkout. Use a new task for an independent plan; reuse the
existing task for the same candidate, including corrections and recovery.

Read only what you need to settle intent and write the brief; leave implementation
exploration to Sol. Before dispatch, identify the checkout, baseline, and relevant
dirty state, your lead task ID/host, and a new assignment ID. Before the first
dispatch to a new Sol task, read
[Sol assignment contract](references/sol-assignment.md) and send its required
receiver instructions in the actual task prompt, including explicit permission
for scoped messages to your task.
Do not assert messaging authority beyond the user's authorized coordination.
Reuse the user-approved communication scope for follow-ups; do not repeat the
approval text or seek permission again merely because a new turn began.
Runtime approval requirements still apply.
Reuse the contract for the same candidate; later messages carry only changed
assignment details. Do not merely
point Sol to this skill or reference.

For the shared-checkout pair, transfer repository custody with the brief. While
Sol holds custody, do not read repository files or diffs, search the codebase, run
shell, Git, build, or test commands, or edit product code. You may answer
consequential questions from supplied context. Concurrent execution follows
`parallel-implement` custody instead.

Use `send_message_to_thread` for questions, answers, and candidate returns to the
known counterpart task. After dispatch or an answer that resumes Sol, end your
turn; its message resumes this workflow without another user instruction.
Dispatch is not completion: report implementation running and review pending.
If message-driven resumption is unavailable, use completion waits with cursors
instead of repeated status reads; ending a turn does not schedule a fallback check.

Answer a matching question without repository access while Sol retains custody.
If inspection is needed, request release and wait for confirmation before inspecting;
then answer and explicitly grant custody back. A release must confirm stopped
writers and subprocesses; idle status alone is not release. Keep messages to
assignments, consequential questions/answers, returns, and necessary recovery.
Batch related questions and findings without delaying blockers or custody
transitions. Omit messages that only acknowledge receipt.

Match messages to the current assignment and process each candidate return once.
For an interrupted resume, stale or duplicate return, or uncertain custody, read
[Continuation](references/continuation.md).

## 3. Review and repair

A matching candidate return confirming stopped writers and released custody
normally permits review without a separate status check. Reconcile missing or
inconsistent evidence before repository access. Classify the return before review:
if it is blocked or required acceptance checks failed, follow
[Repair allowances](references/repairs.md). Review only a candidate returned ready
with its required checks satisfied. Then take custody and use
[change-review](../change-review/SKILL.md) without repeating routine exploration.
Add independent reviewers only when the accepted route or requested assurance
requires them; `change-review` owns their dispatch and convergence.

Send required corrections to the current accepted implementer with a new assignment
ID and explicit custody grant, then end your turn. Read
[Repair allowances](references/repairs.md) before dispatching the repair. A
stronger recovery follows its user-action and acceptance rules; do not silently
implement the correction.

## 4. Finish

Complete when the accepted outcome, required checks, and review gate pass. Report
the candidate, decisive evidence, and any material limitation. If telemetry was
requested, include its measured coverage and limits.
