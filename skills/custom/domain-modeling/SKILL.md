---
name: domain-modeling
description: Resolve or capture project-specific domain meaning, invariants, bounded contexts, relationships, or an already-settled ADR candidate. Exclude vocabulary lookup, code-structure design, and unresolved product or architecture decisions.
---

# Domain Modeling

Settle one bounded domain distinction and keep its owning record current when
durable capture is warranted and authorized.

**Model, don't catalog.** Capture project-specific meaning, defining behavior,
invariants, responsibility, and relationships. Leave generic technical terms,
code indexes, procedures, and code-shape decisions with their owners.

## 1. Ground

Identify the bounded distinction, relevant routed domain records and ADRs,
load-bearing evidence, meaning authority, caller, and return owner. Read
`docs/agents/domain.md` and follow its configured route. If that contract is
missing or incompatible, recommend `$repo-bootstrap` and stop. A missing routed
record is not a setup gap; create the first one only for an authorized settled
distinction.

Code, tests, contracts, runtime behavior, and widespread usage show how the
system works. They do not settle intended meaning. Bounded contexts follow
meaning, language, responsibility, and consistency, not directories or
services. If the correct route itself must change, return that requirement to
`$repo-bootstrap` and stop before writing.

## 2. Clarify

Call out conflicting definitions and sharpen vague or overloaded terms. Use a
concrete normal, edge, failure, inclusion, or exclusion scenario only when its
answer could change the model.

The direct user or named domain authority settles intended meaning. Direct use
may ask that owner one focused question. Under `$grill-with-docs`, accept each
settled answer that may affect domain meaning and return any collision before
dependent questioning continues. Other callers retain unresolved choices.

## 3. Settle

Resolve the canonical term or decision, defining behavior, owning context,
evidence, and authority. Add an alias, invariant, boundary, relationship, or
consequence only when it changes the model. When implementation and intended
meaning disagree, let the meaning authority classify an implementation defect,
model correction, or intentional migration.

For a context relationship, record only the responsibility, crossing contract,
language translation, or change authority whose omission would make the
boundary ambiguous. Code-shape consequences return to the design or
implementation owner.

Reconcile with routed current records before adding text. Prefer no change,
replacement, merge, relocation, or removal over a second current statement.
Keep procedure, commands, mutable state, implementation inventories, and
decision rationale with their owners.

## 4. Capture

Capture only a non-obvious durable distinction that future work would likely
misapply without a record. Otherwise return no change. For a material delta,
return proposed wording by default and write only after an explicit persistence
request or exact caller authority. Read
[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) only when a material context delta needs
rendering or persistence. Read [ADR-FORMAT.md](./ADR-FORMAT.md) only for an
already-settled candidate that may clear its worthiness test. ADR recording
always needs separate approval for that identified candidate.

Before writing, refresh the route and targets and preflight the bounded change.
Order dependent writes so every verified intermediate state retains readable
current truth; make replacements readable before removing displaced material.
Reread every attempted target, including one whose write reports failure, and
classify it as verified changed, verified unchanged, or unknown. On the first
failure, stop and report the exact per-target state. Do not mutate foreign-owner
consequences; return each unapplied consequence to its owner with enough detail
to resume.

## 5. Return

Return the settled distinction, exact unresolved question, no-change result, or
verified changed paths to the user or caller, then stop. Include authority,
blockers, consequences, ADR outcome, and per-target state only when they affect
the result.

Under `$grill-with-docs`, return the current domain result after each answer
that may affect domain meaning. A no-change result is valid. Accumulate only
current domain consequences, collisions, and applicable write evidence. Domain
Modeling does not choose interview materiality, branching, or downstream work.

## Completion

Complete when the bounded distinction is settled or returned to its owner as
one exact question, every in-scope consequence is applied, no-change, or
returned to its owner, every attempted write has exact state, and no downstream
work has started.
