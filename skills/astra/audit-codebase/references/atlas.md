# Visual atlas

Use for whole-codebase exploration, maintained architecture mapping, or continuing
an existing current-format audit workbench.

The helper is [atlas.py](../scripts/atlas.py). Use its current `--help` and
subcommand help for exact CLI syntax. The current format is authoritative; do not
migrate or continue older report schemas.

## Purpose

The HTML is a human decision surface, not a serialized debug dump. It should let
the user answer, in order:

1. What systems and subsystems exist?
2. How do they depend on each other?
3. What has been audited and what source has changed since?
4. What did an audit find?
5. Which improvement candidates are selectable?
6. What did deeper analysis conclude?

Forensic evidence remains available behind drill-downs rather than dominating the
first view.

## Ownership

The agent owns semantic judgment:

- system and subsystem boundaries and purpose;
- ownership, callers, interfaces, dependencies, and proof seams;
- evidence and counterevidence;
- six-lens audit dispositions;
- finding classification and affected scope;
- candidate grouping, qualitative strength, benefit, risk, and required proof;
- candidate analysis and recommendation.

The helper owns:

- repository and source identities;
- complete tracked-path ownership or explicit exclusions for Map;
- schema validation and relationship integrity;
- candidate and finding IDs supplied by the manifest;
- source freshness calculation;
- canonical JSON embedding;
- HTML escaping and deterministic rendering;
- writer exclusion, atomic publication, and read-back.

Do not hand-edit the generated HTML or embedded state.

## Map

Map records structure, not quality judgment.

Group current tracked source into meaningful systems and subsystems based on
runtime or domain ownership, not directory shape alone. Each subsystem records
its purpose, owned behavior, authority, callers, dependency evidence, interfaces,
proof seams, and owned paths.

Every tracked path belongs to one subsystem or one evidenced exclusion. Shared
infrastructure still needs one structural owner and named consumers.

Publish the map and stop for user selection. A mapped subsystem is not audited.

## Audit one selected subsystem

Rebuild the selected subsystem's current source trace and inspect the materially
distinct entry paths, callers, dependencies, interfaces, proof seams, and relevant
history.

Account for these six lenses:

- reliability;
- domain;
- design;
- simplification;
- coding practice; and
- performance.

Each lens ends as `complete`, `evidence gap`, or `not applicable`, with
evidence or a reason. This ledger is coverage bookkeeping, not a finding quota.

Record findings, systemic findings, and coherent improvement candidates. A
candidate must point to at least one admitted defect or opportunity. Give each
candidate one qualitative strength: `strong`, `worth exploring`, or
`speculative`.

Publish the updated report and stop for user selection.

## Analyze one selected candidate

Revalidate current source across every mapped subsystem in the candidate's
affected scope.

Analysis may end as:

- `analyzed`: current evidence supports a recommendation;
- `disproved`: the candidate no longer survives current evidence; or
- `blocked`: one exact decision or missing evidence prevents a responsible
  conclusion.

For an analyzed candidate, compare the materially relevant alternatives and record
their tradeoffs, recommendation, proof, and evidence limits.

Publish and stop. Analysis never creates tickets or starts implementation.

## Visual contract

Keep the report self-contained and offline. Inline CSS, SVG, and deterministic
local JavaScript are allowed; remote assets and network requests are not.

The rendered workbench should provide:

- a top-level coverage/status summary;
- a visual system/subsystem dependency map;
- mapped/audited/source-changed state badges;
- searchable subsystem/finding/candidate cards;
- six-lens coverage visualization;
- findings with expandable evidence;
- candidates with current problem, direction, affected scope, qualitative
  strength, risk, required proof, and any completed analysis;
- copyable explicit commands to Audit a subsystem or Analyze a candidate;
- provenance, exclusions, and history in lower-priority sections.

Local JavaScript may only navigate, filter, or copy text. It does not invoke
commands or mutate state.

## Freshness and publication

Map binds the current tracked repository identity. Audit and Analyze bind the
current source packets needed for their selected scope.

The report may refresh freshness markers without revalidating semantic judgment.
A changed source badge means the prior judgment may be stale; it does not erase or
silently renew that judgment.

After a failed or uncertain write, inspect the current report before retrying.
Never bypass source identity, report-digest, writer-lock, or read-back checks.

The report lives under `.tmp/audit-codebase/<run-id>/report.html` unless the user
or repository separately chooses a durable archival destination. Atlas creation
does not authorize a commit or publication elsewhere.
