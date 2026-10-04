# Investigation methods

Select, combine, and adapt methods that can distinguish the live causal
explanations. No fixed tool, instrumentation framework, statistical threshold, or
experiment count is required. Prefer existing diagnostics or a small targeted
probe over building new diagnostic infrastructure.

## Targeted instrumentation and runtime inspection

When the symptom appears downstream of the bad state, observe selected boundaries
or invariants to narrow the first divergence. Assertions, correlated traces,
counters, or watchpoints can expose the relevant input, output, write, identity,
or state transition. Capture what can change the explanation rather than logging
everything. Account for filtering, sampling, buffering, and timing changes when
interpreting missing or reordered observations.

For hangs or unexplained stalls, thread or task snapshots, progress counters, and
resource or lock ownership can distinguish waiting from slow progress. For
corruption, races, or leaks, consider applicable runtime checks, sanitizers, or
heap and resource profiles. Choose tools supported by the actual runtime and
interpret their findings within the paths and properties they observe.

## Controlled interventions and replay

When several causes fit the observations, vary a suspected causal factor while
keeping relevant comparison conditions stable. A reversible intervention or
negative control can test whether the predicted consequence follows. If several
factors change together, limit attribution to what the comparison distinguishes.

For suspected timing or recovery failures, consider controlled scheduling,
cancellation, timeouts, or injection of a relevant partial failure. Exercise the
specific causal boundary within the authorized scope. Connect an induced failure
to the reported mechanism; exposing some failure does not explain the incident.

For rare failures, preserve captured inputs, seeds, event ordering, or a recorded
execution when supported and useful. Replay can let successive probes examine
the same failure. Establish which nondeterminism and external behavior the replay
preserves before treating it as equivalent to the original execution.

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

Use input or sequence reduction, including delta debugging when useful, to narrow
the elements needed for failure. Keep the failure classifier tied to the reported
symptom; a smaller case that instead fails during setup does not preserve the
mechanism. Retain relevant interactions rather than assuming one input element
must be responsible.

## Reassess an investigation that stops producing information

When attempts stop producing useful information, identify the shared premise and
choose an observation that could reject it or distinguish another explanation.
Recheck the failure classifier, effective runtime, or instrument when those could
explain the uninformative results. Change the investigation in response to
evidence rather than requiring a fixed number of failed fixes.

When concentration or imbalance could distinguish causes, a small rerunnable
census by actor, partition, input class, state, queue, or resource may help. Compare
failures with relevant exposure; a census establishes distribution, not cause.

If a subset carries unexplained skew, investigate what assigns or preserves that
role and test its causal contribution. If the predicted skew is absent, weaken or
reject that premise. Keep a census only while it provides useful evidence; other
failures may need a different probe entirely.

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
