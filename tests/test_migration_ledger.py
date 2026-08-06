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




def test_git_recovery_uses_exact_raw_blob_when_checkout_filter_drifts(
    tmp_path: Path,
) -> None:
    relative = "docs/validation/evals/example/live/index.html"
    content = b"<html>\n<body>fixture</body>\n</html>\n"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_bytes(content)
    head = _commit_fixture(tmp_path)
    row = {
        "recovery": {
            "pointer": (
                f"git:{head}:{relative}@"
                f"{migration_ledger._fingerprint(content)}"
            )
        }
    }

    assert migration_ledger._git_recovery_bytes(tmp_path, row) == content






















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


def _research_synthesis_migration_fixture(
    tmp_path: Path,
) -> tuple[list[dict[str, object]], bytes]:
    source_key = "docs/research/implement-2026-07-24.md"
    source = tmp_path / source_key
    source.parent.mkdir(parents=True)
    source.write_text(
        "# Implement research\n\n"
        "[Language](language/03-high-signal-steering-words.md)\n",
        encoding="utf-8",
    )
    revision = tmp_path / "docs/research/implement-2026-07-24-r2.md"
    revision.write_text(
        "# Implement research r2\n\n"
        "Prior: `docs/research/implement-2026-07-24.md`\n",
        encoding="utf-8",
    )
    language = (
        tmp_path
        / "docs/research/language/03-high-signal-steering-words.md"
    )
    language.parent.mkdir(parents=True)
    language.write_text("# Language\n", encoding="utf-8")
    (language.parent / "README.md").write_text(
        "# Language research\n",
        encoding="utf-8",
    )
    research_readme = tmp_path / "docs/research/README.md"
    research_readme.write_text("# Research\n", encoding="utf-8")
    synthesis_readme = tmp_path / "docs/synthesis/README.md"
    synthesis_readme.parent.mkdir(parents=True)
    synthesis_readme.write_text("# Synthesis\n", encoding="utf-8")
    reference = tmp_path / "docs/synthesis/skills/implement.md"
    reference.parent.mkdir(parents=True)
    reference.write_text(
        "# Implement\n\n"
        "[Research](../../research/implement-2026-07-24.md)\n",
        encoding="utf-8",
    )
    owner = tmp_path / "docs/research/skills/implement/README.md"
    owner.parent.mkdir(parents=True)
    owner.write_text(
        "# Implement research packets\n\n"
        "- [RP-implement-20260724-01]"
        "(RP-implement-20260724-01.md): historical\n"
        "- [RP-implement-20260724-02]"
        "(RP-implement-20260724-02.md): historical\n",
        encoding="utf-8",
    )
    original = source.read_bytes()
    head = _commit_fixture(tmp_path)
    public, _, _ = fresh_epoch_contract.build_migration_control(
        tmp_path,
        public_paths=[
            source_key,
            "docs/research/implement-2026-07-24-r2.md",
            "docs/research/language/03-high-signal-steering-words.md",
            "docs/synthesis/README.md",
            "docs/synthesis/skills/implement.md",
        ],
        private_paths=[],
        reference_paths=[
            source_key,
            "docs/research/implement-2026-07-24-r2.md",
            "docs/research/language/03-high-signal-steering-words.md",
            "docs/synthesis/README.md",
            "docs/synthesis/skills/implement.md",
        ],
        head=head,
        head_paths={
            source_key,
            "docs/research/implement-2026-07-24-r2.md",
            "docs/research/language/03-high-signal-steering-words.md",
            "docs/synthesis/README.md",
            "docs/synthesis/skills/implement.md",
        },
    )
    return public["rows"], original


def test_research_synthesis_plan_settles_moves_and_preserved_owners(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)

    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    by_source = {row["source"]["key"]: row for row in prepared}

    moved = by_source["docs/research/implement-2026-07-24.md"]
    assert moved["migration_disposition"] == "move"
    assert moved["owner"] == "docs/research/skills/implement/README.md"
    assert moved["target"] == {
        "semantic_id": "RP-implement-20260724-01",
        "path": (
            "docs/research/skills/implement/"
            "RP-implement-20260724-01.md"
        ),
    }
    assert moved["status"] == "prepared"

    preserved = by_source["docs/synthesis/README.md"]
    assert preserved["migration_disposition"] == "preserve-in-place"
    assert preserved["owner"] == "docs/synthesis/README.md"
    assert preserved["status"] == "prepared"


def test_research_synthesis_group_moves_rebases_and_verifies(
    tmp_path: Path,
) -> None:
    rows, original = _research_synthesis_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)

    applied = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )
    target = (
        tmp_path
        / "docs/research/skills/implement/RP-implement-20260724-01.md"
    )
    reference = tmp_path / "docs/synthesis/skills/implement.md"

    assert not (tmp_path / "docs/research/implement-2026-07-24.md").exists()
    assert target.is_file()
    assert "artifact_id: RP-implement-20260724-01" in target.read_text("utf-8")
    assert (
        "../../language/03-high-signal-steering-words.md"
        in target.read_text("utf-8")
    )
    assert (
        "../../research/skills/implement/RP-implement-20260724-01.md"
        in reference.read_text("utf-8")
    )

    verified = migration_ledger.verify_research_synthesis_migrations(
        tmp_path,
        applied,
    )

    assert all(row["status"] == "verified" for row in verified)
    assert all(row["observed_result"]["passed"] is True for row in verified)

    rolled_back = migration_ledger.rollback_research_synthesis_migrations(
        tmp_path,
        verified,
    )

    assert (
        tmp_path / "docs/research/implement-2026-07-24.md"
    ).read_bytes() == original
    assert not target.exists()
    assert (
        "../../research/implement-2026-07-24.md"
        in reference.read_text("utf-8")
    )
    assert all(row["status"] == "prepared" for row in rolled_back)


def test_research_synthesis_verification_rejects_broken_moved_link(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    applied = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )
    language = (
        tmp_path
        / "docs/research/language/03-high-signal-steering-words.md"
    )
    language.unlink()
    applied = [
        row
        for row in applied
        if row["source"]["key"]
        != "docs/research/language/03-high-signal-steering-words.md"
    ]

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="moved Markdown link is unresolved",
    ):
        migration_ledger.verify_research_synthesis_migrations(
            tmp_path,
            applied,
        )


def test_research_synthesis_plan_records_specific_preserved_owners(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)

    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    by_source = {row["source"]["key"]: row for row in prepared}

    assert by_source[
        "docs/research/language/03-high-signal-steering-words.md"
    ]["owner"] == "docs/research/language/README.md"
    assert by_source["docs/synthesis/skills/implement.md"]["owner"] == (
        "docs/synthesis/skills/implement.md"
    )


def test_research_synthesis_group_retry_is_idempotent(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    first = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )
    target = (
        tmp_path
        / "docs/research/skills/implement/RP-implement-20260724-01.md"
    )
    first_bytes = target.read_bytes()

    second = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )

    assert target.read_bytes() == first_bytes
    assert next(
        row
        for row in second
        if row["source"]["key"]
        == "docs/research/implement-2026-07-24.md"
    )["status"] == "references-reconciled"


def test_research_synthesis_rollback_rejects_target_collision(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    applied = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )
    target = (
        tmp_path
        / "docs/research/skills/implement/RP-implement-20260724-01.md"
    )
    target.write_text("# Intervening edit\n", encoding="utf-8")

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="rollback target collision",
    ):
        migration_ledger.rollback_research_synthesis_migrations(
            tmp_path,
            applied,
        )

    assert target.read_text("utf-8") == "# Intervening edit\n"
    assert not (tmp_path / "docs/research/implement-2026-07-24.md").exists()


def test_research_synthesis_rollback_rejects_source_collision(
    tmp_path: Path,
) -> None:
    rows, _ = _research_synthesis_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_research_synthesis_migrations(rows)
    applied = migration_ledger.apply_research_synthesis_migrations(
        tmp_path,
        prepared,
    )
    source = tmp_path / "docs/research/implement-2026-07-24.md"
    source.write_text("# Independent recreation\n", encoding="utf-8")

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="rollback source collision",
    ):
        migration_ledger.rollback_research_synthesis_migrations(
            tmp_path,
            applied,
        )

    assert source.read_text("utf-8") == "# Independent recreation\n"












def _validation_row(
    source_key: str,
    *,
    artifact_class: str,
    migration_id: str,
) -> dict[str, object]:
    return {
        "migration_id": migration_id,
        "source": {
            "key": source_key,
            "state": "tracked",
            "fingerprint": "sha256-v1:" + "a" * 64,
            "identity": None,
        },
        "artifact_class": artifact_class,
        "inbound_references": ["docs/validation/README.md"],
        "owner": None,
        "owner_gap": "Validation owner is not yet proved.",
        "migration_disposition": "owner-gap",
        "epoch_disposition": "historical-admission-only",
        "catalog_query_disposition": "unverified-gap",
        "proof_reuse_disposition": "missing",
        "target": {"semantic_id": None, "path": None},
        "basis": ["issue-34-owner-gap-rule"],
        "reference_rewrite_set": [],
        "required_proof": ["fixed-point-identity"],
        "observed_result": None,
        "status": "inventoried",
        "residual_risk": "owner is unsettled",
        "recovery": {
            "pointer": (
                "git:" + "b" * 40 + f":{source_key}@"
                + "sha256-v1:"
                + "a" * 64
            ),
            "applicable_lock": None,
        },
    }


def test_prepare_validation_migrations_assigns_eval_and_transcript_owners() -> None:
    eval_row = _validation_row(
        (
            "docs/validation/evals/convergent-pr-review-2026-07-24/"
            "campaign-decision.json"
        ),
        artifact_class="evaluation",
        migration_id="MIG-0169",
    )
    transcript_row = _validation_row(
        (
            "docs/validation/transcripts/"
            "2026-07-23-research-behavior-eval.md"
        ),
        artifact_class="validation-transcript",
        migration_id="MIG-0292",
    )

    prepared = migration_ledger.prepare_validation_migrations(
        [eval_row, transcript_row]
    )

    assert prepared[0]["owner"] == (
        "docs/validation/skills/convergent-pr-review/README.md"
    )
    assert prepared[0]["target"] == {
        "semantic_id": "EV-convergent-pr-review-prompt4-20260724-01",
        "path": (
            "docs/validation/skills/convergent-pr-review/evals/"
            "EV-convergent-pr-review-prompt4-20260724-01/"
            "campaign-decision.json"
        ),
    }
    assert prepared[1]["owner"] == (
        "docs/validation/skills/research/README.md"
    )
    assert prepared[1]["target"] == {
        "semantic_id": "EV-research-behavior-eval-20260723-01",
        "path": (
            "docs/validation/skills/research/evals/"
            "EV-research-behavior-eval-20260723-01/evidence/"
            "2026-07-23-research-behavior-eval.md"
        ),
    }


def test_prepare_validation_migrations_keeps_ambiguous_pack_evidence_explicit() -> None:
    row = _validation_row(
        (
            "docs/validation/transcripts/"
            "2026-07-13-whole-pack-workflow-traces.md"
        ),
        artifact_class="validation-transcript",
        migration_id="MIG-0248",
    )

    prepared = migration_ledger.prepare_validation_migrations([row])

    assert prepared[0]["migration_disposition"] == "owner-gap"
    assert prepared[0]["status"] == "blocked"
    assert prepared[0]["owner"] == "docs/validation/skill-pack/README.md"
    assert prepared[0]["target"] == {"semantic_id": None, "path": None}


def test_prepare_validation_migrations_verifies_settled_shared_inputs() -> None:
    row = _validation_row(
        "docs/validation/shared/schemas/registry.json",
        artifact_class="validation",
        migration_id="MIG-0241",
    )

    prepared = migration_ledger.prepare_validation_migrations([row])

    assert prepared[0]["migration_disposition"] == "preserve-in-place"
    assert prepared[0]["owner"] == "docs/validation/shared/schemas/README.md"
    assert prepared[0]["status"] == "prepared"


def _validation_migration_fixture(
    root: Path,
) -> tuple[list[dict[str, object]], bytes]:
    source = (
        root
        / "docs/validation/evals/convergent-pr-review-2026-07-24/"
        "campaign-decision.json"
    )
    owner = root / "docs/validation/skills/convergent-pr-review/README.md"
    reference = root / "docs/synthesis/skills/convergent-pr-review.md"
    source.parent.mkdir(parents=True)
    owner.parent.mkdir(parents=True)
    reference.parent.mkdir(parents=True)
    original = (
        b'{\n  "decision": "historical",\n'
        b'  "path": "docs/validation/evals/'
        b'convergent-pr-review-2026-07-24/campaign-decision.json"\n}\n'
    ).replace(b"\n", b"\r\n")
    source.write_bytes(original)
    owner.write_text(
        "# Convergent PR Review validation\n\n"
        "Evaluation directories are named by stable `EV-...` identity.\n",
        encoding="utf-8",
    )
    reference.write_text(
        "[Decision](../../validation/evals/"
        "convergent-pr-review-2026-07-24/campaign-decision.json)\n",
        encoding="utf-8",
    )
    head = _commit_fixture(root)
    row = _validation_row(
        (
            "docs/validation/evals/convergent-pr-review-2026-07-24/"
            "campaign-decision.json"
        ),
        artifact_class="evaluation",
        migration_id="MIG-0169",
    )
    row["source"]["fingerprint"] = migration_ledger._fingerprint(original)
    row["inbound_references"] = [
        "docs/synthesis/skills/convergent-pr-review.md"
    ]
    row["recovery"] = {
        "pointer": (
            f"git:{head}:{row['source']['key']}@"
            f"{row['source']['fingerprint']}"
        ),
        "applicable_lock": None,
    }
    return [row], original


def test_validation_migration_is_recoverable_retry_safe_and_verified(
    tmp_path: Path,
) -> None:
    rows, original = _validation_migration_fixture(tmp_path)
    prepared = migration_ledger.prepare_validation_migrations(rows)

    applied = migration_ledger.apply_validation_migrations(tmp_path, prepared)
    retried = migration_ledger.apply_validation_migrations(tmp_path, applied)
    verified = migration_ledger.verify_validation_migrations(tmp_path, retried)

    target = (
        tmp_path
        / "docs/validation/skills/convergent-pr-review/evals/"
        "EV-convergent-pr-review-prompt4-20260724-01/"
        "campaign-decision.json"
    )
    assert not (
        tmp_path
        / "docs/validation/evals/convergent-pr-review-2026-07-24/"
        "campaign-decision.json"
    ).exists()
    assert b"EV-convergent-pr-review-prompt4-20260724-01" in (
        target.parent.as_posix().encode()
    )
    assert target.read_bytes() != original
    assert verified[0]["status"] == "verified"
    assert verified[0]["observed_result"]["rollback_proved"] is False
    assert (
        "../../validation/skills/convergent-pr-review/evals/"
        "EV-convergent-pr-review-prompt4-20260724-01/"
        "campaign-decision.json"
    ) in (
        tmp_path / "docs/synthesis/skills/convergent-pr-review.md"
    ).read_text("utf-8")

    rolled_back = migration_ledger.rollback_validation_migrations(
        tmp_path, verified
    )
    assert rolled_back[0]["status"] == "prepared"
    assert (
        tmp_path
        / "docs/validation/evals/convergent-pr-review-2026-07-24/"
        "campaign-decision.json"
    ).read_bytes() == original
    assert not target.exists()

    reprepared = migration_ledger.prepare_validation_migrations(rolled_back)
    assert reprepared[0]["observed_result"]["rollback_proved"] is True
    reapplied = migration_ledger.apply_validation_migrations(
        tmp_path, reprepared
    )
    reverified = migration_ledger.verify_validation_migrations(
        tmp_path, reapplied
    )
    assert reverified[0]["observed_result"]["rollback_proved"] is True


def test_validation_target_preserves_plain_historical_locators(
    tmp_path: Path,
) -> None:
    source_key = (
        "docs/validation/transcripts/"
        "2026-07-23-research-behavior-eval.md"
    )
    row = _validation_row(
        source_key,
        artifact_class="validation-transcript",
        migration_id="MIG-0292",
    )
    prepared = migration_ledger.prepare_validation_migrations([row])
    target = prepared[0]["target"]
    target_key = target["path"]
    identity = target["semantic_id"]
    original = (
        f"Historical locator remained `{source_key}` and was hashed as raw.\n"
    ).encode()

    rewritten = migration_ledger._validation_target_bytes(
        tmp_path,
        original,
        source_key=source_key,
        target_key=target_key,
        target_identity=identity,
        moved_targets={source_key: target_key},
        mapped=migration_ledger._validation_mapping(prepared),
    )

    assert source_key.encode() in rewritten
    assert target_key.encode() not in rewritten


def test_validation_target_rewrites_structured_directory_pointer(
    tmp_path: Path,
) -> None:
    source_key = (
        "docs/validation/evals/convergent-pr-review-2026-07-24/"
        "campaign-decision.json"
    )
    old_fixtures = (
        "docs/validation/evals/convergent-pr-review-2026-07-24/fixtures"
    )
    row = _validation_row(
        source_key,
        artifact_class="evaluation",
        migration_id="MIG-0169",
    )
    prepared = migration_ledger.prepare_validation_migrations([row])
    target = prepared[0]["target"]
    target_key = target["path"]
    identity = target["semantic_id"]
    mapped = migration_ledger._validation_mapping(prepared)

    rewritten = migration_ledger._validation_target_bytes(
        tmp_path,
        json.dumps({"fixtures": old_fixtures}).encode(),
        source_key=source_key,
        target_key=target_key,
        target_identity=identity,
        moved_targets={source_key: target_key},
        mapped=mapped,
    )

    payload = json.loads(rewritten)
    assert payload["fixtures"] == (
        "docs/validation/skills/convergent-pr-review/evals/"
        "EV-convergent-pr-review-prompt4-20260724-01/fixtures"
    )


def test_validation_target_marks_local_only_link_without_live_pointer(
    tmp_path: Path,
) -> None:
    source_key = (
        "docs/validation/evals/"
        "parallel-implement-prompt4-r2/results.md"
    )
    row = _validation_row(
        source_key,
        artifact_class="evaluation",
        migration_id="MIG-0190",
    )
    prepared = migration_ledger.prepare_validation_migrations([row])
    target = prepared[0]["target"]
    target_key = target["path"]

    rewritten = migration_ledger._validation_target_bytes(
        tmp_path,
        b"The raw captures are in [`raw/`](raw/).\n",
        source_key=source_key,
        target_key=target_key,
        target_identity=target["semantic_id"],
        moved_targets={source_key: target_key},
        mapped=migration_ledger._validation_mapping(prepared),
    )

    assert rewritten == (
        b"The raw captures are in "
        b"`raw/` (retained as unverifiable local residue; "
        b"not tracked proof).\n"
    )


def test_validation_target_redacts_private_residue_label(
    tmp_path: Path,
) -> None:
    source_key = (
        "docs/validation/transcripts/"
        "2026-07-21-research-extraction-pruning-evidence.md"
    )
    row = _validation_row(
        source_key,
        artifact_class="validation-transcript",
        migration_id="MIG-0271",
    )
    prepared = migration_ledger.prepare_validation_migrations([row])
    target = prepared[0]["target"]
    private_locator = "PRIVATE-RESIDUE-LOCATOR"
    original = (
        f"Frozen at [`{private_locator}`]"
        "(../evals/research-pruning-pre-prune/).\n"
    ).encode()

    rewritten = migration_ledger._validation_target_bytes(
        tmp_path,
        original,
        source_key=source_key,
        target_key=target["path"],
        target_identity=target["semantic_id"],
        moved_targets={source_key: target["path"]},
        mapped=migration_ledger._validation_mapping(prepared),
    )

    assert private_locator.encode() not in rewritten
    assert rewritten == (
        b"Frozen at `pre-prune residue` "
        b"(retained as unverifiable local residue; not tracked proof).\n"
    )


def test_validation_target_records_missing_structured_reference_gap(
    tmp_path: Path,
) -> None:
    source_key = (
        "docs/validation/evals/"
        "parallel-implement-prompt4-r2/protocol-manifest.json"
    )
    row = _validation_row(
        source_key,
        artifact_class="evaluation",
        migration_id="MIG-0188",
    )
    prepared = migration_ledger.prepare_validation_migrations([row])
    target = prepared[0]["target"]
    target_key = target["path"]
    original = {
        "protected": {
            "preserved_surfaces": [
                "docs/validation/evals/parallel-implement-prompt4/**"
            ]
        },
        "affected_surfaces": [
            (
                "docs/validation/transcripts/"
                "2026-07-24-parallel-implement-prompt3-construction-r2.md"
            )
        ],
        "evidence_dispositions": {},
    }

    rewritten = migration_ledger._validation_target_bytes(
        tmp_path,
        json.dumps(original).encode(),
        source_key=source_key,
        target_key=target_key,
        target_identity=target["semantic_id"],
        moved_targets={source_key: target_key},
        mapped=migration_ledger._validation_mapping(prepared),
    )

    payload = json.loads(rewritten)
    assert payload["protected"]["preserved_surfaces"] == [
        (
            "docs/validation/skills/parallel-implement/evals/"
            "EV-parallel-implement-prompt4-r2-20260724-01/**"
        )
    ]
    assert payload["evidence_dispositions"][
        "prompt3_construction_transcript"
    ].startswith("blocked-reference-gap;")


def test_mapped_destination_rebases_a_moved_directory() -> None:
    old_root = "docs/validation/evals/to-tickets/isolation-v2"
    new_root = (
        "docs/validation/skills/to-tickets/evals/"
        "EV-to-tickets-prompt4/isolation-v2"
    )
    moved = {
        f"{old_root}/README.md": f"{new_root}/README.md",
        f"{old_root}/results.md": f"{new_root}/results.md",
    }

    assert migration_ledger._mapped_destination(old_root, moved) == new_root


def test_markdown_link_verification_rejects_moved_source_residue(
    tmp_path: Path,
) -> None:
    markdown = tmp_path / "docs/validation/skills/example/evidence.md"
    residue = tmp_path / "docs/validation/evals/example/fixtures"
    markdown.parent.mkdir(parents=True)
    residue.mkdir(parents=True)
    (residue / "ignored.json").write_text("{}\n", encoding="utf-8")
    markdown.write_text(
        "[fixtures](../../evals/example/fixtures)\n",
        encoding="utf-8",
    )

    with pytest.raises(
        migration_ledger.MigrationBlocked,
        match="moved Markdown link targets legacy residue",
    ):
        migration_ledger._verify_markdown_links(
            tmp_path,
            markdown,
            "docs/validation/skills/example/evidence.md",
            forbidden_paths={
                "docs/validation/evals/example/fixtures/ignored.json"
            },
        )


def test_proof_comparison_allows_later_support_snapshot_evolution() -> None:
    original = {
        "target_fingerprint": "sha256-v1:" + "a" * 64,
        "references_verified": True,
        "support_fingerprints": {
            "docs/validation/README.md": {
                "before": "sha256-v1:" + "b" * 64,
                "after": "sha256-v1:" + "c" * 64,
            }
        },
    }
    current = {
        **original,
        "support_fingerprints": {
            "docs/validation/README.md": {
                "before": "sha256-v1:" + "c" * 64,
                "after": "sha256-v1:" + "d" * 64,
            }
        },
    }

    assert migration_ledger._row_local_proof(current) == (
        migration_ledger._row_local_proof(original)
    )
    assert migration_ledger._row_local_proof(
        {**current, "references_verified": False}
    ) != migration_ledger._row_local_proof(original)


def _private_migration_row(
    relative: str,
    *,
    state: str,
    fingerprint: str,
    migration_id: str,
) -> dict[str, object]:
    return {
        "migration_id": migration_id,
        "source": {
            "key": relative,
            "state": state,
            "fingerprint": fingerprint,
            "identity": None,
        },
        "artifact_class": (
            "local-residue" if state == "local-residue" else "private-evidence"
        ),
        "inbound_references": [],
        "owner": (
            "local-residue-cleanup"
            if state == "local-residue"
            else "ignored-private-evidence"
        ),
        "owner_gap": None,
        "migration_disposition": (
            "remove" if state == "local-residue" else "preserve-in-place"
        ),
        "epoch_disposition": "unverifiable",
        "catalog_query_disposition": "unverified-gap",
        "proof_reuse_disposition": "missing",
        "target": {"semantic_id": None, "path": None},
        "basis": ["private-boundary"],
        "reference_rewrite_set": [],
        "required_proof": ["fixed-point-identity"],
        "observed_result": None,
        "status": "inventoried",
        "residual_risk": "pending",
        "recovery": {
            "pointer": relative,
            "applicable_lock": (
                "authorized-cleanup-lock"
                if state == "local-residue"
                else None
            ),
        },
    }


def test_private_rows_become_verified_or_explicitly_blocked(
    tmp_path: Path,
) -> None:
    evidence = tmp_path / ".tmp/private/evidence.txt"
    residue = tmp_path / ".tmp/private/empty"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("private evidence\n", encoding="utf-8")
    residue.mkdir(parents=True)
    rows = [
        _private_migration_row(
            ".tmp/private/evidence.txt",
            state="private-ignored",
            fingerprint=fresh_epoch_contract._path_fingerprint(evidence),
            migration_id="MIG-0480",
        ),
        _private_migration_row(
            ".tmp/private/empty",
            state="local-residue",
            fingerprint=fresh_epoch_contract._path_fingerprint(residue),
            migration_id="MIG-0503",
        ),
    ]

    terminal = migration_ledger.terminalize_private_rows(tmp_path, rows)

    assert terminal[0]["status"] == "verified"
    assert terminal[0]["observed_result"]["passed"] is True
    assert terminal[1]["status"] == "blocked"
    assert terminal[1]["owner_gap"] == (
        "Cleanup is Lock-gated; local residue is not a Git artifact."
    )
    assert terminal[1]["observed_result"]["passed"] is False
    assert migration_ledger.terminalize_private_rows(
        tmp_path, terminal
    ) == terminal


def test_private_terminal_verification_rejects_evidence_drift_without_locator(
    tmp_path: Path,
) -> None:
    evidence = tmp_path / ".tmp/private/evidence.txt"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("private evidence\n", encoding="utf-8")
    row = _private_migration_row(
        ".tmp/private/evidence.txt",
        state="private-ignored",
        fingerprint=fresh_epoch_contract._path_fingerprint(evidence),
        migration_id="MIG-0480",
    )
    terminal = migration_ledger.terminalize_private_rows(tmp_path, [row])
    evidence.write_text("drift\n", encoding="utf-8")

    assert migration_ledger._verify_private_terminal_rows(
        tmp_path, terminal
    ) == ["Private migration proof drift: MIG-0480"]


def test_private_terminal_verification_rejects_residue_drift_and_deletion(
    tmp_path: Path,
) -> None:
    residue = tmp_path / ".tmp/private/empty"
    residue.mkdir(parents=True)
    row = _private_migration_row(
        ".tmp/private/empty",
        state="local-residue",
        fingerprint=fresh_epoch_contract._path_fingerprint(residue),
        migration_id="MIG-0503",
    )
    terminal = migration_ledger.terminalize_private_rows(tmp_path, [row])

    assert migration_ledger._verify_private_terminal_rows(
        tmp_path, terminal
    ) == []
    (residue / "unexpected.txt").write_text("drift\n", encoding="utf-8")
    assert migration_ledger._verify_private_terminal_rows(
        tmp_path, terminal
    ) == ["Private residue proof drift: MIG-0503"]
    (residue / "unexpected.txt").unlink()
    residue.rmdir()
    assert migration_ledger._verify_private_terminal_rows(
        tmp_path, terminal
    ) == ["Private residue proof drift: MIG-0503"]


def test_local_only_link_rules_do_not_publish_private_absolute_keys() -> None:
    for link_rules in migration_ledger.VALIDATION_LOCAL_ONLY_LINKS.values():
        assert all(
            not locator.startswith(("docs/", ".tmp/"))
            for locator in link_rules
        )
        assert all("docs/" not in note for note in link_rules.values())
