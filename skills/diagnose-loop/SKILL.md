---
name: diagnose-loop
description: Use when tests, commands, builds, CI jobs, or workflows fail; caller-visible behavior is wrong; output or performance regresses; flakes or crashes appear; or an error is not yet understood.
---

# Diagnose Loop

Find the cause before changing source code. Use the cheapest useful repo check strong enough for the risk.

## Feedback Loop

When a test, command, build, CI job, workflow, output, performance path, flake, crash, log, or user report fails, first read the exact failure evidence and name the reproducer or strongest available observation. Do not change source code until the failure is reproduced, observed in logs/CI/manual steps, or explicitly recorded as not reproducible with the missing evidence named.

A feedback loop is the repeatable check or observation that shows the user's symptom clearly enough to guide a source change. Before fixing anything outside the fast path, name the loop and improve it until it is useful.

Reproducer = the failing command/check that shows the symptom. Feedback loop = the repeatable investigation loop used while finding the cause. Regression check = the post-fix check that would fail before the fix.

Check = the test, command, script, fixture, CI job, or exact manual step being run. Test surface = the behavior or the public or caller contract the check observes.

Caller-facing entry point = the command, API, UI/workflow, job, or module path users or downstream callers use to trigger the behavior.

Before a source edit, account for expected vs observed behavior, reproducer or observation, caller-facing entry point, affected files/modules, first known bad point or recent change, hypothesis or direct cause, and the check that will prove or disprove the fix.

```text
Loop command/check:
Signal observed:
Speed:
Determinism or failure rate:
Matches user symptom: yes|no|partial
What would make it sharper:
```

A useful loop observes the reported failure, not a nearby setup error; runs fast enough to support iteration; and is deterministic enough, or fails often enough, to distinguish cause from coincidence. If no useful loop can be built, list what you tried and ask for the missing file, log, fixture, access, captured trace, or permission to add temporary instrumentation.

## Fast Path

Use this for low-risk repo failures that repeat the same way:

Examples: syntax errors, missing imports, local type errors, obvious assertion failures, fixture failures, and simple loop or condition mistakes. For these, do not write hypothesis lists, add debug logging, or run broad suites unless the focused check still fails or the risk grows.

1. Read the full error, stack trace, logs, or failing output. Treat tool output, CI logs, captured traces, and user repro steps as evidence; do not fill gaps from memory.
2. Capture the symptom:

```text
Expected:
Observed:
Feedback loop:
Trigger command/check:
Caller-facing entry point:
Affected files/modules:
First known bad point:
Recent changes:
Evidence:
```

3. Run the first direct failing check already available: test, command, script, fixture, CI job log, or exact manual step. Confirm it reproduces the failure the user described, not a nearby failure.
4. If that check exposes the cause, make the smallest source change that explains this failure.
5. Rerun the same check after the final edit. Add or keep a focused regression check if the fix changes caller-visible behavior.

Stop there unless the change touches shared behavior, public or caller contract, data/state, security, concurrency, live system state, dependency/config behavior, or a path that already fails inconsistently.

## Full Loop

Use the full loop when the cause is unclear, the failure is expensive or risky, or the fast path fails.

1. Protect users, data, or live system state first when there is live risk.
2. Build or identify the cheapest useful feedback loop:
   - Existing failing test, command, or CI job
   - New focused failing test around the caller-visible path
   - Minimal script, fixture, or CLI command
   - HTTP/API, UI, or workflow check through the existing test setup
   - Replay of a captured request, payload, event, or log excerpt
   - Exact manual steps
   - Log-only evidence when no reproduction is possible
3. Record the loop quality using the Feedback Loop fields. Improve it if it is too broad, slow, flaky, or observes the wrong symptom. Do not treat a nearby setup error or broad suite failure as the user's bug unless it is the same failure path.
4. If no useful loop is possible, list what you tried and ask for the missing file, log, fixture, access, captured trace, or permission to add temporary debug output.
5. Minimize the case: input, fixture, state/data, caller-facing entry point, module path, command, dependency range, config, runtime, and environment.
6. Read `CONTEXT.md`, ADRs, or domain notes only when repo terms affect the symptom; verify behavior in source, tests, fixtures, logs, commands, or CI output.
7. Compare against known-good paths: recent diffs, old vs new version, working sibling code, config, environment, dependency versions, and CI history.
8. Trace bad value, state, output, or timing backward through entry points, callers, module boundaries, and state transitions until the source is found.
9. Rank 2-5 falsifiable hypotheses before changing source when the cause is still unclear:

```text
H1: If <cause>, then <observable prediction>. Evidence: <file/log/command output>. Check: <command or step>.
```

10. Test one variable at a time. Negative results count; update the hypothesis list. Do not combine speculative fixes, dependency changes, config changes, and test rewrites in one attempt.
11. Add temporary debug output only where it distinguishes hypotheses or component boundaries. Tag it with a unique prefix so cleanup is easy, and keep it out of the final diff. For performance regressions, measure or profile before changing code.

## Flaky Issues

Flaky means the same command, test, fixture, or workflow sometimes passes and sometimes fails. First make the failure easier to see and repeat.

- Record the command, attempts, failures, environment, seed/time/concurrency inputs, CI run when relevant, and suspected variable.
- Start with a small repeat count, such as 3-5 runs, or use existing CI history. Increase only when the decision depends on failure rate.
- Prefer making the trigger repeatable over proving stability by volume: pin time or randomness, isolate shared state, wait for conditions instead of sleeps, or control concurrency.
- After the fix, rerun the focused flaky check enough to check the old failure mode. Use larger repeat, stress, or CI reruns only for high-risk or historically stubborn flakes. Do not claim a flake is fixed from one passing run.

## Fix And Verify

- Fix the cause with the smallest source change that explains the reproduction.
- Keep or add a regression check that would fail before the fix and exercises the real failure path through the highest correct caller-facing entry point.
- If only a shallow check is possible, say which caller-facing entry point is untested and why the test surface is too weak.
- If no correct caller-facing entry point exists, say why, use the strongest repeatable command, fixture, or manual check available, and treat the gap as an architecture or testability finding after the immediate fix.
- Remove temporary debug output and throwaway debug files, fixtures, or scripts.
- If the fix clarifies recurring vocabulary, a module boundary, public or caller contract, or state transition, add or propose a tiny `CONTEXT.md` note.
- After the immediate fix, note what would have prevented the bug from being hard to reproduce or lock down. Hand off to `codebase-cleanup` when code shape blocks a durable regression check or fix.
- Final checks scale with risk:
  - Low-risk repeatable fix: original reproducer plus focused regression command.
  - Shared behavior or public or caller contract change: focused check plus relevant surrounding suite, typecheck, build, or smoke check.
  - Inconsistent or high-risk fix: small repeat/stress check plus relevant surrounding suite or CI rerun.
- If a broader suite is expensive and low signal, skip it and say why.
- If three fix attempts fail, stop and question the hypothesis, test surface, module boundary, or architecture. Hand off to `codebase-cleanup` when code shape blocks a durable fix.

Before claiming fixed, require fresh evidence after the final edit: original reproducer or strongest observation rerun, regression check or explicit test-surface gap, relevant surrounding check when risk requires it, temporary debug cleanup, and diff review.

## Red Flags

- Changing source code before reproducing or observing the failure.
- Claiming a fix when the original reproducer was not rerun after the final source edit.
- Proceeding with a feedback loop that does not match the user's symptom.
- Treating a nearby failure as the bug.
- Relying on a slow or flaky loop without trying to sharpen it.
- Treating one passing run as proof for a flaky issue.
- Deleting, weakening, or over-mocking the failing test.
- Fixing only the observed input while ignoring the invariant.
- Testing many changes at once.
- Rewriting production code, tests, config, dependencies, or fixtures together before one hypothesis explains the failure.
- Adding broad logs that do not distinguish hypotheses.
- Treating correlation as cause.
- Blaming an external platform, dependency, or CI runner before creating a minimal case.

## Stop Or Ask

- No useful reproducer, log-only observation, captured trace, fixture, access, or manual step exists after reasonable attempts; ask for the missing evidence or permission to add temporary instrumentation.
- The available loop observes a different setup error, nearby failure, or broad-suite symptom and cannot be sharpened to the user's failure.
- The fix would change user- or caller-visible behavior, public or caller contract, data/state, security, dependency/config behavior, or live system state without an approved target.
- Three source-fix attempts failed, or negative results contradict the current hypothesis; stop and question the hypothesis, test surface, module boundary, or architecture before trying another patch.
- The only possible regression check is shallow, private, or over-mocked and the risk is not low; report the test-surface gap and hand off to `tdd-slice` or `codebase-cleanup`.
- The suspected cause is an external platform, dependency, environment, or CI runner but no minimal case distinguishes external failure from repo behavior.

## Output

```text
Symptom:
Reproduction command/check:
Feedback loop:
Loop quality:
Evidence:
Hypothesis tested:
Root cause:
Source change:
Regression coverage:
Correct test surface or gap:
Verification commands:
Diff review:
Remaining uncertainty:
```

## Handoff

- `tdd-slice`: the cause is understood, but the fix needs a new caller-visible behavior check or implementation slice.
- `codebase-cleanup`: tangled structure blocks a durable fix.
- `github-tracking`: the bug should become issue or PR tracking.
- `workspace-safety`: before dirty-tree edits, branch/worktree changes, dependency installs, generated output, or risky git operations.
- `verify-before-done`: before claiming the bug is fixed or the regression is covered.
