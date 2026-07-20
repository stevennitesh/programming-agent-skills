# Issue tracker: GitLab

Issues and specs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. For a multiline description, pass `--description -` and use the configured editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -O json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `view`, `diff`, `note`, `update`, and `close`; comments are notes and use `--message`.

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

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`, `$parallel-implement`, and `$review`.

**Close implemented items:** no.

- **Packet**: the issue description and notes are the durable packet. A parent spec owns intent; child issues own implementation slices and closeout evidence. No separate repo-local packet is required unless `AGENTS.md` points to one. Approved implementation tickets carry the mapped `ready-for-agent` state and one category role when the source settles it.
- **Ready-for-agent contract**: every ready item names one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. `$triage` owns incoming classification and verification; `$to-tickets` owns slicing and dependency order. Both produce this contract.
- **Parent / child**: use native child relationships when available. Otherwise keep an ordered task list in the parent and put `Part of #<parent>` near the top of each child.
- **Blocking**: use native blocking issue links when available. Otherwise put `Blocked by: #<n>, #<n>` near the top of the child description. Normally a work item is unblocked when every blocker is closed. During one recorded `$parallel-implement` campaign, a blocker with an accepted landing that remains in current integration history with valid proof is derived as `landed-awaiting-lock`; it satisfies execution readiness only for in-scope dependents in that campaign. The issue and dependency remain open until Lock. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.
- **Ready query**: list open issues with the mapped `ready-for-agent` state, then drop issues with an unresolved blocker or assignee. Treat an open blocker as resolved only when the verified same-campaign `landed-awaiting-lock` overlay above applies. Within a parent, preserve child order; otherwise choose oldest first.
- **Claim**: assign the work item to the owner or orchestrator before implementation dispatch; the assignee is the concurrency guard.
- **Release**: clear the active assignee when work blocks, is abandoned, or reaches closeout.
- **Closeout**: after required review and commits, post the closeout packet as a note, apply `implemented`, remove the prior state-role label, and release the claim. Close the issue only when `Close implemented items` is `yes` or the user directs it. Close a parent only after its in-scope children and follow-ups are drained.
- **Mutation read-back**: after creating or changing an item, refetch it and verify the intended description, relationships, labels or state, assignee, notes, and open/closed status. A partial mutation is blocked; report applied operations, failed operations, and the safest recovery action.

## Wayfinder tracker mapping

This section maps Wayfinder's provider-neutral objects and primitives to GitLab. Wayfinder owns identity rules, fields, state, claims, recovery, sequencing, and completion.

- **Map object**: one issue carrying the `wayfinder:map` label; its description stores the fields defined by Wayfinder's `MAP-FORMAT.md`. Include open and closed issues when Wayfinder requests map candidates.
- **Ticket object**: a native child issue when available; otherwise an ordered map entry plus `Part of #<map>` in the ticket description.
- **Resolver type mapping**: exactly one of `wayfinder:research`, `wayfinder:prototype`, `wayfinder:diagnosis`, `wayfinder:questionnaire`, `wayfinder:grilling`, `wayfinder:design`, or `wayfinder:task`.
- **Parent and blocking mapping**: use child relationships and blocking links when available; otherwise use the ordered map list and `Blocked by: #<n>` description fields.
- **Claim storage**: the map description stores Wayfinder's campaign-claim block; assignment may mirror its actor but grants no semantic authority.
- **Claim capability**: `unavailable` until the target records an exact conditional mutation or exclusive lock against a captured revision. A configured primitive must fail a losing actor or changed revision; record its invocation and losing-race result here.
- **Claim release mapping**: remove the configured guard, map claim block, and mirrored assignee, then refetch their absence.
- **Revision token**: project and issue identity, `updated_at`, description hash, state, labels, assignees, child and dependency data, and relevant note ids or timestamps.
- **Read-back primitive**: refetch the issue and every affected relationship through `glab`; return provider errors and observed fields to the owning skill.

## When a skill says "post a Codex-ready brief"

Post it as an issue note with `glab issue note <number> --message "..."`.

For an external MR when MRs are a request surface, use `glab mr note <number> --message "..."`.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
