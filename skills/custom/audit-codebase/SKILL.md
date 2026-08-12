---
name: audit-codebase
description: Build a repository atlas, audit one selected subsystem, analyze one selected improvement candidate, or close one analyzed candidate from its exact verified implementation-completion packet. Use explicitly for repository-baseline improvement discovery; exclude diffs, product implementation, release decisions, and automatic selection.
---

# Audit Codebase

Complete exactly one user-selected objective:

```text
Map                         Audit(subsystem)
  observe and account         refresh current Source Trace
  render atlas                apply six-class coverage

Analyze(candidate)          Close(candidate, completion)
  revalidate and compare      verify implementation result
  publish next boundary       reconcile candidate and findings
```

Map precedes judgment. Never choose the next subsystem or candidate.

## Authority

The top-level root owns scope, admission, lens coverage, findings, candidates,
tracker-publication admission, report publication, and Return. Optional
read-only delegates use `fork_turns="none"` to gather evidence in fresh context;
root repeats decisive checks. A delegated invocation of this skill returns a
root-only blocker.

The only durable Audit-owned artifact is
`.scratch/audit-codebase/<run-id>/report.html`. Use only
[REPORT-QUICK-REFERENCE.md](REPORT-QUICK-REFERENCE.md)'s helper interface;
[HTML-REPORT.md](HTML-REPORT.md) owns report state and rendering. Leave product
source, tracked docs, Git state, reviews, and deployments unchanged. Audit
itself mutates no foreign system; only an exact helper-generated To Tickets
invocation may let that callee mutate its configured tracker. Remove
invocation-owned temporary JSON and path lists only after final read-back or a
proven zero-effect failure.

[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) owns candidate judgment and
Close. Analyze may invoke To Tickets only through the helper-generated pickup;
it never implements.

## Resolve And Admit

Choose once:

- **Map:** no selected subsystem or candidate; create a new atlas or update a
  supplied map-only atlas with its current digest. A history-bearing atlas that
  needs structural remapping requires a new explicitly selected report.
- **Audit:** exactly one subsystem ID from a complete Map.
- **Analyze:** exactly one candidate ID inside an audited subsystem.
- **Close:** exactly one analyzed candidate ID plus its exact implementation
  completion packet using the route derived from current tracker state.

An invalid selection never falls back to Map. Inspect an existing report for
the exact objective and ID. Proceed only when the helper returns the selected
record and admits its report path, structural and state versions,
repository/run identity, canonical rendering, digest, and current state. A
failed admission makes zero writes.

An unsupported structural or state version remains immutable historical
evidence. Return `blocked` with an exact user-selected Map invocation targeting
a new report; never migrate or overwrite it in place.

**Current source** is the observed live worktree bound by helper-derived path
and content identities.

## Map

### Observe

Create a report when none exists. Update a supplied map-only report with its
current digest. Run `inventory` first and use its
tracked-live-worktree identity and paths as the boundary. Record target,
observation time, scope, governing contracts, supported scenarios, workloads,
environments, proof expectations, non-goals, and missing authority.

Read repository instructions, manifests, entry points, routed domain records
and ADRs, implementation, representative callers and tests, build/deployment
configuration, and data/control-flow edges.

### Account

Assign every tracked source, test, configuration, and support path exactly once
to one subsystem, to shared infrastructure represented by one owner and named
consumers, or to an evidenced exclusion. Group subsystems into systems. For
each subsystem record one stable ID, purpose, owned behavior, entry points,
interfaces, owned paths, callers, directed dependencies with evidence, flows,
domain terms, decisions, and Proof Seams.

The helper rejects incomplete complete-Map coverage, overlapping or duplicate
ownership, owned/excluded overlap, unknown or self dependencies, and dependency
edges without evidence. Do not audit or rank during Map. Name relevant untracked
files as an evidence limit.

Publish once. Return incomplete coverage and an exact Map re-entry, or complete
coverage and ask the user to select any mapped subsystem. Stop.

## Audit One Subsystem

Require a complete Map and one selected `mapped`, `incomplete`, or explicitly
re-audited subsystem.

Rebuild its Source Trace from current owned files, consumed shared
infrastructure, entry paths, callers, dependents, tests, configuration, routed
domain records, ADRs, and bounded history when current compatibility or
staleness depends on it. Discover the path set before using `source-identity`.

Always load [RELIABILITY-LENS.md](RELIABILITY-LENS.md),
[QUALITY-LENS.md](QUALITY-LENS.md), and
[DEFECT-CONTRACT.md](DEFECT-CONTRACT.md). Quality owns the six-class coverage
ledger and every detailed-lens trigger. Record applicability, coverage,
examined evidence, admitted IDs, detailed-owner use, and reason for Reliability,
Domain, Design, Simplification, Coding Practice, and Performance. Apply
Quality's coverage-completion rule; unavailable required evidence is a gap.

Admit defects and gaps under the Finding contract; admit opportunities and
retained complexity under Quality. Smells and generic thresholds are discovery
hints only. Read [CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) only when an
admitted defect or opportunity needs grouping. Preserve every member and rank
candidates only inside the selected subsystem by verified impact, observed
cost under Quality, confidence, and proof burden.

Recheck current source identity, publish once, return observations, coverage,
and evidence limits, then ask the user to select any candidate. Stop.

## Analyze One Candidate

Require one selected candidate in an audited subsystem. Apply
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md): reinspect its implicated current
source, callers, contracts, decisions, tests, findings, and Proof Seams;
re-admit changed members; and classify it `confirmed`, `changed`, `disproved`,
or `blocked`. Expand only when contradiction reveals another causal owner and
load only implicated detailed lenses.

Compare Keep, Smallest sufficient, Structural, and Replacement. Apply the
Candidate contract's design branch when triggered.

Read [CANDIDATE-FOLLOWUP.md](CANDIDATE-FOLLOWUP.md) only when the result needs a
material user decision, returned evidence, one other owner, or implementation
work publication. It owns To Tickets authority, recovery, and pickup behavior.

Publish once. Return validity, comparison, proof, limits, tracker result, and
next user selection. Stop.

## Close One Candidate

Close is a separate user-selected objective, never an implicit continuation.
Require one analyzed candidate and the exact completion packet requested by its
helper-generated Implement pickup or required by an explicitly authorized,
already-landed direct implementation. Apply
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md)'s Close gate. A mismatch changes
nothing.

Publish once through `close-candidate`. Only that command may enter
`implemented`.

## Publish

For the selected objective, use the strict schema and the single
validate/digest/publish transaction in
[REPORT-QUICK-REFERENCE.md](REPORT-QUICK-REFERENCE.md). Make at most one
effectful call. On failure, use the helper's returned state literally; never
retry, hand-edit, switch mechanisms, or delay Return.

## Return

```text
Outcome: complete | partial | blocked
Objective: Map | Audit | Analyze | Close
Publication: updated | unchanged | failed | not-attempted
Tracker publication: ready-graph | reused | recovery | authority-required | not-applicable
Implementation tracker item: <provider-native identity> | none
Selected item:
Result or state:
Evidence limits:
Report: <absolute-path> | none
Next user selection: <exact action> | none
Release decision: none; product mutation authority: none
Downstream implementation: none; next selection authority: user
```

`complete` requires the selected objective and durable HTML publication.
Implementation-ready Analyze also requires a To Tickets result or
`authority-required` when its exact invocation authority is absent. `partial`
preserves completed analysis with tracker recovery or exact unfinished
coverage. `blocked` means the objective could not proceed.
Findings and gaps do not themselves make a thorough Audit incomplete.
