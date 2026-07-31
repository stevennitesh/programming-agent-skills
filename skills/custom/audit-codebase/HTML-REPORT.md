# Durable HTML Audit Report

Create one self-contained UTF-8 report at
`.scratch/audit-codebase/<run-id>/report.html`. It is the linked repository
atlas, selector, evidence history, and current state projection. Current truth
comes from reinspection, not report age.

## Structural Contract

Version `6` requires:

```html
<meta name="audit-codebase-report-version" content="6">
<header id="report-header"
  data-repository-root="<canonical-root>"
  data-run-id="<run-id>"
  data-map-state="incomplete|complete">...</header>
<main>...</main>
```

Increment the structural version before requiring a new attribute, marker,
projection, or evidence element. Validation fixes may enforce already-declared
structure; they may not redefine it.

The report opens offline: no scripts, network requests, remote fonts, hidden
workflow state, or browser persistence. Escape arbitrary content into text
nodes. IDs are lowercase ASCII letters/digits separated by single hyphens.
Links are report fragments or explicit local file links.

Use semantic landmarks, non-skipping headings, visible focus, high contrast,
responsive layout, table captions/scoped headers, and a plain-language state
legend. Inline SVGs have a `viewBox`, `role="img"`, title, description,
fragment-linked nodes, and an adjacent text alternative. Color is never the
only state signal.

## Admission And Inspection

For a supplied report:

1. resolve exactly
   `<root>/.scratch/audit-codebase/<safe-run-id>/report.html`;
2. reject traversal, redirected/reparse-point parents, containment escapes, or
   mismatched embedded root/run identity;
3. decode strict UTF-8 and require structural version `6`; and
4. use objective-specific inspection:

```text
update_report.py inspect --repo-root <root> --report <report>
  --objective map

update_report.py inspect --repo-root <root> --report <report>
  --objective audit --subsystem-id <id>

update_report.py inspect --repo-root <root> --report <report>
  --objective analyze|close --candidate-id <id>
```

Inspection admits only the requested objective/state, reports its regions and
current records, and returns the report SHA-256. Invalid or ambiguous selection
is a zero-write blocker. Do not parse minified HTML manually or migrate reports
inside the skill.

## Map And Navigation

The Map is the table of contents. Every system has
`id="system-<id>"`; every subsystem is physically contained once as:

```html
<section id="subsystem-<id>"
  data-subsystem-id="<id>"
  data-state="mapped|incomplete|audited"
  data-source-identity="<identity>">...</section>
```

The `summary:map` region contains one relationship SVG and its adjacent linked
Map list. Draw each unique direct evidence-backed dependency once. Group nodes
by system and label the figure with its observation identity and arrow
convention. Omit reverse duplicates, transitive edges, file nodes, findings,
and candidate state.

Each subsystem has exactly two state projections:

```html
<a id="map-node-<id>" data-subsystem-projection="svg-map"
  data-subsystem-id="<id>" data-state="<state>"
  aria-label="<id>: <name>; <state>">
  <rect class="diagram-node state-<state>" .../>
  <text>...
    <tspan class="diagram-node-state"><state> · N files</tspan>
  </text>
</a>

<li id="map-list-<id>" data-subsystem-projection="linked-map"
  data-subsystem-id="<id>" data-state="<state>">
  ... <span class="status"><state></span> · N files
</li>
```

Their machine state, visible text, SVG state class, and SVG aria-label agree
with the subsystem container. `reaudit-subsystem` synchronizes these
atomically. A `summary:map` fragment is needed only when nodes, labels, file
counts, or edges change.

Begin each subsystem detail with a current-state flow figure: governing
contracts/decisions, callers and entry points, responsibility flow, direct
dependencies, Interfaces/outputs, dependents, and Proof Seams. The adjacent
detail owns exact evidence. Candidate proposals never appear in current-state
figures.

Account for every in-scope file under one subsystem, audit-owned shared
infrastructure with named consumers, or the excluded ledger. System lists may
repeat navigation facts but are not state projections.

## Subsystem Records

The static subsystem container owns the current source identity. Its narrative
owns Source Trace, lens dispositions, supported branches, current flow,
opportunities, retained complexity, gaps, disproved observations, coverage, and
local recommendation. Individual findings own current state and preserved
evidence:

```html
<article id="finding-<id>"
  data-finding-id="<id>"
  data-subsystem-id="<subsystem-id>"
  data-state="active|resolved|disproved">...</article>
```

Every `incomplete` or `audited` narrative contains all three collections,
including empty ones:

```html
<ul data-audit-collection="retained-complexity"
  data-subsystem-id="<subsystem-id>">
  <li id="retained-<id>" data-retained-id="<id>"
    data-subsystem-id="<subsystem-id>">...</li>
</ul>
<ul data-audit-collection="gaps" data-subsystem-id="<subsystem-id>">
  <li id="gap-<id>" data-gap-id="<id>"
    data-subsystem-id="<subsystem-id>">...</li>
</ul>
<ul data-audit-collection="opportunities"
  data-subsystem-id="<subsystem-id>">
  <li id="opportunity-<id>" data-opportunity-id="<id>"
    data-subsystem-id="<subsystem-id>">...</li>
</ul>
```

Each wrapper and record is physically inside and names its owning subsystem.
Do not render structured observations as prose-only substitutes.

## Candidate Records

Each candidate has one card and one index row, physically inside the same
subsystem:

```html
<article id="candidate-<id>"
  data-candidate-id="<id>" data-subsystem-id="<subsystem-id>"
  data-state="<state>" data-strength="<strength>">
  <span data-candidate-state="<id>"
    data-state-view="card"><state></span>
  ...
</article>

<tr id="candidate-index-<id>"
  data-candidate-id="<id>" data-subsystem-id="<subsystem-id>"
  data-state="<state>" data-strength="<strength>">
  <td><span data-candidate-state="<id>"
    data-state-view="index"><state></span></td>
  ...
</tr>
```

Card and row agree on ID, subsystem, state, strength, visible state, and pickup.
The card includes title, class/concepts, files/modules, member links, problem,
evidence, direction, benefit, safety floors, proof, decisions, and history.
Finding member links carry
`data-candidate-finding="<candidate-id>"`.

For `presented`, `decision pending`, and `blocked`, render one identical pickup
in each view:

```html
<code data-candidate-pickup="<id>"
  data-pickup-view="card|index">...</code>
```

For `analyzed`, both views either omit pickup or contain one identical pickup.
`implemented` and `disproved` omit it.

Analysis records validity/freshness, changed evidence/members, demonstrated
cost, Keep/Smallest sufficient/Structural/Replacement comparison,
recommendation, rejected alternatives, responsibilities, Interfaces, Seams,
Proof Seams, compatibility/migration/cutover/rollback where applicable, proof,
residual risk, and decision state. Keep history in
`<details data-candidate-history="<id>">`.

Implemented candidates additionally contain exactly one visible
`data-implemented-banner="<id>"` and:

```html
<dl data-implementation-result="complete"
  data-candidate-id="<id>"
  data-commit-sha="<sha>" data-tree-sha="<sha>"
  data-source-status="current|reachable"
  data-proof-status="accepted" data-review-status="accepted"
  data-repair-generations="<nonnegative-integer>"
  data-closure-status="complete" data-blockers="none">...</dl>
```

Header, `summary-progress`, and `report-footer` carry identical derived totals:

```text
data-candidate-progress="presented:N,decision-pending:N,analyzed:N,implemented:N,disproved:N,blocked:N"
data-finding-progress="active:N,resolved:N,disproved:N"
```

## Replaceable Regions

Regions are non-overlapping siblings inside the owning subsystem:

```html
<!-- audit-codebase:subsystem-narrative:<subsystem-id>:start -->
<div id="subsystem-narrative-<subsystem-id>">...</div>
<!-- audit-codebase:subsystem-narrative:<subsystem-id>:end -->

<!-- audit-codebase:finding:<id>:start -->
<article id="finding-<id>" ...>...</article>
<!-- audit-codebase:finding:<id>:end -->
<!-- audit-codebase:finding-insert:<subsystem-id> -->

<!-- audit-codebase:candidate-index:<id>:start -->
<tr id="candidate-index-<id>" ...>...</tr>
<!-- audit-codebase:candidate-index:<id>:end -->
<!-- audit-codebase:candidate-index-insert:<subsystem-id> -->

<!-- audit-codebase:candidate:<id>:start -->
<article id="candidate-<id>" ...>...</article>
<!-- audit-codebase:candidate:<id>:end -->
<!-- audit-codebase:candidate-insert:<subsystem-id> -->
```

The Map alone uses:

```html
<!-- audit-codebase:summary:map:start -->
<section id="summary-map">...</section>
<!-- audit-codebase:summary:map:end -->
```

Every pair/anchor occurs once, has the physical owner named by its ID, and no
region contains another. Fragments contain only their target element and no
markers, scripts, remote resources, or inline styles.

## Publication

Map renders the complete report to an invocation-owned sibling, validates all
structure, coverage, ownership, edges, navigation, state, IDs, links, and
observation identity, then atomically replaces `report.html`.

Incremental publication has two exact paths.

**Audit:** create manifest version `2`, run `reaudit-subsystem --validate-only`,
then publish the unchanged manifest with the returned bundle digest:

```json
{
  "version": 2,
  "expected_report_sha256": "<sha256>",
  "subsystem": {
    "id": "<id>",
    "state": "mapped|incomplete|audited",
    "source_identity": "<identity>",
    "narrative": "<relative-path>"
  },
  "map": "<optional-relative-summary-map-fragment>",
  "findings": [{"id": "<id>", "fragment": "<relative-path>"}],
  "candidates": [
    {"id": "<id>", "card": "<relative-path>", "index": "<relative-path>"}
  ]
}
```

Paths resolve inside the manifest directory. The digest covers the manifest and
every fragment.

**Analyze:** run `validate` with candidate/card sections, then run `update` with
the identical arguments plus the returned `--expected-bundle-sha256`.

Both paths validate prospective complete markup, ownership, lifecycle
transitions, changed anchors/links, derived progress, and report collision
before mutation. Publication atomically replaces then reads back. Generic
update cannot create `implemented`; use `close-candidate` with an admitted
completion packet.

The helper returns `stage`, `mutation_started`, `report_unchanged`, `effect`,
and `report_state`. Zero-write validation is not a publication attempt. After
validation, attempt publication exactly once. On failure, never retry,
hand-edit, switch mechanisms, or delay Return. Before replacement, preserve and
report the unchanged report; after replacement, report unknown state truthfully
unless read-back completed.

The helper owns markup validation, insert/replace mechanics, collision and
bundle checks, state projection synchronization, progress derivation, sibling
cleanup, atomic replacement, and read-back. The auditor owns evidence,
judgment, fragments/manifests, and their cleanup. The top-level root is the
single writer for one report invocation.

## Footer

End with coverage, failed/skipped proof, report path, objective outcome,
publication result, evidence limits, next user selection, and:

```text
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
