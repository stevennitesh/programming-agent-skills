"""Setup validation for current repository owners and retained custom setups."""
from __future__ import annotations

import hashlib
import json
import runpy
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/custom/repo-bootstrap"
VALIDATOR = runpy.run_path(str(PACKAGE / "scripts/validate_setup.py"))


def test_required_setup_reads_valid_and_missing_files(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("valid setup\n", encoding="utf-8")
    failures: list[str] = []

    assert VALIDATOR["read_required"](tmp_path, "AGENTS.md", failures) == (
        "valid setup\n"
    )
    assert failures == []

    assert VALIDATOR["read_required"](tmp_path, "missing.md", failures) == ""
    assert failures == ["Missing required setup file: missing.md"]


def test_tracker_seeds_have_selected_structural_configuration() -> None:
    check = VALIDATOR["tracker_configuration_failures"]

    for name in (
        "issue-tracker-github.md",
        "issue-tracker-gitlab.md",
        "issue-tracker-local.md",
    ):
        tracker = (PACKAGE / name).read_text(encoding="utf-8")
        assert check(tracker) == []

    github = (PACKAGE / "issue-tracker-github.md").read_text(encoding="utf-8")
    assert check(github.replace("native-sub-issues", "when-available", 1)) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitHub mode"
    ]
    assert check(github.replace("# Issue tracker: GitHub", "# Tracker")) == [
        "docs/agents/issue-tracker.md must select GitHub, GitLab, or Local Markdown"
    ]
    gitlab = (PACKAGE / "issue-tracker-gitlab.md").read_text(encoding="utf-8")
    assert check(gitlab.replace("body-links", "when-available", 1)) == [
        "docs/agents/issue-tracker.md must set Parent / child mode "
        "to one configured GitLab mode"
    ]


def test_domain_layout_is_selected_and_routes_to_its_owner() -> None:
    check = VALIDATOR["domain_layout_failures"]
    seed = (PACKAGE / "domain.md").read_text(encoding="utf-8")
    configured = seed.replace("<single-context | multi-context>", "single-context")

    assert check(configured) == []
    assert check(seed) == [
        "docs/agents/domain.md must set Configured layout to "
        "single-context or multi-context"
    ]
    assert check(configured.replace("$domain-modeling", "$model-domain")) == [
        "docs/agents/domain.md must point to $domain-modeling"
    ]
    assert check(
        configured.replace("$domain-modeling", "<!-- $domain-modeling -->")
    ) == ["docs/agents/domain.md must point to $domain-modeling"]


def test_label_seed_maps_required_active_roles() -> None:
    check = VALIDATOR["label_configuration_failures"]
    labels = (PACKAGE / "triage-labels.md").read_text(encoding="utf-8")

    assert check(labels) == []
    assert check(labels.replace("| `implemented` | `implemented` |", "")) == [
        "docs/agents/triage-labels.md is missing the implemented role"
    ]
    assert check(labels.replace("| `implemented` | `implemented` |", "| `implemented` |  |")) == [
        "docs/agents/triage-labels.md is missing the implemented role"
    ]


def test_git_root_check_accepts_only_the_repository_root() -> None:
    check = VALIDATOR["git_root_failures"]

    assert check(ROOT) == []
    assert check(ROOT / "skills") == ["Target must be the Git repository root"]


@pytest.mark.parametrize("domain_owner", ["domain-modeling", "shape-work"])
def test_legacy_repository_setup_remains_supported(
    tmp_path: Path, domain_owner: str,
) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".gitignore").write_text(".tmp/\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(
        "# Repository Instructions\n\n## Commands\n\n"
        "- Run tests: `python -m pytest`\n\n## Pointers\n\n"
        "- docs/agents/issue-tracker.md\n"
        "- docs/agents/triage-labels.md\n"
        "- docs/agents/domain.md\n"
        "- docs/agents/engineering-contract.md\n",
        encoding="utf-8",
    )
    guides = tmp_path / "docs/agents"
    guides.mkdir(parents=True)
    (guides / "issue-tracker.md").write_text(
        (PACKAGE / "issue-tracker-github.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (guides / "triage-labels.md").write_text(
        (PACKAGE / "triage-labels.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    domain = (PACKAGE / "domain.md").read_text(encoding="utf-8")
    (guides / "domain.md").write_text(
        domain.replace("<single-context | multi-context>", "single-context")
        .replace("$domain-modeling", f"${domain_owner}"),
        encoding="utf-8",
    )
    contract = guides / "engineering-contract.md"
    contract.write_text(
        "# Engineering contract\n\n## Local decisions\n\nPreserve ledger identities.\n",
        encoding="utf-8",
    )

    assert VALIDATOR["validate_setup"](
        tmp_path, repository_owned_contract=True, domain_owner=domain_owner,
    ) == []

    contract.unlink()
    assert VALIDATOR["validate_setup"](
        tmp_path, repository_owned_contract=True, domain_owner=domain_owner,
    ) == ["Missing required setup file: docs/agents/engineering-contract.md"]


def legacy_engineering_contract() -> str:
    """Materialize the legacy seed for tests of the custom pack's contract."""
    source = PACKAGE / "engineering-contract.md"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    marker = f"<!-- programming-agent-skills setup-file: engineering-contract.md:{digest} -->"
    return source.read_text(encoding="utf-8").replace(
        "# Engineering Contract\n", f"# Engineering Contract\n\n{marker}\n", 1
    )


def test_repo_bootstrap_validates_selected_domain_layout() -> None:
    def check(text):
        return VALIDATOR["domain_layout_failures"](text, domain_owner="shape-work")
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
    check = VALIDATOR["parallel_support_failures"]
    root = tmp_path / "repo"
    root.mkdir()

    assert check(root) == []

    config = root / VALIDATOR["PARALLEL_CONFIG"]
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


def test_portable_fallback_adoption_removes_the_portable_contract_owner() -> None:
    fallback = (ROOT / "AGENTS_PORTABLE_FALLBACK.md").read_text(encoding="utf-8")

    failures = VALIDATOR["portable_owner_failures"](fallback)
    assert len(failures) == 1
    assert "$repo-bootstrap" in failures[0]
    assert VALIDATOR["portable_owner_failures"](
        "# Repository Instructions\n\n## Skill Pack\n\nAGENTS primes.\n"
    ) == []
    marker = VALIDATOR["PORTABLE_OWNER_MARKER"]
    assert fallback.count(marker) == 1
    partial_adoption = fallback.replace("# Global Codex Instructions", "")
    assert VALIDATOR["portable_owner_failures"](partial_adoption) == failures
    reworded = fallback.replace(
        "Use this as your global `AGENTS.md` when the skill pack is not installed.",
        "This file supplies global engineering defaults without an installed pack.",
    )
    assert VALIDATOR["portable_owner_failures"](reworded) == failures
    assert VALIDATOR["portable_owner_failures"](
        fallback.replace(marker, "")
    ) == []


def test_agents_commands_require_one_unfenced_heading() -> None:
    valid_agents = (
        "# Repository Instructions\n\n"
        "Repository-specific guidance.\n\n"
        "## Commands\n\n- Test: `python -m pytest`\n"
    )
    command_failure = ["AGENTS.md must contain one unfenced ## Commands heading"]
    assert VALIDATOR["agents_commands_failures"](valid_agents) == []
    assert VALIDATOR["agents_commands_failures"](
        valid_agents.replace("## Commands", "## Local Commands")
    ) == command_failure
    assert VALIDATOR["agents_commands_failures"](
        valid_agents.replace("## Commands", "```text\n## Commands\n```")
    ) == command_failure
    assert VALIDATOR["agents_commands_failures"](
        valid_agents + "\n## Commands\n"
    ) == command_failure


def test_engineering_contract_validation_is_structural_and_causal() -> None:
    check = VALIDATOR["engineering_contract_failures"]
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
    marker = VALIDATOR["SETUP_FILE_MARKER_RE"].findall(contract)[0]
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
    pointers = VALIDATOR["AGENT_POINTERS"]
    reworded = "Read these owners when their contracts apply:\n" + "\n".join(
        f"- {pointer}" for pointer in pointers
    )
    assert VALIDATOR["agent_pointer_failures"](reworded) == []

    assert VALIDATOR["agent_pointer_failures"](
        reworded.replace("docs/agents/engineering-contract.md", "docs/engineering.md")
    ) == [
        "AGENTS.md is missing docs/agents/engineering-contract.md"
    ]
    commented = "\n".join(f"<!-- {pointer} -->" for pointer in pointers)
    assert VALIDATOR["agent_pointer_failures"](commented) == [
        f"AGENTS.md is missing {pointer}" for pointer in pointers
    ]
