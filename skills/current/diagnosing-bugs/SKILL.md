---
name: diagnosing-bugs
description: Diagnose hard or uncertain bugs, flaky failures, production-only issues, and performance regressions by building a tight red-capable feedback loop before hypothesising, instrumenting, fixing, and locking the bug down.
---

# Diagnosing Bugs

A discipline for hard bugs. The main job is to build a feedback loop that catches the user's exact symptom. Skip phases only when explicitly justified.

When exploring the codebase, read `docs/agents/domain.md` if present to locate the relevant domain glossary and ADRs. Otherwise, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR/domain docs to get a clear mental model of the relevant modules.

## Phase 1 - Build A Feedback Loop

This is the skill. Before forming a theory, create one command that can catch the bug.

A good loop is **tight**, **red-capable**, and **agent-runnable**. It drives the actual bug code path, asserts the user's exact symptom, and can go green once the bug is fixed.

Wrong loop = wrong bug = wrong fix.

### Ways To Build One

Try these in roughly this order:

1. **Failing test** at whatever seam reaches the bug: unit, integration, or e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with fixture input, diffing stdout or output files against known-good output.
4. **Headless browser script** with Playwright or Puppeteer: DOM, console, and network assertions.
5. **Captured trace replay**: save a real request, payload, event log, or failing fixture and replay it through the code path.
6. **Throwaway harness**: spin up the smallest subset of the system that exercises the bug path with one function call.
7. **Property / fuzz loop**: if the symptom is "sometimes wrong output", run many inputs until the failure mode appears.
8. **Bisection harness**: if the bug appeared between two known states, automate the check so `git bisect run` can use it.
9. **Differential loop**: run the same input through old vs new, config A vs config B, or implementation A vs B and diff the result.
10. **HITL script**: last resort. If a human must click, adapt `scripts/hitl-loop.template.sh` so the loop is still structured and captured.

### Tighten The Loop

Treat the loop as a product.

- **Faster** - cache setup, skip unrelated init, narrow the test scope.
- **Sharper** - assert the specific symptom, not merely "did not crash".
- **More deterministic** - pin time, seed randomness, isolate filesystem, freeze network.

A slow or flaky loop can still mislead you. Keep tightening until it is useful for repeated diagnosis.

### Non-Deterministic Bugs

The goal is not always a perfect repro. The goal is a high enough reproduction rate to debug.

Loop the trigger many times, parallelise when safe, add stress, narrow timing windows, inject sleeps, and measure the repro rate. A 50% flake is diagnosable. A 1% flake usually needs a better loop first.

### When You Cannot Build A Loop

Stop and say so explicitly. List what you tried.

Ask the user for one of:

- access to the environment that reproduces it
- a captured artifact: HAR, log dump, core dump, trace, fixture, screenshot, or screen recording with timestamps
- permission to add temporary instrumentation in the reproducing environment

Do not proceed with diagnosis without a red-capable loop or a clear reason the loop cannot yet exist.

### Phase 1 Gate

Phase 1 is done when you can name one command that you have already run and that is:

- **Red-capable** - it catches the user's exact symptom, not a nearby failure.
- **Deterministic enough** - same verdict each run, or a measured high repro rate for flakes.
- **Fast enough** - practical to run repeatedly while debugging.
- **Agent-runnable** - unattended, except for a structured HITL script when unavoidable.

No red-capable command, no Phase 2.

## Phase 2 - Reproduce And Minimise

Run the loop. Watch it go red.

Confirm:

- the failure matches the user's reported symptom
- the failure reproduces across runs, or at a measured repro rate for flaky bugs
- the exact symptom is captured: error message, wrong output, bad state, slow timing, or visual mismatch

Then minimise.

Shrink the repro to the smallest scenario that still goes red. Cut inputs, callers, config, data, and steps one at a time, re-running the loop after each cut.

Done means every remaining element is **load-bearing**: remove any one of them and the loop goes green or stops proving the bug.

Do not proceed until the bug is reproduced and minimised.

## Phase 3 - Hypothesise

Generate **3-5 ranked hypotheses** before testing any of them. Single-hypothesis debugging anchors too early.

Each hypothesis must be falsifiable:

> If `<cause>` is true, then `<probe or change>` will make `<observable prediction>` happen.

If the prediction is vague, sharpen or discard the hypothesis.

If the user is around, show the ranked list before testing. They may have domain knowledge that re-ranks it immediately. If the user is unavailable, proceed with the ranking and report it later.

Keep a short diagnosis log as you work: hypothesis tested, probe used, result observed, and what it ruled out.

## Phase 4 - Instrument

Each probe must map to a prediction from Phase 3. Change one variable at a time.

Prefer:

1. **Debugger / REPL inspection** when the environment supports it.
2. **Targeted logs** at seams or state transitions that distinguish hypotheses.
3. **Never** broad "log everything and grep" instrumentation.

Tag every temporary debug log with a unique prefix, e.g. `[DEBUG-a4f2]`, so cleanup is mechanical.

For performance regressions, measure first. Classify the bottleneck before changing code: latency, throughput, saturation, errors, resource use, query plan, browser trace, or another measured constraint. Establish a baseline with a timing harness, profiler, trace, benchmark, or query plan. Then bisect or probe against the measured bottleneck.

## Phase 5 - Fix And Lock It Down

Write the regression test before the fix when there is a **correct seam** for it.

A correct seam exercises the real bug pattern as it happened at the call site. A too-shallow test gives false confidence: it may prove a helper while missing the chain that produced the bug.

If a correct seam exists:

1. Turn the minimised repro into a failing regression test.
2. Watch it fail.
3. Apply the smallest fix that addresses the proven cause.
4. Watch the regression test pass.
5. Re-run the original Phase 1 loop against the un-minimised scenario.

If no correct seam exists, document that as a finding. The architecture is preventing the bug from being locked down. Do not fake confidence with a shallow test.

## Phase 6 - Cleanup And Post-Mortem

Before declaring done:

- re-run the original Phase 1 loop and confirm the bug no longer reproduces
- confirm the regression test passes, or document why no correct seam exists
- remove all `[DEBUG-...]` instrumentation
- delete throwaway harnesses or move them to a clearly marked debug location only if they remain useful
- state the winning hypothesis in the commit, PR, or handoff so the next debugger learns from it

Then ask: what would have prevented this bug?

If the answer is architectural - no good test seam, tangled callers, hidden coupling, poor locality, or a shallow module - hand off to `$improve-codebase-architecture` with the specifics. Make that recommendation after the fix, when the diagnosis has produced evidence.
