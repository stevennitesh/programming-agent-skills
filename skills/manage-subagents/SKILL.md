---
name: manage-subagents
description: Use when the user asks for subagents, parallel agents, worker agents, independent review, multi-agent exploration, or several independent tasks can safely run in parallel.
---

# Manage Subagents

Subagents are tools for bounded specialization: exploration, one implementation slice, or independent review. They are not the default way to work.

## Core Rule

Delegate bounded work, not responsibility. The parent owns scope, integration, review triage, and final verification.

## Use Or Avoid

Use subagents when at least one is true:

- The user explicitly asks for subagents or parallel agents.
- Two or more read-only questions can be answered independently.
- One implementation slice has clear scope, clear files, and clear checks.
- A completed slice needs independent spec or quality review.
- Broad review benefits from separate perspectives over non-overlapping areas.

Avoid subagents when:

- The next step depends on one result you need immediately.
- Work is tightly coupled across the same files or shared state.
- You would only be outsourcing judgment the parent must own.
- A simple local inspect/edit/check loop is cheaper.

## Roles

| Role | Use for | Template |
| --- | --- | --- |
| Explorer | Read-only investigation, code mapping, reproduction evidence, options | `templates/explorer.md` |
| Implementer | One vertical slice or disjoint file scope with checks | `templates/implementer.md` |
| Spec reviewer | Did the work match request, plan, and acceptance criteria? | `templates/spec-reviewer.md` |
| Quality reviewer | Correctness, regression risk, security/data risk, maintainability, tests | `templates/quality-reviewer.md` |

Use spec review before quality review. If spec is wrong or incomplete, quality review is premature.

## Packet Rules

- Give each subagent a tight task packet, not the whole conversation.
- Include exact scope, allowed files, forbidden scope, expected output, and evidence required.
- Name the controlling skill for implementation packets: `tdd-slice` for behavior changes, `diagnose-loop` for failing or unexplained symptoms, or `codebase-cleanup` for behavior-preserving refactors.
- Include only the `CONTEXT.md` terms needed for the task; do not dump the whole file by default.
- Paste the task or question into the packet; do not make the subagent reconstruct it from a plan or long thread.
- Prefer read-only explorers and reviewers.
- Do not run parallel implementation on overlapping files.
- Tell implementers they are not alone in the codebase and must preserve others' work.
- Do not trust subagent success claims without parent inspection.
- Do not let subagents make unchecked product, architecture, dependency, or scope decisions.

Base packet:

```text
Role:
Task:
Context:
Controlling skill:
Shared terms:
Allowed files/scope:
Forbidden scope:
First check:
Expected output:
Verification command:
Risks:
```

## Coordination

1. Decide whether subagents add enough value to pay the context, time, and integration cost.
2. Split by subsystem, question, or file ownership. Do not split only to keep agents busy.
3. Dispatch independent read-only work in parallel when possible.
4. Keep implementation write scopes disjoint. If scopes overlap, run sequentially or keep one parent-owned.
5. Let subagents propose `CONTEXT.md` updates, but the parent decides and verifies before editing durable docs.
6. Handle implementer status:
   - `DONE`: inspect diff and proceed to review.
   - `DONE_WITH_CONCERNS`: read concerns before review; address correctness or scope concerns first.
   - `NEEDS_CONTEXT`: provide missing context or narrow the task before retrying.
   - `BLOCKED`: change something: more context, smaller task, stronger model, different route, or user decision.
7. Never force the same blocked task to retry unchanged.
8. Inspect outputs and diffs yourself.
9. Rerun the parent-level checks before claiming completion.

## Review Triage

When multiple reviewers report findings:

1. Normalize and deduplicate.
2. Group by spec gap, correctness bug, test gap, security/data risk, maintainability, or style.
3. Rank:
   - Blocker: wrong behavior, missing acceptance criterion, data/security risk, failing required check.
   - Important: likely regression, weak test coverage, fragile boundary, unclear ownership.
   - Minor: naming, readability, local polish.
4. Verify findings against source, diff, and tests.
5. Resolve conflicts by requirements and tests. If still ambiguous, prefer the smaller reversible change or ask the user.
6. Produce one fix list.
7. Rerun parent verification after fixes.

## Output

```text
Subagents used:
Findings accepted:
Findings rejected:
Fixes made:
Parent verification:
Residual risk:
```
