# Using Programming Agent Skills

The [project front page](../../README.md) introduces the implementation and
demonstrated behavior. This guide covers workflow selection and host integration.
Installation and transaction recovery live in [INSTALLATION.md](../../INSTALLATION.md).

## Select a workflow

For a clear, bounded change, ask Codex to implement and verify it directly.
Use a skill when its task scope matches the work. **Request explicitly** in the
[catalog](../../README.md#find-the-right-skill) means Codex waits for an explicit
request for that workflow; natural-language requests suffice. **Automatic when
relevant** means the agent may select the skill when
the request matches its scope. Either type can be invoked by name.

Examples:

- Develop an idea into agreed behavior with [shape-work](../../skills/astra/shape-work/SKILL.md).
- Compare options with [research](../../skills/astra/research/SKILL.md).
- Investigate a difficult failure with [diagnosing-bugs](../../skills/astra/diagnosing-bugs/SKILL.md).
- Review a proposed change with [change-review](../../skills/astra/change-review/SKILL.md).
- Create a PR or follow it through CI and review to the requested endpoint with [pr-delivery](../../skills/astra/pr-delivery/SKILL.md).
- Adopt and finish another actor's unfinished work with an explicit [takeover](../../skills/astra/takeover/SKILL.md) request.
- Clean up a stale test suite with [test-cleanup](../../skills/astra/test-cleanup/SKILL.md).
- Maintain repository guidance with [context-hygiene](../../skills/astra/context-hygiene/SKILL.md).
- Coordinate requested concurrent work with [parallel-implement](../../skills/astra/parallel-implement/SKILL.md).

For one matching request and one realistic near-miss per skill, see the
[selection examples](selection-examples.md). A review request does not authorize
fixes, and a specification does not authorize implementation. Use the user's
existing authorization to determine what work can proceed.

## Choose testing and verification work

| You need | Skill | Result |
| --- | --- | --- |
| Retire, consolidate, organize, or streamline a selected test suite | [$test-cleanup](../../skills/astra/test-cleanup/SKILL.md) | Less maintenance/execution burden with meaningful regression protection retained |
| Improve reusable tools for agents to exercise real product interfaces | [$verification-harness](../../skills/astra/verification-harness/SKILL.md) | Demonstrated tooling, usage instructions, and honest coverage/resource limits |
| Complete a private or human-only prerequisite | [$wizard](../../skills/astra/wizard/SKILL.md) | A checked human procedure and sufficient non-secret evidence to resume |

All three require an explicit request. Running tests or adding feature coverage
stays with the implementation; its local completion check does not invoke a full
cleanup. Choose by the deliverable, not whether a script or assertion is involved.
A bounded feasibility experiment belongs to prototype. These are separate
responsibilities, not a required testing pipeline. Harness observations remain
agent-visible; wizard private-session input/output remains with the human.

## Choose an investigation method

| You need to decide | Skill | Evidence and endpoint |
| --- | --- | --- |
| What existing sources establish | [$research](../../skills/astra/research/SKILL.md) | Inspected sources and a supported synthesis |
| Whether a bounded approach or interaction works | [$prototype](../../skills/astra/prototype/SKILL.md) | A faithful new observation and its limits |
| Why an existing failure occurs | [$diagnosing-bugs](../../skills/astra/diagnosing-bugs/SKILL.md) | A supported causal mechanism, with a verified repair when requested |
| Whether repeated changes improve a metric | [$hillclimb](../../skills/astra/hillclimb/SKILL.md) | Comparable improvements and final confirmation under a bounded stopping rule |
| Where worthwhile codebase improvements exist | [$audit-codebase](../../skills/astra/audit-codebase/SKILL.md) | A visual map, scoped findings, and selectable candidates |

Choose by the question, not the number of runs. A prototype may need several
attempts; that does not make it an optimization loop. Descriptive dataset profiling
can remain research. A hotspot is not a measured gain, and a mitigation is not a
causal repair. A source recommendation or audit finding grants no new implementation
authority; already-authorized combined work continues within its scope.

## Choose agent-guidance work

| You need | Skill | Result |
| --- | --- | --- |
| Initial repository guidance or a requested setup migration | [$repo-bootstrap](../../skills/astra/repo-bootstrap/SKILL.md) | Verified local commands, constraints, and reading paths |
| Reconcile existing guidance, review memory, or analyze agent sessions | [$context-hygiene](../../skills/astra/context-hygiene/SKILL.md) | Scoped context repairs or supported findings |
| Write or audit a selected instruction, skill, or handoff | [$writing-for-agents](../../skills/astra/writing-for-agents/SKILL.md) | A usable artifact or focused assessment |

The filename does not decide the workflow. Rewriting one selected `AGENTS.md`
section is authoring; reconciling conflicting repository guidance is maintenance.
Neither requires another setup phase. Templates are optional seeds, not a reason
to overwrite local policy. An audit alone stays read-only; a request that also
authorizes fixes continues within that scope. Memory writes still require an
explicit request, and a handoff packet does not transfer custody or message a chat.

## Choose planning or ticketing work

Choose by the unresolved decision rather than following a sequence:

| You need | Skill | Result |
| --- | --- | --- |
| Assess/reconcile tracked work or divide accepted work into tickets | [$ticketing](../../skills/astra/ticketing/SKILL.md) | Supported dispositions, requested corrections, or bounded tickets and dependencies |
| Settle intended behavior, acceptance, or domain meaning | [$shape-work](../../skills/astra/shape-work/SKILL.md) | Agreed meaning or the requested specification/decision record |
| Choose code ownership, reuse, interfaces, or migration | [$codebase-design](../../skills/astra/codebase-design/SKILL.md) | An implementable technical decision within accepted behavior |

A clear idea can go directly to ticketing; a settled small change can go directly
to implementation. Reuse accepted decisions without repeating an interview or
creating a formal spec merely to reach the next skill. Draft tickets may remain
blocked. Readiness requires an actionable next step and available prerequisites,
not just a closed predecessor. Assessment stays read-only unless cleanup is requested and does not create new
work. Decomposition/publication and execution retain their own authority.

## Choose review and delivery work

| You need | Skill | Boundary |
| --- | --- | --- |
| Assess a selected change or supplied findings | [$change-review](../../skills/astra/change-review/SKILL.md) | Technical assessment; repairs only when authorized |
| Publish, refresh, check, monitor, or merge a PR | [$pr-delivery](../../skills/astra/pr-delivery/SKILL.md) | The requested remote endpoint; a status inquiry stays read-only |
| Inspect or resolve an active Git conflict | [$resolving-merge-conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) | The observed operation and authorized continuation; it does not start an integration |
| Adopt another actor's unfinished goal | [$takeover](../../skills/astra/takeover/SKILL.md) | Explicitly requested responsibility, custody, and contributor credit |
| Assess or clean branches/worktrees, integrating retained work when requested | [$git-cleanup](../../skills/astra/git-cleanup/SKILL.md) | Explicitly requested disposition; preserves unique work, custody, and lifecycle contracts |

Review uses one [finding standard](../../skills/astra/change-review/references/finding-standards.md)
for fresh observations and supplied feedback. Findings, incomplete required proof,
and owner-held risk acceptance are different outcomes. A clean review grants no
merge authority. These owners compose when needed; they are not required stages.

Use `$takeover` when responsibility is moving from another actor:

```text
$takeover Finish this other agent's PR using the user's latest corrections.
Preserve contributor credit and leave it ready for me to merge.
```

The agent reconciles the handoff with actual code and write ownership, verifies
the inherited work, and continues within the accepted scope. Preparing a handoff
or replacing a worker in the current assignment does not itself start takeover.

For an existing PR, ask `Bring this PR up to date with its current base and
update the branch`. PR-delivery first checks whether the goal still belongs in
the current codebase. A request only to assess the PR stays read-only.

Specify delivery's finish line in ordinary language: `Open the PR`, `Prepare it
for me to merge`, or `Fix CI and requested review findings, then merge when the
gates pass`. These are different endpoints of pr-delivery. Human-merge preparation
includes accounting for existing auto-merge or queue state. No extra full-send,
full-stop, or babysitting skill is required. Required reviews and permissions
still come from the user and repository.

## Present demonstrated project work

Use [$portfolio-presentation](../../skills/astra/portfolio-presentation/SKILL.md)
when the requested outcome is a coherent presentation across project artifacts:
for example, `Make this project's README, report, and charts clear for recruiters
using the existing evidence`. The work preserves contribution credit, scientific
meaning, and material limitations while checking the rendered reading experience.
It does not commission new experiments or publication. A single wording edit
stays direct; new investigation or evaluation retains its own scope and authority.

## Example: settle retry behavior before implementation

An import job fails after saving some records. Before changing its retry logic,
decide which records can be retried and what users should see:

```text
$shape-work Help me design retries for failed imports in this repo.
Some records may already have been saved. Clarify what can be retried safely,
what users should see, and how we will know the feature works.
```

After those decisions are settled, ask Codex to implement them. Ticketing and
parallel work are optional workflows for tasks that need them.

## Repository guidance and skills

Repository guidance records verified commands, accepted behavior and local
constraints. Skills supply procedures for a selected task. Keep project-specific
facts at their repository owners; allow the agent to choose methods within those
requirements. A general engineering-contract file is not required or supplied
by repo bootstrap.

The [repository entry](../../AGENTS.md), [context](../../CONTEXT.md), and
[design brief](design-brief.md) route contributors to current owners. Retained
research and validation records describe earlier work and do not override
current instructions.

## Models and hosts

The managed pack in `skills/astra/` was developed primarily for GPT 6 Astra and
is intended for capable coding models, including Sol 6.1, Opus 5.5, Fable 5.1
and Sonnet 5.5. The managed integration targets Codex. Other hosts need their own
skill installation and tool integration. Package checks do not establish
equivalent results across models.

The historical [custom pack](../../skills/custom/) remains available for
comparison and separate evaluation. The installer does not deploy it.

## Optional model allocation

Choose one execution arrangement for the same work:

| You want | Invoke | Execution and review |
| --- | --- | --- |
| A compact team and less lead activity | [$controlled-delegation](../../skills/astra/controlled-delegation/SKILL.md) | One primary worker and one shared support slot by default; the lead waits during implementation and accepts the result. Review is proportionate. |
| Native Ultra delegation | [$ultra-model-routing](../../skills/astra/ultra-model-routing/SKILL.md) | Native orchestration chooses the team; three sequential independent reviews precede authorized PR opening. |

Both preserve the selected lead and use the same
[Shared model routing](../../skills/astra/controlled-delegation/references/model-policy.md).
A bounded assignment still needs substantive judgment when its rules are unsettled.
The controlled support slot covers routine help, architecture advice, or review;
an implementation helper cannot independently review its own candidate.

Add parallel-implement only when parallel execution is requested; it owns lanes,
concurrency, integration, and recovery. Other skills supply their conditional
responsibility, without adding a shaping, ticketing, or PR pipeline to ordinary
delegation. Source edits do not install skills or runtime configuration, and savings
need comparable whole-task evidence.
