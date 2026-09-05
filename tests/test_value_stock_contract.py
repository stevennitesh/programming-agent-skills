from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills/extra/value-stock"


def _links(path: Path) -> list[str]:
    return re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))


def test_value_stock_markdown_links_resolve() -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        for target in _links(path):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            assert (path.parent / relative).resolve().exists(), (path, target)
