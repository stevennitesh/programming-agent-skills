"""Deterministic Research Card admission and bounded retrieval controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


FINGERPRINT_PREFIX = "sha256-v1:"
INDEPENDENT_PACKET_FIELDS = (
    "schema_version",
    "packet_id",
    "intended_essence",
    "m0_units",
    "failures",
    "discovered_methods",
    "alternatives",
    "counterpressure",
    "wrong_conditions",
    "unresolved_named_gaps",
)
HISTORICAL_SEED_KEYS = frozenset(
    {
        "card_id",
        "card_ids",
        "catalog_results",
        "current_skill_body",
        "historical_card_ids",
        "incumbent",
        "prior_synthesis",
    }
)
FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "acceptance_decision",
        "adoption",
        "confidence",
        "h1",
        "popularity",
        "recommendation",
        "rubric_score",
        "validation_result",
    }
)
CARD_ID_RE = re.compile(r"RC-[0-9]{4}")
CLAIM_ID_RE = re.compile(r"RC-[0-9]{4}-C[0-9]{2}")
SOURCE_ID_RE = re.compile(r"SRC-[0-9]{4}")
FINGERPRINT_RE = re.compile(r"sha256-v1:[0-9a-f]{64}")
FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(?P<body>.*?)\r?\n---(?:[ \t]*\r?\n|\Z)",
    re.DOTALL,
)
RECORD_STATES = frozenset({"verified", "superseded", "retired"})
METHOD_EVIDENCE = frozenset(
    {"independently-supported", "contested", "pack-specific", "unverified"}
)
CLAIM_STATUSES = frozenset({"supported", "conflicted", "unknown"})
RELATION_TYPES = frozenset(
    {
        "broader",
        "narrower",
        "related",
        "exact-match",
        "close-match",
        "conflicts-with",
        "revision-of",
        "supersedes",
    }
)
DIMENSION_FIELDS = (
    "problems",
    "behaviors",
    "conditions",
    "roles",
    "lifecycle_stages",
    "source_classes",
    "relationships",
)
CARD_FIELDS = (
    "schema_version",
    "card_id",
    "preferred_label",
    "alternative_labels",
    "hidden_labels",
    "record_state",
    "behavior",
    "failure_prevented",
    "recruited_behavior",
    "scope_note",
    "applicability_conditions",
    "counterconditions",
    "wrong_condition",
    "method_evidence",
    "claims",
    "sources",
    "verified_at",
    "refresh_triggers",
    "relations",
    "dimensions",
    "unknowns",
    "claim_limits",
)
CLAIM_FIELDS = frozenset(
    {
        "claim_id",
        "statement",
        "status",
        "source_ids",
        "counterevidence",
        "applicability",
        "limits",
    }
)
SOURCE_FIELDS = frozenset(
    {
        "source_id",
        "authority_class",
        "locator",
        "fixed_point",
        "inspected_anchors",
        "accessed_at",
        "access_depth",
        "limits",
    }
)
SOURCE_FIXED_POINT_FIELDS = frozenset(
    {"revision", "date", "version", "jurisdiction", "population", "method"}
)
QUERY_FIELDS = frozenset(
    {
        "problem",
        "recruited_behavior",
        "conditions",
        "exclusions",
        "role",
        "lifecycle_stage",
        "method_evidence",
        "freshness",
        "application_fixed_point",
        "refresh_events",
        "source_fixed_points",
        "known_terms",
        "maximum_families",
        "named_gap",
        "material_h1_change",
    }
)
CATALOG_FIELDS = frozenset(
    {
        "schema_version",
        "taxonomy_version",
        "catalog_fixed_point",
        "generated_at",
        "entries",
        "integrity",
    }
)
SESSION_FIELDS = frozenset(
    {
        "phase",
        "independent_packet",
        "independent_packet_fingerprint",
        "reconciliation_passes",
        "gap_passes",
        "transition_receipts",
    }
)
CATALOG_PATH = Path("docs/research/skill-pack-composition/catalog.json")
CARD_ROOT = Path("docs/research/skill-pack-composition/cards")
SCHEMA_REGISTRY = Path("docs/validation/shared/schemas/registry.json")
REQUIRED_SCHEMAS = {
    ("research-card", 1): (
        "docs/validation/shared/schemas/research-card-v1.schema.json"
    ),
    ("research-catalog", 1): (
        "docs/validation/shared/schemas/research-catalog-v1.schema.json"
    ),
    ("independent-research-packet", 1): (
        "docs/validation/shared/schemas/"
        "independent-research-packet-v1.schema.json"
    ),
}
SCHEMA_REQUIRED_FIELDS = {
    ("research-card", 1): frozenset(CARD_FIELDS),
    ("research-catalog", 1): CATALOG_FIELDS,
    ("independent-research-packet", 1): frozenset(
        {*INDEPENDENT_PACKET_FIELDS, "fingerprint"}
    ),
}
VALID_FIXTURE = Path(
    "docs/validation/shared/fixtures/research-card-v1/RC-9001.md"
)
INDEPENDENT_PACKET_FIXTURE = Path(
    "docs/validation/shared/fixtures/"
    "independent-research-packet-v1/packet.json"
)


class CardContractError(ValueError):
    """One or more deterministic Research Card contract violations."""


def exact_fingerprint(payload: object) -> str:
    content = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"{FINGERPRINT_PREFIX}{hashlib.sha256(content).hexdigest()}"


def _nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key).casefold() for key in value}
        for child in value.values():
            keys.update(_nested_keys(child))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for child in value:
            keys.update(_nested_keys(child))
        return keys
    return set()


def _nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def _strings(value: object) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def _string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nested_forbidden_keys(
    value: object,
    forbidden: frozenset[str],
) -> set[str]:
    return _nested_keys(value) & forbidden


def _validate_claims(
    card_id: str,
    claims: object,
    source_ids: set[str],
    failures: list[str],
) -> None:
    if not isinstance(claims, list) or not claims:
        failures.append("claims must be a non-empty list")
        return
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            failures.append(f"claim {index} must be an object")
            continue
        if set(claim) != CLAIM_FIELDS:
            failures.append(f"claim {index} has unknown or missing fields")
        claim_id = claim.get("claim_id")
        if (
            not isinstance(claim_id, str)
            or CLAIM_ID_RE.fullmatch(claim_id) is None
            or not claim_id.startswith(f"{card_id}-C")
        ):
            failures.append(f"claim {index} has invalid claim_id")
        elif claim_id in seen:
            failures.append(f"duplicate claim_id: {claim_id}")
        else:
            seen.add(claim_id)
        if not _string(claim.get("statement")):
            failures.append(f"claim {index} has no statement")
        if claim.get("status") not in CLAIM_STATUSES:
            failures.append(f"claim {index} has invalid status")
        referenced = claim.get("source_ids")
        if not _nonempty_strings(referenced):
            failures.append(f"claim {index} has no source_ids")
        else:
            missing = set(referenced) - source_ids
            if missing:
                failures.append(
                    f"claim {index} has unresolved source_ids: {sorted(missing)}"
                )
        for field in ("counterevidence", "applicability", "limits"):
            value = claim.get(field)
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                failures.append(f"claim {index} has invalid {field}")


def _validate_sources(
    sources: object,
    failures: list[str],
) -> set[str]:
    if not isinstance(sources, list) or not sources:
        failures.append("sources must be a non-empty list")
        return set()
    seen: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            failures.append(f"source {index} must be an object")
            continue
        if set(source) != SOURCE_FIELDS:
            failures.append(f"source {index} has unknown or missing fields")
        source_id = source.get("source_id")
        if (
            not isinstance(source_id, str)
            or SOURCE_ID_RE.fullmatch(source_id) is None
        ):
            failures.append(f"source {index} has invalid source_id")
        elif source_id in seen:
            failures.append(f"duplicate source_id: {source_id}")
        else:
            seen.add(source_id)
        for field in (
            "authority_class",
            "locator",
            "accessed_at",
            "access_depth",
        ):
            if not _string(source.get(field)):
                failures.append(f"source {index} has no {field}")
        locator = str(source.get("locator", ""))
        if _is_private_locator(locator):
            failures.append(
                f"source {index} exposes a private source locator"
            )
        fixed_point = source.get("fixed_point")
        if (
            not isinstance(fixed_point, dict)
            or set(fixed_point) != SOURCE_FIXED_POINT_FIELDS
            or any(
                not _string(fixed_point.get(field))
                for field in SOURCE_FIXED_POINT_FIELDS
            )
        ):
            failures.append(f"source {index} has incomplete fixed_point")
        for field in ("inspected_anchors", "limits"):
            if not _nonempty_strings(source.get(field)):
                failures.append(f"source {index} has invalid {field}")
    return seen


def _is_private_locator(locator: str) -> bool:
    normalized = locator.replace("\\", "/")
    parsed = urlsplit(normalized)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return False
    if parsed.scheme:
        return True
    windows = PureWindowsPath(locator)
    if windows.is_absolute() or windows.drive:
        return True
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        return True
    parts = [part.casefold() for part in path.parts if part not in {"", "."}]
    return (
        bool(parts)
        and parts[0] == "sources"
        or len(parts) >= 3
        and parts[:3] == ["docs", "research", "sources"]
    )


def validate_card_payload(payload: object) -> list[str]:
    """Return all mechanical Research Card violations."""

    if not isinstance(payload, dict):
        return ["card payload must be an object"]
    failures: list[str] = []
    missing = [field for field in CARD_FIELDS if field not in payload]
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")
    unknown = sorted(set(payload) - set(CARD_FIELDS))
    if unknown:
        failures.append(f"unknown Card fields: {', '.join(unknown)}")
    forbidden = sorted(_nested_forbidden_keys(payload, FORBIDDEN_AUTHORITY_KEYS))
    if forbidden:
        failures.append(
            f"forbidden authority field: {', '.join(forbidden)}"
        )
    if payload.get("schema_version") != 1:
        failures.append("schema_version must be 1")
    card_id = payload.get("card_id")
    if not isinstance(card_id, str) or CARD_ID_RE.fullmatch(card_id) is None:
        failures.append("card_id must match RC-NNNN")
        card_id = "RC-0000"
    for field in (
        "preferred_label",
        "behavior",
        "failure_prevented",
        "recruited_behavior",
        "scope_note",
        "wrong_condition",
        "verified_at",
    ):
        if not _string(payload.get(field)):
            failures.append(f"{field} must be a non-empty string")
    for field in (
        "alternative_labels",
        "hidden_labels",
        "applicability_conditions",
        "counterconditions",
        "refresh_triggers",
        "claim_limits",
    ):
        if not _nonempty_strings(payload.get(field)):
            failures.append(f"{field} must be a non-empty string list")
    unknowns = payload.get("unknowns")
    if not isinstance(unknowns, list) or not all(
        isinstance(item, str) and item.strip() for item in unknowns
    ):
        failures.append("unknowns must be a string list")

    labels = (
        [payload.get("preferred_label")]
        + (
            payload.get("alternative_labels")
            if isinstance(payload.get("alternative_labels"), list)
            else []
        )
        + (
            payload.get("hidden_labels")
            if isinstance(payload.get("hidden_labels"), list)
            else []
        )
    )
    normalized_labels = [
        item.strip().casefold() for item in labels if isinstance(item, str)
    ]
    if len(normalized_labels) != len(set(normalized_labels)):
        failures.append(
            "preferred, alternative, and hidden labels must be disjoint"
        )
    if payload.get("record_state") not in RECORD_STATES:
        failures.append("record_state is invalid")
    if payload.get("method_evidence") not in METHOD_EVIDENCE:
        failures.append("method_evidence is invalid")

    sources = _validate_sources(payload.get("sources"), failures)
    _validate_claims(str(card_id), payload.get("claims"), sources, failures)

    relations = payload.get("relations")
    if not isinstance(relations, list):
        failures.append("relations must be a list")
    else:
        seen_relations: set[tuple[str, str]] = set()
        for index, relation in enumerate(relations):
            if not isinstance(relation, dict):
                failures.append(f"relation {index} must be an object")
                continue
            if set(relation) != {"type", "target_card_id"}:
                failures.append(f"relation {index} has unknown or missing fields")
            relation_type = relation.get("type")
            target = relation.get("target_card_id")
            if relation_type not in RELATION_TYPES:
                failures.append(f"relation type is invalid: {relation_type!r}")
            if (
                not isinstance(target, str)
                or CARD_ID_RE.fullmatch(target) is None
            ):
                failures.append(f"relation {index} has invalid target_card_id")
            elif target == card_id:
                failures.append(f"relation {index} cannot target its own card")
            identity = (str(relation_type), str(target))
            if identity in seen_relations:
                failures.append(f"duplicate relation: {identity}")
            seen_relations.add(identity)

    dimensions = payload.get("dimensions")
    if not isinstance(dimensions, dict):
        failures.append("dimensions must be an object")
    else:
        if set(dimensions) != set(DIMENSION_FIELDS):
            failures.append("dimensions must use the settled fields")
        for field in DIMENSION_FIELDS:
            if not _nonempty_strings(dimensions.get(field)):
                failures.append(f"dimension {field} must be non-empty")
    return failures


def parse_card(
    path: Path,
    *,
    root: Path,
    expected_fingerprint: str | None = None,
) -> dict[str, object]:
    """Parse and validate one canonical Markdown Research Card."""

    try:
        content = path.read_bytes()
    except OSError as error:
        raise CardContractError(f"cannot read card: {error}") from error
    fingerprint = (
        f"{FINGERPRINT_PREFIX}{hashlib.sha256(content).hexdigest()}"
    )
    if (
        expected_fingerprint is not None
        and expected_fingerprint != fingerprint
    ):
        raise CardContractError(
            f"card fingerprint mismatch: {path} -> {expected_fingerprint}"
        )
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CardContractError(f"card is not UTF-8: {path}") from error
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise CardContractError(f"card has no YAML frontmatter: {path}")
    try:
        payload = yaml.safe_load(match.group("body"))
    except yaml.YAMLError as error:
        raise CardContractError(f"card YAML is invalid: {path}: {error}") from error
    failures = validate_card_payload(payload)
    if failures:
        raise CardContractError("; ".join(failures))
    assert isinstance(payload, dict)
    card_id = str(payload["card_id"])
    if path.stem != card_id:
        raise CardContractError(
            f"card filename must equal card_id: {path.name} -> {card_id}"
        )
    try:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise CardContractError(f"card path escapes root: {path}") from error
    return {
        "card": payload,
        "path": relative,
        "fingerprint": fingerprint,
    }


def _exact_match_families(
    records: list[dict[str, object]],
) -> dict[str, str]:
    parents: dict[str, str] = {}

    def find(item: str) -> str:
        parents.setdefault(item, item)
        if parents[item] != item:
            parents[item] = find(parents[item])
        return parents[item]

    def union(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            canonical = min(left_root, right_root)
            parents[left_root] = canonical
            parents[right_root] = canonical

    known = {
        str(record["card"]["card_id"])
        for record in records
        if isinstance(record.get("card"), dict)
    }
    for card_id in known:
        find(card_id)
    for record in records:
        card = record["card"]
        assert isinstance(card, dict)
        for relation in card["relations"]:
            if (
                relation["type"] == "exact-match"
                and relation["target_card_id"] in known
            ):
                union(str(card["card_id"]), str(relation["target_card_id"]))
    grouped: dict[str, list[str]] = {}
    for card_id in known:
        grouped.setdefault(find(card_id), []).append(card_id)
    result: dict[str, str] = {}
    for members in grouped.values():
        canonical = min(members)
        for member in members:
            result[member] = canonical
    return result


def build_catalog(
    records: list[dict[str, object]],
    *,
    generated_at: str,
) -> dict[str, object]:
    """Derive the thin catalog without copying claim or source narratives."""

    cards: dict[str, dict[str, object]] = {}
    source_records: dict[str, str] = {}
    for record in records:
        card = record.get("card")
        if not isinstance(card, dict):
            raise CardContractError("catalog record has no card payload")
        card_id = str(card.get("card_id"))
        if card_id in cards:
            raise CardContractError(f"duplicate card_id: {card_id}")
        cards[card_id] = record
        for source in card["sources"]:
            source_id = str(source["source_id"])
            serialized = json.dumps(
                source,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            prior = source_records.get(source_id)
            if prior is not None and prior != serialized:
                raise CardContractError(
                    f"source_id collision has different provenance: {source_id}"
                )
            source_records[source_id] = serialized
    for card_id, record in cards.items():
        card = record["card"]
        assert isinstance(card, dict)
        for relation in card["relations"]:
            if relation["target_card_id"] not in cards:
                raise CardContractError(
                    f"unresolved relation target: {card_id} -> "
                    f"{relation['target_card_id']}"
                )
    families = _exact_match_families(records)
    observations = [
        {
            "card_id": card_id,
            "path": record["path"],
            "fingerprint": record["fingerprint"],
        }
        for card_id, record in sorted(cards.items())
    ]
    entries: list[dict[str, object]] = []
    for card_id, record in sorted(cards.items()):
        card = record["card"]
        assert isinstance(card, dict)
        if card["record_state"] != "verified":
            continue
        entries.append(
            {
                "card_id": card_id,
                "canonical_family_id": families[card_id],
                "path": record["path"],
                "fingerprint": record["fingerprint"],
                "preferred_label": card["preferred_label"],
                "alternative_labels": card["alternative_labels"],
                "hidden_labels": card["hidden_labels"],
                "dimensions": card["dimensions"],
                "method_evidence": card["method_evidence"],
                "freshness_state": "unknown",
                "relations": card["relations"],
            }
        )
    return {
        "schema_version": 1,
        "taxonomy_version": 1,
        "catalog_fixed_point": exact_fingerprint(observations),
        "generated_at": generated_at,
        "entries": entries,
        "integrity": {
            "unique_ids": True,
            "resolvable_paths": True,
            "relation_targets": True,
            "claim_source_links": True,
            "canonical_equivalence": True,
        },
    }


def _normalized(value: object) -> str:
    return str(value).strip().casefold()


def _normalized_set(value: object) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {
        _normalized(item)
        for item in value
        if isinstance(item, str) and item.strip()
    }


def _query_failure(
    query: dict[str, object],
) -> str | None:
    if set(query) - QUERY_FIELDS:
        return "query contains unsupported fields"
    primary = [
        field
        for field in ("problem", "recruited_behavior")
        if _string(query.get(field))
    ]
    maximum = query.get("maximum_families")
    required_lists = (
        "conditions",
        "exclusions",
        "method_evidence",
        "freshness",
        "refresh_events",
        "known_terms",
    )
    if len(primary) != 1:
        return "query requires exactly one problem or recruited_behavior"
    if not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 1:
        return "query requires an explicit positive maximum_families"
    if any(not _strings(query.get(field)) for field in required_lists):
        return "query requires explicit filter lists"
    if any(
        field in query and not _string(query.get(field))
        for field in ("role", "lifecycle_stage")
    ):
        return "query optional dimensions must be non-empty strings"
    method_evidence = set(query.get("method_evidence", []))
    freshness = set(query.get("freshness", []))
    if method_evidence - METHOD_EVIDENCE:
        return "query contains an invalid method_evidence filter"
    if freshness - {
        "verified-for-fixed-point",
        "refresh-required",
        "unknown",
    }:
        return "query contains an invalid freshness filter"
    if not _string(query.get("application_fixed_point")) or FINGERPRINT_RE.fullmatch(
        str(query.get("application_fixed_point"))
    ) is None:
        return "query requires application_fixed_point"
    source_fixed_points = query.get("source_fixed_points")
    if not isinstance(source_fixed_points, dict) or any(
        not _string(source_id)
        or not isinstance(value, str)
        or FINGERPRINT_RE.fullmatch(value) is None
        for source_id, value in source_fixed_points.items()
    ):
        return "query requires explicit source_fixed_points"
    return None


def application_fixed_point(query: dict[str, object]) -> str:
    """Derive the exact identity of the caller's applicability boundary."""

    return exact_fingerprint(
        {
            "conditions": query.get("conditions"),
            "exclusions": query.get("exclusions"),
            "role": query.get("role"),
            "lifecycle_stage": query.get("lifecycle_stage"),
        }
    )


def _freshness(
    card: dict[str, object],
    query: dict[str, object],
) -> str:
    events = _normalized_set(query.get("refresh_events"))
    triggers = _normalized_set(card.get("refresh_triggers"))
    if events & triggers:
        return "refresh-required"
    if query.get("application_fixed_point") != application_fixed_point(query):
        return "unknown"
    observations = query.get("source_fixed_points")
    if not isinstance(observations, dict):
        return "unknown"
    for source in card.get("sources", []):
        if not isinstance(source, dict):
            return "unknown"
        source_id = source.get("source_id")
        if observations.get(source_id) != exact_fingerprint(
            source.get("fixed_point")
        ):
            return "unknown"
    if card.get("sources"):
        return "verified-for-fixed-point"
    return "unknown"


def _passes_filters(
    card: dict[str, object],
    query: dict[str, object],
) -> bool:
    method_filter = _normalized_set(query.get("method_evidence"))
    if method_filter and _normalized(card.get("method_evidence")) not in method_filter:
        return False
    freshness_filter = _normalized_set(query.get("freshness"))
    if freshness_filter and _freshness(card, query) not in freshness_filter:
        return False
    conditions = _normalized_set(query.get("conditions"))
    exclusions = _normalized_set(query.get("exclusions"))
    applicability = _normalized_set(card.get("applicability_conditions"))
    dimensions = card.get("dimensions")
    if not isinstance(dimensions, dict):
        return False
    if conditions and not conditions <= applicability:
        return False
    if conditions & _normalized_set(card.get("counterconditions")):
        return False
    if exclusions & (
        _normalized_set(card.get("applicability_conditions"))
        | _normalized_set(
            card.get("dimensions", {}).get("conditions")
            if isinstance(card.get("dimensions"), dict)
            else []
        )
    ):
        return False
    role = query.get("role")
    if _string(role) and _normalized(role) not in _normalized_set(
        dimensions.get("roles")
    ):
        return False
    stage = query.get("lifecycle_stage")
    if _string(stage) and _normalized(stage) not in _normalized_set(
        dimensions.get("lifecycle_stages")
    ):
        return False
    return True


def _catalog_records(
    cards: dict[str, dict[str, object]],
    catalog: dict[str, object],
) -> tuple[
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
] | None:
    if set(catalog) != CATALOG_FIELDS:
        return None
    entries = catalog.get("entries")
    if not isinstance(entries, list) or not _string(catalog.get("generated_at")):
        return None
    try:
        expected = build_catalog(
            list(cards.values()),
            generated_at=str(catalog["generated_at"]),
        )
    except (CardContractError, KeyError, TypeError):
        return None
    if catalog != expected:
        return None
    entry_by_id: dict[str, dict[str, object]] = {}
    visible: dict[str, dict[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            return None
        card_id = entry.get("card_id")
        if not isinstance(card_id, str) or card_id in entry_by_id:
            return None
        record = cards.get(card_id)
        if (
            not isinstance(record, dict)
            or record.get("fingerprint") != entry.get("fingerprint")
            or record.get("path") != entry.get("path")
            or not isinstance(record.get("card"), dict)
        ):
            return None
        entry_by_id[card_id] = entry
        visible[card_id] = record
    return entry_by_id, visible


def _alias_candidates(
    visible: dict[str, dict[str, object]],
    terms: set[str],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for term in terms:
        for card_id, record in visible.items():
            card = record["card"]
            assert isinstance(card, dict)
            labels = {
                _normalized(card["preferred_label"]),
                *_normalized_set(card["alternative_labels"]),
                *_normalized_set(card["hidden_labels"]),
            }
            if term in labels:
                result.setdefault(term, set()).add(card_id)
    return result


def _result_item(
    record: dict[str, object],
    *,
    match_class: str,
    matched_fields: list[str],
    query: dict[str, object],
) -> dict[str, object]:
    card = record["card"]
    assert isinstance(card, dict)
    claims = [
        {
            "claim_id": claim["claim_id"],
            "status": claim["status"],
            "source_ids": claim["source_ids"],
            "counterevidence": claim["counterevidence"],
            "limits": claim["limits"],
        }
        for claim in card["claims"]
    ]
    sources = [
        {
            "source_id": source["source_id"],
            "locator": source["locator"],
            "fixed_point": source["fixed_point"],
        }
        for source in card["sources"]
    ]
    return {
        "match_class": match_class,
        "matched_fields": sorted(matched_fields),
        "card_id": card["card_id"],
        "preferred_label": card["preferred_label"],
        "behavior": card["behavior"],
        "failure_prevented": card["failure_prevented"],
        "recruited_behavior": card["recruited_behavior"],
        "scope_note": card["scope_note"],
        "applicability_conditions": card["applicability_conditions"],
        "counterconditions": card["counterconditions"],
        "method_evidence": card["method_evidence"],
        "claims": claims,
        "source_pointers": sources,
        "freshness": _freshness(card, query),
        "unknowns": card["unknowns"],
        "claim_limits": card["claim_limits"],
        "relations": card["relations"],
        "fingerprint": record["fingerprint"],
    }


def _narrowing_dimensions(
    visible: dict[str, dict[str, object]],
    candidate_ids: set[str],
) -> list[str]:
    result: list[str] = []
    for field in DIMENSION_FIELDS:
        values: set[str] = set()
        for card_id in candidate_ids:
            card = visible[card_id]["card"]
            assert isinstance(card, dict)
            dimensions = card["dimensions"]
            assert isinstance(dimensions, dict)
            values.update(_normalized_set(dimensions[field]))
        if len(values) > 1:
            result.append(field)
    if result:
        return result
    return [
        field
        for field in DIMENSION_FIELDS
        if any(
            _normalized_set(
                visible[card_id]["card"]["dimensions"][field]
            )
            for card_id in candidate_ids
        )
    ]


def _advanced_session(
    session: dict[str, object],
    pass_kind: str,
) -> tuple[dict[str, object] | None, str | None]:
    reconciliation_passes = session.get("reconciliation_passes")
    gap_passes = session.get("gap_passes")
    if (
        not isinstance(reconciliation_passes, int)
        or isinstance(reconciliation_passes, bool)
        or not isinstance(gap_passes, int)
        or isinstance(gap_passes, bool)
        or reconciliation_passes not in {0, 1}
        or gap_passes not in {0, 1}
    ):
        return None, "catalog-session-incompatible"
    advanced = deepcopy(session)
    if pass_kind == "reconciliation":
        if reconciliation_passes >= 1:
            return None, "reconciliation-pass-exhausted"
        advanced["reconciliation_passes"] = 1
        advanced["phase"] = "reconciled"
        _append_transition(advanced, "reconciliation")
        return advanced, None
    if pass_kind == "named-gap":
        if reconciliation_passes != 1:
            return None, "named-gap-not-admitted"
        if gap_passes >= 1:
            return None, "gap-pass-exhausted"
        advanced["gap_passes"] = 1
        advanced["phase"] = "gap-used"
        _append_transition(advanced, "named-gap")
        return advanced, None
    return None, "catalog-query-invalid"


def _transition_receipt(
    *,
    action: str,
    prior: str | None,
    packet_fingerprint: str,
) -> str:
    return exact_fingerprint(
        {
            "action": action,
            "prior": prior,
            "independent_packet_fingerprint": packet_fingerprint,
        }
    )


def _append_transition(session: dict[str, object], action: str) -> None:
    receipts = session["transition_receipts"]
    assert isinstance(receipts, list)
    prior = receipts[-1]["receipt"] if receipts else None
    assert prior is None or isinstance(prior, str)
    packet_fingerprint = session["independent_packet_fingerprint"]
    assert isinstance(packet_fingerprint, str)
    receipts.append(
        {
            "action": action,
            "receipt": _transition_receipt(
                action=action,
                prior=prior,
                packet_fingerprint=packet_fingerprint,
            ),
        }
    )


def _valid_session(session: object) -> bool:
    if not isinstance(session, dict) or set(session) != SESSION_FIELDS:
        return False
    packet = session.get("independent_packet")
    if not isinstance(packet, dict):
        return False
    recorded = record_independent_packet(packet)
    if recorded.get("status") != "independent-recorded":
        return False
    if (
        session.get("independent_packet_fingerprint")
        != packet.get("fingerprint")
    ):
        return False
    packet_fingerprint = session["independent_packet_fingerprint"]
    assert isinstance(packet_fingerprint, str)
    receipts = session.get("transition_receipts")
    if not isinstance(receipts, list) or not receipts:
        return False
    prior: str | None = None
    actions: list[str] = []
    for item in receipts:
        if not isinstance(item, dict) or set(item) != {"action", "receipt"}:
            return False
        action = item.get("action")
        receipt = item.get("receipt")
        if (
            not isinstance(action, str)
            or receipt
            != _transition_receipt(
                action=action,
                prior=prior,
                packet_fingerprint=packet_fingerprint,
            )
        ):
            return False
        actions.append(action)
        prior = str(receipt)
    phase = session.get("phase")
    valid_actions = {
        "independent": ["record"],
        "catalog-open": ["record", "open"],
        "reconciled": ["record", "open", "reconciliation"],
        "gap-used": ["record", "open", "reconciliation", "named-gap"],
        "complete": [
            ["record", "open", "reconciliation", "complete"],
            ["record", "open", "reconciliation", "named-gap", "complete"],
        ],
    }
    expected_actions = valid_actions.get(str(phase))
    if phase == "complete":
        if actions not in expected_actions:
            return False
    elif actions != expected_actions:
        return False
    reconciliation_passes = session.get("reconciliation_passes")
    gap_passes = session.get("gap_passes")
    counts_valid = (
        isinstance(reconciliation_passes, int)
        and not isinstance(reconciliation_passes, bool)
        and reconciliation_passes in {0, 1}
        and isinstance(gap_passes, int)
        and not isinstance(gap_passes, bool)
        and gap_passes in {0, 1}
    )
    if not counts_valid:
        return False
    expected_counts = {
        "independent": (0, 0),
        "catalog-open": (0, 0),
        "reconciled": (1, 0),
        "gap-used": (1, 1),
    }
    if phase == "complete":
        return reconciliation_passes == 1
    return expected_counts.get(str(phase)) == (
        reconciliation_passes,
        gap_passes,
    )


def record_independent_packet(packet: dict[str, object]) -> dict[str, object]:
    """Record a fingerprinted M0-derived packet without opening the catalog."""

    if _nested_keys(packet) & HISTORICAL_SEED_KEYS:
        return {"status": "historical-seed-rejected"}
    if set(packet) != set(INDEPENDENT_PACKET_FIELDS) | {"fingerprint"}:
        return {"status": "independent-packet-invalid"}
    payload = {key: value for key, value in packet.items() if key != "fingerprint"}
    if (
        payload.get("schema_version") != 1
        or not isinstance(payload.get("packet_id"), str)
        or not str(payload["packet_id"]).strip()
        or not isinstance(payload.get("intended_essence"), str)
        or not str(payload["intended_essence"]).strip()
        or any(
            not _nonempty_strings(payload.get(field))
            for field in (
                "m0_units",
                "failures",
                "discovered_methods",
                "alternatives",
                "counterpressure",
                "wrong_conditions",
            )
        )
        or not _strings(payload.get("unresolved_named_gaps"))
    ):
        return {"status": "independent-packet-invalid"}
    expected = exact_fingerprint(payload)
    if packet.get("fingerprint") != expected:
        return {"status": "independent-fingerprint-invalid"}
    session = {
        "phase": "independent",
        "independent_packet": deepcopy(packet),
        "independent_packet_fingerprint": expected,
        "reconciliation_passes": 0,
        "gap_passes": 0,
        "transition_receipts": [],
    }
    _append_transition(session, "record")
    return {
        "status": "independent-recorded",
        "session": session,
    }


def open_catalog(
    session: dict[str, object],
    independent_packet_fingerprint: object,
) -> dict[str, object]:
    """Open catalog access only for the exact recorded independent packet."""

    if (
        not _valid_session(session)
        or
        session.get("phase") != "independent"
        or independent_packet_fingerprint
        != session.get("independent_packet_fingerprint")
    ):
        return {"status": "catalog-not-admitted", "session": deepcopy(session)}
    opened = deepcopy(session)
    opened["phase"] = "catalog-open"
    _append_transition(opened, "open")
    return {"status": "catalog-open", "session": opened}


def query_catalog(
    *,
    cards: dict[str, dict[str, object]],
    catalog: dict[str, object],
    session: dict[str, object],
    query: dict[str, object],
    pass_kind: str = "reconciliation",
) -> dict[str, object]:
    """Run one finite problem-first catalog reconciliation or named-gap pass."""

    if not _valid_session(session):
        return {"status": "catalog-not-admitted", "session": deepcopy(session)}
    if session.get("phase") == "complete":
        return {"status": "workflow-complete", "session": deepcopy(session)}
    if session.get("phase") not in {"catalog-open", "reconciled", "gap-used"}:
        return {"status": "catalog-not-admitted", "session": deepcopy(session)}
    failure = _query_failure(query)
    if failure is not None:
        return {
            "status": "catalog-query-invalid",
            "reason": failure,
            "session": deepcopy(session),
        }
    if pass_kind == "named-gap" and (
        not _string(query.get("named_gap"))
        or not _string(query.get("material_h1_change"))
    ):
        return {
            "status": "named-gap-invalid",
            "session": deepcopy(session),
        }
    if pass_kind == "named-gap":
        packet = session["independent_packet"]
        assert isinstance(packet, dict)
        named_gaps = _normalized_set(packet.get("unresolved_named_gaps"))
        if _normalized(query.get("named_gap")) not in named_gaps:
            return {
                "status": "named-gap-not-admitted",
                "session": deepcopy(session),
            }
    advanced, pass_failure = _advanced_session(session, pass_kind)
    if advanced is None:
        return {
            "status": pass_failure,
            "session": deepcopy(session),
        }
    resolved = _catalog_records(cards, catalog)
    if resolved is None:
        return {"status": "catalog-incompatible", "session": advanced}
    entries, visible = resolved

    terms = _normalized_set(query.get("known_terms"))
    aliases = _alias_candidates(visible, terms)
    family_by_id = {
        card_id: str(entry["canonical_family_id"])
        for card_id, entry in entries.items()
    }
    for term, candidate_ids in sorted(aliases.items()):
        families = {family_by_id[card_id] for card_id in candidate_ids}
        if len(families) > 1:
            return {
                "status": "catalog-ambiguous",
                "ambiguous_term": term,
                "candidates": [
                    {
                        "card_id": card_id,
                        "scope_note": visible[card_id]["card"]["scope_note"],
                    }
                    for card_id in sorted(candidate_ids)
                ],
                "cards_loaded": 0,
                "tree_scans": 0,
                "session": advanced,
            }

    primary_field = (
        "problem" if _string(query.get("problem")) else "recruited_behavior"
    )
    primary = _normalized(query[primary_field])
    exact_ids: set[str] = set()
    matched_fields: dict[str, list[str]] = {}
    for card_id, record in visible.items():
        card = record["card"]
        assert isinstance(card, dict)
        if not _passes_filters(card, query):
            continue
        dimensions = card["dimensions"]
        assert isinstance(dimensions, dict)
        if primary_field == "problem":
            candidates = {
                _normalized(card["failure_prevented"]),
                *_normalized_set(dimensions["problems"]),
            }
            field_name = "failure_prevented"
        else:
            candidates = {
                _normalized(card["recruited_behavior"]),
                *_normalized_set(dimensions["behaviors"]),
            }
            field_name = "recruited_behavior"
        if primary in candidates:
            exact_ids.add(card_id)
            matched_fields[card_id] = [field_name]

    if terms:
        allowed_families = {
            family_by_id[card_id]
            for candidate_ids in aliases.values()
            for card_id in candidate_ids
        }
        exact_ids = {
            card_id
            for card_id in exact_ids
            if family_by_id[card_id] in allowed_families
        }

    close_ids: set[str] = set()
    related_ids: set[str] = set()
    close_types = {"close-match"}
    related_types = RELATION_TYPES - {"exact-match", "close-match"}
    for card_id, record in visible.items():
        card = record["card"]
        assert isinstance(card, dict)
        for relation in card["relations"]:
            target = str(relation["target_card_id"])
            relation_type = str(relation["type"])
            if card_id in exact_ids and target in visible:
                if relation_type in close_types:
                    close_ids.add(target)
                    matched_fields.setdefault(target, []).append(
                        f"relation:{relation_type}"
                    )
                elif relation_type in related_types:
                    related_ids.add(target)
                    matched_fields.setdefault(target, []).append(
                        f"relation:{relation_type}"
                    )
            if target in exact_ids:
                if relation_type in close_types:
                    close_ids.add(card_id)
                    matched_fields.setdefault(card_id, []).append(
                        f"incoming-relation:{relation_type}"
                    )
                elif relation_type in related_types:
                    related_ids.add(card_id)
                    matched_fields.setdefault(card_id, []).append(
                        f"incoming-relation:{relation_type}"
                    )
    close_ids -= exact_ids
    related_ids -= exact_ids | close_ids
    close_ids = {
        card_id
        for card_id in close_ids
        if _passes_filters(visible[card_id]["card"], query)
    }
    related_ids = {
        card_id
        for card_id in related_ids
        if _passes_filters(visible[card_id]["card"], query)
    }

    grouped_ids = {
        "exact": exact_ids,
        "close": close_ids,
        "related": related_ids,
    }
    used_families: set[str] = set()
    representatives: dict[str, list[str]] = {
        "exact": [],
        "close": [],
        "related": [],
    }
    for group in ("exact", "close", "related"):
        by_family: dict[str, list[str]] = {}
        for card_id in grouped_ids[group]:
            by_family.setdefault(family_by_id[card_id], []).append(card_id)
        for family in sorted(by_family):
            if family in used_families:
                continue
            representatives[group].append(min(by_family[family]))
            used_families.add(family)

    eligible_ids = set().union(*grouped_ids.values())
    maximum = int(query["maximum_families"])
    if len(used_families) > maximum:
        return {
            "status": "catalog-overflow",
            "eligible_families": len(used_families),
            "cards_loaded": 0,
            "tree_scans": 0,
            "groups": {"exact": [], "close": [], "related": []},
            "narrowing_dimensions": _narrowing_dimensions(
                visible,
                eligible_ids,
            ),
            "session": advanced,
        }
    groups = {
        group: [
            _result_item(
                visible[card_id],
                match_class=group,
                matched_fields=matched_fields.get(card_id, []),
                query=query,
            )
            for card_id in sorted(representatives[group])
        ]
        for group in ("exact", "close", "related")
    }
    return {
        "status": "catalog-results",
        "groups": groups,
        "cards_loaded": sum(len(items) for items in groups.values()),
        "eligible_families": len(used_families),
        "tree_scans": 0,
        "session": advanced,
    }


def complete_session(session: dict[str, object]) -> dict[str, object]:
    """Close a session only after its one reconciliation pass."""

    if not _valid_session(session):
        return {"status": "catalog-not-admitted", "session": deepcopy(session)}
    if session.get("phase") == "complete":
        return {"status": "workflow-complete", "session": deepcopy(session)}
    reconciliation_passes = session.get("reconciliation_passes")
    gap_passes = session.get("gap_passes")
    if (
        session.get("phase") not in {"reconciled", "gap-used"}
        or reconciliation_passes != 1
        or isinstance(reconciliation_passes, bool)
        or gap_passes not in {0, 1}
        or isinstance(gap_passes, bool)
    ):
        return {"status": "catalog-incomplete", "session": deepcopy(session)}
    completed = deepcopy(session)
    completed["phase"] = "complete"
    _append_transition(completed, "complete")
    return {"status": "workflow-complete", "session": completed}


def load_card_directory(root: Path) -> list[dict[str, object]]:
    """Load canonical visible and historical Card records from their owner."""

    card_root = root / CARD_ROOT
    if not card_root.is_dir():
        raise CardContractError(f"missing Card root: {CARD_ROOT.as_posix()}")
    return [
        parse_card(path, root=root)
        for path in sorted(card_root.glob("RC-[0-9][0-9][0-9][0-9].md"))
    ]


def validate_repository(root: Path) -> list[str]:
    """Validate canonical Cards, derived index, schemas, fixture, and routing."""

    failures: list[str] = []
    registry_path = root / SCHEMA_REGISTRY
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"Cannot read Research Catalog schema registry: {error}"]
    schemas = registry.get("schemas") if isinstance(registry, dict) else None
    observed: dict[tuple[str, int], str] = {}
    observed_fingerprints: dict[tuple[str, int], object] = {}
    validators: dict[tuple[str, int], Draft202012Validator] = {}
    if isinstance(schemas, list):
        for entry in schemas:
            if (
                isinstance(entry, dict)
                and isinstance(entry.get("id"), str)
                and isinstance(entry.get("version"), int)
                and isinstance(entry.get("path"), str)
            ):
                observed[(entry["id"], entry["version"])] = entry["path"]
                observed_fingerprints[(entry["id"], entry["version"])] = (
                    entry.get("fingerprint")
                )
    for identity, expected_path in REQUIRED_SCHEMAS.items():
        if observed.get(identity) != expected_path:
            failures.append(
                f"Missing required Research Catalog schema: "
                f"{identity[0]} v{identity[1]}"
            )
            continue
        schema_path = root / expected_path
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            failures.append(
                f"Cannot read Research Catalog schema: {expected_path}: {error}"
            )
            continue
        expected_id = (
            f"urn:programming-agent-skills:{identity[0]}:v{identity[1]}"
        )
        if not isinstance(schema, dict) or schema.get("$id") != expected_id:
            failures.append(
                f"Research Catalog schema $id mismatch: {expected_path}"
            )
            continue
        if observed_fingerprints.get(identity) != exact_fingerprint(schema):
            failures.append(
                f"Research Catalog schema fingerprint mismatch: {expected_path}"
            )
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            failures.append(
                f"Research Catalog schema is invalid: {expected_path}: {error.message}"
            )
            continue
        required = schema.get("required")
        properties = schema.get("properties")
        expected_fields = SCHEMA_REQUIRED_FIELDS[identity]
        if (
            not isinstance(required, list)
            or set(required) != expected_fields
            or not isinstance(properties, dict)
            or set(properties) != expected_fields
            or schema.get("additionalProperties") is not False
        ):
            failures.append(
                f"Research Catalog schema top-level contract mismatch: "
                f"{expected_path}"
            )
            continue
        validators[identity] = Draft202012Validator(schema)

    try:
        records = load_card_directory(root)
    except CardContractError as error:
        failures.append(str(error))
        records = []
    card_validator = validators.get(("research-card", 1))
    if card_validator is not None:
        for record in records:
            card = record.get("card")
            for error in card_validator.iter_errors(card):
                failures.append(
                    "Research Card schema violation: "
                    f"{record.get('path')}: {error.message}"
                )
    try:
        packet_fixture = json.loads(
            (root / INDEPENDENT_PACKET_FIXTURE).read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"Cannot read independent packet fixture: {error}")
    else:
        packet_validator = validators.get(("independent-research-packet", 1))
        if packet_validator is not None:
            for error in packet_validator.iter_errors(packet_fixture):
                failures.append(
                    f"Independent packet schema violation: {error.message}"
                )
        recorded = record_independent_packet(packet_fixture)
        if recorded.get("status") != "independent-recorded":
            failures.append(
                "Independent packet fixture does not record with its exact "
                "fingerprint."
            )
    try:
        catalog = json.loads((root / CATALOG_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"Cannot read derived Research Catalog: {error}")
        catalog = None
    if isinstance(catalog, dict):
        catalog_validator = validators.get(("research-catalog", 1))
        if catalog_validator is not None:
            for error in catalog_validator.iter_errors(catalog):
                failures.append(
                    f"Research Catalog schema violation: {error.message}"
                )
        generated_at = catalog.get("generated_at")
        if not _string(generated_at):
            failures.append("Derived Research Catalog has no generated_at.")
        else:
            try:
                expected_catalog = build_catalog(
                    records,
                    generated_at=str(generated_at),
                )
            except CardContractError as error:
                failures.append(str(error))
            else:
                if catalog != expected_catalog:
                    failures.append(
                        "Derived Research Catalog differs from canonical Cards."
                    )

    fixture_path = root / VALID_FIXTURE
    try:
        parse_card(fixture_path, root=root)
    except CardContractError as error:
        failures.append(f"Research Card fixture is invalid: {error}")

    readme_path = root / "docs/research/skill-pack-composition/README.md"
    try:
        readme = readme_path.read_text(encoding="utf-8")
    except OSError as error:
        failures.append(f"Cannot read Research Catalog owner README: {error}")
    else:
        for required in (
            "scripts.research_catalog",
            "catalog-not-admitted",
            "catalog-overflow",
            "docs/research/skill-pack-composition/catalog.json",
        ):
            if required not in readme:
                failures.append(
                    f"Research Catalog owner README misses contract: {required}"
                )
    return failures


def write_catalog(root: Path, *, generated_at: str) -> dict[str, object]:
    """Regenerate the tracked thin index from canonical Markdown Cards."""

    catalog = build_catalog(
        load_card_directory(root),
        generated_at=generated_at,
    )
    path = root / CATALOG_PATH
    path.write_bytes(
        (
            json.dumps(
                catalog,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
    )
    return catalog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("build", "validate"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--generated-at")
    arguments = parser.parse_args(argv)
    root = arguments.root.resolve()
    if arguments.action == "build":
        if not _string(arguments.generated_at):
            parser.error("build requires --generated-at")
        catalog = write_catalog(
            root,
            generated_at=str(arguments.generated_at),
        )
        print(f"Research Catalog built: {len(catalog['entries'])} entries.")
        return 0
    failures = validate_repository(root)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("Research Catalog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
