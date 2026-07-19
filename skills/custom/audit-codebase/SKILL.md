---
name: audit-codebase
description: Audit one immutable repository baseline read-only against a bounded caller-defined Charter for correctness, domain robustness, performance, methodology, data, analytics, or other supported behavior. Verify every in-scope finding, advisory, and evidence gap; render one self-contained HTML ledger; attach at most one non-authoritative next-owner suggestion to each item or finding cluster; and return complete or incomplete coverage without a release decision or downstream execution. Use explicitly from the top-level root outside ordinary implementation workflow.
---

# Audit Codebase

**Pin -> Charter -> Trace -> Examine -> Verify -> Synthesize -> Report -> Return**

**Terminal:** produce one verified HTML ledger over one immutable snapshot. `complete` or `incomplete` measures coverage, never acceptance; a complete audit may contain severe defects. Report every verified in-scope item and return control without a release decision or downstream execution.

**Root-owned:** the top-level root owns lens dispatch, the evidence ledger, verification, synthesis, and the report. Delegated invocation stops before Pin with an `incomplete` routing blocker. Lenses are read-only leaves.

**Mutation boundary:** write only disposable evidence and one report under `.tmp/audit-codebase/<run-id>/`. Product files, tracked docs, Git state, trackers, reviews, deployments, and external systems remain unchanged.

## Pin

**Chain of custody.** Record a run ID and one complete immutable target:

- supplied commit or tree: resolve and inspect Git-addressed content;
- branch baseline: capture its commit SHA and tree;
- live worktree baseline: capture `HEAD`, index tree, staged and unstaged diffs, status, and every in-scope untracked path and content.

Hash only live content not already addressed by Git. Return `incomplete` when the target does not resolve, is empty, or cannot be captured completely.

## Charter

Record the caller-defined audit boundary before lens work:

```text
Audit outcome:
Snapshot:
Regions:
Required lenses:
Expected contracts and invariants:
Supported scenarios:
Workloads and environments:
Performance budgets or comparison baselines:
Required evidence and proof:
Non-goals:
Advisories: yes | no
```

Require at least one bounded region, required lens, and authoritative expected contract, invariant, or comparison basis. Partition an explicitly whole-codebase request into named finite regions and lenses. Preserve missing or conflicting authority as an evidence gap that makes only the affected lens incomplete. Ignore observations outside the Charter.

## Trace

Build one Source Trace from the request, repo instructions and routed docs, domain decisions and ADRs, authoritative methodology or model-risk sources supplied by the caller, current implementation, representative callers and tests, data lineage, validation configuration, workloads, and operational constraints.

Map each required lens to its expected contract, code and data paths, supported scenarios, observable evidence seam, and unavailable evidence.

Read [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md) completely. When performance, speed, throughput, latency, memory, resource use, or scalability is in scope, also read [PERFORMANCE-LENS.md](PERFORMANCE-LENS.md) completely. When advisories are enabled, read [ADVISORY-CONTRACT.md](../review/ADVISORY-CONTRACT.md).

## Examine

Dispatch direct fresh-context lenses with `fork_turns="none"` when regions or domains partition cleanly. Give each lens only the immutable snapshot, Charter, Source Trace pointers, assigned region and question, mutation boundary, and output contract. Exclude parent hypotheses and peer results.

```text
status: complete | blocked
domain or lens:
coverage:
defects:
advisories: <when enabled>
evidence gaps:
skipped checks:
blockers:
```

Reconcile active capacity and retry once before degrading. When fresh lenses are unavailable, run separated root passes, reduce confidence, and name the missing independence. Any uncovered required lens makes the audit `incomplete`.

Normalize defects and advisories into separate ledgers. Preserve cross-domain links without collapsing distinct expected contracts. Challenge a disputed defect only with its claim, evidence, contrary evidence, and exact decision needed. Evidence decides; agreement is signal.

## Verify

Verify every reported defect and advisory against the immutable snapshot and its contract. Each defect reaches `verified`, `disproved`, or `not checked`; preserve `not checked` only as an evidence gap with the missing evidence, affected lens, and confidence impact. No candidate or unverified item survives as a finding.

Recheck chain of custody. Target drift makes the audit stale and `incomplete`; the caller alone authorizes a new snapshot.

Delete disposable artifacts that the report does not need or record each intentionally preserved path.

## Synthesize

Assign stable IDs, sort verified defects by severity, and retain every verified in-scope defect, enabled advisory, evidence gap, and disproved or duplicate item.

Apply [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md) once to each item or cohesive cluster. Preserve every member finding.

## Report

Read [HTML-REPORT.md](HTML-REPORT.md) completely, then render one self-contained `.tmp/audit-codebase/<run-id>/report.html`.

Reread the report and, when supported, render or open it. Verify it against the report contract. Any failed check becomes an evidence gap and makes the audit `incomplete`.

## Return

Return exactly one status:

- `complete`: every required region and lens was covered, every survivor reached a terminal evidence state, and the report passed verification;
- `incomplete`: the target, Charter authority, required lens, required evidence, verification, drift, or report gate did not close.

Begin with:

```text
Audit status: complete | incomplete
Snapshot:
Run ID:
Report: <absolute-path>
Charter:
Source Trace:
Lens coverage:
Confidence: full | reduced
```

Summarize counts by severity and item type, then name any suggested owners with `Caller selection required`. End with:

```text
Release decision: none
Return boundary: caller
Mutation authority: none
Downstream execution: none
Successor snapshot authority: none
```

Close only when every Charter cell is covered or explicitly blocked, every surviving item is terminal and reported, chain of custody is intact, and the report verifies.
