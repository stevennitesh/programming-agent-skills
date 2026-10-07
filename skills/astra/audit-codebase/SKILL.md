---
name: audit-codebase
description: Discover evidence-backed codebase improvements using a visual map and scoped audits. Exclude pending-diff review and implementation.
---

# Audit codebase

Discover worthwhile improvements to correctness, reliability, architecture,
simplicity, maintainability, developer workflows, and data or resource use.
Use a visual atlas to identify meaningful systems, investigate demonstrated costs,
and present useful improvement candidates. Choose the mapping granularity,
investigation methods, and recommendations within the requested scope.

Audit is read-only with respect to product behavior. The managed HTML report and
invocation-owned temporary files are the only default writes. Findings and
candidates do not authorize implementation, tracker publication, merge, release,
deployment, or changes to accepted product meaning.

## 1. Establish the map and requested scope

For codebase improvement or exploration, create or update the HTML workbench
using [Visual atlas](references/atlas.md). Its default guided workflow is:

```text
Map repository → user selects subsystem → Audit subsystem
              → user selects candidate → Analyze candidate
```

Honor an already-selected subsystem, flow, candidate, or whole-repository audit
without asking the user to select it again. If the user delegates scope selection,
choose promising areas within that authority and continue the requested audit or
analysis. Otherwise show the map and leave the next selection to the user.
Recommend areas using evidence, current coverage, and real change pressure.

An expressly requested brief or text-only assessment may stay in chat. An explicit
no-write request does not create a report. Investigate the selected scope and
return supported findings with material coverage limits.

## 2. Find demonstrated costs

Read primary repository guidance and relevant architecture documentation to
understand the intended design before selecting investigation areas. Within the
scope, read governing behavior and accepted decisions and inspect enough actual
behavior, ownership, callers, dependencies, proof, and bounded history to
demonstrate the claimed cost and its affected set.

Judge the current design against supported behavior and real change pressure, not
hypothetical extensibility.

Recent churn, repeated fixes, reverts, and changes that repeatedly span owners can
help prioritize investigation when they reveal a current burden. Use history when
it can test that explanation; activity alone does not establish a problem.

Use [Quality questions](references/quality-questions.md) only for dimensions that
can expose a meaningful defect, avoidable cost, justified complexity, or evidence
gap in the selected scope.

Treat coordination costs, leaked representation, duplicated policy, shallow
ownership, repeated workaround shapes, difficult proof, and suspicious complexity
as hypotheses until a concrete scenario and consequence support them. Follow
shared owners or sibling callers far enough to establish the affected set before
calling a problem systemic.

Do not report a boundary as unnecessary merely because it has one implementation
or adds files. Distinct ownership, lifecycle, external contracts, variation, or
meaningful hidden policy can justify complexity.

## 3. Admit findings and form candidates

Classify supported observations as:

- **defect:** an accepted expectation is violated;
- **opportunity:** a demonstrated avoidable cost is worth reducing;
- **retained complexity:** suspicious complexity is justified by current
  requirements; or
- **gap:** evidence is insufficient to settle the claim.

A smell, line count, preference, or unfamiliar architecture is none of these by
itself. Seek evidence capable of disproving the diagnosis.

Distinguish repository observations, reproduced or measured behavior, inference,
and expected benefit. Label consequential uncertainty; a proposed benefit is not
an observed result. Reproduce or measure suspected problems when practical and
useful to establish the claim.

Group defects and opportunities into an improvement candidate only when they share
a coherent causal owner or improvement direction and can be reasoned about
together. Keep individual findings visible.

Candidate strength is qualitative evidence for attention, not a numeric score:

- **strong:** current evidence supports a consequential avoidable cost and a
  credible improvement direction;
- **worth exploring:** the problem is supported but material design/evidence
  uncertainty remains; or
- **speculative:** the signal is plausible but too weak for a stronger claim.

Do not optimize for finding count, deleted lines, architectural novelty, or a
single top recommendation.

## 4. Analyze candidates within the requested scope

Analyze candidates within the user's selected or delegated analysis scope, or stay
within the scope of a requested brief assessment. Follow implicated callers and
shared owners far enough to judge the cause and affected set; this does not select
unrelated areas for another audit.

Reinspect the candidate's current source, implicated subsystems, causal owner,
callers, constraints, findings, and proof seams.

Compare only materially different choices. Consider keeping the current design,
the smallest sufficient change, a structural change, or replacement when each is
actually relevant; do not manufacture alternatives to fill a template.

Use [codebase-design](../codebase-design/SKILL.md) when a consequential ownership,
interface, seam, or migration choice requires dedicated design judgment. Use
[prototype](../prototype/SKILL.md) when a new observation is required before the
candidate can be judged.

Analysis ends with the supported cause, affected scope, relevant options,
recommendation or exact blocker, required proof, and evidence limits. It does not
start implementation.

## 5. Return the decision surface

Update the managed report and show it through the host's available HTML preview.
Inspect navigation, selection handoffs, legibility, and progress meaning at useful
presentation sizes. Return its path and selectable subsystem or candidate IDs;
report a preview limitation when the surface cannot be opened or inspected.
The HTML is a read-only decision surface:
its local controls may navigate, filter, and copy the next explicit invocation,
but they never mutate the repository or start another workflow.

For a requested brief assessment, return the strongest supported findings,
retained complexity, evidence gaps, and useful directions without padding. Give
decisive source references, expected benefit, material tradeoffs, required proof,
and coverage limits. Prioritize by practical impact, frequency, cost, risk, and
confidence when ranking is requested. Evidence strength and priority differ.

Complete when the requested Map, Audit, or Analyze scope is published against
current source and its decision surface is checked, or the requested brief scope
is judged. Leave further selection to the user unless already supplied or delegated.
