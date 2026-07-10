# Parallel Implement Design Note

Status: design rationale only. `skills/custom/parallel-implement/SKILL.md`
and references own execution.

## Rationale

Run an adaptive implementation loop: live orchestrator control plane,
isolated one-commit workers, and one serial integration lane.

The orchestrator lands a finite single wave. A hot integrator exists only when
landing can overlap worker execution or unlock the next frontier; a late
integrator may assemble a completed wave when fresh integration context pays.

The design optimizes throughput without parallel merges: workers produce
serializable commits, a repo-owned landing harness handles deterministic work
when available, and the assigned integration lane closes validation and review.
