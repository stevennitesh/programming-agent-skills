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
| Invocation misses or false-fires | One distinct trigger per branch plus positive and adjacent negative cases |
| A step ends early | Sharper checkable criterion first; context split only after the failure persists |

## Control

Fix the task, full context, model, reasoning settings, tools, authority, evidence, runtime, and rubric. Run without the candidate guidance. Stop when the claimed failure does not appear; the guidance is a no-op candidate.

## Sample

Run control and candidate arms in fresh contexts with at least five independent samples per arm for a behavioral claim. Keep inputs fixed. Alternate or randomize arm order when practical.

Keep candidate language, conclusions, and prior outputs out of control contexts. Ambient collaboration policy decides whether and how workers run; evidence judgment stays with the root.

## Stress

Stress only discipline failures with realistic competing pressures. Keep authority and mutation boundaries fixed. Shape, omission, invocation, conditional, and completion failures use representative positive and negative tasks instead of invented adversity.

## Judge

Use an explicit behavior rubric. Inspect every flagged output; strings, headings, and template echoes are structural evidence only. Accept guidance only when the control demonstrates the failure, the candidate materially improves compliance, variance narrows or remains acceptably bounded, and no new critical failure appears.

## Record

Record the failure, fixed inputs, control, candidate, sample count, runtime, hashes, rubric, per-sample results, aggregate, variance, worst result, critical failures, protocol deviations, unavailable telemetry, decision, and residual gap.

## Completion

Complete when the record is current and supports `accept`, `reject-no-control-failure`, `reject-regression`, `needs-more-evidence`, or `blocked` without extrapolation.
