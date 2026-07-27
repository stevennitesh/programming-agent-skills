# Durable HTML Audit Report Contract

Render one self-contained report at
`.scratch/audit-codebase/<run-id>/report.html`. It is the sole durable map,
subsystem selector, candidate selector, finding record, and analysis history.

## Portability

Write strict UTF-8 HTML with `<html lang="en">`, a meaningful `<title>`, and
`<meta charset="utf-8">`. Open offline with no network requests or runtime
JavaScript. Embed CSS and static SVG only.

Place arbitrary repository, user, and returned-packet content only in escaped
text nodes. Generate IDs from a strict internal ASCII grammar. Allow only
report-local fragments and explicitly rendered local file links. Put no
arbitrary content in CSS, raw HTML, URL schemes, or SVG markup; escape SVG
text separately.

No Tailwind CDN, Mermaid CDN, remote fonts, executable scripts, hidden app
state, or browser-only persistence.

Use a visible-on-focus skip link, one `<header>`, one labeled map `<nav>`, one
`<main>`, one `<footer>`, non-skipping headings, stable anchors, visible focus,
high-contrast text, text labels for color, and a narrow-screen layout.
Use DOM-order keyboard navigation. Tables need a `<caption>` and scoped header
cells. Diagrams need an adjacent text alternative; SVG uses `role="img"` and
`aria-labelledby`.

## Dark Theme

Render dark mode as the only screen theme. Set
`<meta name="color-scheme" content="dark">` and
`:root { color-scheme: dark; }`. Do not add a light-theme toggle or
`prefers-color-scheme` branch.

Define and reuse:

```css
:root {
  color-scheme: dark;
  --background: #0b1020;
  --surface: #111827;
  --surface-raised: #1f2937;
  --border: #374151;
  --text: #f3f4f6;
  --text-muted: #cbd5e1;
  --link: #93c5fd;
  --focus: #fbbf24;
  --positive: #34d399;
  --warning: #fbbf24;
  --danger: #fb7185;
}
```

Use these tokens consistently. Use status colors as text or borders on dark
surfaces unless a filled badge has verified WCAG AA text contrast. Never
encode status by color alone.

## Header

Show repository, snapshot status, Map status, run ID, report content identity,
audit progress,
candidate-analysis progress, scope, workloads and environments, generation
time, and a plain-language state legend. State that candidate strength is
neither global priority nor mutation authority and coverage is not a release
decision.

## Snapshot Manifest

Store the complete logical identity needed to resume without another durable
ledger:

- Git-addressed target: resolved commit and tree object IDs;
- live target: resolved `HEAD` tree plus a sorted overlay for every modified,
  deleted, or untracked working-tree path.

An overlay entry contains the exact forward-slash repo-relative path, kind or
mode, and SHA-256 of raw bytes; a deleted path uses an explicit deletion
marker instead of a hash. Hash a symlink's target bytes; use the resolved
object ID for a submodule. The base tree plus overlay must derive every
in-scope path and byte identity. Staging state alone is irrelevant.

Include scope, exclusions, the report path, and its transient sibling. Mark
both artifact paths excluded from audited content and drift. Render the
canonical manifest once in native `<details>` with visible counts and summary;
other sections link to its entries instead of duplicating them.

Every continuation, subsystem audit, candidate analysis, and returned-evidence
update verifies this manifest before changing the report.

An identity mismatch permits only one atomic status update: set `Snapshot:
stale`, expose the fully instantiated Refresh pickup, and preserve all prior
content. Make no map, audit, or candidate judgment against mixed bytes.

### Resume Gate

Before deriving state from a supplied report:

1. resolve the repository root and require exactly
   `<root>/.scratch/audit-codebase/<safe-run-id>/report.html`;
2. reject traversal, redirected or reparse-point parents, a mismatched embedded
   run or repository identity, and any path outside that root;
3. decode strict UTF-8 and verify the state block, manifest, counts, file
   ownership, IDs, member links, and internal links; and
4. record the source report's SHA-256 for the Finalize Gate.

A corrupt or inconsistent report returns `blocked` with zero writes. It is not
snapshot drift.

## Scope And Evidence Gaps

Render report-level gaps discovered before any subsystem owns them: unresolved
scope, missing governing authority or declared-scope evidence, and their
coverage impact and re-entry requirements. Keep these separate from codebase
findings and artifact-verification failures.

## Linked System Map

Use the map as the table of contents. Give every system
`<section id="system-<system-id>">` and every subsystem
`<section id="subsystem-<subsystem-id>">`. Link each nested map node to its
section and display `mapped`, `incomplete`, or `audited`.

Keep a map node to ID, name, one-sentence purpose, state, file count, direct
evidence-backed dependencies, and its valid pickup. Put entry points,
Interfaces, owned paths, callers, dependents, flows, domain terms, Proof
Seams, and relationship evidence in the linked detail section.

Add a concise static SVG overview or per-system diagram only when it makes
ownership or dependency flow materially easier to understand. Never require
one diagram to contain the whole repository. Give every diagram a text
alternative.

Instantiate every command with the actual stable ID and current absolute
report path; display no placeholder token:

- incomplete Map: show only Continue;
- stale snapshot: show only Refresh;
- complete Map: show Audit only for `mapped` or `incomplete` subsystems; and
- audited subsystem: show no Audit pickup; an explicitly requested fresh audit
  shows only Refresh.

Never rank subsystems or add a global recommendation.

## File Coverage

Account for every inventoried file under one primary subsystem; shared
infrastructure with one audit-owning subsystem and named consumers; or an
excluded ledger with its reason.

## Subsystem Audit

An audited or incomplete subsystem additionally renders:

- Source Trace and per-lens coverage;
- supported scenarios and checked state or failure branches;
- verified defects in severity order, each at
  `item-defect-<subsystem-id>-<item-id>`;
- opportunities grouped by concept class, each at
  `item-opportunity-<subsystem-id>-<item-id>`;
- retained complexity and Revisit Triggers, each at
  `item-retained-<subsystem-id>-<item-id>`;
- evidence gaps at `item-gap-<subsystem-id>-<item-id>`, disproved items at
  `item-disproved-<subsystem-id>-<item-id>`, and duplicates at
  `item-duplicate-<subsystem-id>-<item-id>`;
- performance measurements when applicable;
- a local candidate index when audited;
- improvement candidate cards plus a subsystem-local recommendation when
  audited; and
- exact remaining coverage, with no candidate-analysis pickup, when
  incomplete.

Use exact lens vocabulary and keep every finding visible when it belongs to a
candidate. The candidate index shows ID, name, strength, state, anchor, and
valid pickup.

## Candidate Cards

Give each candidate a stable
`<article id="candidate-<candidate-id>">`. Render:

- title and `Strong`, `Worth exploring`, or `Speculative` badge;
- primary class and exact concepts;
- files, Modules, and member item links;
- problem, snapshot evidence, and improvement direction;
- expected benefit;
- behavior and safety floors;
- required proof and unresolved decisions;
- candidate state; and
- one state-valid, fully instantiated pickup or `none`.

Use a concise static diagram only when structure or flow materially benefits.
Give every diagram a text alternative. The subsystem-local recommendation
links to one candidate but never changes candidate state.

## Candidate Analysis

Append analysis under the same candidate anchor:

- current shape and cost;
- Keep, Smallest sufficient change, Structural change, and Replacement;
- recommended direction and rejected alternatives;
- affected contracts, decisions, compatibility, migration, cutover, and
  rollback when applicable;
- proof plan and residual risk;
- exactly zero or one suggested next step labeled `user selection required`;
- the complete suggested invocation with skill, candidate ID, absolute report
  path, pickup prerequisite, result recipient, and Audit re-entry when a next
  step exists; and
- candidate state.

Render:

- Analyze only for `presented`;
- the complete decision brief and exact `$grilling` or `$grill-with-docs`
  invocation for `decision pending`;
- the exact evidence re-entry for `blocked`;
- the suggested next-owner invocation for `analyzed` when present, otherwise
  `none`; and
- no pickup for `disproved`.

After returned evidence, preserve its status, intact content or pointer,
changed judgments, Domain Delta when applicable, and foreign mutation evidence
without claiming it as Audit work. A Domain Delta that changes an in-scope
live-baseline path makes the report stale and changes no old-snapshot
judgment.

## Navigation

Provide:

- the map as the system and subsystem table of contents;
- candidate links inside their owning subsystem rather than in the global
  map;
- a “back to map” link from every subsystem;
- a “back to subsystem” link from every candidate;
- visible visited and focus states; and
- no link whose target is missing or duplicated.

## Atomic Publish And Verification

### Finalize Gate

Exclusively create one invocation-owned transient sibling. Render the complete
next report to it, reread and verify it, then immediately verify that the
snapshot identity and Resume Gate source-report SHA-256 are unchanged. For
New, require that the target report did not appear after Pin. Only then
atomically replace `report.html` and remove the sibling. Remove only the
invocation-owned sibling. Preserve the last verified report on interruption,
drift, collision, concurrent report change, or failure.

Verify:

- the snapshot manifest is complete, the report path is excluded from the
  baseline, and current identity matches before any resumed update;
- audit scope, IDs, states, counts, file assignments, edges, items, candidate
  order, analyses, and suggestions are internally consistent;
- every internal link resolves exactly once;
- every advertised system, subsystem, item, candidate, and back-link target
  exists exactly once;
- every file and item has one primary home;
- every candidate belongs to one audited subsystem and retains its member IDs;
- changing one subsystem or candidate preserves all prior completed content in
  meaning and stable identity and, outside affected summaries, byte-for-byte;
- every displayed command uses the current absolute report path;
- every displayed command is valid for the current state and contains no
  placeholder token;
- every non-`none` candidate suggestion has one exact invocation and
  callee-compatible pickup prerequisite; and
- no network dependency, executable script, unsafe interpolated text,
  color-only state, or hidden pending coverage exists.

A failed check is an artifact failure. Return `Invocation outcome:
incomplete`, preserve the last verified report, and do not record the failure
inside the unverified candidate or misclassify it as a codebase gap.
The Return names the observed snapshot status, failed update, preserved report
content identity, and sibling cleanup. Fields inside the preserved report
describe its last verified publication, not the failed attempt.

## Footer

End with audit and candidate-analysis coverage, failed or skipped proof, and:

```text
Invocation outcome: complete | incomplete | blocked
Snapshot status: current | stale
Map status: incomplete | complete
Report: <absolute path> | none
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
