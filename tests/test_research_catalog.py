from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from scripts import validate_skills


def catalog_module():
    spec = importlib.util.find_spec("scripts.research_catalog")
    assert spec is not None, "scripts.research_catalog must expose the catalog seam"
    return importlib.import_module("scripts.research_catalog")


def fingerprint(payload: dict[str, object]) -> str:
    content = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256-v1:{hashlib.sha256(content).hexdigest()}"


def independent_packet() -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": 1,
        "packet_id": "M0-alpha-independent",
        "pre_discovery_fixed_point_fingerprint": "sha256-v1:" + "f" * 64,
        "intended_essence": "Bounded evidence discovery",
        "m0_units": ["Retrieve relevant evidence after independent discovery"],
        "failures": ["Catalog anchoring"],
        "discovered_methods": ["Problem-first retrieval"],
        "alternatives": ["Direct source search"],
        "counterpressure": ["Catalog vocabulary can narrow discovery"],
        "wrong_conditions": ["The problem has no reusable evidence dimension"],
        "unresolved_named_gaps": ["Whether one authority boundary is reusable"],
    }
    return {**payload, "fingerprint": fingerprint(payload)}


def source_fixed_point() -> dict[str, str]:
    return {
        "revision": "accepted",
        "date": "2026-07-25",
        "version": "1",
        "jurisdiction": "repository",
        "population": "Fresh Composition Epoch",
        "method": "accepted ADR",
    }


def valid_card(
    card_id: str = "RC-0001",
    *,
    preferred_label: str = "Problem-first retrieval",
    alternative_labels: list[str] | None = None,
    hidden_labels: list[str] | None = None,
    relations: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "card_id": card_id,
        "preferred_label": preferred_label,
        "alternative_labels": alternative_labels or ["Failure-first retrieval"],
        "hidden_labels": hidden_labels or ["problem first search"],
        "record_state": "verified",
        "behavior": "Query evidence by the problem before known methods.",
        "failure_prevented": "Catalog anchoring",
        "recruited_behavior": "Independent discovery precedes catalog lookup",
        "scope_note": "Applies to bounded local evidence reconciliation.",
        "applicability_conditions": ["Independent packet exists"],
        "counterconditions": ["No reusable evidence dimension exists"],
        "wrong_condition": "The caller is performing the independent pass.",
        "method_evidence": "independently-supported",
        "claims": [
            {
                "claim_id": f"{card_id}-C01",
                "statement": "Problem-first ordering reduces catalog seeding.",
                "status": "supported",
                "source_ids": ["SRC-0001"],
                "counterevidence": [],
                "applicability": ["Local catalog follows independent discovery"],
                "limits": ["Does not prove wording efficacy"],
            }
        ],
        "sources": [
            {
                "source_id": "SRC-0001",
                "authority_class": "governing-local",
                "locator": "docs/adr/0009-fresh-composition-epochs-revalidate-skill-pack-knowledge.md",
                "fixed_point": source_fixed_point(),
                "inspected_anchors": ["Fresh Composition Epoch decision"],
                "accessed_at": "2026-07-26",
                "access_depth": "full",
                "limits": ["Local governing decision"],
            }
        ],
        "verified_at": "2026-07-26T00:00:00Z",
        "refresh_triggers": ["governing-version-changed"],
        "relations": relations or [],
        "dimensions": {
            "problems": ["catalog anchoring"],
            "behaviors": ["independent discovery precedes catalog lookup"],
            "conditions": ["independent packet exists"],
            "roles": ["researcher"],
            "lifecycle_stages": ["catalog reconciliation"],
            "source_classes": ["governing-local"],
            "relationships": ["research-to-synthesis"],
        },
        "unknowns": ["Transfer to other catalogs"],
        "claim_limits": ["Evidence does not admit H1"],
    }


def write_card(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        "---\n"
        + yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
        + "---\n\n# "
        + str(payload["preferred_label"])
        + "\n",
        encoding="utf-8",
    )


def opened_session(catalog) -> dict[str, object]:
    packet = independent_packet()
    recorded = catalog.record_independent_packet(
        packet,
        packet["pre_discovery_fixed_point_fingerprint"],
    )
    return catalog.open_catalog(
        recorded["session"],
        packet["fingerprint"],
    )["session"]


def query(problem: str = "Catalog anchoring", maximum: int = 3) -> dict[str, object]:
    payload: dict[str, object] = {
        "problem": problem,
        "conditions": ["independent packet exists"],
        "exclusions": [],
        "method_evidence": ["independently-supported"],
        "freshness": ["verified-for-fixed-point"],
        "refresh_events": [],
        "source_fixed_points": {
            "SRC-0001": fingerprint(source_fixed_point()),
        },
        "known_terms": [],
        "maximum_families": maximum,
    }
    payload["application_fixed_point"] = fingerprint(
        {
            "conditions": payload["conditions"],
            "exclusions": payload["exclusions"],
            "role": None,
            "lifecycle_stage": None,
        }
    )
    return payload


def catalog_records(
    tmp_path: Path,
    payloads: list[dict[str, object]],
):
    catalog = catalog_module()
    records: list[dict[str, object]] = []
    for payload in payloads:
        path = tmp_path / f"{payload['card_id']}.md"
        write_card(path, payload)
        records.append(catalog.parse_card(path, root=tmp_path))
    return catalog, records


def write_catalog_contract_root(root: Path) -> None:
    catalog = catalog_module()
    card_root = root / "docs/research/skill-pack-composition/cards"
    card_root.mkdir(parents=True)
    owner = root / "docs/research/skill-pack-composition/README.md"
    owner.write_text(
        "scripts.research_catalog\n"
        "catalog-not-admitted\n"
        "catalog-overflow\n"
        "docs/research/skill-pack-composition/catalog.json\n",
        encoding="utf-8",
    )
    schemas = []
    for (schema_id, version), relative in catalog.REQUIRED_SCHEMAS.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(Path(relative).read_bytes())
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas.append(
            {
                "id": schema_id,
                "version": version,
                "path": relative,
                "fingerprint": fingerprint(schema),
            }
        )
    registry = root / catalog.SCHEMA_REGISTRY
    registry.write_text(
        json.dumps({"format": 1, "schemas": schemas}),
        encoding="utf-8",
    )
    fixture = root / catalog.VALID_FIXTURE
    fixture.parent.mkdir(parents=True)
    write_card(fixture, valid_card("RC-9001"))
    packet_fixture = root / catalog.INDEPENDENT_PACKET_FIXTURE
    packet_fixture.parent.mkdir(parents=True)
    packet_fixture.write_bytes(
        Path(catalog.INDEPENDENT_PACKET_FIXTURE).read_bytes()
    )
    catalog.write_catalog(
        root,
        generated_at="2026-07-26T00:00:00Z",
    )


def test_catalog_is_sequestered_until_independent_packet_fingerprint() -> None:
    catalog = catalog_module()
    packet = independent_packet()
    recorded = catalog.record_independent_packet(
        packet,
        packet["pre_discovery_fixed_point_fingerprint"],
    )

    assert recorded["status"] == "independent-recorded"
    session = recorded["session"]
    wrong_predecessor = catalog.record_independent_packet(
        packet,
        "sha256-v1:" + "0" * 64,
    )
    assert wrong_predecessor["status"] == "independent-packet-invalid"
    early = catalog.query_catalog(
        cards={},
        catalog={"entries": []},
        session=session,
        query={"problem": "Catalog anchoring", "maximum_families": 1},
    )
    assert early["status"] == "catalog-not-admitted"
    assert early["session"] == session

    wrong = catalog.open_catalog(session, "sha256-v1:" + "0" * 64)
    assert wrong["status"] == "catalog-not-admitted"

    opened = catalog.open_catalog(session, independent_packet()["fingerprint"])
    assert opened["status"] == "catalog-open"
    assert opened["session"]["phase"] == "catalog-open"

    seeded_packet = independent_packet()
    seeded_packet["historical_card_ids"] = ["RC-0001"]
    seeded_payload = {
        key: value for key, value in seeded_packet.items() if key != "fingerprint"
    }
    seeded_packet["fingerprint"] = fingerprint(seeded_payload)

    rejected = catalog.record_independent_packet(
        seeded_packet,
        seeded_packet["pre_discovery_fixed_point_fingerprint"],
    )

    assert rejected["status"] == "historical-seed-rejected"

    no_gap_packet = independent_packet()
    no_gap_packet["unresolved_named_gaps"] = []
    no_gap_payload = {
        key: value for key, value in no_gap_packet.items() if key != "fingerprint"
    }
    no_gap_packet["fingerprint"] = fingerprint(no_gap_payload)
    assert (
        catalog.record_independent_packet(
            no_gap_packet,
            no_gap_packet["pre_discovery_fixed_point_fingerprint"],
        )["status"]
        == "independent-recorded"
    )

    forged = {
        "phase": "catalog-open",
        "independent_packet_fingerprint": independent_packet()["fingerprint"],
        "reconciliation_passes": 0,
        "gap_passes": 0,
    }
    assert (
        catalog.open_catalog(forged, independent_packet()["fingerprint"])[
            "status"
        ]
        == "catalog-not-admitted"
    )
    assert (
        catalog.query_catalog(
            cards={},
            catalog=catalog.build_catalog(
                [],
                generated_at="2026-07-26T00:00:00Z",
            ),
            session=forged,
            query=query(),
        )["status"]
        == "catalog-not-admitted"
    )
    forged_from_valid = deepcopy(session)
    forged_from_valid["phase"] = "catalog-open"
    assert (
        catalog.query_catalog(
            cards={},
            catalog=catalog.build_catalog(
                [],
                generated_at="2026-07-26T00:00:00Z",
            ),
            session=forged_from_valid,
            query=query(),
        )["status"]
        == "catalog-not-admitted"
    )


def test_card_contract_and_thin_catalog_are_deterministic(tmp_path: Path) -> None:
    catalog = catalog_module()
    card_path = tmp_path / "cards/RC-0001.md"
    card_path.parent.mkdir()
    write_card(card_path, valid_card())

    record = catalog.parse_card(card_path, root=tmp_path)
    first = catalog.build_catalog(
        [record],
        generated_at="2026-07-26T00:00:00Z",
    )
    second = catalog.build_catalog(
        [record],
        generated_at="2026-07-26T00:00:00Z",
    )

    assert first == second
    assert first["entries"][0]["freshness_state"] == "unknown"
    assert first["entries"][0]["card_id"] == "RC-0001"
    assert first["entries"][0]["fingerprint"] == record["fingerprint"]
    serialized = json.dumps(first).casefold()
    for forbidden in (
        "adoption",
        "h1",
        "recommendation",
        "validation_result",
        "popularity",
        "confidence",
        "claim narratives",
    ):
        assert forbidden not in serialized
    assert "claims" not in first["entries"][0]
    assert "sources" not in first["entries"][0]

    with pytest.raises(catalog.CardContractError, match="fingerprint"):
        catalog.parse_card(
            card_path,
            root=tmp_path,
            expected_fingerprint="sha256-v1:" + "0" * 64,
        )


def test_card_contract_rejects_alias_relation_and_authority_violations(
    tmp_path: Path,
) -> None:
    catalog = catalog_module()
    path = tmp_path / "RC-0001.md"
    payload = valid_card(
        alternative_labels=["Collision"],
        hidden_labels=["collision"],
        relations=[{"type": "recommends", "target_card_id": "RC-0002"}],
    )
    payload["adoption"] = "selected"
    payload["sources"][0]["locator"] = "docs/research/sources/private.md"  # type: ignore[index]
    write_card(path, payload)

    with pytest.raises(catalog.CardContractError) as error:
        catalog.parse_card(path, root=tmp_path)

    message = str(error.value)
    assert "disjoint" in message
    assert "relation type" in message
    assert "forbidden authority field" in message
    assert "private source locator" in message


@pytest.mark.parametrize(
    "locator",
    [
        "Sources/private.md",
        "./sources/private.md",
        r"C:\private\sources\private.md",
        "file:///C:/private/sources/private.md",
    ],
)
def test_card_contract_rejects_private_locator_aliases(
    tmp_path: Path,
    locator: str,
) -> None:
    catalog = catalog_module()
    path = tmp_path / "RC-0001.md"
    payload = valid_card()
    payload["sources"][0]["locator"] = locator  # type: ignore[index]
    write_card(path, payload)

    with pytest.raises(catalog.CardContractError, match="private source locator"):
        catalog.parse_card(path, root=tmp_path)


def test_query_groups_exact_close_related_without_ranking(
    tmp_path: Path,
) -> None:
    one = valid_card(
        "RC-0001",
        relations=[
            {"type": "close-match", "target_card_id": "RC-0002"},
            {"type": "related", "target_card_id": "RC-0003"},
        ],
    )
    two = valid_card(
        "RC-0002",
        preferred_label="Failure-first retrieval",
        alternative_labels=["Weakness-first retrieval"],
        hidden_labels=["failure first search"],
    )
    two["failure_prevented"] = "Vocabulary-led discovery"
    two["dimensions"]["problems"] = ["vocabulary-led discovery"]  # type: ignore[index]
    three = valid_card(
        "RC-0003",
        preferred_label="Bounded reconciliation",
        alternative_labels=["Finite reconciliation"],
        hidden_labels=["one pass reconciliation"],
    )
    three["failure_prevented"] = "Unbounded catalog search"
    three["dimensions"]["problems"] = ["unbounded catalog search"]  # type: ignore[index]
    four = valid_card(
        "RC-0004",
        preferred_label="Unrelated method",
        alternative_labels=["Different method"],
        hidden_labels=["unrelated"],
    )
    four["failure_prevented"] = "Different failure"
    four["dimensions"]["problems"] = ["different failure"]  # type: ignore[index]
    catalog, records = catalog_records(tmp_path, [four, three, one, two])
    index = catalog.build_catalog(
        records,
        generated_at="2026-07-26T00:00:00Z",
    )
    cards = {record["card"]["card_id"]: record for record in records}

    result = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=query(),
    )

    assert result["status"] == "catalog-results"
    assert [item["card_id"] for item in result["groups"]["exact"]] == ["RC-0001"]
    assert [item["card_id"] for item in result["groups"]["close"]] == ["RC-0002"]
    assert [item["card_id"] for item in result["groups"]["related"]] == ["RC-0003"]
    assert result["cards_loaded"] == 3
    assert result["tree_scans"] == 0
    returned_ids = {
        item["card_id"]
        for group in result["groups"].values()
        for item in group
    }
    assert "RC-0004" not in returned_ids
    repeat = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=query(),
    )
    assert repeat == result
    serialized = json.dumps(result).casefold()
    for forbidden in ("popularity", "confidence_score", "recommendation_rank"):
        assert forbidden not in serialized


def test_query_overflow_and_alias_collision_never_choose_or_truncate(
    tmp_path: Path,
) -> None:
    one = valid_card(
        "RC-0001",
        alternative_labels=["Collision"],
        relations=[
            {"type": "close-match", "target_card_id": "RC-0002"},
            {"type": "related", "target_card_id": "RC-0003"},
        ],
    )
    two = valid_card(
        "RC-0002",
        preferred_label="Failure-first retrieval",
        alternative_labels=["Weakness-first retrieval"],
        hidden_labels=["failure first search"],
    )
    three = valid_card(
        "RC-0003",
        preferred_label="Bounded reconciliation",
        alternative_labels=["Collision"],
        hidden_labels=["one pass reconciliation"],
    )
    catalog, records = catalog_records(tmp_path, [one, two, three])
    index = catalog.build_catalog(
        records,
        generated_at="2026-07-26T00:00:00Z",
    )
    cards = {record["card"]["card_id"]: record for record in records}

    overflow = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=query(maximum=1),
    )

    assert overflow["status"] == "catalog-overflow"
    assert overflow["eligible_families"] == 3
    assert overflow["cards_loaded"] == 0
    assert overflow["groups"] == {"exact": [], "close": [], "related": []}
    assert overflow["narrowing_dimensions"]

    ambiguous_query = query(maximum=3)
    ambiguous_query["known_terms"] = ["collision"]
    ambiguous = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=ambiguous_query,
    )

    assert ambiguous["status"] == "catalog-ambiguous"
    assert ambiguous["cards_loaded"] == 0
    assert [item["card_id"] for item in ambiguous["candidates"]] == [
        "RC-0001",
        "RC-0003",
    ]
    assert all(item["scope_note"] for item in ambiguous["candidates"])


def test_query_requires_explicit_problem_first_bound(tmp_path: Path) -> None:
    catalog = catalog_module()
    session = opened_session(catalog)

    missing_bound = catalog.query_catalog(
        cards={},
        catalog={"entries": []},
        session=session,
        query={
            "problem": "Catalog anchoring",
            "conditions": [],
            "exclusions": [],
        },
    )
    known_method_only = catalog.query_catalog(
        cards={},
        catalog={"entries": []},
        session=session,
        query={
            "known_terms": ["problem-first retrieval"],
            "conditions": [],
            "exclusions": [],
            "maximum_families": 1,
        },
    )

    assert missing_bound["status"] == "catalog-query-invalid"
    assert known_method_only["status"] == "catalog-query-invalid"

    malformed = query()
    malformed["method_evidence"] = [17]
    assert (
        catalog.query_catalog(
            cards={},
            catalog=catalog.build_catalog(
                [],
                generated_at="2026-07-26T00:00:00Z",
            ),
            session=session,
            query=malformed,
        )["status"]
        == "catalog-query-invalid"
    )


def test_catalog_rejects_tampered_or_incomplete_derived_entries(
    tmp_path: Path,
) -> None:
    one = valid_card()
    two = valid_card(card_id="RC-0002")
    catalog, records = catalog_records(tmp_path, [one, two])
    index = catalog.build_catalog(
        records,
        generated_at="2026-07-26T00:00:00Z",
    )
    cards = {record["card"]["card_id"]: record for record in records}

    incomplete = deepcopy(index)
    incomplete["entries"].pop()
    assert (
        catalog.query_catalog(
            cards=cards,
            catalog=incomplete,
            session=opened_session(catalog),
            query=query(),
        )["status"]
        == "catalog-incompatible"
    )

    tampered = deepcopy(index)
    tampered["entries"][1]["canonical_family_id"] = "RC-0001"
    assert (
        catalog.query_catalog(
            cards=cards,
            catalog=tampered,
            session=opened_session(catalog),
            query=query(),
        )["status"]
        == "catalog-incompatible"
    )


def test_conditions_and_application_identity_fail_closed(tmp_path: Path) -> None:
    catalog, records = catalog_records(tmp_path, [valid_card()])
    index = catalog.build_catalog(
        records,
        generated_at="2026-07-26T00:00:00Z",
    )
    cards = {record["card"]["card_id"]: record for record in records}

    mismatched = query()
    mismatched["conditions"] = ["different application"]
    mismatched["application_fixed_point"] = fingerprint(
        {
            "conditions": mismatched["conditions"],
            "exclusions": mismatched["exclusions"],
            "role": None,
            "lifecycle_stage": None,
        }
    )
    result = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=mismatched,
    )
    assert result["groups"] == {"exact": [], "close": [], "related": []}

    stale = query()
    stale["application_fixed_point"] = "sha256-v1:" + "f" * 64
    stale_result = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=stale,
    )
    assert stale_result["groups"] == {"exact": [], "close": [], "related": []}

    source_stale = query()
    source_stale["source_fixed_points"] = {}
    source_stale_result = catalog.query_catalog(
        cards=cards,
        catalog=index,
        session=opened_session(catalog),
        query=source_stale,
    )
    assert source_stale_result["groups"] == {
        "exact": [],
        "close": [],
        "related": [],
    }

    taxonomy_only = valid_card()
    taxonomy_only["applicability_conditions"] = ["different application"]
    catalog, records = catalog_records(tmp_path, [taxonomy_only])
    taxonomy_result = catalog.query_catalog(
        cards={record["card"]["card_id"]: record for record in records},
        catalog=catalog.build_catalog(
            records,
            generated_at="2026-07-26T00:00:00Z",
        ),
        session=opened_session(catalog),
        query=query(),
    )
    assert taxonomy_result["groups"] == {
        "exact": [],
        "close": [],
        "related": [],
    }


def test_catalog_session_allows_one_reconciliation_one_gap_and_completion() -> None:
    catalog = catalog_module()
    index = catalog.build_catalog(
        [],
        generated_at="2026-07-26T00:00:00Z",
    )
    initial = opened_session(catalog)

    early_gap_query = query(problem="Missing authority boundary", maximum=1)
    early_gap_query.update(
        {
            "named_gap": "Whether one authority boundary is reusable",
            "material_h1_change": "Could change whether an authority gate is admitted",
        }
    )
    early_gap = catalog.query_catalog(
        cards={},
        catalog=index,
        session=initial,
        query=early_gap_query,
        pass_kind="named-gap",
    )
    assert early_gap["status"] == "named-gap-not-admitted"

    reconciliation = catalog.query_catalog(
        cards={},
        catalog=index,
        session=initial,
        query=query(),
    )
    assert reconciliation["status"] == "catalog-results"
    assert reconciliation["session"]["reconciliation_passes"] == 1

    repeated = catalog.query_catalog(
        cards={},
        catalog=index,
        session=reconciliation["session"],
        query=query(),
    )
    assert repeated["status"] == "reconciliation-pass-exhausted"

    gap = catalog.query_catalog(
        cards={},
        catalog=index,
        session=reconciliation["session"],
        query=early_gap_query,
        pass_kind="named-gap",
    )
    assert gap["status"] == "catalog-results"
    assert gap["session"]["gap_passes"] == 1

    second_gap = catalog.query_catalog(
        cards={},
        catalog=index,
        session=gap["session"],
        query=early_gap_query,
        pass_kind="named-gap",
    )
    assert second_gap["status"] == "gap-pass-exhausted"

    completed = catalog.complete_session(gap["session"])
    assert completed["status"] == "workflow-complete"
    assert completed["session"]["phase"] == "complete"

    after_completion = catalog.query_catalog(
        cards={},
        catalog=index,
        session=completed["session"],
        query=query(),
    )
    assert after_completion["status"] == "workflow-complete"


def test_named_gap_must_come_from_the_recorded_packet() -> None:
    catalog = catalog_module()
    index = catalog.build_catalog(
        [],
        generated_at="2026-07-26T00:00:00Z",
    )
    packet = independent_packet()
    packet["unresolved_named_gaps"] = []
    packet["fingerprint"] = fingerprint(
        {key: value for key, value in packet.items() if key != "fingerprint"}
    )
    recorded = catalog.record_independent_packet(
        packet,
        packet["pre_discovery_fixed_point_fingerprint"],
    )
    opened = catalog.open_catalog(recorded["session"], packet["fingerprint"])
    reconciliation = catalog.query_catalog(
        cards={},
        catalog=index,
        session=opened["session"],
        query=query(),
    )
    gap_query = query()
    gap_query["named_gap"] = "Invented after independent discovery"
    gap_query["material_h1_change"] = "Could change the evidence class"

    result = catalog.query_catalog(
        cards={},
        catalog=index,
        session=reconciliation["session"],
        query=gap_query,
        pass_kind="named-gap",
    )

    assert result["status"] == "named-gap-not-admitted"


def test_repository_catalog_validator_fails_and_restores(
    tmp_path: Path,
) -> None:
    catalog = catalog_module()
    write_catalog_contract_root(tmp_path)

    assert validate_skills.validate_research_catalog_contract(tmp_path) == []

    schema_path = (
        tmp_path
        / "docs/validation/shared/schemas/research-card-v1.schema.json"
    )
    original_schema = schema_path.read_bytes()
    schema_path.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "urn:programming-agent-skills:research-card:v1",
                "type": "object",
            }
        ),
        encoding="utf-8",
    )
    failures = validate_skills.validate_research_catalog_contract(tmp_path)
    assert any("schema fingerprint mismatch" in failure for failure in failures)
    schema_path.write_bytes(original_schema)
    assert validate_skills.validate_research_catalog_contract(tmp_path) == []

    weakened = json.loads(original_schema)
    weakened["$defs"]["relation"]["properties"]["type"]["enum"].append(  # type: ignore[index]
        "recommends"
    )
    schema_path.write_text(json.dumps(weakened), encoding="utf-8")
    failures = validate_skills.validate_research_catalog_contract(tmp_path)
    assert any("schema fingerprint mismatch" in failure for failure in failures)
    schema_path.write_bytes(original_schema)
    assert validate_skills.validate_research_catalog_contract(tmp_path) == []

    path = tmp_path / "docs/research/skill-pack-composition/cards/RC-0001.md"
    invalid = valid_card()
    invalid["recommendation"] = "adopt"
    write_card(path, invalid)

    failures = validate_skills.validate_research_catalog_contract(tmp_path)

    assert any("forbidden authority field" in failure for failure in failures)

    path.unlink()
    catalog.write_catalog(
        tmp_path,
        generated_at="2026-07-26T00:00:00Z",
    )

    assert validate_skills.validate_research_catalog_contract(tmp_path) == []
