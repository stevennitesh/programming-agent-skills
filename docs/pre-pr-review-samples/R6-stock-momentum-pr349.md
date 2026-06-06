# R6 Stock Momentum PR349

## Sample

- Repo: `stevennitesh/stock-momentum-strategy-research-platform`
- PR: <https://github.com/stevennitesh/stock-momentum-strategy-research-platform/pull/349>
- Branch: `research/cluster-cap-conditional-audit`
- Base: `main` / `43f3388`
- Pre-review head: `ff3ad2a`
- PR review head: `d95533b`
- Risk profile: config/schema, cluster-aware weighting, risk-cap composition, strategy materialization, validation/dashboard artifacts, diagnostic attribution, tests/checks
- Local review mode: `$pre-pr-review` manual self-review plus attempted/completed `codex review --base main`
- External review mode: CodeRabbit PR review; Codex GitHub review

## Local Review Outcome

The pre-PR review found one material should-fix issue before the PR was finalized:

- YAML experiment matrices could request cluster-aware weighting methods with a non-cluster `signal_kind`.
- That pairing materialized outside the cluster candidate path, so the runner would not produce cluster assignments.
- The later weighting path could then exclude selected symbols as missing cluster assignments.

The review recommended rejecting cluster-aware weighting methods unless `signal_kind == "cluster_rule"` and adding a negative matrix-config test.

Observed checks:

- `git diff --check main...HEAD` passed.
- Focused unittest set passed with 138 tests:
  - `tests.test_cluster_weighting_rules`
  - `tests.test_weighting_rules`
  - `tests.test_validation_candidate_diagnostics`
  - `tests.test_dashboard_validation_candidates`
  - `tests.test_eod_candidate_factory`
  - `tests.test_experiment_grid_registry`
  - `tests.test_research_grid_run`
  - `tests.test_eod_csv_runner`
- `pytest` was not available on PATH.
- `ruff` was not installed in the repo venv.
- `codex review --base main` eventually completed and reported no actionable findings.

## External Review Outcome

After the branch was updated, CodeRabbit reported one minor documentation wording issue:

- Replace `hard45` with a clearer `hard 45` or `hard-45` wording in documentation.

Codex GitHub review then reported two P2 semantic findings:

- Cluster-aware weighting applied security caps only when `weighting.metadata.cap_rule == "sp_momentum"` or `weighting.max_position_weight` was set. That missed configurations where the standard `risk.max_position_weight` should flow through `_max_position_weight(config)` and still cap positions.
- Cluster-cap visibility diagnostics copied all residual uninvested weight into `avg_cluster_cap_cash_weight` for cluster-cap candidates. When other caps or intentional underinvestment contribute, this overstates cluster-cap drag and can mislead tuning or rejection decisions.

## Skill Lessons

- Config/schema review should not stop at enum membership. New methods, strategy modes, or matrix fields often require compatible companion fields and producer paths.
- A strategy option that depends on a produced artifact should be rejected early when the selected signal/factory path cannot produce that artifact.
- Review cap composition through the canonical accessor/fallback path. If a shared helper reads both risk-level and method-level caps, tests need to cover both input locations.
- Diagnostic metrics need causal attribution. A residual metric should not be relabeled as cluster-cap-specific when multiple independent caps or underinvestment rules can create the same residual.
- Negative tests for incompatible config-field combinations are high value because happy-path matrices can be valid while user-supplied matrices remain unsafe.
- A completed local `codex review` with no findings can still miss cross-file config/factory/runtime and diagnostic-attribution gaps; manual semantic tracing remains necessary.
- Style-only PR comments should stay optional/noise unless the user requested editorial polish.

## Verdict Calibration

The local pre-PR verdict was directionally accurate: `PR after fixes`, but incomplete. It caught the matrix compatibility issue before PR finalization, while the later GitHub Codex review caught two additional semantic issues around risk-cap fallback and diagnostic attribution. This sample supports stronger config-compatibility, cap-composition, and research-diagnostics review rules.
