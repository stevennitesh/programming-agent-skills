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

## Theme

Render dark mode only. Declare `color-scheme: dark`; use a near-black page, dark panels, soft borders, and high-contrast text. Use one cool accent, red only for leakage, and amber only for warnings.

## Candidate

Include only filter-passing candidates. Render survivors in rank order as `<article id="candidate-n">` cards containing:

- stable `Candidate N` label and a short deepening title;
- recommendation strength: `Strong` or `Worth exploring`;
- compact Source Trace with file and line pointers;
- comparable before/after diagrams;
- one sentence each for Problem, Deepening hypothesis, Trade-off, and Validation angle;
- short wins naming depth, leverage, locality, or caller-facing test surface;
- one ADR warning when material friction may justify reopening a decision.

Report a deepening hypothesis, not a final interface contract. Redraw the diagram when prose grows.

## Diagram

Choose the smallest visual that explains the candidate:

- **Graph** for dependencies, ownership, or flow;
- **Cross-section** for shallow layers becoming one responsibility;
- **Mass diagram** for interface compression.

Keep paired diagrams visually comparable and stack them on narrow screens.

## Top Recommendation

When candidates survive, end with one larger card naming the top-ranked candidate, why it is the best first exploration, and an anchor link to its card. Keep the recommendation at survey level.

When none survive, render one larger **No candidate recommended** card instead. Account for every surveyed region as healthy, cleanup-only, speculative, or an evidence gap. Emit no candidate anchor or selection prompt.

## Voice

Use plain English and established repo and domain terms. For architecture claims, name the module, interface, implementation, seam, adapter, depth, leverage, or locality. Favor schematic labels, whitespace, and explanatory visuals over decoration.
