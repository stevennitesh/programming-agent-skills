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

For requested parallel setup or a concrete execution gap, use
[Parallel support](parallel-support.md). This remains conditional; ordinary
repository setup does not create lanes or enable broader permissions.

Map existing equivalent labels before using the seed's default names. Writing
the mapping does not create remote labels. Provision missing labels only when
the user's authorization covers that operation, then read them back. Otherwise
state that the local mapping is configured and remote provisioning is unverified
or still needed.

Default domain routing to a single root `CONTEXT.md` and `docs/adr/`. Preserve
an existing multi-context route. Create a new multi-context layout only when
distinct domain meanings justify it; multiple packages alone are not enough.
Configure the route without inventing domain records or empty ADRs. Missing
records can remain absent until authorized work supplies their content.

For Local Markdown, ensure the selected durable tracker path can be version
controlled. Correct a conflicting ignore rule only within authorized setup
scope. Do not create example tickets or commit tracker files during setup.

## Existing repositories

Initial setup defaults do not authorize wholesale replacement of existing
guidance. Compare the current bootstrap with repository instructions, the
engineering contract, domain route, tracker guide, and labels. Follow their
current pointers to other agent docs and setup enforcement that may depend on
the old conventions. Include repository-local global-instruction templates only
when affected; an installed global file remains outside repository setup scope.

Distinguish deliberate repository policy from inherited pack boilerplate. Use
local decisions, comments, history, and actual consumers when that distinction
matters. A rule is not a deliberate local choice merely because an earlier
bootstrap copied it into a repository-owned file. Preserve repository facts,
domain meaning, and intentional overrides; reconcile inherited pack guidance
with the current skill and seeds. Ask about a consequential unresolved conflict
instead of silently retaining the old default or erasing a local decision.

Compare the engineering contract section by section for meaning and coverage:
understanding behavior, design, completing changes, proof, and effects. During
an approved update, incorporate missing applicable guidance, replace superseded
pack instructions, and consolidate duplication. Rewrite old wording when it
still directs an agent toward an obsolete practice, even if every link resolves.
Equivalent local wording can remain; do not reformat solely to match a seed.

Trace active root and nested agent instructions, referenced guides, and their
enforcement for remnants of the displaced pack. Typical remnants include
mandatory implementation or ticket pipelines, retired skill routes, unconditional
TDD or delegation defaults, obsolete setup markers, and stale installer commands.
Resolve each against its current owner and any deliberate local override. When
a workflow has no replacement skill, describe direct work or remove the obsolete
route rather than inventing a new mandatory step. Remove superseded prose in
place; appending the new contract beneath conflicting instructions is incomplete.
Historical research and records remain evidence and are not migration targets.

Prepare one reviewable proposal with the exact edits across affected files,
the benefit or incompatibility each addresses, preserved local choices, and the
checks needed to verify the result. If a validator or test enforces a displaced
convention, include its narrow migration in the same proposal while preserving
the underlying protection under the current Astra contract. Do not bypass a
failing check or claim compatibility from prose alone.

Offer the user a single choice to apply this compatibility update or keep the
existing setup. Applying it covers the approved document and enforcement changes
together. A decline preserves the current conventions; continue any separate
requested repair within its original scope. Do not repeat a declined offer for
the same differences in the same task. Prior explicit approval of the update
remains sufficient. A repeat run with no relevant changes should produce no edits.

Projects using this pack target the latest Astra version. Inspect retired routes
to recover their still-valid meaning, then migrate the affected guidance,
configuration and enforcement together. Do not preserve old skill routes as an
alternative. When an Astra workflow changes a convention, update its consuming
guidance and these defaults together. An unavailable current skill is an access
or installation gap, not permission to restore a retired route.

Use a legacy validator only to assess that legacy contract. Its requirements
for markers, fixed documents, or old workflows are not Astra setup requirements.
