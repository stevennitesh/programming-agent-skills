---
name: grilling
description: Grill the user relentlessly, one question at a time, until shared understanding of a bounded plan, design, decision, or idea is explicitly confirmed. Conversation-only and before action.
---

# Grilling

**Outcome:** shared understanding of one bounded plan, design, decision, or idea, left unexecuted.

**Boundary.** Inspect available evidence read-only. Keep recommendations advisory. Write nothing and start no downstream work.

**Bound.** Lock the subject, participant and decision authority, Bound authority, Confirmation authority, caller identity and opaque identifiers when supplied, and return owner. Direct use defaults the authorities and return owner to the user. A fresh session requires at least one unresolved material decision. A choice is material only when its answer changes the outcome, scope, acceptance, contract, risk, irreversible commitment, another material dependency, or a stated human-judgment consequence. Bound authority must accept the known impact of any deferral that weakens the outcome.

**Find.** Resolve inspectable facts yourself. Mark support as cited, participant-supplied, or inferred. Missing evidence or unavailable authority blocks only dependent decisions.

**Grill.** Maintain the frontier of unresolved in-bound material decisions whose prerequisites are settled and decision authority is available. Choose the one with greatest downstream leverage. Ask exactly one thing and wait: recommend an answer and decisive tradeoff for a choice; ask a participant-held fact neutrally.

**Integrate.** Incorporate the answer, preserve material alternatives and deferrals, reopen invalidated decisions, and classify new branches as prerequisites, deferrals, or Bound-authority scope changes. Under `$grill-with-docs` composition, return each settled material answer with the shared subject, source, and relevant opaque identifiers, then pause dependent questioning. Integrate the returned domain collision or blocker and reopen every affected branch before continuing; never classify the domain consequence yourself. Continue `Find -> Grill -> Integrate` until every in-bound material branch is resolved or validly deferred. Permit one focused clarification; return an authority gap instead of rephrasing indefinitely.

**Confirm.** Present the decisions, deferrals, and evidence limits. Continue grilling until Confirmation authority explicitly accepts shared understanding. A correction reopens the loop. Confirmation authorizes no next action.

**Gap.** When unresolved branches remain but neither evidence nor available decision authority can advance them, return `Evidence gap` with kind `evidence` or `decision authority`, the exact missing input, and its impact. Name exactly one uninvoked blocking owner: `$research` for an authoritative source, `$prototype` for runnable design evidence, `$diagnosing-bugs` for causal or reproduction uncertainty, `$to-questionnaire` for an external stakeholder, `$handoff` for cross-session work, and the caller or `none` otherwise. Return the gap and stop.

**Return.** Return `Confirmed` or `Evidence gap`, the bound, confirmed decisions, populated supporting details, caller identity and opaque identifiers when supplied, return owner, and `Downstream execution: none`. Return to the caller or user and stop.
