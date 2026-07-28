from __future__ import annotations

import importlib
from copy import deepcopy
from pathlib import Path


def pack_contract():
    return importlib.import_module("scripts.pack_contract")


def skill(
    skill_id: str,
    *,
    name: str,
    role: str,
    order: int,
    capabilities: list[str],
    relationships: list[str] | None = None,
) -> dict[str, object]:
    return {
        "skill_id": skill_id,
        "canonical_name": name,
        "essential_outcome": f"Complete the {name} outcome",
        "primary_role": role,
        "contract_order": order,
        "invocation_mode": "implicit",
        "positive_entry_predicate": f"{name} is needed",
        "negative_exclusion_predicates": [f"{name} is not needed"],
        "owned_authority_mutation_surfaces": [f"{name} owner"],
        "prohibited_ownership": ["foreign semantic decisions"],
        "required_input": f"{name} request",
        "return_packet": f"{name} result",
        "completion_condition": f"{name} complete",
        "failure_return": f"{name} blocked",
        "owned_capability_ids": capabilities,
        "relationship_ids": relationships or [],
        "acceptance_scenario_ids": ["PS-001"],
        "load_budget_class": "conditional",
        "campaign_state": {
            "status": "not-started",
            "campaign_id": None,
            "terminal_evidence_pointer": None,
        },
    }


def capability(
    capability_id: str,
    owner: str,
    *,
    essential: bool = True,
) -> dict[str, object]:
    return {
        "capability_id": capability_id,
        "essential": essential,
        "observable_outcome": f"{capability_id} outcome",
        "entry_conditions": ["A bounded request exists"],
        "completion_return": f"{capability_id} result",
        "required_authority_mutation": ["local owner"],
        "primary_owner_skill_id": owner,
        "allowed_contributor_skill_ids": [],
        "exclusions": ["foreign ownership"],
        "acceptance_scenario_ids": ["PS-001"],
        "proof_class": "structural",
        "disposition": "selected",
    }


def relationship(
    relationship_id: str,
    caller: str,
    target: str,
    *,
    verb: str = "Invoke",
    ordering_impact: str = "callee-before-caller",
) -> dict[str, object]:
    return {
        "relationship_id": relationship_id,
        "caller_skill_id": caller,
        "verb": verb,
        "target_skill_id": target,
        "entry_condition": "The target result is required",
        "wrong_condition": "The caller can complete locally",
        "input_packet": "bounded request",
        "callee_owned_gates_mutations": ["target local gates"],
        "return_packet": "typed target result",
        "resume_owner_skill_id": caller,
        "combined_exit_owner_skill_id": caller,
        "failure_behavior": "return the exact target blocker",
        "context_loaded": ["target interface only"],
        "affected_capability_ids": ["CAP-002"],
        "ordering_impact": ordering_impact,
        "required_proof_ids": ["PROOF-REL-001"],
    }


def valid_contract() -> dict[str, object]:
    contract = pack_contract().create_draft()
    header = contract["epoch_header"]
    header.update(  # type: ignore[union-attr]
        {
            "composition_epoch_id": "FCE-20260726-01",
            "contract_revision": 1,
            "fixed_point": {
                "repository_tree": "a" * 40,
                "environment": "codex/windows/python-3.12",
                "timestamp": "2026-07-26T00:00:00Z",
            },
            "intended_pack_outcome": "Complete bounded engineering work predictably",
            "scope": ["repository engineering workflows"],
            "exclusions": ["automatic semantic acceptance"],
            "source_pointers": [
                "ADR-0008#sha256-v1:" + "a" * 64,
                "ADR-0009#sha256-v1:" + "b" * 64,
                "issue-36#sha256-v1:" + "c" * 64,
            ],
            "acceptance_scenarios": [
                {
                    "scenario_id": "PS-001",
                    "description": "Leaf to aggregate to router workflow",
                    "expected_owner_skill_id": "SK-003",
                }
            ],
            "load_budget_policy": {
                "metric": "runtime instruction class",
                "ceiling_or_class": "conditional",
                "status": "set",
            },
            "campaign_proof_graph": [
                {
                    "predecessor_skill_id": "SK-001",
                    "successor_skill_id": "SK-002",
                },
                {
                    "predecessor_skill_id": "SK-002",
                    "successor_skill_id": "SK-003",
                },
            ],
        }
    )
    contract["capabilities"] = [
        capability("CAP-001", "SK-001"),
        capability("CAP-002", "SK-002"),
        capability("CAP-003", "SK-003"),
    ]
    contract["selected_skills"] = [
        skill(
            "SK-001",
            name="provider",
            role="leaf",
            order=1,
            capabilities=["CAP-001"],
        ),
        skill(
            "SK-002",
            name="aggregate",
            role="executable-aggregate",
            order=2,
            capabilities=["CAP-002"],
            relationships=["REL-001"],
        ),
        skill(
            "SK-003",
            name="router",
            role="router",
            order=3,
            capabilities=["CAP-003"],
        ),
    ]
    contract["relationships"] = [
        relationship("REL-001", "SK-002", "SK-001"),
    ]
    contract["exclusions_collisions_gaps"] = [
        {
            "issue_id": f"ECG-8{index:02d}",
            "class": collision_class,
            "essential": True,
            "involved_skill_ids": [],
            "involved_capability_ids": [],
            "terms": [],
            "observable_conflict": (
                f"Fixture {collision_class} collision is resolved"
            ),
            "governing_owner": "fixture pack owner",
            "resolution": "one fixture owner and one explicit boundary",
            "negative_control_scenario_id": "PS-001",
            "status": "resolved",
            "future_owner_or_stopping_condition": None,
            "nondependency_proof_ids": [],
        }
        for index, collision_class in enumerate(
            sorted(pack_contract().REQUIRED_COLLISION_CLASSES),
            start=1,
        )
    ]
    return contract


def test_absent_owner_creates_marker_bounded_draft_only() -> None:
    contract = pack_contract()

    draft = contract.create_draft()
    rendered = contract.render_contract(
        draft,
        introduction="# Pack Composition Contract\n\nOwner commentary.\n",
    )

    assert draft["epoch_header"]["status"] == "draft"
    assert draft["epoch_header"]["composition_epoch_id"] is None
    assert draft["capabilities"] == []
    assert draft["selected_skills"] == []
    assert draft["relationships"] == []
    assert draft["exclusions_collisions_gaps"] == []
    assert rendered.count(contract.CONTRACT_BEGIN) == 1
    assert rendered.count(contract.CONTRACT_END) == 1
    assert contract.parse_contract(rendered) == draft
    assert contract.semantic_fingerprint(rendered) == contract.semantic_fingerprint(
        contract.render_contract(draft, introduction="# Different commentary\n")
    )

    freeze = contract.freeze_contract(draft)

    assert freeze["status"] == "contract-invalid"
    assert freeze["contract"] == draft
    assert freeze["failures"]


def test_exact_user_approval_can_authorize_one_explicit_target_invocation() -> None:
    contract = pack_contract()
    draft = valid_contract()
    draft["selected_skills"][0]["invocation_mode"] = "explicit-only"

    assert (
        "explicit-only target SK-001 requires Recommend and stop"
        in contract.validate_contract(draft)
    )

    draft["relationships"][0][
        "explicit_target_authority"
    ] = "exact-user-approved-packet"
    assert contract.validate_contract(draft) == []

    draft["selected_skills"][0]["invocation_mode"] = "implicit"
    assert (
        "relationship REL-001 has inapplicable explicit_target_authority"
        in contract.validate_contract(draft)
    )


def test_freeze_returns_deterministic_order_and_immutable_slice() -> None:
    contract = pack_contract()
    draft = valid_contract()

    frozen = contract.freeze_contract(draft)

    assert frozen["status"] == "contract-frozen"
    assert frozen["contract"]["epoch_header"]["status"] == "frozen"
    assert contract.campaign_order(frozen["contract"]) == [
        "SK-001",
        "SK-002",
        "SK-003",
    ]
    frozen["contract"]["selected_skills"][0]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": "campaign-SK-001",
        "terminal_evidence_pointer": "proof://provider",
    }
    first = contract.contract_slice(
        frozen["contract"],
        "SK-002",
    )
    second = contract.contract_slice(
        frozen["contract"],
        "SK-002",
    )
    assert first == second
    assert first["status"] == "contract-slice"
    assert first["slice"]["skill"]["skill_id"] == "SK-002"
    assert [row["capability_id"] for row in first["slice"]["capabilities"]] == [
        "CAP-002"
    ]
    assert first["slice"]["slice_id"] == "FCE-20260726-01:r1:SK-002"
    assert first["slice_fingerprint"].startswith("sha256-v1:")
    admission = contract.campaign_admission_slice(
        frozen["contract"],
        "SK-002",
    )
    assert admission["status"] == "campaign-admission-slice"
    assert admission["slice"] == {
        "slice_id": "FCE-20260726-01:r1:SK-002:aggregate",
        "selected_capability_ids": ["CAP-002"],
        "selected_relationship_ids": ["REL-001"],
        "selected_scenario_ids": ["PS-001"],
        "hard_proof_predecessor_ids": ["SK-001"],
    }
    semantic_base = contract.freeze_contract(valid_contract())["contract"]
    runtime = deepcopy(semantic_base)
    runtime["epoch_header"]["status"] = "campaign-active"
    runtime["selected_skills"][1]["campaign_state"] = {
        "status": "active",
        "campaign_id": "campaign-SK-002",
        "terminal_evidence_pointer": None,
    }
    leaf_runtime = contract.contract_slice(runtime, "SK-001")
    leaf_frozen = contract.contract_slice(semantic_base, "SK-001")
    assert leaf_runtime["slice_fingerprint"] == leaf_frozen["slice_fingerprint"]
    runtime["selected_skills"][0]["campaign_state"] = {
        "status": "ready",
        "campaign_id": None,
        "terminal_evidence_pointer": None,
    }
    assert contract.contract_slice(runtime, "SK-001")["slice_fingerprint"] == (
        leaf_frozen["slice_fingerprint"]
    )
    runtime["selected_skills"][0]["campaign_state"] = {
        "status": "active",
        "campaign_id": "campaign-SK-001",
        "terminal_evidence_pointer": None,
    }
    assert contract.contract_slice(runtime, "SK-001")["status"] == (
        "campaign-already-started"
    )
    assert (
        contract.contract_slice(draft, "SK-002")["status"]
        == "contract-not-frozen"
    )
    not_ready = contract.freeze_contract(valid_contract())["contract"]
    assert contract.contract_slice(not_ready, "SK-002")["status"] == (
        "campaign-not-ready"
    )
    assert contract.contract_slice(
        not_ready,
        "SK-002",
        terminal_evidence={"SK-001": "proof://forged"},
    )["status"] == "campaign-not-ready"
    locked = deepcopy(frozen["contract"])
    locked["epoch_header"]["status"] = "integration-accepted"
    assert contract.contract_slice(locked, "SK-002")["status"] == (
        "contract-not-frozen"
    )
    locked_status_drift = deepcopy(frozen["contract"])
    locked_status_drift["epoch_header"]["epoch_lock"] = {
        "lock_id": "LOCK-FCE-20260726-01",
        "evidence_pointer": "proof://lock",
    }
    assert contract.contract_slice(locked_status_drift, "SK-001")["status"] == (
        "contract-not-frozen"
    )


def test_frozen_contract_projects_unready_immutable_blueprints() -> None:
    contract = pack_contract()
    frozen = contract.freeze_contract(valid_contract())["contract"]

    admission = contract.contract_slice(frozen, "SK-002")
    blueprint = contract.contract_blueprint(frozen, "SK-002")

    assert admission == {
        "status": "campaign-not-ready",
        "skill_id": "SK-002",
        "missing_predecessor_skill_ids": ["SK-001"],
    }
    assert blueprint["status"] == "contract-slice-blueprint"
    assert blueprint["slice"]["slice_id"] == "FCE-20260726-01:r1:SK-002"
    assert blueprint["predecessor_skill_ids"] == ["SK-001"]
    assert blueprint["slice_fingerprint"].startswith("sha256-v1:")


def test_freeze_rejects_ownership_relationship_cycle_and_semantic_authority() -> None:
    contract = pack_contract()
    draft = valid_contract()
    draft["capabilities"][1]["primary_owner_skill_id"] = "SK-001"
    draft["selected_skills"][0]["owned_capability_ids"].append("CAP-002")
    draft["relationships"][0]["verb"] = "Call"
    draft["epoch_header"]["campaign_proof_graph"].append(
        {
            "predecessor_skill_id": "SK-003",
            "successor_skill_id": "SK-001",
        }
    )
    draft["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "authority",
            "essential": True,
            "involved_skill_ids": ["SK-001", "SK-002"],
            "involved_capability_ids": ["CAP-002"],
            "terms": [],
            "observable_conflict": "Two skills claim final authority",
            "governing_owner": "pack owner",
            "resolution": None,
            "negative_control_scenario_id": "PS-001",
            "status": "unresolved",
            "future_owner_or_stopping_condition": None,
            "nondependency_proof_ids": [],
        }
    )
    draft["selected_skills"][0]["h1"] = "adopt candidate wording"

    result = contract.freeze_contract(draft)

    assert result["status"] == "contract-invalid"
    message = "\n".join(result["failures"])
    assert "ownership" in message
    assert "relationship verb" in message
    assert "cycle" in message
    assert "unresolved" in message
    assert "forbidden semantic field" in message


def test_freeze_rejects_placeholder_collision_and_mutable_source_pointer() -> None:
    contract = pack_contract()
    draft = valid_contract()
    vocabulary = next(
        issue
        for issue in draft["exclusions_collisions_gaps"]
        if issue["class"] == "vocabulary"
    )
    vocabulary["resolution"] = None
    vocabulary["negative_control_scenario_id"] = None
    vocabulary["nondependency_proof_ids"] = []
    draft["epoch_header"]["source_pointers"][0] = "ADR-0008"

    result = contract.freeze_contract(draft)

    assert result["status"] == "contract-invalid"
    message = "\n".join(result["failures"])
    assert "substantive resolved evidence for vocabulary collision" in message
    assert "content-addressed source pointers" in message


def test_amendment_reports_localized_invalidation_without_mutation() -> None:
    contract = pack_contract()
    frozen = contract.freeze_contract(valid_contract())["contract"]
    proposed = deepcopy(frozen)
    proposed["epoch_header"]["contract_revision"] = 2
    proposed["selected_skills"][0]["essential_outcome"] = "Changed provider outcome"
    proof_registry = {
        "SK-001": ["PROOF-SK1"],
        "SK-002": ["PROOF-SK2"],
        "SK-003": ["PROOF-SK3"],
    }

    result = contract.assess_amendment(
        frozen,
        proposed,
        proof_registry=proof_registry,
    )

    assert result["status"] == "behavior-decision-gap"
    assert result["required_contract_revision"] == 2
    assert result["affected_skill_ids"] == ["SK-001", "SK-002", "SK-003"]
    assert result["stale_proof_ids"] == [
        "PROOF-SK1",
        "PROOF-SK2",
        "PROOF-SK3",
    ]
    assert frozen["selected_skills"][0]["essential_outcome"] != (
        proposed["selected_skills"][0]["essential_outcome"]
    )

    unrelated = deepcopy(frozen)
    unrelated["epoch_header"]["contract_revision"] = 2
    unrelated["selected_skills"][2]["load_budget_class"] = "always-loaded"
    local = contract.assess_amendment(
        frozen,
        unrelated,
        proof_registry=proof_registry,
    )
    assert local["affected_skill_ids"] == ["SK-003"]
    assert local["stale_proof_ids"] == ["PROOF-SK3"]

    capability_local = deepcopy(frozen)
    capability_local["epoch_header"]["contract_revision"] = 2
    capability_local["capabilities"][2]["observable_outcome"] = "Changed router cap"
    cap_result = contract.assess_amendment(
        frozen,
        capability_local,
        proof_registry=proof_registry,
    )
    assert cap_result["affected_skill_ids"] == ["SK-003"]

    issue_local = deepcopy(frozen)
    issue_local["epoch_header"]["contract_revision"] = 2
    issue_local["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "gap",
            "essential": False,
            "involved_skill_ids": [],
            "involved_capability_ids": ["CAP-003"],
            "terms": [],
            "observable_conflict": "Router proof gap",
            "governing_owner": "pack owner",
            "resolution": None,
            "negative_control_scenario_id": "PS-001",
            "status": "deferred",
            "future_owner_or_stopping_condition": "router owner",
            "nondependency_proof_ids": ["PROOF-NONDEP"],
        }
    )
    issue_result = contract.assess_amendment(
        frozen,
        issue_local,
        proof_registry=proof_registry,
    )
    assert issue_result["affected_skill_ids"] == ["SK-003"]

    wrong_epoch = deepcopy(frozen)
    wrong_epoch["epoch_header"]["contract_revision"] = 2
    wrong_epoch["epoch_header"]["composition_epoch_id"] = "FCE-20260726-02"
    assert (
        contract.assess_amendment(
            frozen,
            wrong_epoch,
            proof_registry=proof_registry,
        )["status"]
        == "contract-incompatible"
    )
    injected_lock = deepcopy(frozen)
    injected_lock["epoch_header"]["contract_revision"] = 2
    injected_lock["epoch_header"]["epoch_lock"] = {
        "lock_id": "LOCK-INJECTED",
        "evidence_pointer": "proof://injected",
    }
    assert (
        contract.assess_amendment(
            frozen,
            injected_lock,
            proof_registry=proof_registry,
        )["status"]
        == "contract-incompatible"
    )
    locked = deepcopy(frozen)
    locked["epoch_header"]["epoch_lock"] = {
        "lock_id": "LOCK-FCE-20260726-01",
        "evidence_pointer": "proof://lock",
    }
    locked_proposed = deepcopy(locked)
    locked_proposed["epoch_header"]["contract_revision"] = 2
    assert (
        contract.assess_amendment(
            locked,
            locked_proposed,
            proof_registry=proof_registry,
        )["status"]
        == "contract-incompatible"
    )

    expanded = valid_contract()
    expanded["capabilities"].append(capability("CAP-004", "SK-004"))
    expanded["selected_skills"].append(
        skill(
            "SK-004",
            name="independent",
            role="leaf",
            order=4,
            capabilities=["CAP-004"],
        )
    )
    expanded["relationships"][0]["affected_capability_ids"].append("CAP-004")
    expanded_frozen = contract.freeze_contract(expanded)["contract"]
    expanded_proposed = deepcopy(expanded_frozen)
    expanded_proposed["epoch_header"]["contract_revision"] = 2
    expanded_proposed["relationships"][0]["input_packet"] = "changed packet"
    expanded_result = contract.assess_amendment(
        expanded_frozen,
        expanded_proposed,
        proof_registry={"SK-004": ["PROOF-SK4"]},
    )
    assert "SK-004" in expanded_result["affected_skill_ids"]
    assert "PROOF-SK4" in expanded_result["stale_proof_ids"]

    row_proof = valid_contract()
    row_proof["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "gap",
            "essential": False,
            "involved_skill_ids": ["SK-003"],
            "involved_capability_ids": ["CAP-003"],
            "terms": [],
            "observable_conflict": "Deferred router gap",
            "governing_owner": "pack owner",
            "resolution": None,
            "negative_control_scenario_id": "PS-001",
            "status": "deferred",
            "future_owner_or_stopping_condition": "router owner",
            "nondependency_proof_ids": ["PROOF-NONDEP"],
        }
    )
    row_frozen = contract.freeze_contract(row_proof)["contract"]
    row_proposed = deepcopy(row_frozen)
    row_proposed["epoch_header"]["contract_revision"] = 2
    row_proposed["relationships"][0]["input_packet"] = "changed relationship"
    next(
        issue
        for issue in row_proposed["exclusions_collisions_gaps"]
        if issue["issue_id"] == "ECG-001"
    )["future_owner_or_stopping_condition"] = "new router owner"
    row_result = contract.assess_amendment(
        row_frozen,
        row_proposed,
        proof_registry={},
    )
    assert "PROOF-REL-001" in row_result["stale_proof_ids"]
    assert "PROOF-NONDEP" in row_result["stale_proof_ids"]

    scenario_contract = valid_contract()
    scenario_contract["capabilities"].append(capability("CAP-004", "SK-004"))
    scenario_contract["selected_skills"].append(
        skill(
            "SK-004",
            name="independent",
            role="leaf",
            order=4,
            capabilities=["CAP-004"],
        )
    )
    scenario_contract["epoch_header"]["acceptance_scenarios"].append(
        {
            "scenario_id": "PS-002",
            "description": "Independent negative control",
            "expected_owner_skill_id": "SK-004",
        }
    )
    scenario_contract["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "gap",
            "essential": False,
            "involved_skill_ids": ["SK-003"],
            "involved_capability_ids": ["CAP-003"],
            "terms": [],
            "observable_conflict": "Router negative control",
            "governing_owner": "pack owner",
            "resolution": None,
            "negative_control_scenario_id": "PS-002",
            "status": "deferred",
            "future_owner_or_stopping_condition": "router owner",
            "nondependency_proof_ids": ["PROOF-PS2"],
        }
    )
    scenario_frozen = contract.freeze_contract(scenario_contract)["contract"]
    scenario_proposed = deepcopy(scenario_frozen)
    scenario_proposed["epoch_header"]["contract_revision"] = 2
    scenario_proposed["epoch_header"]["acceptance_scenarios"][1][
        "description"
    ] = "Changed independent negative control"
    scenario_result = contract.assess_amendment(
        scenario_frozen,
        scenario_proposed,
        proof_registry={
            "SK-003": ["PROOF-SK3"],
            "SK-004": ["PROOF-SK4"],
        },
    )
    assert {"SK-003", "SK-004"} <= set(scenario_result["affected_skill_ids"])
    assert "PROOF-PS2" in scenario_result["stale_proof_ids"]


def test_result_state_is_validated_but_never_set_by_automation() -> None:
    contract = pack_contract()
    frozen = contract.freeze_contract(valid_contract())["contract"]

    missing = contract.validate_result(frozen)
    accepted = deepcopy(frozen)
    accepted["epoch_header"]["integration_result"] = {
        "decision": "integration-accepted",
        "evidence_pointer": "docs/validation/skill-pack/FCE-20260726-01/results.json",
    }
    premature = contract.validate_result(accepted)
    accepted["epoch_header"]["status"] = "integration-accepted"
    for row in accepted["selected_skills"]:
        row["campaign_state"] = {
            "status": "terminal",
            "campaign_id": f"campaign-{row['skill_id']}",
            "terminal_evidence_pointer": f"proof://{row['skill_id']}",
        }
    allowed = contract.validate_result(accepted)
    pending_completion = contract.validate_completion(accepted)
    accepted["epoch_header"]["epoch_lock"] = {
        "lock_id": "LOCK-FCE-20260726-01",
        "evidence_pointer": "docs/validation/skill-pack/FCE-20260726-01/lock.json",
    }
    complete = contract.validate_completion(accepted)
    forbidden = deepcopy(frozen)
    forbidden["epoch_header"]["integration_result"] = {
        "decision": "recommended",
        "evidence_pointer": "somewhere",
    }

    assert missing["status"] == "result-pending"
    assert premature["status"] == "result-invalid"
    assert allowed["status"] == "result-valid"
    assert allowed["decision"] == "integration-accepted"
    assert pending_completion["status"] == "completion-pending"
    assert complete["status"] == "completion-valid"
    assert contract.validate_result(forbidden)["status"] == "result-invalid"
    assert not hasattr(contract, "set_result")

    inconsistent = deepcopy(frozen)
    inconsistent["epoch_header"]["status"] = "integration-accepted"
    inconsistent["epoch_header"]["integration_result"] = {
        "decision": "blocked",
        "evidence_pointer": "proof://blocked",
    }
    assert contract.validate_result(inconsistent)["status"] == "result-invalid"

    empty_acceptance = deepcopy(accepted)
    empty_acceptance["epoch_header"]["epoch_lock"] = {
        "lock_id": "",
        "evidence_pointer": "",
    }
    empty_acceptance["selected_skills"][0]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": None,
        "terminal_evidence_pointer": "",
    }
    assert contract.validate_result(empty_acceptance)["status"] == "result-invalid"

    premature_draft = valid_contract()
    premature_draft["epoch_header"]["integration_result"] = {
        "decision": "blocked",
        "evidence_pointer": "proof://premature",
    }
    premature_draft["epoch_header"]["epoch_lock"] = {
        "lock_id": "LOCK-PREMATURE",
        "evidence_pointer": "proof://premature-lock",
    }
    assert contract.freeze_contract(premature_draft)["status"] == "contract-invalid"


def test_freeze_enforces_schema_collision_and_graph_parity() -> None:
    contract = pack_contract()
    missing_vocabulary = valid_contract()
    missing_vocabulary["exclusions_collisions_gaps"] = [
        issue
        for issue in missing_vocabulary["exclusions_collisions_gaps"]
        if issue["class"] != "vocabulary"
    ]
    missing_result = contract.freeze_contract(missing_vocabulary)
    assert missing_result["status"] == "contract-invalid"
    assert "vocabulary" in "\n".join(missing_result["failures"])

    missing_field = valid_contract()
    del missing_field["selected_skills"][0]["completion_condition"]
    assert contract.freeze_contract(missing_field)["status"] == "contract-invalid"

    extra_authority = valid_contract()
    extra_authority["selected_skills"][0]["h1_candidate"] = "candidate"
    assert contract.freeze_contract(extra_authority)["status"] == "contract-invalid"

    deferred_collision = valid_contract()
    deferred_collision["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "authority",
            "essential": True,
            "involved_skill_ids": ["SK-001", "SK-002"],
            "involved_capability_ids": ["CAP-002"],
            "terms": [],
            "observable_conflict": "Two final owners",
            "governing_owner": "pack owner",
            "resolution": None,
            "negative_control_scenario_id": "PS-001",
            "status": "deferred",
            "future_owner_or_stopping_condition": "future owner",
            "nondependency_proof_ids": ["PROOF-NONDEP"],
        }
    )
    assert (
        contract.freeze_contract(deferred_collision)["status"]
        == "contract-invalid"
    )

    missing_edge = valid_contract()
    missing_edge["epoch_header"]["campaign_proof_graph"] = [
        missing_edge["epoch_header"]["campaign_proof_graph"][1]
    ]
    result = contract.freeze_contract(missing_edge)
    assert result["status"] == "contract-invalid"
    assert "relationship ordering" in "\n".join(result["failures"])

    unknown_scenario = valid_contract()
    unknown_scenario["selected_skills"][0]["acceptance_scenario_ids"] = [
        "PS-999"
    ]
    assert contract.freeze_contract(unknown_scenario)["status"] == (
        "contract-invalid"
    )
    duplicate_scenario = valid_contract()
    duplicate_scenario["epoch_header"]["acceptance_scenarios"].append(
        deepcopy(
            duplicate_scenario["epoch_header"]["acceptance_scenarios"][0]
        )
    )
    assert contract.freeze_contract(duplicate_scenario)["status"] == (
        "contract-invalid"
    )
    dangling_negative = valid_contract()
    dangling_negative["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "gap",
            "essential": False,
            "involved_skill_ids": ["SK-003"],
            "involved_capability_ids": ["CAP-003"],
            "terms": [],
            "observable_conflict": "Resolved gap",
            "governing_owner": "pack owner",
            "resolution": "resolved",
            "negative_control_scenario_id": "PS-999",
            "status": "resolved",
            "future_owner_or_stopping_condition": None,
            "nondependency_proof_ids": [],
        }
    )
    assert contract.freeze_contract(dangling_negative)["status"] == (
        "contract-invalid"
    )
    preseeded = valid_contract()
    preseeded["selected_skills"][0]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": "forged-campaign",
        "terminal_evidence_pointer": "proof://forged",
    }
    assert contract.freeze_contract(preseeded)["status"] == "contract-invalid"


def test_slice_recruits_only_relevant_scenarios_and_exit_owners() -> None:
    contract = pack_contract()
    draft = valid_contract()
    draft["epoch_header"]["acceptance_scenarios"].append(
        {
            "scenario_id": "PS-002",
            "description": "Unrelated router scenario",
            "expected_owner_skill_id": "SK-003",
        }
    )
    draft["epoch_header"]["acceptance_scenarios"].append(
        {
            "scenario_id": "PS-003",
            "description": "Issue-only negative control",
            "expected_owner_skill_id": "SK-001",
        }
    )
    draft["capabilities"][1]["acceptance_scenario_ids"].append("PS-002")
    draft["exclusions_collisions_gaps"].append(
        {
            "issue_id": "ECG-001",
            "class": "gap",
            "essential": False,
            "involved_skill_ids": ["SK-002"],
            "involved_capability_ids": ["CAP-002"],
            "terms": [],
            "observable_conflict": "Aggregate negative control",
            "governing_owner": "pack owner",
            "resolution": "resolved",
            "negative_control_scenario_id": "PS-003",
            "status": "resolved",
            "future_owner_or_stopping_condition": None,
            "nondependency_proof_ids": [],
        }
    )
    draft["relationships"][0]["combined_exit_owner_skill_id"] = "SK-003"
    frozen = contract.freeze_contract(draft)["contract"]

    frozen["selected_skills"][0]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": "campaign-SK-001",
        "terminal_evidence_pointer": "proof://provider",
    }
    projected = contract.contract_slice(frozen, "SK-002")["slice"]

    assert [
        scenario["scenario_id"]
        for scenario in projected["acceptance_scenarios"]
    ] == ["PS-001", "PS-002", "PS-003"]
    frozen["selected_skills"][1]["campaign_state"] = {
        "status": "terminal",
        "campaign_id": "campaign-SK-002",
        "terminal_evidence_pointer": "proof://aggregate",
    }
    exit_projection = contract.contract_slice(frozen, "SK-003")["slice"]
    assert [
        row["relationship_id"] for row in exit_projection["relationships"]
    ] == ["REL-001"]


def test_repository_owner_and_registered_schema_are_valid() -> None:
    root = Path(__file__).resolve().parents[1]

    assert pack_contract().validate_repository(root) == []
