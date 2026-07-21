---
name: domain-modeling
description: Reconcile and persist a project's context-scoped ubiquitous language, bounded-context responsibilities and relationships, invariants, and already-settled ADR-worthy decisions. Use only when durable domain truth must change or be recorded, including delegated capture; route ordinary vocabulary lookup and unsettled participant judgment elsewhere.
---

# Domain Modeling

Own coherent, context-scoped domain truth and return one complete Domain Delta.

**Model, don't catalog.** Capture meaning, behavior, invariants, responsibility, and relationships. Keep generic technical vocabulary, code indexes, and implementation structure out of the domain model.

## Authority

Lock three independent authorities before resolving:

- **Meaning:** evidence settles source facts; the direct user absent a named conflict, or the caller's named domain authority, settles domain meaning and context boundaries. Under composition, return unsettled participant judgment through `$grill-with-docs` to Grilling; under caller invocation, return it to the caller; standalone leaves it unresolved for terminal routing. Never interview the participant or invoke the composer directly.
- **Context:** use `persist authorized` only after an explicit persistence request or exact caller mode. Otherwise use `render only`. Resolve, decide, model, inspect, and review do not authorize writes.
- **ADR:** use `offer only` unless one identified candidate has explicit approval. Context authority does not approve an ADR, and ADR approval does not authorize other mutation.

Mutate only routed `CONTEXT.md`, `CONTEXT-MAP.md`, and approved ADR files. Preserve caller identifiers, return ownership, and continuation authority. Start no downstream work.

## Spine

```text
Trace -> Challenge -> Resolve -> Reconcile -> (Persist -> Verify | Render) -> Return
```

1. **Trace.** Trace the request or caller packet, repository instructions, `docs/agents/domain.md`, routed context records and ADRs, and only evidence capable of changing an in-scope resolution. Follow configured routing; otherwise an existing root `CONTEXT-MAP.md` selects multi-context and the safe fallback is root `CONTEXT.md`. Create no empty record; create the first only for an authorized settled resolution. Treat code and widespread usage as evidence, not semantic authority. Bounded contexts follow model and responsibility boundaries, never directory, package, service, or repository size alone.

   A single-to-multi-context transition is two-owner work: return the accepted topology and exact routing requirement to `$repo-bootstrap`; resume persistence only after setup read-back agrees.

2. **Challenge.** Test each proposed resolution through **Overload, Alias, Leakage, Boundary, and Contradiction**. Use normal, edge, failure, inclusion, and exclusion examples only when they can change meaning. Finish with every material collision settled or represented by an exact blocker with owner and impact.

3. **Resolve.** Settle the canonical term or decision, precise implementation-independent meaning, owning context, load-bearing sources, decision authority, and any material behavior, invariant, edge, alias, conflict, relationship, or consequence. Keep ubiquitous language context-scoped. Expose implementation contradictions without letting current code silently redefine accepted truth. Leave unresolved meaning out of domain records.

4. **Reconcile.** Update the cumulative Domain Delta and affected context relationships after a material resolution, blocker, authority, scope, supersession, persistence, or verification change. Preserve ordered material events and caller identifiers; invent no version, hash, or session ledger.

   Under `$grill-with-docs` composition, accept every settled material answer with the shared subject, source, and relevant opaque identifiers, including answers with no durable consequence. Classify the domain consequence, update and return the authoritative current cumulative Domain Delta, and return any collision or blocker before dependent Grilling progress. Never decide answer materiality or interview branching.

5. **Persist -> Verify | Render.** Read [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) whenever a glossary, invariant, context map, or relationship must change. Read [ADR-FORMAT.md](./ADR-FORMAT.md) only for a settled plausible ADR candidate.

   For `persist authorized`, refresh and preflight every routed target, apply only the bounded accepted changes, stop on the first write or verification failure, and reread every attempted and changed record. Preserve verified changes and return exact partial state; do not roll back or continue best-effort mutation. For `render only`, return directly applicable wording, target, placement, relationship effects, and ordering without writing.

6. **Return.** Return the Domain Delta to the caller, `$grill-with-docs`, or the direct user and stop:

```text
Domain subject and source:
Decision and mutation authority:
Resolution: no-change | resolved | partial | unresolved
Persistence: complete | partial | failed | not-applicable
Persistence entries: <target>: rendered | verified | failed
Open blockers: <class, condition, owner, impact, re-entry>
Resolved or open consequences:
Return owner:
Caller continuation authority: preserved | not supplied
```

Use blocker class `authority`, `evidence`, `contradiction`, `routing/setup`, or `persistence/verification`. Add resolved language, boundaries, relationships, invariants, conflicts, downstream consequences, changed paths and read-back, rendered changes, and ADR outcomes only when present. A no-change delta needs only the subject and source, `Resolution: no-change`, `Persistence: not-applicable`, no blockers, and return owner.

A caller-invoked pass returns residuals to its caller. After a standalone pass is terminal, a material residual outside Domain Modeling with no owned handoff may invoke the implicit `$skill-router`; surface its one recommendation or `none` without execution.

## Completion

Complete when Trace is current; every consequence is resolved, explicitly no-change, or represented by an exact blocker; every composed answer has a returned current delta before dependent progress; material changes are reconciled; each intended target is verified, rendered, or returned with exact failure state; every plausible ADR candidate has an outcome; mutation stayed inside domain records; the Domain Delta is complete; and Return starts nothing.
