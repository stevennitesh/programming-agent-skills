# Engineering Contract

Explore imaginatively. Converge under proof. Simplify ruthlessly.

Be adventurous in discovery, conservative in claims, and exacting at Lock.

This contract owns engineering taste, shared runtime language, and cross-cutting discipline. `AGENTS.md` owns repo commands and pointers. Domain docs own product language and decisions. Skills own procedures and local contract slices.

Follow `docs/agents/domain.md` to the relevant glossary and ADRs. Preserve accepted terms and decisions across specs, issues, code, tests, and docs.

## Shared Engineering Language

- **Source trace:** the governing request or spec, repo instructions, domain decisions, baseline, constraints, code, and tests.
- **Bounded slice:** the smallest useful scope that preserves commitments and can produce evidence.
- **Commitment boundary:** product intent, acceptance criteria, user-visible behavior, public and data contracts, security/privacy posture, and agreed scope. Technique stays agent-owned.
- **Load-bearing internal:** internal behavior that determines semantic correctness and therefore needs a contract and proof.
- **Semantic correctness:** correctness of meaning, not output existence.
- **Semantic proof:** evidence of semantic correctness through an observable seam.
- **Proof seam:** the caller-facing interface or observable boundary where meaning can be established.
- **Proof lane:** the repo-owned command, fixture, workflow, or artifact that exercises one proof seam.
- **Evidence:** inspectable support for a claim.
- **Tracer bullet:** one narrow, observable path through the real system.
- **Fixed point:** the pinned review baseline.
- **Review snapshot:** the immutable tree or captured target compared with a fixed point.
- **Spec / Standards:** originating commitments / repo conventions and maintainability. Review them separately.
- **Residual risk:** uncertainty or skipped proof remaining after validation.
- **Disposable / durable:** `.tmp/` holds disposable work; `.scratch/` holds durable, version-controlled local state.
- **Lock:** reconciliation and evidence at the authorized completion boundary.

## Engineering Taste

- **Imagination before commitment.** Do not confuse the first workable idea with the best local design. When uncertainty matters, inspect alternatives, invert assumptions, and use experiments to discover what the code can teach.
- **Experiments over speculation.** Prefer a disposable spike, tracer bullet, or runnable prototype to extended guesswork. Keep experiments cheap enough to discard and real enough to change the decision.
- **Semantic proof over plausible output.** Prove that the result means the right thing through an observable seam. Treat plans, summaries, memory, and confident narration as maps, not proof.
- **Deep simplicity.** Prefer locality, small caller-facing surfaces, and complexity hidden behind clear ownership. Add or deepen an abstraction only when the proved system becomes easier to change, test, or reason about.
- **Stewardship.** Preserve unrelated work and accepted language. Leave the selected slice more coherent than you found it without laundering adjacent cleanup into scope.

## Tight Engineering Spine

```text
Explore -> Choose -> Prove -> Expand -> Simplify -> Lock
```

- **Explore:** build the Source Trace; pin the fixed point, commitments, and bounded slice; inspect real seams and generate credible alternatives. Keep probes disposable. Touch production during Explore only for the smallest reversible probe inside the authorized boundary.
- **Choose:** select the strongest local approach and one tracer bullet. Choose technique freely inside the bounded slice. Stop for a user decision when a better approach changes a commitment. Stay inside authorized filesystem, Git, tracker, deployment, and external-mutation boundaries.
- **Prove:** establish semantic proof through the smallest meaningful seam. Observe RED before GREEN when behavior and a useful test seam are known. Treat prototypes as design evidence, not production proof.
- **Expand:** after the tracer bullet works, cover the remaining requirements, edge cases, failure modes, and integrations. Reconsider the design with what the proof revealed. Expand evidence and coverage, not unauthorized scope.
- **Simplify:** remove scaffolding, collapse accidental complexity, sharpen names and boundaries, and deepen abstractions only when correctness, locality, testability, or maintainability improves. Keep proof green.
- **Lock:** run canonical repo checks, reconcile work state, review Spec and Standards separately, record evidence and residual risk, and stop at the authorized boundary.

Tiny work may compress to `Explore -> Prove -> Lock`; uncertain, risky, user-facing, multi-file, data, security, or architecture work uses the full spine. Compress steps, not gates.

## Proof Discipline

Claims need evidence. Expose every load-bearing internal through the smallest meaningful seam.

Treat repo config, CI, and maintained contributor docs as command authority. When `AGENTS.md` commands drift, surface the mismatch and update the primer through its normal approval boundary.

Match proof to meaning: filtering needs included, excluded, and edge fixtures; transformations need known inputs, outputs, and invariants; ordering needs thresholds or relative order; persistence needs before/after evidence and constraints.

Support work earns its place only when it directly unblocks or de-risks a tracer bullet and has observable proof.

For review, a caller-supplied fixed point wins. Otherwise discover the default branch and merge base, state the resolved baseline, and ask only when discovery is ambiguous.

## Work State And Workers

Production changes begin after Choose, except for the authorized Explore probe above.

A **staged worker** returns one bounded staged patch and focused proof to an owner. A **lane worker** returns one bounded commit and proof from an isolated worktree. Neither owns integration, formal review, tracker closeout, or push.

## Lock

Lock only when:

- canonical checks ran or every skip has a reason;
- each nontrivial diff passed separate Spec and Standards review from its fixed point;
- every `.tmp/` path was deleted or intentionally preserved;
- in-scope `.scratch/` state entered review and, when authorized, staging;
- current Git state, evidence, residual risk, and out-of-slice follow-ups were recorded;
- the mutation boundary held and remaining work was handed off.
