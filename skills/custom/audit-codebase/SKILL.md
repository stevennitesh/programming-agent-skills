---
name: audit-codebase
description: Build or refresh one durable linked HTML repository atlas, thoroughly audit one user-selected subsystem against current source, or revalidate and analyze one user-selected improvement candidate. Use explicitly from the top-level root for whole-codebase correctness, robustness, quality, and improvement discovery; exclude diffs, implementation, release decisions, and automatic selection.
---

# Audit Codebase

Complete one user-selected objective:

```text
Map     observe the repository -> map ownership and flows -> publish
Audit   refresh one subsystem Source Trace -> audit -> publish
Analyze revalidate one candidate -> compare and prove -> publish
```

Map precedes judgment. Audit may refresh its selected boundary; Analyze may
refresh its candidate evidence. Never choose the next subsystem or candidate.

**Authority:** the top-level root owns admission, scope, lens dispositions,
findings, candidates, publication, and Return. Optional read-only delegates use
`fork_turns="none"` to gather evidence; root repeats decisive checks.
A delegated invocation of this skill returns a root-only blocker.

**Mutation boundary:** only
`.scratch/audit-codebase/<run-id>/report.html` may persist. Fragment and
manifest files are invocation-owned and removed by the caller. Leave product
code, tracked docs, Git state, trackers, reviews, deployments, and external
systems unchanged.

## Admission

Choose the objective once:

- **Map:** no supplied report-backed selection; observe a new, continued, or
  explicitly refreshed repository atlas.
- **Audit:** exactly one supplied subsystem ID.
- **Analyze:** exactly one supplied candidate ID.

An invalid Audit or Analyze request never falls back to Map.

For an existing report, run helper `inspect` with the exact objective and ID.
Proceed only when [HTML-REPORT.md](HTML-REPORT.md) proves a contained canonical
path, structural version, repository/run identity, selection state, and required
regions. Record its report SHA-256. A failed Admission returns `blocked` with
zero writes. Report age and unrelated repository drift are handled by current
evidence, not Admission.

**Current source** is the requested Git object or the observed live worktree.
Never substitute checkout bytes for an object-targeted atlas.

## Map

### Observe

Use New for no report, Continue for an incomplete report, and Refresh only when
requested or current structure invalidates existing boundaries. Record the
repository target, observation identity and time, scope, required and additional
lenses, governing contracts, supported scenarios, workloads, environments,
proof expectations, and non-goals. Missing authority is a gap; invent none.

Read repository instructions, manifests, entry points, routed domain records
and ADRs, implementation, representative callers and tests, build/deployment
configuration, and data/control-flow edges.

### Map ownership

Account for each in-scope source, test, configuration, and support file under
exactly one:

- subsystem;
- shared infrastructure with one audit owner and named consumers; or
- excluded ledger entry with an evidenced reason.

Group subsystems into systems. Give each stable IDs, purpose, owned behavior,
entry points, Interfaces, paths, callers, dependencies, dependents, flows,
domain terms, decisions, and Proof Seams. Evidence every direct dependency.
Render one repository relationship figure and one current-state flow per
subsystem as specified in `HTML-REPORT.md`; diagrams are views of these facts,
not another analysis stage. Do not audit or rank during Map.

Publish `Map: incomplete` with remaining coverage and one Continue pickup, or
`Map: complete` with file coverage and exactly one user-selectable Audit pickup.
Then stop.

## Audit One Subsystem

**Hot path:** inspect -> rebuild Source Trace -> apply six classes -> admit
observations -> group candidates -> render one manifest -> validate -> publish
once -> inspect.

### Current evidence

Require a complete Map and one selected `mapped` or `incomplete` subsystem
(or an explicitly requested re-audit). Rebuild its Source Trace from current:
owned files, consumed shared infrastructure, entry paths, callers, dependents,
tests, configuration, routed domain records, ADRs, and bounded history when
compatibility or staleness matters. Discover callers and paths; do not trust an
old fingerprint.

Record a current evidence identity before judgment and verify it again before
publication. Helper `source-identity` standardizes an already-discovered path
set; it does not discover scope. Refresh affected local ownership and the
selected subsystem flow. If the boundary is no longer resolvable, publish a
reconciled incomplete Map and return its continuation.

### Audit thoroughly

Always read:

- [RELIABILITY-LENS.md](RELIABILITY-LENS.md) for correctness, robustness,
  supported branches, and Proof Seams;
- [QUALITY-LENS.md](QUALITY-LENS.md) for the six required class dispositions,
  opportunities, and retained complexity; and
- [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md) for defect and gap admission.

Every six-class disposition is explicit and evidenced. Load a detailed owner
when its class is implicated, an observation may belong to it, its vocabulary
affects judgment, or `not applicable` is not obvious. The Quality lens owns the
exact detailed-owner routing.

Apply additional lenses only from authoritative project, domain, methodology,
data, validation, or comparison sources. Smells and generic thresholds are
discovery hints, never findings. Before evidence commands, contain side effects
inside an invocation-owned temporary boundary and verify scoped state afterward.

Admit defects/gaps under `DEFECT-CONTRACT.md` and opportunities/retained
complexity under `QUALITY-LENS.md`. Read
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) only when grouping admitted
items. Preserve every member finding. Rank candidates only within the subsystem
by verified impact, applicable Leverage or Locality, confidence, and proof
burden as `Strong`, `Worth exploring`, or `Speculative`.

If obtainable required evidence or a lens disposition remains unchecked, the
subsystem is `incomplete`. Unavailable evidence is a gap; unfinished work is
not.

### Publish Audit

Use one `reaudit-subsystem` manifest. It atomically refreshes the narrative,
upserts findings/candidates, derives progress, and synchronizes state across the
subsystem and Map projections. Include an optional `map` fragment only for
structural changes to nodes, labels, file counts, or edges; state-only changes
need none.

Return audited observations, candidates, local recommendation, coverage, and
one Analyze pickup, or exact incomplete coverage and the same Audit pickup.
Then stop.

## Analyze One Candidate

Require one candidate in an audited subsystem. Read
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md), treat the card as a hypothesis,
and reinspect current implicated files, callers, contracts, decisions, tests,
member findings, and Proof Seams. Expand only when contradiction reveals
another causal owner. Load only implicated detailed lens owners.

Re-admit changed members under their owning contract. Classify:

- `confirmed`: evidence and direction still hold;
- `changed`: revise evidence/members/direction while it remains one coherent
  improvement;
- `disproved`: publish resolving evidence and stop;
- `blocked`: publish the exact missing evidence or decision and re-entry.

Apply the complete comparison and proof method in `CANDIDATE-CONTRACT.md`.
For design or mixed candidates after user decisions settle, apply
`$codebase-design` Direct Design within the card; create no second artifact.
Read [CANDIDATE-FOLLOWUP.md](CANDIDATE-FOLLOWUP.md) only for a material user
decision, returned evidence, or justified next-owner suggestion. Suggest at
most one uninvoked next owner labeled `user selection required`.

For a matching returned implementation packet, use the candidate contract's
close gate and reconcile member findings while preserving original evidence.
Generic report update may not enter `implemented`; only `close-candidate` may.

Validate candidate fragments, publish the identical digest-locked bundle once,
then return validity, comparison, proof, limits, and any uninvoked suggestion.

## Publication And Return

Follow `HTML-REPORT.md`. Zero-write validation is preparation. After it passes,
make exactly one publication attempt. If publication fails, do not hand-edit,
retry, switch mechanisms, or delay Return. Preserve completed analysis and
report the helper's actual effect: before replacement the report is unchanged;
after replacement its state may be unknown until a later invocation inspects it.

Every Return includes:

```text
Outcome: complete | partial | blocked
Publication: updated | unchanged | failed | not-attempted
Selected item:
Result or state:
Evidence limits:
Report: <absolute-path> | none
Next user selection: <exact action> | none
Release decision: none; product mutation authority: none
Downstream execution: none; next selection authority: user
```

`complete` requires the selected objective and durable publication. `partial`
preserves completed analysis that could not be published or exact unfinished
coverage. `blocked` means the objective could not proceed. Findings and gaps do
not themselves make a thorough audit incomplete.
