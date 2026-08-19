# Behavioral evaluation

Load this reference only when the user explicitly asks to test, compare, or
measure how wording changes agent behavior. Keep the evaluation read-only.
Freeze the control, candidate, task, inputs, runtime, authority, and rubric
before sampling.

## Compare behavior

Name the expected failure or quality deficit and the observable condition that
should expose it. Start with one fresh control and candidate sample on the same
representative input. Inspect their actual outputs against the fixed rubric.

Add samples only when the result varies, the difference is borderline, or the
claim spans materially different conditions. Add a wrong-condition pair when
the wording could activate outside its intended trigger. Keep candidate wording
and earlier outputs out of control contexts. Stop when the evidence supports a
decision or exposes a material regression.

Conclude that the candidate improves behavior only when the control exposes the
registered deficit, the candidate materially improves it, and no protected
behavior regresses. Keep applicability separate from efficacy. Report the
inputs, relevant identities, observed results, deviations, and limits needed to
support that conclusion. Do not create a durable report unless the user asks
for one or the repository requires it.
