# Telemetry

Read only when the user requests usage measurement or a cost/usage budget materially
affects routing or completion.

The primary question is whether controlled delegation reduced total cost or
coordination work for the same accepted outcome. Fewer agents or a quieter lead
can be useful observations, but do not by themselves establish savings.

## Measure bounded actors and runs

Prefer usage, model, effort, timing, and cost metadata exposed directly by the
host. Bind observations to explicit run and actor boundaries and distinguish
requested settings from observed settings.

When available, track separately:

- selected lead input/output or reasoning usage, including activity while a worker
  was active;
- primary-worker usage, with its actual model and effort;
- supporting-agent usage by assignment, distinguishing routine work, architecture
  advice, and review under [Shared model routing](model-policy.md);
- total usage;
- number and approximate size of lead-worker handoffs;
- correction or replacement cycles;
- lead repository/tool activity during delegated implementation; and
- accepted completion and material verification quality.

A controlled run should leave the lead mostly dormant during implementation.
Repeated lead turns, large intermediate worker summaries, or frequent lead
repository inspection are evidence that coordination overhead may be defeating the
routing objective.

Missing telemetry is a coverage limit. Do not spend substantial lead context
reconstructing optional usage data.

If direct host telemetry is unavailable and the bundled
[telemetry helper](../scripts/telemetry.py) still supports the runtime, use its
current interface for a bounded observation. Treat helper output as best-effort
evidence, not an invoice or proof that a hard budget can be enforced.

Do not sum cumulative snapshots, cached-token subsets, overlapping actor durations,
or other counters unless their semantics are established.

## Make efficiency claims honestly

A savings claim requires a comparable route with the same accepted outcome and
materially equivalent task conditions. Choose the baseline for the question:
direct work by the same selected lead, controlled delegation, or native Ultra
delegation with equivalent acceptance and review obligations. State differences
that prevent a fair comparison.

Include failed and abandoned attempts when they consumed the measured budget.
Report wall time separately from summed actor work when actors overlap, and
distinguish subscription/quota observations from API-equivalent price estimates.

If the host cannot expose or enforce a requested hard budget boundary, state that
constraint rather than presenting an estimate as enforcement.
