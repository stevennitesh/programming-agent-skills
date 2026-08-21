# Issue tracker: GitLab

Issues and specs live as GitLab issues. This guide maps skill-owned tracker
actions to GitLab. Skills own packet content, readiness judgment, authorization,
workflow order, claim lifecycle, review, and completion.

## Configuration

**MRs as a request surface:** no.

**Close implemented items:** no.

## Operations

Run `glab` inside the clone; it resolves the project from the remote.

- **Publish:** `glab issue create --title "..." --description "..."`; use
  `--description -` for editor input.
- **Fetch or list:** `glab issue view <number> --comments` or
  `glab issue list -O json`. Use JSON output for machine reads.
- **Comment or brief:** `glab issue note <number> --message "..."`; `$triage`
  owns the brief. Apply attribution only when repository policy requires it.
- **Label:** `glab issue update <number> --label "..."` or `--unlabel "..."`.
- **Close:** post any closing note first, then run `glab issue close <number>`.
- **Merge requests:** when intake is enabled, use the corresponding
  `glab mr view|diff|list|note|update|close` commands. Surface uncertain author
  membership instead of silently excluding the MR.

Issues and MRs have separate number spaces; name the surface with the number.

## Work-item representation

- **Packet:** issue description and notes.
- **State:** mapped category and state labels. `ready-for-agent` and
  `ready-for-human` are navigation metadata, not proof that a packet or
  transition is valid.
- **Parent / child:** use a verified native child relationship when available;
  otherwise use an ordered parent task list and `Part of #<parent>` in each
  child.
- **Blocking:** use verified native blocking links when available; otherwise
  use `Blocked by: #<n>, #<n>`.
- **Ready query:** derive agent and human frontiers separately from open items
  in their mapped readiness state, then exclude unresolved blockers and
  assignees. Preserve parent order; otherwise use oldest first.
- **Claim:** the assignee stores the active claim.
- **Closeout:** post the skill-owned packet as a note, apply `implemented`,
  remove the prior state label, and close only when configured above or
  explicitly directed. Closing a blocker for any other reason must not expose a
  false-ready dependent.

## Wayfinding representation

The map and tickets are issues connected through the configured relationship
representation. Use the fixed map and ticket labels from
`docs/agents/triage-labels.md`; the map body follows `$wayfinder`'s
`MAP-FORMAT.md`.

Store `Type:`, `Decision owner:`, `Accept when:`, and any applicable
`Mutation boundary:` in the issue description. Represent fog as
`Blocked: fog - <gist> - sharpens when <evidence or decision>` and an external
return as `Blocked: waiting - <gist>` with its exact owner and return condition
in a note. Store an active claim in the assignee plus `Claim token:`.
Resolved and out-of-scope tickets close; blocked and waiting tickets
remain open. `$wayfinder` owns frontier selection, claim lifecycle, outcomes,
and map completion.

## Mutation read-back

After a mutation, refetch the target and affected dependents and verify every
intended description, relationship, label or state, assignee, note, open or
closed state, and resulting frontier. Refetch after a failed or indeterminate
command; do not retry blindly. Treat any unverified partial mutation as blocked
and report applied, failed, and unknown effects plus the safest recovery.
