---
name: diagnosing-bugs
description: "Diagnose or debug broken, failing, flaky, slow, environment-only, or production-only behavior when the cause or trusted repro is uncertain. Apply a fix only inside an authorized implementation boundary."
---

# Diagnosing Bugs

**Exact symptom -> tight loop -> load-bearing repro -> falsifiable hypotheses -> discriminating probes -> proven cause -> authorized fix -> regression proof**

**No red-capable loop, no hypothesis. No proven cause, no fix.**

## Ownership And Modes

- **Diagnosis mode:** prove the cause and recommend the smallest fix. Put disposable diagnostic artifacts under `.tmp/diagnosing-bugs/<bug-slug>/`; remove them and all instrumentation before return so no production behavior change remains.
- **Fix mode:** use only when the user or caller authorizes implementation. Apply the smallest causal fix and prove it against both the regression seam and original scenario.
- **Caller:** owns review, staging, commit, tracker or external mutation, push, release, and architecture follow-up.
- **Return owner:** A caller-invoked run returns its diagnosis packet to that caller. A standalone diagnosis-only run recommends `$implement` as its one next owner. Fix mode returns to the caller that authorized implementation.

Uncertain diagnosis stays in `$diagnosing-bugs` through regression proof. Hand off to `$tdd` when behavior and a trusted reproduction are already known before the diagnostic loop begins; retain the original caller as the return owner.

Advance only when the current phase gate is satisfied. Existing evidence may satisfy a gate only when its source, command or artifact, and result are recorded in the Source Trace.

## Preconditions

Read `docs/agents/engineering-contract.md` when present before repo-file instrumentation or a fix.

When exploring the codebase, follow `docs/agents/domain.md` when present. Otherwise use the relevant context map, glossary, ADRs, and nearby code.

Build the **Source Trace** from:

- the user report or caller packet;
- expected and actual behavior;
- exact failure output, logs, traces, screenshots, or timings;
- reproducer, environment, configuration, version, seed, and concurrency inputs;
- acceptance criteria, known-good baseline, and relevant repo contracts.

Record contradictions and missing evidence. The current broken output is not the expected-behavior oracle.

Before repo-file instrumentation, capture the fixed point, worktree status, and pre-existing dirty paths. Preserve user and unrelated work.

Keep local instrumentation reversible, uniquely tagged, and easy to remove. Live or production instrumentation, persisted telemetry, external writes, and sensitive-data capture require explicit approval. Redact secrets and personal data from stored artifacts and the final packet.

## Phase 1 - Build A Tight Loop

Build one command that catches the exact reported symptom. Put disposable scripts, logs, captures, and harnesses under `.tmp/diagnosing-bugs/<bug-slug>/`.

Try these roughly in order:

1. **Failing test** at the seam that reaches the bug.
2. **HTTP script** against a running service.
3. **CLI invocation** with fixture input and asserted output.
4. **Headless browser script** asserting DOM, console, or network behavior.
5. **Captured trace replay** from a real request, payload, event log, or fixture.
6. **Throwaway harness** around the smallest system subset that reaches the bug.
7. **Property or fuzz loop** for intermittent wrong output.
8. **Bisection harness** across known-good and known-bad states.
9. **Differential loop** comparing versions, implementations, or configurations.
10. **Structured HITL script** as a last resort. Adapt `scripts/hitl-loop.template.sh`, or translate it to the available shell while preserving its captured fields.

Tighten the loop:

- **Sharp:** asserts the exact symptom.
- **Deterministic enough:** returns the same verdict, or a measured reproduction rate.
- **Fast enough:** practical to run repeatedly.
- **Agent-runnable:** unattended except for structured HITL.

For flakes, record attempts, failures, reproduction rate, environment, seed, time, and concurrency inputs. Raise the reproduction rate until probes can distinguish hypotheses.

Pass the **loop gate** only when one command has already been run and its invocation plus red output prove the exact symptom.

If no loop can be built, return a blocked diagnosis packet listing attempts and missing evidence. Ask for access, a captured artifact, or approval for live instrumentation. Do not form a causal claim.

## Phase 2 - Reproduce And Minimise

Run the loop and confirm its failure matches the user's exact symptom.

Minimise one element at a time: inputs, callers, configuration, data, environment, dependencies, and steps. Rerun after every cut.

Pass the **repro gate** when every remaining element is either:

- **load-bearing:** removing it stops proving the bug; or
- **unremovable:** reducing it would destroy an environment- or production-only condition, with the reason recorded.

The minimised repro must still explain the original scenario.

## Phase 3 - Rank Hypotheses

Generate **3-5 ranked hypotheses** before testing any of them.

Each hypothesis is falsifiable:

> If `<cause>` is true, then `<probe>` will produce `<observable prediction>`.

No prediction, no hypothesis.

Share the ranked list when the user is available. Proceed without waiting unless a user-owned domain or product decision is required.

Keep a diagnosis log:

- hypothesis;
- probe;
- prediction;
- result;
- what the result ruled out.

## Phase 4 - Run Discriminating Probes

Test one hypothesis and one variable at a time. Negative evidence counts.

Prefer debugger or REPL inspection, then targeted logs at seams or state transitions. Every instrumentation point must distinguish named hypotheses.

Tag temporary instrumentation with a unique prefix such as `[DEBUG-a4f2]`.

For performance regressions, establish a measured baseline, classify the bottleneck, then profile, bisect, or probe against that constraint.

Pass the **cause gate** only when the winning hypothesis:

- produced its predicted observation;
- explains the minimised repro;
- explains the original symptom;
- survives a discriminating probe;
- materially stronger alternatives were falsified or made unnecessary by the evidence.

Otherwise rerank the hypotheses and continue probing.

## Phase 5 - Fix And Prove

In **diagnosis mode**, record the recommended fix and continue to cleanup without retaining a production behavior change. Return to the invoking caller when one exists; otherwise recommend `$implement` and stop with the diagnosis packet as its input.

In **fix mode**, apply the smallest change that addresses the proven cause, complete regression proof, and return the packet to the caller for review and Lock.

When a correct regression seam exists:

1. Turn the minimised repro into a failing regression test.
2. Watch it fail for the expected reason.
3. Apply the causal fix.
4. Watch the regression test pass.
5. Rerun the original Phase 1 loop against the unminimised scenario.

A correct seam reproduces the real bug pattern as it occurred at the call site.

When no correct regression seam exists, record the test-surface gap. Use the original red-capable loop to prove an authorized fix, but do not claim durable regression coverage.

For flakes, compare post-fix attempts and reproduction rate with the recorded baseline. One passing run is not proof.

For performance regressions, compare the post-fix measurement with the original baseline and requested constraint.

If a proposed fix fails the original loop, treat that result as evidence against the hypothesis. Remove only that attempted change, update the diagnosis log, and return to the ranked hypotheses instead of stacking fixes.

## Phase 6 - Cleanup And Return

Before return:

- remove every tagged instrumentation point and grep its prefix;
- delete disposable `.tmp/` harnesses, logs, and captures; move only explicitly approved version-controlled evidence to `.scratch/diagnosing-bugs/<bug-slug>/` and keep it in review and staging scope;
- inspect worktree status and preserve all pre-existing or unrelated changes;
- record whether the original loop remains red in diagnosis mode or is green in fix mode;
- return the diagnosis packet.

After causal evidence exists, ask what would have prevented the bug. Recommend `$improve-codebase-architecture` when the answer is a missing seam, tangled callers, hidden coupling, poor locality, or a shallow module. Keep that work outside the current diagnosis.

## Diagnosis Packet

Return:

- **Mode:** diagnosis or fix;
- **Source Trace:** symptom sources, expected behavior, evidence, environment, and known-good baseline;
- **Tight loop:** command, red output, and reproduction rate where relevant;
- **Load-bearing repro:** minimised case and unremovable conditions;
- **Hypothesis ledger:** ranked hypotheses, probes, and negative results;
- **Winning cause:** cause-gate evidence;
- **Fix authority:** authorized, not authorized, or not requested;
- **Fix:** applied change or recommended change;
- **Regression proof:** RED/GREEN results or documented seam gap;
- **Original scenario:** final loop result;
- **Cleanup:** instrumentation, disposable `.tmp/`, and tracked `.scratch/` status;
- **Validation:** additional checks and skipped reasons;
- **Residual risk:** remaining uncertainty and follow-up route.
- **Return owner:** invoking caller or `$implement` as the one next owner.

## Completion Criteria

Diagnosis is complete only when the exact symptom and Source Trace are recorded, a tight red-capable loop and load-bearing repro exist or their blocker is explicit, the cause gate is satisfied, temporary mutations are removed, the return owner is named, and the diagnosis packet is returned.

Fix work is complete only when implementation was authorized, the causal fix passed its regression proof when a correct seam exists, the original scenario went green, flake or performance comparisons were run when applicable, cleanup is complete, the caller is named, and the packet records residual risk.

A blocked investigation reports the missing loop, access, evidence, or causal proof. It does not claim a cause or fix.
