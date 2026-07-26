"""Verify frozen deploy-campaign fixtures, payloads, and artifact trees."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit
from uuid import uuid4

from jsonschema import Draft202012Validator

from scripts import install_skills, pack_contract
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
        "expected_terminal",
        "expected_terminals",
        "hypothesis",
        "prior_outputs",
        "rubric",
        "rubrics_or_scores",
        "scores",
        "scoring",
    }
)
CAMPAIGN_SCHEMA_VERSION = 1
FRESH_CAMPAIGN_SCHEMA_VERSION = 2
MAX_RESTART_LINEAGE_DEPTH = 64
CAMPAIGN_ROOT = Path("docs/validation/campaigns")
FRESH_CAMPAIGN_ROOT = Path("docs/validation/skills")
FRESH_CAMPAIGN_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "validation"
    / "shared"
    / "schemas"
    / "deploy-campaign-manifest-v2.schema.json"
)
CANONICAL_PACK_CONTRACT_PATH = "docs/synthesis/skill-pack.md"
LEASE_PATH = Path(".tmp/deploy-campaign-lease.json")
DELIVERY_MODES = frozenset({"none", "commit", "push"})
STAGE_ORDER = (
    "prompt-1",
    "research",
    "prompt-2",
    "prompt-3",
    "prompt-4",
    "pruning",
    "prompt-5",
    "prompt-6",
)
STAGE_PROFILES = frozenset(STAGE_ORDER)
FRESH_TERMINAL_LIFECYCLE = {
    "m0": "ready-for-research",
    "research": "research-complete",
    "h1": "ready-for-prompt-3",
    "proof": "accepted",
    "pruning": "complete",
    "p1": "promoted-installed",
}
PREFLIGHT_KINDS = frozenset(
    {
        "behavioral-comparison",
        "git-delivery",
        "installation",
        "markdown",
        "research",
    }
)
REQUIRED_PREFLIGHT_KINDS = {
    "prompt-3": frozenset({"behavioral-comparison", "markdown"}),
    "prompt-5": frozenset({"installation"}),
    "prompt-6": frozenset({"git-delivery"}),
    "research": frozenset({"markdown", "research"}),
}
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
EXACT_FINGERPRINT = re.compile(r"^sha256-v1:[0-9a-f]{64}$")
MECHANICAL_STATUSES = frozenset(
    {"verified", "failed", "stale", "lease-conflict", "execution-error"}
)
IDENTITY_ALGORITHMS = frozenset(
    {
        "campaign-tree-v1",
        "canonical-json-v1",
        "marker-semantic-v1",
        "git-object-v1",
    }
)
LEGACY_PROOF_RECEIPT_SCHEMA_VERSION = 1
PROOF_RECEIPT_SCHEMA_VERSION = 2
PROOF_CACHE_SCHEMA_VERSION = 1
PROOF_PROFILE_SCHEMA_VERSION = 1
PROOF_TIERS = ("cheap", "moderate", "expensive")
PROOF_PROFILES: dict[str, dict[str, object]] = {
    "campaign-artifacts-focused-v1": {
        "schema_version": PROOF_PROFILE_SCHEMA_VERSION,
        "tier": "cheap",
        "argv": (
            sys.executable,
            "-m",
            "pytest",
            "tests/test_campaign_artifacts.py",
            "-q",
        ),
        "full_suite": False,
    },
    "validate-skills-v1": {
        "schema_version": PROOF_PROFILE_SCHEMA_VERSION,
        "tier": "moderate",
        "argv": (sys.executable, "-m", "scripts.validate_skills"),
        "full_suite": False,
    },
    "full-suite-v1": {
        "schema_version": PROOF_PROFILE_SCHEMA_VERSION,
        "tier": "expensive",
        "argv": (sys.executable, "-m", "pytest"),
        "full_suite": True,
    },
}


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


def _campaign_manifest_path(
    worktree: Path,
    campaign_id: str,
    skill: str | None = None,
) -> Path:
    if skill is not None:
        return (
            worktree
            / FRESH_CAMPAIGN_ROOT
            / skill
            / "campaigns"
            / campaign_id
            / "manifest.json"
        )
    return worktree / CAMPAIGN_ROOT / campaign_id / "manifest.json"


def _campaign_id(skill: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{skill}-{stamp}-{uuid4().hex[:8]}"


def _require_nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"Fresh epoch {label} must be a nonempty string")
    return value


def _valid_owner_token(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _validate_fresh_epoch_admission(payload: object) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Fresh epoch admission must be an object")
    expected_sections = {"campaign", "contract", "semantic"}
    if set(payload) != expected_sections:
        raise ValueError(
            "Fresh epoch admission requires only campaign, contract, and semantic"
        )
    campaign = payload.get("campaign")
    contract = payload.get("contract")
    semantic = payload.get("semantic")
    if not all(
        isinstance(section, dict) for section in (campaign, contract, semantic)
    ):
        raise ValueError(
            "Fresh epoch admission requires campaign, contract, and semantic"
        )
    assert isinstance(campaign, dict)
    assert isinstance(contract, dict)
    assert isinstance(semantic, dict)
    composition_epoch_id = _require_nonempty_string(
        campaign.get("composition_epoch_id"),
        "composition_epoch_id",
    )
    if not re.fullmatch(r"FCE-[0-9]{8}-[0-9]{2}", composition_epoch_id):
        raise ValueError("Fresh epoch composition_epoch_id is malformed")
    if set(campaign) != {
        "composition_epoch_id",
        "continuation",
        "supersession",
    }:
        raise ValueError("Fresh epoch campaign admission fields are invalid")
    for nullable in ("continuation", "supersession"):
        if campaign.get(nullable) is not None and not isinstance(
            campaign.get(nullable), str
        ):
            raise ValueError(f"Fresh epoch {nullable} must be a pointer or null")

    required_contract = {
        "pack_contract",
        "slice",
        "independent_m0",
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
        "proof_predecessors",
        "schedule_pointer",
        "schedule_fingerprint",
    }
    missing_contract = required_contract.difference(contract)
    if missing_contract:
        raise ValueError(
            "Fresh epoch contract is missing "
            + ", ".join(sorted(missing_contract))
        )
    if set(contract) != required_contract:
        raise ValueError("Fresh epoch contract contains foreign fields")
    pack_contract = contract["pack_contract"]
    slice_contract = contract["slice"]
    predecessors = contract["proof_predecessors"]
    independent_m0 = contract["independent_m0"]
    if not isinstance(pack_contract, dict):
        raise ValueError("Fresh epoch pack_contract is invalid")
    if pack_contract.get("path") != CANONICAL_PACK_CONTRACT_PATH:
        raise ValueError(
            "Fresh epoch requires the canonical Pack Contract owner"
        )
    if not isinstance(slice_contract, dict):
        raise ValueError("Fresh epoch slice is invalid")
    if not isinstance(independent_m0, dict):
        raise ValueError("Fresh epoch independent_m0 is invalid")
    if not isinstance(predecessors, list):
        raise ValueError("Fresh epoch proof_predecessors are invalid")
    for value, label in (
        (pack_contract.get("path"), "pack_contract.path"),
        (pack_contract.get("revision"), "pack_contract.revision"),
        (slice_contract.get("id"), "slice.id"),
        (slice_contract.get("path"), "slice.path"),
        (independent_m0.get("path"), "independent_m0.path"),
        (contract.get("schedule_pointer"), "schedule_pointer"),
    ):
        _require_nonempty_string(value, label)
    for value, label in (
        (pack_contract.get("fingerprint"), "pack_contract.fingerprint"),
        (slice_contract.get("fingerprint"), "slice.fingerprint"),
        (independent_m0.get("fingerprint"), "independent_m0.fingerprint"),
        (contract.get("schedule_fingerprint"), "schedule_fingerprint"),
    ):
        if not isinstance(value, str) or not EXACT_FINGERPRINT.fullmatch(value):
            raise ValueError(f"Fresh epoch {label} is malformed")
    predecessor_ids: list[str] = []
    for predecessor in predecessors:
        if not isinstance(predecessor, dict) or set(predecessor) != {
            "id",
            "p1",
            "installed",
        }:
            raise ValueError("Fresh epoch proof predecessor shape is invalid")
        predecessor_id = _require_nonempty_string(
            predecessor.get("id"),
            "proof_predecessors.id",
        )
        predecessor_ids.append(predecessor_id)
        for state in ("p1", "installed"):
            identity = predecessor.get(state)
            if not isinstance(identity, dict) or set(identity) != {
                "path",
                "fingerprint",
            }:
                raise ValueError(
                    f"Fresh epoch proof_predecessors.{state} is invalid"
                )
            _require_nonempty_string(
                identity.get("path"),
                f"proof_predecessors.{state}.path",
            )
            fingerprint = identity.get("fingerprint")
            if not isinstance(
                fingerprint,
                str,
            ) or not EXACT_FINGERPRINT.fullmatch(fingerprint):
                raise ValueError(
                    f"Fresh epoch proof_predecessors.{state}.fingerprint "
                    "is malformed"
                )
    if predecessor_ids != sorted(set(predecessor_ids)):
        raise ValueError(
            "Fresh epoch proof predecessor IDs must be sorted and unique"
        )
    for field in (
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
    ):
        values = contract[field]
        if (
            not isinstance(values, list)
            or not all(isinstance(value, str) and value for value in values)
            or values != sorted(set(values))
        ):
            raise ValueError(
                f"Fresh epoch {field} must be a sorted unique list"
            )

    required_semantic = {"stage_token", "terminal_token", "lifecycle", "pointers"}
    if set(semantic) != required_semantic:
        raise ValueError("Fresh epoch semantic fields are invalid")
    if semantic.get("stage_token") not in STAGE_ORDER[:-1]:
        raise ValueError("Fresh epoch stage_token is invalid")
    if semantic.get("terminal_token") is not None and not isinstance(
        semantic.get("terminal_token"), str
    ):
        raise ValueError("Fresh epoch terminal_token is invalid")
    lifecycle = semantic.get("lifecycle")
    pointers = semantic.get("pointers")
    if not isinstance(lifecycle, dict) or not isinstance(pointers, dict):
        raise ValueError("Fresh epoch lifecycle or pointers are invalid")
    required_lifecycle = {"m0", "research", "h1", "proof", "pruning", "p1"}
    if set(lifecycle) != required_lifecycle or not all(
        isinstance(value, str) and value for value in lifecycle.values()
    ):
        raise ValueError("Fresh epoch lifecycle tokens are invalid")
    required_pointers = {
        "decision_capsule",
        "research_packet",
        "skill_synthesis",
        "claim_adjacency",
        "pack_synthesis",
    }
    if set(pointers) != required_pointers or not all(
        isinstance(value, str) and value for value in pointers.values()
    ):
        raise ValueError("Fresh epoch semantic pointers are invalid")


def _admission_path(
    worktree: Path,
    value: object,
    label: str,
    *,
    fragment: bool = False,
) -> tuple[Path, str | None]:
    pointer = _require_nonempty_string(value, label)
    path_value, separator, anchor = pointer.partition("#")
    if fragment and (not separator or not anchor):
        raise ValueError(f"Fresh epoch {label} requires a fragment")
    if not fragment and separator:
        raise ValueError(f"Fresh epoch {label} cannot contain a fragment")
    relative = Path(path_value)
    if (
        relative.is_absolute()
        or path_value != relative.as_posix()
        or ".." in relative.parts
    ):
        raise ValueError(f"Fresh epoch {label} must be a canonical relative path")
    resolved = (worktree / relative).resolve()
    if not _is_within(resolved, worktree):
        raise ValueError(f"Fresh epoch {label} escapes the worktree")
    return resolved, anchor or None


def _verify_admission_identity(
    worktree: Path,
    identity: object,
    label: str,
) -> bytes:
    if not isinstance(identity, dict):
        raise ValueError(f"Fresh epoch {label} identity is invalid")
    path, _ = _admission_path(worktree, identity.get("path"), f"{label}.path")
    try:
        content = path.read_bytes()
    except OSError as error:
        raise ValueError(
            f"Fresh epoch {label} pointer is unreadable: {error}"
        ) from error
    observed = f"sha256-v1:{hashlib.sha256(content).hexdigest()}"
    if identity.get("fingerprint") != observed:
        raise ValueError(f"Fresh epoch {label} fingerprint does not match its pointer")
    return content


def _validate_fresh_epoch_references(
    payload: dict[str, object],
    *,
    worktree: Path,
    skill: str,
) -> None:
    contract = payload["contract"]
    semantic = payload["semantic"]
    assert isinstance(contract, dict)
    assert isinstance(semantic, dict)
    pack_content = _verify_admission_identity(
        worktree,
        contract["pack_contract"],
        "pack_contract",
    )
    slice_content = _verify_admission_identity(
        worktree,
        contract["slice"],
        "slice",
    )
    slice_identity = contract["slice"]
    assert isinstance(slice_identity, dict)
    try:
        slice_payload = json.loads(slice_content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Fresh epoch slice must be a JSON identity record") from error
    required_slice_fields = {
        "slice_id",
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
        "hard_proof_predecessor_ids",
    }
    if (
        not isinstance(slice_payload, dict)
        or set(slice_payload) != required_slice_fields
    ):
        raise ValueError("Fresh epoch slice must be a JSON identity record")
    admitted_slice_id = slice_identity["id"]
    observed_slice_id = slice_payload["slice_id"]
    if observed_slice_id != admitted_slice_id:
        raise ValueError("Fresh epoch slice ID does not match its pointer")
    campaign = payload["campaign"]
    assert isinstance(campaign, dict)
    pack_identity = contract["pack_contract"]
    assert isinstance(pack_identity, dict)
    slice_parts = observed_slice_id.split(":")
    if (
        len(slice_parts) != 4
        or slice_parts[0] != campaign["composition_epoch_id"]
        or slice_parts[1] != f"r{pack_identity['revision']}"
        or not slice_parts[2]
        or slice_parts[3] != skill
    ):
        raise ValueError(
            "Fresh epoch slice does not bind the selected skill, epoch, "
            "and Pack Contract revision"
        )
    semantic_fingerprint = (
        f"sha256-v1:{_canonical_json_sha256(slice_payload)}"
    )
    if slice_identity["fingerprint"] != semantic_fingerprint:
        raise ValueError(
            "Fresh epoch slice fingerprint is not the canonical envelope"
        )
    try:
        canonical_contract = pack_contract.parse_contract(
            pack_content.decode("utf-8")
        )
        produced = pack_contract.campaign_admission_slice(
            canonical_contract,
            slice_parts[2],
        )
    except (UnicodeDecodeError, pack_contract.PackContractError) as error:
        raise ValueError(
            "Fresh epoch slice is not derived from the Pack Contract"
        ) from error
    if (
        produced.get("status") != "campaign-admission-slice"
        or produced.get("slice") != slice_payload
    ):
        raise ValueError(
            "Fresh epoch slice is not derived from the Pack Contract"
        )
    for selected_field in (
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
    ):
        selected_ids = slice_payload[selected_field]
        if (
            not isinstance(selected_ids, list)
            or not all(
                isinstance(selected_id, str) and selected_id
                for selected_id in selected_ids
            )
            or selected_ids != sorted(set(selected_ids))
        ):
            raise ValueError(
                f"Fresh epoch slice {selected_field} are invalid"
            )
        if selected_ids != contract[selected_field]:
            raise ValueError(
                f"Fresh epoch {selected_field} do not match the frozen slice"
            )
    hard_predecessor_ids = slice_payload.get("hard_proof_predecessor_ids")
    if (
        not isinstance(hard_predecessor_ids, list)
        or not all(
            isinstance(predecessor_id, str) and predecessor_id
            for predecessor_id in hard_predecessor_ids
        )
        or hard_predecessor_ids != sorted(set(hard_predecessor_ids))
    ):
        raise ValueError(
            "Fresh epoch slice hard proof predecessor IDs are invalid"
        )
    predecessors = contract["proof_predecessors"]
    assert isinstance(predecessors, list)
    admitted_predecessor_ids = [
        predecessor["id"]
        for predecessor in predecessors
        if isinstance(predecessor, dict)
    ]
    if admitted_predecessor_ids != hard_predecessor_ids:
        raise ValueError(
            "Fresh epoch proof predecessors do not match the frozen slice"
        )
    _verify_admission_identity(
        worktree,
        contract["independent_m0"],
        "independent_m0",
    )
    for index, predecessor in enumerate(predecessors):
        assert isinstance(predecessor, dict)
        _verify_admission_identity(
            worktree,
            predecessor["p1"],
            f"proof_predecessors[{index}].p1",
        )
        _verify_admission_identity(
            worktree,
            predecessor["installed"],
            f"proof_predecessors[{index}].installed",
        )
    schedule, anchor = _admission_path(
        worktree,
        contract["schedule_pointer"],
        "schedule_pointer",
        fragment=True,
    )
    try:
        schedule_content = schedule.read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(
            f"Fresh epoch schedule pointer is unreadable: {error}"
        ) from error
    try:
        schedule_payload = json.loads(schedule_content)
    except json.JSONDecodeError:
        schedule_payload = None
    if not (
        (
            isinstance(schedule_payload, dict)
            and anchor in schedule_payload
        )
        or (
            isinstance(anchor, str)
            and _markdown_fragment_resolves(schedule, anchor)
        )
    ):
        raise ValueError("Fresh epoch schedule fragment does not resolve")
    observed_schedule = f"sha256-v1:{hashlib.sha256(schedule.read_bytes()).hexdigest()}"
    if contract["schedule_fingerprint"] != observed_schedule:
        raise ValueError("Fresh epoch schedule fingerprint does not match its pointer")

    pointers = semantic["pointers"]
    assert isinstance(pointers, dict)
    decision = pointers["decision_capsule"]
    decision_path, decision_anchor = _admission_path(
        worktree,
        decision,
        "decision_capsule",
        fragment=True,
    )
    if (
        decision_path.relative_to(worktree).as_posix() != "decisions.md"
        or not isinstance(decision_anchor, str)
        or not SAFE_ID.fullmatch(decision_anchor)
    ):
        raise ValueError("Fresh epoch decision_capsule pointer is malformed")
    research_prefix = f"docs/research/skills/{skill}/"
    research = pointers["research_packet"]
    research_path, _ = _admission_path(
        worktree,
        research,
        "research_packet",
    )
    if not research_path.relative_to(worktree).as_posix().startswith(
        research_prefix
    ):
        raise ValueError("Fresh epoch research_packet pointer has the wrong owner")
    synthesis = f"docs/synthesis/skills/{skill}.md"
    synthesis_path, _ = _admission_path(
        worktree,
        pointers["skill_synthesis"],
        "skill_synthesis",
    )
    if synthesis_path.relative_to(worktree).as_posix() != synthesis:
        raise ValueError("Fresh epoch skill_synthesis pointer has the wrong owner")
    adjacency = pointers["claim_adjacency"]
    adjacency_path, adjacency_anchor = _admission_path(
        worktree,
        adjacency,
        "claim_adjacency",
        fragment=True,
    )
    if (
        adjacency_path.relative_to(worktree).as_posix() != synthesis
        or not isinstance(adjacency_anchor, str)
        or not SAFE_ID.fullmatch(adjacency_anchor)
    ):
        raise ValueError("Fresh epoch claim_adjacency pointer has the wrong owner")
    pack_pointer = contract["pack_contract"]
    assert isinstance(pack_pointer, dict)
    if pointers["pack_synthesis"] != pack_pointer["path"]:
        raise ValueError("Fresh epoch pack_synthesis pointer disagrees with contract")


def _validate_v2_manifest_schema(manifest: dict[str, object]) -> None:
    schema = _read_json(FRESH_CAMPAIGN_SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(manifest),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        pointer = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"Fresh campaign manifest {pointer}: {error.message}")


def read_campaign_manifest(manifest_path: Path) -> dict[str, object]:
    """Read a supported manifest without rewriting historical evidence."""

    manifest = _read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("Campaign manifest must be an object")
    version = manifest.get("schema_version")
    if version == CAMPAIGN_SCHEMA_VERSION:
        campaign = manifest.get("campaign")
        mechanical = manifest.get("mechanical")
        if not isinstance(campaign, dict) or not isinstance(mechanical, dict):
            raise ValueError("Historical campaign manifest is malformed")
        return manifest
    if version == FRESH_CAMPAIGN_SCHEMA_VERSION:
        campaign = manifest.get("campaign")
        mechanical = manifest.get("mechanical")
        if not isinstance(campaign, dict) or not isinstance(mechanical, dict):
            raise ValueError("Fresh campaign section is malformed")
        admission = {
            "campaign": {
                key: campaign.get(key)
                for key in (
                    "composition_epoch_id",
                    "continuation",
                    "supersession",
                )
            },
            "contract": manifest.get("contract"),
            "semantic": manifest.get("semantic"),
        }
        _validate_fresh_epoch_admission(admission)
        _validate_v2_manifest_schema(manifest)
        supersession_digest = mechanical.get("supersession_digest")
        if (
            mechanical.get("campaign_digest")
            != _campaign_lineage_digest(campaign, supersession_digest)
            or campaign.get("epoch") != campaign.get("id")
            or (
                campaign.get("continuation") is None
                and (
                    campaign.get("supersession") is not None
                    or supersession_digest is not None
                )
            )
            or (
                campaign.get("continuation") == "restart"
                and (
                    not isinstance(campaign.get("supersession"), str)
                    or not isinstance(supersession_digest, str)
                )
            )
        ):
            raise ValueError("Fresh campaign identity or Restart lineage is invalid")
        return manifest
    raise ValueError("Campaign manifest schema is foreign")


def _contract_differences(
    expected: object,
    observed: object,
    prefix: str = "",
) -> list[str]:
    if isinstance(expected, dict) and isinstance(observed, dict):
        keys = sorted(set(expected).union(observed))
        differences: list[str] = []
        for key in keys:
            child = f"{prefix}.{key}" if prefix else str(key)
            if key not in expected or key not in observed:
                differences.append(child)
            else:
                differences.extend(
                    _contract_differences(expected[key], observed[key], child)
                )
        return differences
    return [] if expected == observed else [prefix]


def _observed_fresh_contract(
    contract: dict[str, object],
    *,
    worktree: Path,
) -> dict[str, object]:
    observed = copy.deepcopy(contract)

    def refresh(identity: object, label: str) -> None:
        if not isinstance(identity, dict):
            raise ValueError(f"Fresh epoch {label} identity is invalid")
        path, _ = _admission_path(
            worktree,
            identity.get("path"),
            f"{label}.path",
        )
        try:
            content = path.read_bytes()
        except OSError:
            identity["fingerprint"] = "missing"
        else:
            identity["fingerprint"] = (
                f"sha256-v1:{hashlib.sha256(content).hexdigest()}"
            )

    refresh(observed["pack_contract"], "pack_contract")
    refresh(observed["slice"], "slice")
    refresh(observed["independent_m0"], "independent_m0")
    predecessors = observed["proof_predecessors"]
    assert isinstance(predecessors, list)
    for index, predecessor in enumerate(predecessors):
        assert isinstance(predecessor, dict)
        refresh(predecessor["p1"], f"proof_predecessors[{index}].p1")
        refresh(
            predecessor["installed"],
            f"proof_predecessors[{index}].installed",
        )
    schedule, _ = _admission_path(
        worktree,
        observed["schedule_pointer"],
        "schedule_pointer",
        fragment=True,
    )
    try:
        schedule_content = schedule.read_bytes()
    except OSError:
        observed["schedule_fingerprint"] = "missing"
    else:
        observed["schedule_fingerprint"] = (
            f"sha256-v1:{hashlib.sha256(schedule_content).hexdigest()}"
        )
    return observed


def check_fresh_contract(
    manifest_path: Path,
    observed_contract: dict[str, object],
) -> dict[str, object]:
    """Detect immutable contract drift and return the choice to its owner."""

    manifest = read_campaign_manifest(manifest_path)
    if manifest.get("schema_version") != FRESH_CAMPAIGN_SCHEMA_VERSION:
        raise ValueError("Contract drift checks require a v2 manifest")
    contract = manifest.get("contract")
    mechanical = manifest.get("mechanical")
    if not isinstance(contract, dict) or not isinstance(mechanical, dict):
        raise ValueError("Fresh campaign ownership sections are invalid")
    differences = _contract_differences(contract, observed_contract)
    if not differences:
        return {
            "status": "verified",
            "changed_contract_fields": [],
        }
    receipts = mechanical.get("receipts")
    if not isinstance(receipts, list):
        raise ValueError("Fresh campaign receipts must be a list")
    invalidations = mechanical.get("invalidations")
    if not isinstance(invalidations, list):
        raise ValueError("Fresh campaign invalidations must be a list")
    def depends_on_drift(receipt: object) -> bool:
        if not isinstance(receipt, dict):
            return False
        identity = receipt.get("fresh_epoch_identity")
        if not isinstance(identity, dict):
            return False
        selective = {
            "selected_relationship_ids": "relationship_ids",
            "selected_scenario_ids": "scenario_ids",
        }
        nonselective = [
            difference
            for difference in differences
            if difference not in selective
        ]
        if nonselective:
            return True
        for contract_field, identity_field in selective.items():
            if contract_field not in differences:
                continue
            expected_values = contract.get(contract_field)
            observed_values = observed_contract.get(contract_field)
            relevant_values = identity.get(identity_field)
            if not all(
                isinstance(values, list)
                for values in (
                    expected_values,
                    observed_values,
                    relevant_values,
                )
            ):
                return True
            changed_values = set(expected_values).symmetric_difference(
                observed_values
            )
            if changed_values.intersection(relevant_values):
                return True
        return False

    receipt_ids = sorted(
        str(receipt["id"])
        for receipt in receipts
        if (
            isinstance(receipt, dict)
            and isinstance(receipt.get("id"), str)
            and depends_on_drift(receipt)
        )
    )
    invalidations.append(
        {
            "changed_contract_fields": differences,
            "receipt_ids": receipt_ids,
            "observed_at": _now(),
        }
    )
    update_mechanical_state(
        manifest_path,
        {
            "evidence_state": "stale",
            "invalidations": invalidations,
        },
    )
    result = _failure(
        "stale",
        "contract-drift",
        manifest_path,
        "Immutable Fresh campaign contract drifted",
    )
    result.update({
        "changed_contract_fields": differences,
        "stale_receipts": receipt_ids,
        "owner_action_required": ["resume", "repair", "restart"],
    })
    return result


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
    fresh_epoch: dict[str, object] | None = None,
    _supersedes: str | None = None,
    _held_lease: dict[str, object] | None = None,
    _restart_source: Path | None = None,
) -> dict[str, object]:
    """Create one exact campaign epoch and acquire its worktree lease."""

    skill = _validate_id(skill, "Skill")
    if owner_token is not None and not _valid_owner_token(owner_token):
        raise ValueError("Campaign owner token must be a nonempty string")
    if delivery_mode not in DELIVERY_MODES:
        raise ValueError("Delivery mode must be one of: none, commit, push")
    resolved_worktree = (worktree or Path.cwd()).resolve()
    authenticated_restart_lease: dict[str, object] | None = None
    restart_source_manifest: dict[str, object] | None = None
    if _held_lease is not None:
        if _restart_source is None:
            raise ValueError(
                "Internal Restart handoff requires an authenticated source"
            )
        try:
            source_campaign_id, restart_source_manifest = _control_identity(
                _restart_source,
                resolved_worktree,
            )
            live_lease = _read_json(resolved_worktree / LEASE_PATH)
            source_pointer = (
                _restart_source.resolve()
                .relative_to(resolved_worktree)
                .as_posix()
            )
            if (
                restart_source_manifest.get("schema_version")
                == FRESH_CAMPAIGN_SCHEMA_VERSION
                and isinstance(live_lease, dict)
            ):
                _validate_v2_campaign_identity(
                    restart_source_manifest,
                    worktree=resolved_worktree,
                    manifest_path=_restart_source,
                    lease=live_lease,
                )
        except (OSError, json.JSONDecodeError, ValueError) as error:
            raise ValueError(
                "Internal Restart handoff requires an authenticated source"
            ) from error
        if (
            not isinstance(live_lease, dict)
            or live_lease != _held_lease
            or live_lease.get("worktree") != str(resolved_worktree)
            or live_lease.get("campaign_id") != source_campaign_id
            or not _valid_owner_token(owner_token)
            or not _valid_owner_token(live_lease.get("owner_token"))
            or live_lease.get("owner_token") != owner_token
            or _supersedes != source_pointer
        ):
            raise ValueError(
                "Internal Restart handoff requires an authenticated source"
            )
        authenticated_restart_lease = copy.deepcopy(live_lease)
        if (
            restart_source_manifest.get("schema_version")
            == FRESH_CAMPAIGN_SCHEMA_VERSION
            and fresh_epoch is None
        ):
            raise ValueError(
                "Fresh Restart requires a new Fresh admission"
            )
    if fresh_epoch is not None:
        _validate_fresh_epoch_admission(fresh_epoch)
        _validate_fresh_epoch_references(
            fresh_epoch,
            worktree=resolved_worktree,
            skill=skill,
        )
        fresh_campaign = fresh_epoch["campaign"]
        assert isinstance(fresh_campaign, dict)
        if continuation is None:
            if _held_lease is None and (
                fresh_campaign.get("continuation") is not None
                or fresh_campaign.get("supersession") is not None
            ):
                raise ValueError(
                    "An ordinary Fresh start requires null continuation "
                    "and supersession"
                )
            if _held_lease is not None and (
                fresh_campaign.get("continuation") != "restart"
                or fresh_campaign.get("supersession") != _supersedes
            ):
                raise ValueError(
                    "Fresh Restart requires the exact source supersession"
                )
    if authenticated_restart_lease is not None:
        assert isinstance(restart_source_manifest, dict)
        source_campaign = restart_source_manifest.get("campaign")
        source_semantic = restart_source_manifest.get("semantic")
        if not isinstance(source_campaign, dict):
            raise ValueError(
                "Internal Restart handoff requires an authenticated source"
            )
        restart_identity_unchanged = (
            source_campaign.get("skill") == skill
            and source_campaign.get("delivery_mode") == delivery_mode
        )
        if (
            restart_source_manifest.get("schema_version")
            == FRESH_CAMPAIGN_SCHEMA_VERSION
        ):
            fresh_campaign = (
                fresh_epoch.get("campaign")
                if isinstance(fresh_epoch, dict)
                else None
            )
            fresh_contract = (
                fresh_epoch.get("contract")
                if isinstance(fresh_epoch, dict)
                else None
            )
            restart_identity_unchanged = (
                restart_identity_unchanged
                and isinstance(fresh_campaign, dict)
                and fresh_campaign.get("composition_epoch_id")
                == source_campaign.get("composition_epoch_id")
                and fresh_contract == restart_source_manifest.get("contract")
            )
        if restart_identity_unchanged and not _semantic_terminal(
            source_semantic,
        ):
            raise ValueError(
                "Restart requires changed identity, delivery authority, "
                "or terminal state"
            )
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
            fresh_epoch=fresh_epoch,
        )
    selected_campaign_id = _validate_id(
        campaign_id or _campaign_id(skill),
        "Campaign ID",
    )
    selected_owner_token = owner_token if owner_token is not None else f"codex/{uuid4()}"
    manifest_path = _campaign_manifest_path(
        resolved_worktree,
        selected_campaign_id,
        skill if fresh_epoch is not None else None,
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
    if fresh_epoch is None:
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
                "proof_registrations": [],
                "receipts": [],
                "invalidations": [],
            },
        }
    else:
        campaign_input = fresh_epoch.get("campaign")
        contract_input = fresh_epoch.get("contract")
        semantic_input = fresh_epoch.get("semantic")
        if not all(
            isinstance(section, dict)
            for section in (campaign_input, contract_input, semantic_input)
        ):
            raise ValueError(
                "Fresh epoch admission requires campaign, contract, and semantic"
            )
        assert isinstance(campaign_input, dict)
        campaign_record = {
            "id": selected_campaign_id,
            "skill": skill,
            "epoch": selected_campaign_id,
            "composition_epoch_id": campaign_input.get(
                "composition_epoch_id"
            ),
            "delivery_mode": delivery_mode,
            "continuation": campaign_input.get("continuation"),
            "supersession": campaign_input.get("supersession"),
            "worktree": str(resolved_worktree),
        }
        supersession_digest = (
            restart_source_manifest["mechanical"]["campaign_digest"]
            if isinstance(restart_source_manifest, dict)
            and isinstance(restart_source_manifest.get("mechanical"), dict)
            and isinstance(
                restart_source_manifest["mechanical"].get("campaign_digest"),
                str,
            )
            else None
        )
        campaign_digest = _campaign_lineage_digest(
            campaign_record,
            supersession_digest,
        )
        manifest = {
            "schema_version": FRESH_CAMPAIGN_SCHEMA_VERSION,
            "campaign": campaign_record,
            "contract": copy.deepcopy(contract_input),
            "semantic": copy.deepcopy(semantic_input),
            "mechanical": {
                "created_at": created_at,
                "verified_at": None,
                "campaign_digest": campaign_digest,
                "supersession_digest": supersession_digest,
                "contract_digest": _canonical_json_sha256(contract_input),
                "artifact_identities": [],
                "proof_registrations": [],
                "preflight_registrations": [],
                "receipts": [],
                "invalidations": [],
                "parity": None,
                "evidence_state": "current",
            },
        }
        lease["campaign_digest"] = campaign_digest
        lease["supersession_digest"] = supersession_digest
        _validate_v2_manifest_schema(manifest)
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
        if authenticated_restart_lease is not None:
            try:
                current_lease = _read_json(lease_path)
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError(
                    "Internal Restart handoff lost its authenticated source"
                ) from error
            if current_lease != authenticated_restart_lease:
                raise ValueError(
                    "Internal Restart handoff lost its authenticated source"
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
    fresh_epoch: dict[str, object] | None,
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
        or not _valid_owner_token(owner_token)
        or not _valid_owner_token(lease.get("owner_token"))
        or lease.get("owner_token") != owner_token
    ):
        return _failure(
            "lease-conflict",
            "lease",
            from_manifest,
            "Continuation does not own the exact source campaign lease",
        )
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        try:
            _validate_v2_campaign_identity(
                manifest,
                worktree=worktree,
                manifest_path=from_manifest,
                lease=lease,
            )
        except ValueError as error:
            return _failure(
                "failed",
                "manifest-schema",
                from_manifest,
                str(error),
            )

    identity_unchanged = (
        campaign.get("skill") == skill
        and campaign.get("delivery_mode") == delivery_mode
    )
    relative_manifest = from_manifest.resolve().relative_to(worktree).as_posix()
    if continuation == "resume":
        if not identity_unchanged or _semantic_terminal(semantic):
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Resume requires unchanged identity and a nonterminal campaign",
            )
        if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
            contract = manifest.get("contract")
            if (
                not isinstance(contract, dict)
                or mechanical.get("evidence_state") != "current"
                or mechanical.get("contract_digest")
                != _canonical_json_sha256(contract)
            ):
                return _failure(
                    "failed",
                    "continuation",
                    from_manifest,
                    "Fresh Resume requires current sealed contract evidence",
                )
            try:
                observed_contract = _observed_fresh_contract(
                    contract,
                    worktree=worktree,
                )
            except (OSError, ValueError) as error:
                return _failure(
                    "failed",
                    "continuation",
                    from_manifest,
                    f"Fresh Resume cannot resolve current contract: {error}",
                )
            fresh_campaign = (
                fresh_epoch.get("campaign")
                if isinstance(fresh_epoch, dict)
                else None
            )
            fresh_contract = (
                fresh_epoch.get("contract")
                if isinstance(fresh_epoch, dict)
                else None
            )
            if (
                observed_contract != contract
                or (
                    fresh_epoch is not None
                    and (
                        not isinstance(fresh_campaign, dict)
                        or fresh_campaign.get("composition_epoch_id")
                        != campaign.get("composition_epoch_id")
                        or fresh_contract != contract
                    )
                )
            ):
                return _failure(
                    "failed",
                    "continuation",
                    from_manifest,
                    "Fresh Resume requires unchanged live and admitted contract identity",
                )
        return {
            "status": "verified",
            "campaign_id": prior_campaign_id,
            "manifest": relative_manifest,
            "continuation": "resume",
        }

    if continuation == "repair":
        if not identity_unchanged or _semantic_terminal(semantic):
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

    restart_identity_unchanged = identity_unchanged
    if (
        manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION
        and fresh_epoch is not None
    ):
        fresh_campaign = fresh_epoch.get("campaign")
        fresh_contract = fresh_epoch.get("contract")
        restart_identity_unchanged = (
            restart_identity_unchanged
            and isinstance(fresh_campaign, dict)
            and fresh_campaign.get("composition_epoch_id")
            == campaign.get("composition_epoch_id")
            and fresh_contract == manifest.get("contract")
        )
    if restart_identity_unchanged and not _semantic_terminal(semantic):
        return _failure(
            "failed",
            "continuation",
            from_manifest,
            "Restart requires changed identity, delivery authority, or terminal state",
        )
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        if fresh_epoch is None:
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Fresh Restart requires a new owner-authored admission packet",
            )
        fresh_campaign = fresh_epoch.get("campaign")
        if (
            not isinstance(fresh_campaign, dict)
            or fresh_campaign.get("continuation") != "restart"
            or fresh_campaign.get("supersession") != relative_manifest
        ):
            return _failure(
                "failed",
                "continuation",
                from_manifest,
                "Fresh Restart admission must point to the exact source manifest",
            )
    return start_campaign(
        skill,
        delivery_mode,
        worktree=worktree,
        campaign_id=campaign_id,
        owner_token=owner_token,
        _supersedes=relative_manifest,
        _held_lease=lease,
        _restart_source=from_manifest,
        fresh_epoch=fresh_epoch,
    )


def update_mechanical_state(
    manifest_path: Path,
    updates: dict[str, object],
) -> dict[str, object]:
    """Atomically update only the automation-owned manifest section."""

    forbidden = {
        "campaign",
        "contract",
        "semantic",
        "schema_version",
    }.intersection(updates)
    forbidden.update(
        {
            "campaign_digest",
            "contract_digest",
            "supersession_digest",
        }.intersection(updates)
    )
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
    version = manifest.get("schema_version")
    campaign = manifest.get("campaign")
    if version not in {
        CAMPAIGN_SCHEMA_VERSION,
        FRESH_CAMPAIGN_SCHEMA_VERSION,
    } or not isinstance(campaign, dict):
        raise ValueError("Campaign mechanical-update identity is invalid")
    worktree_value = campaign.get("worktree")
    campaign_id = campaign.get("id")
    skill = campaign.get("skill")
    if (
        not isinstance(worktree_value, str)
        or not isinstance(campaign_id, str)
        or not SAFE_ID.fullmatch(campaign_id)
        or not isinstance(skill, str)
        or not SAFE_ID.fullmatch(skill)
        or (
            version == FRESH_CAMPAIGN_SCHEMA_VERSION
            and not isinstance(skill, str)
        )
    ):
        raise ValueError("Campaign mechanical-update identity is invalid")
    worktree = Path(worktree_value).resolve()
    if worktree_value != str(worktree):
        raise ValueError("Campaign mechanical-update identity is invalid")
    expected_manifest = _campaign_manifest_path(
        worktree,
        campaign_id,
        skill if version == FRESH_CAMPAIGN_SCHEMA_VERSION else None,
    ).resolve()
    try:
        lease = _read_json(worktree / LEASE_PATH)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(
            "Mechanical update requires its exact live lease"
        ) from error
    if (
        manifest_path.resolve() != expected_manifest
        or not isinstance(lease, dict)
        or lease.get("worktree") != str(worktree)
        or lease.get("campaign_id") != campaign_id
        or not isinstance(lease.get("owner_token"), str)
        or not lease.get("owner_token")
    ):
        raise ValueError("Mechanical update requires its exact live lease")
    protected_before = {
        key: copy.deepcopy(manifest.get(key))
        for key in ("campaign", "contract", "semantic")
    }
    manifest["mechanical"].update(copy.deepcopy(updates))
    if any(manifest.get(key) != value for key, value in protected_before.items()):
        raise ValueError("Mechanical updates cannot alter protected fields")
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        _validate_v2_manifest_schema(manifest)
        _validate_v2_campaign_identity(
            manifest,
            worktree=worktree,
            manifest_path=manifest_path,
            lease=lease,
        )
    _replace_json_file(manifest_path, manifest)
    return manifest


def _failure(
    status: str,
    gate: str,
    manifest_path: Path,
    message: str,
    *,
    expensive_work_skipped: bool = True,
) -> dict[str, object]:
    if status not in MECHANICAL_STATUSES:
        raise ValueError(f"Unknown mechanical status: {status}")
    return {
        "status": status,
        "gate": gate,
        "artifact": str(manifest_path),
        "message": message,
        "expected_state": "verified",
        "actual_state": status,
        "expensive_work_skipped": expensive_work_skipped,
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


def _validate_v2_campaign_identity(
    manifest: dict[str, object],
    *,
    worktree: Path,
    manifest_path: Path,
    lease: dict[str, object] | None = None,
    lineage_seen: frozenset[Path] = frozenset(),
    lineage_depth: int = 0,
) -> None:
    resolved_manifest = manifest_path.resolve()
    if (
        resolved_manifest in lineage_seen
        or lineage_depth >= MAX_RESTART_LINEAGE_DEPTH
    ):
        raise ValueError("Fresh campaign Restart lineage is cyclic or too deep")
    lineage_seen = lineage_seen.union({resolved_manifest})
    campaign = manifest.get("campaign")
    mechanical = manifest.get("mechanical")
    if not isinstance(campaign, dict) or not isinstance(mechanical, dict):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    campaign_id = campaign.get("id")
    skill = campaign.get("skill")
    continuation = campaign.get("continuation")
    supersession = campaign.get("supersession")
    supersession_digest = mechanical.get("supersession_digest")
    campaign_digest = _campaign_lineage_digest(
        campaign,
        supersession_digest,
    )
    if (
        mechanical.get("campaign_digest") != campaign_digest
        or campaign.get("epoch") != campaign_id
        or campaign.get("worktree") != str(worktree)
        or not isinstance(campaign_id, str)
        or not SAFE_ID.fullmatch(campaign_id)
        or not isinstance(skill, str)
        or not SAFE_ID.fullmatch(skill)
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    if lease is not None and (
        lease.get("campaign_digest") != campaign_digest
        or lease.get("campaign_id") != campaign_id
        or lease.get("supersession_digest") != supersession_digest
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    if continuation is None and supersession is None:
        if supersession_digest is not None:
            raise ValueError(
                "Fresh campaign identity or Restart lineage is invalid"
            )
        return
    if (
        continuation != "restart"
        or not isinstance(supersession, str)
        or not isinstance(supersession_digest, str)
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    source = (worktree / supersession).resolve()
    expected_source_root = (worktree / FRESH_CAMPAIGN_ROOT / skill / "campaigns").resolve()
    if (
        not _is_within(source, expected_source_root)
        or source == manifest_path.resolve()
        or not source.is_file()
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    try:
        source_manifest = read_campaign_manifest(source)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            "Fresh campaign identity or Restart lineage is invalid"
        ) from error
    source_campaign = (
        source_manifest.get("campaign")
        if isinstance(source_manifest, dict)
        else None
    )
    source_id = (
        source_campaign.get("id")
        if isinstance(source_campaign, dict)
        else None
    )
    if (
        not isinstance(source_manifest, dict)
        or source_manifest.get("schema_version") != FRESH_CAMPAIGN_SCHEMA_VERSION
        or not isinstance(source_campaign, dict)
        or source_campaign.get("epoch") != source_id
        or source_campaign.get("skill") != skill
        or source_campaign.get("worktree") != str(worktree)
        or not isinstance(source_id, str)
        or not SAFE_ID.fullmatch(source_id)
        or source
        != _campaign_manifest_path(worktree, source_id, skill).resolve()
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")
    _validate_v2_campaign_identity(
        source_manifest,
        worktree=worktree,
        manifest_path=source,
        lineage_seen=lineage_seen,
        lineage_depth=lineage_depth + 1,
    )
    source_mechanical = source_manifest.get("mechanical")
    if (
        not isinstance(source_mechanical, dict)
        or supersession_digest != source_mechanical.get("campaign_digest")
    ):
        raise ValueError("Fresh campaign identity or Restart lineage is invalid")


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
    version = manifest.get("schema_version")
    skill = campaign.get("skill")
    expected_path = _campaign_manifest_path(
        worktree,
        str(campaign_id),
        str(skill) if version == FRESH_CAMPAIGN_SCHEMA_VERSION else None,
    )
    if (
        version not in {CAMPAIGN_SCHEMA_VERSION, FRESH_CAMPAIGN_SCHEMA_VERSION}
        or campaign.get("worktree") != str(worktree)
        or not isinstance(campaign_id, str)
        or not SAFE_ID.fullmatch(campaign_id)
        or not isinstance(skill, str)
        or not SAFE_ID.fullmatch(skill)
        or supplied_manifest != expected_path.resolve()
    ):
        raise ValueError("Manifest identity does not match its exact worktree path")
    if version == FRESH_CAMPAIGN_SCHEMA_VERSION:
        _validate_v2_campaign_identity(
            manifest,
            worktree=worktree,
            manifest_path=supplied_manifest,
        )
    return campaign_id, manifest


def _semantic_stage(semantic: object) -> object:
    if not isinstance(semantic, dict):
        return None
    return semantic.get("stage_token", semantic.get("declared_stage"))


def _semantic_terminal(semantic: object) -> bool:
    if not isinstance(semantic, dict):
        return False
    if "terminal_token" in semantic:
        return semantic.get("terminal_token") is not None
    return semantic.get("terminal") is True


def _git_delivery_status(
    worktree: Path,
    delivery_mode: object,
) -> dict[str, object]:
    result: dict[str, object] = {
        "delivery_mode": delivery_mode,
        "local_head": None,
        "branch": "unavailable",
        "tracking_ref": None,
        "remote_head": None,
        "parity": "unavailable",
    }
    if delivery_mode not in {"commit", "push"}:
        return result
    head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if head.returncode != 0 or not head.stdout.strip():
        return result
    result["local_head"] = head.stdout.strip()
    branch = subprocess.run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if branch.returncode != 0 or not branch.stdout.strip():
        result["branch"] = "detached"
        return result
    result["branch"] = branch.stdout.strip()
    tracking = subprocess.run(
        [
            "git",
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
        ],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if tracking.returncode != 0 or not tracking.stdout.strip():
        return result
    result["tracking_ref"] = tracking.stdout.strip()
    remote = subprocess.run(
        ["git", "rev-parse", "--verify", tracking.stdout.strip()],
        cwd=worktree,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if remote.returncode != 0 or not remote.stdout.strip():
        return result
    result["remote_head"] = remote.stdout.strip()
    result["parity"] = (
        "match"
        if result["local_head"] == result["remote_head"]
        else "diverged"
    )
    return result


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
        or not _valid_owner_token(lease.get("owner_token"))
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        try:
            _validate_v2_campaign_identity(
                manifest,
                worktree=resolved_worktree,
                manifest_path=manifest_path,
                lease=lease,
            )
        except ValueError as error:
            return _failure(
                "failed",
                "manifest-schema",
                manifest_path,
                str(error),
            )
    lease["status_read_at"] = _now()
    _replace_json_file(lease_path, lease)
    semantic = manifest.get("semantic")
    stage = _semantic_stage(semantic)
    campaign = manifest.get("campaign")
    delivery_status = _git_delivery_status(
        resolved_worktree,
        campaign.get("delivery_mode") if isinstance(campaign, dict) else None,
    )
    mechanical = manifest.get("mechanical")
    if isinstance(mechanical, dict):
        receipts = mechanical.get("receipts", [])
        invalidations = mechanical.get("invalidations", [])
        registrations = mechanical.get("proof_registrations", [])
        if (
            isinstance(receipts, list)
            and isinstance(invalidations, list)
            and isinstance(registrations, list)
            and all(isinstance(receipt, dict) for receipt in receipts)
        ):
            stale_receipts = _stale_receipts_from_invalidations(
                receipts,
                invalidations,
            )
            receipt_registrations = {
                str(receipt.get("registration_id"))
                for receipt in receipts
                if receipt.get("id") in stale_receipts
            }
            stale_stages = {
                registration.get("stage", stage)
                for registration in registrations
                if isinstance(registration, dict)
                and registration.get("id") in receipt_registrations
                and registration.get("stage", stage) in STAGE_PROFILES
            }
            if mechanical.get("evidence_state") == "stale" and not stale_stages:
                if stage in STAGE_PROFILES:
                    stale_stages.add(stage)
            if stale_stages:
                return {
                    "status": "stale",
                    "campaign_id": campaign_id,
                    "stage": stage,
                    "earliest_stale_stage": min(
                        stale_stages,
                        key=STAGE_ORDER.index,
                    ),
                    "owner_token": lease.get("owner_token"),
                    "lease": "owned",
                    "git_delivery": delivery_status,
                }
    return {
        "status": "verified",
        "campaign_id": campaign_id,
        "stage": stage,
        "owner_token": lease.get("owner_token"),
        "lease": "owned",
        "git_delivery": delivery_status,
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
        or not _valid_owner_token(lease.get("owner_token"))
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        try:
            _validate_v2_campaign_identity(
                manifest,
                worktree=resolved_worktree,
                manifest_path=manifest_path,
                lease=lease,
            )
        except ValueError as error:
            return _failure(
                "failed",
                "manifest-schema",
                manifest_path,
                str(error),
            )
    exact_owner = (
        _valid_owner_token(owner_token)
        and _valid_owner_token(lease.get("owner_token"))
        and owner_token == lease.get("owner_token")
    )
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


def _contained_artifact_path(candidate_root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("Identity path must be a nonempty relative path")
    path = (candidate_root / value).resolve()
    if not _is_within(path, candidate_root):
        raise ValueError("Identity path escapes the explicit candidate root")
    return path


def artifact_identity(
    specification: dict[str, object],
    *,
    candidate_root: Path | None,
) -> dict[str, str]:
    """Compute one versioned identity at its explicitly bounded artifact."""

    if candidate_root is None:
        raise ValueError("Identity requires an explicit candidate root")
    root = candidate_root.resolve()
    algorithm = specification.get("algorithm")
    if algorithm not in IDENTITY_ALGORITHMS:
        raise ValueError("Identity algorithm is foreign or legacy")
    if algorithm == "git-object-v1":
        revision = specification.get("revision")
        if not isinstance(revision, str) or not revision:
            raise ValueError("Git object identity requires an explicit revision")
        top_level = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
        if (
            top_level.returncode != 0
            or Path(top_level.stdout.strip()).resolve() != root
        ):
            raise ValueError(
                "Git object identity candidate root must be the worktree root"
            )
        completed = subprocess.run(
            ["git", "rev-parse", "--verify", f"{revision}^{{tree}}"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
        if completed.returncode != 0:
            raise ValueError(
                "Git object identity cannot resolve the explicit candidate root"
            )
        digest = completed.stdout.strip()
        if not digest:
            raise ValueError("Git object identity returned an empty object")
        return {"algorithm": algorithm, "digest": digest}

    path = _contained_artifact_path(root, specification.get("path"))
    if algorithm == "campaign-tree-v1":
        result = campaign_tree_hash(path)
        return {"algorithm": algorithm, "digest": str(result["sha256"])}
    if algorithm == "canonical-json-v1":
        return {
            "algorithm": algorithm,
            "digest": _canonical_json_sha256(_read_json(path)),
        }

    marker = specification.get("marker")
    if not isinstance(marker, str) or not SAFE_ID.fullmatch(marker):
        raise ValueError("Semantic identity requires a bounded marker ID")
    content = path.read_text(encoding="utf-8")
    begin = f"<!-- campaign-semantic:{marker}:begin -->\n"
    end = f"<!-- campaign-semantic:{marker}:end -->"
    if content.count(begin) != 1 or content.count(end) != 1:
        raise ValueError("Semantic identity markers must each occur exactly once")
    begin_at = content.index(begin) + len(begin)
    end_at = content.index(end)
    if end_at < begin_at:
        raise ValueError("Semantic identity markers must be ordered")
    bounded = content[begin_at:end_at]
    return {
        "algorithm": algorithm,
        "digest": hashlib.sha256(bounded.encode("utf-8")).hexdigest(),
    }


def _environment_identity(candidate_root: Path) -> dict[str, str]:
    dependency_digest = hashlib.sha256()
    for name in ("pyproject.toml", "requirements-dev.txt"):
        path = candidate_root / name
        if path.is_file():
            content = path.read_bytes()
            dependency_digest.update(name.encode("utf-8"))
            dependency_digest.update(b"\0")
            dependency_digest.update(hashlib.sha256(content).digest())
    packages = sorted(
        (
            (distribution.metadata.get("Name") or "").lower(),
            distribution.version,
        )
        for distribution in importlib.metadata.distributions()
    )
    return {
        "python": sys.version.split()[0],
        "implementation": sys.implementation.name,
        "platform": sys.platform,
        "executable": str(Path(sys.executable).resolve()),
        "dependency_files_sha256": dependency_digest.hexdigest(),
        "installed_packages_sha256": _canonical_json_sha256(packages),
        "ambient_environment_sha256": _canonical_json_sha256(
            sorted(os.environ.items())
        ),
    }


def _registration_candidate_root(
    registration: dict[str, object],
    worktree: Path,
) -> Path:
    value = registration.get("candidate_root")
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("Proof registration requires a relative candidate root")
    root = (worktree / value).resolve()
    if not _is_within(root, worktree) or not root.is_dir():
        raise ValueError("Proof candidate root escapes or does not exist")
    return root


def _full_suite_worktree_matches(
    candidate_root: Path,
    target_digest: str,
) -> bool:
    excluded = (
        ":(exclude).tmp/**",
        f":(exclude){CAMPAIGN_ROOT.as_posix()}/**",
        f":(exclude){FRESH_CAMPAIGN_ROOT.as_posix()}/*/campaigns/**",
    )
    tracked = subprocess.run(
        ["git", "diff", "--quiet", target_digest, "--", ".", *excluded],
        cwd=candidate_root,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if tracked.returncode != 0:
        return False
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=candidate_root,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if untracked.returncode != 0:
        return False
    for value in untracked.stdout.split("\0"):
        if not value:
            continue
        path = Path(value)
        if path.parts[:1] == (".tmp",):
            continue
        if path.parts[: len(CAMPAIGN_ROOT.parts)] == CAMPAIGN_ROOT.parts:
            continue
        if (
            path.parts[: len(FRESH_CAMPAIGN_ROOT.parts)]
            == FRESH_CAMPAIGN_ROOT.parts
            and len(path.parts) >= len(FRESH_CAMPAIGN_ROOT.parts) + 3
            and path.parts[len(FRESH_CAMPAIGN_ROOT.parts) + 1] == "campaigns"
        ):
            continue
        return False
    return True


def proof_identity_tuple(
    registration: dict[str, object],
    *,
    candidate_root: Path,
) -> dict[str, object]:
    """Return the complete reusable identity tuple for one registration."""

    profile_name = registration.get("profile")
    profile = PROOF_PROFILES.get(str(profile_name))
    if (
        profile is None
        or profile.get("schema_version") != PROOF_PROFILE_SCHEMA_VERSION
    ):
        raise ValueError("Proof profile is not versioned and allowlisted")
    inputs = registration.get("inputs")
    target = registration.get("target")
    if not isinstance(inputs, list) or not inputs or not isinstance(target, dict):
        raise ValueError("Proof registration inputs and target are incomplete")
    normalized_inputs: list[dict[str, str]] = []
    for item in inputs:
        if not isinstance(item, dict):
            raise ValueError("Proof input identity must be an object")
        name = item.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("Proof input identity requires a name")
        computed = artifact_identity(item, candidate_root=candidate_root)
        expected = item.get("digest")
        if expected != computed["digest"]:
            raise ValueError(f"Proof input identity mismatch: {name}")
        normalized_input = {
            "name": name,
            **computed,
            "candidate_root": str(candidate_root.resolve()),
        }
        for locator in ("path", "revision", "marker"):
            value = item.get(locator)
            if isinstance(value, str):
                normalized_input[locator] = value
        normalized_inputs.append(normalized_input)
    computed_target = artifact_identity(target, candidate_root=candidate_root)
    if target.get("digest") != computed_target["digest"]:
        raise ValueError("Proof target identity mismatch")
    target_identity: dict[str, str] = {
        **computed_target,
        "candidate_root": str(candidate_root.resolve()),
    }
    for locator in ("path", "revision", "marker"):
        value = target.get(locator)
        if isinstance(value, str):
            target_identity[locator] = value
    result = {
        "proof_profile": profile_name,
        "inputs": sorted(normalized_inputs, key=lambda item: item["name"]),
        "target": target_identity,
        "environment": _environment_identity(candidate_root),
    }
    fresh_identity = registration.get("fresh_epoch_identity")
    if fresh_identity is not None:
        required = {
            "composition_epoch_id",
            "pack_contract_revision",
            "slice_fingerprint",
            "relationship_ids",
            "scenario_ids",
        }
        if not isinstance(fresh_identity, dict) or set(fresh_identity) != required:
            raise ValueError("Fresh proof identity tuple is incomplete")
        if not re.fullmatch(
            r"FCE-[0-9]{8}-[0-9]{2}",
            str(fresh_identity.get("composition_epoch_id")),
        ):
            raise ValueError("Fresh proof composition epoch is malformed")
        if not isinstance(fresh_identity.get("pack_contract_revision"), str):
            raise ValueError("Fresh proof pack contract revision is malformed")
        if not EXACT_FINGERPRINT.fullmatch(
            str(fresh_identity.get("slice_fingerprint"))
        ):
            raise ValueError("Fresh proof slice fingerprint is malformed")
        for field in ("relationship_ids", "scenario_ids"):
            values = fresh_identity.get(field)
            if (
                not isinstance(values, list)
                or values != sorted(set(values))
                or not all(isinstance(value, str) and value for value in values)
            ):
                raise ValueError(f"Fresh proof {field} are malformed")
        result["fresh_epoch_identity"] = copy.deepcopy(fresh_identity)
    return result


def make_receipt(
    registration: dict[str, object],
    identity_tuple: dict[str, object],
    *,
    exit_code: int,
    output_digest: str,
    source: str,
    receipt_id: str | None = None,
    observed_at: str | None = None,
    supersedes: str | None = None,
    forced_reason: str | None = None,
) -> dict[str, object]:
    """Create one compact receipt; callers append it without rewriting history."""

    receipt: dict[str, object] = {
        "schema_version": PROOF_RECEIPT_SCHEMA_VERSION,
        "id": receipt_id or f"receipt-{uuid4().hex}",
        "registration_id": registration.get("id"),
        "stage": registration.get("stage"),
        "proof_profile": identity_tuple["proof_profile"],
        "inputs": copy.deepcopy(identity_tuple["inputs"]),
        "target": copy.deepcopy(identity_tuple["target"]),
        "environment": copy.deepcopy(identity_tuple["environment"]),
        "exit_state": {
            "code": exit_code,
            "status": "passed" if exit_code == 0 else "failed",
        },
        "output_digest": output_digest,
        "observed_at": observed_at or _now(),
        "source": source,
        "supersedes": supersedes,
        "forced_reason": forced_reason,
    }
    if "fresh_epoch_identity" in identity_tuple:
        receipt["fresh_epoch_identity"] = copy.deepcopy(
            identity_tuple["fresh_epoch_identity"]
        )
    _seal_receipt(receipt)
    return receipt


def _seal_receipt(receipt: dict[str, object]) -> None:
    payload = {
        key: value
        for key, value in receipt.items()
        if key != "receipt_digest"
    }
    receipt["receipt_digest"] = _canonical_json_sha256(payload)


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _valid_timestamp(value: object, *, allow_future: bool = False) -> bool:
    parsed = _parse_timestamp(value)
    return parsed is not None and (
        allow_future
        or parsed <= datetime.now(UTC) + timedelta(minutes=5)
    )


def _valid_identity_record(value: object, *, require_name: bool) -> bool:
    if not isinstance(value, dict):
        return False
    name_valid = (
        isinstance(value.get("name"), str) and bool(value.get("name"))
        if require_name
        else True
    )
    algorithm = value.get("algorithm")
    digest = value.get("digest")
    digest_valid = (
        isinstance(digest, str)
        and (
            bool(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", digest))
            if algorithm == "git-object-v1"
            else bool(SHA256_HEX.fullmatch(digest))
        )
    )
    return name_valid and algorithm in IDENTITY_ALGORITHMS and digest_valid


def _valid_legacy_identity_record(
    value: object,
    *,
    require_name: bool,
) -> bool:
    if not _valid_identity_record(value, require_name=require_name):
        return False
    assert isinstance(value, dict)
    algorithm = value["algorithm"]
    expected = {"algorithm", "digest", "candidate_root"}
    if require_name:
        expected.add("name")
    if algorithm == "git-object-v1":
        expected.add("revision")
    else:
        expected.add("path")
        if algorithm == "marker-semantic-v1":
            expected.add("marker")
    return (
        set(value) == expected
        and isinstance(value.get("candidate_root"), str)
        and bool(value.get("candidate_root"))
        and all(
            isinstance(value.get(locator), str) and bool(value.get(locator))
            for locator in expected.intersection({"path", "revision", "marker"})
        )
    )


def _valid_receipt(receipt: object) -> bool:
    if not isinstance(receipt, dict):
        return False
    receipt_id = receipt.get("id")
    registration_id = receipt.get("registration_id")
    inputs = receipt.get("inputs")
    target = receipt.get("target")
    environment = receipt.get("environment")
    exit_state = receipt.get("exit_state")
    source = receipt.get("source")
    supersedes = receipt.get("supersedes")
    forced_reason = receipt.get("forced_reason")
    fresh_epoch_identity = receipt.get("fresh_epoch_identity")
    try:
        computed_receipt_digest = _canonical_json_sha256(
            {
                key: value
                for key, value in receipt.items()
                if key != "receipt_digest"
            }
        )
    except (TypeError, ValueError):
        return False
    if not (
        isinstance(inputs, list)
        and inputs
        and all(_valid_identity_record(value, require_name=True) for value in inputs)
        and len({str(value["name"]) for value in inputs}) == len(inputs)
        and _valid_identity_record(target, require_name=False)
        and isinstance(target, dict)
        and isinstance(target.get("candidate_root"), str)
        and bool(target.get("candidate_root"))
        and isinstance(environment, dict)
        and all(
            isinstance(environment.get(field), str)
            and bool(environment.get(field))
            for field in (
                "python",
                "implementation",
                "platform",
                "executable",
                "dependency_files_sha256",
                "installed_packages_sha256",
                "ambient_environment_sha256",
            )
        )
        and SHA256_HEX.fullmatch(
            str(environment["dependency_files_sha256"])
        )
        and SHA256_HEX.fullmatch(
            str(environment["installed_packages_sha256"])
        )
        and isinstance(exit_state, dict)
        and set(exit_state) == {"code", "status"}
        and isinstance(exit_state.get("code"), int)
        and exit_state.get("status")
        == ("passed" if exit_state.get("code") == 0 else "failed")
    ):
        return False
    return (
        receipt.get("schema_version") == PROOF_RECEIPT_SCHEMA_VERSION
        and isinstance(receipt_id, str)
        and bool(SAFE_ID.fullmatch(receipt_id))
        and isinstance(registration_id, str)
        and bool(SAFE_ID.fullmatch(registration_id))
        and isinstance(receipt.get("proof_profile"), str)
        and isinstance(receipt.get("output_digest"), str)
        and bool(SHA256_HEX.fullmatch(str(receipt["output_digest"])))
        and isinstance(receipt.get("receipt_digest"), str)
        and receipt.get("receipt_digest")
        == computed_receipt_digest
        and _valid_timestamp(receipt.get("observed_at"))
        and (
            receipt.get("stage") is None
            or receipt.get("stage") in STAGE_PROFILES
        )
        and source in {"execution", "forced-execution", "tmp-cache"}
        and (supersedes is None or isinstance(supersedes, str))
        and (
            (
                source == "forced-execution"
                and isinstance(forced_reason, str)
                and bool(forced_reason)
            )
            or (
                source != "forced-execution"
                and forced_reason is None
            )
        )
        and (
            fresh_epoch_identity is None
            or (
                isinstance(fresh_epoch_identity, dict)
                and set(fresh_epoch_identity)
                == {
                    "composition_epoch_id",
                    "pack_contract_revision",
                    "slice_fingerprint",
                    "relationship_ids",
                    "scenario_ids",
                }
            )
        )
    )


def _valid_legacy_receipt(receipt: object) -> bool:
    if not isinstance(receipt, dict):
        return False
    legacy_fields = {
        "schema_version",
        "id",
        "registration_id",
        "stage",
        "proof_profile",
        "inputs",
        "target",
        "environment",
        "exit_state",
        "output_digest",
        "observed_at",
        "source",
        "supersedes",
        "forced_reason",
    }
    if set(receipt) != legacy_fields:
        return False
    try:
        _canonical_json_sha256(receipt)
    except (TypeError, ValueError):
        return False
    inputs = receipt.get("inputs")
    target = receipt.get("target")
    environment = receipt.get("environment")
    exit_state = receipt.get("exit_state")
    source = receipt.get("source")
    forced_reason = receipt.get("forced_reason")
    return (
        receipt.get("schema_version") == LEGACY_PROOF_RECEIPT_SCHEMA_VERSION
        and isinstance(receipt.get("id"), str)
        and bool(SAFE_ID.fullmatch(str(receipt["id"])))
        and isinstance(receipt.get("registration_id"), str)
        and bool(SAFE_ID.fullmatch(str(receipt["registration_id"])))
        and isinstance(receipt.get("proof_profile"), str)
        and isinstance(inputs, list)
        and bool(inputs)
        and all(
            _valid_legacy_identity_record(value, require_name=True)
            for value in inputs
        )
        and len({str(value["name"]) for value in inputs}) == len(inputs)
        and _valid_legacy_identity_record(target, require_name=False)
        and isinstance(target, dict)
        and isinstance(target.get("candidate_root"), str)
        and bool(target.get("candidate_root"))
        and isinstance(environment, dict)
        and set(environment)
        == {
            "python",
            "implementation",
            "platform",
            "executable",
            "dependency_files_sha256",
            "installed_packages_sha256",
        }
        and all(
            isinstance(environment.get(field), str)
            and bool(environment.get(field))
            for field in environment
        )
        and bool(
            SHA256_HEX.fullmatch(
                str(environment["dependency_files_sha256"])
            )
        )
        and bool(
            SHA256_HEX.fullmatch(
                str(environment["installed_packages_sha256"])
            )
        )
        and isinstance(exit_state, dict)
        and set(exit_state) == {"code", "status"}
        and isinstance(exit_state.get("code"), int)
        and exit_state.get("status")
        == ("passed" if exit_state.get("code") == 0 else "failed")
        and isinstance(receipt.get("output_digest"), str)
        and bool(SHA256_HEX.fullmatch(str(receipt["output_digest"])))
        and _valid_timestamp(receipt.get("observed_at"))
        and (
            receipt.get("stage") is None
            or receipt.get("stage") in STAGE_PROFILES
        )
        and source in {"execution", "forced-execution", "tmp-cache"}
        and (
            receipt.get("supersedes") is None
            or isinstance(receipt.get("supersedes"), str)
        )
        and (
            (
                source == "forced-execution"
                and isinstance(forced_reason, str)
                and bool(forced_reason)
            )
            or (source != "forced-execution" and forced_reason is None)
        )
    )


def _valid_receipt_history(receipts: list[object]) -> bool:
    seen: set[str] = set()
    for receipt in receipts:
        if not (_valid_receipt(receipt) or _valid_legacy_receipt(receipt)):
            return False
        assert isinstance(receipt, dict)
        receipt_id = str(receipt["id"])
        supersedes = receipt.get("supersedes")
        if receipt_id in seen:
            return False
        if supersedes is not None and supersedes not in seen:
            return False
        seen.add(receipt_id)
    return True


def transitively_stale_receipts(
    receipts: list[dict[str, object]],
    changed_inputs: set[str],
) -> set[str]:
    """Derive transitive staleness without deleting or rewriting receipts."""

    stale: set[str] = set()
    changed = set(changed_inputs)
    while True:
        prior = set(stale)
        for receipt in receipts:
            receipt_id = receipt.get("id")
            inputs = receipt.get("inputs")
            if not isinstance(receipt_id, str) or not isinstance(inputs, list):
                continue
            names = {
                item.get("name")
                for item in inputs
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            }
            if names.intersection(changed) or any(
                name == f"receipt:{dependency}" for dependency in stale
                for name in names
            ):
                stale.add(receipt_id)
        if stale == prior:
            return stale


def _stale_receipts_from_invalidations(
    receipts: list[dict[str, object]],
    invalidations: list[object],
) -> set[str]:
    stale = {
        str(receipt["id"])
        for receipt in receipts
        if receipt.get("schema_version") == LEGACY_PROOF_RECEIPT_SCHEMA_VERSION
        and isinstance(receipt.get("id"), str)
    }
    for event in invalidations:
        if not isinstance(event, dict):
            continue
        event_stale = {
            value
            for value in event.get("receipt_ids", [])
            if isinstance(value, str)
        }
        changed = {
            value
            for value in event.get("changed_inputs", [])
            if isinstance(value, str)
        }
        cutoff = event.get("observed_at")
        cutoff_time = _parse_timestamp(cutoff)
        if changed and cutoff_time is not None:
            for receipt in receipts:
                receipt_id = receipt.get("id")
                observed_at = receipt.get("observed_at")
                observed_time = _parse_timestamp(observed_at)
                inputs = receipt.get("inputs")
                if (
                    not isinstance(receipt_id, str)
                    or observed_time is None
                    or observed_time > cutoff_time
                    or not isinstance(inputs, list)
                ):
                    continue
                names = {
                    item.get("name")
                    for item in inputs
                    if isinstance(item, dict)
                    and isinstance(item.get("name"), str)
                }
                if names.intersection(changed):
                    event_stale.add(receipt_id)
        while True:
            prior = set(event_stale)
            for receipt in receipts:
                receipt_id = receipt.get("id")
                inputs = receipt.get("inputs")
                if not isinstance(receipt_id, str) or not isinstance(inputs, list):
                    continue
                names = {
                    item.get("name")
                    for item in inputs
                    if isinstance(item, dict)
                    and isinstance(item.get("name"), str)
                }
                if any(
                    f"receipt:{dependency}" in names
                    for dependency in event_stale
                ):
                    event_stale.add(receipt_id)
            if event_stale == prior:
                break
        stale.update(event_stale)
    while True:
        prior = set(stale)
        for receipt in receipts:
            receipt_id = receipt.get("id")
            inputs = receipt.get("inputs")
            if not isinstance(receipt_id, str) or not isinstance(inputs, list):
                continue
            names = {
                item.get("name")
                for item in inputs
                if isinstance(item, dict) and isinstance(item.get("name"), str)
            }
            if any(f"receipt:{dependency}" in names for dependency in stale):
                stale.add(receipt_id)
        if stale == prior:
            return stale


def _valid_invalidation_history(invalidations: object) -> bool:
    if not isinstance(invalidations, list):
        return False
    list_fields = {
        "receipt_ids",
        "changed_inputs",
        "changed_contract_fields",
    }
    for event in invalidations:
        if (
            not isinstance(event, dict)
            or not set(event).issubset({"observed_at", *list_fields})
            or not list_fields.intersection(event)
            or _parse_timestamp(event.get("observed_at")) is None
        ):
            return False
        for field in list_fields:
            if field not in event:
                continue
            values = event[field]
            if (
                not isinstance(values, list)
                or not all(isinstance(value, str) and value for value in values)
                or values != sorted(set(values))
            ):
                return False
    return True


def _superseded_receipts(receipts: list[dict[str, object]]) -> set[str]:
    return {
        str(receipt["supersedes"])
        for receipt in receipts
        if isinstance(receipt.get("supersedes"), str)
    }


def _identity_key(identity_tuple: dict[str, object]) -> str:
    return _canonical_json_sha256(identity_tuple)


def _full_suite_key(identity_tuple: dict[str, object]) -> str:
    key = {
        "proof_profile": identity_tuple["proof_profile"],
        "target": identity_tuple["target"],
        "environment": identity_tuple["environment"],
    }
    if "fresh_epoch_identity" in identity_tuple:
        key["fresh_epoch_identity"] = identity_tuple["fresh_epoch_identity"]
    return _canonical_json_sha256(key)


def _exact_receipt(
    receipts: list[dict[str, object]],
    registration: dict[str, object],
    identity_tuple: dict[str, object],
    stale: set[str],
) -> dict[str, object] | None:
    superseded = _superseded_receipts(receipts)
    for receipt in reversed(receipts):
        if (
            receipt.get("schema_version") == PROOF_RECEIPT_SCHEMA_VERSION
            and str(receipt.get("id")) not in stale
            and str(receipt.get("id")) not in superseded
            and receipt.get("registration_id") == registration.get("id")
            and receipt.get("stage") == registration.get("stage")
            and receipt.get("proof_profile") == identity_tuple["proof_profile"]
            and receipt.get("inputs") == identity_tuple["inputs"]
            and receipt.get("target") == identity_tuple["target"]
            and receipt.get("environment") == identity_tuple["environment"]
            and receipt.get("fresh_epoch_identity")
            == identity_tuple.get("fresh_epoch_identity")
            and isinstance(receipt.get("exit_state"), dict)
            and receipt["exit_state"].get("code") == 0
        ):
            return receipt
    return None


def _latest_matching_receipt(
    receipts: list[dict[str, object]],
    registration: dict[str, object],
    identity_tuple: dict[str, object],
) -> dict[str, object] | None:
    for receipt in reversed(receipts):
        if (
            receipt.get("registration_id") == registration.get("id")
            and receipt.get("stage") == registration.get("stage")
            and receipt.get("proof_profile") == identity_tuple["proof_profile"]
            and receipt.get("inputs") == identity_tuple["inputs"]
            and receipt.get("target") == identity_tuple["target"]
            and receipt.get("environment") == identity_tuple["environment"]
            and receipt.get("fresh_epoch_identity")
            == identity_tuple.get("fresh_epoch_identity")
        ):
            return receipt
    return None


def _cache_receipt(
    registration: dict[str, object],
    identity_tuple: dict[str, object],
    *,
    worktree: Path,
) -> dict[str, object] | None:
    value = registration.get("cache_bundle")
    if value is None:
        return None
    if not isinstance(value, str) or Path(value).is_absolute():
        raise ValueError("Proof cache bundle path is malformed")
    cache_path = (worktree / value).resolve()
    tmp_root = (worktree / ".tmp").resolve()
    if not _is_within(cache_path, tmp_root):
        raise ValueError("Proof cache bundle must stay inside .tmp")
    bundle = _read_json(cache_path)
    output_value = bundle.get("output_path") if isinstance(bundle, dict) else None
    if not isinstance(output_value, str) or Path(output_value).is_absolute():
        raise ValueError("Proof cache output path is malformed")
    output_path = (worktree / output_value).resolve()
    if not _is_within(output_path, tmp_root):
        raise ValueError("Proof cache output must stay inside .tmp")
    actual_output_digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    if (
        not isinstance(bundle, dict)
        or bundle.get("schema_version") != PROOF_CACHE_SCHEMA_VERSION
        or bundle.get("proof_profile") != identity_tuple["proof_profile"]
        or bundle.get("proof_lane") != registration.get("id")
        or bundle.get("identity_tuple") != identity_tuple
        or bundle.get("exit_state") != {"code": 0, "status": "passed"}
        or not isinstance(bundle.get("output_digest"), str)
        or bundle.get("output_digest") != actual_output_digest
        or not _valid_timestamp(bundle.get("completed_at"))
    ):
        raise ValueError("Proof cache bundle is corrupt or identity-mismatched")
    return make_receipt(
        registration,
        identity_tuple,
        exit_code=0,
        output_digest=str(bundle["output_digest"]),
        source="tmp-cache",
        observed_at=str(bundle["completed_at"]),
    )


def _run_profile(
    registration: dict[str, object],
    identity_tuple: dict[str, object],
    *,
    candidate_root: Path,
    supersedes: str | None = None,
    forced_reason: str | None = None,
) -> dict[str, object]:
    profile = PROOF_PROFILES[str(registration["profile"])]
    argv = profile["argv"]
    if (
        not isinstance(argv, tuple)
        or not argv
        or any(not isinstance(value, str) or not value for value in argv)
    ):
        raise ValueError("Allowlisted proof profile argv is invalid")
    completed = subprocess.run(
        list(argv),
        cwd=candidate_root,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    raw = completed.stdout.encode("utf-8") + completed.stderr.encode("utf-8")
    return make_receipt(
        registration,
        identity_tuple,
        exit_code=completed.returncode,
        output_digest=hashlib.sha256(raw).hexdigest(),
        source="forced-execution" if forced_reason else "execution",
        supersedes=supersedes,
        forced_reason=forced_reason,
    )


def _proof_failure(
    manifest_path: Path,
    gate: str,
    message: str,
    failures: list[dict[str, str]] | None = None,
    *,
    expensive_work_skipped: bool = True,
) -> dict[str, object]:
    result = _failure(
        "failed",
        gate,
        manifest_path,
        message,
        expensive_work_skipped=expensive_work_skipped,
    )
    if failures is not None:
        result["failures"] = failures
    return result


def _decision_pointer_resolves(
    manifest_path: Path,
    pointer: object,
) -> bool:
    if (
        not isinstance(pointer, str)
        or not pointer.startswith("decisions.md#")
    ):
        return False
    fragment = pointer.split("#", 1)[1]
    if not SAFE_ID.fullmatch(fragment):
        return False
    try:
        content = (manifest_path.parent / "decisions.md").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return False
    marker = f"<!-- campaign-decision:{fragment} -->"
    return content.count(marker) == 1


def _markdown_fragment_resolves(path: Path, fragment: str) -> bool:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    explicit = f"<!-- campaign-section:{fragment} -->"
    if content.count(explicit) == 1:
        return True
    for line in content.splitlines():
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading is None:
            continue
        normalized = re.sub(
            r"[\s-]+",
            "-",
            re.sub(r"[^\w\s-]", "", heading.group(1).lower()),
        ).strip("-")
        if normalized == fragment:
            return True
    return False


def _terminal_semantic_pointers_resolve(
    manifest_path: Path,
    semantic: dict[str, object],
    *,
    contract: dict[str, object],
    skill: str,
    worktree: Path,
) -> bool:
    pointers = semantic.get("pointers")
    if not isinstance(pointers, dict):
        return False
    try:
        research, _ = _admission_path(
            worktree,
            pointers.get("research_packet"),
            "research_packet",
        )
        synthesis, _ = _admission_path(
            worktree,
            pointers.get("skill_synthesis"),
            "skill_synthesis",
        )
        adjacency, fragment = _admission_path(
            worktree,
            pointers.get("claim_adjacency"),
            "claim_adjacency",
            fragment=True,
        )
        pack_synthesis, _ = _admission_path(
            worktree,
            pointers.get("pack_synthesis"),
            "pack_synthesis",
        )
    except ValueError:
        return False
    research_relative = research.relative_to(worktree).as_posix()
    synthesis_relative = synthesis.relative_to(worktree).as_posix()
    expected_synthesis = f"docs/synthesis/skills/{skill}.md"
    pack_contract = contract.get("pack_contract")
    return (
        _decision_pointer_resolves(
            manifest_path,
            pointers.get("decision_capsule"),
        )
        and research.is_file()
        and research_relative.startswith(
            f"docs/research/skills/{skill}/"
        )
        and synthesis.is_file()
        and synthesis_relative == expected_synthesis
        and adjacency == synthesis
        and isinstance(fragment, str)
        and _markdown_fragment_resolves(adjacency, fragment)
        and isinstance(pack_contract, dict)
        and pack_contract.get("path") == CANONICAL_PACK_CONTRACT_PATH
        and pointers.get("pack_synthesis") == pack_contract.get("path")
        and pointers.get("pack_synthesis") == CANONICAL_PACK_CONTRACT_PATH
        and pack_synthesis.is_file()
    )


def _verify_registered_proof(
    manifest_path: Path,
    manifest: dict[str, object],
    *,
    worktree: Path,
    force_proof: str | None,
    force_reason: str | None,
    no_execute: bool,
    read_only: bool = False,
) -> dict[str, object]:
    mechanical = manifest["mechanical"]
    assert isinstance(mechanical, dict)
    registrations = mechanical.get("proof_registrations", [])
    receipts = mechanical.get("receipts", [])
    invalidations = mechanical.get("invalidations", [])
    if (
        not isinstance(registrations, list)
        or not isinstance(receipts, list)
        or not isinstance(invalidations, list)
    ):
        return _proof_failure(
            manifest_path,
            "proof-schema",
            "Proof registrations, receipts, and invalidations must be lists",
        )
    if not _valid_receipt_history(receipts):
        return _proof_failure(
            manifest_path,
            "proof-receipt",
            "A durable proof receipt is corrupt or legacy",
        )
    if not _valid_invalidation_history(invalidations):
        return _proof_failure(
            manifest_path,
            "proof-schema",
            "Proof invalidation history is malformed",
        )
    typed_receipts = [receipt for receipt in receipts if isinstance(receipt, dict)]
    stale = _stale_receipts_from_invalidations(typed_receipts, invalidations)
    seen_ids: set[str] = set()
    required_ids: set[str] = set()
    planned: list[tuple[dict[str, object], Path, dict[str, object]]] = []
    not_applicable: list[str] = []
    blocked: list[str] = []
    cheap_failures: list[dict[str, str]] = []
    profile_failures: list[dict[str, str]] = []
    forbidden_profile_fields = {
        "argv",
        "command",
        "environment",
        "env",
        "network",
        "tier",
    }
    semantic = manifest.get("semantic")
    declared_stage = _semantic_stage(semantic)
    for value in registrations:
        if not isinstance(value, dict):
            cheap_failures.append(
                {"registration": "<unknown>", "message": "registration is not an object"}
            )
            continue
        registration_id = value.get("id")
        applicability = value.get("applicability")
        pointer = value.get("decision_pointer")
        if (
            not isinstance(registration_id, str)
            or not SAFE_ID.fullmatch(registration_id)
            or registration_id in seen_ids
        ):
            cheap_failures.append(
                {
                    "registration": str(registration_id),
                    "message": "registration ID is invalid or duplicated",
                }
            )
            continue
        seen_ids.add(registration_id)
        forbidden = forbidden_profile_fields.intersection(value)
        if forbidden:
            profile_failures.append(
                {
                    "registration": registration_id,
                    "message": (
                        "registration cannot override "
                        + ", ".join(sorted(forbidden))
                    ),
                }
            )
            continue
        if applicability not in {"required", "not-applicable", "blocked"}:
            cheap_failures.append(
                {
                    "registration": registration_id,
                    "message": "applicability is invalid",
                }
            )
            continue
        if not _decision_pointer_resolves(manifest_path, pointer):
            cheap_failures.append(
                {
                    "registration": registration_id,
                    "message": (
                        "applicability requires an exact decision-record pointer"
                    ),
                }
            )
            continue
        registration_stage = value.get("stage", declared_stage)
        if registration_stage not in STAGE_PROFILES:
            cheap_failures.append(
                {
                    "registration": registration_id,
                    "message": "registration stage is invalid",
                }
            )
            continue
        if registration_stage != declared_stage:
            continue
        if applicability == "not-applicable":
            not_applicable.append(registration_id)
            continue
        if applicability == "blocked":
            blocked.append(registration_id)
            continue
        required_ids.add(registration_id)
        if value.get("fresh_behavior") is True:
            return _proof_failure(
                manifest_path,
                "fresh-behavior",
                "Explicitly fresh behavioral sampling cannot use cached deterministic proof",
            )
        try:
            candidate_root = _registration_candidate_root(value, worktree)
            selected_profile = PROOF_PROFILES.get(str(value.get("profile")))
            target = value.get("target")
            if (
                isinstance(selected_profile, dict)
                and selected_profile.get("full_suite") is True
                and (
                    candidate_root != worktree
                    or not isinstance(target, dict)
                    or target.get("algorithm") != "git-object-v1"
                )
            ):
                raise ValueError(
                    "Full-suite proof requires the exact Git worktree identity"
                )
            identity_tuple = proof_identity_tuple(
                value,
                candidate_root=candidate_root,
            )
            if (
                isinstance(selected_profile, dict)
                and selected_profile.get("full_suite") is True
                and not _full_suite_worktree_matches(
                    candidate_root,
                    str(identity_tuple["target"]["digest"]),  # type: ignore[index]
                )
            ):
                raise ValueError(
                    "Full-suite target does not match the live worktree bytes"
                )
            stale_dependencies = {
                str(item["name"]).removeprefix("receipt:")
                for item in identity_tuple["inputs"]  # type: ignore[union-attr]
                if isinstance(item, dict)
                and isinstance(item.get("name"), str)
                and str(item["name"]).startswith("receipt:")
                and str(item["name"]).removeprefix("receipt:") in stale
            }
            if stale_dependencies:
                raise ValueError(
                    "Proof depends on stale receipt(s): "
                    + ", ".join(sorted(stale_dependencies))
                )
        except (OSError, json.JSONDecodeError, ValueError) as error:
            cheap_failures.append(
                {"registration": registration_id, "message": str(error)}
            )
            continue
        planned.append((value, candidate_root, identity_tuple))
    if profile_failures:
        return _proof_failure(
            manifest_path,
            "proof-profile",
            "Proof registrations cannot inject commands, environment, or network",
            profile_failures,
        )
    if cheap_failures:
        return _proof_failure(
            manifest_path,
            (
                "proof-applicability"
                if any("pointer" in failure["message"] for failure in cheap_failures)
                else "proof-identity"
            ),
            "One or more cheap proof registration checks failed",
            cheap_failures,
        )
    if force_proof is not None and force_proof not in required_ids:
        return _proof_failure(
            manifest_path,
            "force-proof",
            "Forced proof names no required registration",
        )
    if force_proof is not None and not force_reason:
        return _proof_failure(
            manifest_path,
            "force-proof",
            "Forced proof requires an owner-supplied reason",
        )
    if force_reason and force_proof is None:
        return _proof_failure(
            manifest_path,
            "force-proof",
            "Forced proof reason requires an exact registration",
        )
    if blocked:
        result = _failure(
            "stale",
            "proof-applicability",
            manifest_path,
            "Owner-declared proof remains blocked",
        )
        result["blocked"] = blocked
        result["decision_pointers"] = [
            value["decision_pointer"]
            for value in registrations
            if isinstance(value, dict) and value.get("id") in blocked
        ]
        return result
    if read_only:
        if force_proof is not None:
            return _proof_failure(
                manifest_path,
                "force-proof",
                "Frozen verification cannot execute a forced proof",
            )
        reused: list[str] = []
        missing: list[dict[str, str]] = []
        for registration, _, identity_tuple in planned:
            exact = _exact_receipt(
                typed_receipts,
                registration,
                identity_tuple,
                stale,
            )
            if exact is None:
                missing.append(
                    {
                        "registration": str(registration["id"]),
                        "message": "current durable proof receipt is missing",
                    }
                )
            else:
                reused.append(str(exact["id"]))
        if missing:
            return _proof_failure(
                manifest_path,
                "proof-receipt",
                "Frozen verification requires current durable proof receipts",
                missing,
            )
        return {
            "status": "verified",
            "proof": {
                "reused_receipts": reused,
                "reused_cache": [],
                "cache_rejections": [],
                "executed": [],
                "deduplicated": [],
                "not_applicable": not_applicable,
                "stale_receipts": sorted(stale),
            },
        }
    if no_execute:
        result = _failure(
            "stale",
            "proof-plan",
            manifest_path,
            "Proof plan requires execution",
        )
        result["plan"] = [
            {
                "registration": value["id"],
                "profile": value["profile"],
                "tier": PROOF_PROFILES[str(value["profile"])]["tier"],
            }
            for value, _, _ in planned
        ]
        return result

    proof_result: dict[str, object] = {
        "reused_receipts": [],
        "reused_cache": [],
        "cache_rejections": [],
        "executed": [],
        "deduplicated": [],
        "not_applicable": not_applicable,
        "stale_receipts": sorted(stale),
    }
    appended: list[dict[str, object]] = []
    completed_keys: set[str] = set()
    superseded_receipts = _superseded_receipts(typed_receipts)
    completed_full_suites = {
        _full_suite_key(
            {
                "proof_profile": receipt["proof_profile"],
                "target": receipt["target"],
                "environment": receipt["environment"],
                **(
                    {
                        "fresh_epoch_identity": receipt[
                            "fresh_epoch_identity"
                        ]
                    }
                    if "fresh_epoch_identity" in receipt
                    else {}
                ),
            }
        )
        for receipt in typed_receipts
        if receipt.get("schema_version") == PROOF_RECEIPT_SCHEMA_VERSION
        and receipt.get("proof_profile") == "full-suite-v1"
        and receipt.get("id") not in stale
        and receipt.get("id") not in superseded_receipts
        and isinstance(receipt.get("exit_state"), dict)
        and receipt["exit_state"].get("code") == 0
    }
    for tier in PROOF_TIERS:
        tier_failures: list[dict[str, str]] = []
        for registration, candidate_root, identity_tuple in planned:
            profile = PROOF_PROFILES[str(registration["profile"])]
            if profile["tier"] != tier:
                continue
            registration_id = str(registration["id"])
            key = _identity_key(identity_tuple)
            full_suite_key = (
                _full_suite_key(identity_tuple)
                if profile.get("full_suite") is True
                else None
            )
            exact = _exact_receipt(
                typed_receipts + appended,
                registration,
                identity_tuple,
                stale,
            )
            latest = _latest_matching_receipt(
                typed_receipts + appended,
                registration,
                identity_tuple,
            )
            forced = force_proof == registration_id
            if exact is not None and not forced:
                collection = (
                    "deduplicated" if key in completed_keys else "reused_receipts"
                )
                proof_result[collection].append(str(exact["id"]))  # type: ignore[union-attr]
                if collection == "deduplicated":
                    proof_result[collection][-1] = registration_id  # type: ignore[index]
                completed_keys.add(key)
                continue
            if (
                full_suite_key is not None
                and full_suite_key in completed_full_suites
                and not forced
            ):
                proof_result["deduplicated"].append(registration_id)  # type: ignore[union-attr]
                continue
            if not forced:
                try:
                    cached = _cache_receipt(
                        registration,
                        identity_tuple,
                        worktree=worktree,
                    )
                except (
                    FileNotFoundError,
                    OSError,
                    json.JSONDecodeError,
                    ValueError,
                ):
                    proof_result["cache_rejections"].append(registration_id)  # type: ignore[union-attr]
                    cached = None
                if (
                    cached is not None
                    and _stale_receipts_from_invalidations(
                        typed_receipts + appended + [cached],
                        invalidations,
                    )
                    .intersection({str(cached["id"])})
                ):
                    proof_result["cache_rejections"].append(registration_id)  # type: ignore[union-attr]
                    cached = None
                if cached is not None:
                    if latest is not None:
                        cached["supersedes"] = str(latest["id"])
                        _seal_receipt(cached)
                    appended.append(cached)
                    proof_result["reused_cache"].append(registration_id)  # type: ignore[union-attr]
                    completed_keys.add(key)
                    if full_suite_key is not None:
                        completed_full_suites.add(full_suite_key)
                    continue
            supersedes = str(latest["id"]) if latest is not None else None
            try:
                receipt = _run_profile(
                    registration,
                    identity_tuple,
                    candidate_root=candidate_root,
                    supersedes=supersedes,
                    forced_reason=force_reason if forced else None,
                )
            except OSError as error:
                result = _failure(
                    "execution-error",
                    "proof-execution",
                    manifest_path,
                    f"Allowlisted proof profile could not start: {error}",
                    expensive_work_skipped=tier != "expensive",
                )
                result["proof"] = proof_result
                return result
            appended.append(receipt)
            if receipt["exit_state"]["code"] != 0:  # type: ignore[index]
                tier_failures.append(
                    {
                        "registration": registration_id,
                        "message": "allowlisted proof profile failed",
                    }
                )
            else:
                proof_result["executed"].append(registration_id)  # type: ignore[union-attr]
                completed_keys.add(key)
                if full_suite_key is not None:
                    completed_full_suites.add(full_suite_key)
        if tier_failures:
            update_mechanical_state(
                manifest_path,
                {"receipts": typed_receipts + appended},
            )
            return _proof_failure(
                manifest_path,
                "proof-execution",
                f"{tier} proof tier failed; later tiers were skipped",
                tier_failures,
                expensive_work_skipped=tier != "expensive",
            )

    if appended or mechanical.get("evidence_state") == "stale":
        update_mechanical_state(
            manifest_path,
            {
                "receipts": typed_receipts + appended,
                "evidence_state": "current",
            },
        )
    return {"status": "verified", "proof": proof_result}


def _verify_preflight_registrations(
    manifest_path: Path,
    manifest: dict[str, object],
    *,
    worktree: Path,
) -> dict[str, object]:
    mechanical = manifest["mechanical"]
    semantic = manifest["semantic"]
    assert isinstance(mechanical, dict)
    assert isinstance(semantic, dict)
    declared_stage = str(_semantic_stage(semantic))
    registrations = mechanical.get("preflight_registrations", [])
    if not isinstance(registrations, list):
        return _proof_failure(
            manifest_path,
            "preflight-registration",
            "Preflight registrations must be a list",
        )
    if any(not isinstance(value, dict) for value in registrations):
        return _proof_failure(
            manifest_path,
            "preflight-registration",
            "Every preflight registration must be an object",
        )
    invalid_stages = [
        str(value.get("stage"))
        for value in registrations
        if isinstance(value, dict)
        and value.get("stage", declared_stage) not in STAGE_PROFILES
    ]
    if invalid_stages:
        return _proof_failure(
            manifest_path,
            "preflight-registration",
            "Preflight registration stage is invalid",
        )
    required_kinds = REQUIRED_PREFLIGHT_KINDS.get(declared_stage, frozenset())
    stage_registrations = [
        value
        for value in registrations
        if isinstance(value, dict)
        and value.get("stage", declared_stage) == declared_stage
    ]
    if declared_stage == "prompt-6":
        delivery_registrations = [
            value
            for value in stage_registrations
            if value.get("kind") == "git-delivery"
        ]
        if (
            len(delivery_registrations) != 1
            or delivery_registrations[0].get("applicability") != "required"
        ):
            return _proof_failure(
                manifest_path,
                "preflight-registration",
                "Prompt 6 requires exactly one applicable Git delivery registration",
            )
    present_kinds = {
        str(value.get("kind"))
        for value in stage_registrations
        if value.get("kind") in PREFLIGHT_KINDS
    }
    if not required_kinds.issubset(present_kinds):
        return _proof_failure(
            manifest_path,
            "preflight-registration",
            "Owner-declared stage is missing its required preflight registration",
        )

    seen: set[str] = set()
    completed: list[str] = []
    skipped: list[str] = []
    blocked: list[str] = []
    failures: list[dict[str, str]] = []
    git_delivery: dict[str, object] | None = None
    installations: list[dict[str, object]] = []
    for registration in stage_registrations:
        registration_id = registration.get("id")
        kind = registration.get("kind")
        applicability = registration.get("applicability")
        pointer = registration.get("decision_pointer")
        if (
            not isinstance(registration_id, str)
            or not SAFE_ID.fullmatch(registration_id)
            or registration_id in seen
        ):
            failures.append(
                {
                    "registration": str(registration_id),
                    "message": "registration ID is invalid or duplicated",
                }
            )
            continue
        seen.add(registration_id)
        if kind not in PREFLIGHT_KINDS:
            failures.append(
                {
                    "registration": registration_id,
                    "message": "preflight kind is invalid",
                }
            )
            continue
        if applicability not in {"required", "not-applicable", "blocked"}:
            failures.append(
                {
                    "registration": registration_id,
                    "message": "applicability is invalid",
                }
            )
            continue
        if not _decision_pointer_resolves(manifest_path, pointer):
            failures.append(
                {
                    "registration": registration_id,
                    "message": "applicability requires an exact decision-record pointer",
                }
            )
            continue
        if kind == "installation" and applicability == "not-applicable":
            failures.append(
                {
                    "registration": registration_id,
                    "message": "Prompt 5 installation verification is always required",
                }
            )
            continue
        if applicability == "not-applicable":
            skipped.append(registration_id)
            continue
        if applicability == "blocked":
            blocked.append(registration_id)
            continue
        try:
            candidate_root = _registration_candidate_root(registration, worktree)
            if kind == "git-delivery":
                git_delivery = _verify_git_delivery_preflight(
                    manifest_path,
                    manifest,
                    registration,
                    candidate_root=candidate_root,
                )
            elif kind == "behavioral-comparison":
                output_root = (
                    worktree
                    / ".tmp"
                    / "campaign-payloads"
                    / str(manifest["campaign"]["id"])  # type: ignore[index]
                    / registration_id
                )
                generated = build_behavioral_payloads(
                    registration,
                    candidate_root=candidate_root,
                    output_root=output_root,
                )
                results = registration.get("results")
                if results is not None:
                    if not isinstance(results, dict) or set(results) != {"m0", "h1"}:
                        raise ValueError(
                            "Behavioral comparison results must name exact m0 and h1 envelopes"
                        )
                    for arm in ("m0", "h1"):
                        result_spec = results[arm]
                        result_identity = _verified_identity(
                            result_spec,
                            candidate_root=candidate_root,
                            label=f"{arm} result envelope",
                        )
                        del result_identity
                        assert isinstance(result_spec, dict)
                        result_path = _contained_artifact_path(
                            candidate_root,
                            result_spec.get("path"),
                        )
                        payload = generated["payloads"][arm]  # type: ignore[index]
                        assert isinstance(payload, dict)
                        runtimes = registration["runtimes"]
                        assert isinstance(runtimes, dict)
                        runtime = runtimes[arm]
                        assert isinstance(runtime, dict)
                        lint_result_envelope(
                            _read_json(result_path),
                            case_id=str(generated["case_id"]),
                            arm=arm,
                            candidate_root=candidate_root,
                            candidate_identity=str(runtime["digest"]),
                            fixture_identity=str(generated["fixture_identity"]),
                            dispatch_payload_sha256=str(
                                payload["dispatch_payload_sha256"]
                            ),
                            require_fresh=registration.get("require_fresh") is True,
                        )
            elif kind == "markdown":
                _verified_identity(
                    registration.get("target"),
                    candidate_root=candidate_root,
                    label="Markdown target",
                )
                paths = registration.get("paths")
                if (
                    not isinstance(paths, list)
                    or not paths
                    or any(not isinstance(path, str) for path in paths)
                ):
                    raise ValueError("Markdown preflight requires nonempty paths")
                policy = registration.get("hard_break_policy")
                for path in paths:
                    lint_markdown(
                        _contained_artifact_path(candidate_root, path),
                        candidate_root=candidate_root,
                        hard_break_policy=str(policy),
                    )
            elif kind == "research":
                registry_spec = registration.get("registry")
                _verified_identity(
                    registry_spec,
                    candidate_root=candidate_root,
                    label="Research registry",
                )
                assert isinstance(registry_spec, dict)
                lint_research_registry(
                    _contained_artifact_path(
                        candidate_root,
                        registry_spec.get("path"),
                    ),
                    candidate_root=candidate_root,
                )
            else:
                installations.append(
                    _verify_installation_preflight(
                        registration,
                        candidate_root=candidate_root,
                    )
                )
        except (
            OSError,
            RuntimeError,
            UnicodeError,
            json.JSONDecodeError,
            ValueError,
        ) as error:
            failures.append(
                {"registration": registration_id, "message": str(error)}
            )
            continue
        completed.append(registration_id)
    if failures:
        return _proof_failure(
            manifest_path,
            "preflight-validation",
            "One or more deterministic preflight checks failed",
            failures,
        )
    if blocked:
        result = _failure(
            "stale",
            "preflight-applicability",
            manifest_path,
            "Owner-declared preflight remains blocked",
        )
        result["blocked"] = blocked
        return result
    result: dict[str, object] = {
        "status": "verified",
        "preflight": {
            "completed": completed,
            "not_applicable": skipped,
        },
    }
    if git_delivery is not None:
        result["preflight"]["git_delivery"] = git_delivery  # type: ignore[index]
    if installations:
        result["preflight"]["installations"] = installations  # type: ignore[index]
    return result


def _git_read(
    candidate_root: Path,
    argv: list[str],
    *,
    label: str,
    allowed_codes: frozenset[int] = frozenset({0}),
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *argv],
        cwd=candidate_root,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    if completed.returncode not in allowed_codes:
        raise ValueError(f"{label} failed")
    return completed


def _delivery_path(value: object, candidate_root: Path) -> str:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("Git delivery paths must be nonempty and relative")
    path = Path(value)
    if value != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("Git delivery paths must be normalized POSIX paths")
    resolved = (candidate_root / path).resolve()
    if not _is_within(resolved, candidate_root):
        raise ValueError("Git delivery path escapes the candidate root")
    if ".tmp" in path.parts:
        raise ValueError("Git delivery cannot depend on a .tmp path")
    return value


def _git_object_at_path(
    candidate_root: Path,
    path: str,
    *,
    state: str,
) -> str:
    revision = f":{path}" if state == "staged" else f"HEAD:{path}"
    completed = _git_read(
        candidate_root,
        ["rev-parse", "--verify", revision],
        label=f"Required {state} Git object for {path}",
    )
    digest = completed.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", digest):
        raise ValueError(f"Required {state} Git object for {path} is invalid")
    return digest


def _verify_git_delivery_preflight(
    manifest_path: Path,
    manifest: dict[str, object],
    registration: dict[str, object],
    *,
    candidate_root: Path,
) -> dict[str, object]:
    campaign = manifest["campaign"]
    assert isinstance(campaign, dict)
    if candidate_root != Path(str(campaign["worktree"])).resolve():
        raise ValueError("Git delivery candidate root must be the worktree root")
    mode = registration.get("delivery_mode")
    if mode not in {"commit", "push"} or mode != campaign.get("delivery_mode"):
        raise ValueError("Git delivery mode must exactly match commit or push authority")

    allowlist_value = registration.get("allowlist")
    required_value = registration.get("required_paths")
    if (
        not isinstance(allowlist_value, list)
        or not allowlist_value
        or not isinstance(required_value, list)
        or not required_value
    ):
        raise ValueError("Git delivery requires an exact nonempty allowlist")
    allowlist = [_delivery_path(value, candidate_root) for value in allowlist_value]
    if allowlist != sorted(set(allowlist)):
        raise ValueError("Git delivery allowlist must be sorted and unique")

    required: dict[str, str] = {}
    for entry in required_value:
        if not isinstance(entry, dict) or set(entry) != {"path", "state"}:
            raise ValueError("Required Git delivery paths must declare path and state")
        path = _delivery_path(entry.get("path"), candidate_root)
        state = entry.get("state")
        if state not in {"staged", "committed", "deleted"} or path in required:
            raise ValueError("Required Git delivery path state is invalid or duplicated")
        required[path] = str(state)
    if set(required) != set(allowlist):
        raise ValueError("Required Git delivery paths must exactly match the allowlist")

    manifest_relative = manifest_path.resolve().relative_to(candidate_root).as_posix()
    if (
        registration.get("prompt5_manifest") != manifest_relative
        or manifest_relative not in required
    ):
        raise ValueError("Frozen Prompt 5 manifest must be an exact required path")
    for path, state in required.items():
        if state != "deleted" and not (candidate_root / path).is_file():
            raise ValueError(f"Required Git delivery path is missing: {path}")

    promoted_p1 = registration.get("promoted_p1")
    if (
        not isinstance(promoted_p1, dict)
        or promoted_p1.get("algorithm") != "campaign-tree-v1"
    ):
        raise ValueError("Git delivery requires the promoted P1 identity")
    p1_path = _delivery_path(promoted_p1.get("path"), candidate_root)
    p1_root = _contained_artifact_path(candidate_root, p1_path)
    p1_files = {
        (Path(p1_path) / relative).as_posix()
        for relative, (kind, _) in tree_entries(p1_root).items()
        if kind == "file"
    }
    omitted_p1 = sorted(
        path
        for path in p1_files
        if path not in required or required[path] == "deleted"
    )
    if omitted_p1:
        raise ValueError(
            "Promoted P1 files are omitted from the delivery allowlist: "
            + ", ".join(omitted_p1)
        )
    ignored = _git_read(
        candidate_root,
        ["check-ignore", "--no-index", "--", p1_path],
        label=f"Ignore check for promoted P1 {p1_path}",
        allowed_codes=frozenset({0, 1}),
    )
    if ignored.returncode == 0:
        raise ValueError("Promoted P1 identity depends on an ignored path")
    for dependency in sorted(p1_files):
        ignored_dependency = _git_read(
            candidate_root,
            ["check-ignore", "--no-index", "--", dependency],
            label=f"Ignore check for promoted P1 dependency {dependency}",
            allowed_codes=frozenset({0, 1}),
        )
        if ignored_dependency.returncode == 0:
            raise ValueError("Promoted P1 identity depends on an ignored path")
    _verified_identity(
        promoted_p1,
        candidate_root=candidate_root,
        label="Promoted P1",
    )

    staged_result = _git_read(
        candidate_root,
        ["diff", "--cached", "--name-only", "-z", "--diff-filter=ACDMRTUXB"],
        label="Staged scope read",
    )
    staged = {line for line in staged_result.stdout.split("\0") if line}
    unauthorized = sorted(staged.difference(allowlist))
    if unauthorized:
        raise ValueError(
            "Unauthorized staged paths are outside the delivery allowlist: "
            + ", ".join(unauthorized)
        )

    campaign_directory = manifest_path.parent.relative_to(candidate_root).as_posix()
    tracked_campaign = _git_read(
        candidate_root,
        ["ls-files", "-z", "--", campaign_directory],
        label="Tracked campaign artifact read",
    )
    allowed_campaign_paths = {
        f"{campaign_directory}/{name}"
        for name in ("decisions.md", "manifest.json", "results.json")
    }
    raw_campaign_paths = sorted(
        path
        for path in tracked_campaign.stdout.split("\0")
        if path and path not in allowed_campaign_paths
    )
    if raw_campaign_paths:
        raise ValueError(
            "Completed campaign contains a tracked raw campaign artifact: "
            + ", ".join(raw_campaign_paths)
        )

    for path, state in required.items():
        artifact = candidate_root / path
        if state == "deleted":
            if path not in staged or artifact.exists():
                raise ValueError(
                    f"Required Git delivery path is not deleted: {path}"
                )
            index_entry = _git_read(
                candidate_root,
                ["--literal-pathspecs", "ls-files", "--error-unmatch", "--", path],
                label=f"Deleted path index check for {path}",
                allowed_codes=frozenset({0, 1}),
            )
            if index_entry.returncode == 0:
                raise ValueError(
                    f"Deleted Git delivery path index still contains: {path}"
                )
            _git_object_at_path(
                candidate_root,
                path,
                state=state,
            )
            continue
        assert artifact.is_file()
        ignored = _git_read(
            candidate_root,
            ["check-ignore", "--no-index", "--", path],
            label=f"Ignore check for {path}",
            allowed_codes=frozenset({0, 1}),
        )
        if ignored.returncode == 0:
            raise ValueError(f"Git delivery cannot depend on ignored path: {path}")
        if (state == "staged") != (path in staged):
            raise ValueError(f"Required Git delivery path is not {state}: {path}")
        expected = _git_object_at_path(
            candidate_root,
            path,
            state=state,
        )
        actual = _git_read(
            candidate_root,
            ["hash-object", f"--path={path}", "--", path],
            label=f"Worktree Git object for {path}",
        ).stdout.strip()
        if actual != expected:
            raise ValueError(
                f"Required Git delivery path identity does not match {state}: {path}"
            )

    _git_read(
        candidate_root,
        ["diff", "--check"],
        label="Worktree diff check",
    )
    _git_read(
        candidate_root,
        ["diff", "--cached", "--check"],
        label="Staged diff check",
    )
    return {
        "delivery_mode": mode,
        "diff_checks": {"staged": "passed", "worktree": "passed"},
    }


def _verify_installation_preflight(
    registration: dict[str, object],
    *,
    candidate_root: Path,
) -> dict[str, object]:
    cohort = registration.get("cohort")
    if (
        not isinstance(cohort, list)
        or not cohort
        or any(
            not isinstance(name, str) or not SAFE_ID.fullmatch(name)
            for name in cohort
        )
        or len(set(cohort)) != len(cohort)
        or cohort != sorted(cohort)
    ):
        raise ValueError(
            "Installation cohort must be a nonempty sorted list of unique skill names"
        )
    state = registration.get("state")
    if state not in {"plan", "post-install"}:
        raise ValueError("Installation state must be plan or post-install")
    installed_value = registration.get("installed_root")
    if not isinstance(installed_value, str) or not installed_value:
        raise ValueError("Installation preflight requires an exact installed root")
    installed_root = Path(installed_value).expanduser()
    if not installed_root.is_absolute():
        raise ValueError("Installation installed root must be absolute")

    evidence = install_skills.install(
        candidate_root,
        installed_root,
        None,
        dry_run=True,
    )
    if (
        evidence.get("schema_version")
        != install_skills.INSTALL_EVIDENCE_SCHEMA_VERSION
        or evidence.get("dry_run") is not True
        or evidence.get("identity_algorithm")
        != install_skills.SKILL_IDENTITY_ALGORITHM
    ):
        raise ValueError("Installer evidence schema is incompatible")
    cohort_fields: dict[str, list[str]] = {}
    for field in ("new", "updated", "unchanged", "retired"):
        values = evidence.get(field)
        if (
            not isinstance(values, list)
            or any(
                not isinstance(name, str) or not SAFE_ID.fullmatch(name)
                for name in values
            )
            or values != sorted(set(values))
        ):
            raise ValueError(f"Installer {field} evidence is malformed")
        cohort_fields[field] = values
    retired = cohort_fields["retired"]
    if retired:
        raise ValueError(
            "Installer dry-run found unexpected retirement drift: "
            + ", ".join(str(name) for name in retired)
        )
    changed = sorted(
        [
            *cohort_fields["new"],
            *cohort_fields["updated"],
        ]
    )
    if state == "plan":
        if changed != cohort:
            raise ValueError(
                "Installer dry-run cohort differs from the owner-declared cohort: "
                f"expected {cohort}, actual {changed}"
            )
        return {"state": "plan", "cohort": cohort}

    if changed:
        raise ValueError(
            "Post-install dry-run is not unchanged for the declared cohort: "
            + ", ".join(changed)
        )
    planned = evidence.get("planned_identities")
    resulting = evidence.get("resulting_identities")
    if not isinstance(planned, dict) or not isinstance(resulting, dict):
        raise ValueError("Installer identity evidence is malformed")
    mismatches = [
        name
        for name in cohort
        if not isinstance(planned.get(name), str)
        or planned.get(name) != resulting.get(name)
    ]
    if mismatches:
        raise ValueError(
            "Canonical and installed identities differ for declared cohort: "
            + ", ".join(mismatches)
        )
    return {
        "state": "post-install",
        "cohort": cohort,
        "identities": {name: planned[name] for name in cohort},
    }


def _verify_fresh_campaign(
    manifest_path: Path,
    manifest: dict[str, object],
    *,
    worktree: Path,
    stage_override: str | None,
    force_proof: str | None,
    force_reason: str | None,
    no_execute: bool,
) -> dict[str, object]:
    try:
        read_campaign_manifest(manifest_path)
        campaign_id, controlled = _control_identity(manifest_path, worktree)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return _failure("failed", "manifest-schema", manifest_path, str(error))
    campaign = controlled["campaign"]
    semantic = controlled["semantic"]
    mechanical = controlled["mechanical"]
    assert isinstance(campaign, dict)
    assert isinstance(semantic, dict)
    assert isinstance(mechanical, dict)
    stage = _semantic_stage(semantic)
    if stage_override is not None and stage_override != stage:
        return _failure(
            "failed",
            "semantic-stage",
            manifest_path,
            "Advanced stage override does not match the owner-written stage token",
        )
    pointers = semantic.get("pointers")
    assert isinstance(pointers, dict)
    decision_pointer = pointers.get("decision_capsule")
    decision_record = str(decision_pointer).split("#", 1)[0]
    decision_path = manifest_path.parent / decision_record
    if (
        not isinstance(decision_pointer, str)
        or Path(decision_record).is_absolute()
        or not _is_within(decision_path, manifest_path.parent)
        or decision_path.resolve()
        != (manifest_path.parent / "decisions.md").resolve()
        or not decision_path.is_file()
    ):
        return _failure(
            "failed",
            "manifest-path",
            manifest_path,
            "Decision capsule pointer escapes or names a foreign artifact",
        )
    lease_path = worktree / LEASE_PATH
    try:
        lease = _read_json(lease_path)
    except (OSError, json.JSONDecodeError):
        return _failure(
            "failed",
            "lease",
            manifest_path,
            "Campaign lease is absent or unreadable",
        )
    if (
        not isinstance(lease, dict)
        or lease.get("worktree") != str(worktree)
        or lease.get("campaign_id") != campaign_id
        or not _valid_owner_token(lease.get("owner_token"))
    ):
        return _failure(
            "lease-conflict",
            "lease",
            manifest_path,
            "A different campaign owns the worktree lease",
        )
    try:
        _validate_v2_campaign_identity(
            controlled,
            worktree=worktree,
            manifest_path=manifest_path,
            lease=lease,
        )
    except ValueError as error:
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            str(error),
        )
    contract = controlled.get("contract")
    assert isinstance(contract, dict)
    if mechanical.get("contract_digest") != _canonical_json_sha256(contract):
        receipts = mechanical.get("receipts")
        invalidations = mechanical.get("invalidations")
        if not isinstance(receipts, list) or not isinstance(invalidations, list):
            return _failure(
                "failed",
                "manifest-schema",
                manifest_path,
                "Fresh campaign receipt or invalidation state is malformed",
            )
        stale_ids = sorted(
            str(receipt["id"])
            for receipt in receipts
            if (
                isinstance(receipt, dict)
                and isinstance(receipt.get("id"), str)
                and isinstance(receipt.get("fresh_epoch_identity"), dict)
            )
        )
        invalidations.append(
            {
                "changed_contract_fields": ["contract.digest"],
                "receipt_ids": stale_ids,
                "observed_at": _now(),
            }
        )
        update_mechanical_state(
            manifest_path,
            {
                "evidence_state": "stale",
                "invalidations": invalidations,
            },
        )
        result = _failure(
            "stale",
            "contract-drift",
            manifest_path,
            "Immutable Fresh campaign contract changed after admission",
        )
        result.update(
            {
                "changed_contract_fields": ["contract.digest"],
                "stale_receipts": stale_ids,
                "owner_action_required": ["resume", "repair", "restart"],
            }
        )
        return result
    observed_contract = _observed_fresh_contract(
        contract,
        worktree=worktree,
    )
    drift = check_fresh_contract(manifest_path, observed_contract)
    if drift["status"] != "verified":
        return drift
    terminal_token = semantic.get("terminal_token")
    if terminal_token is not None and stage != "prompt-5":
        return _failure(
            "failed",
            "semantic-terminal",
            manifest_path,
            "Only Prompt 5 may write a terminal campaign token",
        )
    if stage == "prompt-5" and terminal_token is not None:
        lifecycle = semantic.get("lifecycle")
        if (
            terminal_token != "campaign-complete"
            or not isinstance(lifecycle, dict)
            or lifecycle != FRESH_TERMINAL_LIFECYCLE
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal state requires the exact completed lifecycle",
            )
        if not _terminal_semantic_pointers_resolve(
            manifest_path,
            semantic,
            contract=contract,
            skill=str(campaign["skill"]),
            worktree=worktree,
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal semantic pointers must resolve exactly",
            )
        preflight_registrations = mechanical.get("preflight_registrations")
        if not isinstance(preflight_registrations, list) or not any(
            isinstance(registration, dict)
            and registration.get("kind") == "installation"
            and registration.get("stage", stage) == "prompt-5"
            and registration.get("state") == "post-install"
            for registration in preflight_registrations
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal state requires post-install verification",
            )
        proof_registrations = mechanical.get("proof_registrations")
        if not isinstance(proof_registrations, list) or not proof_registrations:
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal state requires registered proof and receipts",
            )
    pack_contract = contract.get("pack_contract")
    slice_contract = contract.get("slice")
    assert isinstance(pack_contract, dict)
    assert isinstance(slice_contract, dict)
    expected_proof_base = {
        "composition_epoch_id": campaign["composition_epoch_id"],
        "pack_contract_revision": pack_contract["revision"],
        "slice_fingerprint": slice_contract["fingerprint"],
    }
    registrations = mechanical.get("proof_registrations")
    if not isinstance(registrations, list):
        return _failure(
            "failed",
            "manifest-schema",
            manifest_path,
            "Fresh campaign proof registrations must be a list",
        )
    invalid_registration = False
    for registration in registrations:
        identity = (
            registration.get("fresh_epoch_identity")
            if isinstance(registration, dict)
            else None
        )
        if not isinstance(identity, dict) or any(
            identity.get(field) != value
            for field, value in expected_proof_base.items()
        ):
            invalid_registration = True
            break
        for identity_field, contract_field in (
            ("relationship_ids", "selected_relationship_ids"),
            ("scenario_ids", "selected_scenario_ids"),
        ):
            values = identity.get(identity_field)
            selected = contract[contract_field]
            if (
                not isinstance(values, list)
                or values != sorted(set(values))
                or not set(values).issubset(selected)
            ):
                invalid_registration = True
                break
        if invalid_registration:
            break
    if invalid_registration:
        return _failure(
            "stale",
            "proof-identity",
            manifest_path,
            "Fresh proof registration omits or drifts from the exact epoch tuple",
        )
    if terminal_token is not None:
        current_required = [
            registration
            for registration in registrations
            if (
                isinstance(registration, dict)
                and registration.get("applicability") == "required"
                and registration.get("stage") == stage
            )
        ]
        if not current_required:
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal state requires current required proof",
            )
        covered_relationships: set[str] = set()
        covered_scenarios: set[str] = set()
        for registration in current_required:
            identity = registration.get("fresh_epoch_identity")
            assert isinstance(identity, dict)
            covered_relationships.update(identity["relationship_ids"])
            covered_scenarios.update(identity["scenario_ids"])
        if (
            covered_relationships
            != set(contract["selected_relationship_ids"])
            or covered_scenarios != set(contract["selected_scenario_ids"])
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal proof lacks exact relationship and scenario coverage",
            )
    preflight = _verify_preflight_registrations(
        manifest_path,
        controlled,
        worktree=worktree,
    )
    if preflight["status"] != "verified":
        return preflight
    if terminal_token is not None:
        preflight_result = preflight.get("preflight")
        installations = (
            preflight_result.get("installations")
            if isinstance(preflight_result, dict)
            else None
        )
        skill = campaign["skill"]
        if (
            not isinstance(installations, list)
            or len(installations) != 1
            or installations[0].get("state") != "post-install"
            or installations[0].get("cohort") != [skill]
            or not isinstance(installations[0].get("identities"), dict)
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal installation is not bound to this skill",
            )
        installed_identities = installations[0]["identities"]
        assert isinstance(installed_identities, dict)
        installer_digest = installed_identities.get(str(skill))
        installer_fingerprint = (
            f"sha256-v1:{installer_digest}"
            if isinstance(installer_digest, str)
            else None
        )
        artifact_identities = mechanical.get("artifact_identities")
        identities = {
            str(identity.get("name")): identity.get("fingerprint")
            for identity in (
                artifact_identities if isinstance(artifact_identities, list) else []
            )
            if isinstance(identity, dict)
        }
        if (
            identities.get("canonical-p1") != installer_fingerprint
            or identities.get("installed-p1") != installer_fingerprint
            or mechanical.get("parity")
            != {
                "canonical_installed": "match",
                "relationship_ids": contract["selected_relationship_ids"],
            }
        ):
            return _failure(
                "stale",
                "semantic-terminal",
                manifest_path,
                "Prompt 5 terminal identities do not match installer evidence",
            )
    proof: dict[str, object] | None = None
    if mechanical.get("proof_registrations"):
        proof = _verify_registered_proof(
            manifest_path,
            controlled,
            worktree=worktree,
            force_proof=force_proof,
            force_reason=force_reason,
            no_execute=no_execute,
            read_only=terminal_token is not None,
        )
        if proof["status"] != "verified":
            return proof
        controlled = _read_json(manifest_path)
        mechanical = controlled["mechanical"]
        assert isinstance(mechanical, dict)
    if mechanical.get("evidence_state") == "stale":
        return _failure(
            "stale",
            "mechanical-evidence",
            manifest_path,
            "Contract drift invalidated mechanical evidence for this epoch",
        )
    semantic_before = copy.deepcopy(semantic)
    observed_at = _now()
    update_mechanical_state(manifest_path, {"verified_at": observed_at})
    lease["observed_at"] = observed_at
    _replace_json_file(lease_path, lease)
    if _read_json(manifest_path).get("semantic") != semantic_before:
        return _failure(
            "execution-error",
            "semantic-ownership",
            manifest_path,
            "Verification altered owner-written semantic state",
        )
    result: dict[str, object] = {
        "status": "verified",
        "campaign_id": campaign_id,
        "stage": stage,
        "manifest": str(manifest_path),
        "terminal": semantic.get("terminal_token"),
    }
    if proof is not None:
        result["proof"] = proof["proof"]
    return result


def verify_campaign(
    manifest_path: Path,
    *,
    worktree: Path | None = None,
    stage_override: str | None = None,
    force_proof: str | None = None,
    force_reason: str | None = None,
    no_execute: bool = False,
) -> dict[str, object]:
    """Verify one supplied campaign manifest without selecting or advancing it."""

    resolved_worktree = (worktree or Path.cwd()).resolve()
    supplied_manifest = manifest_path.resolve()
    campaign_root = (resolved_worktree / CAMPAIGN_ROOT).resolve()
    fresh_campaign_root = (resolved_worktree / FRESH_CAMPAIGN_ROOT).resolve()
    if not (
        _is_within(supplied_manifest, campaign_root)
        or _is_within(supplied_manifest, fresh_campaign_root)
    ):
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
    if manifest.get("schema_version") == FRESH_CAMPAIGN_SCHEMA_VERSION:
        return _verify_fresh_campaign(
            supplied_manifest,
            manifest,
            worktree=resolved_worktree,
            stage_override=stage_override,
            force_proof=force_proof,
            force_reason=force_reason,
            no_execute=no_execute,
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
    preflight_verification = _verify_preflight_registrations(
        supplied_manifest,
        manifest,
        worktree=resolved_worktree,
    )
    if preflight_verification["status"] != "verified":
        return preflight_verification
    proof_verification: dict[str, object] | None = None
    if mechanical.get("proof_registrations"):
        proof_verification = _verify_registered_proof(
            supplied_manifest,
            manifest,
            worktree=resolved_worktree,
            force_proof=force_proof,
            force_reason=force_reason,
            no_execute=no_execute,
            read_only=declared_stage == "prompt-6",
        )
        if proof_verification["status"] != "verified":
            return proof_verification
        manifest = _read_json(supplied_manifest)
        mechanical = manifest["mechanical"]
        assert isinstance(mechanical, dict)
    if mechanical.get("evidence_state") == "stale":
        return _failure(
            "stale",
            "mechanical-evidence",
            manifest_path,
            "Repair invalidated mechanical evidence for this epoch",
        )

    semantic_before = copy.deepcopy(semantic)
    observed_at = _now()
    if declared_stage != "prompt-6":
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
    result = {
        "status": "verified",
        "campaign_id": campaign_id,
        "stage": declared_stage,
        "manifest": str(supplied_manifest),
    }
    if proof_verification is not None:
        result["proof"] = proof_verification["proof"]
    if preflight_verification["preflight"]["completed"] or preflight_verification[
        "preflight"
    ]["not_applicable"]:
        result["preflight"] = preflight_verification["preflight"]
    return result


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
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _campaign_lineage_digest(
    campaign: dict[str, object],
    supersession_digest: object,
) -> str:
    return _canonical_json_sha256(
        {
            "campaign": campaign,
            "supersession_digest": supersession_digest,
        }
    )


def _verified_identity(
    specification: object,
    *,
    candidate_root: Path,
    label: str,
) -> dict[str, str]:
    if not isinstance(specification, dict):
        raise ValueError(f"{label} identity must be an object")
    expected = specification.get("digest")
    if not isinstance(expected, str) or not SHA256_HEX.fullmatch(expected):
        raise ValueError(f"{label} identity digest is invalid")
    actual = artifact_identity(specification, candidate_root=candidate_root)
    if actual["digest"] != expected:
        raise ValueError(f"{label} identity does not match its candidate root")
    return {
        "algorithm": str(specification["algorithm"]),
        "digest": str(actual["digest"]),
    }


def _set_json_pointer(payload: object, pointer: str, value: object) -> None:
    if not pointer.startswith("/") or pointer == "/":
        raise ValueError(f"Runtime pointer must name one nested value: {pointer!r}")
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.removeprefix("/").split("/")
    ]
    parent = payload
    for part in parts[:-1]:
        if isinstance(parent, dict):
            if part not in parent:
                parent[part] = {}
            parent = parent[part]
        elif isinstance(parent, list) and part.isdigit() and int(part) < len(parent):
            parent = parent[int(part)]
        else:
            raise ValueError(f"Runtime pointer cannot be created: {pointer}")
    leaf = parts[-1]
    if isinstance(parent, dict):
        if leaf in parent:
            raise ValueError(f"Runtime pointer already exists: {pointer}")
        parent[leaf] = value
    elif isinstance(parent, list) and leaf.isdigit() and int(leaf) == len(parent):
        parent.append(value)
    else:
        raise ValueError(f"Runtime pointer cannot be created: {pointer}")


def build_behavioral_payloads(
    registration: dict[str, object],
    *,
    candidate_root: Path,
    output_root: Path,
) -> dict[str, object]:
    """Derive isolated M0/H1 payloads from one schema-v2 worker fixture."""

    root = candidate_root.resolve()
    fixture_spec = registration.get("fixture")
    fixture_identity = _verified_identity(
        fixture_spec,
        candidate_root=root,
        label="Worker fixture",
    )
    assert isinstance(fixture_spec, dict)
    fixture_path = _contained_artifact_path(root, fixture_spec.get("path"))
    fixture_result = lint_worker_fixture(fixture_path)
    if fixture_result["schema_version"] != CURRENT_FIXTURE_SCHEMA_VERSION:
        raise ValueError("Behavioral comparison requires worker-fixture schema version 2")
    terminal_spec = registration.get("terminal_registration")
    _verified_identity(
        terminal_spec,
        candidate_root=root,
        label="Terminal registration",
    )
    assert isinstance(terminal_spec, dict)
    lint_terminal_registration(
        fixture_path,
        _contained_artifact_path(root, terminal_spec.get("path")),
    )
    case_id = registration.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        raise ValueError("Behavioral comparison requires one fixture case")
    fixture_case = _fixture_case(fixture_path, case_id)
    runtime_pointer = registration.get("runtime_pointer")
    if not isinstance(runtime_pointer, str):
        raise ValueError("Behavioral comparison requires one runtime pointer")
    runtimes = registration.get("runtimes")
    if not isinstance(runtimes, dict) or set(runtimes) != {"m0", "h1"}:
        raise ValueError("Behavioral comparison requires exact m0 and h1 runtimes")

    resolved_output = output_root.resolve()
    if not _is_within(resolved_output, root / ".tmp"):
        raise ValueError("Generated behavioral payloads must stay inside .tmp")
    resolved_output.mkdir(parents=True, exist_ok=True)
    generated: dict[str, dict[str, str]] = {}
    for arm in ("m0", "h1"):
        runtime_spec = runtimes[arm]
        runtime_identity = _verified_identity(
            runtime_spec,
            candidate_root=root,
            label=f"{arm} runtime",
        )
        assert isinstance(runtime_spec, dict)
        payload = copy.deepcopy(fixture_case)
        _set_json_pointer(
            payload,
            runtime_pointer,
            {
                "candidate_root": str(root),
                "path": runtime_spec.get("path"),
                "identity": runtime_identity,
            },
        )
        _lint_dispatch_payload(
            payload,
            arm.upper(),
            require_decision_state=True,
        )
        _verify_fixture_fidelity(payload, fixture_case, arm.upper())
        output_path = resolved_output / f"{case_id}-{arm}.json"
        _write_json_file(output_path, payload)
        generated[arm] = {
            "path": str(output_path),
            "candidate_identity": runtime_identity["digest"],
            "dispatch_payload_sha256": _canonical_json_sha256(payload),
        }

    m0_payload = _read_json(Path(generated["m0"]["path"]))
    h1_payload = _read_json(Path(generated["h1"]["path"]))
    normalized_m0 = copy.deepcopy(m0_payload)
    normalized_h1 = copy.deepcopy(h1_payload)
    _remove_json_pointer(normalized_m0, runtime_pointer)
    _remove_json_pointer(normalized_h1, runtime_pointer)
    if normalized_m0 != normalized_h1:
        raise ValueError("Generated payloads differ outside the runtime slot")
    return {
        "status": "ok",
        "case_id": case_id,
        "fixture_identity": fixture_identity["digest"],
        "runtime_pointer": runtime_pointer,
        "shared_payload_sha256": _canonical_json_sha256(normalized_m0),
        "payloads": generated,
    }


def lint_result_envelope(
    envelope: object,
    *,
    case_id: str,
    arm: str,
    candidate_root: Path,
    candidate_identity: str,
    fixture_identity: str,
    dispatch_payload_sha256: str,
    require_fresh: bool,
) -> dict[str, object]:
    """Validate result provenance and shape without interpreting its output."""

    required = {
        "schema_version",
        "case_id",
        "arm",
        "candidate_root",
        "candidate_identity",
        "fixture_identity",
        "dispatch_payload_sha256",
        "fresh",
        "output",
    }
    if not isinstance(envelope, dict) or set(envelope) != required:
        raise ValueError("Result envelope fields are incomplete or unexpected")
    checks = (
        (envelope["schema_version"] == 1, "schema version"),
        (envelope["case_id"] == case_id, "case identity"),
        (envelope["arm"] == arm, "arm identity"),
        (
            envelope["candidate_root"] == str(candidate_root.resolve()),
            "candidate root",
        ),
        (
            envelope["candidate_identity"] == candidate_identity,
            "candidate identity",
        ),
        (envelope["fixture_identity"] == fixture_identity, "fixture identity"),
        (
            envelope["dispatch_payload_sha256"] == dispatch_payload_sha256,
            "dispatch payload identity",
        ),
        (isinstance(envelope["fresh"], bool), "fresh state"),
        (_nonempty(envelope["output"]), "output"),
    )
    for valid, label in checks:
        if not valid:
            raise ValueError(f"Result envelope {label} is invalid")
    if require_fresh and envelope["fresh"] is not True:
        raise ValueError("Result envelope is not a fresh behavioral sample")
    return {"status": "ok", "case_id": case_id, "arm": arm}


def _markdown_anchors(content: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in content.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        text = re.sub(r"<[^>]+>", "", match.group(1)).strip().lower()
        slug = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        if not slug:
            continue
        count = counts.get(slug, 0)
        anchors.add(slug if count == 0 else f"{slug}-{count}")
        counts[slug] = count + 1
    return anchors


def _markdown_table_columns(line: str) -> int:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return 0
    return len(re.split(r"(?<!\\)\|", stripped)) - 2


def lint_markdown(
    path: Path,
    *,
    candidate_root: Path,
    hard_break_policy: str,
) -> dict[str, object]:
    """Check deterministic Markdown structure without judging its prose."""

    root = candidate_root.resolve()
    resolved = path.resolve()
    if not _is_within(resolved, root) or resolved.suffix.lower() != ".md":
        raise ValueError("Markdown path escapes candidate root or is not Markdown")
    if hard_break_policy not in {"allow", "forbid"}:
        raise ValueError("Markdown hard break policy must be allow or forbid")
    try:
        raw = resolved.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise ValueError("Markdown encoding must be UTF-8 without BOM")
        content = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Markdown encoding is not valid UTF-8") from error

    for number, line in enumerate(content.splitlines(), start=1):
        trailing = re.search(r"([ \t]+)$", line)
        if not trailing:
            continue
        whitespace = trailing.group(1)
        if whitespace == "  ":
            if hard_break_policy == "forbid":
                raise ValueError(f"Markdown hard break is forbidden at line {number}")
        else:
            raise ValueError(f"Markdown trailing whitespace at line {number}")

    fence: tuple[str, int] | None = None
    for line in content.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if not match:
            continue
        run = match.group(1)
        marker = run[0]
        if fence is None:
            fence = (marker, len(run))
        elif (
            fence[0] == marker
            and len(run) >= fence[1]
            and not line[match.end() :].strip()
        ):
            fence = None
    if fence is not None:
        raise ValueError("Markdown fence is unbalanced")

    table_rows: list[int] = []
    for line in content.splitlines() + [""]:
        columns = _markdown_table_columns(line)
        if columns:
            table_rows.append(columns)
            continue
        if len(table_rows) >= 2 and len(set(table_rows)) != 1:
            raise ValueError("Markdown table columns are inconsistent")
        table_rows = []

    for match in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)", content):
        target = unquote(match.group(1))
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("//"):
            continue
        path_text, _, fragment = target.partition("#")
        target_path = resolved if not path_text else (resolved.parent / path_text).resolve()
        if not _is_within(target_path, root) or not target_path.is_file():
            raise ValueError(f"Markdown local link does not resolve: {target}")
        if fragment:
            try:
                target_content = target_path.read_text(encoding="utf-8")
            except UnicodeError as error:
                raise ValueError("Markdown linked file encoding is invalid") from error
            if fragment not in _markdown_anchors(target_content):
                raise ValueError(f"Markdown anchor does not resolve: {target}")
    return {"status": "ok", "path": str(resolved)}


def lint_research_registry(
    path: Path,
    *,
    candidate_root: Path,
) -> dict[str, object]:
    """Check research provenance records without assessing evidence quality."""

    root = candidate_root.resolve()
    resolved = path.resolve()
    if not _is_within(resolved, root):
        raise ValueError("Research registry path escapes candidate root")
    registry = _read_json(resolved)
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        raise ValueError("Research registry shape or schema version is invalid")
    claims = registry.get("claims")
    evidence = registry.get("evidence")
    if not isinstance(claims, list) or not claims:
        raise ValueError("Research registry claims are missing")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("Research registry evidence is missing")
    claim_map = {
        item.get("id"): item
        for item in claims
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    evidence_map = {
        item.get("id"): item
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    if len(claim_map) != len(claims) or len(evidence_map) != len(evidence):
        raise ValueError("Research registry IDs are missing or duplicated")
    for claim_id, claim in claim_map.items():
        refs = claim.get("evidence")
        if (
            not isinstance(refs, list)
            or not refs
            or any(ref not in evidence_map for ref in refs)
        ):
            raise ValueError(f"Research claim {claim_id} evidence pointer is invalid")
        if any(
            not isinstance(evidence_map[ref].get("claim_ids"), list)
            or claim_id not in evidence_map[ref]["claim_ids"]
            for ref in refs
        ):
            raise ValueError(
                f"Research claim {claim_id} pointer is not bidirectional"
            )
    for evidence_id, record in evidence_map.items():
        claim_ids = record.get("claim_ids")
        if (
            not isinstance(claim_ids, list)
            or not claim_ids
            or any(claim_id not in claim_map for claim_id in claim_ids)
        ):
            raise ValueError(f"Research evidence {evidence_id} claim pointer is invalid")
        if any(evidence_id not in claim_map[claim_id]["evidence"] for claim_id in claim_ids):
            raise ValueError(f"Research evidence {evidence_id} pointer is not bidirectional")
        revision = record.get("revision")
        if not isinstance(revision, str) or not revision:
            raise ValueError(f"Research evidence {evidence_id} revision is missing")
        url = record.get("url")
        parsed = urlsplit(url) if isinstance(url, str) else None
        if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"Research evidence {evidence_id} URL is invalid")
        if not _nonempty(record.get("classification")):
            raise ValueError(f"Research evidence {evidence_id} classification is missing")
        limitations = record.get("limitations")
        if (
            not isinstance(limitations, list)
            or not limitations
            or any(not isinstance(item, str) or not item for item in limitations)
        ):
            raise ValueError(f"Research evidence {evidence_id} limitations are missing")
        capture = record.get("capture")
        try:
            _verified_identity(capture, candidate_root=root, label="Local capture")
        except (OSError, ValueError) as error:
            raise ValueError(
                f"Research evidence {evidence_id} capture identity is invalid: {error}"
            ) from error
        pointer = record.get("pointer")
        if not isinstance(pointer, str) or "#" not in pointer:
            raise ValueError(f"Research evidence {evidence_id} local pointer is invalid")
        pointer_path, fragment = pointer.split("#", 1)
        capture_path = (root / pointer_path).resolve()
        assert isinstance(capture, dict)
        bounded_capture = _contained_artifact_path(root, capture.get("path"))
        if (
            not _is_within(capture_path, root)
            or not (
                capture_path == bounded_capture
                or (bounded_capture.is_dir() and _is_within(capture_path, bounded_capture))
            )
            or not capture_path.is_file()
            or fragment not in _markdown_anchors(
                capture_path.read_text(encoding="utf-8")
            )
        ):
            raise ValueError(f"Research evidence {evidence_id} local pointer is dangling")
    return {
        "status": "ok",
        "claim_count": len(claim_map),
        "evidence_count": len(evidence_map),
    }


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
    start.add_argument(
        "--fresh-epoch",
        type=Path,
        help="Owner-authored Fresh admission packet for a v2 campaign",
    )
    start.add_argument("--json", action="store_true")

    verify = commands.add_parser("verify")
    verify.add_argument("manifest", type=Path)
    verify.add_argument("--worktree", type=Path, default=Path.cwd())
    verify.add_argument("--stage", dest="stage_override")
    verify.add_argument("--force-proof")
    verify.add_argument("--force-reason")
    verify.add_argument("--no-execute", action="store_true")
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
                    fresh_epoch=(
                        _read_json(args.fresh_epoch)
                        if args.fresh_epoch is not None
                        else None
                    ),
                )
            elif args.command == "verify":
                result = verify_campaign(
                    args.manifest,
                    worktree=args.worktree,
                    stage_override=args.stage_override,
                    force_proof=args.force_proof,
                    force_reason=args.force_reason,
                    no_execute=args.no_execute,
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
