from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts import campaign_artifacts


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")
    if (
        path.name == "manifest.json"
        and isinstance(payload, dict)
        and isinstance(payload.get("mechanical"), dict)
        and isinstance(payload["mechanical"].get("proof_registrations"), list)
    ):
        pointers = {
            registration.get("decision_pointer")
            for registration in (
                payload["mechanical"]["proof_registrations"]
                + payload["mechanical"].get("preflight_registrations", [])
            )
            if isinstance(registration, dict)
            and isinstance(registration.get("decision_pointer"), str)
            and registration["decision_pointer"].startswith("decisions.md#")
        }
        decision_path = path.parent / "decisions.md"
        if pointers and decision_path.exists():
            markers = "".join(
                f"<!-- campaign-decision:{pointer.split('#', 1)[1]} -->\n"
                for pointer in sorted(pointers)
            )
            decision_path.write_text(
                decision_path.read_text("utf-8") + markers,
                encoding="utf-8",
            )


def valid_case() -> dict[str, object]:
    return {
        "id": "Q01",
        "task": "Judge one bounded case.",
        "facts": {"F1": "The registered condition holds."},
        "authority": "Read-only judgment.",
        "initial_state": "Frozen fixture.",
        "decision_state": {
            "target_resolution": "resolved",
            "evidence_availability": "inspectable",
            "mutation_permission": "forbidden",
        },
        "tools_operations": ["read fixture"],
        "mutation_boundary": "none",
        "requested_output": "Decision and evidence.",
    }


def valid_fixture() -> dict[str, object]:
    return {
        "schema_version": 2,
        "isolation": {
            "candidate_terms_present": False,
            "prior_outputs_present": False,
            "conclusions_present": False,
            "arm_delta": "runtime package only",
        },
        "cases": [valid_case()],
    }


def valid_payload(runtime: str) -> dict[str, object]:
    case = valid_case()
    case["runtime"] = runtime
    return case


def valid_registration() -> dict[str, object]:
    return {
        "terminal_profiles": {
            "ready": {
                "required_roles": ["authority", "completion"],
                "adjacent_terminals": ["blocked"],
            }
        },
        "cases": [
            {
                "id": "Q01",
                "expected_terminal": "ready",
                "feasibility": {
                    "role_evidence": {
                        "authority": ["field:authority"],
                        "completion": ["fact:F1", "operation:read fixture"],
                    },
                    "adjacent_terminal_exclusions": {
                        "blocked": ["fact:F1"],
                    },
                },
            }
        ],
    }


def test_campaign_tree_hash_uses_explicit_ordinal_utf8_path_order(
    tmp_path: Path,
) -> None:
    files = {
        "V09.md": b"valid",
        "V09-invalid.md": b"invalid",
    }
    for name, content in files.items():
        (tmp_path / name).write_bytes(content)

    expected = hashlib.sha256()
    for name in sorted(files, key=lambda value: value.encode("utf-8")):
        content = files[name]
        expected.update(
            (
                f"{name}\t{len(content)}\t"
                f"{hashlib.sha256(content).hexdigest()}\n"
            ).encode("utf-8")
        )

    result = campaign_artifacts.campaign_tree_hash(tmp_path)

    assert result == {
        "algorithm": campaign_artifacts.TREE_ALGORITHM,
        "file_count": 2,
        "sha256": expected.hexdigest(),
    }


def test_fixture_lint_requires_every_worker_visible_decision_field(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    payload = valid_fixture()
    write_json(fixture, payload)
    assert campaign_artifacts.lint_worker_fixture(fixture)["case_count"] == 1

    del payload["cases"][0]["authority"]  # type: ignore[index]
    write_json(fixture, payload)

    with pytest.raises(ValueError, match="Q01: authority"):
        campaign_artifacts.lint_worker_fixture(fixture)


def test_fixture_lint_allows_cluster_fields_to_supply_variant_context(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    payload = valid_fixture()
    payload["cases"] = [
        {
            "task": "Judge the selected variant.",
            "authority": "Read-only judgment.",
            "initial_state": "Frozen fixture.",
            "decision_state": {
                "target_resolution": "resolved",
                "evidence_availability": "inspectable",
                "mutation_permission": "forbidden",
            },
            "tools_operations": ["read fixture"],
            "mutation_boundary": "none",
            "requested_output": "Decision and evidence.",
            "variants": [
                {
                    "id": "Q02-A",
                    "source_facts": ["The registered condition holds."],
                }
            ],
        }
    ]
    write_json(fixture, payload)

    assert campaign_artifacts.lint_worker_fixture(fixture)["case_count"] == 1


def test_fixture_lint_requires_valid_decision_state(tmp_path: Path) -> None:
    fixture = tmp_path / "worker.json"
    payload = valid_fixture()
    del payload["cases"][0]["decision_state"]  # type: ignore[index]
    write_json(fixture, payload)

    with pytest.raises(ValueError, match="Q01: decision_state"):
        campaign_artifacts.lint_worker_fixture(fixture)

    payload = valid_fixture()
    payload["cases"][0]["decision_state"]["target_resolution"] = "guess"  # type: ignore[index]
    write_json(fixture, payload)

    with pytest.raises(ValueError, match="target_resolution"):
        campaign_artifacts.lint_worker_fixture(fixture)


def test_fixture_schema_one_remains_replayable_without_decision_state(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    payload = valid_fixture()
    payload["schema_version"] = 1
    del payload["cases"][0]["decision_state"]  # type: ignore[index]
    write_json(fixture, payload)

    assert campaign_artifacts.lint_worker_fixture(fixture)["schema_version"] == 1


def test_terminal_registration_requires_complete_unique_branch_evidence(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    registration = tmp_path / "root.json"
    worker = valid_fixture()
    root = valid_registration()
    write_json(fixture, worker)
    write_json(registration, root)

    result = campaign_artifacts.lint_terminal_registration(fixture, registration)

    assert result["status"] == "ok"
    assert result["case_count"] == 1

    del root["cases"][0]["feasibility"]["role_evidence"]["completion"]  # type: ignore[index]
    write_json(registration, root)
    with pytest.raises(ValueError, match="role evidence must match"):
        campaign_artifacts.lint_terminal_registration(fixture, registration)


def test_terminal_registration_rejects_unknown_worker_evidence(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    registration = tmp_path / "root.json"
    root = valid_registration()
    root["cases"][0]["feasibility"]["adjacent_terminal_exclusions"]["blocked"] = [  # type: ignore[index]
        "fact:F404"
    ]
    write_json(fixture, valid_fixture())
    write_json(registration, root)

    with pytest.raises(ValueError, match="unknown worker evidence: fact:F404"):
        campaign_artifacts.lint_terminal_registration(fixture, registration)


def test_lint_registration_cli_checks_worker_root_pair(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = tmp_path / "worker.json"
    registration = tmp_path / "root.json"
    write_json(fixture, valid_fixture())
    write_json(registration, valid_registration())

    result = campaign_artifacts.main(
        ["lint-registration", str(fixture), str(registration)]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out)["case_count"] == 1


def test_single_payload_lint_freezes_resolved_dispatch_identity(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    dispatch = tmp_path / "dispatch.json"
    payload = valid_payload("runtime/m0")
    write_json(fixture, valid_fixture())
    write_json(dispatch, payload)

    result = campaign_artifacts.lint_dispatch_payload(
        fixture,
        "Q01",
        dispatch,
    )

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    assert result == {
        "status": "ok",
        "case_id": "Q01",
        "runtime_pointer": "/runtime",
        "dispatch_payload_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def test_lint_payload_cli_uses_the_single_arm_gate(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = tmp_path / "worker.json"
    dispatch = tmp_path / "dispatch.json"
    write_json(fixture, valid_fixture())
    write_json(dispatch, valid_payload("runtime/m0"))

    result = campaign_artifacts.main(
        ["lint-payload", str(fixture), "Q01", str(dispatch)]
    )

    assert result == 0
    assert json.loads(capsys.readouterr().out)["case_id"] == "Q01"


def test_payload_comparison_allows_only_the_runtime_slot(tmp_path: Path) -> None:
    fixture = tmp_path / "worker.json"
    control = tmp_path / "control.json"
    candidate = tmp_path / "candidate.json"
    write_json(fixture, valid_fixture())
    write_json(control, valid_payload("runtime/m0"))
    write_json(candidate, valid_payload("runtime/h1"))

    result = campaign_artifacts.compare_payloads(
        fixture,
        "Q01",
        control,
        candidate,
    )

    assert result["status"] == "ok"
    assert result["runtime_pointer"] == "/runtime"


def test_payload_comparison_rejects_missing_authority_or_candidate_cue(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "worker.json"
    control = tmp_path / "control.json"
    candidate = tmp_path / "candidate.json"
    write_json(fixture, valid_fixture())
    control_payload = valid_payload("runtime/m0")
    candidate_payload = valid_payload("runtime/h1")
    del control_payload["authority"]
    write_json(control, control_payload)
    write_json(candidate, candidate_payload)

    with pytest.raises(ValueError, match="Control dispatch payload is incomplete"):
        campaign_artifacts.compare_payloads(
            fixture,
            "Q01",
            control,
            candidate,
        )

    control_payload["authority"] = "Read-only judgment."
    control_payload["candidate_hint"] = "Prefer the candidate behavior."
    candidate_payload["candidate_hint"] = "Prefer the candidate behavior."
    write_json(control, control_payload)
    write_json(candidate, candidate_payload)

    with pytest.raises(ValueError, match="contains root-only fields"):
        campaign_artifacts.compare_payloads(
            fixture,
            "Q01",
            control,
            candidate,
        )


def test_payload_comparison_rejects_shared_fixture_drift(tmp_path: Path) -> None:
    fixture = tmp_path / "worker.json"
    control = tmp_path / "control.json"
    candidate = tmp_path / "candidate.json"
    write_json(fixture, valid_fixture())
    control_payload = valid_payload("runtime/m0")
    candidate_payload = valid_payload("runtime/h1")
    control_payload["authority"] = "Delegated worker authority."
    candidate_payload["authority"] = "Delegated worker authority."
    write_json(control, control_payload)
    write_json(candidate, candidate_payload)

    with pytest.raises(ValueError, match="disagrees with its worker fixture case"):
        campaign_artifacts.compare_payloads(
            fixture,
            "Q01",
            control,
            candidate,
        )


def test_start_campaign_creates_atomic_two_file_epoch_and_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()

    result = campaign_artifacts.start_campaign(
        "review",
        "none",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )

    campaign_path = (
        worktree / "docs" / "validation" / "campaigns" / "review-epoch-1"
    )
    assert result["status"] == "verified"
    assert result["manifest"] == str(
        campaign_path.relative_to(worktree) / "manifest.json"
    ).replace("\\", "/")
    assert sorted(path.name for path in campaign_path.iterdir()) == [
        "decisions.md",
        "manifest.json",
    ]

    manifest = json.loads((campaign_path / "manifest.json").read_text("utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["campaign"] == {
        "id": "review-epoch-1",
        "skill": "review",
        "delivery_mode": "none",
        "worktree": str(worktree.resolve()),
        "supersedes": None,
    }
    assert manifest["semantic"] == {
        "declared_stage": None,
        "terminal": False,
        "decision_record": "decisions.md",
    }
    assert manifest["mechanical"]["receipts"] == []
    assert manifest["mechanical"]["invalidations"] == []

    lease = json.loads(
        (worktree / ".tmp" / "deploy-campaign-lease.json").read_text("utf-8")
    )
    assert lease["worktree"] == str(worktree.resolve())
    assert lease["campaign_id"] == "review-epoch-1"
    assert lease["owner_token"] == "owner-a"


def test_verify_campaign_reads_exact_owner_stage_without_advancing_it(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    write_json(manifest_path, manifest)
    semantic_before = manifest["semantic"].copy()

    mismatch = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        stage_override="prompt-2",
    )
    first = campaign_artifacts.verify_campaign(manifest_path, worktree=worktree)
    second = campaign_artifacts.verify_campaign(manifest_path, worktree=worktree)

    assert mismatch["status"] == "failed"
    assert mismatch["gate"] == "semantic-stage"
    assert first["status"] == "verified"
    assert first["stage"] == "prompt-1"
    assert second["status"] == "verified"
    verified = json.loads(manifest_path.read_text("utf-8"))
    assert verified["semantic"] == semantic_before
    assert verified["mechanical"]["last_verification"]["stage"] == "prompt-1"


@pytest.mark.parametrize(
    ("mutation", "gate"),
    [
        (lambda manifest: manifest.update(schema_version=0), "manifest-schema"),
        (
            lambda manifest: manifest["campaign"].update(
                delivery_mode="deploy"
            ),
            "manifest-schema",
        ),
        (
            lambda manifest: manifest["campaign"].update(worktree="C:/foreign"),
            "manifest-worktree",
        ),
        (
            lambda manifest: manifest["campaign"].update(
                supersedes="../escape/manifest.json"
            ),
            "manifest-path",
        ),
        (
            lambda manifest: manifest["campaign"].update(
                supersedes=(
                    "docs/validation/campaigns/missing/manifest.json"
                )
            ),
            "manifest-path",
        ),
        (
            lambda manifest: manifest["semantic"].update(
                decision_record="../escape.md"
            ),
            "manifest-path",
        ),
    ],
)
def test_verify_campaign_rejects_legacy_foreign_and_path_escaping_manifests(
    tmp_path: Path,
    mutation: object,
    gate: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    mutation(manifest)  # type: ignore[operator]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(manifest_path, worktree=worktree)

    assert result["status"] == "failed"
    assert result["gate"] == gate


def test_verify_campaign_rejects_missing_decision_record(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    (manifest_path.parent / "decisions.md").unlink()

    result = campaign_artifacts.verify_campaign(manifest_path, worktree=worktree)

    assert result["status"] == "failed"
    assert result["gate"] == "manifest-path"


def test_mechanical_update_rejects_semantic_fields(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])

    with pytest.raises(ValueError, match="semantic"):
        campaign_artifacts.update_mechanical_state(
            manifest_path,
            {"semantic": {"declared_stage": "prompt-2"}},
        )


def test_lease_conflict_release_and_reacquisition(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    first = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )

    conflict = campaign_artifacts.start_campaign(
        "tdd",
        worktree=worktree,
        campaign_id="tdd-epoch-1",
        owner_token="owner-b",
    )
    wrong_owner = campaign_artifacts.release_campaign(
        worktree / str(first["manifest"]),
        worktree=worktree,
        owner_token="owner-b",
    )
    released = campaign_artifacts.release_campaign(
        worktree / str(first["manifest"]),
        worktree=worktree,
        owner_token="owner-a",
    )
    reacquired = campaign_artifacts.start_campaign(
        "tdd",
        worktree=worktree,
        campaign_id="tdd-epoch-1",
        owner_token="owner-b",
    )

    assert conflict["status"] == "lease-conflict"
    assert wrong_owner["status"] == "lease-conflict"
    assert released["status"] == "verified"
    assert reacquired["status"] == "verified"


def test_explicit_abandon_requires_status_readback(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])

    premature = campaign_artifacts.release_campaign(
        manifest_path,
        worktree=worktree,
        owner_token="owner-b",
        abandon=True,
    )
    status = campaign_artifacts.campaign_status(
        manifest_path,
        worktree=worktree,
    )
    abandoned = campaign_artifacts.release_campaign(
        manifest_path,
        worktree=worktree,
        owner_token="owner-b",
        abandon=True,
    )

    assert premature["status"] == "failed"
    assert premature["gate"] == "status-read"
    assert status["status"] == "verified"
    assert status["owner_token"] == "owner-a"
    assert abandoned["status"] == "verified"
    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_resume_preserves_one_unchanged_epoch(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        "commit",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    before = manifest_path.read_bytes()

    resumed = campaign_artifacts.start_campaign(
        "review",
        "commit",
        worktree=worktree,
        owner_token="owner-a",
        continuation="resume",
        from_manifest=manifest_path,
    )

    assert resumed["status"] == "verified"
    assert resumed["campaign_id"] == "review-epoch-1"
    assert manifest_path.read_bytes() == before


def test_repair_records_changed_inputs_and_stales_the_epoch(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    write_json(manifest_path, manifest)
    semantic_before = manifest["semantic"]

    repaired = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        owner_token="owner-a",
        continuation="repair",
        from_manifest=manifest_path,
        changed_inputs=["runtime:m0"],
    )

    assert repaired["status"] == "stale"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    assert manifest["mechanical"]["evidence_state"] == "stale"
    assert manifest["mechanical"]["invalidations"][-1]["changed_inputs"] == [
        "runtime:m0"
    ]
    assert manifest["semantic"] == semantic_before
    verification = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert verification["status"] == "stale"
    assert verification["gate"] == "mechanical-evidence"


def test_restart_creates_superseding_epoch_from_terminal_campaign(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    old_manifest_path = worktree / str(started["manifest"])
    old_manifest = json.loads(old_manifest_path.read_text("utf-8"))
    old_manifest["semantic"]["terminal"] = True
    write_json(old_manifest_path, old_manifest)

    restarted = campaign_artifacts.start_campaign(
        "review",
        "push",
        worktree=worktree,
        campaign_id="review-epoch-2",
        owner_token="owner-a",
        continuation="restart",
        from_manifest=old_manifest_path,
    )

    assert restarted["status"] == "verified"
    new_manifest = json.loads(
        (worktree / str(restarted["manifest"])).read_text("utf-8")
    )
    assert new_manifest["campaign"]["id"] == "review-epoch-2"
    assert new_manifest["campaign"]["supersedes"] == str(
        old_manifest_path.relative_to(worktree)
    ).replace("\\", "/")


def test_failed_restart_preserves_the_source_lease(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    old_manifest_path = worktree / str(started["manifest"])
    old_manifest = json.loads(old_manifest_path.read_text("utf-8"))
    old_manifest["semantic"]["terminal"] = True
    write_json(old_manifest_path, old_manifest)
    collision = (
        worktree / "docs" / "validation" / "campaigns" / "review-epoch-2"
    )
    collision.mkdir()

    exit_code = campaign_artifacts.main(
        [
            "start",
            "review",
            "push",
            "--worktree",
            str(worktree),
            "--campaign-id",
            "review-epoch-2",
            "--owner-token",
            "owner-a",
            "--continuation",
            "restart",
            "--from-manifest",
            str(old_manifest_path),
            "--json",
        ]
    )
    result = json.loads(capsys.readouterr().out)
    lease = json.loads(
        (worktree / campaign_artifacts.LEASE_PATH).read_text("utf-8")
    )

    assert exit_code == 5
    assert result["status"] == "execution-error"
    assert lease["campaign_id"] == "review-epoch-1"
    assert lease["owner_token"] == "owner-a"


def test_control_cli_parsing_keeps_ordinary_and_advanced_surfaces_distinct() -> None:
    start = campaign_artifacts.parse_args(["start", "review"])
    verify = campaign_artifacts.parse_args(["verify", "manifest.json"])
    status = campaign_artifacts.parse_args(["status", "manifest.json"])
    release = campaign_artifacts.parse_args(
        ["release", "manifest.json", "--abandon"]
    )

    assert (start.skill, start.delivery_mode) == ("review", "none")
    assert start.continuation is None
    assert verify.manifest == Path("manifest.json")
    assert verify.stage_override is None
    assert status.command == "status"
    assert release.abandon is True

    with pytest.raises(SystemExit):
        campaign_artifacts.parse_args(["verify"])


def test_control_cli_emits_stable_json_and_concise_human_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()

    exit_code = campaign_artifacts.main(
        [
            "start",
            "review",
            "--worktree",
            str(worktree),
            "--campaign-id",
            "review-epoch-1",
            "--owner-token",
            "owner-a",
            "--json",
        ]
    )
    started = json.loads(capsys.readouterr().out)
    manifest_path = worktree / started["manifest"]
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    write_json(manifest_path, manifest)

    verify_exit = campaign_artifacts.main(
        [
            "verify",
            str(manifest_path),
            "--worktree",
            str(worktree),
            "--json",
        ]
    )
    verified = json.loads(capsys.readouterr().out)
    human_exit = campaign_artifacts.main(
        [
            "status",
            str(manifest_path),
            "--worktree",
            str(worktree),
        ]
    )
    human = capsys.readouterr().out.splitlines()

    assert exit_code == 0
    assert verify_exit == 0
    assert verified["status"] == "verified"
    assert verified["status"] in campaign_artifacts.MECHANICAL_STATUSES
    assert human_exit == 0
    assert len(human) <= 3
    assert human[0].startswith("verified:")


def test_verify_rejects_unknown_stage_and_never_selects_latest(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "made-up-stage"
    write_json(manifest_path, manifest)

    unknown = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    missing = campaign_artifacts.verify_campaign(
        worktree
        / "docs"
        / "validation"
        / "campaigns"
        / "missing-epoch"
        / "manifest.json",
        worktree=worktree,
    )
    manifest_path.write_text("{", encoding="utf-8")
    malformed = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert unknown["status"] == "failed"
    assert unknown["gate"] == "semantic-stage"
    assert missing["status"] == "failed"
    assert missing["gate"] == "manifest-read"
    assert malformed["status"] == "failed"
    assert malformed["gate"] == "manifest-read"


def test_bounded_identity_algorithms_are_stable_and_explicit(
    tmp_path: Path,
) -> None:
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    (candidate / "package").mkdir()
    (candidate / "package" / "SKILL.md").write_text(
        "name: review\n",
        encoding="utf-8",
    )
    structured = candidate / "record.json"
    structured.write_text('{"b": 2, "a": 1}', encoding="utf-8")
    decisions = candidate / "decisions.md"
    decisions.write_text(
        "ignored before\n"
        "<!-- campaign-semantic:prompt-1:begin -->\n"
        "accepted meaning\n"
        "<!-- campaign-semantic:prompt-1:end -->\n"
        "ignored after\n",
        encoding="utf-8",
    )

    tree = campaign_artifacts.artifact_identity(
        {
            "algorithm": "campaign-tree-v1",
            "path": "package",
        },
        candidate_root=candidate,
    )
    canonical = campaign_artifacts.artifact_identity(
        {
            "algorithm": "canonical-json-v1",
            "path": "record.json",
        },
        candidate_root=candidate,
    )
    semantic = campaign_artifacts.artifact_identity(
        {
            "algorithm": "marker-semantic-v1",
            "path": "decisions.md",
            "marker": "prompt-1",
        },
        candidate_root=candidate,
    )
    structured.write_text('{\n  "a": 1,\n  "b": 2\n}\n', encoding="utf-8")

    assert tree["algorithm"] == "campaign-tree-v1"
    assert tree["digest"] == campaign_artifacts.campaign_tree_hash(
        candidate / "package"
    )["sha256"]
    assert canonical == campaign_artifacts.artifact_identity(
        {
            "algorithm": "canonical-json-v1",
            "path": "record.json",
        },
        candidate_root=candidate,
    )
    assert semantic["digest"] == hashlib.sha256(
        b"accepted meaning\n"
    ).hexdigest()


def test_git_object_identity_requires_explicit_candidate_root_and_revision(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}

    def fake_run(
        argv: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        observed.setdefault("calls", []).append(argv)  # type: ignore[union-attr]
        observed["kwargs"] = kwargs
        output = f"{tmp_path}\n" if "--show-toplevel" in argv else "abc123\n"
        return subprocess.CompletedProcess(argv, 0, output, "")

    monkeypatch.setattr(campaign_artifacts.subprocess, "run", fake_run)
    result = campaign_artifacts.artifact_identity(
        {
            "algorithm": "git-object-v1",
            "revision": "HEAD",
        },
        candidate_root=tmp_path,
    )

    assert result == {"algorithm": "git-object-v1", "digest": "abc123"}
    assert observed["calls"][-1] == [  # type: ignore[index]
        "git",
        "rev-parse",
        "--verify",
        "HEAD^{tree}",
    ]
    assert observed["kwargs"]["cwd"] == tmp_path.resolve()  # type: ignore[index]
    with pytest.raises(ValueError, match="candidate root"):
        campaign_artifacts.artifact_identity(
            {"algorithm": "git-object-v1", "revision": "HEAD"},
            candidate_root=None,
        )


def test_transitive_receipt_invalidation_preserves_history() -> None:
    receipts = [
        {
            "id": "receipt-a",
            "inputs": [{"name": "skill-tree", "digest": "old"}],
            "supersedes": None,
        },
        {
            "id": "receipt-b",
            "inputs": [{"name": "receipt:receipt-a", "digest": "output-a"}],
            "supersedes": None,
        },
        {
            "id": "receipt-c",
            "inputs": [{"name": "other", "digest": "same"}],
            "supersedes": None,
        },
    ]
    before = json.loads(json.dumps(receipts))

    stale = campaign_artifacts.transitively_stale_receipts(
        receipts,
        {"skill-tree"},
    )

    assert stale == {"receipt-a", "receipt-b"}
    assert receipts == before


def _tree_target(worktree: Path) -> dict[str, object]:
    return {
        "algorithm": "campaign-tree-v1",
        "path": "target",
        "digest": campaign_artifacts.campaign_tree_hash(
            worktree / "target"
        )["sha256"],
    }


def _git_target(worktree: Path) -> dict[str, object]:
    if not (worktree / ".git").exists():
        subprocess.run(
            ["git", "init", "--quiet", str(worktree)],
            check=True,
            capture_output=True,
            text=True,
        )
    subprocess.run(
        ["git", "add", "--", "target"],
        cwd=worktree,
        check=True,
        capture_output=True,
        text=True,
    )
    tree = subprocess.run(
        ["git", "write-tree"],
        cwd=worktree,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return {
        "algorithm": "git-object-v1",
        "revision": tree,
        "digest": tree,
    }


def _registration(
    worktree: Path,
    *,
    registration_id: str = "focused",
    profile: str = "campaign-artifacts-focused-v1",
    tier: str | None = None,
    cache_bundle: str | None = None,
    fresh_behavior: bool = False,
) -> dict[str, object]:
    registration: dict[str, object] = {
        "id": registration_id,
        "profile": profile,
        "applicability": "required",
        "decision_pointer": "decisions.md#prompt-1",
        "candidate_root": ".",
        "target": (
            _git_target(worktree)
            if profile == "full-suite-v1"
            else _tree_target(worktree)
        ),
        "inputs": [
            {
                "name": "skill-tree",
                "algorithm": "campaign-tree-v1",
                "path": "target",
                "digest": campaign_artifacts.campaign_tree_hash(
                    worktree / "target"
                )["sha256"],
            }
        ],
        "fresh_behavior": fresh_behavior,
    }
    if tier is not None:
        registration["tier"] = tier
    if cache_bundle is not None:
        registration["cache_bundle"] = cache_bundle
    return registration


def test_verify_reuses_exact_durable_receipt_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    target = worktree / "target"
    target.mkdir()
    (target / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"output-a").hexdigest(),
            source="execution",
            receipt_id="receipt-existing",
            observed_at="2026-07-25T00:00:00Z",
        )
    ]
    write_json(manifest_path, manifest)

    def should_not_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("exact receipt should be reused")

    monkeypatch.setattr(campaign_artifacts.subprocess, "run", should_not_run)
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["reused_receipts"] == ["receipt-existing"]
    after = json.loads(manifest_path.read_text("utf-8"))
    assert after["mechanical"]["receipts"] == manifest["mechanical"]["receipts"]


def test_verify_rejects_corrupt_cache_then_executes_allowlisted_profile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    cache_path = worktree / ".tmp" / "proof-cache.json"
    cache_path.parent.mkdir()
    cache_path.write_text("{", encoding="utf-8")
    registration = _registration(
        worktree,
        cache_bundle=".tmp/proof-cache.json",
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []

    def fake_run(
        registration: dict[str, object],
        identity_tuple: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        calls.append([str(registration["id"])])
        return campaign_artifacts.make_receipt(
            registration,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"passed").hexdigest(),
            source="execution",
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", fake_run)
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["executed"] == ["focused"]
    assert result["proof"]["cache_rejections"] == ["focused"]
    assert len(calls) == 1
    assert isinstance(calls[0], list)
    assert after_receipt_source(manifest_path) == "execution"


def after_receipt_source(manifest_path: Path) -> str:
    manifest = json.loads(manifest_path.read_text("utf-8"))
    return str(manifest["mechanical"]["receipts"][-1]["source"])


def test_verify_reuses_exact_self_describing_tmp_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(
        worktree,
        cache_bundle=".tmp/proof-cache.json",
    )
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    cache_path = worktree / ".tmp" / "proof-cache.json"
    cache_path.parent.mkdir()
    output_path = worktree / ".tmp" / "proof-output.txt"
    output_path.write_text("cached output", encoding="utf-8")
    write_json(
        cache_path,
        {
            "schema_version": 1,
            "proof_profile": registration["profile"],
            "proof_lane": registration["id"],
            "identity_tuple": identity_tuple,
            "exit_state": {"code": 0, "status": "passed"},
            "output_path": ".tmp/proof-output.txt",
            "output_digest": hashlib.sha256(b"cached output").hexdigest(),
            "completed_at": "2026-07-25T00:00:00Z",
        },
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("valid cache should be reused")
        ),
    )
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["reused_cache"] == ["focused"]
    assert after_receipt_source(manifest_path) == "tmp-cache"


def test_fresh_behavior_rejects_cached_evidence_without_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree, fresh_behavior=True)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("behavioral sampling is not deterministic proof")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "fresh-behavior"


def test_forced_rerun_requires_reason_and_supersedes_exact_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"old").hexdigest(),
            source="execution",
            receipt_id="receipt-old",
            observed_at="2026-07-25T00:00:00Z",
        )
    ]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: subprocess.CompletedProcess(
            argv,
            0,
            "new",
            "",
        ),
    )

    missing_reason = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
    )
    forced = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
        force_reason="diagnose nondeterminism",
    )

    assert missing_reason["status"] == "failed"
    assert missing_reason["gate"] == "force-proof"
    assert forced["status"] == "verified"
    receipts = json.loads(manifest_path.read_text("utf-8"))["mechanical"][
        "receipts"
    ]
    assert receipts[0] == manifest["mechanical"]["receipts"][0]
    assert receipts[1]["supersedes"] == "receipt-old"
    assert receipts[1]["forced_reason"] == "diagnose nondeterminism"


def test_verification_aggregates_cheap_failures_and_short_circuits_later_tiers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    first = _registration(worktree, registration_id="cheap-a")
    second = _registration(worktree, registration_id="cheap-b")
    first["target"]["digest"] = "wrong-a"  # type: ignore[index]
    second["target"]["digest"] = "wrong-b"  # type: ignore[index]
    later = _registration(
        worktree,
        registration_id="moderate",
        profile="validate-skills-v1",
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [first, second, later]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("identity tier failure must skip proof")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-identity"
    assert [failure["registration"] for failure in result["failures"]] == [
        "cheap-a",
        "cheap-b",
    ]
    assert result["expensive_work_skipped"] is True


def test_applicability_requires_pointer_and_full_suite_deduplicates_by_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    skipped = _registration(worktree, registration_id="skip")
    skipped["applicability"] = "not-applicable"
    skipped["decision_pointer"] = "decisions.md#not-applicable"
    first = _registration(
        worktree,
        registration_id="suite-a",
        profile="full-suite-v1",
    )
    second = _registration(
        worktree,
        registration_id="suite-b",
        profile="full-suite-v1",
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [skipped, first, second]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []

    def fake_run(
        registration: dict[str, object],
        identity_tuple: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        calls.append([str(registration["id"])])
        return campaign_artifacts.make_receipt(
            registration,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"passed").hexdigest(),
            source="execution",
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", fake_run)
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert len(calls) == 1
    assert result["proof"]["not_applicable"] == ["skip"]
    assert set(result["proof"]["executed"] + result["proof"]["deduplicated"]) == {
        "suite-a",
        "suite-b",
    }


def test_cache_bundle_digest_mismatch_falls_through_to_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(
        worktree,
        cache_bundle=".tmp/proof-cache.json",
    )
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    output_path = worktree / ".tmp" / "proof-output.txt"
    output_path.parent.mkdir()
    output_path.write_text("actual output", encoding="utf-8")
    write_json(
        worktree / ".tmp" / "proof-cache.json",
        {
            "schema_version": 1,
            "proof_profile": registration["profile"],
            "proof_lane": registration["id"],
            "identity_tuple": identity_tuple,
            "exit_state": {"code": 0, "status": "passed"},
            "output_path": ".tmp/proof-output.txt",
            "output_digest": hashlib.sha256(b"different output").hexdigest(),
            "completed_at": "2026-07-25T00:00:00Z",
        },
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: (
            calls.append(argv)
            or subprocess.CompletedProcess(argv, 0, "fresh", "")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["cache_rejections"] == ["focused"]
    assert len(calls) == 1
    assert after_receipt_source(manifest_path) == "execution"


def test_repair_stales_only_dependent_receipts_and_reuses_unrelated_proof(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    dependent = _registration(worktree, registration_id="dependent")
    unrelated = _registration(worktree, registration_id="unrelated")
    unrelated["inputs"][0]["name"] = "other-tree"  # type: ignore[index]
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [dependent, unrelated]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(
                f"output-{registration['id']}".encode()
            ).hexdigest(),
            source="execution",
            receipt_id=f"receipt-{registration['id']}",
            observed_at="2026-07-25T00:00:00Z",
        )
        for registration in (dependent, unrelated)
    ]
    write_json(manifest_path, manifest)
    repaired = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        owner_token="owner-a",
        continuation="repair",
        from_manifest=manifest_path,
        changed_inputs=["skill-tree"],
    )
    calls: list[list[str]] = []
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: (
            calls.append(argv)
            or subprocess.CompletedProcess(argv, 0, "fresh", "")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    repeated = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert repaired["status"] == "stale"
    assert result["status"] == "verified"
    assert result["proof"]["stale_receipts"] == ["receipt-dependent"]
    assert result["proof"]["reused_receipts"] == ["receipt-unrelated"]
    assert len(calls) == 1
    assert repeated["status"] == "verified"
    assert len(calls) == 1


def test_blocked_applicability_returns_pointer_without_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    blocked = _registration(worktree, registration_id="blocked-proof")
    blocked["applicability"] = "blocked"
    blocked["decision_pointer"] = "decisions.md#blocked-proof"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [blocked]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("blocked proof must not execute")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "stale"
    assert result["gate"] == "proof-applicability"
    assert result["blocked"] == ["blocked-proof"]
    assert result["decision_pointers"] == ["decisions.md#blocked-proof"]


@pytest.mark.parametrize("field", ["argv", "command", "environment", "env", "network"])
def test_registration_rejects_command_environment_and_network_overrides(
    tmp_path: Path,
    field: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration[field] = ["untrusted"] if field == "argv" else "untrusted"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-profile"


def test_no_execute_returns_cost_only_plan_and_cli_parses_force_controls(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        no_execute=True,
    )
    parsed = campaign_artifacts.parse_args(
        [
            "verify",
            "manifest.json",
            "--force-proof",
            "focused",
            "--force-reason",
            "diagnostic",
            "--no-execute",
        ]
    )

    assert result["status"] == "stale"
    assert result["plan"] == [
        {
            "registration": "focused",
            "profile": "campaign-artifacts-focused-v1",
            "tier": "cheap",
        }
    ]
    assert "time" not in json.dumps(result["plan"])
    assert "money" not in json.dumps(result["plan"])
    assert "token" not in json.dumps(result["plan"])
    assert parsed.force_proof == "focused"
    assert parsed.force_reason == "diagnostic"
    assert parsed.no_execute is True


def test_corrupt_or_legacy_durable_receipt_fails_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    manifest["mechanical"]["receipts"] = [{"schema_version": 0}]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("corrupt durable state must not execute")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


def test_status_reports_earliest_stale_stage_without_semantic_routing(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    later = _registration(worktree, registration_id="later")
    later["stage"] = "prompt-4"
    earlier = _registration(worktree, registration_id="earlier")
    earlier["stage"] = "prompt-2"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-4"
    manifest["mechanical"]["proof_registrations"] = [later, earlier]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(
                f"output-{registration['id']}".encode()
            ).hexdigest(),
            source="execution",
            receipt_id=f"receipt-{registration['id']}",
            observed_at="2026-07-25T00:00:00Z",
        )
        for registration in (later, earlier)
    ]
    write_json(manifest_path, manifest)
    campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        owner_token="owner-a",
        continuation="repair",
        from_manifest=manifest_path,
        changed_inputs=["skill-tree"],
    )

    result = campaign_artifacts.campaign_status(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "stale"
    assert result["earliest_stale_stage"] == "prompt-2"
    assert "route" not in result


def test_decision_pointer_must_resolve_to_the_exact_decision_record(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["decision_pointer"] = "../foreign.md#proof"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-applicability"


def test_proof_launch_error_returns_stable_execution_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            OSError("executable unavailable")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "execution-error"
    assert result["gate"] == "proof-execution"
    assert result["exit_code"] == 5


def test_forced_proof_rejects_not_applicable_registration(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["applicability"] = "not-applicable"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
        force_reason="diagnostic",
    )

    assert result["status"] == "failed"
    assert result["gate"] == "force-proof"


def test_identity_registry_rejects_caller_trusted_literal_digest(
    tmp_path: Path,
) -> None:
    with pytest.raises(ValueError, match="foreign or legacy"):
        campaign_artifacts.artifact_identity(
            {"algorithm": "literal-v1", "digest": "trusted"},
            candidate_root=tmp_path,
        )


@pytest.mark.parametrize(
    "mutation",
    [
        lambda receipt: receipt["exit_state"].update(status="failed"),
        lambda receipt: receipt.update(output_digest=""),
        lambda receipt: receipt.update(observed_at="not-a-time"),
        lambda receipt: receipt.update(forced_reason="reason"),
    ],
)
def test_shape_valid_corrupt_receipt_fails_closed(
    tmp_path: Path,
    mutation: object,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    receipt = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"output").hexdigest(),
        source="execution",
        receipt_id="receipt-existing",
        observed_at="2026-07-25T00:00:00Z",
    )
    mutation(receipt)  # type: ignore[operator]
    manifest["mechanical"]["receipts"] = [receipt]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


def test_duplicate_receipt_ids_fail_closed(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    receipt = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"output").hexdigest(),
        source="execution",
        receipt_id="receipt-existing",
        observed_at="2026-07-25T00:00:00Z",
    )
    manifest["mechanical"]["receipts"] = [receipt, receipt.copy()]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


def test_decision_pointer_fragment_must_resolve(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["decision_pointer"] = "decisions.md#missing"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    path = manifest_path.parent / "decisions.md"
    path.write_text("# Deploy Campaign Decisions\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-applicability"


def test_environment_identity_binds_interpreter_and_dependencies(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    (worktree / "pyproject.toml").write_text("[project]\nname='one'\n", "utf-8")
    registration = _registration(worktree)
    first = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    (worktree / "pyproject.toml").write_text("[project]\nname='two'\n", "utf-8")
    second = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )

    assert first["environment"]["executable"]
    assert first["environment"]["installed_packages_sha256"]
    assert first["environment"]["dependency_files_sha256"] != second[
        "environment"
    ]["dependency_files_sha256"]


def test_off_stage_forced_proof_is_rejected_instead_of_ignored(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["stage"] = "prompt-2"
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
        force_reason="diagnostic",
    )

    assert result["status"] == "failed"
    assert result["gate"] == "force-proof"


def test_expensive_tier_failure_reports_that_expensive_work_ran(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts,
        "_run_profile",
        lambda registration, identity_tuple, **kwargs: (
            campaign_artifacts.make_receipt(
                registration,
                identity_tuple,
                exit_code=1,
                output_digest=hashlib.sha256(b"failed").hexdigest(),
                source="execution",
            )
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-execution"
    assert result["expensive_work_skipped"] is False


def test_marker_semantic_identity_rejects_reversed_markers(
    tmp_path: Path,
) -> None:
    path = tmp_path / "decisions.md"
    path.write_text(
        "<!-- campaign-semantic:prompt-1:end -->\n"
        "meaning\n"
        "<!-- campaign-semantic:prompt-1:begin -->\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="ordered"):
        campaign_artifacts.artifact_identity(
            {
                "algorithm": "marker-semantic-v1",
                "path": "decisions.md",
                "marker": "prompt-1",
            },
            candidate_root=tmp_path,
        )


def test_future_cache_timestamp_is_rejected_and_cannot_bypass_repair(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(
        worktree,
        cache_bundle=".tmp/proof-cache.json",
    )
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    output_path = worktree / ".tmp" / "proof-output.txt"
    output_path.parent.mkdir()
    output_path.write_text("cached", encoding="utf-8")
    write_json(
        worktree / ".tmp" / "proof-cache.json",
        {
            "schema_version": 1,
            "proof_profile": registration["profile"],
            "proof_lane": registration["id"],
            "identity_tuple": identity_tuple,
            "exit_state": {"code": 0, "status": "passed"},
            "output_path": ".tmp/proof-output.txt",
            "output_digest": hashlib.sha256(b"cached").hexdigest(),
            "completed_at": "2999-01-01T00:00:00Z",
        },
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: (
            calls.append(argv)
            or subprocess.CompletedProcess(argv, 0, "fresh", "")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["cache_rejections"] == ["focused"]
    assert len(calls) == 1


def test_full_suite_deduplicates_by_repository_target_even_when_inputs_differ(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    first = _registration(
        worktree,
        registration_id="suite-a",
        profile="full-suite-v1",
    )
    second = _registration(
        worktree,
        registration_id="suite-b",
        profile="full-suite-v1",
    )
    second["inputs"][0]["name"] = "other-tree"  # type: ignore[index]
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [first, second]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []
    def fake_full_suite(
        registration: dict[str, object],
        identity_tuple: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        calls.append([str(registration["id"])])
        return campaign_artifacts.make_receipt(
            registration,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"passed").hexdigest(),
            source="execution",
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", fake_full_suite)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert len(calls) == 1
    assert result["proof"]["deduplicated"] == ["suite-b"]


def test_git_object_identity_rejects_nested_candidate_root(
    tmp_path: Path,
) -> None:
    subprocess.run(
        ["git", "init", "--quiet", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    nested = tmp_path / "nested"
    nested.mkdir()

    with pytest.raises(ValueError, match="worktree root"):
        campaign_artifacts.artifact_identity(
            {"algorithm": "git-object-v1", "revision": "HEAD"},
            candidate_root=nested,
        )


def test_automatic_rerun_supersedes_failed_exact_receipt_without_rewrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    failed = campaign_artifacts.make_receipt(
        registration,
        identity_tuple,
        exit_code=1,
        output_digest=hashlib.sha256(b"failed").hexdigest(),
        source="execution",
        receipt_id="receipt-failed",
        observed_at="2026-07-25T00:00:00Z",
    )
    manifest["mechanical"]["receipts"] = [failed]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: subprocess.CompletedProcess(
            argv,
            0,
            "passed",
            "",
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    receipts = json.loads(manifest_path.read_text("utf-8"))["mechanical"][
        "receipts"
    ]

    assert result["status"] == "verified"
    assert receipts[0] == failed
    assert receipts[1]["supersedes"] == "receipt-failed"
    assert receipts[1]["id"] != "receipt-failed"


def test_first_forced_run_records_null_supersession_and_remains_reusable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: (
            calls.append(argv)
            or subprocess.CompletedProcess(argv, 0, "passed", "")
        ),
    )

    first = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
        force_reason="diagnostic",
    )
    second = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    receipt = json.loads(manifest_path.read_text("utf-8"))["mechanical"][
        "receipts"
    ][0]

    assert first["status"] == "verified"
    assert second["status"] == "verified"
    assert receipt["supersedes"] is None
    assert receipt["forced_reason"] == "diagnostic"
    assert len(calls) == 1


def test_receipt_self_digest_detects_coherent_field_tampering(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    receipt = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"output").hexdigest(),
        source="execution",
        receipt_id="receipt-existing",
        observed_at="2026-07-25T00:00:00Z",
    )
    receipt["output_digest"] = hashlib.sha256(b"tampered").hexdigest()
    manifest["mechanical"]["receipts"] = [receipt]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


@pytest.mark.parametrize("mode", ["duplicate", "missing-file"])
def test_decision_pointer_resolution_fails_closed(
    tmp_path: Path,
    mode: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    decision_path = manifest_path.parent / "decisions.md"
    if mode == "duplicate":
        marker = "<!-- campaign-decision:prompt-1 -->\n"
        decision_path.write_text(marker + marker, encoding="utf-8")
    else:
        decision_path.unlink()

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] in {"manifest-path", "proof-applicability"}


def test_environment_identity_binds_ambient_execution_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    monkeypatch.setenv("PYTEST_ADDOPTS", "-q")
    first = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    monkeypatch.setenv("PYTEST_ADDOPTS", "-x")
    second = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )

    assert first["environment"]["ambient_environment_sha256"] != second[
        "environment"
    ]["ambient_environment_sha256"]


def test_timestamp_invalidation_compares_instants_not_strings() -> None:
    receipts = [
        {
            "id": "receipt-a",
            "observed_at": "2026-07-25T00:00:00Z",
            "inputs": [{"name": "skill-tree"}],
        }
    ]
    invalidations = [
        {
            "observed_at": "2026-07-25T00:00:00.100000Z",
            "changed_inputs": ["skill-tree"],
        }
    ]

    stale = campaign_artifacts._stale_receipts_from_invalidations(
        receipts,
        invalidations,
    )

    assert stale == {"receipt-a"}


def test_pre_repair_cache_bundle_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(
        worktree,
        cache_bundle=".tmp/proof-cache.json",
    )
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    output_path = worktree / ".tmp" / "proof-output.txt"
    output_path.parent.mkdir()
    output_path.write_text("cached", encoding="utf-8")
    write_json(
        worktree / ".tmp" / "proof-cache.json",
        {
            "schema_version": 1,
            "proof_profile": registration["profile"],
            "proof_lane": registration["id"],
            "identity_tuple": identity_tuple,
            "exit_state": {"code": 0, "status": "passed"},
            "output_path": ".tmp/proof-output.txt",
            "output_digest": hashlib.sha256(b"cached").hexdigest(),
            "completed_at": "2026-07-25T00:00:00Z",
        },
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    manifest["mechanical"]["invalidations"] = [
        {
            "changed_inputs": ["skill-tree"],
            "observed_at": "2026-07-25T01:00:00Z",
        }
    ]
    write_json(manifest_path, manifest)
    calls: list[list[str]] = []
    monkeypatch.setattr(
        campaign_artifacts.subprocess,
        "run",
        lambda argv, **kwargs: (
            calls.append(argv)
            or subprocess.CompletedProcess(argv, 0, "fresh", "")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["proof"]["cache_rejections"] == ["focused"]
    assert len(calls) == 1


def test_failed_forced_full_suite_does_not_resurrect_superseded_pass(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    passed = campaign_artifacts.make_receipt(
        registration,
        identity_tuple,
        exit_code=0,
        output_digest=hashlib.sha256(b"passed").hexdigest(),
        source="execution",
        receipt_id="receipt-passed",
        observed_at="2026-07-25T00:00:00Z",
    )
    manifest["mechanical"]["receipts"] = [passed]
    write_json(manifest_path, manifest)
    calls: list[str] = []

    def run_profile(
        selected: dict[str, object],
        selected_identity: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        forced_reason = kwargs.get("forced_reason")
        calls.append("forced" if forced_reason else "automatic")
        return campaign_artifacts.make_receipt(
            selected,
            selected_identity,
            exit_code=1 if forced_reason else 0,
            output_digest=hashlib.sha256(
                b"failed" if forced_reason else b"recovered"
            ).hexdigest(),
            source="forced-execution" if forced_reason else "execution",
            supersedes=kwargs.get("supersedes"),  # type: ignore[arg-type]
            forced_reason=forced_reason,  # type: ignore[arg-type]
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", run_profile)
    forced = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
        force_proof="focused",
        force_reason="diagnostic",
    )
    forced_receipts = json.loads(manifest_path.read_text("utf-8"))["mechanical"][
        "receipts"
    ]
    assert campaign_artifacts._valid_receipt_history(
        forced_receipts
    ), forced_receipts
    recovered = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert forced["status"] == "failed"
    assert recovered["status"] == "verified", recovered.get("message")
    assert calls == ["forced", "automatic"]


def test_full_suite_rejects_non_repository_target_identity(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    registration["target"] = _tree_target(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-identity"


def test_expensive_profile_launch_error_records_expensive_work_attempted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts,
        "_run_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("unavailable")),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "execution-error"
    assert result["expensive_work_skipped"] is False


def test_canonical_json_identity_rejects_non_finite_numbers(
    tmp_path: Path,
) -> None:
    path = tmp_path / "record.json"
    path.write_text('{"value": NaN}', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON compliant"):
        campaign_artifacts.artifact_identity(
            {"algorithm": "canonical-json-v1", "path": "record.json"},
            candidate_root=tmp_path,
        )


def test_input_identity_tuple_records_exact_locator(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    for name in ("target", "same-bytes"):
        (worktree / name).mkdir()
        (worktree / name / "value.txt").write_text("current", encoding="utf-8")
    first_registration = _registration(worktree)
    second_registration = json.loads(json.dumps(first_registration))
    second_registration["inputs"][0]["path"] = "same-bytes"
    first = campaign_artifacts.proof_identity_tuple(
        first_registration,
        candidate_root=worktree,
    )
    second = campaign_artifacts.proof_identity_tuple(
        second_registration,
        candidate_root=worktree,
    )

    assert first["inputs"][0]["digest"] == second["inputs"][0]["digest"]
    assert first["inputs"][0]["path"] != second["inputs"][0]["path"]


def test_full_suite_rejects_live_worktree_bytes_that_differ_from_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    value_path = worktree / "target" / "value.txt"
    value_path.write_text("recorded", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    value_path.write_text("different live bytes", encoding="utf-8")
    registration["inputs"][0]["digest"] = campaign_artifacts.campaign_tree_hash(
        worktree / "target"
    )["sha256"]
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts,
        "_run_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("mismatched worktree must fail before execution")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-identity"
    assert "worktree" in result["failures"][0]["message"].lower()


def test_full_suite_rejects_non_excluded_untracked_file_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("recorded", encoding="utf-8")
    registration = _registration(worktree, profile="full-suite-v1")
    (worktree / "rogue.py").write_text("untracked", encoding="utf-8")
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts,
        "_run_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("untracked worktree must fail before execution")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-identity"
    assert "worktree" in result["failures"][0]["message"].lower()


def test_cached_dependent_of_stale_receipt_is_rejected_transitively(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    upstream = _registration(worktree, registration_id="upstream")
    downstream = _registration(
        worktree,
        registration_id="downstream",
        cache_bundle=".tmp/downstream-cache.json",
    )
    downstream["inputs"][0]["name"] = "receipt:receipt-upstream"  # type: ignore[index]
    upstream_identity = campaign_artifacts.proof_identity_tuple(
        upstream,
        candidate_root=worktree,
    )
    upstream_receipt = campaign_artifacts.make_receipt(
        upstream,
        upstream_identity,
        exit_code=0,
        output_digest=hashlib.sha256(b"upstream").hexdigest(),
        source="execution",
        receipt_id="receipt-upstream",
        observed_at="2026-07-25T00:00:00Z",
    )
    downstream_identity = campaign_artifacts.proof_identity_tuple(
        downstream,
        candidate_root=worktree,
    )
    output_path = worktree / ".tmp" / "downstream-output.txt"
    output_path.parent.mkdir()
    output_path.write_text("cached downstream", encoding="utf-8")
    write_json(
        worktree / ".tmp" / "downstream-cache.json",
        {
            "schema_version": 1,
            "proof_profile": downstream["profile"],
            "proof_lane": downstream["id"],
            "identity_tuple": downstream_identity,
            "exit_state": {"code": 0, "status": "passed"},
            "output_path": ".tmp/downstream-output.txt",
            "output_digest": hashlib.sha256(b"cached downstream").hexdigest(),
            "completed_at": "2026-07-25T00:30:00Z",
        },
    )
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [downstream]
    manifest["mechanical"]["receipts"] = [upstream_receipt]
    manifest["mechanical"]["invalidations"] = [
        {
            "changed_inputs": ["skill-tree"],
            "observed_at": "2026-07-25T01:00:00Z",
        }
    ]
    write_json(manifest_path, manifest)
    calls: list[str] = []

    def run_profile(
        selected: dict[str, object],
        identity_tuple: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        calls.append(str(selected["id"]))
        return campaign_artifacts.make_receipt(
            selected,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"fresh downstream").hexdigest(),
            source="execution",
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", run_profile)
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    repeated = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-identity"
    assert "stale receipt" in result["failures"][0]["message"].lower()
    assert repeated["status"] == "failed"
    assert calls == []


def test_non_finite_nested_receipt_corruption_returns_proof_receipt_failure(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    receipt = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"output").hexdigest(),
        source="execution",
    )
    receipt["unexpected"] = {"value": float("nan")}
    manifest["mechanical"]["receipts"] = [receipt]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


def test_legacy_receipt_history_is_preserved_but_never_reused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    current = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"legacy output").hexdigest(),
        source="execution",
        receipt_id="receipt-legacy",
        observed_at="2026-07-25T00:00:00Z",
    )
    legacy = json.loads(json.dumps(current))
    legacy["schema_version"] = 1
    legacy["environment"].pop("ambient_environment_sha256")
    legacy.pop("receipt_digest")
    manifest["mechanical"]["receipts"] = [legacy]
    write_json(manifest_path, manifest)
    calls: list[str] = []

    def run_profile(
        selected: dict[str, object],
        identity_tuple: dict[str, object],
        **kwargs: object,
    ) -> dict[str, object]:
        calls.append(str(selected["id"]))
        return campaign_artifacts.make_receipt(
            selected,
            identity_tuple,
            exit_code=0,
            output_digest=hashlib.sha256(b"fresh output").hexdigest(),
            source="execution",
        )

    monkeypatch.setattr(campaign_artifacts, "_run_profile", run_profile)
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    receipts = json.loads(manifest_path.read_text("utf-8"))["mechanical"][
        "receipts"
    ]

    assert result["status"] == "verified"
    assert calls == ["focused"]
    assert receipts[0] == legacy
    assert receipts[1]["schema_version"] == 2


@pytest.mark.parametrize(
    "mutation",
    [
        lambda receipt: receipt["inputs"][0].update(unexpected="field"),
        lambda receipt: receipt["environment"].update(value=float("nan")),
        lambda receipt: receipt.update(stage="foreign"),
    ],
)
def test_malformed_legacy_receipt_fails_closed(
    tmp_path: Path,
    mutation: object,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "target").mkdir()
    (worktree / "target" / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    manifest["mechanical"]["proof_registrations"] = [registration]
    receipt = campaign_artifacts.make_receipt(
        registration,
        campaign_artifacts.proof_identity_tuple(
            registration,
            candidate_root=worktree,
        ),
        exit_code=0,
        output_digest=hashlib.sha256(b"legacy output").hexdigest(),
        source="execution",
    )
    receipt["schema_version"] = 1
    receipt["environment"].pop("ambient_environment_sha256")
    receipt.pop("receipt_digest")
    assert callable(mutation)
    mutation(receipt)
    manifest["mechanical"]["receipts"] = [receipt]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"


def _identity_spec(
    root: Path,
    path: str,
    algorithm: str = "canonical-json-v1",
) -> dict[str, str]:
    specification = {"algorithm": algorithm, "path": path}
    return {
        **specification,
        "digest": campaign_artifacts.artifact_identity(
            specification,
            candidate_root=root,
        )["digest"],
    }


def test_build_behavioral_payloads_injects_only_registered_runtime(
    tmp_path: Path,
) -> None:
    write_json(tmp_path / "fixture.json", valid_fixture())
    write_json(tmp_path / "registration.json", valid_registration())
    for name in ("m0", "h1"):
        runtime = tmp_path / name
        runtime.mkdir()
        (runtime / "SKILL.md").write_text(name, encoding="utf-8")
    registration = {
        "fixture": _identity_spec(tmp_path, "fixture.json"),
        "terminal_registration": _identity_spec(
            tmp_path,
            "registration.json",
        ),
        "case_id": "Q01",
        "runtime_pointer": "/runtime",
        "runtimes": {
            name: _identity_spec(tmp_path, name, "campaign-tree-v1")
            for name in ("m0", "h1")
        },
    }

    result = campaign_artifacts.build_behavioral_payloads(
        registration,
        candidate_root=tmp_path,
        output_root=tmp_path / ".tmp" / "payloads",
    )
    m0 = json.loads(Path(result["payloads"]["m0"]["path"]).read_text("utf-8"))
    h1 = json.loads(Path(result["payloads"]["h1"]["path"]).read_text("utf-8"))
    assert m0.pop("runtime") != h1.pop("runtime")
    assert m0 == h1 == valid_case()
    assert result["shared_payload_sha256"] == hashlib.sha256(
        json.dumps(
            valid_case(),
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def test_result_envelope_rejects_foreign_candidate_and_cached_fresh_sample(
    tmp_path: Path,
) -> None:
    envelope = {
        "schema_version": 1,
        "case_id": "Q01",
        "arm": "h1",
        "candidate_root": str(tmp_path.resolve()),
        "candidate_identity": "a" * 64,
        "fixture_identity": "b" * 64,
        "dispatch_payload_sha256": "c" * 64,
        "fresh": True,
        "output": {"artifact": "sample-1"},
    }
    campaign_artifacts.lint_result_envelope(
        envelope,
        case_id="Q01",
        arm="h1",
        candidate_root=tmp_path,
        candidate_identity="a" * 64,
        fixture_identity="b" * 64,
        dispatch_payload_sha256="c" * 64,
        require_fresh=True,
    )

    envelope["candidate_identity"] = "d" * 64
    with pytest.raises(ValueError, match="candidate identity"):
        campaign_artifacts.lint_result_envelope(
            envelope,
            case_id="Q01",
            arm="h1",
            candidate_root=tmp_path,
            candidate_identity="a" * 64,
            fixture_identity="b" * 64,
            dispatch_payload_sha256="c" * 64,
            require_fresh=True,
        )
    envelope["candidate_identity"] = "a" * 64
    envelope["candidate_root"] = str((tmp_path / "foreign").resolve())
    with pytest.raises(ValueError, match="candidate root"):
        campaign_artifacts.lint_result_envelope(
            envelope,
            case_id="Q01",
            arm="h1",
            candidate_root=tmp_path,
            candidate_identity="a" * 64,
            fixture_identity="b" * 64,
            dispatch_payload_sha256="c" * 64,
            require_fresh=True,
        )
    envelope["candidate_root"] = str(tmp_path.resolve())
    envelope["fresh"] = False
    with pytest.raises(ValueError, match="fresh"):
        campaign_artifacts.lint_result_envelope(
            envelope,
            case_id="Q01",
            arm="h1",
            candidate_root=tmp_path,
            candidate_identity="a" * 64,
            fixture_identity="b" * 64,
            dispatch_payload_sha256="c" * 64,
            require_fresh=True,
        )
    envelope.pop("output")
    with pytest.raises(ValueError, match="fields"):
        campaign_artifacts.lint_result_envelope(
            envelope,
            case_id="Q01",
            arm="h1",
            candidate_root=tmp_path,
            candidate_identity="a" * 64,
            fixture_identity="b" * 64,
            dispatch_payload_sha256="c" * 64,
            require_fresh=False,
        )


@pytest.mark.parametrize(
    ("name", "content", "message"),
    [
        ("broken.md", "[missing](nope.md)\n", "local link"),
        ("anchor.md", "[missing](#nope)\n", "anchor"),
        ("fence.md", "```python\npass\n", "fence"),
        ("table.md", "| A | B |\n| --- | --- |\n| 1 |\n", "table"),
        ("space.md", "trailing \n", "trailing whitespace"),
        ("break.md", "hard break  \n", "hard break"),
    ],
)
def test_lint_markdown_rejects_named_structural_defects(
    tmp_path: Path,
    name: str,
    content: str,
    message: str,
) -> None:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match=message):
        campaign_artifacts.lint_markdown(
            path,
            candidate_root=tmp_path,
            hard_break_policy="forbid",
        )


def test_lint_markdown_accepts_local_links_anchors_tables_and_allowed_breaks(
    tmp_path: Path,
) -> None:
    (tmp_path / "target.md").write_text("# Target Heading\n", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text(
        "# Source\n\n"
        "[local](target.md#target-heading)\n\n"
        "| A | B |\n"
        "| --- | --- |\n"
        "| 1 | 2 |\n\n"
        "allowed break  \n"
        "next line\n",
        encoding="utf-8",
        newline="\n",
    )
    result = campaign_artifacts.lint_markdown(
        source,
        candidate_root=tmp_path,
        hard_break_policy="allow",
    )
    assert result["status"] == "ok"


def _valid_research_registry(root: Path) -> dict[str, object]:
    capture_root = root / "capture"
    capture_root.mkdir()
    capture = capture_root / "source.md"
    capture.write_text("# Evidence\n", encoding="utf-8")
    return {
        "schema_version": 1,
        "claims": [{"id": "C1", "evidence": ["E1"]}],
        "evidence": [
            {
                "id": "E1",
                "claim_ids": ["C1"],
                "pointer": "capture/source.md#evidence",
                "capture": _identity_spec(root, "capture", "campaign-tree-v1"),
                "revision": "rev-1",
                "url": "https://example.com/source",
                "classification": "primary",
                "limitations": ["Bounded to the inspected revision."],
            }
        ],
    }


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda value: value["claims"][0].update(evidence=["E404"]), "evidence pointer"),
        (lambda value: value["evidence"][0].pop("revision"), "revision"),
        (lambda value: value["evidence"][0].update(url="not-a-url"), "URL"),
        (lambda value: value["evidence"][0].pop("classification"), "classification"),
        (lambda value: value["evidence"][0].update(limitations=[]), "limitations"),
        (
            lambda value: value["evidence"][0]["capture"].update(digest="0" * 64),
            "capture identity",
        ),
        (
            lambda value: value["claims"].append(
                {"id": "C2", "evidence": ["E1"]}
            ),
            "bidirectional",
        ),
    ],
)
def test_lint_research_registry_rejects_structural_defects(
    tmp_path: Path,
    mutate: object,
    message: str,
) -> None:
    registry = _valid_research_registry(tmp_path)
    assert callable(mutate)
    mutate(registry)
    write_json(tmp_path / "registry.json", registry)
    with pytest.raises(ValueError, match=message):
        campaign_artifacts.lint_research_registry(
            tmp_path / "registry.json",
            candidate_root=tmp_path,
        )


def test_prompt3_verify_requires_registered_preflight_before_proof(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-3"
    write_json(manifest_path, manifest)
    monkeypatch.setattr(
        campaign_artifacts,
        "_verify_registered_proof",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("preflight must fail before proof")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert result["status"] == "failed"
    assert result["gate"] == "preflight-registration"


def _start_preflight_campaign(
    worktree: Path,
    *,
    stage: str,
    registrations: list[dict[str, object]],
) -> Path:
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = stage
    manifest["mechanical"]["preflight_registrations"] = registrations
    write_json(manifest_path, manifest)
    return manifest_path


def _behavioral_preflight_registration(
    worktree: Path,
    *,
    applicability: str = "required",
) -> dict[str, object]:
    write_json(worktree / "fixture.json", valid_fixture())
    write_json(worktree / "registration.json", valid_registration())
    for name in ("m0", "h1"):
        runtime = worktree / name
        runtime.mkdir()
        (runtime / "SKILL.md").write_text(name, encoding="utf-8")
    return {
        "id": "prompt3-comparison",
        "kind": "behavioral-comparison",
        "stage": "prompt-3",
        "applicability": applicability,
        "decision_pointer": "decisions.md#prompt3-comparison",
        "candidate_root": ".",
        "fixture": _identity_spec(worktree, "fixture.json"),
        "terminal_registration": _identity_spec(
            worktree,
            "registration.json",
        ),
        "case_id": "Q01",
        "runtime_pointer": "/runtime",
        "runtimes": {
            name: _identity_spec(worktree, name, "campaign-tree-v1")
            for name in ("m0", "h1")
        },
    }


def _not_applicable_preflight(kind: str, stage: str) -> dict[str, object]:
    registration_id = f"{stage}-{kind}"
    return {
        "id": registration_id,
        "kind": kind,
        "stage": stage,
        "applicability": "not-applicable",
        "decision_pointer": f"decisions.md#{registration_id}",
    }


def test_prompt3_verify_generates_isolated_payloads_before_proof(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    registration = _behavioral_preflight_registration(worktree)
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-3",
        registrations=[
            registration,
            _not_applicable_preflight("markdown", "prompt-3"),
        ],
    )
    monkeypatch.setattr(
        campaign_artifacts,
        "_verify_registered_proof",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("no proof was registered")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    payload_root = (
        worktree
        / ".tmp"
        / "campaign-payloads"
        / "review-epoch-1"
        / "prompt3-comparison"
    )
    m0 = json.loads((payload_root / "Q01-m0.json").read_text("utf-8"))
    h1 = json.loads((payload_root / "Q01-h1.json").read_text("utf-8"))
    assert result["status"] == "verified"
    assert result["preflight"]["completed"] == ["prompt3-comparison"]
    assert result["preflight"]["not_applicable"] == ["prompt-3-markdown"]
    assert m0.pop("runtime") != h1.pop("runtime")
    assert m0 == h1 == valid_case()


def test_prompt3_verify_accepts_explicit_no_comparison_applicability(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-3",
        registrations=[
            _not_applicable_preflight(
                "behavioral-comparison",
                "prompt-3",
            ),
            _not_applicable_preflight("markdown", "prompt-3"),
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert result["status"] == "verified"
    assert result["preflight"]["not_applicable"] == [
        "prompt-3-behavioral-comparison",
        "prompt-3-markdown",
    ]


def test_prompt3_verify_rejects_omitted_markdown_applicability(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    (worktree / "changed.md").write_text(
        "[broken](missing.md)\n",
        encoding="utf-8",
    )
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-3",
        registrations=[_behavioral_preflight_registration(worktree)],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert result["status"] == "failed"
    assert result["gate"] == "preflight-registration"


def test_prompt3_verify_rejects_contaminated_fixture_before_proof(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    registration = _behavioral_preflight_registration(worktree)
    fixture = json.loads((worktree / "fixture.json").read_text("utf-8"))
    fixture["cases"][0]["expected_terminal"] = "preferred"
    write_json(worktree / "fixture.json", fixture)
    registration["fixture"] = _identity_spec(worktree, "fixture.json")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-3",
        registrations=[
            registration,
            _not_applicable_preflight("markdown", "prompt-3"),
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "root-only fields" in result["failures"][0]["message"]


def test_prompt3_verify_rejects_missing_terminal_registration_and_fixture_fact(
    tmp_path: Path,
) -> None:
    for name, mutate in (
        (
            "missing-registration",
            lambda registration, fixture: registration.pop(
                "terminal_registration"
            ),
        ),
        (
            "missing-fact",
            lambda registration, fixture: fixture["cases"][0].pop(
                "requested_output"
            ),
        ),
    ):
        worktree = tmp_path / name
        worktree.mkdir()
        registration = _behavioral_preflight_registration(worktree)
        fixture = json.loads((worktree / "fixture.json").read_text("utf-8"))
        mutate(registration, fixture)
        write_json(worktree / "fixture.json", fixture)
        registration["fixture"] = _identity_spec(worktree, "fixture.json")
        manifest_path = _start_preflight_campaign(
            worktree,
            stage="prompt-3",
            registrations=[
                registration,
                _not_applicable_preflight("markdown", "prompt-3"),
            ],
        )
        result = campaign_artifacts.verify_campaign(
            manifest_path,
            worktree=worktree,
        )
        assert result["status"] == "failed"
        assert result["gate"] == "preflight-validation"


def test_lint_markdown_rejects_non_utf8_and_bom(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.md"
    invalid.write_bytes(b"\xff")
    with pytest.raises(ValueError, match="encoding"):
        campaign_artifacts.lint_markdown(
            invalid,
            candidate_root=tmp_path,
            hard_break_policy="forbid",
        )
    invalid.write_bytes(b"\xef\xbb\xbf# Heading\n")
    with pytest.raises(ValueError, match="BOM"):
        campaign_artifacts.lint_markdown(
            invalid,
            candidate_root=tmp_path,
            hard_break_policy="forbid",
        )


def test_lint_markdown_requires_equal_or_longer_closing_fence(
    tmp_path: Path,
) -> None:
    document = tmp_path / "fences.md"
    document.write_text(
        "````python\n"
        "```\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="fence"):
        campaign_artifacts.lint_markdown(
            document,
            candidate_root=tmp_path,
            hard_break_policy="forbid",
        )

    document.write_text(
        "````python\n"
        "```\n"
        "`````\n",
        encoding="utf-8",
    )
    assert campaign_artifacts.lint_markdown(
        document,
        candidate_root=tmp_path,
        hard_break_policy="forbid",
    )["status"] == "ok"


def test_lint_research_registry_accepts_exact_local_provenance(
    tmp_path: Path,
) -> None:
    registry = _valid_research_registry(tmp_path)
    write_json(tmp_path / "registry.json", registry)
    result = campaign_artifacts.lint_research_registry(
        tmp_path / "registry.json",
        candidate_root=tmp_path,
    )
    assert result == {"status": "ok", "claim_count": 1, "evidence_count": 1}


def test_verify_runs_applicable_markdown_and_research_preflights(
    tmp_path: Path,
) -> None:
    markdown_worktree = tmp_path / "markdown"
    markdown_worktree.mkdir()
    document_root = markdown_worktree / "documents"
    document_root.mkdir()
    (document_root / "target.md").write_text("# Target\n", encoding="utf-8")
    (document_root / "source.md").write_text(
        "[target](target.md#target)\n",
        encoding="utf-8",
    )
    registrations = [
        _behavioral_preflight_registration(markdown_worktree),
        {
            "id": "markdown-documents",
            "kind": "markdown",
            "stage": "prompt-3",
            "applicability": "required",
            "decision_pointer": "decisions.md#markdown-documents",
            "candidate_root": ".",
            "target": _identity_spec(
                markdown_worktree,
                "documents",
                "campaign-tree-v1",
            ),
            "paths": ["documents/source.md", "documents/target.md"],
            "hard_break_policy": "forbid",
        },
    ]
    markdown_manifest = _start_preflight_campaign(
        markdown_worktree,
        stage="prompt-3",
        registrations=registrations,
    )
    markdown_result = campaign_artifacts.verify_campaign(
        markdown_manifest,
        worktree=markdown_worktree,
    )
    assert markdown_result["status"] == "verified"
    assert markdown_result["preflight"]["completed"] == [
        "prompt3-comparison",
        "markdown-documents",
    ]

    research_worktree = tmp_path / "research"
    research_worktree.mkdir()
    registry = _valid_research_registry(research_worktree)
    write_json(research_worktree / "registry.json", registry)
    research_registration = {
        "id": "research-registry",
        "kind": "research",
        "stage": "research",
        "applicability": "required",
        "decision_pointer": "decisions.md#research-registry",
        "candidate_root": ".",
        "registry": _identity_spec(research_worktree, "registry.json"),
    }
    research_manifest = _start_preflight_campaign(
        research_worktree,
        stage="research",
        registrations=[
            research_registration,
            _not_applicable_preflight("markdown", "research"),
        ],
    )
    research_result = campaign_artifacts.verify_campaign(
        research_manifest,
        worktree=research_worktree,
    )
    assert research_result["status"] == "verified"
    assert research_result["preflight"]["completed"] == ["research-registry"]
    assert research_result["preflight"]["not_applicable"] == [
        "research-markdown"
    ]


def test_research_verify_requires_registration_and_rejects_dangling_pointer(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "missing"
    worktree.mkdir()
    missing_manifest = _start_preflight_campaign(
        worktree,
        stage="research",
        registrations=[],
    )
    missing = campaign_artifacts.verify_campaign(
        missing_manifest,
        worktree=worktree,
    )
    assert missing["gate"] == "preflight-registration"

    worktree = tmp_path / "dangling"
    worktree.mkdir()
    registry = _valid_research_registry(worktree)
    registry["evidence"][0]["pointer"] = "capture/source.md#missing"
    write_json(worktree / "registry.json", registry)
    registration = {
        "id": "research-registry",
        "kind": "research",
        "stage": "research",
        "applicability": "required",
        "decision_pointer": "decisions.md#research-registry",
        "candidate_root": ".",
        "registry": _identity_spec(worktree, "registry.json"),
    }
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="research",
        registrations=[
            registration,
            _not_applicable_preflight("markdown", "research"),
        ],
    )
    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert result["gate"] == "preflight-validation"
    assert "dangling" in result["failures"][0]["message"]


def test_research_verify_wraps_malformed_claim_ids_and_restores(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    registry = _valid_research_registry(worktree)
    registry["evidence"][0]["claim_ids"] = None
    registry_path = worktree / "registry.json"
    write_json(registry_path, registry)
    registration = {
        "id": "research-registry",
        "kind": "research",
        "stage": "research",
        "applicability": "required",
        "decision_pointer": "decisions.md#research-registry",
        "candidate_root": ".",
        "registry": _identity_spec(worktree, "registry.json"),
    }
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="research",
        registrations=[
            registration,
            _not_applicable_preflight("markdown", "research"),
        ],
    )

    malformed = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert malformed["status"] == "failed"
    assert malformed["gate"] == "preflight-validation"
    assert "bidirectional" in malformed["failures"][0]["message"]

    registry["evidence"][0]["claim_ids"] = ["C1"]
    write_json(registry_path, registry)
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["mechanical"]["preflight_registrations"][0][
        "registry"
    ] = _identity_spec(worktree, "registry.json")
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    restored = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert restored["status"] == "verified"
