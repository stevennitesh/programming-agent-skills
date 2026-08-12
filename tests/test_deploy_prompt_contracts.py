from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CONTEXT = ROOT / "CONTEXT.md"
ADR = ROOT / "docs/adr/0010-deploy-campaigns-advance-through-proof-gates.md"
DEPLOY = ROOT / "docs/synthesis/methods/deploy-prompts.md"
FRESH_EPOCH = ROOT / "docs/synthesis/methods/fresh-composition-epoch.md"
SYNTHESIS_README = ROOT / "docs/synthesis/README.md"
METHODS_README = ROOT / "docs/synthesis/methods/README.md"
BEHAVIOR_EVALS = (
    ROOT / "skills/custom/writing-great-skills/BEHAVIOR-EVALS.md"
)


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _section(text: str, heading: str, next_heading: str | None = None) -> str:
    section = text.split(heading, 1)[1]
    return section if next_heading is None else section.split(next_heading, 1)[0]


def test_active_method_exposes_one_controllerless_four_obligation_path() -> None:
    deploy = _normalized(DEPLOY)

    positions = [
        deploy.index(f"## {heading}")
        for heading in (
            "Contract Lock",
            "Candidate Lock",
            "Behavioral Proof",
            "Release",
        )
    ]
    assert positions == sorted(positions)
    assert "reasoning and proof obligations" in deploy
    assert "not persisted semantic lifecycle state" in deploy
    assert "controllerless" in deploy

    for active in (AGENTS, CONTEXT, ADR, SYNTHESIS_README, METHODS_README):
        text = _normalized(active)
        assert "Contract Lock" in text
        assert "Candidate Lock" in text
        assert "Behavioral Proof" in text
        assert "Release" in text


def test_dependency_ready_fce_slice_is_an_authorized_method_caller() -> None:
    deploy = _normalized(DEPLOY)
    fresh_epoch = _normalized(FRESH_EPOCH)

    assert (
        "For each dependency-ready node, issue its canonical immutable contract slice"
        in fresh_epoch
    )
    assert (
        "the one-skill method at `docs/synthesis/methods/deploy-prompts.md`"
        in fresh_epoch
    )
    assert "the user explicitly invokes `Run Deploy Campaign on <skill>`" in deploy
    assert (
        "a Fresh Composition Epoch issues a dependency-ready canonical contract slice"
        in deploy
    )
    assert "already-authorized epoch execution" in deploy


def test_candidate_lock_blocks_before_behavioral_dispatch_or_promotion() -> None:
    deploy = _normalized(DEPLOY)
    candidate = _section(deploy, "## Candidate Lock", "## Behavioral Proof")

    check_kinds = [
        candidate.index(kind)
        for kind in ("structural", "relationship", "compatibility", "integration")
    ]
    real_caller = candidate.index("checks at the real caller")
    failure = candidate.index("A failed applicable check stops the campaign")
    zero_dispatch = candidate.index("zero behavioral dispatch")
    zero_promotion = candidate.index("zero promotion")
    assert max(check_kinds) < real_caller < failure < zero_dispatch < zero_promotion
    assert "Freeze the exact candidate bytes" in candidate


def test_no_change_path_skips_optional_work() -> None:
    deploy = _normalized(DEPLOY)

    assert "deterministic/no-change" in deploy
    assert "zero research" in deploy
    assert "zero behavioral sampling" in deploy
    assert "zero pruning" in deploy
    assert "Return `no-change`" in deploy


def test_wording_claim_routes_to_existing_conditional_behavior_protocol() -> None:
    deploy = _normalized(DEPLOY)
    behavioral = _section(deploy, "## Behavioral Proof", "## Release")
    protocol = _normalized(BEHAVIOR_EVALS)

    assert (
        "skills/custom/writing-great-skills/BEHAVIOR-EVALS.md" in behavioral
    )
    for claim in (
        "wording",
        "invocation",
        "judgment",
        "action",
        "context loading",
        "Return",
        "completion",
    ):
        assert claim in behavioral
    assert "decision no weaker than the control" in behavioral
    assert "If the registered control deficit does not appear" in protocol
    assert "stop before candidate sampling" in protocol
    assert "Accept only when the control shows the registered deficit" in protocol


def test_release_binds_exact_tested_candidate_and_existing_authorities() -> None:
    deploy = _normalized(DEPLOY)
    release = _section(deploy, "## Release")

    for term in (
        "Promote only the exact Candidate Lock bytes",
        "cheap cut scan",
        "material cut",
        "installation authority",
        "Git delivery",
        "real disposable state",
    ):
        assert term in deploy or term in release


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
        "Deploy Prompt 1",
        "Deploy Research Pass",
        "Deploy Prompt 2",
        "Deploy Prompt 3",
        "Deploy Prompt 4",
        "Deploy Pruning Pass",
        "Deploy Prompt 5",
        "Deploy Prompt 6",
        "four-gate-shadow-v1",
        "deploy-campaign-manifest",
        "scripts.campaign_artifacts",
    ):
        assert legacy not in active_text
        assert legacy not in script_text
