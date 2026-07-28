# Conflict Operations

Load only the row for the observed operation and the relevant class rows for
in-scope conflicts. `SKILL.md` remains authority for scope, mutation, proof,
Return, and completion.

## Operation Roles

| Operation | Goal | Stage 1 / 2 / 3 | Native finish |
| --- | --- | --- | --- |
| Merge | Integrate histories | merge base / current target / merged side | `git merge --continue` |
| Rebase | Replay a commit onto the rebased target | replay base / so-far rebased target / commit being replayed | `git rebase --continue` |
| Cherry-pick | Apply one selected commit delta | selected parent or mainline / current target / selected commit | `git cherry-pick --continue` |
| Revert | Apply the inverse of one selected commit | selected commit / current target / selected parent or mainline | `git revert --continue` |
| Unmerged, unknown | Reconcile only from proven object and intent roles | inspect objects without assigning side labels | none |
| Marker-only | Repair proven residue outside an active operation | no authoritative index stages | none |

Never use bare `ours` or `theirs` as intent. Map the stage to its operation
role first.

## Conflict Classes

| Class | Required reconciliation and proof |
| --- | --- |
| Text or structured content | Inspect all stage objects and the complete candidate; prove syntax, behavior, and applicable contracts. |
| Add, delete, rename, or path topology | Prove intended presence, name, imports, registrations, packaging, and deletion or compatibility obligations. |
| Binary, executable mode, or symlink | Compare object identity and modes; select or construct only from traced intent, then verify the resulting artifact and mode. |
| Generated or filtered artifact | Resolve the authoritative source and regenerate through the repository command when available; do not silently hand-edit derived output. |
| Submodule gitlink | Inspect referenced commits and superproject intent; prove the selected gitlink is available and compatible. |
| Plausible marker-only text | Distinguish residue from intentional fixtures, docs, or literals; repair only proven residue and leave Git finishing to the caller. |

Use **Compose** when both intents coexist, **Transform** when preserving both
requires an adapted result, **Prefer** when authority proves one incompatible
intent wins, and `decision required` when it does not.

## Finish Checks

Before native continuation:

- refresh State and require every unmerged path accounted for;
- stage only exact authorized resolution paths with status-appropriate commands;
- require `git ls-files -u` to be empty;
- inspect the complete staged delta, including deletions, renames, modes, and
  submodule entries;
- prove no unrelated index state was admitted and that the staged
  representation matches the proved candidate.

After continuation, refresh. New conflicts return to **State**. Operation exit
requires final status read-back and any proof invalidated or required by the
resulting tree.

## Recovery Decisions

Abort, skip, quit, reset, whole-side selection, strategy replacement, todo or
message-policy change, hook bypass, and allow-empty handling are separate
decisions. Do not infer any of them from reconciliation or finish authority.
Return the exact state, consequence, and authority needed.
