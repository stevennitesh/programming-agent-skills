---
name: grilling
description: Grill the user relentlessly about a bounded plan, decision, or idea until shared understanding is confirmed. Use when the user wants to stress-test their thinking or uses a "grill" trigger phrase. Conversation-only and before action.
---

# Grilling

Interview relentlessly until shared understanding is confirmed. Grilling writes nothing and starts nothing downstream.

**Bound.** Use caller-supplied subject, authority, identifiers, and return owner; otherwise the user owns decisions, scope changes, confirmation, and return. Ask only material choices whose plausible answers change the outcome or commitment boundary, another material dependency, or a stated human-judgment consequence.

**Grill.** Find inspectable facts instead of asking. Put decisions to their owner one at a time, with one recommendation and decisive tradeoff; ask participant-held facts neutrally. Follow dependency order, incorporate each answer and deferral, and reopen invalidated decisions. Continue while clarification advances or corrects a branch; a repeated non-answer makes that decision authority unavailable.

Under composition, **Relay** every settled material answer and pause dependent progress until any domain collision or blocker returns. Grilling owns materiality, not domain consequences.

**Confirm.** Present the decisions, deferrals, and evidence limits. Continue until confirmation authority explicitly accepts shared understanding. Confirmation starts nothing.

**Gap.** When required branches remain and neither evidence nor available authority can advance them, return `Evidence gap` with kind `evidence` or `decision authority`, missing input, impact, and exactly one uninvoked owner. Choose `$research` for an authoritative source, `$prototype` for runnable design evidence, `$diagnosing-bugs` for causal or reproduction uncertainty, `$to-questionnaire` for an external stakeholder, `$handoff` for cross-session continuation, and the caller or `none` otherwise.

**Return.** Always return status, bound, confirmed decisions, return owner, and `Downstream execution: none`. Add caller identifiers when supplied. For `Evidence gap`, add kind, missing input, impact, and uninvoked owner. Return to the caller or user and stop.
