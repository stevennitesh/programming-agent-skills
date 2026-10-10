# Visual atlas

Use by default for codebase improvement, mapping, and guided exploration, or when
continuing an existing current-format workbench. An explicitly requested brief or
text-only assessment may stay in chat; a no-write assessment creates no report.

The helper is [atlas.py](../scripts/atlas.py). Use its current `--help` and
subcommand help for exact CLI syntax. The helper writes report/state format 4 and
accepts manifest format 1. Only the current report format is supported; create a
new map for an older report.
Read [Atlas maintenance](maintenance.md) when resuming a report, reconciling
structural changes, or recording authorized implementation and delivery.

## Purpose

The HTML is a human decision surface, not a serialized debug dump. It should let
the user answer, in order:

1. What systems and subsystems exist?
2. How do they depend on each other?
3. What has been audited and what source has changed since?
4. What did an audit find?
5. Which improvement candidates are selectable?
6. What did deeper analysis conclude?
7. Which fixes are verified, deferred, or awaiting requested delivery?

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
- structural reconciliation and preserved historical identities;
- separate outcome and delivery records, compact inspection, and static checks;
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

Inventory exposes Git entry modes and object IDs; content identities bind index
modes and object IDs, observed executable bits, and materialization as well as
working content. Staged blob changes count as source changes even if working bytes
are restored. Scoped identities reject index conflicts only among their requested
paths; a new map
needs an unconflicted index.
Gitlinks bind the recorded
submodule commit and, when initialized, its observed checkout and tracked content.
An unexpected regular file at a gitlink path binds its bytes and executable bits.
Empty deinitialized directories are supported; populated gitlink directories
without checkout metadata are rejected rather than reported as fresh.
Missing tracked files remain represented by their index entry and absence;
symlinks bind their link target without following it. These identities do not
establish that unavailable dependency behavior was inspected. State that coverage
limit; the helper does not initialize submodules or materialize missing files.
Gitlink checkouts must resolve beneath the requested repository root.

Show the map and stop for user selection unless the request already selects an
audit scope or delegates that selection. For a whole-repository audit, continue
through the mapped subsystems and make coverage limits visible. A mapped subsystem
is not audited.

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

Publish the updated report. Continue through an already-selected or delegated
audit scope; otherwise stop for user selection. An audit request alone does not
select candidates for deeper analysis.

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

When a visual makes the change easier to judge, supply an optional `comparison`
on the candidate or analysis: `caption`, `before`, and `after`. Each side contains
`nodes` with `id` and `label`, and `edges` with `from`, `to`, and `label`. Use
responsibility or data-flow diagrams to explain what moves, what callers retain,
and where data is read or transformed. Proposed structure is a hypothesis, not an
implemented result. The helper renders these records as escaped inline SVG;
raw HTML or scripts are not accepted. An analysis comparison refines an earlier
candidate comparison when present. No diagram quota is required.

Publish the analysis and continue only within the requested analysis scope.
Analysis alone never creates tickets or starts implementation. A combined request
continues through its authorized effects and records the results separately.

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
- copyable explicit commands to Audit a subsystem, Analyze a candidate, or inspect
  changed evidence and recorded outcomes;
- implementation, verification, deferral, and requested delivery status;
- provenance, exclusions, and history in lower-priority sections.

Coverage accounts for all mapped subsystems, separating current completed and
non-applicable lenses from evidence gaps, changed source, and unaudited scope.
Candidate freshness follows both its originating audit and its analysis source
packet, including evidence outside mapped ownership. Keep stale judgments visible
as prior evidence. Inspect changed paths, ownership, and recorded outcomes before
deciding which conclusions need reassessment. A verified fix can change the source
that supported the original diagnosis; it does not require repeating every
historical audit. Renew affected evidence before reusing an unverified stale
recommendation. Coverage freshness and fix verification remain separate.

Open the report through the host's supported HTML preview and inspect the actual
reading path, map links, filters, copyable selections, labels, and layout. Check
that progress and freshness mean what the user sees. Report unavailable preview
or clipboard capabilities without treating source or build checks as UI proof.
Record an unavailable capability once per environment and reconsider when the host
or capability changes. Repeated references to a limitation are not failed attempts.

Local JavaScript may navigate, filter, reveal retained history, or copy text. It
does not invoke commands or mutate state.

## Freshness and publication

Map binds the current tracked repository identity. Audit and Analyze bind the
current source packets needed for their selected scope.

Use compact `status` or filtered `inspect` to observe a resumed workbench without
writing it; use `refresh` to publish current observations before showing the HTML.
Check ownership drift separately from the freshness of existing source packets.
Freshness markers can update without revalidating semantic judgment.
A changed source badge means the prior judgment may be stale; it does not erase or
silently renew that judgment.
Source observations retain per-path fingerprints for changed-path inspection.

Run `check-report` for canonical state, relationship integrity, ownership coverage,
HTML anchors, IDs, and selection commands. Its static result reports current
ownership and source changes separately and does not establish visual verification.

After a failed or uncertain write, inspect the current report before retrying.
Never bypass source identity, report-digest, writer-lock, or read-back checks.

The report lives under `.tmp/audit-codebase/<run-id>/report.html` unless the user
or repository separately chooses a durable archival destination. Atlas creation
does not authorize a commit or publication elsewhere.
