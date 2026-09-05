---
name: resolving-merge-conflicts
description: Inspect or resolve conflicts in an active Git merge, rebase, cherry-pick, revert, or unmerged index. Use for conflicting integration intent and safe operation completion; exclude planning a new integration, ordinary diff review, and bugs after a completed integration without unresolved Git state.
---

# Resolving merge conflicts

Recover the intended combined behavior, preserve unrelated work, and finish at
the requested Git endpoint. Removing markers alone does not resolve a conflict.

## Establish the operation and authority

Inspect the worktree identity, status, operation metadata, and unmerged index
(`git ls-files -u`). Use Git-resolved metadata paths in linked worktrees; do not
assume `.git` is a directory. Record the relevant commits, conflicted paths, and
existing staged, unstaged, and untracked work before changing anything.

A status, explanation, or review request is read-only. A request to finish the
operation, or an already authorized integration task, carries its ordinary
staging and native continuation steps within repository policy; do not ask again
at every conflict. A resolve-only request does not by itself authorize creating
commits. Respect an explicit endpoint such as leaving resolutions unstaged.

If neither an active operation nor unmerged entries remain, report the observed
state instead of starting an integration. Prepared resolutions may already be
staged: an active operation can still need review and continuation without
unmerged entries. Coordinate with any existing integration owner before mutation;
do not resolve the same worktree concurrently. Reinspect after another writer or
unexpected state change; previous observations no longer justify the next step.

## Reconcile intent

Read the applicable operation row and any present special conflict types in
[Operation details](references/operations.md). Map objects to their actual roles
before using side-selection commands. Stages or marker labels are not intent.

Compare the base and both changes, then trace the commits' purpose through the
affected callers, contracts, tests, and available issue or PR context. Retrieve
only missing decision context; do not make remote research a prerequisite when
local evidence is sufficient. Preserve compatible intent from both changes. If
they conflict semantically, use the governing requirement; ask its owner only
when a consequential choice remains unresolved. Do not invent a third feature
to make the text merge cleanly.

Resolve the whole affected behavior, including automatically merged neighboring
code when one side changes a contract used by the other. Update traced dependent
paths needed for that resolution within scope. Whole-side selection is justified
only when the other change is obsolete or its intent is preserved elsewhere.
Inspect the final path topology, content, and modes, not just marker locations.

## Prove the combined result

Review the resolved delta and run repository-required checks plus the nearest
useful behavior check. For a changed seam, exercise the actual caller with the
combined producer and consumer. Existing branch tests may each pass while the
combination breaks. Fix in-scope integration defects; distinguish unavailable
checks and unrelated failures from evidence that the resolution works.

Treat automatic resolutions, including staged `rerere` results, as candidates to
inspect. Check for unresolved entries and accidental conflict artifacts without
mistaking intentional marker-like text for Git state. Bind proof to the content
and integration base checked. If continuation changes relevant content or base,
refresh affected proof; do not reuse an old green result as final verification.

## Complete the requested endpoint

When staging is authorized, stage exact resolved paths or hunks, including intended
deletions. Do not use blanket staging. Preserve unrelated changes even when they
share a file with the resolution. Before continuation, inspect the entire staged
delta: distinguish legitimate automatically merged changes from unrelated staged
work. Do not silently commit, unstage, or stash unrelated work to get past it.

When continuation is authorized, require an empty unmerged index and use the
observed operation's native continuation. Preserve its selected commits, mainline,
messages, and policy. Follow subsequent conflicts through the same loop until
the requested operation ends or a concrete decision or execution blocker remains.
Do not substitute a plain commit for a replay operation's continuation.

For an empty replay, editor/hook/signing failure, or recovery choice, read the
exception guidance in [Operation details](references/operations.md). Do not skip
work or bypass policy merely to make Git finish.

Inspect final status and operation metadata after continuation, including restored
local work. Report whether resolutions are prepared or the operation is complete,
notable intent choices or tradeoffs, the resulting revision when applicable,
checks performed, and any remaining
conflict or blocker. A successful command or vanished operation marker alone is
not evidence of a clean result. Leave unrelated dirt intact; cleanliness is not
a reason to delete someone else's work.
