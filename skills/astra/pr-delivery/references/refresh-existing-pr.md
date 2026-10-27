# Refresh an existing PR

Read when asked to rebase, modernize, or bring an existing PR up to date. Assess
whether its goal and implementation remain appropriate before replaying commits.
A conflict-free rebase alone does not establish that the change should land.

## Establish intent and change since divergence

Identify the actual PR repository, author, base, head repository and branch,
observed head, checks, and review state. Read enough of its description, linked
requirements, commits, feedback, and complete diff to establish the smallest
coherent goal. Inspect dirty work and write ownership before using a checkout;
isolate the refresh when another task owns it.

For an assessment-only request, use available read-only remote evidence. For an
authorized refresh, fetch the intended base and PR head and preserve their
identities plus the common base. Compare the original change separately from
what landed on the base since divergence. Inspect related open or merged changes
when the code or requirements suggest a replacement or competing implementation.

Look beyond overlapping lines: the problem may already be solved; APIs, schemas,
dependencies, or invariant ownership may have changed; deleted behavior may have
been deliberately retired. Check that landing the old work would not restore an
obsolete behavior or create a competing owner. Age and sunk effort do not decide
whether the work remains useful.

## Choose and carry the supported disposition

- **Refresh:** the goal remains useful and the approach still fits. Perform the
  authorized base update, resolve conflicts, and verify the combined result.
- **Rework:** the goal remains useful but a mechanical replay would retain the
  wrong design. Identify the smallest suitable change and continue if the user's
  existing scope covers it. Otherwise preserve the candidate and surface the
  consequential scope or design decision before dependent mutation.
- **Recommend retirement:** concrete evidence shows the work is superseded,
  obsolete, or no longer justified. Explain that evidence without rebasing merely
  to produce activity. A recommendation does not itself authorize closing the PR
  or removing its branch.

Use [codebase-design](../../codebase-design/SKILL.md) for an unresolved ownership
or integration choice. [Git cleanup](../../git-cleanup/SKILL.md) owns requested
branch and worktree disposition; a PR refresh does not initiate cleanup.

For a refresh, preserve a recoverable pre-update tip. Use the repository's
authorized merge or rebase method and the actual base, rather than assuming the
default branch. Active conflicts belong to
[resolving-merge-conflicts](../../resolving-merge-conflicts/SKILL.md).

Inspect the resulting diff and compare the pre- and post-rebase series with
`git range-diff` when applicable. Confirm intended behavior survived and already
landed or deliberately retired behavior was not reintroduced. Verify affected
combined workflows; old checks on either side alone do not prove integration.

Publish only within existing authority. If an authorized rebase requires history
rewriting, use a lease tied to the previously observed remote head. A failed lease
requires refreshing and reassessing the new work, never an unconditional force
push. Do not infer rewrite authority from a read-only modernization assessment.

Return the disposition, meaningful base changes, resulting candidate and update
status, verification, and remaining decision. A requested delivery continuation
resumes the main skill's current-head checks and review; refresh alone authorizes
neither merge nor closure.
