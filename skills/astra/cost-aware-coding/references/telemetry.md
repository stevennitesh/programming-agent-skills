# Telemetry

Read only when the user requests usage measurement or a cost/usage budget materially
affects routing or completion.

## Measure bounded actors and runs

Prefer usage, model, timing, and cost metadata exposed directly by the current
host. Bind observations to explicit run and actor boundaries and distinguish
requested settings from settings actually observed.

Missing telemetry is a coverage limit. Do not search broadly through unrelated
sessions or delay ordinary execution merely to reconstruct optional usage data.

If direct host telemetry is unavailable and the bundled
[telemetry helper](../scripts/telemetry.py) still supports the current runtime,
use its current interface for a bounded observation. Treat helper output as
best-effort evidence, not an invoice or proof that a hard budget can be enforced.

Do not sum cumulative snapshots, cached-token subsets, overlapping actor durations,
or other counters unless their semantics are established for the runtime.

## Make cost claims honestly

A savings or efficiency claim requires a comparable baseline with the same accepted
outcome and materially equivalent task conditions. Include failed or abandoned
attempts when they consumed the measured budget.

Report wall time separately from summed actor work when actors overlap. Distinguish
subscription/quota observations from API-equivalent price estimates.

If the host cannot expose or enforce a requested hard budget boundary, state that
constraint rather than presenting an estimate as enforcement.
