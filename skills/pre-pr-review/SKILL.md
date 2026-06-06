---
name: pre-pr-review
description: Use when reviewing a branch, commit, working tree, or PR-ready diff before opening or updating a pull request; when asked for pre-PR review, PR readiness, bug finding, regression review, code review, review before merge, or review with Codex; and when the review should focus on actionable correctness, security/privacy, data, contract, test, dependency/config, performance, or migration issues introduced by the diff.
---

# Pre-PR Review

Review code changes before a pull request as a semantic gate. Find real issues introduced or exposed by the diff, keep noise low, and make the remaining risk explicit.

In this skill, "review" means tracing changed behavior through the code that produces it, the code that consumes it, and the tests or checks that would catch it. Reading the diff alone is not enough for a nontrivial review.

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

Do not pass a custom prompt or stdin prompt when using `--base`, `--commit`, or `--uncommitted`. Some CLI builds list a prompt argument in help but reject target flags combined with custom instructions. Run the target-specific command first, then apply this skill's review loop yourself as the manual lens pass. Do not print a compatibility warning for this expected path.

Use this instruction for the manual lens pass unless the user gives a narrower one:

```text
Review this as a pre-PR review. Focus only on actionable issues introduced or exposed by this diff. Ignore style issues covered by formatter/linter and avoid broad rewrites. Prioritize correctness/regression, security/privacy, data integrity, caller contract drift, missing or weak tests, dependency/config/build/migration risk, and performance/concurrency on plausible paths. For each finding include file/line or symbol, failure mechanism, severity: blocking / should-fix / optional, smallest safe fix, and validation. Also report observed or recommended checks, missing tests or weak evidence, final verdict: Safe to PR / PR after fixes / Do not PR yet, confidence, and remaining uncertainty.
```

If `codex review` fails or is interrupted, label the result as manual self-review fallback. Do not present it as a completed built-in review. If it looks quiet on a broad diff, poll the session before assuming failure; a delayed final finding can still be useful, but do not let the tool run replace your own evidence-bound verification.

## Required Review Loop

For every nontrivial branch or PR-ready diff, do this loop before the verdict:

1. Map changed behavior, not just changed files. Name the main behavior groups in plain language, such as "cache key", "config loader", "dashboard artifact", "dependency pins", or "removed route".
2. Pick the matching review lenses from this skill. For each selected lens, inspect at least one producer, one consumer, and one test or validation path when those exist.
3. For each risky changed behavior, answer: what old test would fail if this were wrong? If no test would fail, report a missing or weak test unless the behavior is clearly documentation-only or low-risk.
4. For each reviewed area that does not produce a finding, identify the concrete evidence used: source path, consumer path, test path, command output, or PR/CI evidence.
5. Before returning `Safe to PR`, search for neighboring instances of the same bug class or unchecked pattern in touched files.

Do not count a broad deterministic check as semantic review. Passing tests support a verdict only after you identify what changed behavior those tests cover and what they do not cover.

## Evidence Order

1. Read repo instructions first: `AGENTS.md`, nested instructions for touched paths, and repo docs that define commands, contracts, or review rules.
2. Inspect the diff before reading broad unrelated source.
3. Read affected callers, tests, fixtures, docs, configs, CI/check definitions, and generated-contract files only as needed to verify behavior.
4. Run cheap relevant deterministic checks when they are known and fit the risk. Separate commands actually run from commands only recommended.
5. For high-risk or commit-gate reviews, include the repo standard check if one exists or explain why it was not run.

Use docs and plans as intent. Use source, tests, fixtures, diffs, command output, CI, and PR review threads as proof.

When evidence is unavailable, say exactly which evidence is missing. Do not replace missing evidence with confidence language.

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

For every selected lens, inspect the changed source plus the nearest caller/consumer and the nearest test/check. If you cannot find a caller, consumer, or test, report that as remaining uncertainty or a missing-test gap.

### Data And Schema

Use when the diff touches CSV/parquet/JSON artifacts, dataframes, validation, manifests, schemas, model inputs, reports, or analytics outputs.

Check marker columns and selection flags carefully: `.astype(bool)`, `.astype(int)`, numeric casts, `dropna`, string booleans, fractional values, missing values, and non-numeric values. Tests should cover malformed inputs and round-trip encodings, not only in-memory happy paths.

For time-series or bucketed features, check whether fill operations bridge invalid anchors. `ffill`, `merge_asof`, grouped fills, and shifted sparse signals must preserve intentional `NaN` gaps when the source value at a completed bin, close, boundary, or anchor is missing.

For checked-in generated snapshots, reports, manifests, figures, or evidence bundles, verify provenance as well as bytes. A snapshot matching local generated output is not enough if the manifest records a commit, run id, spec hash, data version, or source path that will not be reachable or auditable from the published PR history.

Do not finish this lens until you have checked both valid data and one malformed, missing, boundary, or round-trip path when the diff changes validation, parsing, artifact schemas, or feature generation.

### Broad Refactor And Removed Surface

Use when code moves, modules split/merge, routes/commands/UI controls are removed, or ownership boundaries change.

Sweep for stale references in callers, tests, README, active specs, visible docs, CLI help, fixtures, and generated outputs. If docs conflict with source, classify whether the doc is active authority, stale background, or an implementation gap.

When boundary tests are added, check alternate import forms such as `import package.submodule`, `from package.submodule import x`, and `from package import submodule`.

### Config And Generated Names

Use when the diff touches config parsing, policy/action settings, thresholds, generated identifiers, feature names, or deduplication.

Reject ambiguous booleans, non-finite floats, and silent coercion. Check for generated-name collisions before deduplication, rounding, normalization, or hashing hides distinct inputs.

For new enum values, policy methods, strategy modes, or matrix/config fields, verify compatible companion fields and producer paths. A config option that requires a specific signal kind, artifact producer, model family, schema version, or execution mode should be rejected by the loader or factory when paired with an incompatible option, not left to fail later through missing artifacts or empty inputs.

When policy values can be supplied through multiple layers, such as risk-level caps and method-level caps, trace the canonical helper or fallback path. Do not assume a behavior is inactive just because the nearest config field is absent if shared code falls back to another field.

Do not finish this lens from parser membership alone. Trace at least one accepted value from loader to factory/materializer to runtime consumer, and check that incompatible combinations are rejected early.

### Performance, Cache, And Hot Path

Use when the diff changes caching, memoization, benchmark/runtime paths, preflight checks, dashboard/report timing, or fast paths.

Check cache key completeness, stale cache identity, hot/cold path equivalence, skip status, CLI exit semantics, timing counter correctness, and producer-consumer ordering for reports, gates, dashboards, manifests, or summaries. Passing unit tests or faster runtime does not prove the hot path measures the intended thing.

If a fast path prunes payloads, metrics, columns, or objects before shared ranking or selection logic, verify that all tie-breakers and downstream semantics remain equivalent.

For content-addressed caches, compare the key against every input consumed by the cached payload, not only obvious dates or file paths. Include policy/profile/window fields, split settings, recipe identities, feature identities, model settings, output schema versions, and any option that can change produced rows or assignments.

For cache-hit materialization, check idempotency and output ownership. A hit should behave correctly when the destination already exists, when hardlinking is unavailable, and when a copy fallback is used. It must not corrupt the cached source, leave stale destination contents, or fail on a normal warm rerun.

For artifact reuse decisions, validate both the cached source identity and the current requested output paths. If the cold path writes several artifacts, the reuse path must either materialize all requested artifacts or explicitly prove they are unnecessary; rewriting only a summary while leaving CSVs, sidecars, or reports absent at the new paths is a review finding.

For diagnostics and research readouts, distinguish aggregate measurements from causal attribution. If several caps, filters, skips, or intentional underinvestment paths can produce the same residual, do not label the entire residual as caused by one rule unless metadata or event-level evidence proves it.

Do not finish this lens from a warm-path happy test alone. Check at least one stale identity, changed option, existing destination, fallback path, mixed-cause metric, or downstream consumer when the diff changes cache, fast-path, or diagnostics behavior.

### Dependency, Build, And Runtime

Use when the diff changes `pyproject.toml`, requirements or lock files, package pins, build-system pins, install commands, Python or language version support, tool target versions, CI setup, or Makefile/package scripts.

Cross-check the advertised runtime floor against every pinned runtime, build, and test dependency. If package metadata is missing, require install/import evidence, upstream docs, or an explicit repo note. Also check tool target versions, install order, editable install behavior, and metadata tests.

When a change generates shell commands, scripts, benchmark packets, or copy-paste CLI instructions, check dynamic paths and values for quoting. Prefer argument arrays where possible; otherwise require shell-quoting for paths, manifests, run directories, timing files, and user-controlled values. Optional readers for summary/report tooling should handle missing, malformed, unreadable, and non-object JSON/YAML according to the caller contract instead of crashing unexpectedly.

Do not finish this lens from imports or unit tests alone. Check install/runtime compatibility, generated commands, or package metadata directly when the diff changes dependency declarations, build tooling, runtime floors, command construction, or benchmark runners.

### Tests And Checks

For each changed behavior, ask what test would fail on the old bug. Weak signs:

- Only happy-path tests for validation changes.
- Tests that assert implementation details but not caller-facing behavior.
- No negative cases for malformed config, stale caches, removed surfaces, or boundary imports.
- No negative cases for incompatible config-field combinations, such as a method that requires a companion signal/artifact path.
- No tests where equivalent policy is supplied through each supported config layer, such as risk-level and method-level caps.
- No diagnostics tests for mixed-cause metrics where only part of a residual should be attributed to a specific rule.
- No provenance check for checked-in generated evidence, such as whether recorded commit hashes are reachable from the PR head or published history.
- A passing full suite but no focused test for the risky branch.
- A skipped or failing check whose output is not triaged.
- Permissive spies or monkeypatches such as `raising=False` when the target symbol should exist.
- Cache tests that prove a hit exists but not that changed policy fields, changed output paths, existing destinations, copy fallback, or malformed cached metadata are handled.

## Subagents

Use subagents only when the user, repo instructions, or approved plan authorizes them and the environment permits delegation.

Subagent fan-out is justified for broad or high-risk diffs with separable lenses, such as data/schema, security/privacy, tests, dependency/build, performance/cache, migration, API/CLI/UI contract, or removed-surface review.

If subagents are unavailable or unauthorized, run the same lenses locally and label the result as self-review. The parent must deduplicate and verify all findings against source, diff, tests, logs, command output, CI, or PR review threads.

## Verdict Rules

Use one verdict:

- `Safe to PR`: no blocking or should-fix findings found, relevant checks are green or remaining checks are low-risk and named.
- `PR after fixes`: should-fix findings, missing focused tests, or unresolved validation gaps remain.
- `Do not PR yet`: blocking correctness, security/privacy, data loss, broken build/install/test, migration, dependency, or caller contract risk exists.

Before returning `Safe to PR`, do a verdict pass:

- Recheck the selected lenses against the diff.
- For each selected lens, name the producer, consumer, and test/check evidence inspected, or name what was missing.
- Name the strongest evidence supporting the `Safe to PR` verdict.
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
