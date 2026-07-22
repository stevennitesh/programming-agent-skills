# UI Prototype

Use this branch for one decision about visual hierarchy, information density, navigation, flow, or interaction structure. [SKILL.md](SKILL.md) owns Freeze, authority, the lifecycle, reconciliation, and Return. This file owns only UI Probe, Smoke, and verdict-evidence mechanics.

## Host

Judge UI under real constraints. Use an existing route and its data, parameters, auth, navigation, and surrounding layout when available and authorized. Use a throwaway route only for a genuinely new top-level surface or standalone flow.

Application-tree work requires the exact frozen paths and a pre-existing development-only or build-excluded boundary that positively isolates the whole prototype surface. Omitting links is not isolation. Use an isolated host or return blocked when repository proof cannot establish production unreachability.

## Bets

Build structurally different bets about layout, hierarchy, density, navigation, or primary affordance. Default to three, use two for a genuinely binary decision, and never exceed five. Color, copy, spacing, or icon changes alone are distinct only when that property is the frozen question.

Keep the same decision-relevant purpose, data, and constraints across variants. Use the repository's component and styling system. Keep mutations fake or stubbed and prototype controls visually distinct from the product surface.

## Switch And Inspect

Give each variant a stable key and direct URL. When the host permits, keep selection URL-backed, make the active variant obvious, wrap previous/next controls, and preserve selection across reload. Gate variant routing, subtrees, and controls together.

Inspect in the actual browser or target UI at decision-relevant viewport sizes. Source inspection alone is not UI evidence.

## Smoke And Evidence

Smoke passes when the real context loads, every variant is reachable and structurally different, switching and reload are stable where supported, controls do not hide important UI, and repository proof confirms the whole surface is unreachable from production behavior and shipping entry points.

Verdict evidence is the named human's explicit feedback or the result of the frozen rule over the representative interactions. Record constraints that could change the judgment.

Return to `Judge` in [SKILL.md](SKILL.md); this branch does not Reconcile or Return.
