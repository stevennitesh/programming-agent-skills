# Locked Sample Outputs

These are the durable normalized packets returned by the formal sample tasks in
[`locked-launch-record.md`](locked-launch-record.md). They retain each worker's
residency result, behavior judgment, failures, deviations, and unavailable
telemetry. No excluded exploratory or pre-repair sample is included.

## LC1 / P1 / Control

- Resident: monolithic Wayfinder Model, Orient, Mutation Gate, Resolver Gate,
  Reconcile, all five operations, Return; full MAP; monolithic Grilling.
- Selected: initial Chart, Research ticket, ready-frontier Grill.
- Result: exact packet approval; Chart's create-only-map, repeat-search, claim,
  then children/edges exception; `charted`; no ticket outcome or retained
  claim. Research adds only note path/write mode and re-enters Wayfinder.
- Inactive but resident: four operations, other type fields/MAP shapes, all gap
  routes, one-owner and Handoff rules.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only.
- Unavailable: live approval, tracker identities, claims/races, mutations,
  resolver result, Grilling answer, token/timing telemetry.

## LC2 / P2 / Control

- Resident: all Wayfinder operations and MAP shapes/type fields; all Grilling
  gap routes.
- Selected: Research Advance, Prototype field definition, authoritative-source
  Evidence gap.
- Result: freeze, claim ticket, resolver, claim map, detect changed dependency,
  record no outcome/map mutation, preserve resolver evidence/effects, release
  both claims, Return exact conflict. Prototype fields remain type-only.
  Grilling selects exactly one uninvoked `$research` owner.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only. Minor shared ambiguity: drift has no distinct
  operation-result enum and is represented as `incomplete` plus exact conflict.
- Unavailable: runtime identities, claims, provider effects, exact post-Orient
  state, token/timing telemetry.

## LC3 / P3 / Control

- Resident: all operations, full MAP, and all Grilling gap routes.
- Selected: one deterministic Maintain repair, Questionnaire fields with
  missing approval, active-Wayfinder Route gap.
- Result: map-claim transaction applies one consequence-only correction and no
  ticket outcome; Questionnaire invokes nothing and returns `approve, then
  re-enter Wayfinder Advance`; intact Route gap returns to active Wayfinder
  without self-recommendation.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only.
- Unavailable: tracker state, repair delta/read-backs, packet values, live gap
  payload, token/timing telemetry.

## LC4 / P4 / Control

- Resident: all operations, all MAP shapes/type fields, all Grilling routes.
- Selected: Closure, Closing Packet, Prototype Evidence gap with Handoff.
- Result: claim-free Gather, Coherence, Domain Modeling once; missing write and
  ADR authority select `render only` and `offer only`; coherent render permits
  Seal; close as delivered. Exactly one `$prototype` gap owner; Handoff is
  uninvoked transport only.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only.
- Unavailable: live Domain Delta, claim/read-back, prototype/transport effects,
  token/timing telemetry.

## LC5 / P5 / Control

- Resident: all Wayfinder operations/resolver routes and the complete Grilling
  Gap procedure; MAP omitted by the fixture.
- Selected: Terminate and ready-frontier Grill.
- Result: capture unresolved obligations/recovery boundary, claim, post, close,
  read back, release, Orient, return `terminated`/`closed`; bypass Closure,
  Domain Modeling, and To Spec. Grilling does not enter a gap.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only.
- Unavailable: live cancellation evidence, tracker/claim effects, Grilling
  answer, token/timing telemetry.

## LK1 / P1 / Candidate

- Resident: Wayfinder main, `CHART.md`, MAP common Ticket/Research lines 49-74,
  Grilling main. No other operation, type section, or gap reference.
- Selected/result: same Chart, Research, ownership, transaction, exception, and
  terminal behavior as LC1.
- Semantic failures: none. Critical failures: none. Deviations: none.
- Unavailable: same live effects as LC1; candidate tree identity was frozen by
  the arm context.

## LK2 / P2 / Candidate

- Resident: Wayfinder main, `ADVANCE.md`, MAP common/Prototype lines, Grilling
  main and terminal-gap reference. Other operation/type sections excluded.
- Selected/result: same post-resolver dependency-drift abort, Prototype-only
  fields, one `$research` gap owner, claim safety, and terminal stop as LC2.
- Semantic failures: none. Critical failures: none. Deviations: none. The same
  noncritical `incomplete`-plus-conflict enum ambiguity remained.
- Unavailable: live claims, resolver effects, post-Orient state, token/timing.

## LK3 / P3 / Candidate

- Resident: Wayfinder main, `MAINTAIN.md`, MAP common/Questionnaire lines,
  Grilling main and terminal-gap reference. Other operations/types excluded.
- Selected/result: same one-repair transaction, no-approval stop, Wayfinder
  re-entry, active-Wayfinder exception, and terminal Return as LC3.
- Semantic failures: none. Critical failures: none. Deviations: none.
- Unavailable: live repair/read-back, packet values, gap payload, token/timing.

## LK4 / P4 / Candidate

- Resident: Wayfinder main, `CLOSURE.md`, exact Closing Packet lines 114-131,
  Grilling main and terminal-gap reference. Ticket/type MAP sections and four
  operation references excluded.
- Selected/result: same claim-free Gather, non-persisting durability modes,
  coherent Seal, one `$prototype` owner, Handoff transport, and terminal stop
  as LC4. Missing write/ADR authority is explicitly not itself a blocker.
- Semantic failures: none. Critical failures: none. Deviations: none.
- Unavailable: live Domain Delta, claim/read-back, prototype/transport effects,
  token/timing.

## LK5 / P5 / Candidate

- Resident: Wayfinder main, `TERMINATE.md`, Grilling main. No MAP, other
  operation, or terminal-gap reference.
- Selected/result: same Terminate transaction/bypass and advanceable-frontier
  Grilling behavior as LC5.
- Semantic failures: none. Critical failures: none. Deviations: none.
- Unavailable: live terminal effects, Grilling answer, token/timing.

## CWC1 / W1 / Control

- Resident: both historical monoliths, including every inactive operation,
  resolver route, generic mutation rule, and terminal gap route. MAP omitted.
- Result: Wayfinder selects no operation and returns `incomplete` with exact
  state gap and no mutation capability; Grilling advances the ready frontier
  and returns no gap.
- Semantic failures: none. Critical failures: none. Deviations: expected
  monolithic over-disclosure only. Runtime effects unavailable.

## CWC2 / W1 / Control

- Same locked residency and behavior as CWC1.
- Semantic failures: none. Critical failures: none. Deviations: none beyond the
  registered control over-disclosure. Runtime effects unavailable.

## CWK1 / W1 / Candidate

- Resident: candidate Wayfinder and Grilling main files only. No operation,
  MAP, or terminal-gap reference.
- Result: same safe no-operation Wayfinder Return and ready-frontier Grilling
  behavior as CWC1. No claim, mutation, resolver, owner, transport, successor,
  or automatic continuation.
- Semantic failures: none. Critical failures: none. Deviations: none. Runtime
  effects unavailable.

## CWK2 / W1 / Candidate

- Same locked residency and behavior as CWK1.
- Semantic failures: none. Critical failures: none. Deviations: none. Runtime
  effects unavailable.
