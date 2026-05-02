---
name: clarify-scope
description: Use when a coding request is fuzzy, product-facing, architectural, broad, ambiguous, or likely to change behavior, interfaces, tests, rollout risk, or reversibility.
---

# Clarify Scope

Turn unclear work into a buildable direction without adding process weight.

## Rule

Clarify only what can change implementation, tests, risk, user or caller behavior, or the ability to undo the work.

Prefer evidence over questions. Prefer a small usable slice over a broad design.

## Procedure

1. Inspect cheap context first: repo instructions, README, relevant docs, current code, tests, linked issue or PR, and recent patterns.
2. State a compact frame:

```text
Goal:
User or caller:
Likely success condition:
Constraints:
Assumptions:
Current evidence:
Blocking decision:
```

3. If one answer materially changes the work, ask one question. Include why it matters, your recommended default, and what you will assume if accepted.
4. If code or docs can answer the question, inspect them instead of asking.
5. If the request is too large, split first. Name the smallest user-visible or caller-visible slice that can be built, tested, and reviewed on its own.
6. For product or interface behavior, separate the user's need from the proposed solution. Treat unsupported opinions as assumptions.
7. For interface work, describe the caller-visible contract: inputs, outputs, invariants, ordering, error modes, required configuration, and performance expectations.
8. If unfamiliar with the area, zoom out before designing:

```text
entry point -> callers or users -> data changed -> failure modes -> implementation boundary -> existing checks
```

9. If multiple approaches are plausible, present at most three. Tie trade-offs to correctness, maintainability, delivery risk, or testability. Recommend one.

## Design Brief

Produce only the fields that help the next step:

```text
Goal:
Non-goals:
Current behavior:
Proposed behavior:
Inputs and outputs:
Impacted modules:
Acceptance checks:
Risks and rollback:
Open questions:
Next skill:
```

## Shared Language And Context.md

- Use existing `CONTEXT.md`, docs, glossary, or domain notes for vocabulary.
- If a new term, role, boundary, or "means / does not mean" distinction emerges and is likely to recur, add or propose a short `CONTEXT.md` entry.
- If no `CONTEXT.md` exists, create it only when the first entry is worth keeping.
- Keep entries small: term, meaning, non-meaning when useful, and source or reason.
- Do not record progress, plans, implementation status, skill summaries, or temporary decisions.
- For current behavior, code and tests are baseline. For target behavior, approved user instruction or spec is target.

## Avoid

- Asking about preferences that do not change the work.
- Designing for future features not in the goal.
- Writing a plan before behavior and boundary are clear.
- Turning every decision into docs; record only hard-to-reverse, surprising, trade-off decisions.
- Treating broad architecture as progress when a small tested slice would answer.

## Exit

Stop when behavior can be tested, the implementation boundary is clear, and remaining unknowns are non-blocking or stated assumptions. Hand off to `thin-plan` for multi-step work, `tdd-slice` for behavior implementation, `diagnose-loop` if the design reveals a bug, or `github-work-tracking` if the result should become a PRD, issue, or durable decision record.
