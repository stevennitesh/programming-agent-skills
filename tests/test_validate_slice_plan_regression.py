from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.focused
def test_validate_slice_plan_regression_script_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    script = root / "skills" / "experimental" / "to-slice-plan" / "scripts" / "test_validate_slice_plan.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stdout + result.stderr
