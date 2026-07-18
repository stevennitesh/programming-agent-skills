# Behavioral Skill Evaluation

Prove that guidance changes behavior, not merely prose.

## Diagnose

Classify the observed failure before choosing its instruction form:

| Failure | Instruction form |
| --- | --- |
| A known discipline is abandoned under pressure | Positive gate plus only observed, necessary guardrails |
| Output has the wrong shape | Ordered positive contract |
| A required element is omitted | Required field, slot, or schema |
| Behavior fires under the wrong condition | Observable predicate |

## Control

Run the realistic task in its full context without the candidate guidance. Keep runtime, model settings, tools, and task evidence fixed.

Stop when the control does not exhibit the claimed failure. Guidance without a demonstrated failure is a no-op candidate.

## Sample

Run control and candidate arms in fresh contexts. Use at least five independent samples per arm for a behavioral claim. Record the runtime, settings, skill hash, scenario, result, and variance.

When available, run fresh-context samples as direct read-only subagents with `fork_turns="none"`. Keep the scenario, evidence, runtime settings, and rubric fixed across arms.

## Stress

Stress only discipline failures. Combine realistic pressures that compete with the owned gate while preserving the actual authority and mutation boundary.

Shape, omission, and conditional failures use representative tasks, not adversarial pressure.

## Judge

Score the promised behavior through an explicit rubric. Inspect every flagged output; string matches and template echoes are not behavioral proof.

Accept guidance only when the control demonstrates the failure, the candidate materially reduces it, variance narrows, and no new critical failure appears.

## Completion

Complete when the failure, control, candidate, runtime, samples, rubric, observed behavior, variance, and residual gap are recorded.
