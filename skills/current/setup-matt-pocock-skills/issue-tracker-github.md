# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the GitHub connector for issue and pull-request operations.

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

## Wayfinding operations

Used by `$wayfinder`. The **map** is a single GitHub issue with child issues as tickets.

- **Map**: create one issue labelled `wayfinder:map`. Its body holds Destination, Notes, Decisions So Far, Not Yet Specified, and Out Of Scope.
- **Child ticket**: create one issue per ticket, linked to the map as a GitHub sub-issue when available. If sub-issues are unavailable, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Label each ticket with exactly one `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task`.
- **Blocking**: use GitHub's native issue dependencies when available. If unavailable, put `Blocked by: #<n>, #<n>` near the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children, then drop tickets with an open blocker or assignee. The first remaining ticket in map order is the frontier.
- **Claim**: assign the ticket to the driver before work; the assignee is the concurrency guard.
- **Resolve**: post the answer as a comment, close the ticket, then append one context pointer to the map's Decisions So Far.

## When a skill says "post a Codex-ready brief"

Post it as an issue comment with the GitHub connector.

For an external PR when PRs are a request surface, post it as a PR comment with the GitHub connector.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
