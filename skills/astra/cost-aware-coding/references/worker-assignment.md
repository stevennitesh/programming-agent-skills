# Worker assignment

Use this reference to prepare a bounded assignment for one serial implementation
worker. The worker must receive the facts and authority it needs explicitly; do
not assume it inherits the lead's conversation.

## Assignment contract

Include only decision-bearing fields that apply:

- **Outcome:** the behavior or result this assignment must deliver and why it
  matters.
- **Accepted source:** the request, plan, specification, or repository guidance
  that governs the work.
- **Scope:** responsibilities, exclusions, and authorized effects.
- **Checkout:** repository path, base or candidate identity, relevant existing
  work, and the worker's write-custody boundary.
- **Acceptance:** observable behavior and required checks.
- **Reserved decisions:** consequential choices the lead or another owner must
  settle rather than the worker inventing.
- **Return:** candidate identity, changed scope, decisive checks, material limits
  or pending proof, consequential deviations, and custody state.

Point to accessible detailed sources rather than copying conversations. For a
small task, the user's request plus relevant repository guidance can be sufficient;
a plan document is not required.

Suggested implementation mechanisms remain suggestions unless the accepted source
makes them binding. The worker resolves routine technical choices within scope and
raises a conflict when satisfying the assignment would change accepted behavior,
scope, risk, or another reserved commitment.

## Custody and communication

Tell the worker that it owns writes to the assigned checkout until it explicitly
releases custody. It must preserve unrelated work and must not assume other actors
are absent.

A blocking question should identify the assignment, the unresolved decision, its
consequence, and current custody state. A nonblocking question should not stop
independent work.

If the lead requests checkout access, the worker stops its writers and relevant
subprocesses, reports their state, and explicitly releases custody before the lead
accesses that mutable checkout.

A candidate return is reviewable only when it identifies the candidate and
material proof, reports unresolved limitations, and releases custody with
worker-owned writers stopped.

For a follow-up, preserve the established outcome and send only changed context,
findings, acceptance, candidate identity, and the renewed custody grant. Reuse the
same worker while its accumulated context is useful and safe.
