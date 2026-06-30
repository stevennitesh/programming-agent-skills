# UI Prototype

Use this branch when the prototype question is **what should this look like?** The answer should come from seeing and comparing real UI, not imagining mockups in conversation.

This file defines the UI branch. Use the lifecycle in [SKILL.md](SKILL.md): write down the question, keep the artifact throwaway, run it once, capture the answer, and clean up or hand off.

## Right Shape

Reach for a UI prototype when the user needs to compare:

- page layout
- information hierarchy
- visual density
- primary action placement
- navigation or flow shape
- different ways to present the same real data

If the question is business logic, state transitions, data shape, or interface feel, use [LOGIC.md](LOGIC.md).

## Route Strategy

Prefer real app constraints without letting prototype chrome become production code.

A UI prototype is easier to judge when it sits against the real app: real header, real sidebar, real data, real auth, real density, and real surrounding constraints. A blank throwaway route hides design problems.

Use `.tmp/` for notes, copied references, static experiments, and any prototype shell that can still answer the question. Move into the app tree only when the question depends on real routing, layout, auth, data fetching, component behavior, or page density.

### Existing Route Preferred

Use the existing route when there is any plausible host page.

Render variants on the same route, gated by a `?variant=` URL param. Keep existing data fetching, params, auth, and surrounding layout. Only swap the rendered subtree that answers the prototype question.

If the prototype is for a new section, card, empty state, step, panel, or dashboard surface that naturally belongs inside an existing page, mount it there.

### Throwaway Route Last

Create a throwaway route only when the UI has no natural existing host: a genuinely new top-level surface, standalone flow, or page that cannot be embedded sensibly.

Follow the repo's routing convention. Name it clearly as prototype code. Use the same `?variant=` pattern.

Before choosing a throwaway route, check whether an existing page would expose better constraints.

## Variant Standard

Default to **3 variants**. Use fewer only when the design space is already narrow. Use more only when the extra variants are genuinely different; cap at 5.

Variants must be structurally different. They should represent different bets, not just different arrangements. They should disagree about layout, information hierarchy, density, navigation, or primary affordance. Name the bet if it is not obvious.

Not enough:

- same card grid with different colors
- same layout with different copy
- same hierarchy with different spacing
- same component arrangement with a different accent

Good variants make the tradeoff obvious.

Each variant should:

- use the page's real purpose and available data
- follow the repo's component and styling system
- have a clear name such as `VariantA`, `VariantB`, `VariantC`
- stay free to use a different structure from the others
- avoid real mutations; stub or fake mutation paths if interaction is needed

Share small primitives when useful, but do not force variants through one shared layout. A shared layout usually defeats the prototype.

## Switcher

Build one floating variant switcher. It should be visible enough that the user knows it is prototype chrome, not part of the design being judged.

The switcher should include:

- previous variant control
- current variant label
- next variant control

Behavior:

- variant state lives in the URL param, e.g. `?variant=A`
- arrows or controls cycle variants and wrap around
- reloading the page preserves the selected variant
- direct links to variants work
- keyboard left/right may cycle variants when safe for the framework
- keyboard handling must not intercept input, textarea, or contenteditable focus
- switcher is hidden or unreachable in production builds

Put the switcher in one reusable prototype component when that fits the repo. Do not introduce a new design system for prototype chrome.

## Visual Check

Run the app and inspect the prototype in a browser when possible.

Verify:

- the route loads with real surrounding app context
- every variant is visible
- variants are structurally distinct
- the active variant is obvious
- the switcher does not cover important UI
- the layout works at the viewport sizes relevant to the question

This is a smoke check, not production QA.

## One Command

Add or report one repo-native command to run the prototype: `pnpm dev`, `npm run dev`, `bun dev`, `make dev`, or the repo's equivalent.

If the app already has a normal dev command, use that. Do not add tooling just for the prototype.

Report the URL and variant params the user should open.

## Smoke Check

Before handing it over, run the command once and verify:

- the route loads
- each variant is reachable by URL param
- the switcher changes the URL
- reload preserves the active variant
- production gating is present for prototype-only chrome

Report the command, URL, variant keys, and any assumption the prototype made.

## Anti-Patterns

- Variants that differ only by color, copy, spacing, or icons.
- Evaluating UI on an empty route when an existing page could host it.
- Sharing a layout so heavily that variants stop being real alternatives.
- Wiring prototype UI to real mutations.
- Treating the winning variant as production code instead of input to a real implementation pass.
- Leaving the switcher, throwaway route, loose variants, or `.tmp/` artifacts in the repo after the decision is made unless the user asked to preserve them.
