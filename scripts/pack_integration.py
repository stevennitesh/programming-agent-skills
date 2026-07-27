"""Pure mechanical verification for one frozen installed skill pack."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts import (
    campaign_artifacts,
    install_skills,
    pack_contract,
    skill_pack_contract,
)


SCHEMA_RELATIVE = Path(
    "docs/validation/shared/schemas/pack-integration-manifest-v1.schema.json"
)
RESULT_SCHEMA_RELATIVE = Path(
    "docs/validation/shared/schemas/pack-integration-result-v1.schema.json"
)
SCHEMA_PATH = Path(__file__).resolve().parents[1] / SCHEMA_RELATIVE
RESULT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / RESULT_SCHEMA_RELATIVE
GATES = {
    "G01": "contract-and-pointer-integrity",
    "G02": "capability-authority-and-mutation-ownership",
    "G03": "positive-negative-and-collision-invocation",
    "G04": "relationship-entry-return-resume-and-nonexecution",
    "G05": "success-material-failure-and-completion",
    "G06": "context-budgets-and-foreign-procedure-absence",
    "G07": "minimal-workflow-coverage",
    "G08": "canonical-installed-manifest-and-relationship-parity",
    "G09": "essential-gap-and-critical-collision-closure",
    "G10": "behavioral-evidence-and-validator-negative-controls",
}
GATE_IDS = tuple(GATES)
BEHAVIORAL_PROFILE = "behavioral-evidence-v1"
STRUCTURAL_PROFILES = {
    gate_id: f"gate-{gate_id.lower()}-v1" for gate_id in GATE_IDS
}
RESULT_FIELDS = {
    "schema_version",
    "registration_id",
    "claim_class",
    "outcome",
    "observations",
}


def create_manifest() -> dict[str, object]:
    """Return an inactive integration manifest without semantic authority."""

    return {
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


def validate_manifest_shape(manifest: object) -> list[str]:
    """Return deterministic schema failures without changing the manifest."""

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, TypeError) as error:
        return [f"Pack integration schema is unavailable or invalid: {error}"]
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(manifest),
            key=lambda item: list(item.absolute_path),
        )
    ]


def validate_result_shape(result: object) -> list[str]:
    try:
        schema = json.loads(RESULT_SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, TypeError) as error:
        return [f"Pack integration result schema is unavailable or invalid: {error}"]
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(result),
            key=lambda item: list(item.absolute_path),
        )
    ]


def file_fingerprint(path: Path) -> str:
    return f"sha256-v1:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def installed_pack_fingerprint(
    installed_root: Path,
    skills: list[dict[str, object]],
) -> str:
    """Derive one installed-pack identity from exact selected skill trees."""

    records: list[dict[str, str]] = []
    for skill in sorted(skills, key=lambda row: str(row.get("skill_id"))):
        skill_id = skill.get("skill_id")
        name = skill.get("canonical_name")
        if not isinstance(skill_id, str) or not isinstance(name, str):
            raise ValueError("Installed pack skills require exact IDs and names")
        path = installed_root / name
        if not path.is_dir():
            raise ValueError(f"Installed skill is absent: {name}")
        records.append(
            {
                "skill_id": skill_id,
                "canonical_name": name,
                "fingerprint": (
                    "sha256-v1:" + install_skills.skill_tree_hash(path)
                ),
            }
        )
    return pack_contract.exact_fingerprint({"skills": records})


def _relationship_index_edges(text: str) -> list[tuple[str, str, str]]:
    """Read the canonical Runtime Composition table without interpreting prose."""

    in_runtime = False
    edges: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        if line == "## Runtime Composition":
            in_runtime = True
            continue
        if in_runtime and line.startswith("## "):
            break
        if not in_runtime or not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] == "Caller":
            continue

        def name(value: str) -> str:
            return value.strip().strip("`").removeprefix("$")

        edges.append((name(cells[0]), cells[1], name(cells[2])))
    return edges


def relationship_edges_match(
    expected: set[tuple[str, str, str]],
    observed: list[tuple[str, str, str]],
    selected_names: set[str],
) -> bool:
    """Require one exact row per selected Pack Contract relationship."""

    selected_edges = [
        edge
        for edge in observed
        if edge[0] in selected_names and edge[2] in selected_names
    ]
    touching_edges = [
        edge
        for edge in observed
        if edge[0] in selected_names or edge[2] in selected_names
    ]
    return (
        len(selected_edges) == len(set(selected_edges))
        and expected == set(selected_edges)
        and touching_edges == selected_edges
    )


def derive_coverage(registrations: object) -> dict[str, object]:
    """Derive gate coverage while leaving evidence interpretation to its owner."""

    failures: list[str] = []
    rows = registrations if isinstance(registrations, list) else []
    if not isinstance(registrations, list):
        failures.append("registrations must be a list")
    identifiers = [
        row.get("id")
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    ]
    if len(identifiers) != len(set(identifiers)):
        failures.append("registrations contain a duplicate ID")
    for row in rows:
        if not isinstance(row, dict):
            continue
        claim_class = row.get("claim_class")
        expected_profile = (
            BEHAVIORAL_PROFILE
            if claim_class == "behavioral"
            else STRUCTURAL_PROFILES.get(str(row.get("gate_id")))
        )
        if row.get("check_profile") != expected_profile:
            failures.append(
                f"{row.get('id')} check profile does not match its claim class"
            )
    gates: list[dict[str, object]] = []
    for gate_id in GATE_IDS:
        matching = [
            row
            for row in rows
            if isinstance(row, dict) and row.get("gate_id") == gate_id
        ]
        claim_classes = sorted(
            {
                str(row["claim_class"])
                for row in matching
                if row.get("claim_class") in {"behavioral", "structural"}
            }
        )
        if not matching:
            failures.append(f"{gate_id} has no registered deterministic check")
        gates.append(
            {
                "gate_id": gate_id,
                "name": GATES[gate_id],
                "registration_ids": sorted(
                    str(row["id"])
                    for row in matching
                    if isinstance(row.get("id"), str)
                ),
                "claim_classes": claim_classes,
            }
        )
    behavioral = [
        row
        for row in rows
        if isinstance(row, dict)
        and row.get("gate_id") == "G10"
        and row.get("claim_class") == "behavioral"
    ]
    if not behavioral:
        failures.append("G10 requires registered fresh behavioral evidence")
    for row in behavioral:
        preregistration = row.get("preregistration")
        required = {
            "protocol",
            "rubric",
            "fixtures",
            "controls",
            "repetitions",
            "variance",
            "environment_bounds",
        }
        if not isinstance(preregistration, dict) or not required.issubset(
            preregistration
        ):
            failures.append(
                f"G10 behavioral registration {row.get('id')} lacks complete "
                "preregistration, controls, repetition, variance, or environment bounds"
            )
    return {
        "status": "complete" if not failures else "blocked",
        "gates": gates,
        "failures": failures,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _contained_path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("Evidence pointer requires a nonempty path")
    relative = Path(value)
    if (
        relative.is_absolute()
        or value != relative.as_posix()
        or ".." in relative.parts
    ):
        raise ValueError("Evidence pointer must be a canonical relative path")
    resolved = skill_pack_contract.lexical_path(root / relative)
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ValueError("Evidence pointer escapes the worktree") from error
    return resolved


def _read_pointer(
    pointer: object,
    *,
    root: Path,
    label: str,
) -> tuple[Path, bytes]:
    if not isinstance(pointer, dict):
        raise ValueError(f"{label} is not an exact pointer")
    path = _contained_path(root, pointer.get("path"))
    skill_pack_contract.reject_unsafe_redirect(path, label)
    if not path.is_file():
        raise ValueError(f"{label} is absent: {pointer.get('path')}")
    content = path.read_bytes()
    observed = f"sha256-v1:{hashlib.sha256(content).hexdigest()}"
    if pointer.get("fingerprint") != observed:
        raise ValueError(f"{label} fingerprint is stale")
    return path, content


def _identity_failures(
    manifest: dict[str, object],
    *,
    root: Path,
    installed_root: Path,
) -> tuple[list[dict[str, str]], dict[str, object] | None]:
    failures: list[dict[str, str]] = []
    identities = manifest.get("identities")
    if not isinstance(identities, dict):
        return [{"code": "identities", "message": "identities are absent"}], None
    contract_pointer = identities.get("contract")
    if not isinstance(contract_pointer, dict) or contract_pointer.get("path") != (
        "docs/synthesis/skill-pack.md"
    ):
        return [
            {
                "code": "contract-owner",
                "message": "Pack Contract must use its canonical owner path",
            }
        ], None
    try:
        contract_path, contract_content = _read_pointer(
            contract_pointer,
            root=root,
            label="Pack Contract",
        )
        contract = pack_contract.parse_contract(contract_content.decode("utf-8"))
    except (
        OSError,
        UnicodeDecodeError,
        ValueError,
        pack_contract.PackContractError,
    ) as error:
        return [{"code": "contract", "message": str(error)}], None
    assert isinstance(contract_pointer, dict)
    expected_semantic = contract_pointer.get("semantic_fingerprint")
    observed_semantic = pack_contract.semantic_fingerprint(
        contract_path.read_text(encoding="utf-8")
    )
    header = contract.get("epoch_header")
    if not isinstance(header, dict):
        failures.append({"code": "contract", "message": "Pack Contract header is absent"})
        return failures, contract
    if pack_contract.validate_contract(contract):
        failures.append({"code": "contract", "message": "Pack Contract is invalid"})
    if (
        expected_semantic != observed_semantic
        or header.get("contract_revision") != contract_pointer.get("revision")
        or header.get("composition_epoch_id")
        != identities.get("composition_epoch_id")
        or header.get("status") not in {"frozen", "campaign-active"}
        or header.get("integration_result")
        != {"decision": None, "evidence_pointer": None}
        or header.get("epoch_lock") is not None
    ):
        failures.append(
            {
                "code": "contract-identity",
                "message": "Pack Contract epoch, revision, lifecycle, or fingerprint is mixed",
            }
        )
    selected = [
        row for row in contract.get("selected_skills", []) if isinstance(row, dict)
    ]
    selected_by_id = {str(row.get("skill_id")): row for row in selected}
    campaign_rows = identities.get("campaigns")
    if not isinstance(campaign_rows, list):
        campaign_rows = []
    campaign_ids = [
        str(row.get("skill_id"))
        for row in campaign_rows
        if isinstance(row, dict)
    ]
    if len(campaign_ids) != len(set(campaign_ids)):
        failures.append(
            {
                "code": "campaign-duplicate",
                "message": "Campaign identities contain a duplicate skill ID",
            }
        )
    campaign_by_id = {
        str(row.get("skill_id")): row
        for row in campaign_rows
        if isinstance(row, dict)
    }
    if set(campaign_by_id) != set(selected_by_id):
        failures.append(
            {
                "code": "campaign-coverage",
                "message": "Campaign identities do not exactly cover selected skills",
            }
        )
    for skill_id, selected_skill in selected_by_id.items():
        row = campaign_by_id.get(skill_id)
        state = selected_skill.get("campaign_state")
        if not isinstance(row, dict) or not isinstance(state, dict):
            continue
        name = selected_skill.get("canonical_name")
        expected_campaign_pointer = state.get("terminal_evidence_pointer")
        expected_campaign_path = (
            f"docs/validation/skills/{name}/campaigns/"
            f"{row.get('campaign_id')}/manifest.json"
        )
        if (
            state.get("status") != "terminal"
            or state.get("campaign_id") != row.get("campaign_id")
            or row.get("canonical_name") != name
            or row.get("contract_revision") != header.get("contract_revision")
            or not isinstance(row.get("manifest"), dict)
            or row["manifest"].get("path") != expected_campaign_pointer
            or expected_campaign_pointer != expected_campaign_path
        ):
            failures.append(
                {
                    "code": "campaign-state",
                    "message": f"{skill_id} campaign state or revision is mixed",
                }
            )
            continue
        try:
            campaign_path, _ = _read_pointer(
                row.get("manifest"),
                root=root,
                label=f"{skill_id} campaign manifest",
            )
            campaign = campaign_artifacts.read_campaign_manifest(campaign_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append(
                {"code": "campaign-manifest", "message": f"{skill_id}: {error}"}
            )
            continue
        campaign_record = campaign.get("campaign")
        campaign_contract = campaign.get("contract")
        semantic = campaign.get("semantic")
        mechanical = campaign.get("mechanical")
        if not all(
            isinstance(value, dict)
            for value in (campaign_record, campaign_contract, semantic, mechanical)
        ):
            failures.append(
                {"code": "campaign-manifest", "message": f"{skill_id} is malformed"}
            )
            continue
        assert isinstance(campaign_record, dict)
        assert isinstance(campaign_contract, dict)
        assert isinstance(semantic, dict)
        assert isinstance(mechanical, dict)
        pack_pointer = campaign_contract.get("pack_contract")
        slice_pointer = campaign_contract.get("slice")
        derived_slice = pack_contract.campaign_admission_slice(
            contract,
            skill_id,
            allow_terminal_projection=True,
        )
        derived_envelope = derived_slice.get("slice")
        artifact_rows = mechanical.get("artifact_identities")
        artifact_map = {
            value.get("name"): value.get("fingerprint")
            for value in artifact_rows
            if isinstance(value, dict)
        } if isinstance(artifact_rows, list) else {}
        if (
            campaign.get("schema_version") != 2
            or campaign_record.get("id") != row.get("campaign_id")
            or campaign_record.get("skill") != name
            or campaign_record.get("composition_epoch_id")
            != identities.get("composition_epoch_id")
            or not isinstance(pack_pointer, dict)
            or pack_pointer.get("revision") != str(header.get("contract_revision"))
            or pack_pointer.get("fingerprint") != expected_semantic
            or not isinstance(slice_pointer, dict)
            or not isinstance(derived_envelope, dict)
            or slice_pointer.get("id") != derived_envelope.get("slice_id")
            or slice_pointer.get("fingerprint")
            != derived_slice.get("slice_fingerprint")
            or row.get("slice_fingerprint")
            != derived_slice.get("slice_fingerprint")
            or campaign_contract.get("selected_capability_ids")
            != derived_envelope.get("selected_capability_ids")
            or campaign_contract.get("selected_relationship_ids")
            != derived_envelope.get("selected_relationship_ids")
            or campaign_contract.get("selected_scenario_ids")
            != derived_envelope.get("selected_scenario_ids")
            or campaign_contract.get("proof_predecessors")
            != derived_envelope.get("hard_proof_predecessor_ids")
            or semantic.get("terminal_token") != "campaign-complete"
            or semantic.get("lifecycle") != campaign_artifacts.FRESH_TERMINAL_LIFECYCLE
            or mechanical.get("evidence_state") != "current"
            or artifact_map.get("canonical-p1")
            != row.get("canonical_p1_fingerprint")
            or artifact_map.get("installed-p1")
            != row.get("installed_p1_fingerprint")
            or mechanical.get("parity")
            != {
                "canonical_installed": "match",
                "relationship_ids": sorted(
                    relationship.get("relationship_id")
                    for relationship in contract.get("relationships", [])
                    if isinstance(relationship, dict)
                    and skill_id
                    in {
                        relationship.get("caller_skill_id"),
                        relationship.get("target_skill_id"),
                        relationship.get("resume_owner_skill_id"),
                        relationship.get("combined_exit_owner_skill_id"),
                    }
                ),
            }
        ):
            failures.append(
                {
                    "code": "campaign-identity",
                    "message": f"{skill_id} terminal campaign identity is mixed",
                }
            )
        canonical_path = root / "skills/custom" / str(name)
        try:
            skill_pack_contract.reject_unsafe_redirect(
                installed_root,
                "installed skill pack",
            )
            canonical_fp = (
                "sha256-v1:" + install_skills.skill_tree_hash(canonical_path)
            )
            installed_fp = (
                "sha256-v1:"
                + install_skills.skill_tree_hash(installed_root / str(name))
            )
        except (OSError, ValueError) as error:
            failures.append(
                {"code": "installed-identity", "message": f"{skill_id} installed: {error}"}
            )
        else:
            if (
                canonical_fp != row.get("canonical_p1_fingerprint")
                or installed_fp != row.get("installed_p1_fingerprint")
                or canonical_fp != installed_fp
            ):
                failures.append(
                    {
                        "code": "installed-identity",
                        "message": f"{skill_id} canonical and installed P1 are mixed",
                    }
                )
    installed_record = identities.get("installed_pack")
    if isinstance(installed_record, dict):
        try:
            skill_pack_contract.reject_unsafe_redirect(
                installed_root,
                "installed skill pack",
            )
            observed_installed = installed_pack_fingerprint(installed_root, selected)
            managed_manifest_path = (
                installed_root / ".programming-agent-skills-manifest.json"
            )
            skill_pack_contract.reject_unsafe_redirect(
                managed_manifest_path,
                "installed skill manifest",
            )
            managed_payload = json.loads(
                managed_manifest_path.read_text(encoding="utf-8")
            )
            managed_names, managed_hashes, managed_failures = (
                skill_pack_contract.parse_managed_manifest_payload(managed_payload)
            )
            selected_names = {
                str(row.get("canonical_name")) for row in selected
            }
            if managed_failures or selected_names != managed_names:
                raise ValueError(
                    "Installed managed manifest does not exactly match selected skills"
                )
            for name in selected_names:
                if managed_hashes.get(name) != install_skills.skill_tree_hash(
                    installed_root / name
                ):
                    raise ValueError(
                        f"Installed managed manifest hash is stale for {name}"
                    )
            observed_manifest = file_fingerprint(managed_manifest_path)
        except (OSError, ValueError) as error:
            failures.append({"code": "installed-pack", "message": str(error)})
        else:
            if (
                installed_record.get("fingerprint") != observed_installed
                or installed_record.get("manifest_fingerprint")
                != observed_manifest
            ):
                failures.append(
                    {
                        "code": "installed-pack",
                        "message": "Installed pack identity is mixed or stale",
                    }
                )
    else:
        failures.append({"code": "installed-pack", "message": "Installed pack is absent"})
    relationship_pointer = identities.get("relationship_index")
    if (
        not isinstance(relationship_pointer, dict)
        or relationship_pointer.get("path")
        != "docs/synthesis/skill-context-relationships.md"
    ):
        failures.append(
            {
                "code": "relationship-owner",
                "message": "Relationship index must use its canonical owner path",
            }
        )
    relationship_content = b""
    try:
        _, relationship_content = _read_pointer(
            relationship_pointer,
            root=root,
            label="relationship index",
        )
    except (OSError, ValueError) as error:
        failures.append({"code": "relationship-index", "message": str(error)})
    expected_relationships = sorted(
        (
            {
                "relationship_id": row.get("relationship_id"),
                "caller_skill_id": row.get("caller_skill_id"),
                "target_skill_id": row.get("target_skill_id"),
                "resume_owner_skill_id": row.get("resume_owner_skill_id"),
                "combined_exit_owner_skill_id": row.get(
                    "combined_exit_owner_skill_id"
                ),
            }
            for row in contract.get("relationships", [])
            if isinstance(row, dict)
        ),
        key=lambda row: str(row["relationship_id"]),
    )
    if identities.get("relationship_projection") != expected_relationships:
        failures.append(
            {
                "code": "relationship-parity",
                "message": "Relationship projection does not match the Pack Contract",
            }
        )
    selected_names_by_id = {
        str(row.get("skill_id")): str(row.get("canonical_name"))
        for row in selected
    }
    expected_edges = {
        (
            selected_names_by_id[str(row.get("caller_skill_id"))],
            str(row.get("verb")),
            selected_names_by_id[str(row.get("target_skill_id"))],
        )
        for row in contract.get("relationships", [])
        if isinstance(row, dict)
        and str(row.get("caller_skill_id")) in selected_names_by_id
        and str(row.get("target_skill_id")) in selected_names_by_id
    }
    observed_edges = _relationship_index_edges(
        relationship_content.decode("utf-8", errors="replace")
    )
    selected_names = set(selected_names_by_id.values())
    if not relationship_edges_match(
        expected_edges,
        observed_edges,
        selected_names,
    ):
        failures.append(
            {
                "code": "relationship-index-parity",
                "message": "Runtime Composition relationships do not match the Pack Contract",
            }
        )
    return failures, contract


def _registration_pointers(registration: dict[str, object]) -> list[tuple[str, object]]:
    pointers = [
        ("result", registration.get("result")),
        *[
            (f"input[{index}]", pointer)
            for index, pointer in enumerate(registration.get("inputs", []))
        ],
    ]
    preregistration = registration.get("preregistration")
    if isinstance(preregistration, dict):
        pointers.extend(
            [
                ("protocol", preregistration.get("protocol")),
                ("rubric", preregistration.get("rubric")),
                ("environment_bounds", preregistration.get("environment_bounds")),
            ]
        )
        pointers.extend(
            (f"fixture[{index}]", pointer)
            for index, pointer in enumerate(preregistration.get("fixtures", []))
        )
    return pointers


def _invalidated_receipt_ids(manifest: dict[str, object]) -> set[str]:
    return {
        str(receipt_id)
        for row in manifest.get("invalidations", [])
        if isinstance(row, dict)
        for receipt_id in row.get("receipt_ids", [])
        if isinstance(receipt_id, str)
    }


def _replace_json(path: Path, payload: object) -> None:
    skill_pack_contract.reject_unsafe_redirect(path, "pack integration write")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _return(
    status: str,
    *,
    failures: list[dict[str, str]],
    coverage: list[dict[str, object]] | None = None,
    invalidated: list[str] | None = None,
    parity: dict[str, str] | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "schema_version": 1,
        "status": status,
        "evidence_class": "mechanical-only",
        "owner": "fresh-composition-epoch",
        "coverage": coverage or [],
        "failures": failures,
        "invalidated_receipt_ids": invalidated or [],
        "parity": parity
        or {
            "contract_campaigns_installed": "mismatch",
            "relationship_index": "mismatch",
        },
    }
    return result


def _run_registration(
    registration: dict[str, object],
    *,
    root: Path,
    manifest: dict[str, object],
    contract: dict[str, object],
) -> tuple[str, list[dict[str, object]], list[dict[str, str]]]:
    """Run one gate-owned deterministic profile without semantic interpretation."""

    profile = registration.get("check_profile")
    if profile == BEHAVIORAL_PROFILE:
        result_pointer = registration.get("result")
        try:
            _, content = _read_pointer(
                result_pointer,
                root=root,
                label=f"{registration.get('id')} behavioral result",
            )
            payload = json.loads(content.decode("utf-8"))
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
        ) as error:
            return "fail", [], [
                {"code": "behavioral-result", "message": str(error)}
            ]
        if (
            not isinstance(payload, dict)
            or set(payload) != RESULT_FIELDS
            or payload.get("schema_version") != 1
            or payload.get("registration_id") != registration.get("id")
            or payload.get("claim_class") != "behavioral"
            or payload.get("outcome") != "evidence-recorded"
            or not isinstance(payload.get("observations"), list)
            or not payload["observations"]
        ):
            return "fail", [], [
                {
                    "code": "behavioral-result",
                    "message": "Behavioral evidence envelope is invalid",
                }
            ]
        return "evidence-recorded", deepcopy(payload["observations"]), []
    gate_id = str(registration.get("gate_id"))
    if profile != STRUCTURAL_PROFILES.get(gate_id):
        return "fail", [], [
            {"code": "check-profile", "message": f"Unknown check profile: {profile}"}
        ]
    header = contract.get("epoch_header")
    skills = [
        row for row in contract.get("selected_skills", []) if isinstance(row, dict)
    ]
    capabilities = [
        row for row in contract.get("capabilities", []) if isinstance(row, dict)
    ]
    relationships = [
        row for row in contract.get("relationships", []) if isinstance(row, dict)
    ]
    issues = [
        row
        for row in contract.get("exclusions_collisions_gaps", [])
        if isinstance(row, dict)
    ]
    skill_ids = {row.get("skill_id") for row in skills}
    checks: dict[str, list[tuple[str, bool]]] = {
        "G01": [
            ("contract-schema-and-identities", not pack_contract.validate_contract(contract))
        ],
        "G02": [
            (
                "capability-owners-and-authority",
                all(
                    row.get("primary_owner_skill_id") in skill_ids
                    and bool(row.get("required_authority_mutation"))
                    for row in capabilities
                ),
            )
        ],
        "G03": [
            (
                "positive-negative-and-scenario-entry",
                all(
                    bool(row.get("positive_entry_predicate"))
                    and bool(row.get("negative_exclusion_predicates"))
                    and bool(row.get("acceptance_scenario_ids"))
                    for row in skills
                ),
            )
        ],
        "G04": [
            (
                "relationship-entry-return-resume",
                all(
                    bool(row.get("entry_condition"))
                    and bool(row.get("wrong_condition"))
                    and bool(row.get("return_packet"))
                    and row.get("resume_owner_skill_id") in skill_ids
                    for row in relationships
                ),
            )
        ],
        "G05": [
            (
                "success-failure-completion",
                all(
                    bool(row.get("completion_condition"))
                    and bool(row.get("failure_return"))
                    and bool(row.get("return_packet"))
                    and isinstance(row.get("campaign_state"), dict)
                    and row["campaign_state"].get("status") == "terminal"
                    for row in skills
                ),
            )
        ],
        "G06": [
            (
                "context-budget-and-exclusions",
                isinstance(header, dict)
                and bool(header.get("load_budget_policy"))
                and bool(header.get("exclusions"))
                and all(bool(row.get("load_budget_class")) for row in skills),
            )
        ],
        "G07": [
            (
                "minimal-workflow-coverage",
                {row.get("primary_owner_skill_id") for row in capabilities}
                .issubset(skill_ids)
                and all(
                    set(row.get("owned_capability_ids", []))
                    == {
                        capability.get("capability_id")
                        for capability in capabilities
                        if capability.get("primary_owner_skill_id")
                        == row.get("skill_id")
                    }
                    for row in skills
                ),
            )
        ],
        "G08": [("canonical-installed-manifest-relationship-parity", True)],
        "G09": [
            (
                "essential-gap-and-collision-closure",
                all(
                    row.get("status") == "resolved"
                    or (
                        not row.get("essential")
                        and row.get("class")
                        not in pack_contract.COLLISION_CLASSES
                        and row.get("status") == "deferred"
                        and bool(row.get("resolution"))
                        and bool(
                            row.get("future_owner_or_stopping_condition")
                        )
                        and bool(row.get("nondependency_proof_ids"))
                    )
                    for row in issues
                ),
            )
        ],
        "G10": [
            (
                "behavioral-and-negative-control-registration",
                any(
                    isinstance(row, dict)
                    and row.get("gate_id") == "G10"
                    and row.get("claim_class") == "behavioral"
                    for row in manifest.get("registrations", [])
                ),
            )
        ],
    }
    observations = [
        {"check": name, "passed": passed}
        for name, passed in checks.get(gate_id, [])
    ]
    if not observations:
        return "fail", [], [
            {"code": "check-profile", "message": f"No built-in check for {gate_id}"}
        ]
    return (
        "pass" if all(row["passed"] for row in observations) else "fail",
        observations,
        [],
    )


def _candidate_fingerprint(
    manifest: dict[str, object],
    *,
    installed_root: Path,
) -> str:
    identities = deepcopy(manifest["identities"])
    assert isinstance(identities, dict)
    identities["installed_root"] = str(
        skill_pack_contract.lexical_path(installed_root)
    )
    return pack_contract.exact_fingerprint(identities)


def _receipt_history_failures(manifest: dict[str, object]) -> list[dict[str, str]]:
    registrations = manifest.get("registrations")
    receipts = manifest.get("receipts")
    invalidations = manifest.get("invalidations")
    assert isinstance(registrations, list)
    assert isinstance(receipts, list)
    assert isinstance(invalidations, list)
    registrations_by_id = {
        row["id"]: row
        for row in registrations
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    receipt_ids = [
        row.get("id") for row in receipts if isinstance(row, dict)
    ]
    failures: list[dict[str, str]] = []
    if len(receipt_ids) != len(set(receipt_ids)):
        failures.append(
            {"code": "receipt-history", "message": "Receipt IDs must be unique"}
        )
    known_receipts = {value for value in receipt_ids if isinstance(value, str)}
    for receipt in receipts:
        if not isinstance(receipt, dict):
            continue
        registration = registrations_by_id.get(receipt.get("registration_id"))
        if (
            not isinstance(registration, dict)
            or receipt.get("gate_id") != registration.get("gate_id")
            or receipt.get("claim_class") != registration.get("claim_class")
        ):
            failures.append(
                {
                    "code": "receipt-history",
                    "message": "Receipt metadata contradicts its registration",
                }
            )
    invalidated: list[str] = []
    for row in invalidations:
        if not isinstance(row, dict):
            continue
        invalidated.extend(
            value for value in row.get("receipt_ids", []) if isinstance(value, str)
        )
    if len(invalidated) != len(set(invalidated)) or not set(invalidated).issubset(
        known_receipts
    ):
        failures.append(
            {
                "code": "receipt-history",
                "message": "Invalidations must reference unique known receipts",
            }
        )
    return failures


def verify_integration(
    manifest_path: Path,
    *,
    worktree: Path | None = None,
    installed_root: Path | None = None,
    result_path: Path | None = None,
    no_write: bool = False,
) -> dict[str, object]:
    """Verify one exact pack candidate without interpreting or advancing it."""

    root = skill_pack_contract.lexical_path(worktree or Path.cwd())
    installed = skill_pack_contract.lexical_path(
        installed_root or root / "installed"
    )
    supplied = skill_pack_contract.lexical_path(manifest_path)
    try:
        skill_pack_contract.reject_unsafe_redirect(
            supplied,
            "pack integration manifest",
        )
        supplied.relative_to(root)
        manifest = json.loads(supplied.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return _return(
            "blocked",
            failures=[{"code": "manifest", "message": str(error)}],
        )
    identities = manifest.get("identities") if isinstance(manifest, dict) else None
    epoch_id = (
        identities.get("composition_epoch_id")
        if isinstance(identities, dict)
        else None
    )
    if isinstance(epoch_id, str):
        expected_manifest = skill_pack_contract.lexical_path(
            root
            / "docs/validation/skill-pack"
            / epoch_id
            / "integration-manifest.json"
        )
        if supplied != expected_manifest:
            return _return(
                "blocked",
                failures=[
                    {
                        "code": "manifest-owner",
                        "message": "Integration manifest is outside its epoch owner",
                    }
                ],
            )
    if result_path is not None:
        destination = skill_pack_contract.lexical_path(result_path)
        if destination != supplied.parent / "results.json":
            return _return(
                "blocked",
                failures=[
                    {
                        "code": "result-owner",
                        "message": "Integration result must be the epoch-owned results.json",
                    }
                ],
            )
    shape_failures = validate_manifest_shape(manifest)
    if shape_failures:
        return _return(
            "blocked",
            failures=[
                {"code": "manifest-schema", "message": failure}
                for failure in shape_failures
            ],
        )
    assert isinstance(manifest, dict)
    coverage_result = derive_coverage(manifest.get("registrations"))
    if coverage_result["status"] != "complete":
        return _return(
            "blocked",
            failures=[
                {"code": "coverage", "message": failure}
                for failure in coverage_result["failures"]  # type: ignore[index]
            ],
        )
    registrations_for_owner = manifest.get("registrations")
    assert isinstance(registrations_for_owner, list)
    for registration in registrations_for_owner:
        assert isinstance(registration, dict)
        for label, registered_pointer in _registration_pointers(registration):
            if not isinstance(registered_pointer, dict):
                continue
            try:
                registered_path = _contained_path(
                    root,
                    registered_pointer.get("path"),
                )
                registered_path.relative_to(supplied.parent)
            except ValueError:
                return _return(
                    "blocked",
                    failures=[
                        {
                            "code": "evidence-owner",
                            "message": (
                                f"{registration.get('id')} {label} is outside "
                                "the pack-validation epoch"
                            ),
                        }
                    ],
                )
    history_failures = _receipt_history_failures(manifest)
    if history_failures:
        return _return("blocked", failures=history_failures)
    identity_failures, contract = _identity_failures(
        manifest,
        root=root,
        installed_root=installed,
    )
    if identity_failures:
        active_receipts = [
            str(row["id"])
            for row in manifest.get("receipts", [])
            if isinstance(row, dict)
            and isinstance(row.get("id"), str)
            and row["id"] not in _invalidated_receipt_ids(manifest)
        ]
        if active_receipts:
            invalidations = manifest.get("invalidations")
            assert isinstance(invalidations, list)
            invalidations.append(
                {
                    "registration_id": "candidate",
                    "receipt_ids": active_receipts,
                    "changed_inputs": sorted(
                        {failure["code"] for failure in identity_failures}
                    ),
                    "observed_at": _now(),
                }
            )
            if not no_write:
                _replace_json(supplied, manifest)
        return _return(
            "blocked",
            failures=identity_failures,
            invalidated=active_receipts,
        )
    assert isinstance(contract, dict)
    receipts = manifest.get("receipts")
    invalidations = manifest.get("invalidations")
    registrations = manifest.get("registrations")
    assert isinstance(receipts, list)
    assert isinstance(invalidations, list)
    assert isinstance(registrations, list)
    invalidated_ids = _invalidated_receipt_ids(manifest)
    candidate_fingerprint = _candidate_fingerprint(
        manifest,
        installed_root=installed,
    )
    previous_candidate_receipts = [
        str(row["id"])
        for row in receipts
        if isinstance(row, dict)
        and isinstance(row.get("id"), str)
        and row["id"] not in invalidated_ids
        and row.get("candidate_fingerprint") != candidate_fingerprint
    ]
    if previous_candidate_receipts:
        invalidations.append(
            {
                "registration_id": "candidate",
                "receipt_ids": previous_candidate_receipts,
                "changed_inputs": ["candidate_fingerprint"],
                "observed_at": _now(),
            }
        )
        invalidated_ids.update(previous_candidate_receipts)
    coverage: dict[str, dict[str, object]] = {
        gate_id: {
            "gate_id": gate_id,
            "name": GATES[gate_id],
            "registration_ids": [],
            "receipt_ids": [],
            "claim_classes": [],
        }
        for gate_id in GATE_IDS
    }
    stale_registration_ids: list[str] = []
    stale_receipt_ids: list[str] = []
    for registration in registrations:
        assert isinstance(registration, dict)
        registration_id = str(registration["id"])
        pointer_identities: list[dict[str, str]] = []
        try:
            for label, registered_pointer in _registration_pointers(registration):
                path, _ = _read_pointer(
                    registered_pointer,
                    root=root,
                    label=f"{registration_id} {label}",
                )
                assert isinstance(registered_pointer, dict)
                pointer_identities.append(
                    {
                        "label": label,
                        "path": path.relative_to(root).as_posix(),
                        "fingerprint": str(registered_pointer["fingerprint"]),
                    }
                )
        except (OSError, ValueError) as error:
            stale_registration_ids.append(registration_id)
            dependent = [
                str(receipt["id"])
                for receipt in receipts
                if isinstance(receipt, dict)
                and receipt.get("registration_id") == registration_id
                and isinstance(receipt.get("id"), str)
                and receipt["id"] not in invalidated_ids
            ]
            stale_receipt_ids.extend(dependent)
            if dependent:
                invalidations.append(
                    {
                        "registration_id": registration_id,
                        "receipt_ids": dependent,
                        "changed_inputs": [str(error)],
                        "observed_at": _now(),
                    }
                )
                invalidated_ids.update(dependent)
            continue
        outcome, observations, check_failures = _run_registration(
            registration,
            root=root,
            manifest=manifest,
            contract=contract,
        )
        if check_failures:
            if (
                stale_receipt_ids or previous_candidate_receipts
            ) and not no_write:
                _replace_json(supplied, manifest)
            return _return("failed", failures=check_failures)
        identity = pack_contract.exact_fingerprint(
            {
                "candidate_fingerprint": candidate_fingerprint,
                "registration": registration,
                "pointers": pointer_identities,
                "outcome": outcome,
                "observations": observations,
            }
        )
        replaced = [
            str(receipt["id"])
            for receipt in receipts
            if isinstance(receipt, dict)
            and receipt.get("registration_id") == registration_id
            and receipt.get("candidate_fingerprint") == candidate_fingerprint
            and receipt.get("identity") != identity
            and isinstance(receipt.get("id"), str)
            and receipt["id"] not in invalidated_ids
        ]
        if replaced:
            invalidations.append(
                {
                    "registration_id": registration_id,
                    "receipt_ids": replaced,
                    "changed_inputs": ["registration_identity"],
                    "observed_at": _now(),
                }
            )
            stale_receipt_ids.extend(replaced)
            invalidated_ids.update(replaced)
        contradictory = next(
            (
                receipt
                for receipt in receipts
                if isinstance(receipt, dict)
                and receipt.get("registration_id") == registration_id
                and receipt.get("identity") == identity
                and receipt.get("candidate_fingerprint") == candidate_fingerprint
                and receipt.get("id") not in invalidated_ids
                and (
                    receipt.get("outcome") != outcome
                    or receipt.get("observations") != observations
                )
            ),
            None,
        )
        if contradictory is not None:
            if (previous_candidate_receipts or stale_receipt_ids) and not no_write:
                _replace_json(supplied, manifest)
            return _return(
                "blocked",
                failures=[
                    {
                        "code": "receipt-history",
                        "message": "Receipt outcome or observations contradict execution",
                    }
                ],
            )
        matching = next(
            (
                receipt
                for receipt in receipts
                if isinstance(receipt, dict)
                and receipt.get("registration_id") == registration_id
                and receipt.get("identity") == identity
                and receipt.get("candidate_fingerprint") == candidate_fingerprint
                and receipt.get("id") not in invalidated_ids
            ),
            None,
        )
        if matching is None:
            receipt = {
                "id": (
                    f"PIREC-{identity.removeprefix('sha256-v1:')[:16]}-"
                    f"{len(receipts) + 1:04d}"
                ),
                "registration_id": registration_id,
                "gate_id": registration["gate_id"],
                "claim_class": registration["claim_class"],
                "identity": identity,
                "candidate_fingerprint": candidate_fingerprint,
                "outcome": outcome,
                "observations": observations,
                "observed_at": _now(),
            }
            receipts.append(receipt)
        else:
            receipt = matching
        gate = coverage[str(registration["gate_id"])]
        gate["registration_ids"].append(registration_id)  # type: ignore[union-attr]
        gate["receipt_ids"].append(receipt["id"])  # type: ignore[union-attr]
        gate["claim_classes"].append(registration["claim_class"])  # type: ignore[union-attr]
        if outcome == "fail":
            if not no_write:
                _replace_json(supplied, manifest)
            return _return(
                "failed",
                failures=[
                    {
                        "code": "registered-check",
                        "message": f"{registration_id} reported structural failure",
                    }
                ],
                coverage=list(coverage.values()),
            )
    if stale_registration_ids:
        if not no_write:
            _replace_json(supplied, manifest)
        return _return(
            "stale",
            failures=[
                {
                    "code": "stale-identity",
                    "message": (
                        "Exact evidence identity drifted for "
                        + ", ".join(stale_registration_ids)
                    ),
                }
            ],
            invalidated=stale_receipt_ids,
        )
    for gate in coverage.values():
        gate["registration_ids"] = sorted(set(gate["registration_ids"]))  # type: ignore[arg-type]
        gate["receipt_ids"] = sorted(set(gate["receipt_ids"]))  # type: ignore[arg-type]
        gate["claim_classes"] = sorted(set(gate["claim_classes"]))  # type: ignore[arg-type]
    parity = {
        "contract_campaigns_installed": "match",
        "relationship_index": "match",
    }
    manifest["parity"] = deepcopy(parity)
    if not no_write:
        _replace_json(supplied, manifest)
    result = _return(
        "verified",
        failures=[],
        coverage=list(coverage.values()),
        parity=parity,
    )
    result_failures = validate_result_shape(result)
    if result_failures:
        return _return(
            "failed",
            failures=[
                {"code": "result-schema", "message": failure}
                for failure in result_failures
            ],
        )
    if result_path is not None and not no_write:
        destination = skill_pack_contract.lexical_path(result_path)
        _replace_json(destination, result)
    return result


def validate_repository(root: Path) -> list[str]:
    """Validate the inactive owners and the verifier's mechanical surface."""

    failures: list[str] = []
    for path, label in (
        (root / SCHEMA_RELATIVE, "manifest schema"),
        (root / RESULT_SCHEMA_RELATIVE, "result schema"),
    ):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except (OSError, json.JSONDecodeError, TypeError) as error:
            failures.append(f"Pack integration {label} is invalid: {error}")
    owner = root / "docs/validation/skill-pack/README.md"
    try:
        owner_text = owner.read_text(encoding="utf-8")
    except OSError as error:
        failures.append(f"Pack integration owner is unreadable: {error}")
    else:
        for required in (
            "all ten gates",
            "mechanical",
            "cannot accept",
            "scripts.pack_integration",
        ):
            if required not in owner_text:
                failures.append(
                    f"Pack integration owner omits required boundary: {required}"
                )
    help_text = build_parser().format_help().casefold()
    for operation in ("accept", "lock", "repair", "schedule", "score", "start"):
        if operation in help_text:
            failures.append(
                f"Pack integration verifier exposes forbidden operation: {operation}"
            )
    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify exact pack integration evidence."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--worktree", type=Path, default=Path.cwd())
    parser.add_argument("--installed-root", type=Path, required=True)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--no-write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = verify_integration(
        args.manifest,
        worktree=args.worktree,
        installed_root=args.installed_root,
        result_path=args.result,
        no_write=args.no_write,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
