# Issue tracker: Local Markdown

Tracker state is version-controlled Markdown under
`.scratch/<feature-slug>/`.

## Operations

- **Parent:** `.scratch/<feature-slug>/SPEC.md`.
- **Issue:** `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.
- **Publish:** create the applicable parent or issue file.
- **Fetch:** read the referenced file.
- **Comment:** append under `## Comments`.
- **Close:** append the skill-owned result, set the mapped implemented state,
  and remove any active claim.

## Representation

- Content lives in the parent or issue body, comments, and implementation notes.
- Category and state use values from `docs/agents/triage-labels.md`.
- The parent links children in order; each child links its parent.
- `Blocked by:` stores dependencies.
- `Claimed by:` stores an active claim.

Closing or superseding a blocker must not expose a dependent as ready while it
remains blocked.

## Mutation read-back

After a mutation, reread changed files and affected dependents. Verify the
intended content, relationships, state, claim, and closeout. If an operation
stops partway through, inspect the resulting files before deciding whether to
retry and report the safest recovery.
