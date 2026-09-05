from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CONTEXT = ROOT / "docs/agents/legacy-pack-context.md"
ADR = ROOT / "docs/adr/0010-deploy-campaigns-advance-through-proof-gates.md"
DEPLOY = ROOT / "docs/synthesis/methods/deploy-prompts.md"
SYNTHESIS_README = ROOT / "docs/synthesis/README.md"
METHODS_README = ROOT / "docs/synthesis/methods/README.md"


def test_legacy_campaign_runtime_is_not_discoverable() -> None:
    removed_paths = (
        ROOT / "scripts/campaign_artifacts.py",
        ROOT / "tests/test_campaign_artifacts.py",
        ROOT / "docs/validation/shared/schemas/deploy-campaign-manifest-v2.schema.json",
        ROOT / "docs/validation/shared/schemas/deploy-campaign-manifest-v3.schema.json",
        ROOT / "docs/validation/shared/fixtures/campaign-manifest-v1.json",
    )
    assert all(not path.exists() for path in removed_paths)

    active_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            AGENTS,
            CONTEXT,
            ADR,
            DEPLOY,
            SYNTHESIS_README,
            METHODS_README,
            ROOT / "docs/validation/shared/schemas/registry.json",
            ROOT / "docs/validation/shared/schemas/README.md",
            ROOT / "docs/validation/skills/README.md",
            ROOT / "skills/experimental/README.md",
        )
    )
    script_text = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "scripts").glob("*.py")
    )
    for legacy in (
        "four-gate-shadow-v1",
        "deploy-campaign-manifest",
        "scripts.campaign_artifacts",
    ):
        assert legacy not in active_text
        assert legacy not in script_text
