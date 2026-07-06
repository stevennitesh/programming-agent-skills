# Skill Pack Guide AGENTS.md

This is the installed-pack suggestion map. It names the pack's vocabulary and suggests the one next skill when a specialized workflow would help.

It does not teach skill procedures, tracker mechanics, domain routing, labels, or the engineering contract. Repo-local `AGENTS.md` and `docs/agents/*` own those details.

Do not combine this guide with `AGENTS_PORTABLE_FALLBACK.md` in the same Codex profile. The fallback is for repos or environments without the skill pack; this guide is for installed-pack environments.

## North Star

Build faster without making the repo harder to trust.

Use these as routing handles, not procedures:

- **grilling session**: reduce ambiguity before building.
- **decision map**: make fog of war visible.
- **prototype**: answer one design question by trying it.
- **PRD**: preserve product intent beyond the current thread.
- **ready-for-agent**: specific enough for a fresh implementation session.
- **fixed-point review**: review a diff from a known starting point.
- **convergent review**: use independent passes when one review is not enough.
- **handoff**: preserve workflow state for a fresh session.

## Suggestion Index

Use `ask-matt` when route choice is the work.

Suggest shaping skills before implementation:

- `grill-with-docs` when product intent is foggy and repo context matters.
- `grilling` when the user needs a grilling session without repo-doc work.
- `decision-mapping` when unresolved decisions block a PRD, plan, or implementation.
- `prototype` when conversation cannot settle a design question without trying it.
- `handoff` when context must cross sessions.

Suggest product-to-implementation skills:

- `to-prd` when a multi-session idea needs a durable parent PRD before implementation issues.
- `to-issues` when a PRD, spec, plan, or parent issue should become dependency-ordered, ready-for-agent tracer-bullet issues.
- `triage` when incoming issues or external PRs need state roles and ready-for-agent briefs.
- `implement` when one ready-for-agent issue should be implemented, verified, reviewed, committed, and noted.
- `parallel-implement` when a parent, packet, or batch of ready-for-agent issues should be implemented through delegated workers and serialized integration.

Suggest quality-loop skills:

- `tdd` when behavior is clear enough for red-green-refactor.
- `diagnosing-bugs` when the symptom, cause, or reproduction is uncertain.
- `review` when an ordinary branch or work-in-progress diff needs fixed-point Standards and Spec review.
- `convergent-pr-review` when a local PR review or high-risk local-diff review needs independent passes, a finding ledger, and patch-ready triage.

Suggest design and language skills:

- `domain-modeling` for shared language, glossary terms, or ADR-worthy decisions.
- `codebase-design` for module, interface, seam, adapter, depth, leverage, and locality vocabulary.
- `improve-codebase-architecture` for architecture review and deepening candidates.
- `writing-great-skills` for skill language, invocation, context load, and predictability.
- `setup-matt-pocock-skills` when a repo needs the issue tracker, triage labels, domain docs, or engineering contract expected by the pack.

## Boundary

This guide may name leading words and suggest one next route. It must not teach workflows, tracker operations, repo-specific domain rules, label policy, engineering-contract discipline, or invocation mechanics.

If a route depends on missing repo-local setup docs, suggest `setup-matt-pocock-skills`.
