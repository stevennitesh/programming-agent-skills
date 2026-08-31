from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/extra/value-stock"
SKILL = SKILL_ROOT / "SKILL.md"
RUNBOOK = SKILL_ROOT / "references/analyst-runbook.md"
MARKET_CONTEXT = SKILL_ROOT / "references/market-context.md"


def _links(path: Path) -> list[str]:
    return re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))


def test_value_stock_common_path_is_small_and_ordered() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    normalized = " ".join(skill.split())

    assert len(skill.split()) <= 1_050
    assert len(runbook.splitlines()) <= 200
    for step in range(1, 8):
        assert f"{step}. " in skill
    assert "Evidence Pack owns sourced facts" in normalized
    assert "Model Lock owns the calculation inputs" in normalized
    assert "mechanical_status: pass" in skill
    assert "Use verdict mode by default" in skill


def test_value_stock_uses_only_repository_owned_calculation() -> None:
    package_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILL_ROOT.rglob("*.md")
    )

    assert "Do not use a separate skill-bundled calculator" in package_text
    assert "stockval value <model-lock.json>" in package_text
    assert "stockval audit <run-dir>" in package_text
    assert not (SKILL_ROOT / "scripts/valuation_gateway.py").exists()
    assert not (SKILL_ROOT / "references/model-lock-v1.schema.json").exists()
    assert not (SKILL_ROOT / "examples").exists()


def test_value_stock_market_context_preserves_required_lanes_and_safe_failure() -> None:
    market = MARKET_CONTEXT.read_text(encoding="utf-8")
    for lane in (
        "own_history",
        "competitive_peers",
        "economic_peers",
        "industry",
        "broad_market",
    ):
        assert f"`{lane}`" in market
    assert "Select one primary relative metric" in market
    assert "Freeze selection before outcomes" in market
    assert "Do not substitute manual" in market
    assert "Never average intrinsic and relative values" in market


def test_value_stock_markdown_links_resolve() -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        for target in _links(path):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            assert (path.parent / relative).resolve().exists(), (path, target)
