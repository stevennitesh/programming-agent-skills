# Pre-PR Review Evidence Ledger

Use this ledger to summarize review evidence gathered across repos. Put detailed notes in separate sample files using `docs/pre-pr-review-sample-template.md`.

## Sample Index

| ID | Repo | Sample type | Risk profile | Target | Base | Spec/source | Review modes run | External evidence | Sample notes path | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | `stevennitesh/secom-yield-monitoring` | real | data-schema-risk, artifact lineage | local `/review` @ `0803ea6`; PR #4 fixed through `c30d9a9` | `main` | `/review` transcript, PR body, CodeRabbit thread | structured `/review` before PR; CodeRabbit on PR | local true positive, CodeRabbit true positive, CI success, resolved thread | `docs/pre-pr-review-samples/R1-secom-yield-monitoring-pr4.md` | captured |
| R2 | `stevennitesh/StockMarket-ML-Gate` | real | broad refactor, operator contract, config normalization | fallback review @ `15ca557`; PR #257 @ `9fa5595` | `main` | `/review` transcript, PR body, CodeRabbit threads | user-stopped first `/review`; failed nested `codex review --base`; manual fallback review; CodeRabbit on PR | local true positives, CodeRabbit true positives, unresolved threads | `docs/pre-pr-review-samples/R2-stockmarket-ml-gate-pr257.md` | captured |
| R3 | `stevennitesh/stock-momentum-strategy-research-platform` | real | performance hot path, cache identity, dashboard telemetry | local fallback review; PR #347 @ `0a8d92e` | `main` | `/review` transcript, PR body, CodeRabbit comments, Codex GitHub comments | failed nested `codex review --base`; manual fallback review; CodeRabbit on PR; Codex GitHub on PR | local clean verdict, external true positives, duplicate external finding, checks passed | `docs/pre-pr-review-samples/R3-stock-momentum-pr347.md` | captured |
| R4 | `stevennitesh/secom-yield-monitoring` | real | dependency/runtime contract, broad artifact validation, CLI workflow failures | local `/review` @ `e324f68`; PR #5 fixed through `13abb27` | `main` | `/review` transcript, PR body, CodeRabbit comments, CI | completed `codex review --base`; CodeRabbit on PR | local true positive, external minor follow-up, CI success, style/cleanup noise | `docs/pre-pr-review-samples/R4-secom-yield-monitoring-pr5.md` | captured |
| R5 | `stevennitesh/StockMarket-ML-Gate` | real | performance/cache, artifact reuse, generated commands, time-series fills | `$pre-pr-review` on `fix-experiment-grid-run-findings`; PR #258 @ `1cd3cc0` | `main` | pre-PR transcript, PR body, CodeRabbit review threads | skill-guided manual review; long-running `codex review --base`; CodeRabbit on PR | local true positives, delayed Codex true positive, external true positives, focused tests passed | `docs/pre-pr-review-samples/R5-stockmarket-ml-gate-pr258.md` | captured |
| R6 | `stevennitesh/stock-momentum-strategy-research-platform` | real | config/schema, cluster weighting, cap composition, diagnostic attribution | `$pre-pr-review` on `research/cluster-cap-conditional-audit`; PR #349 @ `d95533b` | `main` | pre-PR transcript, PR body, CodeRabbit thread, Codex GitHub comments | skill-guided manual review; completed `codex review --base`; CodeRabbit on PR; Codex GitHub on PR | local true positive, local Codex no findings, Codex GitHub true positives, CodeRabbit style-only nit | `docs/pre-pr-review-samples/R6-stock-momentum-pr349.md` | captured |
| F1 |  | fixture | missed-spec-gap |  |  |  |  |  |  | planned |
| F2 |  | fixture | weak-test-surface |  |  |  |  |  |  | planned |
| F3 |  | fixture | data-schema-risk |  |  |  |  |  |  | planned |

## Findings Summary

| ID | Mode | Blocking true positives | Should-fix true positives | False positives | Missed issues | Best finding | Worst noise | Verdict accuracy |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| R1 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R1 | structured | 0 | 1 | 0 | 1 related issue later found | P2 feature-stability selected-flag coercion | None captured | correct pre-PR block |
| R1 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R2 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R2 | structured-fallback | 0 | 2 | 0 | 4 external threads / 3 unique issues | Stale removed pipeline UI/spec expectations | None captured | correct pre-PR block, incomplete breadth |
| R2 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R3 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R3 | structured-fallback | 0 | 0 | 0 | 7 unique external issues | None | None captured | incorrect clean verdict |
| R3 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R4 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R4 | structured | 0 | 1 | 0 | 1 minor external follow-up | Python floor conflicted with dependency pins | None captured | correct pre-PR block |
| R4 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R5 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R5 | structured | 0 | 2 | 0 | 6 external issues / 5 unique bug classes | Artifact reuse ignored current CSV paths | None captured | correct pre-PR block, incomplete breadth |
| R5 | built-in Codex review | 0 | 1 | 0 | n/a | Cache materialization idempotency | Long-running quiet session complicated orchestration | useful delayed second opinion |
| R5 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R6 | baseline | n/a | n/a | n/a | n/a | Not run | Not run | Not run |
| R6 | structured | 0 | 1 | 0 | 2 external semantic issues after fix | Incompatible matrix signal/weighting pairing | None captured | correct pre-PR block, incomplete breadth |
| R6 | built-in Codex review | 0 | 0 | 0 | 1 local-only true positive plus 2 later GitHub Codex issues | No findings | None captured | missed cross-file config/factory/runtime and cap/diagnostic issues |
| R6 | Codex GitHub review | 0 | 2 | 0 | n/a | Risk-level cap fallback skipped by cluster weighting | None captured | useful PR second opinion |
| R6 | subagents | n/a | n/a | n/a | n/a | Not run | Not run | Not run |

## Miss Taxonomy Counts

| Miss type | Count | Sample IDs | Skill implication |
| --- | ---: | --- | --- |
| wrong-base |  |  |  |
| missed-spec-gap | 1 | R2 | For removed public/operator surfaces, sweep active docs/specs plus stale visible docs and classify authority. |
| missed-contract-risk | 5 | R2, R3, R4, R5, R6 | Strengthen broad-refactor, hot-path, and dependency review for generated-name collisions, config normalization, import-boundary tests, cache identity, skip contracts, cap composition, artifact ordering, generated commands, and Python/install compatibility. |
| missed-correctness | 5 | R1, R2, R3, R5, R6 | Strengthen analogous-pattern sweeps, config/data normalization edge-case checks, cache-key completeness, cap fallback checks, missing-anchor fill checks, and fast-path equivalence checks. |
| missed-security-data |  |  |  |
| missed-test-gap | 5 | R1, R2, R3, R5, R6 | Require malformed-input, boundary, stale-cache, changed-policy, existing-destination, copy-fallback, mixed-cap, missing-anchor, skip-exit, and fast-path equivalence tests for each changed contract path, not only the first reviewed one. |
| missed-check-output |  |  |  |
| missed-performance-concurrency | 2 | R3, R5 | Add a dedicated hot-path review lens for cache keys, stale cache identity, materialization idempotency, skip semantics, telemetry counts, and producer-consumer ordering. |
| missed-diagnostic-attribution | 1 | R6 | Distinguish aggregate residual measurements from rule-specific causal attribution in dashboards, reports, and research readouts. |
| missed-context-source | 1 | R4 | For dependency pinning, inspect every pinned package and use package metadata, install/import evidence, or explicit docs when metadata is missing. |

## Noise Taxonomy Counts

| Noise type | Count | Sample IDs | Skill implication |
| --- | ---: | --- | --- |
| off-diff |  |  |  |
| style-only | 3 | R1, R4, R6 | Keep terminology/style comments optional unless requested. |
| speculative |  |  |  |
| broad-rewrite | 1 | R4 | Suppress optional shared-helper extraction suggestions unless they prevent a concrete failure or the user asked for cleanup. |
| duplicate | 2 | R2, R3 | Deduplicate overlapping external review comments before counting unique issues. |
| stale |  |  |  |
| wrong-severity |  |  |  |
| unsupported |  |  |  |

## Command Discovery

| Repo | Source of commands | Commands found | Commands run | Commands skipped and why | Skill/script implication |
| --- | --- | --- | --- | --- | --- |
| `secom-yield-monitoring` | `/review` transcript, PR body, and CI | `.venv/bin/python -m pytest -q tests/test_selection.py tests/test_univariate_selectors.py tests/test_study_audit.py tests/test_benchmark_replication.py tests/test_temporal_robustness.py tests/test_final_report.py tests/test_report_skeleton.py`; `make PYTHON=.venv/bin/python check`; `scripts/run_audit.py --output-dir runs/benchmark_replication --strict`; `scripts/run_audit.py --output-dir runs/evidence/2026-06-04-full-benchmark-pearson-original-krr-tuned/benchmark_replication --strict`; `git diff --cached --check` | `/review` ran targeted tests and `make check`; PR checks inspected; small local Pandas reproduction run | Full secom checks not rerun during evidence capture because current PR CI was already checked | Save raw `/review` transcript including uncollapsed command outputs for future samples. |
| `secom-yield-monitoring` R4 | `/review` transcript, PR body, CodeRabbit, and CI | `.venv/bin/python -m pytest -q`; `.venv/bin/python -m ruff check .`; `make PYTHON=.venv/bin/python check`; `git diff --check`; `git diff --cached --check`; `codex review --base origin/main` | local review ran full pytest, completed `codex review --base`, ran ruff, and probed dependency metadata; PR checks inspected | Full local checks not rerun during evidence capture because current PR CI was already checked | Add dependency metadata collection for every pinned package, including packages with missing `requires_python`. |
| `StockMarket-ML-Gate` | fallback review transcript, PR body, and CodeRabbit | `.venv/bin/python -m pytest -q`; `.venv/bin/python -m ruff check src`; `.venv/bin/ruff check src/tests/test_analysis_ui_playwright.py`; `.venv/bin/python -m pytest -q src/tests/test_analysis_ui_playwright.py --run-slow -rs`; `git diff --check` | fallback review ran full pytest and ruff; PR state inspected; small reproductions run for CodeRabbit findings | Full tests not rerun during evidence capture because this was classification, not fix verification | Record user-stopped review separately from actual review-command failures. |
| `StockMarket-ML-Gate` R5 | pre-PR transcript, PR body, CodeRabbit review, and Codex review output | `.venv/bin/python -m pytest -q src/tests/test_analysis_feature_dataset_evaluation.py src/tests/test_workflow_dataset_build.py src/tests/test_experiment_grid_fold_validation.py src/tests/test_experiment_grid_runner.py src/tests/test_feature_engineering_build_benchmark.py src/tests/test_feature_engineering_snapshot_cache_reuse.py`; `git diff --check origin/main...HEAD`; `codex review --base origin/main` | skill-guided review ran focused pytest, diff whitespace check, manual source inspection, and a long-running `codex review --base` | Full suite not run in transcript; external review supplied additional misses after PR opened | Broad cache/hot-path reviews should explicitly inspect key inputs, materialization idempotency, generated commands, optional readers, and missing-anchor fills. |
| `stock-momentum-strategy-research-platform` | local transcript, PR body, live CodeRabbit/Codex review comments, and `pyproject.toml` | `.venv/bin/python -m pytest -q tests/test_eod_walk_forward_validation.py tests/test_validation_stability.py tests/test_dashboard_validation_candidates.py tests/test_runtime_benchmark_matrix.py tests/test_eod_csv_runner.py tests/test_research_grid_run.py`; `.venv/bin/python -m unittest tests.test_eod_walk_forward_validation tests.test_validation_stability tests.test_dashboard_validation_candidates tests.test_runtime_benchmark_matrix tests.test_eod_csv_runner tests.test_research_grid_run`; `.venv/bin/python -m unittest discover -s tests`; `git diff --check main...HEAD`; `git diff --check origin/main...HEAD` | local fallback review ran targeted unittest modules, full unittest discovery, and `git diff --check`; PR state and review comments inspected | `pytest` path failed because `pytest` was not installed in the venv; full tests not rerun during evidence capture because this was classification, not fix verification | Add command-discovery fallback from pytest to unittest when repo evidence shows unittest is the working check. |
| `stock-momentum-strategy-research-platform` R6 | pre-PR transcript, PR body, CodeRabbit review, local Codex review, and Codex GitHub review | `.venv/bin/python -m unittest tests.test_cluster_weighting_rules tests.test_weighting_rules tests.test_validation_candidate_diagnostics tests.test_dashboard_validation_candidates tests.test_eod_candidate_factory tests.test_experiment_grid_registry tests.test_research_grid_run tests.test_eod_csv_runner`; `git diff --check main...HEAD`; `codex review --base main` | skill-guided review ran focused unittest set, diff whitespace check, manual source inspection, and completed `codex review --base` | `pytest` unavailable on PATH; `ruff` not installed in venv | Config/matrix reviews should trace method enum values through factory/runtime artifact producers, cap accessors, and diagnostic attribution paths. |

## Subagent Evidence

| ID | Was fan-out justified? | Lenses used | Unique true positives added | Noise added | Parent dedup needed? | Gate implication |
| --- | --- | --- | ---: | ---: | --- | --- |
| R1 | yes, in hindsight | data/schema and tests/coverage would have fit | unknown | unknown | unknown | Broad artifact-schema and lineage-validation PRs should qualify for selective fan-out. |
| R2 | yes | contract/docs, config normalization, import boundaries, UI/tests | unknown | unknown | unknown | Broad ownership-boundary refactors and removed UI/API controls should qualify for selective fan-out. |
| R3 | yes | performance/cache, dashboard telemetry, artifact ordering, selection semantics, tests/coverage | unknown | unknown | yes | Hot-path optimization PRs should qualify for selective fan-out even when deterministic checks pass. |
| R4 | yes | dependency/install, CLI/workflow failures, artifact validation, reporting/audit, tests/coverage | unknown | unknown | unknown | Dependency pin or Python support changes should trigger a dependency/install lens even when tests pass. |
| R5 | yes | performance/cache, generated commands, time-series fills, artifact reuse, tests/coverage | unknown | unknown | yes | Broad cache and runtime-improvement PRs should qualify for selective fan-out even when local review already found blockers. |
| R6 | yes | config/schema, strategy materialization, cap composition, diagnostic attribution, tests/coverage | unknown | unknown | yes | Cross-file config/factory/runtime and research-diagnostic reviews should use separate lenses when many strategy modes or cap variants are added. |

## Design Implications

Use this section after every few samples.

### Rules To Add To `SKILL.md`

- Add an analogous-pattern sweep rule: when review finds one concrete bug class, search the touched area for neighboring instances before final verdict.
- Add a Pandas/dataframe checklist item: scrutinize `.astype(bool)`, `astype(int)`, `dropna`, and numeric casts on marker, selected, enabled, active, or `is_*` columns, especially for CSV-backed artifacts where `"False"`, `"0"`, fractional values, non-numeric strings, and missing values may appear.
- Require malformed marker-flag tests when review changes select/filter logic for artifact validation, and check each changed marker column.
- Add fallback labeling: user-stopped reviews are not tool failures; failed review commands should trigger manual/self-review fallback labeling and report the tool failure.
- Add removed-surface sweeps for broad refactors: API routes, UI controls, tests, README, active specs, and visible stale docs with authority classified.
- Add boundary-test checks for alternate AST import forms, including `from package import submodule`.
- Add config-normalization checks for ambiguous booleans and non-finite floats.
- Add config-compatibility checks for new enum/method values that require companion fields, signal kinds, artifact producers, model families, or execution modes.
- Add cap-composition checks for policy values available through multiple layers, such as method-level and risk-level caps.
- Add diagnostic-attribution checks so aggregate residuals are not labeled as caused by one rule when multiple rules can contribute.
- Add generated-name collision checks before deduplication.
- Add performance/cache checks for hot-path changes: cache-key completeness, stale cache identity, skip/exit semantics, timing counter correctness, and hot/cold path equivalence.
- Add producer-consumer artifact-ordering checks for report, gate, dashboard, and manifest generation.
- Add fast-path semantic equivalence checks when a PR prunes payloads, metrics, or columns before shared ranking or selection logic.
- Add content-addressed cache-key completeness checks against every field consumed by the cached payload, including split policy/profile/window fields.
- Add warm-hit materialization checks for existing destinations, hardlink failure, copy fallback, and cache-source immutability.
- Add artifact-reuse checks that compare current requested output paths and ensure every cold-path artifact is materialized or explicitly unnecessary.
- Add time-series missing-anchor checks for `ffill`, `merge_asof`, grouped fills, and shifted sparse features.
- Add generated shell-command checks for quoting dynamic paths and values.
- Add optional JSON/YAML reader checks for malformed, unreadable, and non-object documents when the caller contract expects a tolerant summary.
- Add test-spy checks for permissive `raising=False` or equivalent behavior when the target symbol is expected to exist.
- Add dependency/runtime contract checks for changes to Python support, `pyproject.toml`, `requirements.txt`, build-system pins, install commands, and tool target versions.
- When dependency pins change, verify every pinned package against the advertised Python floor; packages with missing metadata need install/import evidence or explicit compatibility documentation.
- Keep style-only wording comments out of blocking or should-fix review output unless editorial polish is requested.

### Details To Move To References

- Data/schema reference: CSV round-trip boolean semantics, nullable values, fractional values, non-numeric strings, dropped malformed rows, and marker-flag coercion.
- Tests reference: validation changes need positive and negative contract cases.
- Refactor contract reference: removed surface checklist, active-vs-stale doc authority, import-boundary AST forms, generated-name collision risks, config-normalization edge cases, config compatibility across factory/runtime producer paths, and policy fallback paths.
- Diagnostics reference: aggregate vs causal metrics, mixed-cap residuals, event-level attribution, and report labels that imply causality.
- Performance/cache reference: cache key inputs, split-policy identity, identity/freshness checks, materialization idempotency, output-path reuse, skip status and CLI exit semantics, telemetry counters, producer-consumer artifact ordering, and fast-path tie-breakers.
- Dependency/install reference: project Python floor, package `Requires-Python`, missing package metadata, build-system pins, Makefile install order, tool target versions, and metadata tests.
- Generated-command reference: shell quoting for paths, manifests, run directories, timing sidecars, and user-controlled values.
- Time-series feature reference: missing anchors, completed-bin semantics, grouped fills, shifted sparse mappings, and `NaN` preservation.

### Script Needs

- Optional changed-diff scan for `.astype(bool)`, `astype(int)`, `dropna`, and boolean-looking dataframe columns as review context, not an automatic failure.
- Optional removed route/control-name scan across source, tests, README, docs, and active specs.
- Optional AST import fixture for boundary-test changes.
- Optional scan for `bool(` in config-normalization modules and `dict.fromkeys` in generated-name paths.
- Optional scan for newly accepted config enum/method values and whether loaders reject incompatible companion fields.
- Optional scan for cap helpers or policy accessors where callers gate behavior on one config field but shared code falls back to another.
- Optional scan for diagnostics that copy an aggregate residual into a rule-specific metric name.
- Optional scan for cache-key builders whose downstream calls pass wider candidate or scenario identities than the key includes.
- Optional scan for cache-key builders that key on date cutoffs while downstream payloads consume split policies, profiles, recipes, windows, or generated feature identities.
- Optional scan for `os.link`, `shutil.copy2`, hardlink/copy fallback, `Path.exists`, and destination materialization code without existing-destination tests.
- Optional scan for unquoted formatted shell commands in benchmark or command-packet builders.
- Optional scan for `ffill`, `merge_asof`, and grouped fill operations in feature builders without missing-anchor tests.
- Optional scan for `raising=False` in tests.
- Optional scan for hard-coded telemetry counts near repeated read/write wrappers.
- Optional scan for `returncode` aggregation over rows that also carry `run_executed`, skipped, or preflight status fields.
- Optional scan for report/gate/dashboard generation before the producer stage writes the artifact being consumed.
- Optional dependency metadata script that reads `pyproject.toml` and `requirements.txt`, checks each pinned version, compares package `Requires-Python` to the project floor, and reports missing metadata.

### Repo-Specific Guidance Instead Of Portable Skill Rules

- None from R1. The miss appears portable to Pandas/data artifact review.
- R2 repo-specific note: `StockMarket-ML-Gate` AGENTS says the active workflow-boundary plan outranks stale MBP specs. Reviewers should still identify visible contradictions, but must classify whether each spec is active authority or stale background.
- None from R4. The Python floor and dependency-pin checks are portable.

### Open Questions Before V1

- Need raw local `/review` transcripts with uncollapsed command outputs for future samples.
- Need one low-risk sample where external review also agrees with a clean local verdict.

## V1 Readiness Check

- [x] At least 3 real samples captured.
- [x] At least 1 high-risk sample captured.
- [ ] At least 1 low-risk sample captured.
- [ ] At least 2 review modes compared for most samples.
- [x] Repeated misses/noise summarized.
- [ ] Proposed skill rules trace to evidence or pressure tests.
- [ ] Fixture samples created or explicitly deferred.
