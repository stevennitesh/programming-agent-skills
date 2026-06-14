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

Use the fast path by default:

1. Inspect the cheapest repo evidence that could answer the ambiguity: instructions, source entry points/callers, tests/fixtures, docs/specs, issues/PRs, diffs, logs, CI output, or shared language files when terms affect the work.
2. Identify only the material missing decision.
3. If blocked, ask one question in this shape:

```text
Blocking question:
Why it matters:
Recommended assumption:
If accepted, I will:
```

4. If not blocked, state the reversible assumption and proceed to the next route.

If the request is too large, name the smallest user-visible or caller-visible slice that can be built, tested, and reviewed on its own. If multiple approaches are plausible, present at most three, tie trade-offs to correctness, compatibility, maintainability, delivery risk, or testability, and recommend one.

For interface work, describe only the contract details that matter to the next route: inputs, outputs, invariants, ordering, error modes, required configuration, performance expectations, and compatibility expectations.

If unfamiliar with the area, zoom out only enough to answer the ambiguity:

```text
entry point -> callers or users -> public or caller contract -> state/data changed -> failure modes -> module boundary -> existing checks
```

## One Blocking Question

Ask exactly one blocking question only when repo evidence cannot resolve one material decision. Use reversible assumptions for non-blocking naming, formatting, helper shape, minor copy, test-file placement, or implementation preference.

Use this shape and no extra template unless the work needs a durable brief:

```text
Blocking question:
Why it matters:
Recommended assumption:
If accepted, I will:
```

## Niche Prototype Path

Use only when source/test evidence and one material question are slower or insufficient, and a small throwaway artifact can answer a specific design, state-machine, data-model, or UI choice faster than discussion.

State only the prototype question, artifact location, run command or URL, data/persistence safety, disposal or absorption path, and durable decision capture.

Prototype constraints:

- Mark it throwaway from the start.
- Use the repo's existing runtime and task runner; do not add a package manager or framework just for the prototype.
- Avoid production persistence, real irreversible mutations, credentials, network services, and external systems unless explicitly approved.
- Keep persistence in memory or in clearly marked scratch storage unless persistence is the question being tested.
- Do not add tests for the throwaway shell. If the validated logic is absorbed into production code, protect that behavior through `tdd-slice`.
- Do not generalize beyond the question. Delete losing UI variants, terminal shells, scratch routes, and unused prototype code after the answer is captured or absorbed.

## Durable Brief

Use a design brief only when clarification must become a durable plan, issue, PRD, ADR, or handoff.

```text
Goal:
Non-goals:
Current behavior:
Proposed behavior:
Public or caller contract:
Affected entry points/modules:
Acceptance checks:
Risks and rollback:
Repo evidence:
Open questions:
Next skill:
```

## Shared Language

Use durable context only for recurring terms, module boundaries, public or caller contracts, state transitions, or "means / does not mean" distinctions likely to matter again.

If a term conflict changes behavior, interface, data/state path, tests, or durable records, surface the conflict. Recommend the source-backed term when evidence is strong; ask one material question when it is not.

Keep entries tiny and factual. Never record specs, scratch notes, progress, plans, status, skill summaries, or temporary decisions there. Offer an ADR only when a decision is hard to reverse, surprising without context, and the result of a real trade-off.

Treat context as a map. Current behavior comes from repo evidence; target behavior comes from approved user instruction, issue, PRD, or spec.

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
