# Matt Skill Pack Vocabulary Audit

Durable source and reconstruction: [UPSTREAM-SOURCE.md](UPSTREAM-SOURCE.md).

This document compares Matt Pocock's upstream skills clone in `.tmp/mattpocock-skills/` with this repo's active skills in `skills/custom/`.

The question: do the active skills preserve Matt's method and vocabulary, and where has important language drifted?

## Short Answer

The two packs match on the main engineering methods, but they do not match cleanly on vocabulary.

Matt's clone is more faithful to Matt's native public language:

- `user-invoked` and `model-invoked`
- `main flow`, `on-ramp`, and `standalone`
- `grilling session`
- `shared language`
- `independently-grabbable issues`
- `AFK agent`
- `red-green-refactor`

This repo's `skills/custom/` is more operational and Codex-specific:

- `explicit-only` and `implicitly invocable`
- `ready-for-agent`
- `Codex-ready brief`
- `tracer-bullet vertical slice`
- `bounded slice`
- `support issue`
- `acceptance criteria`
- `fixed-point review`
- `Standards` and `Spec`
- `evidence`

The active skills are stronger as an execution system. Matt's clone is stronger as a vocabulary source.

The best direction is not to revert to upstream wholesale. Keep this repo's stronger contracts, but restore selected Matt vocabulary where it teaches the mental model better.

## What Still Matches

The active skills preserve the core intent:

- Shape unclear work before implementation.
- Preserve shared project language in `CONTEXT.md`.
- Record hard-to-reverse decisions in ADRs.
- Split larger work into vertical slices.
- Prefer tracer bullets over horizontal layer work.
- Use TDD when behavior is clear enough to prove.
- Test behavior through meaningful interfaces and seams.
- Keep implementation scoped to one issue or slice.
- Use review and Git evidence before calling work done.

The divergence is mostly dialect, not philosophy.

## Where This Repo Is Stronger

### Issue Pipeline Discipline

`skills/custom/to-issues` is more precise than upstream about what makes a good implementation issue:

- dependency order
- bounded slices
- acceptance criteria
- blockers
- parent references
- support issues only when they unblock or de-risk tracer bullets
- avoiding stale file paths unless the path is the contract

That is useful. It should stay.

### Implementation Scope

`skills/custom/implement` is much stronger than upstream. It enforces:

- one ready-for-agent issue
- baseline capture
- worktree preservation
- acceptance criteria
- focused verification
- review from a fixed point
- commit and implementation note

Upstream `implement` is intentionally short. This repo's version better encodes the professional "deliberate and scoped coding" behavior.

### TDD As Tracer Bullets

`skills/custom/tdd` connects TDD to tracer-bullet vertical slices, seams, interfaces, observable behavior, and refactoring while green.

Upstream keeps the more recognizable phrase `red-green-refactor`, but this repo better explains how TDD should behave inside the issue pipeline.

### Codebase Design Vocabulary

`skills/custom/codebase-design` gives fuller definitions for:

- module
- interface
- implementation
- depth
- seam
- adapter
- leverage
- locality

This is a strength. The current skill makes the design vocabulary more usable across PRDs, issues, implementation, review, and architecture work.

## Where Matt's Clone Is More Faithful

### Invocation Axis

Upstream centers the split on:

- `user-invoked`
- `model-invoked`
- `disable-model-invocation`

This repo correctly translates the control into Codex terms:

- `explicit-only`
- `implicitly invocable`
- `policy.allow_implicit_invocation: false`

That translation is technically correct for Codex. But when teaching the method, the upstream terms are clearer and more portable. The repo should keep Codex-native config wording, but use `user-invoked` and `model-invoked` as conceptual aliases when explaining the axis.

### Ask Matt Flow Language

Upstream `ask-matt` uses a very clear map:

- `main flow`
- `on-ramps`
- `codebase health`
- `crossing sessions`
- `standalone`

The current `ask-matt` is more compact and operational, but it loses some of that mental model. The active skill should restore the upstream flow vocabulary while preserving this repo's additions, especially `decision-mapping`, `diagnosing-bugs`, `tdd`, and `review`.

### Independently-Grabbable Issues

Upstream says `independently-grabbable issues`.

This repo says `independently pick-up-able bounded slices`.

The upstream phrase is better. It is memorable, plain, and captures the intended behavior: a fresh agent can grab one issue without dragging the whole plan along.

Recommendation: use `independently-grabbable` in `to-issues`, README, and pipeline docs.

### AFK Agent

Upstream uses `AFK agent` and `AFK-ready`.

This repo often says `unattended Codex implementation session` or `delegated implementation subagent`.

The current wording is precise but heavy. `AFK-ready` is a useful shorthand because it names the operating mode: the issue is good enough for an agent to work while the human is away.

Recommendation: prefer `ready-for-agent` as the canonical tracker role, and allow `AFK-ready` as the human-readable explanation.

### Grilling Session

Upstream uses `grilling session` as a named practice.

This repo sometimes thins that into `interview loop`, `questioning`, or route descriptions.

The phrase `grilling session` is part of the pack's personality and intent. It means more than asking questions. It means relentlessly resolving ambiguity before building.

Recommendation: restore `grilling session` in `ask-matt`, `grill-with-docs`, README, and any route explanation.

### Shared Language

Upstream explains `CONTEXT.md` as a way to create a `shared language`.

This repo often uses `domain glossary`, `domain model`, and `domain language`.

Those terms are good, but `shared language` explains the why. It also aligns with DDD and makes the value obvious to engineers, PMs, and domain experts.

Recommendation: use `shared language` as the plain-language framing, and `domain model` / `domain glossary` as the implementation vocabulary.

### Red-Green-Refactor

Upstream explicitly names `red-green-refactor`.

This repo has `RED`, `GREEN`, and `REFACTOR` sections, but the named phrase is less prominent.

Recommendation: restore `red-green-refactor` in the `tdd` description and opening philosophy.

### Make The Change Easy

Upstream keeps the phrase:

> Make the change easy, then make the easy change.

This repo uses `prefactoring` and `support issue`.

The repo's operational terms are good, but the Kent Beck phrase is memorable and teaches the instinct. Keep `prefactoring` and `support issue`, but reintroduce the phrase in `to-issues` and `tdd` where it clarifies why a support slice might exist.

## Vocabulary Drift Table

| Upstream term | Current term | Recommendation |
| --- | --- | --- |
| `user-invoked` | `explicit-only` | Keep `explicit-only` for Codex config; use `user-invoked` as conceptual alias. |
| `model-invoked` | `implicitly invocable` | Keep `implicitly invocable`; use `model-invoked` when explaining the axis publicly. |
| `disable-model-invocation` | `policy.allow_implicit_invocation: false` | Do not restore Claude-only metadata; keep Codex-native policy files. |
| `/skill` | `$skill` | Keep `$skill` for this repo's runtime vocabulary. |
| `main flow` | `Main Flow: Idea -> Ship` | Restore `main flow`, `on-ramp`, and `standalone` as stable map terms. |
| `grilling session` | `interview loop` / `questioning` | Restore `grilling session`. |
| `shared language` | `domain glossary` / `domain model` | Use both: shared language is the outcome, domain model is the mechanism. |
| `independently-grabbable` | `independently pick-up-able` | Prefer `independently-grabbable`. |
| `AFK-ready` | `unattended Codex implementation session` | Use `AFK-ready` as shorthand; keep precise explanation where needed. |
| `agent-ready` | `Codex-ready` / `ready-for-agent` | Prefer `ready-for-agent`; reduce `Codex-ready` in public-facing text. |
| `red-green-refactor` | `RED` / `GREEN` / `REFACTOR` | Restore the named method. |
| `Make the change easy...` | `prefactoring` / `support issue` | Keep both, with the quote as the teaching phrase. |

## Synthesis Promotion

The audit findings that became chosen language direction now live in
[`../../synthesis/language-direction.md`](../../synthesis/language-direction.md).
This file stays as the research comparison; synthesis owns the canonical
language recommendations and proposed changes.

## Final Judgment

This repo is in the right direction.

The active skills are more professional and implementation-ready than upstream. They better encode quality work, speed without sacrificing quality, deliberate scoping, verification, review, and Git hygiene.

But the active folder should borrow back selected Matt vocabulary. Those words are not decoration. They encode the mental model that makes the skill pack teachable:

- how skills are reached,
- how work flows,
- when context should fork,
- what makes an issue safe for an agent,
- and why shared language matters.

The target is a hybrid: Matt's memorable vocabulary plus this repo's stronger
contracts. The accepted direction is tracked in synthesis, not here.
