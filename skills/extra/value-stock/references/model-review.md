# Model Review And Reconciliation

Use this branch only when the user requests independent validation, the locked
calculation does not reproduce, or complex claims, conventions, methods, or
alternative values could materially change the conclusion. Full alone is not a
trigger.

## Classify The Difference

| Difference | Required action |
| --- | --- |
| Conflicting reported fact | Resolve from the owning source |
| Arithmetic, timing, cash-flow/rate, or claim mismatch | Repair before completion |
| Defensible accounting convention | Choose one base; show the alternative sensitivity |
| Forecast judgment | Preserve as a causal scenario |
| Valuation-method difference | Explain what each method measures |
| Unsupported difference | Reject |

Recompute one canonical valuation from the Model Lock after admitted
corrections. Never average targets, select their median, or treat reviewer count
as evidence.

## Fresh Challenge When Supported

Give each reviewer the identical Model Lock and factual source packet. Use
fresh context with `fork_turns="none"` when supported. Include every locked
input needed for the assigned lens, including terminal or residual inputs.
Withhold the parent's suspected weaknesses, desired conclusion, preferred
alternative assumptions, and other reviewers' output. Reviewers are read-only
candidate finders: they do not mutate, spawn, admit findings, or own the final
valuation.

Default to two lenses:

1. **Reproduction and claims** - reproduce the locked value without
   changing assumptions, then inspect claim basis, accounting conventions,
   cash, debt, awards, dilution, and share count.
2. **Economics and required returns** - challenge growth, margins,
   reinvestment, competitive duration, asset realization, sector-specific
   drivers, discount construction, timing, terminal or residual economics,
   probabilities, sensitivities, and price-implied expectations.

Add one focused third reviewer only for a distinct load-bearing disagreement
that neither default lens owns. Run exactly one reproduction-and-claims lens.
Additional reviewers verify the same lock identity, inspect only their assigned
lens, and need not reproduce the entire model. Require:

```text
status: complete | blocked
lens:
reproduced value and difference:
finding:
classification:
evidence:
correction or alternative:
estimated valuation effect:
confidence:
```

The root verifies the lock identity, reproduction, evidence, scope, and
classification; then admits or rejects each finding and recomputes the model.
An unresolved reproduction, evidence, or mechanical mismatch prevents
`complete`.

If fresh reviewers are unavailable, run separated root passes and disclose
reduced independence. If the user explicitly required independent validation,
return `partial` rather than implying that it occurred.
