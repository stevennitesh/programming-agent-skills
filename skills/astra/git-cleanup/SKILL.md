---
name: git-cleanup
description: Assess and clean branches or worktrees, including retained-work integration when requested. Exclude routine commits, pushes, and active conflict resolution.
---

# Git cleanup

Reconcile the requested branches and worktrees while preserving useful work and
active ownership. Finish with evidence for what was retained, integrated, or
removed and the resulting repository state. Choose the inspection, comparison,
integration, and cleanup methods appropriate to the repository and host.

An assessment-only request stays read-only. For authorized cleanup or integration,
carry the work through without asking again for effects already covered. Cleanup
does not by itself authorize discarding unique work or rewriting shared history.
Retain uncertain candidates while completing independent, supported cleanup.

## Establish the actual state

Identify the repository, intended remotes and target branch, local and remote
candidate tips, PR identities where relevant, and associated worktrees. Do not
assume the default branch's name or that a remote-tracking ref is current. Refresh
state through the available read-only remote surface for a read-only assessment;
fetch when mutations are authorized. State freshness limits when verification is
unavailable.

Inspect staged, unstaged, untracked, and relevant ignored contents before removing
a checkout. Establish whether another task, process, or person still owns writes
there. Preserve active checkouts, local-only work not otherwise retained, required
data, and unresolved Git operations. Honor explicit requirements to retain commit
history even when its content is integrated elsewhere. A clean tracked status
does not establish that a worktree is disposable. Do not stash, reset, or commit
unrelated work to make cleanup possible.

## Decide what each candidate needs

Establish whether its work is already integrated, superseded, still useful, or
uncertain. Branch age, a missing upstream, and a closed or absent PR do not prove
disposability. Bind conclusions to the observed candidate and destination tips.

When ancestry is inconclusive, histories were rewritten, or a branch has distinct
changes whose disposition is unclear, read
[Integration evidence](references/integration-evidence.md).

If the user requests integration of worthwhile work, assess its actual changes
against current requirements and the target code before selecting what to retain.
Use [change-review](../change-review/SKILL.md) for candidate assessment and
[codebase-design](../codebase-design/SKILL.md) when reuse or ownership remains
unresolved. Do not replay every old commit merely because it is unmerged.

Integrate accepted work within the requested scope and repository policy, then
verify the combined result with checks appropriate to its affected behavior.
Use [resolving-merge-conflicts](../resolving-merge-conflicts/SKILL.md) if an active
operation conflicts. Confirm the accepted result is retained at the intended
destination before retiring its source.

## Apply supported cleanup

Recheck candidate identity, preservation requirements, and write ownership before
removal. Use conditional ref deletion tied to the exact observed object ID where
available; never replace a failed guard with an unconditional force operation.
If a ref moved, reassess that candidate. When a surface cannot guard the mutation,
establish exclusive control or retain the candidate rather than assume no race.

Remove or archive managed worktrees through their lifecycle owner. For
parallel-implement lanes, preserve that workflow's integration and cleanup
contract. Confirm the exact checkout path and disposition of nontracked contents;
do not assume an archive includes ignored data. Release worktrees safely before
deleting their checked-out branches, and preserve primary or shared checkouts.

When synchronization is requested, update the intended local branch to the
verified remote state without discarding local commits or unrelated changes.
A diverged branch requires reconciliation within scope, not a reset for cosmetic
equality. Publication, PR closure, and history rewriting require their own existing
authority; branch deletion alone does not establish those effects.

## Verify the endpoint

Read back affected local and remote refs, worktree registrations, relevant PR
state, and working-tree status. Confirm requested synchronization by actual commit
identity and divergence. Distinguish remote changes from local-only results and
unverified remote state. After an uncertain operation, inspect what happened
before retrying.

Report completed integration and removals, retained candidates with material
reasons, preservation or synchronization limits, and decisive verification. Keep
the report proportional to the request; no permanent inventory is required.
