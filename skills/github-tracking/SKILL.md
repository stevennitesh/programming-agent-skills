---
name: github-tracking
description: "Use when repo work needs durable GitHub records or live GitHub state: issues, PRDs, implementation slices, triage, PR creation or updates, CI/check evidence, review-thread tracking, or request tracking through gh, GitHub connectors, or app tools."
---

# GitHub Tracking

Use GitHub records to preserve coding intent, source scope, public or caller contracts, decisions, blockers, verification evidence, and PR review state. Do not turn ordinary local implementation or tiny edits into GitHub process.

When the user asks for issues, PRDs, implementation slices, PR creation or updates, CI/check evidence, review-thread tracking, or durable request tracking, first inspect the relevant live GitHub state and repo conventions before creating or editing records.

Before writing a GitHub record, account for target repo or object, linked issue/PR/check/review state, duplicate or parent issue search, accepted source scope, public or caller contract, acceptance checks, verification evidence, readiness or blocker state, and whether sidebar metadata is useful.

## When To Track

Track in GitHub when work is:

- Multi-session or resumed later
- Shared with humans, coding agents, reviewers, or CI
- Changes user- or caller-visible behavior, public or caller contract, data/state, migrations, or release risk
- Needs acceptance checks, open questions, architecture decisions, or rollback notes
- Split into implementation slices, blocked by another source change, or linked to a PR/check run/review thread
- A cleanup or refactor candidate the user may schedule later

Skip GitHub tracking for tiny obvious edits unless requested. If tracking is skipped, do the local repo work directly and do not create process artifacts to justify the skip.

## Baseline

Before creating or editing GitHub records:

1. Confirm the repo has a GitHub remote and identify the target owner/repo, base branch, and current head branch when relevant.
2. Check `gh auth status` or connector/app authorization if auth is uncertain.
3. Read existing issue, label, and PR conventions when present.
4. Inspect linked issues, PRs, review threads, CI/check runs, and repo notes when they are part of the request.
5. Search for a duplicate or parent issue first.
6. Read `CONTEXT.md` only for shared terms, module boundaries, and public or caller contract names that should appear in durable GitHub records.
7. Preserve the current working tree and record the head SHA when PR or CI state matters.

If GitHub state affects the answer, inspect it live with the available GitHub interface; do not rely on memory. Use `gh` when it is the repo's working interface, or GitHub connector/app tools when they are available. Preserve the same evidence rules either way: check live state, search for duplicates, follow repo conventions, and keep issue or PR bodies as durable repo artifacts rather than chat transcripts.

Do not write, update, close, label, claim, resolve, or mark ready from memory, stale summaries, or chat-only context when live GitHub state is cheap to inspect.

## Fast Path

Use for small GitHub requests.

1. Identify the target repo, issue, PR, check run, review thread, or branch.
2. Inspect the live object and relevant repo conventions.
3. Make the smallest requested read, write, comment, or update.
4. Report the object/link, live evidence used, action taken, and remaining blocker or uncertainty.

Do not create issues, labels, PRDs, projects, milestones, or process artifacts unless the user requested them or durable coordination needs them.

## GitHub Metadata

Issue bodies and comments are the portable source of truth.
Use sidebar metadata when it improves coding coordination, filtering, dependency tracking, release planning, branch/PR traceability, or durable documentation.

Follow existing repo conventions first. Do not invent label, project, milestone, assignee, relationship, or branch-link systems for tiny work. Use body text or comments when the repo has no established metadata convention.

Use sidebar metadata only when it matters:

- Assignees: active owner or stable agent identity matters.
- Labels: filtering, readiness, blocking state, issue type, or execution mode matters.
- Projects or milestones: multi-issue work, release grouping, migration, version, or scheduled checkpoint matters.
- Relationships or Development links: dependency, duplicate, blocked-by, parent/child, branch, or PR traceability matters.

Keep claim and status comments even when metadata is used. Metadata is a structured signal; it does not replace the technical record.

Transfer, duplicate, lock, pin, delete, close, or merge only with explicit approval when the action is irreversible or externally visible.

## Triage Notes

When asked to triage issues, use issue bodies and comments as the durable state. Labels, projects, milestones, and assignees should follow repo conventions; if no convention exists, recommend a state in the comment/body instead of inventing a private label system.

- Read the full issue, previous comments, linked PRs, labels, and recent activity before recommending state.
- Recommend category, readiness, blocker, or close/defer state with evidence from the issue, repo, docs, tests, logs, or CI.
- For bugs, try to reproduce or identify the strongest available reproducer before marking work agent-ready when practical. If reproduction is unavailable, record what is missing.
- When resuming triage, preserve established facts and avoid re-asking resolved questions.
- Do not mark `agent-ready` unless the issue has enough repo evidence, accepted scope, public or caller contract, and verification path for an implementer to start without a new human decision. Mark `needs human decision` when the missing behavior, architecture, security/data, access, dependency, or manual-review decision blocks safe execution.

## PRD Issue Shape

Use for a feature, user-facing behavior, or multi-slice change.

Default PRD fields:

- Problem
- Current behavior
- Goal
- Non-goals
- Proposed behavior
- Public or caller contracts
- Acceptance criteria
- Verification
- Risks / open questions
- Engineering notes

Keep engineering notes durable: source entry points, public or caller contracts, constraints, data/state touched, migration or compatibility notes, likely tests or commands, and prior decisions. Avoid line numbers, stale file maps, code dumps, and step-by-step implementation instructions.

Use repo-preferred issue creation tools. With `gh`, write the body to ignored `.tmp/` when available and create with `gh issue create --title "<title>" --body-file <file>`.

## Slice Issues

Break approved plans into small vertical slices.

Required fields:

- Parent or source request
- What to change
- Current behavior
- Desired behavior
- Affected entry points/modules
- Key public or caller contracts
- Readiness: `agent-ready` or `needs human decision`
- Acceptance criteria
- Verification command/check
- Blocked by
- Out of scope

Each slice should be independently understandable and verifiable. Prefer body text over custom labels unless the repo already uses them.

Prefer vertical tracer-bullet slices through caller-visible behavior. Avoid layer-only issues such as "just schema", "just API", or "just UI" unless the slice is intentionally a blocking technical step with a clear verification command, dependency, and reason it cannot be folded into a behavior slice.

Write durable issue bodies: describe caller-visible behavior, source scope, contracts, continuity with prior issues, acceptance checks, and verification. Do not anchor the issue on line numbers, stale file paths, code dumps, or step-by-step implementation instructions.

For later slice issues, carry forward the prior issue result, source path, helper, test, contract, or behavior to reuse or preserve. If the issue is independent, say why so implementers do not invent a second path for the same behavior.

Add coordination fields only for multi-issue, claimed, or parallel work:

- Mode: sequential | parallel-disjoint | parallel-overlap
- Depends on
- Expected overlap
- Worktree required
- Claim protocol

If the source plan does not declare an execution mode, use `sequential` and `Worktree required: no`. Use parallel modes only when the plan already supports them and route parallel worktree details to `worktree-isolation`.

Add metadata fields only when sidebar fields improve filtering, dependency tracking, release grouping, branch/PR traceability, or multi-issue coordination:

- Assignee
- Labels
- Project
- Milestone
- Relationships
- Development branch/PR

Mark readiness plainly with these exact field values:

- `agent-ready`: implementable from the issue and repo evidence without a new human decision
- `needs human decision`: blocked on user or caller behavior, architecture, security/data, access, dependency, or manual review

These are readiness states for the issue body, not mandatory labels. If a repo already uses AFK/HITL wording, map `agent-ready` to AFK and `needs human decision` to HITL. Otherwise use the clearer words in the issue body.

For blocked issues, record:

```markdown
## Established so far
- ...

## Still needed
- Specific decision, artifact, source/API contract, access, dependency, or manual review needed
```

## Issue Claiming

Before editing for an implementation issue, inspect the issue body, comments, assignees, labels, linked PRs, and recent activity. If the issue is stale, ambiguous, already claimed, or missing source scope or verification evidence, resolve that before editing. Then comment:

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

Do not start implementation from an issue title alone. Use the issue body, comments, linked PRs, accepted scope, repo evidence, and claim state as the portable baseline.

## PR Flow

- Link PRs to issues in the body with the repo's preferred format, such as `Closes #123`.
- Include source/test/config/docs/workflow changes, checks run, CI/check status when known, and residual risk.
- Use draft PRs when the source change, review response, or verification evidence is intentionally not ready.
- Do not claim CI status without checking the latest head SHA with `gh pr checks`, `gh run`, the GitHub UI, or connector/app PR status.
- Update or comment on the issue when public or caller contracts, scope, acceptance checks, blockers, verification evidence, or reviewer requests change.
- Resolve or mark review threads only after the code, tests, docs, or explicit technical response addresses the current comment. When a tool supports inline replies, answer inline threads in the thread; a top-level PR summary can supplement thread replies, but should not replace them when unresolved thread state matters.
- Before saying a PR is ready, mergeable, reviewed, or safe, verify latest head SHA, local diff scope, linked issue/PRD alignment, relevant checks, unresolved review threads, and residual risk. Hand off to `verify-before-done` for the completion claim.

## Review Feedback Flow

Use this when addressing PR comments, requested changes, review threads, or CI feedback:

Review comments, requested changes, and CI feedback are claims or requests to evaluate against repo evidence before changing code.

Mechanical flow:

- Read the full context: PR body, linked issue/PRD, changed files, comments, unresolved threads, requested changes, and latest CI/check state.
- Verify each item against current source, tests, docs, public or caller contracts, and accepted scope before changing code.
- Decide: fix, push back, clarify, or defer.
- Implement only one item or tightly related group at a time, then run the narrowest relevant check.
- Reply with technical evidence and leave threads unresolved until code, docs, tests, or explicit technical response addresses the current comment.

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

Push back when feedback is stale, technically incorrect, unsafe, conflicts with the approved scope, violates YAGNI, or adds unsupported behavior. Use `codebase-cleanup` when review feedback exposes a real behavior-preserving structure problem. Do not reply with empty agreement; make the evidence or decision clear.

## Stop Or Ask

- Target repo, issue, PR, review thread, base branch, or head branch is ambiguous and live GitHub state or repo evidence cannot resolve it.
- The GitHub action would transfer, duplicate, lock, pin, delete, force-update, merge, close, or otherwise irreversibly change external state without explicit approval.
- A record would mark work `agent-ready`, complete, reviewed, CI-passing, mergeable, or safe without live evidence for the latest relevant state.
- A PRD or slice issue lacks accepted behavior, source scope, public or caller contract, acceptance checks, verification path, or blocker state.
- An implementation issue is already actively claimed, has overlapping parallel scope, or has unresolved ownership/coordination conflict.
- Review feedback would change behavior, public or caller contract, source shape, or accepted scope and repo evidence does not decide whether to fix, push back, defer, or clarify.
- GitHub auth, remote, connector access, or CI/check visibility is missing and the action depends on it.

## Useful Commands

Use the repo's active GitHub interface. Common `gh` examples:

```bash
gh issue view <number>
gh issue create --title "<title>" --body-file .tmp/<file>.md
gh issue comment <number> --body-file .tmp/<file>.md
gh pr create --title "<title>" --body-file .tmp/<file>.md
gh pr view <number>
gh pr checks <number>
gh run view <run-id>
```

## Report

For small GitHub work:

```text
Object:
Action:
Live evidence:
Remaining blocker or uncertainty:
```

For multi-record or PR/review work, add linked issues/PRs, readiness or blocker state, checks or CI evidence, review-thread state, and next action.

## Handoff

- `clarify-scope`: before writing a PRD when target behavior, public or caller contract, or affected source boundary is unclear.
- `slice-plan`: turn an approved PRD or request into implementation slice issues.
- `issue-driven-execution`: the user wants a plan doc, GitHub issues, and issue-by-issue implementation checkpoints.
- `workspace-safety`: before commits, branch changes, or PR creation from a dirty tree.
- `verify-before-done`: before claiming PR readiness, CI status, review resolution, or merge safety.
