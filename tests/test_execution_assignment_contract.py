from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import re
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "skills/custom/implement/scripts/execution_assignment.py"
)


def load_contract() -> ModuleType:
    assert CONTRACT_PATH.is_file(), "the implement-owned validator is missing"
    spec = importlib.util.spec_from_file_location("execution_assignment", CONTRACT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_assignment() -> dict[str, object]:
    capsule_bytes = b'{"ticket":"#66"}'
    return {
        "schema_version": 1,
        "kind": "execution-assignment",
        "assignment_id": "assignment-66-1",
        "source": {"id": "issue-65", "sha256": "a" * 64},
        "parent": {"id": "issue-65", "sha256": "b" * 64},
        "ticket": {"id": "issue-66", "sha256": "c" * 64},
        "attempt_id": "attempt-1",
        "actor_id": "actor-1",
        "base": {
            "repository": "stevennitesh/programming-agent-skills",
            "head": "d" * 40,
        },
        "checkout": {"path": r"E:\pi\pas-001\wt\assignment-66-1"},
        "dependencies": {"status": "ready", "blockers": []},
        "claim": {
            "status": "claimed",
            "owner": "stevennitesh",
            "token": "claim-66",
        },
        "requested_profile": {
            "id": "clear-worker",
            "agent_type": "luna_max",
            "model": "gpt-5.6-luna",
            "reasoning_effort": "max",
        },
        "capsule": {
            "id": "capsule-1",
            "sha256": hashlib.sha256(capsule_bytes).hexdigest(),
            "encoding": "base64",
            "bytes": base64.b64encode(capsule_bytes).decode("ascii"),
        },
        "write_scope": ["skills/custom/implement/"],
        "exclusions": [
            "CONTEXT.md",
            "docs/adr/",
            "skills/custom/implement/generated/",
        ],
        "permissions": [
            "read-repository",
            "write-authorized-scope",
            "run-proof",
        ],
        "proof_obligations": ["assignment schema", "authority rejection"],
        "return_policy": {
            "allowed_statuses": [
                "done",
                "blocker",
                "needs-feedback",
                "transport/binding-failure",
            ],
            "delivery_completion": False,
        },
        "failure_policy": {
            "contradiction": "needs-feedback",
            "authority_gap": "blocker",
            "transport_mismatch": "transport/binding-failure",
        },
    }


def test_execution_assignment_accepts_exact_versioned_packet_without_mutation() -> None:
    contract = load_contract()
    packet = valid_assignment()
    before = copy.deepcopy(packet)

    assert contract.validate_execution_assignment(packet) is None
    assert packet == before


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda packet: packet.pop("permissions"), "missing fields: permissions"),
        (
            lambda packet: packet.__setitem__("delivery_complete", True),
            "unknown fields: delivery_complete",
        ),
        (
            lambda packet: packet.__setitem__("schema_version", 2),
            "unsupported schema_version",
        ),
        (
            lambda packet: packet["source"].__setitem__("sha256", "not-a-hash"),
            "source.sha256",
        ),
        (
            lambda packet: packet["claim"].__setitem__("tracker_closeout", True),
            "claim unknown fields: tracker_closeout",
        ),
        (
            lambda packet: packet.__setitem__("write_scope", []),
            "write_scope must be a non-empty list",
        ),
        (
            lambda packet: packet["return_policy"].__setitem__(
                "allowed_statuses", ["done"]
            ),
            "return_policy.allowed_statuses",
        ),
    ],
)
def test_execution_assignment_rejects_incomplete_invalid_or_authority_widening_packets(
    mutate: object, message: str
) -> None:
    contract = load_contract()
    packet = valid_assignment()
    mutate(packet)

    with pytest.raises(contract.ContractValidationError, match=message):
        contract.validate_execution_assignment(packet)


def test_execution_assignment_rejects_capsule_byte_identity_mismatch() -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["capsule"]["bytes"] = base64.b64encode(b"different").decode("ascii")

    with pytest.raises(
        contract.ContractValidationError, match="capsule.sha256 does not match capsule.bytes"
    ):
        contract.validate_execution_assignment(packet)


def test_extra_delivery_authority_negative_control_restores_valid_assignment() -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["delivery_complete"] = True

    with pytest.raises(
        contract.ContractValidationError,
        match="unknown fields: delivery_complete",
    ):
        contract.validate_execution_assignment(packet)

    packet.pop("delivery_complete")
    assert contract.validate_execution_assignment(packet) is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "missing-worker"),
        ("agent_type", "default"),
        ("model", "gpt-5.6-sol"),
        ("reasoning_effort", "high"),
    ],
)
def test_execution_assignment_rejects_noncanonical_runtime_profile_binding(
    field: str, value: str
) -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["requested_profile"][field] = value

    with pytest.raises(
        contract.ContractValidationError,
        match="requested_profile does not match the canonical runtime profile",
    ):
        contract.validate_execution_assignment(packet)


@pytest.mark.parametrize("effort", ["medium", "high"])
def test_execution_assignment_accepts_canonical_serial_integrator_bindings(
    effort: str,
) -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["requested_profile"] = {
        "id": "serial-integrator",
        "agent_type": "default",
        "model": "gpt-5.6-sol",
        "reasoning_effort": effort,
    }

    assert contract.validate_execution_assignment(packet) is None


@pytest.mark.parametrize(
    "scope",
    [
        ["../outside"],
        ["/outside"],
        ["C:/outside"],
        ["skills/../outside"],
        [r"skills\custom\implement"],
    ],
)
def test_execution_assignment_rejects_noncanonical_or_external_write_scope(
    scope: list[str],
) -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["write_scope"] = scope

    with pytest.raises(contract.ContractValidationError, match="write_scope"):
        contract.validate_execution_assignment(packet)


def test_prohibited_permission_negative_control_restores_valid_assignment() -> None:
    contract = load_contract()
    packet = valid_assignment()
    packet["permissions"].append("close-tracker")

    with pytest.raises(
        contract.ContractValidationError,
        match="permissions must equal the canonical worker capabilities",
    ):
        contract.validate_execution_assignment(packet)

    packet["permissions"].pop()
    assert contract.validate_execution_assignment(packet) is None


@pytest.mark.parametrize("field", ["write_scope", "exclusions"])
def test_execution_assignment_rejects_nul_path_and_restores_valid_packet(
    field: str,
) -> None:
    contract = load_contract()
    packet = valid_assignment()
    original = packet[field][0]
    packet[field][0] = original + "\x00suffix"

    with pytest.raises(
        contract.ContractValidationError,
        match="canonical repository-relative POSIX path",
    ):
        contract.validate_execution_assignment(packet)

    packet[field][0] = original
    assert contract.validate_execution_assignment(packet) is None


def valid_worker_return(
    assignment: dict[str, object], status: str = "done"
) -> dict[str, object]:
    candidate_head = "e" * 40
    succeeded = status == "done"
    return {
        "schema_version": 1,
        "kind": "worker-return",
        "assignment_id": assignment["assignment_id"],
        "attempt_id": assignment["attempt_id"],
        "actor_id": assignment["actor_id"],
        "task_id": "provider-task-1",
        "status": status,
        "final_checkout": {
            "path": assignment["checkout"]["path"],
            "head": candidate_head if succeeded else assignment["base"]["head"],
            "clean": True,
        },
        "candidate": {"head": candidate_head} if succeeded else None,
        "acceptance_proof": (
            [
                {
                    "acceptance_id": "assignment schema",
                    "evidence": "focused contract test passed",
                },
                {
                    "acceptance_id": "authority rejection",
                    "evidence": "authority negative control passed",
                },
            ]
            if succeeded
            else []
        ),
        "scope_report": {
            "written_paths": [
                "skills/custom/implement/scripts/execution_assignment.py"
            ]
            if succeeded
            else [],
            "unrelated_work_preserved": True,
        },
        "risk_or_blocker": None if succeeded else f"{status} evidence",
        "recovery_owner": None if succeeded else "delivery coordinator",
    }


@pytest.mark.parametrize(
    "status",
    ["done", "blocker", "needs-feedback", "transport/binding-failure"],
)
def test_worker_return_accepts_only_the_four_bound_outcomes_without_mutation(
    status: str,
) -> None:
    contract = load_contract()
    assert hasattr(contract, "validate_worker_return"), "Worker Return validator is missing"
    assignment = valid_assignment()
    packet = valid_worker_return(assignment, status)
    before_assignment = copy.deepcopy(assignment)
    before_packet = copy.deepcopy(packet)

    assert contract.validate_worker_return(packet, assignment) is None
    assert assignment == before_assignment
    assert packet == before_packet


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda packet: packet.__setitem__("status", "complete"),
            "status must be one of",
        ),
        (
            lambda packet: packet.__setitem__("delivery_complete", True),
            "unknown fields: delivery_complete",
        ),
        (
            lambda packet: packet.__setitem__("assignment_id", "another-assignment"),
            "assignment_id does not match",
        ),
        (
            lambda packet: packet.__setitem__("attempt_id", "another-attempt"),
            "attempt_id does not match",
        ),
        (
            lambda packet: packet.__setitem__("actor_id", "another-actor"),
            "actor_id does not match",
        ),
        (
            lambda packet: packet.__setitem__("task_id", ""),
            "task_id must be a non-empty string",
        ),
        (
            lambda packet: packet["final_checkout"].__setitem__(
                "path", r"E:\pi\pas-001\wt\another-assignment"
            ),
            "final_checkout.path does not match",
        ),
        (
            lambda packet: packet.__setitem__("candidate", None),
            "done Return requires candidate",
        ),
        (
            lambda packet: packet["candidate"].__setitem__("head", "f" * 40),
            "candidate.head must equal final_checkout.head",
        ),
        (
            lambda packet: packet["final_checkout"].__setitem__("clean", False),
            "done Return requires a clean final checkout",
        ),
        (
            lambda packet: packet["scope_report"].__setitem__(
                "unrelated_work_preserved", False
            ),
            "done Return requires unrelated_work_preserved",
        ),
    ],
)
def test_done_worker_return_rejects_mismatch_or_extra_delivery_authority(
    mutate: object, message: str
) -> None:
    contract = load_contract()
    assert hasattr(contract, "validate_worker_return"), "Worker Return validator is missing"
    assignment = valid_assignment()
    packet = valid_worker_return(assignment)
    mutate(packet)

    with pytest.raises(contract.ContractValidationError, match=message):
        contract.validate_worker_return(packet, assignment)


@pytest.mark.parametrize("status", ["blocker", "needs-feedback", "transport/binding-failure"])
def test_non_done_worker_return_requires_evidence_and_recovery_owner(status: str) -> None:
    contract = load_contract()
    assert hasattr(contract, "validate_worker_return"), "Worker Return validator is missing"
    assignment = valid_assignment()
    packet = valid_worker_return(assignment, status)
    packet["risk_or_blocker"] = None

    with pytest.raises(
        contract.ContractValidationError,
        match=f"{re.escape(status)} Return requires risk_or_blocker",
    ):
        contract.validate_worker_return(packet, assignment)

    packet = valid_worker_return(assignment, status)
    packet["recovery_owner"] = None
    with pytest.raises(
        contract.ContractValidationError,
        match=f"{re.escape(status)} Return requires recovery_owner",
    ):
        contract.validate_worker_return(packet, assignment)


@pytest.mark.parametrize("mode", ["missing", "unknown", "duplicate"])
def test_done_worker_return_requires_exact_complete_proof_mapping(mode: str) -> None:
    contract = load_contract()
    assignment = valid_assignment()
    packet = valid_worker_return(assignment)

    if mode == "missing":
        packet["acceptance_proof"].pop()
    elif mode == "unknown":
        packet["acceptance_proof"][0]["acceptance_id"] = "unassigned proof"
    else:
        packet["acceptance_proof"].append(
            copy.deepcopy(packet["acceptance_proof"][0])
        )

    expected = {
        "missing": "done Return missing proof obligations",
        "unknown": "acceptance_proof contains unassigned acceptance_id",
        "duplicate": "acceptance_proof contains duplicate acceptance_id",
    }[mode]
    with pytest.raises(contract.ContractValidationError, match=expected):
        contract.validate_worker_return(packet, assignment)


@pytest.mark.parametrize(
    "written_path",
    [
        "skills/custom/parallel-implement/SKILL.md",
        "../outside.txt",
        "/outside.txt",
        "C:/outside.txt",
        "docs/adr/0012.md",
        "skills/custom/implement/generated/cache.json",
    ],
)
def test_worker_return_rejects_noncanonical_out_of_scope_or_excluded_write(
    written_path: str,
) -> None:
    contract = load_contract()
    assignment = valid_assignment()
    packet = valid_worker_return(assignment)
    packet["scope_report"]["written_paths"] = [written_path]

    with pytest.raises(contract.ContractValidationError, match="written_paths"):
        contract.validate_worker_return(packet, assignment)


def test_worker_return_scope_negative_control_restores_valid_packet() -> None:
    contract = load_contract()
    assignment = valid_assignment()
    packet = valid_worker_return(assignment)
    valid_path = packet["scope_report"]["written_paths"][0]
    packet["scope_report"]["written_paths"] = ["docs/adr/0012.md"]

    with pytest.raises(
        contract.ContractValidationError,
        match=r"written_paths\[0\] is outside write_scope",
    ):
        contract.validate_worker_return(packet, assignment)

    packet["scope_report"]["written_paths"] = [valid_path]
    assert contract.validate_worker_return(packet, assignment) is None


def test_worker_return_rejects_nul_written_path_and_restores_valid_packet() -> None:
    contract = load_contract()
    assignment = valid_assignment()
    packet = valid_worker_return(assignment)
    valid_path = packet["scope_report"]["written_paths"][0]
    packet["scope_report"]["written_paths"] = [valid_path + "\x00suffix"]

    with pytest.raises(
        contract.ContractValidationError,
        match="canonical repository-relative POSIX path",
    ):
        contract.validate_worker_return(packet, assignment)

    packet["scope_report"]["written_paths"] = [valid_path]
    assert contract.validate_worker_return(packet, assignment) is None
