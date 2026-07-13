---
name: implement
description: Implement exactly one selected ready work item through staging, review, one commit, and repo-policy tracker closeout; in staged-worker mode, stop at a staged patch and handoff.
---

# Implement

Implement exactly one **selected work item**: one tracker item, chat-selected bounded slice, or path or URL whose content already defines one ready item.

A parent spec, plan, queue, batch, list, or bare source path is selection context, not implementation scope.

- **Explicit target:** Treat the user's target as binding. If it is ineligible, blocked, ambiguous, or unready, stop on that target and report the failed gate.
- **No target:** Use repo-visible readiness, dependency, and ordering policy to select the next unblocked ready-for-agent item. When that policy does not identify one next item, ask instead of choosing by taste.
- **Selection boundary:** Selection reads state; it does not repair it. Do not substitute, split, relabel, promote, or reprioritize tracker state. Return unsliced source to `$to-tickets` and other failed gates to the owner that can settle them.

Apply the **readiness gate** before Patch: the selected work item is eligible when tracker-backed; its expected behavior and acceptance criteria are settled; it is unblocked; and an observable done signal exists. A non-diagnostic path also names a proof seam from repo evidence. An uncertain bug may instead enter `$diagnosing-bugs` when expected and actual behavior are clear enough to investigate. If the gate fails, stop with the exact gap and one next owner.

## Preconditions

Read `docs/agents/engineering-contract.md`. If that contract or another required setup document or named operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`.

Read tracker docs only for tracker selection, claim, semantics, or closeout.

## Modes

- **Owner:** implements or integrates one selected work item; owns fixed point, authoritative proof, review route, Lock, commit, and tracker closeout.
- **Staged worker:** owns only the assigned patch, focused proof, staging of that patch, and the handoff packet. Within this skill, `worker` means staged worker.
- **Scout:** owns read-only advice on seam, scope, or validation.

Formal review, commit, tracker mutation, and delegation are owner-only.

**Owner authority:** Explicit owner-mode invocation authorizes selected-work staging, one commit, and tracker closeout allowed by repo policy. Push, deployment, PR creation, unrelated external messages, and destructive Git require separate authority.

## Intake

Identify the selected work item, source, acceptance criteria, blockers, and out-of-scope boundaries.

**Clean baseline:** before editing or dispatch, capture the **fixed point** and inspect the worktree and index. If unrelated staged work exists, preserve it and use a clean worktree for the selected work; never unstage prior work. Stop if safe isolation is unavailable. Workers never commit prior dirty work. Owners may commit prior dirty work only when the user explicitly asks or a named repo doc defines that finish mode. If other dirty work remains, continue only when the selected work item can be isolated safely; record unrelated dirty files in the final note.

For tracker-backed work, claim the item through `docs/agents/issue-tracker.md` before editing or dispatch.

Read only task-relevant comments, parent context, files, and nearby code. Treat the work item as one bounded slice.

## Patch

For red-testable new behavior, invoke `$tdd`. For a bug, invoke `$tdd` only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known.

When a bug's exact symptom, cause, or trusted red-capable reproduction is uncertain, invoke `$diagnosing-bugs` in fix mode with the selected work item as its caller. It owns the tight loop, cause gate, causal fix, and regression proof, then returns here for Converge. Implement retains review, staging, commit, tracker closeout, and Lock.

For work without a red-capable seam, name the proof seam, use the strongest focused evidence, and record why RED was unsuitable. Keep the patch inside the selected work item; record adjacent work as follow-ups.

## Staged Worker Handoff

Only owner acceptance of the staged packet closes the **handoff gate**. Returning the packet makes the staged worker handoff-ready.

The packet includes `git status --short`, staged diff summary, validation, skipped checks, residual risk, and unrelated dirty files.

Workers run focused proof plus `git diff --cached --check`; add the full suite only when broad, high-risk, cheap, or explicitly requested. On feedback, update the patch, refresh staging, rerun focused proof, and return a revised packet.

## Converge

If supervising a worker, avoid overlapping code changes while the worker runs. After handoff, inspect `git status --short` and the staged diff.

Run **authoritative proof** on the assembled diff: acceptance checks, canonical focused checks from `AGENTS.md`, whitespace, and risk-scaled broader validation.

**Scope fence:** stage every selected-work-item change before review, including in-scope tracker files and accepted worker handoff. Verify the cached diff contains no unrelated file or hunk, then run `git diff --cached --check`.

For repo-local tracker files, prepare review-visible closeout metadata before pinning the review target: summary, validation, skipped checks, residual risk, and `Review: pending`. Append it under `## Implementation Notes`, move the item to `implemented`, release its claim, stage the tracker file with the implementation diff, and apply the tracker's **Mutation read-back** rule. Repo-local notes need not include the commit SHA.

Capture the immutable **review tree** with `git write-tree`.

**Review route:** Invoke `$review` by default. Invoke `$convergent-pr-review` for a local PR or high-risk diff matching its trigger. Record the route and invoke exactly that route with `Spec required: yes`, the selected work item and acceptance criteria, Source Trace, fixed point, review tree, and `git diff <fixed-point> <review-tree>`. An unavailable route or unresolved Spec source blocks Lock.

**Review acceptance:** For `$convergent-pr-review`, `pass` unlocks Lock; `pass with residual risk` unlocks Lock only when the selected work item, repo policy, or user accepts every named residual risk and the closeout packet records that authority; `blocked` or `incomplete` keeps Lock closed. For `$review`, any P0/P1 finding, missing required validation, or incomplete Spec axis keeps Lock closed; record lower non-blocking findings as residual risk unless repo or user policy blocks them.

Fix in-scope findings with targeted verification. For repo-local tracker work, refresh the provisional closeout metadata after every finding fix, restage the complete selected-work diff, capture a new review tree, and run another pass through the selected review route. The final repo-local packet stays inside the reviewed tree.

After an acceptable review, prepare the closeout packet: summary, review result, validation run, skipped checks, and residual risk. For repo-local tracker work, replace `Review: pending` with the actual result and read the file back; the review-result field is the only post-review metadata change. Keep connector-backed closeout pending until Lock.

Restage every selected-work-item change and capture the **lock tree** with `git write-tree`.

**Delta gate:** inspect `git diff <review-tree> <lock-tree>`. Finding-only fixes and closeout-only metadata need targeted verification. A material behavior, scope, or contract delta requires another pass through the selected review route with the lock tree as the new review tree. Reselect the route when the delta changes risk. Apply findings, restage, capture a new lock tree, and repeat until the lock tree is reviewed or differs only by verified finding fixes and closeout metadata.

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

Owner done means one selected work item is implemented or integrated from worker handoff, validated, reviewed from the fixed point through the selected route and an immutable review tree, committed with a tree matching the approved lock tree, and, when tracker-backed, noted and moved to `implemented`.

Staged-worker handoff-ready means a focused patch is staged and reported. Delegated work is done only after owner acceptance.
