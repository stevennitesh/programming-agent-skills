---
name: grill-with-docs
description: Compose a repo-backed decision through $grilling and $domain-modeling when user-owned ambiguity resolution and active durable domain capture are both required. Use directly or from Wayfinder, Triage, or Improve Codebase; return without downstream execution.
---

# Grill With Docs

Return one bounded Grilling packet and Domain Modeling's current cumulative Domain Delta as one coherent result.

**Boundary.** Own only composition. Grilling owns the interview and its exit packet; Domain Modeling owns domain meaning, persistence, ADR handling, and the cumulative Domain Delta; the caller owns continuation. Interpret neither component, mutate nothing outside Domain Modeling's authority, and start no downstream work.

```text
Admit -> Disclose -> Compose [Grill <-> Relay <-> Model] -> Join -> Return
```

**Admit.** Admit a direct user, Wayfinder, Triage, or Improve Codebase only when one bounded subject needs both capabilities. Establish the shared subject and Source Trace, an admission-ready bound and authority lock for each component, domain context action (`persist authorized` or `render only`), ADR action (`offer only` or approved candidate identifiers), caller identity and opaque identifiers, and return owner. Each component validates its own requirements; direct composition uses only its documented direct defaults. Direct use defaults missing persistence intent to `render only`; callers must supply a context action. ADR creation always requires separate explicit approval. Preserve caller vocabulary and identifiers intact.

On a direct mismatch, name the narrower owner and stop without starting it. On a caller mismatch, return the exact mismatch. A mismatch has no joint status. Missing or contradictory admitted fields return `Blocked` with their owner and safe resumption requirement before either component starts.

**Disclose.** Before Grilling asks its first question, state the context action, separate ADR approval gate, possibility that a domain collision may reopen or block a branch, and that confirmation starts nothing downstream. Disclosure reports authority; it grants none.

**Compose.** Run one Grilling session with Domain Modeling active. Relay each settled material answer with the shared subject, source, and relevant opaque identifiers; carry Domain Modeling's authoritative current cumulative Domain Delta opaquely; and return every material collision or blocker to Grilling before dependent questioning continues. Grilling owns answer materiality; Domain Modeling owns domain consequence and delta accumulation. The composer filters or merges neither. A cumulative no-change delta is valid.

**Join.** When Grilling reaches a terminal candidate, derive one joint status without re-performing either component's completion criterion:

- `Confirmed`: both results are current and complete with no material nondeferred collision or blocker.
- `Evidence gap`: Grilling returns its legitimate gap packet and the Domain Delta is current through the last settled answer.
- `Blocked`: admission, disclosure, component integrity, collision processing, persistence or verification, payload currency, or compatibility cannot close.

Only Grilling originates `Evidence gap`. Every `Blocked` result names the exact blocker, owner, and safe resumption requirement.

**Return.** Return only:

```text
Status: Confirmed | Evidence gap | Blocked
Caller identity and opaque identifiers: <when supplied>
Grilling exit packet: <attached intact when available>
Domain Delta: <attached intact when available>
Composition blocker, owner, and resumption requirement: <Blocked only>
Return owner:
```

Return to the named owner and stop. An Evidence gap preserves Grilling's uninvoked blocking owner; Confirmed selects no next route; Blocked reports recovery without performing it. This is a return, not a general handoff.

## Completion

Complete only when Admit establishes the shared seam or returns the mismatch; Disclose precedes questioning; every answer and collision traverses Relay before dependent progress; Join uses intact current component results; Return reaches the named owner; and downstream execution remains unstarted.
