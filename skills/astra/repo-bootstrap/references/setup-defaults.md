# Setup defaults

Preserve established repository choices. Where a setting is absent, apply the
defaults below within the requested setup scope. Ask only when evidence conflicts
or no default resolves a consequential choice. Continue independent setup while
that choice is unresolved.

## Initial setup

For a new Codex repository, create `AGENTS.md` with commands grounded in source,
local constraints, and these conditional pointers:

- Before nontrivial coding, read the engineering contract.
- When domain meaning or an accepted design decision matters, follow the domain
  route.
- For tracker-backed work, read the tracker guide and label mapping.

Use the repository's existing instruction file and document locations when
established. Otherwise write these files under `docs/agents/`:

| Output | Seed |
| --- | --- |
| `engineering-contract.md` | [Engineering contract](../templates/engineering-contract.md) |
| `domain.md` | [Domain routing](../templates/domain.md) |
| `issue-tracker.md` | One provider template selected below |
| `triage-labels.md` | [Label mapping](../templates/triage-labels.md) |

Adapt the seeds to the repository and update relative links if their locations
change. These are repository-owned documents, not managed mirrors. Record an
unresolved tracker selection as a setup gap rather than inventing its configuration.

## Select the tracker

Use the established tracker even if it differs from the Git hosting provider.
Otherwise resolve the intended project from the configured remote and choose
[GitHub](../templates/issue-tracker-github.md) or
[GitLab](../templates/issue-tracker-gitlab.md). Record the resolved project URL
in the resulting guide. Multiple remotes or an unfamiliar host may need further
inspection before that choice is clear.

With no established tracker or identifiable provider, ask which tracker to use.
Use [Local Markdown](../templates/issue-tracker-local.md) when selected; do not
silently treat the absence of a remote as that selection.

Keep the provider defaults unless the repository or user chooses otherwise:

| Provider | Request surface | Relationships | Close implemented items |
| --- | --- | --- | --- |
| GitHub | Issues | Native sub-issues and dependencies | Yes |
| GitLab | Issues | Body links | No |
| Local Markdown | Files under `.scratch/<feature-slug>/` | File links and `Blocked by:` | Record the implemented state and clear the claim |

Check that the selected representation is supported by the actual service and
available tools before claiming it is ready. If not, report the gap or resolve
an alternative; do not silently switch representations. Keep changing API syntax
in current tool documentation rather than copying command recipes into the guide.

The guides define storage and configured behavior. A consuming workflow owns
readiness criteria, claiming, transitions, and completion evidence. These settings
do not authorize external mutations or create a mandatory ticket pipeline.

## Labels and domain routing

Map existing equivalent labels before using the seed's default names. Writing
the mapping does not create remote labels. Provision missing labels only when
the user's authorization covers that operation, then read them back. Otherwise
state that the local mapping is configured and remote provisioning is unverified
or still needed. Include Wayfinder labels only when that workflow is adopted;
use its current contract to determine them.

Default domain routing to a single root `CONTEXT.md` and `docs/adr/`. Preserve
an existing multi-context route. Create a new multi-context layout only when
distinct domain meanings justify it; multiple packages alone are not enough.
Configure the route without inventing domain records or empty ADRs. Missing
records can remain absent until authorized work supplies their content.

For Local Markdown, ensure the selected durable tracker path can be version
controlled. Correct a conflicting ignore rule only within authorized setup
scope. Do not create example tickets or commit tracker files during setup.

## Existing repositories and mixed skill use

Initial setup defaults do not authorize wholesale replacement of existing
guidance. Reconcile missing or requested settings, preserve local additions,
and avoid duplicate sections. A repeat run with no relevant changes should
produce no edits.

If an older skill remains active, inspect the configuration it reads and preserve
its required fields and meanings. When a new Astra workflow changes a convention,
update its consuming guidance and these defaults together. Do not remove old
fields until the remaining consumers can work without them.

Use a legacy validator only to assess that legacy contract. Its requirements
for markers, fixed documents, or old workflows are not Astra setup requirements.
