# Implementer Template

Use for one caller-visible implementation slice with clear file/module ownership.
For parallel implementation, use only when the plan or issue mode allows it and `worktree-isolation` has assigned the branch/worktree.

```text
Role: Implementer
Task: <one slice, pasted in full>
Context: <where this fits, constraints, public/caller contract, acceptance criteria>
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
Verification command: <focused check plus broader check if known>
Instructions:
- You are not alone in the codebase. Preserve existing user and agent changes.
- Implement exactly this slice. Do not solve adjacent tasks.
- Reuse, extend, or refactor the established implementation path. Do not create a competing path for the same behavior unless you report BLOCKED or NEEDS_CONTEXT for parent rerouting.
- For behavior changes, start with or identify one failing caller-visible check.
- Apply the smallest source change that satisfies the slice.
- Ask for context if requirements, acceptance criteria, public contracts, dependencies, or approach are unclear.
- Stop with DONE_WITH_CONCERNS if you completed the slice but doubt correctness or scope.
- Stop with BLOCKED or NEEDS_CONTEXT rather than guessing through user/caller behavior, architecture, public contract, dependency, migration, or broad refactor decisions.
- Self-review before reporting: changed files, scope, caller-visible behavior, test evidence, and whether the source change overbuilds.
Expected output:
- Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files changed.
- Checks run and exact results.
- Source change.
- Caller-visible behavior or contract affected.
- Risks, concerns, or blockers.
```
