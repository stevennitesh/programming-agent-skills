# Engineering Contract

<!-- programming-agent-skills setup-file: engineering-contract.md:5be3c0494dfb -->

Explore imaginatively. Converge under proof. Simplify ruthlessly.

This document states shared engineering defaults and condition-triggered
methods. It is not a workflow, checklist, review gate, completion contract, or
authority to mutate files, Git state, trackers, deployments, or external
systems.

Repository instructions own local commands and boundaries. Domain records own
product meaning and settled decisions. Skills own procedures, checks, stopping
conditions, and outputs. No generic rule overrides an explicit request,
accepted product commitment, or repository contract.

- **Must** marks a correctness, safety, integrity, or honesty floor.
- **Prefer** marks the default engineering choice. Deviate for a supported
  reason; obtain authority only when the deviation changes a commitment.
- **Method** names a practice activated by its stated condition. The responsible
  task or skill owns its procedure and evidence. An inactive method creates no
  checklist, artifact, reviewer, `N/A`, or explanation obligation.

Shared terms:

- **Traceability** is the inspectable chain from request, rules, decisions, and
  current source through behavior and real callers to evidence.
- A **bounded slice** is the smallest useful scope that preserves commitments
  and can produce meaningful evidence.
- The **commitment boundary** is accepted product intent, behavior, public and
  data contracts, compatibility, security and privacy posture, and agreed
  scope. Technique remains agent-owned until it changes a commitment.

## Correctness And Evidence — Must

- Preserve the explicit request, accepted behavior, applicable context-scoped
  Ubiquitous Language, preconditions, postconditions, invariants, contracts,
  and unrelated work. Give every decision-bearing term, threshold, unit, or
  equivalence an operational definition or authoritative owner. Surface
  ambiguity instead of inventing meaning.

- Preserve correct behavior over relevant inputs, states, lifecycle
  transitions, failures, supported environments, applicable accessibility
  semantics, and observable effects. Address the causal owner across affected
  callers instead of masking one symptom. Preserve atomicity, recovery, retry,
  idempotency, compatibility, cancellation, concurrency, and observability only
  where the supported contract exposes them.

- At a changed trust or data boundary, validate machine-consumed,
  action-driving input against its functional contract at the boundary that
  owns it. Validate accepted input once at that boundary. Use a typed internal
  representation when it prevents invalid states or repeated validation.
  Preserve applicable data meaning, identity, integrity, provenance, schema,
  units, ordering, and lifecycle. Do not weaken accepted authorization,
  privacy, confidentiality, encoding, secret-handling, or external-effect
  guarantees. Preserving touched guarantees is ordinary correctness; it does
  not authorize a security program.

- Match proof to the claim. Run the smallest discriminating check at the real
  caller or closest observable boundary. A **Proof Seam** is that caller-facing
  boundary, not the test that exercises it; name the concrete test, fixture,
  check, workflow, or artifact used. When a behavioral claim could self-confirm,
  use an oracle independent of the implementation logic; it need not be a
  separate reviewer. Prefer state verification; use behavior verification only
  when the interaction is itself
  a responsibility or is needed for failure isolation. Structural checks,
  mocks, generated artifacts, and narration do not prove live behavior. Label
  the strongest safe substitute as a proxy.

- Complete **Change Closure**: remove paths made obsolete, redundant, or
  contradictory by the change, or retain them only for a supported obligation
  with named callers, owner, reason, evidence, selection or cutover behavior,
  and removal condition. Report material skipped proof and **Residual Risk**,
  meaning uncertainty that limits the claim.

## Design Defaults — Prefer

- Trace the current behavior owner and real callers. Change the smallest
  repository-native path through them that minimizes total caller, maintainer,
  migration, operational, coordination, and proof burden. Do not create an
  orphan component, speculative layer, or parallel `V2` path. Replace or
  relocate ownership only when direct evidence shows that ownership is the
  material problem and one bounded migration can close the displaced path.

- Preserve conceptual integrity and essential complexity while removing
  demonstrated accidental complexity. Use information hiding and deep modules
  to contain change. Avoid shallow modules and pass-through methods whose
  interface burden approaches their useful behavior.

- Make interfaces easy to use correctly and hard to misuse. Prefer clear names,
  explicit data relationships, local ownership, readable control flow, and
  representations that define errors out of existence where accepted behavior
  permits.

- Start with repository conventions, owned abstractions, native facilities,
  and established dependencies. Novelty is neither a goal nor a defect. Add an
  abstraction, dependency, adapter, cache, concurrency mechanism, or
  configurability only for supported variation or demonstrated material value.

- Apply DRY to knowledge and policy, not repeated syntax. Apply yagni to
  speculative capability. Prefer bounded duplication to the wrong abstraction
  when meanings, owners, change rates, or failure modes differ. Refactoring
  preserves observable behavior; prove intentional behavior changes separately.

Use change amplification, cognitive load, unknown unknowns, deep or shallow
module, information hiding, essential or accidental complexity, and conceptual
integrity only when they sharpen a design judgment. They are diagnostics, not
scorecards or Return fields.

## Methods When The Condition Applies

### Reason Across State And Lifecycle Boundaries

When requested behavior materially depends on reachable state, persistence,
projection, ordering, retry, resume, cancellation, concurrency, or lifecycle
transitions, distinguish the supported states, access paths, and transitions
that can change meaning. Cover distinct behavior and material interactions, not
a blind Cartesian product.

### Use A Negative Control

When a validator, hook, policy check, dependency rule, or other enforcement
boundary changes, show that a representative controlled violation fails for
the intended reason. Also show a representative conforming input. Repeat the
conforming case after failure only when mutable state, caching, hooks, or
partial mutation could contaminate it.

### Prove Durable Artifacts Proportionally

When a change creates or changes a durable or machine-consumed artifact, prove
only the properties required by its consumer and the claim: format for
consumption, identity and destination for persistence or routing, read-back
after durable or external mutation, and real-consumer behavior when integration
or publication is claimed. Structural validity alone does not prove semantics
or consumption.

### Measure Consequential Claims

When an accepted decision or claim depends on performance, capacity,
reliability, latency, cost, or resource use, measure it against a comparable
workload, environment, build, method, sample, and baseline or budget. If
meaningful measurement is unavailable, narrow the claim and report the
Residual Risk.

### Invoke Heavier Owners Only From Their Trigger

Use Codebase Design when one consequential responsibility, interface,
ownership, seam, substitution, or migration decision remains unresolved. Use
TDD only when the user explicitly requests test-first or RED-GREEN-REFACTOR, or
repository policy requires it.

Delegate only when the user explicitly requests subagents or an explicitly
invoked skill owns required fanout. Multiple files, spare capacity,
possible parallelism, or an independently ownable subtask does not activate
delegation.

Invoke independent Change Review only when the user or repository requires it;
the candidate recombines mutations from two or more independent authors; or
focused proof establishes behavior but a material shared-contract or
irreversible-migration acceptance judgment still warrants fresh independent
judgment and review is the lowest-burden way to obtain it. Missing required
proof stops the work; it is not a review trigger.

High-Assurance Review, security programs, and production/SRE work require an
explicit user or accepted-task objective. Generic risk, external input, file
type, release packaging, or production adjacency does not activate them.
Preserve any touched accepted guarantees without expanding the objective.
