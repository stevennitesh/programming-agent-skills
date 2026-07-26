from __future__ import annotations

import copy
from pathlib import Path
import subprocess

from scripts import fresh_epoch_contract, migration_ledger


def valid_control() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    public = {
        "format": 1,
        "fixed_point": {
            "source_head": "a" * 40,
            "public_inventory_fingerprint": "sha256-v1:" + "b" * 64,
            "private_inventory_fingerprint": "sha256-v1:" + "c" * 64,
        },
        "private_sidecar": {
            "path": ".tmp/fresh-composition-epoch/migration-ledger-private.json",
            "fingerprint": "sha256-v1:" + "d" * 64,
        },
        "rows": [
            {
                "migration_id": "MIG-0001",
                "source": {
                    "key": "docs/research/example.md",
                    "state": "tracked",
                    "fingerprint": "sha256-v1:" + "e" * 64,
                    "identity": None,
                },
                "artifact_class": "research",
                "inbound_references": [],
                "owner": "docs/research/README.md",
                "owner_gap": None,
                "migration_disposition": "move",
                "epoch_disposition": "historical-admission-only",
                "catalog_query_disposition": "unverified-gap",
                "proof_reuse_disposition": "missing",
                "target": {
                    "semantic_id": None,
                    "path": "docs/research/skills/example/<pending-id>.md",
                },
                "basis": ["topology-contract"],
                "reference_rewrite_set": [],
                "required_proof": ["target-read-back", "reference-reconciliation"],
                "observed_result": None,
                "status": "inventoried",
                "residual_risk": "target identity not minted",
                "recovery": {
                    "pointer": "git:a" * 20,
                    "applicable_lock": "FCE-pack-lock",
                },
            }
        ],
    }
    private = {
        "format": 1,
        "fixed_point": {"source_head": "a" * 40},
        "rows": [
            {
                "migration_id": "MIG-0002",
                "source": {
                    "key": ".tmp/private-evidence.bin",
                    "state": "private-ignored",
                    "fingerprint": "sha256-v1:" + "f" * 64,
                    "identity": None,
                },
                "artifact_class": "private-evidence",
                "inbound_references": [],
                "owner": "ignored-private-evidence",
                "owner_gap": None,
                "migration_disposition": "preserve-in-place",
                "epoch_disposition": "unverifiable",
                "catalog_query_disposition": "unverified-gap",
                "proof_reuse_disposition": "missing",
                "target": {"semantic_id": None, "path": None},
                "basis": ["private-boundary"],
                "reference_rewrite_set": [],
                "required_proof": ["privacy-boundary"],
                "observed_result": None,
                "status": "inventoried",
                "residual_risk": "private evidence remains local",
                "recovery": {
                    "pointer": ".tmp/private-evidence.bin",
                    "applicable_lock": None,
                },
            }
        ],
    }
    observed = {
        "current_head": "a" * 40,
        "public_inventory_fingerprint": "sha256-v1:" + "b" * 64,
        "private_inventory_fingerprint": "sha256-v1:" + "c" * 64,
        "public_source_keys": ["docs/research/example.md"],
        "private_source_keys": [".tmp/private-evidence.bin"],
    }
    return public, private, observed


def validate(
    public: dict[str, object],
    private: dict[str, object],
    observed: dict[str, object],
) -> list[str]:
    validator = getattr(
        fresh_epoch_contract,
        "validate_migration_control",
        None,
    )
    assert callable(validator), "fresh_epoch_contract must expose migration control"
    return validator(public, private, observed)


def test_migration_control_accepts_complete_fixed_point() -> None:
    public, private, observed = valid_control()

    assert validate(public, private, observed) == []


def test_migration_control_rejects_missing_duplicate_and_drift() -> None:
    public, private, observed = valid_control()
    observed["public_source_keys"] = [
        "docs/research/example.md",
        "docs/synthesis/missing.md",
    ]
    public["rows"].append(copy.deepcopy(public["rows"][0]))  # type: ignore[union-attr]
    public["fixed_point"]["public_inventory_fingerprint"] = (  # type: ignore[index]
        "sha256-v1:" + "9" * 64
    )

    failures = validate(public, private, observed)

    assert any("Duplicate migration source" in item for item in failures)
    assert any("Missing migration row" in item for item in failures)
    assert any("Fixed point drift" in item for item in failures)


def test_migration_control_allows_control_only_successor_head() -> None:
    public, private, observed = valid_control()
    observed["current_head"] = "9" * 40

    assert validate(public, private, observed) == []


def test_migration_check_survives_control_only_commit_and_rejects_source_drift(
    tmp_path: Path,
) -> None:
    research = tmp_path / "docs/research/example.md"
    research.parent.mkdir(parents=True)
    research.write_text("# Example\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Fixture\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "fixture@example.invalid"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Fixture"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "source fixed point"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    assert migration_ledger.freeze(tmp_path) == 0
    subprocess.run(
        ["git", "add", ".scratch/fresh-composition-epoch"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "add migration control"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    assert migration_ledger.check(tmp_path) == 0

    research.write_text("# Drifted\n", encoding="utf-8")

    assert migration_ledger.check(tmp_path) == 1


def test_migration_control_preserves_axes_privacy_and_lock_boundaries() -> None:
    public, private, observed = valid_control()
    row = public["rows"][0]  # type: ignore[index]
    del row["catalog_query_disposition"]
    row["status"] = "verified"
    row["observed_result"] = None
    row["recovery"]["applicable_lock"] = None
    public["rows"].append(copy.deepcopy(private["rows"][0]))  # type: ignore[union-attr]

    failures = validate(public, private, observed)

    assert any("distinct disposition axes" in item for item in failures)
    assert any("verified before proof" in item for item in failures)
    assert any("move/remove row requires an applicable Lock" in item for item in failures)
    assert any("Private inventory leaked into public ledger" in item for item in failures)


def test_migration_control_blocks_unreadable_identity_and_unsafe_removal() -> None:
    public, private, observed = valid_control()
    row = public["rows"][0]  # type: ignore[index]
    row["source"]["fingerprint"] = None
    row["source"]["identity"] = "inferred-from-name"
    row["status"] = "inventoried"
    row["migration_disposition"] = "remove"
    row["basis"] = ["old", "verbose", "low-link-count"]

    failures = validate(public, private, observed)

    assert any("Unreadable source must be blocked" in item for item in failures)
    assert any("identity must not be inferred" in item for item in failures)
    assert any("unsafe removal basis" in item for item in failures)


def test_migration_control_build_is_deterministic_and_keeps_private_paths_local(
    tmp_path: Path,
) -> None:
    public_path = tmp_path / "docs/research/example.md"
    public_path.parent.mkdir(parents=True)
    public_path.write_text("# Example\n", encoding="utf-8")
    referrer = tmp_path / "README.md"
    referrer.write_text("See `docs/research/example.md`.\n", encoding="utf-8")
    private_path = tmp_path / ".tmp/source-stack/private.txt"
    private_path.parent.mkdir(parents=True)
    private_path.write_text("secret source locator\n", encoding="utf-8")
    relative_referrer = tmp_path / "docs/research/related.md"
    relative_referrer.write_text(
        "[Example](example.md)\n",
        encoding="utf-8",
    )

    builder = getattr(
        fresh_epoch_contract,
        "build_migration_control",
        None,
    )
    assert callable(builder), "fresh_epoch_contract must build migration control"
    first_public, first_private, first_observed = builder(
        tmp_path,
        public_paths=["docs/research/example.md"],
        private_paths=[".tmp/source-stack"],
        reference_paths=["README.md", "docs/research/related.md"],
        head="1" * 40,
    )
    second_public, second_private, second_observed = builder(
        tmp_path,
        public_paths=["docs/research/example.md"],
        private_paths=[".tmp/source-stack"],
        reference_paths=["README.md", "docs/research/related.md"],
        head="1" * 40,
    )

    assert first_public == second_public
    assert first_private == second_private
    assert first_observed == second_observed
    assert first_public["rows"][0]["inbound_references"] == [
        "README.md",
        "docs/research/related.md",
    ]
    assert ".tmp/source-stack" not in repr(first_public)
    assert first_private["rows"][0]["source"]["key"] == ".tmp/source-stack"
    assert validate(first_public, first_private, first_observed) == []


def test_migration_control_propagates_campaign_identity_to_every_member(
    tmp_path: Path,
) -> None:
    campaign = tmp_path / "docs/validation/campaigns/alpha-2026-07-25"
    campaign.mkdir(parents=True)
    manifest = campaign / "manifest.json"
    manifest.write_text(
        '{"campaign":{"skill":"alpha","epoch":"2026-07-25"}}',
        encoding="utf-8",
    )
    decisions = campaign / "decisions.md"
    decisions.write_text("# Decisions\n", encoding="utf-8")
    builder = getattr(
        fresh_epoch_contract,
        "build_migration_control",
        None,
    )
    assert callable(builder)

    public, private, observed = builder(
        tmp_path,
        public_paths=[
            "docs/validation/campaigns/alpha-2026-07-25/decisions.md",
            "docs/validation/campaigns/alpha-2026-07-25/manifest.json",
        ],
        private_paths=[],
        reference_paths=[],
        head="1" * 40,
    )

    assert {
        row["source"]["identity"] for row in public["rows"]
    } == {"campaign:alpha:2026-07-25"}
    assert validate(public, private, observed) == []

    public["rows"][0]["source"]["identity"] = None
    assert any(
        "Campaign member has no applicable identity" in failure
        for failure in validate(public, private, observed)
    )
