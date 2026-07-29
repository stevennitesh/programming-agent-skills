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
- `<meta name="audit-codebase-report-version" content="3">`;
- no network requests, executable scripts, hidden workflow state, remote
  fonts, CDN assets, or browser-only persistence;
- arbitrary repository, user, and returned content only in escaped text nodes;
- strict internal ASCII IDs and only report fragments or explicit local file
  links in `href`;
- one header, labeled map navigation, main region, footer, non-skipping
  headings, visible focus, high contrast, and narrow-screen layout;
- captions and scoped headers for tables; and
- responsive inline SVG figures with a `viewBox`, `role="img"`, titles,
  descriptions, fragment-linked nodes, and adjacent text alternatives.

Use dark mode with reusable background, surface, border, text, muted, link,
focus, positive, warning, and danger tokens. Never encode state by color alone.
Style figures through reusable report classes; section fragments use no inline
styles. Diagrams summarize the adjacent evidence and never become another
ledger or validation workflow.
These are template invariants checked at Map publication, not re-proved as a
separate workflow during every section update.

## Entry Gate

Before deriving selection state from a supplied report:

1. resolve the repository root and require exactly
   `<root>/.scratch/audit-codebase/<safe-run-id>/report.html`;
2. reject traversal, redirected or reparse-point parents, a path outside that
   root, or mismatched embedded repository and run identities;
3. decode strict UTF-8 and require report version `3`, one map state, and one
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

Lead the `summary:map` region with one repository relationship figure. Group
every subsystem node inside its system container and draw every unique direct
evidence-backed dependency exactly once. Link each node to its subsystem, state
one arrow convention, label it `Observed at <map identity>`, and include a
legend. Route within-system edges inside
their container and cross-system edges through container boundaries. Do not add
reverse caller or dependent duplicates, transitive edges, file nodes, findings,
or candidate state. Keep the linked text table of contents adjacent and
canonical for exact labels, state, pickups, and accessible navigation.

Begin each subsystem detail with one current-state context-flow figure showing
its governing contracts or decisions, callers and entry points, material
responsibility flow, direct dependencies, Interfaces or outputs, dependents,
and Proof Seams. Map shows only mapped behavior; Audit may refine the selected
flow with verified responsibility steps and branches. Analyze updates it only
when revalidation changes current-source relationship facts. Never render a
proposed candidate shape into the current-state figure. The adjacent detail
remains the evidence owner. After a later selected-unit update, unchanged map
content is a labeled historical observation, not an assertion of current truth.

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

The candidate card owns candidate facts. Render each as:

```html
<article
  id="candidate-<candidate-id>"
  data-candidate-id="<candidate-id>"
  data-state="<state>"
  data-strength="<strength>"
>
```

Include its title, class and concepts, files and Modules, member links, problem,
current evidence, direction, expected benefit, safety floors, required proof,
decisions, state, strength, and pickup. Lead with current state and its
available action, if any. After Analyze, keep the presentation and analysis
record in `<details data-candidate-history="<candidate-id>">` so history remains
available without dominating navigation.

Render its index row as a required projection with the same
`data-candidate-id`, `data-state`, and `data-strength` values. Mark an exact
visible pickup in each view as:

```html
<code
  data-candidate-pickup="<candidate-id>"
  data-pickup-view="card|index"
>...</code>
```

The card and row pickup text must match. Omit both elements when no pickup
exists. The visible row repeats the remaining facts and links to the card.

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

For `implemented`, show a visible
`data-implemented-banner="<candidate-id>"`, keep history collapsed, and append
the visible completion packet plus one machine-readable evidence element:

```html
<dl
  data-implementation-result="complete"
  data-candidate-id="<candidate-id>"
  data-commit-sha="<sha>"
  data-tree-sha="<sha>"
  data-source-status="current|reachable"
  data-proof-status="accepted"
  data-review-status="accepted"
  data-repair-generations="<nonnegative integer>"
  data-closure-status="complete"
  data-blockers="none"
>...</dl>
```

Show Analyze for `presented`, exact re-entry for `decision pending` or
`blocked`, zero or one user-selected next-owner pickup for `analyzed`, and no
pickup for `implemented` or `disproved`.

Header, progress summary, and footer use IDs `report-header`,
`summary-progress`, and `report-footer`. Each carries the same
`data-candidate-progress` value in this fixed order:

```text
presented:<n>,decision-pending:<n>,analyzed:<n>,implemented:<n>,disproved:<n>,blocked:<n>
```

## Stable Update Markers

Wrap independently replaceable regions:

```html
<!-- audit-codebase:subsystem:<id>:start -->
<section id="subsystem-<id>">...</section>
<!-- audit-codebase:subsystem:<id>:end -->

<!-- audit-codebase:candidate:<id>:start -->
<article id="candidate-<id>">...</article>
<!-- audit-codebase:candidate:<id>:end -->

<!-- audit-codebase:candidate-index:<id>:start -->
<tr id="candidate-index-<id>" ...>...</tr>
<!-- audit-codebase:candidate-index:<id>:end -->

<!-- audit-codebase:summary:<id>:start -->
<section id="summary-<id>">...</section>
<!-- audit-codebase:summary:<id>:end -->
```

IDs use lowercase ASCII letters, digits, and single hyphens. Marker pairs are
unique and properly nested. Candidate cards, index rows, and affected summaries
have independent, non-overlapping regions. Map publication creates them; later
publication replaces one or more marked regions atomically.
Use `summary:report-header` and `summary:report-footer` markers around their
same-named anchors.

## Report Consistency

Before publication, validate the prospective complete report:

- report version is `3`;
- every candidate ID has exactly one card and one index row;
- each card and row agree on ID, state, strength, and marked pickup text;
- pickup follows the candidate-state rules;
- header, progress, and footer totals equal the card states; and
- every implemented card has one complete matching implementation evidence
  element.

These are projections of candidate-card facts, not another evidence ledger.

## Map Publish Gate

For New, Continue, or explicit Refresh:

1. render the complete report to one invocation-owned sibling;
2. verify template invariants, Report Consistency, contained paths, scope, IDs, states, file
   assignments, evidence-backed edges, member ownership, map navigation,
   current pickups, marker uniqueness, and internal links;
3. verify current Map observation identity and target non-collision; and
4. atomically replace `report.html`, then remove only the invocation sibling.

On interruption, source change, collision, or failure, preserve the last
verified report. An incomplete Map may publish only with exact remaining
coverage and one Continue pickup.

## Incremental Publish Gate

After a passed Entry Gate, inspect the selected report through the helper.
Render only the selected regions, then run zero-write `validate`. Correct
rendering or validation failures while the helper reports
`mutation_started: false` and `report_unchanged: true`; this is preparation, not
a publication attempt. Once validation passes, attempt incremental publication
exactly once with one `update` call containing every selected region:

1. render only the selected subsystem or candidate plus affected summary
   fragments;
2. require strict UTF-8, safe text, the exact target anchor, no marker
   injection, and no executable or remote-resource markup;
3. replace the unique marked regions, parse the complete result, and verify
   Report Consistency, changed anchors, and changed-fragment links;
4. verify the source report SHA-256 is unchanged; and
5. atomically replace and read back the report.

Use the package-owned standard-library helper:

```text
python <audit-codebase>/scripts/update_report.py inspect
  --repo-root <root>
  --report <absolute-report-path>
  [--candidate-id <id>]

python <audit-codebase>/scripts/update_report.py validate
  --repo-root <root>
  --report <absolute-report-path>
  --expected-sha256 <sha256>
  --section <kind> <id> <fragment-path>
  [--section <kind> <id> <fragment-path> ...]

python <audit-codebase>/scripts/update_report.py update
  --repo-root <root>
  --report <absolute-report-path>
  --expected-sha256 <sha256>
  --section <kind> <id> <fragment-path>
  [--section <kind> <id> <fragment-path> ...]
```

Fragments contain only the inner target element and must not contain update
markers. For example:

```html
<article id="candidate-alpha-fix"
  data-candidate-id="alpha-fix"
  data-state="analyzed"
  data-strength="Strong">...</article>
```

The helper owns collision detection, changed-section and complete-report
validation, sibling cleanup, atomic replacement, and read-back. Every success or
error reports `stage`, `mutation_started`, and `report_unchanged`; success also
returns changed regions, validated candidate states, and progress totals. The
caller owns and removes fragment files. The helper does not judge codebase
evidence, render the Map, or maintain another ledger.

After the root admits a matching implementation completion packet under
`CANDIDATE-CONTRACT.md`, publish its derived projections once without fragments:

```text
python <audit-codebase>/scripts/update_report.py close-candidate
  --repo-root <root>
  --report <absolute-report-path>
  --expected-sha256 <sha256>
  --candidate-id <id>
  --completion <completion-json>
```

If the attempt fails, stop publication immediately. Do not rerun the helper,
hand-edit the report, use another publication mechanism, or delay the Return.
Preserve the last report and return completed source analysis with `Publication
result: failed`, the failed region, and the preserved report identity. This is
an artifact failure, not a codebase gap.

## Navigation And Footer

Provide the map as the system/subsystem table of contents, candidate links
inside their subsystem, back-to-map and back-to-subsystem links, and visible
visited and focus states. Changed-fragment links must resolve exactly once.

End with audit and candidate-analysis coverage, failed or skipped proof, and:

```text
Objective result: complete | incomplete | blocked
Publication result: updated | unchanged | failed
Outcome: complete | partial | blocked
Report: <absolute path> | none
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
