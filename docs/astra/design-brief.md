# Astra skills pack design brief

Current direction, reconciled 2026-10-06. The pack is built primarily for
**GPT 6 Astra**. Optional cost-aware execution routes implementation to GPT 6.1 Sol
and bounded work, including large-context retrieval and bulk writing, to GPT 6 Luna.
This document owns design rationale and composition for `skills/astra/`;
individual skills own execution.
[Issue #94](https://github.com/stevennitesh/programming-agent-skills/issues/94)
preserves the original proposal. Subsequent accepted decisions below replace its
pilot sequence and candidate inventory, without claiming its evaluation goals met.

## Purpose and philosophy

Supply the context, project decisions, and selected workflow contracts a capable
agent needs. Ordinary coding stays direct, with freedom over methods within the
user's accepted scope. No default skill pipeline or coding tutorial is needed.

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

Discovery metadata is shared model context. Keep each skill description to the
smallest reliable selector plus its nearest useful exclusion; procedure and
rationale belong in the skill body. Keep the root `SKILL.md` to the method every
applicable run needs and route recognizable branch-specific mechanics through
conditional references.

Ask what necessary information would disappear if guidance were deleted. Retain
user priorities, repository facts, accepted obligations, and useful workflow
contracts. Remove generic advice, duplicated defaults, and obsolete scaffolding.
A model upgrade is an opportunity to reassess that need; claims of improved or
equivalent performance still require behavioral evidence.

Keep brief project requirements in AGENTS.md or their existing owner. Separate
guides need substantial local content, such as scientific assumptions or actual
compatibility guarantees. The generic engineering contract and bootstrap seed are
retired. Preserve focused safeguards at their applicable skill owners, including
shared-validation ownership, persisted-input acceptance, writer custody, and
review evidence. A selected workflow may require more within its own scope.

## Composition and ownership

| Decision or responsibility | Current owner |
| --- | --- |
| Local commands, facts, conditional pointers | Repository `AGENTS.md`, `CONTEXT.md`, and `docs/agents/` |
| Initial repository guidance and requested setup migrations | [Repo bootstrap](../../skills/astra/repo-bootstrap/SKILL.md) |
| Ongoing repository context, durable memory, and requested agent-session retrospectives | [Context hygiene](../../skills/astra/context-hygiene/SKILL.md) |
| Selected instruction artifacts, skills, prompts, and handoffs | [Writing for agents](../../skills/astra/writing-for-agents/SKILL.md) |
| User alignment, specifications, domain meaning, and durable decision capture | [Shape work](../../skills/astra/shape-work/SKILL.md), including affected document reconciliation |
| Code reuse, ownership, simplification, integration, and retirement decisions; empirical feasibility | [Codebase design](../../skills/astra/codebase-design/SKILL.md) for the design decision and [prototype](../../skills/astra/prototype/SKILL.md) for a needed new observation |
| Reusable tooling for agents to exercise and verify real product interfaces | [Verification harness](../../skills/astra/verification-harness/SKILL.md), only when explicitly requested |
| Requested intake assessment, backlog reconciliation, and actionable handoff | [Triage](../../skills/astra/triage/SKILL.md), only when explicitly requested |
| Delivery decomposition and tracker publication | [To tickets](../../skills/astra/to-tickets/SKILL.md), using repository tracker guidance and an accepted source |
| Model allocation and execution authority | [Cost-aware coding](../../skills/astra/cost-aware-coding/SKILL.md), only when requested |
| Concurrent implementation scheduling, custody, and integration | [Parallel implement](../../skills/astra/parallel-implement/SKILL.md), only when requested |
| Candidate correctness and maintainability assessment | [Change review](../../skills/astra/change-review/SKILL.md); the lead chooses direct, independent, or scoped high-assurance review |
| Visual codebase mapping and baseline improvement discovery, hard bugs, or measured optimization | [Audit codebase](../../skills/astra/audit-codebase/SKILL.md), [diagnosing bugs](../../skills/astra/diagnosing-bugs/SKILL.md), and [hillclimb](../../skills/astra/hillclimb/SKILL.md) |
| Evidence gathering and guided procedures | [Research](../../skills/astra/research/SKILL.md) and [wizard](../../skills/astra/wizard/SKILL.md) |
| Active Git conflicts | [Resolving merge conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) |
| Branch and worktree disposition, requested retained-work integration, and cleanup | [Git cleanup](../../skills/astra/git-cleanup/SKILL.md), only when explicitly requested |
| Evidence-backed project presentation for external readers | [Portfolio presentation](../../skills/astra/portfolio-presentation/SKILL.md), only when explicitly requested |

Choose a skill by the decision or effect it owns, not merely by the artifact being
edited. Shape-work owns product alignment, domain meaning, and durable capture of
settled decisions; codebase-design resolves reuse, ownership, simplification, and
integration choices, including necessary caller transitions and retirement.
When cost-aware-coding is selected, its worker assignment and final review carry
those obligations through implementation without a mandatory cleanup phase or
unrelated repository sweep. Research investigates substantive questions through
inspected sources and critical synthesis, including credible counterevidence;
prototype obtains new evidence for a bounded uncertainty, adapting and repeating
experiments when needed to answer it. Audit-codebase discovers evidence-backed
codebase improvements through an HTML map and scoped audits. Guided exploration
leaves selection to the user; already-selected whole-repository scopes or delegated
selection proceed within that authority. Coverage and source freshness support
further selection; investigation, abstraction choices, simplification, and measured
optimization remain matters of agent judgment. Explicit brief or no-write
assessments can stay in chat.
Resumed atlases reconcile ownership and retain original evidence while recording
authorized fixes, verification, deferral, and requested delivery separately.
Changed source calls for inspecting the relevant delta; it does not reopen every
historical finding. Explicit combined analysis-and-fix requests continue through
their authorized effects, with methods and sufficient proof left to agent judgment.
The atlas augments user exploration and shows meaningful audit progress. Its
helper prepares mechanical packet fields, references finding evidence, derives
counts, and handles cosmetic edits without another audit. Relevant lenses are
concise coverage prompts; omitted dimensions stay uninspected. Investigation,
probes, comparisons, and any authorized delegation remain discretionary.
Publication protections stay enforced in code. Preview and validation effort
follow the changed surface, with unavailable host capability recorded once.
Change-review judges a fixed change candidate. Verification-harness creates
or improves reusable repository tooling for agents to exercise and verify real
UI, command, and agent interfaces. It reduces repeated setup and fragile
interactions while preserving target identity, meaningful evidence, and resource
ownership. The agent chooses methods and demonstrates the requested capability;
failure attribution follows evidence, including unresolved causes. Routine test
execution needs no tooling workflow. Wizard prepares the smallest
useful terminal handoff for a private or human-only step, reusing existing tools
where suitable. Private input and session output stay with the human, while a
deliberate non-secret result can establish the prerequisite for already-authorized
work to resume. Triage assesses requested intake or existing backlog and applies
authorized tracker corrections using the repository's state model. It preserves
active ownership and requires evidence for readiness, completion, and dependency
changes; investigation methods and queue ordering remain discretionary. It does
not itself start deep diagnosis, code review, decomposition, or implementation;
to-tickets decomposes specs, shaped work, or sufficiently clear ideas using the
repository's tracker conventions. Its bounded tickets supply fresh-agent context,
acceptance, and predecessor-result conditions; unresolved consequential meaning
remains gated, and potential parallelism remains subject to execution ownership.
Repo-bootstrap owns initial guidance and
requested setup migrations. Context-hygiene owns ongoing context maintenance;
writing-for-agents owns an already-scoped instruction artifact. Routine context
maintenance needs no bootstrap or authoring phase.
Cost-aware-coding may be combined with parallel-implement:
the former owns model and budget routing, while the latter owns concurrency,
custody, and integration.
Parallel implementation establishes task-relevant runtime and data readiness before
dispatch, shares durable inputs by reference, and isolates mutable outputs. The
coordinator may use supported host-managed worktrees or the bundled helper while
preserving each lifecycle owner's integration and cleanup contract.

Git-cleanup owns branch and worktree disposition, including requested integration
of worthwhile retained work. It preserves active ownership, uses evidence suited
to rewritten history, and verifies authorized cleanup through the actual lifecycle
owner. Parallel-implement still owns its lanes, and resolving-merge-conflicts owns
active conflict resolution. Routine commits and pushes need no cleanup workflow.
Portfolio-presentation owns a coherent, evidence-backed reading experience across
the requested project artifacts. Analysis and evaluation contracts stay with the
project; the agent chooses narrative, visuals, tools, and organization. Finished
prose targets a domain-aware newcomer with roughly equal parts ASD-STE100
Simplified Technical English and domain language. The skill owns how that
STE-informed blend and pstack's unslop principles support concrete, natural
writing. Isolated wording edits, new research, and general website construction
remain outside its scope. Both skills require an explicit request.

The managed pack currently contains 20 skills. Their metadata owns invocation
behavior; the README lists explicit-only workflows. Continuation handoffs belong
to writing-for-agents, with execution-specific state added by the relevant workflow.
Ordinary implementation uses the accepted assignment and applicable repository
requirements. Worker scope and custody come from the active workflow; methods and
local implementation decisions remain with the worker within those boundaries.

Writing-for-agents preserves intent, receiver context, authority, and completion
for selected instruction artifacts, reusable guidance, consequential assignments,
and handoffs. Ordinary worker dispatch does not require a separate authoring
phase. Capable receivers choose their methods within the accepted constraints;
the skill's references carry conditional continuity and evidence rules, while
host skill-creation guidance owns packaging mechanics. Editorial and structural
checks do not establish improved agent performance, and ordinary edits need no
behavioral evaluation campaign.

Context-hygiene can be selected when scattered, stale, conflicting, or missing
context affects the active task or an agent-session retrospective is requested.
It chooses investigation and consolidation methods within that scope. A
conditional session reference steers toward supported causes, proportionate
corrections, and verified effects while leaving evidence selection, methods,
depth, and judgment to the agent. The initial explanation may be challenged;
no durable change or an unresolved cause can be a valid result. Correct harness
mechanisms at their owners when prose does not address the cause. Repository
guidance may own accepted requirements; managed memory supplies recall, with
temporary state kept in task records or history and durable lessons kept
conditional on their evidence and applicability.
Memory writes require an explicit request and the runtime's supported mechanism.
Read-only audits finish with findings; cleanup distinguishes verified changes
from pending memory updates. Selection does not initiate unrelated context sweeps.

Shape-work develops and challenges ideas through an adaptive interview and delivers
a specification when requested. Domain and ADR capture can run directly for
settled decisions. Shaping reconciles the current documents affected by those
decisions; context-hygiene owns general context maintenance. Product priorities,
stages, and dependencies can belong in a spec, while implementation planning stays
with the execution lead. Cost-aware-coding organizes delivery when selected;
ordinary planning needs no additional skill phase.

A feature can be shaped and implemented without tickets. Tickets become useful
when delivery needs tracked units; they do not authorize concurrent writers.
Parallel implementation requires independent ownership and integration proof.
Specialists can also work sequentially without activating parallel delivery.
Skills remain usable individually; cost-aware coding is not an umbrella requirement.

The [canonical selection examples](selection-examples.md) provide one positive
request and one nearest realistic non-match for each managed skill. They are
maintenance checks for discovery boundaries, not another router or execution
contract; frontmatter descriptions and skill bodies remain authoritative.

## Cost-aware roles and autonomy

[Cost-aware coding](../../skills/astra/cost-aware-coding/SKILL.md) owns the accepted
lead, worker, bounded-helper, and reviewer responsibilities, optional checkpoints,
and quiet waiting during delegated implementation. Its
[model policy](../../skills/astra/cost-aware-coding/references/model-policy.md)
owns exact models and effort choices; the user selects the starting lead.

When parallel implementation is requested, parallel-implement owns concurrency,
custody, integration, and recovery. Keep current routing and execution mechanics
at these skill owners instead of duplicating them in repository context.

## Installation and migration

`skills/astra/` is the managed source. `skills/custom/` is historical source retained
for comparison and separate evaluation; it is not deployed by the current installer.
The custom pack contains more detailed instructions, but current model-specific
comparisons are not sufficient to claim that smaller models perform better with
that historical package.

Repo bootstrap owns initial guidance and requested setup migrations: accurate repository
guidance, preserved deliberate decisions, reconciled obsolete routes, and a
coherent reading path. The agent chooses the investigation, files, organization,
and verification. Conditional references supply migration and optional setup
conventions; domain and tracker templates are starting material only when useful.
No generic engineering contract, document tree, or template parity is required.
Tracker setup requires requested or established tracking, and parallel
prerequisites do not start workers.
Adopted guidance belongs to the repository. Policy choices need user input only
when consequential meaning remains unresolved.

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
