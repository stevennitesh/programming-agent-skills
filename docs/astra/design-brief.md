# Astra skills pack design brief

Current direction, reconciled 2026-09-23. The pack is built primarily for
**GPT 6 Astra**. Optional cost-aware execution routes substantial implementation
to GPT 6 Sol and compact bounded work to GPT 6 Luna. This document owns design
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

Shared coding judgment belongs at one repository owner: inline for brief guidance,
or in a separate engineering contract when useful. Do not duplicate it
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
| Raw tracker intake disposition and ready handoff | [Triage](../../skills/astra/triage/SKILL.md), only when explicitly requested |
| Delivery decomposition and tracker publication | [To tickets](../../skills/astra/to-tickets/SKILL.md), using repository tracker guidance and an accepted source |
| Model allocation and execution authority | [Cost-aware coding](../../skills/astra/cost-aware-coding/SKILL.md), only when requested |
| Concurrent implementation scheduling, custody, and integration | [Parallel implement](../../skills/astra/parallel-implement/SKILL.md), only when requested |
| Candidate correctness and maintainability assessment | [Change review](../../skills/astra/change-review/SKILL.md); high assurance is separately requested |
| Architecture-wide improvement, hard bugs, or measured optimization | [Audit codebase](../../skills/astra/audit-codebase/SKILL.md), [diagnosing bugs](../../skills/astra/diagnosing-bugs/SKILL.md), and [hillclimb](../../skills/astra/hillclimb/SKILL.md) |
| Evidence gathering, context upkeep, and guided procedures | [Research](../../skills/astra/research/SKILL.md), [context hygiene](../../skills/astra/context-hygiene/SKILL.md), and [wizard](../../skills/astra/wizard/SKILL.md) |
| Active Git conflicts | [Resolving merge conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) |

The managed pack currently contains 17 skills. Their metadata owns invocation
behavior; the README lists explicit-only workflows. Continuation handoffs belong
to writing-for-agents, with execution-specific state added by the relevant workflow.
Ordinary implementation uses repository guidance and the engineering contract
directly. A separate implementer-method skill is not required: worker scope and
custody come from the active assignment, while implementation judgment comes from
the repository engineering contract.

A feature can be shaped and implemented without tickets. Tickets become useful
when delivery needs tracked units; they do not authorize concurrent writers.
Parallel implementation requires independent ownership and integration proof.
Specialists can also work sequentially without activating parallel delivery.
Skills remain usable individually; cost-aware coding is not an umbrella requirement.

## Why cost-aware coding has stronger gates

Cost-aware coding is an explicit workflow whose objective is to reduce Astra lead
token and context churn without weakening the accepted result. Its default GPT-6
roles are Astra Medium for consequential reasoning and final review, Sol Medium
for substantial implementation, and Luna Max for compact bounded work when
briefing and verification remain cheap.

The workflow delegates only when expected Astra-context savings exceed handoff,
coordination, verification, and recovery overhead. While a worker owns
implementation, Astra stays mostly dormant instead of shadowing the work or
polling for routine progress. The worker returns a stable candidate,
decision-relevant evidence, material limits, and released custody.

For requested coordinated serial delivery, meaningful checkpoints are optional.
Use them when an early wrong interface, persisted representation, or integration
decision would make later work materially expensive to redo. Checkpoint proof is
reused only while later changes leave its relevant inputs and assumptions valid;
the final integrated review still governs completion.

Recovery follows the actual cause rather than fixed attempt allowances. Requirement,
permission, environment, or contradictory-acceptance failures return to their
owner. Local implementation corrections normally return to the same worker while
its retained context remains useful. A Luna task that grows beyond its bounded
contract moves to Sol. Sol effort escalates only for demonstrated implementation
reasoning difficulty; Astra effort escalates only when stronger lead reasoning can
materially change a consequential decision.

When combined, parallel-implement owns concurrency, lane custody, integration, and
parallel recovery. Cost-aware coding retains model and effort routing, budget
policy, and final review. Deterministic helpers may manage lanes or collect
bounded telemetry, but they do not replace judgment or turn logged counters into
proven savings.

## Installation and migration

`skills/astra/` is the managed source. `skills/custom/` is historical source retained
for comparison and users evaluating the more detailed pack; it is not deployed by
the current installer. Smaller models may need those additional instructions;
compatibility is not evidence of equivalent behavior across models.

Repo bootstrap adapts the engineering contract and offers reconciliation of
existing agent guidance. Where local policy differs, it offers reconciliation
that preserves useful local choices or adoption of identified template defaults,
with their consequences made explicit. Both retain verified repository facts and
operating constraints while replacing obsolete pack routes within the approved
scope. New repositories start with compact agent instructions; separate guides
need useful content, and tracker setup requires requested or established tracking.
The resulting contract is repository-owned, not a mirror that must match its seed
forever.

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
