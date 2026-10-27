# Quality questions

Use only prompts that could expose a consequential defect, avoidable cost,
justified complexity, or evidence gap in the selected scope. These are not a
checklist, finding quota, or reason to add unrequested operating capabilities.

## Workflow value and ownership

Identify the actor, supported task, current path, and evidenced friction. Separate
observed limitations from assumptions about demand or benefit; proposed value must
justify implementation and maintenance. Unsettled product behavior belongs to
[shape-work](../../shape-work/SKILL.md), not an audit's recommendation.

Does a caller need policy or representation knowledge the owner should hide?
Do coordinated edits, competing paths, implementation imports, registries, or
vendor/framework details cause actual drift or change burden? Use relevant history
when it can test the explanation. A deeper owner can reduce caller burden without
adding a layer; removing a wrapper helps only if it removes complexity rather
than dispersing decisions. Similar syntax alone does not justify coupling policies.

## Meaning, failure, and real boundaries

Do names, units, states, relationships, and representations preserve accepted
meaning? Trace authoritative data, writers, synchronization, and ordinary readers
before treating multiple representations as duplicate ownership. Current behavior
does not itself define the intended domain.

Where supported workflows require them, can callers distinguish rejection, partial
success, cancellation, retry, restart, or uncertain effects? Is authorization enforced
at the reachable boundary? Preserve required durability, security, accessibility,
and data-loss protections. Real independently deployed consumers or persistent data
may require compatibility and migration; consequential redesign belongs to
[codebase-design](../../codebase-design/SKILL.md). Do not replace accepted decisions
with hypothetical benefits.

## Simplification and proof

Could existing repository, platform, library, or dependency behavior replace custom
machinery without changing semantics? Before calling a path dead, inspect dynamic
registration, generated ownership, persisted formats, external consumers, and useful
history. Include migration and lifecycle costs; shorter code alone does not prove
safe removal.

Does proof exercise the ordinary caller and the relevant integration, persistence,
concurrency, or rendering mechanism? Do tests have independent expectations and
distinct obligations, and would they reject a plausible wrong result? Use a
distinguishing input, transition, or control when ordinary success fits the wrong
rule. Coverage alone is insufficient. Naming, types, comments, control flow, or
test organization need concrete ambiguity, coordination, or change cost.

## Performance and resources

Is expensive work actually consumed? Trace representative reads, copies, decoding,
transformations, materialization, and retention. Consider removing repeated work,
batching, streaming, reuse, or caching only while preserving required outputs,
ordering, freshness, ownership, scientific meaning, and evaluation boundaries.

Support cost claims with an attributable trace, representative measurement, or
deterministic work count under comparable workload, scale, environment, and noise.
A hotspot is a lead, not a measured benefit. Resource controls require a concrete
exhaustion or interference path. An evidenced cost may be an opportunity without
a formal budget; a defect requires a violated expectation. State missing operational
signals or production evidence rather than presenting local proof as production
behavior.
