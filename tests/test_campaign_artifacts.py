from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts import campaign_artifacts, install_skills, pack_contract


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
            current = decision_path.read_text("utf-8")
            markers = "".join(
                f"<!-- campaign-decision:{pointer.split('#', 1)[1]} -->\n"
                for pointer in sorted(pointers)
                if (
                    f"<!-- campaign-decision:{pointer.split('#', 1)[1]} -->"
                    not in current
                )
            )
            decision_path.write_text(
                current + markers,
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


def _admission_file(worktree: Path, relative: str, content: str) -> str:
    path = worktree / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))
    return f"sha256-v1:{hashlib.sha256(content.encode()).hexdigest()}"


def _pack_contract_for_admission(
    *,
    ticket: str,
    predecessor_ids: list[str],
    capability_ids: list[str],
    relationship_ids: list[str],
    scenario_ids: list[str],
) -> dict[str, object]:
    draft = pack_contract.create_draft()
    placeholder_scenario_id = "PS-999"
    scenario_owner = (
        predecessor_ids[0]
        if predecessor_ids
        else ("SK-900" if relationship_ids else ticket)
    )
    contract_scenario_ids = scenario_ids or [placeholder_scenario_id]
    header = draft["epoch_header"]
    header.update(  # type: ignore[union-attr]
        {
            "composition_epoch_id": "FCE-20260725-01",
            "contract_revision": 1,
            "fixed_point": {
                "repository_tree": "a" * 40,
                "environment": "test/windows/python-3.12",
                "timestamp": "2026-07-25T00:00:00Z",
            },
            "intended_pack_outcome": "Exercise one Fresh campaign",
            "scope": ["Fresh campaign admission"],
            "exclusions": ["automatic semantic acceptance"],
            "source_pointers": ["issue-44#sha256-v1:" + "d" * 64],
            "acceptance_scenarios": [
                {
                    "scenario_id": scenario_id,
                    "description": f"Exercise {scenario_id}",
                    "expected_owner_skill_id": (
                        ticket if scenario_ids else scenario_owner
                    ),
                }
                for scenario_id in contract_scenario_ids
            ],
            "load_budget_policy": {
                "metric": "runtime instruction class",
                "ceiling_or_class": "conditional",
                "status": "set",
            },
            "campaign_proof_graph": [
                {
                    "predecessor_skill_id": predecessor_id,
                    "successor_skill_id": ticket,
                }
                for predecessor_id in predecessor_ids
            ],
        }
    )

    def selected_skill(
        skill_id: str,
        name: str,
        order: int,
        *,
        owned: list[str] | None = None,
        relationships: list[str] | None = None,
        state: str = "not-started",
    ) -> dict[str, object]:
        return {
            "skill_id": skill_id,
            "canonical_name": name,
            "essential_outcome": f"Complete {name}",
            "primary_role": "leaf",
            "contract_order": order,
            "invocation_mode": "implicit",
            "positive_entry_predicate": f"{name} is needed",
            "negative_exclusion_predicates": [f"{name} is not needed"],
            "owned_authority_mutation_surfaces": [f"{name} local state"],
            "prohibited_ownership": ["foreign semantic decisions"],
            "required_input": f"{name} request",
            "return_packet": f"{name} result",
            "completion_condition": f"{name} complete",
            "failure_return": f"{name} blocked",
            "owned_capability_ids": owned or [],
            "relationship_ids": relationships or [],
            "acceptance_scenario_ids": (
                scenario_ids
                if skill_id == ticket
                else (
                    contract_scenario_ids
                    if not scenario_ids and skill_id == scenario_owner
                    else []
                )
            ),
            "load_budget_class": "conditional",
            "campaign_state": {
                "status": state,
                "campaign_id": (
                    f"{skill_id.lower()}-complete" if state == "terminal" else None
                ),
                "terminal_evidence_pointer": (
                    f"evidence://{skill_id}" if state == "terminal" else None
                ),
            },
        }

    relation_targets = [
        f"SK-{899 + index:03d}"
        for index, _ in enumerate(relationship_ids, start=1)
    ]
    other_ids = [*predecessor_ids, *relation_targets]
    draft["selected_skills"] = [
        *[
            selected_skill(
                predecessor_id,
                predecessor_id.lower(),
                index,
            )
            for index, predecessor_id in enumerate(predecessor_ids, start=1)
        ],
        *[
            selected_skill(
                relation_target,
                relation_target.lower(),
                len(predecessor_ids) + index,
            )
            for index, relation_target in enumerate(relation_targets, start=1)
        ],
        selected_skill(
            ticket,
            "implement",
            len(other_ids) + 1,
            owned=capability_ids,
            relationships=relationship_ids,
        ),
    ]
    draft["capabilities"] = [
        {
            "capability_id": capability_id,
            "essential": True,
            "observable_outcome": f"{capability_id} outcome",
            "entry_conditions": ["A bounded request exists"],
            "completion_return": f"{capability_id} result",
            "required_authority_mutation": ["local owner"],
            "primary_owner_skill_id": ticket,
            "allowed_contributor_skill_ids": [],
            "exclusions": ["foreign ownership"],
            "acceptance_scenario_ids": scenario_ids,
            "proof_class": "structural",
            "disposition": "selected",
        }
        for capability_id in capability_ids
    ]
    draft["relationships"] = [
        {
            "relationship_id": relationship_id,
            "caller_skill_id": ticket,
            "verb": "Invoke",
            "target_skill_id": target_id,
            "entry_condition": "The target result is required",
            "wrong_condition": "The caller can complete locally",
            "input_packet": "bounded request",
            "callee_owned_gates_mutations": ["target local gates"],
            "return_packet": "typed target result",
            "resume_owner_skill_id": ticket,
            "combined_exit_owner_skill_id": ticket,
            "failure_behavior": "return the exact target blocker",
            "context_loaded": ["target interface only"],
            "affected_capability_ids": capability_ids,
            "ordering_impact": "none",
            "required_proof_ids": [f"PROOF-{relationship_id}"],
        }
        for relationship_id, target_id in zip(
            relationship_ids,
            relation_targets,
            strict=True,
        )
    ]
    draft["exclusions_collisions_gaps"] = [
        {
            "issue_id": f"ECG-7{index:02d}",
            "class": collision_class,
            "essential": True,
            "involved_skill_ids": [],
            "involved_capability_ids": [],
            "terms": [],
            "observable_conflict": (
                f"Campaign fixture {collision_class} collision is resolved"
            ),
            "governing_owner": "campaign fixture owner",
            "resolution": "one fixture owner and one explicit boundary",
            "negative_control_scenario_id": contract_scenario_ids[0],
            "status": "resolved",
            "future_owner_or_stopping_condition": None,
            "nondependency_proof_ids": [],
        }
        for index, collision_class in enumerate(
            sorted(pack_contract.REQUIRED_COLLISION_CLASSES),
            start=1,
        )
    ]
    frozen = pack_contract.freeze_contract(draft)
    assert frozen["status"] == "contract-frozen", frozen
    frozen_contract = frozen["contract"]
    for selected in frozen_contract["selected_skills"]:
        if selected["skill_id"] not in predecessor_ids:
            continue
        selected["campaign_state"] = {
            "status": "terminal",
            "campaign_id": f"{selected['skill_id'].lower()}-complete",
            "terminal_evidence_pointer": f"evidence://{selected['skill_id']}",
        }
    return frozen_contract


def valid_fresh_epoch_admission(
    worktree: Path,
    *,
    ticket: str = "T05",
    predecessor_ids: list[str] | None = None,
    include_m0: bool = True,
) -> dict[str, object]:
    selected_predecessor_tickets = (
        ["T04"] if predecessor_ids is None else predecessor_ids
    )
    pack_skill_id = f"SK-{int(ticket.removeprefix('T')):03d}"
    selected_predecessors = [
        f"SK-{int(value.removeprefix('T').removeprefix('SK-')):03d}"
        for value in selected_predecessor_tickets
    ]
    slice_id = f"FCE-20260725-01:r1:{pack_skill_id}:implement"
    selected_capability_ids = ["CAP-005"]
    selected_relationship_ids = ["REL-005"]
    selected_scenario_ids = ["PS-005"]
    pack_path = "docs/synthesis/skill-pack.md"
    slice_path = (
        f"docs/validation/skill-pack/FCE-20260725-01/slices/{ticket}.json"
    )
    schedule_path = "docs/validation/skill-pack/FCE-20260725-01/schedule.json"
    m0_path = "docs/validation/skills/implement/prompt1-m0.md"
    schedule_fingerprint = _admission_file(
        worktree,
        schedule_path,
        json.dumps({ticket: "implement"}, separators=(",", ":")) + "\n",
    )
    proof_predecessors = []
    for predecessor_id in selected_predecessors:
        p1_path = (
            f"docs/validation/skills/{predecessor_id.lower()}/p1.json"
        )
        installed_path = (
            f"docs/validation/skills/{predecessor_id.lower()}/installed.json"
        )
        proof_predecessors.append(
            {
                "id": predecessor_id,
                "p1": {
                    "path": p1_path,
                    "fingerprint": _admission_file(
                        worktree,
                        p1_path,
                        f"{predecessor_id} p1 predecessor\n",
                    ),
                },
                "installed": {
                    "path": installed_path,
                    "fingerprint": _admission_file(
                        worktree,
                        installed_path,
                        f"{predecessor_id} installed predecessor\n",
                    ),
                },
            }
        )
    frozen_pack = _pack_contract_for_admission(
        ticket=pack_skill_id,
        predecessor_ids=selected_predecessors,
        capability_ids=selected_capability_ids,
        relationship_ids=selected_relationship_ids,
        scenario_ids=selected_scenario_ids,
    )
    pack_content = pack_contract.render_contract(frozen_pack)
    admission = {
        "campaign": {
            "composition_epoch_id": "FCE-20260725-01",
            "continuation": None,
            "supersession": None,
        },
        "contract": {
            "pack_contract": {
                "path": pack_path,
                "revision": "1",
                "fingerprint": _admission_file(
                    worktree,
                    pack_path,
                    pack_content,
                ),
            },
            "slice": {
                "id": slice_id,
                "path": slice_path,
                "fingerprint": _admission_file(
                    worktree,
                    slice_path,
                    json.dumps(
                        {
                            "slice_id": slice_id,
                            "selected_capability_ids": selected_capability_ids,
                            "selected_relationship_ids": (
                                selected_relationship_ids
                            ),
                            "selected_scenario_ids": selected_scenario_ids,
                            "hard_proof_predecessor_ids": selected_predecessors,
                        },
                        separators=(",", ":"),
                        sort_keys=True,
                    )
                ),
            },
            "selected_capability_ids": selected_capability_ids,
            "selected_relationship_ids": selected_relationship_ids,
            "selected_scenario_ids": selected_scenario_ids,
            "proof_predecessors": proof_predecessors,
            "schedule_pointer": (
                f"{schedule_path}#{ticket}"
            ),
            "schedule_fingerprint": schedule_fingerprint,
        },
        "semantic": {
            "stage_token": "prompt-1",
            "terminal_token": None,
            "lifecycle": {
                "m0": "pending",
                "research": "pending",
                "h1": "pending",
                "proof": "pending",
                "pruning": "pending",
                "p1": "pending",
            },
            "pointers": {
                "decision_capsule": "decisions.md#prompt-1",
                "m0_checkpoint": m0_path,
                "research_packet": (
                    "docs/research/skills/implement/"
                    "RP-implement-20260725-01.md"
                ),
                "skill_synthesis": "docs/synthesis/skills/implement.md",
                "claim_adjacency": (
                    "docs/synthesis/skills/implement.md#claim-adjacency"
                ),
                "pack_synthesis": "docs/synthesis/skill-pack.md",
            },
        },
    }
    if include_m0:
        _admission_file(
            worktree,
            m0_path,
            "# Prompt 1 M0\n\nFrozen fixture checkpoint.\n",
        )
    return admission


def _sync_slice_projection(
    worktree: Path,
    admission: dict[str, object],
) -> None:
    contract = admission["contract"]  # type: ignore[index]
    slice_identity = contract["slice"]
    slice_payload = json.loads(
        (worktree / slice_identity["path"]).read_text("utf-8")
    )
    ticket = slice_payload["slice_id"].split(":")[2]
    predecessor_ids = [
        predecessor["id"]
        for predecessor in contract["proof_predecessors"]
    ]
    frozen_pack = _pack_contract_for_admission(
        ticket=ticket,
        predecessor_ids=predecessor_ids,
        capability_ids=contract["selected_capability_ids"],
        relationship_ids=contract["selected_relationship_ids"],
        scenario_ids=contract["selected_scenario_ids"],
    )
    pack_identity = contract["pack_contract"]
    pack_identity["fingerprint"] = _admission_file(
        worktree,
        pack_identity["path"],
        pack_contract.render_contract(frozen_pack),
    )
    produced = pack_contract.campaign_admission_slice(frozen_pack, ticket)
    assert produced["status"] == "campaign-admission-slice"
    slice_payload = produced["slice"]
    slice_identity["id"] = slice_payload["slice_id"]
    slice_identity["fingerprint"] = _admission_file(
        worktree,
        slice_identity["path"],
        json.dumps(
            slice_payload,
            separators=(",", ":"),
            sort_keys=True,
        ),
    )


def test_fresh_start_creates_pointer_oriented_v2_manifest_and_firewall(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree, include_m0=False)

    result = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )

    expected = (
        "docs/validation/skills/implement/campaigns/"
        "implement-epoch-1/manifest.json"
    )
    assert result["status"] == "verified"
    assert result["manifest"] == expected
    manifest_path = worktree / expected
    manifest = json.loads(manifest_path.read_text("utf-8"))
    assert manifest["schema_version"] == 2
    assert manifest["campaign"]["composition_epoch_id"] == "FCE-20260725-01"
    assert manifest["contract"] == admission["contract"]
    assert manifest["semantic"] == admission["semantic"]
    assert manifest["mechanical"]["evidence_state"] == "current"
    assert manifest["mechanical"]["campaign_digest"] == (
        campaign_artifacts._campaign_lineage_digest(
            manifest["campaign"],
            manifest["mechanical"]["supersession_digest"],
        )
    )
    lease = json.loads(
        (worktree / campaign_artifacts.LEASE_PATH).read_text("utf-8")
    )
    assert lease["campaign_digest"] == manifest["mechanical"]["campaign_digest"]
    assert lease["supersession_digest"] is None

    for protected in ("campaign", "contract", "semantic"):
        with pytest.raises(ValueError, match=protected):
            campaign_artifacts.update_mechanical_state(
                manifest_path,
                {protected: {}},
            )
    with pytest.raises(ValueError, match="campaign_digest"):
        campaign_artifacts.update_mechanical_state(
            manifest_path,
            {"campaign_digest": "0" * 64},
        )


def test_fresh_prompt1_freezes_m0_only_after_lease_acquisition(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree, include_m0=False)

    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    manifest_path = worktree / str(started["manifest"])
    checkpoint_path = (
        worktree
        / admission["semantic"]["pointers"]["m0_checkpoint"]  # type: ignore[index]
    )

    missing = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_path.write_text(
        "frozen prompt 1 M0\n",
        encoding="utf-8",
        newline="\n",
    )
    frozen = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    manifest = json.loads(manifest_path.read_text("utf-8"))
    checkpoint_path.write_text(
        "drifted prompt 1 M0\n",
        encoding="utf-8",
        newline="\n",
    )
    drifted = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert missing["status"] == "failed"
    assert missing["gate"] == "m0-checkpoint"
    assert frozen["status"] == "verified"
    assert manifest["mechanical"]["artifact_identities"] == [
        {
            "fingerprint": (
                "sha256-v1:"
                + hashlib.sha256(b"frozen prompt 1 M0\n").hexdigest()
            ),
            "name": "prompt-1-m0",
            "path": checkpoint_path.relative_to(worktree).as_posix(),
        }
    ]
    assert drifted["status"] == "stale"
    assert drifted["gate"] == "m0-checkpoint"


def test_fresh_start_accepts_semantic_pack_revision_in_git_worktree(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    _git(worktree, "init", "--quiet")
    admission = valid_fresh_epoch_admission(worktree)

    result = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-git-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )

    assert result["status"] == "verified"
    assert (worktree / str(result["manifest"])).exists()


def test_fresh_git_worktree_still_rejects_pack_fingerprint_drift(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    _git(worktree, "init", "--quiet")
    admission = valid_fresh_epoch_admission(worktree)
    pack_path = worktree / admission["contract"]["pack_contract"]["path"]  # type: ignore[index]
    pack_path.write_text("drifted pack contract\n", encoding="utf-8")

    with pytest.raises(ValueError, match="pack_contract fingerprint"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-git-epoch-1",
            owner_token="owner-a",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_requires_canonical_pack_contract_owner_before_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    foreign_path = "docs/synthesis/foreign-pack.md"
    admission["contract"]["pack_contract"]["path"] = foreign_path  # type: ignore[index]
    admission["contract"]["pack_contract"]["fingerprint"] = _admission_file(  # type: ignore[index]
        worktree,
        foreign_path,
        "foreign pack contract\n",
    )
    admission["semantic"]["pointers"]["pack_synthesis"] = foreign_path  # type: ignore[index]

    with pytest.raises(ValueError, match="canonical Pack Contract"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_requires_prompt1_m0_owner_before_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["semantic"]["pointers"]["m0_checkpoint"] = (  # type: ignore[index]
        "docs/validation/skills/review/prompt1-m0.md"
    )

    with pytest.raises(ValueError, match="m0_checkpoint.*wrong owner"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            owner_token="owner-a",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    ("canonical_name", "accepted"),
    [("implement", True), ("review", False)],
)
def test_fresh_start_consumes_pack_owned_canonical_slice_envelope(
    tmp_path: Path,
    canonical_name: str,
    accepted: bool,
) -> None:
    worktree = tmp_path / canonical_name
    worktree.mkdir()
    fixture = (
        Path(__file__).parents[1]
        / "docs/validation/shared/fixtures/"
        "pack-composition-contract-v1/contract.json"
    )
    draft = json.loads(fixture.read_text("utf-8"))
    draft["epoch_header"]["composition_epoch_id"] = "FCE-20260725-01"
    draft["selected_skills"][0]["canonical_name"] = canonical_name
    frozen = pack_contract.freeze_contract(draft)
    assert frozen["status"] == "contract-frozen"
    envelope = pack_contract.campaign_admission_slice(
        frozen["contract"],
        "SK-001",
    )
    assert envelope["status"] == "campaign-admission-slice"
    admission = valid_fresh_epoch_admission(
        worktree,
        ticket="T01",
        predecessor_ids=[],
    )
    contract = admission["contract"]  # type: ignore[assignment]
    contract["pack_contract"]["revision"] = "1"
    contract["pack_contract"]["fingerprint"] = _admission_file(
        worktree,
        contract["pack_contract"]["path"],
        pack_contract.render_contract(frozen["contract"]),
    )
    projected = envelope["slice"]
    for field in (
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
    ):
        contract[field] = projected[field]
    slice_identity = contract["slice"]
    slice_identity["id"] = projected["slice_id"]
    slice_identity["fingerprint"] = _admission_file(
        worktree,
        slice_identity["path"],
        json.dumps(projected, separators=(",", ":"), sort_keys=True),
    )

    if accepted:
        result = campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-canonical-slice",
            owner_token="owner-a",
            fresh_epoch=admission,
        )
        assert result["status"] == "verified"
    else:
        with pytest.raises(ValueError, match="selected skill"):
            campaign_artifacts.start_campaign(
                "implement",
                worktree=worktree,
                campaign_id="implement-wrong-slice",
                owner_token="owner-a",
                fresh_epoch=admission,
            )
        assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_rejects_self_consistent_slice_not_derived_from_pack(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(
        worktree,
        ticket="T01",
        predecessor_ids=[],
    )
    slice_path = worktree / admission["contract"]["slice"]["path"]  # type: ignore[index]
    projected = json.loads(slice_path.read_text("utf-8"))
    projected["selected_capability_ids"] = ["CAP-forged"]
    admission["contract"]["selected_capability_ids"] = ["CAP-forged"]  # type: ignore[index]
    admission["contract"]["slice"]["fingerprint"] = _admission_file(  # type: ignore[index]
        worktree,
        admission["contract"]["slice"]["path"],  # type: ignore[index]
        json.dumps(projected, separators=(",", ":"), sort_keys=True),
    )

    with pytest.raises(ValueError, match="derived from the Pack Contract"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-forged-slice",
            owner_token="owner-a",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_root_start_accepts_explicitly_empty_proof_predecessors(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(
        worktree,
        ticket="T01",
        predecessor_ids=[],
    )

    result = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-root-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )

    assert result["status"] == "verified"
    manifest_path = worktree / str(result["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    assert manifest["contract"]["proof_predecessors"] == []
    assert (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    ("continuation", "supersession"),
    [
        ("restart", "docs/validation/skills/implement/campaigns/missing/manifest.json"),
        (None, "docs/validation/skills/implement/campaigns/missing/manifest.json"),
        ("repair", None),
    ],
)
def test_ordinary_fresh_start_rejects_forged_continuation_before_lease(
    tmp_path: Path,
    continuation: str | None,
    supersession: str | None,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["campaign"]["continuation"] = continuation  # type: ignore[index]
    admission["campaign"]["supersession"] = supersession  # type: ignore[index]

    with pytest.raises(ValueError, match="ordinary Fresh start"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-forged-continuation",
            owner_token="owner-a",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    "field",
    [
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
    ],
)
def test_fresh_start_accepts_authoritative_empty_selected_sets(
    tmp_path: Path,
    field: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["contract"][field] = []  # type: ignore[index]
    _sync_slice_projection(worktree, admission)

    result = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id=f"implement-empty-{field.replace('_', '-')}",
        owner_token="owner-a",
        fresh_epoch=admission,
    )

    assert result["status"] == "verified"
    manifest = json.loads(
        (worktree / str(result["manifest"])).read_text("utf-8")
    )
    assert manifest["contract"][field] == []


@pytest.mark.parametrize("case", ["omitted", "extra", "duplicate", "mismatch"])
def test_fresh_start_refuses_predecessor_set_drift_before_lease(
    tmp_path: Path,
    case: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    predecessors = admission["contract"]["proof_predecessors"]  # type: ignore[index]
    if case == "omitted":
        predecessors.clear()
    elif case == "extra":
        predecessors.append(
            {
                "id": "T03",
                "p1": {
                    "path": "docs/validation/skills/t03/p1.json",
                    "fingerprint": _admission_file(
                        worktree,
                        "docs/validation/skills/t03/p1.json",
                        "T03 p1 predecessor\n",
                    ),
                },
                "installed": {
                    "path": "docs/validation/skills/t03/installed.json",
                    "fingerprint": _admission_file(
                        worktree,
                        "docs/validation/skills/t03/installed.json",
                        "T03 installed predecessor\n",
                    ),
                },
            }
        )
        predecessors.sort(key=lambda predecessor: predecessor["id"])
    elif case == "duplicate":
        predecessors.append(json.loads(json.dumps(predecessors[0])))
    else:
        predecessors[0]["id"] = "T03"

    with pytest.raises(ValueError, match="predecessor"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    "field",
    [
        "selected_capability_ids",
        "selected_relationship_ids",
        "selected_scenario_ids",
    ],
)
def test_fresh_start_refuses_selected_set_drift_from_slice_before_lease(
    tmp_path: Path,
    field: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["contract"][field] = [f"{field}-foreign"]  # type: ignore[index]

    with pytest.raises(ValueError, match="frozen slice"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_refuses_cross_graph_slice_identity_before_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["contract"]["slice"]["id"] = (  # type: ignore[index]
        "OTHER-GRAPH:T05"
    )

    with pytest.raises(ValueError, match="slice ID"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    "schedule_content",
    [
        '{"note":"T05"}\n',
        '{"T050":"implement"}\n',
    ],
)
def test_fresh_start_requires_exact_schedule_fragment_before_lease(
    tmp_path: Path,
    schedule_content: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    contract = admission["contract"]  # type: ignore[assignment]
    schedule_path = str(contract["schedule_pointer"]).split("#", 1)[0]
    contract["schedule_fingerprint"] = _admission_file(
        worktree,
        schedule_path,
        schedule_content,
    )

    with pytest.raises(ValueError, match="schedule fragment"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_refuses_incomplete_admission_before_acquiring_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    del admission["contract"]["slice"]  # type: ignore[index]

    with pytest.raises(ValueError, match="slice"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_start_resolves_admitted_identity_before_acquiring_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    slice_path = worktree / admission["contract"]["slice"]["path"]  # type: ignore[index]
    slice_path.write_text('{"ticket":"drifted"}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="slice fingerprint"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


@pytest.mark.parametrize(
    ("pointer", "value"),
    [
        (
            "research_packet",
            "docs/research/skills/implement/../other.md",
        ),
        (
            "research_packet",
            r"docs\research\skills\implement\packet.md",
        ),
        (
            "claim_adjacency",
            "docs/synthesis/skills/implement.md#../claim-adjacency",
        ),
    ],
)
def test_fresh_start_refuses_noncanonical_semantic_pointer_before_lease(
    tmp_path: Path,
    pointer: str,
    value: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["semantic"]["pointers"][pointer] = value  # type: ignore[index]

    with pytest.raises(ValueError, match="pointer|canonical|owner"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-1",
            fresh_epoch=admission,
        )

    assert not (worktree / campaign_artifacts.LEASE_PATH).exists()


def test_fresh_verify_reads_owner_tokens_without_advancing_lifecycle(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    semantic_before = json.loads(manifest_path.read_text("utf-8"))["semantic"]

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["stage"] == "prompt-1"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    assert manifest["semantic"] == semantic_before
    assert manifest["mechanical"]["verified_at"].endswith("Z")


def test_fresh_verify_detects_live_contract_drift_and_returns_owner(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    slice_path = worktree / admission["contract"]["slice"]["path"]  # type: ignore[index]
    slice_path.write_text('{"ticket":"drifted"}\n', encoding="utf-8")

    result = campaign_artifacts.verify_campaign(
        worktree / str(started["manifest"]),
        worktree=worktree,
    )

    assert result["status"] == "stale"
    assert result["gate"] == "contract-drift"
    assert result["changed_contract_fields"] == ["slice.fingerprint"]
    assert result["owner_action_required"] == ["resume", "repair", "restart"]
    resumed = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        owner_token="owner-a",
        continuation="resume",
        from_manifest=worktree / str(started["manifest"]),
    )
    assert resumed["status"] == "failed"
    assert resumed["gate"] == "continuation"


def test_fresh_verify_detects_direct_contract_identity_rewrite(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["contract"]["pack_contract"]["revision"] = "fabricated"
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "stale"
    assert result["gate"] == "contract-drift"
    assert result["changed_contract_fields"] == ["contract.digest"]


def _complete_fresh_lifecycle(manifest: dict[str, object]) -> None:
    manifest["semantic"]["lifecycle"] = {  # type: ignore[index]
        "m0": "ready-for-research",
        "research": "research-complete",
        "h1": "ready-for-prompt-3",
        "proof": "accepted",
        "pruning": "complete",
        "p1": "promoted-installed",
    }


def _write_fresh_semantic_artifacts(
    worktree: Path,
    manifest: dict[str, object],
    *,
    claim_adjacency: bool = True,
) -> tuple[Path, Path]:
    pointers = manifest["semantic"]["pointers"]  # type: ignore[index]
    research = worktree / pointers["research_packet"]
    research.parent.mkdir(parents=True, exist_ok=True)
    research.write_text("# Research Packet\n", encoding="utf-8")
    synthesis = worktree / pointers["skill_synthesis"]
    synthesis.parent.mkdir(parents=True, exist_ok=True)
    synthesis.write_text(
        "# Implement Synthesis\n"
        + ("## Claim Adjacency\n" if claim_adjacency else "## Evidence\n"),
        encoding="utf-8",
    )
    return research, synthesis


def test_fresh_terminal_is_prompt5_post_install_only(tmp_path: Path) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    assert campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["terminal_token"] = "campaign-complete"
    write_json(manifest_path, manifest)

    wrong_stage = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert wrong_stage["status"] == "failed"
    assert wrong_stage["gate"] == "semantic-terminal"

    manifest["semantic"]["stage_token"] = "prompt-5"
    _complete_fresh_lifecycle(manifest)
    _write_fresh_semantic_artifacts(worktree, manifest)
    decisions_path = manifest_path.parent / "decisions.md"
    decisions_path.write_text(
        decisions_path.read_text("utf-8")
        + "<!-- campaign-decision:prompt-1 -->\n",
        encoding="utf-8",
    )
    manifest["mechanical"]["preflight_registrations"] = [
        {
            "kind": "installation",
            "stage": "prompt-5",
            "state": "plan",
        }
    ]
    write_json(manifest_path, manifest)
    planned_only = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert planned_only["status"] == "stale"
    assert planned_only["gate"] == "semantic-terminal"
    assert "post-install" in str(planned_only["message"])


def test_fresh_terminal_binds_installer_identity_to_campaign_skill(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "implement", "runtime")
    install_skills.install(worktree, installed, None)
    admission = valid_fresh_epoch_admission(worktree)
    admission["contract"]["selected_relationship_ids"] = [  # type: ignore[index]
        "REL-005",
        "REL-006",
    ]
    admission["contract"]["selected_scenario_ids"] = [  # type: ignore[index]
        "PS-005",
        "PS-006",
    ]
    _sync_slice_projection(worktree, admission)
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    manifest_path = worktree / str(started["manifest"])
    assert campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )["status"] == "verified"
    manifest = json.loads(manifest_path.read_text("utf-8"))
    research_path, synthesis_path = _write_fresh_semantic_artifacts(
        worktree,
        manifest,
    )
    decisions_path = manifest_path.parent / "decisions.md"
    decisions_path.write_text(
        decisions_path.read_text("utf-8")
        + "<!-- campaign-decision:prompt-1 -->\n",
        encoding="utf-8",
    )
    digest = install_skills.skill_tree_hash(
        worktree / "skills" / "custom" / "implement"
    )
    fingerprint = f"sha256-v1:{digest}"
    manifest["semantic"]["terminal_token"] = "campaign-complete"
    manifest["semantic"]["stage_token"] = "prompt-5"
    _complete_fresh_lifecycle(manifest)
    manifest["mechanical"]["preflight_registrations"] = [
        _installation_preflight(
            worktree,
            installed,
            ["implement"],
            state="post-install",
        )
    ]
    manifest["mechanical"]["artifact_identities"] = [
        manifest["mechanical"]["artifact_identities"][0],
        {"name": "canonical-p1", "fingerprint": fingerprint},
        {"name": "installed-p1", "fingerprint": fingerprint},
    ]
    manifest["mechanical"]["parity"] = {
        "canonical_installed": "match",
        "relationship_ids": manifest["contract"]["selected_relationship_ids"],
    }
    write_json(manifest_path, manifest)

    missing_proof = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert missing_proof["status"] == "stale"
    assert missing_proof["gate"] == "semantic-terminal"
    assert "proof" in str(missing_proof["message"])

    target = worktree / "target"
    target.mkdir()
    (target / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["fresh_epoch_identity"] = {
        "composition_epoch_id": manifest["campaign"]["composition_epoch_id"],
        "pack_contract_revision": manifest["contract"]["pack_contract"][
            "revision"
        ],
        "slice_fingerprint": manifest["contract"]["slice"]["fingerprint"],
        "relationship_ids": manifest["contract"]["selected_relationship_ids"],
        "scenario_ids": manifest["contract"]["selected_scenario_ids"],
    }
    manifest["mechanical"]["proof_registrations"] = [registration]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(b"terminal-proof").hexdigest(),
            source="execution",
            receipt_id="receipt-terminal-unstaged",
        )
    ]
    write_json(manifest_path, manifest)

    unstaged = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert unstaged["status"] == "stale"
    assert unstaged["gate"] == "semantic-terminal"
    assert "current required proof" in str(unstaged["message"])

    registration["stage"] = "prompt-4"
    manifest["mechanical"]["proof_registrations"] = [registration]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(b"terminal-proof").hexdigest(),
            source="execution",
            receipt_id="receipt-terminal",
        )
    ]
    write_json(manifest_path, manifest)

    off_stage = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert off_stage["status"] == "stale"
    assert off_stage["gate"] == "semantic-terminal"
    assert "current required proof" in str(off_stage["message"])

    registration["stage"] = "prompt-5"
    write_json(manifest_path, manifest)
    wrong_stage_receipt = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert wrong_stage_receipt["status"] in {"failed", "stale"}
    assert wrong_stage_receipt["gate"] == "proof-receipt"

    registration["fresh_epoch_identity"]["relationship_ids"] = [  # type: ignore[index]
        "REL-005"
    ]
    registration["fresh_epoch_identity"]["scenario_ids"] = [  # type: ignore[index]
        "PS-005"
    ]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(b"terminal-proof").hexdigest(),
            source="execution",
            receipt_id="receipt-terminal-subset",
        )
    ]
    write_json(manifest_path, manifest)
    incomplete_coverage = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert incomplete_coverage["status"] == "stale"
    assert incomplete_coverage["gate"] == "semantic-terminal"
    assert "relationship and scenario coverage" in str(
        incomplete_coverage["message"]
    )

    registration["fresh_epoch_identity"]["relationship_ids"] = manifest[  # type: ignore[index]
        "contract"
    ]["selected_relationship_ids"]
    registration["fresh_epoch_identity"]["scenario_ids"] = manifest[  # type: ignore[index]
        "contract"
    ]["selected_scenario_ids"]
    manifest["mechanical"]["receipts"] = [
        campaign_artifacts.make_receipt(
            registration,
            campaign_artifacts.proof_identity_tuple(
                registration,
                candidate_root=worktree,
            ),
            exit_code=0,
            output_digest=hashlib.sha256(b"terminal-proof").hexdigest(),
            source="execution",
            receipt_id="receipt-terminal",
        )
    ]
    write_json(manifest_path, manifest)

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["terminal"] == "campaign-complete"

    research_path.unlink()
    missing_research = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert missing_research["status"] == "stale"
    assert missing_research["gate"] == "semantic-terminal"
    _write_fresh_semantic_artifacts(worktree, manifest)

    synthesis_path.unlink()
    missing_synthesis = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert missing_synthesis["status"] == "stale"
    assert missing_synthesis["gate"] == "semantic-terminal"
    _write_fresh_semantic_artifacts(
        worktree,
        manifest,
        claim_adjacency=False,
    )

    missing_adjacency = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert missing_adjacency["status"] == "stale"
    assert missing_adjacency["gate"] == "semantic-terminal"
    _write_fresh_semantic_artifacts(worktree, manifest)

    restored = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert restored["status"] == "verified"

    original_pointers = json.loads(
        json.dumps(manifest["semantic"]["pointers"])
    )
    foreign_research = worktree / "docs/research/skills/other/packet.md"
    foreign_research.parent.mkdir(parents=True, exist_ok=True)
    foreign_research.write_text("# Foreign Research\n", encoding="utf-8")
    foreign_synthesis = worktree / "docs/synthesis/skills/other.md"
    foreign_synthesis.parent.mkdir(parents=True, exist_ok=True)
    foreign_synthesis.write_text(
        "# Other\n## Claim Adjacency\n",
        encoding="utf-8",
    )
    manifest["semantic"]["pointers"].update(  # type: ignore[index]
        {
            "research_packet": (
                "docs/research/skills/other/packet.md"
            ),
            "skill_synthesis": "docs/synthesis/skills/other.md",
            "claim_adjacency": (
                "docs/synthesis/skills/other.md#claim-adjacency"
            ),
        }
    )
    write_json(manifest_path, manifest)
    foreign_owner = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert foreign_owner["status"] == "stale"
    assert foreign_owner["gate"] == "semantic-terminal"

    manifest["semantic"]["pointers"] = json.loads(  # type: ignore[index]
        json.dumps(original_pointers)
    )
    manifest["semantic"]["pointers"]["decision_capsule"] = (  # type: ignore[index]
        "decisions.md#missing-decision"
    )
    write_json(manifest_path, manifest)
    missing_decision = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert missing_decision["status"] == "stale"
    assert missing_decision["gate"] == "semantic-terminal"

    manifest["semantic"]["pointers"] = json.loads(  # type: ignore[index]
        json.dumps(original_pointers)
    )
    manifest["semantic"]["pointers"]["pack_synthesis"] = (  # type: ignore[index]
        "docs/synthesis/missing-pack.md"
    )
    write_json(manifest_path, manifest)
    missing_pack = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert missing_pack["status"] == "stale"
    assert missing_pack["gate"] == "semantic-terminal"

    manifest["semantic"]["pointers"] = original_pointers  # type: ignore[index]
    write_json(manifest_path, manifest)
    owner_restored = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert owner_restored["status"] == "verified"


def test_campaign_reader_preserves_historical_v1_without_upgrade(
    tmp_path: Path,
) -> None:
    path = tmp_path / "manifest.json"
    legacy = {
        "campaign": {
            "id": "legacy-v1-compatibility-fixture",
            "skill": "example",
        },
        "mechanical": {"evidence_state": "historical-read-only"},
        "schema_version": 1,
    }
    write_json(path, legacy)
    before = path.read_bytes()

    result = campaign_artifacts.read_campaign_manifest(path)

    assert result == legacy
    assert path.read_bytes() == before
    assert "contract" not in result
    assert "semantic" not in result


def test_campaign_reader_preserves_compact_historical_manifest_without_upgrade(
    tmp_path: Path,
) -> None:
    path = tmp_path / "manifest.json"
    historical = {
        "schema": {
            "name": "deploy-campaign-final-manifest",
            "version": 5,
            "profile": "compact-prompt5-final",
        },
        "campaign": {
            "skill": "to-tickets",
            "epoch": "2026-07-25",
            "status": "complete",
        },
        "runtime_identities": {
            "tree_algorithm": "campaign-tree-v1",
            "v1": {
                "tree_sha256": "4" * 64,
                "identity_relationship": "equals-m0-and-final-h1",
            },
        },
    }
    write_json(path, historical)
    before = path.read_bytes()

    result = campaign_artifacts.read_campaign_manifest(path)

    assert result == historical
    assert path.read_bytes() == before
    assert result["runtime_identities"]["tree_algorithm"] == "campaign-tree-v1"
    assert "schema_version" not in result


def test_campaign_reader_rejects_malformed_compact_historical_manifest(
    tmp_path: Path,
) -> None:
    path = tmp_path / "manifest.json"
    historical = {
        "schema": {
            "name": "deploy-campaign-final-manifest",
            "version": 5,
        },
        "campaign": {
            "skill": "to-tickets",
            "epoch": "2026-07-25",
        },
        "runtime_identities": {"tree_algorithm": "invented-v2"},
    }
    write_json(path, historical)

    with pytest.raises(
        ValueError,
        match="Compact historical campaign manifest is malformed",
    ):
        campaign_artifacts.read_campaign_manifest(path)


def test_fresh_contract_drift_stales_receipts_and_returns_owner_choice(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["mechanical"]["receipts"] = [
        {
            "id": "receipt-a",
            "fresh_epoch_identity": {
                "composition_epoch_id": "FCE-20260725-01"
            },
        },
        {"id": "receipt-unrelated"},
    ]
    write_json(manifest_path, manifest)
    observed = json.loads(json.dumps(admission["contract"]))
    observed["slice"]["fingerprint"] = f"sha256-v1:{'9' * 64}"

    result = campaign_artifacts.check_fresh_contract(
        manifest_path,
        observed,
    )

    assert result["status"] == "stale"
    assert result["owner_action_required"] == [
        "resume",
        "repair",
        "restart",
    ]
    assert result["changed_contract_fields"] == ["slice.fingerprint"]
    updated = json.loads(manifest_path.read_text("utf-8"))
    assert updated["contract"] == admission["contract"]
    assert updated["semantic"] == admission["semantic"]
    assert updated["mechanical"]["evidence_state"] == "stale"
    assert updated["mechanical"]["invalidations"][-1]["receipt_ids"] == [
        "receipt-a"
    ]


def test_relationship_drift_stales_only_receipts_for_changed_edge(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    admission["contract"]["selected_relationship_ids"] = [  # type: ignore[index]
        "REL-005",
        "REL-006",
    ]
    _sync_slice_projection(worktree, admission)
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["mechanical"]["receipts"] = [
        {
            "id": "receipt-review",
            "fresh_epoch_identity": {
                "relationship_ids": ["REL-006"]
            },
        },
        {
            "id": "receipt-tdd",
            "fresh_epoch_identity": {
                "relationship_ids": ["REL-005"]
            },
        },
    ]
    write_json(manifest_path, manifest)
    observed = json.loads(json.dumps(admission["contract"]))
    observed["selected_relationship_ids"] = ["REL-005"]

    result = campaign_artifacts.check_fresh_contract(
        manifest_path,
        observed,
    )

    assert result["stale_receipts"] == ["receipt-review"]


def test_fresh_resume_repair_and_restart_remain_distinct(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    admission = valid_fresh_epoch_admission(worktree)
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=admission,
    )
    manifest_path = worktree / str(started["manifest"])
    before = manifest_path.read_bytes()

    resumed = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        owner_token="owner-a",
        continuation="resume",
        from_manifest=manifest_path,
    )
    after_resume = manifest_path.read_bytes()
    repaired = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        owner_token="owner-a",
        continuation="repair",
        from_manifest=manifest_path,
        changed_inputs=["slice.fingerprint"],
    )

    assert resumed["status"] == "verified"
    assert after_resume == before
    assert before != manifest_path.read_bytes()
    assert repaired["status"] == "stale"

    terminal = json.loads(manifest_path.read_text("utf-8"))
    terminal["semantic"]["terminal_token"] = "campaign-complete"
    terminal["semantic"]["stage_token"] = "prompt-5"
    terminal["semantic"]["lifecycle"]["p1"] = "promoted-installed"
    write_json(manifest_path, terminal)
    next_admission = valid_fresh_epoch_admission(worktree)
    next_admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
    next_admission["campaign"]["supersession"] = str(  # type: ignore[index]
        manifest_path.relative_to(worktree)
    ).replace("\\", "/")

    restarted = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-2",
        owner_token="owner-a",
        continuation="restart",
        from_manifest=manifest_path,
        fresh_epoch=next_admission,
    )

    assert restarted["status"] == "verified"
    new_manifest = json.loads(
        (worktree / str(restarted["manifest"])).read_text("utf-8")
    )
    assert new_manifest["campaign"]["continuation"] == "restart"
    assert new_manifest["campaign"]["supersession"] == str(
        manifest_path.relative_to(worktree)
    ).replace("\\", "/")


def test_fresh_restart_accepts_changed_contract_identity_while_nonterminal(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    next_admission = valid_fresh_epoch_admission(worktree)
    next_admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
    next_admission["campaign"]["supersession"] = str(  # type: ignore[index]
        manifest_path.relative_to(worktree)
    ).replace("\\", "/")
    contract = next_admission["contract"]  # type: ignore[assignment]
    contract["schedule_fingerprint"] = _admission_file(
        worktree,
        str(contract["schedule_pointer"]).split("#", 1)[0],
        '{"T05":"implement","revision":2}\n',
    )

    not_resumed = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        owner_token="owner-a",
        continuation="resume",
        from_manifest=manifest_path,
        fresh_epoch=next_admission,
    )
    restarted = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-2",
        owner_token="owner-a",
        continuation="restart",
        from_manifest=manifest_path,
        fresh_epoch=next_admission,
    )

    assert not_resumed["status"] == "failed"
    assert not_resumed["gate"] == "continuation"
    assert restarted["status"] == "verified"
    assert restarted["campaign_id"] == "implement-epoch-2"


@pytest.mark.parametrize(
    "supersession",
    [
        None,
        "docs/validation/skills/implement/campaigns/missing/manifest.json",
        "docs/validation/skills/other/campaigns/implement-epoch-1/manifest.json",
    ],
)
def test_fresh_restart_rejects_nonexact_source_supersession(
    tmp_path: Path,
    supersession: str | None,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    admission = valid_fresh_epoch_admission(worktree)
    admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
    admission["campaign"]["supersession"] = supersession  # type: ignore[index]

    result = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-2",
        owner_token="owner-a",
        continuation="restart",
        from_manifest=manifest_path,
        fresh_epoch=admission,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "continuation"
    assert not (
        worktree
        / "docs/validation/skills/implement/campaigns/implement-epoch-2"
    ).exists()

def test_direct_restart_handoff_requires_authenticated_source_and_preserves_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    source_manifest = worktree / str(started["manifest"])
    source_pointer = source_manifest.relative_to(worktree).as_posix()
    admission = valid_fresh_epoch_admission(worktree)
    admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
    admission["campaign"]["supersession"] = source_pointer  # type: ignore[index]
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_bytes = lease_path.read_bytes()
    held_lease = json.loads(lease_bytes)

    with pytest.raises(ValueError, match="authenticated source"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-2",
            owner_token="owner-a",
            fresh_epoch=admission,
            _supersedes=source_pointer,
            _held_lease=held_lease,
        )

    assert lease_path.read_bytes() == lease_bytes
    assert not (
        worktree
        / "docs/validation/skills/implement/campaigns/implement-epoch-2"
    ).exists()

    with pytest.raises(ValueError, match="changed identity"):
        campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-epoch-2",
            owner_token="owner-a",
            fresh_epoch=admission,
            _supersedes=source_pointer,
            _held_lease=held_lease,
            _restart_source=source_manifest,
        )

    assert lease_path.read_bytes() == lease_bytes
    assert not (
        worktree
        / "docs/validation/skills/implement/campaigns/implement-epoch-2"
    ).exists()


@pytest.mark.parametrize("authorized_change", ["terminal-source", "delivery-mode"])
def test_v2_restart_handoff_requires_new_fresh_admission_before_mutation(
    tmp_path: Path,
    authorized_change: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    source_manifest = worktree / str(started["manifest"])
    source_pointer = source_manifest.relative_to(worktree).as_posix()
    if authorized_change == "terminal-source":
        source = json.loads(source_manifest.read_text("utf-8"))
        source["semantic"]["terminal_token"] = "campaign-complete"
        write_json(source_manifest, source)
    delivery_mode = "commit" if authorized_change == "delivery-mode" else "none"
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_bytes = lease_path.read_bytes()

    with pytest.raises(ValueError, match="new Fresh admission"):
        campaign_artifacts.start_campaign(
            "implement",
            delivery_mode,
            worktree=worktree,
            campaign_id="implement-epoch-2",
            owner_token="owner-a",
            fresh_epoch=None,
            _supersedes=source_pointer,
            _held_lease=json.loads(lease_bytes),
            _restart_source=source_manifest,
        )

    assert lease_path.read_bytes() == lease_bytes
    assert not (
        worktree
        / "docs/validation/campaigns/implement-epoch-2"
    ).exists()
    assert not (
        worktree
        / "docs/validation/skills/implement/campaigns/implement-epoch-2"
    ).exists()


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


def test_historical_v1_verify_and_repair_are_read_only_without_live_lease(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        campaign_id="review-historical-v1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["semantic"]["declared_stage"] = "prompt-1"
    write_json(manifest_path, manifest)
    active = campaign_artifacts.update_mechanical_state(
        manifest_path,
        {"evidence_state": "current"},
    )
    assert active["mechanical"]["evidence_state"] == "current"
    before = manifest_path.read_bytes()
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_bytes = lease_path.read_bytes()
    lease_path.unlink()

    verified = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    repaired = campaign_artifacts.start_campaign(
        "review",
        worktree=worktree,
        owner_token="owner-a",
        continuation="repair",
        from_manifest=manifest_path,
        changed_inputs=["runtime:m0"],
    )
    with pytest.raises(ValueError, match="exact live lease"):
        campaign_artifacts.update_mechanical_state(
            manifest_path,
            {"evidence_state": "stale"},
        )

    assert verified["status"] == "failed"
    assert verified["gate"] == "lease"
    assert repaired["status"] == "failed"
    assert repaired["gate"] == "continuation"
    assert manifest_path.read_bytes() == before
    assert json.loads(before)["schema_version"] == 1
    lease_path.write_bytes(lease_bytes)
    restored = campaign_artifacts.update_mechanical_state(
        manifest_path,
        {"evidence_state": "stale"},
    )
    assert restored["mechanical"]["evidence_state"] == "stale"


@pytest.mark.parametrize("lease_state", ["absent", "foreign", "noncanonical"])
def test_fresh_mechanical_update_requires_exact_live_lease_and_path(
    tmp_path: Path,
    lease_state: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    active = campaign_artifacts.update_mechanical_state(
        manifest_path,
        {"verified_at": "2026-07-26T00:00:00Z"},
    )
    assert active["mechanical"]["verified_at"] == "2026-07-26T00:00:00Z"
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_bytes = lease_path.read_bytes()
    target = manifest_path
    if lease_state == "absent":
        lease_path.unlink()
    elif lease_state == "foreign":
        foreign_lease = json.loads(lease_bytes)
        foreign_lease["campaign_id"] = "foreign-epoch"
        write_json(lease_path, foreign_lease)
    else:
        target = manifest_path.parent / "copied-manifest.json"
        target.write_bytes(manifest_path.read_bytes())
    before = target.read_bytes()

    with pytest.raises(ValueError, match="exact live lease"):
        campaign_artifacts.update_mechanical_state(
            target,
            {"verified_at": "2026-07-27T00:00:00Z"},
        )

    assert target.read_bytes() == before
    lease_path.write_bytes(lease_bytes)
    restored = campaign_artifacts.update_mechanical_state(
        manifest_path,
        {"verified_at": "2026-07-28T00:00:00Z"},
    )
    assert restored["mechanical"]["verified_at"] == "2026-07-28T00:00:00Z"


@pytest.mark.parametrize(
    ("campaign_id", "worktree_value"),
    [
        ("../escaped", None),
        ("review-epoch-1", "noncanonical"),
    ],
)
def test_v1_mechanical_update_rejects_noncanonical_identity(
    tmp_path: Path,
    campaign_id: str,
    worktree_value: str | None,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    manifest_path = worktree / "outside" / "manifest.json"
    manifest_path.parent.mkdir()
    manifest = {
        "schema_version": 1,
        "campaign": {
            "id": campaign_id,
            "skill": "review",
            "delivery_mode": "none",
            "worktree": (
                str(worktree) + "\\."
                if worktree_value == "noncanonical"
                else str(worktree)
            ),
            "supersedes": None,
        },
        "semantic": {},
        "mechanical": {},
    }
    write_json(manifest_path, manifest)
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_path.parent.mkdir(parents=True)
    write_json(
        lease_path,
        {
            "worktree": str(worktree),
            "campaign_id": campaign_id,
            "owner_token": "owner-a",
        },
    )
    before = manifest_path.read_bytes()

    with pytest.raises(ValueError, match="identity"):
        campaign_artifacts.update_mechanical_state(
            manifest_path,
            {"evidence_state": "stale"},
        )

    assert manifest_path.read_bytes() == before


def test_v2_mechanical_update_rejects_malformed_invalidation_before_write(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    before = manifest_path.read_bytes()

    with pytest.raises(ValueError, match="invalidations"):
        campaign_artifacts.update_mechanical_state(
            manifest_path,
            {
                "invalidations": [
                    {
                        "receipt_ids": "receipt-a",
                        "observed_at": "2026-07-26T00:00:00Z",
                    }
                ]
            },
        )

    assert manifest_path.read_bytes() == before


@pytest.mark.parametrize("operation", ["verify", "resume", "repair", "restart", "release"])
def test_empty_owner_token_fails_closed_before_campaign_mutation(
    tmp_path: Path,
    operation: str,
) -> None:
    worktree = tmp_path / operation
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease = json.loads(lease_path.read_text("utf-8"))
    lease["owner_token"] = ""
    write_json(lease_path, lease)
    manifest_before = manifest_path.read_bytes()
    lease_before = lease_path.read_bytes()

    if operation == "verify":
        result = campaign_artifacts.verify_campaign(
            manifest_path,
            worktree=worktree,
        )
    elif operation == "release":
        result = campaign_artifacts.release_campaign(
            manifest_path,
            worktree=worktree,
            owner_token="",
        )
    else:
        kwargs: dict[str, object] = {
            "worktree": worktree,
            "owner_token": "",
            "continuation": operation,
            "from_manifest": manifest_path,
        }
        if operation == "repair":
            kwargs["changed_inputs"] = ["slice.fingerprint"]
        if operation == "restart":
            kwargs["campaign_id"] = "implement-epoch-2"
            next_admission = valid_fresh_epoch_admission(worktree)
            next_admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
            next_admission["campaign"]["supersession"] = (  # type: ignore[index]
                manifest_path.relative_to(worktree).as_posix()
            )
            kwargs["fresh_epoch"] = next_admission
        try:
            result = campaign_artifacts.start_campaign("implement", **kwargs)
        except ValueError as error:
            assert "owner token" in str(error)
            result = {"status": "failed"}

    assert result["status"] in {"failed", "lease-conflict"}
    assert manifest_path.read_bytes() == manifest_before
    assert lease_path.read_bytes() == lease_before


@pytest.mark.parametrize("version", [1, 2])
def test_empty_owner_cannot_record_status_or_abandon_campaign(
    tmp_path: Path,
    version: int,
) -> None:
    worktree = tmp_path / f"v{version}"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement" if version == 2 else "review",
        worktree=worktree,
        campaign_id=f"campaign-v{version}",
        owner_token="owner-a",
        fresh_epoch=(
            valid_fresh_epoch_admission(worktree)
            if version == 2
            else None
        ),
    )
    manifest_path = worktree / str(started["manifest"])
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease = json.loads(lease_path.read_text("utf-8"))
    lease["owner_token"] = ""
    write_json(lease_path, lease)
    before = lease_path.read_bytes()

    status = campaign_artifacts.campaign_status(
        manifest_path,
        worktree=worktree,
    )
    abandoned = campaign_artifacts.release_campaign(
        manifest_path,
        worktree=worktree,
        owner_token="",
        abandon=True,
    )

    assert status["status"] == "lease-conflict"
    assert abandoned["status"] == "lease-conflict"
    assert lease_path.read_bytes() == before


@pytest.mark.parametrize("mutation", ["epoch", "forged-restart"])
def test_v2_verify_rejects_forged_campaign_identity_before_write(
    tmp_path: Path,
    mutation: str,
) -> None:
    worktree = tmp_path / mutation
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-epoch-1",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    if mutation == "epoch":
        manifest["campaign"]["epoch"] = "other-epoch"
    else:
        manifest["campaign"]["continuation"] = "restart"
        manifest["campaign"]["supersession"] = (
            "docs/validation/skills/implement/campaigns/"
            "missing-epoch/manifest.json"
        )
    write_json(manifest_path, manifest)
    before = manifest_path.read_bytes()

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "manifest-schema"
    assert manifest_path.read_bytes() == before


@pytest.mark.parametrize(
    "mutation",
    ["ordinary-to-real-restart", "restart-to-ordinary"],
)
def test_v2_verify_rejects_creation_lineage_drift_before_write(
    tmp_path: Path,
    mutation: str,
) -> None:
    worktree = tmp_path / mutation
    worktree.mkdir()
    source = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-source",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    source_manifest = worktree / str(source["manifest"])
    source_pointer = source_manifest.relative_to(worktree).as_posix()
    if mutation == "ordinary-to-real-restart":
        released = campaign_artifacts.release_campaign(
            source_manifest,
            worktree=worktree,
            owner_token="owner-a",
        )
        assert released["status"] == "verified"
        target = campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-target",
            owner_token="owner-b",
            fresh_epoch=valid_fresh_epoch_admission(worktree),
        )
    else:
        terminal = json.loads(source_manifest.read_text("utf-8"))
        terminal["semantic"]["terminal_token"] = "campaign-complete"
        write_json(source_manifest, terminal)
        admission = valid_fresh_epoch_admission(worktree)
        admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
        admission["campaign"]["supersession"] = source_pointer  # type: ignore[index]
        target = campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id="implement-target",
            owner_token="owner-a",
            continuation="restart",
            from_manifest=source_manifest,
            fresh_epoch=admission,
        )
    target_manifest = worktree / str(target["manifest"])
    forged = json.loads(target_manifest.read_text("utf-8"))
    if mutation == "ordinary-to-real-restart":
        forged["campaign"]["continuation"] = "restart"
        forged["campaign"]["supersession"] = source_pointer
        source_payload = json.loads(source_manifest.read_text("utf-8"))
        forged["mechanical"]["supersession_digest"] = source_payload[
            "mechanical"
        ]["campaign_digest"]
    else:
        forged["campaign"]["continuation"] = None
        forged["campaign"]["supersession"] = None
        forged["mechanical"]["supersession_digest"] = None
    forged["mechanical"]["campaign_digest"] = (
        campaign_artifacts._campaign_lineage_digest(
            forged["campaign"],
            forged["mechanical"]["supersession_digest"],
        )
    )
    write_json(target_manifest, forged)
    before = target_manifest.read_bytes()

    result = campaign_artifacts.verify_campaign(
        target_manifest,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "manifest-schema"
    assert target_manifest.read_bytes() == before


def test_v2_restart_rejects_drifted_source_lineage_before_write(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "source-drift"
    worktree.mkdir()
    source = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-source",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    source_manifest = worktree / str(source["manifest"])
    source_pointer = source_manifest.relative_to(worktree).as_posix()
    terminal = json.loads(source_manifest.read_text("utf-8"))
    terminal["semantic"]["terminal_token"] = "campaign-complete"
    write_json(source_manifest, terminal)
    admission = valid_fresh_epoch_admission(worktree)
    admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
    admission["campaign"]["supersession"] = source_pointer  # type: ignore[index]
    target = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-target",
        owner_token="owner-a",
        continuation="restart",
        from_manifest=source_manifest,
        fresh_epoch=admission,
    )
    target_manifest = worktree / str(target["manifest"])
    source_payload = json.loads(source_manifest.read_text("utf-8"))
    source_payload["campaign"]["continuation"] = "restart"
    source_payload["campaign"]["supersession"] = (
        target_manifest.relative_to(worktree).as_posix()
    )
    target_payload = json.loads(target_manifest.read_text("utf-8"))
    source_payload["mechanical"]["supersession_digest"] = target_payload[
        "mechanical"
    ]["campaign_digest"]
    source_payload["mechanical"]["campaign_digest"] = (
        campaign_artifacts._campaign_lineage_digest(
            source_payload["campaign"],
            source_payload["mechanical"]["supersession_digest"],
        )
    )
    write_json(source_manifest, source_payload)
    target_before = target_manifest.read_bytes()
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_before = lease_path.read_bytes()

    result = campaign_artifacts.verify_campaign(
        target_manifest,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "manifest-schema"
    assert target_manifest.read_bytes() == target_before
    assert lease_path.read_bytes() == lease_before


def _three_epoch_restart_chain(
    worktree: Path,
) -> tuple[Path, Path, Path]:
    first = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-first",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    first_manifest = worktree / str(first["manifest"])

    def restart(source_manifest: Path, campaign_id: str) -> Path:
        terminal = json.loads(source_manifest.read_text("utf-8"))
        terminal["semantic"]["terminal_token"] = "campaign-complete"
        write_json(source_manifest, terminal)
        admission = valid_fresh_epoch_admission(worktree)
        admission["campaign"]["continuation"] = "restart"  # type: ignore[index]
        admission["campaign"]["supersession"] = (  # type: ignore[index]
            source_manifest.relative_to(worktree).as_posix()
        )
        started = campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            campaign_id=campaign_id,
            owner_token="owner-a",
            continuation="restart",
            from_manifest=source_manifest,
            fresh_epoch=admission,
        )
        return worktree / str(started["manifest"])

    second_manifest = restart(first_manifest, "implement-second")
    third_manifest = restart(second_manifest, "implement-third")
    return first_manifest, second_manifest, third_manifest


@pytest.mark.parametrize(
    "operation",
    ["verify", "resume", "status", "release", "mechanical-update"],
)
def test_chained_restart_rejects_predecessor_drift_on_every_active_path(
    tmp_path: Path,
    operation: str,
) -> None:
    worktree = tmp_path / operation
    worktree.mkdir()
    first_manifest, _, active_manifest = _three_epoch_restart_chain(worktree)
    predecessor = json.loads(first_manifest.read_text("utf-8"))
    predecessor["campaign"]["delivery_mode"] = "commit"
    predecessor["mechanical"]["campaign_digest"] = (
        campaign_artifacts._canonical_json_sha256(
            {
                "campaign": predecessor["campaign"],
                "supersession_digest": predecessor["mechanical"].get(
                    "supersession_digest"
                ),
            }
        )
    )
    write_json(first_manifest, predecessor)
    active_before = active_manifest.read_bytes()
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease_before = lease_path.read_bytes()

    if operation == "verify":
        result = campaign_artifacts.verify_campaign(
            active_manifest,
            worktree=worktree,
        )
    elif operation == "resume":
        result = campaign_artifacts.start_campaign(
            "implement",
            worktree=worktree,
            owner_token="owner-a",
            continuation="resume",
            from_manifest=active_manifest,
        )
    elif operation == "status":
        result = campaign_artifacts.campaign_status(
            active_manifest,
            worktree=worktree,
        )
    elif operation == "release":
        result = campaign_artifacts.release_campaign(
            active_manifest,
            worktree=worktree,
            owner_token="owner-a",
        )
    else:
        with pytest.raises(ValueError, match="lineage"):
            campaign_artifacts.update_mechanical_state(
                active_manifest,
                {"verified_at": "2026-07-27T00:00:00Z"},
            )
        result = {"status": "failed"}

    assert result["status"] == "failed"
    assert active_manifest.read_bytes() == active_before
    assert lease_path.read_bytes() == lease_before


def test_restart_lineage_cycle_fails_closed_before_write(tmp_path: Path) -> None:
    worktree = tmp_path / "cycle"
    worktree.mkdir()
    started = campaign_artifacts.start_campaign(
        "implement",
        worktree=worktree,
        campaign_id="implement-cycle",
        owner_token="owner-a",
        fresh_epoch=valid_fresh_epoch_admission(worktree),
    )
    manifest_path = worktree / str(started["manifest"])
    payload = json.loads(manifest_path.read_text("utf-8"))
    payload["campaign"]["continuation"] = "restart"
    payload["campaign"]["supersession"] = (
        manifest_path.relative_to(worktree).as_posix()
    )
    payload["mechanical"]["supersession_digest"] = payload["mechanical"][
        "campaign_digest"
    ]
    payload["mechanical"]["campaign_digest"] = (
        campaign_artifacts._campaign_lineage_digest(
            payload["campaign"],
            payload["mechanical"]["supersession_digest"],
        )
    )
    write_json(manifest_path, payload)
    lease_path = worktree / campaign_artifacts.LEASE_PATH
    lease = json.loads(lease_path.read_text("utf-8"))
    lease["campaign_digest"] = payload["mechanical"]["campaign_digest"]
    lease["supersession_digest"] = payload["mechanical"][
        "supersession_digest"
    ]
    write_json(lease_path, lease)
    manifest_before = manifest_path.read_bytes()
    lease_before = lease_path.read_bytes()

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "manifest-schema"
    assert manifest_path.read_bytes() == manifest_before
    assert lease_path.read_bytes() == lease_before


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


def test_contract_receipt_invalidation_is_exact_and_transitive() -> None:
    receipts = [
        {"id": "receipt-a", "inputs": [{"name": "slice"}]},
        {"id": "receipt-b", "inputs": [{"name": "receipt:receipt-a"}]},
        {"id": "receipt-unrelated", "inputs": [{"name": "other"}]},
    ]

    stale = campaign_artifacts._stale_receipts_from_invalidations(
        receipts,
        [{"receipt_ids": ["receipt-a"], "observed_at": "2026-07-25T00:00:00Z"}],
    )

    assert stale == {"receipt-a", "receipt-b"}


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


def test_fresh_proof_reuse_identity_binds_epoch_slice_and_relationships(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    target = worktree / "target"
    target.mkdir()
    (target / "value.txt").write_text("current", encoding="utf-8")
    registration = _registration(worktree)
    registration["fresh_epoch_identity"] = {
        "composition_epoch_id": "FCE-20260725-01",
        "pack_contract_revision": "f8115df444ab",
        "slice_fingerprint": f"sha256-v1:{'2' * 64}",
        "relationship_ids": ["REL-005"],
        "scenario_ids": ["PS-005"],
    }

    identity = campaign_artifacts.proof_identity_tuple(
        registration,
        candidate_root=worktree,
    )
    receipt = campaign_artifacts.make_receipt(
        registration,
        identity,
        exit_code=0,
        output_digest=hashlib.sha256(b"output").hexdigest(),
        source="execution",
        receipt_id="receipt-fresh",
    )

    assert identity["fresh_epoch_identity"] == registration[
        "fresh_epoch_identity"
    ]
    assert receipt["fresh_epoch_identity"] == registration[
        "fresh_epoch_identity"
    ]


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
    fresh_identity = {
        "composition_epoch_id": "FCE-20260725-01",
        "pack_contract_revision": "f8115df444ab",
        "slice_fingerprint": f"sha256-v1:{'a' * 64}",
        "relationship_ids": ["REL-review"],
        "scenario_ids": ["SCN-review"],
    }
    first["fresh_epoch_identity"] = json.loads(json.dumps(fresh_identity))
    second["fresh_epoch_identity"] = json.loads(json.dumps(fresh_identity))
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

    repeated = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert repeated["status"] == "verified"
    assert len(calls) == 1
    assert repeated["proof"]["deduplicated"] == ["suite-b"]


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


def _write_campaign_skill(root: Path, name: str, content: str) -> None:
    skill = root / "skills" / "custom" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(content, encoding="utf-8")


def _installation_preflight(
    worktree: Path,
    installed: Path,
    cohort: list[str],
    *,
    state: str,
) -> dict[str, object]:
    return {
        "id": "prompt5-installation",
        "kind": "installation",
        "stage": "prompt-5",
        "applicability": "required",
        "decision_pointer": "decisions.md#prompt5-installation",
        "candidate_root": ".",
        "installed_root": str(installed.resolve()),
        "cohort": cohort,
        "state": state,
    }


def _git(worktree: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=worktree,
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return completed.stdout.strip()


def _init_git_delivery_campaign(
    worktree: Path,
    *,
    delivery_mode: str = "commit",
) -> tuple[Path, dict[str, object]]:
    worktree.mkdir()
    _git(worktree, "init")
    _git(worktree, "config", "user.email", "campaign@example.com")
    _git(worktree, "config", "user.name", "Campaign Fixture")
    (worktree / "base.txt").write_text("base\n", encoding="utf-8")
    _git(worktree, "add", "base.txt")
    _git(worktree, "commit", "-m", "base")

    p1 = worktree / "p1"
    p1.mkdir()
    (p1 / "SKILL.md").write_text("P1\n", encoding="utf-8")
    started = campaign_artifacts.start_campaign(
        "review",
        delivery_mode,
        worktree=worktree,
        campaign_id="review-epoch-1",
        owner_token="owner-a",
    )
    manifest_path = worktree / str(started["manifest"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest_relative = manifest_path.relative_to(worktree).as_posix()
    decision_relative = manifest_path.with_name("decisions.md").relative_to(
        worktree
    ).as_posix()
    allowlist = sorted(
        [manifest_relative, decision_relative, "p1/SKILL.md"]
    )
    registration = {
        "id": "prompt6-delivery",
        "kind": "git-delivery",
        "stage": "prompt-6",
        "applicability": "required",
        "decision_pointer": "decisions.md#prompt6-delivery",
        "candidate_root": ".",
        "delivery_mode": delivery_mode,
        "allowlist": allowlist,
        "required_paths": [
            {"path": path, "state": "staged"} for path in allowlist
        ],
        "prompt5_manifest": manifest_relative,
        "promoted_p1": _identity_spec(
            worktree,
            "p1",
            "campaign-tree-v1",
        ),
    }
    manifest["semantic"]["declared_stage"] = "prompt-6"
    manifest["mechanical"]["preflight_registrations"] = [registration]
    write_json(manifest_path, manifest)
    _git(worktree, "add", *allowlist)
    return manifest_path, registration


def test_prompt6_verify_accepts_exact_staged_scope_without_mutating_git(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, _ = _init_git_delivery_campaign(worktree)
    before_status = _git(worktree, "status", "--porcelain=v1")
    before_manifest = manifest_path.read_bytes()
    before_index = _git(worktree, "write-tree")

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified", json.dumps(result, indent=2)
    assert result["preflight"] == {
        "completed": ["prompt6-delivery"],
        "not_applicable": [],
        "git_delivery": {
            "delivery_mode": "commit",
            "diff_checks": {"staged": "passed", "worktree": "passed"},
        },
    }
    assert manifest_path.read_bytes() == before_manifest
    assert _git(worktree, "write-tree") == before_index
    assert _git(worktree, "status", "--porcelain=v1") == before_status


def test_prompt6_status_reads_committed_tracking_parity_without_git_mutation(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, registration = _init_git_delivery_campaign(worktree)
    manifest = json.loads(manifest_path.read_text("utf-8"))
    for required in registration["required_paths"]:
        required["state"] = "committed"
    manifest["mechanical"]["preflight_registrations"] = [registration]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _git(worktree, "add", *registration["allowlist"])
    _git(worktree, "commit", "-m", "deliver campaign")
    verified = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )
    assert verified["status"] == "verified"
    branch = _git(worktree, "symbolic-ref", "--short", "HEAD")
    _git(worktree, "remote", "add", "origin", ".")
    _git(worktree, "config", f"branch.{branch}.remote", "origin")
    _git(worktree, "config", f"branch.{branch}.merge", f"refs/heads/{branch}")
    tracking_ref = f"refs/remotes/origin/{branch}"
    _git(worktree, "update-ref", tracking_ref, "HEAD")
    head = _git(worktree, "rev-parse", "HEAD")
    before_status = _git(worktree, "status", "--porcelain=v1")

    result = campaign_artifacts.campaign_status(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["git_delivery"] == {
        "delivery_mode": "commit",
        "local_head": head,
        "branch": branch,
        "tracking_ref": f"origin/{branch}",
        "remote_head": head,
        "parity": "match",
    }
    assert _git(worktree, "status", "--porcelain=v1") == before_status


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("unauthorized-staged", "Unauthorized staged paths"),
        ("missing-required", "path is missing"),
        ("ignored-required", "ignored path"),
        ("p1-drift", "Promoted P1 identity"),
        ("manifest-drift", "identity does not match staged"),
    ],
)
def test_prompt6_verify_rejects_scope_and_identity_drift_without_mutation(
    tmp_path: Path,
    case: str,
    message: str,
) -> None:
    worktree = tmp_path / case
    manifest_path, _ = _init_git_delivery_campaign(worktree)
    if case == "unauthorized-staged":
        (worktree / "unrelated.txt").write_text("unrelated\n", encoding="utf-8")
        _git(worktree, "add", "unrelated.txt")
    elif case == "missing-required":
        (worktree / "p1" / "SKILL.md").unlink()
    elif case == "ignored-required":
        (worktree / ".git" / "info" / "exclude").write_text(
            "p1/SKILL.md\n",
            encoding="utf-8",
        )
    elif case == "p1-drift":
        (worktree / "p1" / "SKILL.md").write_text("drift\n", encoding="utf-8")
    else:
        manifest_path.write_text(
            manifest_path.read_text("utf-8") + " ",
            encoding="utf-8",
        )
    before_status = _git(worktree, "status", "--porcelain=v1")
    before_index = _git(worktree, "write-tree")

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert message in result["failures"][0]["message"]
    assert _git(worktree, "write-tree") == before_index
    assert _git(worktree, "status", "--porcelain=v1") == before_status


def test_prompt6_verify_rejects_disposable_dependency_and_failed_diff_check(
    tmp_path: Path,
) -> None:
    omitted_root = tmp_path / "omitted"
    omitted_manifest, registration = _init_git_delivery_campaign(omitted_root)
    _git(omitted_root, "reset", "HEAD", "--", "p1/SKILL.md")
    registration["allowlist"].remove("p1/SKILL.md")
    registration["required_paths"] = [
        value
        for value in registration["required_paths"]
        if value["path"] != "p1/SKILL.md"
    ]
    manifest = json.loads(omitted_manifest.read_text("utf-8"))
    manifest["mechanical"]["preflight_registrations"] = [registration]
    omitted_manifest.write_text(json.dumps(manifest), encoding="utf-8")
    _git(
        omitted_root,
        "add",
        omitted_manifest.relative_to(omitted_root).as_posix(),
    )

    omitted = campaign_artifacts.verify_campaign(
        omitted_manifest,
        worktree=omitted_root,
    )

    assert omitted["status"] == "failed"
    assert "P1 files are omitted" in omitted["failures"][0]["message"]

    disposable_root = tmp_path / "disposable"
    manifest_path, registration = _init_git_delivery_campaign(disposable_root)
    _git(disposable_root, "reset", "HEAD", "--", "p1/SKILL.md")
    evidence = disposable_root / ".tmp" / "evidence.txt"
    evidence.parent.mkdir(exist_ok=True)
    evidence.write_text("evidence\n", encoding="utf-8")
    registration["allowlist"][-1] = ".tmp/evidence.txt"
    registration["allowlist"].sort()
    for required in registration["required_paths"]:
        if required["path"] == "p1/SKILL.md":
            required["path"] = ".tmp/evidence.txt"
    registration["required_paths"].sort(key=lambda value: value["path"])
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["mechanical"]["preflight_registrations"] = [registration]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _git(disposable_root, "add", manifest_path.relative_to(disposable_root).as_posix())
    _git(disposable_root, "add", "-f", ".tmp/evidence.txt")

    disposable = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=disposable_root,
    )

    assert disposable["status"] == "failed"
    assert ".tmp" in disposable["failures"][0]["message"]

    diff_root = tmp_path / "diff-check"
    manifest_path, _ = _init_git_delivery_campaign(diff_root)
    (diff_root / "p1" / "SKILL.md").write_text("P1 \n", encoding="utf-8")
    manifest = json.loads(manifest_path.read_text("utf-8"))
    registration = manifest["mechanical"]["preflight_registrations"][0]
    registration["promoted_p1"] = _identity_spec(
        diff_root,
        "p1",
        "campaign-tree-v1",
    )
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _git(diff_root, "add", "p1/SKILL.md", manifest_path.relative_to(diff_root).as_posix())

    failed_diff = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=diff_root,
    )

    assert failed_diff["status"] == "failed"
    assert failed_diff["failures"][0]["message"] == "Staged diff check failed"


def test_prompt6_verify_accepts_allowlisted_cleanup_deletion(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, registration = _init_git_delivery_campaign(worktree)
    _git(worktree, "commit", "-m", "campaign before cleanup")
    raw_relative = "obsolete.txt"
    raw_path = worktree / raw_relative
    raw_path.write_text('{"raw": true}\n', encoding="utf-8")
    _git(worktree, "add", raw_relative)
    _git(worktree, "commit", "-m", "tracked raw output")

    manifest = json.loads(manifest_path.read_text("utf-8"))
    registration = manifest["mechanical"]["preflight_registrations"][0]
    for required in registration["required_paths"]:
        required["state"] = (
            "staged"
            if required["path"] == manifest_path.relative_to(worktree).as_posix()
            else "committed"
        )
    registration["allowlist"].append(raw_relative)
    registration["allowlist"].sort()
    registration["required_paths"].append(
        {"path": raw_relative, "state": "deleted"}
    )
    registration["required_paths"].sort(key=lambda value: value["path"])
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    raw_path.unlink()
    _git(
        worktree,
        "add",
        manifest_path.relative_to(worktree).as_posix(),
        raw_relative,
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified", result


def test_prompt6_verify_treats_deleted_path_as_literal_pathspec(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, _ = _init_git_delivery_campaign(worktree)
    _git(worktree, "commit", "-m", "campaign before cleanup")
    raw_relative = "obsolete[1].txt"
    raw_path = worktree / raw_relative
    raw_path.write_text('{"raw": true}\n', encoding="utf-8")
    matching_path = worktree / "obsolete1.txt"
    matching_path.write_text("keep\n", encoding="utf-8")
    _git(worktree, "add", raw_relative, matching_path.name)
    _git(worktree, "commit", "-m", "tracked cleanup candidates")

    manifest = json.loads(manifest_path.read_text("utf-8"))
    registration = manifest["mechanical"]["preflight_registrations"][0]
    for required in registration["required_paths"]:
        required["state"] = (
            "staged"
            if required["path"] == manifest_path.relative_to(worktree).as_posix()
            else "committed"
        )
    registration["allowlist"].append(raw_relative)
    registration["allowlist"].sort()
    registration["required_paths"].append(
        {"path": raw_relative, "state": "deleted"}
    )
    registration["required_paths"].sort(key=lambda value: value["path"])
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    raw_path.unlink()
    _git(
        worktree,
        "add",
        manifest_path.relative_to(worktree).as_posix(),
        raw_relative,
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified", result


def test_prompt6_verify_rejects_worktree_only_cleanup_deletion(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, _ = _init_git_delivery_campaign(worktree)
    _git(worktree, "commit", "-m", "campaign before cleanup")
    raw_relative = "obsolete.txt"
    raw_path = worktree / raw_relative
    raw_path.write_text('{"raw": true}\n', encoding="utf-8")
    _git(worktree, "add", raw_relative)
    _git(worktree, "commit", "-m", "tracked raw output")

    manifest = json.loads(manifest_path.read_text("utf-8"))
    registration = manifest["mechanical"]["preflight_registrations"][0]
    manifest_relative = manifest_path.relative_to(worktree).as_posix()
    for required in registration["required_paths"]:
        required["state"] = (
            "staged"
            if required["path"] == manifest_relative
            else "committed"
        )
    registration["allowlist"].append(raw_relative)
    registration["allowlist"].sort()
    registration["required_paths"].append(
        {"path": raw_relative, "state": "deleted"}
    )
    registration["required_paths"].sort(key=lambda value: value["path"])
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    raw_path.write_text('{"raw": "modified"}\n', encoding="utf-8")
    _git(worktree, "add", manifest_relative, raw_relative)
    raw_path.unlink()

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert "index still contains" in result["failures"][0]["message"]


def test_prompt6_verify_rejects_allowlisted_tracked_raw_campaign_output(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, _ = _init_git_delivery_campaign(worktree)
    raw_relative = manifest_path.with_name("sample-output.json").relative_to(
        worktree
    ).as_posix()
    raw_path = worktree / raw_relative
    raw_path.write_text('{"raw": true}\n', encoding="utf-8")
    manifest = json.loads(manifest_path.read_text("utf-8"))
    registration = manifest["mechanical"]["preflight_registrations"][0]
    registration["allowlist"].append(raw_relative)
    registration["allowlist"].sort()
    registration["required_paths"].append(
        {"path": raw_relative, "state": "staged"}
    )
    registration["required_paths"].sort(key=lambda value: value["path"])
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _git(
        worktree,
        "add",
        manifest_path.relative_to(worktree).as_posix(),
        raw_relative,
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert "raw campaign artifact" in result["failures"][0]["message"]


def test_prompt6_verify_requires_exact_delivery_authority_and_accepts_push(
    tmp_path: Path,
) -> None:
    none_root = tmp_path / "none"
    none_manifest, _ = _init_git_delivery_campaign(
        none_root,
        delivery_mode="none",
    )
    none = campaign_artifacts.verify_campaign(
        none_manifest,
        worktree=none_root,
    )
    assert none["status"] == "failed"
    assert "commit or push authority" in none["failures"][0]["message"]

    push_root = tmp_path / "push"
    push_manifest, _ = _init_git_delivery_campaign(
        push_root,
        delivery_mode="push",
    )
    pushed = campaign_artifacts.verify_campaign(
        push_manifest,
        worktree=push_root,
    )
    assert pushed["status"] == "verified"
    assert pushed["preflight"]["git_delivery"]["delivery_mode"] == "push"

    duplicate_root = tmp_path / "duplicate"
    duplicate_manifest, registration = _init_git_delivery_campaign(duplicate_root)
    manifest = json.loads(duplicate_manifest.read_text("utf-8"))
    duplicate = dict(registration)
    duplicate["id"] = "prompt6-delivery-two"
    manifest["mechanical"]["preflight_registrations"].append(duplicate)
    duplicate_manifest.write_text(json.dumps(manifest), encoding="utf-8")
    _git(
        duplicate_root,
        "add",
        duplicate_manifest.relative_to(duplicate_root).as_posix(),
    )
    duplicate_result = campaign_artifacts.verify_campaign(
        duplicate_manifest,
        worktree=duplicate_root,
    )
    assert duplicate_result["status"] == "failed"
    assert duplicate_result["gate"] == "preflight-registration"


def test_prompt6_verify_requires_frozen_proof_receipts_without_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    manifest_path, registration = _init_git_delivery_campaign(worktree)
    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["mechanical"]["proof_registrations"] = [
        {
            "id": "prompt6-current-checks",
            "stage": "prompt-6",
            "profile": "campaign-artifacts-focused-v1",
            "applicability": "required",
            "decision_pointer": "decisions.md#prompt6-current-checks",
            "candidate_root": ".",
            "target": _identity_spec(
                worktree,
                "p1",
                "campaign-tree-v1",
            ),
            "inputs": [
                {
                    "name": "promoted-p1",
                    **_identity_spec(
                        worktree,
                        "p1",
                        "campaign-tree-v1",
                    ),
                }
            ],
        }
    ]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    decision_path = manifest_path.with_name("decisions.md")
    decision_path.write_text(
        decision_path.read_text("utf-8")
        + "<!-- campaign-decision:prompt6-current-checks -->\n",
        encoding="utf-8",
    )
    _git(worktree, "add", *registration["allowlist"])
    before_manifest = manifest_path.read_bytes()
    monkeypatch.setattr(
        campaign_artifacts,
        "_run_profile",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Prompt 6 must not execute proof")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "proof-receipt"
    assert manifest_path.read_bytes() == before_manifest

    manifest = json.loads(manifest_path.read_text("utf-8"))
    proof_registration = manifest["mechanical"]["proof_registrations"][0]
    identity_tuple = campaign_artifacts.proof_identity_tuple(
        proof_registration,
        candidate_root=worktree,
    )
    receipt = campaign_artifacts.make_receipt(
        proof_registration,
        identity_tuple,
        exit_code=0,
        output_digest="0" * 64,
        source="execution",
    )
    manifest["mechanical"]["receipts"] = [receipt]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    _git(worktree, "add", manifest_path.relative_to(worktree).as_posix())
    before_manifest = manifest_path.read_bytes()

    restored = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert restored["status"] == "verified"
    assert restored["proof"]["reused_receipts"] == [receipt["id"]]
    assert restored["proof"]["executed"] == []
    assert manifest_path.read_bytes() == before_manifest


def test_prompt6_status_reports_unavailable_detached_and_diverged_tracking(
    tmp_path: Path,
) -> None:
    missing_root = tmp_path / "missing"
    missing_manifest, _ = _init_git_delivery_campaign(missing_root)
    missing = campaign_artifacts.campaign_status(
        missing_manifest,
        worktree=missing_root,
    )
    assert missing["git_delivery"]["parity"] == "unavailable"
    assert missing["git_delivery"]["tracking_ref"] is None

    detached_root = tmp_path / "detached"
    detached_manifest, _ = _init_git_delivery_campaign(detached_root)
    _git(detached_root, "checkout", "--detach")
    detached = campaign_artifacts.campaign_status(
        detached_manifest,
        worktree=detached_root,
    )
    assert detached["git_delivery"]["branch"] == "detached"
    assert detached["git_delivery"]["parity"] == "unavailable"

    diverged_root = tmp_path / "diverged"
    diverged_manifest, registration = _init_git_delivery_campaign(diverged_root)
    manifest = json.loads(diverged_manifest.read_text("utf-8"))
    for required in registration["required_paths"]:
        required["state"] = "committed"
    manifest["mechanical"]["preflight_registrations"] = [registration]
    write_json(diverged_manifest, manifest)
    _git(diverged_root, "add", *registration["allowlist"])
    _git(diverged_root, "commit", "-m", "deliver campaign")
    branch = _git(diverged_root, "symbolic-ref", "--short", "HEAD")
    _git(diverged_root, "remote", "add", "origin", ".")
    _git(diverged_root, "config", f"branch.{branch}.remote", "origin")
    _git(diverged_root, "config", f"branch.{branch}.merge", f"refs/heads/{branch}")
    _git(diverged_root, "update-ref", f"refs/remotes/origin/{branch}", "HEAD^")

    diverged = campaign_artifacts.campaign_status(
        diverged_manifest,
        worktree=diverged_root,
    )

    assert diverged["git_delivery"]["parity"] == "diverged"
    assert diverged["git_delivery"]["local_head"] != diverged["git_delivery"][
        "remote_head"
    ]


def test_prompt5_plan_verifies_exact_declared_cohort_without_installing(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="plan",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert result["preflight"]["completed"] == ["prompt5-installation"]
    assert not installed.exists()


def test_prompt5_installation_preflight_cannot_be_not_applicable(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    registration = _installation_preflight(
        worktree,
        installed,
        ["alpha"],
        state="plan",
    )
    registration["applicability"] = "not-applicable"
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[registration],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "required" in result["failures"][0]["message"]
    assert not installed.exists()


def test_prompt5_plan_accepts_updated_multi_skill_declared_cohort(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "old")
    _write_campaign_skill(worktree, "beta", "old")
    install_skills.install(worktree, installed, None)
    (worktree / "skills/custom/alpha/SKILL.md").write_text("new", encoding="utf-8")
    (worktree / "skills/custom/beta/SKILL.md").write_text("new", encoding="utf-8")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha", "beta"],
                state="plan",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert (installed / "alpha/SKILL.md").read_text("utf-8") == "old"
    assert (installed / "beta/SKILL.md").read_text("utf-8") == "old"


@pytest.mark.parametrize(
    ("declared", "extra_skill"),
    [
        (["alpha"], "beta"),
        (["alpha", "beta"], None),
    ],
)
def test_prompt5_plan_rejects_additions_and_omissions(
    tmp_path: Path,
    declared: list[str],
    extra_skill: str | None,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    if extra_skill is not None:
        _write_campaign_skill(worktree, extra_skill, "unexpected")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                declared,
                state="plan",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "cohort" in result["failures"][0]["message"]
    assert not installed.exists()


def test_prompt5_rejects_retirement_drift(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    _write_campaign_skill(worktree, "retired", "old")
    install_skills.install(worktree, installed, None)
    (worktree / "skills/custom/retired/SKILL.md").unlink()
    (worktree / "skills/custom/retired").rmdir()
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="post-install",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert "retirement" in result["failures"][0]["message"]
    assert (installed / "retired/SKILL.md").read_text("utf-8") == "old"


def test_prompt5_post_install_proves_parity_and_ignores_unmanaged_skill(
    tmp_path: Path,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    install_skills.install(worktree, installed, None)
    personal = installed / "personal"
    personal.mkdir()
    (personal / "SKILL.md").write_text("unmanaged", encoding="utf-8")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="post-install",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "verified"
    assert (personal / "SKILL.md").read_text("utf-8") == "unmanaged"


@pytest.mark.parametrize("mirror_state", ["missing", "drifted"])
def test_prompt5_post_install_rejects_missing_or_drifted_mirror(
    tmp_path: Path,
    mirror_state: str,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    if mirror_state == "drifted":
        install_skills.install(worktree, installed, None)
        (installed / "alpha/SKILL.md").write_text("drift", encoding="utf-8")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="post-install",
            )
        ],
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"


def test_prompt5_rejects_incompatible_installer_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="plan",
            )
        ],
    )
    monkeypatch.setattr(
        install_skills,
        "install",
        lambda *args, **kwargs: {
            "schema_version": 1,
            "dry_run": True,
            "identity_algorithm": "skill-tree-v1",
            "new": None,
            "updated": [],
            "unchanged": [],
            "retired": [],
        },
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "malformed" in result["failures"][0]["message"]


def test_prompt5_wraps_installer_recovery_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="plan",
            )
        ],
    )
    monkeypatch.setattr(
        install_skills,
        "install",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("unfinished transaction")
        ),
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "unfinished transaction" in result["failures"][0]["message"]


def test_prompt5_rejects_planned_resulting_identity_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    worktree = tmp_path / "repo"
    worktree.mkdir()
    installed = tmp_path / "installed"
    _write_campaign_skill(worktree, "alpha", "v1")
    manifest_path = _start_preflight_campaign(
        worktree,
        stage="prompt-5",
        registrations=[
            _installation_preflight(
                worktree,
                installed,
                ["alpha"],
                state="post-install",
            )
        ],
    )
    monkeypatch.setattr(
        install_skills,
        "install",
        lambda *args, **kwargs: {
            "schema_version": 1,
            "dry_run": True,
            "identity_algorithm": "skill-tree-v1",
            "new": [],
            "updated": [],
            "unchanged": ["alpha"],
            "retired": [],
            "planned_identities": {"alpha": "a" * 64},
            "resulting_identities": {"alpha": "b" * 64},
        },
    )

    result = campaign_artifacts.verify_campaign(
        manifest_path,
        worktree=worktree,
    )

    assert result["status"] == "failed"
    assert result["gate"] == "preflight-validation"
    assert "identities differ" in result["failures"][0]["message"]


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
