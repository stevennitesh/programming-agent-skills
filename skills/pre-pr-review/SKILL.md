---
name: pre-pr-review
description: Use when reviewing a branch, commit, working tree, or PR-ready diff before opening or updating a pull request; when asked for pre-PR review, PR readiness, bug finding, regression review, code review, review before merge, or review with Codex; and when the review should focus on actionable correctness, security/privacy, data, contract, test, dependency/config, performance, or migration issues introduced by the diff.
---

# Pre-PR Review

Review code changes before a pull request as a semantic gate. Find real issues introduced or exposed by the diff, keep noise low, and make the remaining risk explicit.

Do not edit source during a review unless the user asks for fixes. If you switch from reviewing to fixing, say so and route to the relevant implementation or diagnosis workflow.

## Start

First identify the review target:

- Working tree or staged changes.
- Branch against a base branch.
- One commit or commit range.
- Existing PR head.
- User-supplied diff.

Record the base and head when Git evidence is available. If the base is unclear and choosing the wrong base could change findings, inspect branch tracking, merge base, PR metadata, or ask.

If Codex CLI review is available, prefer it for the target:

```bash
codex review --uncommitted
codex review --base <base>
codex review --commit <sha>
```

Use this instruction unless the user gives a narrower one:

```text
Review this as a pre-PR review. Focus only on actionable issues introduced or exposed by this diff. Ignore style issues covered by formatter/linter and avoid broad rewrites. Prioritize correctness/regression, security/privacy, data integrity, caller contract drift, missing or weak tests, dependency/config/build/migration risk, and performance/concurrency on plausible paths. For each finding include file/line or symbol, failure mechanism, severity: blocking / should-fix / optional, smallest safe fix, and validation. Also report observed or recommended checks, missing tests or weak evidence, final verdict: Safe to PR / PR after fixes / Do not PR yet, confidence, and remaining uncertainty.
```

If `codex review` fails or is interrupted, label the result as manual self-review fallback. Do not present it as a completed built-in review.

## Evidence Order

1. Read repo instructions first: `AGENTS.md`, nested instructions for touched paths, and repo docs that define commands, contracts, or review rules.
2. Inspect the diff before reading broad unrelated source.
3. Read affected callers, tests, fixtures, docs, configs, CI/check definitions, and generated-contract files only as needed to verify behavior.
4. Run cheap relevant deterministic checks when they are known and fit the risk. Separate commands actually run from commands only recommended.
5. For high-risk or commit-gate reviews, include the repo standard check if one exists or explain why it was not run.

Use docs and plans as intent. Use source, tests, fixtures, diffs, command output, CI, and PR review threads as proof.

## Finding Standard

A valid finding must satisfy all of these:

- Introduced or exposed by this diff.
- Actionable by the author.
- Supported by file/line or symbol evidence, a concrete execution path, a violated contract, a failing or missing check, or current tool output.
- More important than formatter, linter, grammar, or style noise.

Suppress:

- Vague concerns without a failure mechanism.
- Broad rewrites or architecture preferences not required by the diff.
- Off-diff issues unless they are newly exposed by this change.
- Style-only, grammar-only, or naming comments unless the user asked for editorial polish.
- Optional helper extraction unless duplication creates a concrete failure, test gap, or maintenance hazard in the changed path.
- Findings that cannot name a minimal fix or validation path.

When you find one concrete bug class, search the touched area for neighboring instances before final verdict. Do not stop after the first example.

## Review Lenses

Use only the lenses that match the diff, but make the choice explicit for nontrivial reviews.

### Data And Schema

Use when the diff touches CSV/parquet/JSON artifacts, dataframes, validation, manifests, schemas, model inputs, reports, or analytics outputs.

Check marker columns and selection flags carefully: `.astype(bool)`, `.astype(int)`, numeric casts, `dropna`, string booleans, fractional values, missing values, and non-numeric values. Tests should cover malformed inputs and round-trip encodings, not only in-memory happy paths.

### Broad Refactor And Removed Surface

Use when code moves, modules split/merge, routes/commands/UI controls are removed, or ownership boundaries change.

Sweep for stale references in callers, tests, README, active specs, visible docs, CLI help, fixtures, and generated outputs. If docs conflict with source, classify whether the doc is active authority, stale background, or an implementation gap.

When boundary tests are added, check alternate import forms such as `import package.submodule`, `from package.submodule import x`, and `from package import submodule`.

### Config And Generated Names

Use when the diff touches config parsing, policy/action settings, thresholds, generated identifiers, feature names, or deduplication.

Reject ambiguous booleans, non-finite floats, and silent coercion. Check for generated-name collisions before deduplication, rounding, normalization, or hashing hides distinct inputs.

### Performance, Cache, And Hot Path

Use when the diff changes caching, memoization, benchmark/runtime paths, preflight checks, dashboard/report timing, or fast paths.

Check cache key completeness, stale cache identity, hot/cold path equivalence, skip status, CLI exit semantics, timing counter correctness, and producer-consumer ordering for reports, gates, dashboards, manifests, or summaries. Passing unit tests or faster runtime does not prove the hot path measures the intended thing.

If a fast path prunes payloads, metrics, columns, or objects before shared ranking or selection logic, verify that all tie-breakers and downstream semantics remain equivalent.

### Dependency, Build, And Runtime

Use when the diff changes `pyproject.toml`, requirements or lock files, package pins, build-system pins, install commands, Python or language version support, tool target versions, CI setup, or Makefile/package scripts.

Cross-check the advertised runtime floor against every pinned runtime, build, and test dependency. If package metadata is missing, require install/import evidence, upstream docs, or an explicit repo note. Also check tool target versions, install order, editable install behavior, and metadata tests.

### Tests And Checks

For each changed behavior, ask what test would fail on the old bug. Weak signs:

- Only happy-path tests for validation changes.
- Tests that assert implementation details but not caller-facing behavior.
- No negative cases for malformed config, stale caches, removed surfaces, or boundary imports.
- A clean full suite but no focused test for the risky branch.
- A skipped or failing check whose output is not triaged.

## Subagents

Use subagents only when the user, repo instructions, or approved plan authorizes them and the environment permits delegation.

Subagent fan-out is justified for broad or high-risk diffs with separable lenses, such as data/schema, security/privacy, tests, dependency/build, performance/cache, migration, API/CLI/UI contract, or removed-surface review.

If subagents are unavailable or unauthorized, run the same lenses locally and label the result as self-review. The parent must deduplicate and verify all findings against source, diff, tests, logs, command output, CI, or PR review threads.

## Verdict Rules

Use one verdict:

- `Safe to PR`: no blocking or should-fix findings found, relevant checks are green or remaining checks are low-risk and named.
- `PR after fixes`: should-fix findings, missing focused tests, or unresolved validation gaps remain.
- `Do not PR yet`: blocking correctness, security/privacy, data loss, broken build/install/test, migration, dependency, or caller contract risk exists.

Before returning `Safe to PR`, do a clean-verdict pass:

- Recheck the selected lenses against the diff.
- Name the strongest evidence supporting the clean verdict.
- Name unrun checks, skipped tests, collapsed transcript gaps, unavailable tools, or areas not inspected.
- Avoid saying "review passed" if review tooling failed and only manual fallback ran.

## Output

Lead with findings. Keep summaries secondary.

```text
Review path:
Target:
Base:
Risk lenses:

Blocking findings:
- B1. <title>
  Severity:
  File/line or symbol:
  Issue:
  Failure mechanism:
  Minimal fix:
  Validation:

Should-fix findings:
- S1. <title>
  Severity:
  File/line or symbol:
  Issue:
  Failure mechanism:
  Minimal fix:
  Validation:

Missing or weak tests:
- ...

Optional:
- Only unusually high-leverage optional items.

Checks:
- Observed:
- Recommended:

Verdict:
Confidence:
Remaining uncertainty:
Next action:
```

If there are no findings, write `No blocking findings` and `No should-fix findings`; still include checks, verdict, confidence, and remaining uncertainty.

## Stop Or Reroute

Stop or reroute when:

- Target behavior, base branch, source authority, dependency/runtime support, data/security risk, migration semantics, or caller contract needs a human decision.
- The review command fails and no equivalent self-review can be performed from repo evidence.
- A deterministic check fails and the cause is not understood; use `diagnose-loop`.
- The user asks to fix findings; use `tdd-slice`, `diagnose-loop`, or a small inspect/edit/check loop.
- PR threads, CI, or review status matter; use `github-tracking`.
- Subagents are requested or an approved review plan calls for them; use `subagent-workflow`.
- You are about to claim the change is ready, reviewed, safe, or mergeable after edits; use `verify-before-done`.

## Handoff

- `github-tracking`: live PR metadata, review threads, CI, or review-response tracking.
- `subagent-workflow`: authorized multi-lens independent review.
- `diagnose-loop`: failing checks, crashes, regressions, or unclear command output.
- `tdd-slice`: fixing an approved finding with a behavior check.
- `verify-before-done`: before readiness or merge-safety claims.
