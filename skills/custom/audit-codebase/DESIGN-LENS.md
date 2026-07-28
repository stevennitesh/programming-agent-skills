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
- **Interface is the Test Surface:** callers and behavior tests should cross
  the same Seam. Tests that must reach past it expose misplaced ownership or
  an incomplete Interface.
- **Variation Test:** a Seam is earned by supported variation or required
  substitution at a real external boundary. A fake created only because the
  Seam exists is not independent evidence.

Example:

```text
Before: Handler -> Validator -> Mapper -> Repository wrapper
        each Interface exposes the next Module

After:  Order intake Module
        one caller-facing Interface; validation, mapping, and persistence
        coordination remain hidden Implementation
```

The after shape is stronger only when it increases Leverage and Locality while
preserving a justified persistence Seam. Fewer boxes alone are not proof.

## Dependency Classes

- **In-process:** pure computation or in-memory state; test directly.
- **Local-substitutable:** a real local stand-in exists; keep its Seam internal
  when callers do not need it.
- **Remote but owned:** a port and production/test Adapters may be earned.
- **True external:** inject the external dependency at the narrowest useful
  Seam and test with a controlled Adapter.

## Candidate Bound

During subsystem audit, name the friction and change direction, not an exact
new public Interface. During candidate analysis, compare keep, inline/merge,
deepening, Seam movement, and earned Adapter alternatives.

For a design or mixed candidate, settle any user-owned trade-off first, then
load `$codebase-design` Direct Design and fold its result into the candidate.
Audit retains the HTML and Return; emit no separate design packet or later
Codebase Design step.
