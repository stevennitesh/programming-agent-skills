# Investigation methods

Use only the method that can distinguish the live causal explanations. No fixed
tool, instrumentation framework, statistical threshold, or experiment count is
required.

## Intermittency, concurrency, and test pollution

Record failures relative to attempts or relevant exposure and the conditions of
each comparison. Preserve seeds, event ordering, concurrency, or captured inputs
when they matter. Stress or controlled scheduling can increase reproduction, but
confirm that the amplified failure is the original mechanism rather than overload
introduced by the harness. Zero failures in a short run does not prove elimination.

Logging, debugger pauses, synchronization, and sleeps can change scheduling. If
instrumentation suppresses the symptom, treat that as evidence about timing rather
than a fix. Prefer waiting on an observable condition over arbitrary delay unless
elapsed time is itself the behavior under test. Do not repair a production race by
making only the test wait longer.

For order-dependent tests, compare isolated behavior with the failing sequence and
narrow the polluting predecessor set. Inspect shared globals, resources, filesystem
state, clocks, environment, and cleanup at their owner. A test that passes alone
is not exonerated when the failure depends on leaked state.

## Cross-system and environment-specific failures

Follow one attributable request or state transition across the boundaries that can
change the explanation. Compare what the producer emitted with what the consumer
received, decoded, stored, and acted on. Preserve identity and ordering; similar
log lines from different requests do not form a causal chain.

For environment-only failures, compare the relevant deployed code, runtime and
dependency versions, configuration, permissions, filesystem or network semantics,
and data shape. Verify effective runtime values instead of assuming intended
configuration was loaded.

For restart or persistence-sensitive failures, inspect stored state, caches, locks,
and migrations. Clearing state can localize a trigger without proving deletion is
the correct fix. Preserve evidence before authorized destructive experiments.

When production cannot be replayed safely, use attributable traces, read-only
state, or sanitized artifacts and state the confidence limit. Do not replay a
captured request into effectful systems without authorization. If only a human can
reproduce the problem, request the minimal action and observation needed.

## History, differential checks, and reduction

Compare known working and failing states under the same relevant input and
environment. A historical implementation is a comparison, not automatically the
correct specification. A first-bad commit localizes introduction; inspect the
changed mechanism before calling it the root cause.

Use bisection only when the symptom classifier is reliable enough for the search.
Distinguish build or setup failure from the target defect and skip untestable
revisions rather than classifying them as bad. Preserve the user's active work
when executing historical states.

Reduce failing input or sequence only while the reduced case continues to expose
the reported mechanism.

## Challenge a shared premise after repeated failed fixes

When two or more attempted fixes fail the same gate while assuming the same
mechanism, write that shared premise explicitly before trying another variant.

Build the smallest rerunnable census that can show where the relevant imbalance or
failure is concentrated: by actor, partition, input class, state, worker, queue,
resource, or other causal unit. A census establishes distribution, not cause.

If the same subset repeatedly carries the skew, investigate what assigns or
preserves that role and test that assignment as the next causal hypothesis. Prefer
removing a demonstrated asymmetry over adding another compensating path around it.

If the census does not show the predicted skew, reject or weaken the shared premise
and look elsewhere. Keep the census only when it remains useful evidence.

## Performance regressions

Establish equivalent useful work, input scale, measured boundary, and relevant
environment before comparing versions. Separate workload, cache, and environment
differences from the regression.

Use profiling, tracing, or deterministic work counts to identify a plausible
mechanism, then measure its actual effect. A hotspot alone does not prove it caused
the observed slowdown.

Account for warmup, cache state, ordering, and noise when material. Faster
incomplete or behaviorally different work is not a repaired regression.
Open-ended optimization without a violated behavior or causal regression belongs
to [hillclimb](../../hillclimb/SKILL.md).
