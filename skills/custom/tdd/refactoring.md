# Refactoring After GREEN

Refactor only while tests are GREEN.

The goal is to improve design without changing behavior. Keep the tested public **interface** stable unless the tracer bullet proved the interface is wrong. If the interface must change, stop and start a new RED cycle for the intended behavior through the new interface.

The interface is the test surface. Refactoring should make behavior easier to prove through that surface, not add private seams or test-only hooks.

## Moves

Prefer moves that increase **depth**, **leverage**, or **locality**:

- Remove duplication that appeared during the tracer bullet.
- Rename concepts to match the domain glossary.
- Move behavior to the module that owns the domain concept.
- Deepen shallow modules: move complexity behind a smaller interface.
- Replace scattered branching with one module that owns the decision.
- Replace test-only seams with real seams only when real adapters justify them.
- Delete implementation-detail tests once behavior is covered through a better interface.

These are refactoring moves only when behavior stays the same. New behavior starts a new RED cycle.

## Discipline

Make one meaningful refactor at a time.

After each move, rerun the focused test that just went GREEN. If it fails, fix or revert the refactor before continuing.

Before leaving the tracer bullet, rerun the nearest relevant test group.

Do not add behavior while refactoring.

Do not change a passing behavior test just to fit the refactor. Change tests only when the public interface intentionally changes or the test was coupled to implementation details.

Do not add production methods, flags, visibility, or optional parameters solely for tests. Put setup, cleanup, and inspection helpers in test utilities unless they are real public interface behavior.

## Stop

Stop refactoring when the slice is clear, the interface is testable, and the next improvement would expand scope beyond the current tracer bullet.

If refactoring reveals a larger design problem, record it as a follow-up instead of widening the slice. Use `$codebase-design` or `$improve-codebase-architecture` when the follow-up needs architectural exploration.
