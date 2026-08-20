---
name: grilling
description: Grill one bounded user-owned or approved caller-owned decision until shared understanding is confirmed. Use for direct stress-testing or an invoked conversation-only decision; remain before action.
---

# Grilling

Settle one bounded decision through live questioning. Write nothing and start
nothing downstream.

## 1. Bound

Preserve any caller-supplied subject, decision owner, authority, identifiers,
and return owner. Otherwise the user owns the decision, scope changes,
confirmation, and return. If the subject contains several independent
decisions, first narrow it to one outcome or decision.

Ask only about a choice whose plausible answers could change that outcome, its
commitment boundary, a material dependency, or a stated human-judgment
consequence.

## 2. Learn

Inspect available facts instead of asking the user to retrieve them. For an
engineering choice, trace real callers and existing constraints. A hypothetical
or preferred style is not material without a reachable consequence. Ask
participant-held facts, goals, and constraints neutrally.

## 3. Grill

Maintain the **decision frontier**: material decisions whose prerequisites are
settled. Ask its highest-leverage decision one at a time. Recommend only after
the decision-relevant prerequisites are known, and state the decisive tradeoff.

Recompute after each answer, fact, deferral, or invalidation. Let a blocked
branch pause only its dependents. Treat adoption of the recommendation as a
decision, postponement as a deferral, and inability or refusal to decide as
unavailable authority. Never repeat an unchanged question.

When no frontier decision can advance and a required branch remains blocked,
load [Terminal gap routing](references/TERMINAL-GAP-ROUTING.md), return one gap,
and stop. Otherwise do not load it.

## 4. Confirm and return

Present the decision, reasons, decisive tradeoffs, material deferrals, and
evidence limits. For one decision with no material deferral or evidence limit,
the owner's explicit choice also confirms the understanding. Otherwise obtain
explicit confirmation.

Return the confirmed understanding to the supplied return owner, or to the
user on direct invocation. Include caller identifiers only when supplied. Stop
without selecting or starting downstream work.

Complete when the owner has confirmed one bounded understanding or Grilling has
returned one exact gap it cannot resolve conversationally.
