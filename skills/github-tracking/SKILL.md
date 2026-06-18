---
name: github-tracking
description: "Use when repo work needs durable GitHub recordkeeping: issue/PRD/slice bodies, claim/status/blocker comments, PR/issue links, readiness fields, or CI/review evidence recorded in GitHub; skip ordinary local work, generic triage, PR publishing, CI debugging, and review-comment resolution when narrower workflows own them."
---

# GitHub Tracking

Use GitHub records to preserve coding intent, source scope, public or caller contracts, decisions, blockers, verification evidence, and PR review state. This is a durable recordkeeping skill, not a general GitHub client, PR publisher, CI debugger, or review-comment workflow.

When the user asks to create or update issue bodies, PRDs, implementation slice issues, claim/status/blocker comments, PR or issue links, readiness fields, or recorded CI/review evidence, first inspect the relevant live GitHub state and repo conventions.

Before writing a GitHub record, inspect only record-affecting inputs: target repo or object, source record, linked issue/PR/check/review state, accepted source scope, public or caller contract, acceptance checks, verification evidence, readiness or blocker state, duplicate or parent state, and sidebar metadata when they could change the record.

## When To Track

Track in GitHub only when the output is a durable GitHub record or an update to one:

- The user asks for an issue, PRD, implementation slice issue, claim/status/blocker comment, PR body/update note, issue/PR link, readiness field, or recorded CI/review evidence.
- Approved GitHub-backed work needs accepted scope, public or caller contract, acceptance checks, blockers, verification evidence, or status preserved in an issue, PR, or comment.
- Existing issue, PR, check, or review state changes the durable record to write or update and must be inspected or cited before that record changes.
- A cleanup or refactor candidate should be scheduled later by issue because the user requested it or repo convention expects it.

Do not start this skill merely because work is multi-session, shared with humans, changes behavior, touches CI, or has review feedback. If the current job is local implementation, generic GitHub triage, PR publishing, CI debugging, semantic review, or review-comment resolution, use the narrower workflow for that job and return here only to update durable records.

## Baseline

Before creating or editing GitHub records:

1. Confirm the repo has a GitHub remote and identify the target owner/repo, base branch, and current head branch when relevant.
2. Check `gh auth status` or connector/app authorization if auth is uncertain.
3. Read existing issue, label, and PR conventions when present.
4. Inspect linked issues, PRs, review threads, CI/check runs, and repo notes when they are part of the request.
5. Search for a duplicate or parent issue only when creating a new issue, PRD, slice record, or when duplicate or parent state could change the requested record.
6. Read durable context or glossary files, when present, only for shared terms, module boundaries, and public or caller contract names that should appear in durable GitHub records.
7. Preserve the current working tree and record the head SHA when PR or CI state matters.

If GitHub state affects the answer, inspect it live with the available GitHub interface; do not rely on memory. Use `gh` when it is the repo's working interface, or GitHub connector/app tools when they are available. Preserve the same evidence rules either way: check live state, search for duplicates only when relevant, follow repo conventions, and keep issue or PR bodies as durable repo artifacts rather than chat transcripts.

Do not write, update, close, label, claim, resolve, or mark ready from memory, stale summaries, or chat-only context. If live GitHub state cannot be inspected and the action depends on it, stop or ask.

## Fast Path

Use for small GitHub record requests.

1. Identify the target repo and durable record to inspect, draft, create, update, link, or comment on.
2. Inspect the live record, source object, and relevant repo conventions.
3. If the user asked for a draft, recommendation, or record shape, prepare the draft only; do not post it.
4. If the user asked to create, update, comment, link, or record evidence, make the smallest requested GitHub write.
5. If write intent is unclear, ask before posting, updating, commenting, labeling, linking, closing, or marking state.
6. Report the record/link or draft, live evidence used, action taken, and remaining blocker or uncertainty.

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

Use a body or comment trail when metadata would otherwise hide claim, status, blocker, readiness reasoning, or verification evidence. Metadata is a structured signal; it does not replace the technical record.

Transfer, duplicate, lock, pin, delete, close, or merge only with explicit approval when the action is irreversible or externally visible.

## Issue State Notes

Use this only when issue state should become or update a durable record. For general repo, PR, or issue summaries, use the host's GitHub triage workflow instead.

When asked to update or recommend issue state, use issue bodies and comments as the durable state. Labels, projects, milestones, and assignees should follow repo conventions; if no convention exists, recommend a state in the comment/body instead of inventing a private label system.

- Read the full issue, previous comments, linked PRs, labels, and recent activity before recommending state.
- Recommend category, readiness, blocker, or close/defer state with evidence from the issue, repo, docs, tests, logs, or CI.
- For bugs, use the existing reproducer, logs, CI output, issue evidence, or a cheap focused check when practical before marking work agent-ready. If reproduction becomes real investigation or debugging, use `diagnose-loop`; if no reproducer is available, record what is missing.
- When resuming issue-state work, preserve established facts and avoid re-asking resolved questions.
- Do not mark `agent-ready` unless the issue has enough repo evidence, accepted scope, public or caller contract, and verification path for an implementer to start without a new human decision. Mark `needs human decision` when the missing behavior, architecture, security/data, access, dependency, or manual-review decision blocks safe execution.

## PRD Record Shape

Use when an accepted feature, user-facing behavior, or multi-slice change should be recorded as a GitHub PRD or issue. This section defines the durable record shape; it does not decide target behavior, source boundaries, or implementation slices. Use `clarify-scope` or `slice-plan` first when those are unresolved.

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

## Slice Issue Records

Use when an approved plan or request is being recorded as GitHub implementation issues. This section defines issue-body shape; it does not own planning. Use `slice-plan` first when task boundaries, checks, continuity, or execution mode are still unclear.

Record small vertical slices.

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

Use claim comments only when the user, repo convention, approved issue workflow, or multi-agent coordination expects a claim. Do not invent claim ceremony for ordinary local work.

Before recording a claim for an implementation issue, inspect the issue body, comments, assignees, labels, linked PRs, and recent activity. If the issue is stale, ambiguous, already claimed, or missing source scope or verification evidence, resolve that before recording the claim. Then comment:

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

Do not record a claim, status, readiness, blocker, or PR update from an issue title alone. Use the issue body, comments, linked PRs, accepted scope, repo evidence, and claim state as the portable baseline.

## PR Record Flow

Use this section when a PR, linked issue, or comment needs a durable record update. Do not use it to publish a PR, debug CI, perform semantic review, or resolve review threads; use the narrower workflow for that job, then return here only if the durable record needs updating.

- Link PRs to issues in the body with the repo's preferred format, such as `Closes #123`.
- Record source/test/config/docs/workflow changes, checks run, CI/check status when known, and residual risk.
- Mark draft or not-ready status in the PR body or comment when the source change, review response, or verification evidence is intentionally not ready.
- Do not record or claim CI status without checking the latest head SHA with `gh pr checks`, `gh run`, the GitHub UI, or connector/app PR status.
- Update or comment on the issue when public or caller contracts, scope, acceptance checks, blockers, verification evidence, or reviewer requests change.
- Record review-thread decisions only after the review workflow decides fix, push back, clarify, or defer. Do not post replies or resolve review threads from this skill unless the user explicitly asks for that GitHub write action.
- Before recording a PR as ready, mergeable, reviewed, or safe, verify latest head SHA, local diff scope, linked issue/PRD alignment, relevant checks, unresolved review threads, and residual risk. Hand off to `verify-before-done` for the completion claim.

## Review Feedback Record Flow

Use this only to record the outcome of PR comments, requested changes, review threads, or CI feedback. Use `pre-pr-review` for semantic diff review, `diagnose-loop` for failing checks, and the host's GitHub review-comment workflow for thread-level fixing, replies, or resolution.

Review comments, requested changes, and CI feedback are claims or requests to evaluate against repo evidence before changing code. This skill preserves the durable decision trail after that evaluation; it does not own the implementation loop.

Recordkeeping flow:

- Read the target comment, thread, requested change, or CI feedback first. Then read only the PR body, linked issue/PRD, changed files, source/tests/docs, unresolved threads, and latest check state needed to justify the durable record.
- Verify each recorded decision against current source, tests, docs, public or caller contracts, accepted scope, and the narrow workflow that handled the item.
- Record the decision: fix, push back, clarify, or defer.
- Record the check or evidence after the change or response.
- Leave threads unresolved in the record until code, docs, tests, or explicit technical response addresses the current comment.

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

Push back when feedback is stale, technically incorrect, unsafe, conflicts with the approved scope, violates YAGNI, or adds unsupported behavior. Use `codebase-cleanup` when review feedback exposes a real behavior-preserving structure problem. Do not record empty agreement; make the evidence or decision clear.

## Stop Or Ask

- Target repo, issue, PR, review thread, base branch, or head branch is ambiguous and live GitHub state or repo evidence cannot resolve it.
- GitHub write intent is unclear; draft locally and ask before posting, updating, commenting, labeling, linking, closing, or marking state.
- The GitHub action would transfer, duplicate, lock, pin, delete, force-update, merge, close, or otherwise irreversibly change external state without explicit approval.
- A record would mark work `agent-ready`, complete, reviewed, CI-passing, mergeable, or safe without live evidence for the latest relevant state.
- A PRD or slice issue lacks accepted behavior, source scope, public or caller contract, acceptance checks, verification path, or blocker state.
- An implementation issue is already actively claimed, has overlapping parallel scope, or has unresolved ownership/coordination conflict.
- Review feedback would change behavior, public or caller contract, source shape, or accepted scope and the narrower review, debugging, or implementation workflow has not decided whether to fix, push back, defer, or clarify.
- GitHub auth, remote, connector access, or CI/check visibility is missing and the action depends on it.

## Useful Commands

Use the repo's active GitHub interface. Common `gh` examples for record updates and evidence capture:

```bash
gh issue view <number>
gh issue create --title "<title>" --body-file .tmp/<file>.md
gh issue comment <number> --body-file .tmp/<file>.md
gh pr view <number>
gh pr edit <number> --body-file .tmp/<file>.md
gh pr comment <number> --body-file .tmp/<file>.md
gh pr checks <number>
gh run view <run-id>
```

Use check and run commands here to capture status or evidence for a durable record. If CI logs or root cause debugging matter, use the narrower CI debugging workflow instead.

## Report

For small GitHub record work:

```text
Object:
Action:
Live evidence:
Remaining blocker or uncertainty:
```

For multi-record work, add linked issues/PRs, readiness or blocker state, checks or CI evidence recorded, review-thread decision state recorded, and next action.

## Handoff

- `clarify-scope`: before writing a PRD when target behavior, public or caller contract, or affected source boundary is unclear.
- `slice-plan`: define reviewable source, test, docs, task boundaries, checks, continuity, and execution mode before those slices become GitHub issues.
- `issue-driven-execution`: the user wants a plan doc, GitHub issues, issue-by-issue implementation, and an explicit checkpoint policy.
- `workspace-safety`: before branch, commit, or overlapping dirty-path operations while updating records.
- `verify-before-done`: before recording or claiming PR readiness, CI status, review resolution, or merge safety.
