# R5 StockMarket-ML-Gate PR258

## Sample

- Repo: `stevennitesh/StockMarket-ML-Gate`
- PR: <https://github.com/stevennitesh/StockMarket-ML-Gate/pull/258>
- Branch: `fix-experiment-grid-run-findings`
- Base: `origin/main`
- Risk profile: performance/cache, artifact reuse, generated benchmark commands, time-series feature semantics, tests/coverage
- Local review mode: `$pre-pr-review` plus attempted `codex review --base origin/main`
- External review mode: CodeRabbit PR review

## Local Review Outcome

The local pre-PR review correctly identified two should-fix issues:

- Dataset-table cache materialization could fail or use stale destination state when the output path already existed and hardlink/copy behavior differed.
- Raw dataset validation reuse compared cached report identity but did not ensure all currently requested CSV artifact paths were materialized on reuse.

The local review also ran focused tests for touched analysis, workflow, experiment-grid, benchmark, and cache paths, and `git diff --check origin/main...HEAD`.

The built-in `codex review --base origin/main` appeared quiet for a long time but eventually returned a useful cache-materialization finding. Lesson: on broad diffs, poll before treating a quiet review run as failed, but still keep manual verification as the final authority.

## External Review Outcome

CodeRabbit reported several additional actionable issues:

- Dataset-table cache key omitted split-policy identity beyond date cutoffs, allowing different split profiles to alias the same cached `dataset.parquet`.
- Label-split cache key omitted split-policy identity even though the cached artifact contains assigned split values.
- Generated timed command strings interpolated unquoted dynamic paths into shell commands.
- Optional JSON summary reader handled only missing files, not malformed JSON or unreadable content.
- Completed intraday feature logic used fill operations that could bridge missing bin-end closes and suppress intended `NaN` gaps.
- A test spy used `raising=False` even though the patched symbol should exist, weakening future refactor detection.

There was also one low-value grammar nit, which should remain optional/noise for this skill.

## Misses

The pre-PR skill needed stronger wording in these areas:

- Cache keys must include every policy/profile/window/recipe option consumed by the cached payload, not just obvious boundary dates.
- Cache-hit materialization must be idempotent when destinations already exist and must not mutate or corrupt the cache source.
- Artifact reuse must prove current requested output paths are satisfied, not only that the cached source report is valid.
- Time-series fill operations need missing-anchor tests; passing whole-session or happy-path cases is not enough.
- Generated shell command packets need path quoting or argument arrays.
- Optional report/summary readers need caller-contract error handling for malformed or unreadable files.
- Test spies should fail fast when the target symbol disappears unless the absence is intentionally allowed.

## Skill Changes Implied

- Strengthen `Performance, Cache, And Hot Path` with content-addressed cache key completeness, warm-hit materialization idempotency, and artifact-output-path reuse checks.
- Strengthen `Data And Schema` with a missing-anchor/fill-operation check for bucketed time-series features.
- Strengthen `Dependency, Build, And Runtime` with generated shell-command quoting and optional-reader robustness.
- Strengthen `Tests And Checks` with permissive spy and cache-hit negative-test checks.

## Verdict Calibration

The local review verdict was directionally correct because it blocked PR readiness with two should-fix issues, but it still undercounted the risk surface. For future broad cache/hot-path PRs, a clean or partial local review should not be treated as enough unless cache-key inputs, output materialization, copy/hardlink fallback, malformed metadata, generated commands, and fill/NaN semantics were explicitly inspected.
