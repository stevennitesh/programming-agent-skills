# Using Programming Agent Skills

The [project front page](../../README.md) introduces the implementation and
demonstrated behavior. This guide covers workflow selection and host integration.
Installation and transaction recovery live in [INSTALLATION.md](../../INSTALLATION.md).

## Select a workflow

For a clear, bounded change, ask Codex to implement and verify it directly.
Use a skill when its task scope matches the work. **Request explicitly** in the
[catalog](../../README.md#find-the-right-skill) means Codex waits for a named
request. **Automatic when relevant** means the agent may select the skill when
the request matches its scope. Either type can be invoked by name.

Examples:

- Develop an idea into agreed behavior with [shape-work](../../skills/astra/shape-work/SKILL.md).
- Compare options with [research](../../skills/astra/research/SKILL.md).
- Investigate a difficult failure with [diagnosing-bugs](../../skills/astra/diagnosing-bugs/SKILL.md).
- Review a proposed change with [change-review](../../skills/astra/change-review/SKILL.md).
- Create a PR or follow it through CI and review to the requested endpoint with [pr-delivery](../../skills/astra/pr-delivery/SKILL.md).
- Clean up a stale test suite with [test-cleanup](../../skills/astra/test-cleanup/SKILL.md).
- Maintain repository guidance with [context-hygiene](../../skills/astra/context-hygiene/SKILL.md).
- Coordinate requested concurrent work with [parallel-implement](../../skills/astra/parallel-implement/SKILL.md).

For one matching request and one realistic near-miss per skill, see the
[selection examples](selection-examples.md). A review request does not authorize
fixes, and a specification does not authorize implementation. Use the user's
existing authorization to determine what work can proceed.

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

[Cost-aware coding](../../skills/astra/cost-aware-coding/SKILL.md) is an explicit
workflow for assigning tasks to specific models. The starting lead retains
planning, consequential decisions and final review. The
[model policy](../../skills/astra/cost-aware-coding/references/model-policy.md)
describes assignments. Assess cost across the whole task, including handoffs,
review and repair; savings need measurement.
