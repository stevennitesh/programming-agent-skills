# Implementer Template

Use for one caller-visible implementation slice with clear file/module ownership.
For parallel implementation, use only when the plan or issue mode allows it and `worktree-isolation` has assigned the branch/worktree.

```text
Role: Implementer
Task: <one slice, pasted in full>
Context: <where this fits, constraints, public or caller contract, acceptance criteria>
Controlling skill: <tdd-slice | diagnose-loop | codebase-cleanup | micro-loop>
Execution mode: <sequential | parallel-disjoint | parallel-overlap>
Parallel group: <none | group name>
Issue claim: <claim status, issue number, or none>
Worktree/branch: <path and branch, or parent workspace>
Builds on / must preserve: <prior issue result, source path, helper, test, contract, behavior, or none>
Existing logic to reuse or extend: <established implementation path, or why this slice is independent>
Owned files/modules: <owned files, directories, modules, fixtures, or docs>
Forbidden files/behaviors: <files, caller-visible behaviors, dependencies, refactors, generated output, external actions>
First check: <test, search, or file read that should happen first>
Acceptance check: <observable behavior, regression check, diff review target, or issue criterion>
Verification command: <focused check plus broader check if known>
Scope:
- Preserve existing user and agent changes.
- Implement exactly this slice; do not solve adjacent tasks.
- Reuse, extend, or refactor the established implementation path. Do not create a competing path for the same behavior without parent approval.

Implementation:
- Start from the first check and current repo evidence, not from a task title, stale summary, or guessed file list.
- For behavior changes, start with or identify one failing caller-visible check.
- Apply the smallest source change that satisfies the acceptance check.
- Self-review changed files, scope, caller-visible behavior, test evidence, and overbuild risk before reporting.

Stop states:
- NEEDS_CONTEXT when owned scope, forbidden scope, first check, acceptance criteria, public or caller contract, dependencies, approach, or verification evidence is missing.
- BLOCKED when safe progress requires a user or parent decision about behavior, architecture, public contract, dependency, migration, or broad refactor scope.
- DONE_WITH_CONCERNS when the slice is complete but correctness, scope, or evidence is uncertain.

Report:
- Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files changed.
- Checks run and exact results.
- Source change.
- Caller-visible behavior or contract affected.
- Acceptance check result.
- Risks, concerns, or blockers.
```
