---
name: diagnosing-bugs
description: Explicit-only investigation and optional causal fix for hard, intermittent, performance, environment-only, production-only, or otherwise causally ambiguous bugs.
---

# Diagnosing Bugs

Find and support the cause of one hard bug. When the caller authorizes source
changes, apply the smallest causal fix and prove the original symptom is gone.

Run only when explicitly selected. Ordinary deterministic bugs stay with the
implementation owner. If intended behavior is unsettled, return the decision to
its owner rather than treating broken output as the oracle. If the failure is
ordinary and locally reproducible without dedicated investigation, return
`route mismatch` with the facts unchanged.

Diagnosis alone retains no source or runtime behavior change. It may use
invocation-owned temporary local instrumentation when that is the cheapest
discriminating probe, but must restore it before Return. A request to fix the
bug grants authority only for the bounded local source change, not live or
production instrumentation, external writes, review, staging, commit, tracker
closeout, or push. Get separate approval before capturing sensitive data or
changing a live system, and redact secrets from commands, output, and artifacts.

Read the repository instructions and relevant code. Apply the repository's
engineering and domain guidance when present. Preserve unrelated work and keep
disposable artifacts under `.tmp/diagnosing-bugs/<bug-slug>/`.

## 1. Reproduce

Establish the expected behavior, actual behavior, exact symptom, and the
environment that exposes it. A characterization test records current behavior;
it does not prove that behavior is correct.

Build the nearest practical feedback loop that catches the reported symptom,
not a nearby failure. Choose the cheapest faithful method: an existing test,
CLI or HTTP command, browser path, captured replay, differential comparison,
bisection, or a small throwaway harness. Make it repeatable enough to guide the
investigation. For intermittent failures, track reproduction rate and relevant
conditions. For performance regressions, establish a comparable baseline.

If available evidence cannot support a useful probe, return the missing access,
artifact, or instrumentation approval. Make no causal claim.

## 2. Discriminate

Trace the symptom through the behavior owner, real callers, data, and state.
State a falsifiable explanation and the observation it predicts. Inspect or
instrument the cheapest signal that distinguishes it from the strongest viable
alternative. Change one variable at a time and prefer direct state inspection
over broad logging.

Minimize the reproduction when doing so reduces uncertainty or produces useful
regression evidence. Stop when another reduction costs more than it teaches or
would stop representing the real failure.

Treat the cause as supported only when the predicted observation occurs and the
explanation accounts for the original symptom. If a materially different cause
remains viable, run another useful authorized discriminating probe. When none
remains, return the viable explanation and the exact missing access, evidence,
or next probe without claiming completion.

## 3. Resolve

In diagnosis-only work, recommend the smallest causal fix and change no source
or runtime behavior.

With fix authority, correct the cause across affected callers instead of
guarding one symptom. Add or change a regression test only when repository
policy requires it or when it is the cheapest durable protection at a seam that
reaches the real bug pattern. Do not add a shallow test that cannot fail for the
reported behavior.

Rerun the original feedback loop after the fix. Compare reproduction rates or
performance measurements only on those branches. If the attempted fix fails,
remove only changes made for that attempt, preserve unrelated work, and resume
the investigation or return the exact remaining state.

## 4. Return

Remove temporary instrumentation and disposable artifacts. Return the symptom
and oracle, the supported cause or remaining uncertainty, the reproducer or
decisive evidence, the recommended or applied fix, verification, and any
material gap. Start no successor.

Diagnosis is complete only when the cause is supported. An unresolved return is
incomplete even when its evidence boundary is precise. An authorized fix is
complete only when the causal change is in scope, the original symptom no longer
reproduces, relevant proof passes, and debugging residue is gone.
