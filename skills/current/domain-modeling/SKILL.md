---
name: domain-modeling
description: Build and sharpen a project's ubiquitous language. Use when the user wants to pin down domain terminology, resolve overloaded words, record an ADR-worthy decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Build the project's **ubiquitous language** as it changes. This is the active discipline: challenge fuzzy terms, stress-test concept boundaries, cross-check language against code, and record resolved terms or ADR-worthy decisions as they crystallize.

Merely reading `CONTEXT.md` is not domain modeling. Use this skill when the language or decision record is changing, not when another skill only needs vocabulary.

## Files

Create files lazily, only when something has been resolved.

Use `CONTEXT.md` for domain language. It is a glossary, not a spec, plan, scratchpad, implementation note, or issue tracker.

Single-context repos use root `CONTEXT.md` and `docs/adr/`.

Multi-context repos use root `CONTEXT-MAP.md` to point at each context's `CONTEXT.md` and local ADRs. Use `CONTEXT-MAP.md` to choose the relevant context. If the topic crosses contexts, update each relevant `CONTEXT.md`; if the right context is unclear, ask.

Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) for glossary format and [ADR-FORMAT.md](./ADR-FORMAT.md) for ADR format.

## During The Session

Challenge glossary conflicts immediately: if the user uses a term differently from `CONTEXT.md`, surface the mismatch and ask which meaning should win.

Sharpen vague or overloaded terms into precise canonical language. Prefer the project's existing terms when they fit; otherwise propose a better term and list rejected synonyms under `_Avoid_`.

Stress-test domain relationships with concrete scenarios, especially edge cases that force boundaries between concepts to become precise.

Cross-reference user claims with code. If code and language disagree, surface the contradiction instead of silently choosing one.

Update the right `CONTEXT.md` as soon as a term is resolved. Do not batch resolved language.

ADRs: offer only when a decision is hard to reverse, surprising without context, and the result of a real trade-off. Create one only after user approval or an explicit request to record the decision. Record why the decision was made, not a long template.

Update only the relevant glossary and ADR files.

## Completion Criteria

Done means resolved domain terms are captured in the right `CONTEXT.md`, ADR-worthy decisions have been offered or recorded, and unresolved terminology is surfaced.
