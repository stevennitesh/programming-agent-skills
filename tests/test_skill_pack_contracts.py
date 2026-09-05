from __future__ import annotations

import hashlib
import json
import re
import runpy
from pathlib import Path

from scripts import (
    skill_pack_contract,
    validate_skills,
)


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "skills/custom"


def legacy_engineering_contract() -> str:
    """Materialize the legacy seed for tests of the custom pack's contract."""
    source = CUSTOM / "repo-bootstrap/engineering-contract.md"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    marker = f"<!-- programming-agent-skills setup-file: engineering-contract.md:{digest} -->"
    return source.read_text(encoding="utf-8").replace(
        "# Engineering Contract\n", f"# Engineering Contract\n\n{marker}\n", 1
    )


def exact_tree_hash(directory: Path) -> str:
    files = [
        (name, content)
        for name, (kind, content) in skill_pack_contract.tree_entries(directory).items()
        if kind == "file"
    ]
    digest = hashlib.sha256()
    for name, content in sorted(files, key=lambda item: item[0].encode("utf-8")):
        file_sha256 = hashlib.sha256(content).hexdigest()
        digest.update(f"{name}\t{len(content)}\t{file_sha256}\n".encode("utf-8"))
    return digest.hexdigest()


def implicit_policy(skill: Path) -> bool:
    text = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    match = re.search(r"allow_implicit_invocation:\s*(true|false)", text)
    assert match is not None
    return match.group(1) == "true"


def test_router_names_every_custom_skill() -> None:
    router = (CUSTOM / "skill-router/SKILL.md").read_text(encoding="utf-8")
    skill_names = {skill.name for skill in CUSTOM.iterdir() if skill.is_dir()}
    routes = re.findall(
        r"(?m)^\| (?!-)([^|]+?) \| `\$([a-z0-9][a-z0-9-]*)` \|$", router
    )
    routed = [skill for _, skill in routes]

    assert set(routed) | {"repo-bootstrap"} == skill_names - {"skill-router"}
    assert len(routed) == len(set(routed))
    assert routed.count("high-assurance-review") == 1


def test_repo_bootstrap_validates_provider_tracker_templates() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["tracker_configuration_failures"]
    trackers = (
        CUSTOM / "repo-bootstrap/issue-tracker-github.md",
        CUSTOM / "repo-bootstrap/issue-tracker-gitlab.md",
        CUSTOM / "repo-bootstrap/issue-tracker-local.md",
    )

    for tracker in trackers:
        text = tracker.read_text(encoding="utf-8")
        assert check(text) == []

    github = trackers[0].read_text(encoding="utf-8")
    missing_mode = github.replace("native-sub-issues", "when-available", 1)
    assert check(missing_mode) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitHub mode"
    ]


def test_repo_bootstrap_validates_selected_domain_layout() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    def check(text):
        return validator["domain_layout_failures"](text, domain_owner="shape-work")
    domain = (ROOT / "docs/agents/domain.md").read_text(encoding="utf-8")

    assert check(domain) == []
    assert check(domain.replace("single-context.", "unknown.")) == [
        "docs/agents/domain.md must set Configured layout to "
        "single-context or multi-context"
    ]
    assert check(domain.replace("$shape-work", "$domain-modeling")) == [
        "docs/agents/domain.md must point to $shape-work"
    ]


def test_repo_bootstrap_owns_optional_parallel_support_and_reconciliation(
    tmp_path: Path,
) -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["parallel_support_failures"]
    root = tmp_path / "repo"
    root.mkdir()

    assert check(root) == []

    config = root / validator["PARALLEL_CONFIG"]
    config.parent.mkdir(parents=True)
    config.write_text('default_permissions = "workspace"\n', encoding="utf-8")
    assert check(root) == []

    lane_root = tmp_path / "lanes" / "wt"
    encoded_lane_root = json.dumps(str(lane_root.resolve()))
    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{encoded_lane_root} = true\n"
        f"{json.dumps(str((tmp_path / 'cache').resolve()))} = true\n",
        encoding="utf-8",
    )
    assert check(root) == []

    nested_root = root / "nested" / "wt"
    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{json.dumps(str(nested_root.resolve()))} = true\n",
        encoding="utf-8",
    )
    assert check(root) == ["parallel lane root must be outside the repository"]

    config.write_text(
        "default_permissions = \"project-lanes\"\n\n"
        "[permissions.project-lanes]\n"
        "extends = \":workspace\"\n\n"
        "[permissions.project-lanes.workspace_roots]\n"
        f"{encoded_lane_root} = true\n",
        encoding="utf-8",
    )
    assert check(root) == []


def test_repo_bootstrap_schema_fingerprint_matches_shipped_files() -> None:
    assert validate_skills.validate_setup_schema_manifest(ROOT) == []


def test_portable_fallback_adoption_removes_the_portable_contract_owner() -> None:
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )

    failures = validator["portable_owner_failures"](fallback)
    assert len(failures) == 1
    assert "$repo-bootstrap" in failures[0]
    assert validator["portable_owner_failures"](
        "# Repository Instructions\n\n## Skill Pack\n\nAGENTS primes.\n"
    ) == []
    marker = validator["PORTABLE_OWNER_MARKER"]
    assert fallback.count(marker) == 1
    partial_adoption = fallback.replace("# Global Codex Instructions", "")
    assert validator["portable_owner_failures"](partial_adoption) == failures
    reworded = fallback.replace(
        "Use this as your global `AGENTS.md` when the skill pack is not installed.",
        "This file supplies global engineering defaults without an installed pack.",
    )
    assert validator["portable_owner_failures"](reworded) == failures
    assert validator["portable_owner_failures"](
        fallback.replace(marker, "")
    ) == []

    valid_agents = (
        "# Repository Instructions\n\n"
        "Repository-specific guidance.\n\n"
        "## Commands\n\n- Test: `python -m pytest`\n"
    )
    command_failure = ["AGENTS.md must contain one unfenced ## Commands heading"]
    assert validator["agents_commands_failures"](valid_agents) == []
    assert validator["agents_commands_failures"](
        valid_agents.replace("## Commands", "## Local Commands")
    ) == command_failure
    assert validator["agents_commands_failures"](
        valid_agents.replace("## Commands", "```text\n## Commands\n```")
    ) == command_failure
    assert validator["agents_commands_failures"](
        valid_agents + "\n## Commands\n"
    ) == command_failure

    assert validator["git_root_failures"](ROOT) == []
    assert validator["git_root_failures"](ROOT / "skills") == [
        "Target must be the Git repository root"
    ]


def test_engineering_contract_validation_is_structural_and_causal() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    check = validator["engineering_contract_failures"]
    contract = legacy_engineering_contract()

    assert check(contract, "engineering-contract.md") == []
    for invalid in (
        contract.replace("# Engineering Contract\n", ""),
        contract.replace(
            "# Engineering Contract\n",
            "# Engineering Contract\n\n# Engineering Contract\n",
        ),
        contract.replace(
            "# Engineering Contract\n",
            "```text\n# Engineering Contract\n```\n",
        ),
        contract.replace("<!-- programming-agent-skills setup-file:", "<!-- stale:"),
        contract.replace(
            "<!-- programming-agent-skills setup-file: engineering-contract.md:",
            "<!-- programming-agent-skills setup-file: engineering-contract.md:deadbeefdead -->\n"
            "<!-- programming-agent-skills setup-file: engineering-contract.md:",
        ),
        contract.replace(
            "<!-- programming-agent-skills setup-file:",
            "```text\n<!-- programming-agent-skills setup-file:",
        ).replace(" -->\n\nExplore imaginatively", " -->\n```\n\nExplore imaginatively", 1),
    ):
        assert check(invalid, "engineering-contract.md")

    renamed_outline = contract.replace(
        "## Design Defaults — Prefer", "## Design Guidance"
    ).replace("### Use A Negative Control", "### Exercise A Failing Case")
    assert check(renamed_outline, "engineering-contract.md") == []
    marker = validator["SETUP_FILE_MARKER_RE"].findall(contract)[0]
    assert check(f"# Engineering Contract\n\n{marker}\n", "engineering-contract.md")
    assert check(
        f"# Engineering Contract\n\n{marker}\n\n## Empty\n\n<!-- comment only -->\n",
        "engineering-contract.md",
    )
    assert check(
        f"# Engineering Contract\n\n{marker}\n\n## Empty\n\n"
        "```text\nexample only\n```\n",
        "engineering-contract.md",
    )
    assert check(
        f"# Engineering Contract\n\n{marker}\n\nprose outside a section\n\n## Empty\n",
        "engineering-contract.md",
    )


def test_repo_bootstrap_accepts_reworded_owner_pointers() -> None:
    validator = runpy.run_path(
        str(CUSTOM / "repo-bootstrap/scripts/validate_setup.py")
    )
    pointers = validator["AGENT_POINTERS"]
    reworded = "Read these owners when their contracts apply:\n" + "\n".join(
        f"- {pointer}" for pointer in pointers
    )
    assert validator["agent_pointer_failures"](reworded) == []

    assert validator["agent_pointer_failures"](
        reworded.replace("docs/agents/engineering-contract.md", "docs/engineering.md")
    ) == [
        "AGENTS.md is missing docs/agents/engineering-contract.md"
    ]
    commented = "\n".join(f"<!-- {pointer} -->" for pointer in pointers)
    assert validator["agent_pointer_failures"](commented) == [
        f"AGENTS.md is missing {pointer}" for pointer in pointers
    ]


def test_implement_current_reconciliation_tracks_runtime_tree() -> None:
    synthesis = (ROOT / "docs/synthesis/skills/implement.md").read_text(
        encoding="utf-8"
    )
    current_reconciliation = synthesis.split(
        "## Active Promoted And Installed Decision", 1
    )[0]

    assert "revision 51 and machine contract revision 39" in current_reconciliation
    assert exact_tree_hash(CUSTOM / "implement") in current_reconciliation


def test_runtime_composition_edges_respect_lean_review_and_planning_policy() -> None:
    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    rows = re.findall(
        r"(?m)^\| `([a-z0-9][a-z0-9-]*)` \| "
        r"(Load|Invoke|Compose|Hand off|Recommend and stop) \| "
        r"`\$([a-z0-9][a-z0-9-]*)` \|",
        relationships,
    )
    edges = set(rows)

    for edge in (
        ("to-spec", "Recommend and stop", "implement"),
        ("to-spec", "Recommend and stop", "to-tickets"),
        ("to-tickets", "Recommend and stop", "implement"),
        ("to-tickets", "Recommend and stop", "parallel-implement"),
        ("parallel-implement", "Recommend and stop", "implement"),
        ("implement", "Invoke", "change-review"),
        ("parallel-implement", "Invoke", "change-review"),
        ("triage", "Recommend and stop", "change-review"),
        ("triage", "Recommend and stop", "diagnosing-bugs"),
        ("triage", "Recommend and stop", "to-tickets"),
    ):
        assert edge in edges
    assert not any(
        caller == "wayfinder" and callee in {"domain-modeling", "implement", "to-spec"}
        for caller, _, callee in edges
    )
    assert ("skill-router", "Recommend and stop", "high-assurance-review") in edges
    assert not any(
        callee == "high-assurance-review"
        and caller in {"implement", "parallel-implement", "change-review"}
        for caller, _, callee in edges
    )
    assert ("implement", "Recommend and stop", "to-tickets") not in edges
    assert "ToSpec --> Labels" not in relationships
    assert not implicit_policy(CUSTOM / "high-assurance-review")
