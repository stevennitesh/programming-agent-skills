# Telemetry

Read only when the user requests usage measurement or a cost/usage budget materially
affects routing or completion.

The primary question for this skill is whether delegation reduced **Astra lead
token/context consumption for the same accepted outcome**, not merely whether the
worker was cheap in isolation.

## Measure bounded actors and runs

Prefer usage, model, effort, timing, and cost metadata exposed directly by the host.
Bind observations to explicit run and actor boundaries and distinguish requested
settings from observed settings.

When available, track separately:

- Astra lead input/output or reasoning usage;
- Sol and Luna worker usage;
- total usage;
- number and approximate size of lead-worker handoffs;
- correction or replacement cycles; and
- accepted completion and material verification quality.

Missing telemetry is a coverage limit. Do not spend substantial Astra context
reconstructing optional usage data.

If direct host telemetry is unavailable and the bundled
[telemetry helper](../scripts/telemetry.py) still supports the runtime, use its
current interface for a bounded observation. Treat helper output as best-effort
evidence, not an invoice or proof that a hard budget can be enforced.

Do not sum cumulative snapshots, cached-token subsets, overlapping actor durations,
or other counters unless their semantics are established.

## Make efficiency claims honestly

A savings claim requires a comparable route with the same accepted outcome and
materially equivalent task conditions. The most relevant baseline is often direct
Astra execution versus Astra-led delegated execution.

Include failed and abandoned attempts when they consumed the measured budget.
Report wall time separately from summed actor work when actors overlap, and
distinguish subscription/quota observations from API-equivalent price estimates.

If the host cannot expose or enforce a requested hard budget boundary, state that
constraint rather than presenting an estimate as enforcement.
