# Issue tracker: GitLab

Issues and specifications live in GitLab Issues.

## Configuration

**MRs as a request surface:** no.

**Close implemented items:** no.

**Parent / child mode:** body-links.

**Dependency mode:** body-links.

## Operations

Run `glab` inside the clone so it resolves the configured project.

- **Publish:** `glab issue create`.
- **Fetch:** `glab issue view <number> --comments` or JSON output from
  `glab issue list`.
- **Comment:** `glab issue note <number> --message "..."`.
- **Label:** `glab issue update <number> --label "..."` or `--unlabel "..."`.
- **Close:** add any skill-owned closing note, then run
  `glab issue close <number>` when configured or explicitly directed.
- **Relationships:** use the configured native-link or body-link representation.

Issues and merge requests have separate number spaces. Name the surface with
the number. Resolve the operation and its read-back route before the first
external mutation.

## Representation

- Content lives in the issue description and notes.
- Category and state use values from `docs/agents/triage-labels.md`.
- Parent, child, and blocking links use the configured relationship form.
- An active claim uses the assignee.

Do not switch relationship representations during one publication. Closing or
superseding a blocker must not expose a dependent as ready while it remains
blocked.

## Mutation read-back

After a mutation, refetch the target and affected relationships. Verify the
intended description, labels, state, assignee, notes, and open or closed state.
After a failed or indeterminate command, refetch before deciding whether to
retry. Report any observed partial result and the safest recovery.
