# Refactoring After GREEN

Refactor only while tests are GREEN. Preserve observable behavior and the current public contract; intended behavior or contract changes start a new RED cycle.

Prefer moves that increase **depth**, **leverage**, or **locality**:

- remove duplication introduced by the tracer bullet;
- rename concepts to match the domain glossary;
- move behavior to its owning module;
- deepen shallow modules behind smaller interfaces;
- consolidate scattered decisions;
- delete implementation-detail tests after better behavioral coverage exists.

Make one meaningful move at a time. Rerun the focused test after each move and the nearest relevant test group before leaving the tracer bullet. Preserve correct behavior tests and keep test-only hooks out of production interfaces.

Stop when the intended material cleanup is complete and the focused plus nearest relevant tests are GREEN, or when the next improvement would expand scope.

If refactoring reveals a larger design problem, return it as residual follow-up evidence without mutating a tracker or widening the slice. Recommend `$codebase-design` and stop for one bounded interface or seam question. Recommend `$improve-codebase-architecture` and stop for a wide candidate-finding survey.
