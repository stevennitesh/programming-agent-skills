---
name: subagent-workflow
description: Use when the user asks for subagents, parallel agents, worker agents, independent code review, or multi-agent codebase exploration; or when repo work has independent source modules, checks, or review scopes that can safely run in parallel.
---

# Subagent Workflow

Subagents are tools for bounded coding work: codebase exploration, one implementation slice, or independent review of a changed source scope. They are not the default way to work.

## Core Rule

Delegate bounded work, not responsibility. The parent owns scope, integration, review triage, and final verification.

## Use Or Avoid

Use subagents when the current environment permits delegation and at least one is true:

- The user explicitly asks for subagents or parallel agents.
- Two or more read-only codebase questions can be answered independently.
- One implementation slice has clear caller-visible behavior, owned files/modules, and verification commands.
- A completed source change needs independent spec or quality review.
- Broad diff review benefits from separate perspectives over non-overlapping modules, contracts, or risk areas.

Avoid subagents when:

- The current environment, policy, or user instruction does not permit delegation.
- The next step depends on one result you need immediately.
- Work is tightly coupled across the same files, caller contract, migration, or state/data path.
- You would only be outsourcing judgment the parent must own.
- A simple local inspect/edit/check loop is cheaper.

Implementation subagents follow the plan or issue execution mode. Missing mode means `sequential`.

- `sequential`: do not run implementation issues in parallel.
- `parallel-disjoint`: use `worktree-isolation` so each active implementer has a separate branch/worktree.
- `parallel-overlap`: use `worktree-isolation` plus the approved integration strategy before editing.

Read-only explorers and reviewers do not require worktrees.

## Roles

| Role | Use for | Template |
| --- | --- | --- |
| Explorer | Read-only source investigation, code mapping, reproduction evidence, implementation options | `templates/explorer.md` |
| Implementer | One caller-visible slice or disjoint file/module scope with checks | `templates/implementer.md` |
| Spec reviewer | Does the diff match the request, plan, public contract, and acceptance criteria? | `templates/spec-reviewer.md` |
| Quality reviewer | Correctness, regression risk, security/data risk, dependency/config risk, maintainability, tests | `templates/quality-reviewer.md` |

Use spec review before quality review. If spec is wrong or incomplete, quality review is premature.

For delegated implementation slices, reviewers are a gate, not an optional perspective.
Run both reviewers before marking the slice complete unless review subagents are unavailable or the user explicitly asks to skip review.
If a slice is tiny enough that local self-review is clearly cheaper, avoid delegation up front instead of dispatching an implementer and skipping reviewers.
Record any skip reason.
If subagents are unavailable, run the same gates yourself and label them as self-review, not independent review.

When dispatching a role that has a template, start from that template by default.
Copy or adapt its fields into the packet instead of rebuilding the packet from memory.
Use the base packet only for unusual roles, tiny one-off tasks, or when a role template would add no useful control.
If you skip an applicable template, say why in the parent notes or final report.

## Packet Rules

- Give each subagent a tight task packet, not the whole conversation.
- Choose the role first, then use that role's template as the packet skeleton when one exists.
- Include exact coding scope, owned files/modules, forbidden files/behaviors, expected output, and evidence required.
- Include execution mode, parallel group, issue claim state, and dependencies when implementing from a GitHub issue.
- Include the worktree path and branch when `worktree-isolation` created an isolated workspace for the task.
- Name the controlling skill for implementation packets.
- Use `tdd-slice` for behavior changes, `diagnose-loop` for failing symptoms, or `codebase-cleanup` for behavior-preserving refactors.
- Include only task-relevant `CONTEXT.md` terms; do not dump the whole file.
- Paste the task or question into the packet; do not make the subagent reconstruct it from a plan or long thread.
- Prefer read-only explorers and reviewers.
- Do not run parallel implementation when the plan or issue is missing mode metadata or says `sequential`.
- For `parallel-disjoint`, keep implementation ownership separate and use `worktree-isolation`.
- For `parallel-overlap`, use `worktree-isolation` and the approved integration strategy.
- Tell implementers they are not alone in the codebase and must preserve others' work.
- Do not trust subagent success claims without parent diff inspection and, when needed, rerunning verification commands.
- Do not let subagents make unchecked user/caller behavior, architecture, public contract, dependency, data migration, or scope decisions.

Base packet for custom roles or fallback use:

```text
Role:
Task:
Context:
Controlling skill:
Shared terms:
Execution mode:
Parallel group:
Issue claim:
Owned files/modules:
Forbidden files/behaviors:
Public or caller contract:
First check:
Acceptance check:
Expected output:
Verification command:
Worktree/branch:
Risks:
```

## Reviewer Gate

Use this gate after an implementer reports `DONE` or `DONE_WITH_CONCERNS`.

1. Parent inspects the changed files and diff before spawning reviewers. If the diff is obviously off-scope, send it back to implementation before review.
2. Dispatch the spec reviewer from `templates/spec-reviewer.md`.
3. Handle spec verdict:
   - `BLOCK`: fix the spec gap, then rerun spec review. Do not start quality review.
   - `WARN`: either fix it or record the accepted residual risk before quality review.
   - `PASS`: proceed to quality review.
4. Dispatch the quality reviewer from `templates/quality-reviewer.md` only after spec review passes or a spec warning is explicitly accepted.
5. Handle quality verdict:
   - `BLOCK`: fix the quality issue, then rerun quality review. If the fix changes scope or behavior, rerun spec review first.
   - `WARN`: either fix it or record the accepted residual risk before marking the slice complete.
   - `PASS`: proceed to parent verification.
6. Parent reruns the relevant verification command after final fixes. Do not rely on subagent reports.
7. Mark the slice complete only after review blockers are closed, accepted warnings are recorded, and parent verification has run.

For multi-slice work, run one final parent diff review after all slices.
Add a final whole-diff quality reviewer when slices touch shared contracts, cross-module behavior, migrations, security/data, dependency/config, or integration points.

## Coordination

1. Decide whether subagents add enough value to pay the context, time, and integration cost.
2. Split by subsystem, source entry point, caller contract, question, or file ownership. Do not split only to keep agents busy.
3. Dispatch independent read-only work in parallel when possible.
4. Before parallel implementation, inspect the plan or issue execution coordination and current claim state.
5. If mode is missing or `sequential`, run implementation issues one at a time or keep one parent-owned.
6. For `parallel-disjoint`, use `worktree-isolation` and keep file/module ownership separate.
7. For `parallel-overlap`, use `worktree-isolation` and the approved integration strategy.
8. Let subagents propose `CONTEXT.md` updates, but the parent verifies and decides before editing durable docs.
9. Handle implementer status:
   - `DONE`: inspect diff and run the Reviewer Gate.
   - `DONE_WITH_CONCERNS`: read concerns before review; address correctness or scope concerns first.
   - `NEEDS_CONTEXT`: provide missing context or narrow the task before retrying.
   - `BLOCKED`: change something: more repo context, smaller task, stronger model, different route, or user decision.
10. Never force the same blocked task to retry unchanged.
11. Inspect outputs and diffs yourself, including worktree diffs before integration.
12. Rerun the parent-level checks before claiming completion.

## Review Triage

When multiple reviewers report findings:

1. Normalize and deduplicate.
2. Group by spec gap, correctness bug, regression risk, test gap, security/data risk, dependency/config risk, maintainability, or style.
3. Rank:
   - Blocker: wrong caller-visible behavior, missing acceptance criterion, data/security risk, failing required check, broken public contract.
   - Important: likely regression, weak test coverage, fragile module boundary, unclear file ownership.
   - Minor: naming, readability, local polish.
4. Verify findings against source, diff, tests, logs, CI output, or manual check evidence.
5. Resolve conflicts by requirements, public contracts, and tests. If still ambiguous, prefer the smaller reversible change or ask the user.
6. Produce one fix list.
7. Rerun parent verification after fixes.

## Output

```text
Subagents used:
Review gates:
Findings accepted:
Findings rejected:
Fixes made:
Parent verification:
Residual risk:
```

## Handoff

- Return to `coding-router` after subagent reports, review gates, and parent verification update the route.
- Use `worktree-isolation` when approved parallel implementation needs separate branches/worktrees; overlap also needs an integration strategy.
- Use `workspace-safety` before delegated edits in a dirty tree, branch/worktree changes, dependency installs, generated output, or risky git operations.
- Use `github-tracking` when subagent work should become issue, PR, CI/check, or review-thread evidence.
- Use `verify-before-done` before claiming delegated work is complete, reviewed, ready, safe, or mergeable.
