---
name: manage-subagents
description: Use when the user asks for subagents, parallel agents, worker agents, independent review, or multi-agent exploration; or when the current environment permits delegation and several independent tasks can safely run in parallel.
---

# Manage Subagents

Subagents are tools for bounded specialization: exploration, one implementation slice, or independent review. They are not the default way to work.

## Core Rule

Delegate bounded work, not responsibility. The parent owns scope, integration, review triage, and final verification.

## Use Or Avoid

Use subagents when the current environment permits delegation and at least one is true:

- The user explicitly asks for subagents or parallel agents.
- Two or more read-only questions can be answered independently.
- One implementation slice has clear scope, clear files, and clear checks.
- A completed slice needs independent spec or quality review.
- Broad review benefits from separate perspectives over non-overlapping areas.

Avoid subagents when:

- The current environment, policy, or user instruction does not permit delegation.
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

For delegated implementation slices, reviewers are a gate, not an optional perspective. Run both reviewers before marking the slice complete unless review subagents are unavailable or the user explicitly asks to skip review. If a slice is tiny enough that local self-review is clearly cheaper, avoid delegation up front instead of dispatching an implementer and skipping reviewers. Record any skip reason. If subagents are unavailable, run the same gates yourself and label them as self-review, not independent review.

When dispatching a role that has a template, start from that template by default. Copy or adapt its fields into the packet instead of rebuilding the packet from memory. Use the base packet only for unusual roles, tiny one-off tasks, or when a role template would add no useful control; if you skip an applicable template, say why in the parent notes or final report.

## Packet Rules

- Give each subagent a tight task packet, not the whole conversation.
- Choose the role first, then use that role's template as the packet skeleton when one exists.
- Include exact scope, allowed files, forbidden scope, expected output, and evidence required.
- Name the controlling skill for implementation packets: `tdd-slice` for behavior changes, `diagnose-loop` for failing or unexplained symptoms, or `codebase-cleanup` for behavior-preserving refactors.
- Include only the `CONTEXT.md` terms needed for the task; do not dump the whole file by default.
- Paste the task or question into the packet; do not make the subagent reconstruct it from a plan or long thread.
- Prefer read-only explorers and reviewers.
- Do not run parallel implementation on overlapping files.
- Tell implementers they are not alone in the codebase and must preserve others' work.
- Do not trust subagent success claims without parent inspection.
- Do not let subagents make unchecked product, architecture, dependency, or scope decisions.

Base packet for custom roles or fallback use:

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

## Reviewer Gate

Use this gate after an implementer reports `DONE` or `DONE_WITH_CONCERNS`.

1. Parent inspects the diff before spawning reviewers. If the diff is obviously off-scope, send it back to implementation before review.
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

For multi-slice work, run one final parent diff review after all slices. Add a final quality reviewer over the whole diff when slices touch shared contracts, cross-module behavior, migrations, security/data boundaries, or integration points.

## Coordination

1. Decide whether subagents add enough value to pay the context, time, and integration cost.
2. Split by subsystem, question, or file ownership. Do not split only to keep agents busy.
3. Dispatch independent read-only work in parallel when possible.
4. Keep implementation write scopes disjoint. If scopes overlap, run sequentially or keep one parent-owned.
5. Let subagents propose `CONTEXT.md` updates, but the parent decides and verifies before editing durable docs.
6. Handle implementer status:
   - `DONE`: inspect diff and run the Reviewer Gate.
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
Review gates:
Findings accepted:
Findings rejected:
Fixes made:
Parent verification:
Residual risk:
```
