---
name: audit-codebase
description: Audit one immutable repository baseline read-only against a bounded caller-defined correctness, methodology, model-risk, data-leakage, validation, calibration, metric, analytics, or performance Charter. Return verified defects, optional advisories, evidence gaps, coverage, and complete or incomplete status without a release decision, ranking, routing, or mutation. Use explicitly from the top-level root agent when the target is repository behavior rather than a pending diff.
---

# Audit Codebase

**Pin -> Charter -> Trace -> Examine -> Verify -> Return**

Own one bounded repository-baseline audit. A complete audit may contain severe defects; status describes coverage, never acceptance.

**Root-only guard:** the top-level root is the sole lens dispatcher, evidence-ledger owner, verifier, and reporter. If invoked inside a delegated task, stop before Pin and return `incomplete` with a routing blocker. Lens agents never spawn, edit, or mutate external state.

**Boundary:** inspect one immutable snapshot only. Leave product files, tracked docs, the index, commits, trackers, PR reviews, deployments, and external messages unchanged. Use `.tmp/audit-codebase/<run-id>/` only for disposable captured evidence and name anything preserved.

Route instead of auditing when the actual target is:

- a pending ordinary diff -> `$review`;
- a PR, release candidate, or high-risk diff needing a release decision -> `$convergent-pr-review`;
- uncertainty about which structural improvement to make -> `$improve-codebase`;
- one uncertain symptom or cause -> `$diagnosing-bugs`;
- one interface or ownership design -> `$codebase-design`.

## Pin

Record a run ID and one complete immutable target:

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
Expected contracts or methodology:
Supported scenarios and environments:
Required evidence and proof:
Non-goals:
Advisories: yes | no
```

Require at least one bounded region, required lens, and authoritative expected contract or methodology source. A request for “everything” must still be partitioned into named finite regions and lenses. Missing or conflicting authority makes only the affected lens incomplete; do not invent a methodology.

## Trace

Build one Source Trace from the request, repo instructions and routed docs, domain decisions and ADRs, authoritative methodology or model-risk sources supplied by the caller, current implementation, representative callers and tests, data lineage, validation configuration, and operational constraints.

Map each required lens to its expected contract, code and data paths, supported scenarios, observable evidence seam, and unavailable evidence. Keep release readiness and change attribution out of the audit; they belong to diff review.

Read [DEFECT-CONTRACT.md](DEFECT-CONTRACT.md). When advisories are enabled, also read [ADVISORY-CONTRACT.md](../review/ADVISORY-CONTRACT.md).

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

Reconcile active capacity and retry once before degrading. When fresh lenses are unavailable, run separated root passes with an explicit lens reset and report reduced confidence. Independence strengthens confidence but does not replace coverage. If any required lens remains uncovered, the audit is `incomplete`.

Normalize defects into one ledger. Preserve cross-domain links without collapsing distinct expected contracts. Challenge a disputed defect only with the claim, evidence, contrary evidence, and exact decision needed. Evidence decides; agreement is signal.

Keep advisories in a separate ledger. A violated expected contract is a defect even when nonblocking. Unsupported speculation is omitted.

## Verify

The root verifies every reported defect and advisory against the immutable snapshot and its contract. Each defect reaches `verified`, `disproved`, or `not checked`; preserve `not checked` only with the missing evidence, affected lens, and confidence impact. No candidate or unverified item survives.

Run the drift check against the captured target. Any target change makes the audit stale and `incomplete`; the caller alone authorizes a new snapshot.

Delete disposable artifacts or record each intentionally preserved path.

## Return

Return exactly one status:

- `complete`: every required region and lens was covered and every survivor reached a terminal evidence state;
- `incomplete`: the target, Charter authority, required lens, required evidence, verification, or drift gate did not close.

Begin with:

```text
Audit status: complete | incomplete
Snapshot:
Run ID:
Charter:
Source Trace:
Lens coverage:
Confidence: full | reduced
```

Then return:

```md
## Verified Defects
## Disproved Or Duplicate
## Evidence Gaps
## Advisories
```

Render the Advisories section only when enabled. Severe verified defects do not change `complete` to a release `blocked` decision; this skill issues no release decision. End with:

```text
Release decision: none
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Complete only when the immutable snapshot and bounded Charter are recorded; every required lens is covered or named as a blocker; defects and enabled advisories pass their separate contracts; evidence gaps and confidence are explicit; drift and the read-only boundary are checked; and one coverage status returns control.
