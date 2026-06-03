---
name: clarify-scope
description: Use when a coding request is unclear, broad, user- or caller-visible, architectural, or likely to change runtime behavior, public or caller contract, tests, release risk, data/state, or rollback path.
---

# Clarify Scope

Turn unclear coding work into a clear implementation boundary, caller-visible behavior, and testable next slice.

## Rule

Clarify only what can change source code, tests, public or caller behavior, API/CLI/UI contract, data/state, release risk, or the rollback path.

Prefer repo evidence over questions. Prefer a small caller-visible, testable slice over a broad design.

Public or caller contract = the compatibility promise a user, API, CLI, UI, workflow, or downstream module depends on.

When the user request or repo evidence is unclear, broad, architectural, user- or caller-visible, or likely to change runtime behavior, public or caller contract, tests, data/state, release risk, or rollback, clarify the implementation boundary before designing, planning, prototyping, opening issues, or editing production code.

First inspect the cheapest repo evidence named or implied by the request: entry point, caller or user path, tests or fixtures, docs or specs, issues, recent diffs, logs, CI output, or shared language files when terms affect the work.

Before proceeding or asking, account for current behavior, target behavior or missing target, public or caller contract, affected entry points/modules, success criteria, constraints, assumptions, repo evidence inspected, terminology risk, and the one blocking question, if any.

Ask exactly one blocking question only when repo evidence cannot resolve one material decision about target behavior, public or caller contract, test strategy, data/state/security, release or rollback risk, ownership boundary, or durable decision records. Use a reversible local assumption for non-blocking naming, formatting, helper shape, minor copy, test-file placement, or implementation preference.

## Procedure

1. Inspect relevant repo evidence first: instructions, source entry points/callers, tests/fixtures, docs/specs, issues/PRs, diffs, logs, CI output, or shared language files when terms affect the work.
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
Terminology risk or context note:
Blocking question:
```

3. If one material answer remains unresolved after evidence review, ask one question in this shape:

```text
Blocking question:
Why it matters:
Recommended assumption:
If accepted, I will:
```

4. If you are about to ask but cheap repo evidence can answer the question, inspect it instead.
5. If the request is too large, split first. Name the smallest user-visible or caller-visible slice that can be built, tested, and reviewed on its own.
6. For user-facing, API, CLI, UI, or module behavior, separate the observed need or failing workflow from the proposed implementation. Treat unsupported claims as assumptions.
7. For interface work, describe the public or caller contract: inputs, outputs, invariants, ordering, error modes, required configuration, performance expectations, and compatibility expectations.
8. If names are ambiguous, overloaded, or conflicting, resolve only the terms that can change behavior, the public or caller contract, data/state, module boundaries, tests, or durable records.
9. If unfamiliar with the area, zoom out before designing:

```text
entry point -> callers or users -> public or caller contract -> state/data changed -> failure modes -> module boundary -> existing checks
```

10. If multiple approaches are plausible, present at most three. Tie trade-offs to correctness, compatibility, maintainability, delivery risk, or testability. Recommend one.

## Prototype Option

Use a prototype only when a small throwaway artifact can answer a design, state-machine, data-model, or UI choice faster than more discussion.
Do not make prototypes part of normal TDD implementation.

Before proposing or creating one, state:

```text
Question it answers:
Prototype type: logic | state | data | UI
Artifact location:
Run command or URL:
Data/persistence safety:
Disposal or absorption path:
Decision capture:
```

Decision capture = the durable place where the answer will be recorded, such as an issue comment, ADR, plan note, or final implementation decision.

Prototype constraints:

- Mark it throwaway from the start.
- Use the repo's existing runtime and task runner; do not add a package manager or framework just for the prototype.
- Avoid production persistence, real irreversible mutations, credentials, network services, and external systems unless explicitly approved.
- Keep persistence in memory or in clearly marked scratch storage unless persistence is the question being tested.
- Do not add tests for the throwaway shell. If the validated logic is absorbed into production code, protect that behavior through `tdd-slice`.
- Do not generalize beyond the question. Delete losing UI variants, terminal shells, scratch routes, and unused prototype code after the answer is captured or absorbed.

## Design Brief

Produce only the fields that help the next step:

```text
Goal:
Non-goals:
Current behavior:
Proposed behavior:
Public or caller contract:
Affected entry points/modules:
Repo evidence:
Data/state touched:
Acceptance checks:
Verification command or check:
Risks and rollback:
Terminology risk or context note:
Prototype question/artifact:
Decision capture:
Open questions:
Next skill:
```

## Shared Language

- Use `CONTEXT.md`, `CONTEXT-MAP.md`, relevant ADRs, docs, or glossary files for recurring domain terms, module boundaries, and public or caller contracts.
- If these files do not exist, proceed silently unless the current work resolves a recurring term, boundary, contract, state transition, or durable decision.
- If a user term conflicts with repo vocabulary, source, tests, docs, or ADRs, surface the conflict. Recommend the source-backed term when evidence is strong; ask one material question when it is not.
- If a term is overloaded, name the competing meanings and resolve only the one that affects the current behavior, interface, data/state path, test, or durable record.
- Add or propose a `CONTEXT.md` note only for a term, boundary, contract, state transition, or "means / does not mean" distinction likely to recur.
- Keep entries tiny: term, meaning, non-meaning when useful, and source or reason.
- Never record specs, scratch notes, progress, plans, status, skill summaries, or temporary decisions there.
- Offer an ADR only when a decision is hard to reverse, surprising without context, and the result of a real trade-off.
- Treat context as a map. Current behavior comes from repo evidence; target behavior comes from approved user instruction, issue, PRD, or spec.

## Forbidden Shortcuts

- Asking about preferences that do not change the work.
- Asking a list of questions when one material blocking question would unblock the next slice.
- Asking before checking cheap repo evidence that could answer the question.
- Designing for future features not in the goal.
- Replacing one material blocking question with a broad architecture plan.
- Starting implementation, tracker creation, or prototype work before the behavior frame makes the target testable.
- Prototyping when a focused code read, test, fixture, or one material question would answer.
- Letting prototype code become production code without normal implementation, review, and tests.
- Writing a plan before target behavior, public contract, and module boundary are clear.
- Turning every decision into docs; record only hard to roll back, surprising, contract-shaping decisions.
- Treating broad architecture as progress when a small tested slice or focused code read would answer.

## Stop Or Ask

Stop or ask when:

- target behavior, caller-visible success criteria, test strategy, data/state/security, release or rollback risk, or ownership boundary remains materially ambiguous after evidence review
- a term conflict changes behavior, public or caller contract, data/state, test expectations, or durable records and repo evidence does not resolve it
- multiple plausible public or caller contracts remain after evidence review
- a prototype would require production persistence, irreversible mutation, credentials, external services, a new runtime/package manager, or unclear cleanup
- a UI or visual decision cannot be resolved through text and no prototype, mockup, or visual check has been approved

## Exit

Stop when target behavior can be tested, the implementation boundary is clear, and remaining unknowns are non-blocking or stated assumptions.

## Handoff

- `slice-plan`: scoped work needs multiple reviewable source, test, docs, or tracking slices.
- `issue-driven-execution`: the user wants the clarified work turned into a plan doc, GitHub issues, and issue-by-issue execution.
- `tdd-slice`: behavior implementation.
- `diagnose-loop`: investigation reveals a bug.
- `codebase-cleanup`: clarification reveals module-boundary, duplicate-vocabulary, caller-interface, or test-surface problems.
- `github-tracking`: the result should become a PRD, issue, or long-lived decision record.
- Consider a future `prototype-spike` skill only if prototype work becomes common enough that this skill's compact option is no longer enough.
