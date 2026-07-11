from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import validate_skills


def write_skill(root: Path, name: str, body: str = "") -> Path:
    skill_dir = root / "skills/custom" / name
    (skill_dir / "agents").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Example skill.\n---\n\n{body}\n",
        encoding="utf-8",
    )
    (skill_dir / "agents/openai.yaml").write_text(
        "policy:\n  allow_implicit_invocation: true\n",
        encoding="utf-8",
    )
    return skill_dir


def test_skill_validation_covers_markdown_and_cross_skill_references(tmp_path: Path) -> None:
    example = write_skill(tmp_path, "example", "Read [guide](GUIDE.md).")
    (example / "GUIDE.md").write_text("# Guide\n", encoding="utf-8")
    review = write_skill(tmp_path, "review")
    (review / "BASE.md").write_text("# Baseline\n", encoding="utf-8")
    (example / "SKILL.md").write_text(
        "---\nname: example\ndescription: Example skill.\n---\n\n"
        "Read [guide](GUIDE.md) and [baseline](../review/BASE.md).\n",
        encoding="utf-8",
    )

    names, failures = validate_skills.validate_skill_folders(tmp_path)

    assert names == ["example", "review"]
    assert failures == []


def test_skill_validation_rejects_missing_reference_and_policy(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, "example", "Read [missing](MISSING.md).")
    (skill / "agents/openai.yaml").unlink()

    _, failures = validate_skills.validate_skill_folders(tmp_path)

    assert any("missing invocation policy" in failure for failure in failures)
    assert any("resource reference is missing" in failure for failure in failures)


def test_skill_validation_rejects_missing_nested_markdown_reference(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, "example")
    (skill / "GUIDE.md").write_text(
        "Read [missing](references/MISSING.md).\n",
        encoding="utf-8",
    )

    _, failures = validate_skills.validate_skill_folders(tmp_path)

    assert failures == [
        "Skill resource reference is missing: "
        f"{(skill / 'GUIDE.md').as_posix()} -> references/MISSING.md"
    ]


def test_skill_handle_validation_rejects_unknown_custom_skill(tmp_path: Path) -> None:
    write_skill(tmp_path, "example", "Route to `$missing-skill`.")

    failures = validate_skills.validate_skill_handle_references(tmp_path, ["example"])

    assert failures == [
        "Active surface references missing custom skill: "
        "skills/custom/example/SKILL.md -> $missing-skill"
    ]


def test_skill_handle_validation_rejects_unknown_yaml_handle(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, "example")
    (skill / "agents/openai.yaml").write_text(
        "policy:\n"
        "  allow_implicit_invocation: true\n"
        "interface:\n"
        "  default_prompt: Use $missing-skill.\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_skill_handle_references(tmp_path, ["example"])

    assert failures == [
        "Active surface references missing custom skill: "
        "skills/custom/example/agents/openai.yaml -> $missing-skill"
    ]


def test_setup_schema_fingerprint_detects_contract_drift(tmp_path: Path) -> None:
    setup = tmp_path / validate_skills.SETUP_SKILL_ROOT
    (setup / "scripts").mkdir(parents=True)
    (setup / "domain.md").write_text("# Domain\n", encoding="utf-8")
    contract_files = ["domain.md"]
    fingerprint = validate_skills.setup_contract_hash(tmp_path, contract_files)
    marker = f"<!-- programming-agent-skills setup-schema: 1:{fingerprint[:12]} -->"

    (tmp_path / "AGENTS.md").write_text(f"{marker}\n", encoding="utf-8")
    (setup / "SKILL.md").write_text(f"{marker}\n", encoding="utf-8")
    (setup / "scripts/validate_setup.py").write_text(
        f"SETUP_SCHEMA_TOKEN = {marker!r}\n",
        encoding="utf-8",
    )
    (setup / "setup-schema.json").write_text(
        json.dumps(
            {
                "format": 1,
                "version": 1,
                "contract_files": contract_files,
                "contract_sha256": fingerprint,
            }
        ),
        encoding="utf-8",
    )

    assert validate_skills.validate_setup_schema_manifest(tmp_path) == []

    (setup / "domain.md").write_text("# Changed Domain\n", encoding="utf-8")

    failures = validate_skills.validate_setup_schema_manifest(tmp_path)
    assert any("contract fingerprint is stale" in failure for failure in failures)


def test_relationship_invocation_map_must_match_policies(tmp_path: Path) -> None:
    write_skill(tmp_path, "implicit")
    explicit = write_skill(tmp_path, "explicit")
    (explicit / "agents/openai.yaml").write_text(
        "policy:\n  allow_implicit_invocation: false\n",
        encoding="utf-8",
    )
    relationship_map = tmp_path / "docs/synthesis/skill-context-relationships.md"
    relationship_map.parent.mkdir(parents=True)
    relationship_map.write_text(
        "| Skill | Invocation |\n"
        "| --- | --- |\n"
        "| `explicit` | implicitly invocable |\n"
        "| `retired` | explicit-only |\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_relationship_invocation_map(tmp_path)

    assert "Relationship invocation map is missing skill: implicit" in failures
    assert "Relationship invocation map contains unknown skill: retired" in failures
    assert any("disagrees with policy: explicit" in failure for failure in failures)


def test_installed_validation_preserves_unrelated_skills(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    source = write_skill(root, "example")
    installed.mkdir()
    (installed / "finance-brain").mkdir()
    destination = installed / "example"
    destination.mkdir()
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        if path.is_dir():
            (destination / relative).mkdir(exist_ok=True)
        else:
            (destination / relative).write_bytes(path.read_bytes())
    (installed / validate_skills.INSTALLED_MANIFEST).write_text(
        json.dumps({"skills": ["example"]}),
        encoding="utf-8",
    )

    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert failures == []


def test_git_diff_validation_checks_worktree_and_index(monkeypatch, tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def fake_run_git(args: list[str], *, cwd: Path, check: bool = False):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(validate_skills, "run_git", fake_run_git)

    assert validate_skills.validate_git_diff_check(tmp_path) == []
    assert ["diff", "--check"] in calls
    assert ["diff", "--cached", "--check"] in calls
