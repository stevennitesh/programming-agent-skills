# Durable HTML Audit Report

Render one self-contained report at
`.scratch/audit-codebase/<run-id>/report.html`. It is the durable repository
atlas, subsystem and candidate selector, finding record, and analysis history.
The report preserves evidence; current truth comes from each selected
objective's Source Trace.

## Portable Template

Write strict UTF-8 HTML that opens offline, with:

- `<html lang="en">`, a meaningful `<title>`, and
  `<meta charset="utf-8">`;
- `<meta name="audit-codebase-report-version" content="2">`;
- no network requests, executable scripts, hidden workflow state, remote
  fonts, CDN assets, or browser-only persistence;
- arbitrary repository, user, and returned content only in escaped text nodes;
- strict internal ASCII IDs and only report fragments or explicit local file
  links in `href`;
- one header, labeled map navigation, main region, footer, non-skipping
  headings, visible focus, high contrast, and narrow-screen layout;
- captions and scoped headers for tables; and
- adjacent text alternatives for useful static SVG diagrams.

Use dark mode with reusable background, surface, border, text, muted, link,
focus, positive, warning, and danger tokens. Never encode state by color alone.
These are template invariants checked at Map publication, not re-proved as a
separate workflow during every section update.

## Entry Gate

Before deriving selection state from a supplied report:

1. resolve the repository root and require exactly
   `<root>/.scratch/audit-codebase/<safe-run-id>/report.html`;
2. reject traversal, redirected or reparse-point parents, a path outside that
   root, or mismatched embedded repository and run identities;
3. decode strict UTF-8 and require report version `2`, one map state, and one
   unique selected subsystem or candidate anchor in an admissible state; and
4. record the report SHA-256 for collision detection.

Do not validate every unrelated count, link, command, or evidence identity at
Entry. A corrupt or ambiguous selected identity returns `blocked` with zero
writes. Report age and unrelated source drift pass to the selected objective's
Current Evidence Gate.

## Provenance And Freshness

The header shows repository, Map state, run ID, map observation identity and
time, audit progress, candidate-analysis progress, scope, workloads and
environments, and a plain-language state legend. State that candidate strength
is neither global priority nor mutation authority and coverage is not a release
decision.

For a Git-addressed target, record commit and tree. For a live target, record
HEAD provenance and one compact digest derived from sorted in-scope path, mode,
and content identities. Do not render a per-file hash ledger.

Each subsystem and candidate shows:

```text
Last verified identity:
Current Source Trace or owned paths:
Evidence fingerprint:
```

Older sections are historical evidence, not a reason to block current analysis.
Audit and Analyze replace the selected unit's freshness and evidence after
reinspection.

## Linked System Map

Use the map as the table of contents. Give every system
`<section id="system-<system-id>">` and subsystem
`<section id="subsystem-<subsystem-id>">`. Display `mapped`, `incomplete`, or
`audited`.

Each map node contains stable ID, name, purpose, state, file count, direct
evidence-backed dependencies, and its valid user pickup. Its detail contains
entry points, Interfaces, owned paths, shared consumers, callers, dependents,
flows, domain terms, decisions, Proof Seams, relationship evidence, and
evidence fingerprint.

Account for every in-scope file under one primary subsystem, shared
infrastructure with one audit-owning subsystem and named consumers, or an
excluded ledger with reason. Never rank subsystems or add a global
recommendation.

## Subsystem Audit

An audited or incomplete subsystem renders:

- current Source Trace and mandatory six-class lens ledger;
- supported scenarios and checked state or failure branches;
- verified defects in severity order;
- opportunities by primary class;
- retained complexity and Revisit Triggers;
- evidence gaps, disproved items, and duplicates;
- performance evidence when applicable;
- local candidate index and cards when audited;
- one advisory subsystem-local recommendation; and
- exact remaining obtainable coverage when incomplete.

Keep every member finding visible when it belongs to a candidate. Candidate
pickups appear only for an audited subsystem.

## Candidate Card And Analysis

Give each candidate `<article id="candidate-<candidate-id>">` with its title,
strength, class and concepts, files and Modules, member links, problem, current
evidence, direction, expected benefit, safety floors, required proof, decisions,
state, and valid pickup.

After Analyze, append:

- current-source validity and last verified identity;
- current Source Trace and changed evidence or members;
- current shape and demonstrated cost;
- Keep, Smallest sufficient change, Structural change, and Replacement;
- recommendation and rejected alternatives;
- material Responsibilities, Interfaces, Seams, and Proof Seams;
- affected contracts and applicable compatibility, migration, cutover, and
  rollback;
- proof plan, residual risk, decision status, and candidate state; and
- conditional decision, evidence, or next-owner content only when
  `CANDIDATE-FOLLOWUP.md` applies.

Show Analyze for `presented`, exact re-entry for `decision pending` or
`blocked`, zero or one user-selected next-owner pickup for `analyzed`, and no
pickup for `disproved`.

## Stable Update Markers

Wrap independently replaceable regions:

```html
<!-- audit-codebase:subsystem:<id>:start -->
<section id="subsystem-<id>">...</section>
<!-- audit-codebase:subsystem:<id>:end -->

<!-- audit-codebase:candidate:<id>:start -->
<article id="candidate-<id>">...</article>
<!-- audit-codebase:candidate:<id>:end -->

<!-- audit-codebase:summary:<id>:start -->
<section id="summary-<id>">...</section>
<!-- audit-codebase:summary:<id>:end -->
```

IDs use lowercase ASCII letters, digits, and single hyphens. Marker pairs are
unique and properly nested. Map publication creates them; later publication
replaces one or more non-overlapping marked regions atomically.

## Map Publish Gate

For New, Continue, or explicit Refresh:

1. render the complete report to one invocation-owned sibling;
2. verify template invariants, contained paths, scope, IDs, states, file
   assignments, evidence-backed edges, member ownership, map navigation,
   current pickups, marker uniqueness, and internal links;
3. verify current Map observation identity and target non-collision; and
4. atomically replace `report.html`, then remove only the invocation sibling.

On interruption, source change, collision, or failure, preserve the last
verified report. An incomplete Map may publish only with exact remaining
coverage and one Continue pickup.

## Incremental Publish Gate

After a passed Entry Gate, attempt incremental publication exactly once with
one `update_report.py` call containing every selected region:

1. render only the selected subsystem or candidate plus affected summary
   fragments;
2. require strict UTF-8, safe text, the exact target anchor, no marker
   injection, and no executable or remote-resource markup;
3. replace the unique marked regions, parse the complete result, and verify the
   changed anchors and changed-fragment links;
4. verify the source report SHA-256 is unchanged; and
5. atomically replace the report and remove invocation fragments.

Use the package-owned standard-library helper:

```text
python <audit-codebase>/scripts/update_report.py
  --repo-root <root>
  --report <absolute-report-path>
  --expected-sha256 <sha256>
  --section <kind> <id> <fragment-path>
  [--section <kind> <id> <fragment-path> ...]
```

The helper owns collision detection, changed-section validation, sibling
cleanup, and atomic replacement. It does not judge codebase evidence, render
the Map, or maintain another ledger.

If the attempt fails, stop publication immediately. Do not rerun the helper,
hand-edit the report, use another publication mechanism, or delay the Return.
Preserve the last report and return completed source analysis with `Report
update: failed`, the failed region, and the preserved report identity. This is
an artifact failure, not a codebase gap.

## Navigation And Footer

Provide the map as the system/subsystem table of contents, candidate links
inside their subsystem, back-to-map and back-to-subsystem links, and visible
visited and focus states. Changed-fragment links must resolve exactly once.

End with audit and candidate-analysis coverage, failed or skipped proof, and:

```text
Outcome: complete | incomplete | blocked
Report update: updated | unchanged | failed
Report: <absolute path> | none
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
