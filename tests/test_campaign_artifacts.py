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
