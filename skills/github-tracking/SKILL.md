---
name: github-tracking
description: Use when repo work needs GitHub issues, PRDs, implementation slices, triage, PR creation or updates, CI/check evidence, review-thread tracking, or durable request tracking through gh, GitHub connectors, or app tools.
---

# GitHub Tracking

Use GitHub records to preserve coding intent, source scope, caller-visible contracts, decisions, blockers, verification evidence, and PR review state. Do not turn tiny local edits into issue process.

## When To Track

Track in GitHub when work is:

- Multi-session or resumed later
- Shared with humans, coding agents, reviewers, or CI
- Changes user- or caller-visible behavior, public contracts, data/state, migrations, or release risk
- Needs acceptance checks, open questions, architecture decisions, or rollback notes
- Split into implementation slices, blocked by another source change, or linked to a PR/check run/review thread
- A cleanup or refactor candidate the user may schedule later

Skip GitHub tracking for tiny obvious edits unless requested.

## Baseline

Before creating or editing GitHub records:

1. Confirm the repo has a GitHub remote and identify the target owner/repo, base branch, and current head branch when relevant.
2. Check `gh auth status` or connector/app authorization if auth is uncertain.
3. Read existing issue, label, and PR conventions when present.
4. Inspect linked issues, PRs, review threads, CI/check runs, and repo notes when they are part of the request.
5. Search for a duplicate or parent issue first.
6. Read `CONTEXT.md` only for shared terms, module boundaries, and public contract names that should appear in durable GitHub records.
7. Preserve the current working tree and record the head SHA when PR or CI state matters.

If GitHub state affects the answer, inspect it live with the available GitHub interface; do not rely on memory. Use `gh` when it is the repo's working interface, or GitHub connector/app tools when they are available. Preserve the same evidence rules either way: check live state, search for duplicates, follow repo conventions, and keep issue or PR bodies as durable repo artifacts rather than chat transcripts.

## GitHub Metadata

Issue bodies and comments are the portable source of truth.
Use sidebar metadata when it improves coding coordination, filtering, dependency tracking, release planning, branch/PR traceability, or durable documentation.

Follow existing repo conventions first. Do not invent label, project, milestone, assignee, or branch-link systems for tiny work.

Required when useful:

- Assignees: active owner or stable agent identity matters.
- Labels: filtering, readiness, blocking state, issue type, or execution mode matters.
- Projects: the repo or team already uses GitHub Projects for multi-issue work.
- Milestones: release, migration, version, or scheduled checkpoint matters.
- Relationships: parent/child, dependency, duplicate, or blocked-by tracking matters.
- Development: branch or PR exists for implementation.

Usually optional:

- Notifications
- Participants

Human-approved only:

- Transfer issue
- Duplicate issue
- Lock conversation
- Pin issue
- Delete issue

Keep claim and status comments even when assignees, labels, relationships, or Development links are used.
Metadata is a structured signal; it does not replace the technical record.

## PRD Issue Shape

Use for a feature, user-facing behavior, or multi-slice change.

```markdown
## Problem

## Current behavior

## Goal

## Non-goals

## Proposed behavior

## Public / caller contracts

## Acceptance criteria
- [ ] ...

## Verification

## Risks / open questions

## Engineering notes
```

Keep engineering notes durable: source entry points, caller contracts, constraints, data/state touched, migration or compatibility notes, likely tests or commands, and prior decisions. Avoid line numbers, stale file maps, code dumps, and step-by-step implementation instructions.

Use `CONTEXT.md` terms in PRDs and slice issues when they clarify intent. Never copy progress, status, or skill summaries into `CONTEXT.md`.

Create with `gh issue create --title "<title>" --body-file <file>` or the equivalent connector/app issue action.

Use `.tmp/` for temporary body files.

## Slice Issues

Break approved plans into small vertical slices:

```markdown
## Parent

## What to change

## Current behavior

## Desired behavior

## Affected entry points/modules

## Key contracts
- Caller-visible interfaces, types, commands, config, or workflows that matter

## Acceptance criteria
- [ ] ...

## Verification command/check

## Blocked by
None | #123

## Execution coordination
Mode: sequential | parallel-disjoint | parallel-overlap
Parallel group: None | <group-name>
Depends on: None | #123
Expected overlap: None | files/modules/contracts/generated/dependency-config
Worktree required: no | yes
Claim protocol: comment before starting; update on pause/completion

## Out of scope
```

Each slice should be independently understandable and verifiable. Prefer body text over custom labels unless the repo already uses them.

Write durable issue bodies: describe caller-visible behavior, source scope, contracts, acceptance checks, and verification. Do not anchor the issue on line numbers, stale file paths, code dumps, or step-by-step implementation instructions.

If the source plan does not declare an execution mode, write `Mode: sequential` and `Worktree required: no`.

Use parallel modes only when the plan already supports them:

- `parallel-disjoint`: ownership is separated for concurrent implementation.
- `parallel-overlap`: the overlap and integration owner are named.

Mark readiness plainly:

- `Agent-ready`: implementable from the issue and repo evidence without a new human decision
- `Needs decision`: blocked on user/caller behavior, architecture, security/data, access, dependency, or manual review

For blocked issues, record:

```markdown
## Established so far
- ...

## Still needed
- Specific decision, artifact, source/API contract, access, dependency, or manual review needed
```

## Issue Claiming

Before editing for an implementation issue, inspect the issue body, comments, assignees, labels, linked PRs, and recent activity. Then comment:

```markdown
Claiming this issue for implementation.

Agent/session: <identifier if available>
Branch/worktree: <branch or path if relevant>
Scope: <short source/test/docs scope>
Started: <timestamp>
Expected next update: <checkpoint or condition>
```

Use comments as the portable baseline. Add labels or assignees only when the repo already uses them for ownership.

Collision rules:

- `sequential`: if a fresh claim exists and is not released, do not start unless the user directs a takeover or the claim is clearly stale.
- `parallel-disjoint`: work only on the issue's declared ownership scope; if another claim overlaps the same files, modules, contracts, generated output, or dependency/config state, stop or coordinate first.
- `parallel-overlap`: use the named worktree and integration strategy before editing; do not improvise a merge plan from comments alone.

When pausing, completing, blocking, or releasing the issue, comment:

```markdown
Status update.

State: paused | completed | blocked | released
Changed files:
Checks:
Commit/branch/PR:
Open risks:
Next action:
```

## PR Flow

- Link PRs to issues in the body with the repo's preferred format, such as `Closes #123`.
- Include source/test/config/docs/workflow changes, checks run, CI/check status when known, and residual risk.
- Use draft PRs when the source change, review response, or verification evidence is intentionally not ready.
- Do not claim CI status without checking the latest head SHA with `gh pr checks`, `gh run`, the GitHub UI, or connector/app PR status.
- Update or comment on the issue when public contracts, scope, acceptance checks, blockers, verification evidence, or reviewer requests change.
- Resolve or mark review threads only after the code, tests, docs, or explicit technical response addresses the current comment.

## Review Feedback Flow

Use this when addressing PR comments, requested changes, review threads, or CI feedback:

1. Read the full review context: PR body, linked issue or PRD, changed files, comments, unresolved threads, requested changes, and latest CI/check state.
2. Group feedback into blockers, correctness/test issues, questions, small cleanup, and possible pushback.
3. Verify each item against current source, tests, docs, public/caller contracts, and accepted scope before changing code.
4. If an item is unclear and related to other requested changes, clarify before implementing a partial subset.
5. Implement one item or tightly related group at a time, then run the narrowest relevant check.
6. Reply or update the PR with the technical outcome: changed files or behavior, check evidence, unresolved risk, or reasoned pushback.
7. Leave threads unresolved until the code, docs, tests, or explicit technical response addresses the current comment.

Push back when feedback is stale, technically incorrect, unsafe, conflicts with the approved scope, or adds unsupported behavior. Do not reply with empty agreement; make the evidence or decision clear.

Useful `gh` commands when the CLI is the active GitHub interface:

```bash
gh issue list
gh issue view <number>
gh issue create --title "<title>" --body-file .tmp/<file>.md
gh issue comment <number> --body-file .tmp/<file>.md
gh pr create --title "<title>" --body-file .tmp/<file>.md
gh pr status
gh pr view <number>
gh pr diff <number>
gh pr checks <number>
gh run view <run-id>
```

## Handoff

- `clarify-scope`: before writing a PRD when target behavior, public contract, or affected source boundary is unclear.
- `slice-plan`: turn an approved PRD or request into implementation slice issues.
- `issue-driven-execution`: the user wants a plan doc, GitHub issues, and issue-by-issue implementation checkpoints.
- `workspace-safety`: before commits, branch changes, or PR creation from a dirty tree.
- `verify-before-done`: before claiming PR readiness, CI status, review resolution, or merge safety.
