---
name: implement
description: Implement one selected ready work item automatically through bounded review repair, one commit, and repo-policy closeout; when explicitly assigned as a staged worker, stop at a staged patch.
---

# Implement

Implement exactly one selected ready work item.

Owner mode is the default. Staged-worker mode requires an explicit assignment and accepting owner.

**Owner: Select -> Charter -> Patch -> Review -> Repair -> Lock -> Close.**

**Staged worker: Select -> Patch -> Return.**

- **Owner:** owns tracker claim and release, review, commit, Lock, and closeout.
- **Staged worker:** owns only its assigned patch, focused proof, staging, and handoff; it never mutates tracker state.

Owner-mode invocation authorizes in-scope staging, Repair within the recorded Budget, one commit, and repo-policy closeout. Push, deployment, PR creation, destructive Git, and unrelated external mutations require separate authority.

## Select

Read `docs/agents/engineering-contract.md`. If it or another required setup surface is absent or incompatible with this skill, recommend `$repo-bootstrap` and stop. Read tracker docs only for tracker-backed work.

A parent spec, plan, queue, batch, list, or bare source path is context, not implementation scope.

- An explicit target is binding. If it is blocked, ambiguous, or unready, report that gate instead of substituting another item.
- Without a target, follow repo readiness, dependency, and ordering policy. Ask when it does not identify one next item.
- Selection reads state; it does not split, relabel, promote, reprioritize, or otherwise repair it. Return unsliced work to `$to-tickets`.

Ready means expected behavior and acceptance criteria are settled, the item is unblocked, and an observable proof seam exists. Tracker-backed items must also satisfy tracker eligibility.

For tracker-backed work, the owner claims the item before editing or dispatch. A staged worker verifies that claim and does not mutate tracker state. Capture the fixed point, worktree, and index; preserve unrelated work and isolate the selected diff.

## Charter

Record one implementation **Charter** from the selected item and Source Trace: outcome, acceptance criteria, supported workflows and environments, required validation, commitment boundary, non-goals, fixed point, review route, and Repair Budget. Default the Budget to two generations unless the caller explicitly sets a smaller bound.

The Charter controls every review and Repair generation. Technique may change inside it; a product, acceptance, public or data contract, security or privacy posture, dependency-authority, supported-environment, or scope change requires a caller decision before mutation.

## Patch

Keep changes inside the selected item.

Invoke `$tdd` for red-testable new behavior. For bugs, use `$tdd` only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. When a bug's exact symptom, cause, or trusted red-capable reproduction is uncertain, invoke `$diagnosing-bugs` in fix mode and resume here after regression proof.

When RED is unsuitable, name the proof seam and use the strongest focused evidence.

A staged worker stages only its assigned patch, runs focused proof plus `git diff --cached --check`, and returns status, staged diff summary, validation, skipped checks, residual risk, and unrelated dirty files. Only owner acceptance completes the handoff.

## Review

The owner runs canonical acceptance and risk-scaled proof on the assembled diff.

Stage the complete selected-work diff, exclude unrelated hunks, and run `git diff --cached --check`. Capture the immutable **review tree** with `git write-tree`.

Invoke exactly one route for the campaign:

- `$review` for an ordinary diff;
- `$convergent-pr-review` for a local PR or matching high-risk diff.

Pass `Spec required: yes`, `Review mode: initial`, the Charter, selected work item, Source Trace, acceptance criteria, fixed point, review tree, and its diff.

Review is acceptable only when complete and no admitted blocker remains. `pass with residual risk` is acceptable automatically only when every residual is nonblocking under the Charter and repo policy requires no separate acceptance. An incomplete review, unresolved Spec, missing required validation, or admitted blocker keeps Lock closed.

The recorded Charter and remaining Budget control Repair.

## Repair

Read [FINDING-CONTRACT.md](../review/FINDING-CONTRACT.md) and independently validate the complete report before editing.

Continue automatically only when every blocker is admitted, marked `automatic-in-scope`, preserves the Charter, has bounded proof, and the Budget remains. If any blocker is ambiguous or `decision-required`, return the whole decision packet without partially repairing it. An `incomplete` review is not repair authority.

Batch every eligible blocker into one Repair generation. Patch only those finding IDs, run their required proof plus regression proof, restage, and capture one successor review tree. Invoke the same route with `Review mode: remediation`, the original Charter, generation number, prior snapshot, carried finding IDs, repair delta, and remaining original acceptance.

Stop when the review is acceptable, a decision is required, or the recorded Budget is exhausted.

After acceptable review, prepare the closeout packet: summary, review result, validation, skipped checks, and residual risk. For repo-local trackers, record it, move the item to `implemented`, release the claim, apply Mutation read-back, and stage the tracker file.

## Lock

Capture the **lock tree** with `git write-tree`.

Inspect `git diff <review-tree> <lock-tree>`. Only verified closeout metadata may differ from the reviewed tree. Any implementation, behavior, scope, or contract delta returns to Review.

Require the index tree to equal the approved lock tree, run `git diff --cached --check`, and commit once to the current branch. Then require `HEAD^{tree}` to equal the approved lock tree.

A mismatch blocks external closeout. Add the commit SHA to the closeout packet.

## Close

After Lock, apply connector-backed tracker closeout through repo policy and Mutation read-back. Failed read-back is blocked, not done.

Done means the selected item is proven, the current snapshot has no admitted blocker, the approved tree is committed, and, when tracker-backed, the item is moved to `implemented`.

Return the mode, selected item, final status, commit SHA or staged-handoff summary, review result, validation, skipped checks, residual risk, tracker read-back or `not applicable`, current Git state, and the exact next action for any blocked outcome.
