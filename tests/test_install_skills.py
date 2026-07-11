from __future__ import annotations

import json
from pathlib import Path

from scripts import install_skills


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
    assert "Suggest `$skill-router`" in text
    assert "Personal before" in text
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
