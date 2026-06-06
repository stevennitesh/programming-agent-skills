# R3 - stock-momentum-strategy-research-platform PR 347

## Sample Metadata

Sample ID: R3

Repo: `stevennitesh/stock-momentum-strategy-research-platform`

Date captured: 2026-06-06

Reviewer: Codex local `/review` style pre-PR review with manual fallback, then CodeRabbit and Codex GitHub review on PR

Sample type: real

Risk profile: performance hot path, cache identity, dashboard telemetry, validation artifact ordering, selection semantics

Target:

- Base: `main` at `0c2fe6f7eddd437aa38c5b6fd1557bd31b126fca`
- Local pre-PR review target: `codex/validation-dashboard-hot-path-runtime`
- PR review target: PR #347 at `0a8d92efb78f3c19e1053cc3c63f89ba206deb68`

Base: `main`

Comparison command:

```bash
codex review --base main "<AGENTS.md pre-PR review prompt>"
```

Spec, issue, PRD, or user request:

- PR title: `Improve validation dashboard hot-path runtime`
- PR body summary: reuse validation dashboard input bundles, memoize stability scenario metrics, avoid repeated dashboard artifact reads, add runtime timing/preflight detail, and record runtime evidence/tests.

External evidence available:

- PR: https://github.com/stevennitesh/stock-momentum-strategy-research-platform/pull/347
- CodeRabbit review: 3 inline actionable comments and 1 outside-diff comment on current head.
- Codex GitHub review: 3 inline comments plus one duplicate body-level finding overlapping CodeRabbit.
- Live review threads: unresolved at capture time.
- PR body verification: `.venv/bin/python -m unittest discover tests` passed with 665 tests; `git diff --check origin/main...HEAD` passed.

## Repo Evidence Read

Instructions and standards:

- `AGENTS.md`: not checked directly for this sample.
- nested `AGENTS.md`: not checked for this sample.
- review docs: `docs/validation_dashboard_hot_path_runtime_plan.md` was part of the PR diff.
- `CONTEXT.md` or ADRs: not checked for this sample.
- README/contributing: not checked for this sample.
- tool configs: `pyproject.toml` was inspected enough to discover test configuration.

Source evidence:

- changed files: 17 files across `docs/`, `src/stock_momentum/dashboard/`, `src/stock_momentum/examples/`, `src/stock_momentum/tools/`, `src/stock_momentum/validation/`, and tests.
- callers checked by local pre-PR review: validation walk-forward, stability/stability engine, dashboard candidate rendering, EOD CSV runner, research grid runner, runtime benchmark matrix, and relevant tests.
- tests/fixtures checked by local pre-PR review: targeted unittest modules and then full unittest discovery.
- CI/check output checked: PR body, live PR metadata, CodeRabbit review body, Codex GitHub inline comments, and PR checks.

Command discovery:

- source of commands: local transcript, `pyproject.toml`, PR body, and live PR state.
- commands found:
  - `.venv/bin/python -m pytest -q tests/test_eod_walk_forward_validation.py tests/test_validation_stability.py tests/test_dashboard_validation_candidates.py tests/test_runtime_benchmark_matrix.py tests/test_eod_csv_runner.py tests/test_research_grid_run.py`
  - `.venv/bin/python -m unittest tests.test_eod_walk_forward_validation tests.test_validation_stability tests.test_dashboard_validation_candidates tests.test_runtime_benchmark_matrix tests.test_eod_csv_runner tests.test_research_grid_run`
  - `.venv/bin/python -m unittest discover -s tests`
  - `git diff --check main...HEAD`
  - `git diff --check origin/main...HEAD`
- commands run during local pre-PR review:
  - `pytest -q ...` did not provide useful review evidence in the copied transcript.
  - `.venv/bin/python -m pytest ...` failed because `pytest` was not installed in the repo venv.
  - `codex review --base main` failed with `failed to initialize in-process app-server client: Read-only file system`.
  - `.venv/bin/python -m unittest tests.test_eod_walk_forward_validation tests.test_validation_stability tests.test_dashboard_validation_candidates tests.test_runtime_benchmark_matrix tests.test_eod_csv_runner tests.test_research_grid_run` passed.
  - `.venv/bin/python -m unittest discover -s tests` passed.
  - `git diff --check main...HEAD` passed.
- commands run during evidence capture:
  - live PR metadata, review, comment, and check queries with `gh`.
- commands skipped and why:
  - Full local tests were not rerun during evidence capture because this sample is review-evidence classification, not PR fix verification.

## Known Ground Truth

High-confidence true issues from external review:

1. CodeRabbit found that dashboard input-read telemetry records `validation_artifact_count=13` while the in-memory path reads 14 dashboard inputs.
2. CodeRabbit found that validation bundle key/build helpers include `validation_candidate_ids` but not `validation_static_candidate_ids`, while downstream walk-forward and stability calls request both. Static-only candidates can fall out of the reused hot-path bundle.
3. CodeRabbit and Codex both found that the sortino fast path prunes `sharpe`, but the shared selection key expects `(primary, sortino, sharpe)`. Tied sortino candidates can therefore select a different winner than the reference walk-forward path.
4. CodeRabbit found that walk-forward artifact-write telemetry uses a hard-coded artifact count instead of counting the actual timed writes across conditional compact/non-compact paths.
5. Codex GitHub found that skipped hot-replay variants use `returncode=2`, while the runtime benchmark `main()` exits successfully only when every summary return code is zero. Intentional skips can therefore fail the CLI run.
6. Codex GitHub found that hot-replay preflight checks cache counts only, not whether cache entries match the current matrix/candidate identities. Stale cache sidecars can make a hot benchmark sample look eligible when it is not.
7. Codex GitHub found that the promotion gate is built before `run_validation_stability()` writes the current stability summary, so the dashboard gate can omit current stability evidence or reuse stale evidence.

Known non-issues / tempting false positives:

1. The initial interrupted `/review` was not a model/tool issue in this sample; the user intentionally restarted review in a new agent.
2. The `pytest` failure is an environment/command-discovery issue, not a code failure. The repo's working local test command for this sample was `unittest`.
3. CodeRabbit's docstring coverage warning is not automatically actionable for this repo unless the repo enforces that threshold.
4. The sortino tie-breaker appears in both CodeRabbit and Codex GitHub review. Count it once as a unique issue.

Expected verdict:

- At PR head `0a8d92e`: Do not merge yet until the runtime/cache/telemetry/selection findings are fixed or explicitly rejected.

Remaining uncertainty:

- The local review transcript is partially collapsed, so some intermediate command outputs are unavailable.
- The external findings are high-confidence source-level issues, but this capture did not run reproductions or fixes for each one.
- No completed built-in `codex review --base main` result exists for this sample because the nested command hit a read-only filesystem initialization error.

## Review Mode: Baseline

Prompt used:

```text
Not run for this sample.
```

Observed checks:

- Not applicable.

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
| Not run | n/a | n/a | n/a | none | Baseline mode was not run. |

Missed issues:

- Not applicable.

False positives/noise:

- Not applicable.

Verdict:

Not run.

## Review Mode: Structured Prompt

Prompt used:

```text
do a pre pr review
```

Observed checks:

- The local review inspected the branch diff against `main`.
- `.venv/bin/python -m pytest ...` failed because `pytest` was not installed.
- `codex review --base main` failed with a read-only filesystem app-server initialization error.
- The agent continued with manual source/diff review and local checks.
- Targeted `unittest` modules passed.
- Full `unittest discover -s tests` passed.
- `git diff --check main...HEAD` passed.

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
| No actionable correctness issues found | n/a | no | missed-correctness, missed-contract-risk, missed-performance-concurrency | weak | External review later found seven unique issues on the same PR head. |

Missed issues:

- Dashboard artifact count off by one.
- Validation bundle cache scope omits static candidate IDs.
- Sortino fast path drops the `sharpe` tie-breaker.
- Walk-forward artifact-write telemetry uses a hard-coded count.
- Hot-replay intentional skips can make the CLI exit fail.
- Hot-replay preflight validates cache counts instead of current cache identities.
- Promotion gate is built before current stability evidence is written.

False positives/noise:

- None captured in the final local pre-PR review output.

Verdict:

The local clean verdict was incomplete. Deterministic checks passed, but semantic review missed several runtime/caching contract issues.

## Review Mode: Selective Subagents

Use only when the diff is high-risk or broad.

Subagent gate:

- Authorized by: not run.
- Why fan-out was useful: this diff changed hot-path runtime behavior, cache reuse, timing evidence, dashboard payload assembly, and selection semantics. Separate performance/cache, artifact-ordering, dashboard telemetry, and selection-correctness lenses would have been justified.
- Lenses used: none.
- Lenses skipped: performance/concurrency, correctness/regression, tests/coverage, API/data contract, dashboard/reporting contract.

Findings before parent deduplication:

- Not applicable.

Parent synthesis:

- accepted findings: not applicable.
- rejected findings: not applicable.
- duplicate findings: not applicable.
- final verdict: not applicable.

Did subagents add unique value?

Unknown.

Did subagents add noise?

Unknown.

## External Review Comparison

External sources: CodeRabbit and Codex GitHub review

External findings:

- CodeRabbit: dashboard artifact-read timing count is off by one.
- CodeRabbit: validation bundle reuse omits static candidates from bundle scope.
- CodeRabbit and Codex GitHub: sortino fast path drops the `sharpe` tie-breaker.
- CodeRabbit: walk-forward artifact-write telemetry count is hard-coded.
- Codex GitHub: skipped hot-replay rows still make the benchmark CLI fail.
- Codex GitHub: hot-replay preflight checks aggregate cache counts, not current cache identities.
- Codex GitHub: promotion gate is computed before current stability outputs are available.

Local review caught:

- No actionable issues.

Local review missed:

- All seven unique external findings above.

Local review found valid issue external review missed:

- None captured.

## Classification

Miss labels:

- [ ] wrong-base
- [ ] missed-spec-gap
- [x] missed-contract-risk
- [x] missed-correctness
- [ ] missed-security-data
- [x] missed-test-gap
- [ ] missed-check-output
- [x] missed-performance-concurrency
- [ ] missed-context-source

Noise labels:

- [ ] off-diff
- [ ] style-only
- [ ] speculative
- [ ] broad-rewrite
- [x] duplicate
- [ ] stale
- [ ] wrong-severity
- [ ] unsupported

## Skill Implications

Rules to add or strengthen:

- For performance or hot-path PRs, review semantic correctness of the cache path, telemetry, and acceptance contract. Passing runtime checks and tests do not prove the hot path is measuring the intended thing.
- For bundle/cache reuse changes, verify the cache key includes every input that affects bundle contents, including static candidate sets, scenario parameters, identities, and feature/result selectors.
- For preflight checks, verify identity, freshness, and compatibility of cached artifacts. Counting files or directories is not enough when stale artifacts can satisfy the count.
- For intentional skip paths, review the CLI exit contract separately from the report payload. A skipped row should not fail the command unless that is the explicit contract.
- For derived artifact/report/dashboard generation, check producer-consumer ordering. Gates and summaries that read generated artifacts should be computed after the current producer stage writes them.
- For fast paths that prune metrics or payloads, verify they preserve the full downstream ranking/selection semantics, including tie-breakers.
- When a local review command fails, label the result as manual/self-review fallback and avoid a clean "review passed" conclusion unless an equivalent review was actually completed.

Reference checklist items:

- Performance/cache lens: cache key completeness, stale cache identity, skip semantics, acceptance status, CLI exit code, timing counter correctness, and hot/cold path equivalence.
- Dashboard/reporting lens: in-memory versus file-backed parity, artifact ordering, stale evidence reuse, and telemetry count consistency.
- Selection lens: metric-pruning safety, tie-breaker preservation, reference-path equivalence, and deterministic candidate ordering.
- Tests lens: tests for static-only candidates, stale cache identities, skipped hot-replay exit semantics, tied sortino/sharpe candidate selection, and promotion-gate ordering.

Script/context collection needs:

- Optional scan for cache-key builders and downstream calls that pass wider identity sets than the cache key includes.
- Optional scan for hard-coded telemetry counts near repeated write/read wrappers.
- Optional scan for `returncode` aggregation over rows that also include `run_executed` or skip status fields.
- Optional scan for derived report/gate generation before producer stages write the artifacts they read.

Subagent gate implications:

- A PR focused on performance hot paths, cache reuse, timing instrumentation, or benchmark preflight should qualify for selective fan-out even when source files are localized and deterministic checks pass.

Repo-specific guidance needed instead:

- None yet. The misses are portable performance/cache review patterns.

## Summary For Ledger

One-line summary:

Local pre-PR review returned a clean verdict after unittest checks passed, but CodeRabbit and Codex GitHub found seven unique hot-path/cache/telemetry/selection issues on the same PR head.

Best evidence:

- Local final verdict: no actionable correctness issues found; full unittest suite passed.
- PR body verification: `.venv/bin/python -m unittest discover tests` passed with 665 tests and `git diff --check origin/main...HEAD` passed.
- Live CodeRabbit comments on dashboard count, static candidate bundle scope, sortino tie-breaker, and artifact count.
- Live Codex GitHub comments on skipped hot-replay exit behavior, cache identity preflight, and promotion-gate ordering.

Biggest miss:

The local review treated passing unit tests and broad diff inspection as enough for a clean verdict, but missed semantic cache and artifact-ordering contracts introduced by the hot-path optimization.

Worst noise:

The sortino tie-breaker appeared in both CodeRabbit and Codex GitHub review and should be counted once.

Decision implication:

The future review guidance needs a dedicated performance/cache lens. It should force reviewers to trace cache keys, stale-cache identity, skip/exit semantics, producer-consumer artifact ordering, and fast-path equivalence instead of only checking that tests pass.
