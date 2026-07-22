---
name: domain-modeling
description: Model and persist a project's context-scoped ubiquitous language, invariants, bounded contexts, relationships, and approved durable decisions. Use when domain meaning needs focused clarification or capture, including delegated capture, or an already-settled decision needs ADR assessment; exclude ordinary vocabulary lookup and general design debate.
---

# Domain Modeling

Keep the project's domain model coherent and return one complete Domain Delta.

**Model, don't catalog.** Capture meaning, behavior, invariants, responsibility, and relationships. Omit generic technical vocabulary, code indexes, and boundaries inferred only from implementation layout.

## Authority

Lock three independent authorities:

- **Meaning:** evidence settles source facts; the direct user unless a source names another authority, or the caller's named domain authority, settles intended meaning. Direct use may ask focused questions about terms, invariants, bounded contexts, and relationships. Under `$grill-with-docs`, Grilling asks and relays settled answers. A caller-invoked pass returns unresolved choices to its caller.
- **Context:** use `persist authorized` only after an explicit persistence request or exact caller mode; otherwise use `render only`.
- **ADR:** use `offer only` unless one identified, already-settled candidate has explicit recording approval. The originating workflow owns the decision.

Mutate only routed domain records and approved ADRs. Return setup, code, spec, plan, tracker, and implementation consequences to their owners. Invoke no Router, composer, or downstream work.

## Runtime

```text
Trace -> Challenge -> Resolve -> (Persist -> Verify | Render) -> Return
```

1. **Trace.** Trace the bounded subject, repository instructions and domain routing, relevant domain records and ADRs, load-bearing evidence, authorities, caller, and return owner. Follow the repository's configured domain-document route. Without one, an existing root `CONTEXT-MAP.md` selects multiple contexts; otherwise root `CONTEXT.md` is the fallback. Create the first record only for an authorized settled resolution.

   Treat code, tests, contracts, runtime behavior, and widespread usage as evidence about implementation, not authority over intended meaning. Bounded contexts follow model, language, responsibility, and consistency boundaries—not directories, packages, services, or repository size. When managed routing must change, return the accepted topology and exact setup requirement; resume only in a later invocation after setup read-back agrees.

2. **Challenge.** Test material uncertainty for **language collisions** (overload, aliases, implementation leakage), **model boundaries** (responsibility, invariants, relationship contract, language ownership, change authority), and **contradictions** (records, evidence, decisions, implementation). Use concrete normal, edge, failure, inclusion, and exclusion scenarios only when they can change the model. Resolve each material collision or return its exact blocker and owner.

3. **Resolve.** Settle the canonical term or decision, implementation-independent meaning, owning context, load-bearing sources, and decision authority. Add aliases, invariants, boundaries, relationships, conflicts, and consequences only when material. Preserve intended truth when implementation differs, expose the contradiction, and keep unresolved meaning out of durable records.

   For each context relationship, settle interaction direction, responsibilities, contract, language ownership, and change authority. Apply a DDD Context Mapping pattern only when it fits; exact representation and the optional recognized patterns live in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

4. **Persist -> Verify | Render.** Read [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) only to render or persist language, invariants, context maps, or relationships. Read [ADR-FORMAT.md](./ADR-FORMAT.md) only for a plausible already-settled ADR candidate.

   For `persist authorized`, refresh routing and every target, preflight the bounded set, write only accepted changes, and reread each attempted and changed record. On the first write or verification failure, preserve verified changes, stop mutation, and return exact partial state. For `render only`, return directly applicable wording, target, placement, and relationship effects without writing.

5. **Return.** Return the Domain Delta to the direct user, caller, or `$grill-with-docs` and stop:

```text
Semantic outcome: no-change | resolved | partial | unresolved
Persistence outcome: complete | partial | failed | not-applicable
Blockers and consequences:
Return owner:
```

Add authority, resolved language, context boundaries, invariants, relationships, per-target state, caller identifiers, ADR outcomes, and continuation authority only when present or caller-required. Each blocker names its condition, owner, impact, and re-entry requirement. Keep a no-change result minimal.

   Under `$grill-with-docs`, accept every settled material answer, including one with no durable consequence. Return the authoritative cumulative Domain Delta and any collision before dependent questioning continues; never choose interview materiality or branching.

## Completion

Complete when Trace is current; every in-scope consequence is resolved, no-change, or an exact blocker; each intended target is verified, rendered, or returned with exact failure state; every plausible ADR candidate has an outcome; mutation stayed inside routed domain records and approved ADRs; the Domain Delta is complete; and Return starts nothing.
