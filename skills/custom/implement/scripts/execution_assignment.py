"""Strict validation for the implement-owned delegated execution contract."""

from __future__ import annotations

import base64
import binascii
import hashlib
import importlib.util
import re
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
RETURN_STATUSES = (
    "done",
    "blocker",
    "needs-feedback",
    "transport/binding-failure",
)
WORKER_PERMISSIONS = (
    "read-repository",
    "write-authorized-scope",
    "run-proof",
)

ASSIGNMENT_FIELDS = {
    "schema_version",
    "kind",
    "assignment_id",
    "source",
    "parent",
    "ticket",
    "attempt_id",
    "actor_id",
    "base",
    "checkout",
    "dependencies",
    "claim",
    "requested_profile",
    "capsule",
    "write_scope",
    "exclusions",
    "permissions",
    "proof_obligations",
    "return_policy",
    "failure_policy",
}
WORKER_RETURN_FIELDS = {
    "schema_version",
    "kind",
    "assignment_id",
    "attempt_id",
    "actor_id",
    "task_id",
    "status",
    "final_checkout",
    "candidate",
    "acceptance_proof",
    "scope_report",
    "risk_or_blocker",
    "recovery_owner",
}


class ContractValidationError(ValueError):
    """The packet does not satisfy the shared execution contract."""


def _mapping(value: object, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractValidationError(f"{path} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise ContractValidationError(f"{path} field names must be strings")
    return value


def _exact_fields(
    value: object, expected: set[str], path: str
) -> Mapping[str, Any]:
    packet = _mapping(value, path)
    missing = sorted(expected - set(packet))
    unknown = sorted(set(packet) - expected)
    if missing:
        raise ContractValidationError(f"{path} missing fields: {', '.join(missing)}")
    if unknown:
        raise ContractValidationError(f"{path} unknown fields: {', '.join(unknown)}")
    return packet


def _string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContractValidationError(f"{path} must be a non-empty string")
    return value


def _sha256(value: object, path: str) -> str:
    digest = _string(value, path)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ContractValidationError(f"{path} must be a lowercase SHA-256")
    return digest


def _commit(value: object, path: str) -> str:
    commit = _string(value, path)
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ContractValidationError(f"{path} must be a lowercase Git commit")
    return commit


def _string_list(value: object, path: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise ContractValidationError(f"{path} must be {qualifier} of non-empty strings")
    if not all(isinstance(item, str) and item for item in value):
        raise ContractValidationError(f"{path} must contain only non-empty strings")
    return value


def _unique_string_list(
    value: object, path: str, *, allow_empty: bool = False
) -> list[str]:
    items = _string_list(value, path, allow_empty=allow_empty)
    if len(set(items)) != len(items):
        raise ContractValidationError(f"{path} must not contain duplicates")
    return items


def _repository_scope_list(value: object, path: str) -> list[str]:
    entries = _unique_string_list(value, path)
    for index, entry in enumerate(entries):
        _repository_path(entry, f"{path}[{index}]", allow_directory=True)
    return entries


def _repository_path(value: object, path: str, *, allow_directory: bool) -> str:
    raw = _string(value, path)
    directory = raw.endswith("/")
    candidate = raw[:-1] if directory else raw
    if (
        not candidate
        or raw.startswith("/")
        or "\\" in raw
        or "//" in raw
        or ":" in raw
        or "\x00" in raw
        or any(part in {"", ".", ".."} for part in candidate.split("/"))
    ):
        raise ContractValidationError(
            f"{path} must be a canonical repository-relative POSIX path"
        )
    if directory and not allow_directory:
        raise ContractValidationError(f"{path} must identify a file, not a directory")
    return raw


def _path_is_within(path: str, scope: str) -> bool:
    if scope.endswith("/"):
        return path.startswith(scope)
    return path == scope


@lru_cache(maxsize=1)
def _runtime_profile_resolver() -> Any:
    resolver_path = (
        Path(__file__).resolve().parents[2]
        / "parallel-implement/scripts/run_ledger.py"
    )
    spec = importlib.util.spec_from_file_location(
        "_execution_assignment_runtime_resolver", resolver_path
    )
    if spec is None or spec.loader is None:
        raise ContractValidationError("canonical runtime profile resolver is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    profiles = module.runtime_profiles()
    if not isinstance(profiles, Mapping):
        raise ContractValidationError("canonical runtime profile resolver is invalid")
    if not callable(getattr(module, "runtime_profile_matches", None)):
        raise ContractValidationError("canonical runtime profile matcher is unavailable")
    return module


def _identity(value: object, path: str) -> None:
    identity = _exact_fields(value, {"id", "sha256"}, path)
    _string(identity["id"], f"{path}.id")
    _sha256(identity["sha256"], f"{path}.sha256")


def _optional_string(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _string(value, path)


def validate_execution_assignment(packet: object) -> None:
    """Validate one assignment without mutating or normalizing its bytes."""

    assignment = _exact_fields(packet, ASSIGNMENT_FIELDS, "execution assignment")
    version = assignment["schema_version"]
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        raise ContractValidationError(
            f"unsupported schema_version: expected {SCHEMA_VERSION}; "
            "return to the implement contract owner for recovery"
        )
    if assignment["kind"] != "execution-assignment":
        raise ContractValidationError("kind must be execution-assignment")

    _string(assignment["assignment_id"], "assignment_id")
    _identity(assignment["source"], "source")
    _identity(assignment["parent"], "parent")
    _identity(assignment["ticket"], "ticket")
    _string(assignment["attempt_id"], "attempt_id")
    _string(assignment["actor_id"], "actor_id")

    base = _exact_fields(assignment["base"], {"repository", "head"}, "base")
    _string(base["repository"], "base.repository")
    _commit(base["head"], "base.head")

    checkout = _exact_fields(assignment["checkout"], {"path"}, "checkout")
    _string(checkout["path"], "checkout.path")

    dependencies = _exact_fields(
        assignment["dependencies"], {"status", "blockers"}, "dependencies"
    )
    if dependencies["status"] != "ready":
        raise ContractValidationError("dependencies.status must be ready")
    blockers = dependencies["blockers"]
    if not isinstance(blockers, list):
        raise ContractValidationError("dependencies.blockers must be a list")
    for index, blocker in enumerate(blockers):
        _identity(blocker, f"dependencies.blockers[{index}]")
    if blockers:
        raise ContractValidationError(
            "dependencies.blockers must be empty when dependencies.status is ready"
        )

    claim = _exact_fields(assignment["claim"], {"status", "owner", "token"}, "claim")
    if claim["status"] != "claimed":
        raise ContractValidationError("claim.status must be claimed")
    _string(claim["owner"], "claim.owner")
    _string(claim["token"], "claim.token")

    profile = _exact_fields(
        assignment["requested_profile"],
        {"id", "agent_type", "model", "reasoning_effort"},
        "requested_profile",
    )
    for field in ("id", "agent_type", "model", "reasoning_effort"):
        _string(profile[field], f"requested_profile.{field}")
    resolver = _runtime_profile_resolver()
    if not resolver.runtime_profile_matches(
        profile["id"],
        profile["agent_type"],
        profile["model"],
        profile["reasoning_effort"],
    ):
        raise ContractValidationError(
            "requested_profile does not match the canonical runtime profile"
        )

    capsule = _exact_fields(
        assignment["capsule"],
        {"id", "sha256", "encoding", "bytes"},
        "capsule",
    )
    _string(capsule["id"], "capsule.id")
    capsule_sha256 = _sha256(capsule["sha256"], "capsule.sha256")
    if capsule["encoding"] != "base64":
        raise ContractValidationError("capsule.encoding must be base64")
    encoded = _string(capsule["bytes"], "capsule.bytes")
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ContractValidationError("capsule.bytes must be valid base64") from error
    if not decoded:
        raise ContractValidationError("capsule.bytes must decode to non-empty bytes")
    if hashlib.sha256(decoded).hexdigest() != capsule_sha256:
        raise ContractValidationError("capsule.sha256 does not match capsule.bytes")

    _repository_scope_list(assignment["write_scope"], "write_scope")
    _repository_scope_list(assignment["exclusions"], "exclusions")
    if assignment["permissions"] != list(WORKER_PERMISSIONS):
        raise ContractValidationError(
            "permissions must equal the canonical worker capabilities"
        )
    _unique_string_list(assignment["proof_obligations"], "proof_obligations")

    return_policy = _exact_fields(
        assignment["return_policy"],
        {"allowed_statuses", "delivery_completion"},
        "return_policy",
    )
    if return_policy["allowed_statuses"] != list(RETURN_STATUSES):
        raise ContractValidationError(
            "return_policy.allowed_statuses must contain the canonical statuses in order"
        )
    if return_policy["delivery_completion"] is not False:
        raise ContractValidationError("return_policy.delivery_completion must be false")

    failure_policy = _exact_fields(
        assignment["failure_policy"],
        {"contradiction", "authority_gap", "transport_mismatch"},
        "failure_policy",
    )
    expected_failure_policy = {
        "contradiction": "needs-feedback",
        "authority_gap": "blocker",
        "transport_mismatch": "transport/binding-failure",
    }
    if dict(failure_policy) != expected_failure_policy:
        raise ContractValidationError("failure_policy must match the canonical policy")


def validate_worker_return(packet: object, assignment_packet: object) -> None:
    """Validate one Return against the exact assignment that authorized it."""

    validate_execution_assignment(assignment_packet)
    assignment = _mapping(assignment_packet, "execution assignment")
    worker_return = _exact_fields(packet, WORKER_RETURN_FIELDS, "Worker Return")

    version = worker_return["schema_version"]
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        raise ContractValidationError(
            f"unsupported schema_version: expected {SCHEMA_VERSION}; "
            "return to the implement contract owner for recovery"
        )
    if worker_return["kind"] != "worker-return":
        raise ContractValidationError("kind must be worker-return")

    for field in ("assignment_id", "attempt_id", "actor_id"):
        actual = _string(worker_return[field], field)
        if actual != assignment[field]:
            raise ContractValidationError(f"{field} does not match the assignment")
    _string(worker_return["task_id"], "task_id")

    status = worker_return["status"]
    if status not in RETURN_STATUSES:
        raise ContractValidationError(
            "status must be one of: " + ", ".join(RETURN_STATUSES)
        )

    final_checkout = _exact_fields(
        worker_return["final_checkout"],
        {"path", "head", "clean"},
        "final_checkout",
    )
    final_path = _string(final_checkout["path"], "final_checkout.path")
    assignment_checkout = _mapping(assignment["checkout"], "checkout")
    if final_path != assignment_checkout["path"]:
        raise ContractValidationError(
            "final_checkout.path does not match the assignment checkout"
        )
    final_head = _commit(final_checkout["head"], "final_checkout.head")
    if not isinstance(final_checkout["clean"], bool):
        raise ContractValidationError("final_checkout.clean must be a boolean")

    candidate_value = worker_return["candidate"]
    candidate: Mapping[str, Any] | None = None
    if candidate_value is not None:
        candidate = _exact_fields(candidate_value, {"head"}, "candidate")
        candidate_head = _commit(candidate["head"], "candidate.head")
        if candidate_head != final_head:
            raise ContractValidationError(
                "candidate.head must equal final_checkout.head"
            )

    proof_value = worker_return["acceptance_proof"]
    if not isinstance(proof_value, list):
        raise ContractValidationError("acceptance_proof must be a list")
    seen_acceptance: set[str] = set()
    for index, row_value in enumerate(proof_value):
        row = _exact_fields(
            row_value,
            {"acceptance_id", "evidence"},
            f"acceptance_proof[{index}]",
        )
        acceptance_id = _string(
            row["acceptance_id"], f"acceptance_proof[{index}].acceptance_id"
        )
        _string(row["evidence"], f"acceptance_proof[{index}].evidence")
        if acceptance_id in seen_acceptance:
            raise ContractValidationError(
                f"acceptance_proof contains duplicate acceptance_id: {acceptance_id}"
            )
        seen_acceptance.add(acceptance_id)

    assigned_proof = set(
        _unique_string_list(assignment["proof_obligations"], "proof_obligations")
    )
    unknown_proof = sorted(seen_acceptance - assigned_proof)
    if unknown_proof:
        raise ContractValidationError(
            "acceptance_proof contains unassigned acceptance_id: "
            + ", ".join(unknown_proof)
        )

    scope_report = _exact_fields(
        worker_return["scope_report"],
        {"written_paths", "unrelated_work_preserved"},
        "scope_report",
    )
    written_paths = _string_list(
        scope_report["written_paths"], "scope_report.written_paths", allow_empty=True
    )
    write_scope = _repository_scope_list(assignment["write_scope"], "write_scope")
    exclusions = _repository_scope_list(assignment["exclusions"], "exclusions")
    for index, written_path_value in enumerate(written_paths):
        written_path = _repository_path(
            written_path_value,
            f"scope_report.written_paths[{index}]",
            allow_directory=False,
        )
        if not any(_path_is_within(written_path, scope) for scope in write_scope):
            raise ContractValidationError(
                f"scope_report.written_paths[{index}] is outside write_scope"
            )
        if any(_path_is_within(written_path, exclusion) for exclusion in exclusions):
            raise ContractValidationError(
                f"scope_report.written_paths[{index}] is excluded"
            )
    unrelated_preserved = scope_report["unrelated_work_preserved"]
    if not isinstance(unrelated_preserved, bool):
        raise ContractValidationError(
            "scope_report.unrelated_work_preserved must be a boolean"
        )

    risk_or_blocker = _optional_string(
        worker_return["risk_or_blocker"], "risk_or_blocker"
    )
    recovery_owner = _optional_string(
        worker_return["recovery_owner"], "recovery_owner"
    )

    if status == "done":
        if candidate is None:
            raise ContractValidationError("done Return requires candidate")
        if final_checkout["clean"] is not True:
            raise ContractValidationError("done Return requires a clean final checkout")
        if not proof_value:
            raise ContractValidationError("done Return requires acceptance_proof")
        missing_proof = sorted(assigned_proof - seen_acceptance)
        if missing_proof:
            raise ContractValidationError(
                "done Return missing proof obligations: " + ", ".join(missing_proof)
            )
        if not written_paths:
            raise ContractValidationError("done Return requires written_paths")
        if unrelated_preserved is not True:
            raise ContractValidationError(
                "done Return requires unrelated_work_preserved"
            )
        if risk_or_blocker is not None or recovery_owner is not None:
            raise ContractValidationError(
                "done Return cannot include risk_or_blocker or recovery_owner"
            )
        return

    if risk_or_blocker is None:
        raise ContractValidationError(f"{status} Return requires risk_or_blocker")
    if recovery_owner is None:
        raise ContractValidationError(f"{status} Return requires recovery_owner")
