"""Run the canonical helper tests against the exact experimental candidate paths."""

from pathlib import Path

import pytest


class CandidatePaths:
    def pytest_collection_modifyitems(self, session, config, items):
        root = Path(__file__).resolve().parents[4]
        candidate = root / "skills/experimental/parallel-implement/scripts"
        for item in items:
            module = item.module
            if hasattr(module, "LANE"):
                module.LANE = candidate / "lane_worktree.py"
            if hasattr(module, "LEDGER"):
                module.LEDGER = candidate / "run_ledger.py"


if __name__ == "__main__":
    raise SystemExit(
        pytest.main(
            ["-q", "tests/test_parallel_implement_helpers.py"],
            plugins=[CandidatePaths()],
        )
    )
