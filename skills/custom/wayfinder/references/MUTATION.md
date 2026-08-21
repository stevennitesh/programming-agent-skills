# Tracker mutation

Load this reference only before Wayfinder writes durable tracker state.

The approved Chart packet authorizes its exact creation. For an existing map,
mutate only when the invocation asks to advance, reconcile a supplied return, or
finish that exact map. A status inquiry is read-only. A changed destination,
wider scope, or material expansion needs destination-owner approval.

Use the configured tracker operation and read-back routes. A claim route must
serialize ownership or expose an observable losing race. Otherwise use one
confirmed writer and stop when another session may mutate the same item. Give
every invocation a fresh unpredictable claim token so sessions using the same
tracker account remain distinguishable. Another token owns the item even when
the assignee matches. Time alone never expires a claim. Replace one only with
explicit destination-owner or provider-administrator approval after recording
the prior claim and reason. Before every write or release, reread the assignee
and token and proceed only while this invocation still owns both.

For Chart, establish one creation writer, search the exact destination, create
only the map, and search again. Continue only when that map is the sole match:
claim and read it back before creating children and edges. If a race leaves
several empty map shells, stop. The destination owner may designate one
canonical shell and approve renaming the others out of the destination
identity. Read back one exact match, then claim that shell and resume the
already-approved children and edges.

For Advance, claim and read back the ticket before resolver work. Claim the map
only for reconciliation. After the map claim, reread the question, owner,
resolver route, dependencies, eligibility, destination, and scope. Ignore
unrelated comments or metadata. Material drift records no outcome.

For Finish, claim and read back the map, then reread every question, fog item,
decision, closing condition, destination, and scope before posting either
terminal record. Drift stops the close.

Apply one bounded change. Refetch the changed items, affected dependencies, and
resulting frontier. Release every claim and refetch to prove the assignee and
claim token are absent. A failed or indeterminate operation must be inspected
before retry. Report applied, failed, and unknown effects with the safest
recovery. Never report completion from unverified state.
