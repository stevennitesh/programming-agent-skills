# Astra skills pack design brief

Current direction, reconciled 2026-09-07. The pack is built primarily for
**GPT 6 Astra**, with **GPT 5.6 Sol compatibility**. This document owns design
rationale and composition for `skills/astra/`; individual skills own execution.
[Issue #94](https://github.com/stevennitesh/programming-agent-skills/issues/94)
preserves the original proposal. Subsequent accepted decisions below replace its
pilot sequence and candidate inventory, without claiming its evaluation goals met.

## Purpose and philosophy

Improve coding beyond a capable agent's baseline through useful engineering
judgment and project context. Ordinary coding stays direct: understand the request
and real callers, choose a sound design, implement, run the nearest useful check,
inspect the result, and remove displaced code. No default skill pipeline is needed.

> Explore imaginatively. Converge under proof. Simplify ruthlessly.

Use Matt Pocock's recognizable skill shape, useful engineering judgment from
pstack, and selected methods from Ponytail, Superpowers, and this repository.
Upstream packages are evidence, not bundles to combine or synchronization contracts.
The [README](../../README.md) is the introduction and current skill inventory;
this brief explains why the pieces fit together.

## What earns a place

Keep an instruction when it improves a likely decision or prevents a credible
failure. Put it at the owner of that decision; use code or existing tools for
mechanical work. Put substantial conditional detail behind a clear trigger and
pointer. A few natural actions and a recognizable outcome are useful shapes,
not a word-count or step-count target.

Shared coding judgment belongs in the engineering contract. Do not duplicate it
across skills or make ordinary coding require tickets, TDD, full suites, reviewers,
subagents, or process artifacts. Preserve concrete protections for authority,
concurrent writers, partial effects, recovery, fixed review candidates, and evidence.
An explicitly selected workflow can impose stronger requirements within its scope.

## Composition and ownership

| Decision or responsibility | Current owner |
| --- | --- |
| Local commands, facts, conditional pointers | Repository `AGENTS.md`, `CONTEXT.md`, and `docs/agents/` |
| Engineering judgment during coding | [Repository engineering contract](../agents/engineering-contract.md), adapted from the [bootstrap seed](../../skills/astra/repo-bootstrap/templates/engineering-contract.md) |
| Setup and reconciliation of agent guidance | [Repo bootstrap](../../skills/astra/repo-bootstrap/SKILL.md); [writing for agents](../../skills/astra/writing-for-agents/SKILL.md) owns instruction authoring |
| Feature behavior, substantial approach decisions, and domain meaning | [Shape work](../../skills/astra/shape-work/SKILL.md), including its conditional domain path |
| Unsettled integration design or empirical feasibility | [Codebase design](../../skills/astra/codebase-design/SKILL.md) and [prototype](../../skills/astra/prototype/SKILL.md) |
| Delivery decomposition and tracker publication | [To tickets](../../skills/astra/to-tickets/SKILL.md), using repository tracker guidance and an accepted source |
| Model allocation and execution authority | [Cost-aware coding](../../skills/astra/cost-aware-coding/SKILL.md), only when requested |
| Concurrent implementation scheduling, custody, and integration | [Parallel implement](../../skills/astra/parallel-implement/SKILL.md), only when requested |
| Candidate correctness and maintainability assessment | [Change review](../../skills/astra/change-review/SKILL.md); high assurance is separately requested |
| Architecture-wide improvement, hard bugs, or measured optimization | [Audit codebase](../../skills/astra/audit-codebase/SKILL.md), [diagnosing bugs](../../skills/astra/diagnosing-bugs/SKILL.md), and [hillclimb](../../skills/astra/hillclimb/SKILL.md) |
| Evidence gathering, context upkeep, and guided procedures | [Research](../../skills/astra/research/SKILL.md), [context hygiene](../../skills/astra/context-hygiene/SKILL.md), and [wizard](../../skills/astra/wizard/SKILL.md) |
| Active Git conflicts | [Resolving merge conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) |

The managed pack currently contains 16 skills. Their metadata owns invocation
behavior; the README lists explicit-only workflows. Continuation handoffs belong
to writing-for-agents, with execution-specific state added by the relevant workflow.
There is no standalone implement skill. Implementers use repository guidance and
the engineering contract directly.

A feature can be shaped and implemented without tickets. Tickets become useful
when delivery needs tracked units; they do not authorize concurrent writers.
Parallel implementation requires independent ownership and integration proof.
Specialists can also work sequentially without activating parallel delivery.
Skills remain usable individually; cost-aware coding is not an umbrella requirement.

## Why cost-aware coding has stronger gates

Cost-aware coding is an explicit experimental workflow, compatible with a Sol
Medium or Astra Medium root. It separates an accepted coordination plan from
execution. Feature shaping and implementation planning remain with shape-work;
the coordination proposal selects actors, responsibilities, dependencies, checks,
and permitted recovery. Reuse accepted decisions instead of creating competing plans.

The root may implement with bounded sequential specialist help or concentrate on
coordination. It can adapt assignments and scheduling within accepted boundaries;
changes outside those boundaries need acceptance. Root model changes are presented
to the user, not accomplished by instructions declaring a different model.

Feature delivery in this workflow requires delegated independent Astra review,
even when the root is Astra and did not implement. This is a chosen assurance
requirement within which cost is optimized, not a rule for all ordinary coding.
Repair accounting distinguishes work-unit implementation recovery from shared
integrated-candidate review rounds. The skill and its references own exact limits,
role permissions, custody, and acceptance semantics; do not duplicate them here.

When combined, parallel-implement owns concurrency mechanics while cost-aware
coding retains routing authority, accepted responsibility boundaries, and repair
and review constraints. Helpers handle deterministic work such as lane management,
report generation, installation, and bounded metadata extraction. They do not
replace judgment or turn logged counters into proven task costs or savings.

## Installation and migration

`skills/astra/` is the managed source. `skills/custom/` is historical source retained
for comparison and users evaluating the more detailed pack; it is not deployed by
the current installer. Smaller models may need those additional instructions;
compatibility is not evidence of equivalent behavior across models.

Repo bootstrap adapts the engineering contract and offers reconciliation of
existing agent guidance, preserving local meaning while replacing obsolete pack
routes. New repositories receive tracker, label, and domain defaults without
forcing ticketed work. The resulting contract is repository-owned, not a mirror
that must match its seed forever.

Follow [installation and recovery](../../INSTALLATION.md) for managed-copy ownership
and updates. Editing source does not install it. Global preferences and external
repositories require their own authorized updates. Migrate changed skills, callers,
references, and validation together; retain history as evidence, not an active
compatibility route. Legacy composition epochs and Deploy Campaigns apply only to
selected legacy work, not as prerequisites for Astra changes.

## Evidence, history, and next evaluation

Issue #94 proposed an implement-first pilot. The work instead began with authoring
and bootstrap, then evaluated implement; the limited comparisons did not establish
an advantage sufficient to retain that skill. The original four-skill proposal
and legacy inventory are historical inputs, not today's implementation backlog.

Package validation and focused tests establish specific helper and structural
behavior. Reviews and editorial reconciliation do not establish better generated
code, lower total cost, or equivalent quality across models. Model assignments
remain hypotheses requiring workload-specific calibration.

Use actual runs to evaluate unnecessary spawns, context transfers, approval turns,
repair attempts, ownership disagreements, and elapsed time alongside correctness
and maintainability. Include failures and compare equivalent accepted outcomes;
logged telemetry alone does not prove savings. Do not restart a broad rewrite
without a concrete behavioral gap.

For deeper evidence, consult the [initial assessment](../research/gpt-6-astra-skill-pack-assessment-2026-09-05.md)
and [contract assessment](../research/astra-engineering-contract-2026-09-05.md) as
historical snapshots. The [documentation status](documentation-status.md) identifies
other stale surfaces and retention decisions; the [ADR index](../adr/README.md)
distinguishes legacy decisions from current execution owners.
