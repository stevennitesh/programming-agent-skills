---
name: convergent-pr-review
description: "Coordinate independent PR review passes into a verified finding ledger and patch-ready triage."
---

# Convergent PR Review

## Intent

Use this skill to review a pinned PR or local diff through independent reviewer passes, converge findings into one ledger, verify surviving risks, and report only actionable issues.

This is a bug/risk convergence gate. It complements `$review`, which is the default Standards/Spec review skill. When Standards or Spec compliance matters, include those sources in the review packet or run `$review` separately.

Do not edit files unless the user explicitly asks to fix findings.

## Defaults

- Base ref: `main`
- Reviewers: `2`
- Reasoning effort: `high`
- Max rounds: `2`
- Review depth: `standard`
- Severity: `P0/P1/P2/P3`

Use a third round only for unresolved P0/P1/P2 findings, exhaustive review, or explicit user request.

## Use

Use this skill for risky PRs, release gates, shared plumbing, migrations, permissions, config, CI, workflow changes, or cases where one linear review pass is not enough.

Do not use it for tiny docs-only changes, formatting-only changes, or routine Standards/Spec checks where `$review` is enough.

## 1. Pin The Fixed Point

Establish exactly what is being reviewed.

Run:

- `git status --short --branch`
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse <base> HEAD`
- `git merge-base <base> HEAD`
- `git diff --stat <base>...HEAD`
- `git diff <base>...HEAD`
- `git log --oneline <base>..HEAD`

For PR numbers, resolve the PR base/head with GitHub tooling or `gh`, fetch the head if needed, then review the local fixed point.

For WIP review, include `git diff` and `git diff --cached` only when the user asks to review local changes.

Stop if the base does not resolve or the diff is empty.

Completion criterion: base/head SHAs, merge base, branch or PR target, diff stat, and commit range are captured, or the review has been stopped with the reason.

## 2. Build The Review Packet

Create a compact packet before reviewer passes. Include only context that changes review behavior:

- pinned base/head SHAs, branch or PR target, diff stat, and commits;
- repo instructions such as `AGENTS.md`, `CLAUDE.md`, README guidance, active plans, or workflow docs;
- Standards sources and Spec source, when applicable;
- changed surfaces and owned contracts;
- validation commands from repo docs, scripts, CI, or package config;
- generated artifact, migration, network, permission, fixture, or external-service constraints.

Completion criterion: reviewers have the repo rules, relevant Standards/Spec sources, changed surfaces, contracts, and validation commands needed to avoid generic assumptions.

## 3. Run Independent Passes

Spawn reviewers in parallel when subagents are available. Keep first-pass reviews independent: do not share other reviewers' findings, suspected risks, or consensus hints.

Assign complementary lenses from the changed surface:

- runtime correctness and data contracts;
- workflow behavior, CLI/config/operator paths;
- tests, CI, validation, and docs integration;
- edge cases, error handling, and backward compatibility;
- performance, caching, generated artifacts, permissions, migrations, or security.

If subagents are unavailable, run reduced-confidence mode: perform separate manual passes with different lenses, keep the same ledger, and label the final report reduced-confidence.

Reviewer prompt:

```text
Review the local diff against <base> using `git diff <base>...HEAD`.

Base: <base sha>
Head: <head sha>
Target: <branch or PR>

Review packet:
<packet>

Do not edit files. Prioritize correctness bugs, behavioral regressions, broken contracts, workflow failures, operator risk, missing validation, and CI blockers. Return only high-confidence findings with precise file:line evidence, impact, severity, and remediation direction. Avoid style-only feedback, broad refactors, and speculation.

Lens: <assigned lens>
```

Completion criterion: every requested reviewer pass has returned, failed, or timed out; if fewer than requested complete, the ledger and final report are marked reduced-confidence.

## 4. Build The Finding Ledger

Normalize all reviewer output into one ledger.

Each finding has:

- ID
- severity
- axis: Standards, Spec, runtime correctness, workflow behavior, data contract, validation, operator risk, security, migration, or performance
- title
- file/line evidence
- impact
- remediation direction
- originating reviewer(s)
- confidence
- status: `candidate`, `accepted`, `rejected`, or `disputed`
- verification: `unverified`, `verified`, `disproved`, or `not checked`
- blocking decision

Deduplicate overlaps, but do not discard a finding only because one reviewer found it. A single-reviewer finding can be accepted if evidence verifies it. A unanimous finding can be rejected if evidence disproves it.

Completion criterion: every reviewer output is represented as an accepted duplicate, candidate, accepted, rejected, or disputed ledger item, and every surviving candidate has an ID.

## 5. Converge

Run cross-review rounds against the ledger, not raw reviewer transcripts.

For each round, ask reviewers to confirm, reject, revise, merge, split, or dispute ledger items. New findings after round 1 must have direct file/line or command evidence and should be labeled `new in round <N>`.

Stop early when the latest round has no material delta:

- no new findings;
- no status changes;
- no severity changes;
- no material impact/remediation changes;
- no unresolved accept/reject disagreement.

If max rounds are reached, preserve unresolved disagreements as `disputed`.

Completion criterion: the ledger has an empty material delta, or max rounds have been reached and all remaining disagreement is marked `disputed`.

## 6. Verify Survivors

The orchestrator owns verification. Reviewer consensus is evidence, not proof.

Use cheap local checks where practical:

- inspect cited lines;
- inspect nearby tests and sibling entrypoints;
- run `git diff --check`;
- run targeted tests, type checks, lint, or repo-local validation tied to the changed surface;
- check shared plumbing, config loading, path resolution, migrations, and operator workflows when findings touch those contracts.

Avoid installs, network-heavy probes, external services, destructive commands, or large generated artifacts unless the user requested that depth or repo docs make them part of the validation contract.

Completion criterion: every accepted or disputed finding has verification state `verified`, `disproved`, or `not checked` with a reason.

## 7. Triage

Accepted findings must be concrete, actionable, and tied to impact.

Severity:

- `P0`: data loss, security exposure, or catastrophic production break.
- `P1`: merge-blocking correctness, contract, or workflow failure on an important path.
- `P2`: CI/required-validation failure, important missing validation, optional-tooling blocker, or significant edge-case bug.
- `P3`: lower-risk correctness or maintainability issue with concrete impact.

P0/P1 block merge. P2 blocks when required validation or CI is affected. P3 does not block unless the user says otherwise.

Reject findings that are duplicates, style-only, speculative, disproved, already covered by adequate tests, or based on misunderstanding the diff.

Completion criterion: every ledger item is accepted, rejected, or disputed; every accepted item has severity, impact, remediation direction, verification state, and blocking decision.

## 8. Report

Before reporting, rerun `git rev-parse HEAD`. If HEAD changed from the pinned head SHA, mark the review stale or partial and do not present findings as current without rerunning.

Report from the ledger.

Lead with accepted findings by severity. For each finding include ID, severity, title, file:line evidence, impact, blocking decision, remediation direction, verification state, and consensus level.

Then include rejected/disputed counts, notable reasons, fixed point, review depth, reviewers, effort, rounds, convergence status, validation run, and residual risk.

If accepted findings remain, add a patch-ready handoff: finding ID, evidence, likely files to edit, and validation that should pass after the fix.

If there are no accepted findings, say that plainly and list verification performed plus residual risk.

Completion criterion: the final report is generated from the ledger, HEAD staleness is checked, and any remaining accepted finding has a patch-ready handoff.
