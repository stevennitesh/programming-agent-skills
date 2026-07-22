---
name: grill-with-docs
description: Compose one explicitly invoked repo-backed decision through $grilling and $domain-modeling; return intact component results without downstream execution.
---

# Grill With Docs

Compose `$grilling` with `$domain-modeling` for one bounded repo-backed decision. Own only their admission, ordering, transport, combined status, and Return; interpret neither component and start nothing downstream.

```text
Admit -> Compose [Grill <-> Relay <-> Model] -> Return
```

1. **Admit.** Accept only the direct user's explicit invocation when the decision needs both components. Align their bounded subject and Source Trace. Default the context action to `render only` unless the user separately authorizes persistence; default the ADR action to `offer only` unless the user separately approves an identified candidate.

   Before Grilling asks its first question, state the effective context action, separate ADR approval gate, possibility that a domain collision may reopen or block a branch, and that confirmation starts no downstream work. If the request needs only one component, name that narrower owner and stop without invoking it. Return a missing or contradictory requirement as `Blocked` with the exact blocker and re-entry condition before starting either component.

2. **Compose.** Run one Grilling session with Domain Modeling active. After every settled material answer, Relay it with the shared subject and source to Domain Modeling, carry its authoritative current cumulative Domain Delta opaquely, and return any collision or blocker to Grilling before dependent questioning continues.

   Grilling owns materiality, questioning, Evidence gap, confirmation, and its packet. Domain Modeling owns domain consequences, mutation, ADR handling, and delta accumulation. A cumulative no-change delta is valid. Return `Blocked` when Domain Modeling cannot supply a current delta.

3. **Return.** When Grilling reaches a terminal result, derive one status without re-performing either component's completion criterion or asking for another confirmation:

   - `Confirmed`: the confirmed Grilling packet and Domain Delta are current and complete, with no material collision or blocker.
   - `Evidence gap`: Grilling returns its complete gap packet and the Domain Delta is current through the last settled answer.
   - `Blocked`: admission, component integrity, Relay, collision processing, mutation verification, payload currency, or compatibility cannot close.

   Only Grilling originates `Evidence gap`. Return to the user and stop:

   ```text
   Status: Confirmed | Evidence gap | Blocked
   Grilling exit packet: <attached intact when available>
   Domain Delta: <attached intact when available>
   Composition blocker and re-entry condition: <Blocked only>
   ```

   `Confirmed` selects no next route. `Evidence gap` preserves Grilling's uninvoked evidence owner. `Blocked` explains re-entry without performing recovery.

## Completion

Complete only when authority was disclosed before questioning, every settled material answer and returned collision traversed Relay before dependent progress, the component payloads are current and intact, the Return has exactly one allowed status, every blocker has an exact re-entry condition, and downstream execution remains unstarted.
