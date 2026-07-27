from __future__ import annotations

import importlib
import json
import os
from copy import deepcopy
from pathlib import Path

import pytest

from scripts import campaign_artifacts, install_skills, pack_contract


def pack_integration():
    return importlib.import_module("scripts.pack_integration")


def test_create_manifest_is_mechanical_only() -> None:
    manifest = pack_integration().create_manifest()

    assert manifest == {
        "schema_version": 1,
        "identities": {
            "composition_epoch_id": None,
            "contract": None,
            "installed_pack": None,
            "relationship_index": None,
            "relationship_projection": [],
            "campaigns": [],
        },
        "registrations": [],
        "receipts": [],
        "invalidations": [],
        "parity": {
            "contract_campaigns_installed": "pending",
            "relationship_index": "pending",
        },
    }
    assert not (
        {
            "acceptance",
            "decision",
            "lock",
            "repair",
            "rubric_score",
            "schedule",
        }
        & set(manifest)
    )


def registrations() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for number in range(1, 11):
        rows.append(
            {
                "id": f"gate-{number:02d}-structural",
                "gate_id": f"G{number:02d}",
                "claim_class": "structural",
                "check_profile": f"gate-g{number:02d}-v1",
                "inputs": [],
                "result": {
                    "path": f"results/gate-{number:02d}.json",
                    "fingerprint": "sha256-v1:" + str(number % 10) * 64,
                },
            }
        )
    rows.append(
        {
            "id": "gate-10-behavioral",
            "gate_id": "G10",
            "claim_class": "behavioral",
            "check_profile": "behavioral-evidence-v1",
            "inputs": [],
            "result": {
                "path": "results/gate-10-behavioral.json",
                "fingerprint": "sha256-v1:" + "b" * 64,
            },
            "preregistration": {
                "protocol": {
                    "path": "protocol.md",
                    "fingerprint": "sha256-v1:" + "c" * 64,
                },
                "rubric": {
                    "path": "rubric.md",
                    "fingerprint": "sha256-v1:" + "d" * 64,
                },
                "fixtures": [
                    {
                        "path": "fixtures/cases.json",
                        "fingerprint": "sha256-v1:" + "e" * 64,
                    }
                ],
                "controls": ["no-guidance", "nearest-negative"],
                "repetitions": 3,
                "variance": {
                    "measure": "rubric-total",
                    "reported": True,
                    "worst_case_reported": True,
                },
                "environment_bounds": {
                    "path": "bounds.json",
                    "fingerprint": "sha256-v1:" + "f" * 64,
                },
            },
        }
    )
    return rows


def test_manifest_schema_and_coverage_enforce_the_judgment_firewall() -> None:
    module = pack_integration()
    manifest = module.create_manifest()
    manifest["registrations"] = registrations()

    assert module.validate_manifest_shape(manifest) == []
    coverage = module.derive_coverage(manifest["registrations"])
    assert coverage["status"] == "complete"
    assert [row["gate_id"] for row in coverage["gates"]] == [
        f"G{number:02d}" for number in range(1, 11)
    ]
    assert coverage["gates"][-1]["claim_classes"] == [
        "behavioral",
        "structural",
    ]

    forbidden = deepcopy(manifest)
    forbidden["acceptance"] = "integration-accepted"
    assert any(
        "Additional properties" in failure
        for failure in module.validate_manifest_shape(forbidden)
    )


def test_behavioral_registration_requires_controls_repetition_variance_and_bounds() -> None:
    module = pack_integration()
    baseline = registrations()
    for field in ("controls", "repetitions", "variance", "environment_bounds"):
        invalid = deepcopy(baseline)
        invalid[-1]["preregistration"].pop(field)
        coverage = module.derive_coverage(invalid)
        assert coverage["status"] == "blocked"
        assert any("G10" in failure for failure in coverage["failures"])


def test_no_semantic_workflow_operation_is_exposed() -> None:
    module = pack_integration()
    parser = module.build_parser()
    help_text = parser.format_help().casefold()

    for operation in ("accept", "lock", "repair", "schedule", "score", "start"):
        assert operation not in help_text


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def pointer(path: Path, root: Path) -> dict[str, str]:
    return {
        "path": path.relative_to(root).as_posix(),
        "fingerprint": pack_integration().file_fingerprint(path),
    }


def integration_fixture(root: Path) -> Path:
    contract = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "docs/validation/shared/fixtures/"
            "pack-composition-contract-v1/contract.json"
        ).read_text(encoding="utf-8")
    )
    contract["epoch_header"]["status"] = "campaign-active"
    contract["selected_skills"][0]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": "fixture-leaf-campaign",
        "terminal_evidence_pointer": (
            "docs/validation/skills/fixture-leaf/campaigns/"
            "fixture-leaf-campaign/manifest.json"
        ),
    }
    contract_path = root / "docs/synthesis/skill-pack.md"
    contract_path.parent.mkdir(parents=True)
    contract_path.write_text(
        pack_contract.render_contract(contract),
        encoding="utf-8",
        newline="\n",
    )
    contract_fingerprint = pack_contract.semantic_fingerprint(
        contract_path.read_text(encoding="utf-8")
    )

    canonical = root / "skills/custom/fixture-leaf"
    installed = root / "installed/fixture-leaf"
    canonical.mkdir(parents=True)
    installed.mkdir(parents=True)
    (canonical / "SKILL.md").write_text("# Fixture leaf\n", encoding="utf-8")
    (installed / "SKILL.md").write_text("# Fixture leaf\n", encoding="utf-8")
    p1_fingerprint = (
        "sha256-v1:" + install_skills.skill_tree_hash(canonical)
    )

    relationship_index = root / "docs/synthesis/skill-context-relationships.md"
    relationship_index.write_text("# Relationships\n", encoding="utf-8")
    installed_manifest = root / "installed/.programming-agent-skills-manifest.json"
    write_json(
        installed_manifest,
        {
            "format": 1,
            "source": "skills/custom",
            "skills": ["fixture-leaf"],
            "hashes": {
                "fixture-leaf": install_skills.skill_tree_hash(installed)
            },
        },
    )
    campaign_path = (
        root
        / "docs/validation/skills/fixture-leaf/campaigns/"
        "fixture-leaf-campaign/manifest.json"
    )
    admission = pack_contract.campaign_admission_slice(
        contract,
        "SK-001",
        allow_terminal_projection=True,
    )
    admission_slice = admission["slice"]
    campaign = {
        "schema_version": 2,
        "campaign": {
            "id": "fixture-leaf-campaign",
            "skill": "fixture-leaf",
            "epoch": "fixture-leaf-campaign",
            "composition_epoch_id": "FCE-20990101-01",
            "delivery_mode": "none",
            "continuation": None,
            "supersession": None,
            "worktree": str(root.resolve()),
        },
        "contract": {
            "pack_contract": {
                "path": "docs/synthesis/skill-pack.md",
                "revision": "1",
                "fingerprint": contract_fingerprint,
            },
            "slice": {
                "id": admission_slice["slice_id"],
                "path": "slice.json",
                "fingerprint": admission["slice_fingerprint"],
            },
            "selected_capability_ids": admission_slice[
                "selected_capability_ids"
            ],
            "selected_relationship_ids": admission_slice[
                "selected_relationship_ids"
            ],
            "selected_scenario_ids": admission_slice[
                "selected_scenario_ids"
            ],
            "proof_predecessors": admission_slice[
                "hard_proof_predecessor_ids"
            ],
            "schedule_pointer": "schedule.json#SK-001",
            "schedule_fingerprint": "sha256-v1:" + "4" * 64,
        },
        "semantic": {
            "stage_token": "prompt-5",
            "terminal_token": "campaign-complete",
            "lifecycle": deepcopy(campaign_artifacts.FRESH_TERMINAL_LIFECYCLE),
            "pointers": {
                "decision_capsule": "decisions.md#prompt-5",
                "m0_checkpoint": "docs/validation/skills/fixture-leaf/m0.md",
                "research_packet": "research.md",
                "skill_synthesis": "synthesis.md",
                "claim_adjacency": "synthesis.md#claims",
                "pack_synthesis": "docs/synthesis/skill-pack.md",
            },
        },
        "mechanical": {
            "created_at": "2099-01-01T00:00:00Z",
            "campaign_digest": "5" * 64,
            "supersession_digest": None,
            "contract_digest": "6" * 64,
            "verified_at": "2099-01-01T00:00:00Z",
            "artifact_identities": [
                {"name": "canonical-p1", "fingerprint": p1_fingerprint},
                {"name": "installed-p1", "fingerprint": p1_fingerprint},
            ],
            "proof_registrations": [{"id": "prompt-5-proof"}],
            "preflight_registrations": [
                {"kind": "installation", "state": "post-install"}
            ],
            "receipts": [],
            "invalidations": [],
            "parity": {
                "canonical_installed": "match",
                "relationship_ids": [],
            },
            "evidence_state": "current",
        },
    }
    campaign["mechanical"]["campaign_digest"] = (
        campaign_artifacts._campaign_lineage_digest(  # noqa: SLF001
            campaign["campaign"],
            None,
        )
    )
    campaign["mechanical"]["contract_digest"] = (
        campaign_artifacts._canonical_json_sha256(  # noqa: SLF001
            campaign["contract"]
        )
    )
    write_json(campaign_path, campaign)

    result_root = root / "docs/validation/skill-pack/FCE-20990101-01"
    rows = registrations()
    for row in rows:
        result_path = result_root / str(row["result"]["path"])
        outcome = (
            "evidence-recorded"
            if row["claim_class"] == "behavioral"
            else "pass"
        )
        write_json(
            result_path,
            {
                "schema_version": 1,
                "registration_id": row["id"],
                "claim_class": row["claim_class"],
                "outcome": outcome,
                "observations": [{"sample_count": 3}],
            },
        )
        row["result"] = pointer(result_path, root)
        if row["claim_class"] == "behavioral":
            preregistration = row["preregistration"]
            for name in ("protocol", "rubric"):
                target = result_root / str(preregistration[name]["path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"# {name.title()}\n", encoding="utf-8")
                preregistration[name] = pointer(target, root)
            target = result_root / str(preregistration["fixtures"][0]["path"])
            write_json(target, {"cases": []})
            preregistration["fixtures"] = [pointer(target, root)]
            target = result_root / str(preregistration["environment_bounds"]["path"])
            write_json(
                target,
                {
                    "model": "fixture-model",
                    "host": "fixture-host",
                    "configuration": "fixture-config",
                    "tools": ["fixture-tool"],
                },
            )
            preregistration["environment_bounds"] = pointer(target, root)

    installed_identity = pack_integration().installed_pack_fingerprint(
        root / "installed",
        [{"skill_id": "SK-001", "canonical_name": "fixture-leaf"}],
    )
    manifest = pack_integration().create_manifest()
    manifest["identities"] = {
        "composition_epoch_id": "FCE-20990101-01",
        "contract": {
            **pointer(contract_path, root),
            "semantic_fingerprint": contract_fingerprint,
            "revision": 1,
        },
        "installed_pack": {
            "fingerprint": installed_identity,
            "manifest_fingerprint": pack_integration().file_fingerprint(
                installed_manifest
            ),
        },
        "relationship_index": pointer(relationship_index, root),
        "relationship_projection": [],
        "campaigns": [
            {
                "skill_id": "SK-001",
                "canonical_name": "fixture-leaf",
                "campaign_id": "fixture-leaf-campaign",
                "manifest": pointer(campaign_path, root),
                "contract_revision": 1,
                "slice_fingerprint": admission["slice_fingerprint"],
                "canonical_p1_fingerprint": p1_fingerprint,
                "installed_p1_fingerprint": p1_fingerprint,
            }
        ],
    }
    manifest["registrations"] = rows
    manifest_path = result_root / "integration-manifest.json"
    write_json(manifest_path, manifest)
    return manifest_path


def rewrite_candidate_contract(
    root: Path,
    manifest_path: Path,
    mutate,
) -> None:
    module = pack_integration()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    contract_pointer = manifest["identities"]["contract"]
    contract_path = root / contract_pointer["path"]
    contract = pack_contract.parse_contract(
        contract_path.read_text(encoding="utf-8")
    )
    mutate(contract)
    contract_path.write_text(
        pack_contract.render_contract(contract),
        encoding="utf-8",
        newline="\n",
    )
    semantic = pack_contract.semantic_fingerprint(
        contract_path.read_text(encoding="utf-8")
    )
    contract_pointer["fingerprint"] = module.file_fingerprint(contract_path)
    contract_pointer["semantic_fingerprint"] = semantic
    campaign_row = manifest["identities"]["campaigns"][0]
    campaign_path = root / campaign_row["manifest"]["path"]
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    admission = pack_contract.campaign_admission_slice(
        contract,
        "SK-001",
        allow_terminal_projection=True,
    )
    envelope = admission["slice"]
    campaign["contract"]["pack_contract"]["fingerprint"] = semantic
    campaign["contract"]["slice"]["id"] = envelope["slice_id"]
    campaign["contract"]["slice"]["fingerprint"] = admission[
        "slice_fingerprint"
    ]
    campaign["contract"]["selected_capability_ids"] = envelope[
        "selected_capability_ids"
    ]
    campaign["contract"]["selected_relationship_ids"] = envelope[
        "selected_relationship_ids"
    ]
    campaign["contract"]["selected_scenario_ids"] = envelope[
        "selected_scenario_ids"
    ]
    campaign["contract"]["proof_predecessors"] = envelope[
        "hard_proof_predecessor_ids"
    ]
    campaign["mechanical"]["contract_digest"] = (
        campaign_artifacts._canonical_json_sha256(  # noqa: SLF001
            campaign["contract"]
        )
    )
    write_json(campaign_path, campaign)
    campaign_row["manifest"]["fingerprint"] = module.file_fingerprint(
        campaign_path
    )
    campaign_row["slice_fingerprint"] = admission["slice_fingerprint"]
    write_json(manifest_path, manifest)


def test_verify_binds_contract_campaign_install_and_ten_gate_evidence(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    contract_path = tmp_path / "docs/synthesis/skill-pack.md"
    contract_before = contract_path.read_bytes()

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "verified"
    assert result["evidence_class"] == "mechanical-only"
    assert len(result["coverage"]) == 10
    assert result["parity"] == {
        "contract_campaigns_installed": "match",
        "relationship_index": "match",
    }
    assert contract_path.read_bytes() == contract_before
    assert not (
        {"acceptance", "decision", "lock", "repair", "score"} & set(result)
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest["receipts"]) == 11

    reused = module.verify_integration(manifest_path, worktree=tmp_path)
    assert reused["status"] == "verified"
    assert len(json.loads(manifest_path.read_text(encoding="utf-8"))["receipts"]) == 11

    result_path = manifest_path.parent / "results.json"
    cli_result = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
        result_path=result_path,
    )
    assert cli_result["status"] == "verified"
    assert module.validate_result_shape(
        json.loads(result_path.read_text(encoding="utf-8"))
    ) == []


def test_stale_result_invalidates_only_its_exact_receipt_and_restores(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(manifest_path, worktree=tmp_path)["status"] == (
        "verified"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    target_registration = manifest["registrations"][0]
    target = tmp_path / target_registration["result"]["path"]
    original = target.read_bytes()
    target.write_bytes(original + b" ")

    stale = module.verify_integration(manifest_path, worktree=tmp_path)

    assert stale["status"] == "stale"
    assert stale["owner"] == "fresh-composition-epoch"
    assert stale["invalidated_receipt_ids"] == [
        next(
            receipt["id"]
            for receipt in manifest["receipts"]
            if receipt["registration_id"] == target_registration["id"]
        )
    ]
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(after["invalidations"]) == 1
    assert len(after["invalidations"][0]["receipt_ids"]) == 1

    target.write_bytes(original)
    restored = module.verify_integration(manifest_path, worktree=tmp_path)
    assert restored["status"] == "verified"


def test_mixed_revision_and_installed_identity_block_without_acceptance(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["identities"]["campaigns"][0]["contract_revision"] = 2
    write_json(manifest_path, manifest)

    mixed = module.verify_integration(manifest_path, worktree=tmp_path)

    assert mixed["status"] == "blocked"
    assert mixed["owner"] == "fresh-composition-epoch"
    assert "acceptance" not in mixed
    manifest["identities"]["campaigns"][0]["contract_revision"] = 1
    write_json(manifest_path, manifest)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"

    manifest_path = integration_fixture(tmp_path / "installed-drift")
    installed_skill = tmp_path / "installed-drift/installed/fixture-leaf/SKILL.md"
    installed_skill.write_text("# drift\n", encoding="utf-8")
    drift = module.verify_integration(
        manifest_path,
        worktree=tmp_path / "installed-drift",
    )
    assert drift["status"] == "blocked"
    assert any("installed" in failure["message"] for failure in drift["failures"])
    installed_skill.write_text("# Fixture leaf\n", encoding="utf-8")
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path / "installed-drift",
    )["status"] == "verified"


def test_failed_registered_check_returns_evidence_without_repair(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["epoch_header"].__setitem__(
            "exclusions",
            [],
        ),
    )

    failed = module.verify_integration(manifest_path, worktree=tmp_path)

    assert failed["status"] == "failed"
    assert failed["owner"] == "fresh-composition-epoch"
    assert not ({"repair", "schedule", "acceptance", "lock"} & set(failed))
    persisted = json.loads(manifest_path.read_text(encoding="utf-8"))
    failure_receipt = next(
        receipt
        for receipt in persisted["receipts"]
        if receipt["registration_id"] == "gate-06-structural"
    )
    assert failure_receipt["outcome"] == "fail"
    assert failure_receipt["observations"] == [
        {"check": "context-budget-and-exclusions", "passed": False}
    ]
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["epoch_header"].__setitem__(
            "exclusions",
            ["Automated semantic acceptance"],
        ),
    )
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"


def test_malformed_behavioral_result_and_owner_path_fail_cleanly_then_restore(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    registration = manifest["registrations"][-1]
    result_path = tmp_path / registration["result"]["path"]
    original = result_path.read_bytes()
    result_path.write_text("{", encoding="utf-8")
    registration["result"] = pointer(result_path, tmp_path)
    write_json(manifest_path, manifest)

    malformed = module.verify_integration(manifest_path, worktree=tmp_path)
    assert malformed["status"] == "failed"
    assert malformed["failures"][0]["code"] == "behavioral-result"

    result_path.write_bytes(original)
    registration["result"] = pointer(result_path, tmp_path)
    write_json(manifest_path, manifest)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"

    foreign_manifest = tmp_path / "integration-manifest.json"
    foreign_manifest.write_bytes(manifest_path.read_bytes())
    blocked = module.verify_integration(foreign_manifest, worktree=tmp_path)
    assert blocked["status"] == "blocked"
    assert blocked["failures"][0]["code"] == "manifest-owner"

    blocked = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
        result_path=tmp_path / "docs/synthesis/results.json",
    )
    assert blocked["status"] == "blocked"
    assert blocked["failures"][0]["code"] == "result-owner"


def test_duplicate_registration_does_not_create_false_coverage() -> None:
    rows = registrations()
    rows[1]["id"] = rows[0]["id"]

    coverage = pack_integration().derive_coverage(rows)

    assert coverage["status"] == "blocked"
    assert any("duplicate" in failure for failure in coverage["failures"])


def test_all_ten_named_gates_are_exposed() -> None:
    coverage = pack_integration().derive_coverage(registrations())

    assert {
        row["gate_id"]: row["name"] for row in coverage["gates"]
    } == pack_integration().GATES


def test_rubric_is_registered_but_never_interpreted(tmp_path: Path) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    behavioral = manifest["registrations"][-1]
    rubric_path = tmp_path / behavioral["preregistration"]["rubric"]["path"]
    rubric_path.write_bytes(b"\xff\x00not-a-rubric")
    behavioral["preregistration"]["rubric"] = pointer(rubric_path, tmp_path)
    write_json(manifest_path, manifest)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "verified"


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("registration_id", "wrong-registration"),
        ("claim_class", "structural"),
        ("observations", []),
    ],
)
def test_behavioral_result_envelope_is_exact_without_scoring(
    tmp_path: Path,
    field: str,
    replacement: object,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    behavioral = manifest["registrations"][-1]
    result_path = tmp_path / behavioral["result"]["path"]
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    payload[field] = replacement
    write_json(result_path, payload)
    behavioral["result"] = pointer(result_path, tmp_path)
    write_json(manifest_path, manifest)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "failed"
    assert result["failures"][0]["code"] == "behavioral-result"


def test_check_profile_must_match_claim_class() -> None:
    rows = registrations()
    rows[-1]["check_profile"] = "gate-g10-v1"

    coverage = pack_integration().derive_coverage(rows)

    assert coverage["status"] == "blocked"
    assert any("check profile" in failure for failure in coverage["failures"])


def test_no_write_suppresses_manifest_and_result_writes(tmp_path: Path) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    before = manifest_path.read_bytes()
    result_path = manifest_path.parent / "results.json"

    result = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
        result_path=result_path,
        no_write=True,
    )

    assert result["status"] == "verified"
    assert manifest_path.read_bytes() == before
    assert not result_path.exists()


def test_hand_authored_pass_cannot_override_gate_owned_profile(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    registration = manifest["registrations"][5]
    result_path = tmp_path / registration["result"]["path"]
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result["outcome"] = "pass"
    write_json(result_path, result)
    registration["result"] = pointer(result_path, tmp_path)
    write_json(manifest_path, manifest)
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["epoch_header"].__setitem__(
            "exclusions",
            [],
        ),
    )

    verified = module.verify_integration(manifest_path, worktree=tmp_path)

    assert verified["status"] == "failed"
    assert verified["failures"][0]["code"] == "registered-check"


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("selected_capability_ids", []),
        ("selected_scenario_ids", []),
        ("proof_predecessors", ["SK-999"]),
    ],
)
def test_campaign_admission_fields_are_independently_derived(
    tmp_path: Path,
    field: str,
    replacement: object,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    campaign_pointer = manifest["identities"]["campaigns"][0]["manifest"]
    campaign_path = tmp_path / campaign_pointer["path"]
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    campaign["contract"][field] = replacement
    write_json(campaign_path, campaign)
    campaign_pointer["fingerprint"] = module.file_fingerprint(campaign_path)
    write_json(manifest_path, manifest)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "blocked"
    assert any(
        failure["code"].startswith("campaign")
        for failure in result["failures"]
    )


def test_external_installed_root_and_managed_manifest_are_verified(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    external = tmp_path.parent / f"{tmp_path.name}-external-install"
    (tmp_path / "installed").rename(external)

    result = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
        installed_root=external,
    )

    assert result["status"] == "verified"
    managed = external / ".programming-agent-skills-manifest.json"
    payload = json.loads(managed.read_text(encoding="utf-8"))
    payload["hashes"]["fixture-leaf"] = "0" * 64
    write_json(managed, payload)
    stale = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
        installed_root=external,
    )
    assert stale["status"] == "blocked"
    assert any("manifest" in failure["message"] for failure in stale["failures"])


def test_duplicate_campaign_and_receipt_histories_are_rejected(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["identities"]["campaigns"].append(
        deepcopy(manifest["identities"]["campaigns"][0])
    )
    write_json(manifest_path, manifest)
    duplicate_campaign = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )
    assert duplicate_campaign["status"] == "blocked"
    assert any(
        failure["code"] == "campaign-duplicate"
        for failure in duplicate_campaign["failures"]
    )

    manifest_path = integration_fixture(tmp_path / "receipts")
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path / "receipts",
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["receipts"].append(deepcopy(manifest["receipts"][0]))
    write_json(manifest_path, manifest)
    duplicate_receipt = module.verify_integration(
        manifest_path,
        worktree=tmp_path / "receipts",
    )
    assert duplicate_receipt["status"] == "blocked"


def test_candidate_drift_invalidates_bound_receipts(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    before = json.loads(manifest_path.read_text(encoding="utf-8"))
    contract_path = tmp_path / "docs/synthesis/skill-pack.md"
    contract_path.write_bytes(contract_path.read_bytes() + b"\n")

    drift = module.verify_integration(manifest_path, worktree=tmp_path)

    assert drift["status"] == "blocked"
    assert set(drift["invalidated_receipt_ids"]) == {
        receipt["id"] for receipt in before["receipts"]
    }
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert after["invalidations"][-1]["registration_id"] == "candidate"


def test_stale_invalidation_survives_later_malformed_check(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    first = manifest["registrations"][0]
    first_path = tmp_path / first["result"]["path"]
    first_path.write_bytes(first_path.read_bytes() + b" ")
    behavioral = manifest["registrations"][-1]
    behavioral_path = tmp_path / behavioral["result"]["path"]
    behavioral_path.write_text("{", encoding="utf-8")
    behavioral["result"] = pointer(behavioral_path, tmp_path)
    write_json(manifest_path, manifest)

    failed = module.verify_integration(manifest_path, worktree=tmp_path)

    assert failed["status"] == "failed"
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert after["invalidations"]
    assert after["invalidations"][-1]["registration_id"] == first["id"]


def test_stale_invalidation_and_controlled_failure_persist_atomically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    first = manifest["registrations"][0]
    first_path = tmp_path / first["result"]["path"]
    first_path.write_bytes(first_path.read_bytes() + b" ")
    original_runner = module._run_registration

    def controlled(registration, **kwargs):
        if registration["id"] == "gate-02-structural":
            return (
                "fail",
                [{"check": "controlled-failure", "passed": False}],
                [],
            )
        return original_runner(registration, **kwargs)

    monkeypatch.setattr(module, "_run_registration", controlled)
    failed = module.verify_integration(manifest_path, worktree=tmp_path)

    assert failed["status"] == "failed"
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert any(
        row["registration_id"] == first["id"]
        for row in after["invalidations"]
    )
    failure = next(
        receipt
        for receipt in after["receipts"]
        if receipt["registration_id"] == "gate-02-structural"
        and receipt["outcome"] == "fail"
    )
    assert failure["observations"][0]["check"] == "controlled-failure"


def test_declared_registration_change_invalidates_only_dependent_receipt(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    before = json.loads(manifest_path.read_text(encoding="utf-8"))
    target = before["registrations"][0]
    note = manifest_path.parent / "registered-note.json"
    write_json(note, {"note": "new declared input"})
    target["inputs"] = [pointer(note, tmp_path)]
    write_json(manifest_path, before)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "verified"
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    invalidated = after["invalidations"][-1]["receipt_ids"]
    expected = [
        receipt["id"]
        for receipt in before["receipts"]
        if receipt["registration_id"] == target["id"]
    ]
    assert invalidated == expected
    assert len(after["receipts"]) == len(before["receipts"]) + 1


def test_consistent_candidate_transition_invalidates_all_old_receipts(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    before = json.loads(manifest_path.read_text(encoding="utf-8"))
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["epoch_header"].__setitem__(
            "exclusions",
            ["Automated semantic acceptance", "Foreign semantic mutation"],
        ),
    )

    transitioned = module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )

    assert transitioned["status"] == "verified"
    after = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate_invalidation = next(
        row
        for row in after["invalidations"]
        if row["registration_id"] == "candidate"
    )
    assert set(candidate_invalidation["receipt_ids"]) == {
        receipt["id"] for receipt in before["receipts"]
    }
    assert len(after["receipts"]) == 2 * len(before["receipts"])


def test_receipt_outcome_contradiction_is_rejected(tmp_path: Path) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["receipts"][0]["outcome"] = "fail"
    write_json(manifest_path, manifest)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "blocked"
    assert result["failures"][0]["code"] == "receipt-history"


def test_extra_managed_skill_blocks_exact_installed_parity(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    extra = tmp_path / "installed/extra-skill"
    extra.mkdir()
    (extra / "SKILL.md").write_text("# Extra\n", encoding="utf-8")
    managed = tmp_path / "installed/.programming-agent-skills-manifest.json"
    payload = json.loads(managed.read_text(encoding="utf-8"))
    payload["skills"].append("extra-skill")
    payload["hashes"]["extra-skill"] = install_skills.skill_tree_hash(extra)
    write_json(managed, payload)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["identities"]["installed_pack"]["manifest_fingerprint"] = (
        module.file_fingerprint(managed)
    )
    write_json(manifest_path, manifest)

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "blocked"
    assert any(
        failure["code"] == "installed-pack" for failure in result["failures"]
    )


def test_relationship_edge_parity_rejects_duplicate_missing_and_extra() -> None:
    module = pack_integration()
    expected = {("caller", "Invoke", "target")}
    selected = {"caller", "target"}
    exact = [("caller", "Invoke", "target")]
    assert module.relationship_edges_match(expected, exact, selected)
    assert not module.relationship_edges_match(expected, exact * 2, selected)
    assert not module.relationship_edges_match(expected, [], selected)
    assert not module.relationship_edges_match(
        expected,
        exact + [("caller", "Invoke", "foreign")],
        selected,
    )


def contract_issue(
    issue_class: str,
    *,
    essential: bool,
    status: str,
) -> dict[str, object]:
    return {
        "issue_id": "ECG-001",
        "class": issue_class,
        "essential": essential,
        "involved_skill_ids": ["SK-001"],
        "involved_capability_ids": ["CAP-001"],
        "terms": [],
        "observable_conflict": "The bounded fixture has a conflicting owner",
        "governing_owner": "pack owner",
        "resolution": None,
        "negative_control_scenario_id": "PS-001",
        "status": status,
        "future_owner_or_stopping_condition": "Resolve before integration",
        "nondependency_proof_ids": [],
    }


@pytest.mark.parametrize("issue_class", sorted(pack_contract.COLLISION_CLASSES))
def test_g09_rejects_every_unresolved_critical_collision(
    tmp_path: Path,
    issue_class: str,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["exclusions_collisions_gaps"].append(
            contract_issue(
                issue_class,
                essential=False,
                status="unresolved",
            )
        ),
    )

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "failed"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    receipt = next(
        row
        for row in manifest["receipts"]
        if row["registration_id"] == "gate-09-structural"
    )
    assert receipt["outcome"] == "fail"


def test_g09_allows_bounded_deferred_nonessential_gap(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["exclusions_collisions_gaps"].append(
            {
                **contract_issue("gap", essential=False, status="deferred"),
                "resolution": "Deferred because no selected workflow depends on it",
                "nondependency_proof_ids": ["PROOF-NONDEPENDENCY-001"],
            }
        ),
    )

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "verified"


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("resolution", None),
        ("future_owner_or_stopping_condition", None),
        ("nondependency_proof_ids", []),
    ],
)
def test_g09_rejects_unbounded_deferred_nonessential_gap(
    tmp_path: Path,
    field: str,
    replacement: object,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    issue = {
        **contract_issue("gap", essential=False, status="deferred"),
        "resolution": "Deferred because no selected workflow depends on it",
        "nondependency_proof_ids": ["PROOF-NONDEPENDENCY-001"],
    }
    issue[field] = replacement
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["exclusions_collisions_gaps"].append(issue),
    )

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "failed"


@pytest.mark.parametrize(
    ("issue", "expected_status"),
    [
        (
            contract_issue("gap", essential=True, status="unresolved"),
            "failed",
        ),
        (
            {
                **contract_issue(
                    "authority",
                    essential=False,
                    status="resolved",
                ),
                "resolution": "Pack owner selected one authority",
            },
            "verified",
        ),
    ],
)
def test_g09_essential_gap_and_resolved_collision_boundaries(
    tmp_path: Path,
    issue: dict[str, object],
    expected_status: str,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["exclusions_collisions_gaps"].append(issue),
    )

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == expected_status


def test_candidate_invalidation_persists_before_behavioral_failure(
    tmp_path: Path,
) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    assert module.verify_integration(
        manifest_path,
        worktree=tmp_path,
    )["status"] == "verified"
    before = json.loads(manifest_path.read_text(encoding="utf-8"))
    old_receipt_ids = {row["id"] for row in before["receipts"]}
    rewrite_candidate_contract(
        tmp_path,
        manifest_path,
        lambda contract: contract["epoch_header"].__setitem__(
            "exclusions",
            ["Automated semantic acceptance", "Foreign semantic mutation"],
        ),
    )
    transitioned = json.loads(manifest_path.read_text(encoding="utf-8"))
    behavioral = transitioned["registrations"][-1]
    behavioral_path = tmp_path / behavioral["result"]["path"]
    original = behavioral_path.read_bytes()
    behavioral_path.write_text("{", encoding="utf-8")
    behavioral["result"] = pointer(behavioral_path, tmp_path)
    write_json(manifest_path, transitioned)

    failed = module.verify_integration(manifest_path, worktree=tmp_path)

    assert failed["status"] == "failed"
    after_failure = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate_invalidation = next(
        row
        for row in after_failure["invalidations"]
        if row["registration_id"] == "candidate"
    )
    assert set(candidate_invalidation["receipt_ids"]) == old_receipt_ids

    behavioral_path.write_bytes(original)
    after_failure["registrations"][-1]["result"] = pointer(
        behavioral_path,
        tmp_path,
    )
    write_json(manifest_path, after_failure)
    restored = module.verify_integration(manifest_path, worktree=tmp_path)
    assert restored["status"] == "verified"


def test_manifest_owner_rejects_symlink_redirection(tmp_path: Path) -> None:
    module = pack_integration()
    manifest_path = integration_fixture(tmp_path)
    epoch_dir = manifest_path.parent
    actual = tmp_path.parent / f"{tmp_path.name}-actual-epoch"
    epoch_dir.rename(actual)
    try:
        os.symlink(actual, epoch_dir, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlink creation is unavailable")

    result = module.verify_integration(manifest_path, worktree=tmp_path)

    assert result["status"] == "blocked"
    assert "link/reparse" in result["failures"][0]["message"]


def test_repository_validation_clean_fail_restored(tmp_path: Path) -> None:
    module = pack_integration()
    repository = Path(__file__).resolve().parents[1]
    paths = (
        "docs/validation/shared/schemas/pack-integration-manifest-v1.schema.json",
        "docs/validation/shared/schemas/pack-integration-result-v1.schema.json",
        "docs/validation/skill-pack/README.md",
    )
    for relative in paths:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((repository / relative).read_bytes())

    assert module.validate_repository(tmp_path) == []
    result_schema = tmp_path / paths[1]
    original_schema = result_schema.read_bytes()
    result_schema.unlink()
    assert any(
        "result schema" in failure
        for failure in module.validate_repository(tmp_path)
    )
    result_schema.write_bytes(original_schema)
    assert module.validate_repository(tmp_path) == []

    owner = tmp_path / paths[2]
    original_owner = owner.read_text(encoding="utf-8")
    owner.write_text(
        original_owner.replace("cannot accept", "does not process"),
        encoding="utf-8",
    )
    assert any(
        "cannot accept" in failure
        for failure in module.validate_repository(tmp_path)
    )
    owner.write_text(original_owner, encoding="utf-8")
    assert module.validate_repository(tmp_path) == []
