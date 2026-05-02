---
name: github-work-tracking
description: Use when the user wants GitHub CLI issue tracking, PRDs, implementation issues, triage, PR creation, PR updates, or durable change/request tracking with gh.
---

# GitHub Work Tracking

Use GitHub as lightweight shared memory for intent, scope, decisions, and PR evidence. Do not turn tiny edits into ticket process.

## When To Track

Track in GitHub when work is:

- Multi-session or resumed later
- Shared with other people or agents
- User-facing, product-significant, or risky
- Needs acceptance criteria, open questions, or a decision record
- Split into slices, blocked by other work, or linked to a PR
- A cleanup candidate the user may schedule later

Skip GitHub tracking for tiny obvious edits unless requested.

## Baseline

Before creating or editing GitHub records:

1. Confirm the repo has a GitHub remote.
2. Check `gh auth status` if auth is uncertain.
3. Read existing issue, label, and PR conventions when present.
4. Search for a duplicate or parent issue first.
5. Read `CONTEXT.md` when it exists so issues use shared vocabulary.
6. Preserve the current working tree.

If GitHub state affects the answer, inspect it live with `gh`; do not rely on memory.

## PRD Issue Shape

Use for a feature, product behavior, or multi-slice change.

```markdown
## Problem

## Current behavior

## Goal

## Non-goals

## Proposed behavior

## Acceptance criteria
- [ ] ...

## Risks / open questions

## Implementation notes
```

Keep implementation notes durable: interfaces, constraints, prior decisions, and likely entry points. Avoid line numbers, stale file maps, code dumps, and implementation steps.

Use `CONTEXT.md` terms in PRDs and slice issues when they clarify intent. Do not copy progress, implementation status, or skill summaries into `CONTEXT.md`.

Create with `gh issue create --title "<title>" --body-file <file>`.

Use `.tmp/` for temporary body files.

## Slice Issues

Break approved plans into small vertical slices:

```markdown
## Parent

## What to build

## Current behavior

## Desired behavior

## Key contracts
- Caller-visible interfaces, types, commands, config, or workflows that matter

## Acceptance criteria
- [ ] ...

## Blocked by
None | #123

## Verification

## Out of scope
```

Each slice should be independently understandable and verifiable. Prefer body text over custom labels unless the repo already uses them.

Write durable issue bodies: describe behavior and contracts, not line numbers, stale file paths, or step-by-step implementation instructions.

Mark readiness plainly:

- `Agent-ready`: implementable without a new human decision
- `Needs decision`: blocked on human, product, architecture, access, or manual review

For blocked issues, record:

```markdown
## Established so far
- ...

## Still needed
- Specific decision, artifact, access, or manual review needed
```

## PR Flow

- Link PRs to issues in the body with the repo's preferred format, such as `Closes #123`.
- Include summary, checks run, and residual risk.
- Use draft PRs when the work is intentionally not ready.
- Do not claim CI status without checking it with `gh pr checks`, `gh run`, or the GitHub UI.
- Update or comment on the issue when scope, acceptance, or blockers change.

Useful commands:

```bash
gh issue list
gh issue view <number>
gh issue create --title "<title>" --body-file .tmp/<file>.md
gh issue comment <number> --body-file .tmp/<file>.md
gh pr create --title "<title>" --body-file .tmp/<file>.md
gh pr status
gh pr checks
```

## Handoff

Use `clarify-scope` before writing a PRD when target behavior is unclear. Use `thin-plan` to turn an approved PRD or request into slice issues. Use `workspace-safety` before commits, branch changes, or PR creation from a dirty tree. Use `verify-before-done` before claiming PR readiness, CI status, or merge safety.
