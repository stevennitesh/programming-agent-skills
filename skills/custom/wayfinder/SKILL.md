---
name: wayfinder
description: Resolve one bounded, interdependent foggy effort through a tracker-backed decision map, then return a coherent settled source or terminal decision.
---

# Wayfinder

Resolve one finite, foggy, multi-session effort. Own its map, resolver routing,
reconciliation, and terminal packet. Tickets answer questions and prerequisites;
they never deliver the destination.

## Model

- **Destination:** owner, outcome, scope, exclusions, route-closing condition,
  terminal kind, and return owner.
- **Map:** orientation index; tickets own detail.
- **Frontier:** `Pending`, dependency-unblocked, unclaimed tickets in map order;
  Waiting and Blocked enter only through their evidence-qualified Orient rows.
- **Fog:** one in-scope uncertainty without a sharp question, tethered to a
  finite sharpening source, owner, trigger, and fallback.
- **Operation result:** what this invocation accomplished.
- **Map condition:** `active | waiting | blocked | closeable | closed`.

Use linked titles for people; use provider IDs only for tracker operations.
Keep every sharp question in a ticket, even when blocked.

## Orient

Load the tracker `Wayfinding representation` and, when hosted labels apply,
`Wayfinding Labels`. Freeze its parent/child and dependency modes. Require
inspect and read-back before resolving map identity. Missing or incompatible
inspection setup recommends `$repo-bootstrap` and stops before mutation.

Search open and closed maps for the exact destination tuple. One open match
supplies current state; several open matches return the identity conflict. With
no open match, select exactly one branch: a successor may enter Chart only with
one explicitly selected closed predecessor, one material new gap, explicit
imports, and zero maps matching the destination tuple plus predecessor; one
explicitly selected closed match returns its immutable packet; zero closed
matches may enter initial Chart. Any other ambiguity returns without mutation.
For one map derive:

- **Integrity:** `verified`, `repairable-drift` when accepted evidence permits
  exactly one consequence-only correction, or `incompatible` otherwise.
- **Condition:** use this precedence.

| Evidence | Next operation or return |
| --- | --- |
| Map is closed | Return its immutable closing packet. |
| Integrity is incompatible | Return the exact owner or setup precondition. |
| Integrity is repairable-drift | Maintain. |
| Destination owner confirms cancellation, supersession, or out-of-scope termination | Terminate. |
| A frontier ticket exists | Advance. |
| A Waiting or Blocked ticket has evidence that can answer it | Advance that ticket. |
| A recorded trigger or intervention changes only readiness or fog sharpness | Maintain. |
| Unresolved external triggers remain | Return `waiting` with their owners and required evidence. |
| An authority, capability, growth, or prerequisite blocker remains | Return `blocked` with its intervention. |
| No unresolved ticket, fog, wait, or blocker remains and cited evidence satisfies the route-closing condition | Closure. |
| None applies | Return `incomplete` with the state gap. |

After Orient selects one operation, load only its procedure:

- `Chart`: [CHART.md](references/CHART.md)
- `Advance`: [ADVANCE.md](references/ADVANCE.md)
- `Maintain`: [MAINTAIN.md](references/MAINTAIN.md)
- `Closure`: [CLOSURE.md](references/CLOSURE.md)
- `Terminate`: [TERMINATE.md](references/TERMINATE.md)

Do not load any unselected operation procedure.

After selecting one operation and excluding its no-mutation Returns, require
only its create, update, link, close, claim, release, and read-back
capabilities, including an exclusive claim route with an observable losing-race
result when that operation claims state. A no-mutation Return requires none of
those mutation capabilities. Missing or incompatible selected-operation setup
recommends `$repo-bootstrap` and stops before mutation.

Run exactly one selected operation and return its verified result. A later
invocation re-orients from read-back state and may independently select Closure.

## Mutation Gate

For each invocation generate fresh `codex/<lowercase UUIDv4>` and
`<YYYY-MM-DDTHH:MM:SSZ>` claim values. Reuse them for its ticket and map, never
across invocations. A different token owns an item even for the same actor;
elapsed time alone never makes a claim stale. Replace another token only with
explicit approval from an affirmed destination owner or provider administrator,
after recording the old claim, approver authority, and reason.

**Mutation read-back.** Every non-exception mutation uses one transaction:
verify authority and captured state; acquire every operation-required claim and
read back ownership; refresh decision-bearing state; apply only the selected
change; read back all direct effects and frontier; release every claim; verify
claim absence; Orient. Refresh an indeterminate result before any retry.
Unverified effects return `incomplete` with verified, failed, and unknown state.

Chart is the only pre-claim exception: approve the exact packet, confirm zero
matches for its initial or successor identity, create only the map, repeat
identity search, then claim the sole created canonical map before children or
edges.

Advance freezes the map identity and open state, selected ticket contract and
claim, dependency identities, and frontier eligibility before resolver work.
After acquiring the map claim, require those fields unchanged except for this
invocation's ticket claim. Drift records no tracker outcome or map mutation;
release both claims and verify their absence, preserve and report resolver
evidence and effects within the frozen mutation boundary, and return the
conflict.

## Resolver Gate

Each ticket locks one type, participation, resolution owner, resolver, expected
return, mutation boundary, and `$wayfinder` re-entry:

| Type | Participation and resolver |
| --- | --- |
| Research | AFK; `$research` with the question, supported map use, scope, exact state, Source Trace, Wayfinder return owner, and [Research fields](MAP-FORMAT.md#research-fields). |
| Prototype | HITL or AFK; `$prototype` with [Prototype fields](MAP-FORMAT.md#prototype-fields). |
| Diagnosis | AFK after explicit separate start; return `diagnosis-required` with evidence, environment, exact state, authorities, and Wayfinder as return owner. |
| Grilling | HITL; `$grilling` for a conversation-only user decision, or `$grill-with-docs` while durable domain capture remains active. |
| Questionnaire | External; `$to-questionnaire` only after the user approves its [Questionnaire fields](MAP-FORMAT.md#questionnaire-fields) and `Delivery: not performed`. |
| Task | AFK for one bounded objectively provable repository or operational fact; HITL only for required live human action; no durable mutation. |

A Prototype ticket with a named human judge uses HITL. One with a predeclared
objective rule may use AFK. Its mutation boundary transports named authority
evidence; it does not create authority.

Wayfinder normalizes the intact resolver Return; it never copies callee status
labels blindly:

| Return evidence | Map effect |
| --- | --- |
| Supported answer, confirmed decision, or objective verdict | `resolved` |
| Intact Research `conflicted` | `blocked` with the conflict owner and one observable intervention; never `resolved` or generic `incomplete` |
| Verified questionnaire artifact, human verdict wait, or `diagnosis-required` | `waiting` with owner, trigger, and required evidence |
| Advance receives nested Grilling `Route gap` | Keep the ticket blocked on the admitted replacement graph; never recommend Wayfinder to itself |
| Chart receives a Grilling decision or `Route gap` | Treat it as claim-free proposed Chart input; record no ticket outcome or map mutation, and require exact approval of the resulting packet |
| Exact evidence, authority, setup, or prerequisite gap | `blocked` with one intervention |
| Governing evidence places the question outside the destination | `out of scope` |
| Missing approval, malformed or mismatched return, transport failure, or callee non-admission | `incomplete`; release claims, record no tracker outcome or map mutation, and report any frozen-boundary resolver effects |

`Questionnaire ready` is Waiting, never an answer. Only matching attributable
answers can resolve it. Without exact questionnaire approval, return the packet
and `approve, then re-enter Wayfinder Advance`; do not invoke the callee or
mutate shared state.

## Reconcile

Record one normalized result and only its direct consequences. Give each
affected fog item one disposition: **retain** with its tether, **graduate** into
one or more sharp tickets, **resolve** through linked evidence, or **exclude**
with a governing pointer.

Chart freezes one destination-owner-approved post-Chart ticket allowance,
defaulting to the number of initial fog items. Every later ticket creation
consumes one; other state changes consume none. Add only in-scope obligations
caused by accepted evidence. Exhaustion, destination change, or unsupported
growth returns `blocked` for a new finite approval, Terminate, or successor.
Never invoke another resolver while reconciling.

## Return

Return only applicable fields:

```text
Operation result: oriented | charted | advanced | maintained | closed | terminated | not-needed | incomplete
Map condition: active | waiting | blocked | closeable | closed
Map and operation:
Destination and integrity:
Selected ticket and normalized outcome:
Evidence and direct changes:
Growth allowance: total | used | remaining
Domain Delta: <intact packet or not applicable>
Claims: <verified release or exact conflict>
Next admission: <frontier ticket | trigger | intervention | Closure | successor | none>
Suggested owner: <one uninvoked skill or user action, or none>
```

When a frontier remains, end with `Next frontier: [<ticket title>](<link>).
Invoke $wayfinder to advance it.`
