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
    assert contract["epoch_header"]["contract_revision"] == 4
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


def test_first_epoch_revision_preserves_r2_and_derives_r3_blueprints() -> None:
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    historical_schedule = json.loads(
        (
            ROOT / "docs/validation/skill-pack" / EPOCH / "schedule.json"
        ).read_text(encoding="utf-8")
    )
    skill_by_id = {
        skill["skill_id"]: skill for skill in contract["selected_skills"]
    }

    historical_entries = historical_schedule["campaign_order"]
    assert historical_schedule["contract_fingerprint"] != (
        pack_contract.contract_fingerprint(contract)
    )
    assert all(
        entry["slice_path"].startswith(
            f"docs/validation/skill-pack/{EPOCH}/slices/"
        )
        for entry in historical_entries
    )
    assert {"review", "convergent-pr-review"} <= {
        entry["canonical_name"] for entry in historical_entries
    }

    order = pack_contract.campaign_order(contract)
    assert len(order) == len(skill_by_id) == 24
    for skill_id in order:
        projected = pack_contract.contract_blueprint(
            contract,
            skill_id,
        )
        assert projected["slice"]["slice_id"].startswith(
            f"{EPOCH}:r4:"
        )
        assert projected["slice"]["skill"] == skill_by_id[skill_id]
    assert {
        skill_by_id["SK-014"]["canonical_name"],
        skill_by_id["SK-015"]["canonical_name"],
    } == {"change-review", "high-assurance-review"}


def test_current_topology_materializes_the_post_freeze_amendment() -> None:
    contract = pack_contract.parse_contract(
        (ROOT / "docs/synthesis/skill-pack.md").read_text(encoding="utf-8")
    )
    skill_by_name = {
        skill["canonical_name"]: skill for skill in contract["selected_skills"]
    }
    assert contract["epoch_header"]["status"] == "frozen"
    assert contract["epoch_header"]["contract_revision"] == 4
    assert skill_by_name["high-assurance-review"]["invocation_mode"] == "explicit-only"
    assert "user explicitly invokes" in (
        skill_by_name["high-assurance-review"]["positive_entry_predicate"]
    )
    assert "release candidate, or supported-risk" in (
        skill_by_name["change-review"]["positive_entry_predicate"]
    )
    assert "REL-013" not in skill_by_name["implement"]["relationship_ids"]
    assert "REL-030" not in skill_by_name["parallel-implement"]["relationship_ids"]
    assert "REL-049" not in skill_by_name["skill-router"]["relationship_ids"]

    relationship_ids = {
        relationship["relationship_id"] for relationship in contract["relationships"]
    }
    assert {"REL-013", "REL-030", "REL-049"}.isdisjoint(relationship_ids)
    graph_edges = {
        (edge["predecessor_skill_id"], edge["successor_skill_id"])
        for edge in contract["epoch_header"]["campaign_proof_graph"]
    }
    assert not any(predecessor == "SK-014" for predecessor, _ in graph_edges)

    contract_text = (
        ROOT / "docs/synthesis/skill-pack.md"
    ).read_text(encoding="utf-8")
    amendment = contract_text.split("Revision 16", 1)[1].split(
        "It binds the complete fingerprinted", 1
    )[0]
    amendment_flat = " ".join(amendment.split())
    assert "machine contract revision 4" in amendment_flat
    assert "High-Assurance Review explicit" in amendment
    assert "Direct Implement requires a commit only" in amendment
    assert "dispatch economics change concurrency, not campaign custody" in amendment_flat

    metadata = yaml.safe_load(
        (
            ROOT
            / "skills/custom/high-assurance-review/agents/openai.yaml"
        ).read_text(encoding="utf-8")
    )
    assert metadata["policy"]["allow_implicit_invocation"] is False

    adr = (
        ROOT
        / "docs/adr/0013-automatic-implementation-review-uses-one-change-review-path.md"
    ).read_text(encoding="utf-8")
    assert "**Status**: accepted" in adr
    assert "High-Assurance Review is explicit-only" in adr

    relationships = (
        ROOT / "docs/synthesis/skill-context-relationships.md"
    ).read_text(encoding="utf-8")
    assert "| `implement` | Invoke | `$change-review` |" in relationships
    assert "| `parallel-implement` | Invoke | `$change-review` |" in relationships
    assert "| `implement` | Invoke | `$high-assurance-review` |" not in relationships
    assert "| `parallel-implement` | Invoke | `$high-assurance-review` |" not in relationships
    assert "| `wayfinder` | Recommend and stop | `$implement` |" in relationships
    assert "| `to-spec` | Recommend and stop | `$implement` |" in relationships
