---
name: convergent-pr-review
description: "Use for local PR review, or high-risk local-diff review where one reviewer pass is not enough: release gates, shared plumbing, migrations, security/permissions, CI/workflow/config, public interfaces, or data contracts. For ordinary fixed-point Standards/Spec review, use review."
---

# Convergent PR Review

Review a local PR or high-risk local diff through independent reviewer passes, then converge their findings into one verified ledger.

This is a read-only convergence gate. Subagents are reviewers; the main agent is the orchestrator. Reviewer consensus is evidence, not truth. The orchestrator pins the fixed point, scopes reviewers, verifies surviving findings, decides severity, and writes the handoff.

Use `$review` instead for ordinary branch, WIP, or `review since X` fixed-point review where Standards and Spec are the main axes.

## Defaults

- Base ref: `main`
- Reviewers: `2`
- Max rounds: `2`
- Severity: `P0/P1/P2/P3`

Use more reviewers to broaden review lenses, not to repeat the same review:

- `2 reviewers`: default local PR review.
- `3 reviewers`: distinct runtime, validation, and workflow/API risk surfaces.
- `4-5 reviewers`: high-blast-radius changes with separable security, migration, public contract, CI/release, performance, or data-contract risk.
- `>5 reviewers`: only by explicit user request.

## 1. Pin The Fixed Point

Establish exactly what is being reviewed.

For branch or PR review, capture status, branch, base SHA, head SHA, merge base, diff stat, full diff, and commit range:

- `git status --short --branch`
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse <base> HEAD`
- `git merge-base <base> HEAD`
- `git diff --stat <base>...HEAD`
- `git diff <base>...HEAD`
- `git log --oneline <base>..HEAD`

For a PR number, resolve the PR base/head first, fetch the head if needed, then review the local fixed point.

For uncommitted worktree review, capture `git diff` and `git diff --cached`, and mark the review as worktree-based.

Stop if the base does not resolve or the diff is empty.

Done means the base, head, merge base, target, diff stat, and commit range are captured, or the review is stopped with the reason.

## 2. Build The Review Packet

Give reviewers only the context that changes review behavior:

- fixed point and diff command;
- repo instructions and engineering contract;
- Standards and Spec sources when they matter;
- acceptance criteria or bounded slice;
- touched seams, public interfaces, and data contracts;
- validation commands from repo docs, scripts, package config, or CI;
- known migration, generated-artifact, permission, network, or external-service constraints.

Done means reviewers have enough context to avoid generic review and stay inside the real repo contract.

## 3. Dispatch Independent Reviewers

Run independent reviewer passes in parallel when subagents are available. Keep first-pass reviewers isolated from each other's findings.

Assign each reviewer one primary lens from the changed surface: runtime correctness, validation/CI, operator workflow, public API, backward compatibility, data contracts, migration, generated artifacts, security, permissions, performance, or caching.

Reviewer prompt:

```text
Review the local diff against <base> using the pinned fixed point.

Fixed point:
<base/head/merge-base/target/diff command>

Review packet:
<packet>

Lens:
<lens>

Do not edit files. Return only high-confidence actionable findings with file:line evidence, impact, severity, and remediation direction. Prioritize correctness bugs, behavioral regressions, broken contracts, workflow failures, missing validation, CI blockers, security/permission risk, and operator risk. Avoid style-only feedback, broad refactors, and speculation.
```

If subagents are unavailable, run separate manual passes with distinct lenses and mark the report reduced-confidence.

Done means every reviewer pass has returned, failed, or timed out, and missing reviewers are reflected in the confidence of the final report.

## 4. Build The Ledger

Normalize reviewer output into one finding ledger.

Each ledger item includes ID, severity, axis, title, evidence, impact, remediation direction, reviewer lens, confidence, status, verification state, and blocking decision.

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

Do not accept a finding because reviewers agree. Do not reject a finding because only one reviewer found it. Evidence decides.

Done means every reviewer finding is represented as accepted, rejected, duplicate, or disputed, and every surviving candidate has an ID.

## 5. Converge

Run convergence rounds against the ledger, not raw transcripts.

Ask reviewers to confirm, reject, revise, merge, split, or dispute ledger items from their lens. New findings after round 1 need direct file, diff, or command evidence and must be marked `new in round <N>`.

Stop early when the round has no material delta: no new findings, status changes, severity changes, material remediation changes, or unresolved accept/reject disagreement.

Done means the ledger has converged, or max rounds were reached and remaining disagreement is marked disputed.

## 6. Verify Survivors

The orchestrator verifies accepted and disputed findings.

Use the cheapest meaningful evidence: inspect cited lines, inspect nearby tests, run `git diff --check`, run targeted validation, or inspect affected config, migrations, permissions, or operator workflows.

Avoid installs, network-heavy checks, external services, destructive commands, or large generated artifacts unless the user requested that depth or the repo contract requires it.

Done means every accepted or disputed finding is verified, disproved, or explicitly marked not checked with a reason.

## 7. Triage And Report

Severity:

- `P0`: data loss, security exposure, or catastrophic production break.
- `P1`: merge-blocking correctness, contract, or workflow failure on an important path.
- `P2`: required validation or CI failure, important missing validation, optional-tooling blocker, or significant edge-case bug.
- `P3`: lower-risk correctness or maintainability issue with concrete impact.

P0/P1 block merge. P2 blocks when required validation or CI is affected. P3 does not block unless the user says otherwise.

Before reporting, rerun the staleness check. If HEAD or the worktree changed from the pinned fixed point, mark the review stale unless rerun.

Report accepted findings first by severity. Include ID, evidence, impact, blocking decision, remediation direction, verification state, and consensus level. Then include disputed/rejected counts, fixed point, reviewer lenses, rounds, validation run, confidence, and residual risk.

If accepted findings remain, end with a patch-ready handoff: finding ID, likely files to edit, and validation that should pass after the fix.

Done means the final report comes from the verified ledger, drift is checked, and every accepted finding has a handoff.
