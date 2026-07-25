from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from scripts import campaign_artifacts


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


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
