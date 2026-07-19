# HTML Improvement Report Contract

Render one self-contained semantic improvement survey under repo-local `.tmp/improvement-reviews/`.

## Portability

**Offline.** Use no network requests or runtime JavaScript. Embed CSS and static SVG. Pre-render Mermaid only with an existing local renderer under strict security; otherwise use inline SVG or positioned HTML.

## Layout

Lead with the survey bound and **Top recommendation**, then ranked candidate cards and the complete survey ledger. The header names the repo, date, inspected history or scope, and only visual encodings in use. Keep candidate and ledger anchors stable.

## Theme And Accessibility

**Dark and accessible.** Declare `color-scheme: dark`. Use near-black pages, dark panels, soft borders, high-contrast text, visible keyboard focus, semantic headings and lists, and a narrow-screen stack. Pair every color with a label: one cool accent, red only for removal pressure, amber for uncertainty, green for retained or verified state.

## Survey Ledger

**Ledger.** Account for every region with disposition, compact evidence, and candidate anchor when applicable. Keep `Retain` in the ledger, not action cards. Record speculation as rejected with its missing evidence; promote it to `Investigate` only for an exact decision-relevant question.

## Candidate

Render ranked `Eliminate`, `Concentrate`, and `Investigate` candidates as `<article id="candidate-n">` cards containing:

- stable `Candidate N`, disposition, concise title, and `Strong` or `Worth exploring` recommendation strength;
- compact Source Trace with file and line pointers;
- observed friction and deletion-test result;
- behavior and commitment boundary;
- elimination target or responsibility to concentrate;
- proof seam;
- resolution need and evidence route;
- sequence relationship, risk, blast radius, and rank rationale;
- provisional destination and exact immediate pickup invocation.

Keep each card provisional: a survey hypothesis, not an interface or implementation contract.

An `Eliminate` card names `$simplify-code`, never `$tdd` or `$implement`; its immediate pickup still resumes `$improve-codebase`. A `Concentrate` card names selected design or delivery resolution. An `Investigate` card names one evidence route.

## Visual

Choose the smallest visual that changes understanding:

- **Eliminate:** before/after dependency, branch, or control-flow removal;
- **Concentrate:** responsibility consolidation, dependency flow, or interface compression;
- **Investigate:** question-to-evidence surface without a fabricated after-state.

Keep pairs comparable. Omit a diagram when the ledger or compact code-flow sketch is clearer.

## Ranking

Explain order through evidence and proofability, complexity or caller burden addressed, recurring friction, risk and reversibility, and overlap. Use no fabricated scores; prefer `Eliminate` on ties.

## Top Recommendation

Render one prominent card naming the highest-value next move, why it wins now, and its candidate anchor. For `Investigate`, name the exact question and evidence route.

When no candidate survives, render **No candidate recommended** and show why every region was retained, disproved, or rejected as speculation. Emit no candidate anchor or selection prompt.

## Resolution

After a selected-candidate pass, update that card with resolver, returned evidence or decision, final disposition, route, and time. Preserve IDs. Include only surviving prototype paths; retain verdicts from deleted probes without stale links.

## Voice

Use plain repo and domain language. Name concrete modules, callers, decisions, dependencies, interfaces, seams, proof lanes, and risks. Prefer schematic labels and whitespace over decoration.
