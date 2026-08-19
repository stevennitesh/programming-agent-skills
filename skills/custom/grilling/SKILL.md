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

**Gap.** Only when no frontier decision can advance and at least one required
branch remains blocked, load
[TERMINAL-GAP-ROUTING.md](references/TERMINAL-GAP-ROUTING.md), select exactly
one terminal gap route, and stop. Otherwise do not load it.

**Return.** Always return status, bound, confirmed decisions, return owner,
`Spec source: ready | not ready | not requested`, and `Downstream execution:
none`. Set `ready` only after Confirm closes, `not ready` when a requested spec
source returns a gap, and `not requested` otherwise. Add caller identifiers
when supplied. For a gap, add its kind, unresolved or missing input, impact,
uninvoked owner, intact gap identity, required result, and exact re-entry
instruction. When applicable, add `Transport: $handoff (uninvoked)` without
changing that owner. Return to the caller or user and stop.
