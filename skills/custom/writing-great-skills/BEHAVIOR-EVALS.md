# Behavioral Skill Evaluation

Use this read-only proof branch only for a claim that exact skill wording
changes invocation, judgment, action, context loading, Return, or completion.
Read-only means the control, candidate, and repository remain unchanged during
sampling; the branch still runs fresh isolated model executions. Freeze control
and candidate bytes before sampling. Return the parent operation status plus
one evaluation decision.

Use **control** and **candidate** below. A deploy campaign may call them M0 and
H1.

## Register the control

Register `defect-correction` or `quality-lift`. Fix the task, full context,
model, host, reasoning configuration, tools, authority, evidence, runtime,
rubric, and inputs. For defect correction, name the expected failure. For
quality lift, name the meaningful rubric deficit while the control remains
viable.

Record an observable entry predicate. Classify applicability as `common`,
`situational`, `rare`, or `unknown` with its evidence basis; fixture frequency
does not establish prevalence. If the registered control deficit does not
appear, stop before candidate sampling with `reject-no-control-deficit`.

## Freeze the cohorts

Freeze separate entry-positive and wrong-condition cohorts. Keep candidate
language, conclusions, and prior outputs out of control contexts. Keep inputs
fixed. Use the host's fresh-context mechanism; never reuse the authoring
conversation as a sample. Alternate or randomize arm order when practical.
Reuse samples only when their frozen bytes, inputs, and runtime identity are
unchanged. Evidence judgment stays with the root.

## Apply the adaptive gate

Run at least five fresh entry-positive controls. Run at least five fresh
entry-positive candidates only when the registered deficit appears. Run frozen
wrong-condition control/candidate pairs only after the candidate clears the
entry-positive contribution gate. A rejected candidate receives no
wrong-condition samples.

Keep wrong-condition results separate; do not dilute a situational effect with
non-triggering cases. Extend sampling for material variance, a borderline
effect, or protocol deviation. Stop early for a critical regression. Five is a
minimum, not automatic evidence sufficiency.

## Judge conditional efficacy

Inspect every flagged output against the fixed rubric. Strings, headings, and
template echoes are structural evidence only. Accept only when the control
shows the registered deficit, the candidate materially improves it, variance
is acceptably bounded, and no critical or protected-behavior regression appears.

Judge conditional efficacy on entry-positive cases before deciding whether
bounded applicability justifies runtime load. Keep applicability separate from
efficacy.

## Record the result

Record the registration, expected deficit, task, rubric, entry predicate,
applicability basis, fixed inputs, control/candidate hashes, model, host,
reasoning configuration, runtime, tools, authority, evidence, cohort counts and
per-sample results, aggregate, variance, worst result, critical failures,
protocol deviations, unavailable telemetry, decision, and residual transfer
gap.

Choose exactly one evaluation decision: `accept`,
`reject-no-control-deficit`, `reject-insufficient-contribution`,
`reject-regression`, `needs-more-evidence`, or `blocked`, without extrapolation.
Reserve `reject-regression` for an observed critical or protected-behavior
regression.
