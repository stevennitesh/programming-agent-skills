---
name: domain-modeling
description: Resolve and persist a project's ubiquitous language, context boundaries, and ADR-worthy decisions. Use when canonical domain terms or boundaries are changing, an ADR may be warranted, or another skill delegates durable domain capture.
---

# Domain Modeling

Own durable domain truth. Vocabulary consumption follows repo domain routing; this skill starts when domain truth is changing.

## Process

1. **Trace.** Trace the request or caller packet, repo instructions, `docs/agents/domain.md` when present, routed context docs, ADRs, and evidence needed for factual claims. Without configured routing, an existing root `CONTEXT-MAP.md` selects multi-context; otherwise use root `CONTEXT.md`. Create domain files only while persisting the first resolution.

2. **Challenge.** Surface collisions among requested language, existing language, ADRs, and code. Sharpen vague or overloaded terms; stress-test concept and context boundaries with concrete edge cases; keep contradictions open until resolved.

3. **Resolve.** Settle each term's canonical name, definition, owning context, and material conflicts. Evidence settles facts; the user or caller packet settles contested language, boundaries, and decisions.

4. **Persist.** A request to change domain truth, or a caller contract that includes durable domain capture, authorizes context writes; otherwise return patch-ready wording and target paths. Read [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), capture resolved terms immediately, and reconcile affected context relationships. Apply [ADR-FORMAT.md](./ADR-FORMAT.md) to ADR candidates; create an ADR only after an explicit request or user approval. Mutate only `CONTEXT.md`, `CONTEXT-MAP.md`, and ADR files; return other work to its owner. After any write, reread every changed domain file and reconcile it with the pending domain delta before Return.

5. **Return.** Return a **domain delta** with the Source Trace; resolved terms and owning contexts; changed paths or patch-ready wording; ADR offers, paths, and outcomes; and unresolved terms, contradictions, and evidence gaps. Complete only when every resolution, unresolved term, contradiction, evidence gap, and affected context relationship is accounted for in the domain delta; every ADR candidate is offered, recorded, or declined; every authorized write passed Persist read-back; and no mutation crossed domain scope.
