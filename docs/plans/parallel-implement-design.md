# Parallel Implement Design Note

Status: design rationale only. `skills/custom/parallel-implement/SKILL.md`
and references own execution.

## Rationale

Run an adaptive implementation loop: live orchestrator control plane,
fresh-context one-commit workers in isolated worktrees, and one serial
integration lane. Context isolation and checkout isolation are separate gates.

The orchestrator lands a finite single wave. A hot integrator exists only when
landing can overlap worker execution or unlock the next frontier; a late
integrator may assemble a completed wave when fresh integration context pays.

The design optimizes throughput without parallel merges: workers produce
serializable commits, a repo-owned landing harness handles deterministic work
when available, and the assigned integration lane closes validation and returns
a review-ready packet. The orchestrator is the sole dispatcher and invokes
formal review after lane agents are idle.

The default delegated lane pairs one root-created detached Git worktree with one
fresh-context internal worker. Codex App-managed worktree tasks are an explicit
background-task branch, not a competing default.
