# Candidate Follow-up

Load this branch-only contract only for a material current-user decision,
returned evidence, or one justified next-owner suggestion.

## Suggest Zero Or One Next Owner

Choose the first unresolved work, not an eventual workflow:

| Remaining work | Suggested owner |
| --- | --- |
| One non-diagnostic source-answerable authoritative fact | `$research` |
| One settled design question needing a disposable runnable probe or performance experiment | `$prototype` |
| Broken or slow behavior with uncertain expectation, symptom, cause, or trusted reproduction | `$diagnosing-bugs` |
| Settled domain language, Invariant, Bounded Context, Context Relationship, or ADR candidate needing durable capture | `$domain-modeling` |
| One current-user decision that also requires domain-record maintenance | `$grill-with-docs` |
| One conversation-only current-user decision | `$grilling` |
| One identifiable external stakeholder holding unavailable knowledge | `$to-questionnaire` |
| Multiple interdependent unresolved decisions or prerequisites | `$wayfinder` |
| Settled direction and commitments needing a parent specification | `$to-spec` |
| Settled multi-slice implementation with a parent spec or no need for one | `$to-tickets` |
| One bounded behavior-preserving reduction | `$simplify-code` |
| One settled non-reduction correction or addition with finite Repair budget | `$implement` |
| Disproved candidate or no justified route | `none` |

Diagnosis wins over Prototype for an uncertain observed symptom. A current-user
decision precedes design. To Spec wins when a parent specification is required.
Codebase Design is loaded during Analyze for design or mixed candidates and is
not a next owner.

Label a suggestion `user selection required`, invoke nothing, and encode no
workflow chain. For a non-`none` suggestion record:

```text
Suggested next step:
Suggestion reason:
Pickup prerequisite:
Result recipient:
Audit re-entry: <exact invocation> | none
Suggested invocation:
```

The invocation names the skill, candidate ID, absolute report path, and
callee-compatible admission facts without copying the callee's procedure.
The callee never re-enters Audit.

For an `$implement` suggestion, the generated pickup also authorizes the root
to reconcile the matching candidate from the exact completion packet after a
successful verified commit and before responding to the user. Attempt the
Audit-owned report update once. If it fails, preserve the implementation
success and existing HTML, return the exact reconciliation failure and future
Audit re-entry, and stop. Do not start another candidate.

Other planning and execution routes use `Audit re-entry: none`.

## Decision Brief

When one material current-user-owned decision blocks analysis, record:

```text
Run ID:
Subsystem ID:
Candidate ID:
Last verified identity:
Decision:
Why it is material:
Governing domain terms, Invariants, relationships, and ADRs:
Constraints:
Viable options and consequences:
Evidence already settled:
Exact unresolved question:
Decision owner: current user
Documentation effect: none | Domain Delta required
Re-entry invocation:
```

Recommend `$grilling` when documentation effect is `none`,
`$domain-modeling` when meaning is settled and only durable capture remains,
and `$grill-with-docs` when the decision and Domain Delta are both required.
Render context only unless domain mutation is separately authorized.

## Returned Evidence

Before changing a judgment, match the report, run, subsystem, candidate,
question or claim, result owner, authority, status, freshness, and intact
payload or pointer. A mismatch changes no judgment.

- Answering evidence reruns only dependent judgments.
- Disproving evidence marks the candidate `disproved`.
- A matching complete implementation packet applies the Close Implemented gate.
- Unresolved required evidence marks it `blocked` with exact re-entry.
- A foreign recommendation is evidence only; Audit chooses any next owner.
- `Questionnaire ready` is not answer evidence; require attributable
  stakeholder answers.
- An unchanged exhausted or blocked return keeps suggestion `none` until its
  named unblock condition changes.

A returned Domain Delta is current evidence. Rebuild the affected Source Trace
and judgments. Require Map reconciliation only when it changes the subsystem
boundary; do not invalidate unrelated report content.

## Bound

Follow-up transports one decision, evidence packet, or suggestion. It grants no
mutation authority and starts no downstream work.
