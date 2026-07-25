# Behavioral Skill Evaluation

Use this procedure only for a claim that exact skill wording changes
invocation, judgment, action, context loading, Return, or completion.

## Register the control

Register `defect-correction` or `quality-lift` before sampling. Fix the task,
full context, model, host, reasoning configuration, tools, authority,
evidence, runtime, and rubric. For defect correction, name the expected
failure. For quality lift, name the meaningful rubric deficit expected while
the control remains viable.

Record an observable entry predicate and classify applicability as `common`,
`situational`, `rare`, or `unknown` with its evidence basis. Fixture frequency
does not establish real-world prevalence. If the registered control deficit
does not appear, stop before H1 with `reject-no-control-deficit`.

## Freeze the cohorts

Freeze separate entry-positive and wrong-condition cohorts. Keep candidate
language, conclusions, and prior outputs out of control contexts. Keep inputs
fixed, use fresh contexts, and alternate or randomize arm order when practical.
Ambient collaboration policy decides dispatch; evidence judgment stays with
the root.

## Apply the adaptive gate

Run at least five fresh M0 entry-positive controls. Run at least five fresh H1
entry-positive samples only when the registered M0 defect or meaningful
quality deficit appears. Run frozen wrong-condition M0/H1 pairs only after H1
clears the entry-positive contribution gate. A rejected entry-positive
candidate receives no wrong-condition samples.

Keep wrong-condition results separate; do not dilute a situational effect with
non-triggering cases. Extend sampling for material variance, a borderline
effect, or protocol deviation, and stop early for a critical regression. Five
samples are a minimum floor, not automatic evidence sufficiency.

## Judge conditional efficacy

Inspect every flagged output against the fixed behavior rubric. Strings,
headings, and template echoes are structural evidence only. Accept only when
M0 demonstrates the registered defect or meaningful quality deficit, H1
materially improves it, variance narrows or remains acceptably bounded, and no
critical or protected-behavior regression appears.

Judge conditional efficacy on entry-positive cases before judging whether its
bounded applicability justifies runtime load. Keep applicability evidence
separate from efficacy and do not infer prevalence from fixture frequency.

## Record the result

Record contribution mode, entry predicate, applicability and basis,
registered control deficit, fixed inputs, entry-positive and wrong-condition
counts, model, host, reasoning configuration, tools, authority, evidence,
runtime identities, hashes, rubric, per-sample results, aggregate, variance,
worst result, critical failures, protocol deviations, unavailable telemetry,
decision, and residual transfer gap.

Complete with exactly one of `accept`, `reject-no-control-deficit`,
`reject-insufficient-contribution`, `reject-regression`,
`needs-more-evidence`, or `blocked`, without extrapolation. Reserve
`reject-regression` for an observed critical or protected-behavior regression.
