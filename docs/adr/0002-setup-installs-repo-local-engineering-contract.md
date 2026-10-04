# Setup Installs The Repo-Local Engineering Contract

> **Current applicability — [ADR-0018](0018-astra-composition-and-decision-applicability.md):** Superseded for Astra: repo-bootstrap no longer supplies a generic engineering contract. It establishes only needed repository facts, accepted requirements, and workflow configuration. Existing substantive local requirements retain their owners.
> Status and decisions below preserve the original record; this notice controls present applicability.

`$repo-bootstrap` installs the engineering contract into each target repo instead of relying only on this source repo's README or skill files. We chose this because target repos need the operating discipline in their own context: agents should be able to orient from local files, issue-tracker rules, triage labels, and domain-doc routing without rediscovering the skill pack's intent.

**Consequences**:
The setup skill owns the target repo setup surface. Changes to the engineering contract should update both the source template and the public docs that explain why it exists.
