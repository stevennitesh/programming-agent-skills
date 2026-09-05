# Delivery boundaries

Read for cross-ticket composition, risky learning, or a wide migration.

## Preserve meaning across tickets

Assign the first dependency-complete consumer responsibility for checking the
introduced or changed caller-visible path. Pass the producer's actual result or
its actual persisted representation through the ordinary consumer. Isolated
producer and consumer tests do not establish their connection.

Carry source-defined success and rejection states, nullability, issue scope,
provenance, availability, identity, units, time meaning, and governing versions
when losing them would violate acceptance. A mixed valid/invalid case is useful
when independent inputs must remain isolated. Preserve precedence where accepted
rules or stopping criteria can disagree. A learning ticket's budget exhaustion
does not authorize a success verdict.

Keep the required evidence class: fixtures, representative artifacts, measured
comparisons, and live checks establish different claims. Preserve source-defined
conditions on safe inputs and unresolved evidence gaps. Deployment or installation
acceptance must observe the intended target, not merely command success.

Do not defer every connection to a final integration ticket. Check each complete
path at its earliest useful consumer; reserve final integration for properties
that actually require the combined result.

## Choose migration boundaries from real constraints

When consumers can move together, prefer one coherent migration over compatibility
code added solely to keep intermediate edits green. When old/new clients, workers,
or stored data must coexist, sequence expansion, migration, and removal around
those obligations. Each stage names its guarantee, verification, and dependency;
include rollback and data-conversion constraints that affect delivery.

If separate changes cannot be independently usable, keep them in one delivery
unit or explicitly designate their shared integration and verification boundary.
Do not claim individually releasable tickets where only their combination works.
Temporary breakage is acceptable only within authorized, isolated, reversible
work; it is not permission to break shared consumers or deployment contracts.

## Use learning to change the plan

Name the uncertainty, the observation that would distinguish outcomes, and which
later decisions depend on it. Later ticket bodies should remain conditional where
the experiment may change them. After evidence returns, revise affected scope and
dependencies before treating those tickets as ready. A prototype is not a
production implementation merely because its experiment succeeded.
