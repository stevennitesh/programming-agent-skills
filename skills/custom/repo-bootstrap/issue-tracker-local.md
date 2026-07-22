# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`. This directory is durable, version-controlled tracker state.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The parent spec is `.scratch/<feature-slug>/SPEC.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage is recorded with `Category:` and `Status:` lines near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

Example triage header:

```markdown
Category: enhancement
Status: ready-for-agent
```

## When a skill says "publish to the issue tracker"

For a parent spec, create `.scratch/<feature-slug>/SPEC.md` (creating the directory if needed). For implementation issues, use `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`, `$parallel-implement`, and `$review`.

**Implemented items remain as tracked files.**

- **Packet**: `SPEC.md`, issue bodies, `## Comments`, and `## Implementation Notes` are the durable packet. Approved implementation issues use `Status: ready-for-agent` and one category role when the source settles it.
- **Ready-for-agent contract**: every ready item names one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. `$triage` owns incoming classification and verification; `$to-tickets` owns slicing and dependency order. Both produce this contract.
- **Parent / child**: `SPEC.md` is the parent. Its ordered issue list links each file, and every issue records `Parent: ../SPEC.md`.
- **Blocking**: put `Blocked by: <NN>, <NN>` near the top of an issue. Normally a work item is unblocked when every listed issue has `Status: implemented`. During one recorded `$parallel-implement` campaign, a blocker with an accepted landing that remains in current integration history with valid proof is derived as `landed-awaiting-lock`; it satisfies execution readiness only for in-scope dependents in that campaign. The recorded dependency remains until Lock. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.
- **Ready query**: list issues with `Status: ready-for-agent`, then drop issues with an unresolved blocker or `Claimed by`. Treat a recorded blocker as resolved only when the verified same-campaign `landed-awaiting-lock` overlay above applies. Preserve the order in `SPEC.md`; without a parent order, choose the lowest issue number.
- **Claim**: add `Claimed by: <driver/session>` before implementation dispatch; keep the state role unchanged.
- **Release**: remove `Claimed by` when work blocks, is abandoned, or reaches closeout.
- **Closeout**: after acceptable review and before Lock, append the final closeout packet under `## Implementation Notes`, set `Status: implemented`, remove the claim, stage the tracker file with the selected-work diff, and apply **Mutation read-back**.
- **Mutation read-back**: after creating or changing tracker files, reread the changed files and every affected dependent file; verify the intended file bodies, relationships, state, claims, comments, closeout metadata, and resulting ready frontier. A partial mutation is blocked; report applied operations, failed operations, and the safest recovery action.

## Wayfinding operations

Used by `$wayfinder`. The **map** is one markdown file with child ticket files.

- **Map**: create `.scratch/<feature-slug>/wayfinder/map.md`. Put `Status: Open | Complete` near the top and follow the invoking Wayfinder's `MAP-FORMAT.md` contract.
- **Child ticket**: create `.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md`. Put `Part of: map.md`, `Type: research | prototype | grilling | task`, `Participation: HITL | AFK`, and `Status: Pending | In Progress | Resolved | Blocked | Out Of Scope` near the top. Add `Claimed by: codex`, `Claim token: codex/<lowercase UUIDv4>`, and `Claimed at: <YYYY-MM-DDTHH:MM:SSZ>` only while claimed; add `Blocked by: <NN>, <NN>` only when blocked by sharp tickets.
- **Blocking**: a ticket is unblocked when every ticket in `Blocked by` is `Resolved` or `Out Of Scope`. When the last blocker clears, change `Status: Blocked` to `Status: Pending`.
- **Frontier query**: list tickets with `Status: Pending`, then drop tickets with an unresolved blocker or active `Claim token:`. The remaining tickets in map order are the frontier; the first is the default selection.
- **Claim**: Advance claims the selected ticket; Maintain claims the map. Put `Claimed by: codex`, `Claim token: codex/<lowercase UUIDv4>`, and `Claimed at: <YYYY-MM-DDTHH:MM:SSZ>` on the claimed item; also set a claimed ticket to `Status: In Progress`. Generate one fresh UUIDv4 per Wayfinder invocation, reuse it for every claim in that invocation, and never reuse it across invocations. Read back the exact token and timestamp; a different token owns the item even when the driver is the same.
- **Release**: remove `Claimed by`, `Claim token:`, and `Claimed at:` when active work ends.
- **Stale claim**: Elapsed time alone never makes a claim stale. Replace a different token only after explicit user approval; first record the prior token, claimed-at value, and takeover reason under `## Comments`, then apply Mutation read-back to the replacement claim.
- **Resolve**: record the answer, set `Status: Resolved`, release the claim, then append one context pointer to the map's Decisions So Far.
- **Block**: record the blocker, set `Status: Blocked`, add `Blocked by` when the blocker is sharp or return it to map fog, then release the claim.
- **Out of scope**: record the reason, set `Status: Out Of Scope`, release the claim, then append one linked note to the map's Out Of Scope section.
- **Complete map**: after the map's closing conditions hold, record the destination and next route, set the map to `Status: Complete`, read back the completed state, release any map claim, then read back the claim's absence.

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment. Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
