# HTML Improvement Report Contract

Render one self-contained semantic improvement survey under repo-local `.tmp/improvement-reviews/`.

## Portability

The report must open offline with no network requests or runtime JavaScript. Embed CSS and static SVG. If the repo already provides a local Mermaid renderer, pre-render with its default strict security level; otherwise use inline SVG or positioned HTML.

## Layout

Show the survey bound and **Top recommendation** first, followed by ranked candidate cards and the complete survey ledger. The header contains the repo name, date, inspected history or named scope, and only visual encodings actually used. Candidate and ledger anchors must be stable.

## Theme And Accessibility

Declare `color-scheme: dark`; use a near-black page, dark panels, soft borders, and high-contrast text. Use one cool accent, red only for leakage or removal pressure, amber only for uncertainty, and green only for retained or verified state. Pair every color with a text label, preserve visible keyboard focus, use semantic headings and lists, and stack cleanly on narrow screens.

## Survey Ledger

Account for every surveyed region with its disposition, compact evidence, and candidate anchor when applicable. Render `Retain` regions in the ledger rather than inventing action cards. Record speculative regions as rejected with the missing evidence; promote one to `Investigate` only when it has an exact decision-relevant question.

## Candidate

Render numbered `Eliminate`, `Concentrate`, and `Investigate` candidates in rank order as `<article id="candidate-n">` cards containing:

- stable `Candidate N`, disposition badge, concise title, and recommendation strength: `Strong` or `Worth exploring`;
- compact Source Trace with file and line pointers;
- observed friction and deletion-test result;
- behavior and commitment boundary;
- elimination target or responsibility to concentrate;
- proof seam;
- uncertainty and evidence route;
- sequence relationship, risk, blast radius, and rank rationale;
- recommended next skill and exact pickup invocation.

State a survey-level hypothesis, not a final interface or implementation contract.

An `Eliminate` card names `$simplify-code` as its provisional downstream owner, never `$tdd` or `$implement`; its immediate pickup still resumes `$improve-codebase` for verification. A `Concentrate` card names selected design or delivery resolution. An `Investigate` card names exactly one evidence route.

## Visual

Choose the smallest visual that changes understanding:

- **Eliminate:** before/after dependency, branch, or control-flow removal;
- **Concentrate:** responsibility consolidation, dependency flow, or interface compression;
- **Investigate:** question-to-evidence decision surface without a fabricated after-state.

Keep paired diagrams comparable when a pair is useful. Omit a diagram when the ledger or a compact code-flow sketch is clearer.

## Ranking

Explain the ordering through evidence and proofability, total complexity or caller burden addressed, recurring friction, risk and reversibility, and overlap. Do not fabricate numeric scores. Prefer `Eliminate` when otherwise tied.

## Top Recommendation

Render one prominent card naming the highest-value next move, why it wins now, and an anchor to its candidate. An `Investigate` recommendation names the exact question and evidence route.

When no numbered candidate survives, render **No candidate recommended** instead. The ledger must show why each region is retained, disproved, or too speculative to investigate. Emit no candidate anchor or selection prompt.

## Resolution

After an explicit selected-candidate pass, update that card with the resolver used, returned evidence or decision, final disposition, route, and resolution time. Preserve stable IDs. Include only post-reconciliation prototype paths; record verdicts from deleted probes without stale artifact links.

## Voice

Use plain English and established repo and domain terms. Name concrete modules, callers, decisions, dependencies, interfaces, seams, proof lanes, and risks. Favor schematic labels, whitespace, and explanatory visuals over decoration.
