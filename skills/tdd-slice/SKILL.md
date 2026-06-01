---
name: tdd-slice
description: Use when implementing or changing caller-visible behavior, fixing reproduced bugs, adding features, refactoring while preserving behavior, or creating repeatable repo checks.
---

# TDD Slice

One caller-visible behavior, one focused check, minimal source change, cleanup after the check passes.

## Rule

If runtime behavior changes, get a check that fails for the right reason before trusting the source change.

If behavior should stay the same, run an existing check before and after the refactor. Add a new regression check only when important caller-visible behavior is not protected.

Keep simple edits simple. Pure syntax, import, formatting, or type-only fixes with no behavior decision can use the direct focused check from `diagnose-loop`.

## Tracer Bullet Rule

Start with one narrow end-to-end behavior through the real caller-facing path. This tracer bullet proves the test surface, test shape, and source route before expanding coverage.

Caller-facing entry point = the API, CLI, UI/workflow, command, job, or integration path users or downstream callers use. Highest correct entry point means closest to the user or most abstract while still focused; for example, test the CLI command or UI action instead of a low-level helper when that is the behavior contract. Test surface = the behavior or contract the check observes.

Do not write a batch of imagined tests and then a batch of implementation. Add one behavior check, watch it fail for the right reason, make the smallest source change, watch it pass, then repeat.

If the behavior is caller-visible, do not test only data shape, private method shape, or mock call shape.

## Cycle

1. Choose the next smallest caller-visible behavior:

```text
When <input/state/event>, the user, caller, API, CLI, or UI sees <result>.
```

2. Choose the highest correct caller-facing entry point and write or identify one focused check. For a reproduced bug, reuse the failing command, test, fixture, or manual check from `diagnose-loop` when it already proves the bug.

Prefer:

- The same entry point users or callers use
- Command-line, HTTP/API, UI, or workflow checks through the existing test setup
- Exported functions, modules, or commands
- Checks around the real state/data change, persisted output, emitted event, or error path

Avoid:

- Private method tests
- Mocks that only prove the mock was called
- Snapshot-only assertions
- Tests copied from implementation logic
- Batches of imagined tests before any source change

3. RED: run the focused check and capture the expected failure. It should fail because the behavior is missing or wrong, not because of setup, spelling, fixture, or test code mistakes.
   - If it passes immediately, the check targets existing behavior or is too weak.
   - If it errors for setup reasons, fix the check before implementation.
   - If it fails for a different symptom, adjust the check or use `diagnose-loop`.
4. GREEN: implement the minimum source change that explains the failing check.
5. Run the focused check until it passes. If it fails, fix the source change or correct the check only when the check is wrong.
6. REFACTOR: clean up only after the check passes. Keep behavior unchanged and rerun the focused check.
7. Repeat from step 1 for the next behavior, using what the previous cycle taught.
8. Run the smallest broader repo check that protects the touched area: nearby tests, typecheck, lint, build, smoke test, or relevant workflow command.

## Test Shape

- Test caller-visible behavior, not internal steps.
- Prefer the highest correct caller-facing entry point. The caller interface is the test surface: inputs, outputs, invariants, ordering, state/data changes, emitted events, error modes, configuration, and compatibility expectations.
- Use `CONTEXT.md` names when they clarify behavior, domain concepts, or module boundaries.
- If a test needs recurring vocabulary, a boundary, contract, or state transition, add or propose a tiny `CONTEXT.md` note instead of private test-only language.
- Use simple inputs, fixtures, or states that show the behavior clearly.
- Keep one main action per check.
- Mock only dependency boundaries you do not control, such as network calls, time, randomness, file systems, external processes, or third-party services.
- Before mocking, know which real side effects, state changes, or downstream calls the test still depends on. Keep enough real observable behavior through the public path that the check would fail if the behavior regressed.
- Do not add implementation methods, options, flags, or dependency hooks that exist only to make tests easier.
- If the only possible check is private, shallow, or setup-heavy, question the caller interface or use a higher-level entry point. Consider `codebase-cleanup` when code shape blocks a useful behavior check.

## If No Test Setup Exists

Create the smallest repeatable repo check available: script, fixture, CLI command, smoke test, or repeatable manual check. It should observe the caller-visible behavior and be strong enough to guide the source change.

Report which behavior remains unprotected and what would be needed for a durable regression check.

## Red Flags

- Implementing before the RED check exists.
- Treating an immediately passing check as proof.
- Changing source when RED fails for setup, spelling, fixture, or the wrong symptom.
- Writing several tests before any source change.
- Testing private shape, data shape, or mock calls instead of caller-visible behavior.
- Refactoring while the focused check is still red.
- Substituting a broad suite for the focused behavior check.

## Slice Report

```text
Tracer bullet behavior:
Test surface/check:
RED result:
Source change:
GREEN result:
Refactor check:
Focused verification command:
Broader verification command or skipped reason:
Unprotected behavior or test-surface gap:
Diff review:
Remaining risk:
```

## Handoff

- `diagnose-loop`: the failure is not understood.
- `slice-plan`: the behavior expands into multiple independent slices.
- `codebase-cleanup`: code shape blocks a simple implementation or behavior-preserving refactor.
- `workspace-safety`: before dirty-tree edits, branch/worktree changes, dependency installs, generated output, or risky git operations.
- `verify-before-done`: before claiming the slice is done, fixed, passing, or ready for PR.
