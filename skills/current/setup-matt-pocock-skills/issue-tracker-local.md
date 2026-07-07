# Issue tracker: Local Markdown

Issues and PRDs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The PRD is `.scratch/<feature-slug>/PRD.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage is recorded with `Category:` and `Status:` lines near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

Example triage header:

```markdown
Category: enhancement
Status: ready-for-agent
```

## When a skill says "publish to the issue tracker"

For a PRD, create `.scratch/<feature-slug>/PRD.md` (creating the directory if needed). For implementation issues, use `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `$wayfinder`. The **map** is one markdown file with child ticket files.

- **Map**: create `.scratch/<feature-slug>/wayfinder/map.md`. Its body holds Destination, Notes, Decisions So Far, Not Yet Specified, and Out Of Scope.
- **Child ticket**: create `.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md`. Put `Part of: map.md`, `Type: research | prototype | grilling | task`, `Status: Pending | In Progress | Resolved | Blocked | Out Of Scope`, and optional `Blocked by: <NN>, <NN>` lines near the top.
- **Blocking**: a ticket is unblocked when every ticket in `Blocked by` is `Resolved` or `Out Of Scope`.
- **Frontier query**: read open ticket headers, then drop tickets with an unresolved blocker or `Status: In Progress`. The first remaining ticket in map order is the frontier.
- **Claim**: set `Status: In Progress` before work.
- **Resolve**: record the answer in the ticket, set `Status: Resolved`, then append one context pointer to the map's Decisions So Far.

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment. Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
