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
does not establish real-world prevalence. When the registered control deficit
does not appear, stop before the candidate and return
`reject-no-control-deficit`.

## Freeze and sample

Freeze separate entry-positive and wrong-condition cohorts. Run at least five
independent entry-positive M0 controls in fresh contexts. Run at least five H1
entry-positive samples only when the registered M0 deficit appears. Keep
inputs fixed and alternate or randomize arm order when practical.

Dispatch frozen wrong-condition M0/H1 pairs only after H1 clears its
entry-positive contribution gate. Keep wrong-condition results separate; do
not dilute a situational effect with non-triggering cases. Extend sampling for
material variance, a borderline effect, or protocol deviation, and stop early
for a critical regression. Five samples are a minimum floor, not an automatic
sufficiency rule.

Keep candidate language, conclusions, and prior outputs out of control
contexts. Ambient collaboration policy decides dispatch; evidence judgment
stays with the root.

## Judge

Inspect every flagged output against the fixed behavior rubric. Strings,
headings, and template echoes are structural evidence only. Accept guidance
only when M0 demonstrates the registered defect or meaningful quality deficit,
H1 materially improves it, variance narrows or remains acceptably bounded,
and no critical or protected-behavior regression appears.

Judge conditional efficacy on entry-positive cases before judging whether its
bounded applicability justifies runtime load. A rejected entry-positive
candidate receives no wrong-condition samples.

## Record

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
