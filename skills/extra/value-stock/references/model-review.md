# Model Review And Reconciliation

Use this branch only when the main-skill Review Readiness receipt says
`ready: yes` and names the same frozen Model Lock version and calculation
artifact supplied for review. If the receipt is absent, not ready, or
mismatched, return `blocked` to the root without reviewing or repairing the
candidate. Full alone is not a trigger.

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

Give each reviewer the identical frozen Model Lock, calculation artifact, and
Lock-bound review evidence packet. Use fresh context with `fork_turns="none"`
when supported. Review only the supplied candidate and packet. Reviewers may
challenge source meaning, dependencies, conflicts, bounds, assumptions, and
calculations, but may not search for, admit, substitute, or rely on new factual
evidence. Report missing or insufficient source context as a blocked check; the
root owns later evidence collection and admission. Include every locked input
needed for the assigned lens, including terminal or residual inputs. Withhold
the parent's suspected weaknesses, desired conclusion, preferred alternative
assumptions, and other reviewers' output. Reviewers are read-only candidate
finders: they do not mutate, spawn, admit findings, or own the final valuation.

Default to two lenses:

1. **Reproduction and claims** - reproduce the locked value without
   changing assumptions, then inspect claim basis, as-of and intervening-event
   bridges, accounting conventions, cash, debt, awards, dilution, and share
   count.
2. **Economics and required returns** - challenge growth, margins,
   reinvestment, the first forecast cash-flow bridge against admitted reported
   or guided anchors, prior-investment timing, competitive duration, asset
   realization, sector-specific drivers, discount construction, timing,
   terminal or residual economics, probabilities, sensitivities, and whether
   price-implied expectations are conditional or jointly coherent.

Add one focused third reviewer only for a distinct load-bearing disagreement
that neither default lens owns. Run exactly one reproduction-and-claims lens.
Additional reviewers verify the same lock identity, inspect only their assigned
lens, and need not reproduce the entire model. Require:

```text
status: complete | blocked
model lock version:
calculation artifact identity:
lens:
semantic dependencies:
coverage performed:
coverage omitted or blocked:
reproduced value and difference:
findings:
  - finding:
    classification:
    packet evidence or blocked dependency:
    correction or alternative:
    estimated valuation effect:
    confidence:
```

Return every material finding within the assigned lens. Use `findings: none`
only when status is `complete` and no assigned check is omitted; otherwise name
each omitted or blocked check. The root verifies Lock and artifact identity,
reproduction, packet evidence, scope, dependencies, and classification, then
admits or rejects each finding; only the root admits factual evidence. Apply the
main skill's Model Lock invalidation rule after every admitted finding. An
unresolved reproduction, evidence, or mechanical mismatch prevents `complete`.
Any change to the canonical calculation artifact or its unrounded result
invalidates reproduction. If dependency identity cannot be verified, rerun the
affected lens.

Record each finding's root disposition as `rejected`, `corrected`, `bounded`, or
`unresolved`. A bounded disposition identifies its owning conservative evidence
and full valuation effect. When a correction changes load-bearing content, name
the new Lock and the prior gate, reproduction, or review coverage it invalidates;
do not reuse invalidated coverage until it is rerun against that Lock.

If fresh reviewers are unavailable, run separated root passes and disclose
reduced independence. If the user explicitly required independent validation,
return `partial` rather than implying that it occurred.
