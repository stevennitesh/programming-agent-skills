---
name: audit-codebase
description: Find and rank evidence-backed improvements to an existing codebase's architecture and maintainability. Optionally create or continue a visual system map and coverage atlas. Use for baseline improvement discovery; exclude reviewing a pending diff and implementing fixes.
---

# Audit codebase

Find changes worth making, with enough evidence to distinguish a real design
cost from necessary complexity. Inspect product code without changing it. Reports
and isolated checks support the audit; they do not authorize production effects,
implementation, tickets, or changes to accepted domain decisions.

## 1. Choose the scope and presentation

Start with the user's area, pain point, or change scenario. Otherwise use recent
changes, recurring fixes, critical flows, and shared owners to choose promising
areas. Churn guides attention; it does not prove a design problem. Include stable
but consequential boundaries when failures there would matter.

When the user wants a visual map, coverage tracking, or continuation of an atlas,
read [Atlas](references/atlas.md). Mapping is optional and may be partial. A map
shows structure; it does not establish audit coverage. If asked to map and await
selection, do that. If the user already authorized auditing an area or the whole
repository, proceed within that scope without another selection gate.

State what will be examined and the important exclusions. For a comprehensive
audit, cover materially distinct flows and relevant quality dimensions; do not
claim comprehensive coverage from a few sampled files. For a focused audit,
report its actual limits rather than expanding it to satisfy a taxonomy.
For comprehensive atlas coverage, use the helper-generated lens ledger and
account for examined evidence, justified exclusions, and gaps. A complete list
of entries does not itself establish sufficient inspection.

## 2. Trace the behavior and the cost of change

Read governing contracts and accepted decisions. Follow representative behavior
through entry points, callers, state owners, dependencies, and tests. Use a recent
change or a concrete upcoming requirement supplied by the user to see where one
decision requires coordinated edits. Do not invent speculative features to make
the current architecture look inadequate.

Look for duplicated policy, callers coordinating invariants, leaked internal
representations, and responsibilities split by execution stage rather than the
knowledge they own. Also look for unrelated policies forced through one owner:
consolidation and separation can each improve design. A boundary earns its place
through useful hidden decisions, meaningful ownership, variation, or an external
contract, even with one implementation.

Use [Quality questions](references/quality-questions.md) for the dimensions that
can affect the requested scope. These are discovery questions, not mandatory
findings. Follow shared owners and sibling callers far enough to establish the
affected set before calling a problem systemic.

## 3. Challenge and admit findings

For each proposed finding, establish a supported scenario, current source
evidence, and a concrete consequence. Seek evidence against the diagnosis: an
external contract, independent lifecycle, migration, or domain distinction may
justify the shape. Distinguish an architectural cause from one poor caller or an
isolated hard case. Record an unresolved cause without inventing certainty.

Separate a violated accepted expectation (defect), a demonstrated avoidable cost
(opportunity), justified complexity (retain), and missing evidence (gap). A smell,
line count, or preference alone is none of these. A useful opportunity needs a
plausible improvement mechanism, not a fully designed replacement or an existing
destination owner. Name the demonstrated cost the mechanism removes; when
ownership changes, say where responsibility would go. No findings is a valid result.

Verify disputed behavior using existing evidence or a small isolated check when
useful and authorized. Missing production access or a representative workload is
an evidence limit, not proof of failure. Read-only product scope permits scratch
files and caches for isolated checks; it does not permit real external mutations.

## 4. Rank improvement directions

Group findings only when they share a causal explanation and coherent direction.
Avoid reporting the same cause as many independent wins. Compare retention with
the smallest sound improvement; consider a new boundary when it removes a proven
cost. Explain expected benefit, affected callers, migration disruption, confidence,
and the behavior that must remain true. Rank by consequence and relevance to real
work against change and verification cost, not lines removed or finding count.

Return the strongest candidates with source locations, scenario, causal evidence,
counterevidence, direction, and the check that would establish improvement while
preserving behavior. Include significant retained complexity and evidence gaps
without padding the report with a ledger of every rejected suspicion.

Keep full interface design and competing architecture choices with
`$codebase-design`, and executable feasibility questions with `$prototype` when
available. Their absence does not block findings. The audit supplies the question
and decisive evidence; downstream work follows the user's authorized scope.

## 5. Record the result

Use a concise report unless the atlas was requested. With an atlas, use its helper
for scoped reads, prepared updates, IDs, source snapshots, coverage bookkeeping,
and HTML generation. Never hand-edit its HTML. Refreshing source fingerprints
does not revalidate a judgment: reread changed decisive evidence before replacing
a finding. Preserve unrelated records and mark unresolved evidence honestly.

Finish with ranked opportunities, what was examined, important limits, and the
recommended next decision. An audit establishes where improvement is justified;
it does not claim the proposed design or implementation has already succeeded.
