# Domain Docs

How engineering skills consume repo domain documentation when exploring codebase context.

This file is routing guidance. It points agents to relevant glossary and ADR files without loading all domain docs by default. Do not create missing domain docs during setup.

## Before Exploring

Read only the domain docs relevant to the selected issue, interface, bounded slice, or changed module:

- `CONTEXT.md` at the repo root for single-context repos.
- `CONTEXT-MAP.md` at the repo root for multi-context repos; follow it to relevant context `CONTEXT.md` files.
- `docs/adr/` for repo-wide decisions touching the work.
- `src/<context>/docs/adr/` for context-local decisions in multi-context repos.

If any file or directory is absent, proceed silently. Do not flag its absence or suggest creating it upfront. The `$domain-modeling` skill creates domain docs lazily when terms or decisions get resolved.

## Use Glossary Vocabulary

When your output names a domain concept in an issue title, refactor proposal, hypothesis, test name, commit message, or implementation note, use the term as defined in the relevant `CONTEXT.md`.

If the concept is missing, either reconsider the invented language or note the gap for `$domain-modeling`.

## Flag ADR Conflicts

If your output contradicts an existing ADR, surface it explicitly instead of silently overriding it:

> Contradicts ADR-0007 (event-sourced orders), but worth reopening because...
