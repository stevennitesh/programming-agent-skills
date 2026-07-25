"""Verify frozen deploy-campaign fixtures, payloads, and artifact trees."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from scripts.skill_pack_contract import tree_entries


TREE_ALGORITHM = (
    "campaign-tree-v1: SHA-256 of UTF-8 lines sorted by ordinal UTF-8 "
    "POSIX path; path<TAB>byte_count<TAB>file_sha256<LF>"
)
CURRENT_FIXTURE_SCHEMA_VERSION = 2
REQUIRED_CASE_FIELDS = (
    "task",
    "authority",
    "initial_state",
    "tools_operations",
    "mutation_boundary",
    "requested_output",
)
DECISION_STATE_VALUES = {
    "target_resolution": frozenset({"resolved", "unresolved", "not-applicable"}),
    "evidence_availability": frozenset(
        {"inspectable", "unavailable", "not-applicable"}
    ),
    "mutation_permission": frozenset({"allowed", "forbidden", "not-applicable"}),
}
CASE_CONTEXT_FIELDS = REQUIRED_CASE_FIELDS + ("decision_state",)
SOURCE_FIELDS = ("facts", "source_facts")
ISOLATION_FALSE_FIELDS = (
    "candidate_terms_present",
    "prior_outputs_present",
    "conclusions_present",
)
FORBIDDEN_DISPATCH_KEYS = frozenset(
    {
        "candidate_hint",
        "candidate_language",
        "candidate_terms",
        "conclusions",
        "expected_weakness",
        "expected_weaknesses",
        "hypothesis",
        "prior_outputs",
        "rubric",
        "rubrics_or_scores",
        "scores",
        "scoring",
    }
)
CAMPAIGN_SCHEMA_VERSION = 1
CAMPAIGN_ROOT = Path("docs/validation/campaigns")
LEASE_PATH = Path(".tmp/deploy-campaign-lease.json")
DELIVERY_MODES = frozenset({"none", "commit", "push"})
STAGE_PROFILES = frozenset(
    {
        "prompt-1",
        "research",
        "prompt-2",
        "prompt-3",
        "prompt-4",
        "pruning",
        "prompt-5",
        "prompt-6",
    }
)
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MECHANICAL_STATUSES = frozenset(
    {"verified", "failed", "stale", "lease-conflict", "execution-error"}
)


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _validate_id(value: str, label: str) -> str:
    if not SAFE_ID.fullmatch(value):
        raise ValueError(
            f"{label} must contain only lowercase letters, digits, and hyphens"
        )
    return value


def _write_json_file(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _replace_json_file(path: Path, payload: object) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _install_exclusive_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _campaign_manifest_path(worktree: Path, campaign_id: str) -> Path:
    return worktree / CAMPAIGN_ROOT / campaign_id / "manifest.json"


def _campaign_id(skill: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{skill}-{stamp}-{uuid4().hex[:8]}"


def start_campaign(
    skill: str,
    delivery_mode: str = "none",
    *,
    worktree: Path | None = None,
    campaign_id: str | None = None,
    owner_token: str | None = None,
    continuation: str | None = None,
    from_manifest: Path | None = None,
    changed_inputs: list[str] | None = None,
    _supersedes: str | None = None,
    _held_lease: dict[str, object] | None = None,
) -> dict[str, object]:
    """Create one exact campaign epoch and acquire its worktree lease."""

    skill = _validate_id(skill, "Skill")
    if delivery_mode not in DELIVERY_MODES:
        raise ValueError("Delivery mode must be one of: none, commit, push")
    resolved_worktree = (worktree or Path.cwd()).resolve()
    if continuation is not None:
        if from_manifest is None:
            raise ValueError("Continuation requires an exact source manifest")
        return _continue_campaign(
            skill,
            delivery_mode,
            continuation=continuation,
            from_manifest=from_manifest,
            worktree=resolved_worktree,
            campaign_id=campaign_id,
            owner_token=owner_token,
            changed_inputs=changed_inputs or [],
        )
    selected_campaign_id = _validate_id(
        campaign_id or _campaign_id(skill),
        "Campaign ID",
    )
    selected_owner_token = owner_token or f"codex/{uuid4()}"
    manifest_path = _campaign_manifest_path(
        resolved_worktree,
        selected_campaign_id,
    )
    lease_path = resolved_worktree / LEASE_PATH
    created_at = _now()
    lease = {
        "schema_version": CAMPAIGN_SCHEMA_VERSION,
        "worktree": str(resolved_worktree),
        "campaign_id": selected_campaign_id,
        "owner_token": selected_owner_token,
        "acquired_at": created_at,
        "observed_at": created_at,
        "status_read_at": None,
    }
    if _held_lease is None:
        try:
            _install_exclusive_json(lease_path, lease)
        except FileExistsError:
            return _failure(
                "lease-conflict",
                "lease",
                manifest_path,
                "Another Deploy Campaign owns this worktree lease",
            )

    manifest = {
        "schema_version": CAMPAIGN_SCHEMA_VERSION,
        "campaign": {
            "id": selected_campaign_id,
            "skill": skill,
            "delivery_mode": delivery_mode,
            "worktree": str(resolved_worktree),
            "supersedes": _supersedes,
        },
        "semantic": {
            "declared_stage": None,
            "terminal": False,
            "decision_record": "decisions.md",
        },
        "mechanical": {
            "created_at": created_at,
            "evidence_state": "current",
            "last_verification": None,
            "receipts": [],
            "invalidations": [],
        },
    }
    campaign_parent = manifest_path.parent.parent
    campaign_parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(
        tempfile.mkdtemp(
            dir=campaign_parent,
            prefix=f".{selected_campaign_id}.",
        )
    )
    try:
        _write_json_file(temporary / "manifest.json", manifest)
        (temporary / "decisions.md").write_text(
            "# Deploy Campaign Decisions\n\n"
            "<!-- campaign-owner: append immutable marker-bounded stage capsules -->\n",
            encoding="utf-8",
            newline="\n",
        )
        os.replace(temporary, manifest_path.parent)
        if _held_lease is not None:
            _replace_json_file(lease_path, lease)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        if _held_lease is None:
            lease_path.unlink(missing_ok=True)
        raise

    relative_manifest = manifest_path.relative_to(resolved_worktree).as_posix()
    return {
        "status": "verified",
        "campaign_id": selected_campaign_id,
        "owner_token": selected_owner_token,
        "manifest": relative_manifest,
        "next_command": (
            f"python -m scripts.campaign_artifacts verify {relative_manifest}"
        ),
    }


def _continue_campaign(
    skill: str,
    delivery_mode: str,
    *,
    continuation: str,
    from_manifest: Path,
    worktree: Path,
    campaign_id: str | None,
    owner_token: str | None,
    changed_inputs: list[str],
) -> dict[str, object]:
    if continuation not in {"resume", "repair", "restart"}:
        raise ValueError("Continuation must be one of: resume, repair, restart")
    try:
        prior_campaign_id, manifest = _control_identity(from_manifest, worktree)
        lease_path = worktree / LEASE_PATH
        lease = _read_json(lease_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return _failure(
            "failed",
            "continuation",
            from_manifest,
            f"Continuation source is invalid: {error}",
        )
    campaign = manifest["campaign"]
    semantic = manifest.get("semantic")
    mechanical = manifest.get("mechanical")
    assert isinstance(campaign, dict)
    if not isinstance(semantic, dict) or not isinstance(mechanical, dict):
        return _failure(
            "failed",
            "manifest-schema",
            from_manifest,
            "Continuation ownership sections are invalid",
        )
    if (
        not isinstance(lease, dict)
        or lease.get("worktree") != str(worktree)
        or lease.get("campaign_id") != prior_campaign_id
        or owner_token is None
        or lease.get("owner_token") != owner_token
    ):
        return _failure(
            "lease-conflict",
            "lease",
            from_manifest,
            "Continuation does not own the exact source campaign lease",
        )

    identity_unchanged = (
        campaign.get("skill") == skill
        and campaign.get("delivery_mode") == delivery_mode
    )
    relative_manifest = from_manifest.resolve().relative_to(worktree).as_posix()
    if continuation == "resume":
        if not identity_unchanged or semantic.get("terminal") is True:
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Resume requires unchanged identity and a nonterminal campaign",
            )
        return {
            "status": "verified",
            "campaign_id": prior_campaign_id,
            "manifest": relative_manifest,
            "continuation": "resume",
        }

    if continuation == "repair":
        if not identity_unchanged or semantic.get("terminal") is True:
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Repair requires unchanged identity and a nonterminal campaign",
            )
        if not changed_inputs or any(
            not isinstance(value, str) or not value for value in changed_inputs
        ):
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Repair requires at least one changed mechanical input",
            )
        invalidations = mechanical.get("invalidations")
        if not isinstance(invalidations, list):
            return _failure(
                "failed",
                "manifest-schema",
                from_manifest,
                "Mechanical invalidations must be a list",
            )
        invalidations.append(
            {
                "changed_inputs": sorted(set(changed_inputs)),
                "observed_at": _now(),
            }
        )
        update_mechanical_state(
            from_manifest,
            {
                "evidence_state": "stale",
                "invalidations": invalidations,
            },
        )
        return {
            "status": "stale",
            "campaign_id": prior_campaign_id,
            "manifest": relative_manifest,
            "continuation": "repair",
            "changed_inputs": sorted(set(changed_inputs)),
        }

    if identity_unchanged and semantic.get("terminal") is not True:
        return _failure(
            "failed",
            "continuation",
            from_manifest,
            "Restart requires changed identity, delivery authority, or terminal state",
        )
    return start_campaign(
        skill,
        delivery_mode,
        worktree=worktree,
        campaign_id=campaign_id,
        owner_token=owner_token,
        _supersedes=relative_manifest,
        _held_lease=lease,
    )


def update_mechanical_state(
    manifest_path: Path,
    updates: dict[str, object],
) -> dict[str, object]:
    """Atomically update only the automation-owned manifest section."""

    forbidden = {"campaign", "semantic", "schema_version"}.intersection(updates)
    if forbidden:
        raise ValueError(
            "Mechanical updates cannot write "
            + ", ".join(sorted(forbidden))
            + " fields"
        )
    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict) or not isinstance(
        manifest.get("mechanical"),
        dict,
    ):
        raise ValueError("Campaign manifest mechanical section is invalid")
    semantic_before = copy.deepcopy(manifest.get("semantic"))
    manifest["mechanical"].update(copy.deepcopy(updates))
    if manifest.get("semantic") != semantic_before:
        raise ValueError("Mechanical updates cannot alter semantic fields")
    _replace_json_file(manifest_path, manifest)
    return manifest


def _failure(
    status: str,
    gate: str,
    manifest_path: Path,
    message: str,
) -> dict[str, object]:
    if status not in MECHANICAL_STATUSES:
        raise ValueError(f"Unknown mechanical status: {status}")
    return {
        "status": status,
        "gate": gate,
        "artifact": str(manifest_path),
        "message": message,
        "expensive_work_skipped": True,
        "exit_code": {
            "failed": 2,
            "stale": 3,
            "lease-conflict": 4,
            "execution-error": 5,
        }.get(status, 0),
        "reentry_command": (
            f"python -m scripts.campaign_artifacts verify {manifest_path}"
        ),
    }


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _control_identity(
    manifest_path: Path,
    worktree: Path,
) -> tuple[str, dict[str, object]]:
    supplied_manifest = manifest_path.resolve()
    manifest = _read_json(supplied_manifest)
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be a JSON object")
    campaign = manifest.get("campaign")
    if not isinstance(campaign, dict):
        raise ValueError("Manifest campaign section is invalid")
    campaign_id = campaign.get("id")
    if (
        manifest.get("schema_version") != CAMPAIGN_SCHEMA_VERSION
        or campaign.get("worktree") != str(worktree)
        or not isinstance(campaign_id, str)
        or not SAFE_ID.fullmatch(campaign_id)
        or supplied_manifest != _campaign_manifest_path(worktree, campaign_id).resolve()
    ):
        raise ValueError("Manifest identity does not match its exact worktree path")
    return campaign_id, manifest


def campaign_status(
    manifest_path: Path,
    *,
    worktree: Path | None = None,
) -> dict[str, object]:
    """Read one exact campaign and record the observation needed for abandon."""

    resolved_worktree = (worktree or Path.cwd()).resolve()
    try:
        campaign_id, manifest = _control_identity(
            manifest_path,
            resolved_worktree,
        )
        lease_path = resolved_worktree / LEASE_PATH
        lease = _read_json(lease_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return _failure(
            "failed",
            "status-read",
            manifest_path,
            f"Campaign status is unavailable: {error}",
        )
    if (
        not isinstance(lease, dict)
        or lease.get("worktree") != str(resolved_worktree)
        or lease.get("campaign_id") != campaign_id
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )
    lease["status_read_at"] = _now()
    _replace_json_file(lease_path, lease)
    semantic = manifest.get("semantic")
    stage = semantic.get("declared_stage") if isinstance(semantic, dict) else None
    return {
        "status": "verified",
        "campaign_id": campaign_id,
        "stage": stage,
        "owner_token": lease.get("owner_token"),
        "lease": "owned",
    }


def release_campaign(
    manifest_path: Path,
    *,
    worktree: Path | None = None,
    owner_token: str | None = None,
    abandon: bool = False,
) -> dict[str, object]:
    """Release an exact-owner lease or explicitly abandon after status read-back."""

    resolved_worktree = (worktree or Path.cwd()).resolve()
    try:
        campaign_id, manifest = _control_identity(
            manifest_path,
            resolved_worktree,
        )
        lease_path = resolved_worktree / LEASE_PATH
        lease = _read_json(lease_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return _failure(
            "failed",
            "lease",
            manifest_path,
            f"Campaign lease cannot be released: {error}",
        )
    if (
        not isinstance(lease, dict)
        or lease.get("worktree") != str(resolved_worktree)
        or lease.get("campaign_id") != campaign_id
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )
    exact_owner = owner_token is not None and owner_token == lease.get("owner_token")
    if not exact_owner and not abandon:
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "Owner token does not match the campaign lease",
        )
    if abandon and lease.get("status_read_at") is None:
        return _failure(
            "failed",
            "status-read",
            manifest_path,
            "Explicit abandon requires a prior status read-back",
        )
    lease_path.unlink()
    return {
        "status": "verified",
        "campaign_id": campaign_id,
        "released": True,
        "abandoned": abandon and not exact_owner,
    }


def verify_campaign(
    manifest_path: Path,
    *,
    worktree: Path | None = None,
    stage_override: str | None = None,
) -> dict[str, object]:
    """Verify one supplied campaign manifest without selecting or advancing it."""

    resolved_worktree = (worktree or Path.cwd()).resolve()
    supplied_manifest = manifest_path.resolve()
    campaign_root = (resolved_worktree / CAMPAIGN_ROOT).resolve()
    if not _is_within(supplied_manifest, campaign_root):
        return _failure(
            "failed",
            "manifest-path",
            manifest_path,
            "Manifest is outside the configured campaign root",
        )
    try:
        manifest = _read_json(supplied_manifest)
    except FileNotFoundError:
        return _failure(
            "failed",
            "manifest-read",
            manifest_path,
            "Manifest does not exist",
        )
    except (OSError, json.JSONDecodeError) as error:
        return _failure(
            "failed",
            "manifest-read",
            manifest_path,
            f"Manifest cannot be read: {error}",
        )
    if not isinstance(manifest, dict):
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            "Manifest must be a JSON object",
        )
    if manifest.get("schema_version") != CAMPAIGN_SCHEMA_VERSION:
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            "Manifest schema is foreign or legacy",
        )
    campaign = manifest.get("campaign")
    semantic = manifest.get("semantic")
    mechanical = manifest.get("mechanical")
    if not all(
        isinstance(section, dict)
        for section in (campaign, semantic, mechanical)
    ):
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            "Manifest ownership sections are incomplete",
        )
    assert isinstance(campaign, dict)
    assert isinstance(semantic, dict)
    assert isinstance(mechanical, dict)
    if campaign.get("worktree") != str(resolved_worktree):
        return _failure(
            "failed",
            "manifest-worktree",
            manifest_path,
            "Manifest belongs to a different worktree",
        )
    skill = campaign.get("skill")
    delivery_mode = campaign.get("delivery_mode")
    if (
        not isinstance(skill, str)
        or not SAFE_ID.fullmatch(skill)
        or delivery_mode not in DELIVERY_MODES
    ):
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            "Campaign skill or delivery mode is invalid",
        )
    campaign_id = campaign.get("id")
    if (
        not isinstance(campaign_id, str)
        or not SAFE_ID.fullmatch(campaign_id)
        or supplied_manifest
        != _campaign_manifest_path(resolved_worktree, campaign_id).resolve()
    ):
        return _failure(
            "failed",
            "manifest-path",
            manifest_path,
            "Manifest path does not match its exact campaign identity",
        )
    decision_record = semantic.get("decision_record")
    supersedes = campaign.get("supersedes")
    if supersedes is not None:
        supersedes_path = resolved_worktree / str(supersedes)
        if (
            not isinstance(supersedes, str)
            or Path(supersedes).is_absolute()
            or not _is_within(supersedes_path, campaign_root)
            or supersedes_path.name != "manifest.json"
            or not supersedes_path.is_file()
        ):
            return _failure(
                "failed",
                "manifest-path",
                manifest_path,
                "Superseded manifest pointer escapes or is malformed",
            )
    decision_path = supplied_manifest.parent / str(decision_record)
    if (
        not isinstance(decision_record, str)
        or Path(decision_record).is_absolute()
        or not _is_within(decision_path, supplied_manifest.parent)
        or decision_path.resolve()
        != (supplied_manifest.parent / "decisions.md").resolve()
        or not decision_path.is_file()
    ):
        return _failure(
            "failed",
            "manifest-path",
            manifest_path,
            "Decision record pointer escapes or names a foreign artifact",
        )

    lease_path = resolved_worktree / LEASE_PATH
    try:
        lease = _read_json(lease_path)
    except (OSError, json.JSONDecodeError):
        return _failure(
            "failed",
            "lease",
            manifest_path,
            "Campaign lease is absent or unreadable",
        )
    owner_token = lease.get("owner_token") if isinstance(lease, dict) else None
    if (
        not isinstance(lease, dict)
        or lease.get("worktree") != str(resolved_worktree)
        or lease.get("campaign_id") != campaign_id
        or not isinstance(owner_token, str)
        or not owner_token
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )

    declared_stage = semantic.get("declared_stage")
    if declared_stage is None:
        return _failure(
            "stale",
            "semantic-stage",
            manifest_path,
            "Campaign owner has not declared a stage",
        )
    if (
        not isinstance(declared_stage, str)
        or declared_stage not in STAGE_PROFILES
        or not isinstance(semantic.get("terminal"), bool)
    ):
        return _failure(
            "failed",
            "semantic-stage",
            manifest_path,
            "Owner-declared stage or terminal state is invalid",
        )
    if stage_override is not None and stage_override != declared_stage:
        return _failure(
            "failed",
            "semantic-stage",
            manifest_path,
            "Advanced stage override does not match the owner-declared stage",
        )
    if mechanical.get("evidence_state") == "stale":
        return _failure(
            "stale",
            "mechanical-evidence",
            manifest_path,
            "Repair invalidated mechanical evidence for this epoch",
        )

    semantic_before = copy.deepcopy(semantic)
    observed_at = _now()
    update_mechanical_state(
        supplied_manifest,
        {
            "last_verification": {
                "stage": declared_stage,
                "status": "verified",
                "observed_at": observed_at,
            }
        },
    )
    lease["observed_at"] = observed_at
    _replace_json_file(lease_path, lease)
    verified = _read_json(supplied_manifest)
    if verified.get("semantic") != semantic_before:
        return _failure(
            "execution-error",
            "semantic-ownership",
            manifest_path,
            "Verification altered owner-written semantic state",
        )
    return {
        "status": "verified",
        "campaign_id": campaign_id,
        "stage": declared_stage,
        "manifest": str(supplied_manifest),
    }


def _nonempty(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, bytes, list, tuple, dict, set)):
        return bool(value)
    return True


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def _canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_decision_state(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} decision_state must be an object")
    missing = sorted(set(DECISION_STATE_VALUES).difference(value))
    unexpected = sorted(set(value).difference(DECISION_STATE_VALUES))
    invalid = sorted(
        field
        for field, allowed in DECISION_STATE_VALUES.items()
        if field in value and value[field] not in allowed
    )
    failures: list[str] = []
    if missing:
        failures.append("missing " + ", ".join(missing))
    if unexpected:
        failures.append("unexpected " + ", ".join(unexpected))
    if invalid:
        failures.append("invalid " + ", ".join(invalid))
    if failures:
        raise ValueError(f"{label} decision_state is invalid: {'; '.join(failures)}")


def campaign_tree_hash(directory: Path) -> dict[str, object]:
    entries = tree_entries(directory)
    files = [
        (name, content)
        for name, (kind, content) in entries.items()
        if kind == "file"
    ]
    digest = hashlib.sha256()
    for name, content in sorted(files, key=lambda item: item[0].encode("utf-8")):
        if "\t" in name or "\r" in name or "\n" in name:
            raise ValueError(f"Campaign artifact path is not hash-safe: {name!r}")
        file_sha256 = hashlib.sha256(content).hexdigest()
        digest.update(f"{name}\t{len(content)}\t{file_sha256}\n".encode("utf-8"))
    return {
        "algorithm": TREE_ALGORITHM,
        "file_count": len(files),
        "sha256": digest.hexdigest(),
    }


def _case_nodes(
    value: object,
    inherited: dict[str, object] | None = None,
) -> list[tuple[str, dict[str, object]]]:
    context = dict(inherited or {})
    cases: list[tuple[str, dict[str, object]]] = []
    if isinstance(value, dict):
        for field in CASE_CONTEXT_FIELDS:
            if field in value:
                context[field] = value[field]
        if "id" in value and any(field in value for field in SOURCE_FIELDS):
            case = dict(context)
            case.update(value)
            cases.append((str(value["id"]), case))
        for child in value.values():
            cases.extend(_case_nodes(child, context))
    elif isinstance(value, list):
        for child in value:
            cases.extend(_case_nodes(child, context))
    return cases


def lint_worker_fixture(path: Path) -> dict[str, object]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Worker fixture must be a JSON object")
    schema_version = payload.get("schema_version", 1)
    if schema_version not in (1, CURRENT_FIXTURE_SCHEMA_VERSION):
        raise ValueError(
            "Worker fixture schema_version must be 1 or "
            f"{CURRENT_FIXTURE_SCHEMA_VERSION}"
        )
    requires_decision_state = schema_version >= CURRENT_FIXTURE_SCHEMA_VERSION

    isolation = payload.get("isolation")
    if not isinstance(isolation, dict):
        raise ValueError("Worker fixture must define an isolation object")
    if isolation.get("arm_delta") != "runtime package only":
        raise ValueError("Worker fixture isolation.arm_delta must be runtime package only")
    leaked_or_unstated = [
        key
        for key in ISOLATION_FALSE_FIELDS
        if isolation.get(key) is not False
    ]
    leaked_or_unstated.extend(
        key
        for key, value in isolation.items()
        if key.endswith("_present")
        and value is not False
        and key not in leaked_or_unstated
    )
    if leaked_or_unstated:
        raise ValueError(
            "Worker fixture isolation must explicitly exclude: "
            + ", ".join(sorted(leaked_or_unstated))
        )

    inherited = payload.get("fixed_execution")
    if inherited is not None and not isinstance(inherited, dict):
        raise ValueError("Worker fixture fixed_execution must be an object")
    cases = _case_nodes(payload, inherited)
    if not cases:
        raise ValueError("Worker fixture must contain at least one sourced case")
    case_ids = [case_id for case_id, _case in cases]
    duplicate_ids = sorted(
        case_id for case_id in set(case_ids) if case_ids.count(case_id) > 1
    )
    if duplicate_ids:
        raise ValueError(
            "Worker fixture contains duplicate case IDs: "
            + ", ".join(duplicate_ids)
        )

    failures: list[str] = []
    for case_id, case in cases:
        missing = [
            field for field in REQUIRED_CASE_FIELDS if not _nonempty(case.get(field))
        ]
        if requires_decision_state and not _nonempty(case.get("decision_state")):
            missing.append("decision_state")
        if not any(_nonempty(case.get(field)) for field in SOURCE_FIELDS):
            missing.append("facts|source_facts")
        if missing:
            failures.append(f"{case_id}: {', '.join(missing)}")
    if failures:
        raise ValueError("Worker fixture cases are incomplete: " + "; ".join(failures))
    for case_id, case in cases:
        if "decision_state" in case:
            _validate_decision_state(case["decision_state"], f"Case {case_id}")

    return {
        "status": "ok",
        "schema_version": schema_version,
        "case_count": len(cases),
    }


def _worker_evidence_refs(case: dict[str, object]) -> set[str]:
    refs = {
        f"field:{field}"
        for field in REQUIRED_CASE_FIELDS + ("decision_state",)
        if _nonempty(case.get(field))
    }
    decision_state = case.get("decision_state")
    if isinstance(decision_state, dict):
        refs.update(
            f"field:decision_state.{field}"
            for field, value in decision_state.items()
            if _nonempty(value)
        )
    for source_field in SOURCE_FIELDS:
        source = case.get(source_field)
        if isinstance(source, dict):
            refs.update(f"fact:{fact_id}" for fact_id in source)
        elif isinstance(source, list):
            refs.update(f"fact:{index}" for index, _value in enumerate(source))
    operations = case.get("tools_operations")
    if isinstance(operations, dict):
        refs.update(f"operation:{operation_id}" for operation_id in operations)
    elif isinstance(operations, list):
        refs.update(f"operation:{operation}" for operation in operations)
    return refs


def _evidence_list(
    value: object,
    label: str,
    allowed: set[str],
) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item for item in value)
    ):
        raise ValueError(f"{label} must be a nonempty list of evidence references")
    unknown = sorted(set(value).difference(allowed))
    if unknown:
        raise ValueError(f"{label} names unknown worker evidence: {', '.join(unknown)}")
    return value


def lint_terminal_registration(
    fixture_path: Path,
    registration_path: Path,
) -> dict[str, object]:
    """Verify root-only terminal feasibility against worker-visible evidence."""

    fixture_result = lint_worker_fixture(fixture_path)
    fixture = _read_json(fixture_path)
    registration = _read_json(registration_path)
    if not isinstance(fixture, dict) or not isinstance(registration, dict):
        raise ValueError("Fixture and terminal registration must be JSON objects")

    inherited = fixture.get("fixed_execution")
    worker_cases = {
        case_id: case
        for case_id, case in _case_nodes(
            fixture,
            inherited if isinstance(inherited, dict) else None,
        )
    }
    profiles = registration.get("terminal_profiles")
    registered = registration.get("cases")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError("Terminal registration must define terminal_profiles")
    if not isinstance(registered, list) or not registered:
        raise ValueError("Terminal registration must define cases")

    registered_cases: dict[str, dict[str, object]] = {}
    for item in registered:
        if not isinstance(item, dict) or not _nonempty(item.get("id")):
            raise ValueError("Every terminal registration case must name an id")
        case_id = str(item["id"])
        if case_id in registered_cases:
            raise ValueError(f"Terminal registration contains duplicate case: {case_id}")
        registered_cases[case_id] = item

    missing = sorted(set(worker_cases).difference(registered_cases))
    unexpected = sorted(set(registered_cases).difference(worker_cases))
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected))
        raise ValueError("Terminal registration case mismatch: " + "; ".join(details))

    for case_id, item in registered_cases.items():
        terminal = item.get("expected_terminal")
        if not isinstance(terminal, str) or terminal not in profiles:
            raise ValueError(
                f"Case {case_id} expected_terminal must name a terminal profile"
            )
        profile = profiles[terminal]
        if not isinstance(profile, dict):
            raise ValueError(f"Terminal profile {terminal} must be an object")
        roles = profile.get("required_roles")
        adjacent = profile.get("adjacent_terminals")
        if (
            not isinstance(roles, list)
            or not roles
            or any(not isinstance(role, str) or not role for role in roles)
            or len(set(roles)) != len(roles)
        ):
            raise ValueError(
                f"Terminal profile {terminal} required_roles must be unique and nonempty"
            )
        if (
            not isinstance(adjacent, list)
            or not adjacent
            or any(not isinstance(name, str) or not name for name in adjacent)
            or terminal in adjacent
            or len(set(adjacent)) != len(adjacent)
        ):
            raise ValueError(
                f"Terminal profile {terminal} adjacent_terminals must be unique, "
                "nonempty, and exclude itself"
            )

        feasibility = item.get("feasibility")
        if not isinstance(feasibility, dict):
            raise ValueError(f"Case {case_id} must define feasibility")
        role_evidence = feasibility.get("role_evidence")
        exclusions = feasibility.get("adjacent_terminal_exclusions")
        if not isinstance(role_evidence, dict):
            raise ValueError(f"Case {case_id} feasibility.role_evidence must be an object")
        if not isinstance(exclusions, dict):
            raise ValueError(
                f"Case {case_id} feasibility.adjacent_terminal_exclusions "
                "must be an object"
            )
        if set(role_evidence) != set(roles):
            raise ValueError(
                f"Case {case_id} role evidence must match terminal profile roles"
            )
        if set(exclusions) != set(adjacent):
            raise ValueError(
                f"Case {case_id} adjacent exclusions must match terminal profile"
            )

        allowed = _worker_evidence_refs(worker_cases[case_id])
        for role, evidence in role_evidence.items():
            _evidence_list(evidence, f"Case {case_id} role {role}", allowed)
        for other_terminal, evidence in exclusions.items():
            _evidence_list(
                evidence,
                f"Case {case_id} exclusion {other_terminal}",
                allowed,
            )

    return {
        "status": "ok",
        "schema_version": fixture_result["schema_version"],
        "case_count": len(worker_cases),
        "fixture_sha256": _canonical_json_sha256(fixture),
        "registration_sha256": _canonical_json_sha256(registration),
    }


def _fixture_case(path: Path, case_id: str) -> dict[str, object]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Worker fixture must be a JSON object")
    inherited = payload.get("fixed_execution")
    cases = {
        candidate_id: case
        for candidate_id, case in _case_nodes(
            payload,
            inherited if isinstance(inherited, dict) else None,
        )
    }
    if case_id not in cases:
        raise ValueError(f"Worker fixture case is missing: {case_id}")
    return cases[case_id]


def _remove_json_pointer(payload: object, pointer: str) -> object:
    if not pointer.startswith("/") or pointer == "/":
        raise ValueError(f"Runtime pointer must name one nested value: {pointer!r}")
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.removeprefix("/").split("/")
    ]
    parent = payload
    for part in parts[:-1]:
        if isinstance(parent, dict) and part in parent:
            parent = parent[part]
        elif isinstance(parent, list) and part.isdigit() and int(part) < len(parent):
            parent = parent[int(part)]
        else:
            raise ValueError(f"Runtime pointer is missing: {pointer}")
    leaf = parts[-1]
    if isinstance(parent, dict) and leaf in parent:
        return parent.pop(leaf)
    elif isinstance(parent, list) and leaf.isdigit() and int(leaf) < len(parent):
        return parent.pop(int(leaf))
    else:
        raise ValueError(f"Runtime pointer is missing: {pointer}")


def _forbidden_dispatch_keys(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        found.update(FORBIDDEN_DISPATCH_KEYS.intersection(value))
        for child in value.values():
            found.update(_forbidden_dispatch_keys(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_forbidden_dispatch_keys(child))
    return found


def _lint_dispatch_payload(
    payload: object,
    label: str,
    *,
    require_decision_state: bool,
) -> None:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} dispatch payload must be a JSON object")
    missing = [
        field for field in REQUIRED_CASE_FIELDS if not _nonempty(payload.get(field))
    ]
    if require_decision_state and not _nonempty(payload.get("decision_state")):
        missing.append("decision_state")
    if not any(_nonempty(payload.get(field)) for field in SOURCE_FIELDS):
        missing.append("facts|source_facts")
    if missing:
        raise ValueError(f"{label} dispatch payload is incomplete: {', '.join(missing)}")
    if "decision_state" in payload:
        _validate_decision_state(
            payload["decision_state"],
            f"{label} dispatch payload",
        )
    forbidden = _forbidden_dispatch_keys(payload)
    if forbidden:
        raise ValueError(
            f"{label} dispatch payload contains root-only fields: "
            + ", ".join(sorted(forbidden))
        )


def _verify_fixture_fidelity(
    payload: dict[str, object],
    fixture_case: dict[str, object],
    label: str,
) -> None:
    fields = list(REQUIRED_CASE_FIELDS)
    if "decision_state" in fixture_case:
        fields.append("decision_state")
    fields.extend(field for field in SOURCE_FIELDS if field in fixture_case)
    mismatched = [
        field
        for field in fields
        if payload.get(field) != fixture_case.get(field)
    ]
    if mismatched:
        raise ValueError(
            f"{label} dispatch payload disagrees with its worker fixture case: "
            + ", ".join(mismatched)
        )


def lint_dispatch_payload(
    fixture_path: Path,
    case_id: str,
    payload_path: Path,
    runtime_pointer: str = "/runtime",
) -> dict[str, object]:
    fixture_result = lint_worker_fixture(fixture_path)
    fixture_case = _fixture_case(fixture_path, case_id)
    payload = _read_json(payload_path)
    _lint_dispatch_payload(
        payload,
        "Resolved",
        require_decision_state=(
            fixture_result["schema_version"] >= CURRENT_FIXTURE_SCHEMA_VERSION
        ),
    )
    _verify_fixture_fidelity(payload, fixture_case, "Resolved")

    runtime_check = copy.deepcopy(payload)
    runtime = _remove_json_pointer(runtime_check, runtime_pointer)
    if not _nonempty(runtime):
        raise ValueError("Resolved dispatch payload must name a nonempty runtime")
    return {
        "status": "ok",
        "case_id": case_id,
        "runtime_pointer": runtime_pointer,
        "dispatch_payload_sha256": _canonical_json_sha256(payload),
    }


def compare_payloads(
    fixture_path: Path,
    case_id: str,
    control_path: Path,
    candidate_path: Path,
    runtime_pointer: str = "/runtime",
) -> dict[str, object]:
    fixture_result = lint_worker_fixture(fixture_path)
    fixture_case = _fixture_case(fixture_path, case_id)
    control = _read_json(control_path)
    candidate = _read_json(candidate_path)
    require_decision_state = (
        fixture_result["schema_version"] >= CURRENT_FIXTURE_SCHEMA_VERSION
    )
    _lint_dispatch_payload(
        control,
        "Control",
        require_decision_state=require_decision_state,
    )
    _lint_dispatch_payload(
        candidate,
        "Candidate",
        require_decision_state=require_decision_state,
    )
    _verify_fixture_fidelity(control, fixture_case, "Control")
    _verify_fixture_fidelity(candidate, fixture_case, "Candidate")

    normalized_control = copy.deepcopy(control)
    normalized_candidate = copy.deepcopy(candidate)
    control_runtime = _remove_json_pointer(normalized_control, runtime_pointer)
    candidate_runtime = _remove_json_pointer(normalized_candidate, runtime_pointer)
    if not _nonempty(control_runtime) or not _nonempty(candidate_runtime):
        raise ValueError("Both dispatch payloads must name a nonempty runtime")
    if control_runtime == candidate_runtime:
        raise ValueError("Control and candidate dispatch runtimes must differ")
    if normalized_control != normalized_candidate:
        raise ValueError(
            "Control and candidate dispatch payloads differ outside the runtime slot"
        )

    return {
        "status": "ok",
        "runtime_pointer": runtime_pointer,
        "shared_payload_sha256": _canonical_json_sha256(normalized_control),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Control Deploy Campaign records and verify campaign artifacts."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    start = commands.add_parser("start")
    start.add_argument("skill")
    start.add_argument(
        "delivery_mode",
        nargs="?",
        default="none",
        choices=sorted(DELIVERY_MODES),
    )
    start.add_argument("--worktree", type=Path, default=Path.cwd())
    start.add_argument("--campaign-id")
    start.add_argument("--owner-token")
    start.add_argument(
        "--continuation",
        choices=("resume", "repair", "restart"),
    )
    start.add_argument("--from-manifest", type=Path)
    start.add_argument("--changed-input", action="append", default=[])
    start.add_argument("--json", action="store_true")

    verify = commands.add_parser("verify")
    verify.add_argument("manifest", type=Path)
    verify.add_argument("--worktree", type=Path, default=Path.cwd())
    verify.add_argument("--stage", dest="stage_override")
    verify.add_argument("--json", action="store_true")

    status = commands.add_parser("status")
    status.add_argument("manifest", type=Path)
    status.add_argument("--worktree", type=Path, default=Path.cwd())
    status.add_argument("--json", action="store_true")

    release = commands.add_parser("release")
    release.add_argument("manifest", type=Path)
    release.add_argument("--worktree", type=Path, default=Path.cwd())
    release.add_argument("--owner-token")
    release.add_argument("--abandon", action="store_true")
    release.add_argument("--json", action="store_true")

    hash_tree = commands.add_parser("hash-tree")
    hash_tree.add_argument("path", type=Path)

    lint_fixture = commands.add_parser("lint-fixture")
    lint_fixture.add_argument("path", type=Path)

    lint_registration = commands.add_parser("lint-registration")
    lint_registration.add_argument("fixture", type=Path)
    lint_registration.add_argument("registration", type=Path)

    lint_payload = commands.add_parser("lint-payload")
    lint_payload.add_argument("fixture", type=Path)
    lint_payload.add_argument("case_id")
    lint_payload.add_argument("payload", type=Path)
    lint_payload.add_argument("--runtime-pointer", default="/runtime")

    compare = commands.add_parser("compare-payloads")
    compare.add_argument("fixture", type=Path)
    compare.add_argument("case_id")
    compare.add_argument("control", type=Path)
    compare.add_argument("candidate", type=Path)
    compare.add_argument("--runtime-pointer", default="/runtime")
    return parser.parse_args(argv)


def _print_control_result(result: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, sort_keys=True))
        return
    status = str(result["status"])
    if status != "verified":
        detail = result.get("message") or result.get("gate") or "mechanical state"
        print(f"{status}: {detail}")
        reentry = result.get("reentry_command")
        if reentry:
            print(str(reentry))
        return
    identity = result.get("manifest") or result.get("campaign_id")
    stage = result.get("stage")
    suffix = f" stage={stage}" if stage is not None else ""
    print(f"verified: {identity}{suffix}")
    owner_token = result.get("owner_token")
    if owner_token:
        print(f"owner-token: {owner_token}")
    next_command = result.get("next_command")
    if next_command:
        print(str(next_command))


def _control_exit_code(result: dict[str, object]) -> int:
    if "exit_code" in result:
        return int(result["exit_code"])
    return {
        "verified": 0,
        "failed": 2,
        "stale": 3,
        "lease-conflict": 4,
        "execution-error": 5,
    }[str(result["status"])]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command in {"start", "verify", "status", "release"}:
        try:
            if args.command == "start":
                result = start_campaign(
                    args.skill,
                    args.delivery_mode,
                    worktree=args.worktree,
                    campaign_id=args.campaign_id,
                    owner_token=args.owner_token,
                    continuation=args.continuation,
                    from_manifest=args.from_manifest,
                    changed_inputs=args.changed_input,
                )
            elif args.command == "verify":
                result = verify_campaign(
                    args.manifest,
                    worktree=args.worktree,
                    stage_override=args.stage_override,
                )
            elif args.command == "status":
                result = campaign_status(
                    args.manifest,
                    worktree=args.worktree,
                )
            else:
                result = release_campaign(
                    args.manifest,
                    worktree=args.worktree,
                    owner_token=args.owner_token,
                    abandon=args.abandon,
                )
        except (OSError, json.JSONDecodeError, ValueError) as error:
            artifact = getattr(args, "manifest", Path("<start>"))
            result = _failure(
                "execution-error",
                args.command,
                artifact,
                str(error),
            )
        _print_control_result(result, args.json)
        return _control_exit_code(result)

    try:
        if args.command == "hash-tree":
            result = campaign_tree_hash(args.path)
        elif args.command == "lint-fixture":
            result = lint_worker_fixture(args.path)
        elif args.command == "lint-registration":
            result = lint_terminal_registration(
                args.fixture,
                args.registration,
            )
        elif args.command == "lint-payload":
            result = lint_dispatch_payload(
                args.fixture,
                args.case_id,
                args.payload,
                args.runtime_pointer,
            )
        else:
            result = compare_payloads(
                args.fixture,
                args.case_id,
                args.control,
                args.candidate,
                args.runtime_pointer,
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
