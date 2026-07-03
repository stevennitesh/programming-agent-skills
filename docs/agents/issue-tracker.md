# Issue Tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the GitHub connector for issue and pull-request operations.

Repository: `stevennitesh/programming-agent-skills`

## Conventions

- **Create an issue**: use the GitHub connector's issue creation action.
- **Read an issue**: use the GitHub connector to fetch the issue body, comments, and labels.
- **List issues**: use the GitHub connector to list open issues with number, title, body, labels, and comments; filter by mapped labels when needed.
- **Comment on an issue**: use the GitHub connector's issue comment action.
- **Apply / remove labels**: use the GitHub connector's issue edit or label action.
- **Close**: use the GitHub connector's close issue action with a closing comment when relevant.

Infer the owner and repo from `git remote -v` when the connector needs explicit repository arguments.

Use the `gh` CLI only as a fallback when the connector cannot perform the required operation in the current environment.

## Pull Requests As A Triage Surface

**PRs as a request surface: no.**

This repo does not treat external PRs as feature requests for `$triage`. Use normal PR review workflows for pull requests.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either. Resolve with the GitHub connector's pull-request lookup first, then issue lookup when necessary.

## When A Skill Says "Publish To The Issue Tracker"

Create a GitHub issue.

## When A Skill Says "Fetch The Relevant Ticket"

Fetch the issue with the GitHub connector, including comments and labels.

## When A Skill Says "Post A Codex-Ready Brief"

Post it as an issue comment with the GitHub connector.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
