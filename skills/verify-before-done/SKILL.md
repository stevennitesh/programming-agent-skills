---
name: verify-before-done
description: Use before claiming repo work is done, fixed, passing, reviewed, ready, resolved, clean, safe to merge, mergeable, or before creating/merging a PR after source, test, config, docs, or workflow changes.
---

# Verify Before Done

Repo evidence before completion claims. Diff review before trusting passing checks.

## Rule

Do not make completion, correctness, readiness, or merge-safety claims until fresh repo evidence after the final edit supports the exact wording.

Narrow evidence supports narrow claims.

When this skill triggers, first write the exact claim you are about to make. This changes the route from doing work to proving the claim. Do not use casual completion language such as "done", "fixed", "ready", "safe", "passing", "reviewed", "addressed", or "clean" unless the evidence below supports that exact word.

Claim-ready evidence means:

- Final edit point is known: source, test, docs, config, workflow, generated output, issue/PR metadata, or branch state changed no later than the evidence run.
- Diff scope was inspected against the request, accepted scope, public or caller contract, and acceptance checks.
- Each claim maps to fresh evidence: command output, test result, fixture, diff review, CI/PR state, review-thread state, or recorded manual check.
- The evidence covers the touched path or the claim is downgraded.
- Remaining uncertainty, skipped checks, warnings, flakes, or unrelated failures are named.

Do not turn "I ran a command" into "the work is done." Verification supports claims only when the command and diff review cover the requested behavior, source scope, and risk.

## Completion Gate

Before any completion claim:

1. List the claims you are about to make.
2. Name the final edit point and changed path types: source, tests, docs, config, workflow, generated output, issue/PR metadata, branch state, or none.
3. Map each claim to fresh evidence: command/test/fixture, diff inspection, PR/CI status, review-thread state, or repeatable manual check.
4. Choose the smallest sufficient checks:
   - Focused check for the changed caller-visible behavior, public or caller contract, or reproduced bug
   - Relevant surrounding tests for the touched source modules, commands, UI/API paths, or fixtures
   - Typecheck, lint, build, or smoke check when integration risk exists
   - CI or PR status on the latest commit or head SHA for PR or merge readiness
5. Run checks after the final edit.
6. Inspect the final diff before the report.
7. Read exit code, output, skipped tests, warnings, touched-path coverage, and whether the command exercised the changed behavior.
8. Downgrade unsupported claims.
9. If evidence fails or points to an unexplained problem, do not claim completion; route to the controlling fix workflow.

## Evidence Rules

- A check run before the final edit does not support the final claim.
- A passing command that does not exercise the changed caller-facing entry point, source module, fixture, or workflow is weak evidence. Say so.
- A simulation, dry run, read-only review, or "would do" answer does not support a claim that behavior was execution-tested.
- Passing tests do not prove the approved request is met; inspect the diff against the request, public or caller contract, and acceptance checks.
- For cleanup claims such as "nothing useful remains", "cleanup is exhausted", or "the requested scope is cleaned up", passing tests only support behavior preservation. Require the `codebase-cleanup` coverage ledger with inspected scope, searches/checks, remaining low-return/risky/out-of-scope items, and uninspected areas.
- Subagent reports count only after the parent inspects changed files, diffs, or reruns the relevant command.
- Self-review or local fallback review supports only a self-review claim. It does not support "independently reviewed", "reviewed by a separate agent", or "reviewed by GitHub reviewers".
- Review claims should name the review path: self-review, parent diff review, subagent review, GitHub review, CI/check review, or another explicit source.
- Manual checks count only when the exact steps, environment, input/state, and observed result are recorded.
- If verification cannot run, state the blocker and the strongest weaker evidence.
- "Not run" is an evidence result, not a pass. Pair it with a reason and the claim it leaves unsupported.
- An issue update, PR comment, plan note, or status summary is not proof unless it points to current source, diff, check, CI, or review-thread evidence.

## Diff Review

Inspect the working-tree or PR diff against the request:

- Every changed source, test, docs, config, generated, or workflow file should trace to the request, an acceptance check, or a named risk-reduction step
- Missing acceptance criteria or public or caller contract details
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
- New or renamed durable terms, module boundaries, or public or caller contracts without a `CONTEXT.md` update or stated skip reason

Block completion for wrong behavior, failing required checks, missing acceptance criteria, overwritten user work, or unhandled security/data/dependency/migration risk. Defer minor naming, readability, or docs only when caller-visible behavior and verification outcome are unchanged; say so.

If the diff includes unrelated files or user changes, separate them in the report. Do not let unrelated dirty work support or weaken claims about the requested slice.

## PR Or Merge Readiness

Before claiming a branch, PR, review response, or merge is ready:

- Confirm the final diff matches the request, linked issue/PRD, review feedback, and accepted scope.
- Run or inspect checks after the final source, test, config, docs, workflow, or generated-file edit.
- Check CI or PR status on the latest head SHA when CI or merge readiness is part of the claim.
- Check unresolved review threads or requested changes before claiming review feedback is addressed.
- Ensure the PR body or final report lists source/test/config/docs/workflow changes, checks run, known CI status, and residual risk.
- Distinguish local checks, self-review, parent diff review, subagent review, GitHub review, CI status, and branch protection; do not let one evidence type stand in for another.
- Do not claim merge safety from local checks alone when branch protection, CI, required reviews, migrations, or release gates still matter.
- Do not claim review feedback is resolved from a local fix alone; inspect unresolved review threads, requested-changes state, or the relevant review source when that state is part of the claim.

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

## Stop Or Downgrade

Stop, reroute, or downgrade the claim when:

- The final edit happened after the last relevant command, CI status, diff review, or manual check.
- The check does not exercise the changed caller-visible or user-visible behavior, public or caller contract, source module, fixture, workflow, or risk named in the claim.
- The diff has not been inspected against the approved request, accepted scope, acceptance checks, and unrelated dirty work.
- Required checks fail, skip unexpectedly, warn about the touched path, or produce output the agent does not understand.
- CI, branch protection, review approvals, review threads, mergeability, or latest head SHA matter but were not checked.
- The evidence is only a simulation, dry run, stale summary, subagent claim, old command output, or manual confidence.
- The requested wording is stronger than the evidence, such as "fixed" when only a narrow smoke passed, "passing" when only one focused test ran, or "safe to merge" when CI/reviews were not checked.
- A failure or review finding needs more investigation; use `diagnose-loop`, `tdd-slice`, `codebase-cleanup`, `github-tracking`, or `clarify-scope` rather than reporting done.

## If Review Finds Work

- Missing or unclear target behavior, public or caller contract, or acceptance check -> `clarify-scope`.
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
- `<command>` -> pass|fail|not run (<reason>; what it covers)

Review evidence:
- ...

Claims supported:
- ...

Claims not fully supported:
- ...

Downgraded wording:
- ...

Still uncertain:
- ...

Next useful action:
- ...
```

If verification fails, do not claim done. State the failure and smallest next action.
