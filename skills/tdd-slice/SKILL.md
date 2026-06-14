---
name: tdd-slice
description: "Use when approved work changes caller-visible or user-visible behavior, adds a new behavior path, or an understood bug needs a new durable behavior or regression check."
---

# TDD Slice

One caller-visible behavior, one focused check, smallest source change.

## Rule

Use this only when approved work changes caller-visible behavior or an understood bug needs a new durable behavior check.

Do not use this as the default for every bug, refactor, or repeatable check. Use `diagnose-loop` when the failure is not understood, `codebase-cleanup` for behavior-preserving refactors, and `verify-before-done` for final claim wording.

First visible move:

```text
Behavior:
Caller/user:
Public or caller contract:
Focused check:
Existing check or new check:
RED needed: yes|no and why
```

Prefer an existing caller-facing check when it already covers the behavior. Write a new check only when behavior is missing, changed, or unprotected.

## Fast Path

Use when an existing caller-facing check already covers the behavior.

- State the behavior and check.
- Run the check before the change when preserving behavior, or use the reproduced failure from `diagnose-loop`.
- Make the smallest source change.
- Rerun the same check.
- Use `verify-before-done` for final done, fixed, passing, ready, or covered claims.

Stop there unless the change expands behavior, weakens the check surface, or adds generated/config/workflow/dependency risk.

## RED/GREEN Path

Use when behavior is missing, changed, or unprotected.

1. Write or identify one focused caller-facing check.
2. Run it and confirm it fails for the right reason.
3. Make the smallest source change that explains the failure.
4. Rerun the focused check until it passes.
5. Clean up only after GREEN, then rerun the focused check.
6. Run the smallest nearby broader check when risk warrants.

If the check passes immediately, do not edit source from that check. Inspect whether the behavior already exists, the assertion is too weak, or the test surface is wrong.

If RED fails for setup, spelling, fixture, or a different symptom, fix the check or use `diagnose-loop` before changing source.

## Test Shape

Prefer the highest practical caller-facing entry point: API, CLI, UI/workflow, command, job, exported module, or integration path users or downstream callers use.

Use simple inputs, fixtures, and states that show the behavior clearly. Keep one main action per check.

Avoid:

- private-shape tests
- mock-call-only tests
- snapshot-only assertions
- implementation-copied expectations
- batches of imagined tests before source changes
- dependency hooks, flags, or options that exist only to make tests easier

Mock only dependency boundaries you do not control, such as network, time, randomness, file systems, external processes, or third-party services. Keep enough real observable behavior that the check would fail if the behavior regressed.

If the only possible check is private, shallow, or setup-heavy for non-low-risk work, stop and question the entry point. Use `codebase-cleanup` when code shape blocks a useful behavior check.

## If No Test Setup Exists

Create the smallest repeatable check available: script, fixture, CLI command, smoke command, or repeatable manual check.

The check should observe caller-visible behavior strongly enough to guide the source change. If no repeatable check can be created without a behavior, dependency, data, or interface decision, stop and ask before changing source.

## Stop Or Ask

Stop or ask before source edits when:

- behavior, public or caller contract, acceptance check, or non-goal is materially unclear after cheap repo evidence
- the first check cannot fail for the right reason because the entry point, fixture, setup, state/data path, or dependency boundary is unknown
- the change would exceed the approved slice or alter API, CLI, UI workflow, data contract, dependency behavior, migration, security/data path, or user-visible behavior beyond scope
- the only available check is private, shallow, or mock-only and risk is not low
- RED contradicts the request, existing tests, fixtures, docs, logs, CI, or caller contract
- a broader check fails after GREEN for a reason unrelated to the slice and the cause is not understood

## Handoff

Use `diagnose-loop` for unexplained failures, `codebase-cleanup` when code shape blocks a useful check or simple implementation, `workspace-safety` for dirty tree or Git risk, and `verify-before-done` for final claims.

Use `slice-plan` only when the behavior expands into multiple real slices that need a written plan or handoff.

## Report

For a small slice:

```text
Behavior:
Check:
RED or baseline:
GREEN:
Broader check or skipped reason:
Risk:
```

For nontrivial slices, also include test-surface gap and diff-review note.
