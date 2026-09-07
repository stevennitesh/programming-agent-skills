# Skills Encode Local Contract Slices

> **Current applicability — [ADR-0018](0018-astra-composition-and-decision-applicability.md):** Partially superseded: task-specific skill procedures remain useful; copying shared engineering rules into skill-local contract slices is replaced by the single shared owner and conditional pointers in ADR-0018.
> Status and decisions below preserve the original record; this notice controls present applicability.

Skills should encode the part of the engineering contract that directly affects their own behavior, not require every skill to reread the whole contract. We chose this to preserve predictability and reduce context load while keeping each skill responsible for the discipline it actually executes.

**Consequences**:
When the contract changes, audit affected skills for their local contract slice. Do not copy the full contract into every skill, and do not make every skill depend on reading `docs/agents/engineering-contract.md`.
