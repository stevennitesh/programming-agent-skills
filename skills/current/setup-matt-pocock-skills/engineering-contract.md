# Engineering Contract

Good agentic coding is fast discovery plus disciplined convergence.

Give the agent room to discover, then force it to converge.

## Language Shapes Behavior

The words in this repo are not decoration. They steer how agents plan, code, test, review, and report work.

Use the repo's shared language. Preserve domain terms from `CONTEXT.md`, ADRs, specs, issues, and source code.

## Convergence Loop

Use this rhythm scaled to task size:

```text
Orient -> Explore -> Choose -> Prove -> Expand -> Converge -> Simplify -> Lock
```

- **Orient**: name product intent, current behavior, constraints, acceptance criteria, fixed point, and what must be preserved.
- **Explore**: inspect seams, compare local approaches, and use `.tmp/` for disposable spikes when useful.
- **Choose**: pick the best local approach inside the bounded slice.
- **Prove**: prove semantic correctness; use red-green-refactor when appropriate.
- **Expand**: add remaining requirements as bounded tracer bullets or focused checks.
- **Converge**: review against Spec and Standards from the fixed point.
- **Simplify**: remove scaffolding, collapse bloated branches, deepen modules where it helps, and preserve behavior.
- **Lock**: rerun the right checks, delete scratch artifacts unless asked to preserve them, record evidence, commit or hand off.

Compress this loop for tiny edits. Make the gates explicit for uncertain, risky, multi-file, user-facing, or architecture-touching work.

## Autonomy And Commitment

Technique belongs to the agent. Commitments belong to the user.

The commitments are product intent, acceptance criteria, semantic correctness, user-visible behavior, public contracts, data semantics, security/privacy posture, and the bounded slice.

The agent may choose any implementation approach inside the bounded slice when it preserves those commitments and can prove the result.

Stop and ask when the better approach changes a commitment.

## Load-Bearing Internals

Internals are not automatically irrelevant.

If internal behavior determines whether the requested result is correct, it is load-bearing. Give it a contract and prove it through the smallest meaningful seam.

Do not treat output existence as correctness.

Examples:

- Data filtering needs fixtures that prove included, excluded, and edge rows.
- Transformations need known input/output examples and invariants.
- Ranking needs explainable examples, thresholds, or relative-order checks.
- Migrations need before/after counts, constraints, checksums, and sample records.

## Proof

Claims need evidence.

For code behavior, use red-green-refactor when the behavior is clear enough and the repo has a useful seam.

For docs, config, exploration, or behavior-preserving work, use the strongest practical evidence: commands, typechecks, screenshots, logs, fixtures, rendered output, diff inspection, or user confirmation.

Never replace TDD discipline with after-the-fact checks when a code slice is suitable for TDD.

## Slicing

Prefer tracer-bullet vertical slices over horizontal slices.

A tracer bullet proves one observable behavior through the real system and reduces uncertainty about behavior, a seam, or a risk.

Support work is allowed when it clearly unblocks or de-risks tracer bullets and has observable validation.

## Exploration

Use `.tmp/` for disposable spikes, copied references, experiments, and rough notes.

Production files should normally change after Choose. Tiny reversible production edits during Explore are acceptable only when they are the fastest way to understand the real seam.

Delete scratch artifacts before final delivery unless the user asks to preserve them.

## Review And Lock

For nontrivial work, review from a fixed point:

- **Standards**: documented repo conventions and maintainability expectations.
- **Spec**: originating issue, PRD, user request, acceptance criteria, and semantic correctness.

Lock with evidence: checks run, skipped checks, residual risk, commit or handoff, and follow-ups that do not belong in the slice.

## What Not To Do

- Do not expand the mission while exploring.
- Do not mistake a runnable prototype for semantic proof.
- Do not hide correctness-critical logic behind "implementation detail."
- Do not add abstractions unless they improve correctness, locality, testability, or maintainability.
- Do not leave `.tmp` scratch behind unless asked.
- Do not claim done without evidence.
