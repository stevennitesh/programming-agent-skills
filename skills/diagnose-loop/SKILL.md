---
name: diagnose-loop
description: Use when tests, commands, builds, CI jobs, or workflows fail; caller-visible behavior is wrong; output or performance regresses; flakes or crashes appear; or an error is not yet understood.
---

# Diagnose Loop

Find the cause before changing source code. Use the cheapest useful repo check strong enough for the risk.

## Fast Path

Use this for low-risk repo failures that repeat the same way:

Examples: syntax errors, missing imports, local type errors, obvious assertion failures, fixture failures, and simple loop or condition mistakes. For these, do not write hypothesis lists, add debug logging, or run broad suites unless the focused check still fails or the risk grows.

1. Read the full error, stack trace, logs, or failing output.
2. Capture the symptom:

```text
Expected:
Observed:
Trigger command/check:
Entry point or caller path:
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
2. Establish the cheapest useful check:
   - Existing failing test, command, or CI job
   - New focused failing test around the caller-visible path
   - Minimal script, fixture, or CLI command
   - HTTP/API, UI, or workflow check through the existing test setup
   - Replay of a captured request, payload, event, or log excerpt
   - Exact manual steps
   - Log-only evidence when no reproduction is possible
3. Shape the check until it is useful: it matches the reported failure, is as fast as practical, observes the specific symptom, and is repeatable enough to guide a source change.
4. If no useful check is possible, list what you tried and ask for the missing file, log, fixture, access, or permission to add temporary debug output.
5. Minimize the case: input, fixture, state/data, entry point, module path, command, dependency range, config, runtime, and environment.
6. Read `CONTEXT.md`, ADRs, or domain notes only when repo terms affect the symptom; verify behavior in source, tests, fixtures, logs, commands, or CI output.
7. Compare against known-good paths: recent diffs, old vs new version, working sibling code, config, environment, dependency versions, and CI history.
8. Trace bad value, state, output, or timing backward through entry points, callers, module boundaries, and state transitions until the source is found.
9. Rank 2-5 hypotheses:

```text
H1: If <cause>, then <observable prediction>. Evidence: <file/log/command output>. Check: <command or step>.
```

10. Test one variable at a time. Negative results count; update the hypothesis list.
11. Add temporary debug output only where it distinguishes hypotheses. Tag it with a unique prefix so cleanup is easy, and keep it out of the final diff.

## Flaky Issues

Flaky means the same command, test, fixture, or workflow sometimes passes and sometimes fails. First make the failure easier to see and repeat.

- Record the command, attempts, failures, environment, seed/time/concurrency inputs, CI run when relevant, and suspected variable.
- Start with a small repeat count, such as 3-5 runs, or use existing CI history. Increase only when the decision depends on failure rate.
- Prefer making the trigger repeatable over proving stability by volume: pin time or randomness, isolate shared state, wait for conditions instead of sleeps, or control concurrency.
- After the fix, rerun the focused flaky check enough to check the old failure mode. Use larger repeat, stress, or CI reruns only for high-risk or historically stubborn flakes.

## Fix And Verify

- Fix the cause with the smallest source change that explains the reproduction.
- Keep or add a regression check that would fail before the fix and exercises the real failure path through the caller-visible entry point.
- If only a shallow check is possible, say which caller path is untested and consider `codebase-cleanup` after the fix.
- If no correct test entry point exists, say why and use the strongest repeatable command, fixture, or manual check available.
- Remove temporary debug output and throwaway debug files, fixtures, or scripts.
- If the fix clarifies recurring vocabulary, a module boundary, public contract, or state transition, add or propose a tiny `CONTEXT.md` note.
- Final checks scale with risk:
  - Low-risk repeatable fix: original reproducer plus focused regression command.
  - Shared behavior or public contract change: focused check plus relevant surrounding suite, typecheck, build, or smoke check.
  - Inconsistent or high-risk fix: small repeat/stress check plus relevant surrounding suite or CI rerun.
- If a broader suite is expensive and low signal, skip it and say why.
- If three fix attempts fail, stop and question the hypothesis, test entry point, module boundary, or architecture. Hand off to `codebase-cleanup` when code shape blocks a durable fix.

## Red Flags

- Changing source code before reproducing or observing the failure.
- Treating one passing run as proof for a flaky issue.
- Deleting, weakening, or over-mocking the failing test.
- Fixing only the observed input while ignoring the invariant.
- Testing many changes at once.
- Treating correlation as cause.
- Blaming an external platform, dependency, or CI runner before creating a minimal case.

## Output

```text
Symptom:
Reproduction command/check:
Evidence:
Root cause:
Source change:
Regression coverage:
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
