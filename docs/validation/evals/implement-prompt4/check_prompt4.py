"""Deterministic Prompt 4 identity, invocation, context, and relationship checks."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts import skill_pack_contract as contract  # noqa: E402


PACKAGE = ROOT / "skills" / "experimental" / "implement"
M0 = PACKAGE / "controls" / "m0"


def check_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert text.count("```") % 2 == 0
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if "://" not in target:
            assert (path.parent / target).resolve().exists(), (path, target)
    rows = text.splitlines()
    for index, row in enumerate(rows):
        if re.match(r"^\|(?: *:?-+:? *\|)+$", row):
            width = row.count("|")
            assert rows[index - 1].count("|") == width
            cursor = index + 1
            while cursor < len(rows) and rows[cursor].startswith("|"):
                assert rows[cursor].count("|") == width
                cursor += 1


def main() -> None:
    manifest = json.loads(
        (PACKAGE / "evaluation-manifest.json").read_text(encoding="utf-8")
    )
    results = json.loads(
        (
            ROOT
            / "docs"
            / "validation"
            / "evals"
            / "implement-prompt4"
            / "results-manifest.json"
        ).read_text(encoding="utf-8")
    )
    root_skill = (PACKAGE / "SKILL.md").read_bytes()
    m0_skill = (M0 / "SKILL.md").read_bytes()
    root_metadata = (PACKAGE / "agents" / "openai.yaml").read_bytes()
    m0_metadata = (M0 / "agents" / "openai.yaml").read_bytes()
    text = root_skill.decode("utf-8")

    assert root_skill == m0_skill
    assert root_metadata == m0_metadata
    assert manifest["runtimes"]["m0"]["tree_sha256"] == contract.tree_hash(M0)
    assert manifest["runtimes"]["h1"]["tree_sha256"] == contract.tree_hash(
        PACKAGE,
        ignore=lambda path, _is_dir: path.name
        in {"controls", "evaluation-manifest.json"},
    )
    assert manifest["runtimes"]["h1"]["transformations"] == []
    assert results["v1"]["sha256"] == manifest["runtimes"]["m0"]["tree_sha256"]
    assert results["m0_viability"]["passes"] == 17
    assert all(
        cluster["decision"] == "rejected-no-control-deficit"
        and cluster["m0_samples"] >= 5
        and cluster["h1_samples"] == 0
        and len(cluster["families"]) >= 2
        for cluster in results["clusters"].values()
    )

    assert "allow_implicit_invocation: false" in root_metadata.decode("utf-8")
    assert "Use only when the user or a caller explicitly selects the item." in text
    for token in (
        "$repo-bootstrap",
        "$parallel-implement",
        "$review",
        "$convergent-pr-review",
        "$resolving-merge-conflicts",
        "$tdd",
        "$diagnosing-bugs",
        "Return unsettled source",
        "configured tracker",
    ):
        assert token in text
    for rejected in (
        "Hold one independently understandable",
        "classify each intended effect",
        "blind replay",
        "commit rollback",
        "staged worker",
        "two generations",
    ):
        assert rejected not in text

    assert text.count("```") % 2 == 0
    check_markdown(ROOT / "docs" / "synthesis" / "skills" / "implement.md")
    check_markdown(
        ROOT
        / "docs"
        / "validation"
        / "transcripts"
        / "2026-07-24-implement-prompt4.md"
    )
    print("Prompt 4 deterministic checks passed")


if __name__ == "__main__":
    main()
