---
name: cost-aware-coding
description: Delegate a substantial coding task to one implementation worker while the lead retains consequential decisions and final review. Use only when explicitly requested; exclude parallel implementation.
---

# Cost-aware coding

Delegate substantial implementation to one worker when the lead effort saved is
likely to exceed assignment, custody, and review overhead.

The lead owns consequential decisions, routing, and final acceptance. The worker
owns implementation investigation, coding, debugging, and checks within the
assignment. This skill defines a serial delegation contract, not a fixed model
pair.

## 1. Choose direct or delegated execution

Delegate when enough implementation and verification can proceed independently to
repay the handoff. Work directly when the task is small, accumulated lead context
is the work, or consequential decisions remain too entangled with implementation.

Explicit invocation still permits this cost judgment unless the user explicitly
requires delegation or a particular available worker route.

Reuse accepted requirements and plans. Use [shape-work](../shape-work/SKILL.md)
when consequential behavior or accepted meaning remains unresolved. Use
[parallel-implement](../parallel-implement/SKILL.md) when the user requests
concurrent implementation; this skill owns only one serial implementation worker.

Use a worker route explicitly selected by the user or supported by the current
host. Do not treat historical benchmark snapshots or model names as durable routing
authority. When usage measurement or a hard budget materially affects routing,
read [Telemetry](references/telemetry.md).

For coordinated delivery with meaningful checkpoints, read
[Planned delivery](references/planned-delivery.md).

## 2. Assign one worker

Read only enough to settle the assignment and its reserved decisions. Use
[Worker assignment](references/worker-assignment.md) to give the worker the
outcome, accepted context, scope, authority, checkout, acceptance, and return
contract it cannot safely infer. Do not assume the worker inherited the lead's
conversation or skill context.

Give one actor write custody of the delegated checkout at a time. While the worker
holds that custody, the lead must not mutate or perform conflicting inspection on
the same mutable state. Read-only work on independent immutable context is fine
when it cannot race with the worker.

Use the host's supported delegated-agent and event-driven wait/resume mechanisms.
Do not spend lead effort duplicating the worker's implementation investigation or
polling merely for progress. Respond to substantive questions, candidate returns,
failures, user intervention, or other events that require the lead.

If the lead must inspect or take over the delegated checkout, first obtain explicit
custody release and establish that worker-owned writers or subprocesses have
stopped. Idle, interrupted, or timed-out status alone does not establish release.

## 3. Review and recover

A reviewable return identifies the candidate, decisive checks and limits, and
releases write custody with worker-owned writers stopped.

Review the candidate with [change-review](../change-review/SKILL.md), reusing valid
candidate-bound evidence. Pending required proof remains incomplete until it passes
or its owner revises the requirement.

Return locally correctable implementation findings to the same worker when its
accumulated context remains useful. Read [Recovery](references/recovery.md) for
blocking questions, prerequisite failures, interruption, custody uncertainty,
worker replacement, or route failure.

Do not change worker route merely because requirements are incomplete, acceptance
is contradictory, permissions are missing, or the environment is broken. Resolve
those causes at their owner. Replace or escalate the worker only for a demonstrated
capability or recovery problem, subject to the user's route and budget constraints.

Do not silently take implementation ownership while delegation remains the
accepted route. If ownership changes, make the transfer explicit and reconcile
custody first.

## 4. Finish

Complete when the accepted outcome is present in the reviewed candidate, required
checks pass, and material evidence limits are resolved or explicitly owned.

Report the candidate, decisive evidence, and material remaining limits. Include
usage or cost telemetry only when requested or needed for a governing budget.
Review success does not authorize merge, publication, deployment, or other
external effects.
