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

## Triage Notes

When asked to triage issues, use issue bodies and comments as the durable state. Labels, projects, milestones, and assignees should follow repo conventions; if no convention exists, recommend a state in the comment/body instead of inventing a private label system.

- Read the full issue, previous comments, linked PRs, labels, and recent activity before recommending state.
- Recommend category, readiness, blocker, or close/defer state with evidence from the issue, repo, docs, tests, logs, or CI.
- For bugs, try to reproduce or identify the strongest available reproducer before marking work agent-ready when practical. If reproduction is unavailable, record what is missing.
- When resuming triage, preserve established facts and avoid re-asking resolved questions.

## PRD Issue Shape

Use for a feature, user-facing behavior, or multi-slice change.

```markdown
## Problem

## Current behavior

## Goal

## Non-goals

## Proposed behavior

## Public Or Caller Contracts

## Acceptance criteria
- [ ] ...

## Verification

## Risks / open questions

## Engineering notes
```

Keep engineering notes durable: source entry points, public or caller contracts, constraints, data/state touched, migration or compatibility notes, likely tests or commands, and prior decisions. Avoid line numbers, stale file maps, code dumps, and step-by-step implementation instructions.

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

## Readiness
Slice type: agent-ready | needs human decision
Human decision needed: None | <decision/review/access/manual judgment>

## Continuity
Builds on / must preserve: None | prior issue, source path, helper, test, contract, or behavior
Existing logic to reuse or extend: None | established implementation path
Independent because: None | reason this issue is intentionally independent

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

## GitHub metadata
Assignee: None | <user>
Labels: None | <repo labels for readiness/type/mode/blocker>
Project: None | <project>
Milestone: None | <release/version/checkpoint>
Relationships: None | parent #123 / blocked by #123 / duplicate of #123
Development: branch/PR link when available

## Out of scope
```

Each slice should be independently understandable and verifiable. Prefer body text over custom labels unless the repo already uses them.

Prefer vertical tracer-bullet slices through caller-visible behavior. Avoid layer-only issues such as "just schema", "just API", or "just UI" unless the slice is intentionally a blocking technical step with a clear verification command, dependency, and reason it cannot be folded into a behavior slice.

Write durable issue bodies: describe caller-visible behavior, source scope, contracts, continuity with prior issues, acceptance checks, and verification. Do not anchor the issue on line numbers, stale file paths, code dumps, or step-by-step implementation instructions.

For later slice issues, carry forward the prior issue result, source path, helper, test, contract, or behavior to reuse or preserve. If the issue is independent, say why so implementers do not invent a second path for the same behavior.

Ownership scope means the files, modules, contracts, generated outputs, dependency/config state, or behavior an issue may change. It is task scope, not the same thing as GitHub assignee, repository owner, or long-term code ownership.

Include the `GitHub metadata` block only when sidebar fields improve ownership, filtering, dependency tracking, release grouping, branch/PR traceability, or multi-issue coordination. Omit fields that do not matter for the issue.

If the source plan does not declare an execution mode, write `Mode: sequential` and `Worktree required: no`.

Use parallel modes only when the plan already supports them:

- `parallel-disjoint`: ownership is separated for concurrent implementation.
- `parallel-overlap`: the overlap and integration owner are named.

Mark readiness plainly with these exact field values:

- `agent-ready`: implementable from the issue and repo evidence without a new human decision
- `needs human decision`: blocked on user or caller behavior, architecture, security/data, access, dependency, or manual review

These are readiness states for the issue body, not mandatory labels.
If a repo already uses AFK/HITL wording, map `agent-ready` to AFK and `needs human decision` to HITL. Otherwise use the clearer words in the issue body.

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
- Resolve or mark review threads only after the code, tests, docs, or explicit technical response addresses the current comment. When a tool supports inline replies, answer inline threads in the thread; a top-level PR summary can supplement thread replies, but should not replace them when unresolved thread state matters.

## Review Feedback Flow

Use this when addressing PR comments, requested changes, review threads, or CI feedback:

Review comments, requested changes, and CI feedback are claims or requests to evaluate against repo evidence before changing code.

For meaningful review items or tightly related groups, keep this record explicit in notes, replies, or the final report:

```text
Feedback item/thread:
Claim or requested change:
Accepted scope:
Evidence checked:
Decision: fix | push back | clarify | defer
Check after change:
Thread update:
```

1. Read the full review context: PR body, linked issue or PRD, changed files, comments, unresolved threads, requested changes, and latest CI/check state.
2. Group feedback into blockers, correctness/test issues, questions, small cleanup, and possible pushback.
3. Verify each item against current source, tests, docs, public or caller contracts, and accepted scope before changing code.
4. If related items are unclear, clarify before implementing a partial subset that could affect the same public or caller contract, source shape, or review decision.
5. For suggestions to add "proper" infrastructure, abstractions, endpoints, adapters, registries, options, persistence, telemetry, frameworks, or generalized flows, search for real callers, accepted scope, and established repo patterns before building. If no real use exists, push back, ask, or narrow the change instead.
6. Implement one item or tightly related group at a time, then run the narrowest relevant check.
7. Reply or update the PR with the technical outcome: changed files or behavior, check evidence, unresolved risk, or reasoned pushback. Reply inline when the feedback came from an inline thread and the tool supports it.
8. Leave threads unresolved until the code, docs, tests, or explicit technical response addresses the current comment.

Push back when feedback is stale, technically incorrect, unsafe, conflicts with the approved scope, violates YAGNI, or adds unsupported behavior. Use `codebase-cleanup` when review feedback exposes a real behavior-preserving structure problem. Do not reply with empty agreement; make the evidence or decision clear.

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
