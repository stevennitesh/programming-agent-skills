"""Run focused pytest checks without the default xdist fanout."""

from __future__ import annotations

import subprocess
import sys


DEFAULT_ARGS = ("tests/test_skill_pack_contracts.py",)


def main(argv: list[str] | None = None) -> int:
    args = list(DEFAULT_ARGS if argv is None else argv)
    if not args:
        args = list(DEFAULT_ARGS)
    command = [sys.executable, "-m", "pytest", "-n", "0", *args]
    return subprocess.run(command).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
