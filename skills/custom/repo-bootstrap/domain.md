# Domain Docs

**Configured layout:** <single-context | multi-context>

## Route

Load only model records relevant to the selected work:

- **single-context:** root `CONTEXT.md` and applicable `docs/adr/`.
- **multi-context:** follow root `CONTEXT-MAP.md` to relevant context records
  and `<context-root>/docs/adr/`; load root `docs/adr/` for applicable repo-wide
  decisions.

Missing records are not setup gaps. Proceed silently; setup neither creates nor
recommends them. `$domain-modeling` alone may create or change domain truth for
an authorized settled meaning or decision.

## Preserve The Model

Use each context's canonical terms, invariants, ownership, and relationship
language. Do not flatten different meanings across contexts. If needed meaning
is absent or ambiguous, reconsider the wording or return the exact gap to
`$domain-modeling`.

Name conflicts with routed domain records or ADRs; never silently override them.
Conform or return the reopening question to the decision owner.
