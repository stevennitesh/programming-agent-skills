# Astra composition and decision applicability

**Status**: accepted 2026-09-07

## Context

Earlier ADRs record several generations of the pack. Their accepted statuses and
retired skill names can look authoritative when opened directly, even though
current Astra composition has moved on. Loading that history for ordinary work
also adds context without helping the task.

## Decision

The [design brief](../astra/design-brief.md) owns current composition rationale.
[CONTEXT.md](../../CONTEXT.md) owns repository purpose and source boundaries.
Applicable AGENTS.md pointers select repository guidance; current
[skills/astra](../../skills/astra/) owners supply execution procedures.
Read historical ADRs only when their rationale or a named legacy mechanism is
relevant. Their original status records a decision at that time; the current
applicability notice controls which parts remain in force.

- **Shared engineering guidance:** the repository engineering contract is the
  shared owner. Skills add task-specific decisions and conditional references,
  rather than maintaining competing copies of common rules.
- **Composition and installation:** Astra is the managed skill source, primarily
  for GPT 6 Astra with GPT 5.6 Sol compatibility. Custom skills remain historical
  and separately usable source material, not an alternative managed route.
- **Workflow ownership:** ordinary coding needs no skill pipeline. Shape-work
  owns substantial shaping and its conditional domain-modeling path; to-tickets
  and parallel-implement are optional workflows. No standalone Implement, To Spec,
  Domain Modeling, or High-Assurance Review route is restored by an old ADR.
- **Review and delegation:** change-review owns review judgment and optional
  high-assurance detail. Explicitly selected cost-aware-coding owns routing
  acceptance, model allocation, and its independent review floor. Parallel-implement
  owns concurrent execution mechanics. Historical profiles and review flags do
  not add requirements to these owners or to ordinary coding.
- **Decision custody:** record or reconcile ADRs within the user's authorization.
  Existing authorization does not require a second approval merely to record it;
  an agent inference does not establish an accepted decision.
- **Legacy machinery:** epoch and Deploy Campaign records retain their named,
  explicitly selected legacy scope. Their files and identifiers remain available
  to existing consumers; they do not impose campaign gates on Astra maintenance.

## Supersession and remaining scope

The applicability notices on ADRs 0001–0017 identify each record's remaining
scope. This decision supersedes their conflicting Astra installation, ownership,
workflow, and duplicated-context requirements; it does not replace still-scoped
legacy mechanisms or rewrite historical evidence.

Foundational separation of concerns, decision traceability, mechanical validation,
exclusive writer custody, safe integration, and evidence-based review remain
useful. Their current implementation belongs to the owners above, without needing
to load predecessor procedures alongside them.

## Consequences

The ADR index routes by task instead of requiring a chronological read. Original
record bodies and links remain intact, with prominent applicability notices for
readers arriving directly. Future supersession should update the affected notice
and current owner, preserving any still-governing scope rather than accumulating
competing amendments. Exact model settings and execution limits stay in skills
so this record does not become another runtime policy copy.
