# UI Prototype

Use this branch to compare **structurally different bets** for one UI question.

[SKILL.md](SKILL.md) owns the prototype contract, write boundary, verdict, and cleanup. This file owns the UI artifact and smoke gate.

## Right Shape

Reach for a UI prototype to compare:

- page layout;
- information hierarchy;
- visual density;
- primary action placement;
- navigation or flow shape;
- different presentations of the same real data.

Use [LOGIC.md](LOGIC.md) for business logic, state transitions, data shape, or interface feel.

## Route Strategy

Judge UI under real constraints. A blank route is a **vacuum**: it hides density, data, auth, navigation, and layout conflicts.

Use an existing route whenever one can host the question. Create a throwaway route only for a genuinely new top-level surface or standalone flow.

### Existing Route Preferred

Render variants on the same route behind a `?variant=` URL parameter. Keep existing data fetching, parameters, auth, and surrounding layout; swap only the rendered subtree that answers the question.

Mount a new section, card, empty state, step, panel, or dashboard surface inside its natural host page.

### Throwaway Route Last

Use a throwaway route for a top-level surface or flow that has no natural host. Follow the repo's routing convention, mark the path as prototype code, and use the same `?variant=` pattern.

Choose the route that exposes the strongest real constraints.

## Variant Standard

Default to **3 structurally different bets**. Use fewer when the design space is already narrow; add a variant only for a genuinely different bet, with a hard cap of 5.

Variants must disagree about layout, information hierarchy, density, navigation, or primary affordance. Cosmetic variations in color, copy, spacing, or icons are **wallpaper**.

Each variant:

- serves the page's real purpose and available data;
- follows the repo's component and styling system;
- has a clear name such as `VariantA`, `VariantB`, or `VariantC`;
- remains free to use a different structure;
- keeps mutations fake or stubbed.

Share small primitives when useful. Keep each layout independent enough to preserve its bet.

## Switcher

Build one visible floating switcher as unmistakable prototype chrome.

Include:

- previous variant;
- current variant label;
- next variant.

Behavior:

- variant state lives in the URL, for example `?variant=A`;
- controls cycle variants and wrap around;
- reload preserves the selected variant;
- direct variant links work;
- prototype chrome is hidden or unreachable in production builds.

Reuse local components and styles when they fit. Keep the switcher isolated from the designs being judged.

## One Command

Add or report one repo-native command: `pnpm dev`, `npm run dev`, `bun dev`, `make dev`, or the repo's equivalent.

Use the app's normal development command when one exists. Report the URL and variant parameters.

## Smoke Gate

Run the app and inspect the prototype in a browser. Verify:

- the route loads in its real surrounding context;
- every variant has a direct URL;
- variants are structurally different;
- controls update the URL and wrap between variants;
- reload preserves the active variant;
- the active variant is obvious;
- the switcher leaves important UI unobscured at relevant viewport sizes;
- prototype-only chrome is hidden or unreachable in production builds.

Report the command, URL, variant keys, and every assumption that affects judgment.
