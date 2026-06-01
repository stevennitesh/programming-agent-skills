---
name: verify-before-done
description: Use before claiming repo work is done, fixed, passing, reviewed, ready, safe to merge, or before creating/merging a PR after source, test, config, docs, or workflow changes.
---

# Verify Before Done

Repo evidence before completion claims. Diff review before trusting passing checks.

## Rule

Do not make completion, correctness, readiness, or merge-safety claims until fresh repo evidence after the final edit supports the exact wording.

Narrow evidence supports narrow claims.

## Completion Gate

Before any completion claim:

1. List the claims you are about to make.
2. Map each claim to fresh evidence: command/test/fixture, diff inspection, PR/CI status, or repeatable manual check.
3. Choose the smallest sufficient checks:
   - Focused check for the changed caller-visible behavior, public contract, or reproduced bug
   - Relevant surrounding tests for the touched source modules, commands, UI/API paths, or fixtures
   - Typecheck, lint, build, or smoke check when integration risk exists
   - CI or PR status on the latest commit or head SHA for PR or merge readiness
4. Run checks after the final edit.
5. Read exit code, output, skipped tests, warnings, touched-path coverage, and whether the command exercised the changed behavior.
6. Downgrade unsupported claims.

## Evidence Rules

- A check run before the final edit does not support the final claim.
- A passing command that does not exercise the changed caller-facing entry point, source module, fixture, or workflow is weak evidence. Say so.
- A simulation, dry run, read-only review, or "would do" answer does not support a claim that behavior was execution-tested.
- Passing tests do not prove the approved request is met; inspect the diff against the request, public contract, and acceptance checks.
- Subagent reports count only after the parent inspects changed files, diffs, or reruns the relevant command.
- Self-review or local fallback review supports only a self-review claim. It does not support "independently reviewed", "reviewed by a separate agent", or "reviewed by GitHub reviewers".
- Review claims should name the review path: self-review, parent diff review, subagent review, GitHub review, CI/check review, or another explicit source.
- Manual checks count only when the exact steps, environment, input/state, and observed result are recorded.
- If verification cannot run, state the blocker and the strongest weaker evidence.

## Diff Review

Inspect the working-tree or PR diff against the request:

- Every changed source, test, docs, config, generated, or workflow file should trace to the request, an acceptance check, or a named risk-reduction step
- Missing acceptance criteria or public contract details
- Evidence that is weaker than the requested success criterion, such as simulated tests reported as behavior tests
- Caller-visible behavior outside scope
- Missing or weak tests
- Tests that only prove mocks, snapshots, or test-only implementation hooks
- Security, data/state, concurrency, dependency, config, or migration risk
- Unnecessary complexity
- New competing implementation path that ignores established logic, prior issue results, helpers, tests, contracts, or source paths the task was supposed to reuse or preserve
- Drive-by formatting or unrelated refactor
- User changes overwritten or mixed in
- `CONTEXT.md` entries that record progress, plans, status, or claims
- New or renamed durable terms, module boundaries, or public contracts without a `CONTEXT.md` update or stated skip reason

Block completion for wrong behavior, failing required checks, missing acceptance criteria, overwritten user work, or unhandled security/data/dependency/migration risk. Defer minor naming, readability, or docs only when caller-visible behavior and verification outcome are unchanged; say so.

## PR Or Merge Readiness

Before claiming a branch, PR, review response, or merge is ready:

- Confirm the final diff matches the request, linked issue/PRD, review feedback, and accepted scope.
- Run or inspect checks after the final source, test, config, docs, workflow, or generated-file edit.
- Check CI or PR status on the latest head SHA when CI or merge readiness is part of the claim.
- Check unresolved review threads or requested changes before claiming review feedback is addressed.
- Ensure the PR body or final report lists source/test/config/docs/workflow changes, checks run, known CI status, and residual risk.
- Distinguish local checks, self-review, parent diff review, subagent review, GitHub review, CI status, and branch protection; do not let one evidence type stand in for another.
- Do not claim merge safety from local checks alone when branch protection, CI, required reviews, migrations, or release gates still matter.

## Review Feedback

Review comments, inline PR feedback, and CI failures are claims to evaluate, not orders.

- Read the full review or failing check context before changing code.
- Verify each item against current source, tests, docs, CI output, and accepted scope.
- If related items are unclear, clarify before implementing a partial subset.
- Fix blockers first, then important correctness, test, data/state, security, dependency/config, or maintainability issues.
- Push back with evidence when feedback is technically wrong, stale, unsafe, or outside the approved scope.
- Drop minor churn when it does not improve correctness, maintainability, test coverage, or caller-visible behavior.
- After each fix or tightly related group, run the relevant check and report the changed files plus evidence.
- No empty agreement. State the technical fix, check result, or reason.

## If Review Finds Work

- Missing or unclear target behavior, public contract, or acceptance check -> `clarify-scope`.
- Missing caller-visible behavior check or approved behavior change -> `tdd-slice`.
- Unexplained failing test, bug, regression, flaky check, log error, or build failure -> `diagnose-loop`.
- Behavior-preserving source structure or testability problem -> `codebase-cleanup`.
- Dirty tree, staging, commit, branch, generated-output, dependency install, or destructive-operation risk -> `workspace-safety`.
- Issue, PRD, PR body, CI status, review thread, or long-lived tracking gap -> `github-tracking`.

## Verification Report

```text
Changed files/behavior:
- ...

Verified:
- `<command>` -> pass|fail|not run (<reason>)

Review evidence:
- ...

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
