# Tracker delivery

Read this reference only when the fixed delivery set is one complete
tracker-backed parent graph.

## Admit

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either
is missing or incompatible, recommend `$repo-bootstrap` and stop. Refresh the
parent and every child, verify that the fixed set covers the complete graph,
then claim the parent and initial ready frontier. Before each claim, require the
item to be unclaimed or demonstrably retained by this run through its known
actor, lane, and commit state. Stop on any other or ambiguous ownership. Read
the claim back and confirm one current actor before dispatch.

When landing exposes another ready child, refetch it and apply the same claim
and read-back rule before dispatch. Leave blocked descendants unclaimed.

When the next frontier requires user authorization or another external
decision, stop new dispatch. Let healthy workers finish and land unless the
gate invalidates their scope or continued mutation is unsafe. Then close
completed children, remove completed lanes, and return a clean integration
state. Leave the gated child unclaimed until the decision is recorded. Preserve
dirty or incomplete work instead of treating the pause as cleanup authority.

## Finish

For each completed child, preserve its category, remove its readiness roles,
apply `implemented`, close it when configured, and read the result back. Refetch
open dependents after each child; apply `ready-for-agent` only to complete
accepted packets whose blockers are resolved, read each change back, and leave
the others non-ready.

After all children finish, refetch the complete graph. Apply `implemented` to
the parent and close it when configured only when every child is implemented
and the main skill's integrated-proof gate is satisfied for that exact `HEAD`,
then read the parent back.

On a failed, partial, or indeterminate tracker effect, stop further mutation,
refetch the graph, preserve implementation state, and report the observed state
and safest configured recovery.
