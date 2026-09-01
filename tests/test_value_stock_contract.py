from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/extra/value-stock"
SKILL = SKILL_ROOT / "SKILL.md"
RUNBOOK = SKILL_ROOT / "references/analyst-runbook.md"
MARKET_CONTEXT = SKILL_ROOT / "references/market-context.md"
SOURCE_PROTOCOL = SKILL_ROOT / "references/source-protocol.md"
VALUATION_METHODS = SKILL_ROOT / "references/valuation-methods.md"
BANK_RI = SKILL_ROOT / "references/bank-residual-income.md"


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
    assert "Return the strongest actively assembled report" in skill
    assert "If the selected intrinsic path is failed or unsupported" in skill
    assert (
        "A passed calculator receipt closes only its mechanical calculation branch"
        in normalized
    )
    assert "assemble the active report" in normalized


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


def test_value_stock_semantic_support_and_causal_range_contract() -> None:
    source = " ".join(SOURCE_PROTOCOL.read_text(encoding="utf-8").split())
    methods = " ".join(VALUATION_METHODS.read_text(encoding="utf-8").split())

    for claim in (
        "zero",
        "absence",
        "source classification",
        "balancing residuals",
    ):
        assert claim in source
    assert "intended use" in source
    assert "mechanically passed parameter bundle" in methods
    assert "company-specific cause" in methods
    assert "inspectable transmission" in methods


def test_value_stock_pinned_jpm_false_complete_evaluation() -> None:
    bank = " ".join(BANK_RI.read_text(encoding="utf-8").split())

    assert (
        "pinned false-complete JPM pattern remains `partial` or `blocked`" in bank
    )
    for missing_support in (
        "timing",
        "normalization",
        "share coverage",
        "cost of equity",
        "forecast foundation",
        "preserved market artifacts",
        "peer roles",
        "adequacy",
        "industry-universe support",
    ):
        assert missing_support in bank
    assert "even if its calculators pass" in bank
    assert "requires passed report assembly" in bank


def test_value_stock_nonblocking_not_comparable_evaluation() -> None:
    market = " ".join(MARKET_CONTEXT.read_text(encoding="utf-8").split())
    bank = " ".join(BANK_RI.read_text(encoding="utf-8").split())

    assert "correct `not_comparable` disposition is nonblocking" in market
    assert (
        "Broad-market P/E may correctly be nonblocking `not_comparable`" in bank
    )
    assert (
        "Allow correct `not_applicable` and nonblocking `not_comparable` lanes "
        "without forcing `partial`" in bank
    )
    assert "supplies no bank P/TBV ratio or fabricated membership evidence" in bank


def test_value_stock_markdown_links_resolve() -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        for target in _links(path):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            assert (path.parent / relative).resolve().exists(), (path, target)
