from __future__ import annotations

import runpy
from pathlib import Path


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


def test_current_repository_setup_is_structurally_valid() -> None:
    assert VALIDATOR["validate_setup"](
        ROOT, repository_owned_contract=True, domain_owner="shape-work"
    ) == []
