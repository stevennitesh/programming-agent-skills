# Wayfinder Map Format

Read the applicable groups while drafting, creating, orienting, reconciling, or closing a map. This file owns persisted meaning; `SKILL.md` owns state, mutation, growth, and completion; `OPERATIONS.md` owns branch procedure; the target tracker mapping supplies provider representation and primitives only.

The map is an index, not a transcript. Resolution detail stays in its ticket or resolver artifact. Use linked human-readable names in reports and provider ids only for transport and relationships.

## Map

```markdown
## Campaign

Stable destination identity:
Provider identity and Chart refetch evidence:
Predecessor:
Lifecycle: open | closed
Disposition: active | waiting | blocked | delivered | superseded | cancelled | out-of-scope
Closure generation:

## Authority

Destination owner:
Observable authority evidence:
Chart approval evidence:
Reserved decisions:
Bounded delegate, when one exists:
Allowed resolver types:
Graph-expansion authority: destination-owner approval under Budget Authority
Destination-change authority: successor only
Domain persistence: authorized now | deferred to Closeout
ADR creation: explicit approval required

## Destination

Destination:
Scope boundary:
Route-closing condition:
Explicit exclusions:
Design-coherence reference:

## Budgets

Outcome total, reserved, used, uncommitted, and calculation:
Expansion total, used, remaining, and calculation:
Correction total, reserved, used, uncommitted, and calculation:
Named contingency and justification, or none:

## Source Trace

<repo, domain, design, evidence, and predecessor pointers>

## Ticket Index

- [<ticket name>](link) - <type>; <state>; blocked by <links | none>

## Decisions So Far

- [<ticket name>](link) - <one-line gist>

## Not Yet Specified

<tethered fog items; when empty, write exactly: None - all remaining in-scope questions are ticket-owned.>

## Out Of Scope

- [<governing resolution, ticket, map, or successor>](link) - <reason>

## Liveness

Waiting owner and trigger:
Waiting needed-back ledger and artifact:
Blocked intervention:
Budget exhaustion evidence, when applicable:
Resume history:
Active frontier:

## Closure

Closeout attempts and typed gaps:
Gather revision vector:
Pre-Seal revision vector:
Post-close revision:
Post-release revision:
Durability result:
Sealed or terminal packet pointers:

## Corrections

To Spec returns and approved packets or amendments:
Correction graph and proof:
Correction capacity:
Reopen generations:
```

Do not create a ticket only to provide an Out Of Scope link. Use the existing resolution, map, or successor that governs the exclusion.

## Ticket

```markdown
## Wayfinder Ticket

Parent map:
Resolver type: Research | Prototype | Diagnosis | Questionnaire | Grilling | Design | Task
Participation: AFK | HITL | external
Question or prerequisite:
Destination impact:
Resolution authority:
Dependencies:
Expected return:
Proof or confirmation:
Mutation boundary:
Budget source: outcome | correction
Reservation:
State: open | awaiting-external-response | resolved | blocked | out-of-scope

## Resolver Fields

Research note path:
Prototype claim level: shape/feel | design evidence
Prototype human judge | objective verdict criteria:
Questionnaire caller and return owner:
Questionnaire caller item or decision identifier:
Questionnaire recipient name or role:
Questionnaire recipient expertise and relationship to sender:
Questionnaire downstream decision or prerequisite:
Questionnaire needed-back ledger:
Questionnaire authorized context and source pointers:
Questionnaire deadline and effort budget:
Questionnaire authorized output root or exact path:
Questionnaire sensitive-context constraints:
Questionnaire known delivery assumptions:
Questionnaire waiting owner, observable trigger, and artifact:
Design acceptance owner or objective criteria:

## Outcome

Disposition and answer:
Evidence and artifact pointers:
Direct consequences:
```

Use exactly one resolver type. Classify by resolution authority, not wording. Split independently decidable facts from human-owned choices.

## Campaign Claim

```text
Actor:
Token:
Timestamp:
Operation: Advance | Maintain | Resume | Closeout-gap | Closeout-Seal | Terminate | Reopen
Selected ticket, Advance only:
```

`SKILL.md` owns token generation, claim lifetime, staleness, takeover, recovery, and release semantics. The tracker mapping owns only provider representation and primitives. Persist no independent ticket claim.

## Tethered Fog

Every fog item records:

```text
Unresolved uncertainty:
Destination impact:
In-scope reason:
Expected sharpening source:
Unlock condition or observable trigger:
Affecting tickets or external events:
Fallback disposition if the trigger never arrives:
```

`Not Yet Specified` is the only fog container. Orphan fog without a finite sharpening path is an Admission evidence gap.

## Closure Snapshot

Each Gather and sealed generation records:

```text
Identity, lifecycle, disposition, generation, and Gather revision vector:
Authority, destination, scope, closing condition, budgets, and claim absence:
Complete in-scope ticket index with resolver, state, dependencies, dispositions, and revisions:
Accepted, rejected, deferred, and excluded decisions with evidence pointers:
Research, prototype, diagnosis, questionnaire, grilling, task, and design returns:
Domain deltas, ADR outcomes, and accepted engineering constraints:
Actor, workflow, edge-case, failure, proof, and observable-outcome constraints:
Residual nonmaterial uncertainty and revision evidence for every declared source:
Coherence lens results and typed gaps:
Durability result and changed paths:
Pre-Seal revision vector:
```

Every sealed generation is immutable. Post-close and post-release revisions live in the map's Closure fields and provider history because they occur after sealing; the snapshot does not duplicate a full tracker snapshot or make itself self-referential.

## Terminal Packet

```text
Disposition: superseded | cancelled | out-of-scope
Destination-owner confirmation:
Reason and evidence:
Budgets:
Unresolved obligations:
Recovery or successor boundary:
Closed-state and claim-absence evidence:
```

## Correction And Successor

A delivered-map correction packet records the To Spec evidence, in-scope classification, one cohesive dependency graph, finite cumulative correction capacity, acceptance authority, proof, and amendment history.

A successor records:

```text
Predecessor and terminal disposition:
Reason destination or scope changed:
Decisions and evidence imported unchanged:
Decisions invalidated or reopened, with reasons:
Unresolved obligations deliberately transferred:
Exclusions retained or reconsidered:
Governing domain and design constraints:
Fresh destination, scope, closing condition, graph, budgets, and approval:
```

Claims, state, frontier order, budgets, and closure status never transfer implicitly.
