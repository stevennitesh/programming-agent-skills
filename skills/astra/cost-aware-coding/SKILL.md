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
standard route without a separate proposal. If no reusable Sol task exists and
the user did not authorize creating one, ask only for that authorization. Propose
first when the user requests a proposal, substantial shaping remains unresolved,
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
integration, and concurrent recovery.

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
dirty state. Before the first dispatch to a new Sol task, read
[Sol assignment contract](references/sol-assignment.md) and send its required
receiver instructions in the actual task prompt. Reuse that contract for the same
candidate; later messages carry only changed assignment details. Do not merely
point Sol to this skill or reference.

For the shared-checkout pair, transfer repository custody with the brief. While
Sol holds custody, do not read repository files or diffs, search the codebase, run
shell, Git, build, or test commands, or edit product code. You may answer
consequential questions or wait. Use completion waits rather than routine
status reads. Concurrent execution follows `parallel-implement` custody instead.

Handle Sol questions and returns through the assignment contract. Answer
consequential questions without investigating the assigned implementation. Treat
custody as released only when Sol's return confirms that its writers and
subprocesses stopped. Keep cross-task messages to the brief, consequential
questions, candidate return, and review findings.

For a cross-turn run or uncertain custody, read
[Continuation](references/continuation.md).

## 3. Review and repair

A completed task status and the implementer's return normally establish that the
current implementer is idle and released custody. Check status separately only
when that evidence is missing or inconsistent. Classify the return before review:
if it is blocked or required acceptance checks failed, follow
[Repair allowances](references/repairs.md). Review only a candidate returned ready
with its required checks satisfied. Then take custody and use
[change-review](../change-review/SKILL.md) without repeating routine exploration.
Add independent reviewers only when the accepted route or requested assurance
requires them; `change-review` owns their dispatch and convergence.

Return required corrections to the current accepted implementer and transfer
custody before it edits. Read [Repair allowances](references/repairs.md). A
stronger recovery follows its user-action and acceptance rules; do not silently
implement the correction.

## 4. Finish

Complete when the accepted outcome, required checks, and review gate pass. Report
the candidate, decisive evidence, and any material limitation. If telemetry was
requested, include its measured coverage and limits.
