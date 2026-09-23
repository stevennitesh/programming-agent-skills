# Tracker publication and repair

Read only when durable tracker publication or repair is requested. Follow the
repository's configured tracker, relationship, readiness, and label conventions.
An ordinary draft is not a published tracker graph.

## Prepare the concrete effects

Resolve the target project, parent when applicable, existing items, relationships,
status, readiness, and active ownership. Inspect before creating so equivalent
work can be reused; title similarity alone does not establish equivalence.

For repair, bound which ticket bodies, relationships, and readiness states may
change. Preserve unrelated content and active claims. Do not rewrite or release
work another actor is executing without coordinated authority.

If accepted meaning or acceptance changes while tickets, assignments, or proof
depend on the current revision, use
[Active delivery revisions](../../shape-work/references/active-delivery-revisions.md)
first. Then reconcile only the tracker content, relationships, readiness, and
claims affected by that settled revision.

Prepare the exact ticket bodies, parent/child and blocking relationships, and
intended state changes before mutation. Missing or incompatible tracker setup
leaves a reviewable draft plus the concrete publication gap.

Use only existing publication authority. When another approval is required, ask
about the prepared effects that need it; do not repeatedly reconfirm unchanged
authorized mutations.

## Apply and verify

Refresh affected tracker state before writing when intervening activity can occur,
or use supported conditional writes against the inspected version. Reconcile
relevant drift instead of overwriting it.

Reuse matching items and create only missing work. Record each returned identity
and read it back before depending on it for later relationships. Where readiness
exists, keep new or materially revised work non-ready until its body and required
relationships are verified.

Use the configured native relationship representation when one exists; do not
replace required parent/dependency links with prose. Mark only work whose
decisions, permissions, and blockers are actually resolved as actionable.
Human-only readiness does not authorize an agent to take over a human decision or
action.

After publication, independently verify affected bodies, relationships, readiness,
and ownership. Derive the actual starting set from that verified graph rather
than assuming planned writes succeeded. Preserve the source-to-published identity
mapping needed for later repair or delivery.

For version-controlled local tickets, identify the canonical checkout containing
the published graph. Publication does not imply a Git commit, and worker lane
copies do not become independent tracker authorities.

## Recover without duplicates

If a create, update, relationship change, or readiness mutation has a partial,
failed, or indeterminate result, stop dependent mutations and inspect the affected
graph. Resume from observed identities after reconciliation.

Do not blindly retry an uncertain create, replay the entire publication sequence,
release an ambiguous claim, close a parent, or alter unrelated ownership merely to
make the tracker match the intended plan.

Finish publication when the requested graph is verified in its configured
representation and any remaining publication or ownership uncertainty is explicit.
