# Validator Enforces Publishing Hygiene, Not Language

> **Current applicability — [ADR-0018](0018-astra-composition-and-decision-applicability.md):** Retained: validators enforce mechanical integrity rather than prose vocabulary. Current checks belong to the repository validator; this record does not prescribe its complete check inventory.
> Status and decisions below preserve the original record; this notice controls present applicability.

The validator checks public-publishing hygiene such as secrets and ignored files, but it does not police vocabulary. We chose this because language is how the skill pack steers agent behavior; forbidding ordinary words can erase useful leading words, weaken Matt Pocock-style vocabulary, and push maintainers toward worse phrasing just to satisfy a brittle check.

**Consequences**:
Language quality is reviewed through `CONTEXT.md`, `$writing-for-agents`, skill review, and human judgment. The validator should stay focused on mechanical risks that are safe to automate.
