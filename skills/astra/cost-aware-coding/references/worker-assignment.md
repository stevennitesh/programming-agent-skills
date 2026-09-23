# Worker assignment

Prepare the smallest self-contained assignment that lets the selected worker act
without importing the lead's conversation. The packet should transfer necessary
context once, not make Astra follow implementation continuously.

## Assignment contract

Include only decision-bearing fields that apply:

- **Outcome:** the behavior or result the assignment must deliver.
- **Accepted source:** the request, plan, specification, or repository guidance
  that governs the work.
- **Scope:** responsibilities, exclusions, and authorized effects.
- **Checkout:** repository path, base or candidate identity, relevant existing
  work, and write-custody boundary.
- **Acceptance:** observable behavior and required checks.
- **Reserved decisions:** consequential choices Astra or another owner must settle.
- **Return:** candidate identity, material changed scope, decisive checks, material
  limits or pending proof, consequential deviations, and custody state.

Point to accessible detailed sources instead of copying conversations. Do not
front-load repository facts the worker can cheaply discover itself.

For Luna Max, keep the packet especially compact and fully bounded. If the task needs a
large repository brief, open-ended exploration, or substantial implementation
judgment, route it to Sol rather than spending Astra tokens manufacturing a
pseudo-bounded assignment.

Suggested mechanisms remain suggestions unless an accepted source makes them
binding. The worker resolves routine technical choices within scope and raises a
conflict only when satisfying the assignment would change accepted behavior,
scope, risk, or another reserved commitment.

## Custody and communication

The worker owns writes to the assigned checkout until it explicitly releases
custody. It preserves unrelated work and must not assume other actors are absent.

A blocking question identifies the unresolved decision, why it matters, and
current custody state. A nonblocking question does not stop independent work.

If Astra requests checkout access, the worker stops its writers and relevant
subprocesses, reports their state, and releases custody before Astra accesses that
mutable checkout.

A candidate return is reviewable only when it identifies the candidate and material
proof, reports unresolved limitations, and releases custody with worker-owned
writers stopped.

Return decision-relevant evidence, not a narrated implementation journey. Do not
send every file inspected, rejected idea, debugging step, or routine test iteration
unless it changes review or recovery.

For follow-ups, preserve the established outcome and send only changed context,
findings, acceptance, candidate identity, and renewed custody grant. Reuse the same
worker while its accumulated context remains useful and safe.
