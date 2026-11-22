# Worker assignment

Use the relevant branch when an assignment involves migration, support, or
changing write custody. Follow [Native spawning](native-spawning.md) for host
controls and the context needed by a fresh worker.

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

If support is useful, name who can dispatch it. The lead can authorize the
worker to use the slot at assignment time with a defined scope and budget.
Within that authority the worker chooses when to use it. Otherwise route a
support request to the lead. Reuse a suitable existing agent or finish the
active support assignment before starting another. Supporting agents have no
delegation authority. In combined parallel work, follow the checkout
coordinator's scheduling within the agreed staffing and budget limits.

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

For a decision or blocker that needs the lead, send the evidence, the decision
needed, and a recommendation. Continue independent work within scope. For
corrections, reuse suitable worker context and send the changed requirements or
findings, candidate identity, and renewed custody.
