# Smell Baseline

Use this baseline only when documented repo standards and meaningful nearby conventions are thin. Repo standards override it. Treat each smell as a judgement prompt, not a violation or automatic refactoring prescription. Report one only when the diff creates a concrete, actionable maintainability risk; state the required outcome, and leave tooling-enforced style to tooling.

- **Mysterious Name:** Flag names that hide intent; rename them around the domain behavior they represent.
- **Duplicated Code:** Flag repeated knowledge or behavior; consolidate it at the narrowest stable owner.
- **Feature Envy:** Flag logic that chiefly manipulates another owner's data without adding coordinating policy; move it toward that owner when doing so improves cohesion.
- **Data Clumps:** Flag values that repeatedly travel together and carry shared meaning or invariants; introduce a named type or parameter object when it would protect that concept.
- **Primitive Obsession:** Flag domain concepts encoded as loose strings, numbers, or flags; introduce a type when it protects rules or meaning.
- **Repeated Switches:** Flag repeated branching on the same type or state; centralize the variation behind one owner.
- **Shotgun Surgery:** Flag one change that requires scattered edits; pull the responsibility behind a single seam.
- **Divergent Change:** Flag one module that changes for unrelated reasons; split responsibilities along stable change axes.
- **Speculative Generality:** Flag abstractions without a current caller or requirement; remove them until concrete pressure exists.
- **Message Chains:** Flag callers that traverse object internals; expose the needed operation at a nearer boundary.
- **Middle Man:** Flag pass-through layers that add no policy or leverage; collapse them or give them real ownership.
- **Refused Bequest:** Flag a subtype that cannot honor or use much of its inherited contract; narrow the interface or prefer composition.
- **Scope-Shaped Abstraction:** Flag abstractions shaped around one task's temporary boundary; collapse them or move the seam to an enduring responsibility.
