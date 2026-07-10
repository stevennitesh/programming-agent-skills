---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
---

# Improve Codebase Architecture

Run this as **periodic architecture maintenance** or when one concept requires too much bouncing across small modules.

This skill is the **survey**: surface **architectural friction** and propose **deepening opportunities**. `$codebase-design` is the **design bench** for the chosen candidate.

This is discovery and decision work, not refactoring. Do not implement changes. Find candidates, make the friction visible, help the user choose one, then recommend one next route.

Use repo domain language for business concepts and `$codebase-design` for architecture claims. Domain language names good seams; architecture language judges depth; ADRs mark decisions this skill should not re-litigate.

## Process

### 1. Explore

Read `docs/agents/engineering-contract.md` when present; keep candidates inside its slicing, proof, and commitment-boundary discipline.

Follow `docs/agents/domain.md` to the relevant glossary and ADRs. If no routing exists, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR/domain docs.

Explore organically. Follow architectural friction first, checklist second.

Look for:

- shallow modules: interface nearly as complex as implementation
- behavior or decisions spread across callers
- pure functions extracted only for testability while bugs hide in how they are called
- seams that leak implementation knowledge
- pass-through adapters or wrappers
- owned modules mocked in tests instead of behavior proved through an interface
- scattered domain ownership that makes fresh-agent navigation hard
- behavior-preserving support slices that would unlock later tracer bullets

Apply the **deletion test**: would removing this module concentrate complexity behind a smaller interface, or just move it around? Only "concentrates" earns a candidate.

Filter hard. A report full of cleanup advice has failed the skill. Keep only candidates that plausibly improve **depth**, **leverage**, **locality**, test surface, or AI-navigability.

### 2. Present Candidates

Write a self-contained HTML report to repo-local `.tmp/architecture-reviews/` when available, with OS temp as fallback. Do not stage or commit generated reports.

Open the report for the user when possible and report the absolute path.

Use [HTML-REPORT.md](HTML-REPORT.md) for card fields, visual style, tone, and diagram patterns.

Make the report visual first: diagrams prove shallowness and proposed depth.

ADR conflicts: surface only friction worth reopening.

End with a numbered **Top recommendation**.

After the report is written and opened or reported, ask:

> Which candidate number would you like to explore? I recommend Candidate N because ...

### 3. Grill The Chosen Candidate

Run `$grilling` on the chosen candidate: constraints, seams, adapters or substitutes, validation, migration, and out-of-scope boundaries.

Use `$codebase-design` only when the candidate needs dependency classification, seam discipline, or design-it-twice alternatives.

Durable language: use `$domain-modeling` only for resolved domain terms or ADR-worthy decisions. Do not record ephemeral "not now" reasons.

### 4. Recommend One Route

After grilling, classify the candidate:

- **single-slice**: one bounded slice can complete the architectural intent
- **multi-slice**: direction is clear, but completion needs dependency-ordered slices
- **underspecified**: intent, acceptance, architecture, or validation is unresolved

Recommend exactly one route:

- `$implement` for single-slice candidates with clear validation and no major unresolved decisions
- `$to-tickets` for multi-slice candidates, even when the first slice is ready
- `$to-spec` when product behavior, user-facing concerns, parent spec, acceptance, architecture, or validation is unresolved

## Completion Criteria

Initial pass done means a visual report was written outside staged files, only real deepening candidates survived, the path was reported or opened, no refactor was implemented, and the user was asked which candidate to explore.

Chosen-candidate pass done means the candidate was grilled through constraints, seams, validation, migration, and scope boundaries; classified as single-slice, multi-slice, or underspecified; and recommended to exactly one next skill.
