---
name: diagnosing-bugs
description: "Diagnose broken, failing, flaky, slow, environment-only, or production-only behavior when the exact symptom, cause, or trusted red-capable reproduction is uncertain. Fix only when implementation is authorized."
---

# Diagnosing Bugs

**Trace -> Loop -> Minimise -> Hypothesise -> Probe -> Prove -> Return**

**No red-capable loop, no hypothesis. No proven cause, no fix.**

## Boundary

Own uncertain diagnosis through causal proof and regression evidence.

- **Diagnosis mode:** prove the cause and recommend the smallest fix; leave production behavior unchanged.
- **Fix mode:** only with user or caller implementation authority; apply the smallest causal fix.
- **Caller:** owns scope, review, staging, commit, tracker or external mutation, push, release, Lock, and architecture follow-up.

A caller-invoked run returns its diagnosis packet to that caller. A standalone diagnosis-only run recommends `$implement` as its one next owner.

Hand off to `$tdd` only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known before **Trace**. Retain the original caller; do not bounce between skills without new evidence.

Apply `docs/agents/engineering-contract.md` and `docs/agents/domain.md` when present. Put disposable artifacts under `.tmp/diagnosing-bugs/<bug-slug>/`. Live or production instrumentation, persisted telemetry, external writes, and sensitive-data capture require explicit approval.

## 1. Trace

Record the Source Trace, including expected and actual behavior, exact evidence, reproducer and environment, known-good baseline, contradictions, and missing evidence. Broken output is not the expected-behavior oracle.

Before instrumentation, record the fixed point, worktree state, and pre-existing changes. Existing evidence satisfies a later gate only when its source and result are recorded.

## 2. Loop

**Relentless diagnosis:** build and run one command that catches the exact reported symptom.

Start at the nearest automated seam; escalate through replay, a throwaway harness, fuzzing, bisection, differential comparison, then structured HITL. When automation is impossible, use a shell-appropriate HITL harness that captures the exact symptom, expected and actual behavior, steps, attempts, failures, environment, and observations.

The **Loop** must be:

- **sharp:** asserts the exact symptom;
- **repeatable:** deterministic or measured by reproduction rate;
- **tight:** practical to run repeatedly;
- **agent-runnable:** unattended except for structured HITL.

For flakes, record attempts, failures, rate, seed, time, environment, and concurrency. For performance, record the baseline and constraint.

If no red-capable Loop can be built, return blocked with attempts, missing evidence, and the required access, artifact, or instrumentation approval. Make no causal claim.

## 3. Minimise

Remove one input, caller, configuration, dependency, environment condition, or step at a time; rerun the Loop after every cut.

Stop when every remaining element is load-bearing or explicitly unremovable without destroying an environment- or production-only condition. The minimised repro must still explain the original scenario.

## 4. Hypothesise

Rank three to five falsifiable hypotheses before testing them:

> If `<cause>` is true, `<probe>` will produce `<observable prediction>`.

Keep a ledger of hypothesis, probe, prediction, result, and what the result ruled out.

## 5. Probe

Test one hypothesis and one variable at a time. Prefer direct state inspection, then targeted instrumentation that distinguishes named hypotheses. Tag every temporary instrumentation point uniquely.

The **cause gate** passes only when the winning cause:

- produces its predicted observation;
- explains the minimised repro and original symptom;
- survives a discriminating probe;
- leaves stronger alternatives falsified or unnecessary.

Otherwise rerank and continue probing.

## 6. Prove

In diagnosis mode, record the recommended causal fix and retain no production behavior change.

In fix mode, when a correct regression seam reproduces the real bug pattern:

1. turn the minimised repro into a regression test;
2. observe RED for the expected reason;
3. apply the causal fix;
4. observe GREEN;
5. rerun the original, unminimised Loop.

When no correct seam exists, record the test-surface gap and prove the authorized fix with the original Loop without claiming durable regression coverage.

Compare flake rates or performance measurements with their baselines. If the original Loop remains red, remove only the attempted fix, record the evidence, and return to **Hypothesise**.

## 7. Return

Remove tagged instrumentation and disposable `.tmp/` artifacts, verify their absence, and reconcile the worktree with its starting state. Preserve durable evidence under `.scratch/diagnosing-bugs/<bug-slug>/` only with explicit approval.

Return one diagnosis packet containing:

- mode, fix authority, and return owner;
- Source Trace, tight Loop, and load-bearing repro;
- hypothesis ledger and cause-gate evidence;
- applied or recommended fix;
- regression proof or seam gap;
- original-scenario result;
- cleanup, validation, residual risk, and skipped checks.

Record architecture concerns as follow-up evidence for the caller; do not start architecture work here.

Diagnosis is complete only when the cause gate passes, cleanup is complete, and the packet is returned. Fix work additionally requires authority, regression proof where a correct seam exists, a green original scenario, and relevant flake or performance comparison. A blocked packet names the missing loop, access, evidence, or causal proof and claims no cause or fix.
