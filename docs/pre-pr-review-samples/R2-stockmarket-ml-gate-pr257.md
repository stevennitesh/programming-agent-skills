# R2 - StockMarket-ML-Gate PR 257

## Sample Metadata

Sample ID: R2

Repo: `stevennitesh/StockMarket-ML-Gate`

Date captured: 2026-06-06

Reviewer: user-stopped first `/review`, failed nested `codex review --base`, manual/self-review fallback, then CodeRabbit on PR

Sample type: real

Risk profile: broad refactor, public/operator contract removal, config normalization, import-boundary tests

Target:

- Base: `main` at `d39bd37ffa6d4bdccca6f2e96852a63bdd7ef2fa`
- Local fallback review target: `post-refactor-review` at `15ca557f5a8d4b4e9dff3d8e3415d59a19731ae3`
- PR review target: PR #257 at `9fa5595912ec3a34f960808d39821adc4052a068`

Base: `main`

Comparison command:

```bash
codex review --base d39bd37ffa6d4bdccca6f2e96852a63bdd7ef2fa "<AGENTS.md pre-PR review prompt>"
```

Spec, issue, PRD, or user request:

- PR title: `Align analysis UI pipeline removal checks`
- PR body summary: update slow Playwright analysis UI check for removed full-pipeline action and narrow MBP stage-index analysis contract to single-stage `Run Stage` requests.

External evidence available:

- PR: https://github.com/stevennitesh/StockMarket-ML-Gate/pull/257
- CodeRabbit review: 4 actionable comments and 1 nitpick on current PR head.
- Live review threads: 4 unresolved CodeRabbit threads.
- CodeRabbit status context: success.

## Repo Evidence Read

Instructions and standards:

- `AGENTS.md`: active refactor plan outranks stale `docs/MBP_SPEC/**`; old spec behavior should not be preserved only because it appears in specs.
- nested `AGENTS.md`: not checked for this sample.
- review docs: active plan is `docs/plans/2026-06-03-workflow-boundary-refactor-plan.md`.
- `CONTEXT.md` or ADRs: not checked for this sample.
- README/contributing: README is part of the PR diff.
- tool configs: not checked for this sample.

Source evidence:

- changed files: 47 files across docs, `src/mlgate/**`, and `src/tests/**`.
- callers checked by local fallback review: analysis runtime/UI, CLI, experiment-grid modules, modeling recipe modules, policy modules, boundary tests, README, MBP stage index, and MBP detailed specs.
- tests/fixtures checked by local fallback review: full pytest, ruff, Playwright test in skipped and slow modes, boundary/test files.
- CI/check output checked: PR body, CodeRabbit status, and live review-thread state.

Command discovery:

- source of commands: local transcript, PR body, and live PR state.
- commands found:
  - `.venv/bin/python -m pytest -q`
  - `.venv/bin/python -m ruff check src`
  - `.venv/bin/ruff check src/tests/test_analysis_ui_playwright.py`
  - `.venv/bin/python -m pytest -q src/tests/test_analysis_ui_playwright.py -rs`
  - `.venv/bin/python -m pytest -q src/tests/test_analysis_ui_playwright.py --run-slow -rs`
  - `git diff --check`
- commands run during local fallback review:
  - `.venv/bin/python -m pytest -q` passed.
  - `.venv/bin/python -m ruff check src` passed.
  - Playwright test skipped without `--run-slow`; with `--run-slow`, it skipped because Chromium was not installed.
- commands run during evidence capture:
  - live PR metadata and review-thread queries with `gh`
  - source inspection with `nl`, `rg`, and `git show`
  - small reproductions for quantile-label collisions, string truthiness, `NaN` float validation, and AST import shape.
- commands skipped and why:
  - full local tests were not rerun during evidence capture because this sample is review-evidence classification, not PR fix verification.

## Known Ground Truth

Known true issues:

1. Local fallback review found stale removal follow-through before PR creation: the branch removed `AnalysisController.run_pipeline`, `/api/run/pipeline`, and the `Run Full Pipeline` UI control, but left a slow Playwright expectation and MBP stage-index text expecting that removed control. Commit `9fa5595` fixed those two reported items.
2. CodeRabbit found that `generated_feature_names` deduplicates generated names with `tuple(dict.fromkeys(names))`; quantile thresholds such as `0.801` and `0.804` both round to `trainquantile_p80`, silently collapsing distinct configured transforms.
3. CodeRabbit found that `_normalize_policy_actions` uses `bool(...)` on `enabled` fields, so string `"0"` or `"false"` enables actions.
4. CodeRabbit found that `_bounded_float` accepts non-finite values. `float("nan")` passes the existing range check because both comparisons are false.
5. CodeRabbit found that `test_refactor_boundaries.py` misses `from mlgate import experiment_grid`, because that parses as `ast.ImportFrom(module="mlgate", names=["experiment_grid"])`.

Known non-issues / tempting false positives:

1. CodeRabbit's separate `_bounded_float` thread duplicates the `NaN` portion of the policy-recipes thread. Count it as one unique issue.
2. CodeRabbit's docstring-coverage pre-merge warning is not automatically actionable for this repo unless the team enforces that threshold.
3. Residual `Run Pipeline` references remain in unmodified MBP analysis/shared-contract docs. This may be a real follow-up spec gap, but confidence is lower because repo `AGENTS.md` explicitly says some MBP specs predate the workflow-boundary refactor and the active refactor plan outranks stale MBP guidance.

Expected verdict:

- At `15ca557`: PR after fixes, because local fallback review found stale operator-contract/test expectations.
- At `9fa5595`: Do not merge yet until CodeRabbit's unresolved correctness/test-boundary threads are triaged and fixed or explicitly rejected.

Remaining uncertainty:

- The first interactive `/review` attempt was intentionally stopped by the user to run review in a new agent. Do not count that as a tool failure.
- A separate nested `codex review --base ...` command failed with `failed to initialize in-process app-server client: Read-only file system`.
- The final review result should therefore be labeled manual/self-review fallback due to the nested command failure, not a completed built-in `/review` run.

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
Review this as a pre-PR review. Focus only on actionable issues introduced or exposed by this diff. Ignore style issues covered by formatter/linter and avoid broad rewrites. Prioritize correctness, security, data integrity, tests, API contracts, migrations, backward compatibility, performance/concurrency risk, and repo-specific constraints.
```

Observed checks:

- The first interactive `/review` was user-stopped to rerun in a new agent.
- The nested `codex review --base ...` command then failed with a read-only filesystem initialization error.
- The agent continued with manual source/diff review and local checks.
- `.venv/bin/python -m pytest -q` passed.
- `.venv/bin/python -m ruff check src` passed.
- Playwright slow test could not execute locally because Chromium was not installed.

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
| Update Playwright expectation after removing Run Full Pipeline | P3 | yes | n/a | strong | Fixed in `9fa5595`. |
| Remove stale Run Pipeline contract text from stage index | P3 | yes | n/a | strong | Fixed in `9fa5595`. |

Missed issues:

- Quantile-label collision in generated feature names.
- String truthiness for policy action `enabled` flags.
- Non-finite float acceptance in `_bounded_float`.
- Import-boundary test gap for `from mlgate import experiment_grid`.
- Possible broader stale `Run Pipeline` references in unmodified MBP analysis/shared-contract docs.

False positives/noise:

- None captured in the local fallback review output.

Verdict:

PR after fixes. This was correct for the stale UI/spec findings it identified, but incomplete for config-normalization and import-boundary risks.

## Review Mode: Selective Subagents

Use only when the diff is high-risk or broad.

Subagent gate:

- Authorized by: not run.
- Why fan-out was useful: this diff touched 47 files, renamed/moved cross-stage modules, removed a UI/API control, and added boundary tests. Separate contract/docs, config-normalization, import-boundary, and UI/test lenses would have been justified.
- Lenses used: none.
- Lenses skipped: correctness/regression, tests/coverage, API/operator contract, config/data validation, import-boundary architecture.

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

- Actionable: reject duplicate generated quantile labels before `generated_feature_names` can deduplicate them.
- Actionable: require actual booleans for policy action `enabled` fields and reject non-finite bounded floats.
- Actionable duplicate: reject non-finite floats in `_bounded_float`.
- Actionable: detect `from mlgate import experiment_grid` in the import-boundary test.
- Nitpick/test suggestion: add a duplicate-quantile-label regression test.

Local review caught:

- Local fallback review caught stale UI/test and stage-index contract text after pipeline-run removal.

Local review missed:

- The config-normalization and import-boundary test issues above.

Local review found valid issue external review missed:

- CodeRabbit reviewed after the local fallback review fix commit, so it did not have the same pre-fix state. Treat this as a sequence, not a head-to-head comparison on identical code.

## Classification

Miss labels:

- [ ] wrong-base
- [x] missed-spec-gap
- [x] missed-contract-risk
- [x] missed-correctness
- [ ] missed-security-data
- [x] missed-test-gap
- [ ] missed-check-output
- [ ] missed-performance-concurrency
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

- If `/review` is user-stopped, record it as user-controlled and do not count it as a tool failure. If `codex review --base` or another review command fails, continue only as a clearly labeled manual/self-review fallback and record the tool failure as evidence. Do not treat the result as a completed built-in `/review`.
- For broad refactors, run explicit contract sweeps for removed public/operator surfaces: API routes, UI controls, tests, README, active specs, and stale-but-still-visible docs.
- When a branch adds import-boundary tests, check alternate import syntax using AST shapes, especially `import package.submodule`, `from package.submodule import x`, and `from package import submodule`.
- In config-normalization code, reject ambiguous booleans and non-finite numeric values. Do not use `bool(...)` for user/config flags unless all accepted input types are already strict booleans.
- In generated-name or identifier code, detect collisions before deduplication. Deduplication should not hide distinct config inputs collapsing to the same output name.
- Deduplicate external reviewer comments before counting misses; overlapping CodeRabbit threads can represent one unique issue.

Reference checklist items:

- API/operator contract lens: removed UI/API commands, route names, button text, tests, docs, and active spec references.
- Config lens: bool coercion, `NaN`/`inf`, bounded floats, finite checks, string flags, and JSON hash behavior.
- Boundary-test lens: AST import forms and alias/import-from coverage.
- Generated-name lens: rounding, normalization, collision detection, and deduplication masking.

Script/context collection needs:

- Optional changed-diff scans for removed route/control names across source, tests, README, docs, and active specs.
- Optional AST import probe fixture for boundary-test changes.
- Optional static scan for `bool(` in config-normalization modules and `dict.fromkeys` in generated-name paths.

Subagent gate implications:

- A 47-file refactor that moves ownership boundaries and removes UI/API controls should trigger selective fan-out or separate local lenses, even if the deterministic checks pass.

Repo-specific guidance needed instead:

- In this repo, `AGENTS.md` says the active workflow-boundary plan outranks stale MBP specs. Reviewers should still identify visible contradictions, but they must distinguish active contract text from known stale background specs.

## Summary For Ledger

One-line summary:

Manual fallback review caught stale pipeline-removal UI/spec follow-through, then CodeRabbit found config-normalization and import-boundary test gaps on the PR.

Best evidence:

- Local fallback final findings for Playwright and MBP stage-index stale `Run Pipeline` expectations.
- Commit `9fa5595` fixed the local fallback findings.
- Live CodeRabbit threads on feature quantile-label collisions, policy bool/NaN validation, and AST import-boundary coverage.
- Local reproductions: `0.801` and `0.804` collapse to one generated name; string `"0"` enables hard filter; `NaN` passes `_bounded_float`; `from mlgate import experiment_grid` parses as `ImportFrom mlgate`.

Biggest miss:

The fallback review focused on removed UI/operator contract follow-through but missed config normalization and import-boundary edge cases introduced by the broader module move.

Worst noise:

CodeRabbit duplicated the non-finite float finding across two actionable threads.

Decision implication:

The future skill should not only ask for "correctness and contracts"; it needs mechanical fallback labeling, removed-surface sweeps, AST import-form checks for boundary tests, and config-normalization edge-case checks.
