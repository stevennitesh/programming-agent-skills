# HTML Report Contract

Render one self-contained semantic architecture survey under repo-local `.tmp/architecture-reviews/`.

## Portability

The report must open offline with no network requests or runtime JavaScript. Embed CSS and static SVG. If the repo already provides a local Mermaid renderer, pre-render with its default strict security level; otherwise use inline SVG or positioned HTML.

## Layout

Start with the candidates. The header contains the repo name, date, and only the visual encodings actually used:

- solid box = module;
- dashed line = seam;
- red arrow = leakage;
- thick box = deep module.

## Candidate

Include only candidates that pass the parent skill's deletion and deepening gates. Render each as one `<article id="candidate-n">` containing:

- stable `Candidate N` label and a short deepening title;
- recommendation strength: `Strong` or `Worth exploring`;
- compact Source Trace with file and line pointers;
- comparable before/after diagrams;
- one sentence each for Problem, Deepening hypothesis, Trade-off, and Validation angle;
- short wins in `$codebase-design` terms;
- one ADR warning when material friction may justify reopening a decision.

Report a deepening hypothesis, not a final interface contract. Redraw the diagram when prose grows.

## Diagram

Choose the smallest visual that explains the candidate:

- **Graph** for dependencies, ownership, or flow;
- **Cross-section** for shallow layers becoming one responsibility;
- **Mass diagram** for interface compression.

Keep paired diagrams visually comparable and stack them on narrow screens.

## Top Recommendation

End with one larger card naming the recommended candidate, why it is the best first exploration, and an anchor link to its card. Keep the recommendation at survey level.

## Voice

Use plain English, established repo and domain terms, and `$codebase-design` vocabulary for architecture claims. Use a near-black page, dark panels, high-contrast text, one cool accent, red only for leakage, and amber only for warnings. Favor schematic labels, whitespace, and explanatory visuals over decoration.
