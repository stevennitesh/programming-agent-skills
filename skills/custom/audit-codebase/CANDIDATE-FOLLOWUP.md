# Candidate Follow-up

Apply this branch-only contract only after `SKILL.md` admits it.

## Publish Implementation Work

Accept only To Tickets `ready-graph`, or an exact-semantic `reused` result,
bound to the candidate digest with publication read-back and a Ready-for-agent
tracker item. Record the provider-native graph and item identities. The helper
generates one Implement pickup bound to the Ready tracker item, candidate,
report, and exact Close packet; publish it unchanged and do not invoke it.

A non-ready or partial ticket result is `recovery`: record observed state and
publish no Implement prompt.

If the candidate is implementation-ready but the selected Analyze invocation
lacks the generated prompt's exact To Tickets authority, publish
`authority-required`, invoke nothing, and use the helper-derived Analyze
re-entry. This is not tracker recovery.

## Suggest Zero Or One Other Owner

Choose the first unresolved work, not an eventual workflow:

| Remaining work | Suggested owner |
| --- | --- |
| One non-diagnostic source-answerable authoritative fact | `$research` |
| One settled design question needing a disposable runnable probe or performance experiment | `$prototype` |
| Broken or slow behavior with uncertain expectation, symptom, cause, or trusted reproduction | `none`; return `blocked` with result `diagnosis-required`, the evidence limit, and exact re-entry |
| Settled domain language, Invariant, Bounded Context, Context Relationship, or ADR candidate needing durable capture | `$domain-modeling` |
| One current-user decision that also requires domain-record maintenance | `$grill-with-docs` |
| One conversation-only current-user decision | `$grilling` |
| One identifiable external stakeholder holding unavailable knowledge | `$to-questionnaire` |
| Multiple interdependent unresolved decisions or prerequisites | `$wayfinder` |
| Settled direction and commitments needing a parent specification | `$to-spec` |
| One bounded behavior-preserving reduction | `$simplify-code` |
| Disproved candidate or no justified route | `none` |

Implementation-ready work without a required parent specification uses
**Publish Implementation Work**, not this table. An uncertain observed symptom
is not Prototype work. A current-user decision precedes design.

Except for To Tickets above, label a suggestion
`user selection required`, invoke nothing, and encode no workflow chain. For a
non-`none` suggestion record:

```text
Suggested next step:
Suggestion reason:
Pickup prerequisite:
Result recipient:
Audit re-entry: <exact invocation> | none
Suggested invocation:
```

For every route, `update_report.py inspect` returns the complete selected JSON
record. The root constructs the callee-compatible packet without parsing HTML
or copying the callee's procedure into the pickup.

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
- A matching complete implementation packet is admissible evidence for a
  separately selected Close objective.
- Unresolved required evidence marks it `blocked` with exact re-entry.
- A foreign recommendation is evidence only; reapply this contract's
  first-unresolved-work rule.
- `Questionnaire ready` is not answer evidence; require attributable
  stakeholder answers.
- An unchanged exhausted or blocked return keeps suggestion `none` until its
  named unblock condition changes.

A returned Domain Delta is current evidence. Rebuild the affected Source Trace
and judgments. Require Map reconciliation only when it changes the subsystem
boundary; do not invalidate unrelated report content.

## Bound

Follow-up transports one decision or evidence packet, publishes one bounded
implementation tracker graph through `$to-tickets`, or suggests one other owner.
It grants no product mutation authority and never starts implementation.
