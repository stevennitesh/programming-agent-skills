# R1 - secom-yield-monitoring PR 4

## Sample Metadata

Sample ID: R1

Repo: `stevennitesh/secom-yield-monitoring`

Date captured: 2026-06-06

Reviewer: Codex local `/review` before PR, then CodeRabbit on PR

Sample type: real

Risk profile: data-schema-risk, artifact lineage, broad validation workflow change

Target:

- Local `/review` target: `audit/selector-math` at `0803ea63f3345f6f0fe3e13597a201f31ceb2f69`
- PR review target: PR #4 at `bbdbf6896c55796b1d1b6063e37a6a2e6161c369`
- Current PR head after fixes: `c30d9a9a942538a8f4e9d5c1e9a868cd78cb091b`

Base: `main` at `9207bae800850dcd7fe2769ecba61b222d35c326`

Comparison command:

```bash
codex review --base main "<AGENTS.md pre-PR review prompt>"
```

Spec, issue, PRD, or user request:

- PR title: `Audit selector behavior and artifact contracts`
- PR body summary: harden selector math, failure behavior, temporal role selection, config grids, reporting claim boundaries, pooled Ttest alignment, and selector artifact lineage/schema validation.

External evidence available:

- PR: https://github.com/stevennitesh/secom-yield-monitoring/pull/4
- CodeRabbit review thread: https://github.com/stevennitesh/secom-yield-monitoring/pull/4#discussion_r3366533698
- CI: `Ruff and pytest` passed on current head `c30d9a9`.
- CodeRabbit thread is resolved and says it was addressed in commit `c30d9a9`.

## Repo Evidence Read

Instructions and standards:

- `AGENTS.md`: the branch was reviewed before PR with the new pre-PR review prompt from AGENTS guidance.
- nested `AGENTS.md`: not checked for this sample.
- review docs: not checked for this sample.
- `CONTEXT.md` or ADRs: not checked for this sample.
- README/contributing: README was part of the diff and had one CodeRabbit style nitpick.
- tool configs: not checked for this sample.

Source evidence:

- changed files: 22 files in README, `src/secom/`, and tests.
- callers checked by local `/review`: artifacts, benchmark workflows, tuning, feature selection, reporting, temporal robustness, README, tests, and artifact contract docs.
- tests/fixtures checked by local `/review`: targeted tests and then `make PYTHON=.venv/bin/python check`.
- CI/check output checked: PR body, `gh pr view` status check rollup, and live review-thread state.

Command discovery:

- source of commands: local `/review` transcript, PR body, and CI.
- commands found:
  - `.venv/bin/python -m pytest -q tests/test_selection.py tests/test_univariate_selectors.py tests/test_study_audit.py tests/test_benchmark_replication.py tests/test_temporal_robustness.py tests/test_final_report.py tests/test_report_skeleton.py`
  - `make PYTHON=.venv/bin/python check`
  - `scripts/run_audit.py --output-dir runs/benchmark_replication --strict`
  - `scripts/run_audit.py --output-dir runs/evidence/2026-06-04-full-benchmark-pearson-original-krr-tuned/benchmark_replication --strict`
  - `git diff --cached --check`
- commands run during local `/review`:
  - `python -m pytest ...` failed because `python` was unavailable.
  - `.venv/bin/python -m pytest ...` passed with 80 tests.
  - `make PYTHON=.venv/bin/python check` passed with 136 tests.
  - local Pandas parsing/coercion probes for `is_selected_config`.
- commands run during evidence capture:
  - live PR metadata and review-thread queries with `gh`
  - local source/test inspection with `nl`, `rg`, and `git show`
  - local Pandas truthiness reproduction with `.venv/bin/python`
- commands skipped and why:
  - full secom checks were not rerun during evidence capture because the purpose was review-evidence classification, not PR fix verification.

## Known Ground Truth

Known true issues:

1. Local `/review` found a real pre-PR bug in `_validate_binary_selected_values`: the old implementation converted selected values with `to_numeric(...).dropna().astype(int)` before checking `{0, 1}`, so `0.5` became `0` and non-numeric strings were dropped instead of rejected. The branch fixed this in `bbdbf68`.
2. CodeRabbit later found a related marker-flag bug in `_selected_tuned_search_configs`: `search_df["is_selected_config"].astype(bool)` treated non-empty strings such as `"False"` and `"0"`, and also `NaN`, as truthy. The branch fixed this in `c30d9a9`.

Known non-issues / tempting false positives:

1. README spelling/style change from `pooled Ttest` to `pooled T-test` is a style-only nitpick. It should stay optional and should not drive the local reviewer design.

Expected verdict:

- At `0803ea6`: PR after fixes, because local `/review` found a real P2 artifact-contract issue.
- At `bbdbf68`: PR after fixes, because CodeRabbit found a related marker-flag issue.
- At `c30d9a9`: no unresolved CodeRabbit threads and CI passed, based on live PR state.

Remaining uncertainty:

- The local `/review` transcript is partially collapsed in the copied UI output, so exact intermediate command output is incomplete.
- This sample shows local `/review` can find real data-contract defects, but also that a follow-up fix needs an analogous-pattern sweep across nearby marker columns.

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
Review this branch against the base branch as a pre-PR review.

Use repository instructions and the Pre-PR Review guidance in AGENTS.md.

Focus only on actionable issues introduced or exposed by this branch. Ignore style issues covered by formatter/linter. Prioritize correctness, security, data integrity, tests, API contracts, migrations, backward compatibility, performance/concurrency risk, and repo-specific constraints.

Return blocking findings, should-fix findings, missing tests, checks to run before PR, and a final verdict.
```

Observed checks:

- Initial `python -m pytest ...` failed because `python` was not available.
- `.venv/bin/python -m pytest ...` passed with 80 tests.
- `make PYTHON=.venv/bin/python check` passed with 136 tests.
- Local review also inspected diffs, artifact code, tests, and repo docs.

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
| Reject fractional selected flags before casting | P2 | yes | n/a | strong | Found feature-stability selected-flag false negative in artifact validation. |

Missed issues:

- The structured review did not report the analogous `is_selected_config.astype(bool)` issue in `_selected_tuned_search_configs`, which CodeRabbit found later.

False positives/noise:

- None captured in the final local `/review` output.

Verdict:

PR after fixes. The local reviewer correctly identified a should-fix artifact-contract bug.

## Review Mode: Selective Subagents

Use only when the diff is high-risk or broad.

Subagent gate:

- Authorized by: not run.
- Why fan-out was useful: this diff was broad and touched artifact schemas, lineage validation, workflow behavior, and tests. A data/schema review lens and tests/coverage lens would have been justified.
- Lenses used: none.
- Lenses skipped: correctness/regression, tests/coverage, data/schema/model behavior.

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

External source: CodeRabbit

External findings:

- Actionable: `src/secom/artifacts.py` lines 652-657 used `astype(bool)` on `is_selected_config`, causing `"False"`, `"0"`, and `NaN` to be selected. This was addressed in `c30d9a9`.
- Nitpick: README used `pooled Ttest`; CodeRabbit suggested `pooled T-test`. This was also changed in `c30d9a9`.

Local review caught:

- Local `/review` caught the related feature-stability `selected` coercion issue before PR creation.

Local review missed:

- Local `/review` did not catch the neighboring tuned-search `is_selected_config` coercion issue before the PR.

Local review found valid issue external review missed:

- CodeRabbit reviewed after the local `/review` fix commit, so it did not have the same pre-fix state. Treat this as a sequence, not a head-to-head comparison on identical code.

## Classification

Miss labels:

- [ ] wrong-base
- [ ] missed-spec-gap
- [ ] missed-contract-risk
- [x] missed-correctness
- [ ] missed-security-data
- [x] missed-test-gap
- [ ] missed-check-output
- [ ] missed-performance-concurrency
- [ ] missed-context-source

Noise labels:

- [ ] off-diff
- [x] style-only
- [ ] speculative
- [ ] broad-rewrite
- [ ] duplicate
- [ ] stale
- [ ] wrong-severity
- [ ] unsupported

## Skill Implications

Rules to add or strengthen:

- When a review finds a class of bug, perform an analogous-pattern sweep in the touched area before final verdict. In this sample, a `selected` marker coercion bug should have triggered a second look at `is_selected_config` and other marker columns.
- In dataframes or CSV-backed artifact code, scrutinize `.astype(bool)`, numeric casts, `dropna`, and `astype(int)` on marker, selected, enabled, active, or `is_*` columns. String `"False"`, string `"0"`, fractional values, non-numeric strings, and missing values must not become selected or disappear by accident.
- For artifact lineage or schema validation changes, require tests that cover malformed marker flags and CSV-like string values, not only in-memory booleans.
- Keep style-only documentation preferences out of blocking or should-fix review output unless the user explicitly asks for editorial polish.

Reference checklist items:

- Data/schema lens: marker flag coercion, CSV round-trip behavior, `pd.NA`/`NaN` behavior, boolean parsing semantics, fractional numeric values, non-numeric strings, and dropped malformed rows.
- Tests lens: changed validation logic should include one negative test for malformed input and one positive test for accepted encodings.

Script/context collection needs:

- Optional changed-diff scan for `.astype(bool)`, `astype(int)`, `dropna`, and boolean-looking dataframe columns. This should be a review aid, not an automatic failure.

Subagent gate implications:

- A broad PR touching artifact schemas, lineage validation, and data workflows should qualify for selective data/schema and tests/coverage subagents.

Repo-specific guidance needed instead:

- None yet. The finding is portable to Pandas/data artifact review, not unique to this repo.

## Summary For Ledger

One-line summary:

Local `/review` found one real selected-flag artifact validation bug, then CodeRabbit found a related marker-flag coercion bug after the local fix.

Best evidence:

- Local `/review` final finding: `[P2] Reject fractional selected flags before casting`.
- Commit `bbdbf68` fixed malformed feature-stability flags.
- CodeRabbit thread found `is_selected_config.astype(bool)` truthiness and was addressed in `c30d9a9`.
- Current code uses explicit numeric/string masks for `is_selected_config`.

Biggest miss:

The local review did not generalize from one marker-flag coercion bug to an analogous nearby marker column before PR creation.

Worst noise:

CodeRabbit's README `pooled Ttest` comment is style-only and should stay optional.

Decision implication:

The AGENTS prompt is already useful: it found a concrete P2 before PR. A future skill should focus on making follow-up review more systematic after a finding: sweep analogous patterns, require nearby malformed-input tests, and gate data/schema subagents for broad artifact-contract changes.
