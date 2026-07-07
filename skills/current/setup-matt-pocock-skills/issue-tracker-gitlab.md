# Issue tracker: GitLab

Issues and PRDs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `glab mr view`, `glab mr note`, etc. — the same shape as `gh pr ...` with `mr` in place of `pr` and `note`/`--message` in place of `comment`/`--body`.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

## Merge requests as a triage surface

**MRs as a request surface: no.** _(Set to `yes` if this repo treats external merge requests as feature requests; `$triage` reads this flag.)_

When set to `yes`, MRs run through the same labels and states as issues, using the `glab mr` equivalents:

- **Read an MR**: `glab mr view <number> --comments` and `glab mr diff <number>` for the diff.
- **List external MRs for triage**: `glab mr list -F json`, then keep only MRs whose author is not a project member/owner (a contributor's MR, not a maintainer's in-flight work). If author membership cannot be determined confidently, surface the MR as a candidate instead of silently dropping it.
- **Comment / label / close**: `glab mr note`, `glab mr update --label`/`--unlabel`, `glab mr close`.

Unlike GitHub, GitLab numbers issues and MRs separately, so `#42` is unambiguous once you know which surface the maintainer means.

## When a skill says "publish to the issue tracker"

Create a GitLab issue.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.

For an external MR when MRs are a request surface, run `glab mr view <number> --comments` and `glab mr diff <number>`.

## Wayfinding operations

Used by `$wayfinder`. The **map** is a single GitLab issue with child issues as tickets.

- **Map**: create one issue labelled `wayfinder:map`. Its body holds Destination, Notes, Decisions So Far, Not Yet Specified, and Out Of Scope. On GitLab tiers with native epics, an epic may hold the map instead; a labelled issue works everywhere.
- **Child ticket**: create one issue per ticket. If native child relationships are unavailable, add `Part of #<map>` at the top of the child body. Label each ticket with exactly one `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task`.
- **Blocking**: use GitLab's native issue links/blocking relationship when available. If unavailable, put `Blocked by: #<n>, #<n>` near the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's open children, then drop tickets with an open blocker or assignee. The first remaining ticket in map order is the frontier.
- **Claim**: assign the ticket to the driver before work; the assignee is the concurrency guard.
- **Resolve**: post the answer as a note, close the ticket, then append one context pointer to the map's Decisions So Far.

## When a skill says "post a Codex-ready brief"

Post it as an issue note with `glab issue note <number> --message "..."`.

For an external MR when MRs are a request surface, use `glab mr note <number> --message "..."`.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
