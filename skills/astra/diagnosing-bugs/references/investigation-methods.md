# Investigation methods

Use only the method that can distinguish the live hypotheses. No fixed tool,
instrumentation framework, statistical threshold, or experiment count is required.

## Intermittency, concurrency, and test pollution

Record failures relative to attempts or relevant exposure and the conditions of
each comparison. Preserve seeds, event ordering, concurrency, or captured inputs
when useful. Stress or controlled scheduling can increase reproduction, but confirm
the amplified failure is the original mechanism rather than overload introduced
by the harness. Zero failures in a short run does not prove elimination.

Logging, debugger pauses, synchronization, and sleeps can change scheduling. If
instrumentation suppresses the symptom, treat that as evidence about timing, not
a fix. Prefer bounded waits for an actual observable condition over arbitrary
delays unless elapsed time is itself the behavior being tested. Do not repair a
race by making only the test wait longer while production remains incorrect.

For failures dependent on test order, compare isolation with the failing sequence
and narrow the polluting predecessor set. Inspect leaked globals, resources,
filesystem state, clocks, environment, and cleanup at the owner. Preserve enough
sequence to demonstrate the interaction; a test that passes alone is not exonerated.

## Cross-system and environment-specific failures

Follow one attributable request or state transition across relevant boundaries.
Compare what the producer actually emitted with what the consumer received,
decoded, stored, and acted on. Correlate identity and ordering; similar log lines
from different requests do not form a causal chain. Instrument only missing
decisive boundaries, not every layer by default.

For environment-only failures, compare relevant deployed code, dependency/runtime
versions, configuration, permissions, filesystem or network semantics, and data
shape. Verify actual runtime values rather than assuming the intended configuration
was loaded. For restart failures, inspect persisted state, caches, locks, and
migrations. Clearing state may localize the trigger but is not proof that deletion
is the correct fix. Preserve evidence before authorized destructive experiments.

When production cannot be replayed safely, use attributable traces, read-only
state, or sanitized artifacts and state the resulting confidence limit. Do not
replay a captured request into real effectful systems without authorization.
If only a human can reproduce it, give minimal steps and the observation needed;
do not require a custom human-driving script before accepting useful evidence.

## History, differential checks, and reduction

Compare known working and failing states under the same relevant input and
environment. A historical implementation is a comparison, not automatically the
correct specification. A first-bad commit localizes introduction; inspect its
mechanism before naming it the root cause.

Bisect only when the symptom classifier is reliable enough for the search. Distinguish
build/setup failure from the target defect and skip untestable revisions rather
than labeling them bad. Use isolated checkouts for historical execution so the
user's active work is preserved. Reduce a failing input or sequence incrementally,
retaining the conditions that reproduce the reported failure.

## Performance regressions

Establish equivalent useful work, input scale, measured boundaries, and relevant
environment before comparing versions. Separate workload or cache differences
from the regression. Use profiling or deterministic work counts to identify the
mechanism, then measure its actual impact. A hotspot alone is not proof that it
caused the observed slowdown.

Account for warmup, cache state, ordering, and noise when material. Avoid competing
measurements that distort the comparison. Fix correctness and preserve outputs;
faster incomplete work is not a repaired regression. Open-ended optimization with
no violated behavior belongs to a different task.
