---
name: diagnose-loop
description: Use when tests, commands, builds, CI jobs, or workflows fail; caller-visible behavior is wrong; output or performance regresses; flakes or crashes appear; or an error is not yet understood.
---

# Diagnose Loop

Find the cause before changing source code. Use the cheapest useful repo check strong enough for the risk.

## Feedback Loop

A feedback loop is the repeatable check or observation that shows the user's symptom clearly enough to guide a source change. Before fixing anything outside the fast path, name the loop and improve it until it is useful.

Reproducer = the failing command/check that shows the symptom. Feedback loop = the repeatable investigation loop used while finding the cause. Regression check = the post-fix check that would fail before the fix.

Check = the test, command, script, fixture, CI job, or exact manual step being run. Test surface = the behavior or contract the check observes.

Caller-facing entry point = the command, API, UI/workflow, job, or module path users or downstream callers use to trigger the behavior.

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

1. Read the full error, stack trace, logs, or failing output.
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
4. If that check exposes the cause, make the smallest source change.
5. Rerun the same check. Add or keep a focused regression check if the fix changes caller-visible behavior.

Stop there unless the change touches shared behavior, public contracts, data/state, security, concurrency, live system state, dependency/config behavior, or a path that already fails inconsistently.

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
3. Record the loop quality using the Feedback Loop fields. Improve it if it is too broad, slow, flaky, or observes the wrong symptom.
4. If no useful loop is possible, list what you tried and ask for the missing file, log, fixture, access, captured trace, or permission to add temporary debug output.
5. Minimize the case: input, fixture, state/data, caller-facing entry point, module path, command, dependency range, config, runtime, and environment.
6. Read `CONTEXT.md`, ADRs, or domain notes only when repo terms affect the symptom; verify behavior in source, tests, fixtures, logs, commands, or CI output.
7. Compare against known-good paths: recent diffs, old vs new version, working sibling code, config, environment, dependency versions, and CI history.
8. Trace bad value, state, output, or timing backward through entry points, callers, module boundaries, and state transitions until the source is found.
9. Rank 2-5 falsifiable hypotheses:

```text
H1: If <cause>, then <observable prediction>. Evidence: <file/log/command output>. Check: <command or step>.
```

10. Test one variable at a time. Negative results count; update the hypothesis list.
11. Add temporary debug output only where it distinguishes hypotheses or component boundaries. Tag it with a unique prefix so cleanup is easy, and keep it out of the final diff. For performance regressions, measure or profile before changing code.

## Flaky Issues

Flaky means the same command, test, fixture, or workflow sometimes passes and sometimes fails. First make the failure easier to see and repeat.

- Record the command, attempts, failures, environment, seed/time/concurrency inputs, CI run when relevant, and suspected variable.
- Start with a small repeat count, such as 3-5 runs, or use existing CI history. Increase only when the decision depends on failure rate.
- Prefer making the trigger repeatable over proving stability by volume: pin time or randomness, isolate shared state, wait for conditions instead of sleeps, or control concurrency.
- After the fix, rerun the focused flaky check enough to check the old failure mode. Use larger repeat, stress, or CI reruns only for high-risk or historically stubborn flakes.

## Fix And Verify

- Fix the cause with the smallest source change that explains the reproduction.
- Keep or add a regression check that would fail before the fix and exercises the real failure path through the highest correct caller-facing entry point.
- If only a shallow check is possible, say which caller-facing entry point is untested and why the test surface is too weak.
- If no correct caller-facing entry point exists, say why, use the strongest repeatable command, fixture, or manual check available, and treat the gap as an architecture or testability finding after the immediate fix.
- Remove temporary debug output and throwaway debug files, fixtures, or scripts.
- If the fix clarifies recurring vocabulary, a module boundary, public contract, or state transition, add or propose a tiny `CONTEXT.md` note.
- After the immediate fix, note what would have prevented the bug from being hard to reproduce or lock down. Hand off to `codebase-cleanup` when code shape blocks a durable regression check or fix.
- Final checks scale with risk:
  - Low-risk repeatable fix: original reproducer plus focused regression command.
  - Shared behavior or public contract change: focused check plus relevant surrounding suite, typecheck, build, or smoke check.
  - Inconsistent or high-risk fix: small repeat/stress check plus relevant surrounding suite or CI rerun.
- If a broader suite is expensive and low signal, skip it and say why.
- If three fix attempts fail, stop and question the hypothesis, test surface, module boundary, or architecture. Hand off to `codebase-cleanup` when code shape blocks a durable fix.

## Red Flags

- Changing source code before reproducing or observing the failure.
- Proceeding with a feedback loop that does not match the user's symptom.
- Treating a nearby failure as the bug.
- Relying on a slow or flaky loop without trying to sharpen it.
- Treating one passing run as proof for a flaky issue.
- Deleting, weakening, or over-mocking the failing test.
- Fixing only the observed input while ignoring the invariant.
- Testing many changes at once.
- Adding broad logs that do not distinguish hypotheses.
- Treating correlation as cause.
- Blaming an external platform, dependency, or CI runner before creating a minimal case.

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
