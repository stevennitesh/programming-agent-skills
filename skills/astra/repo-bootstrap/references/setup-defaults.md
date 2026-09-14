# Setup defaults

Preserve established repository choices unless the user selects their replacement.
Apply defaults only for applicable concerns within the requested setup scope;
an absent optional setting is not a setup gap. Ask only when evidence conflicts
or no default resolves a consequential choice. Continue independent setup while
that choice is unresolved.

## Initial setup

For a new Codex repository, start with one compact `AGENTS.md`: commands grounded
in source, non-obvious local constraints, and applicable engineering guidance.
Preserve useful existing instruction files and document owners. Split guidance
only when its content or distinct reading conditions warrant a separate guide;
do not create files or pointers merely to complete a template set.

Use these seeds only for applicable content, adapting rather than copying them
wholesale: [Engineering contract](../templates/engineering-contract.md),
[Domain routing](../templates/domain.md), and
[Label mapping](../templates/triage-labels.md). When separate guides are useful and
no location is established, use `docs/agents/`. Repair relative links when adapting
locations. These are repository-owned documents, not managed mirrors.

## Select the tracker

Configure tracking only when requested or established by repository practice.
A Git remote alone does not establish that issues are used. Otherwise omit
tracker and label setup without treating their absence as a gap.

For applicable tracker setup, preserve the established provider even when it
differs from Git hosting. Use [GitHub](../templates/issue-tracker-github.md),
[GitLab](../templates/issue-tracker-gitlab.md), or
[Local Markdown](../templates/issue-tracker-local.md) for the selected provider.
Use remotes to resolve a selected hosted project, not to select tracking itself.
Ask only when an unresolved provider or project prevents requested tracker setup;
do not silently choose Local Markdown because no remote exists. Record the
resolved project URL for hosted tracking.

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

For applicable tracker setup, map existing equivalent labels before using the
seed's default names. Writing the mapping does not create remote labels. Provision missing labels only when
the user's authorization covers that operation, then read them back. Otherwise
state that the local mapping is configured and remote provisioning is unverified
or still needed.

Preserve existing domain owners. Keep brief local meaning inline; introduce a
domain guide or route only when actual content needs it. A root `CONTEXT.md` and
`docs/adr/` are available conventions, not required outputs. Use multiple contexts
only when distinct domain meanings justify them; multiple packages alone are not
enough. Do not create empty records or routes to nonexistent content.

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
domain meaning, and intentional overrides unless their replacement is selected;
reconcile inherited pack guidance
with the current skill and seeds. Ask about a consequential unresolved conflict
instead of silently retaining the old default or erasing a local decision.
Classify differences as outdated inherited guidance, verified repository facts,
intentional policy/customization, or unresolved provenance. Compare each applicable
current seed: engineering contract, domain route, selected tracker guide, and label
mapping, plus the agent-instruction structure. Judge meaning and behavior rather
than exact wording. A difference alone does not establish a defect.

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

Where intentional local policy differs, present concrete alternatives in one
proposal: reconcile current defaults with useful repository choices, or adopt the
identified template defaults and explain which local policies that replaces.
Both options retain verified commands, paths, provider configuration, and real
operating constraints; template adoption is not placeholder copying. Keep the
existing setup available when the update is optional. Applying the selected option
covers the approved document and enforcement changes
together. A decline preserves the current conventions; continue any separate
requested repair within its original scope. Do not repeat a declined offer for
the same differences in the same task. Prior explicit approval of the update
remains sufficient for settled changes; ask only about consequential policy choices
it does not resolve, while continuing independent reconciliation. A repeat run
with no relevant changes should produce no edits.

Projects using this pack target the latest Astra version. Inspect retired routes
to recover their still-valid meaning, then migrate the affected guidance,
configuration and enforcement together. Do not preserve old skill routes as an
alternative. When an Astra workflow changes a convention, update its consuming
guidance and these defaults together. An unavailable current skill is an access
or installation gap, not permission to restore a retired route.

Use a legacy validator only to assess that legacy contract. Its requirements
for markers, fixed documents, or old workflows are not Astra setup requirements.
