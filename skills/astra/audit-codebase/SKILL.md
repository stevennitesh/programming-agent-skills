---
name: audit-codebase
description: Audit an existing codebase for evidence-backed defects and worthwhile architecture or maintainability improvements. Exclude reviewing a pending change and implementing fixes.
---

# Audit codebase

Find demonstrated baseline defects or avoidable costs worth changing while
distinguishing justified complexity and missing evidence.

An audit is complete when the strongest opportunities in scope are supported by
concrete scenarios and current evidence, significant justified complexity is not
misreported as a defect, and coverage limits are explicit.

Audit is read-only with respect to product behavior. Findings do not authorize
implementation, tracker publication, external effects, or changes to accepted
domain meaning.

## 1. Bound the audit

Start with the user's scope, pain point, or concrete change pressure. For an
open-ended audit, prioritize consequential flows and owners where repeated fixes,
coordination cost, change frequency, or failure impact make inspection useful.
Churn is a lead, not evidence of a defect.

Match the coverage claim to the evidence. A focused audit may inspect only the
relevant flow. A comprehensive claim requires materially distinct flows and
applicable quality dimensions to be accounted for; a sampled file list is not
comprehensive coverage.

When the user requests a maintained map, visual report, explicit coverage atlas,
or continuation of an existing atlas, read [Atlas](references/atlas.md). Mapping
is an artifact choice and does not itself establish audit coverage.

## 2. Find demonstrated costs

Read the governing behavior and accepted decisions relevant to the selected scope.
Inspect enough of the actual behavior, ownership, and change history to demonstrate
the claimed cost and its affected set.

Judge the current design against supported behavior and real change pressure, not
hypothetical future features or extensibility.

Look for demonstrated coordination costs such as duplicated policy, callers
enforcing invariants that belong elsewhere, leaked representation, or unrelated
policies forced to change together. Treat each as a hypothesis until a real
scenario and consequence support it.

Use [Quality questions](references/quality-questions.md) only for dimensions that
can affect the requested scope. Follow shared owners or sibling callers far enough
to establish the affected set before calling a problem systemic.

Do not report a boundary as unnecessary merely because it has one implementation
or adds files. Distinct ownership, external contracts, lifecycle, variation, or
meaningful hidden policy can justify complexity.

## 3. Challenge and admit findings

For each proposed finding, establish a concrete supported scenario, current source
evidence, and a consequential effect or avoidable cost. Seek evidence that could
disprove the diagnosis; migration, independent lifecycle, external contracts, or
domain distinctions may justify the current shape.

Classify the result as one of:

- **defect:** an accepted expectation is violated;
- **opportunity:** a demonstrated avoidable cost is worth reducing;
- **retain:** suspicious complexity is justified by current requirements; or
- **gap:** evidence is insufficient to support a conclusion.

A smell, line count, preference, or unfamiliar design is none of these by itself.
No findings is a valid result.

An opportunity must identify the demonstrated cost and a plausible direction for
removing it. Detailed replacement architecture belongs to
[codebase-design](../codebase-design/SKILL.md).

Use proportionate read-only or isolated checks when they can resolve a disputed
finding. Missing production access or a representative workload is an evidence
limit, not proof of failure. Do not mutate live product state as part of the audit.

## 4. Rank and return the useful result

Group findings that share one causal explanation instead of reporting the same
cost as many independent wins.

Rank the strongest opportunities by demonstrated consequence, expected benefit,
confidence, relevance to real work, and likely change and verification cost.
Do not optimize for finding count, files removed, or architectural novelty.

Return the strongest supported candidates with the evidence and consequence needed
to judge them, plus significant retained complexity and material evidence gaps.
Do not pad the result with every rejected suspicion.

The audit establishes the problem and evidence, not the replacement design. Use
[codebase-design](../codebase-design/SKILL.md) when a consequential architecture
choice must be settled and [prototype](../prototype/SKILL.md) when a new
observation is required before deciding.

Use a concise report unless the user requested the atlas. Audit-only requests end
with the findings and requested artifacts. Broader work may continue only within
its existing authorization; the audit itself grants no implementation authority.
