---
name: convergent-pr-review
description: "Use for local PR review or high-risk local-diff review that needs independent reviewer subagents and a verified finding ledger: release gates, shared plumbing, migrations, security/permissions, CI/workflow/config, public interfaces, or data contracts. For ordinary fixed-point Standards/Spec review, use review."
---

# Convergent PR Review

Run a read-only **convergence gate** over one pinned **review snapshot**:

**review snapshot -> source trace -> independent reviewers -> evidence ledger -> verified survivors -> drift check -> patch-ready handoff**

Reviewer subagents inspect; the main agent orchestrates and verifies. Consensus is signal, not truth.

**Read-only boundary:** inspection, ref fetches, and routed validation may create only disposable `.tmp/` artifacts. Patches, tracked `.scratch/` evidence, staging, commits, and tracker mutations belong to downstream implementation. Sandbox-crossing or external validation follows normal tool approval and is reported.

Use `$review` instead for ordinary branch, WIP, or `review since X` fixed-point review where Standards and Spec are the main axes.

## Defaults

- Base ref: caller-supplied; otherwise discover the repository default branch and merge base
- Reviewers: `2`
- Max rounds: `2`
- Severity: `P0/P1/P2/P3`

Scale reviewers by coverage:

- `2`: Standards and Spec.
- `3`: Standards, Spec, and the highest-risk changed surface.
- `4-5`: Standards, Spec, plus distinct security, migration, public-contract, CI/release, performance, caching, or data-contract lenses.
- `>5`: explicit user request only.

If no Spec source exists, record `Spec: skipped` and replace that reviewer with the highest-risk uncovered lens.

## 1. Pin The Review Snapshot

Resolve the fixed point and capture the complete review target once.

- **Supplied review tree:** verify it with `git cat-file -e <review-tree>^{tree}` and inspect snapshot content with `git show <review-tree>:<path>`.
- **Branch or PR:** capture status, branch, base SHA, head SHA, merge base, diff stat, full diff, and commit range.
- **Worktree:** capture `HEAD`, status, staged diff, unstaged diff, and every in-scope untracked file.

For a PR number, resolve and read the PR before fetching its head when needed.

Give every reviewer the captured snapshot, not a live diff command.

**Target gate:** stop before dispatch when the fixed point or review tree does not resolve, the target is empty, or the complete snapshot cannot be captured.

Done means the fixed point, review snapshot, status, diff command, captured content, and commit range are recorded.

## 2. Trace Sources And Build The Review Packet

Trace the current request or caller packet, PR body and decision-bearing comments, linked issue or spec, repo `AGENTS.md`, `docs/agents/engineering-contract.md`, and validation configuration. Read every named source in full.

For Standards, include repo rules and [SMELL-BASELINE.md](../review/SMELL-BASELINE.md) when repo standards are thin.

Record every relied-on source under `Source Trace`. Record missing Standards or Spec sources and the affected axes. Use `Spec: skipped - no source available` when no Spec can be found.

The packet contains:

- captured review snapshot;
- Source Trace;
- repo instructions and engineering contract;
- Standards and Spec sources;
- acceptance criteria or bounded slice;
- touched seams, public interfaces, and data contracts;
- validation commands;
- migration, generated-artifact, permission, network, and external-service constraints.

Done means every reviewer receives the same snapshot, source trace, repo contract, risk surfaces, and validation context.

## 3. Dispatch Independent Reviewers

Dispatch the configured reviewer subagents in parallel, isolated from one another and from each other's findings.

Assign one reviewer the Standards axis and one the Spec axis. Assign additional reviewers distinct risk lenses from the changed surface.

Every reviewer receives the same captured snapshot and Source Trace.

Reviewer prompt:

```text
Review the captured snapshot against its fixed point.

Review snapshot:
<captured target>

Source Trace:
<sources>

Axis:
<Standards / Spec / Risk>

Lens:
<primary lens>

Review read-only. Return only high-confidence actionable findings with file:line evidence, impact, severity, and remediation direction. Focus on correctness, behavioral regressions, broken contracts, workflow failures, missing validation, CI blockers, security/permission risk, and operator risk. Style-only feedback, broad refactors, and speculation are out of scope.
```

If subagents are unavailable, run separated manual lens passes and mark the report reduced-confidence. These passes are distinct, not independent.

**Independence gate:** require at least two isolated reviewer passes over the same snapshot. Replace failed or timed-out reviewers. When isolation is unavailable, allow two separated manual lens passes only as a reduced-confidence fallback and label the review non-independent.

Done means at least two independent passes completed over the same snapshot, or two reduced-confidence separated passes were reported as non-independent, or the review stopped incomplete with the missing lenses reported.

## 4. Build The Evidence Ledger

Normalize reviewer output into one evidence ledger.

Each ledger item includes ID, severity, axis, title, evidence, impact, remediation direction, reviewer lens, confidence, status, verification state, and blocking decision.

Axis is `Standards`, `Spec`, or `Risk`; lens is the reviewer's assigned focus. Cross-axis overlap may be linked but remains separate.

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

Verification and status must agree:

- verified survivor -> `accepted`
- disproved finding -> `rejected`
- unresolved finding -> `disputed`
- unavailable verification -> `not checked` with reason and confidence impact

Evidence decides: consensus is signal, not truth; one-reviewer findings can survive; agreed findings can fail.

Done means every reviewer finding is represented, and every surviving candidate has an ID.

## 5. Converge

Run convergence rounds against the ledger, not raw transcripts.

Ask reviewers to confirm, reject, revise, merge, split, or dispute ledger items from their lens. New findings after round 1 need direct file, diff, or command evidence and must be marked `new in round <N>`.

Merge duplicates only within an axis; link cross-axis overlap without collapsing it.

Stop early on no material delta: no new findings, status changes, severity changes, remediation changes, or unresolved accept/reject disagreement.

Done means the ledger converged, or max rounds were reached and remaining disagreement is marked disputed.

## 6. Verify Survivors

The orchestrator verifies accepted and disputed findings.

Use the cheapest meaningful evidence: inspect cited lines, inspect nearby tests, run `git diff --check`, run targeted validation, or inspect affected config, migrations, permissions, or operator workflows.

Keep generated verification artifacts local and disposable under `.tmp/`; delete them or name each intentionally preserved path in the report. Hand off any evidence that must become tracked `.scratch/` state to downstream implementation. Use installs, network or external services, destructive commands, or large generated artifacts only when explicitly requested and permitted by the repo contract and tool policy.

Done means every accepted or disputed finding has a consistent status and verification state; disproved findings were rejected; and every `not checked` item records the blocker, confidence impact, and provisional blocking decision.

## 7. Triage And Report

Severity:

- `P0`: data loss, security exposure, or catastrophic production break.
- `P1`: merge-blocking correctness, contract, or workflow failure on an important path.
- `P2`: required validation or CI failure, important missing validation, optional-tooling blocker, or significant edge-case bug.
- `P3`: lower-risk correctness or maintainability issue with concrete impact.

P0/P1 block merge. P2 blocks when required validation or CI is affected. P3 does not block unless the user says otherwise.

Before reporting, rerun the staleness check. If HEAD or the worktree changed from the pinned fixed point, mark the review stale unless rerun.

Begin with:

```text
Review snapshot: <fixed point and captured target>
Source Trace: <sources and skipped axes>
Reviewers: <completed lenses / requested lenses>
Rounds: <completed / maximum>
Confidence: <full / reduced with reason>
```

Report the final ledger under:

```md
## Standards
## Spec
## Risk
## Rejected Or Duplicate
```

Keep findings in their axis. Sort within each axis by severity. Include ID, location, evidence, impact, remediation direction, verification state, confidence, and blocking decision.

When no accepted finding exists for an axis, report `No accepted findings.`

End accepted findings with a patch-ready handoff: finding ID, likely files, required change, and validation expected after the fix.

Done means the report returns the complete ledger, preserves axis separation, records drift and confidence, and provides a patch-ready handoff for every accepted finding.

## Completion Criteria

Complete only when the fixed point and non-empty review snapshot are pinned; Source Trace is recorded; at least two isolated reviewer passes reviewed the same captured target, or the result is explicitly reduced-confidence and non-independent; Standards and Spec ran or Spec was explicitly skipped and replaced; every reviewer finding is represented in the ledger; status and verification agree; survivors are verified or explicitly not checked; drift and the read-only boundary were checked; severity and blocking decisions are clear; and the final ledger plus any patch-ready handoff were returned.
