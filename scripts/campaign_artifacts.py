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

from scripts import install_skills
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
CAMPAIGN_ROOT = Path("docs/validation/campaigns")
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
PREFLIGHT_KINDS = frozenset(
    {"behavioral-comparison", "installation", "markdown", "research"}
)
REQUIRED_PREFLIGHT_KINDS = {
    "prompt-3": frozenset({"behavioral-comparison", "markdown"}),
    "prompt-5": frozenset({"installation"}),
    "research": frozenset({"markdown", "research"}),
}
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
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
            "proof_registrations": [],
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
                }
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
    return {
        "proof_profile": profile_name,
        "inputs": sorted(normalized_inputs, key=lambda item: item["name"]),
        "target": target_identity,
        "environment": _environment_identity(candidate_root),
    }


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
        changed = {
            value
            for value in event.get("changed_inputs", [])
            if isinstance(value, str)
        }
        cutoff = event.get("observed_at")
        cutoff_time = _parse_timestamp(cutoff)
        if not changed or cutoff_time is None:
            continue
        event_stale: set[str] = set()
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
                if isinstance(item, dict) and isinstance(item.get("name"), str)
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


def _superseded_receipts(receipts: list[dict[str, object]]) -> set[str]:
    return {
        str(receipt["supersedes"])
        for receipt in receipts
        if isinstance(receipt.get("supersedes"), str)
    }


def _identity_key(identity_tuple: dict[str, object]) -> str:
    return _canonical_json_sha256(identity_tuple)


def _full_suite_key(identity_tuple: dict[str, object]) -> str:
    return _canonical_json_sha256(
        {
            "proof_profile": identity_tuple["proof_profile"],
            "target": identity_tuple["target"],
            "environment": identity_tuple["environment"],
        }
    )


def _exact_receipt(
    receipts: list[dict[str, object]],
    identity_tuple: dict[str, object],
    stale: set[str],
) -> dict[str, object] | None:
    superseded = _superseded_receipts(receipts)
    for receipt in reversed(receipts):
        if (
            receipt.get("schema_version") == PROOF_RECEIPT_SCHEMA_VERSION
            and str(receipt.get("id")) not in stale
            and str(receipt.get("id")) not in superseded
            and receipt.get("proof_profile") == identity_tuple["proof_profile"]
            and receipt.get("inputs") == identity_tuple["inputs"]
            and receipt.get("target") == identity_tuple["target"]
            and receipt.get("environment") == identity_tuple["environment"]
            and isinstance(receipt.get("exit_state"), dict)
            and receipt["exit_state"].get("code") == 0
        ):
            return receipt
    return None


def _latest_matching_receipt(
    receipts: list[dict[str, object]],
    identity_tuple: dict[str, object],
) -> dict[str, object] | None:
    for receipt in reversed(receipts):
        if (
            receipt.get("proof_profile") == identity_tuple["proof_profile"]
            and receipt.get("inputs") == identity_tuple["inputs"]
            and receipt.get("target") == identity_tuple["target"]
            and receipt.get("environment") == identity_tuple["environment"]
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


def _verify_registered_proof(
    manifest_path: Path,
    manifest: dict[str, object],
    *,
    worktree: Path,
    force_proof: str | None,
    force_reason: str | None,
    no_execute: bool,
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
    declared_stage = (
        semantic.get("declared_stage") if isinstance(semantic, dict) else None
    )
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
                identity_tuple,
                stale,
            )
            latest = _latest_matching_receipt(
                typed_receipts + appended,
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
    declared_stage = str(semantic["declared_stage"])
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
            if kind == "behavioral-comparison":
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
                _verify_installation_preflight(
                    registration,
                    candidate_root=candidate_root,
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
    return {
        "status": "verified",
        "preflight": {
            "completed": completed,
            "not_applicable": skipped,
        },
    }


def _verify_installation_preflight(
    registration: dict[str, object],
    *,
    candidate_root: Path,
) -> None:
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
        return

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
