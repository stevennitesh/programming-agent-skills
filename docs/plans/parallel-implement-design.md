# Parallel Implement Design Note

Status: design rationale only. `skills/current/parallel-implement/SKILL.md`
and references own execution.

## Rationale

Run a three-lane implementation loop: live orchestrator control plane,
isolated issue workers, and one persistent serial integrator.

The design optimizes for throughput without parallel merges: workers produce
commits independently; the integrator lands serially; the orchestrator keeps the
ready frontier moving.
