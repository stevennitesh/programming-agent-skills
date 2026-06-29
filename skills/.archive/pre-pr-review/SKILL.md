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

## Fast Review Path

Use for tiny or narrow diffs with obvious blast radius.

- Identify the target, base, and head when Git evidence is available.
- Inspect the diff, plus the nearest caller or test only if behavior changed.
- Pick only the matching risk lenses, often none or one.
- Run or recommend one relevant check when a check is cheap and useful.
- Report findings, or `No findings in inspected scope`, with checks, verdict, confidence, and remaining uncertainty.

Switch to the Full Review Path when the diff changes runtime behavior across modules, config, dependencies, generated output, data/schema, security/privacy, migrations, performance, public or caller contracts, or when the fast read leaves meaningful uncertainty.

## Full Review Path

Use for every nontrivial branch or PR-ready diff before the verdict:

1. Map changed behavior, not just changed files. Name the main behavior groups in plain language, such as "cache key", "config loader", "dashboard artifact", "dependency pins", or "removed route".
2. Pick the matching review lenses from this skill. For each selected lens, inspect at least one producer, one consumer, and one test or validation path when those exist.
3. For each risky changed behavior, answer: what old test would fail if this were wrong? If no test would fail, report a missing or weak test unless the behavior is clearly documentation-only or low-risk.
4. For each reviewed area that does not produce a finding, identify the concrete evidence used: source path, consumer path, test path, command output, or PR/CI evidence.
5. Before returning `Safe to PR`, search for neighboring instances of the same bug class or unchecked pattern in touched files.

Do not count a broad deterministic check as semantic review. Passing tests support a verdict only after you identify what changed behavior those tests cover and what they do not cover.

## Evidence Order

1. Read repo instructions first: existing root instruction files such as `AGENTS.md`, `CLAUDE.md`, `AGENTS_PORTABLE_FALLBACK.md`, or `AGENTS_SKILL_PACK_ROUTER.md`; nested instructions for touched paths; and repo docs that define commands, contracts, or review rules.
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

For every selected lens, inspect the changed source plus the nearest producer or caller, the nearest consumer, and the nearest test/check when they exist. If you cannot find one, report that as remaining uncertainty or a missing-test gap.

Do not apply niche checks to unrelated diffs. Load deeper repo-specific context only when the selected lens and diff risk justify it.

### Data And Schema

Use when the diff touches CSV/parquet/JSON artifacts, dataframes, validation, manifests, schemas, model inputs, reports, or analytics outputs.

- Check parsing, validation, casts, missing values, ordering/time boundaries, and schema compatibility.
- Check both valid data and one malformed, missing, boundary, or round-trip path when validation or parsing changes.
- Verify checked-in generated artifacts by provenance, schema/version, and reachable source evidence, not just matching bytes.
- Trace at least one downstream consumer that depends on the changed shape or semantics.

### Broad Refactor And Removed Surface

Use when code moves, modules split/merge, routes/commands/UI controls are removed, or ownership boundaries change.

- Sweep for stale references in callers, tests, docs, CLI/UI surfaces, fixtures, and generated outputs.
- Check import, route, command, and compatibility paths that callers may still use.
- Verify the new boundary reduces coupling or caller knowledge rather than hiding simple control flow.
- If docs conflict with source, classify active authority, stale background, or implementation gap.

### Config And Generated Names

Use when the diff touches config parsing, policy/action settings, thresholds, generated identifiers, feature names, or deduplication.

- Reject ambiguous booleans, non-finite numbers, silent coercion, and incompatible option combinations early.
- Trace at least one accepted value from loader/parser to runtime consumer; parser membership alone is not enough.
- Check companion fields, defaults, fallback layers, and producer paths for new modes or enum/config values.
- Check generated-name collision, stability, normalization, rounding, and deduplication behavior.

### Performance, Cache, And Hot Path

Use when the diff changes caching, memoization, benchmark/runtime paths, preflight checks, dashboard/report timing, or fast paths.

- Check cache key completeness against every consumed input, option, and output schema version.
- Compare hot/cold or cached/uncached semantics, output materialization, idempotency, stale identity, existing destination, and fallback behavior.
- Check status, exit semantics, timing counters, producer-consumer ordering, and downstream consumers.
- Treat aggregate performance or diagnostic numbers as causal only when metadata or event-level evidence supports the attribution.

### Dependency, Build, And Runtime

Use when the diff changes `pyproject.toml`, requirements or lock files, package pins, build-system pins, install commands, Python or language version support, tool target versions, CI setup, or Makefile/package scripts.

- Cross-check runtime floors, dependency pins, lockfiles, tool target versions, CI setup, and install order.
- Verify package metadata, editable install behavior, or import/install evidence when dependency declarations change.
- Check generated commands, scripts, and copy-paste instructions for quoting and dynamic paths; prefer argument arrays when possible.
- Check missing, malformed, unreadable, or optional config/report inputs according to the caller contract.

### Security, Privacy, And Destructive Risk

Use when the diff touches auth, permissions, secrets, PII, filesystem/network access, data deletion, migrations, publishing, or external services.

- Check that new data exposure, logging, telemetry, artifacts, and errors do not leak secrets or private data.
- Check authorization, path traversal, shell injection, request validation, and unsafe defaults on plausible paths.
- Check destructive operations for target scope, reversibility, dry-run behavior, and user approval boundaries.
- Verify security/privacy behavior through source, tests, docs, or CI evidence; do not infer safety from intent.

### Tests And Checks

For each changed behavior, ask what test would fail on the old bug. Weak signs:

- Only happy-path tests for validation changes.
- Tests that assert implementation details but not caller-facing behavior.
- No negative or boundary cases for malformed config, stale caches, removed surfaces, generated names, destructive operations, or boundary imports.
- A passing full suite but no focused test for the risky branch.
- A skipped or failing check whose output is not triaged.
- Permissive spies, mocks, monkeypatches, or fixtures that can pass while the real caller-facing path is broken.
- Checked-in generated evidence without provenance or consumer checks.

## Subagents

Use subagents only when authorized and the diff is broad or high-risk with separable lenses. Otherwise run the lenses locally and label the result as self-review.

The parent must deduplicate and verify all findings against source, diff, tests, logs, command output, CI, or PR review threads.

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

For small reviews:

```text
Findings:
Checks:
Verdict:
Confidence:
Remaining uncertainty:
```

For broad or high-risk reviews, include the detail needed to make each finding actionable:

```text
Review path:
Target:
Base:
Risk lenses:

Findings:
- <blocking|should-fix|optional>: <title>
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
- PR threads, CI, or review status need durable record updates; use `github-tracking`.
- Subagents are requested or an approved review plan calls for them; use `subagent-workflow`.
- You are about to claim the change is ready, reviewed, safe, or mergeable after edits; use `verify-before-done`.
- The next route after the review is unclear, or the user changes from review to implementation, planning, PR tracking, merge, or cleanup; return to `coding-router` and choose one controlling route.

## Handoff

- `coding-router`: choose the next controlling route after the review verdict, especially when the user asks to fix findings, open/update a PR, merge, plan work, or continue with implementation.
- `github-tracking`: durable PR/issue record updates, recorded CI/review evidence, or review-response decision records.
- `subagent-workflow`: authorized multi-lens independent review.
- `diagnose-loop`: failing checks, crashes, regressions, or unclear command output.
- `tdd-slice`: fixing an approved finding with a behavior check.
- `verify-before-done`: before readiness or merge-safety claims.
