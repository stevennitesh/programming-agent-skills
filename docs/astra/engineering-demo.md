# Installer and worktree demonstrations

These examples exercise authored Python tools using temporary fixtures. They
show specific package behavior; they do not measure the quality or productivity
of an AI-generated implementation.

## Preserve an edited skill during an update

The [modified-copy regression](../../tests/test_install_skills.py#L1207-L1227)
creates a source skill called `alpha`, installs version `v1`, then changes its
installed content to `personal change`. The source advances to `v2`.

When the installer attempts the update, it raises an `overwrite modified managed
skill` error. The test compares the complete installed tree and global
instructions before and after: both remain unchanged. No transaction remains.
This prevents a managed update from silently discarding an edited installed copy.

## Recover after a committed update

The [committed-cleanup regression](../../tests/test_install_skills.py#L558-L596)
updates `alpha` to `v2` and injects a failure while clearing operation claims.
The retained transaction reports `committed`, and the installed skill is already
`v2`. Recovery returns `cleared-commit`, retains `v2`, and removes the transaction.
It distinguishes failed cleanup from an update that must be rolled back.

## Keep ignored artifacts during worktree cleanup

The [worktree regression](../../tests/test_lane_worktree.py#L175-L246)
creates an isolated Git worktree, then places `worker.cache` and a pytest cache
inside it. Git reports a clean worktree because the files are ignored. The helper
nevertheless reports them in `ignored_entries` and refuses cleanup with
`ignored artifacts present`. The test verifies that `worker.cache` survives.

This check covers both the current Astra helper and the retained custom helper.
The helper reports mechanical eligibility; the caller still establishes that
no agent is actively using the worktree.

## Reproduce these controlled examples

Run from the repository root with a local environment and the pinned
development dependencies:

```sh
python -m venv .venv
# Activate .venv for your shell, then:
python -m pip install -r requirements-dev.txt
python -m pytest -n 0 tests/test_install_skills.py tests/test_lane_worktree.py -k "refuses_to_overwrite_a_modified_managed_skill or committed_cleanup_failure_recovers_without_rolling_back or inspect_and_cleanup_block_ignored_artifacts"
python -m scripts.validate_skills --public
```

These tests operate on temporary fixtures. They do not install the pack into
your personal skills directory. [CI](../../.github/workflows/ci.yml) runs public
validation and the full suite on Ubuntu and Windows.

For real installation and recovery commands, use
[Installation and recovery](../../INSTALLATION.md). The actual implementation
owners are the [installer](../../scripts/install_skills.py),
[worktree helper](../../skills/astra/parallel-implement/scripts/lane_worktree.py),
and [validator](../../scripts/validate_skills.py).
