# R7 SECOM Yield Monitoring PR6

## Sample

- Repo: `stevennitesh/secom-yield-monitoring`
- PR: <https://github.com/stevennitesh/secom-yield-monitoring/pull/6>
- Branch: `docs/public-repo-polish`
- Base: `main` / `8646100`
- Pre-review head: `373a9e5`
- PR follow-up head: `c154807`
- Risk profile: public docs/CLI contract, result artifact provenance, generated evidence snapshot consistency, removed legacy surface references
- Local review mode: `$pre-pr-review` with `codex review --base main` and manual evidence verification
- External review mode: Codex GitHub review; CodeRabbit PR review

## Local Review Outcome

The pre-PR review returned `Safe to PR` after checking:

- `codex review --base main` completed with no actionable findings.
- `make PYTHON=.venv/bin/python check` passed with 190 tests.
- Focused CLI/report tests passed with 30 tests.
- `git diff --check main...HEAD` passed.
- `docs/results/*` report, CSV/JSON evidence, and PNG figures matched `runs/full_study/reports/*` byte-for-byte.
- README commands existed under `scripts/` and CLI help paths were covered.
- Stale-reference sweep found no tracked references to removed archive/notebook/report paths.

## External Review Outcome

Codex GitHub review found one P2 issue:

- `docs/results/evidence/run_manifest.json` recorded `git_commit: 094315c...` as the generating commit, but the reviewed public commit history did not make that hash reachable from the PR head. A public reader checking out the snapshot could fail to resolve or audit the claimed provenance commit.

The PR later added `c154807` to clarify public snapshot provenance. CodeRabbit's later review reported no actionable comments, with CI passing on Python 3.11 and 3.12.

## Misses

The local review correctly compared the checked-in snapshot to the local generated run, but it did not check whether the manifest's recorded provenance commit would be reachable in the published branch history.

## Skill Lessons

- Byte-for-byte equality with local generated artifacts is necessary but not sufficient for a public evidence snapshot.
- Review generated evidence manifests for public auditability: recorded commit hashes, run ids, spec hashes, data versions, and source paths must be reachable or clearly explained from the PR head or published history.
- A stale-reference sweep should include provenance references, not only file paths and commands.
- For docs/results PRs, the review should name whether full regeneration was run, local generated artifacts were compared, and public provenance was checked.

## Verdict Calibration

The local `Safe to PR` verdict was too strong. The deterministic checks and byte comparisons were useful, but the missing provenance reachability check left a real public auditability issue. This sample adds a generated-evidence provenance rule to the skill.
