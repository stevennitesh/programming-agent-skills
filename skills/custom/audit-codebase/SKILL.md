---
name: audit-codebase
description: Build or continue an organized HTML map of a repository, audit one user-selected subsystem for architecture and code-quality problems, or analyze one user-selected candidate. Use explicitly for thorough repository-baseline improvement discovery; exclude pending diffs, implementation, ticket publication, and release decisions.
---

# Audit codebase

Build one evidence-backed repository audit over time:

```text
Map repository -> Audit user-selected subsystems -> Analyze user-selected candidates
```

The HTML report preserves structure, coverage, findings, and history across
invocations. The user chooses every subsystem and candidate. The report may
recommend an order, but never selects or starts the next item.

## Authority

Audit is read-only except for its report and invocation-owned temporary files
under `.tmp/audit-codebase/<run-id>/`. Leave product source, tracked docs, Git,
trackers, reviews, and external systems unchanged.

The top-level agent owns scope, findings, report publication, and Return. Use
read-only subagents only when the user requests them. Inspect their evidence
before relying on it.

Use [Report CLI](REPORT-QUICK-REFERENCE.md) as the only report interface.
[HTML report](HTML-REPORT.md) owns persisted state and rendering.

## Choose one mode

- **Map:** create a new report from the current repository.
- **Audit:** inspect exactly one subsystem selected from the current map.
- **Analyze:** deepen exactly one candidate selected from the current report.

Inspect an existing report for the selected mode and ID before working. An
invalid or stale selection changes nothing and returns the current choices.
Never fall back to Map or choose another item.

## Map the repository

Inventory the current tracked worktree. Read repository instructions,
manifests, entry points, domain records, ADRs, implementation, representative
callers and tests, build and deployment configuration, and data or control
flows.

Group the repository into systems and subsystems that reflect runtime
ownership. Record each subsystem's purpose, owned behavior, entry points,
interfaces, callers, dependencies with evidence, flows, decisions, Proof
Seams, and paths. Assign every relevant source, test, configuration, and
support path to one subsystem, shared infrastructure with named consumers, or
an evidenced exclusion. Name important untracked material as an evidence
limit.

Map records structure, not audit judgment. It may suggest a dependency or
hotspot-informed audit order without ranking architectural quality. Publish
the report, present all mapped subsystems and their coverage state, and stop
for user selection.

## Audit one subsystem

Rebuild the selected subsystem's current Source Trace from its files, shared
owners, entry paths, callers, dependents, tests, configuration, domain records,
ADRs, and bounded history. Trace representative vertical flows for every
materially distinct entry-path family and include high-fan-in shared owners.

Read [Quality coverage](QUALITY-LENS.md),
[Reliability](RELIABILITY-LENS.md), and
[Finding contract](DEFECT-CONTRACT.md). Record coverage for Reliability,
Domain, Design, Simplification, Coding Practice, and Performance. Load the
detailed lens only when Quality's trigger applies. A class is complete when
its relevant contracts, flows, and available evidence have been examined, not
when it has a finding. Preserve unavailable required evidence as a gap.

For each credible observation, search sibling callers, similar instances, and
bounded history until the pattern is disproved or its affected set and causal
owner are named. A repeated workaround, branch shape, leaked representation,
or ownership conflict can be systemic. One isolated hard case may be necessary
domain complexity.

Admit defects, opportunities, retained complexity, and gaps under the Finding
and Quality contracts. Group a candidate only when its members share one
coherent improvement direction and Proof Seam. A systemic candidate may span
subsystems when one causal owner or repeated cross-subsystem policy explains
the members. Read [Candidate analysis](CANDIDATE-CONTRACT.md) when grouping is
needed.

Rank candidates across audited evidence by demonstrated impact or cost,
confidence, change reach, and proof burden. Recheck decisive current source,
publish the report, present every candidate, and stop for user selection.

## Analyze one candidate

Reinspect the candidate's current source, implicated subsystems, causal owner,
callers, contracts, decisions, tests, findings, and Proof Seams. Re-admit
changed members. Expand only when current evidence reveals another affected
caller, subsystem, or causal owner.

Apply [Candidate analysis](CANDIDATE-CONTRACT.md). Compare the present shape
with the smallest sound change and any materially different structural or
replacement option. Do not force irrelevant alternatives. For one
consequential architecture question, load `$codebase-design` and fold its
recommendation into the report.

Publish the analysis and stop. Suggest at most one natural next owner when an
unresolved question clearly belongs elsewhere. Never invoke it, publish
tickets, design an implementation graph, or start implementation.

## Completion

Map completes when every relevant path is owned or excluded and the new report
shows all selectable subsystems. Audit completes when the selected subsystem's
six classes are complete or have explicit gaps, every suspected systemic
pattern has been widened, and the report shows all selectable candidates.
Analyze completes when the selected candidate has current evidence, a bounded
recommendation or exact gap, proportional proof, and no downstream work has
started.

Return the completed mode, selected item, strongest findings or recommendation,
coverage limits, report path, and current user-selectable next items.
