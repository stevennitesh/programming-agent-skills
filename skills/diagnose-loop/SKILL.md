---
name: diagnose-loop
description: Use when tests fail, behavior is wrong, output or performance regresses, builds fail, flakes appear, crashes occur, or an error is not yet understood.
---

# Diagnose Loop

Find the cause before changing the system. Use the cheapest useful check strong enough for the risk.

## Fast Path

Use this for low-risk failures that repeat the same way:

Examples: syntax errors, missing imports, local type errors, obvious assertion failures, and simple loop or condition mistakes. For these, do not write hypothesis lists, add debug logging, or run broad suites unless the focused check still fails or the risk grows.

1. Read the full error, stack trace, logs, or failing output.
2. Capture the symptom:

```text
Expected:
Observed:
Trigger:
Scope:
First known bad point:
Recent changes:
```

3. Run the first direct failing check already available: test, command, script, fixture, or exact manual step. Confirm it reproduces the failure the user described, not a nearby failure.
4. If that check exposes the cause, make the smallest fix.
5. Rerun the same check. Add or keep a focused regression check if the fix changes behavior.

Stop there unless the change touches shared behavior, public interfaces, data, security, concurrency, production state, or a path that already fails inconsistently.

## Full Loop

Use the full loop when the cause is unclear, the failure is expensive or risky, or the fast path fails.

1. Protect users, data, or production state first when there is live risk.
2. Establish the cheapest useful check:
   - Existing failing test
   - New focused failing test
   - Minimal script, fixture, or CLI command
   - Exact manual steps
   - Log-only evidence when no reproduction is possible
3. Shape the check until it is useful: it matches the reported failure, is as fast as practical, observes the specific symptom, and is repeatable enough to guide a fix.
4. If no useful check is possible, list what you tried and ask for the missing file, log, access, or permission to add temporary debug output.
5. Minimize the case: input, state, module path, command, dependency range, environment.
6. Read `CONTEXT.md` or domain notes when project terms affect the symptom, but verify behavior in source, tests, logs, or commands.
7. Compare against known-good paths: recent changes, old vs new version, working sibling code, config, environment, dependency versions.
8. Trace bad value, state, output, or timing backward through boundaries until the source is found.
9. Rank 2-5 hypotheses:

```text
H1: If <cause>, then <observable prediction>. Evidence: <evidence>. Test: <check>.
```

10. Test one variable at a time. Negative results count; update the hypothesis list.
11. Add temporary debug output only where it distinguishes hypotheses. Tag it with a unique prefix so cleanup is easy.

## Flaky Issues

Flaky means the same trigger sometimes passes and sometimes fails. First make the failure easier to see and repeat.

- Record the command, attempts, failures, environment, and suspected variable.
- Start with a small repeat count, such as 3-5 runs, or use existing CI history. Increase only when the decision depends on failure rate.
- Prefer making the trigger repeatable over proving stability by volume: pin time or randomness, isolate shared state, wait for conditions instead of sleeps, or control concurrency.
- After the fix, rerun the focused flaky check enough to check the old failure mode. Use larger repeat or stress runs only for high-risk or historically stubborn flakes.

## Fix And Verify

- Fix the cause with the smallest change that explains the reproduction.
- Keep or add a regression check that would fail before the fix and exercises the real failure path through the caller-visible entry point.
- If only a shallow check is possible, say why it gives limited confidence and consider `codebase-cleanup` after the fix.
- If no correct test entry point exists, say why and use the strongest repeatable check available.
- Remove temporary debug output and throwaway debug files.
- If the fix clarifies a recurring term, role, or boundary, add or propose a small `CONTEXT.md` note.
- Final checks scale with risk:
  - Low-risk repeatable fix: original check plus focused regression.
  - Shared behavior or public interface change: focused check plus relevant surrounding suite.
  - Inconsistent or high-risk fix: small repeat/stress check plus relevant surrounding suite.
- If a broader suite is expensive and low signal, skip it and say why.
- If three fix attempts fail, stop and question the hypothesis, test entry point, or architecture. Hand off to `codebase-cleanup` when code shape blocks a durable fix.

## Red Flags

- Changing code before reproducing or observing the failure.
- Treating one passing run as proof for a flaky issue.
- Deleting, weakening, or over-mocking the failing test.
- Fixing only the observed input while ignoring the invariant.
- Testing many changes at once.
- Treating correlation as cause.
- Debugging an external platform bug before creating a minimal case.

## Output

```text
Symptom:
Reproduction:
Root cause:
Fix:
Regression coverage:
Verification:
Remaining uncertainty:
```

## Handoff

Use `tdd-slice` when the cause is understood but the fix needs a new behavior check or implementation slice. Use `codebase-cleanup` when tangled structure blocks a durable fix. Use `github-work-tracking` when the bug should become a durable issue or PR note. Use `verify-before-done` before claiming the bug is fixed or the regression is covered.
