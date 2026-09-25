# Agent instruction files

## Repository instructions

Inspect the root instruction file and any nested instructions that govern the
requested scope. Preserve narrower rules at their own scope. Use the files the
target agent actually reads; do not create parallel instruction files merely to
match a preferred template.

Keep working commands, non-obvious repository constraints, and conditional
pointers in the nearest useful instruction surface. Verify commands against their
scripts or configuration. Keep brief guidance inline and move substantial
conditional procedure to an existing maintained owner.

When a routine local workflow is verified safe but that safety is not obvious,
record the boundary and its existing within-task permission if doing so prevents
needless approval turns. For example, if the owning configuration proves a test
command uses only disposable fixtures and cannot reach production or durable
external state, guidance may say the agent can run, fix, and rerun that workflow
within otherwise-authorized work. Verify the claim from the mechanism that
enforces it; never infer safety from convention, redact a real risk, or broaden
authorization beyond the user's task.

When changing scope, ownership, or reading paths, check that future agents encounter
the applicable guidance before the decision it governs. Preserve compatible
instructions for other tools unless the user requested their reconciliation.

Pack migration and compatibility work belongs to
[Reconcile existing guidance](reconcile-existing.md); ordinary instruction-file
setup does not compare every local rule against current templates.

## Global instructions

Global instructions hold durable cross-repository user preferences and
environment-specific constraints. Keep project commands, repository facts, and
project engineering procedures with their local owners.

Reconcile global guidance only when explicitly authorized. A repository-local
setup or migration does not include installed global files.

When global setup is requested, use
[the global seed](../templates/global-agents.md) only as a starting point and
preserve the user's actual preferences and host-specific constraints. Bootstrap
does not seed delegation or context-inheritance policy; those belong to the
active runtime, user instructions, and workflow that performs delegation.

The managed installer may own a separate bootstrap section in the user's global
instructions. This skill does not overwrite installer-owned or unrelated global
content merely because its seed changed.
