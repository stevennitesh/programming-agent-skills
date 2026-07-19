# HTML Audit Report Contract

Render one self-contained audit report at `.tmp/audit-codebase/<run-id>/report.html`.

## Portability

The report opens offline with no network requests or runtime JavaScript. Embed CSS and static SVG. Use semantic HTML, stable anchors, visible keyboard focus, high-contrast text, text labels for every color, and a narrow-screen layout.

## Header

Show repository, snapshot, run ID, audit status, confidence, Charter summary, workloads and environments, generation time, and only visual encodings actually used. State that status measures coverage, not release acceptance.

## Coverage Matrix

Render a **Coverage Matrix** crossing every named region with every required lens. Each cell links to its evidence or gap and uses one labeled state: `covered`, `gap`, `blocked`, or `not applicable`. The matrix must account for the full Charter.

## Audit Ledger

Show counts by defect severity, advisories, evidence gaps, and disproved or duplicate items. Render every verified defect in severity order with its full finding contract and stable `<article id="finding-id">` anchor. Preserve disproved and duplicate items in a compact ledger.

Render separate domain and robustness, performance, evidence-gap, enabled-advisory, and finding-cluster sections using each item's complete owning contract. Add only presentation-specific context: the governing domain boundary, the complete performance measurement, or cluster member IDs, shared boundary, unresolved decisions, and Wayfinder eligibility.

Use compact static charts or tables only when they clarify measured values, distributions, scaling, or comparisons. Label inferred benefits as inference.

## Suggested Handoffs

Group suggestions by immediate owner. Each row links to the item, states the reason and pickup prerequisite, and says `caller selection required`. Keep `none` items in the audit ledger.

**Ledger, not leaderboard:** show every item. Severity orders defects; work shape determines suggested ownership. Select no **Top recommendation**.

## Footer

End with coverage status, preserved disposable paths, failed or skipped proof, and:

```text
Release decision: none
Mutation authority: none
Downstream execution: none
Return boundary: caller
```
