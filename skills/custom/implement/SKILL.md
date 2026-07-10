---
name: implement
description: Implement one bounded work item through the repo's convergence loop, with standalone closeout or staged worker handoff.
---

# Implement

Implement exactly one selected work item: a chat-selected slice, GitHub issue, local tracker issue, spec/path/URL slice, or another explicit implementation target.

If the source contains multiple slices, choose one bounded ready-for-agent slice and stop after it. If no work item is supplied, select the next unblocked ready-for-agent item from the tracker.

Apply the **readiness gate** before Patch: the selected work item is unblocked, its behavior and acceptance criteria are settled, and a proof seam can be named from repo evidence. If the gate fails, stop with the gaps and recommend shaping.

## Preconditions

Read `docs/agents/engineering-contract.md`. If it is missing, stop and recommend `$setup-matt-pocock-skills`.

Read tracker docs only for tracker selection, claim, semantics, or closeout.

## Modes

- **Owner:** implements or integrates one selected work item; owns fixed point, authoritative proof, `$review`, Lock, commit, and tracker closeout.
- **Staged worker:** owns only the assigned patch, focused proof, staging of that patch, and the handoff packet. Within this skill, `worker` means staged worker.
- **Scout:** owns read-only advice on seam, scope, or validation.

Formal review, commit, tracker mutation, and delegation are owner-only.

## Intake

Identify the selected work item, source, acceptance criteria, blockers, and out-of-scope boundaries.

**Clean baseline:** before editing or dispatch, capture the **fixed point** and inspect the worktree and index. If unrelated staged work exists, preserve it and use a clean worktree for the selected work; never unstage prior work. Stop if safe isolation is unavailable. Workers never commit prior dirty work. Owners may commit prior dirty work only when the user explicitly asks or a named repo doc defines that finish mode. If other dirty work remains, continue only when the selected work item can be isolated safely; record unrelated dirty files in the final note.

For tracker-backed work, claim the item through `docs/agents/issue-tracker.md` before editing or dispatch.

Read only task-relevant comments, parent context, files, and nearby code. Treat the work item as one bounded slice.

## Patch

Use `$tdd` when behavior is clear enough for a RED test through a useful seam. Otherwise name the proof seam, use the strongest focused evidence, and record why RED was unsuitable. Keep the patch inside the selected work item; record adjacent work as follow-ups.

## Staged Worker Handoff

Only owner acceptance of the staged packet closes the **handoff gate**. Returning the packet makes the staged worker handoff-ready.

The packet includes `git status --short`, staged diff summary, validation, skipped checks, residual risk, and unrelated dirty files.

Workers run focused proof plus `git diff --cached --check`; add the full suite only when broad, high-risk, cheap, or explicitly requested. On feedback, update the patch, refresh staging, rerun focused proof, and return a revised packet.

## Converge

If supervising a worker, avoid overlapping code changes while the worker runs. After handoff, inspect `git status --short` and the staged diff.

Run **authoritative proof** on the assembled diff: acceptance checks, canonical focused checks from `AGENTS.md`, whitespace, and risk-scaled broader validation.

**Scope fence:** stage every selected-work-item change before review, including in-scope tracker files and accepted worker handoff. Verify the cached diff contains no unrelated file or hunk, then run `git diff --cached --check`.

Capture the immutable **review tree** with `git write-tree`. Invoke `$review` with the fixed point, review tree, and `git diff <fixed-point> <review-tree>`. If `$review` is unavailable, stop before Lock and report the missing review route.

Fix in-scope findings with targeted verification. Prepare the closeout packet: summary, review result, validation run, skipped checks, and residual risk. For repo-local tracker files, add the packet and move the item to `implemented` before capturing the lock tree. Repo-local notes need not include the commit SHA.

Restage every selected-work-item change and capture the **lock tree** with `git write-tree`.

**Delta gate:** inspect `git diff <review-tree> <lock-tree>`. Finding-only fixes and closeout-only metadata need targeted verification. A material behavior, scope, or contract delta requires another `$review` with the lock tree as the new review tree. Apply findings, restage, capture a new lock tree, and repeat until the lock tree is reviewed or differs only by verified finding fixes and closeout metadata.

## Lock

Prefer one commit per work item unless the user asks for separate commits or repo policy requires split commits.

**Index lock:** immediately before commit, require `git write-tree` to equal the approved lock tree, then run `git diff --cached --check`. A mismatch returns to the delta gate.

Commit to the current branch with a message that names the selected work item or behavior.

Verify `git rev-parse HEAD^{tree}` equals the approved lock tree. Treat a mismatch as lock failure and stop before external tracker closeout.

Add the commit SHA to the closeout packet for connector posting or the final response.

For connector-backed trackers, mutate external tracker state only after the commit succeeds and its tree matches the lock tree: post the closeout packet, add/apply `implemented`, remove any prior state-role label, and close only if the user or tracker docs say so.

Apply the tracker's **Mutation read-back** rule. A closeout that cannot be read back is blocked, not done.

If the work item is not tracker-backed, after commit use the closeout packet as the final response.

## Done

Owner done means one selected work item is implemented or integrated from worker handoff, validated, reviewed from the fixed point through an immutable review tree, committed with a tree matching the approved lock tree, and, when tracker-backed, noted and moved to `implemented`.

Staged-worker handoff-ready means a focused patch is staged and reported. Delegated work is done only after owner acceptance.
