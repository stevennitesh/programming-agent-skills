# Smell Baseline

Use this baseline only when documented repo standards and meaningful nearby conventions are thin. Repo standards override it. Treat every smell as a judgement call, not a violation. Leave tooling-enforced style to tooling.

- **Mysterious Name:** Flag names that hide intent; rename them around the domain behavior they represent.
- **Duplicated Code:** Flag repeated knowledge or behavior; consolidate it at the narrowest stable owner.
- **Feature Envy:** Flag logic that depends more on another module's data than its own; move the behavior toward that data.
- **Data Clumps:** Flag values that repeatedly travel together; give the stable group a named type or parameter object.
- **Primitive Obsession:** Flag domain concepts encoded as loose strings, numbers, or flags; introduce a type when it protects rules or meaning.
- **Repeated Switches:** Flag repeated branching on the same type or state; centralize the variation behind one owner.
- **Shotgun Surgery:** Flag one change that requires scattered edits; pull the responsibility behind a single seam.
- **Divergent Change:** Flag one module that changes for unrelated reasons; split responsibilities along stable change axes.
- **Speculative Generality:** Flag abstractions without a current caller or requirement; remove them until concrete pressure exists.
- **Message Chains:** Flag callers that traverse object internals; expose the needed operation at a nearer boundary.
- **Middle Man:** Flag pass-through layers that add no policy or leverage; collapse them or give them real ownership.
- **Refused Bequest:** Flag inheritance whose consumers reject or override the parent contract; prefer a smaller interface or composition.
- **Scope-Shaped Abstraction:** Flag abstractions shaped around one task's temporary boundary; collapse them or move the seam to an enduring responsibility.
