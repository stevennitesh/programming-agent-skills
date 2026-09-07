# Separate Active And Experimental Skill Trees

> **Current applicability — [ADR-0018](0018-astra-composition-and-decision-applicability.md):** Superseded for current installation and routing: skills/astra is the managed source. The custom/experimental topology below describes historical pack organization, not current eligibility.
> Status and decisions below preserve the original record; this notice controls present applicability.

`skills/custom/` is the only active, routable, validated, and managed-install source. `skills/experimental/` preserves inactive alternatives under the same skill names, with provenance and tree identities recorded in `skills/experimental/manifest.json`; experimental candidates never enter the installed pack until explicitly promoted into `skills/custom/`.

This separation keeps the installed baseline authoritative for active behavior while retaining divergent design work without silently publishing it. `skills/.archive/` remains the destination for retired history rather than live experiments.
