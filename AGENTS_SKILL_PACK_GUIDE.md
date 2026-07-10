# Skill Pack Guide AGENTS.md

Installed-pack suggestion map. It names routing handles and suggests one next skill when a specialized workflow would help.

Do not combine this guide with `AGENTS_PORTABLE_FALLBACK.md`; that file is for environments without the installed skill pack.

Repo-local `AGENTS.md` primes. `docs/agents/*` owns tracker, labels, domain routing, and engineering-contract details. Skills own procedures.

North star: build faster without making the repo harder to trust.

## Routing Handles

- **grilling session**: reduce ambiguity before building.
- **wayfinding map**: make fog of war visible.
- **research note**: answer source questions with primary-source trace.
- **prototype**: answer one design question by trying it.
- **spec**: preserve product intent beyond the current thread.
- **ready-for-agent**: specific enough for a fresh implementation session.
- **fixed-point review**: review a diff from a known starting point.
- **conflict resolution**: preserve both intents through a Git conflict.
- **convergent review**: use independent passes when one review is not enough.
- **handoff**: preserve workflow state for a fresh session.

## Suggestion Index

Recommend `ask-matt` when route choice is the work.

Shape:

- `grill-with-docs` when product intent is foggy and repo context matters.
- `grilling` when the user needs a grilling session without repo-doc work.
- `wayfinder` when unresolved decisions block a spec, plan, or implementation.
- `research` when a source question needs a primary-source note.
- `prototype` when conversation cannot settle a design question without trying it.
- `handoff` when context must cross sessions.

Build:

- `to-spec` when a multi-session idea needs a durable parent spec before implementation issues.
- `to-tickets` when a spec, plan, or parent issue should become dependency-ordered, ready-for-agent tracer-bullet issues.
- `triage` when incoming issues or external PRs need state roles and ready-for-agent briefs.
- `implement` when one ready-for-agent issue should be implemented, verified, reviewed, committed, and noted.
- `parallel-implement` when a parent, packet, or batch of ready-for-agent issues should be implemented through delegated workers and serialized integration.

Quality:

- `tdd` when behavior is clear enough for red-green-refactor.
- `diagnosing-bugs` when the symptom, cause, or reproduction is uncertain.
- `resolving-merge-conflicts` when a merge, rebase, cherry-pick, revert, or conflict marker needs source-traced resolution.
- `review` when an ordinary branch or work-in-progress diff needs fixed-point Standards and Spec review.
- `convergent-pr-review` when a local PR review or high-risk local-diff review needs independent passes, a finding ledger, and patch-ready triage.

Design:

- `domain-modeling` for shared language, glossary terms, or ADR-worthy decisions.
- `codebase-design` for module, interface, seam, adapter, depth, leverage, and locality vocabulary.
- `improve-codebase-architecture` for architecture review and deepening candidates.
- `writing-great-skills` for skill language, invocation, context load, and predictability.
- `setup-matt-pocock-skills` when a repo needs the verified setup surface expected by the pack.

## Boundary

This guide may name leading words and suggest one next route. It must not teach workflows, tracker operations, repo-specific domain rules, label policy, engineering-contract discipline, or invocation mechanics.

If a route depends on missing repo-local setup docs, suggest `setup-matt-pocock-skills`.
