# Issue tracker: Local Markdown

Tracker state is version-controlled Markdown under `.scratch/<feature-slug>/`.
Use this layout for tracker-backed work; direct coding creates no ticket files.

## Operations

- **Parent:** `.scratch/<feature-slug>/SPEC.md`.
- **Issue:** `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.
- **Publish:** create the applicable parent or issue file.
- **Fetch:** read the referenced file.
- **Comment:** append under `## Comments`.
- **Close:** record the workflow's completion evidence, set the mapped
  implemented state, and remove the active claim.

## Representation

- Content lives in the parent or issue body, comments, and implementation notes.
- Category and state use [the label mapping](triage-labels.md).
- The parent links its children in order; each child links its parent.
- `Blocked by:` stores dependency links.
- `Claimed by:` stores an active claim when the workflow requires claiming.

The consuming workflow defines readiness and transitions. Completing a blocker
does not establish readiness if other dependencies remain unresolved. Keep the
durable tracker path available to version control; it is not disposable scratch.

## Mutation read-back

Reread changed files and affected dependents. Verify the intended content,
relationships, state, and claim. After a partial operation, inspect the resulting
files before retrying and report any remaining gap.
