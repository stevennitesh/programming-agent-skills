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

## Cycle

1. Choose the next smallest caller-visible behavior:

```text
When <input/state/event>, the user, caller, API, CLI, or UI sees <result>.
```

2. Write or identify one focused check. For a reproduced bug, reuse the failing command, test, fixture, or manual check from `diagnose-loop` when it already proves the bug.

Prefer:

- The same public entry point users or callers use
- Command-line, HTTP/API, UI, or workflow checks through the existing test setup
- Exported functions, modules, or commands
- Checks around the real state/data change, persisted output, emitted event, or error path

Avoid:

- Private method tests
- Mocks that only prove the mock was called
- Snapshot-only assertions
- Tests copied from implementation logic
- Batches of imagined tests before any source change

3. Run the focused check and capture the expected failure. It should fail because the behavior is missing or wrong, not because of setup, spelling, fixture, or test code mistakes. If it passes immediately, the check targets existing behavior or is too weak. If it errors for setup reasons, fix the check before implementation.
4. Implement the minimum source change that explains the failing check.
5. Run the focused check until it passes. If it fails, fix the source change or correct the check only when the check is wrong.
6. Clean up only after the check passes. Keep behavior unchanged and rerun the focused check.
7. Run the smallest broader repo check that protects the touched area: nearby tests, typecheck, lint, build, smoke test, or relevant workflow command.

## Test Shape

- Test caller-visible behavior, not internal steps.
- Use `CONTEXT.md` names when they clarify behavior, domain concepts, or module boundaries.
- If a test needs recurring vocabulary, a boundary, contract, or state transition, add or propose a tiny `CONTEXT.md` note instead of private test-only language.
- Use simple inputs, fixtures, or states that show the behavior clearly.
- Keep one main action per check.
- Mock only dependency boundaries you do not control, such as network calls, time, randomness, file systems, external processes, or third-party services.
- Before mocking, know which real side effects, state changes, or downstream calls the test still depends on and keep the mock shape complete enough for source code.
- Do not add implementation methods, options, flags, or dependency hooks that exist only to make tests easier.
- If test setup is larger than the behavior being tested, question the caller interface or use a higher-level entry point.

## If No Test Setup Exists

Create the smallest repeatable repo check available: script, fixture, CLI command, smoke test, or repeatable manual check. Say which behavior remains unprotected.

## Slice Report

```text
Behavior slice:
Failing check or baseline:
Source change:
Focused verification command:
Broader verification command or skipped reason:
Diff review:
Remaining risk:
```

## Handoff

- `diagnose-loop`: the failure is not understood.
- `slice-plan`: the behavior expands into multiple independent slices.
- `codebase-cleanup`: code shape blocks a simple implementation or behavior-preserving refactor.
- `workspace-safety`: before dirty-tree edits, branch/worktree changes, dependency installs, generated output, or risky git operations.
- `verify-before-done`: before claiming the slice is done, fixed, passing, or ready for PR.
