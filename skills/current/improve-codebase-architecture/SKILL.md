---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: changes that turn shallow modules into deep ones. The aim is testability, AI-navigability, and better **locality** for future work.

This skill is a discovery and decision skill. It does not implement refactors. It finds candidates, visualizes why they matter, and helps the user choose one to explore.

Use the repo's domain glossary for domain language and `$codebase-design` for architecture language: **module**, **interface**, **implementation**, **depth**, **seam**, **adapter**, **leverage**, and **locality**.

## Process

### 1. Explore

Read `docs/agents/engineering-contract.md` when present so candidates respect the repo's slicing, proof, and commitment-boundary discipline.

When exploring codebase context, read `docs/agents/domain.md` when present and follow it to the relevant glossary and ADRs. If no routing exists, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR/domain docs.

Walk the codebase organically and note where understanding, changing, or testing one concept requires bouncing across many modules.

Look for:

- shallow modules: interface nearly as complex as implementation
- behavior or decisions spread across callers
- pure functions extracted only for testability while bugs hide in how they are called
- seams that leak implementation knowledge
- adapters that are only pass-through indirection
- owned modules mocked in tests instead of behavior proved through an interface
- code that is hard for a fresh agent to navigate because domain ownership is scattered
- areas where a behavior-preserving support slice would unlock later tracer bullets

Apply the deletion test to suspected shallow modules: if deleting it makes complexity vanish, it is probably pass-through; if complexity reappears across callers, tests, or workflows, it may be earning its keep.

A candidate earns its place only if it plausibly improves **depth**, **leverage**, **locality**, test surface, or AI-navigability. Do not include generic cleanup, style churn, speculative abstractions, or "nice to have" rewrites.

### 2. Present Candidates As An HTML Report

Write a self-contained HTML file to the repo-local temp directory. Resolve the repo root with `git rev-parse --show-toplevel` when available, create `.tmp/architecture-reviews/`, and write to:

```text
<repo-root>/.tmp/architecture-reviews/architecture-review-<timestamp>.html
```

If no repo root is available or `.tmp` cannot be written, fall back to the OS temp directory from `$TMPDIR`, `/tmp`, or `%TEMP%`.

Do not stage or commit generated `.tmp` reports.

Open it for the user when possible and report the absolute path.

Use [HTML-REPORT.md](HTML-REPORT.md) for the scaffold, visual style, candidate card shape, and diagram patterns.

Each candidate should include:

- **Number** - stable `Candidate N` identifier used in the report, top recommendation, and chat
- **Files** - files or modules involved
- **Problem** - what architectural friction exists
- **Why it matters** - the cost in locality, leverage, test surface, or AI-navigability
- **Deepening opportunity** - what responsibility could move behind a smaller interface
- **Dependency category** - from `$codebase-design` / `DEEPENING.md`
- **Validation angle** - how behavior could be proved through the deeper interface
- **Before / after diagram** - visual proof of shallowness and proposed depth
- **Recommendation strength** - `Strong`, `Worth exploring`, or `Speculative`

Use the repo's domain glossary vocabulary for domain concepts, and `$codebase-design` vocabulary for architecture. Preserve real repo/domain terms, but do not substitute vague architecture words for the shared vocabulary.

If a candidate contradicts an ADR, surface it only when the friction is real enough to justify revisiting the decision. Mark the conflict clearly and explain why it may be worth reopening.

Do not propose final interfaces yet. The report should show candidate areas and why they matter, not settle the design.

End the report with a **Top recommendation** section naming the numbered candidate you would explore first and why.

After the report is written and opened or reported, ask:

> Which candidate number would you like to explore? I recommend Candidate N because ...

### 3. Grill The Chosen Candidate

Once the user picks a candidate, run `$grilling` to walk the design tree: constraints, dependencies, current callers, the deeper module, what moves behind the interface, seam placement, adapters or substitutes, validation, migration path, and what stays out of scope.

Use `$codebase-design` after selection when the candidate needs dependency classification, seam discipline, or design-it-twice alternatives.

Use `$domain-modeling` only when durable domain terms or decisions actually land:

- Add a glossary term when the deepened module uses a domain concept not yet recorded.
- Sharpen fuzzy domain language when the user resolves it.
- Offer an ADR when the user rejects a candidate for a load-bearing reason future agents need to respect.

Do not write ADRs for ephemeral reasons, obvious non-decisions, or "not now."

### 4. Recommend The Next Route

After exploring the chosen candidate, recommend exactly one next route for the candidate as a whole.

Before choosing, classify the candidate:

- **single-slice**: one bounded behavior-preserving or behavior-changing slice can complete the candidate's architectural intent.
- **multi-slice**: the direction is clear, but completion requires multiple dependency-ordered slices.
- **underspecified**: product intent, acceptance criteria, architectural commitments, or validation expectations are still unresolved.

Choose:

- `$implement` only when the candidate is single-slice, validation is clear, and no major design or product decisions remain.
- `$to-issues` when the candidate is multi-slice, even if the first slice is already ready to implement.
- `$to-prd` when the change affects product behavior, crosses multiple user-facing concerns, needs a parent spec, or still has unresolved intent, acceptance criteria, architectural commitments, or validation expectations.

If the candidate is multi-slice but the first slice is obvious, name that first slice as a suggested Issue 1 under the `$to-issues` recommendation. Do not recommend `$implement` merely because the first slice is ready.

Do not run the next skill automatically. Stop after the recommendation unless the user asks to continue.

## Completion Criteria

Initial pass done means the codebase was explored through domain and architecture vocabulary, candidates were filtered for real deepening value, a self-contained HTML report was written to repo-local `.tmp` when available or OS temp as fallback with numbered candidates, the path was reported or opened, a numbered top recommendation was included, ADR conflicts were surfaced when relevant, no refactor was implemented, generated reports were not staged, and the user was asked which candidate number to explore.

After the user chooses a candidate, done means the candidate was grilled through constraints, seams, validation, migration, and out-of-scope boundaries; the candidate was classified as single-slice, multi-slice, or underspecified; and exactly one next route was recommended for the candidate as a whole: `$to-prd`, `$to-issues`, or `$implement`.
