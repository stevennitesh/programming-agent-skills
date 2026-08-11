# Codebase Design Lens

Use this vocabulary exactly for architecture claims. Use repository and domain
terms for business concepts.

## Concepts

- **Module:** an Interface plus its hidden Implementation; scale may be a
  function, class, package, workflow, or tier-spanning slice.
- **Interface:** everything callers must know: operations, inputs, outputs,
  Invariants, ordering, errors, configuration, performance, and behavior.
- **Implementation:** behavior and design decisions hidden behind the Interface
  through **information hiding**.
- **Depth:** coherent functionality relative to Interface burden; not a
  ratio of implementation lines to interface lines.
- **Deep Module:** a small Interface hiding substantial useful behavior.
- **Shallow Module:** an Interface nearly as burdensome as its Implementation.
- **Somewhat General-Purpose Module:** functionality stays within current needs,
  while the Interface avoids caller-specific special cases.
- **Seam:** where behavior can vary without editing callers; the Interface
  lives there.
- **Adapter:** a concrete Implementation satisfying an Interface at a Seam.
- **Change amplification:** the number of places a supported change requires.
- **Cognitive load:** the information a caller or maintainer must hold in mind.
- **Unknown unknowns:** affected code or dependencies that are hard to discover.

## Tests

- **Deletion Test:** imagine removing only the Module boundary while
  preserving supported behavior. If the same necessary complexity spreads
  into callers, the Module earns its keep. If behavior and proof become
  simpler at an existing owner, the boundary may be pass-through.
- **State Testing:** treat a test as the first user of an Interface. Callers and
  caller-facing tests should observe state through the same Interface. Use
  interaction testing only for contractual interactions or necessary failure
  isolation. A need to bypass the Interface is evidence of a possible
  ownership or information-hiding gap. Focused tests of hidden algorithms are
  not independently such evidence.
- **Variation Test:** a Seam is earned by supported variation or required
  substitution at a real external boundary. A fake created only because the
  Seam exists is not independent evidence.

Fewer boxes alone are not proof. Design establishes whether a boundary is
earned; Simplification owns the earliest sufficient removal or reuse direction.

Example: `Handler -> Validator -> Mapper -> Repository wrapper` may collapse
into one caller-facing Order intake Module only when Depth or information
hiding improves, complexity symptoms fall, and any persistence Seam remains
justified.

## Dependency Classes

- **In-process:** pure computation or in-memory state; test directly.
- **Local-substitutable:** a real local stand-in exists; keep its Seam internal
  when callers do not need it.
- **Remote but owned:** a port and production/test Adapters may be earned.
- **True external:** inject the external dependency at the narrowest useful
  Seam and test with a controlled Adapter.

## Candidate Bound

During subsystem Audit, name the Interface, Seam, ownership friction, and proof
impact, not an exact replacement API. Candidate Analyze owns the Keep /
Smallest sufficient / Structural / Replacement comparison.

For a design or mixed candidate, settle any user-owned trade-off first, then
apply `CANDIDATE-CONTRACT.md`'s design branch.
