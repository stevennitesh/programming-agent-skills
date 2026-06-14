---
name: subagent-workflow
description: "Use when the user explicitly asks for subagents, parallel agents, worker agents, independent code review, multi-agent codebase exploration, subagent-ready handoffs, or an approved plan/issue calls for authorized, bounded delegation that is cheaper than local work."
---

# Subagent Workflow

Subagents are tools for bounded read-only exploration, one implementation slice, or independent review. They are not the default way to work.

## Core Rule

Default to local work. Delegate bounded work, not responsibility.

The parent owns scope, integration, review triage, and final verification. Do not treat a subagent report as proof; inspect it against source, diffs, tests, logs, command output, CI, or the approved request.

Ownership scope means the files, modules, contracts, behavior, or read-only question delegated to a subagent. It is task scope, not long-term code ownership or permission to change adjacent areas.

A request for "subagents" changes the route only when the work can be bounded into an agent-ready packet.

## Fast Gate

Before dispatching, name:

```text
Authorization source:
Available tooling:
Execution mode:
Ownership or read-only scope:
Why delegation beats local work:
Expected evidence:
Parent verification:
```

Then choose:

- If delegation is unauthorized, unavailable, unbounded, or slower than local work, do not dispatch.
- If the task is read-only and independent, use an Explorer or Reviewer packet.
- If implementation is delegated, require ownership scope, forbidden scope, acceptance check, verification command, and parent review plan.

Subagent-ready means the packet names the task, allowed or owned scope, forbidden scope, first check, expected output or acceptance check, required evidence, and parent follow-up. If those fields cannot be filled from repo evidence and approved scope, explore locally or clarify before dispatching.

## Authorization

Do not dispatch a subagent unless delegation is authorized for this task and the current environment or tool policy permits it.

Delegation is authorized when:

- the user explicitly asks for subagents, parallel agents, worker agents, or independent review
- the user approves a plan, issue, or workflow that explicitly calls for subagents
- existing repo or issue instructions require subagent review and no newer user instruction forbids it

This can be standing authorization. If an approved plan, issue, repo instruction, or current user request already grants delegation, do not ask again just to use an appropriate subagent.

If authorization or tooling is missing, run the same gates locally and label the result as `self-review`, not independent review. Do not imply a separate agent inspected or verified the work.

If the user explicitly requires separate-agent evidence and tooling is unavailable, report that constraint instead of simulating independence.

## Use Or Avoid

Use subagents only when delegation is authorized, available, bounded, and worth the overhead, and at least one is true:

- The user explicitly asks for subagents or parallel agents.
- Two or more read-only codebase questions can be answered independently.
- A completed source change needs independent spec or quality review.
- Broad diff review benefits from separate perspectives over non-overlapping modules, contracts, or risk areas.
- One implementation slice has clear caller-visible behavior, owned files/modules, acceptance checks, verification commands, and enough value to justify the review gate.

Avoid subagents when:

- the current environment, policy, or user instruction does not permit delegation
- a simple local inspect, edit, check, or self-review loop is cheaper
- the next step depends on one result you need immediately
- work is tightly coupled across the same files, public or caller contract, migration, or state/data path
- you would only be outsourcing judgment the parent must own
- the packet would need `TBD` for scope, forbidden scope, first check, expected evidence, or acceptance criteria

Read-only explorers and reviewers do not require worktrees.

Implementation subagents follow the plan or issue execution mode. Missing mode means `sequential`; do not run implementation issues in parallel. For `parallel-disjoint` or `parallel-overlap`, use `worktree-isolation` before editing; overlap also needs the approved integration strategy.

## Role Templates

| Role | Use for | Template |
| --- | --- | --- |
| Explorer | Read-only source investigation, code mapping, reproduction evidence, implementation options | `templates/explorer.md` |
| Implementer | One caller-visible slice or disjoint file/module scope with checks | `templates/implementer.md` |
| Spec reviewer | Does the diff match the request, plan, public contract, and acceptance criteria? | `templates/spec-reviewer.md` |
| Quality reviewer | Correctness, regression risk, security/data risk, dependency/config risk, maintainability, tests | `templates/quality-reviewer.md` |

Use the template. Fill only fields relevant to the task, and paste the actual task or question into the packet. Do not make the subagent reconstruct work from a plan title, issue title, stale summary, or long thread.

Use an Explorer before an Implementer when source ownership, existing logic, or the first check is not yet known. Use spec review before quality review; if spec is wrong or incomplete, quality review is premature.

Use the base packet only for unusual roles, tiny one-off tasks, or when a role template would add no useful control:

```text
Role:
Task or question:
Allowed or owned scope:
Forbidden scope:
First check:
Expected output or acceptance check:
Verification or evidence required:
Parent follow-up:
```

For implementation packets, prefer `templates/implementer.md` and include execution mode, worktree or branch, controlling skill, dependencies, and continuity context there.

## Implementation Review Gate

Use this gate only after a delegated Implementer reports `DONE` or `DONE_WITH_CONCERNS`.

Parent flow:

- inspect changed files and diff before review; return off-scope work to implementation first
- run spec review from `templates/spec-reviewer.md`
- run quality review from `templates/quality-reviewer.md` only after spec passes or the parent explicitly accepts a spec warning
- fix blockers, record accepted warnings, and rerun the relevant parent verification command
- mark the slice complete only after parent diff review, review blockers, accepted warnings, and parent verification are handled

If review subagents are unavailable, run the same gates yourself and label them as `self-review`, not independent review. If a slice is tiny enough that self-review is clearly cheaper, avoid implementation delegation up front.

For multi-slice work, run one final parent diff review after all slices. Add a whole-diff quality review only when slices touch shared contracts, cross-module behavior, migrations, security/data, dependency/config, or integration points and the extra review is worth the overhead.

## Stop Or Ask

Stop or ask before dispatching when:

- delegation is not authorized, tooling is unavailable, or separate-agent evidence is required but cannot be produced
- the work cannot be bounded to an agent-ready packet with allowed or owned scope, forbidden scope, first check, expected evidence, and acceptance criteria
- target behavior, public or caller contract, source ownership, dependency/config impact, data/security risk, migration scope, or integration strategy needs a human decision
- the user asks for parallel implementation but execution mode, worktree isolation, disjoint ownership, dependencies, or integration strategy is missing
- the proposed split only mirrors file layers or keeps agents busy instead of separating independent questions, contracts, or source ownership
- a subagent reports `BLOCKED` or `NEEDS_CONTEXT`; change the context, scope, model, route, or ask the user instead of retrying unchanged
- reviewer findings conflict and repo evidence does not resolve the requirement or risk

Do not let subagents make unchecked user or caller behavior, architecture, public contract, dependency, data migration, durable context, or scope decisions.

## Output

```text
Delegation decision:
Subagents used:
Scope:
Evidence received:
Parent verification:
Findings or fixes:
Residual risk:
```

For read-only work, `Findings or fixes` can be parent-verified findings. For implementation, include review gates, fixes made, accepted warnings, and checks rerun.

## Handoff

- Return to `coding-router` after subagent reports, review gates, and parent verification update the route.
- Use `worktree-isolation` when approved parallel implementation needs separate branches/worktrees; overlap also needs an integration strategy.
- Use `workspace-safety` before delegated edits in a dirty tree, branch/worktree changes, dependency installs, generated output, or risky git operations.
- Use `github-tracking` when subagent work should become issue, PR, CI/check, or review-thread evidence.
- Use `verify-before-done` before claiming delegated work is complete, reviewed, ready, safe, or mergeable.
