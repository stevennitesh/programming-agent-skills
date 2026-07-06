---
name: implement
description: Implement one bounded work item through the repo's convergence loop, with standalone closeout or staged worker handoff.
---

# Implement

Implement exactly one selected work item: a chat-selected slice, GitHub issue, local tracker issue, PRD/spec/path/URL slice, or another explicit implementation target.

If the source contains multiple slices, choose one bounded ready-for-agent slice and stop after it. If no work item is supplied, select the next unblocked ready-for-agent item from the tracker.

Implement is execution, not product discovery: the work item should be settled enough to name the behavior, acceptance criteria, and proof seam. If the work is not settled, stop and recommend the shaping skill that fits; do not reopen product decisions inside `$implement`.

## Preconditions

Read `docs/agents/engineering-contract.md`. If it is missing, stop and recommend `$setup-matt-pocock-skills`.

Read tracker docs only for tracker selection, tracker semantics, or tracker closeout.

## Modes

- Owner: implements or integrates one selected work item; owns fixed point, authoritative proof, review, lock, commit, and tracker closeout.
- Worker: implements only the assigned slice; stages the patch and returns a handoff packet.

Workers do not commit, run formal `$review`, mutate trackers, fan out, or stage unrelated changes.

A read-only scout may advise on seam, scope, or validation only when the owner says so before dispatch. Scouts do not edit, stage, commit, run formal `$review`, or mutate tracker state.

## Intake

Identify the selected work item, source, acceptance criteria, blockers, and out-of-scope boundaries.

Clean baseline: inspect the worktree before editing. Workers never commit prior dirty work. Owners may commit prior dirty work only when the user explicitly asks or a named repo doc defines that finish mode. If dirty work remains, continue only when the selected work item can be isolated safely; record unrelated dirty files in the final note.

Read only task-relevant comments, parent context, files, and nearby code. Treat the work item as one bounded slice.

## Patch

Patch in tight red-green slices at pre-agreed seams. Before the first test, name the seam under test; if no red seam fits, use the strongest focused evidence and say why. Record follow-ups instead of adding adjacent cleanup or extra slices.

## Worker Handoff

Delegated work is done only when the worker returns a staged handoff packet and the owner accepts it. Do not infer completion from dispatch, silence, elapsed time, or partial progress.

The packet includes `git status --short`, staged diff summary, validation, skipped checks, residual risk, and unrelated dirty files.

Workers run focused proof plus `git diff --cached --check`; add the full suite only when broad, high-risk, cheap, or explicitly requested. On feedback, update the patch, refresh staging, rerun focused proof, and return a revised packet.

## Converge

Owners capture the fixed point before editing or worker assignment.

If supervising a worker, avoid overlapping code changes while the worker runs. After handoff, inspect `git status --short` and the staged diff.

Run authoritative proof on the assembled diff: acceptance checks, quick repo lint when discoverable, whitespace check, and risk-scaled broader validation.

For repo-local tracker files, add the closeout packet and move the item to `implemented` before final review.

Stage new selected-work-item files before review. Invoke `$review` with the fixed point after the final diff is assembled; use a labeled local fallback if unavailable. Fix in-scope findings with targeted verification.

## Lock

Prefer one commit per work item unless the user asks for separate commits or repo policy requires split commits.

Prepare one closeout packet: summary, review result, validation run, skipped checks, and residual risk. Add the commit SHA after commit for connector posting or final response; repo-local tracker notes need not include it.

Stage only selected-work-item changes, including in-scope tracker files, review fixes, and accepted worker handoff diff. Leave unrelated files and hunks unstaged, then run `git diff --cached --check`.

Commit to the current branch with a message that names the selected work item or behavior.

For connector-backed trackers, mutate external tracker state only after the commit succeeds: post the closeout packet, add/apply `implemented`, remove any prior state-role label, and close only if the user or tracker docs say so.

If the work item is not tracker-backed, after commit use the closeout packet as the final response.

## Done

Owner done means one selected work item is implemented or integrated from worker handoff, validated, reviewed once from the fixed point, committed, and, when tracker-backed, noted and moved to `implemented`.

Worker done means a focused patch is staged and reported in a handoff packet.
