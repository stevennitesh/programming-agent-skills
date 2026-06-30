# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

This file is routing guidance. Do not create missing domain docs during setup.

## Layout

This is a single-context repo.

Use:

- `CONTEXT.md` at the repo root for shared domain language, when it exists.
- `docs/adr/` at the repo root for architectural decisions, when it exists.

If either file or directory does not exist, proceed silently. Do not flag its absence or suggest creating it upfront. The `$domain-modeling` skill, reached via `$grill-with-docs` and `$improve-codebase-architecture`, creates domain docs lazily when terms or decisions actually get resolved.

## Use The Glossary's Vocabulary

When your output names a domain concept in an issue title, refactor proposal, hypothesis, or test name, use the term as defined in `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If the concept you need is not in the glossary yet, that is a signal: either you are inventing language the project does not use, or there is a real gap to note for `$domain-modeling`.

## Flag ADR Conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> Contradicts ADR-0007 (event-sourced orders), but worth reopening because...
