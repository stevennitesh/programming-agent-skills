# Worker assignment

Use before transferring implementation custody. Supply the accepted scope,
acceptance, sources, effects, and return context under
[Native spawning](native-spawning.md). The worker chooses techniques, tools, local
design, and sequencing within those boundaries; routine reversible choices need
no lead approval.

## Preserve the transition obligations

When replacing or consolidating behavior, include affected callers, migration,
retirement, compatibility, and required proof in the assignment. Completion moves
supported callers to the intended owner and removes displaced code, configuration,
tests, and guidance within scope. Explain any retained path and its removal
condition; lack of direct references alone does not prove disuse.

Retire a test when its asserted obligation is obsolete, preserving meaningful
coverage of supported behavior. Passing only the new path does not prove that
existing consumers survived the transition. Cleanup belongs to delivery, without
a separate phase or unrelated repository sweep.

## Use one support slot

The lead dispatches the shared support slot or explicitly grants the primary
worker access within its scope and budget. Identify the dispatcher and existing
agent handle to prevent duplicate helpers. Otherwise the worker requests support
from the lead. Supporting agents do not spawn descendants; finish or reuse the
current assignment before another occupies the slot. Explicit parallel execution
uses its coordinator's dispatch and team rules instead.

A support assignment identifies the question or settled production rule, source
material, observable result, and completion boundary. Return concise findings
with source locations and gaps; bulk production still delivers the full requested
artifacts. Architecture advisers return recommendations for the lead to decide.
A helper that helped author the candidate cannot become its independent reviewer;
review follows [change-review](../../change-review/SKILL.md).

## Transfer custody and return

One actor owns implementation writes. Support uses fixed or independent inputs
and is read-only by default. Support writes require an explicit custody transfer,
not a second implementation writer. Before the lead accesses the mutable checkout,
the worker stops its writers and subprocesses and explicitly releases custody.
Status alone does not establish release.

Return candidate identity, material changes, decisive checks, unresolved obligations,
limits, and custody state. Ask for a lead decision when accepted meaning,
architecture, scope, or a significant unforeseen constraint requires it; state
the evidence and recommendation, continuing independent work when possible.
Send questions, chosen checkpoints, failures, and completion rather than timed
narration. For follow-ups, retain useful worker context and send only changed
requirements, findings, candidate identity, and renewed custody.
