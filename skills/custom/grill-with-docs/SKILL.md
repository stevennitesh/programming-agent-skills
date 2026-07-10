---
name: grill-with-docs
description: Compose a repo-backed grilling session with durable domain capture. Use when both the interview loop and domain-model upkeep are required, including when another skill needs both.
---

# Grill With Docs

Run one `$grilling` session with `$domain-modeling` active throughout.

When a caller supplies a bound, pass it to `$grilling`. Treat material branches beyond that bound as explicit deferrals to the caller's named artifact or workflow; keep the normal Confirmed and Evidence gap exits.

- `$grilling` owns the design tree, one-decision turns, and exit packet.
- `$domain-modeling` owns every `CONTEXT.md` or ADR write and applies its persistence and approval rules unchanged.

**Domain gate:** before either exit, ensure every resolved domain term is captured and every resolved ADR-worthy decision is offered or recorded. Add changed domain paths and ADR outcomes to the exit packet.

Return through `$grilling`'s **Confirmed** or **Evidence gap** gate.
