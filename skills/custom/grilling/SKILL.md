---
name: grilling
description: Grill the user relentlessly about a bounded plan, decision, or idea until shared understanding is confirmed. Use when the user wants to stress-test their thinking or uses a "grill" trigger phrase. Conversation-only and before action.
---

# Grilling

Interview relentlessly until shared understanding is confirmed. Grilling writes
nothing and starts nothing downstream.

**Bound.** Use caller-supplied subject, authority, identifiers, and return
owner; otherwise the user owns decisions, scope changes, confirmation, and
return. Ask only material choices whose plausible answers change the outcome or
commitment boundary, another material dependency, or a stated human-judgment
consequence.

**Grill.** Find inspectable facts instead of asking. Put decisions to their
owner one at a time, with one recommendation and decisive tradeoff; ask
participant-held facts neutrally. Follow dependency order, incorporate each
answer and deferral, and reopen invalidated decisions. Continue while
clarification advances or corrects a branch; a repeated non-answer makes that
decision authority unavailable.

Under composition, **Relay** every settled material answer and pause dependent
progress until any domain collision or blocker returns. Grilling owns
materiality, not domain consequences.

**Confirm.** Present the decisions, deferrals, and evidence limits. Continue
until confirmation authority explicitly accepts shared understanding.
Confirmation starts nothing.

**Gap.** When one conversation exposes several interdependent unresolved
decisions or non-conversational prerequisites, return `Route gap` with the
intact bound, recommend uninvoked `$wayfinder`, give the exact re-entry
instruction, and stop. Otherwise, when one required branch cannot advance,
return `Evidence gap` with kind `evidence` or `decision authority`, missing
input, impact, exactly one uninvoked owner, and the exact instruction for
returning its result to the original decision owner without changing the gap
identity. Choose `$research` for an authoritative source, `$prototype` for
runnable design evidence, `$diagnosing-bugs` for causal or reproduction
uncertainty, `$to-questionnaire` for an external stakeholder, and the caller or
`none` otherwise. When the intact gap must cross into a fresh context, preserve
that owner and add uninvoked `$handoff` only as transport; Handoff neither
answers nor owns the gap.

**Return.** Always return status, bound, confirmed decisions, return owner, and
`Downstream execution: none`. Add caller identifiers when supplied. For a gap,
add its kind, missing input, impact, uninvoked owner, intact gap identity,
required result, and exact re-entry instruction. When applicable, add
`Transport: $handoff (uninvoked)` without changing that owner. Return to the
caller or user and stop.
