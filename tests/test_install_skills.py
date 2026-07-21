from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import install_skills, skill_pack_contract


def write_source_skill(root: Path, name: str, marker: str) -> None:
    skill = root / "skills/custom" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(marker, encoding="utf-8")


def write_template(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\n"
        "- **Route:** Suggest `$skill-router`.\n",
        encoding="utf-8",
    )


def tree_snapshot(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def transaction_dirs(skills_dir: Path) -> list[Path]:
    return sorted(skills_dir.parent.glob(".programming-agent-skills-transaction-*"))


def test_install_lock_excludes_a_recovery_process(tmp_path: Path) -> None:
    transaction = tmp_path / install_skills.ACTIVE_TRANSACTION_NAME
    transaction.mkdir()
    install_skills.write_transaction_state(
        transaction,
        install_skills.preparing_transaction_state(
            tmp_path / "skills",
            tmp_path / "AGENTS.md",
            [],
            False,
        ),
    )

    with install_skills.install_lock(tmp_path):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "scripts.install_skills",
                "--recover-transaction",
                str(transaction),
                "--skills-dir",
                str(tmp_path / "skills"),
                "--global-agents",
                str(tmp_path / "AGENTS.md"),
            ],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    assert result.returncode == 1
    assert "another install or recovery process owns" in result.stderr.lower()
    assert transaction.is_dir()


def test_incomplete_transaction_blocks_another_root_sharing_global_bootstrap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root_a = tmp_path / "repo-a"
    root_b = tmp_path / "repo-b"
    skills_a = tmp_path / "first/.agents/skills"
    skills_b = tmp_path / "second/.agents/skills"
    global_agents = tmp_path / "shared/.codex/AGENTS.md"
    write_source_skill(root_a, "alpha", "v1")
    write_source_skill(root_b, "beta", "v1")
    write_template(root_a)
    write_template(root_b)
    install_skills.install(root_a, skills_a, global_agents)
    before_agents = global_agents.read_bytes()

    (root_a / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    (root_a / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\n"
        "- **Route:** Updated route.\n",
        encoding="utf-8",
    )
    original_bootstrap = install_skills.install_global_bootstrap
    original_restore = install_skills.restore_file

    def fail_after_bootstrap(template: Path, target: Path) -> str:
        original_bootstrap(template, target)
        raise OSError("injected global commit failure")

    def fail_global_restore(path: Path, snapshot: Path | None) -> None:
        if path.resolve() == global_agents.resolve():
            raise OSError("injected global rollback failure")
        original_restore(path, snapshot)

    monkeypatch.setattr(
        install_skills,
        "install_global_bootstrap",
        fail_after_bootstrap,
    )
    monkeypatch.setattr(install_skills, "restore_file", fail_global_restore)

    with pytest.raises(RuntimeError, match="recovery snapshot preserved at"):
        install_skills.install(root_a, skills_a, global_agents)

    transactions = transaction_dirs(skills_a)
    assert len(transactions) == 1
    monkeypatch.setattr(
        install_skills,
        "install_global_bootstrap",
        original_bootstrap,
    )
    monkeypatch.setattr(install_skills, "restore_file", original_restore)

    global_agents.write_text("user edit after crash\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Live install targets changed"):
        install_skills.recover_transaction(
            transactions[0],
            skills_a,
            global_agents,
        )
    assert global_agents.read_text(encoding="utf-8") == "user edit after crash\n"
    global_agents.write_bytes(before_agents)

    claim_paths = [
        install_skills.operation_claim_path(parent)
        for parent in install_skills.operation_lock_parents(skills_a, global_agents)
    ]
    assert len(claim_paths) == 2
    mixed_claim = claim_paths[0]
    original_claim = mixed_claim.read_bytes()
    claim_payload = json.loads(original_claim)
    assert claim_payload["mutation_started"] is True
    with pytest.raises(RuntimeError, match="Unfinished skill-pack transaction"):
        install_skills.install(root_b, skills_b, global_agents)

    claim_payload["mutation_started"] = False
    install_skills.write_operation_claim(mixed_claim, claim_payload)
    result = install_skills.recover_transaction(
        transactions[0],
        skills_a,
        global_agents,
    )
    assert result["status"] == "restored"
    assert global_agents.read_bytes() == before_agents

    installed_b = install_skills.install(root_b, skills_b, global_agents)
    assert installed_b["new"] == ["beta"]


def test_orphan_operation_claim_blocks_install_and_is_preserved(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    missing_transaction = tmp_path / install_skills.ACTIVE_TRANSACTION_NAME
    state = install_skills.preparing_transaction_state(installed, None, [], False)
    claim_path = install_skills.operation_claim_path(tmp_path)
    install_skills.write_operation_claim(
        claim_path,
        {
            "format": 1,
            "transaction": str(missing_transaction),
            "plan_sha256": install_skills.transaction_plan_hash(state),
            "mutation_started": True,
        },
    )

    with pytest.raises(RuntimeError, match="Orphaned skill-pack operation claim"):
        install_skills.install(root, installed, None)

    assert claim_path.is_file()
    assert not installed.exists()


def test_install_preserves_preexisting_temporary_siblings(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")

    tree_collision = installed / ".alpha.installing"
    tree_collision.mkdir()
    (tree_collision / "sentinel.txt").write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="managed-skill temporary path"):
        install_skills.install(root, installed, None)
    assert (tree_collision / "sentinel.txt").read_text(encoding="utf-8") == "keep"
    (tree_collision / "sentinel.txt").unlink()
    tree_collision.rmdir()

    manifest_collision = installed / f".{install_skills.MANIFEST_NAME}.installing"
    manifest_collision.write_text("keep", encoding="utf-8")
    with pytest.raises(RuntimeError, match="manifest temporary path"):
        install_skills.install(root, installed, None)
    assert manifest_collision.read_text(encoding="utf-8") == "keep"


def test_unchanged_install_returns_without_a_transaction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, global_agents)
    before = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    def fail_if_transaction_starts(*args, **kwargs):
        raise AssertionError("unchanged install started a transaction")

    monkeypatch.setattr(install_skills, "claim_transaction", fail_if_transaction_starts)
    result = install_skills.install(root, installed, global_agents)

    assert result["unchanged"] == ["alpha"]
    assert tree_snapshot(installed) == before
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_global_bootstrap_replace_failure_restores_target_and_cleans_temp(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, global_agents)
    before = global_agents.read_bytes()
    (root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\n"
        "- **Route:** Changed route.\n",
        encoding="utf-8",
    )
    original_replace = Path.replace

    def fail_global_replace(path: Path, target: Path):
        if (
            path == install_skills.global_agents_temporary_path(global_agents)
            and target == global_agents
        ):
            raise OSError("injected atomic global replace failure")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_global_replace)

    with pytest.raises(OSError, match="atomic global replace failure"):
        install_skills.install(root, installed, global_agents)

    assert global_agents.read_bytes() == before
    assert not install_skills.global_agents_temporary_path(global_agents).exists()
    assert transaction_dirs(installed) == []


def test_committed_cleanup_failure_recovers_without_rolling_back(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_clear = install_skills.clear_operation_claims
    monkeypatch.setattr(
        install_skills,
        "clear_operation_claims",
        lambda parents, transaction: ["injected claim cleanup failure"],
    )

    with pytest.raises(RuntimeError, match="claim cleanup is incomplete"):
        install_skills.install(root, installed, None)

    transaction = transaction_dirs(installed)[0]
    state = json.loads(
        (transaction / "transaction-state.json").read_text(encoding="utf-8")
    )
    assert state["status"] == "committed"
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v2"

    pending_state = transaction / ".transaction-state.json.installing"
    pending_state.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(install_skills, "clear_operation_claims", original_clear)
    result = install_skills.recover_transaction(transaction, installed, None)

    assert result["status"] == "cleared-commit"
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v2"
    assert transaction_dirs(installed) == []


def test_truncated_active_state_temporary_uses_committed_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_clear = install_skills.clear_operation_claims
    monkeypatch.setattr(
        install_skills,
        "clear_operation_claims",
        lambda parents, transaction: ["injected claim cleanup failure"],
    )
    with pytest.raises(RuntimeError, match="claim cleanup is incomplete"):
        install_skills.install(root, installed, None)
    transaction = transaction_dirs(installed)[0]
    (transaction / ".transaction-state.json.installing").write_text(
        "{", encoding="utf-8"
    )

    monkeypatch.setattr(install_skills, "clear_operation_claims", original_clear)
    result = install_skills.recover_transaction(transaction, installed, None)

    assert result["status"] == "cleared-commit"
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v2"
    assert transaction_dirs(installed) == []


@pytest.mark.parametrize("pending_status", ["rolled-back", "recovery-incomplete"])
def test_prepared_state_reconciles_recovery_outcomes(
    tmp_path: Path,
    pending_status: str,
) -> None:
    transaction = tmp_path / install_skills.ACTIVE_TRANSACTION_NAME
    transaction.mkdir()
    current = install_skills.preparing_transaction_state(
        tmp_path / "skills", None, ["alpha"], False
    )
    current["status"] = "prepared"
    install_skills.write_transaction_state(transaction, current)
    pending = dict(current)
    pending["status"] = pending_status
    (transaction / ".transaction-state.json.installing").write_text(
        json.dumps(pending, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    install_skills.reconcile_transaction_state_temporary(transaction)

    reconciled = json.loads(
        (transaction / "transaction-state.json").read_text(encoding="utf-8")
    )
    assert reconciled["status"] == pending_status
    assert not (transaction / ".transaction-state.json.installing").exists()


def test_safe_orphan_preparing_state_is_cleared_before_install(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    preparing = tmp_path / install_skills.PREPARING_TRANSACTION_NAME
    preparing.mkdir()
    state = install_skills.preparing_transaction_state(installed, None, ["alpha"], False)
    install_skills.write_transaction_state(preparing, state)

    result = install_skills.install(root, installed, None)

    assert result["new"] == ["alpha"]
    assert not preparing.exists()


def test_safe_orphan_preparing_state_temporary_is_cleared_before_install(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    preparing = tmp_path / install_skills.PREPARING_TRANSACTION_NAME
    preparing.mkdir()
    state = install_skills.preparing_transaction_state(installed, None, ["alpha"], False)
    (preparing / ".transaction-state.json.installing").write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result = install_skills.install(root, installed, None)

    assert result["new"] == ["alpha"]
    assert not preparing.exists()


def test_empty_orphan_preparing_directory_is_cleared_before_install(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    preparing = tmp_path / install_skills.PREPARING_TRANSACTION_NAME
    preparing.mkdir()

    result = install_skills.install(root, installed, None)

    assert result["new"] == ["alpha"]
    assert not preparing.exists()


@pytest.mark.parametrize(
    "state_name",
    ["transaction-state.json", ".transaction-state.json.installing"],
)
def test_truncated_orphan_preparing_state_is_cleared_before_install(
    tmp_path: Path,
    state_name: str,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    preparing = tmp_path / install_skills.PREPARING_TRANSACTION_NAME
    preparing.mkdir()
    (preparing / state_name).write_text("{", encoding="utf-8")

    result = install_skills.install(root, installed, None)

    assert result["new"] == ["alpha"]
    assert not preparing.exists()


def test_post_crash_temporary_sibling_drift_is_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_manifest = install_skills.write_manifest
    original_restore = install_skills.restore_tree

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original_manifest(path, payload)
        raise OSError("injected apply failure")

    def fail_restore(source: Path, destination: Path) -> None:
        raise OSError("injected rollback failure")

    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)
    monkeypatch.setattr(install_skills, "restore_tree", fail_restore)
    with pytest.raises(RuntimeError, match="recovery snapshot preserved"):
        install_skills.install(root, installed, None)
    transaction = transaction_dirs(installed)[0]
    monkeypatch.setattr(install_skills, "write_manifest", original_manifest)
    monkeypatch.setattr(install_skills, "restore_tree", original_restore)

    sibling = installed / ".alpha.installing"
    sibling.mkdir()
    (sibling / "sentinel.txt").write_text("user", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Live install targets changed"):
        install_skills.recover_transaction(transaction, installed, None)

    assert (sibling / "sentinel.txt").read_text(encoding="utf-8") == "user"
    assert transaction.is_dir()

    (sibling / "sentinel.txt").unlink()
    sibling.rmdir()
    manifest_sibling = installed / f".{install_skills.MANIFEST_NAME}.installing"
    manifest_sibling.write_text("user", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Live install targets changed"):
        install_skills.recover_transaction(transaction, installed, None)

    assert manifest_sibling.read_text(encoding="utf-8") == "user"
    assert transaction.is_dir()


def test_post_crash_applied_displacement_drift_is_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_manifest = install_skills.write_manifest
    original_restore = install_skills.restore_tree

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original_manifest(path, payload)
        raise OSError("injected apply failure")

    def fail_restore(source: Path, destination: Path) -> None:
        raise OSError("injected rollback failure")

    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)
    monkeypatch.setattr(install_skills, "restore_tree", fail_restore)
    with pytest.raises(RuntimeError, match="recovery snapshot preserved"):
        install_skills.install(root, installed, None)
    transaction = transaction_dirs(installed)[0]
    displaced = transaction / "displaced-skills/alpha"
    (displaced / "sentinel.txt").write_text("user", encoding="utf-8")
    monkeypatch.setattr(install_skills, "write_manifest", original_manifest)
    monkeypatch.setattr(install_skills, "restore_tree", original_restore)

    with pytest.raises(RuntimeError, match="applied displaced tree is outside the plan"):
        install_skills.recover_transaction(transaction, installed, None)

    assert (displaced / "sentinel.txt").read_text(encoding="utf-8") == "user"
    assert transaction.is_dir()


def test_edit_between_identity_check_and_rollback_is_quarantined_and_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_manifest = install_skills.write_manifest
    original_rollback = install_skills.rollback_install

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original_manifest(path, payload)
        raise OSError("injected apply failure")

    def edit_then_rollback(**kwargs):
        (installed / "alpha/SKILL.md").write_text("user edit", encoding="utf-8")
        return original_rollback(**kwargs)

    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)
    monkeypatch.setattr(install_skills, "rollback_install", edit_then_rollback)

    with pytest.raises(RuntimeError, match="rollback is incomplete"):
        install_skills.install(root, installed, None)

    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "user edit"
    assert len(transaction_dirs(installed)) == 1


@pytest.mark.parametrize("target_kind", ["skills", "global"])
def test_install_rejects_top_level_symlink_targets(
    tmp_path: Path, target_kind: str
) -> None:
    root = tmp_path / "repo"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    real_skills = tmp_path / "real-skills"
    real_skills.mkdir()
    real_global = tmp_path / "real-AGENTS.md"
    real_global.write_text("personal\n", encoding="utf-8")
    skills = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    try:
        if target_kind == "skills":
            skills.symlink_to(real_skills, target_is_directory=True)
            global_agents = None
        else:
            skills = real_skills
            global_agents.symlink_to(real_global)
    except OSError as error:
        pytest.skip(f"symlink creation unavailable: {error}")

    with pytest.raises(ValueError, match="link/reparse point"):
        install_skills.install(root, skills, global_agents)

    assert real_global.read_text(encoding="utf-8") == "personal\n"


def test_install_locks_a_shared_global_target_across_different_skill_roots(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    first_skills = tmp_path / "first/.agents/skills"
    second_skills = tmp_path / "second/.agents/skills"
    global_agents = tmp_path / "shared/.codex/AGENTS.md"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    global_agents.parent.mkdir(parents=True)
    global_agents.write_text("Personal rule.\n", encoding="utf-8")
    before_agents = global_agents.read_bytes()
    script = (
        "import sys\n"
        "from pathlib import Path\n"
        "from scripts.install_skills import install\n"
        "install(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))\n"
    )

    lock_parents = install_skills.operation_lock_parents(first_skills, global_agents)
    with install_skills.install_locks(lock_parents):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                str(root),
                str(second_skills),
                str(global_agents),
            ],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    assert result.returncode != 0
    assert "another install or recovery process owns" in result.stderr.lower()
    assert not second_skills.exists()
    assert global_agents.read_bytes() == before_agents


def test_install_updates_managed_skills_and_preserves_unrelated(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    global_agents = tmp_path / ".codex/AGENTS.md"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    (installed / "finance-brain").mkdir(parents=True)
    (installed / "finance-brain/SKILL.md").write_text("personal", encoding="utf-8")
    global_agents.parent.mkdir(parents=True)
    global_agents.write_text("# Global Codex Instructions\n\nPersonal rule.\n", encoding="utf-8")

    first = install_skills.install(root, installed, global_agents)

    assert first["skills"] == ["alpha"]
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v1"
    assert (installed / "finance-brain/SKILL.md").read_text(encoding="utf-8") == "personal"
    assert install_skills.BOOTSTRAP_HEADING in global_agents.read_text(encoding="utf-8")

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    write_source_skill(root, "beta", "new")
    second = install_skills.install(root, installed, global_agents)

    assert second["skills"] == ["alpha", "beta"]
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v2"
    assert (installed / "finance-brain").is_dir()
    manifest = json.loads(
        (installed / install_skills.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    assert manifest["skills"] == ["alpha", "beta"]


def test_install_ignores_same_named_experimental_skill(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    write_source_skill(root, "alpha", "active")
    experimental = root / "skills/experimental/alpha"
    experimental.mkdir(parents=True)
    (experimental / "SKILL.md").write_text("candidate", encoding="utf-8")
    write_template(root)

    result = install_skills.install(root, installed, None)

    assert result["skills"] == ["alpha"]
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "active"
    manifest = json.loads(
        (installed / install_skills.MANIFEST_NAME).read_text(encoding="utf-8")
    )
    assert manifest["source"] == "skills/custom"
    assert manifest["skills"] == ["alpha"]


def test_install_excludes_and_ignores_python_cache_artifacts(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    source_scripts = root / "skills/custom/alpha/scripts"
    (source_scripts / "__pycache__").mkdir(parents=True)
    (source_scripts / "__pycache__/helper.cpython-312.pyc").write_bytes(b"cached")
    (source_scripts / "helper.pyc").write_bytes(b"loose-cache")

    result = install_skills.install(root, installed, None)

    assert result["new"] == ["alpha"]
    assert not (installed / "alpha/scripts/__pycache__").exists()
    assert not (installed / "alpha/scripts/helper.pyc").exists()

    runtime_cache = installed / "alpha/scripts/__pycache__"
    runtime_cache.mkdir(parents=True)
    (runtime_cache / "runtime.cpython-312.pyc").write_bytes(b"runtime-cache")

    preview = install_skills.install(root, installed, None, dry_run=True)

    assert preview["unchanged"] == ["alpha"]
    assert preview["updated"] == []


def test_install_migrates_a_legacy_cache_inclusive_manifest(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    source_cache = root / "skills/custom/alpha/scripts/__pycache__"
    source_cache.mkdir(parents=True)
    (source_cache / "helper.cpython-312.pyc").write_bytes(b"legacy-cache")
    installed.mkdir(parents=True)
    shutil.copytree(root / "skills/custom/alpha", installed / "alpha")
    install_skills.write_manifest(
        installed / install_skills.MANIFEST_NAME,
        {
            "format": skill_pack_contract.MANIFEST_FORMAT,
            "source": skill_pack_contract.MANIFEST_SOURCE,
            "skills": ["alpha"],
            "hashes": {"alpha": skill_pack_contract.tree_hash(installed / "alpha")},
        },
    )

    preview = install_skills.install(root, installed, None, dry_run=True)
    result = install_skills.install(root, installed, None)

    assert preview["updated"] == ["alpha"]
    assert result["updated"] == ["alpha"]
    assert not (installed / "alpha/scripts/__pycache__").exists()
    assert install_skills.install(root, installed, None, dry_run=True)["unchanged"] == [
        "alpha"
    ]


def test_install_refuses_a_conflicting_unmanaged_same_name_skill(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    global_agents = tmp_path / ".codex/AGENTS.md"
    write_source_skill(root, "alpha", "pack version")
    write_template(root)
    (installed / "alpha").mkdir(parents=True)
    (installed / "alpha/SKILL.md").write_text("personal", encoding="utf-8")
    global_agents.parent.mkdir(parents=True)
    global_agents.write_text("Personal rule.\n", encoding="utf-8")
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    with pytest.raises(ValueError, match="unmanaged skill path"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert not (installed / install_skills.MANIFEST_NAME).exists()
    assert transaction_dirs(installed) == []


def test_install_refuses_to_claim_an_identical_unmanaged_same_name_skill(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    write_source_skill(root, "alpha", "same bytes")
    write_template(root)
    (installed / "alpha").mkdir(parents=True)
    (installed / "alpha/SKILL.md").write_text("same bytes", encoding="utf-8")
    before_skills = tree_snapshot(installed)

    with pytest.raises(ValueError, match="unmanaged skill path"):
        install_skills.install(root, installed, None)

    assert tree_snapshot(installed) == before_skills
    assert not (installed / install_skills.MANIFEST_NAME).exists()
    assert transaction_dirs(installed) == []


def test_install_rejects_manifest_path_traversal_without_touching_siblings(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    victim = installed.parent / "victim"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    installed.mkdir(parents=True)
    victim.mkdir()
    (victim / "sentinel.txt").write_text("keep", encoding="utf-8")
    (installed / install_skills.MANIFEST_NAME).write_text(
        json.dumps(
            {
                "format": 1,
                "source": "skills/custom",
                "skills": ["../victim"],
                "hashes": {"../victim": skill_pack_contract.tree_hash(victim)},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unsafe skill name"):
        install_skills.install(root, installed, None)

    assert (victim / "sentinel.txt").read_text(encoding="utf-8") == "keep"
    assert transaction_dirs(installed) == []


def test_install_rejects_global_target_inside_the_skills_tree(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    manifest_target = installed / install_skills.MANIFEST_NAME

    with pytest.raises(ValueError, match="target topology"):
        install_skills.install(root, installed, manifest_target)

    assert not installed.exists()


def test_install_rejects_skills_tree_inside_the_global_target_path(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    global_agents = tmp_path / "intended-AGENTS.md"
    installed = global_agents / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)

    with pytest.raises(ValueError, match="target topology"):
        install_skills.install(root, installed, global_agents)

    assert not global_agents.exists()


@pytest.mark.parametrize(
    "reserved_name",
    [
        install_skills.INSTALL_LOCK_NAME,
        install_skills.OPERATION_CLAIM_NAME,
        install_skills.ACTIVE_TRANSACTION_NAME,
    ],
)
def test_install_rejects_global_target_on_reserved_coordination_path(
    tmp_path: Path,
    reserved_name: str,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "shared" / reserved_name
    write_source_skill(root, "alpha", "v1")
    write_template(root)

    with pytest.raises(ValueError, match="target topology"):
        install_skills.install(root, installed, global_agents)

    assert not global_agents.exists()
    assert not installed.exists()


def test_recovery_rejects_a_forged_prefix_transaction_directory(
    tmp_path: Path,
) -> None:
    skills_dir = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    transaction = tmp_path / ".programming-agent-skills-transaction-forged"
    transaction.mkdir()
    install_skills.write_transaction_state(
        transaction,
        install_skills.preparing_transaction_state(
            skills_dir,
            global_agents,
            [],
            False,
        ),
    )

    with pytest.raises(ValueError, match="Not a skill-pack transaction snapshot"):
        install_skills.recover_transaction(
            transaction,
            skills_dir,
            global_agents,
        )

    assert transaction.is_dir()


def test_install_refuses_to_overwrite_a_modified_managed_skill(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, global_agents)

    (installed / "alpha/SKILL.md").write_text("personal change", encoding="utf-8")
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    with pytest.raises(ValueError, match="overwrite modified managed skill"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_install_refuses_a_symlinked_managed_file_even_with_identical_bytes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    install_skills.install(root, installed, None)
    external = tmp_path / "external-skill.md"
    external.write_text("v1", encoding="utf-8")
    installed_file = installed / "alpha/SKILL.md"
    installed_file.unlink()
    try:
        installed_file.symlink_to(external)
    except OSError as error:
        pytest.skip(f"symlink creation unavailable: {error}")

    with pytest.raises(ValueError, match="Unsafe special tree entry"):
        install_skills.install(root, installed, None)

    assert installed_file.is_symlink()
    assert external.read_text(encoding="utf-8") == "v1"


def test_tree_hash_rejects_windows_reparse_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tree = tmp_path / "tree"
    tree.mkdir()
    target = tree / "SKILL.md"
    target.write_text("same bytes", encoding="utf-8")
    original_lstat = skill_pack_contract.os.lstat
    reparse_flag = 0x400
    monkeypatch.setattr(
        skill_pack_contract.stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        reparse_flag,
        raising=False,
    )

    class ReparseMetadata:
        def __init__(self, metadata):
            self.st_mode = metadata.st_mode
            self.st_file_attributes = (
                getattr(metadata, "st_file_attributes", 0) | reparse_flag
            )

    def fake_lstat(path):
        metadata = original_lstat(path)
        if Path(path) == target:
            return ReparseMetadata(metadata)
        return metadata

    monkeypatch.setattr(skill_pack_contract.os, "lstat", fake_lstat)

    with pytest.raises(ValueError, match="link/reparse point"):
        skill_pack_contract.tree_hash(tree)


def test_install_rejects_windows_reparse_target_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    skills = tmp_path / "skills"
    skills.mkdir()
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    original_lstat = skill_pack_contract.os.lstat
    reparse_flag = 0x400
    monkeypatch.setattr(
        skill_pack_contract.stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        reparse_flag,
        raising=False,
    )

    class ReparseMetadata:
        def __init__(self, metadata):
            self.st_mode = metadata.st_mode
            self.st_file_attributes = (
                getattr(metadata, "st_file_attributes", 0) | reparse_flag
            )

    def fake_lstat(path):
        metadata = original_lstat(path)
        if Path(path) == skills:
            return ReparseMetadata(metadata)
        return metadata

    monkeypatch.setattr(skill_pack_contract.os, "lstat", fake_lstat)

    with pytest.raises(ValueError, match="managed skills target link/reparse point"):
        install_skills.install(root, skills, None)


@pytest.mark.parametrize("entry_kind", ["lock", "claim"])
def test_install_rejects_windows_reparse_coordination_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    entry_kind: str,
) -> None:
    root = tmp_path / "repo"
    skills = tmp_path / "skills"
    write_source_skill(root, "alpha", "v1")
    write_template(root)
    entry = tmp_path / (
        install_skills.INSTALL_LOCK_NAME
        if entry_kind == "lock"
        else install_skills.OPERATION_CLAIM_NAME
    )
    entry.write_text("sentinel", encoding="utf-8")
    original_lstat = skill_pack_contract.os.lstat
    reparse_flag = 0x400
    monkeypatch.setattr(
        skill_pack_contract.stat,
        "FILE_ATTRIBUTE_REPARSE_POINT",
        reparse_flag,
        raising=False,
    )

    class ReparseMetadata:
        def __init__(self, metadata):
            self.st_mode = metadata.st_mode
            self.st_file_attributes = (
                getattr(metadata, "st_file_attributes", 0) | reparse_flag
            )

    def fake_lstat(path):
        metadata = original_lstat(path)
        if Path(path) == entry:
            return ReparseMetadata(metadata)
        return metadata

    monkeypatch.setattr(skill_pack_contract.os, "lstat", fake_lstat)

    with pytest.raises(ValueError, match="link/reparse point"):
        install_skills.install(root, skills, None)
    assert entry.read_text(encoding="utf-8") == "sentinel"


def test_tree_hash_preserves_format_one_file_order(tmp_path: Path) -> None:
    tree = tmp_path / "tree"
    (tree / "agents").mkdir(parents=True)
    (tree / "agents/openai.yaml").write_text("agent", encoding="utf-8")
    (tree / "SKILL.md").write_text("skill", encoding="utf-8")
    legacy = install_skills.hashlib.sha256()
    for path in sorted(item for item in tree.rglob("*") if item.is_file()):
        legacy.update(path.relative_to(tree).as_posix().encode("utf-8"))
        legacy.update(b"\0")
        legacy.update(path.read_bytes())
        legacy.update(b"\0")

    assert skill_pack_contract.tree_hash(tree) == legacy.hexdigest()


def test_install_refuses_to_retire_a_modified_managed_skill(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_source_skill(root, "retired", "pack version")
    write_template(root)
    install_skills.install(root, installed, None)

    (root / "skills/custom/retired/SKILL.md").unlink()
    (root / "skills/custom/retired").rmdir()
    (installed / "retired/SKILL.md").write_text("personal change", encoding="utf-8")

    with pytest.raises(ValueError, match="modified managed skill"):
        install_skills.install(root, installed, None)

    assert (installed / "retired/SKILL.md").read_text(encoding="utf-8") == "personal change"
    assert transaction_dirs(installed) == []


def test_install_updates_only_existing_bootstrap_section(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    target = tmp_path / "AGENTS.md"
    write_template(root)
    target.write_text(
        "# Global Codex Instructions\n\nPersonal before.\n\n"
        "## Skill Pack Bootstrap\n\nOld route.\n\n"
        "## Personal After\n\nKeep me.\n",
        encoding="utf-8",
    )

    status = install_skills.install_global_bootstrap(
        root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
        target,
    )

    text = target.read_text(encoding="utf-8")
    assert status == "updated"
    assert "Old route" not in text
    assert install_skills.bootstrap_section(
        root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md"
    ) in text
    assert "Personal before" in text
    assert "## Personal After\n\nKeep me." in text


def test_bootstrap_section_uses_one_real_level_two_heading(tmp_path: Path) -> None:
    template = tmp_path / "template.md"
    template.write_text(
        "# Global Codex Instructions\n\n"
        "Mention `## Skill Pack Bootstrap` without opening it.\n\n"
        "## Skill Pack Bootstrap\n\nManaged.\n\n"
        "## Personal Reference\n\nUnmanaged.\n",
        encoding="utf-8",
    )

    assert install_skills.bootstrap_section(template) == (
        "## Skill Pack Bootstrap\n\nManaged.\n"
    )

    template.write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\nFirst.\n\n"
        "## Skill Pack Bootstrap\n\nSecond.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="exactly one"):
        install_skills.bootstrap_section(template)


def test_install_ignores_bootstrap_heading_inside_fenced_example(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    target = tmp_path / "AGENTS.md"
    write_template(root)
    target.write_text(
        "# Global Codex Instructions\n\n"
        "```markdown\n## Skill Pack Bootstrap\nExample only.\n```\n\n"
        "## Skill Pack Bootstrap\n\nOld route.\n\n"
        "## Personal After\n\nKeep me.\n",
        encoding="utf-8",
    )

    status = install_skills.install_global_bootstrap(
        root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
        target,
    )

    text = target.read_text(encoding="utf-8")
    assert status == "updated"
    assert "```markdown\n## Skill Pack Bootstrap\nExample only.\n```" in text
    assert "Old route" not in text
    assert "## Personal After\n\nKeep me." in text


def test_install_migrates_legacy_skill_pack_guide(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    target = tmp_path / "AGENTS.md"
    write_template(root)
    target.write_text(
        "# Global Codex Instructions\n\nPersonal before.\n\n"
        "## Skill Pack Guide\n\nOld primer.\n\n"
        "## Routing Handles\n\nOld routes.\n\n"
        "## Suggestion Index\n\nOld index.\n\n"
        "## Boundary\n\nOld boundary.\n\n"
        "## Personal After\n\nKeep me.\n",
        encoding="utf-8",
    )

    status = install_skills.install_global_bootstrap(
        root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
        target,
    )

    text = target.read_text(encoding="utf-8")
    assert status == "migrated"
    assert "## Skill Pack Guide" not in text
    assert "Old routes" not in text
    assert install_skills.BOOTSTRAP_HEADING in text
    assert "Personal before" in text
    assert "## Personal After\n\nKeep me." in text


def test_install_removes_only_previously_managed_retired_skills(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, None)
    (installed / "personal").mkdir()

    for path in (root / "skills/custom/alpha").rglob("*"):
        if path.is_file():
            path.unlink()
    (root / "skills/custom/alpha").rmdir()
    write_source_skill(root, "beta", "v1")

    result = install_skills.install(root, installed, None)

    assert result["retired"] == ["alpha"]
    assert not (installed / "alpha").exists()
    assert (installed / "beta").is_dir()
    assert (installed / "personal").is_dir()


def test_retirement_uses_atomic_displacement_not_recursive_live_deletion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_template(root)
    write_source_skill(root, "retired", "v1")
    install_skills.install(root, installed, None)
    (root / "skills/custom/retired/SKILL.md").unlink()
    (root / "skills/custom/retired").rmdir()
    original_rmtree = install_skills.shutil.rmtree

    def reject_live_retirement(path: Path, *args, **kwargs) -> None:
        if Path(path) == installed / "retired":
            raise AssertionError("live retirement must be an atomic rename")
        original_rmtree(path, *args, **kwargs)

    monkeypatch.setattr(install_skills.shutil, "rmtree", reject_live_retirement)

    result = install_skills.install(root, installed, None)

    assert result["retired"] == ["retired"]
    assert not (installed / "retired").exists()


def test_dry_run_reports_new_updated_unchanged_and_retired(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    write_source_skill(root, "beta", "v1")
    write_source_skill(root, "old", "v1")
    install_skills.install(root, installed, global_agents)

    (root / "skills/custom/beta/SKILL.md").write_text("v2", encoding="utf-8")
    (root / "skills/custom/old/SKILL.md").unlink()
    (root / "skills/custom/old").rmdir()
    write_source_skill(root, "gamma", "v1")

    result = install_skills.install(
        root,
        installed,
        global_agents,
        dry_run=True,
    )

    assert result["new"] == ["gamma"]
    assert result["updated"] == ["beta"]
    assert result["unchanged"] == ["alpha"]
    assert result["retired"] == ["old"]
    assert result["global_bootstrap"] == "present"


def test_dry_run_does_not_create_the_install_parent(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / ".agents/skills"
    write_template(root)
    write_source_skill(root, "alpha", "v1")

    result = install_skills.install(root, installed, None, dry_run=True)

    assert result["new"] == ["alpha"]
    assert not installed.parent.exists()


def test_install_rolls_back_every_skill_when_the_second_swap_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    write_source_skill(root, "beta", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    (root / "skills/custom/beta/SKILL.md").write_text("v2", encoding="utf-8")
    original = install_skills.replace_tree
    calls = 0

    def fail_second_swap(source: Path, destination: Path, displaced: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected second swap failure")
        original(source, destination, displaced)

    monkeypatch.setattr(install_skills, "replace_tree", fail_second_swap)

    with pytest.raises(OSError, match="injected second swap failure"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_recovery_handles_interruption_between_update_renames(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_rename = Path.rename
    interrupted = False

    def interrupt_after_displacement(path: Path, target: Path):
        nonlocal interrupted
        result = original_rename(path, target)
        if (
            not interrupted
            and path == installed / "alpha"
            and target.parent.name == "displaced-skills"
        ):
            interrupted = True
            raise KeyboardInterrupt("injected process interruption")
        return result

    monkeypatch.setattr(Path, "rename", interrupt_after_displacement)
    with pytest.raises(KeyboardInterrupt, match="injected process interruption"):
        install_skills.install(root, installed, None)
    transaction = transaction_dirs(installed)[0]
    assert not (installed / "alpha").exists()
    assert (installed / ".alpha.installing/SKILL.md").read_text(
        encoding="utf-8"
    ) == "v2"
    assert (transaction / "displaced-skills/alpha/SKILL.md").read_text(
        encoding="utf-8"
    ) == "v1"

    monkeypatch.setattr(Path, "rename", original_rename)
    result = install_skills.recover_transaction(transaction, installed, None)

    assert result["status"] == "restored"
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v1"
    assert transaction_dirs(installed) == []


def test_install_restores_a_retired_skill_when_retirement_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    write_source_skill(root, "retired", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    (root / "skills/custom/retired/SKILL.md").unlink()
    (root / "skills/custom/retired").rmdir()
    original = install_skills.retire_tree
    failed = False

    def fail_after_retirement(path: Path, displaced: Path) -> None:
        nonlocal failed
        original(path, displaced)
        if not failed:
            failed = True
            raise OSError("injected retirement failure")

    monkeypatch.setattr(install_skills, "retire_tree", fail_after_retirement)

    with pytest.raises(OSError, match="injected retirement failure"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_install_restores_skills_and_retirements_when_manifest_write_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    write_source_skill(root, "retired", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    (root / "skills/custom/retired/SKILL.md").unlink()
    (root / "skills/custom/retired").rmdir()
    original = install_skills.write_manifest

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original(path, payload)
        raise OSError("injected manifest failure")

    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)

    with pytest.raises(OSError, match="injected manifest failure"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_rollback_records_terminal_state_before_recursive_quarantine_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, None)
    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_manifest = install_skills.write_manifest
    original_clear = install_skills.clear_claims_then_transaction
    observed_terminal_quarantine = False

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original_manifest(path, payload)
        raise OSError("injected commit failure")

    def inspect_before_cleanup(
        parents: list[Path], transaction: Path, outcome: str
    ) -> None:
        nonlocal observed_terminal_quarantine
        state = json.loads(
            (transaction / "transaction-state.json").read_text(encoding="utf-8")
        )
        if state["status"] == "rolled-back":
            assert (transaction / "rollback-live/alpha-live").is_dir()
            observed_terminal_quarantine = True
        original_clear(parents, transaction, outcome)

    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)
    monkeypatch.setattr(
        install_skills, "clear_claims_then_transaction", inspect_before_cleanup
    )

    with pytest.raises(OSError, match="injected commit failure"):
        install_skills.install(root, installed, None)

    assert observed_terminal_quarantine
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v1"
    assert transaction_dirs(installed) == []


def test_install_restores_the_pack_when_global_bootstrap_write_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    (root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md").write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\n"
        "- **Route:** Updated route.\n",
        encoding="utf-8",
    )
    original = install_skills.install_global_bootstrap

    def fail_after_bootstrap(template: Path, target: Path) -> str:
        original(template, target)
        raise OSError("injected global bootstrap failure")

    monkeypatch.setattr(
        install_skills,
        "install_global_bootstrap",
        fail_after_bootstrap,
    )

    with pytest.raises(OSError, match="injected global bootstrap failure"):
        install_skills.install(root, installed, global_agents)

    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_install_rolls_back_when_global_step_corrupts_the_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_bootstrap = install_skills.install_global_bootstrap

    def corrupt_manifest(template: Path, target: Path) -> str:
        status = original_bootstrap(template, target)
        (installed / install_skills.MANIFEST_NAME).write_text("{}", encoding="utf-8")
        return status

    monkeypatch.setattr(
        install_skills,
        "install_global_bootstrap",
        corrupt_manifest,
    )

    with pytest.raises(RuntimeError, match="rollback is incomplete"):
        install_skills.install(root, installed, global_agents)

    transactions = transaction_dirs(installed)
    assert len(transactions) == 1
    assert (installed / install_skills.MANIFEST_NAME).read_text(encoding="utf-8") == "{}"
    (installed / install_skills.MANIFEST_NAME).write_bytes(
        (transactions[0] / "previous-manifest.json").read_bytes()
    )
    monkeypatch.setattr(
        install_skills,
        "install_global_bootstrap",
        original_bootstrap,
    )
    result = install_skills.recover_transaction(
        transactions[0], installed, global_agents
    )

    assert result["status"] == "restored"
    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_preparing_interruption_leaves_a_safe_recovery_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_copytree = install_skills.shutil.copytree

    def interrupt_staging(source: Path, destination: Path, *args, **kwargs):
        raise KeyboardInterrupt("injected preparing interruption")

    monkeypatch.setattr(install_skills.shutil, "copytree", interrupt_staging)
    with pytest.raises(KeyboardInterrupt, match="preparing interruption"):
        install_skills.install(root, installed, global_agents)

    transactions = transaction_dirs(installed)
    assert len(transactions) == 1
    state = json.loads(
        (transactions[0] / "transaction-state.json").read_text(encoding="utf-8")
    )
    assert state["status"] == "preparing"

    monkeypatch.setattr(install_skills.shutil, "copytree", original_copytree)
    result = install_skills.recover_transaction(
        transactions[0],
        installed,
        global_agents,
    )

    assert result["status"] == "cleared-preparation"
    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_preparation_cleanup_failure_preserves_safe_recovery_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    transaction = installed.parent / install_skills.ACTIVE_TRANSACTION_NAME
    original_copytree = install_skills.shutil.copytree
    original_rmtree = install_skills.shutil.rmtree

    def fail_preparation(source: Path, destination: Path, *args, **kwargs):
        raise OSError("injected preparation failure")

    def fail_transaction_cleanup(path: Path, *args, **kwargs):
        if Path(path).resolve() == transaction.resolve():
            raise OSError("injected transaction cleanup failure")
        return original_rmtree(path, *args, **kwargs)

    monkeypatch.setattr(install_skills.shutil, "copytree", fail_preparation)
    monkeypatch.setattr(install_skills.shutil, "rmtree", fail_transaction_cleanup)

    with pytest.raises(RuntimeError, match="failed before mutation"):
        install_skills.install(root, installed, global_agents)

    state = json.loads(
        (transaction / "transaction-state.json").read_text(encoding="utf-8")
    )
    assert state["status"] == "preparing"
    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents

    monkeypatch.setattr(install_skills.shutil, "copytree", original_copytree)
    monkeypatch.setattr(install_skills.shutil, "rmtree", original_rmtree)
    result = install_skills.recover_transaction(
        transaction,
        installed,
        global_agents,
    )

    assert result["status"] == "cleared-preparation"
    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []


def test_install_preserves_recovery_snapshot_when_rollback_cannot_complete(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "skills"
    global_agents = tmp_path / "AGENTS.md"
    write_template(root)
    write_source_skill(root, "alpha", "v1")
    install_skills.install(root, installed, global_agents)
    before_skills = tree_snapshot(installed)
    before_agents = global_agents.read_bytes()

    (root / "skills/custom/alpha/SKILL.md").write_text("v2", encoding="utf-8")
    original_restore_tree = install_skills.restore_tree
    original_manifest = install_skills.write_manifest
    def fail_rollback_restore(source: Path, destination: Path) -> None:
        raise OSError("injected rollback restore failure")

    def fail_after_manifest(path: Path, payload: dict[str, object]) -> None:
        original_manifest(path, payload)
        raise OSError("injected commit failure")

    monkeypatch.setattr(install_skills, "restore_tree", fail_rollback_restore)
    monkeypatch.setattr(install_skills, "write_manifest", fail_after_manifest)

    with pytest.raises(RuntimeError, match="recovery snapshot preserved at"):
        install_skills.install(root, installed, global_agents)

    transactions = transaction_dirs(installed)
    assert len(transactions) == 1
    assert (transactions[0] / "transaction-state.json").is_file()
    state = json.loads(
        (transactions[0] / "transaction-state.json").read_text(encoding="utf-8")
    )
    assert state["status"] == "rollback-incomplete"
    assert state["rollback_errors"]
    assert (transactions[0] / "previous-skills/alpha/SKILL.md").read_text(
        encoding="utf-8"
    ) == "v1"
    assert (transactions[0] / "displaced-skills/alpha/SKILL.md").read_text(
        encoding="utf-8"
    ) == "v1"

    (installed / install_skills.MANIFEST_NAME).write_text("{", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unfinished skill-pack transaction"):
        install_skills.install(root, installed, global_agents)

    monkeypatch.setattr(install_skills, "restore_tree", original_restore_tree)
    monkeypatch.setattr(install_skills, "write_manifest", original_manifest)

    state_path = transactions[0] / "transaction-state.json"
    original_state = state_path.read_bytes()
    victim = tmp_path / "victim.md"
    victim.write_text("keep", encoding="utf-8")

    downgraded = json.loads(original_state)
    downgraded["status"] = "preparing"
    install_skills.write_transaction_state(transactions[0], downgraded)
    with pytest.raises(RuntimeError, match="mutation phase"):
        install_skills.recover_transaction(
            transactions[0],
            installed,
            global_agents,
        )
    assert transactions[0].is_dir()
    state_path.write_bytes(original_state)

    redirected = json.loads(original_state)
    redirected["global_agents"] = str(victim)
    install_skills.write_transaction_state(transactions[0], redirected)
    with pytest.raises(ValueError, match="requested recovery targets"):
        install_skills.recover_transaction(
            transactions[0],
            installed,
            global_agents,
        )
    assert victim.read_text(encoding="utf-8") == "keep"

    state_path.write_bytes(original_state)
    omitted = json.loads(original_state)
    omitted["previous_hashes"] = {}
    install_skills.write_transaction_state(transactions[0], omitted)
    with pytest.raises(RuntimeError, match="transaction plan"):
        install_skills.recover_transaction(
            transactions[0],
            installed,
            global_agents,
        )
    state_path.write_bytes(original_state)

    backup_skill = transactions[0] / "previous-skills/alpha/SKILL.md"
    backup_skill.write_text("corrupted snapshot", encoding="utf-8")
    with pytest.raises(RuntimeError, match="snapshot hash mismatch"):
        install_skills.recover_transaction(
            transactions[0],
            installed,
            global_agents,
        )
    assert transactions[0].is_dir()
    backup_skill.write_text("v1", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Live install targets changed"):
        install_skills.recover_transaction(
            transactions[0],
            installed,
            global_agents,
        )
    assert transactions[0].is_dir()
    assert (installed / install_skills.MANIFEST_NAME).read_text(encoding="utf-8") == "{"

    (installed / "alpha").mkdir(exist_ok=True)
    (installed / "alpha/SKILL.md").write_text("v1", encoding="utf-8")
    (installed / install_skills.MANIFEST_NAME).write_bytes(
        (transactions[0] / "previous-manifest.json").read_bytes()
    )

    result = install_skills.recover_transaction(
        transactions[0],
        installed,
        global_agents,
    )

    assert result["status"] == "restored"
    assert tree_snapshot(installed) == before_skills
    assert global_agents.read_bytes() == before_agents
    assert transaction_dirs(installed) == []

    install_skills.install(root, installed, global_agents)
    assert (installed / "alpha/SKILL.md").read_text(encoding="utf-8") == "v2"


def test_readme_documents_the_executable_recovery_path() -> None:
    readme = (
        Path(__file__).resolve().parents[1] / "README.md"
    ).read_text(encoding="utf-8")

    assert "python -m scripts.install_skills --recover-transaction <snapshot-path>" in readme
