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

Give each reviewer the identical Model Lock and factual source packet. Use
fresh context with `fork_turns="none"` when supported. Include every locked
input needed for the assigned lens, including terminal or residual inputs.
Withhold the parent's suspected weaknesses, desired conclusion, preferred
alternative assumptions, and other reviewers' output. Reviewers are read-only
candidate finders: they do not mutate, spawn, admit findings, or own the final
valuation.

Default to two lenses:

1. **Reproduction and claims** - reproduce the locked value without
   changing assumptions, then inspect claim basis, as-of and intervening-event
   bridges, accounting conventions, cash, debt, awards, dilution, and share
   count.
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
    evidence:
    correction or alternative:
    estimated valuation effect:
    confidence:
```

Return every material finding within the assigned lens. Use `findings: none`
only when status is `complete` and no assigned check is omitted; otherwise name
each omitted or blocked check. The root verifies the lock identity,
reproduction, evidence, scope, and classification; then admits or rejects each
finding and recomputes the model. An unresolved reproduction, evidence, or
mechanical mismatch prevents `complete`.

After an admitted correction, rerun each lens whose locked input, formula,
source meaning, assigned claim, classification, or reproduced result could
change. Carry an unaffected lens forward only after the root verifies that
every load-bearing dependency consumed by it is unchanged. Any change to the
canonical calculation artifact or its unrounded result invalidates
reproduction. If identity or dependency cannot be verified, rerun the affected
packet; never synthesize coverage across Lock versions without that check.

If fresh reviewers are unavailable, run separated root passes and disclose
reduced independence. If the user explicitly required independent validation,
return `partial` rather than implying that it occurred.
