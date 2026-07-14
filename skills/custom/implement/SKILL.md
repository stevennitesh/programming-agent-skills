---
name: implement
description: Implement one selected ready work item through review, one commit, and repo-policy closeout; when explicitly assigned as a staged worker, stop at a staged patch.
---

# Implement

Implement exactly one selected ready work item.

Owner mode is the default. Staged-worker mode requires an explicit assignment and accepting owner.

**Owner: Select -> Patch -> Review -> Lock -> Close.**

**Staged worker: Select -> Patch -> Return.**

- **Owner:** owns tracker claim and release, review, commit, Lock, and closeout.
- **Staged worker:** owns only its assigned patch, focused proof, staging, and handoff; it never mutates tracker state.

Owner-mode invocation authorizes in-scope staging, one commit, and repo-policy closeout. Push, deployment, PR creation, destructive Git, and unrelated external mutations require separate authority.

## Select

Read `docs/agents/engineering-contract.md`. If it or another required setup surface is absent or incompatible with this skill, recommend `$repo-bootstrap` and stop. Read tracker docs only for tracker-backed work.

A parent spec, plan, queue, batch, list, or bare source path is context, not implementation scope.

- An explicit target is binding. If it is blocked, ambiguous, or unready, report that gate instead of substituting another item.
- Without a target, follow repo readiness, dependency, and ordering policy. Ask when it does not identify one next item.
- Selection reads state; it does not split, relabel, promote, reprioritize, or otherwise repair it. Return unsliced work to `$to-tickets`.

Ready means expected behavior and acceptance criteria are settled, the item is unblocked, and an observable proof seam exists. Tracker-backed items must also satisfy tracker eligibility.

For tracker-backed work, the owner claims the item before editing or dispatch. A staged worker verifies that claim and does not mutate tracker state. Capture the fixed point, worktree, and index; preserve unrelated work and isolate the selected diff.

## Patch

Keep changes inside the selected item.

Invoke `$tdd` for red-testable new behavior. For bugs, use `$tdd` only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. When a bug's exact symptom, cause, or trusted red-capable reproduction is uncertain, invoke `$diagnosing-bugs` in fix mode and resume here after regression proof.

When RED is unsuitable, name the proof seam and use the strongest focused evidence.

A staged worker stages only its assigned patch, runs focused proof plus `git diff --cached --check`, and returns status, staged diff summary, validation, skipped checks, residual risk, and unrelated dirty files. Only owner acceptance completes the handoff.

## Review

The owner runs canonical acceptance and risk-scaled proof on the assembled diff.

Stage the complete selected-work diff, exclude unrelated hunks, and run `git diff --cached --check`. Capture the immutable **review tree** with `git write-tree`.

Invoke exactly one route:

- `$review` for an ordinary diff;
- `$convergent-pr-review` for a local PR or matching high-risk diff.

Pass `Spec required: yes`, the selected work item, Source Trace, acceptance criteria, fixed point, review tree, and its diff.

Review is acceptable only when complete and every finding is fixed or explicitly accepted as residual risk by selected-item, repo, or user authority. A route decision of `blocked` or `incomplete`, unresolved Spec, or missing required validation keeps Lock closed.

Fix findings, restage, capture a new review tree, and repeat the selected route.

After acceptable review, prepare the closeout packet: summary, review result, validation, skipped checks, and residual risk. For repo-local trackers, record it, move the item to `implemented`, release the claim, apply Mutation read-back, and stage the tracker file.

## Lock

Capture the **lock tree** with `git write-tree`.

Inspect `git diff <review-tree> <lock-tree>`. Only verified closeout metadata may differ from the reviewed tree. Any implementation, behavior, scope, or contract delta returns to Review.

Require the index tree to equal the approved lock tree, run `git diff --cached --check`, and commit once to the current branch. Then require `HEAD^{tree}` to equal the approved lock tree.

A mismatch blocks external closeout. Add the commit SHA to the closeout packet.

## Close

After Lock, apply connector-backed tracker closeout through repo policy and Mutation read-back. Failed read-back is blocked, not done.

Done means the selected item is proven, reviewed from its fixed point, committed with the approved tree, and, when tracker-backed, moved to `implemented`.

Return the mode, selected item, final status, commit SHA or staged-handoff summary, review result, validation, skipped checks, residual risk, tracker read-back or `not applicable`, current Git state, and the exact next action for any blocked outcome.
