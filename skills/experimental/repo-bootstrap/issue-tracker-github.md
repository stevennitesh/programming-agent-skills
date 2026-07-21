# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. Use the GitHub connector for issue and pull-request operations.

## Conventions

- **Create an issue**: use the GitHub connector's issue creation action.
- **Read an issue**: use the GitHub connector to fetch the issue body, comments, and labels.
- **List issues**: use the GitHub connector to list open issues with number, title, body, labels, and comments; filter by mapped labels when needed.
- **Comment on an issue**: use the GitHub connector's issue comment action.
- **Apply / remove labels**: use the GitHub connector's issue edit or label action.
- **Close**: use the GitHub connector's close issue action with a closing comment when relevant.

Infer the owner and repo from `git remote -v` when the connector needs explicit repository arguments.

Use the `gh` CLI only as a fallback when the connector cannot perform the required operation in the current environment.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `$triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues using the GitHub connector:

- **Read a PR**: fetch the PR body, comments, labels, author, author association, and diff.
- **List external PRs for triage**: list open PRs with number, title, body, labels, author, author association, and comments; keep only `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE` author associations and drop `OWNER`, `MEMBER`, and `COLLABORATOR`.
- **Comment / label / close**: use the connector's PR comment, edit/label, and close actions.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either. Resolve with the GitHub connector's pull-request lookup first, then issue lookup when necessary.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Fetch the issue with the GitHub connector, including comments and labels.

For an external PR when PRs are a request surface, fetch the PR with the GitHub connector, including comments, labels, author metadata, and diff.

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`, `$parallel-implement`, and `$review`.

**Close implemented items:** yes.

- **Packet**: the issue body and comments are the durable packet. A parent spec owns intent; child issues own implementation slices and closeout evidence. No separate repo-local packet is required unless `AGENTS.md` points to one. Approved implementation tickets carry the mapped `ready-for-agent` state and one category role when the source settles it.
- **Ready-for-agent contract**: every ready item names one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. `$triage` owns incoming classification and verification; `$to-tickets` owns slicing and dependency order. Both produce this contract.
- **Parent / child**: use GitHub sub-issues when available. Otherwise keep an ordered task list in the parent and put `Part of #<parent>` near the top of each child.
- **Blocking**: use native issue dependencies when available. Otherwise put `Blocked by: #<n>, #<n>` near the top of the child body. Normally a work item is unblocked when every blocker is closed. During one recorded `$parallel-implement` campaign, a blocker with an accepted landing that remains in current integration history with valid proof is derived as `landed-awaiting-lock`; it satisfies execution readiness only for in-scope dependents in that campaign. The issue and dependency remain open until Lock. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.
- **Ready query**: list open issues with the mapped `ready-for-agent` state, then drop issues with an unresolved blocker or assignee. Treat an open blocker as resolved only when the verified same-campaign `landed-awaiting-lock` overlay above applies. Within a parent, preserve child order; otherwise choose oldest first.
- **Claim**: assign the work item to the owner or orchestrator before implementation dispatch; the assignee is the concurrency guard.
- **Release**: remove the active assignee when work blocks, is abandoned, or reaches closeout.
- **Closeout**: after required review and commits, post the closeout packet, apply or retain `implemented`, remove the prior state-role label, release the claim, and close the implementation issue as completed. Preserve dependency links: closing a completed blocker retains history and removes it from the active blocker set. Close a parent spec only after every in-scope child and follow-up is closed; post a final summary before closing it.
- **Non-completed closure**: before closing a blocker as not planned, duplicate, or superseded, inspect every dependent. Rewire it, give it an explicit open blocker, or close it for its own reason. Closure must not create a false-ready frontier.
- **Mutation read-back**: after creating or changing an item, refetch the item and its affected dependents; verify the intended body, relationships, labels or state, assignee, comments, close reason, open/closed status, and resulting frontier. A partial mutation is blocked; report applied operations, failed operations, and the safest recovery action.

## Wayfinder tracker mapping

This section maps Wayfinder's provider-neutral objects and primitives to GitHub. Wayfinder owns identity rules, fields, state, claims, recovery, sequencing, and completion.

- **Map object**: one issue carrying the `wayfinder:map` label; its body stores the fields defined by Wayfinder's `MAP-FORMAT.md`. Include open and closed issues when Wayfinder requests map candidates.
- **Ticket object**: a GitHub sub-issue when available; otherwise a map task-list entry plus `Part of #<map>` in the ticket body.
- **Resolver type mapping**: exactly one of `wayfinder:research`, `wayfinder:prototype`, `wayfinder:diagnosis`, `wayfinder:questionnaire`, `wayfinder:grilling`, `wayfinder:design`, or `wayfinder:task`.
- **Parent and blocking mapping**: use sub-issues and native blocking links when available; otherwise use the ordered map task list and `Blocked by: #<n>` body fields.
- **Claim storage**: the map body stores Wayfinder's campaign-claim block; assignment may mirror its actor but grants no semantic authority.
- **Claim capability**: `unavailable` until the target records an exact conditional mutation or exclusive lock against a captured revision. A configured primitive must fail a losing actor or changed revision; record its invocation and losing-race result here.
- **Claim release mapping**: remove the configured guard, map claim block, and mirrored assignee, then refetch their absence.
- **Revision token**: issue id, `updatedAt`, body hash, state, labels, assignees, child and dependency data, and relevant comment ids or timestamps.
- **Read-back primitive**: refetch the issue and every affected relationship through the GitHub connector; return provider errors and observed fields to the owning skill.

## When a skill says "post a Codex-ready brief"

Post it as an issue comment with the GitHub connector.

For an external PR when PRs are a request surface, post it as a PR comment with the GitHub connector.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
