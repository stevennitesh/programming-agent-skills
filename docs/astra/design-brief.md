# Astra skills pack design brief

Current direction, reconciled 2026-10-26. The pack is built primarily for
**GPT 6 Astra**. Controlled delegation supplies a compact team and waiting lead;
Ultra model routing preserves the user's selected native delegation mode.
Both use one shared Sol/Terra child-routing policy while retaining separate
execution rules and the user's selected lead.
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
| Tracker assessment/reconciliation, delivery decomposition, and authorized publication | [Ticketing](../../skills/astra/ticketing/SKILL.md), only when explicitly requested |
| Controlled delegation, limited support, and quiet waiting during implementation | [Controlled delegation](../../skills/astra/controlled-delegation/SKILL.md), only when requested |
| Native Ultra delegation and its pre-PR review sequence | [Ultra model routing](../../skills/astra/ultra-model-routing/SKILL.md), only when requested |
| Shared child-model and effort routing for both execution workflows | [Shared model routing](../../skills/astra/controlled-delegation/references/model-policy.md) |
| Concurrent implementation scheduling, custody, and integration | [Parallel implement](../../skills/astra/parallel-implement/SKILL.md), only when requested |
| Candidate correctness and maintainability assessment | [Change review](../../skills/astra/change-review/SKILL.md); the lead chooses direct, independent, or scoped high-assurance review |
| PR creation, status, requested CI and hosted-review follow-through, and authorized merge | [PR delivery](../../skills/astra/pr-delivery/SKILL.md), selected for requested PR delivery rather than review-only assessment |
| Adopting unfinished work from another PR, branch, or conversation, including custody reconciliation and contributor credit | [Takeover](../../skills/astra/takeover/SKILL.md), only when explicitly requested |
| Test retirement, consolidation, organization, and execution efficiency | [Test cleanup](../../skills/astra/test-cleanup/SKILL.md), only when explicitly requested; routine verification and feature test authoring stay with their work |
| Visual codebase mapping and baseline improvement discovery, hard bugs, or measured optimization | [Audit codebase](../../skills/astra/audit-codebase/SKILL.md), [diagnosing bugs](../../skills/astra/diagnosing-bugs/SKILL.md), and [hillclimb](../../skills/astra/hillclimb/SKILL.md) |
| Evidence gathering and guided procedures | [Research](../../skills/astra/research/SKILL.md) and [wizard](../../skills/astra/wizard/SKILL.md) |
| Active Git conflicts | [Resolving merge conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) |
| Branch and worktree disposition, requested retained-work integration, and cleanup | [Git cleanup](../../skills/astra/git-cleanup/SKILL.md), only when explicitly requested |
| Evidence-backed project presentation for external readers | [Portfolio presentation](../../skills/astra/portfolio-presentation/SKILL.md), only when explicitly requested |

Choose a skill by the decision or effect it owns, not merely by the artifact being
edited. Shape-work owns product alignment, domain meaning, and durable capture of
settled decisions; codebase-design resolves reuse, ownership, simplification, and
integration choices, including necessary caller transitions and retirement.
When controlled-delegation is selected, its worker assignment and final review carry
those obligations through implementation without a mandatory cleanup phase or
unrelated repository sweep. Research interprets inspected existing evidence;
prototype obtains a faithful new observation for a bounded uncertainty. Diagnosis
establishes an existing failure's cause; hillclimb iteratively retains measured
improvements and confirms the final result. Choose by the deciding question,
not a required research/experiment/optimization sequence. Specialized evidence,
causal, and measurement references remain at those method owners.
Audit-codebase discovers improvements through an HTML map and scoped audits. Its
maintenance reference owns report checking and preview procedure; the root and
visual contract route there instead of maintaining competing copies. Guided exploration
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
Prepared independent results share one guarded publication; narrow follow-ups
retain existing analysis. Passing-check receipts can carry across Git-only changes
when relevant inputs remain equivalent. Gap dispositions stay separate from fix
and delivery outcomes. Immutable snapshots and evidence are interned inside the
self-contained report; the pack supports one current format.
Publication protections stay enforced in code. Preview and validation effort
follow the changed surface, with unavailable host capability recorded once.
Change-review judges a fixed change candidate. Verification-harness creates
or improves reusable repository tooling for agents to exercise and verify real
UI, command, and agent interfaces. It reduces repeated setup and fragile
interactions while preserving target identity, meaningful evidence, and resource
ownership. The agent chooses methods and demonstrates the requested capability.
Requested human inspection retains a usable preview with an explicit resource
handoff and teardown condition. Failure attribution follows evidence, including
unresolved causes. Routine test
execution needs no tooling workflow. Wizard prepares the smallest
useful terminal handoff for a private or human-only step, reusing existing tools
where suitable. Private input and session output stay with the human, while a
deliberate non-secret result can establish the prerequisite for already-authorized
work to resume. Test-cleanup owns supported regression protection and suite burden;
verification-harness owns reusable agent-operated product proof routes; wizard owns
private human procedures. Select by the requested deliverable. Their similar
evidence language does not justify a shared verification framework or required
pipeline. All three retain explicit invocation. Wizard's existing inputs/effects
reference owns consequential-effect confirmation and safe non-secret handback;
its root owns private launch and continuation. The global owner retains routine
work-section test completion checks.

Ticketing owns tracker assessment/reconciliation and decomposition/publication as
independent explicit modes. Its [Work-item brief](../../skills/astra/ticketing/references/work-item-brief.md)
and [Tracker publication and repair](../../skills/astra/ticketing/references/tracker-publication.md)
also serve callers without selecting the workflow or granting extra authority.
Assessment or cleanup does not create new work. A clear idea needs no prior
triage, spec, or interview before requested decomposition. Shaping owns meaning,
codebase-design owns technical choices, and execution owns scheduling, custody,
and parent closeout. Readiness requires available predecessor results and resolved
gates. Repository tracker conventions and active-revision branches remain binding.

Repo-bootstrap owns initial guidance and requested setup migrations; context-hygiene
owns ongoing context maintenance. Both use one
[Repository guidance reconciliation](../../skills/astra/context-hygiene/references/audit-and-changes.md)
method, preserving local policy and consumers without requiring template parity.
Writing-for-agents owns the selected instruction artifact. Choose by the work,
not the filename; routine maintenance needs no extra setup or authoring phase.
Memory updates, retrospectives, handoffs, and behavior evaluation retain their
conditional contracts and authority boundaries. Shared references select no new
workflow, and an audit does not cancel separately authorized fixes.

Controlled delegation may be combined with parallel-implement:
the former retains controlled assignments and model routing; the latter owns
concurrency, custody, and integration.
Parallel implementation establishes task-relevant runtime and data readiness before
dispatch, shares durable inputs by reference, and isolates mutable outputs. The
coordinator may use supported host-managed worktrees or the bundled helper while
preserving each lifecycle owner's integration and cleanup contract.

Git-cleanup owns branch and worktree disposition, including requested integration
of worthwhile retained work. It preserves active ownership, uses evidence suited
to rewritten history, and verifies authorized cleanup through the actual lifecycle
owner. Parallel-implement still owns its lanes, and resolving-merge-conflicts owns
active conflict resolution. Routine commits and pushes need no cleanup workflow.
Candidate review remains conditional on need; retained-work assessment and proof
of the combined result still precede source retirement. Lane-specific cleanup
guarantees remain with their execution owner.
PR-delivery owns requested PR creation or updates and the requested endpoint:
a status report, publication, merge-readiness, or authorized merge. It reuses
change-review for technical feedback assessment and keeps CI, hosted-review
completion, unresolved findings, and candidate freshness distinct. Monitoring
does not authorize merging. PR-delivery also owns GitHub feedback retrieval,
posting, thread resolution, and verified remote state; change-review owns the
technical assessment used by those actions. The workflow uses existing tools
rather than adding a watcher or prescribing review delegation. Editorial review
and package checks do not establish reliable delivery behavior.

The review/delivery group retains four decision owners: candidate assessment,
remote PR state, active Git-operation resolution, and adoption of inherited work.
PR-delivery's root owns common verification, candidate freshness, merge gates,
and remote readback. Its endpoint reference adds human-merge preparation and
automation-state safeguards; monitoring adds waiting and resource lifecycle.
Git-specific side roles and recovery remain in conflict resolution's operation
reference. Takeover adds custody, independent assessment of inherited claims,
and contributor credit, with candidate review conditional on need. These routes
do not create a required review/integration/delivery sequence.

Change-review keeps finding admission, priority, and gate semantics in one
standalone standard, shared by fresh review and feedback assessment. Independent
and multiple-reviewer contracts share one reference; impact and repair procedures
remain conditional. Compatibility-sensitive review retains its distinguishing
regression requirement. Pending risk acceptance is an owner decision, and missing
required proof leaves the review incomplete. Output requirements describe the
needed evidence without imposing a report template.

Selected ideas from [Tstack at revision 7de017b](https://github.com/t3dotgg/tstack/tree/7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd)
are adopted at existing decision owners. PR-delivery owns conditional stale-PR
refresh, supported monitoring, delivery through an authorized merge, and readiness
for human merge. Refresh assesses whether a PR remains useful before replaying it;
readiness accounts for existing auto-merge and queue state. Change-review owns
optional provider diversity, evidence-based feedback, and bounded repair loops.
These Tstack review and delivery methods extend current workflows rather than
adding council, model-specific review, comment-formatting, or end-to-end umbrella
skills. The pack adds no PR watcher, fixed bot gates, numerical acceptance scores,
or blanket permission overrides.

Takeover is a separate explicit-only workflow because receiving responsibility
for another actor's unfinished work crosses intent, candidate, custody, and
contributor-credit boundaries. It reconstructs the actual state and continues to
the requested endpoint using existing execution and delivery owners. Writing a
handoff remains with writing-for-agents; replacement within a current delegated
assignment remains with that workflow's recovery. A takeover does not require a
replacement PR, authorize closing the source, or select model allocation or
parallel implementation. The adopted contracts have source and package validation;
that does not establish improved agent effectiveness.

Portfolio-presentation owns a coherent, evidence-backed reading experience across
the requested project artifacts. Analysis and evaluation contracts stay with the
project; the agent chooses narrative, visuals, tools, and organization. Finished
prose targets a domain-aware newcomer with roughly equal parts ASD-STE100
Simplified Technical English and domain language. The skill owns how that
STE-informed blend and pstack's unslop principles support concrete, natural
writing. Numeric disagreements are traced within existing authority; unresolved
analysis changes remain with their owner rather than becoming presentation edits.
Isolated wording edits, new research, and general website construction remain
outside its scope. Git-cleanup and portfolio-presentation require explicit requests.

Test-cleanup owns explicitly requested removal of low-value tests, consolidation,
organization, and reduced execution cost. Its central decision is which plausible
regression a test catches in supported behavior. Agents choose what to keep,
rewrite, consolidate, reorganize, or remove, with evidence for retirement and
preserved distinct failure cases. A cleanup request permits local test edits;
read-only audits finish with findings. The user's global agent guidance owns a
brief local completion check of tests added or modified in a work section, removing one-off
checks with no continuing purpose. Substantive cleanup can be suggested, but does
not automatically invoke the full skill. Validation and replacement regression
tests are part of cleanup when needed. The skill does not require a full audit
for ordinary coding, drop support, change production behavior, or require an audit
ledger, new framework, mutation campaign, or full-suite rerun after every edit.
Shared fixture impact and unresolved questions determine broader validation.
The method is instruction-only because semantic test value is the decision;
existing repository tools own collection and execution.
A conditional bulk-pruning reference adds a shared rubric, review of proposed
deletions, exact syntax-aware batches, affected configuration cleanup, and
comparable measurements for requested broad purges. Independent review is an
option when delegation is authorized; agreement does not replace evidence for
retiring a requirement. Category labels and deletion targets do not decide value.

This design applies the concise discovery and reduced scaffolding guidance in
OpenAI's [Astra prompting guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
and [skills article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra),
alongside Anthropic's [skill authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
[Opus 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5),
[Opus 5.5 usage article](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/),
and [context engineering article](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/).
These sources support the authoring choices; they do not establish cleanup
effectiveness or equivalent behavior across models.

The managed pack currently contains 23 skills. Their metadata owns invocation
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
with the execution lead. Controlled delegation organizes delivery when selected;
ordinary planning needs no additional skill phase.

A feature can be shaped and implemented without tickets. Tickets become useful
when delivery needs tracked units; they do not authorize concurrent writers.
Parallel implementation requires independent ownership and integration proof.
Specialists can also work sequentially without activating parallel delivery.
Skills remain usable individually; controlled delegation is not an umbrella requirement.

The [canonical selection examples](selection-examples.md) provide one positive
request and one nearest realistic non-match for each managed skill. They are
maintenance checks for discovery boundaries, not another router or execution
contract; frontmatter descriptions and skill bodies remain authoritative.

## Model allocation and autonomy

The user selects the starting lead. Choose
[controlled delegation](../../skills/astra/controlled-delegation/SKILL.md) for a compact
team and waiting lead, or [native Ultra delegation](../../skills/astra/ultra-model-routing/SKILL.md)
for native orchestration and its three sequential pre-PR reviews.

Both load [Shared model routing](../../skills/astra/controlled-delegation/references/model-policy.md)
and [Native spawning](../../skills/astra/controlled-delegation/references/native-spawning.md).
These references own routing and host mechanics without selecting an execution
arrangement. Controlled assignments own their briefs, support slot, and checkpoints;
explicit parallel implementation owns its lanes, dispatch, integration, and recovery.
Parallel recovery reads shared routing directly, without importing controlled team
limits. Change-review owns technical assessment and finding disposition; risk
acceptance remains with its authorized owner. PR-delivery owns remote publication
and requested follow-through. Shaping, design, ticketing, and takeover
remain conditional responsibilities, not a required delegation pipeline.

The earlier Astra/Luna allocation and fixed cost assumption are superseded. Source
instructions do not enforce runtime budgets or publication gates, and package
validity does not establish lower cost or equivalent output quality.

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
