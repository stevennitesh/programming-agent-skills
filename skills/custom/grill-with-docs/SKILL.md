---
name: grill-with-docs
description: Compose grilling one bounded user-owned repo-backed decision with keeping its domain language, invariants, or relationships current; exclude conversation-only grilling and settled-domain-only work.
---

# Grill With Docs

Return one intact Grilling packet and Domain Modeling's current cumulative
Domain Delta. Own only their composition.

```text
Admit -> Compose [Grill <-> Relay <-> Model] -> Return
```

1. **Admit.** Accept a direct-user request or a caller packet that preserves the
   current user as decision owner and supplies the return owner when the
   decision needs both components. Align their bounded subject and Source
   Trace. Default the context action to `render only` unless the user separately
   authorizes persistence;
   default the ADR action to `offer only` unless the user separately approves an
   identified candidate.

   Before Grilling asks its first question, state the effective context action,
   separate ADR approval gate, possibility that a domain collision may reopen or
   block a branch, and that confirmation starts no downstream work. If the
   request needs only one component, name that narrower owner and stop without
   invoking it. Return a missing or contradictory requirement as `Blocked` with
   the exact blocker and re-entry condition before starting either component.

2. **Compose.** Run one `$grilling` session with `$domain-modeling` active.
   Relay each settled material answer to Domain Modeling and every returned
   collision or blocker to Grilling before dependent progress. Carry Domain
   Modeling's current cumulative Domain Delta opaquely; never merge or
   reinterpret it. Grilling owns the interview and materiality; Domain Modeling
   owns domain consequences, mutation, ADR handling, and delta accumulation. A
   no-change delta is valid; a missing current delta is `Blocked`.

3. **Return.** When Grilling reaches a terminal result, derive one status
   without re-performing either component's completion criterion or asking for
   another confirmation. Any material blocker in the current Domain Delta makes
   the combined status `Blocked`; never relabel it as a Grilling gap.

   - `Confirmed`: the confirmed Grilling packet and Domain Delta are current and
     complete, with no material collision or blocker.
   - `Evidence gap`: Grilling returns its complete gap packet and the Domain
     Delta is current through the last settled answer.
   - `Route gap`: Grilling returns its complete route packet and the Domain
     Delta is current through the last settled answer.
   - `Blocked`: admission, component integrity, Relay, collision processing,
     mutation verification, payload currency, or compatibility cannot close.

   Only Grilling originates `Evidence gap` or `Route gap`. Return to the user
   and stop:

   ```text
   Status: Confirmed | Evidence gap | Route gap | Blocked
   Grilling exit packet: <attached intact when available>
   Domain Delta: <attached intact when available>
   Composition blocker, owner, and re-entry condition: <Blocked only>
   ```

   `Confirmed` selects no next route. `Evidence gap` preserves Grilling's
   uninvoked evidence owner. `Route gap` preserves Grilling's uninvoked
   Wayfinder recommendation. `Blocked` preserves the originating blocker and
   owner without performing recovery.

## Completion

Complete only when authority was disclosed before questioning, every settled
material answer and returned collision or blocker traversed Relay before
dependent progress, the component payloads are current and intact, the Return
has exactly one allowed status, every blocker has an exact re-entry condition,
and downstream execution remains unstarted.
