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

During parallel delivery, the root's selected integration checkout is the canonical
tracker. Only the root mutates tracker files there; worker copies are read-only
snapshots, not current claims or readiness. Record run and item actor identities
in `Claimed by:` so a shared account cannot disguise competing runs. The execution
workflow owns tracker commits and completion evidence for the code candidate.
Publication alone does not authorize commits.

## Mutation read-back

Reread changed files and affected dependents. Verify the intended content,
relationships, state, and claim. After a partial operation, inspect the resulting
files before retrying and report any remaining gap.
