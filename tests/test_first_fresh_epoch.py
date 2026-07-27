"""Acceptance proof for the first frozen Fresh Composition Epoch contract."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

import yaml

from scripts import pack_contract
from scripts import research_catalog


ROOT = Path(__file__).resolve().parents[1]
EPOCH = "FCE-20260727-01"
EPOCH_RESEARCH = (
    ROOT / "docs/research/skill-pack-composition/epochs" / EPOCH
)


def test_independent_discovery_packet_precedes_catalog_reconciliation() -> None:
    fixed_point = json.loads(
        (EPOCH_RESEARCH / "pre-discovery-fixed-point.json").read_text(
            encoding="utf-8"
        )
    )
    packet = json.loads(
        (EPOCH_RESEARCH / "independent-discovery.json").read_text(
            encoding="utf-8"
        )
    )
    reconciliation = json.loads(
        (EPOCH_RESEARCH / "catalog-reconciliation.json").read_text(
            encoding="utf-8"
        )
    )

    fixed_point_payload = {
        key: value
        for key, value in fixed_point.items()
        if key != "fixed_point_fingerprint"
    }
    recorded = research_catalog.record_independent_packet(
        packet,
        fixed_point["fixed_point_fingerprint"],
    )
    catalog = json.loads(
        (
            ROOT / "docs/research/skill-pack-composition/catalog.json"
        ).read_text(encoding="utf-8")
    )
    rejected = research_catalog.open_catalog(
        recorded["session"],
        "sha256-v1:" + "0" * 64,
    )
    opened = research_catalog.open_catalog(
        recorded["session"],
        packet["fingerprint"],
    )
    queried = research_catalog.query_catalog(
        cards={},
        catalog=catalog,
        session=opened["session"],
        query=reconciliation["query"],
    )
    completed = research_catalog.complete_session(queried["session"])

    assert recorded["status"] == "independent-recorded"
    assert fixed_point["fixed_point_fingerprint"] == (
        research_catalog.exact_fingerprint(fixed_point_payload)
    )
    assert packet["pre_discovery_fixed_point_fingerprint"] == (
        fixed_point["fixed_point_fingerprint"]
    )
    assert rejected["status"] == "catalog-not-admitted"
    assert opened["status"] == "catalog-open"
    assert queried["status"] == "catalog-results"
    assert queried["groups"] == {"exact": [], "close": [], "related": []}
    assert completed["status"] == "workflow-complete"
    assert (
        reconciliation["independent_packet_fingerprint"]
        == packet["fingerprint"]
    )
    assert reconciliation["catalog_opened_after_independent_record"] is True
    assert reconciliation["reconciliation_passes"] == 1
    assert reconciliation["named_gap_passes"] == 0
    assert reconciliation["cards_loaded"] == 0
    assert reconciliation["result"] == "catalog-results"
    assert reconciliation["discovery_sequence"] == [
        {
            "fingerprint": fixed_point["fixed_point_fingerprint"],
            "kind": "pre-discovery-fixed-point",
            "sequence": 1,
        },
        {
            "fingerprint": packet["fingerprint"],
            "kind": "independent-discovery",
            "sequence": 2,
        },
        {
            "fingerprint": catalog["catalog_fixed_point"],
            "kind": "catalog-open",
            "sequence": 3,
        },
    ]


def test_first_epoch_contract_freezes_complete_h1_free_composition() -> None:
    content = (ROOT / "docs/synthesis/skill-pack.md").read_text(
        encoding="utf-8"
    )
    contract = pack_contract.parse_contract(content)
    fixed_point = json.loads(
        (EPOCH_RESEARCH / "pre-discovery-fixed-point.json").read_text(
            encoding="utf-8"
        )
    )
    selected_names = {
        skill["canonical_name"] for skill in contract["selected_skills"]
    }
    active_names = {
        path.parent.name
        for path in (ROOT / "skills/custom").glob("*/SKILL.md")
    }

    assert pack_contract.validate_contract(contract) == []
    assert contract["epoch_header"]["composition_epoch_id"] == EPOCH
    assert contract["epoch_header"]["contract_revision"] == 2
    assert contract["epoch_header"]["status"] == "frozen"
    assert contract["epoch_header"]["integration_result"] == {
        "decision": None,
        "evidence_pointer": None,
    }
    assert contract["epoch_header"]["epoch_lock"] is None
    assert contract["epoch_header"]["intended_pack_outcome"] == (
        fixed_point["intended_pack_outcome"]
    )
    assert contract["epoch_header"]["scope"] == fixed_point["scope"]
    assert contract["epoch_header"]["research_bound"] == (
        fixed_point["research_bound"]
    )
    assert contract["epoch_header"]["load_budget_policy"] == {
        **fixed_point["load_budget_policy"],
        "status": "set",
    }
    environment = contract["epoch_header"]["fixed_point"]["environment"]
    assert all(
        identity in environment
        for identity in (
            "model=gpt-5.6-sol",
            "reasoning_effort=medium",
            "thread_id=019f9c92-07fb-7b80-b8a2-a218bbfd9a1f",
            "python=3.12.12",
        )
    )
    assert contract["epoch_header"]["source_pointers"][0] == (
        "docs/research/skill-pack-composition/epochs/"
        f"{EPOCH}/pre-discovery-fixed-point.json#"
        f"{fixed_point['fixed_point_fingerprint']}"
    )
    assert selected_names == active_names
    assert len(contract["capabilities"]) == len(selected_names) == 24
    assert {
        skill["primary_role"] for skill in contract["selected_skills"]
    } == {"leaf", "executable-aggregate", "router"}
    assert sum(
        skill["primary_role"] == "router"
        for skill in contract["selected_skills"]
    ) == 1
    assert all(
        issue["status"] == "resolved"
        for issue in contract["exclusions_collisions_gaps"]
    )
    assert pack_contract.REQUIRED_COLLISION_CLASSES <= {
        issue["class"] for issue in contract["exclusions_collisions_gaps"]
    }


def test_first_epoch_schedule_matches_every_immutable_blueprint() -> None:
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    schedule = json.loads(
        (
            ROOT / "docs/validation/skill-pack" / EPOCH / "schedule.json"
        ).read_text(encoding="utf-8")
    )
    entries = schedule["campaign_order"]
    skill_by_id = {
        skill["skill_id"]: skill for skill in contract["selected_skills"]
    }

    assert schedule["contract_fingerprint"] == (
        pack_contract.contract_fingerprint(contract)
    )
    assert [entry["skill_id"] for entry in entries] == (
        pack_contract.campaign_order(contract)
    )
    assert [entry["tier"] for entry in entries] == sorted(
        (entry["tier"] for entry in entries),
        key={
            "leaf-provider": 0,
            "executable-aggregate": 1,
            "router": 2,
        }.__getitem__,
    )
    assert len(entries) == len(skill_by_id) == 24
    for entry in entries:
        blueprint = json.loads(
            (ROOT / entry["slice_path"]).read_text(encoding="utf-8")
        )
        projected = pack_contract.contract_blueprint(
            contract,
            entry["skill_id"],
        )
        assert blueprint == projected
        assert entry["slice_fingerprint"] == projected["slice_fingerprint"]
        assert entry["predecessor_skill_ids"] == (
            projected["predecessor_skill_ids"]
        )
        assert blueprint["slice"]["skill"] == skill_by_id[entry["skill_id"]]


def test_first_epoch_invocation_and_relationship_parity() -> None:
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    skill_by_id = {
        skill["skill_id"]: skill for skill in contract["selected_skills"]
    }
    id_by_name = {
        skill["canonical_name"]: skill["skill_id"]
        for skill in contract["selected_skills"]
    }
    for name, skill_id in id_by_name.items():
        metadata = yaml.safe_load(
            (
                ROOT / "skills/custom" / name / "agents/openai.yaml"
            ).read_text(encoding="utf-8")
        )
        implicit = bool(
            metadata.get("policy", {}).get("allow_implicit_invocation")
        )
        assert skill_by_id[skill_id]["invocation_mode"] == (
            "implicit" if implicit else "explicit-only"
        )

    relationship_text = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    runtime_table = relationship_text.split("## Runtime Composition", 1)[1]
    runtime_table = runtime_table.split("The accepted future", 1)[0]
    expected_runtime: set[tuple[str, str, str, str]] = set()
    pattern = re.compile(
        r"^\| `([^`]+)` \| ([^|]+?) \| `\$([^`]+)` \| (.+) \|$"
    )
    for line in runtime_table.splitlines():
        match = pattern.match(line)
        if match is None:
            continue
        caller = match.group(1).replace(" finding contract", "")
        expected_runtime.add(
            (
                caller,
                match.group(2).strip().replace("`", ""),
                match.group(3),
                match.group(4),
            )
        )
    actual_runtime = {
        (
            skill_by_id[row["caller_skill_id"]]["canonical_name"],
            row["verb"],
            skill_by_id[row["target_skill_id"]]["canonical_name"],
            row["entry_condition"],
        )
        for row in contract["relationships"]
        if row["caller_skill_id"] != id_by_name["skill-router"]
    }
    router_rows = [
        row
        for row in contract["relationships"]
        if row["caller_skill_id"] == id_by_name["skill-router"]
    ]

    assert actual_runtime == expected_runtime
    assert {row["target_skill_id"] for row in router_rows} == (
        set(skill_by_id) - {id_by_name["skill-router"]}
    )
    assert {row["verb"] for row in router_rows} == {"Recommend and stop"}
