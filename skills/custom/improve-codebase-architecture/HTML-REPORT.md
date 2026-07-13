# HTML Report Format

Render one self-contained architecture survey under repo-local `.tmp/architecture-reviews/`.

The report compares source-traced deepening candidates. The chosen-candidate pass owns dependency classification and interface contracts.

## Portability Gate

The report must open offline with no network request. Embed CSS and SVG directly. Use no runtime JavaScript.

When the repo already provides a local Mermaid renderer, render Mermaid to static SVG with its default strict security level and embed the SVG. Otherwise draw the relationship with inline SVG or positioned HTML.

## Structure

Produce one self-contained semantic HTML report with embedded CSS and SVG. Include the current structure, friction points, numbered candidates, trade-offs, and a visibly marked Top recommendation.

## Header

Include repo name, date, and a compact legend:

- solid box = module;
- dashed line = seam;
- red arrow = leakage;
- thick box = deep module.

Start with candidates; omit an introductory essay.

## Candidate Card

Include only candidates that pass the parent skill's deepening gate. Each candidate is one `<article>` with:

- stable `Candidate N` label and `id="candidate-n"`;
- short title naming the deepening;
- recommendation strength: `Strong`, `Worth exploring`, or `Speculative`;
- compact Source Trace with file and line pointers;
- side-by-side before/after diagrams;
- one sentence each for Problem, Why it matters, Deepening hypothesis, and Validation angle;
- short wins in `$codebase-design` terms;
- one warning line when an ADR may need reopening.

Redraw the diagram when prose grows.

## Diagram Patterns

Choose the smallest visual that explains the candidate:

- **Graph:** locally pre-rendered Mermaid SVG or hand-built inline SVG for dependencies, ownership, or flow.
- **Cross-section:** stacked bands showing many shallow layers becoming one deeper responsibility.
- **Mass diagram:** paired interface/implementation rectangles showing interface compression.

Keep diagrams around 320px tall so before and after remain comparable.

## Style

- Lean editorial, not a dashboard.
- Near-black page, dark panels, soft borders, high-contrast text.
- One cool accent; reserve red for leakage and amber for warnings.
- Schematic module labels; generous whitespace.
- Every visual explains architecture; decoration remains subordinate.

## Top Recommendation

End with one larger card containing the chosen candidate number and name, one sentence explaining why it is the best first exploration, and an anchor link to its card.

Keep the recommendation at survey level. The chosen-candidate pass owns the final interface.

## Tone

Use plain English and the `$codebase-design` vocabulary loaded by the parent skill. Preserve established repo and domain terms.

Every architecture claim names a module, interface, implementation, seam, adapter, depth, leverage, or locality. Every gain names depth, leverage, locality, or caller-facing test surface.
