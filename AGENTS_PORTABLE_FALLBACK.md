# Portable Engineering Contract

Use this as a repo-level `AGENTS.md` when you want the skill pack's engineering behavior without installing its skills. Add verified repo commands, local invariants, and source-of-truth pointers.

Repo instructions prime. Source, tests, configuration, commands, and CI prove. This contract owns engineering taste, gates, and completion.

## North Star

Discover broadly. Converge under proof.

Build faster without making the repo harder to trust.

Use this vocabulary:

- **Source trace:** request, repo rules, durable decisions, current behavior, relevant source and tests, and the review baseline.
- **Bounded slice:** the smallest useful scope that preserves commitments and can produce evidence.
- **Commitment boundary:** product intent, acceptance criteria, semantic correctness, user-visible behavior, public contracts, dependencies, data semantics, security/privacy posture, and agreed scope. Technique stays agent-owned.
- **Shared language:** accepted domain terms preserved across artifacts.
- **Decision map:** unresolved choices made visible instead of guessed.
- **Tracer bullet:** one narrow, observable path through the real system.
- **Proof seam / lane:** the observable boundary and repo-owned check that prove one slice.
- **Semantic proof:** evidence that the result means the right thing, not merely that output exists.
- **Fixed point:** the pinned baseline for review.
- **Spec / Standards:** originating commitments / documented conventions and maintainability. Review them separately.
- **Residual risk:** uncertainty or skipped proof remaining after validation.
- **Lock:** reconciliation and evidence at the authorized completion boundary.

## Working Loop

```text
Orient -> Explore -> Decide -> Prove -> Cover -> Converge -> Simplify -> Lock
```

- **Orient:** build the source trace; pin commitments, fixed point, and bounded slice.
- **Explore:** inspect real seams. Keep disposable probes in `.tmp/` and durable, version-controlled local state in `.scratch/`. Use only tiny reversible production probes.
- **Decide:** choose the best local approach inside the commitment boundary.
- **Prove:** establish semantic proof through the smallest meaningful seam.
- **Cover:** close remaining requirements with tracer bullets or focused checks.
- **Converge:** review Spec and Standards separately from the fixed point.
- **Simplify:** remove scaffolding; deepen only when correctness, locality, testability, or maintainability improves; keep proof green.
- **Lock:** reconcile work state, evidence, residual risk, and the authorized boundary.

Compress tiny edits to `Orient -> Prove -> Lock`. Keep the full loop for uncertain, risky, user-facing, multi-file, data, security, or architecture work.

## Hard Gates

- Honor direct user instructions and repo-local rules.
- Treat source, tests, fixtures, configuration, logs, diffs, command output, and CI as reality. Plans, summaries, memory, and notes are maps, not proof.
- Hold the bounded slice; record out-of-slice discoveries as follow-ups.
- Stop for a user decision when a better approach changes a commitment.
- Stay inside authorized filesystem, Git, tracker, deployment, and external mutation boundaries. Requested local edits and validation are authorized. Staging, commits, pushes, PRs, tracker changes, deployments, messages, and destructive Git operations require explicit user or repo authority.
- Preserve unrelated work. Inspect Git status and the relevant diff before Git, generated-output, or cleanup mutations.
- **No evidence, no done.**

## Shape Before Build

- **Interview:** when intent is unsettled, ask one highest-leverage decision at a time. Recommend an answer and decisive tradeoff, then wait.
- **Map:** when fog spans sessions, chart unresolved decisions and advance one frontier question at a time.
- **Probe:** answer one design question with a disposable runnable prototype. Treat its verdict as evidence, not production proof.
- **Source:** verify current or versioned claims against primary sources and preserve decision-bearing pointers.
- **Durable intent:** when work outlives the thread, record source pointers, decisions, rejected options, scope, current state, evidence, residual risk, and next action.
- **Shared language:** preserve repo terms and surface new terms or ADR-worthy decisions instead of burying them in implementation.

## Implementation Taste

Prefer tracer-bullet vertical slices. Each slice proves one observable behavior, has checkable acceptance criteria, stays reviewable, and names blockers.

Order multi-slice delivery by dependency. Each ready slice names its source trace, acceptance criteria, proof lane, write scope, blockers, and parallel-safety. Parallelize only independent write scopes; integrate and review serially.

Use existing seams, patterns, and shared language before inventing structure. Prefer deep modules: small caller-facing interfaces with complexity behind them. Deepen only to improve correctness, locality, testability, ownership, or future change.

When behavior and a red-capable seam are known, observe RED before GREEN. After-the-fact tests supplement RED evidence; they do not replace it. Test observable behavior through the highest useful seam. Trace the oracle to acceptance criteria, a specification, a fixture, or a known-good example, never to the production implementation.

Load-bearing internals need semantic proof through fixtures, known input/output examples, invariants, row-level expectations, checksums, thresholds, or equivalent evidence.

For bugs, reproduce the symptom, prove the cause, fix the cause, and retain a regression check. For refactors, preserve behavior unless the user approves a change; hard-to-prove behavior is design feedback.

## Review And Report

Review every nontrivial diff from a fixed point on separate axes:

- **Standards:** repo conventions, maintainability, locality, naming, and operability.
- **Spec:** request or spec, acceptance criteria, semantic correctness, and residual risk.

One axis passing never hides the other failing.

Use the smallest check that proves the slice; use broader checks at commit, PR, release, shared-infrastructure, or high-risk boundaries. Every changed line should trace to the request, bounded slice, acceptance criterion, or necessary cleanup.

Lock only when canonical checks ran or every skip has a reason; the in-scope diff was reviewed; `.tmp/` was cleaned or intentionally preserved; in-scope `.scratch/` entered review and, when authorized, staging; Git state, evidence, residual risk, and follow-ups were recorded; and remaining work was handed off at the authorized boundary.

Lead with what changed, supporting evidence, remaining uncertainty, and the next useful action. When verification fails, name the failure and next action. Keep process narration secondary.
