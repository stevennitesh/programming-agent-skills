# HTML Report Format

Render the architecture review as a single self-contained HTML file in the repo-local temp directory, normally `.tmp/architecture-reviews/`, with OS temp as a fallback.

The report should help the user see the architectural friction quickly, compare deepening candidates visually, and choose one candidate to explore. It is not a design proposal and should not settle final interfaces.

Tailwind and Mermaid come from CDNs. Mermaid handles graph-shaped diagrams well; hand-built divs and inline SVG handle editorial visuals like mass diagrams, cross-sections, and collapsed call graphs. Mix them. Do not lean on Mermaid for everything or the report will feel generic.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review - {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "dark", securityLevel: "loose" });
    </script>
    <style>
      :root { color-scheme: dark; }

      /* Small custom layer for things Tailwind does not cover cleanly:
         dashed seam lines, hand-drawn-feeling arrowheads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #f87171; }
      .deep { background: linear-gradient(135deg, #111827, #1e3a5f); }
    </style>
  </head>
  <body class="bg-zinc-950 text-zinc-100 font-sans antialiased">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Include repo name, date, and a compact legend:

- solid box = module
- dashed line = seam
- red arrow = leakage
- thick dark box = deep module

Skip the intro paragraph. Go straight into candidates.

## Candidate Card

The diagrams carry the weight. Prose is sparse, plain, and uses `$codebase-design` vocabulary without ceremony.

Do not include candidates that fail the real-deepening filter from `SKILL.md`.

Each candidate is one `<article>`.

Include:

- **Number and anchor** - stable `Candidate N` label and `id="candidate-n"` anchor so chat can refer to it.
- **Title** - short, names the deepening, e.g. `Candidate 1: Collapse the Order intake pipeline`.
- **Badge row** - recommendation strength (`Strong`, `Worth exploring`, `Speculative`) plus dependency category (`in-process`, `local-substitutable`, `remote-owned`, `true-external`).
- **Files** - monospaced list of files or modules involved.
- **Before / after diagram** - the centerpiece. Two columns, side by side.
- **Problem** - one sentence naming the architectural friction.
- **Why it matters** - one sentence naming the cost in locality, leverage, test surface, or AI-navigability.
- **Deepening opportunity** - one sentence naming what responsibility could move behind a smaller interface.
- **Validation angle** - one sentence naming how behavior could be proved through the deeper interface.
- **Wins** - short bullets in `$codebase-design` terms.
- **ADR callout** - one amber-tinted line when a candidate contradicts an ADR strongly enough to consider reopening it.

No long paragraphs. If a candidate needs a paragraph to be understood, redraw the diagram.

## Diagram Patterns

Pick the pattern that fits the candidate. Mix patterns across candidates so the report does not feel generic.

### Mermaid Graph

Use Mermaid `flowchart`, `graph`, or `sequenceDiagram` when the point is call flow, dependency flow, or too many round trips.

Wrap Mermaid in a dark Tailwind-styled card so it feels integrated.

```html
<div class="rounded-lg border border-zinc-800 bg-zinc-900/80 p-4 shadow-sm shadow-black/30">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leaks.-> D[PricingClient]
      classDef leak stroke:#f87171,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-Built Boxes And Arrows

Use positioned `<div>` modules with inline SVG arrows when Mermaid's layout fights the idea.

Reach for this when the after diagram should feel like one thick-bordered deep module with faded internal implementation.

### Cross-Section

Use stacked horizontal bands to show shallow layers a call must pass through.

Before: many thin bands, each doing little.
After: one thick band labeled with the consolidated responsibility.

### Mass Diagram

Use two rectangles per module: interface size and implementation size.

Before: interface rectangle nearly as large as implementation.
After: smaller interface, larger hidden implementation.

### Call-Graph Collapse

Use nested boxes to show a scattered call tree.

Before: branching call tree across modules.
After: one deep module with formerly scattered calls faded inside as implementation.

## Style Guidance

- Lean editorial, not corporate dashboard.
- Use dark mode by default: near-black page, dark zinc/slate panels, soft borders, high-contrast text.
- Use generous whitespace.
- Use color sparingly: one cool accent plus red for leakage and amber for warnings.
- Keep before/after diagrams around 320px tall so they sit side by side without scrolling.
- Use schematic labels for modules, such as `text-xs uppercase tracking-wider`.
- The only scripts are Tailwind CDN and Mermaid ESM import. The report is otherwise static.
- Use `bg-zinc-950`, `bg-zinc-900`, `border-zinc-800`, `text-zinc-100`, `text-zinc-400`, `text-sky-300`, `text-red-300`, and `text-amber-300` as the default palette unless the repo has a clear reason to vary it.

Avoid decorative complexity. The visual should explain architecture, not decorate it.

## Top Recommendation

End with one larger card:

- candidate number and name, e.g. `Candidate 1: Collapse the Order intake pipeline`
- one sentence on why it is the best first exploration
- anchor link to its candidate card

Do not settle the final interface here. Recommend the numbered candidate to explore next.

## Tone

Use plain English, concise prose, and the shared architecture vocabulary.

Use exactly for architecture claims:

- module
- interface
- implementation
- depth
- deep
- shallow
- seam
- adapter
- leverage
- locality

Preserve repo/domain terms when they are real domain language. If the repo calls a domain concept `Service Level`, keep that term. But do not use vague architecture substitutes where `$codebase-design` vocabulary is more precise.

Avoid as architecture substitutes:

- component, unit, service when you mean module
- API, signature when you mean interface
- boundary when you mean seam
- layer, wrapper when you mean module

Phrasings that fit:

- `Order intake module is shallow: interface nearly matches implementation.`
- `Pricing leaks across the seam.`
- `Deepen: one interface, one place to test.`
- `Two adapters justify the seam: HTTP in production, in-memory in tests.`
- `Validation angle: prove checkout behavior through the order intake interface.`

Wins bullets should name the gain in glossary terms:

- `locality: bugs concentrate in one module`
- `leverage: one interface, many callers`
- `test surface: behavior proved through one seam`
- `AI-navigability: one module owns the workflow`
- `interface shrinks; implementation absorbs the sequence`

Do not write generic gains like `cleaner code`, `better architecture`, or `easier to maintain`. Name the gain precisely.

No hedging, no throat-clearing, no filler. If a sentence can be a bullet, make it a bullet. If a bullet can be cut, cut it.
