---
name: audit-codebase
description: Discover evidence-backed codebase improvements using a visual map and scoped audits. Exclude pending-diff review and unrequested fixes.
---

# Audit codebase

Find worthwhile improvements to correctness, reliability, architecture,
simplicity, maintainability, developer workflows, and data or resource use.
The atlas helps the user explore systems, see audit progress and evidence, and
choose useful work. Choose mapping granularity, investigation methods, and depth
within the requested scope. Spend effort on questions that can change the result.

Audit is read-only with respect to product behavior. The managed HTML report and
invocation-owned temporary files are the only default writes. Findings and
candidates do not authorize implementation, tracker publication, merge, release,
deployment, or changes to accepted product meaning.

When fixes are also authorized, carry the selected set through the requested
analysis, implementation, and verification, then record its outcomes together.
Use suitable methods or an already-selected execution workflow. Commit, release,
and deployment follow the user's actual delivery scope. The audit's default write
boundary does not truncate a combined request.

## Select scope and prepare

Create or resume the workbench using [Visual atlas](references/atlas.md). Map
meaningful owners at a useful initial granularity; deepen the map where the
investigation needs it. For guided exploration, show the map and let the user
select a subsystem, then a candidate for deeper analysis. Honor an already-selected
scope, including a whole-repository audit or delegated scope selection, without
asking the user to select it again.

For a selected audit, use `prepare-audit` to create one editable packet with the
current report guard and source snapshot. Fill in judgments and evidence; the
helper handles validation and publication. See [Audit packet](references/audit-packet.md)
for the concise input and optional detail. The ordinary path is:

```text
Select scope → prepare packet → investigate → publish → check the result
```

An explicit brief or text-only assessment may stay in chat. A no-write request
creates no report. Return supported findings with material coverage limits.

## Investigate demonstrated costs

Read relevant guidance and accepted decisions, then trace the selected behavior
and its implicated owners and callers. Judge supported behavior and real change
pressure. Coordination costs, leaked representation, duplicated policy, shallow
modules, repeated workarounds, difficult proof, and suspicious complexity are
hypotheses until a concrete scenario and consequence support them.

Use the six lenses—reliability, domain, design, simplification, coding practice,
and performance—as concise coverage prompts. [Quality questions](references/quality-questions.md)
offers optional questions where useful. Record dimensions actually examined and
material gaps; omitted lenses remain **not inspected**. No finding, probe,
alternative, or per-lens essay quota is required.

Seek counterexamples that could disprove the diagnosis. Passing tests alone may
not distinguish the intended rule from a plausible wrong one. Choose probes,
measurements, history reads, or reviews that resolve a remaining question; reuse
passing checks when their relevant inputs are unchanged. If delegation is
authorized, split distinct hypotheses or owners and request location, observation,
consequence, counterevidence, and limits from each reviewer. Avoid duplicate
investigation or a new report format for delegated results.

Follow shared owners or sibling callers far enough to establish the affected set
before calling a problem systemic. One implementation, extra files, or unfamiliar
architecture does not establish unnecessary complexity. Preserve justified
ownership, lifecycle, contracts, and hidden policy.

## Record findings and useful candidates

Classify supported observations as:

- **defect:** an accepted expectation is violated;
- **opportunity:** a demonstrated avoidable cost is worth reducing;
- **retained complexity:** current requirements justify the complexity;
- **gap:** evidence is insufficient to settle the claim.

Distinguish observations, reproduced or measured behavior, inference, and expected
benefit. Keep the decisive evidence and uncertainty with the finding. Candidates
reference those findings and add a coherent improvement direction; repeat facts
only when the candidate adds material context. The helper derives counts and
candidate scope from linked findings when scope is omitted. Show defects separately
from retained complexity and gaps.

Group defects or opportunities only when they share a causal owner or direction
that can be judged together. Strength is qualitative evidence for attention:
`strong` for a consequential supported cost and credible direction,
`worth exploring` for a supported problem with material uncertainty, or
`speculative` for a plausible weak signal. Do not optimize for finding count,
deleted lines, or architectural novelty.

For selected candidate analysis, revalidate implicated source, constraints, and
proof. Compare only materially different choices; keeping the design, a small
change, a structural change, or replacement are options when relevant.
Use [codebase-design](../codebase-design/SKILL.md) for a consequential ownership or
migration decision, or [prototype](../prototype/SKILL.md) for a needed new observation.
Conclude with a supported recommendation, a disproved proposal, or an exact
blocker. Analysis alone does not start implementation.

## Publish a useful decision surface

Publish a meaningful scope batch when it is ready, or when an intermediate result
helps the user's ongoing exploration. Keep source identities, stable IDs, guarded
publication, and read-back. Use `edit-presentation` for display-title changes;
wording and layout adjustments do not require another audit event.

Use [Atlas maintenance](references/maintenance.md) to inspect relevant changes,
reconcile ownership, and retain fix and delivery outcomes. Changed source prompts
inspection of the delta and relevant conclusions. It does not reopen every
historical finding or erase evidence of a verified fix.

Run `check-report` after publication. For ordinary content updates, inspect the
changed content and its links and selection commands. For renderer changes,
also check layout and relevant interactions at useful window widths. Try the
host's supported HTML preview once and record opened, pending, or unavailable
honestly; opening alone does not establish visual verification. Record an
unavailable capability once per environment and reconsider when the host or
capability changes. Avoid temporary servers and repeated tab recovery for an
ordinary audit. Static checks remain separate from visual proof.

Return the report path, strongest supported conclusions, selectable IDs, and
material limits. Complete when the requested scope has been judged and the result
checked, with any preview limitation stated. For combined requests, also finish
authorized fixes and verification and record their outcomes, making blockers or
requested delivery still pending clear. Further selection belongs to the user
unless already supplied or delegated. HTML controls navigate, filter, and copy
selections; they never mutate the repository or start another workflow.
