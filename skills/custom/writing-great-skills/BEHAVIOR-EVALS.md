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
| Behavior is viable but lower quality | Intent-adjacent steering plus a pre-registered comparative rubric |

## Control

Register either `defect-correction` or `quality-lift` before sampling. Fix the
task, full context, model, host, reasoning settings, tools, authority, evidence,
runtime, and rubric. Run without candidate guidance. For defect correction,
name the expected failure. For quality lift, name the meaningful rubric deficit
expected while the control remains viable. Record an observable entry
predicate plus `common`, `situational`, `rare`, or `unknown` applicability with
its evidence basis. Fixture frequency does not establish real-world prevalence.
When neither registered deficit appears, stop before the candidate; the
guidance is a no-op candidate.

## Sample

Freeze separate entry-positive and wrong-condition cohorts. Run at least five
independent entry-positive control samples in fresh contexts. Run at least five
candidate samples only when the registered control deficit appears under that
predicate. Dispatch frozen wrong-condition control/candidate pairs only after
the candidate clears its entry-positive contribution gate; a candidate rejected
earlier receives no further samples. Keep inputs fixed and alternate or
randomize arm order when practical. Use wrong-condition cases to detect false
firing and regression before acceptance; never dilute a situational effect with
non-triggering cases. Extend sampling only for material variance, borderline
effect, or protocol deviation; stop early for a critical candidate regression.

Keep candidate language, conclusions, and prior outputs out of control contexts. Ambient collaboration policy decides whether and how workers run; evidence judgment stays with the root.

## Stress

Stress only discipline failures with realistic competing pressures. Keep authority and mutation boundaries fixed. Shape, omission, invocation, conditional, and completion failures use representative positive and negative tasks instead of invented adversity.

## Judge

Use an explicit behavior rubric. Inspect every flagged output; strings,
headings, and template echoes are structural evidence only. Accept guidance
only when the control demonstrates the registered defect or meaningful quality
deficit, the candidate materially improves it, variance narrows or remains
acceptably bounded, and no new critical failure appears. Judge conditional
efficacy on entry-positive cases, then judge whether its bounded applicability
justifies the runtime load. Keep wrong-condition results separate.

## Record

Record the contribution mode, entry predicate, applicability and evidence
basis, registered control deficit, fixed inputs, entry-positive and
wrong-condition counts, control, candidate, model, host, reasoning
configuration, tools, runtime, hashes, rubric, per-sample results, aggregate,
variance, worst result, critical failures, protocol deviations, unavailable
telemetry, decision, and residual transfer gap.

## Completion

Complete when the record is current and supports `accept`,
`reject-no-control-deficit`, `reject-insufficient-contribution`,
`reject-regression`, `needs-more-evidence`, or `blocked` without
extrapolation. Reserve `reject-regression` for an actual critical or protected
behavior regression.
