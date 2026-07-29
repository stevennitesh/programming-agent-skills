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
fresh context with `fork_turns="none"` when supported. Withhold parent
hypotheses, preferred conclusions, peer output, and terminal cues. Reviewers are
read-only candidate finders: they do not mutate, spawn, admit findings, or own
the final valuation.

Dispatch only warranted lenses, at most three:

1. **Reproduction and claims** - first reproduce the locked value without
   changing assumptions, then inspect claim basis, accounting conventions,
   cash, debt, awards, dilution, and share count.
2. **Business or asset economics** - challenge growth, margins, reinvestment,
   competitive duration, asset realization, and sector-specific drivers.
3. **Required returns and residual value** - challenge discount construction,
   timing, terminal or residual economics, probabilities, sensitivities, and
   price-implied expectations.

Every independent branch includes the first lens. Require:

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
