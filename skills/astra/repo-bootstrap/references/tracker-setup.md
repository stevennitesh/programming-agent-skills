# Tracker setup

Read only when tracker configuration is requested or already established repository
practice needs agent guidance. A repository remote does not by itself establish
that issues are used.

## Select and record the actual tracker

Preserve the established provider even when it differs from Git hosting. If no
provider is established, resolve it from the user's request or repository evidence;
ask only when the choice blocks the requested setup.

Use the applicable guide for configured behavior:

- [GitHub](../templates/issue-tracker-github.md)
- [GitLab](../templates/issue-tracker-gitlab.md)
- [Local Markdown](../templates/issue-tracker-local.md)

For hosted tracking, record the exact project location. Use remotes to resolve a
selected project, not to select tracking itself. Do not silently fall back to
Local Markdown because no remote exists.

The provider guide defines storage and configured representation. The consuming
workflow owns readiness, claiming, transitions, and completion evidence. Tracker
setup does not make tickets mandatory for direct coding.

## Labels and relationships

When label mapping is needed, adapt
[the label seed](../templates/triage-labels.md) to existing equivalent values
before introducing new names. Writing a mapping does not create remote labels.

Provision or mutate remote labels only when authorized, then read back the result.
Otherwise state that the local mapping is configured and remote state remains
unverified or incomplete.

Check that the configured parent/child, dependency, claim, and closure
representation is actually supported by the selected service and available tools.
Do not silently switch representation merely because another API is easier.

For Local Markdown, ensure the durable tracker path can be version controlled.
Correct a conflicting ignore rule only within authorized setup scope. Do not create
example tickets or commits merely to prove the layout.

## Verify configured behavior

Check the selected guide, project identity, label mapping when applicable, and
relationship representation. Distinguish local configuration from verified remote
state and tool capability.

External publication, mutation, and workflow transitions require their own
authorization. Tracker setup is complete when future agents can locate the
configured tracker and know which representation the consuming workflow expects.
