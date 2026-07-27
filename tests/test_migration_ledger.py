from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess

import pytest

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


def test_staged_new_file_never_claims_recovery_from_absent_head(
    tmp_path: Path,
) -> None:
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
    relative = "docs/validation/new-schema.json"
    added = tmp_path / relative
    added.parent.mkdir(parents=True)
    added.write_text("{}\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Changed\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", relative, "README.md"],
        cwd=tmp_path,
        check=True,
    )

    assert migration_ledger.freeze(tmp_path) == 0
    ledger = json.loads(
        (tmp_path / migration_ledger.PUBLIC_LEDGER).read_text("utf-8")
    )
    row = next(item for item in ledger["rows"] if item["source"]["key"] == relative)
    changed_row = next(
        item for item in ledger["rows"] if item["source"]["key"] == "README.md"
    )

    assert row["source"]["state"] == "tracked"
    assert row["recovery"]["pointer"] == relative
    assert changed_row["recovery"]["pointer"] == "README.md"


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


CATALOG_SOURCE = (
    "docs/research/skill-pack-composition/catalog-contract-research.md"
)
CATALOG_TARGET = (
    "docs/research/skill-pack-composition/sources/SRC-0001.md"
)


def _commit_fixture(root: Path) -> str:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "fixture@example.invalid"],
        cwd=root,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Fixture"],
        cwd=root,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(
        ["git", "commit", "-m", "migration source"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _catalog_migration_fixture(
    tmp_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    source = tmp_path / CATALOG_SOURCE
    source.parent.mkdir(parents=True)
    source.write_text(
        "# Catalog contract\n\n"
        f"Canonical note: `{CATALOG_SOURCE}`.\n",
        encoding="utf-8",
    )
    owner = tmp_path / "docs/research/skill-pack-composition/sources/README.md"
    owner.parent.mkdir(parents=True)
    owner.write_text("# Public source packets\n", encoding="utf-8")
    head = _commit_fixture(tmp_path)
    public, _, _ = fresh_epoch_contract.build_migration_control(
        tmp_path,
        public_paths=[
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        ],
        private_paths=[],
        reference_paths=[CATALOG_SOURCE],
        head=head,
        head_paths={
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        },
    )
    row = next(
        item
        for item in public["rows"]
        if item["source"]["key"] == CATALOG_SOURCE
    )
    return public, row


def test_catalog_note_plan_freezes_exact_public_source_migration(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)

    assert row["migration_disposition"] == "move"
    assert row["owner"] == (
        "docs/research/skill-pack-composition/sources/README.md"
    )
    assert row["target"] == {
        "semantic_id": "SRC-0001",
        "path": CATALOG_TARGET,
    }
    assert row["reference_rewrite_set"] == [CATALOG_SOURCE]
    assert row["status"] == "inventoried"


def test_catalog_migration_retries_partial_state_and_rolls_back(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    source = tmp_path / CATALOG_SOURCE
    target = tmp_path / CATALOG_TARGET
    original = source.read_bytes()

    target.write_bytes(original)
    source.unlink()
    applied = migration_ledger.apply_migration(tmp_path, row)

    assert not source.exists()
    assert target.is_file()
    assert CATALOG_SOURCE not in target.read_text(encoding="utf-8")
    assert CATALOG_TARGET in target.read_text(encoding="utf-8")
    assert applied["status"] == "references-reconciled"
    assert applied["observed_result"]["moved_fingerprint"] == (
        fresh_epoch_contract.exact_content_fingerprint(original)
    )

    rolled_back = migration_ledger.rollback_migration(tmp_path, applied)

    assert source.read_bytes() == original
    assert not target.exists()
    assert rolled_back["status"] == "prepared"

    reapplied = migration_ledger.apply_migration(tmp_path, rolled_back)

    assert reapplied["observed_result"]["rollback_proved"] is True


def test_catalog_migration_reconciles_exact_duplicate_target(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    source = tmp_path / CATALOG_SOURCE
    target = tmp_path / CATALOG_TARGET
    target.write_bytes(source.read_bytes())

    applied = migration_ledger.apply_migration(tmp_path, row)

    assert not source.exists()
    assert target.is_file()
    assert applied["observed_result"]["exact_target_reconciled"] is True


def test_catalog_migration_collision_preserves_both_files(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    source = tmp_path / CATALOG_SOURCE
    target = tmp_path / CATALOG_TARGET
    target.write_text("# Different packet\n", encoding="utf-8")
    source_before = source.read_bytes()
    target_before = target.read_bytes()

    with pytest.raises(migration_ledger.MigrationBlocked, match="collision"):
        migration_ledger.apply_migration(tmp_path, row)

    assert source.read_bytes() == source_before
    assert target.read_bytes() == target_before


def test_catalog_migration_rolls_back_after_reference_failure(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    source = tmp_path / CATALOG_SOURCE
    target = tmp_path / CATALOG_TARGET
    original = source.read_bytes()
    row["reference_rewrite_set"] = [
        CATALOG_SOURCE,
        "docs/research/missing-reference.md",
    ]

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="declared reference is absent",
    ):
        migration_ledger.apply_migration(tmp_path, row)

    assert source.read_bytes() == original
    assert not target.exists()


def test_catalog_migration_verifies_normalized_target_and_old_path_scan(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)

    applied = migration_ledger.apply_migration(tmp_path, row)
    verified = migration_ledger.verify_migration(tmp_path, applied)

    assert verified["status"] == "verified"
    assert verified["observed_result"]["passed"] is True
    assert verified["observed_result"]["source_absent"] is True
    assert verified["observed_result"]["target_identity"] == "SRC-0001"


def test_catalog_migration_verification_rejects_unexplained_old_path(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    applied = migration_ledger.apply_migration(tmp_path, row)
    stray = tmp_path / "README.md"
    stray.write_text(f"See `{CATALOG_SOURCE}`.\n", encoding="utf-8")

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="unexplained old-path reference",
    ):
        migration_ledger.verify_migration(tmp_path, applied)


def test_migration_check_accepts_one_verified_path_replacement(
    tmp_path: Path,
) -> None:
    public, row = _catalog_migration_fixture(tmp_path)
    _, private, _ = fresh_epoch_contract.build_migration_control(
        tmp_path,
        public_paths=[
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        ],
        private_paths=[],
        reference_paths=[CATALOG_SOURCE],
        head=public["fixed_point"]["source_head"],
        head_paths={
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        },
    )
    applied = migration_ledger.apply_migration(tmp_path, row)
    public["rows"] = [
        applied if item["migration_id"] == row["migration_id"] else item
        for item in public["rows"]
    ]
    ledger_path = tmp_path / migration_ledger.PUBLIC_LEDGER
    sidecar_path = tmp_path / migration_ledger.PRIVATE_LEDGER
    ledger_path.parent.mkdir(parents=True)
    sidecar_path.parent.mkdir(parents=True)
    ledger_path.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sidecar_path.write_text(
        json.dumps(private, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    verified = migration_ledger.verify_migration(tmp_path, applied)
    public["rows"] = [
        verified if item["migration_id"] == row["migration_id"] else item
        for item in public["rows"]
    ]
    ledger_path.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (tmp_path / migration_ledger.CLOSEOUT).write_bytes(
        migration_ledger._closeout(public, private).encode("utf-8"),
    )

    assert migration_ledger.check(tmp_path) == 0


def test_catalog_migration_resumes_after_normalization_before_ledger_write(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    first = migration_ledger.apply_migration(tmp_path, row)

    resumed = migration_ledger.apply_migration(tmp_path, row)

    assert resumed["status"] == "references-reconciled"
    assert resumed["observed_result"]["target_fingerprint"] == (
        first["observed_result"]["target_fingerprint"]
    )


def test_catalog_rollback_resumes_after_source_restore(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    source = tmp_path / CATALOG_SOURCE
    original = source.read_bytes()
    migration_ledger.apply_migration(tmp_path, row)
    source.write_bytes(original)

    rolled_back = migration_ledger.rollback_migration(tmp_path, row)

    assert source.read_bytes() == original
    assert not (tmp_path / CATALOG_TARGET).exists()
    assert rolled_back["observed_result"]["rollback_proved"] is True


def test_catalog_verification_rejects_semantic_body_replacement(
    tmp_path: Path,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    applied = migration_ledger.apply_migration(tmp_path, row)
    target = tmp_path / CATALOG_TARGET
    target.write_text(
        target.read_text(encoding="utf-8").replace(
            "# Catalog contract",
            "# Unrelated replacement",
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="allowed source normalization",
    ):
        migration_ledger.verify_migration(tmp_path, applied)


def test_catalog_verification_blocks_unreadable_inventory_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, row = _catalog_migration_fixture(tmp_path)
    applied = migration_ledger.apply_migration(tmp_path, row)
    unreadable = tmp_path / "README.md"
    unreadable.write_text("# Inventory\n", encoding="utf-8")
    real_read_bytes = Path.read_bytes

    def read_bytes(path: Path) -> bytes:
        if path.resolve() == unreadable.resolve():
            raise OSError("locked fixture")
        return real_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", read_bytes)

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="cannot complete old-path scan",
    ):
        migration_ledger.verify_migration(tmp_path, applied)


def test_operate_reconciles_ledger_closeout_interruption(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    public, row = _catalog_migration_fixture(tmp_path)
    _, private, _ = fresh_epoch_contract.build_migration_control(
        tmp_path,
        public_paths=[
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        ],
        private_paths=[],
        reference_paths=[CATALOG_SOURCE],
        head=public["fixed_point"]["source_head"],
        head_paths={
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        },
    )
    applied = migration_ledger.apply_migration(tmp_path, row)
    public["rows"] = [
        applied if item["migration_id"] == row["migration_id"] else item
        for item in public["rows"]
    ]
    ledger_path = tmp_path / migration_ledger.PUBLIC_LEDGER
    sidecar_path = tmp_path / migration_ledger.PRIVATE_LEDGER
    closeout_path = tmp_path / migration_ledger.CLOSEOUT
    ledger_path.parent.mkdir(parents=True)
    sidecar_path.parent.mkdir(parents=True)
    ledger_path.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sidecar_path.write_text(
        json.dumps(private, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    closeout_path.write_bytes(
        migration_ledger._closeout(public, private).encode("utf-8"),
    )
    verified = migration_ledger.verify_migration(tmp_path, applied)
    public["rows"] = [
        verified if item["migration_id"] == row["migration_id"] else item
        for item in public["rows"]
    ]

    # Simulate process termination after the ledger replacement but before
    # the closeout replacement.
    ledger_path.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    assert migration_ledger.check(tmp_path) == 1
    assert "Migration closeout differs" in capsys.readouterr().out
    assert migration_ledger.operate(
        tmp_path,
        action="verify",
        migration_id=str(row["migration_id"]),
    ) == 0
    assert migration_ledger.check(tmp_path) == 0


def test_operate_preflights_private_control_before_filesystem_mutation(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    public, row = _catalog_migration_fixture(tmp_path)
    _, private, _ = fresh_epoch_contract.build_migration_control(
        tmp_path,
        public_paths=[
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        ],
        private_paths=[],
        reference_paths=[CATALOG_SOURCE],
        head=public["fixed_point"]["source_head"],
        head_paths={
            CATALOG_SOURCE,
            "docs/research/skill-pack-composition/sources/README.md",
        },
    )
    ledger_path = tmp_path / migration_ledger.PUBLIC_LEDGER
    sidecar_path = tmp_path / migration_ledger.PRIVATE_LEDGER
    closeout_path = tmp_path / migration_ledger.CLOSEOUT
    ledger_path.parent.mkdir(parents=True)
    sidecar_path.parent.mkdir(parents=True)
    ledger_path.write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    sidecar_path.write_bytes(b"{truncated")
    closeout_path.write_bytes(
        migration_ledger._closeout(public, private).encode("utf-8"),
    )
    source = tmp_path / CATALOG_SOURCE
    target = tmp_path / CATALOG_TARGET
    original_source = source.read_bytes()
    original_ledger = ledger_path.read_bytes()
    original_sidecar = sidecar_path.read_bytes()
    original_closeout = closeout_path.read_bytes()

    assert migration_ledger.operate(
        tmp_path,
        action="migrate",
        migration_id=str(row["migration_id"]),
    ) == 1

    assert "Cannot read migration control" in capsys.readouterr().out
    assert source.read_bytes() == original_source
    assert not target.exists()
    assert ledger_path.read_bytes() == original_ledger
    assert sidecar_path.read_bytes() == original_sidecar
    assert closeout_path.read_bytes() == original_closeout
