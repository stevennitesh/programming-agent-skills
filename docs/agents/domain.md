# Domain docs

**Configured layout:** single-context.

## Route

When domain meaning or an accepted decision affects the task, read the relevant
parts of root `CONTEXT.md`. Use the [ADR index](../adr/README.md) only when decision
rationale or applicability is needed; select relevant records in `docs/adr/`
instead of loading the history. This repository uses a single context. Preserve
accepted terminology and distinguish decisions from proposals and historical
research.

Missing domain records are not setup gaps. Astra
[shape-work](../../skills/astra/shape-work/SKILL.md) owns domain
clarification, settled decision capture, and reconciliation of affected domain
records, ADRs, and guidance. Settled technical decisions can be recorded without
another feature interview; unresolved architecture belongs to codebase-design.
Context-hygiene owns broader context maintenance. Repo-bootstrap configures
this route.

Suggest `$shape-work` when domain clarification or durable decision capture is
needed; use it when the user requests that workflow. Reading existing domain records does not invoke it.
Retired domain routes are not compatibility alternatives.
