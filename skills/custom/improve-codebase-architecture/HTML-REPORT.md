# HTML Report Format

Render one self-contained architecture survey under repo-local `.tmp/architecture-reviews/`.

The report compares source-traced deepening candidates. The chosen-candidate pass owns dependency classification and interface contracts.

## Portability Gate

The report must open offline with no network request. Embed CSS and SVG directly. Use no runtime JavaScript.

When the repo already provides a local Mermaid renderer, render Mermaid to static SVG with its default strict security level and embed the SVG. Otherwise draw the relationship with inline SVG or positioned HTML.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Architecture review - {{repo name}}</title>
    <style>
      :root {
        color-scheme: dark;
        --page: #09090b;
        --panel: #18181b;
        --border: #3f3f46;
        --text: #f4f4f5;
        --muted: #a1a1aa;
        --accent: #7dd3fc;
        --leak: #f87171;
        --warn: #fbbf24;
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--page); color: var(--text); font: 15px/1.5 system-ui, sans-serif; }
      main { width: min(1100px, calc(100% - 32px)); margin: 0 auto; padding: 48px 0 72px; }
      header, article, .recommendation { margin-bottom: 40px; }
      article, .recommendation { border: 1px solid var(--border); border-radius: 14px; background: var(--panel); padding: 24px; }
      .comparison { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
      .diagram { min-height: 320px; border: 1px solid var(--border); border-radius: 10px; padding: 16px; overflow: auto; }
      .muted { color: var(--muted); }
      .accent { color: var(--accent); }
      .warning { color: var(--warn); }
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: var(--leak); }
      @media (max-width: 760px) { .comparison { grid-template-columns: 1fr; } }
    </style>
  </head>
  <body>
    <main>
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation" class="recommendation">...</section>
    </main>
  </body>
</html>
```

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

- **Static graph:** locally pre-rendered Mermaid SVG or hand-built inline SVG for call, dependency, or round-trip flow.
- **Boxes and arrows:** positioned modules with inline SVG arrows when automatic layout obscures the point.
- **Cross-section:** stacked bands showing many shallow layers becoming one deeper responsibility.
- **Mass diagram:** paired interface/implementation rectangles showing interface compression.
- **Call-graph collapse:** scattered calls faded inside one deep module.

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
