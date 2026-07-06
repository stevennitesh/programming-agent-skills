# Skill Pack Guide AGENTS.md

This is an environment-wide guide for repos where this skill pack is installed.

Most workflow skills in this pack are explicit-only. Do not silently run explicit-only skills and do not recreate their procedures here. A few quality-loop skills are model-invocable by design. This file is a suggestion index: preserve the pack's vocabulary, shape the agent's taste, and suggest the one next skill when a specialized explicit-only workflow would help.

Do not combine this guide with `AGENTS_PORTABLE_FALLBACK.md` in the same Codex profile. The fallback is for repos or environments without the skill pack; this guide is for installed-pack environments.

Repo-local `AGENTS.md` and `docs/agents/*` files own tracker, domain, label, and engineering-contract details. Use this guide as the environment-wide taste and routing layer.

## North Star

Build faster without making the repo harder to trust.

Good agentic coding is deliberate and scoped. This guide keeps the pack's leading words active so Codex can route to the right skill or repo-local discipline.

Language shapes behavior. Use these terms as attention handles, not full procedures:

- **grilling session**: reduce ambiguity before building.
- **decision map**: make fog of war visible instead of guessing.
- **PRD**: preserve product intent beyond the current thread.
- **tracer bullet**: prove one real path through the system.
- **vertical slice**: split by observable behavior, not technical layer.
- **ready-for-agent**: specific enough for a fresh session without hidden context.
- **acceptance criteria**: done has observable proof.
- **red-green-refactor**: test-first work when behavior is clear enough to prove.
- **interface**, **seam**, **deep module**: improve leverage, locality, and testability.
- **fixed-point review**: check the diff against a known starting point.
- **commitment boundary**: requirements, semantic correctness, and end result belong to the user; internal technique belongs to the agent unless internal behavior is load-bearing for that result.
- **load-bearing internal**: internal behavior that determines whether the requested result is correct; it needs a contract and proof through the smallest meaningful seam.
- **evidence**: source, tests, fixtures, logs, diffs, command output, CI, or explicit user confirmation.

## Suggestion Behavior

If the user explicitly names a skill, use that skill.

If no skill is named and the task is tiny or clear, continue normally.

If no skill is named but a model-invocable skill clearly matches, use it.

If no skill is named but a specialized explicit-only skill would clearly improve the work, suggest one next skill and why.

If several routes plausibly fit, suggest `ask-matt`.

Do not simulate unavailable skills or copy a skill's hidden workflow into this file.

## Suggestion Index

Use `ask-matt` when route choice is the work.

Suggest shaping skills before implementation:

- `grill-with-docs` when product intent is foggy and repo context matters.
- `grilling` when the user needs a grilling session without repo-doc work.
- `decision-mapping` when unresolved decisions block a PRD, plan, or implementation.
- `prototype` when a runnable answer is needed before deciding.
- `handoff` when context must cross sessions.

Suggest product-to-implementation skills:

- `to-prd` when an idea needs a durable PRD.
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

Suggest experimental routes only when the user explicitly asks for them or has installed and named them:

- `to-slice-plan`
- `next-slice`
- `slice-plan-runner`

## Boundary

This guide may name leading words. It must not teach the coding loop, proof steps, review procedure, tracker operations, or repo-specific domain rules.

Repo-local `docs/agents/domain.md` owns domain-doc routing; use it to find relevant glossary and ADR context when a skill asks for domain docs.

For actual coding work, follow the target repo's `AGENTS.md` and `docs/agents/engineering-contract.md`. If they are missing and the work needs the pack's repo-local contract, suggest `setup-matt-pocock-skills` instead of recreating that contract here.
