# Domain Modeling Records Approved ADRs

> **Current applicability — [ADR-0018](0018-astra-composition-and-decision-applicability.md):** Partially superseded: distinguish settling a decision from recording it. Astra shape-work owns conditional domain modeling and authorized ADR reconciliation; there is no standalone Domain Modeling route or additional approval turn when the user has already authorized the record.
> Status and decisions below preserve the original record; this notice controls present applicability.

Domain Modeling is the skill pack's single recorder for explicitly approved ADR-worthy decisions. The workflow that owns the underlying domain, product, interface, architecture, or engineering decision retains settlement authority; Domain Modeling assesses worthiness, records only settled decisions, and creates an ADR only after separate explicit approval.

**Consequences**:
Decision-owning workflows return settled ADR candidates instead of duplicating ADR persistence. Domain Modeling's recording authority never grants authority to make a non-domain decision or continue the originating workflow.
