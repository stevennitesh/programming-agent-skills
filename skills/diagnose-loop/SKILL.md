---
name: diagnose-loop
description: Use when tests, commands, builds, CI jobs, or workflows fail; behavior is wrong; output or performance regresses; flakes or crashes appear; or an error is not yet understood.
---

# Diagnose Loop

Find the cause before changing source code. Use the fast path for obvious repeatable failures and the full loop only when uncertainty or risk earns it.

## Rule

Before changing source for a failure, read the exact failure evidence and name the reproducer or strongest observation.

Do not patch from memory, guesses, nearby failures, or broad-suite noise. The loop must match the user's symptom or be explicitly named as partial.

First visible move:

```text
Symptom:
Reproducer or observation:
Matches user symptom: yes|no|partial
Fast path or full loop:
Next check:
```

Reproducer means the command, test, CI job, captured log, fixture, or manual step that shows the failure. If no reproducer exists, use the strongest observation and name what evidence is missing.

## Fast Path

Use for repeatable low-risk failures: syntax errors, missing imports, local type errors, obvious assertions, fixture failures, and simple loop or condition mistakes.

1. Read the full failure output, stack trace, log, or report.
2. Run the direct failing check when available.
3. Make the smallest fix that explains that failure.
4. Rerun the same check after the final edit.
5. Stop unless the fix touches shared behavior, public or caller contract, data/state, security, concurrency, dependency/config behavior, generated output, or the check still fails.

Do not write hypothesis lists, add debug logging, or run broad suites for a fast-path failure unless the focused loop fails or risk grows.

## Full Loop

Use when the cause is unclear, the failure is flaky, expensive, risky, mismatched to the reported symptom, or the fast path fails.

- Build the cheapest useful loop: failing test, command, CI log, focused fixture, replay, captured request, or exact manual step.
- Sharpen loops that are broad, slow, flaky, nondeterministic, or observe a nearby setup error instead of the reported symptom.
- Minimize the case: input, fixture, state/data, config, dependency range, environment, command, and caller-facing entry point.
- Rank 2-5 falsifiable hypotheses only when the cause is still unclear.
- Test one variable at a time; negative results count.
- Add temporary debug output only when it distinguishes hypotheses or component boundaries, and remove it before the final diff.
- Do not combine speculative source, test, config, dependency, or fixture changes in one attempt.

## Flakes

Flaky means the same command, test, fixture, or workflow sometimes passes and sometimes fails.

- Record the command, attempts, failures, environment, seed/time/concurrency inputs, and CI run when relevant.
- Start with a small repeat count, such as 3-5 runs, or use existing CI history.
- Prefer making the trigger repeatable over proving stability by volume: pin time or randomness, isolate shared state, wait for conditions instead of sleeps, or control concurrency.
- After the fix, rerun the focused flaky check enough to check the old failure mode.
- Do not claim a flake is fixed from one passing run.

## Fix And Check

Fix the cause with the smallest source change that explains the observed failure.

Keep or add a regression check when the fix changes behavior or covers a recurring bug. If the correct behavior check needs design or broader implementation, use `tdd-slice`.

After the final edit, rerun the reproducer or strongest observation. Use `verify-before-done` to calibrate final fixed, covered, passing, or ready claims.

## Stop Or Ask

Stop or ask when:

- no useful reproducer, log-only observation, captured trace, fixture, access, or manual step exists after reasonable attempts
- the loop observes a different setup error, nearby failure, or broad-suite symptom and cannot be sharpened
- behavior, public or caller contract, data/state, security, dependency/config behavior, generated output, or live system state would change without an approved target
- three source-fix attempts fail or negative results contradict the current hypothesis
- the only possible regression check is shallow, private, or over-mocked and the risk is not low
- the suspected cause is external but no minimal case distinguishes external failure from repo behavior

## Handoff

Use `tdd-slice` for approved behavior checks, `codebase-cleanup` when structure blocks a durable fix or test, `workspace-safety` before dirty-tree or Git risk, `github-tracking` when the bug should become durable issue/PR state, and `verify-before-done` for final fixed/covered/passing claims.

## Report

For small fixes:

```text
Symptom:
Reproducer:
Cause:
Fix:
Rerun result:
Remaining risk:
```

For full investigations, also include hypotheses tested and any test-surface gap.
