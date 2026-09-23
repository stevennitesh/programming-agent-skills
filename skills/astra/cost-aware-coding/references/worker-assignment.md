# Worker assignment

Prepare the smallest self-contained assignment that lets the selected worker act
without importing the lead's conversation. Transfer necessary context once; do
not make Astra continuously follow implementation.

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

When overriding Astra to Sol or Luna Max with Codex multi-agent v2, use
`fork_turns="none"` by default or a small positive turn count only when those
recent turns replace a cheaper explicit brief. A full-history fork (`"all"` or
the inherited default) keeps the parent model and reasoning effort and cannot use
the Sol/Luna override; it also defeats the goal of avoiding unnecessary parent
context transfer.

For Luna Max, the packet must remain compact and fully bounded. If creating a
self-contained Luna assignment requires substantial repository explanation,
open-ended exploration, or a long list of judgment calls, use Sol instead.

For Sol, give enough accepted context to own implementation end to end. Do not
keep decisions with Astra merely so the lead can stay involved; reserve only
choices whose consequences genuinely belong to the lead or user.

Suggested mechanisms remain suggestions unless an accepted source makes them
binding. The worker resolves routine technical choices within scope and raises a
conflict only when satisfying the assignment would change accepted behavior,
scope, risk, or another reserved commitment.

## Custody and communication

The worker owns writes to the assigned checkout until it explicitly releases
custody. It preserves unrelated work and must not assume other actors are absent.

A blocking question identifies the unresolved decision, why it matters, and
current custody state. A nonblocking question does not stop independent work.

Do not send routine progress reports. Astra should not pay input/output tokens to
consume intermediate implementation narration that does not change a lead-owned
decision.

If Astra requests checkout access, the worker stops its writers and relevant
subprocesses, reports their state, and releases custody before Astra accesses that
mutable checkout.

A candidate return is reviewable only when it identifies the candidate and
material proof, reports unresolved limitations, and releases custody with
worker-owned writers stopped.

Return decision-relevant evidence, not a narrated implementation journey. Omit
every file inspected, rejected idea, debugging step, and routine test iteration
unless it changes review, recovery, or a consequential decision.

For follow-ups, preserve the established outcome and send only changed context,
findings, acceptance, candidate identity, and renewed custody grant. Reuse the
same worker while its accumulated context remains useful and safe.
