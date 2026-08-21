---
name: grill-with-docs
description: Use when one user-owned repo-backed decision needs live grilling while its domain meaning, invariants, or relationships are kept current; exclude conversation-only grilling and already-settled domain capture.
---

# Grill With Docs

Grill one repo-backed decision while keeping its domain meaning current.

## 1. Bound

Use this only when one bounded user-owned decision needs both live questioning
and domain reconciliation. If it needs only conversation, use `$grilling`. If
the meaning is already settled and needs only capture, use `$domain-modeling`.

On caller invocation, preserve the current user as decision owner and require a
return owner. Keep Domain Modeling's context-write and ADR approval gates intact.

## 2. Compose

Run one `$grilling` session with `$domain-modeling` active. After each settled
answer that may change domain meaning, invariants, or relationships, let Domain
Modeling reconcile it before Grilling asks a dependent question. Return a
collision to the decision conversation instead of building on it.

Grilling owns questioning, materiality judgment, and confirmation. Domain
Modeling owns domain relevance, reconciliation, and the domain result,
including no change, proposed wording, authorized writes, or a blocker.

## 3. Return

Return the confirmed decision or exact Grilling gap with Domain Modeling's
current result. A material domain collision prevents confirmation. Return to
the caller, or to the user on direct invocation, and stop before downstream
work.

## Completion

Complete when one confirmed decision or exact unresolved gap, together with
Domain Modeling's current result, has returned to its owner.
