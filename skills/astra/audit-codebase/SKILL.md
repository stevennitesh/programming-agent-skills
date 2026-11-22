---
name: audit-codebase
description: Discover evidence-backed codebase improvements through focused assessments or an atlas for systematic audits. Exclude pending-diff review and unrequested fixes.
---

# Audit codebase

Discover worthwhile improvements through source evidence. Choose boundaries,
hypotheses, methods, and depth for the request. Atlas work can write the managed
report and invocation-owned temporary files. Product changes, revised product
meaning, tracker publication, merge, release, and deployment require existing
authority. For combined analysis-and-fix requests, complete and verify the
authorized set, recording outcomes in the atlas when used.

## Choose chat or an atlas

Honor the requested output and scope. Use chat for a bounded question that a
focused trace or check can answer and that needs no durable map or audit record.
Give the conclusion, decisive evidence, and material limits. Keep text-only or
no-write assessments in chat.

Use the atlas for a codebase map, guided exploration across systems, a
whole-codebase audit, or work that needs to resume with coverage, findings, and
improvement candidates intact. Map meaningful ownership and dependencies so the
user can navigate the codebase and track coverage over successive audits.

For a new atlas, follow [Map](references/atlas.md#map). To resume an atlas, use
[Inspect the relevant work](references/maintenance.md#inspect-the-relevant-work)
with compact `status` and filtered `inspect`.

## Investigate the selected scope

Use a supplied or delegated scope directly. Before investigating a subsystem
for atlas publication, prepare the source-bound inputs with
[Audit packet](references/audit-packet.md). The helper owns validation and
publication. The agent owns judgments and evidence.

Trace accepted behavior, implicated owners/callers, and concrete consequences.
Treat complexity, duplication, coordination costs, and suspected bottlenecks as
hypotheses until supported. Seek counterexamples, use discriminating probes when
needed, and reuse valid checks. Follow shared owners far enough to establish the
affected set before calling a problem systemic. Extra files or unfamiliar design
alone prove no avoidable complexity; preserve justified policy and lifecycle.

For systematic audits, use reliability, domain, design, simplification, coding
practice, and performance as coverage prompts. Use
[Quality questions](references/quality-questions.md) when a lens needs more
detail. Record actual coverage and gaps. For bounded questions, follow the
evidence the question needs.
For authorized delegation, split distinct hypotheses/owners and collect attributable
evidence and limits without duplicate investigation.

## Record supported findings and candidates

Distinguish defects violating accepted expectations, opportunities with demonstrated
avoidable cost, retained complexity protecting requirements, and evidence gaps.
Keep observations, reproduced/measured results, inference, and expected benefit
distinct. A material gap needs its smallest deciding observation, usable evidence,
missing input/authority, and revisit condition; pursue closure within scope.

Group findings only by a coherent causal owner or improvement direction. Candidates
link findings and add a useful direction, qualitative strength, risks, and required
proof where material; the helper derives counts and scope. Do not optimize for
finding count, deleted lines, or novelty.

For selected analysis, revalidate source and constraints and compare materially
different options only. [Codebase-design](../codebase-design/SKILL.md) owns an
unresolved ownership/migration choice; [prototype](../prototype/SKILL.md) obtains
a needed new observation. Return a supported recommendation, disproved proposal,
or exact blocker. Analysis alone starts no implementation.

## Publish and verify atlas updates

Publish meaningful scope batches through guarded operations and retain stable IDs,
source identities, and readback. Use [Prepared work and verification](references/workflow.md)
for coordinated batches, narrow follow-ups, check receipts, and gap dispositions;
no universal operation sequence is required. Use `edit-presentation` for display
changes rather than another audit.

Use [Atlas maintenance](references/maintenance.md) for resumed or changed source,
ownership, and fix/delivery records. Inspect relevant deltas without reopening all
history or erasing original evidence of verified work.

After publication, follow
[Check and preview](references/maintenance.md#check-and-preview-the-report).
Return the report path and selectable IDs for atlas work. HTML controls
navigate/copy selections; they never execute workflows.

## Finish the requested scope

In guided exploration, stop and hand back when the user has enough to choose
what to inspect next. A readable map with ownership, dependencies, and coverage
can be enough for the first choice. After an audit, show the strongest findings,
selectable candidates, and any evidence gap that would affect the choice. Give
the report path and relevant IDs. Continue deeper analysis when selected or
delegated.

For an already-selected whole-codebase or narrower audit, continue through the
requested scope and make remaining coverage gaps visible. Complete authorized
fixes and verification, and report pending delivery or blockers.
