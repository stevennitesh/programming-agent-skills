# Target Spine

This document promotes the language research into the common synthesis target
for the skill pack.

It is not runtime skill text. It is the sequence future skills should compress
into their own process, gates, and completion criteria.

## Canonical Target Spine

```text
product intent
  -> shared language / domain model
  -> acceptance criteria
  -> bounded tracer-bullet slice
  -> red-green-refactor when suitable
  -> seam / interface proof
  -> semantic correctness
  -> evidence
  -> fixed-point review
  -> residual risk / follow-ups
```

## Agentic Bridge Variant

Use this variant when a skill needs to express how an LLM should operate, not
only what engineering practice it should recruit.

```text
product intent
  -> context engineering
  -> shared language / domain model
  -> bounded slice
  -> tracer-bullet trajectory
  -> agent-computer interface
  -> reason-act loop
  -> feedback signal
  -> evaluation harness
  -> evidence
  -> fixed-point review
  -> residual risk
```

This preserves the software-engineering target while adding the terms that tell
an LLM how to operate.

## What Each Step Recruits

| Step | What It Should Make The Agent Do |
| --- | --- |
| `product intent` | Start from the outcome the work exists to create, not the first technical task that appears. |
| `shared language / domain model` | Preserve the repo's real concepts in issues, code, tests, PRDs, commits, and notes. |
| `acceptance criteria` | Turn intent into observable pass/fail commitments. |
| `bounded tracer-bullet slice` | Build one narrow real-system path before adding breadth or adjacent cases. |
| `red-green-refactor when suitable` | Use test-first proof when behavior is clear enough to drive through a useful seam. |
| `seam / interface proof` | Prove behavior through the strongest practical boundary instead of brittle internals or shallow output checks. |
| `semantic correctness` | Check that the result means the right thing, not merely that an artifact exists. |
| `evidence` | Back claims with tests, fixtures, logs, diffs, screenshots, CI, commands, rendered output, or user confirmation. |
| `fixed-point review` | Compare the diff against a known starting ref on both Standards and Spec. |
| `residual risk / follow-ups` | Report what remains uncertain or intentionally out of scope instead of widening the slice. |

## Skill-Writing Formula

Each skill should translate the target spine into its own surface:

```text
Use <software-engineering taste term>
through <agent execution surface>
until <checkable evidence gate>.
```

Examples:

```text
Use a bounded tracer-bullet slice
through one real user/caller/operator path
until the acceptance criteria are proven and adjacent work is recorded as follow-up.
```

```text
Use red-green-refactor
through the highest useful interface or seam
until the test has failed for the right reason, passed with the smallest implementation, and refactoring preserves behavior.
```

```text
Use fixed-point review
against the starting ref
until Standards and Spec have both been checked, every finding is actionable and source-backed, and residual risk is named.
```

## Guardrails

- Do not use the whole target spine in every skill.
- Choose the part of the target spine that changes the skill's behavior.
- Prefer strong terms that recruit professional priors.
- Pair each strong term with an agent execution instruction.
- End each runtime step with a checkable completion criterion.
- Keep exploratory vocabulary in research until it has a proven runtime job.

## Vocabulary Promotion Rule

A vocabulary item is ready to move from research into runtime wording when it:

- changes agent behavior compared with ordinary instructions;
- points to a high-quality professional practice or a real agent-control surface;
- can be paired with a concrete evidence gate;
- does not duplicate a stronger term already in the skill or engineering contract;
- survives a pruning pass for no-ops, sediment, and sprawl.
