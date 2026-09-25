---
name: repo-bootstrap
description: Set up, migrate, or repair repository agent guidance. Exclude wording-only edits to an already-scoped instruction artifact, ordinary coding, and environment installation.
---

# Repo bootstrap

Give future agents the repository-specific facts, constraints, and pointers they
need to work correctly. Create or reconcile only the guidance the requested
repository actually needs. For an inspection request, return findings without
editing.

Repo bootstrap owns which repository-level guidance surfaces, routes, and facts
should exist and remain current. When that surface is already established and the
task is only to write or audit one scoped instruction artifact, use
[writing-for-agents](../writing-for-agents/SKILL.md) instead.

## 1. Establish the current instruction surface

Resolve the target root and inspect its working state. Read the agent instruction
files that govern the requested scope and the current owners of any guidance they
reference. Verify build, test, lint, and other important commands against the
scripts or configuration that define them.

Identify operating facts only when they can change future engineering decisions,
such as a non-obvious deployment model, persistence boundary, supported runtime,
or material scale constraint. A verified safety boundary for a routine local
workflow can also earn a place when future agents would otherwise stop for
unnecessary approval—for example, a test command that is mechanically confined to
disposable local fixtures. Verify that boundary from its owning configuration or
mechanism and record only the permission already implied by the authorized task;
never infer safety or broaden authority to reduce questions. Preserve an existing
owner rather than copying the fact into another document.

Distinguish verified commands and facts from unexecuted source discoveries and
missing prerequisites. A missing preferred document is not itself a setup gap or
a reason to block ordinary coding. Identify the information future work actually
needs.

## 2. Choose the smallest useful guidance

Keep repository instructions focused on working commands, non-obvious local
constraints, and conditional pointers to maintained guidance. Use the instruction
files the target agent actually reads and preserve narrower rules at their proper
scope. Read [Agent instruction files](references/agent-instructions.md) when
creating or changing those surfaces.

For initial setup, read [Setup defaults](references/setup-defaults.md). Seeds are
starting material, not managed mirrors; adapt only the guidance that applies to
the repository.

For an explicit compatibility update, pack migration, or repair of known stale
skill-pack routes, read
[Reconcile existing guidance](references/reconcile-existing.md). Do not compare
every local document with every current template merely because their wording or
coverage differs.

For requested tracker configuration or an established tracker whose agent guidance
needs setup, read [Tracker setup](references/tracker-setup.md). Ordinary repository
setup does not create a ticketing requirement.

When parallel execution setup is requested or an execution workflow reports a
concrete repository prerequisite gap, read
[Parallel support](references/parallel-support.md). Bootstrap configures
prerequisites; it does not create lanes or start workers.

If global guidance is explicitly in scope, keep only durable cross-repository
preferences, environment-specific constraints, and a direction to follow each
repository's instructions. Keep project commands, repository facts, and project
engineering guidance local. Otherwise do not edit global instructions.

## 3. Apply the requested changes

For an authorized setup, migration, or repair, edit the current owners directly.
Preserve verified repository facts, deliberate local policy, and unrelated work.
Ask only when a consequential repository policy or operating commitment remains
unresolved; continue independent authorized changes while that choice is pending.

Prefer updating existing instructions and pointers over appending parallel
guidance. Keep mechanical enforcement in its owning configuration or tooling.
A guidance task does not by itself authorize dependency installation, new
tooling, tracker mutations, global-file edits, commits, or publication.

When substantial shared engineering guidance is useful, adapt
[the engineering contract seed](templates/engineering-contract.md) to the
repository rather than copying it wholesale. The resulting guidance is
repository-owned and does not need to track future template wording.

## 4. Verify the receiving path

Read the result as a future agent entering the repository. Check that applicable
instructions are discoverable at the right scope, commands match their current
owners, conditional pointers lead to existing guidance, and the repository's
meaning and deliberate policy remain intact.

Inspect the changed guidance for duplicate or conflicting obligations, stale
pointers introduced by the edit, and requirements that do not apply to supported
workflows. Execute a documented command only when necessary to substantiate a
claim about that command; otherwise distinguish source verification from runtime
verification.

For a pack migration or compatibility repair, use the reconciliation reference's
additional checks for displaced routes and affected consumers. Updating installed
copies, external repositories, or user-global state remains separately scoped.

Finish when the requested repository guidance is coherent, discoverable, grounded
in its real sources, and sufficient for the future decisions in scope. Report the
changes and any material unresolved gap.
