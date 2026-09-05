# Tracker publication and repair

Read only when publishing or reconciling durable tickets is requested. Follow the
repository's tracker and label guidance if present. Use the available connector,
CLI, or repository helper; do not embed provider-specific label names or API
mechanics in the delivery method. A configured local-file tracker follows its
own format; an ordinary draft is not automatically a published tracker graph.

## Prepare concrete effects

Resolve the target project, parent if any, existing items, relationships, status,
and active ownership. Read decision-changing comments. Inspect before creating
so equivalent existing work can be reused. Similar titles alone do not establish
equivalence; compare scope, acceptance, dependencies, and current state.

For repair, bound which bodies, edges, and readiness states may change. Preserve
unrelated content and active claims. Do not rewrite or release work another agent
is executing; return that conflict unless coordinated change is authorized.
Duplicate, ambiguous, or divergent items require reconciliation within authority,
not silently creating a second graph.

When shaping revises an accepted source, identify the accepted revision and changed
commitments. Coordinate affected active work with its execution owner before
repairing tickets; keep affected pending work non-ready until acceptance, source
pointers, gates and assignments agree. Preserve unaffected tickets and claims.

Prepare the exact titles, bodies, parent/child and blocking relationships, and
intended state changes. Verify the needed mutation and independent read-back
operations before the first effect. Missing setup leaves a reviewable draft and
the specific publication gap; suggest setup repair only when needed.

Use the user's existing publication authority and applicable repository rules.
When approval is required, ask about the concrete prepared effects. Reconfirm
only a material change outside the accepted scope, not every routine technical
adjustment or an unchanged graph already authorized for publication.

## Apply and verify

Refetch affected state immediately before mutation. Reconcile relevant drift
before proceeding; do not overwrite an intervening edit. Reuse unchanged matching
items and create verified missing items in dependency order. Record each returned
identity and read it back before using it in later relationships.

Where the tracker has a readiness state, keep new or materially revised work
non-ready until its content and required relationships are verified. Respect
active claims. Attach parent and dependency links through the configured
representation; do not substitute prose for required native relationships.
If text is the configured representation, keep it consistent and verify it.

Mark only work whose decisions, permissions, and blockers are actually resolved
as actionable under the configured policy. A closed predecessor alone does not
prove its required outcome exists. Preserve category and state distinctions;
known dependency-blocked work is not necessarily awaiting triage or information.

Use mapped agent-readiness only for executable agent work; preserve human-only
readiness for human handoffs. Neither a resolved blocker nor a ready-for-human
label authorizes an agent to take over the human decision or action.

After publication, read back bodies, relationships, readiness, and affected
ownership. Derive the actual starting set from the verified graph rather than
assuming the planned writes succeeded. Keep the source-to-published identity
mapping so a resumed run can inspect the same items.

For version-controlled local tickets, identify the canonical checkout containing
the published graph. Publication does not imply a Git commit. Before subsequent
parallel delivery, the execution owner needs authority to commit owned tracker
changes and a clean baseline containing the accepted graph. Do not let lane copies
become independent tracker authorities.

## Recover without duplicates

On a failed, partial, or indeterminate effect, stop further mutations and inspect
the affected graph. Report confirmed changes, unchanged items, unknown outcomes,
and the next safe recovery step. Never retry an uncertain create blindly or
pretend the remaining graph was published. Resume from observed identities after
reconciliation; do not replay the entire creation sequence. Do not close or
reclassify a parent or change unrelated assignments without authorization.
