---
name: implement
description: Implement one selected ready work item automatically through bounded review repair, one commit, and repo-policy closeout; when explicitly assigned as a staged worker, stop at a staged patch.
---

# Implement

Deliver exactly one selected ready work item.

**Owner: Select -> Charter -> Patch -> Review -> Repair -> Lock -> Close -> Return.**

**Staged worker: Select -> Patch -> Return.**

The owner holds tracker claim and release, accepted scope, review, Repair,
commit, Lock, and closeout. An explicitly assigned staged worker owns only its
patch, focused proof, staging, and handoff to a named accepting owner; it never
mutates tracker state.

Owner invocation authorizes selected-work staging, budgeted Repair, one commit,
and repo-policy closeout. Push, deployment, PR creation, destructive Git, and
unrelated external mutation require separate authority.

## Select

Read `docs/agents/engineering-contract.md` and, only for tracker-backed work,
tracker guidance. Missing or incompatible setup Returns a `$repo-bootstrap`
precondition without mutation.

Select one ready item:

- a named target is binding; Return its dependency or identity blocker without
  substitution;
- a parent spec, plan, queue, batch, list, or bare path is context, not scope;
  Return unsliced or shaping-unready work to `$to-tickets` with its defects;
- otherwise follow repository readiness, dependency, and ordering policy; ask
  when it does not determine one item; and
- read selection state without splitting, relabeling, promoting,
  reprioritizing, or making work ready.

Ready means settled behavior and acceptance, satisfied dependencies, an
observable proof seam, and applicable tracker eligibility.

Before editing or dispatch, the owner acquires and reads back any required
claim; a staged worker verifies it. Capture the fixed point, worktree, and
index, preserve unrelated work, and isolate the selected diff.

## Charter And Patch

Record one immutable **Charter**: selected item and source, outcome, acceptance,
supported workflows and environments, required proof, commitment boundary,
non-goals, fixed point, review route, and Repair Budget. Default to two
generations unless the caller sets a smaller bound.

Hold one bounded slice and proof story inside it: behavior or support purpose,
acceptance link, highest meaningful proof seam, non-goals, and required coupled
surfaces. A change to product intent, acceptance, public or data contracts,
security or privacy posture, dependency authority, supported environment, or
scope Returns for caller judgment before mutation.

Invoke `$tdd` for settled red-testable behavior. For a bug, use `$tdd` only
when expected behavior, exact symptom, cause, and a trusted red-capable
reproduction are known; otherwise invoke `$diagnosing-bugs` in fix mode and
resume from its causal packet.

When RED is unsuitable, record why and use the strongest focused semantic
evidence through the highest meaningful supported seam. Tie every changed
artifact to acceptance or the proof story; Return optional adjacent work.

A staged worker stages only its assignment, runs focused proof and
`git diff --cached --check`, then Returns staged paths, proof, skips, risk,
unrelated state, and the exact owner action. Only owner acceptance completes
the handoff.

## Review And Repair

The owner runs canonical acceptance, stages only the selected-work diff, runs
`git diff --cached --check`, and captures one immutable review tree.

Invoke exactly one campaign route: `$review` for an ordinary diff or
`$convergent-pr-review` for a local PR or matching high-risk diff. Pass
`Spec required: yes`, `Review mode: initial`, the Charter, item, Source Trace,
acceptance, fixed point, review tree and diff, validation, skips, and risk.

Accept only a complete current review with no admitted blocker.
`pass with residual risk` also requires every residual to be nonblocking under
the Charter and no separate repository-policy acceptance.

Before editing, read `$review`'s disclosed `FINDING-CONTRACT.md` and validate
the complete report. Repair only when every blocker is admitted,
`automatic-in-scope`, Charter-preserving, proof-bounded, and within Budget;
otherwise Return the whole decision packet without a partial fix.

One Repair generation batches every eligible ID, proves the patch, captures
one successor tree, and invokes the same route in `Review mode: remediation`
with the original Charter, generation, prior tree, IDs, delta, and remaining
acceptance. Stop on acceptable review, caller decision, proof or isolation
blocker, or exhausted Budget.

## Lock And Close

After acceptable review, prepare closeout. For a repo-local tracker, write the
final note, mark `implemented`, release the claim, read back the mutation, and
stage the tracker file before Lock.

Capture the lock tree and inspect
`git diff <review-tree> <lock-tree>`. Only verified closeout metadata may
differ; any implementation, behavior, scope, or contract delta Returns to
Review. Require index-tree equality, run `git diff --cached --check`, commit
once, and require `HEAD^{tree}` to equal the lock tree.

For a connector-backed tracker, add the commit SHA, apply repo-policy closeout
after Lock, and refetch every intended field. Partial or failed read-back
Returns blocked with applied, failed, and safest recovery actions.

## Return

Return exactly one:

| Result | Required Evidence |
| --- | --- |
| Setup precondition | Missing surface, state, `$repo-bootstrap`, no mutation |
| Selection gate | Checked target or candidates, failed gate, preserved tracker, exact question or `$to-tickets` repair |
| Assignment blocker | Missing worker authority and owner action |
| Staged handoff | Staged diff, proof, skips, risk, unrelated state, owner action |
| Decision required | Immutable target, complete choices, consequences, resume point |
| Blocked | Item, preserved work, blocker owner, release condition, resume operation |
| Complete | Item, commit and tree identity, review, proof, risk, tracker read-back, next boundary |

Complete only when the selected item is proved, the current review has no
admitted blocker, the approved tree is committed exactly once, and applicable
closeout reads back. A staged handoff is not implementation completion. Stop
before push, deployment, PR creation, parent closure, or another item without
separate authority.
