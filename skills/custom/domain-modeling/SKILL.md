---
name: domain-modeling
description: Build a project's ubiquitous language and ADR record. Use when domain terms or boundaries are being resolved, a decision may be ADR-worthy, or another skill delegates durable domain capture.
---

# Domain Modeling

Build the project's **ubiquitous language** as it changes.

Vocabulary consumption belongs to repo domain routing. This discipline begins when domain language, context boundaries, or decision records are changing.

## Orient

Build the **Source Trace** from the current request or caller packet, repo instructions, `docs/agents/domain.md` when present, the relevant context map, glossaries, ADRs, and any code evidence needed by factual claims.

Follow configured domain routing. Without it, a root `CONTEXT-MAP.md` selects multi-context; otherwise use a root `CONTEXT.md`. Create domain files only when the first resolution needs them.

Orienting is complete when the owning context, existing language, relevant decisions, and evidence gaps are known.

## Model

- **Challenge:** Surface collisions between user language, glossary language, ADRs, and code.
- **Sharpen:** Replace vague or overloaded language with one precise canonical term. Prefer existing terms when they fit; record rejected synonyms under `_Avoid_`.
- **Stress-test:** Use concrete edge cases to force concept and context boundaries.
- **Cross-check:** Test factual claims against code and named sources. Keep contradictions open until resolved.
- **Resolve:** Require a settled canonical name, definition, owning context, and material conflicts. Source evidence settles facts; the user or caller packet settles contested language, boundaries, and decisions.

## Persist

**Write gate:** A request to change domain truth, or an invoked caller whose contract includes durable domain capture, authorizes glossary and context-map writes. Otherwise return patch-ready wording and target paths.

- **Glossary:** Read [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md), then capture each resolved term immediately in the owning `CONTEXT.md`.
- **Map:** Create or update `CONTEXT-MAP.md` when a context boundary or cross-context relationship resolves.
- **ADR:** Apply the **ADR-worthy gate** in [ADR-FORMAT.md](./ADR-FORMAT.md) when a resolved decision may deserve a durable record. Create an ADR only after an explicit request or user approval.
- **Scope:** Mutate only `CONTEXT.md`, `CONTEXT-MAP.md`, and ADR files. Return code, spec, plan, ticket, or tracker work to its owning skill.

## Handoff

Return a **domain delta** containing:

- Source Trace;
- resolved terms and owning contexts;
- changed domain paths or patch-ready wording;
- ADR offers, paths, and outcomes;
- unresolved terms, contradictions, and evidence gaps.

## Completion Criteria

Complete only when every resolved term is captured or handed off patch-ready; every affected context map is reconciled; every ADR candidate has an offered, recorded, or declined outcome; every unresolved contradiction is named; writes stayed inside the domain scope; and the domain delta was returned.
