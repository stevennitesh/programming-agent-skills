---
name: wayfinder
description: Coordinate one bounded destination whose interdependent decision questions need tracker-backed multi-session resolution. Exclude one-session decisions, settled specifications, implementation planning, and delivery.
---

# Wayfinder

Clear one bounded, foggy decision route through a shared tracker map. The map is
an index. Tickets own the questions, evidence, and decisions. Wayfinding plans;
it never implements the destination.

An invocation charts a map, advances one ticket, or finishes the route. It does
not do more than one of those.

## Bound

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` for the
configured tracker operations, relationships, and labels. If either contract is
missing or incompatible, recommend `$repo-bootstrap` and stop. Name one
destination with its owner, outcome, in and out boundary, observable closing
condition, and return owner.

Use Wayfinder only when several coupled questions or prerequisites, including
at least one non-conversational resolver, need durable sequencing across
sessions. If one conversation, one resolver, or settled source can finish the
work, return `not needed` with the smaller need and do not create a map.

Search open and closed maps for the exact destination. Return a closed map's
record unchanged. Several matches are an identity conflict. With one open map,
read its current questions, dependencies, claims, decisions, fog, and scope.
With no match, continue to Chart.

## Chart

Work breadth-first. Create one ticket for each question or prerequisite that is
sharp now. A ticket must be resolvable by a fresh agent from its own question,
importance, owner, dependencies, and acceptance evidence. Keep an in-scope
uncertainty as fog only while the question cannot yet be stated sharply; name
the evidence or decision that would sharpen it.

Label the map `wayfinder:map`. Give each ticket exactly one label matching its
`Type`: Research uses `wayfinder:research`, Prototype uses
`wayfinder:prototype`, Grilling uses `wayfinder:grilling`, Questionnaire uses
`wayfinder:questionnaire`, and Task uses `wayfinder:task`. Wayfinder status
lives in its recorded condition, claims, dependencies, and tracker open or
closed state, not in the triage state roles.

Order dependency-ready tickets by how much they can unblock, invalidate, or
reshape the remaining route. Use map order as the tie-breaker.

Show the destination owner one concise packet conforming to
[MAP-FORMAT.md](MAP-FORMAT.md). After exact approval, read
[Mutation](references/MUTATION.md), create the map first, repeat the identity
search, then create its tickets and edges. Complete mutation read-back of the
graph and stop.

## Advance

Select a named eligible ticket or the highest-value unclaimed frontier ticket.
Read [Resolvers](references/RESOLVERS.md) only for the selected ticket. When an
explicit-only resolver first needs user action, return its exact packet and
re-entry instruction before any claim or shared mutation. Otherwise, before
resolver work, read [Mutation](references/MUTATION.md), claim the ticket, and
freeze only the question, owner, resolver route, dependencies, eligibility,
destination, and scope.

Resolve that question through its owner. Accept cited source evidence, a
runnable verdict, or an attributable human decision only when it answers the
ticket as written. A summary, questionnaire path, malformed return, or
unsupported status is not an answer.

## Reconcile

Claim the map for the short reconciliation step and reread the frozen fields.
On material drift, preserve the resolver evidence, record no ticket outcome,
release the claims, and return the conflict.

Otherwise record one answer, wait, blocker, or out-of-scope result and only its
direct map consequences. Detailed evidence stays in the ticket; the map gets a
linked one-line gist. Add a ticket only when accepted evidence exposes a new
sharp in-scope question needed for closure. A changed destination, wider scope,
or material expansion of the remaining effort needs destination-owner approval
or a new map.

Read back the affected ticket, map, dependencies, and frontier. Release every
claim, verify absence, and stop. Never retain a claim across an external or
user wait.

## Finish

When questions or fog remain, return the next frontier ticket, exact wait, or
blocker with its owner and observable return condition.

Close successfully only when every in-scope question and fog item has a
disposition and current cited evidence satisfies the closing condition. Post
the concise closing record from [MAP-FORMAT.md](MAP-FORMAT.md), close through
[Mutation](references/MUTATION.md), read back closed state, and stop.

For owner-confirmed cancellation, supersession, or out-of-scope termination,
use the separate termination record. Do not claim route-closing satisfaction.
Closed maps are immutable.

Wayfinder returns the map, what changed, decisive evidence, the next question
or condition, and verified claim state. After Finish it starts no downstream
skill.

Completion requires the exact map to be closed, every in-scope obligation to
have an evidence-backed disposition, the approved destination condition to be
satisfied or truthfully terminated, no claim to remain, and the terminal record
to be read back.
