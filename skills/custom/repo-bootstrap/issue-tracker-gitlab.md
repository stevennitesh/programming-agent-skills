# Issue tracker: GitLab

Issues and specs for this repo live as GitLab issues. Use the
[`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`.
  For a multiline description, pass `--description -` and use the configured
  editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for
  machine-readable output.
- **List issues**: `glab issue list -O json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab
  calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` /
  `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the
  flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a
  closing comment, so post the explanation first with
  `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`,
  `view`, `diff`, `note`, `update`, and `close`; comments are notes and use
  `--message`.

Infer the repo from `git remote -v` — `glab` does this automatically when run
inside a clone.

## Merge requests as a triage surface

**MRs as a request surface: no.** _(Set to `yes` if this repo treats external
merge requests as feature requests; `$triage` reads this flag.)_

When set to `yes`, MRs run through the same labels and states as issues, using
the `glab mr` equivalents:

- **Read an MR**: `glab mr view <number> --comments` and `glab mr diff <number>`
  for the diff.
- **List external MRs for triage**: `glab mr list -F json`, then keep only MRs
  whose author is not a project member/owner (a contributor's MR, not a
  maintainer's in-flight work). If author membership cannot be determined
  confidently, surface the MR as a candidate instead of silently dropping it.
- **Comment / label / close**: `glab mr note`,
  `glab mr update --label`/`--unlabel`, `glab mr close`.

Unlike GitHub, GitLab numbers issues and MRs separately, so `#42` is unambiguous
once you know which surface the maintainer means.

## When a skill says "publish to the issue tracker"

Create a GitLab issue.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.

For an external MR when MRs are a request surface, run
`glab mr view <number> --comments` and `glab mr diff <number>`.

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`,
`$parallel-implement`, `$change-review`, and `$high-assurance-review`.

**Close implemented items:** no.

- **Packet**: the issue description and notes are the durable packet. A parent
  spec owns intent; child issues own implementation slices and closeout
  evidence. No separate repo-local packet is required unless `AGENTS.md` points
  to one. Approved implementation tickets carry their mapped `ready-for-agent`
  or source-authorized `ready-for-human` state and one category role when the
  source settles it.
- **Ready-for-agent state**: the configured state marks an item whose producing
  workflow verified its owned packet. The state is navigation metadata, not
  proof of content completeness. `$triage` owns its Codex-ready brief and Ready
  Gate; `$to-tickets` owns its execution packets and graph readiness.
- **Ready-for-human state**: the configured state marks a shaped item whose
  next action requires a named human owner. It never makes the item eligible for
  agent dispatch.
- **Parent / child**: use native child relationships when available. Otherwise
  keep an ordered task list in the parent and put `Part of #<parent>` near the
  top of each child.
- **Blocking**: use native blocking issue links when available. Otherwise put
  `Blocked by: #<n>, #<n>` near the top of the child description. Normally a
  work item is unblocked when every blocker is closed. During one recorded
  `$parallel-implement` campaign, a blocker with an accepted landing that
  remains in current integration history with valid proof is derived as
  `landed-awaiting-lock`; it satisfies execution readiness only for in-scope
  dependents in that campaign. The issue and dependency remain open until Lock.
  Rollback, invalidation, or failed proof removes the overlay and reblocks
  dependents.
- **Ready query**: derive agent and human frontiers separately from open issues
  with their mapped readiness state, then drop issues with an unresolved blocker
  or assignee. Treat an open blocker as resolved only when the verified
  same-campaign `landed-awaiting-lock` overlay above applies. Within a parent,
  preserve child order; otherwise choose oldest first.
- **Claim**: assign the work item to the owner or orchestrator before
  implementation dispatch; the assignee is the concurrency guard.
- **Release**: clear the active assignee when work blocks, is abandoned, or
  reaches closeout.
- **Closeout**: after required review and commits, post the closeout packet as a
  note, apply `implemented`, remove the prior state-role label, and release the
  claim. Close the issue only when `Close implemented items` is `yes` or the
  user directs it. Close a parent only after its in-scope children and
  follow-ups are drained.
- **Mutation read-back**: after creating or changing an item, refetch it and its
  affected dependents; verify the intended description, relationships, labels or
  state, assignees, notes, open/closed status, and resulting ready frontier. A
  partial mutation is blocked; report applied operations, failed operations, and
  the safest recovery action.

## Wayfinding operations

Used by `$wayfinder`. The **map** is a single GitLab issue with child issues as
tickets.

- **Map**: create one issue labelled `wayfinder:map`. Its body follows the
  invoking Wayfinder's `MAP-FORMAT.md` contract. On GitLab tiers with native
  epics, an epic may hold the map instead; a labelled issue works everywhere.
- **Child ticket**: create one issue per ticket. If native child relationships
  are unavailable, add `Part of #<map>` at the top. Put
  `Participation: HITL | AFK`, `Resolution owner:`, `Resolver:`,
  `Expected return:`, and `Re-entry owner: $wayfinder` near the top. Label it
  with exactly one `wayfinder:<type>` label: `research`, `prototype`,
  `diagnosis`, `grilling`, or `task`. During Chart, create children in approved
  map order, read back their exact identities, then wire edges.
- **Blocking and waiting**: use the work-item blocking convention. For fog, put
  `Blocked: fog - <gist>` near the top. For an external return, put
  `Blocked: waiting - <gist>` near the top and record its exact return trigger,
  return owner, and any artifact pointer and durability in a note. Resume only
  through Advance after attributable returned evidence matches the exact
  trigger; remove only the satisfied marker while applying the outcome.
- **Frontier query**: list the map's open children, then drop tickets with an
  open blocker, a `Blocked:` marker, an assignee, or an active `Claim token:`.
  The remaining tickets in map order are the frontier; the first is the default
  selection.
- **Claim**: Advance first claims the selected ticket for resolver work, then
  claims the map before recording any ticket outcome, edge, fog disposition, or
  other shared map mutation. Closure also requires the map claim. Maintain
  claims the map. Use the work-item assignee convention, then put
  `Claim token: codex/<lowercase UUIDv4>` and
  `Claimed at: <YYYY-MM-DDTHH:MM:SSZ>` near the top. Generate one fresh UUIDv4
  per Wayfinder invocation, reuse it for both claims in that invocation, and
  never reuse it across invocations. Read back the assignee, exact token, and
  timestamp; a different token owns the item even when the assignee is the same.
- **Release**: clear the active assignee and remove `Claim token:` and
  `Claimed at:` when active work ends.
- **Stale claim**: Elapsed time alone never makes a claim stale. Replace a
  different token only after explicit user approval; first record the prior
  token, claimed-at value, and takeover reason in a note, then apply Mutation
  read-back to the replacement claim.
- **Outcome**: while the map claim is held, post the canonical resolution note.
  Resolve by closing the ticket and adding its context pointer to `Decisions So
  Far`; block by wiring a sharp blocker or adding the fog marker; wait by adding
  the waiting marker; or close as out of scope and append its linked scope note.
  Apply map consequences and read back, then release the ticket claim. Keep the
  map claim through eligible Closure; otherwise release it. Read back every
  final claim state. A failed map claim records no ticket outcome or shared
  mutation.
- **Complete map**: while the map claim is held and no unresolved child, wait,
  blocker, or fog remains, post the compact closing source or decision packet
  as a closing note, close the map, read back its state and empty frontier,
  release the claim, then read back the claim's absence.

## When a skill says "post a Codex-ready brief"

Post it as an issue note with `glab issue note <number> --message "..."`.

For an external MR when MRs are a request surface, use
`glab mr note <number> --message "..."`.

The brief text, including the AI triage disclaimer when required, comes from
`$triage`.
