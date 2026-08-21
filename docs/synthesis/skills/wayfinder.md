# Wayfinder current runtime synthesis

Status: current ownership and relationship reference. Runtime procedure remains
in `skills/custom/wayfinder/`.

## Outcome and boundary

Wayfinder clears one bounded multi-session decision route through a shared
tracker map. It owns destination identity, question tickets, fog, dependencies,
frontier choice, per-session claims, resolver selection, direct consequence
reconciliation, and truthful finish.

The map is an index. Tickets own detailed questions, evidence, and decisions.
Wayfinder never implements the destination, slices delivery work, or chooses a
later delivery route.

Entry requires all of these:

- one bounded destination;
- several coupled unresolved questions or prerequisites;
- at least one non-conversational resolver; and
- a real need for tracker-backed sequencing across sessions.

Upstream skills recommend explicit Wayfinder and stop. One conversation, one
resolver, settled source, implementation planning, and delivery remain outside
its boundary.

## Runtime authority

- `skills/custom/wayfinder/SKILL.md`: Bound, Chart, Advance, Reconcile, Finish,
  and the sole completion condition.
- `skills/custom/wayfinder/MAP-FORMAT.md`: lean persisted decision shapes.
- `skills/custom/wayfinder/references/MUTATION.md`: loaded only before a durable
  tracker write.
- `skills/custom/wayfinder/references/RESOLVERS.md`: loaded only for the
  selected ticket.
- `skills/custom/wayfinder/agents/openai.yaml`: explicit-only invocation.
- configured tracker `Wayfinding representation`: provider operations, claim
  storage, labels, relationships, and mutation read-back.

No other Wayfinder package is runnable or manifest-tracked.

## Five-action loop

```text
Bound
├─ no map and route earns durable sequencing -> Chart and stop
├─ one open map with an eligible question -> Advance one ticket
├─ no eligible question but exact wait or blocker -> return it
└─ every obligation disposed -> Finish and stop

Advance -> Reconcile -> read back -> release -> stop
```

Chart works breadth-first. It creates tickets only for sharp questions and
keeps unsharp in-scope uncertainty as fog with one sharpening condition. Among
ready tickets, information value controls order: prefer the question most
likely to unblock, invalidate, or reshape the route, then use map order.

Advance resolves one ticket. Reconcile records one attributable answer, wait,
blocker, or scope disposition and only its direct map consequences. A changed
destination, wider scope, or material expansion returns for owner approval or a
new map. No numeric growth allowance is persisted.

Finish closes successfully only from current cited evidence satisfying the
destination condition. Cancellation, supersession, and out-of-scope termination
use a separate record and never claim successful closure.

## Mutation protection

Wayfinder uses a fresh unpredictable claim token because several sessions may
share one tracker account. It claims the ticket before resolver work and the map
only for the reconciliation or closing write. Another token remains foreign
until the destination owner or provider administrator approves replacement;
time alone never expires it.

Chart detects a duplicate race by creating the map before children, repeating
the destination search, and continuing only with one match. Reconcile refreshes
only decision-bearing state after long resolver work. Unrelated comments do not
create drift.

Every durable write reads back the changed items, affected dependencies,
resulting frontier, and claim release. Failed or indeterminate writes are
inspected before retry. Partial state is reported as applied, failed, and
unknown with the safest recovery.

## Resolver composition

| Ticket | Relationship and boundary |
| --- | --- |
| Research | Invoke `$research` for one source-answerable question. |
| Prototype | Invoke `$prototype` with a named human judge or objective rule. |
| Grilling | Invoke `$grilling` for one conversation-only user decision, or `$grill-with-docs` when that decision also needs live domain reconciliation. |
| Questionnaire | Recommend explicit `$to-questionnaire` and stop before claims or shared mutation. A returned path is waiting evidence, never an answer. |
| Task | Establish one bounded prerequisite without durable mutation; a required human action becomes waiting. |

Resolver skills own their method, evidence judgment, local mutation, and Return.
Wayfinder accepts a result only when cited evidence or an attributable decision
answers the selected question. It never copies a callee status blindly.

## Durable shapes

The map stores destination, scope, closing condition, return owner, only the
pointers every session needs, linked decision gists, fog, and exclusions.

A ticket stores its type, decision owner, dependencies, acceptance evidence,
one sharp question, why the answer matters, and a mutation boundary only when
applicable. Type-derived resolver and participation fields and the constant
Wayfinder re-entry field are not persisted.

Successful closure stores destination, closing evidence, decision links,
exclusions or residuals, and return owner. Unsuccessful termination stores the
confirming owner and evidence, unresolved or preserved work, recovery or
successor pointer, and return owner.

## Active relationships

- Router, Grilling, Triage, and Audit Codebase recommend Wayfinder and stop only
  on the complete entry predicate.
- Wayfinder invokes Research, Prototype, Grilling, or Grill With Docs only for
  one selected ticket.
- Wayfinder recommends Repo Bootstrap only when required tracker setup is
  missing.
- Wayfinder recommends To Questionnaire only for explicit user invocation.
- After Finish, Wayfinder returns to the named owner and starts no specification,
  ticketing, implementation, or domain-persistence workflow.

## Proof surface

Current proof should establish narrow admission, exact-map duplicate refusal,
one-ticket progress, same-account claim exclusion, post-resolver drift fencing,
claim-free explicit resolver re-entry, direct-only map growth, truthful waiting
and blocking, distinct finish and termination records, evidence-backed closure,
and verified claim absence.

Exact wording, removed operation names, numeric allowance fields, and return
taxonomies are not protected behavior.

Historical validation and issue #88's progressive-disclosure evaluation remain
evidence for the prior five-operation contract. They are not current runtime
instructions or proof that those operations still earn their cost.

## Current reconciliation

Pack composition revision 30 and machine contract revision 18 own the current
runtime projection. Canonical Wayfinder package tree SHA-256:
`2ee050f8870ab54f40ec0a6ea6a4098b218223eb078f1d152d5c18b4899302fc`.
