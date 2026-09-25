from __future__ import annotations

import json
import runpy
import shutil
import stat
import subprocess
import sys
import tomllib
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import pytest_focused, pytest_runtime, skill_pack_contract, validate_skills


def test_repository_owned_contract_accepts_local_changes_without_a_marker() -> None:
    root = Path(__file__).resolve().parents[1]
    check = runpy.run_path(
        str(root / "skills/custom/repo-bootstrap/scripts/validate_setup.py")
    )["engineering_contract_failures"]
    contract = "# Engineering contract\n\n## Local decisions\n\nPreserve ledger identities.\n"
    assert check(contract, "contract.md", repository_owned=True) == []
    assert check(contract, "contract.md")  # Legacy mode still requires its marker.
    assert validate_skills.validate_setup_surface(root) == []


@pytest.mark.parametrize("contract", [
    "# Wrong document\n\n## Rules\n\nContent.\n",
    "# Engineering contract\n\n# Engineering contract\n\n## Rules\n\nContent.\n",
    "# Engineering contract\n\n## Rules\n\n<!-- comment only -->\n",
    "# Engineering contract\n\n## Rules\n\n```text\nexample only\n```\n",
])
def test_repository_owned_contract_rejects_missing_structure(contract: str) -> None:
    root = Path(__file__).resolve().parents[1]
    check = runpy.run_path(
        str(root / "skills/custom/repo-bootstrap/scripts/validate_setup.py")
    )["engineering_contract_failures"]
    assert check(contract, "contract.md", repository_owned=True)


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


def test_astra_validates_implicit_metadata_resources_and_own_routes(tmp_path: Path) -> None:
    skill = tmp_path / "skills/astra/example"
    skill.mkdir(parents=True)
    entry = skill / "SKILL.md"
    entry.write_text("---\nname: example\ndescription: Example task.\n---\n", encoding="utf-8")
    write_skill(tmp_path, "retired")
    assert validate_skills.validate_astra(tmp_path) == (["example"], [])
    (skill / "agents").mkdir()
    policy = skill / "agents/openai.yaml"
    policy.write_text("policy:\n  allow_implicit_invocation: False\n", encoding="utf-8")
    assert validate_skills.validate_astra(tmp_path)[1] == []
    policy.write_text("policy:\n  allow_implicit_invocation: 'false'\n", encoding="utf-8")
    assert any("boolean" in item for item in validate_skills.validate_astra(tmp_path)[1])
    policy.write_text(
        "policy:\n  allow_implicit_invocation: false\n  broken: [\n",
        encoding="utf-8",
    )
    assert any(
        "Invalid skill metadata" in item
        for item in validate_skills.validate_astra(tmp_path)[1]
    )
    policy.unlink()
    entry.write_text(entry.read_text() + (
        "Read [guide](references/missing.md). Use $retired.\n"
        "Read [old](../../custom/retired/SKILL.md).\n"
    ))
    failures = validate_skills.validate_astra(tmp_path)[1]
    assert any("resource reference is missing" in item for item in failures)
    assert any("Astra references missing skill" in item for item in failures)
    assert any("must stay inside skills/astra/" in item for item in failures)


def test_astra_metadata_rejects_invalid_optional_interface_fields(
    tmp_path: Path,
) -> None:
    skill = tmp_path / "skills/astra/example"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Example task.\n---\n",
        encoding="utf-8",
    )
    (skill / "agents/openai.yaml").write_text(
        "interface:\n"
        "  display_name: []\n"
        "  short_description: \"\"\n"
        "policy:\n"
        "  allow_implicit_invocation: false\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_astra(tmp_path)[1]

    assert any("display_name must be a non-empty string" in item for item in failures)
    assert any("short_description must be a non-empty string" in item for item in failures)


def test_astra_readme_catalog_matches_packages_and_invocation_metadata(
    tmp_path: Path,
) -> None:
    automatic = tmp_path / "skills/astra/automatic"
    automatic.mkdir(parents=True)
    (automatic / "SKILL.md").write_text(
        "---\nname: automatic\ndescription: Automatic task.\n---\n",
        encoding="utf-8",
    )

    explicit = tmp_path / "skills/astra/explicit"
    (explicit / "agents").mkdir(parents=True)
    (explicit / "SKILL.md").write_text(
        "---\nname: explicit\ndescription: Explicit task.\n---\n",
        encoding="utf-8",
    )
    (explicit / "agents/openai.yaml").write_text(
        "policy:\n  allow_implicit_invocation: false\n",
        encoding="utf-8",
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        "| Your task | Skill | Use |\n"
        "| --- | --- | --- |\n"
        "| Automatic work | [$automatic](skills/astra/automatic/SKILL.md) | "
        "Automatic when relevant |\n"
        "| Explicit work | [$explicit](skills/astra/explicit/SKILL.md) | "
        "Request explicitly |\n",
        encoding="utf-8",
    )

    assert validate_skills.validate_astra_readme_catalog(
        tmp_path, ["automatic", "explicit"]
    ) == []

    readme.write_text(
        "| Your task | Skill | Use |\n"
        "| --- | --- | --- |\n"
        "| Wrong mode | [$automatic](skills/astra/automatic/SKILL.md) | "
        "Request explicitly |\n"
        "| Wrong link | [$explicit](skills/astra/automatic/SKILL.md) | "
        "Request explicitly |\n"
        "| Duplicate | [$explicit](skills/astra/explicit/SKILL.md) | "
        "Request explicitly |\n"
        "| Unknown | [$retired](skills/astra/retired/SKILL.md) | "
        "Automatic when relevant |\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_astra_readme_catalog(
        tmp_path, ["automatic", "explicit", "missing"]
    )

    assert "README Astra catalog repeats skill: explicit" in failures
    assert "README Astra catalog is missing skill: missing" in failures
    assert "README Astra catalog contains unknown skill: retired" in failures
    assert any("link disagrees with skill name: explicit" in item for item in failures)
    assert any("invocation disagrees with metadata: automatic" in item for item in failures)


def test_astra_selection_examples_match_managed_inventory(tmp_path: Path) -> None:
    examples = tmp_path / validate_skills.ASTRA_SELECTION_EXAMPLES
    examples.parent.mkdir(parents=True)
    examples.write_text(
        "| Skill | Canonical request | Expected behavior | Nearest non-match |\n"
        "| --- | --- | --- | --- |\n"
        "| [$automatic](../../skills/astra/automatic/SKILL.md) | request | expected | near miss |\n"
        "| [$explicit](../../skills/astra/explicit/SKILL.md) | request | expected | near miss |\n",
        encoding="utf-8",
    )

    assert validate_skills.validate_astra_selection_examples(
        tmp_path, ["automatic", "explicit"]
    ) == []

    examples.write_text(
        "| Skill | Canonical request | Expected behavior | Nearest non-match |\n"
        "| --- | --- | --- | --- |\n"
        "| [$automatic](../../skills/astra/automatic/SKILL.md) | request | expected | near miss |\n"
        "| [$explicit](../../skills/astra/automatic/SKILL.md) | request | expected | near miss |\n"
        "| [$explicit](../../skills/astra/explicit/SKILL.md) | request | expected | near miss |\n"
        "| [$retired](../../skills/astra/retired/SKILL.md) | request | expected | near miss |\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_astra_selection_examples(
        tmp_path, ["automatic", "explicit", "missing"]
    )

    assert "Astra selection examples repeat skill: explicit" in failures
    assert "Astra selection examples are missing skill: missing" in failures
    assert "Astra selection examples contain unknown skill: retired" in failures
    assert any("link disagrees with skill name: explicit" in item for item in failures)


def test_astra_frontmatter_uses_yaml_and_rejects_nonstring_identity(
    tmp_path: Path,
) -> None:
    skill = tmp_path / "skills/astra/example"
    skill.mkdir(parents=True)
    entry = skill / "SKILL.md"
    entry.write_text(
        "---\n"
        "name: example\n"
        "description: >-\n"
        "  Multi-line discovery description\n"
        "  remains valid YAML.\n"
        "---\n",
        encoding="utf-8",
    )

    assert validate_skills.validate_astra(tmp_path) == (["example"], [])

    entry.write_text(
        "---\nname: [example]\ndescription: 123\n---\n",
        encoding="utf-8",
    )
    _, failures = validate_skills.validate_astra(tmp_path)

    assert any("Skill name must match its directory" in item for item in failures)
    assert any("Skill name is invalid" in item for item in failures)
    assert any("Skill description is missing" in item for item in failures)


def test_current_required_docs_do_not_depend_on_legacy_custom_pack(
    tmp_path: Path,
) -> None:
    for relative in validate_skills.CURRENT_REQUIRED_FILES:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("current\n", encoding="utf-8")

    assert validate_skills.validate_required_docs(tmp_path) == []

    failures = validate_skills.validate_required_docs(tmp_path, include_legacy=True)
    assert failures == [
        "Missing required repository file: "
        "skills/custom/repo-bootstrap/engineering-contract.md"
    ]


def test_current_active_surface_scan_excludes_legacy_custom_pack(
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text("Current guidance.\n", encoding="utf-8")
    legacy = tmp_path / "skills/custom/example/SKILL.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("Use $improve-codebase.\n", encoding="utf-8")

    assert validate_skills.validate_active_surfaces(tmp_path) == []
    assert validate_skills.validate_active_surfaces(
        tmp_path, include_legacy=True
    ) == [
        "Active surface contains stale token: "
        "skills/custom/example/SKILL.md -> $improve-codebase"
    ]


def test_legacy_handle_validation_uses_current_and_legacy_surfaces(
    tmp_path: Path,
) -> None:
    current = tmp_path / "README.md"
    current.write_text("Use $current.\n", encoding="utf-8")
    legacy = tmp_path / "docs/synthesis/skill-context-relationships.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("Use $legacy.\n", encoding="utf-8")

    current_skill = tmp_path / "skills/astra/current"
    current_skill.mkdir(parents=True)
    (current_skill / "SKILL.md").write_text(
        "---\nname: current\ndescription: Current task.\n---\n",
        encoding="utf-8",
    )
    legacy_skill = tmp_path / "skills/custom/legacy"
    legacy_skill.mkdir(parents=True)

    assert validate_skills.validate_skill_handle_references(
        tmp_path, ["legacy"]
    ) == []


def test_manifest_rejects_nonscalar_source_without_crashing() -> None:
    _, _, failures = skill_pack_contract.parse_managed_manifest_payload({
        "format": 1, "source": [], "skills": [], "hashes": {},
    })
    assert "Installed skill manifest source must be skills/astra." in failures


def install_example_skill(
    root: Path,
    installed: Path,
    *,
    manifest_payload: dict[str, object] | None = None,
    write_manifest: bool = True,
) -> tuple[Path, Path, Path]:
    source = write_skill(root, "example")
    target = root / "skills/astra/example"
    target.parent.mkdir(parents=True)
    source.rename(target)
    source = target
    destination = installed / "example"
    shutil.copytree(source, destination)
    manifest = installed / validate_skills.INSTALLED_MANIFEST
    if write_manifest:
        payload = manifest_payload or {
            "format": 1,
            "source": "skills/astra",
            "skills": ["example"],
            "hashes": {"example": skill_pack_contract.tree_hash(source)},
        }
        manifest.write_text(json.dumps(payload), encoding="utf-8")
    return source, destination, manifest


def test_installed_astra_parity_ignores_runtime_caches_but_rejects_legacy_source(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    source, destination, manifest = install_example_skill(root, installed)
    for folder in (source, destination):
        cache = folder / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "helper.pyc").write_bytes(str(folder).encode())
    assert validate_skills.validate_installed_skills(root, ["example"], str(installed), True) == []
    payload = json.loads(manifest.read_text())
    payload["source"] = "skills/custom"
    manifest.write_text(json.dumps(payload))
    failures = validate_skills.validate_installed_skills(root, ["example"], str(installed), True)
    assert any("source must be skills/astra" in item for item in failures)


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

    assert len(failures) == 1
    assert "resource reference is missing" in failures[0]
    assert (skill / "GUIDE.md").as_posix() in failures[0]
    assert "references/MISSING.md" in failures[0]


def test_experimental_manifest_tracks_candidates_without_activating_them(
    tmp_path: Path,
) -> None:
    active = write_skill(tmp_path, "example")
    experimental = tmp_path / "skills/experimental/example"
    shutil.copytree(active, experimental)
    candidate_hash = skill_pack_contract.tree_hash(experimental)
    baseline_hash = skill_pack_contract.tree_hash(active)
    manifest = tmp_path / "skills/experimental/manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "format": 1,
                "active_root": "skills/custom",
                "experimental_root": "skills/experimental",
                "skills": {
                    "example": {
                        "origin": "test capture",
                        "reason": "test candidate",
                        "candidate_sha256": candidate_hash,
                        "active_baseline_sha256": baseline_hash,
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    assert validate_skills.validate_experimental_skills(tmp_path) == []

    (experimental / "SKILL.md").write_text(
        (experimental / "SKILL.md").read_text(encoding="utf-8") + "changed\n",
        encoding="utf-8",
    )
    assert "Experimental candidate hash differs: example" in (
        validate_skills.validate_experimental_skills(tmp_path)
    )

    shutil.rmtree(active)
    failures = validate_skills.validate_experimental_skills(tmp_path)
    assert "Experimental skill has no active custom counterpart: example" in failures


def test_global_bootstrap_validation_requires_one_structured_managed_section(
    tmp_path: Path,
) -> None:
    template = tmp_path / validate_skills.GLOBAL_AGENTS_TEMPLATE
    template.write_text(
        "# Global Codex Instructions\n\n"
        "**Route:** **Setup:** **Boundary:**\n\n"
        "```markdown\n## Skill Pack Bootstrap\n```\n\n"
        "## Skill Pack Bootstrap\n\n"
        "Mention `$skill-router` and `$repo-bootstrap` without role bullets.\n",
        encoding="utf-8",
    )

    failures = validate_skills.validate_global_agents_template(
        tmp_path, ["repo-bootstrap", "skill-router"]
    )

    assert any("structured Route, Setup, and Boundary roles" in item for item in failures)

    template.write_text(
        "# Global Codex Instructions\n\n"
        "## Skill Pack Bootstrap\n\n"
        "- **Route:** `$skill-router`\n"
        "- **Setup:** `$repo-bootstrap`\n"
        "- **Boundary:** owners\n\n"
        "## Skill Pack Bootstrap\n\nDuplicate.\n",
        encoding="utf-8",
    )
    failures = validate_skills.validate_global_agents_template(
        tmp_path, ["repo-bootstrap", "skill-router"]
    )
    assert any("exactly one" in item for item in failures)


def test_skill_handle_validation_rejects_unknown_custom_skill(tmp_path: Path) -> None:
    write_skill(tmp_path, "example", "Route to `$missing-skill`.")

    failures = validate_skills.validate_skill_handle_references(tmp_path, ["example"])

    assert len(failures) == 1
    assert "missing custom skill" in failures[0]
    assert "skills/custom/example/SKILL.md" in failures[0]
    assert "$missing-skill" in failures[0]


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

    assert len(failures) == 1
    assert "missing custom skill" in failures[0]
    assert "skills/custom/example/agents/openai.yaml" in failures[0]
    assert "$missing-skill" in failures[0]


def test_active_surface_validation_rejects_retired_improvement_names_only_on_active_surfaces(
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text(
        "Use improve-codebase-architecture.\n", encoding="utf-8"
    )
    historical = tmp_path / "docs/validation/transcripts/historical.md"
    historical.parent.mkdir(parents=True)
    historical.write_text("Used improve-codebase-architecture.\n", encoding="utf-8")

    failures = validate_skills.validate_active_surfaces(tmp_path)

    assert failures == [
        "Active surface contains stale token: README.md -> "
        "improve-codebase-architecture"
    ]

    (tmp_path / "README.md").write_text("Use $improve-codebase.\n", encoding="utf-8")
    assert validate_skills.validate_active_surfaces(tmp_path) == [
        "Active surface contains stale token: README.md -> $improve-codebase"
    ]


def test_setup_schema_fingerprint_detects_contract_drift(tmp_path: Path) -> None:
    setup = tmp_path / validate_skills.SETUP_SKILL_ROOT
    (setup / "scripts").mkdir(parents=True)
    (setup / "domain.md").write_text("# Domain\n", encoding="utf-8")
    contract_files = ["domain.md"]
    fingerprint = validate_skills.setup_contract_hash(tmp_path, contract_files)
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


def test_setup_schema_rejects_paths_outside_its_package(tmp_path: Path) -> None:
    setup = tmp_path / validate_skills.SETUP_SKILL_ROOT
    setup.mkdir(parents=True)
    outside = tmp_path / "outside.md"
    outside.write_text("not a setup seed\n", encoding="utf-8")

    for relative in ("../../../outside.md", str(outside.resolve())):
        (setup / "setup-schema.json").write_text(
            json.dumps(
                {
                    "format": 1,
                    "version": 1,
                    "contract_files": [relative],
                    "contract_sha256": "0" * 64,
                }
            ),
            encoding="utf-8",
        )
        failures = validate_skills.validate_setup_schema_manifest(tmp_path)
        assert any("normalized relative paths" in failure for failure in failures)


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
    installed.mkdir()
    (installed / "finance-brain").mkdir()
    install_example_skill(root, installed)

    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert failures == []


def test_installed_validation_rejects_empty_directory_drift(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    _, destination, _ = install_example_skill(root, installed)
    (destination / "extra-empty").mkdir()

    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert "Installed skill differs from repo: example" in failures
    assert any(
        "Only in installed copy: directory extra-empty" in failure
        for failure in failures
    )


def test_installed_validation_rejects_symlinked_and_empty_directory_drift(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    _, destination, _ = install_example_skill(root, installed)
    (destination / "extra-empty").mkdir()
    external = tmp_path / "external-skill.md"
    external.write_bytes((destination / "SKILL.md").read_bytes())
    (destination / "SKILL.md").unlink()
    try:
        (destination / "SKILL.md").symlink_to(external)
    except OSError as error:
        pytest.skip(f"symlink creation unavailable: {error}")
    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert "Installed skill differs from repo: example" in failures
    assert any("Unsafe special tree entry" in failure for failure in failures)


@pytest.mark.parametrize("unsafe_kind", ["root", "manifest"])
def test_installed_validation_rejects_reparse_root_and_manifest_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    unsafe_kind: str,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    _, _, manifest = install_example_skill(root, installed)
    unsafe = installed if unsafe_kind == "root" else manifest
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
        if Path(path) == unsafe:
            return ReparseMetadata(metadata)
        return metadata

    monkeypatch.setattr(skill_pack_contract.os, "lstat", fake_lstat)

    failures = validate_skills.validate_installed_skills(
        root, ["example"], str(installed), True
    )

    assert any("unsafe" in failure.lower() for failure in failures)


def test_installed_validation_rejects_manifest_contract_and_hash_drift(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    install_example_skill(
        root,
        installed,
        manifest_payload={
            "format": 2,
            "source": "legacy/source",
            "skills": ["example"],
            "hashes": {"example": "0" * 64},
        },
    )

    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert "Installed skill manifest must use format 1." in failures
    assert "Installed skill manifest source must be skills/astra." in failures
    assert "Installed manifest hash differs from repo: example" in failures


def test_required_installed_validation_rejects_a_missing_manifest(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    installed = tmp_path / "installed"
    install_example_skill(root, installed, write_manifest=False)

    failures = validate_skills.validate_installed_skills(
        root,
        ["example"],
        str(installed),
        True,
    )

    assert len(failures) == 1
    assert "installed skill manifest is missing" in failures[0]
    assert str(installed / validate_skills.INSTALLED_MANIFEST) in failures[0]


def test_public_scan_safe_markers_cover_reserved_fixture_values() -> None:
    assert "@example.invalid" in validate_skills.PUBLIC_SCAN_SAFE_MARKERS
    assert "correct-horse-battery-staple" in validate_skills.PUBLIC_SCAN_SAFE_MARKERS


def test_public_mode_scans_only_current_public_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls: list[list[str]] = []

    def fake_run_git(args: list[str], *, cwd: Path, check: bool = False):
        calls.append(args)
        if args == ["ls-files"]:
            return subprocess.CompletedProcess(args, 0, "README.md\n", "")
        if args == ["ls-files", "-ci", "--exclude-standard"]:
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:4] == ["grep", "-n", "-I", "-E"]:
            return subprocess.CompletedProcess(args, 1, "", "")
        raise AssertionError(args)

    monkeypatch.setattr(validate_skills, "run_git", fake_run_git)

    assert validate_skills.validate_public_mode(tmp_path) == []

    grep_call = next(call for call in calls if call[:4] == ["grep", "-n", "-I", "-E"])
    assert grep_call[grep_call.index("--") + 1 :] == list(
        validate_skills.PUBLIC_CURRENT_SCAN_PATHS
    )
    assert "." not in grep_call[grep_call.index("--") + 1 :]


def test_portable_and_bootstrap_contracts_keep_continuation_boundary() -> None:
    root = Path(__file__).resolve().parents[1]
    surfaces = (
        root / "AGENTS_PORTABLE_FALLBACK.md",
        root / "skills/astra/repo-bootstrap/templates/engineering-contract.md",
    )
    for path in surfaces:
        text = " ".join(path.read_text(encoding="utf-8").split())
        for marker in (
            "Continue through authorized implementation, verification",
            "Status updates, intermediate findings, passing checks, and reversible "
            "non-blocking choices are not stopping points",
            "Stop when required user input or authority is missing",
        ):
            assert marker in text


def test_writing_for_agents_keeps_long_run_instruction_boundaries() -> None:
    root = Path(__file__).resolve().parents[1]
    skill = (root / "skills/astra/writing-for-agents/SKILL.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        "state the continuation policy",
        "offer to continue",
        '"think carefully," "think hard,"',
        "host's supported reasoning/effort control",
        "small durable progress artifact",
        "Do not create a progress artifact for ordinary bounded work",
    ):
        assert marker in skill


def test_current_triage_and_verification_harness_keep_safety_boundaries() -> None:
    root = Path(__file__).resolve().parents[1]
    triage = (root / "skills/astra/triage/SKILL.md").read_text(encoding="utf-8")
    harness = (root / "skills/astra/verification-harness/SKILL.md").read_text(
        encoding="utf-8"
    )

    for marker in (
        "exactly one configured category role",
        "exactly one configured state role",
        "active configured blocker",
        "do not replay a comment, brief, or role",
        "Do not claim rollback",
    ):
        assert marker in triage

    for marker in (
        "**Failure sensitivity:**",
        "**Harness defect:**",
        "**Product defect:**",
        "**Environment blocker:**",
        "shown capable of failing",
    ):
        assert marker in harness


def test_git_diff_validation_checks_worktree_and_index(monkeypatch, tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def fake_run_git(args: list[str], *, cwd: Path, check: bool = False):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(validate_skills, "run_git", fake_run_git)

    assert validate_skills.validate_git_diff_check(tmp_path) == []
    assert ["diff", "--check"] in calls
    assert ["diff", "--cached", "--check"] in calls


def test_focused_pytest_default_targets_current_contract_suite(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(command: list[str]):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(pytest_focused.subprocess, "run", fake_run)

    assert pytest_focused.main(None) == 0
    target = "tests/test_validate_skills.py"
    selector = (
        "astra or current_ or installed or global_bootstrap or git_diff or pytest_runtime"
    )
    assert (Path(__file__).resolve().parents[1] / target).is_file()
    assert calls == [[
        sys.executable,
        "-m",
        "pytest",
        "-n",
        "0",
        target,
        "-k",
        selector,
    ]]


def test_default_pytest_parallelism_is_capped_at_ten() -> None:
    root = Path(__file__).resolve().parents[1]
    config = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    addopts = config["tool"]["pytest"]["ini_options"]["addopts"]

    assert addopts[addopts.index("-n") + 1] == "auto"
    assert addopts[addopts.index("--maxprocesses") + 1] == "10"


def test_pytest_runtime_isolates_and_removes_disposable_state(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    identity = uuid.UUID("e4bf66bb-dd58-43b1-9413-bf434935edf5")
    config = SimpleNamespace(
        rootpath=tmp_path,
        option=SimpleNamespace(basetemp=None),
        _inicache={"cache_dir": ".pytest_cache"},
    )
    monkeypatch.setattr(pytest_runtime.uuid, "uuid4", lambda: identity)

    pytest_runtime.pytest_configure(config)

    session = tmp_path / ".tmp" / f"pytest-session-{identity}"
    assert session.is_dir()
    assert config.option.basetemp == str(session / "tmp")
    assert config._inicache["cache_dir"] == str(session / "cache")

    read_only = session / "tmp" / "nested" / "fixture.txt"
    read_only.parent.mkdir(parents=True)
    read_only.write_text("fixture\n", encoding="utf-8")
    read_only.chmod(stat.S_IREAD)

    pytest_runtime.remove_session(config)

    assert not session.exists()
