# Domain docs

**Configured layout:** single-context.

## Route

- **single-context:** load the root `CONTEXT.md` and applicable `docs/adr/`.
- **multi-context:** follow the root `CONTEXT-MAP.md` to the relevant context
  record and its `docs/adr/`; also load applicable repository-wide ADRs.

Missing domain records are not setup gaps. `$domain-modeling` owns settled
domain meaning and any authorized context or ADR write. Repo Bootstrap only
configures this route.
