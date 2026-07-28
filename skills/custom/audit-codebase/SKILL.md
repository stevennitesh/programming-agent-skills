---
name: audit-codebase
description: Build, continue, or refresh one durable linked HTML repository atlas; thoroughly audit one user-selected subsystem against current source; or revalidate and analyze one user-selected improvement candidate or returned evidence. Use explicitly from the top-level root for whole-codebase correctness, robustness, quality, and improvement discovery; exclude diffs, implementation, release decisions, and automatic selection.
---

# Audit Codebase

Map before the first judgment. Complete one user objective per invocation:

```text
Map:     observe current repository -> map remaining ownership -> publish
Audit:   refresh one selected subsystem Source Trace -> audit -> publish
Analyze: revalidate one selected candidate -> analyze or disprove -> publish
```

Audit may perform the selected objective's prerequisite source refresh in the
same invocation. It never selects a subsystem or candidate and starts no
downstream work.

**Root-owned:** the top-level root owns scope, selection admission, lens
coverage, findings, candidates, publication, and Return. It may use up to six
fresh-context read-only delegates for repository inventory or independent
Source Trace inspection when concurrency is useful. Delegates use
`fork_turns="none"`, mutate nothing, and return evidence; root repeats decisive
checks before admitting a judgment. A delegated invocation of this skill
returns a root-only blocker.

**Artifact boundary:** the only lasting mutation is
`.scratch/audit-codebase/<run-id>/report.html`. Invocation-owned fragments and
atomic-write siblings are temporary and removed before Return. Exclude them
from audited content. Leave product code, ordinary tracked docs, Git refs and
index, trackers, reviews, deployments, and external systems unchanged.

## Entry Gate

Choose the requested objective once. Use Map only when no report-backed
selection was supplied. Never replace an invalid or ambiguous Audit or Analyze
selection with Map.

For a supplied report, apply the Entry Gate in
[HTML-REPORT.md](HTML-REPORT.md). Pass only with a contained canonical path,
supported report version, matching repository and run identities, strict UTF-8,
and one uniquely resolved selected ID in an admissible state. Record the report
SHA-256 for publication collision detection.

A failed Entry Gate returns `blocked` with zero writes and the exact invalid
input. Report-wide age or unrelated repository drift is not an Entry failure;
Audit and Analyze establish current truth at the selected unit.

**Current source** means the report's repository target: the exact Git object
for an object-targeted atlas, or the observed live worktree for a live atlas.
Never substitute checkout bytes for a supplied Git object.

## Map

### Observe And Scope

Use one branch:

- **New:** create one run ID and observe the requested repository target.
- **Continue:** reuse an incomplete report, reconcile current path changes, and
  map only missing or affected ownership.
- **Refresh:** when explicitly requested or when structural change makes the
  existing system boundaries unusable, remap current source in the same report
  unless the user requested a new run.

For a supplied commit or tree, read only that Git-addressed target. For a live
repository, record the current commit and tree provenance, generation time, and
one compact digest of the sorted in-scope path, mode, and content identities.
Do not render a per-file hash ledger. Each subsystem records its owned path list
and an evidence fingerprint that later objectives may replace.

Record:

```text
Repository:
Map observation:
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
Missing governing authority is a report-level gap; do not invent policy.

### Map Ownership

Map behavior and ownership, not directories alone. Read repository
instructions, manifests, entry points, routed domain records and ADRs,
implementation, representative callers and tests, build and deployment
configuration, and data or control-flow edges.

Account for every in-scope tracked source, test, configuration, and support file
plus in-scope untracked content under exactly one:

- named subsystem;
- shared infrastructure with one audit-owning subsystem and named consumers; or
- excluded ledger entry with an evidence-backed reason.

Group subsystems into systems. Give each stable IDs, purpose, owned behavior,
entry points, Interfaces, paths, callers, dependencies, dependents, flows,
domain terms, decisions, and Proof Seams. Every dependency edge needs source
evidence. Do not audit or rank a subsystem during Map.

When mapping cannot finish, publish `Map: incomplete` with exact remaining
coverage and one Continue pickup. Expose subsystem pickups only after every file
is accounted for and `Map: complete`.

### Publish Map

Apply the Map Publish Gate in `HTML-REPORT.md`. Return the absolute report path,
systems, subsystem IDs and names, file coverage, and exactly one pattern:

`$audit-codebase audit <subsystem-id> from <absolute-report-path>`

Then stop for user selection.

## Audit One Subsystem

### Current Evidence Gate

Require a complete map and one uniquely selected `mapped`, `incomplete`, or
explicitly re-audited subsystem. Rebuild its Source Trace from current source:
owned files, consumed shared infrastructure, entry paths, callers, dependents,
tests, configuration, routed domain records, ADRs, and bounded history when
compatibility or staleness matters. Discover current callers and paths rather
than trusting the old fingerprint.

Record the current evidence identity and update affected local map ownership.
If structural change makes the selected boundary unresolvable, publish the
reconciled map as incomplete and return its exact Map continuation instead of
auditing a guessed subsystem.

### Mandatory Lens Gate

Always read:

- [RELIABILITY-LENS.md](RELIABILITY-LENS.md) for Semantic Correctness,
  Robustness, supported state and failure branches, and Proof Seams;
- [QUALITY-LENS.md](QUALITY-LENS.md) for the mandatory six-class coverage
  ledger, class ownership, opportunities, and retained complexity; and
- [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md) for defects and evidence gaps.

Apply every required lens class and record one evidenced disposition. A class
is never skipped silently.

Load a detailed owner when the Source Trace implicates it, an observation may
belong to it, exact vocabulary affects judgment, or `not applicable` is not
obvious:

- [DOMAIN-LENS.md](DOMAIN-LENS.md)
- [DESIGN-LENS.md](DESIGN-LENS.md)
- [SIMPLIFICATION-LENS.md](SIMPLIFICATION-LENS.md)
- [CODING-PRACTICES-LENS.md](CODING-PRACTICES-LENS.md)
- [PERFORMANCE-LENS.md](PERFORMANCE-LENS.md) when performance or resource
  behavior is declared, observed, or claimed

Apply additional lenses only from their authoritative project, domain,
methodology, data, validation, or comparison sources. Generic smells and
thresholds are discovery hints, never findings.

Before an evidence command, establish its filesystem and external effects.
Redirect disposable outputs to an invocation-owned temporary boundary, verify
scoped state afterward, and record a gap when read-only containment cannot be
proved.

Admit defects and gaps under `DEFECT-CONTRACT.md`; opportunities and retained
complexity under `QUALITY-LENS.md`. Read
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) only when grouping admitted
items into user-selectable candidates. Keep every member finding visible.

Rank candidates only inside this subsystem by verified impact, applicable
Leverage or Locality, confidence, and proof burden. Use `Strong`, `Worth
exploring`, or `Speculative` with an evidence-backed reason. A local
recommendation is advisory and selects nothing.

If any required file, lens disposition, or supported branch remains unchecked
although obtainable, mark the subsystem `incomplete`. Unavailable evidence is a
gap; unfinished obtainable work is not.

### Publish Audit

Apply the Incremental Publish Gate to the selected subsystem and affected
summaries. For `audited`, return findings, retained complexity, gaps, candidate
IDs and names, the local recommendation, coverage, and:

`$audit-codebase analyze <candidate-id> from <absolute-report-path>`

For `incomplete`, return exact remaining coverage and the same subsystem Audit
pickup. Then stop.

## Analyze One Candidate

### Current Evidence Gate

Require one candidate inside an audited subsystem. Read
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md), then treat the recorded card as
a hypothesis rather than proof. Reinspect current implicated files, callers,
contracts, decisions, tests, member findings, and Proof Seams; expand the Source
Trace when current evidence reveals another causal owner. Load only implicated
detailed lens owners.

When revalidation adds, removes, or reclassifies a member finding, reload
`DEFECT-CONTRACT.md` or `QUALITY-LENS.md` as applicable and repeat its admission
gate before changing the candidate.

Classify current validity:

- `confirmed`: evidence and improvement direction still hold;
- `changed`: revise the evidence, members, or direction and continue only while
  the candidate remains one coherent improvement;
- `disproved`: publish the resolving evidence and stop;
- `blocked`: publish the exact missing evidence or decision and re-entry.

Unrelated repository changes do not block. If current structural change
destroys the candidate's subsystem boundary or makes its identity ambiguous,
stop with the exact Map or Audit selection needed.

### Analyze Thoroughly

Apply the complete comparison and proof contract in `CANDIDATE-CONTRACT.md`.
For a design or mixed candidate after current-user decisions settle, load
`$codebase-design` Direct Design as a discipline and fold its material
Responsibilities, Interfaces, Seams, Proof Seams, migration, and safe gaps
into this candidate. Create no second design artifact.

Read [CANDIDATE-FOLLOWUP.md](CANDIDATE-FOLLOWUP.md) only when a material user
decision, returned evidence, or justified next-owner suggestion exists. Suggest
zero or one next owner labeled `user selection required`; invoke nothing.

### Publish Analysis

Apply the Incremental Publish Gate to the candidate and affected summaries.
Return the current validity judgment, complete analysis or disproval, evidence
limits, and zero or one uninvoked next-owner suggestion. Then stop.

## Publication And Return

Follow [HTML-REPORT.md](HTML-REPORT.md). A failed Map publication preserves the
last verified report and returns `incomplete`. Apply its one-attempt
Incremental Publish Gate after a passed Entry Gate. Failure does not erase
completed source analysis: return immediately with the analysis, `Report
update: failed`, the failed update, and the preserved report identity. Leave
the report unchanged.

State is local:

```text
Map: none | incomplete | complete
Subsystem: none | mapped | incomplete | audited
Candidate: none | presented | decision pending | analyzed | disproved | blocked
Evidence freshness: map, subsystem, and candidate each record last verified identity
```

Every Return includes:

```text
Outcome: complete | incomplete | blocked
Selected item:
Result or state:
Evidence limits:
Report update: updated | unchanged | failed
Report: <absolute-path> | none
Next user selection: <exact action> | none
```

Also state once: `Release decision: none; product mutation authority: none;
downstream execution: none; next selection authority: user.`

Complete only when the selected objective's current Source Trace, mandatory
coverage, obtainable proof, report update result, and next user selection are
explicit. A complete audit may contain severe defects, presented candidates,
retained complexity, and evidence gaps; coverage is not a release decision.
