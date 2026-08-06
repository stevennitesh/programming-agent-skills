# Issue tracker: GitHub

Issues and specs live as GitHub issues. This guide maps skill-owned tracker
actions to GitHub. Skills own packet content, readiness judgment, authorization,
workflow order, claim lifecycle, review, and completion.

## Configuration

**PRs as a request surface: no.**

**Close implemented items:** yes.

**Parent / child mode:** native-sub-issues.

**Dependency mode:** native-dependencies.

## Operations

Use the GitHub connector for issues and pull requests. Infer owner and repository
from `git remote -v` when explicit arguments are required. Use `gh` only when
the connector lacks the required operation.

- **Publish:** create a GitHub issue.
- **Fetch:** read the issue body, comments, labels, state, assignee, and
  relationships.
- **Comment or brief:** post an issue comment. When PR intake is enabled, post a
  PR comment instead; `$triage` owns the brief and disclaimer.
- **Close:** use the connector's close action and include the skill-owned closing
  comment when applicable.
- **Relationships:** use connector actions when exposed; otherwise use GitHub's
  sub-issue and issue-dependency REST endpoints through `gh api`. Resolve the
  authenticated operation and read-back route before the first create.
When PR intake is enabled, fetch the PR body, comments, labels, author
association, and diff. External candidates have author association
`CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR`, or `NONE`. GitHub issues and PRs share
one number space, so resolve an ambiguous `#<n>` as a PR first and then as an
issue.

## Work-item representation

- **Packet:** issue body and comments.
- **State:** mapped category and state labels. `ready-for-agent` and
  `ready-for-human` are navigation metadata, not proof that a packet or
  transition is valid.
- **Parent / child:** `native-sub-issues` uses GitHub sub-issues;
  `parent-task-list` uses an ordered parent task list and
  `Part of #<parent>` in each child.
- **Blocking:** `native-dependencies` uses GitHub issue dependencies;
  `body-links` uses `Blocked by: #<n>, #<n>` in the child.
- **Ready query:** derive agent and human frontiers separately from open items
  in their mapped readiness state, then exclude unresolved blockers and
  assignees. Preserve child order within a parent; otherwise use oldest first.
- **Claim:** the assignee stores the active claim.
- **Closeout:** post the skill-owned packet, apply `implemented`, remove the
  prior state label, and close only when configured above or explicitly
  directed. Preserve completed dependency history. Closing a blocker for any
  other reason must not expose a false-ready dependent.

Freeze both relationship modes before publication. Stop before creation when a
configured operation or read-back route is unavailable; never switch
representations during one publication.

## Wayfinding representation

The map and tickets are issues connected through the configured relationships.
Use the fixed map and ticket labels from `docs/agents/triage-labels.md`. The map
body follows `$wayfinder`'s `MAP-FORMAT.md`.

Store `Participation:`, `Resolution owner:`, `Resolver:`, `Expected return:`,
`Mutation boundary:`, and `Re-entry owner: $wayfinder` in the issue body. Represent fog as
`Blocked: fog - <gist>` and an external return as
`Blocked: waiting - <gist>` with its exact return record in a comment. Store an
active claim in the assignee plus `Claim token:` and `Claimed at:` body fields.
Resolved and out-of-scope tickets close; blocked and waiting tickets remain
open. `$wayfinder` owns frontier selection, claim lifecycle, outcomes, and map
completion.

## Mutation read-back

After a mutation, refetch the target and affected dependents and verify every
intended body, relationship, label or state, assignee, comment, close reason,
open or closed state, and resulting frontier. Refetch after a failed or
indeterminate command; do not retry blindly. Treat any unverified partial
mutation as blocked and report applied, failed, and unknown effects plus the
safest recovery.
