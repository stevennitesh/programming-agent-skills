# Engineering Contract

Discover broadly. Converge under proof.

## Shared Engineering Language

This contract owns shared runtime engineering language and cross-cutting coding discipline. Domain docs own product language. `AGENTS.md` owns repo commands and pointers. Skills own procedures and local contract slices.

Follow `docs/agents/domain.md` to the relevant glossary and ADRs. Preserve accepted domain terms and decisions across specs, issues, code, tests, and docs.

- **Source trace:** the request, issue or spec, repo instructions, domain decisions, current behavior and constraints, relevant code and tests, and fixed point that govern the slice.
- **Bounded slice:** the smallest useful scope that preserves the commitment boundary and can produce evidence.
- **Commitment boundary:** product intent, acceptance criteria, semantic correctness, user-visible behavior, public contracts, data semantics, security/privacy posture, and agreed scope. Technique stays agent-owned.
- **Load-bearing internal:** internal behavior that determines semantic correctness and therefore needs a contract and proof.
- **Semantic correctness:** correctness of the result's meaning, not merely the existence of output.
- **Semantic proof:** evidence that establishes semantic correctness through an observable seam.
- **Proof seam:** the caller-facing interface or observable boundary through which semantic correctness can be established.
- **Proof lane:** the named repo-owned command, fixture, workflow, or artifact that will exercise a proof seam for one work item.
- **Evidence:** inspectable support for a claim: source, tests, fixtures, logs, diffs, commands, CI, screenshots, rendered output, or user confirmation.
- **Tracer bullet:** one narrow, observable path through the real system.
- **Fixed point:** the pinned baseline for review.
- **Review snapshot:** the immutable tree or captured target compared with a fixed point.
- **Spec / Standards:** originating intent and semantic commitments / documented repo conventions and maintainability; review the axes separately.
- **Residual risk:** uncertainty or skipped proof that remains after validation.
- **Disposable / durable:** `.tmp/` holds disposable local work; `.scratch/` holds durable, version-controlled local state.
- **Lock:** reconciliation and evidence at the authorized completion boundary.

## Repo-Owned Commands

Run canonical setup and validation commands from `AGENTS.md` and their named config.

Repair command drift by tracing repo config, CI, or maintained contributor docs; update the primer through the repo's normal approval boundary.

For review, a caller-supplied fixed point wins. Otherwise discover the repository default branch and merge base, state the resolved baseline, and ask only when discovery is ambiguous.

## Tight Convergence Loop

Scale one tight loop to risk:

```text
Orient -> Explore -> Decide -> Prove -> Cover -> Converge -> Simplify -> Lock
```

- **Orient:** build the source trace; pin the fixed point, commitments, and bounded slice.
- **Explore:** inspect real seams and keep probes disposable.
- **Decide:** choose the best local approach inside the commitment boundary.
- **Prove:** establish semantic proof through the smallest meaningful seam; capture red before green when TDD applies.
- **Cover:** close remaining requirements with tracer bullets or focused checks.
- **Converge:** review Spec and Standards separately from the fixed point.
- **Simplify:** remove scaffolding, collapse bloated branches, and add or deepen an abstraction only when it improves correctness, locality, testability, or maintainability; keep proof green.
- **Lock:** run canonical checks, reconcile work state, record evidence and residual risk, and stop at the authorized boundary.

For tiny edits, compress the loop to Orient -> Prove -> Lock. Keep every gate for uncertain, risky, user-facing, multi-file, or architecture-touching work.

## Commitment Boundary

Choose implementation technique freely inside the bounded slice while commitments and semantic proof hold.

Stop for a user decision when a better approach changes a commitment.

Stay inside the authorized filesystem, Git, tracker, and external-mutation boundary. Lock the authorized state and hand off anything beyond it.

## Semantic Proof

Claims need evidence. Prove semantic correctness, not output existence.

When behavior is clear enough and the repo has a useful test seam, capture red before green; after-the-fact checks supplement that evidence.

For docs, config, exploration, or behavior-preserving work, use the strongest practical evidence.

Treat a runnable prototype as a question answered, not production proof. Expose each load-bearing internal through the smallest meaningful seam.

Examples:

- Data filtering needs fixtures that prove included, excluded, and edge rows.
- Transformations need known input/output examples and invariants.
- Ranking needs explainable examples, thresholds, or relative-order checks.
- Migrations need before/after counts, constraints, checksums, and sample records.

## Tracer Bullets

Prefer tracer-bullet vertical slices over horizontal slices.

Support work earns its place only when it directly unblocks or de-risks a tracer bullet and has observable proof.

## Work State

Explore with disposable `.tmp/` spikes, copied references, experiments, and rough notes.

Store durable, version-controlled local work state in `.scratch/`. A Local Markdown tracker is one such use.

A **staged worker** returns one bounded staged patch and proof to an owner. A **lane worker** returns one bounded commit from an isolated worktree. Neither owns integration, formal review, tracker closeout, or push.

Change production files after Decide. Use a tiny reversible production edit during Explore only when it is the shortest probe of the real seam.

At Lock, delete each disposable `.tmp/` path or name the path intentionally preserved for the user or next session. Preserve in-scope `.scratch/` state through cleanup; include it in review and in staging when staging is in scope.

## Lock

Lock only when:

- canonical checks ran or every skipped check has a reason;
- each nontrivial diff was reviewed from its fixed point against Spec and Standards separately;
- every `.tmp/` path was deleted or intentionally preserved;
- in-scope `.scratch/` state entered review and, when authorized, staging;
- current Git state, evidence, residual risk, and out-of-slice follow-ups were recorded;
- the authorized mutation boundary was respected and remaining work was handed off.
