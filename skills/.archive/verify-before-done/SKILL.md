---
name: verify-before-done
description: "Use before claiming repo work is done, fixed, passing, reviewed, ready, resolved, clean, safe to merge, mergeable, or complete; calibrates claim strength to fresh evidence."
---

# Verify Before Done

Calibrate completion and readiness claims to fresh repo evidence. This is a gate, not a semantic review workflow.

## Rule

Before saying done, fixed, passing, reviewed, ready, resolved, clean, safe, mergeable, or complete, write the exact claim and prove only that claim.

First visible move:

```text
Claim:
Final edit point:
Evidence after final edit:
Diff checked: yes|no
Supported wording:
```

Narrow evidence supports narrow claims. If evidence is weak, stale, partial, simulated, missing, or does not cover the touched behavior or risk, downgrade the wording.

Do not turn "I ran a command" into "the work is done." The check, diff review, CI/PR state, review state, or manual observation must support the exact claim.

Do not use this skill to perform semantic PR review or review-comment resolution. Route that work through `coding-router`.

## Fast Claim Check

Use for tiny edits, narrow reports, doc-only changes, read-only answers, and small local fixes.

1. Write the exact claim.
2. Name the final edit point, or `none` for read-only work.
3. Name evidence gathered after the final edit: command, test, diff inspection, source read, CI/PR state, review state, or manual step.
4. Check the diff when local files changed.
5. State the strongest supported wording.

For small work, one line is enough:

```text
Verified: <claim> supported by <evidence>; remaining risk: <risk|none named>.
```

## Full Gate

Use for behavior changes, PR/merge readiness, generated/config/workflow changes, broad cleanup, public or caller risk, or when the requested claim is stronger than local evidence.

- Inspect the final diff against the request and scope; separate unrelated dirty work.
- Run the smallest sufficient check after the final edit; say what it covers and what it does not cover.
- Check CI, PR, branch, mergeability, and review-thread state only when that state is part of the claim.
- Name skipped checks, warnings, flakes, unrelated failures, manual-only evidence, and residual risk.
- Downgrade unsupported claims.

## Diff Review

When files changed, inspect the diff for:

- changes outside the request or accepted scope
- behavior outside scope, missing acceptance coverage, or weak test surface
- evidence that does not exercise the touched path or stated risk
- unrelated user work, generated output, config, dependency, migration, or workflow changes
- failed, skipped, stale, simulated, or pre-final-edit evidence

Diff review is not a substitute for `pre-pr-review`. If semantic review is the job, return to `coding-router`.

## Stop Or Downgrade

Stop, reroute, or downgrade the claim when:

- the final edit happened after the last relevant check, diff review, CI/PR state check, or manual observation
- the check does not cover the touched behavior, public or caller contract, source path, config/workflow change, generated output, or named risk
- the diff was not inspected
- CI, review, branch, merge, or PR state matters but was not checked
- evidence is simulated, stale, manual confidence, or subagent-only
- failures, warnings, flakes, or unrelated changes are unexplained
- the requested wording is stronger than the evidence supports

## Handoff

If proving the claim reveals new work, return to `coding-router`.

Use `pre-pr-review` for semantic diff review, `diagnose-loop` for unexplained failures, `workspace-safety` for overlapping dirty paths or Git risk, `github-tracking` for durable issue/PR records, and GitHub plugin skills or tools for live PR/comment/CI state.

## Report

For small work, use the one-line Fast Claim Check report.

For nontrivial work:

```text
Claim:
Evidence:
Diff review:
Unsupported or downgraded claims:
Remaining risk:
```
