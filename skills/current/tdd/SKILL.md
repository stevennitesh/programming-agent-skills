---
name: tdd
description: "Test-driven development through tracer-bullet vertical slices. Use when the behavior change is understood enough to write a red test: features, bug fixes with a known repro, behavior changes, and integration coverage."
---

# Test-Driven Development

Use TDD to build one **tracer bullet** at a time: one failing behavior test through the highest useful public **interface** or **seam**, one minimal implementation that makes it pass, then one green refactor if needed.

Use `$diagnosing-bugs` first when the symptom, root cause, or repro is uncertain. Use `$tdd` once the behavior to prove is clear enough to write a red test.

When another skill says to prove a code slice, do not weaken this discipline into after-the-fact checks. If the behavior is suitable for TDD, prove it through red-green-refactor.

See [tests.md](tests.md) for good and bad test examples, [mocking.md](mocking.md) when a seam needs a fake, stub, or mock, and [refactoring.md](refactoring.md) after GREEN.

## Philosophy

A tracer bullet earns its place by reducing uncertainty about behavior, a seam, or a risk. Prefer a few strong tracer bullets over many weak variations.

A good test reads like a specification: it names what a caller or user can do and proves the outcome through the system's interface. A bad test couples to implementation: it mocks owned modules, tests private helpers, asserts internal calls, or breaks when behavior is unchanged but internals move.

The interface is the test surface. If a behavior is hard to test, treat that as design feedback: the interface may be too shallow, too coupled, or at the wrong seam. Mock only at system boundaries through adapters.

## Anti-Pattern: Horizontal Slices

Do not write all tests first, then all implementation.

Horizontal slicing outruns your understanding:

```text
WRONG:
  RED:   test1, test2, test3, test4
  GREEN: impl1, impl2, impl3, impl4
```

Move vertically through tracer bullets:

```text
RIGHT:
  test1 -> verify RED -> impl1 -> verify GREEN -> refactor
  test2 -> verify RED -> impl2 -> verify GREEN -> refactor
  test3 -> verify RED -> impl3 -> verify GREEN -> refactor
```

Each test should respond to what the previous cycle taught you.

## Preconditions

Read `docs/agents/engineering-contract.md` when present before this TDD pass changes repo behavior.

When exploring the codebase, read `docs/agents/domain.md` if present so test names and behavior descriptions use the repo's domain glossary and respect ADRs. Otherwise, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR/domain docs.

Resolve the behavior from the issue, PRD, spec, acceptance criteria, bug report, or current user request. Ask only when the behavior, public interface, or test seam would otherwise be guesswork.

## Workflow

### 1. Choose The Next Tracer Bullet

Pick one narrow behavior to prove next.

The behavior should be observable by a caller or user, cross the highest useful public interface or seam, and move the implementation toward an acceptance criterion.

Start with the happy path when no path is proven yet. Add another tracer bullet only when it proves a materially distinct behavior, branch, failure mode, permission boundary, state transition, integration seam, or migration risk.

Stop adding tracer bullets when remaining cases are data variations of the same behavior. Use smaller focused tests for dense pure logic when they add confidence, but keep them behind a meaningful module interface.

Do not pick speculative edge cases before the main path is green. Do not split by layer unless the slice is a behavior-preserving prefactor that unlocks later tracer bullets.

### 2. RED

Write one focused test for the behavior.

The test should describe behavior in domain language, use real code paths where practical, and assert observable outcomes rather than internal calls.

Run the focused test before writing production code.

Verify RED:

- the test fails
- the failure is expected
- the failure is caused by missing or wrong behavior, not setup, typo, import, fixture, or unrelated breakage

If the test passes immediately, stop. Rewrite the test or choose behavior not already covered.

If you already wrote production code for this behavior in the current session before a RED test, treat that code as exploration. Prefer to set it aside, write the test, watch RED, then reintroduce only the code needed to make the test GREEN.

### 3. GREEN

Write the smallest production change that makes the focused test pass.

Do not add future behavior, broad cleanup, new abstractions, or unrelated fixes.

Run the focused test. Then run the nearest relevant test group.

Verify GREEN:

- the focused test passes
- the behavior is implemented through the chosen interface or seam
- nearby tests still pass
- output is clean enough to trust

If a test fails, fix production code unless the test is proving the wrong behavior.

### 4. REFACTOR

Refactor only while GREEN.

Use [refactoring.md](refactoring.md). Keep behavior unchanged and rerun the focused tests after each meaningful move.

Prefer deepening modules over adding shallow pass-through helpers. The interface is the test surface.

### 5. Repeat

Pick the next tracer bullet and repeat.

Stop when acceptance criteria are proven through tests, or when a remaining behavior needs user clarification.

## Completion Criteria

Done means each implemented behavior was built as a tracer bullet that reduced uncertainty, each test went RED for the expected reason before implementation, GREEN was verified through the chosen interface or seam, refactoring happened only while GREEN, and relevant validation was run or explicitly skipped.
