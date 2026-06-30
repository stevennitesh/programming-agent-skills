# Setup Installs The Repo-Local Engineering Contract

`setup-matt-pocock-skills` installs the engineering contract into each target repo instead of relying only on this source repo's README or skill files. We chose this because target repos need the operating discipline in their own context: agents should be able to orient from local files, issue-tracker rules, triage labels, and domain-doc routing without rediscovering the skill pack's intent.

**Consequences**:
The setup skill owns the target repo setup surface. Changes to the engineering contract should update both the source template and the public docs that explain why it exists.
