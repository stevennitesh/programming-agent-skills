---
name: diagnosing-bugs
description: Diagnose hard or uncertain bugs, flaky failures, production-only issues, and performance regressions by building a tight red-capable feedback loop before hypothesising, instrumenting, fixing, and locking the bug down.
---

# Diagnosing Bugs

Hard bugs need evidence before theory. Build a **tight**, **red-capable**, **agent-runnable** loop that catches the user's exact symptom. Everything else is mechanical once the loop is right.

Skip phases only when explicitly justified.

Read `docs/agents/engineering-contract.md` when present before changing repo behavior or locking in the fix.

When exploring the codebase, read `docs/agents/domain.md` if present to locate the relevant domain glossary and ADRs. Otherwise, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR/domain docs.

## Phase 1 - Build A Tight Loop

Before forming a theory, create one command that can catch the bug.

A good loop drives the actual bug path, asserts the user's exact symptom, goes red before the fix, and can go green after the fix. Wrong loop = wrong bug = wrong fix.

Ways to build one, roughly in order:

1. **Failing test** at whatever seam reaches the bug: unit, integration, or e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with fixture input, diffing stdout or output files.
4. **Headless browser script** with DOM, console, and network assertions.
5. **Captured trace replay** from a real request, payload, event log, or fixture.
6. **Throwaway harness** around the smallest system subset that exercises the bug path.
7. **Property / fuzz loop** for "sometimes wrong output" symptoms.
8. **Bisection harness** for bugs between two known states.
9. **Differential loop** comparing old vs new, config A vs B, or implementation A vs B.
10. **HITL script** as last resort: adapt `scripts/hitl-loop.template.sh` when a human must click.

Tighten the loop:

- **Faster** - cache setup, skip unrelated init, narrow scope.
- **Sharper** - assert the exact symptom, not merely "did not crash".
- **More deterministic** - pin time, seed randomness, isolate filesystem, freeze network.

For flakes, the goal is a higher reproduction rate until the bug is diagnosable. Loop the trigger, parallelise when safe, add stress, narrow timing windows, inject sleeps, and measure the repro rate.

If you cannot build a loop, stop and say so. List what you tried. Ask for access to the reproducing environment, a captured artifact, or approval for temporary instrumentation.

Phase 1 is done when you can paste one command you have already run, plus its red output, and that command is:

- **Red-capable** - catches the user's exact symptom, not a nearby failure.
- **Deterministic enough** - same verdict each run, or a measured high repro rate.
- **Fast enough** - practical to run repeatedly.
- **Agent-runnable** - unattended, except for structured HITL.

If you catch yourself reading code to build a theory before this command exists, stop. No red-capable command, no Phase 2.

## Phase 2 - Reproduce And Minimise

Run the loop. Watch it go red.

Confirm the failure matches the user's symptom, reproduces across runs or at a measured rate, and captures the exact error, wrong output, bad state, slow timing, or visual mismatch.

Minimise the repro. Cut inputs, callers, config, data, and steps one at a time, re-running after each cut.

Done means every remaining element is **load-bearing**: remove any one and the loop goes green or stops proving the bug.

## Phase 3 - Hypothesise

Generate **3-5 ranked hypotheses** before testing any of them. Single-hypothesis debugging anchors too early.

Each hypothesis must be falsifiable:

> If `<cause>` is true, then `<probe or change>` will make `<observable prediction>` happen.

If the prediction is vague, sharpen or discard it.

Show the ranked list before testing when the user is available. If not, proceed and report it later.

Keep a short diagnosis log: hypothesis, probe, result, and what it ruled out.

## Phase 4 - Instrument

Each probe maps to a Phase 3 prediction. Change one variable at a time.

Prefer debugger or REPL inspection, then targeted logs at seams or state transitions. Never use broad "log everything and grep" instrumentation.

Tag every temporary debug log with a unique prefix, e.g. `[DEBUG-a4f2]`.

For performance regressions, measure first. Establish a baseline, classify the bottleneck, then bisect or probe against the measured constraint.

## Phase 5 - Fix And Lock It Down

Write the regression test before the fix when there is a **correct seam**.

A correct seam exercises the real bug pattern as it happened at the call site. A too-shallow test gives false confidence.

If a correct seam exists:

1. Turn the minimised repro into a failing regression test.
2. Watch it fail.
3. Apply the smallest fix that addresses the proven cause.
4. Watch the regression test pass.
5. Re-run the original Phase 1 loop against the un-minimised scenario.

If no correct seam exists, document that as a finding. The architecture is preventing the bug from being locked down.

## Phase 6 - Cleanup And Post-Mortem

Before declaring done:

- re-run the original Phase 1 loop and confirm the bug no longer reproduces
- confirm the regression test passes, or document why no correct seam exists
- remove all `[DEBUG-...]` instrumentation; grep the prefix before declaring done
- delete throwaway harnesses or move them to a clearly marked debug location only if useful
- state the winning hypothesis in the commit, PR, or handoff

Then ask: what would have prevented this bug?

If the answer is architectural - no good test seam, tangled callers, hidden coupling, poor locality, or a shallow module - recommend `$improve-codebase-architecture` with the specifics after the fix has evidence.
