---
name: verify-before-done
description: Use before claiming work is done, fixed, passing, ready, reviewed, safe to merge, or before creating/merging a PR after coding changes.
---

# Verify Before Done

Evidence before completion claims. Diff review before trusting passing checks.

## Rule

Do not make completion or safety claims until fresh evidence after the final edit supports the exact wording.

Narrow evidence supports narrow claims.

## Completion Gate

Before any completion claim:

1. List the claims you are about to make.
2. Map each claim to evidence: command, test, diff inspection, or repeatable check.
3. Choose the smallest sufficient checks:
   - Focused check for the changed behavior or reproduced bug
   - Relevant surrounding tests for the touched area
   - Typecheck, lint, build, or smoke check when integration risk exists
   - CI or PR status on the latest commit for PR or merge readiness
4. Run checks after the final edit.
5. Read exit code, output, skipped tests, warnings, and path coverage.
6. Downgrade unsupported claims.

## Evidence Rules

- A check run before the final edit does not support the final claim.
- A passing command that does not exercise the changed path is weak evidence. Say so.
- A simulation, dry run, read-only review, or "would do" answer does not support a claim that behavior was execution-tested.
- Passing tests do not prove requirements are met; inspect the diff against the request or acceptance checks.
- Subagent reports count only after the parent inspects the diff or reruns the relevant check.
- Manual checks count only when the exact steps and observed result are recorded.
- If verification cannot run, state the blocker and the strongest weaker evidence.

## Diff Review

Inspect the diff against the request:

- Every changed file should trace to the request, an acceptance check, or a named risk-reduction step
- Missing acceptance criteria
- Evidence that is weaker than the requested success criterion, such as simulated tests reported as behavior tests
- Behavior outside scope
- Missing or weak tests
- Tests that only prove mocks, snapshots, or test-only production hooks
- Security, data, concurrency, or migration risk
- Unnecessary complexity
- Drive-by formatting or unrelated refactor
- User changes overwritten or mixed in
- `CONTEXT.md` entries that record progress, plans, status, or claims instead of shared meaning
- New or renamed shared terms without a matching `CONTEXT.md` update or stated reason to skip it

Block completion for wrong behavior, failing required checks, missing acceptance criteria, overwritten user work, or unhandled security/data/migration risk. Defer minor naming, readability, or docs only when the outcome is unchanged; say so.

## Review Feedback

Review comments are claims to evaluate, not orders.

- Verify against current code before implementing.
- If multiple review items are related and any are unclear, clarify before implementing a partial subset.
- Push back when technically wrong or out of scope.
- Fix blockers first.
- Fix important issues before completion unless explicitly deferred.
- Drop minor churn when it does not improve the outcome.
- No empty agreement. State the technical fix or reason.

## If Review Finds Work

- Missing or unclear target behavior -> `clarify-scope`.
- Missing behavior check or approved behavior change -> `tdd-slice`.
- Unexplained failure or regression -> `diagnose-loop`.
- Behavior-preserving structure problem -> `codebase-cleanup`.
- Dirty tree, staging, commit, branch, or destructive-operation risk -> `workspace-safety`.
- Issue, PRD, PR body, CI status, or durable tracking gap -> `github-work-tracking`.

## Verification Report

```text
Changed:
- ...

Verified:
- `<command>` -> pass|fail|not run (<reason>)

Claims supported:
- ...

Claims not fully supported:
- ...

Still uncertain:
- ...

Next useful action:
- ...
```

If verification fails, do not claim done. State the failure and smallest next action.
