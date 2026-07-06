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

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment. Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
