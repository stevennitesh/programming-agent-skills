# Codebase Design Lens

Use this vocabulary exactly for architecture claims. Use repository and domain
terms for business concepts.

## Concepts

- **Module:** an Interface plus its hidden Implementation; scale may be a
  function, class, package, workflow, or tier-spanning slice.
- **Interface:** everything callers must know: operations, inputs, outputs,
  Invariants, ordering, errors, configuration, performance, and behavior.
- **Implementation:** behavior hidden behind the Interface.
- **Depth:** caller and test Leverage per unit of Interface learned; not a
  ratio of implementation lines to interface lines.
- **Deep Module:** a small Interface hiding substantial useful behavior.
- **Shallow Module:** an Interface nearly as burdensome as its Implementation.
- **Seam:** where behavior can vary without editing callers; the Interface
  lives there.
- **Adapter:** a concrete Implementation satisfying an Interface at a Seam.
- **Leverage:** capability callers gain per unit of Interface learned.
- **Locality:** change, bugs, decisions, knowledge, and verification
  concentrate in one place.

## Tests

- **Deletion Test:** imagine removing only the Module boundary while
  preserving supported behavior. If the same necessary complexity spreads
  into callers, the Module earns its keep. If behavior and proof become
  simpler at an existing owner, the boundary may be pass-through.
- **Interface is the Test Surface:** callers and caller-facing behavior tests
  should cross the same Seam. Their need to bypass it is evidence of a possible
  ownership or Interface gap. Focused tests of hidden algorithms are not
  independently such evidence.
- **Variation Test:** a Seam is earned by supported variation or required
  substitution at a real external boundary. A fake created only because the
  Seam exists is not independent evidence.

Fewer boxes alone are not proof. Design establishes whether a boundary is
earned; Simplification owns the earliest sufficient removal or reuse direction.

Example: `Handler -> Validator -> Mapper -> Repository wrapper` may collapse
into one caller-facing Order intake Module only when Leverage and Locality
improve and any persistence Seam remains justified.

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
load `$codebase-design` Direct Design and fold its result into the candidate.
Audit retains the HTML and Return; emit no separate design packet or later
Codebase Design step.
