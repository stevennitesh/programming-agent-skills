from __future__ import annotations

import errno
import runpy
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = runpy.run_path(
    str(ROOT / "skills/custom/repo-bootstrap/scripts/validate_setup.py")
)


def assert_typed_failure(
    failure: object,
    *,
    kind: str,
    operation: str,
    path: str | None,
) -> None:
    failure_type = VALIDATOR["ValidationFailure"]
    assert isinstance(failure, failure_type)
    assert failure.kind.value == kind
    assert failure.operation == operation
    assert failure.path == path


def test_required_setup_read_normalizes_unreadable_input(
    tmp_path: Path, monkeypatch
) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("setup", encoding="utf-8")
    original_read_text = Path.read_text

    def unreadable(path: Path, *args, **kwargs) -> str:
        if path == target:
            raise PermissionError(errno.EACCES, "secret operating-system detail")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", unreadable)
    failures: list[object] = []

    assert VALIDATOR["read_required"](tmp_path, "AGENTS.md", failures) == ""
    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="filesystem-io",
        operation="read setup file",
        path="AGENTS.md",
    )
    assert "secret operating-system detail" not in VALIDATOR["render_failure"](
        failures[0]
    )


def test_required_setup_read_normalizes_invalid_encoding(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_bytes(b"\xff")
    failures: list[object] = []

    assert VALIDATOR["read_required"](tmp_path, "AGENTS.md", failures) == ""
    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="text-decoding",
        operation="decode setup file",
        path="AGENTS.md",
    )


def test_git_root_check_normalizes_missing_git(tmp_path: Path, monkeypatch) -> None:
    def missing_git(*args, **kwargs):
        raise FileNotFoundError(errno.ENOENT, "secret executable location")

    monkeypatch.setattr(VALIDATOR["subprocess"], "run", missing_git)
    failures = VALIDATOR["git_root_failures"](tmp_path)

    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="git-unavailable",
        operation="find Git root",
        path=None,
    )
    assert "secret executable location" not in VALIDATOR["render_failure"](failures[0])


def test_canonical_source_resolution_normalizes_filesystem_failure(
    monkeypatch,
) -> None:
    contract = (
        ROOT / "skills/custom/repo-bootstrap/engineering-contract.md"
    ).read_text(encoding="utf-8")

    def inaccessible_path(path: Path, *args, **kwargs) -> Path:
        raise PermissionError(errno.EACCES, "secret canonical location")

    monkeypatch.setattr(Path, "resolve", inaccessible_path)
    failures = VALIDATOR["engineering_contract_failures"](
        contract, "docs/agents/engineering-contract.md"
    )

    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="filesystem-io",
        operation="read canonical setup file",
        path="engineering-contract.md",
    )
    assert "secret canonical location" not in VALIDATOR["render_failure"](
        failures[0]
    )


def test_git_output_decoding_failure_is_typed(tmp_path: Path, monkeypatch) -> None:
    def undecodable_output(*args, **kwargs):
        raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "secret decoder detail")

    monkeypatch.setattr(VALIDATOR["subprocess"], "run", undecodable_output)
    failures = VALIDATOR["git_root_failures"](tmp_path)

    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="text-decoding",
        operation="decode Git output from find Git root",
        path=None,
    )
    assert "secret decoder detail" not in VALIDATOR["render_failure"](failures[0])


def test_git_ignore_check_normalizes_invocation_failure(
    tmp_path: Path, monkeypatch
) -> None:
    def unavailable_cwd(*args, **kwargs):
        raise OSError(errno.EACCES, "secret repository location")

    monkeypatch.setattr(VALIDATOR["subprocess"], "run", unavailable_cwd)
    ignored, failure = VALIDATOR["check_ignore"](
        tmp_path, ".tmp/setup-validation-probe"
    )

    assert ignored is None
    assert_typed_failure(
        failure,
        kind="git-invocation",
        operation="check Git ignore state",
        path=None,
    )
    assert "secret repository location" not in VALIDATOR["render_failure"](failure)


def test_repository_root_resolution_omits_private_input(
    monkeypatch, capsys
) -> None:
    private_root = "C:/Users/private-customer/secret-project"

    def inaccessible_path(path: Path, *args, **kwargs) -> Path:
        raise PermissionError(errno.EACCES, "secret operating-system detail")

    monkeypatch.setitem(
        VALIDATOR["main"].__globals__,
        "parse_args",
        lambda: SimpleNamespace(repo=private_root),
    )
    monkeypatch.setattr(Path, "resolve", inaccessible_path)

    assert VALIDATOR["main"]() == 1
    output = capsys.readouterr().out
    assert "[filesystem-io] resolve repository root failed for repository root" in output
    assert "private-customer" not in output
    assert "secret-project" not in output
    assert "secret operating-system detail" not in output


def test_parallel_config_normalizes_invalid_encoding(tmp_path: Path) -> None:
    config = tmp_path / ".codex/config.toml"
    config.parent.mkdir()
    config.write_bytes(b"\xff")
    agent = tmp_path / ".codex/agents/luna_max.toml"
    agent.parent.mkdir()
    template = ROOT / "skills/custom/parallel-implement/assets/luna_max.toml"
    agent.write_bytes(template.read_bytes())

    failures = VALIDATOR["parallel_support_failures"](tmp_path)

    assert len(failures) == 1
    assert_typed_failure(
        failures[0],
        kind="text-decoding",
        operation="decode parallel configuration",
        path=".codex/config.toml",
    )


def test_required_setup_read_preserves_valid_and_missing_results(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("valid setup\n", encoding="utf-8")
    failures: list[object] = []

    assert VALIDATOR["read_required"](tmp_path, "AGENTS.md", failures) == (
        "valid setup\n"
    )
    assert failures == []

    assert VALIDATOR["read_required"](tmp_path, "missing.md", failures) == ""
    assert failures == ["Missing required setup file: missing.md"]
