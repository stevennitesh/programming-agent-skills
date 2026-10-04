---
name: writing-for-agents
description: Write or audit a selected agent instruction, skill, or handoff. Exclude routine worker dispatch, repository-wide context work, and product shaping.
---

# Writing for agents

Give the receiver the intent, context, and boundaries it needs, with freedom to
choose how to reach the accepted outcome. Use this standard for a requested
instruction artifact, reusable guidance, a consequential assignment, or a
continuation handoff. Ordinary worker prompts can be written directly within
their owning workflow; this skill is not a prerequisite for delegation.

For an audit, return findings without editing. Initial repository guidance and
requested setup migrations belong to [repo-bootstrap](../repo-bootstrap/SKILL.md).
Maintenance of scattered, stale, conflicting, or missing repository context
belongs to [context-hygiene](../context-hygiene/SKILL.md). This skill owns the
content of a selected instruction artifact.

## Preserve intent and supply missing context

Establish what the receiving agent will actually see. Preserve the user's
accepted outcome, decisions, constraints, authorized effects, and completion
criteria. Distinguish requirements from defaults, suggestions, examples, and
historical evidence. Do not invent policy to fill a consequential gap.

When a requirement or prohibition is easy to misinterpret, describe the observable
outcome or pattern; use an example when it removes consequential ambiguity.

Supply project facts, decision rationale, and context the receiver cannot infer
or retrieve. For an assignment, make scope, authority, acceptance, and the
expected return available in the prompt or an explicitly loaded source; do not
assume inherited conversation context. Leave orchestration with its actual owner.

Let the agent choose investigation, reasoning, tools, and implementation methods
within those boundaries. Prescribe a sequence or technique when an accepted
workflow, dependency, or fragile operation makes it necessary. Require a fixed
output shape only when a consumer or acceptance criterion needs it. Ask for
useful evidence, uncertainty, and concise rationale rather than narrated reasoning
or generic exhortations to think harder.

## Keep guidance at its owner

Keep shared requirements in the main instruction and substantial conditional
detail behind a clear trigger and pointer. Reference authoritative sources rather
than copying facts or procedures that change elsewhere. Use existing mechanical
enforcement where it can own a rule; retain the context and authority it cannot
express.

When meaning, discovery, ownership, or authority changes, reconcile directly
affected callers and competing current guidance within scope. Preserve history
as evidence. For conflicting or displaced specs, plans, or decision records, use
[Document reconciliation](../shape-work/references/document-reconciliation.md).

Remove generic writing advice, repeated defaults, and unnecessary procedural
scaffolding. Preserve non-inferable context, user choices, effect and custody
boundaries, acceptance, recovery contracts, and consequential ordering. A past
failure or preferred technique alone does not justify a universal rule.

Load these references only for the relevant branch:

- [Skill authoring](references/skill-authoring.md): skill discovery, invocation,
  packaging, or model/host adaptation.
- [Long-running instructions](references/long-running-instructions.md): when
  continuation, steering, or durable progress needs explicit treatment.
- [Continuation handoffs](references/continuation-handoffs.md): preparing another
  agent or fresh context to resume work.
- [Behavior evaluation](references/behavior-evaluation.md): deciding what evidence
  a consequential method change, migration, or performance claim needs.

## Check the result

Read the artifact with only the receiver's expected context. It should make the
intended outcome, applicable boundaries, available discretion, and completion
recognizable without inventing missing requirements. Check for unintended scope
expansion, approval stops, mandatory process, or lost obligations.

Choose verification to match the change. For changed discovery or conditional
routes, consider an applicable request and a realistic near-miss. Check affected
links and machine-read structure; exercise executable instructions when useful
and authorized. Ordinary edits do not require a behavioral evaluation campaign.
Editorial review and package checks do not prove improved agent performance.

Return the requested artifact or audit findings, the material changes, and any
consequential verification limits. No fixed report template is required.
