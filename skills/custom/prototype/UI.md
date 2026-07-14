# UI Prototype

Use this branch to compare **structurally different bets** for one UI question.

[SKILL.md](SKILL.md) owns the question, write boundary, command, verdict, and reconciliation. This file owns the UI artifact and smoke gate.

## Host

Judge UI under real constraints. A blank route is a **vacuum**: it hides density, data, auth, navigation, and layout conflicts.

Use an existing route whenever one can host the question. Keep its data fetching, parameters, auth, and surrounding layout; switch only the rendered subtree that answers the question.

Use a throwaway route only for a genuinely new top-level surface or standalone flow. Follow the repo's routing convention and expose the same `?variant=` URL state.

Choose the host that exposes the strongest real constraints.

## Bet

Default to **3 structurally different bets**. Use fewer when the design space is narrow; cap the set at 5.

Variants disagree about layout, information hierarchy, density, navigation, or primary affordance. Differences limited to color, copy, spacing, or icons are **wallpaper**.

Each variant:

- serves the page's real purpose and available data;
- follows the repo's component and styling system;
- has a clear name;
- remains structurally independent;
- keeps mutations fake or stubbed.

Share small primitives without forcing variants through one layout.

## Switch

Build visible prototype chrome with previous, current, and next controls.

Keep variant state URL-backed. Controls wrap, reload preserves the selection, direct links work, and the active variant remains obvious. Isolate the switcher from the designs and hide or exclude it from production builds.

## Smoke

Run the app and inspect the prototype in a browser. Verify:

- the route loads in its real surrounding context;
- every variant has a direct URL and is structurally different;
- controls update the URL and wrap between variants;
- reload preserves the active variant;
- the active variant is obvious;
- the switcher leaves important UI unobscured at relevant viewport sizes;
- prototype-only chrome is hidden or unreachable in production builds.
