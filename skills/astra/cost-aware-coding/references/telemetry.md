# Telemetry

Use this reference only when the user requests usage measurement or a hard budget
depends on it. Capture inexpensive start/end observations when exposed by the
host or helper below. Capture new actors when admitted
and refresh after model changes or resume. Use exposed metadata or one bounded
helper attempt per actor at each capture point; reuse known paths. After a failed
lookup, do not search further or repeat it at later captures without new location
evidence, unless measurement was requested or affects a hard constraint. Further
investigation must remain bounded and address that specific measurement or constraint.
Missing records,
tools, or telemetry are coverage limits, not a reason for broad searches or delay.
Report them under the main skill's completion guidance.
Detailed historical attribution and pricing are conditional on a measurement request.

## Observe without loading conversation text

Reuse existing runtime or dispatch observations for the fields and capture boundary
they actually cover; do not call the helper again for equivalent evidence. Requested
settings do not verify effective settings, and model identity alone supplies no
starting usage counters. Reuse an identity observation as a start snapshot only
for fields present at that boundary; missing fields remain unknown.

Prefer runtime metadata and usage events already exposed by the host. On local
Codex, `CODEX_THREAD_ID` can identify the root. Session files normally live under
`$CODEX_HOME/sessions` (default `~/.codex/sessions`). Use an exact known path or a
bounded filename lookup by thread ID; verify session identity before using it.
Track child IDs from dispatch results rather than scanning unrelated conversations.
For UUIDv7 IDs, the helper first checks nearby creation-date directories, then
falls back to a capped lookup. Use an already-known exact path in preference to
lookup; reaching the cap does not authorize another search to discover that path.

Run the bundled helper with the available Python interpreter. Paths below are
relative to this skill; resolve them from its installed location:

```text
python scripts/telemetry.py --thread-id <uuid>
python scripts/telemetry.py --thread-id <uuid> --session <exact-rollout.jsonl>
```

It reads a bounded tail and identity header, emits only allowlisted metadata as
JSON, and writes nothing. It reports unavailable or partial coverage explicitly.
Use the existing scratch/run record if start observations must survive the turn;
no separate ledger is required. Capture each known actor separately. Do not spawn
telemetry workers, poll counters, or dump raw logs into model context.

## Read model metadata

`turn_context` reports the latest observed logged settings, which may precede the
active turn. Match the active turn before treating them as current; they are not
proof of every provider execution.
Defaults, explicit requests, logged settings, and observed rerouting are distinct.
An unavailable recent context is unknown, not the configured default.

## When interpreting or estimating usage

Token events can contain cumulative and last-request counters. The helper does
not associate these counters with the adjacent model record: each observation has
its own timestamp and may precede the current turn. It reports the latest available
records within the tail, not complete turn coverage. The helper does
not derive task totals or costs: reset, resume, inherited-history, and parent/child
inclusion semantics must first be validated for the host. Never sum snapshots or
add cached/reasoning subsets to input/output totals blindly. Missing baselines,
partial tails, mixed models, or resets prevent unsupported aggregate claims.

For requested measurement, record exact run boundaries and actor coverage before
attributing usage. Count known spawns, transfers, transitions, and submitted repair
attempts from actual events/records, not inferred phases. These are overhead proxies,
not dollars or proof of savings. Wall time spans the measured run; overlapping actor
durations cannot be summed into wall time, and idle/user waiting is not model latency.
Pre-final captures exclude later output and must carry their cutoff.

Account usage limits are shared across tasks. Local tokens are not an invoice;
API-equivalent estimates need applicable pricing and known token categories, and
must be labeled estimates. A savings claim requires a comparable measured baseline.
This best-effort helper cannot enforce a hard budget.
