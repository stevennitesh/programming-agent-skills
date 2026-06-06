# R4 - secom-yield-monitoring PR 5

## Sample Metadata

Sample ID: R4

Repo: `stevennitesh/secom-yield-monitoring`

Date captured: 2026-06-06

Reviewer: Codex local pre-PR review, then CodeRabbit on PR

Sample type: real

Risk profile: dependency/runtime contract, broad artifact validation, CLI workflow failure handling, reporting/audit contracts

Target:

- Base: `origin/main` at `14a892a69882e0387c5f15ba7207c4698681944a`
- Local pre-PR review target: `audit/classifier-model-evaluation` at `e324f6859315582afd452d0183eb3e9907b4155d`
- PR review target after local fix: PR #5 at `13abb2717b5fdbce7e2e48cdf293299541199603`

Base: `main`

Comparison command:

```bash
codex review --base origin/main "<AGENTS.md pre-PR review prompt>"
```

Spec, issue, PRD, or user request:

- PR title: `Validate study artifact contracts and Python support`
- PR body summary: harden workflow status, audit, report, and artifact contract handling; add CLI and metadata regression coverage; require Python 3.11 to match pinned dependency metadata.

External evidence available:

- PR: https://github.com/stevennitesh/secom-yield-monitoring/pull/5
- CodeRabbit review: 2 actionable comments and 1 nitpick on current head.
- CI: `Ruff and pytest` passed on current head.
- PR body verification: `make PYTHON=.venv/bin/python check`, `git diff --check`, and `git diff --cached --check`.

## Repo Evidence Read

Instructions and standards:

- `AGENTS.md`: the branch was reviewed with the pre-PR review prompt.
- nested `AGENTS.md`: not checked for this sample.
- review docs: not checked for this sample.
- `CONTEXT.md` or ADRs: not checked for this sample.
- README/contributing: README was part of the diff and CodeRabbit left one grammar/style comment.
- tool configs: `pyproject.toml`, `requirements.txt`, `Makefile`, and metadata tests were part of the diff.

Source evidence:

- changed files: 37 files across `.gitignore`, `Makefile`, README, dependency metadata, scripts, `src/secom/**`, and tests.
- callers checked by local review: artifact validators, workflow manifests, full study orchestration, CLI scripts, reporting, report figures, temporal robustness, benchmark workflows, metadata/dependency files, and tests.
- tests/fixtures checked by local review: full pytest and ruff.
- CI/check output checked: PR body, live PR metadata, CodeRabbit review body/comments, and PR checks.

Command discovery:

- source of commands: local pre-PR transcript, PR body, live PR state, and repo metadata.
- commands found:
  - `.venv/bin/python -m pytest -q`
  - `.venv/bin/python -m ruff check .`
  - `make PYTHON=.venv/bin/python check`
  - `git diff --check`
  - `git diff --cached --check`
  - `codex review --base origin/main`
- commands run during local pre-PR review:
  - `.venv/bin/python -m pytest -q` passed with 186 tests.
  - `codex review --base origin/main` completed after a non-blocking read-only PATH warning.
  - `.venv/bin/python -m ruff check .` passed.
  - local dependency metadata probes checked installed package `Requires-Python` values for the major pinned runtime/build/test dependencies.
- commands run during evidence capture:
  - live PR metadata, review, comment, and check queries with `gh`.
  - local `git show` checks compared `pyproject.toml` at the local review head and current PR head.
- commands skipped and why:
  - Full local checks were not rerun during evidence capture because this sample is review-evidence classification, not PR fix verification.

## Known Ground Truth

Known true issues:

1. Local pre-PR review found a real install/runtime contract bug at `e324f68`: the project still advertised `requires-python = ">=3.10"` while newly pinned NumPy/Pandas/SciPy/scikit-learn releases required Python 3.11 or newer. This would make installation unsatisfiable in an advertised Python 3.10 environment.
2. The branch fixed the local finding by commit `13abb27`, raising `requires-python` to `>=3.11` and aligning the Ruff target with Python 3.11.
3. CodeRabbit later found a minor dependency-evidence gap on current head: `skrebate==0.62` lacks a `requires_python` metadata field, so Python 3.11 compatibility is not explicitly documented by package metadata.

Known non-issues / tempting false positives:

1. CodeRabbit's README comment changes `Audit generated artifacts` to `Audit-generated artifacts`. This is style-only and should not drive pre-PR review output.
2. CodeRabbit's duplicate `_project_root()` helper comment is a maintainability nitpick that suggests a shared helper across three workflow modules. It may be reasonable cleanup, but it is not a pre-PR blocker without a concrete failure mode.
3. CodeRabbit reviewed after the local dependency-floor fix, so it did not evaluate the same pre-fix dependency state that local review flagged.

Expected verdict:

- At `e324f68`: PR after fixes, because advertised Python support contradicted pinned dependency metadata.
- At `13abb27`: major local finding fixed; PR checks passed; CodeRabbit left minor follow-up comments to triage.

Remaining uncertainty:

- The copied transcript has some collapsed diff output, so the exact full review context is incomplete.
- This sample does not prove whether CodeRabbit would have caught the original Python-floor bug, because the PR was reviewed after the fix commit.
- The `skrebate==0.62` compatibility comment is a weaker issue than the original Python-floor mismatch because it is about missing metadata/documentation, not a demonstrated install failure.

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

- The local review inspected the branch diff against `origin/main`.
- `.venv/bin/python -m pytest -q` passed with 186 tests.
- `codex review --base origin/main` completed and produced the dependency-floor finding.
- `.venv/bin/python -m ruff check .` passed.
- The local review inspected package metadata for major pinned dependencies.

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
| Align dependency pins with advertised Python support | P2 | yes | n/a | strong | Pinned dependencies required Python 3.11 while project metadata advertised Python 3.10 support. |

Missed issues:

- Local review did not explicitly check or document `skrebate==0.62`, whose package metadata lacks a `requires_python` field.

False positives/noise:

- None captured in the final local pre-PR review output.

Verdict:

PR after fixes. The local review caught a real dependency/runtime contract issue that was fixed before PR review.

## Review Mode: Selective Subagents

Use only when the diff is high-risk or broad.

Subagent gate:

- Authorized by: not run.
- Why fan-out was useful: this diff touched dependency metadata, CLI behavior, failure manifests, artifact validation, reporting, and tests. A dedicated dependency/install lens would have been justified even though the single local review caught the main issue.
- Lenses used: none.
- Lenses skipped: dependency/install contract, CLI/workflow failure behavior, artifact validation, reporting/audit contract, tests/coverage.

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

- Actionable minor: verify and document Python 3.11 compatibility for `skrebate==0.62`, because package metadata does not declare `requires_python`.
- Actionable minor/style: hyphenate `Audit generated artifacts` in README.
- Nitpick: consider centralizing duplicate `_project_root()` helpers.

Local review caught:

- Local review caught the main dependency/Python-floor contract bug before PR review.

Local review missed:

- The weaker `skrebate==0.62` metadata/documentation gap.

Local review found valid issue external review missed:

- CodeRabbit reviewed after the Python-floor fix, so this is not a head-to-head miss.

## Classification

Miss labels:

- [ ] wrong-base
- [ ] missed-spec-gap
- [x] missed-contract-risk
- [ ] missed-correctness
- [ ] missed-security-data
- [ ] missed-test-gap
- [ ] missed-check-output
- [ ] missed-performance-concurrency
- [x] missed-context-source

Noise labels:

- [ ] off-diff
- [x] style-only
- [ ] speculative
- [x] broad-rewrite
- [ ] duplicate
- [ ] stale
- [ ] wrong-severity
- [ ] unsupported

## Skill Implications

Rules to add or strengthen:

- Add a dependency/runtime contract lens: when a PR changes `pyproject.toml`, `requirements.txt`, build-system pins, lock/install commands, or tool target versions, cross-check advertised Python support against every pinned runtime/build/test dependency.
- Do not stop dependency metadata checks after the obvious major packages. Verify every pinned package, including smaller runtime dependencies such as `skrebate`.
- If a package has no `requires_python` metadata, require another evidence source: install/import smoke under the advertised Python floor, upstream docs, or an explicit repo note explaining compatibility.
- Cross-check `requires-python`, `tool.ruff.target-version`, `requirements.txt`, build-system requirements, Makefile install order, metadata tests, and runtime `library_versions()` reporting when dependency policy changes.
- Suppress grammar-only documentation comments and optional shared-helper refactors from blocking or should-fix review output unless they create a concrete failure mode or the user requested cleanup.

Reference checklist items:

- Dependency/install lens: Python floor, package `Requires-Python`, package existence, build-system pins, editable install behavior, Makefile install order, test/dev dependency pins, tool target versions, and packages with missing metadata.
- Tests lens: metadata tests should fail when the Python floor and pinned dependency metadata diverge.

Script/context collection needs:

- Optional dependency metadata script that reads `pyproject.toml` and `requirements.txt`, checks each pinned package version, compares `Requires-Python` to the project floor, and reports packages with missing metadata as evidence gaps.
- Optional install/import smoke guidance for packages without metadata, scoped to the advertised Python floor when that interpreter is available.

Subagent gate implications:

- A broad PR that changes dependency pins or Python support should qualify for a dependency/install contract lens even if source tests pass.

Repo-specific guidance needed instead:

- None yet. The dependency/Python-floor check is portable.

## Summary For Ledger

One-line summary:

Local pre-PR review found a real Python support versus pinned dependency mismatch, which was fixed before CodeRabbit reviewed the PR.

Best evidence:

- Local final finding: `requires-python = ">=3.10"` contradicted NumPy/Pandas/SciPy/scikit-learn pins that require Python 3.11 or newer.
- Current PR head `13abb27` raises `requires-python` to `>=3.11`.
- CI `Ruff and pytest` passed on the current PR head.
- CodeRabbit current-head review found only minor follow-up items around README style, `skrebate` compatibility documentation, and duplicated helper cleanup.

Biggest miss:

The local review did not verify every pinned package; `skrebate==0.62` lacks package metadata for Python compatibility and should have been checked or documented.

Worst noise:

The README hyphenation and shared-helper extraction comments are not useful pre-PR blockers.

Decision implication:

The future review guidance needs a lightweight dependency/install lens, but it should distinguish true install-contract breaks from grammar or optional cleanup comments.
