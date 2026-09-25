# Skill authoring

Use this reference when creating a skill or changing its discovery, invocation,
package structure, or host-specific behavior.

## Make discovery precise

Write the description for selection, not explanation. Name the task or observable
request that should activate the skill and add exclusions only for realistic
neighboring intents that could select it incorrectly. Keep the procedure in the
body.

Treat discovery metadata as scarce shared context: available skill names and
descriptions compete with the user's task and each other, and hosts may shorten
overlong metadata. Keep a description to the minimum reliable selector plus the
nearest useful exclusion; do not put procedure, rationale, examples, or a catalog
of distant non-matches there.

Prefer a narrow reliable trigger over a broad description that loads the method
for work the base agent can handle directly. When changing discovery, consider
both representative positive requests and realistic near-misses.

Keep the folder name, frontmatter name, and invocation metadata consistent.
Preserve the intended invocation policy. For a new skill, use the target host's
current default unless another policy is required.

Discovery and context loading are host behavior. Do not assume that explicit-only
invocation hides all metadata, that every host interprets the same metadata, or
that a listed skill was actually loaded. Check current host documentation when
that behavior matters.

## Keep the package proportional

Put the shared method, key boundaries, and completion condition in `SKILL.md`.
Keep information every applicable invocation needs there.

Move substantial detail into a reference when it supports a recognizable branch.
Place the pointer at the decision that triggers that branch and state when the
reader should follow it. Do not move required guidance behind an ambiguous pointer
merely to shorten the root file. When one root skill serves several recognizable
branches, keep the shared method and branch triggers in `SKILL.md` and use
progressive disclosure for branch-specific mechanics.

Add scripts, templates, or deterministic helpers when they remove repeated work,
enforce a mechanical contract, or make a fragile procedure safer. Do not add
machinery merely to make the skill package look complete.

Keep model- and host-specific mechanics out of the universal method when they can
change independently. Design the primary Astra method for Astra: do not retain
compensating scaffolding there solely because an earlier or different receiver
needed it. On a model upgrade, evaluate whether existing instructions can be
simplified or retired before adding new model-specific procedure. If another
receiver still needs extra scaffolding, isolate it behind an explicit
model-/host-specific route or separately evaluated package rather than taxing the
primary Astra path.

Use current host documentation or the bundled skill-creation guidance for schemas,
metadata, installation, and packaging details.

Edit the source package rather than an installed copy unless the installation
mechanism explicitly owns direct edits. Preserve unrelated metadata and
installation state.

## Check the package and its claim

Use the available package validator for frontmatter, naming, and supported
structure. Resolve local links from their containing files. Confirm that referenced
tools, files, scripts, and templates exist in the intended environment.

For a discovery change, inspect representative positive and near-negative
requests. For a material method change, model migration, keep-or-retire decision,
or claim that the skill improves behavior, read
[Behavior evaluation](behavior-evaluation.md).

Report packaging and link checks separately from behavioral evidence. A valid
package establishes that the skill can be consumed; it does not establish that
the skill is useful or that the host selected it correctly.
