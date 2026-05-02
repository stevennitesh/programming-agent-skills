---
name: tdd-slice
description: Use when writing or changing behavior, fixing reproduced bugs, adding features, refactoring while preserving behavior, or creating repeatable checks.
---

# TDD Slice

One behavior, one check, minimal implementation, cleanup after the check passes.

## Rule

If behavior changes, get a check that fails for the right reason before trusting the implementation.

If behavior should stay the same, run an existing check before and after the refactor. Add a new check only when important behavior is not protected.

Keep simple edits simple. Pure syntax, import, formatting, or type-only fixes with no behavior decision can use the direct focused check from `diagnose-loop`.

## Cycle

1. Choose the next smallest visible behavior:

```text
When <condition>, the user or caller sees <result>.
```

2. Write or identify one focused check. For a reproduced bug, reuse the failing check from `diagnose-loop` when it already proves the bug.

Prefer:

- The same entry point users or callers use
- Command-line, HTTP, or UI checks through the existing test setup
- Exported functions or modules
- Checks around the real state change

Avoid:

- Private method tests
- Mocks that only prove the mock was called
- Snapshot-only assertions
- Tests copied from implementation logic
- Batches of imagined tests before any implementation

3. Run the check and capture the expected failure. It should fail because the behavior is missing or wrong, not because of setup, spelling, or test code mistakes. If it passes immediately, the check targets existing behavior or is too weak. If it errors for setup reasons, fix the check before implementation.
4. Implement the minimum production change that explains the check.
5. Run the focused check until it passes. If it fails, fix the code or correct the check only when the check is wrong.
6. Clean up only after the check passes. Keep behavior unchanged and rerun the focused check.
7. Run the smallest broader check that protects the touched area: nearby tests, typecheck, lint, build, or the relevant workflow.

## Test Shape

- Test behavior, not internal steps.
- Use names from `CONTEXT.md` when they make behavior clearer.
- If a test needs a new recurring term or boundary, add or propose a small `CONTEXT.md` note instead of inventing private vocabulary.
- Use simple inputs that show the behavior clearly.
- Keep one main action per check.
- Mock only boundaries you do not control, such as network calls, time, randomness, file systems, or third-party services.
- Before mocking, know which real side effects the test still depends on and keep the mock shape complete enough for downstream code.
- Do not add production methods or options that exist only to make tests easier.
- If test setup is larger than the behavior being tested, question the interface or use a higher-level entry point.

## If No Test Setup Exists

Create the smallest repeatable check available: script, fixture, CLI command, or repeatable manual check. Say what remains unprotected.

## Slice Report

```text
Slice:
Failing check:
Implementation:
Focused verification:
Broader verification or skipped reason:
Remaining risk:
```

## Handoff

Use `diagnose-loop` when the failure is not understood. Use `thin-plan` when the behavior expands into multiple independent slices. Use `codebase-cleanup` when code shape blocks a simple implementation or behavior-preserving refactor. Use `verify-before-done` before claiming the slice is done, fixed, passing, or ready for PR.
