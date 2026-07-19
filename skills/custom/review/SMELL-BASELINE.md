# Smell Baseline

**Fallback only:** use this baseline only when documented repo standards and meaningful nearby conventions are thin. Repo standards override it. Treat each smell as a judgement prompt, not a violation or automatic refactoring prescription. Report one only when the diff creates a concrete, actionable maintainability risk; state the required outcome, and leave tooling-enforced style to tooling.

- **Mysterious Name:** names hide intent; rename them around the represented domain behavior.
- **Duplicated Code:** knowledge or behavior repeats; consolidate it at the narrowest stable owner.
- **Feature Envy:** logic chiefly manipulates another owner's data without coordinating policy; move it toward that owner when cohesion improves.
- **Data Clumps:** values repeatedly travel together with shared meaning or invariants; introduce a named type or parameter object when it protects that concept.
- **Primitive Obsession:** loose strings, numbers, or flags encode domain concepts; introduce a type when it protects rules or meaning.
- **Repeated Switches:** branching repeats on the same type or state; centralize the variation behind one owner.
- **Shotgun Surgery:** one change requires scattered edits; pull the responsibility behind a single seam.
- **Divergent Change:** one module changes for unrelated reasons; split responsibilities along stable change axes.
- **Speculative Generality:** an abstraction lacks a current caller or requirement; remove it until concrete pressure exists.
- **Message Chains:** callers traverse object internals; expose the needed operation at a nearer boundary.
- **Middle Man:** pass-through layers add no policy or leverage; collapse them or give them real ownership.
- **Refused Bequest:** a subtype cannot honor or use much of its inherited contract; narrow the interface or prefer composition.
- **Scope-Shaped Abstraction:** an abstraction follows one task's temporary boundary; collapse it or move the seam to an enduring responsibility.
