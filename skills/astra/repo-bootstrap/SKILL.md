---
name: repo-bootstrap
description: Inspect, create, or reconcile a repository's agent guidance when the user requests setup or a specific guidance repair. Covers repository instructions and engineering conventions; exclude ordinary coding, environment installation, and automatic setup merely because a preferred document is missing.
---

# Repo bootstrap

Give future agents the repository facts and engineering guidance they need to
work well. Reconcile existing guidance in place. For an inspection request,
report findings without editing.

## 1. Read the repository

Resolve the target root and inspect its working state. Read applicable agent
instructions, the current engineering guidance, and the scripts or configuration
that own build and verification commands. Follow existing pointers to domain
decisions only far enough to identify their owners and relevant constraints.

Distinguish verified commands, commands found in source but not executed, and
missing prerequisites. An absent preferred document is not evidence that coding
must stop. Identify the actual missing information before proposing setup.

## 2. Choose the smallest useful guidance

Keep repository instructions short: working commands, non-obvious local
constraints, and pointers with clear reading conditions. Use the instruction
file the target agent actually reads; preserve other tools' compatible guidance.
When creating or reconciling instruction files, read
[Agent instruction files](references/agent-instructions.md) for local and global
ownership, nested scopes, and pointer checks.

When shared engineering guidance is missing or needs revision, use
[the engineering contract](templates/engineering-contract.md) as a seed.
Reconcile it with repository-owned choices rather than replacing them with the
template. Prefer an existing authoritative location; otherwise use
`docs/agents/engineering-contract.md` and add a pointer for nontrivial coding
to the repository's instruction file. The resulting contract is repository-owned,
not a mirror that future bootstrap runs overwrite.

For initial repository setup or work on tracker, label, or domain configuration,
read [Setup defaults](references/setup-defaults.md). Preserve established choices
and fill absent settings from those defaults. A focused repair changes only its
requested scope. Configuring a tracker does not require direct coding tasks to
become tickets.

When parallel execution setup is requested or execution reports a concrete
environment gap, read [Parallel support](references/parallel-support.md).
Reconcile the prerequisites without creating lanes or starting workers.

Link existing domain rules and operating procedures at their current Astra owners.
Projects using this pack target the latest Astra contracts. Migrate retired routes
and obsolete setup fields rather than retaining compatibility branches. Preserve
repository-specific meaning and historical evidence, not obsolete execution paths.

If global guidance is explicitly in scope, keep only cross-repository preferences
and a direction to follow each repository's instructions there. Preserve personal
environment rules. Keep project commands and the engineering contract local.
Otherwise report any relevant global conflict without editing the global file.

## 3. Offer a compatibility update

For an existing setup, compare its agent docs with this version of bootstrap.
When a material difference warrants reconciliation, follow
[Existing repositories](references/setup-defaults.md#existing-repositories)
to prepare one proposal covering all affected docs and compatibility checks.
Show the concrete edits, preserved choices, and any validation changes before
asking whether to apply the compatibility update or keep the current conventions.
Explain that the choice is needed because this updates established setup policy.

Wait for the user's choice before applying that optional update. A decline keeps
the existing conventions and does not block independently authorized work. If
the user already requested the compatibility update, proceed within that scope
without asking again. With no material difference, report that the setup is
current; do not ask merely because wording or a template version differs.

## 4. Apply the requested changes

For an authorized setup or repair, make the supported local edits directly.
Ask only when an unresolved choice would change a consequential repository
policy or operating commitment. Continue independent edits while that choice
is unresolved. Preserve existing authorization rather than adding another
approval step for an already requested change.

Check affected content again before writing and preserve unrelated edits.
Update existing sections and pointers instead of appending duplicates. Keep
mechanical enforcement in its owning configuration or tooling; a documentation
request alone does not authorize new tooling, dependency installation, external
tracker changes, or global file edits.

## 5. Verify the guidance

Read the resulting files as a future agent. Check that pointers resolve, commands
match their source, and local requirements remain intact. Run relevant existing
documentation checks. Execute a documented command when practical and necessary
to substantiate a setup claim; report unexecuted commands as such. Inspect the
diff for duplicate rules and unintended changes to policy or unrelated work.
Verify current Astra owner pointers and identify any installed/source mismatch;
do not claim migration complete while the affected route still selects a retired
skill. Updating installed copies or other repositories remains separately scoped.
For an accepted compatibility update, verify the whole approved set together;
do not leave dependent docs or validation rules for separate follow-up turns.

Finish when the requested guidance is coherent, discoverable, and supported by
the repository, or report the specific unresolved gap. State what changed and
what was verified. If setup is part of a larger authorized task, resume that task.
