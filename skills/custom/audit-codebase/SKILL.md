---
name: audit-codebase
description: Build, continue, or refresh one durable linked HTML map of an immutable repository; audit exactly one user-selected subsystem; or analyze exactly one user-selected improvement candidate or returned evidence. Use explicitly from the top-level root for whole-codebase correctness, robustness, quality, and improvement discovery; exclude diffs, implementation, release decisions, and automatic selection.
---

# Audit Codebase

Map before judging. Run exactly one path per invocation:

```text
Map:     Pin or verify snapshot -> Map remaining repository -> Publish
Audit:   Verify completed map and user selection -> Audit one subsystem -> Publish
Analyze: Verify candidate or returned evidence -> Analyze one candidate -> Publish
```

A new or refreshed run maps and stops. An incomplete map continues from the
same report. After mapping completes, the user selects one subsystem and may
later select one candidate. Audit never selects either and starts no
downstream work.

**Root-owned:** the top-level root owns the immutable snapshot, report, audit,
candidate analysis, and Return. A delegated invocation returns a root-only
blocker before Pin or mutation. Do not delegate, fan out, implement, mutate
the product, or issue a release decision.

**Artifact boundary:** the sole durable artifact and only lasting worktree
mutation is `.scratch/audit-codebase/<run-id>/report.html`. Its transient
atomic-write sibling must be removed before Return. Exclude both paths from
the audited content and drift calculation. Leave product code, ordinary
tracked docs, Git refs and index, trackers, reviews, deployments, and external
systems unchanged.

Before using a supplied report, apply the Resume Gate in
[HTML-REPORT.md](HTML-REPORT.md). Before every report replacement, apply its
Finalize Gate. Every Return reports the gate result. A failed gate preserves
the last verified report and returns the exact observed state without
continuing another path.

Resolve the requested path once. Use Map when no report and no path-local
selection were supplied. Never replace an explicit invalid, ambiguous, or
stale Audit or Analyze request with Map; return `blocked` without changing the
report and expose only state-valid report pickups.

## Map

### 1. Pin Scope

Choose one branch:

- **New:** no report was supplied. Create one run ID and pin one target.
- **Continue:** the supplied report has `Snapshot: current`, `Map:
  incomplete`, and a complete manifest. Reuse its run and map only uncovered
  content.
- **Refresh:** the user explicitly supplied a stale report or requested a
  semantic rebuild or fresh audit of a current report. Create a new run and
  map the current target from scratch. Carry no map, finding, candidate, or
  analysis state into the new snapshot.

Pin the target as:

- supplied commit or tree: retain the resolved object IDs and read in-scope
  content only from those objects;
- branch baseline: resolve its commit and tree once; or
- live worktree baseline: retain the resolved `HEAD` tree as provenance plus
  the deterministic working-tree overlay defined by `HTML-REPORT.md`.

Exclude the report and its transient sibling. Store the complete logical
manifest in the HTML so later invocations can verify audited bytes without
another ledger. Capture each live byte identity from the same read used as
evidence. Staging or unstaging unchanged bytes is not drift.

Record:

```text
Repository:
Snapshot:
Regions: whole repository
Required lenses: correctness, robustness, domain, design, simplification, coding practices
Additional lenses:
Expected contracts and invariants:
Supported scenarios:
Workloads and environments:
Performance budgets or comparison baselines:
Required evidence and proof:
Non-goals:
```

The six required classes apply unless the user explicitly excludes one.
Missing governing authority becomes a report-level gap; do not invent policy.
An empty, unresolved, or incompletely captured target returns `blocked` with
`Report: none` when no verified report exists. Never emit Continue without a
complete manifest. A live worktree continues only while every captured content
identity matches.

### 2. Map Repository

Map behavior and ownership, not directories alone. Read repository
instructions, manifests, entry points, routed domain records and ADRs,
implementation, representative callers and tests, build and deployment
configuration, and data or control-flow edges.

Inventory every in-scope tracked source, test, configuration, and support file
plus in-scope untracked content. Give each file exactly one primary home:

- one named subsystem;
- shared infrastructure with one audit-owning subsystem and named consumers;
  or
- excluded, with an evidence-backed reason such as generated, vendored, or
  build output.

Group subsystems into systems. Assign stable IDs and record purpose, owned
behavior, entry points, interfaces, paths, callers, dependencies, dependents,
flows, domain terms, decisions, and proof seams. Every dependency edge needs
source evidence. Account for every file before declaring the map complete. Do
not audit or rank a subsystem during Map.

When coverage cannot finish, publish `Map: incomplete` and return one Continue
pickup. Do not expose subsystem-audit pickups until every file is accounted
for and the Map is `complete`.

### 3. Publish And Stop

Follow [HTML-REPORT.md](HTML-REPORT.md). A failed report gate preserves the
last verified report and returns `Invocation outcome: incomplete`.

For a complete map, return the absolute report path, systems, subsystem IDs
and names, file coverage, and this one selection pattern:

`$audit-codebase audit <subsystem-id> from <absolute-report-path>`

The report contains every fully instantiated subsystem pickup.

For an incomplete map, return:

`$audit-codebase continue the map from <absolute-report-path>`

For a stale report that has not been refreshed, return:

`$audit-codebase refresh the map from <absolute-report-path>`

Then stop.

## Audit One Subsystem

### 1. Verify Selection

Require the supplied absolute report path, `Snapshot: current`, `Map:
complete`, and one uniquely resolved user-selected `mapped` or `incomplete`
subsystem. Drift marks the report stale and returns only the Map Refresh
pickup. An invalid or ambiguous selection returns `blocked` without changing
the report. An audited subsystem is a complete no-op unless the user requests
a fresh audit; a fresh audit uses Map Refresh and a new run.

### 2. Load Audit Concepts And Audit

Read each owner below completely:

- **Semantic Correctness**, **Root Cause**, and **Proof Seam** test observable
  meaning. **Robustness**, **Trust Boundary**, **Failure Atomicity**,
  **Recovery**, **Idempotency**, **Concurrency**, **State Lifecycle**,
  **Compatibility**, **Environmental Variation**, and **Observability** test
  supported edge, failure, security, operational, and environmental paths.
  Read [RELIABILITY-LENS.md](RELIABILITY-LENS.md).
- **Ubiquitous Language**, **Language Collision**, **Bounded Context**,
  **Invariant**, **Context Relationship**, **Implementation Contradiction**,
  and **ADR Conflict** test domain meaning and ownership. Read
  [DOMAIN-LENS.md](DOMAIN-LENS.md).
- **Module**, **Interface**, **Implementation**, **Depth**, **Deep Module**,
  **Shallow Module**, **Seam**, **Adapter**, **Leverage**, and **Locality**
  expose shallow indirection and misplaced ownership. Read
  [DESIGN-LENS.md](DESIGN-LENS.md).
- **YAGNI**, **KISS**, **DRY**, **Readability First**, **Repository Reuse**,
  **Standard Library**, **Native Platform**, **Installed Dependency**,
  **Collapse**, **Known Ceiling**, and **Revisit Trigger** seek the first
  sufficient behavior-preserving reduction. Read
  [SIMPLIFICATION-LENS.md](SIMPLIFICATION-LENS.md).
- **Descriptive Naming**, **Type Safety**, **Immutability Default**,
  **Explicit Error Handling**, **Input Validation**, **Clear Control Flow**,
  **Why Comments**, **Behavior Tests**, and **Focused Concurrency** test
  whether implementation makes its contract easy to read and prove. Read
  [CODING-PRACTICES-LENS.md](CODING-PRACTICES-LENS.md).

Read [QUALITY-LENS.md](QUALITY-LENS.md) for class tie-breakers, opportunity
admission, and retained complexity; [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md)
for defects and gaps; and
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) for candidate grouping. Generic
smells and thresholds are discovery hints, never findings.

Build the subsystem Source Trace from owned files, consumed shared
infrastructure, entry paths, callers, dependents, tests, configuration, domain
records, ADRs, and bounded history when staleness or compatibility matters.
Apply every loaded concept owner and record per-lens coverage. Read
[PERFORMANCE-LENS.md](PERFORMANCE-LENS.md) only when performance or resource
behavior is in scope. Apply additional lenses only from their authoritative
project, domain, methodology, data, validation, or comparison sources.

Before running any evidence command, establish its filesystem and external
effects. Redirect disposable outputs to an invocation-owned temporary
boundary, verify scoped state afterward, and record a gap instead when
read-only containment cannot be proved.

Verify defects and gaps under `DEFECT-CONTRACT.md`. Admit opportunities and
retained complexity under `QUALITY-LENS.md`. Convert each cohesive,
user-selectable improvement into a candidate under `CANDIDATE-CONTRACT.md`;
keep its member findings visible.

Rank candidates only inside this subsystem by verified impact, applicable
Leverage or Locality, confidence, and proof burden. Use `Strong`, `Worth
exploring`, or `Speculative` and explain the strength. A subsystem-local
recommendation is advisory and never selects a candidate.

If any required file, lens, or supported branch remains unchecked although it
is obtainable within Audit authority, mark the subsystem `incomplete`.
Preserve observations but expose no candidate-analysis pickup until the
subsystem is `audited`. An evidence gap records unavailable evidence; it does
not hide unfinished audit work.

### 3. Publish And Stop

Update only the selected subsystem and report-level coverage. Preserve every
other completed section exactly as required by `HTML-REPORT.md`, then verify
the complete report.

For an audited subsystem, return its defects, opportunities, retained
complexity, gaps, ranked candidate IDs and names, local recommendation,
remaining coverage, and this one selection pattern:

`$audit-codebase analyze <candidate-id> from <absolute-report-path>`

The report contains every fully instantiated candidate pickup.

For an incomplete subsystem, return its exact remaining coverage and:

`$audit-codebase audit <subsystem-id> from <absolute-report-path>`

Preserve other valid subsystem pickups. Then stop.

## Analyze One Candidate

### 1. Verify Selection

Require the absolute report path, current snapshot, complete map, audited
subsystem, and one unambiguous user-selected candidate.

Read [CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) completely. Load only the
lens owners implicated by the candidate's recorded classes. Load
`DEFECT-CONTRACT.md` or `QUALITY-LENS.md` only when returned evidence reopens
finding admission.

- Analyze `presented`.
- Resume `decision pending` only with the intact returned decision packet.
- Resume `blocked` only with its exact re-entry evidence.
- Reanalyze `analyzed` only when the user explicitly supplies new evidence.
- Reject stale reports and ambiguous or disproved candidates unconditionally.

### 2. Analyze

Trace the candidate's behavior, callers, dependencies, decisions, member
findings, alternatives, proof seams, change surface, and conflicts under
`CANDIDATE-CONTRACT.md`. It owns comparison, confirmation, decision briefs,
returned-evidence judgment, candidate transitions, and exactly zero or one
next-owner suggestion. Invoke nothing.

### 3. Publish And Stop

Update only the selected candidate and affected coverage summaries. Preserve
other completed sections exactly as required by `HTML-REPORT.md`, verify the
complete report, and return the analysis plus exactly zero or one next-owner
suggestion labeled `user selection required`. Start nothing downstream.

## State And Completion

```text
Invocation outcome: complete | incomplete | blocked
Snapshot: none | current | stale
Map: none | incomplete | complete
Subsystem: none | mapped | incomplete | audited
Candidate: none | presented | decision pending | analyzed | disproved | blocked
```

Selection is invocation-local, not persistent state. Evidence gaps are
findings, not candidate states. `incomplete` is resumable and never equals
`audited`. Audit coverage completes only when every mapped subsystem is
`audited`. Candidate analysis is optional. A complete audit may contain severe
defects, presented candidates, retained complexity, and evidence gaps.
`blocked` means the requested path cannot proceed safely without a named
authority or state change; it never selects another path implicitly.

Every Return includes:

```text
Invocation outcome:
Snapshot status:
Map status:
Run ID: <id> | none
Report: <absolute-path> | none
Current subsystem:
Current candidate:
Audit coverage:
Candidate-analysis coverage:
Selection required: subsystem | candidate | decision workflow | next step | none
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
