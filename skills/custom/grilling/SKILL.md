---
name: grilling
description: Grill one bounded user-owned or approved caller-owned decision until shared understanding is confirmed. Use for direct stress-testing or an invoked conversation-only decision; remain before action.
---

# Grilling

Interview relentlessly until shared understanding is confirmed. Grilling writes
nothing and starts nothing downstream.

**Bound.** Use caller-supplied subject, authority, identifiers, intended result,
and return owner; otherwise the user owns decisions, scope changes,
confirmation, and return. Treat an intended result as a readiness target only
when it changes completion. Ask only material choices whose plausible answers
change the outcome or commitment boundary, another material dependency, or a
stated human-judgment consequence.

**Grill.** Find inspectable facts instead of asking. Maintain the **decision
frontier**: material decisions whose prerequisites are settled. Put its
highest-leverage decision to its owner one at a time, with one recommendation
and decisive tradeoff; ask participant-held facts neutrally. Recompute after
each answer, deferral, fact, or invalidation. Let blocked evidence pause only
its dependent branches. Continue while clarification advances or corrects a
branch; a repeated non-answer makes that decision authority unavailable.

Under composition, **Relay** every settled material answer and pause dependent
progress until any domain collision or blocker returns. Grilling owns
materiality, not domain consequences.

**Confirm.** Present the decisions, deferrals, evidence limits, and applicable
readiness assessment. When the intended result is a spec source, treat
readiness as an exit test, never a question filter: challenge every unresolved
assumption that could change purpose or outcome, scope, non-goals, or
limitations, observable behavior or Invariants, applicable failure, state,
security, privacy, compatibility, or lifecycle behavior, a decision or owner,
or acceptance and proof. Each material concern must be settled, excluded, an
owned nonblocking deferral whose answer cannot change the parent commitment, or
a blocking gap. Continue until confirmation authority explicitly accepts the
presented shared understanding. Confirmation starts nothing.

**Gap.** When the bounded interview cannot close in one conversation because
several interdependent unresolved decisions or non-conversational prerequisites
need a tracker-backed multi-session route, return `Route gap` with kind
`multi-decision route`, the intact bound, unresolved branches or prerequisites,
and impact. When active `$wayfinder` is the return owner, return the intact gap
to it for graph reconciliation without recommending another Wayfinder. Otherwise
recommend uninvoked `$wayfinder`, give the exact re-entry instruction, and stop.
When no `Route gap` applies, only when no frontier decision can advance and one
required branch remains blocked, return `Evidence gap` with kind
`evidence` or `decision authority`, missing input, impact, exactly one uninvoked
owner, and the exact instruction for returning its result to the original
decision owner without changing the gap identity. Choose `$research` for an
authoritative source, `$prototype` for runnable design evidence,
`$to-questionnaire` for an external stakeholder, and the caller or `none`
otherwise. Mark causal or reproduction uncertainty `diagnosis-required`. When
the intact gap must cross into a fresh context, preserve that owner and add
uninvoked `$handoff` only as transport; Handoff neither answers nor owns the gap.

**Return.** Always return status, bound, confirmed decisions, return owner,
`Spec source: ready | not ready | not requested`, and `Downstream execution:
none`. Set `ready` only after Confirm closes, `not ready` when a requested spec
source returns a gap, and `not requested` otherwise. Add caller identifiers
when supplied. For a gap, add its kind, unresolved or missing input, impact,
uninvoked owner, intact gap identity, required result, and exact re-entry
instruction. When applicable, add `Transport: $handoff (uninvoked)` without
changing that owner. Return to the caller or user and stop.
