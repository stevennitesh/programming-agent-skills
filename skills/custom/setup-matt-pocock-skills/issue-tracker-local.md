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
- **Parent / child**: `SPEC.md` is the parent. Its ordered issue list links each file, and every issue records `Parent: ../SPEC.md`.
- **Blocking**: put `Blocked by: <NN>, <NN>` near the top of an issue. A work item is unblocked when every listed issue has `Status: implemented`.
- **Ready query**: list issues with `Status: ready-for-agent`, then drop issues with an unresolved blocker or `Claimed by`. Preserve the order in `SPEC.md`; without a parent order, choose the lowest issue number.
- **Claim**: add `Claimed by: <driver/session>` before implementation dispatch; keep the state role unchanged.
- **Release**: remove `Claimed by` when work blocks, is abandoned, or reaches closeout.
- **Closeout**: before final review, append the closeout packet under `## Implementation Notes`, set `Status: implemented`, remove the prior state value and claim, and stage the tracker file with the implementation diff.

## Wayfinding operations

Used by `$wayfinder`. The **map** is one markdown file with child ticket files.

- **Map**: create `.scratch/<feature-slug>/wayfinder/map.md`. Put `Status: Open | Complete` near the top. Its body holds Destination, Notes, Decisions So Far, Not Yet Specified, and Out Of Scope.
- **Child ticket**: create `.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md`. Put `Part of: map.md`, `Type: research | prototype | grilling | task`, `Participation: HITL | AFK`, `Status: Pending | In Progress | Resolved | Blocked | Out Of Scope`, optional `Claimed by: <driver/session>`, and optional `Blocked by: <NN>, <NN>` lines near the top.
- **Blocking**: a ticket is unblocked when every ticket in `Blocked by` is `Resolved` or `Out Of Scope`. When the last blocker clears, change `Status: Blocked` to `Status: Pending`.
- **Frontier query**: list tickets with `Status: Pending`, then drop tickets with an unresolved blocker. The first remaining ticket in map order is the frontier.
- **Claim**: set `Status: In Progress` and `Claimed by: <driver/session>` before work; those fields are the concurrency guard.
- **Release**: remove `Claimed by` when active work ends.
- **Resolve**: record the answer, set `Status: Resolved`, release the claim, then append one context pointer to the map's Decisions So Far.
- **Block**: record the blocker, set `Status: Blocked`, add `Blocked by` when the blocker is sharp or return it to map fog, then release the claim.
- **Out of scope**: record the reason, set `Status: Out Of Scope`, release the claim, then append one linked note to the map's Out Of Scope section.
- **Complete map**: after the map's closing conditions hold, record the destination and next route, then set the map to `Status: Complete`.

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment. Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
