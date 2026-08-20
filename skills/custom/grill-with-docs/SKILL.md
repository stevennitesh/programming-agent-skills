---
name: grill-with-docs
description: Compose grilling one bounded user-owned repo-backed decision with keeping its domain language, invariants, or relationships current; exclude conversation-only grilling and settled-domain-only work.
---

# Grill With Docs

Compose one Grilling conversation with current domain capture. Return the
confirmed understanding and Domain Modeling's current cumulative Domain Delta,
or the concrete blocker that prevents either result.

1. **Admit.** Accept a direct-user request or a caller packet that preserves the
   current user as decision owner and supplies the return owner when the
   decision needs both components. Align their bounded subject and Source
   Trace. Domain Modeling returns proposed wording unless the user separately
   authorizes context persistence. ADR recording needs separate approval for an
   identified, already-settled candidate.

   If the request needs only one component, name that narrower owner and stop
   without invoking it. A missing or contradictory requirement returns to its
   owner before either component starts.

2. **Compose.** Run one `$grilling` session with `$domain-modeling` active.
   Relay each settled material answer to Domain Modeling and every returned
   collision or blocker to Grilling before dependent progress. Carry Domain
   Modeling's current cumulative Domain Delta opaquely; never merge or
   reinterpret it. Grilling owns the interview and materiality; Domain Modeling
   owns domain consequences, mutation, ADR handling, and delta accumulation. A
   no-change delta is valid. A missing current delta is a composition blocker.

3. **Return.** Return the current Grilling understanding or intact gap with the
   current cumulative Domain Delta. Do not repeat either component's completion
   judgment or ask for another confirmation. A material Domain Delta blocker
   prevents a confirmed combined result; return that blocker, its owner, and
   re-entry condition instead. Preserve an originating Grilling gap and its
   owner without selecting a route or recovery.

   Return to the declared return owner, or the user on direct invocation, and
   stop without starting downstream work.

## Completion

Complete when every settled material answer and returned collision traversed
Relay before dependent questioning, and either the confirmed understanding or
intact gap plus the current Domain Delta, or the concrete composition blocker,
has returned intact to its owner.
