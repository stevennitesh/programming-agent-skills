---
name: clarify-scope
description: Use when a coding request is unclear, broad, user- or caller-visible, architectural, or likely to change runtime behavior, public contracts, tests, release risk, data/state, or rollback path.
---

# Clarify Scope

Turn unclear coding work into a clear implementation boundary, caller-visible behavior, and testable next slice.

## Rule

Clarify only what can change source code, tests, public or caller behavior, API/CLI/UI contracts, data/state, release risk, or the rollback path.

Prefer repo evidence over questions. Prefer a small caller-visible, testable slice over a broad design.

## Procedure

1. Inspect relevant repo evidence first: instructions, source entry points/callers, tests/fixtures, docs/specs, issues/PRs, diffs, logs, or CI output.
2. State a compact frame:

```text
Goal:
User or caller:
Current behavior:
Target behavior:
Public or caller contract:
Affected entry points/modules:
Success criteria:
Constraints:
Assumptions:
Repo evidence:
Blocking question:
```

3. If one answer changes code shape, public contract, test strategy, release risk, or rollback path, ask one question. Include why it matters, your recommended assumption, and what you will assume if accepted.
4. If repo evidence can answer the question, inspect it instead of asking.
5. If the request is too large, split first. Name the smallest user-visible or caller-visible slice that can be built, tested, and reviewed on its own.
6. For user-facing, API, CLI, UI, or module behavior, separate the observed need or failing workflow from the proposed implementation. Treat unsupported claims as assumptions.
7. For interface work, describe the caller-visible contract: inputs, outputs, invariants, ordering, error modes, required configuration, performance expectations, and compatibility expectations.
8. If unfamiliar with the area, zoom out before designing:

```text
entry point -> callers or users -> public contract -> state/data changed -> failure modes -> module boundary -> existing checks
```

9. If multiple approaches are plausible, present at most three. Tie trade-offs to correctness, compatibility, maintainability, delivery risk, or testability. Recommend one.

## Design Brief

Produce only the fields that help the next step:

```text
Goal:
Non-goals:
Current behavior:
Proposed behavior:
Public or caller contract:
Affected entry points/modules:
Data/state touched:
Acceptance checks:
Verification command or check:
Risks and rollback:
Open questions:
Next skill:
```

## Shared Language

- Use `CONTEXT.md`, ADRs, docs, or glossary files for recurring domain terms, module boundaries, and public contracts.
- Add or propose a `CONTEXT.md` note only for a term, boundary, contract, state transition, or "means / does not mean" distinction likely to recur.
- Keep entries tiny: term, meaning, non-meaning when useful, and source or reason.
- Never record progress, plans, status, skill summaries, or temporary decisions there.
- Treat context as a map. Current behavior comes from repo evidence; target behavior comes from approved user instruction, issue, PRD, or spec.

## Avoid

- Asking about preferences that do not change the work.
- Designing for future features not in the goal.
- Writing a plan before target behavior, public contract, and module boundary are clear.
- Turning every decision into docs; record only hard to roll back, surprising, contract-shaping decisions.
- Treating broad architecture as progress when a small tested slice or focused code read would answer.

## Exit

Stop when target behavior can be tested, the implementation boundary is clear, and remaining unknowns are non-blocking or stated assumptions.

## Handoff

- `slice-plan`: scoped work needs multiple reviewable source, test, docs, or tracking slices.
- `issue-driven-execution`: the user wants the clarified work turned into a plan doc, GitHub issues, and issue-by-issue execution.
- `tdd-slice`: behavior implementation.
- `diagnose-loop`: investigation reveals a bug.
- `github-tracking`: the result should become a PRD, issue, or long-lived decision record.
