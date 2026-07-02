---
name: implement
description: Pick up one ready-for-agent issue, implement it through the repo's existing seams, verify it, review it, commit it, and leave an implementation note.
---

# Implement

Implement one ready-for-agent issue. Stop after one issue.

If the user names an issue, path, or URL, implement that. If the user names a PRD or spec, use it to find or choose one ready-for-agent issue, then stop after that issue. Otherwise, find the next unblocked issue labeled `ready-for-agent` using `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. For local markdown trackers, scan the configured local issue files and use the mapped ready status.

## Preconditions

Read `docs/agents/engineering-contract.md`, `docs/agents/issue-tracker.md`, and `docs/agents/triage-labels.md`; run `$setup-matt-pocock-skills` if any are missing.

When touching codebase context, read `docs/agents/domain.md` if present so implementation, tests, issue notes, and commit text use domain glossary vocabulary and respect ADRs.

## Process

Use the convergence loop scaled to the issue: orient, explore, choose, prove, expand, converge, simplify, lock. Tiny issues can compress the loop; uncertain or risky issues should make the gates explicit.

### 1. Select The Issue

If no issue is provided, choose the next unblocked ready-for-agent issue in dependency order. Skip issues whose blockers are incomplete.

If multiple issues are ready and order is ambiguous, ask the user which one to pick. If no issue is available, stop and say so.

### 2. Capture Baseline

Inspect the worktree before editing. Preserve unrelated changes.

Capture the starting ref before editing; `$review` uses this fixed point.

Stage and commit only files touched for this issue.

### 3. Orient And Explore

Read the full issue, comments or local notes, parent PRD/spec, linked context, acceptance criteria, blockers, and out-of-scope boundaries.

Treat the selected issue as one bounded slice. For a tracer-bullet issue, identify the behavior to prove, the acceptance criteria it must satisfy, and the highest useful interface or seam to test through. For a support issue, identify what it unblocks or proves, how it stays behavior-preserving when relevant, and what observable validation shows it is complete. Prefer existing seams. Use `$tdd` where practical.

Explore enough to choose the best local approach. Use `.tmp/` for disposable spikes, copied references, experiments, and rough notes when that reduces uncertainty; delete scratch artifacts before final delivery unless the user asks to preserve them.

Ask only when implementation would otherwise be guesswork or when the better approach changes the commitment: product intent, acceptance criteria, semantic correctness, user-visible behavior beyond the request, public contracts, dependency or tooling choices, migration/data semantics, security/privacy posture, or the bounded slice itself.

### 4. Choose And Implement

Choose one approach and make the narrow change needed to complete the selected slice. Technique belongs to the agent; requirements and end result belong to the user. If internal behavior is load-bearing for the result, give it a contract and prove it through the smallest meaningful seam.

Do not expand scope beyond the selected slice.

Do not add extra tracer bullets or support slices just because adjacent cases exist. Add another behavior test or validation check only when it proves a materially different branch, risk, acceptance criterion, or unblocker. Record useful follow-ups in the final note instead of widening the slice.

For behavior changes, use red-green-refactor through the highest useful interface or seam when the code slice is suitable for TDD. Do not replace TDD discipline with after-the-fact checks. Prove semantic correctness: fixtures, examples, invariants, row-level expectations, checksums, or other evidence should show the output is correct, not merely present.

Run focused checks regularly: single test files, typecheck, lint, or the repo's closest equivalent.

### 5. Prove And Simplify

Confirm acceptance criteria are satisfied.

Run focused tests/checks and the full test suite or repo-standard validation if feasible. Explain skipped validation.

Simplify only while behavior is protected: remove disposable scaffolding, collapse bloated branches, improve names, and deepen modules only when it helps this slice. Keep behavior unchanged unless the issue requires the change.

### 6. Converge

Run `$review` against the starting ref using its default sequential mode.

If this `$implement` run is itself delegated to a subagent, do not treat that as permission to spawn review subagents. Escalate only when the user explicitly requests review delegation, or when the selected review layer is `$convergent-pr-review` for local PR or high-risk convergence review.

Fix in-scope findings. Record out-of-scope findings in the final note instead of expanding the slice.

### 7. Lock

Commit to the current branch with a message that references the issue.

Leave a concise implementation note on the issue. Include commit SHA, summary, review layer, validation run, skipped checks, and residual risk. For local markdown trackers, append the note using the repo convention, or under `## Implementation Notes` if none exists.

Do not close, relabel, change `Status:`, or otherwise change issue state unless the user asks or `docs/agents/issue-tracker.md` defines that workflow.

## Completion Criteria

Done means one issue is implemented, reviewed against the starting ref, committed, and noted; validation is recorded; unrelated work is preserved; issue state changes only when requested or repo-defined.
