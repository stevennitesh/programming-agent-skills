# Language Direction

This synthesis note promotes the actionable findings from
[`../research/language/02-upstream-skill-pack-audit.md`](../research/language/02-upstream-skill-pack-audit.md).

Research found that this repo's active skills are stronger as an execution
system, while Matt Pocock's upstream skill pack is stronger as a vocabulary
source. The direction is not to revert to upstream. The direction is a hybrid:
Matt's memorable vocabulary plus this repo's stronger contracts.

## Canonical Language

Use these terms consistently going forward:

- **ready-for-agent**: the canonical tracker role.
- **AFK-ready**: human-readable shorthand for work safe enough for an agent while the human is away.
- **independently-grabbable issue**: an issue a fresh session can pick up without rereading the whole PRD.
- **tracer-bullet vertical slice**: a narrow behavior through the real system that proves an observable path.
- **support issue**: bounded, independently verifiable work that unblocks or de-risks tracer bullets.
- **grilling session**: the ambiguity-reduction interview before committing to a plan.
- **shared language**: the outcome captured in `CONTEXT.md`.
- **domain model**: the structured project vocabulary and concepts behind the shared language.
- **ADR-worthy decision**: hard to reverse, surprising without context, and the result of a real trade-off.
- **red-green-refactor**: the TDD cycle used one tracer bullet at a time.
- **fixed-point review**: review a diff against a known starting ref.
- **Standards and Spec**: the two axes of review.
- **explicit-only / implicitly invocable**: Codex-native invocation controls.
- **user-invoked / model-invoked**: conceptual explanation of the invocation axis.

## Proposed Changes

Do not revert `skills/current/` to upstream. Instead:

1. Update `ask-matt` to restore `main flow`, `on-ramp`, `standalone`, `grilling session`, and `independently-grabbable`, while keeping the current routes.
2. Update `to-issues` to prefer `independently-grabbable issues` and explain `AFK-ready` beside `ready-for-agent`.
3. Update `tdd` to name `red-green-refactor` in the description and first paragraph.
4. Update README wording to reduce `Codex-ready` in public-facing sections and prefer `ready-for-agent` / `AFK-ready`.
5. Audit the validator so it does not block Matt vocabulary that carries intent, especially `AFK`, `agent-ready`, `user-invoked`, `model-invoked`, `shared language`, and `grilling session`.

## Boundary

This file owns the chosen language direction. The research audit owns evidence
and comparison. Runtime skills own active behavior only after their `SKILL.md`
files are edited.
