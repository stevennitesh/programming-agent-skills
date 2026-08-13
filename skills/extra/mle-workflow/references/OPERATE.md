# Operate, Respond, Refresh, and Retire

Read this file when the requested operation concerns an active system,
production-readiness scope reaches field operation, or the task includes
refresh, incident response, rollback, or retirement.

## Resolve authority before effects

Separate:

- **Observe or diagnose:** read-only inspection, evidence collection, and
  recommended response.
- **Respond or recover:** state-changing stop, traffic control, isolation,
  fallback, rollback, repair, or replay.

Before an effect, identify the lifecycle-transition owner, escalation route,
and explicit execution authority or approved automatic safety control. Tests,
alerts, dashboards, and gates provide evidence; they do not grant authority.
Without authority, return the recommended action and block only the transition.

After each attempted effectful transition, read the authoritative target state
and material external effects. Distinguish `not attempted`, `zero effect`,
`success`, `partial effect`, and `uncertain effect`. A request acknowledgement,
tool return, or desired configuration is not state read-back. For a partial or
uncertain effect, stop dependent transitions, preserve affected identity,
contain when required, and follow the recovery path. Retry only under proved
idempotency or deduplication, or after reconciliation establishes that a new
attempt is safe.

## Monitor field behavior

Before a production-readiness, ramp, or scale decision depends on service
behavior, recover owner-confirmed service objectives: user-visible scope and
cohort, indicator, target or budget and window, measurement route, and degraded
or fallback response. Select only material availability, latency, freshness,
correctness or quality, capacity, and cost objectives. A provider SLA or
component uptime is dependency evidence, not proof of the end-to-end service
objective. When an objective or measurement route is missing, block only the
dependent readiness, ramp, or scale decision and continue safe observation.

Correlate secure internal telemetry with release/artifact identity, Purpose
Lock, config and data-contract versions, and rollout cohort. Select applicable:

- availability, errors, timeouts, queue depth, throughput, latency, memory,
  energy, and cost;
- schema, missingness, range, category, freshness, and transformation health;
- training-inference skew, prediction distribution, confidence, and model age;
- load-bearing dependency version or contract state, semantic-health signals,
  and active failure or fallback state;
- mature outcome quality, calibration, and error slices;
- product, scientific, safety, or business guardrails; and
- feedback, appeal, override, security/abuse, compliance, and wider impacts.

For delayed or revised outcomes, monitor arrival completeness and revisions,
declare the maturity-eligible cohort/window, and evaluate quality only on
mature evidence. Until then, report quality as `unknown`; proxy signals are
guardrails, not proof.

Give every actionable alert an owner, triage condition, evidence pointer, and
recovery playbook. Treat drift as diagnostic evidence, not proof of degradation
or attack.

Evaluate consequential service signals against the metric, window, target or
budget, and breach action in the Delivery Contract. Dashboard existence and
single-point observations are not service-objective evidence.

When staleness can invalidate use, define age from the freshness-bearing source
for that failure mode—such as the training-data cutoff, evidence cutoff, or last
accepted learned-state epoch with qualified new evidence—the maximum permitted
age by operating context, its measurement source and owner, and the safe
stop/degrade/fallback action. Packaging, rebuild, or acceptance alone does not
reset data or evidence age. Exceeding the limit may trigger that action or
create a refresh candidate; it never authorizes promotion.

## Refresh and adaptation

Manual requests, schedules, qualified new data, verified degradation, contract
or policy changes, and implementation changes may create a candidate. They
never authorize validation, staging, or activation. Re-enter all applicable
data, evaluation, security, promotion, and rollout gates.

Keep feedback and observed outcomes separate from trusted training labels until
provenance, consent, exposure, selection, intervention, attribution, maturity,
and label quality are checked.

For bounded in-place adaptation or online learning, bind each learned-state
epoch to:

- base release and Purpose Lock;
- update policy, permitted adaptation envelope, and update window/data;
- checkpoint and active-state identity;
- evaluation isolation and current evidence;
- field telemetry and safe-stop condition; and
- rollback state and compatibility.

If the project lacks a candidate/promotion mechanism or safe rollback for live
learned state, freeze adaptation and return that specialized branch incomplete.
Do not treat every event as a fully promoted release or let mutable state evade
release identity.

## Contain and recover

During an authorized incident response:

1. Bound harm and affected traffic, data, outputs, consumers, and time window.
2. Restore a stable state through the approved stop, isolation, fallback,
   traffic control, rollback, compensation, or replay path.
3. Preserve evidence and communication needs.
4. Reconcile stateful or externally consumed outputs.
5. Trace the cause across data, policy, configuration, code, model, serving,
   consumers, and feedback.
6. Add a regression, invariant, monitor, runbook correction, or accepted-debt
   record at the owning seam.

Before declaring recovery complete, read back the active release or artifact,
configuration and contract versions, learned or persistent state, and
affected-output reconciliation. Then exercise the representative real
caller/consumer path when safe and authorized. Scope the restored claim to what
that read-back and exercise establish. Re-evaluate the initiating incident
signal and each affected service objective or guardrail over its eligible
window; otherwise close only as degraded or partial and name the remaining
condition.

For committed batch or stream outputs, a bounded partition limits blast radius
but is not inherently reversible. Require affected-output identity plus
idempotent replay, compensation, or reconciliation ownership before ramp.

## Retire safely

Use this order:

1. Obtain retirement authorization from the named service and lifecycle
   owners before changing promotion, traffic, schedules, consumers, or
   resources.
2. Block new promotion and refresh into the retiring path.
3. Inventory and migrate downstream consumers; verify the replacement or
   approved removal.
4. Drain and stop traffic, schedules, event subscriptions, and adaptive
   updates.
5. Mark artifacts non-promotable and retire resources and alerts.
6. Obtain any separately required deletion authorization, then apply
   retention/deletion and notification policy.
7. Preserve required lineage, approval, and read-back evidence.

Do not delete data or stop service merely because a retirement checklist exists.
