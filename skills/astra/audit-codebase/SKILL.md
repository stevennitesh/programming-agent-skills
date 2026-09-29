---
name: audit-codebase
description: Map or audit existing code for evidence-backed baseline defects and worthwhile improvements. Exclude pending-diff review and implementation.
---

# Audit codebase

Investigate the current codebase for demonstrated defects and worthwhile
improvements, or build a visual atlas for guided exploration. Match the depth and
result to the requested investigation.

Audit is read-only with respect to product behavior. The managed HTML report and
invocation-owned temporary files are the only default writes. Findings and
candidates do not authorize implementation, tracker publication, merge, release,
deployment, or changes to accepted product meaning.

## 1. Choose direct discovery, focused audit, or visual atlas

For improvement discovery, ranked opportunities, or a whole-codebase audit without
a requested map, investigate promising areas autonomously and return a bounded
set of supported recommendations. Follow the strongest leads rather than reviewing
every file. Selecting where to investigate does not authorize implementation.

For a user-selected subsystem, flow, or concrete baseline problem, perform a
focused audit and return concise findings unless the user asks to preserve it in
an atlas.

For a requested map, maintained report, or guided subsystem exploration, use
[Visual atlas](references/atlas.md). The atlas owns the interactive workflow:

```text
Map repository → user selects subsystem → Audit subsystem
              → user selects candidate → Analyze candidate
```

Within the atlas workflow, do not choose the user's next subsystem or candidate.
The report may expose
evidence-backed qualitative strength and coverage to support that choice.

## 2. Find demonstrated costs

Read primary repository guidance and relevant architecture documentation to
understand the intended design before selecting investigation areas. Within the
scope, read governing behavior and accepted decisions and inspect enough actual
behavior, ownership, callers, dependencies, proof, and bounded history to
demonstrate the claimed cost and its affected set.

Judge the current design against supported behavior and real change pressure, not
hypothetical extensibility.

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

For direct discovery, analyze promising candidates far enough to support the
recommendation and its priority. For a focused audit, stay within its selected
scope. In atlas mode, analyze only the candidate the user selects.

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

For direct discovery, return at most five distinct opportunities by default,
ranked in the order worth addressing; use fewer when evidence supports fewer.
For each, give a specific title and category, affected actor or workflow, trigger,
current problem, source paths and line numbers, and decisive evidence. Recommend
the smallest useful change with expected benefit, rough effort (Small / Medium /
Large), main tradeoff or risk, and a brief priority rationale. Rank by practical
impact and frequency, implementation and maintenance cost, regression risk, and
confidence. Evidence strength and implementation priority are different judgments.
State material coverage limits and do not split one underlying problem to fill
the list. This shortlist limit does not cap atlas findings or require ranking a map.

For a focused audit, return the strongest findings, retained complexity, evidence
gaps, and useful candidates without padding.

For atlas work, update the managed report and return its path plus the currently
selectable subsystem or candidate IDs. The HTML is a read-only decision surface:
its local controls may navigate, filter, and copy the next explicit invocation,
but they never mutate the repository or start another workflow.

Complete when direct discovery returns its supported shortlist and coverage
limits (including an empty shortlist when warranted), the requested focused scope
is judged, or the requested atlas operation—Map, Audit one selected subsystem, or
Analyze one selected candidate—is published against current source with the next
selection left to the user.
