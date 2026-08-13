# Risk and Exposure Branches

Read only the branches activated by observed project facts. Record the trigger,
owner, governing source, required controls, evidence, and unresolved residual
risk. Do not infer consent, legal applicability, risk tolerance, or approval.

## Sensitive or regulated data

Record owner-provided jurisdiction, sector, operator role, use context, affected
rights, data categories, organizational policy, and escalation route. Then:

- enforce purpose limitation, minimization, least privilege, protected
  transport/storage, retention/deletion, and logging constraints;
- test leakage through artifacts, examples, prompts, outputs, telemetry, and
  debugging paths; and
- use de-identification, differential privacy, or privacy auditing only when
  they address the identified threat and utility tradeoff.

If applicability is unresolved, block only the dependent data use or release
decision and escalate. Source research is evidence, not a legal verdict.

## Weakly governed or automatically recycled training inputs

Activate this branch for untrusted contributors or writers, automated
recycling, adversarial influence, or unresolved governance that can affect a
consequential claim or live state. External origin alone is not enough; ordinary
external data stays under the common provenance, permission, and limitation
contract.

- preserve origin, license/policy, consent where applicable, integrity, writer
  identity, and transformation lineage;
- define poisoning, tampering, label manipulation, and backdoor assumptions;
- restrict writers and validate anomalies and labels; and
- regression-test refreshes before promotion.

## Acquired components and executable artifacts

Activate this branch for a third-party executable artifact or a component that
crosses a material trust, update, deployment, or high-impact boundary:

- verify origin, integrity, license/policy, and compatibility;
- deepen vulnerability, malicious-content, maintenance/end-of-life, and update
  review according to the format, update path, exposure, and impact;
- preserve a component and artifact manifest when promotion, longevity, or
  material dependency risk requires it; and
- never execute untrusted or potentially tampered serialization.

Prefer a non-code-executing format when compatible. Otherwise use trusted
provenance, integrity verification, an approved isolated runtime, least
privilege, and resource controls. A hash from the same untrusted source and a
nominally safer format are not guarantees.

## Public or adversarial access

When users or adversaries control prediction inputs, queries, or model-facing
resources:

- validate inputs and resource boundaries;
- test feasible problem-space evasion, abuse, extraction, and privacy attacks;
- minimize exposed output detail;
- monitor suspicious use; and
- enforce rate, concurrency, timeout, memory, compute, and cost limits where
  abuse can affect availability or budget.

Do not require adversarial training or formal verification unless the identified
threat and evidence justify them.

## High-impact or safety-critical use

For irreversible, safety-critical, rights-affecting, or broad public use:

- obtain independent domain and risk review;
- evaluate context-relevant reliability, robustness, fairness, privacy,
  explainability, and safe-failure behavior;
- use staged exposure and stricter owner-held residual-risk acceptance;
- provide meaningful human intervention, appeal, override, or deactivation
  where the system context requires it; and
- rehearse fallback, kill, rollback, and affected-party response.

Do not hard-code fairness metrics or group lists. Derive them from affected
parties, failure costs, governing obligations, and available lawful evidence.

## Generative and tool-using capabilities

Activate controls by capability, not by the label "GenAI":

- The composed-AI branch owns behavior identity, retrieval and memory
  contracts, grader validity, tool state, human controls, injection trust-flow
  proof, and inference economics. Add only the matching exposure controls here.
- **Fine-tuning or learned adaptation:** test training-data poisoning,
  circumvention, regression, and update identity.
- **Open or externally sourced weights:** apply acquired-component and
  executable-artifact controls.

Use generative-quality evaluation appropriate to the task; do not force
classification metrics onto open-ended outputs.

## Resource-intensive systems

For expensive training or high-volume/elastic inference:

- benchmark quality with the applicable latency, throughput, memory,
  accelerator, energy, and cost ceilings;
- prove only the overload, backpressure, timeout, quota, cancellation, cleanup,
  retry, and idempotency behavior material to the system; and
- define cost and resource owners plus a safe degradation mode.

## Long-lived, shared, or cascaded systems

Deepen system-debt inspection for model and data entanglement, correction
cascades, undeclared consumers, unstable or unused features, configuration
sprawl, pipeline jungles, dead experiments, feedback loops, and propagated
upstream/downstream changes. Preserve an owner and removal condition for
accepted debt.

## Edge or intermittently connected deployment

For embedded, fleet, or offline-capable inference, define device/runtime
compatibility, constrained resources, offline behavior, stale-model limits,
secure update and rollback, fleet version visibility, failed-update recovery,
and telemetry buffering/privacy. Test the actual target class or a justified
representative environment.
