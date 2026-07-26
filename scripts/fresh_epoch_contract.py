"""Validate the mechanical Fresh Composition Epoch ownership envelope."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


TOPOLOGY_PATH = "docs/validation/shared/fresh-epoch-topology.json"
REQUIRED_IDENTITY_PATTERNS = {
    "composition-epoch": r"^FCE-[0-9]{8}-[0-9]{2}$",
    "research-card": r"^RC-[0-9]{4}$",
    "card-claim": r"^RC-[0-9]{4}-C[0-9]{2}$",
    "source-record": r"^SRC-[0-9]{4}$",
    "skill-research-packet": r"^RP-[a-z0-9-]+-[0-9]{8}-[0-9]{2}$",
    "evaluation": r"^EV-[a-z0-9-]+-[a-z0-9-]+-[0-9]{8}-[0-9]{2}$",
    "migration-entry": r"^MIG-[0-9]{4}$",
}
REQUIRED_ROUTES = {
    "docs/research/README.md": frozenset(
        {
            "docs/research/skill-pack-composition/README.md",
            "docs/research/skills/README.md",
        }
    ),
    "docs/research/skill-pack-composition/README.md": frozenset(
        {
            "docs/research/skill-pack-composition/cards",
            "docs/research/skill-pack-composition/sources",
        }
    ),
    "docs/research/skills/README.md": frozenset({"docs/research/skills"}),
    "docs/synthesis/README.md": frozenset(
        {
            "docs/synthesis/skill-pack.md",
            "docs/synthesis/skills",
            "docs/synthesis/methods/README.md",
        }
    ),
    "docs/synthesis/methods/README.md": frozenset(
        {
            "docs/synthesis/methods/fresh-composition-epoch.md",
            "docs/synthesis/methods/deploy-prompts.md",
        }
    ),
    "docs/validation/README.md": frozenset(
        {
            "docs/validation/shared/README.md",
            "docs/validation/skills/README.md",
            "docs/validation/skill-pack/README.md",
        }
    ),
    "docs/validation/shared/README.md": frozenset(
        {
            "docs/validation/shared/protocols",
            "docs/validation/shared/fixtures",
            "docs/validation/shared/schemas",
        }
    ),
}
REQUIRED_OWNERS = {
    "research-card": {
        "path": "docs/research/skill-pack-composition/cards",
        "route": "docs/research/skill-pack-composition/README.md",
        "required": True,
        "identity_family": "research-card",
    },
    "source-record": {
        "path": "docs/research/skill-pack-composition/sources",
        "route": "docs/research/skill-pack-composition/README.md",
        "required": True,
        "identity_family": "source-record",
    },
    "skill-research-packet": {
        "path": "docs/research/skills",
        "route": "docs/research/skills/README.md",
        "required": True,
        "identity_family": "skill-research-packet",
    },
    "pack-composition-contract": {
        "path": "docs/synthesis/skill-pack.md",
        "route": "docs/synthesis/README.md",
        "required": False,
    },
    "per-skill-synthesis": {
        "path": "docs/synthesis/skills",
        "route": "docs/synthesis/README.md",
        "required": True,
    },
    "fresh-epoch-controller": {
        "path": "docs/synthesis/methods/fresh-composition-epoch.md",
        "route": "docs/synthesis/methods/README.md",
        "required": False,
    },
    "one-skill-controller": {
        "path": "docs/synthesis/methods/deploy-prompts.md",
        "route": "docs/synthesis/methods/README.md",
        "required": True,
    },
    "shared-validation-contract": {
        "path": "docs/validation/shared",
        "route": "docs/validation/shared/README.md",
        "required": True,
    },
    "per-skill-validation": {
        "path": "docs/validation/skills",
        "route": "docs/validation/README.md",
        "required": True,
        "identity_family": "evaluation",
    },
    "pack-integration-validation": {
        "path": "docs/validation/skill-pack",
        "route": "docs/validation/README.md",
        "required": True,
        "identity_family": "composition-epoch",
    },
}
REQUIRED_SCHEMAS = {
    ("exact-content-fingerprint", 1): (
        "docs/validation/shared/schemas/"
        "exact-content-fingerprint-v1.schema.json"
    ),
    ("fresh-epoch-topology", 1): (
        "docs/validation/shared/schemas/fresh-epoch-topology-v1.schema.json"
    ),
}
IDENTITY_SCAN_RULES = {
    "research-card": ("metadata", "*", True),
    "source-record": ("metadata", "*", True),
    "skill-research-packet": ("metadata", "**/*", True),
    "per-skill-validation": ("directory", "*/evals/*", True),
    "pack-integration-validation": ("directory", "*", True),
}
MARKDOWN_FRONTMATTER_RE = re.compile(
    r"\A---\s*\r?\n(?P<body>.*?)\r?\n---(?:\s*\r?\n|\Z)",
    re.DOTALL,
)
MARKDOWN_FIELD_RE = re.compile(r"(?m)^([a-zA-Z0-9_-]+):\s*(.*?)\s*$")


def exact_content_fingerprint(content: bytes) -> str:
    """Return the v1 exact-byte identity used by mutable epoch artifacts."""

    return f"sha256-v1:{hashlib.sha256(content).hexdigest()}"


def _read_json(path: Path, failures: list[str], label: str) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"Cannot read {label}: {path}: {error}")
        return None


def _safe_relative_path(value: object) -> str | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    if re.match(r"^[A-Za-z]:", value):
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value:
        return None
    if any(part in {"", ".", ".."} for part in path.parts):
        return None
    return value


def _record_path(
    value: object,
    failures: list[str],
    *,
    context: str,
) -> str | None:
    safe = _safe_relative_path(value)
    if safe is None:
        failures.append(f"Unsafe fresh-epoch path in {context}: {value!r}")
    return safe


def _markdown_metadata(path: Path) -> dict[str, str]:
    match = MARKDOWN_FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if match is None:
        return {}
    return {
        key: value.strip().strip("\"'")
        for key, value in MARKDOWN_FIELD_RE.findall(match.group("body"))
    }


def _artifact_metadata(path: Path) -> dict[str, object]:
    if path.suffix == ".md":
        return _markdown_metadata(path)
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    return {}


def _validate_routes(
    root: Path,
    payload: dict[str, object],
    failures: list[str],
) -> None:
    routes = payload.get("routes")
    if not isinstance(routes, list):
        failures.append("Fresh-epoch routes must be a list.")
        return

    seen: set[str] = set()
    observed: dict[str, set[str]] = {}
    for index, entry in enumerate(routes):
        if not isinstance(entry, dict):
            failures.append(f"Fresh-epoch route {index} must be an object.")
            continue
        route = _record_path(
            entry.get("path"),
            failures,
            context=f"route {index}",
        )
        if route is None:
            continue
        if route in seen:
            failures.append(f"Duplicate fresh-epoch route: {route}")
        seen.add(route)
        route_path = root / route
        if not route_path.is_file():
            failures.append(f"Missing fresh-epoch route: {route}")
            continue
        try:
            text = route_path.read_text(encoding="utf-8")
        except OSError as error:
            failures.append(f"Cannot read fresh-epoch route: {route}: {error}")
            continue
        targets = entry.get("targets")
        if not isinstance(targets, list) or not targets:
            failures.append(f"Fresh-epoch route has no targets: {route}")
            continue
        observed[route] = {
            target for target in targets if isinstance(target, str)
        }
        for target_index, raw_target in enumerate(targets):
            target = _record_path(
                raw_target,
                failures,
                context=f"route {route} target {target_index}",
            )
            if target is not None and target not in text:
                failures.append(
                    f"Fresh-epoch route does not point to target: {route} -> {target}"
                )
    for route, required_targets in REQUIRED_ROUTES.items():
        if route not in observed:
            failures.append(f"Missing required fresh-epoch route: {route}")
            continue
        missing_targets = required_targets - observed[route]
        for target in sorted(missing_targets):
            failures.append(
                f"Missing required fresh-epoch route target: {route} -> {target}"
            )


def _validate_identities(
    payload: dict[str, object],
    failures: list[str],
) -> dict[str, re.Pattern[str]]:
    families = payload.get("identity_families")
    if not isinstance(families, list):
        failures.append("Fresh-epoch identity_families must be a list.")
        return {}

    compiled: dict[str, re.Pattern[str]] = {}
    observed_patterns: dict[str, str] = {}
    for index, entry in enumerate(families):
        if not isinstance(entry, dict):
            failures.append(f"Identity family {index} must be an object.")
            continue
        name = entry.get("name")
        pattern = entry.get("pattern")
        if not isinstance(name, str) or not name:
            failures.append(f"Identity family {index} has no name.")
            continue
        if name in compiled:
            failures.append(f"Duplicate identity family: {name}")
            continue
        if not isinstance(pattern, str):
            failures.append(f"Identity family has no pattern: {name}")
            continue
        try:
            compiled[name] = re.compile(pattern)
        except re.error as error:
            failures.append(f"Identity family pattern is invalid: {name}: {error}")
        else:
            observed_patterns[name] = pattern
    for name, expected_pattern in REQUIRED_IDENTITY_PATTERNS.items():
        observed_pattern = observed_patterns.get(name)
        if observed_pattern is None:
            failures.append(f"Missing required identity family: {name}")
        elif observed_pattern != expected_pattern:
            failures.append(
                f"Identity family pattern drift: {name} -> {observed_pattern!r}"
            )
    return compiled


def _record_observed_id(
    artifact_id: object,
    *,
    family_name: str,
    family: re.Pattern[str],
    relative: str,
    observed_ids: dict[str, str],
    failures: list[str],
) -> None:
    if not isinstance(artifact_id, str) or family.fullmatch(artifact_id) is None:
        failures.append(
            f"Fresh-epoch artifact ID does not match {family_name}: "
            f"{artifact_id!r} -> {relative}"
        )
        return
    prior = observed_ids.get(artifact_id)
    if prior is not None:
        failures.append(
            f"Duplicate stable ID: {artifact_id} -> {prior}, {relative}"
        )
    observed_ids[artifact_id] = relative


def _scan_owner_identifiers(
    root: Path,
    *,
    information_class: str,
    owner_path: Path,
    family_name: str,
    family: re.Pattern[str],
    observed_ids: dict[str, str],
    failures: list[str],
) -> None:
    mode, pattern, require_id = IDENTITY_SCAN_RULES.get(
        information_class,
        ("metadata", "*", True),
    )
    if mode == "directory":
        for artifact in sorted(owner_path.glob(pattern)):
            if not artifact.is_dir():
                continue
            _record_observed_id(
                artifact.name,
                family_name=family_name,
                family=family,
                relative=artifact.relative_to(root).as_posix(),
                observed_ids=observed_ids,
                failures=failures,
            )
        return

    for artifact in sorted(owner_path.glob(pattern)):
        if not artifact.is_file() or artifact.name.casefold() == "readme.md":
            continue
        if artifact.suffix not in {".md", ".json"}:
            continue
        relative = artifact.relative_to(root).as_posix()
        try:
            metadata = _artifact_metadata(artifact)
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"Cannot read fresh-epoch artifact: {artifact}: {error}")
            continue
        artifact_id = metadata.get("artifact_id")
        if artifact_id is None:
            if require_id:
                failures.append(
                    f"Fresh-epoch artifact has no stable ID: {relative}"
                )
            continue
        _record_observed_id(
            artifact_id,
            family_name=family_name,
            family=family,
            relative=relative,
            observed_ids=observed_ids,
            failures=failures,
        )


def _validate_owners(
    root: Path,
    payload: dict[str, object],
    identities: dict[str, re.Pattern[str]],
    failures: list[str],
) -> None:
    owners = payload.get("owners")
    if not isinstance(owners, list):
        failures.append("Fresh-epoch owners must be a list.")
        return

    seen_classes: set[str] = set()
    seen_paths: dict[str, str] = {}
    observed_ids: dict[str, str] = {}
    observed_owners: dict[str, dict[str, object]] = {}
    for index, entry in enumerate(owners):
        if not isinstance(entry, dict):
            failures.append(f"Fresh-epoch owner {index} must be an object.")
            continue
        information_class = entry.get("information_class")
        if not isinstance(information_class, str) or not information_class:
            failures.append(f"Fresh-epoch owner {index} has no information class.")
            continue
        if information_class in seen_classes:
            failures.append(f"Duplicate information-class owner: {information_class}")
        seen_classes.add(information_class)
        observed_owners[information_class] = entry

        owner = _record_path(
            entry.get("path"),
            failures,
            context=f"owner {information_class}",
        )
        route = _record_path(
            entry.get("route"),
            failures,
            context=f"owner {information_class} route",
        )
        if owner is None or route is None:
            continue
        prior_class = seen_paths.get(owner)
        if prior_class is not None:
            failures.append(
                f"Owner path collision: {owner} -> "
                f"{prior_class}, {information_class}"
            )
        seen_paths[owner] = information_class

        route_path = root / route
        if not route_path.is_file():
            failures.append(f"Missing fresh-epoch owner route: {route}")
        else:
            try:
                route_text = route_path.read_text(encoding="utf-8")
            except OSError as error:
                failures.append(
                    f"Cannot read fresh-epoch owner route: {route}: {error}"
                )
            else:
                if owner not in route_text:
                    failures.append(
                        f"Fresh-epoch owner route does not name owner: "
                        f"{route} -> {owner}"
                    )
        if entry.get("required") is not False and not (root / owner).exists():
            failures.append(f"Missing fresh-epoch owner: {owner}")

        family_name = entry.get("identity_family")
        if family_name is None:
            continue
        family = identities.get(str(family_name))
        if family is None:
            failures.append(
                f"Fresh-epoch owner uses unknown identity family: "
                f"{information_class} -> {family_name}"
            )
            continue
        owner_path = root / owner
        if not owner_path.is_dir():
            continue
        _scan_owner_identifiers(
            root,
            information_class=information_class,
            owner_path=owner_path,
            family_name=str(family_name),
            family=family,
            observed_ids=observed_ids,
            failures=failures,
        )

    for information_class, expected in REQUIRED_OWNERS.items():
        observed = observed_owners.get(information_class)
        if observed is None:
            failures.append(
                f"Missing required fresh-epoch owner: {information_class}"
            )
            continue
        for field, value in expected.items():
            if observed.get(field) != value:
                failures.append(
                    f"Fresh-epoch owner contract drift: {information_class} "
                    f"{field} -> {observed.get(field)!r}"
                )


def _validate_schema_registry(
    root: Path,
    payload: dict[str, object],
    failures: list[str],
) -> None:
    relative = _record_path(
        payload.get("schema_registry"),
        failures,
        context="schema registry",
    )
    if relative is None:
        return
    registry = _read_json(root / relative, failures, "fresh-epoch schema registry")
    if not isinstance(registry, dict):
        return
    if registry.get("format") != 1:
        failures.append("Fresh-epoch schema registry must use format 1.")
    schemas = registry.get("schemas")
    if not isinstance(schemas, list):
        failures.append("Fresh-epoch schema registry schemas must be a list.")
        return

    seen: set[tuple[str, int]] = set()
    seen_paths: set[str] = set()
    observed_schemas: dict[tuple[str, int], str] = {}
    for index, entry in enumerate(schemas):
        if not isinstance(entry, dict):
            failures.append(f"Fresh-epoch schema {index} must be an object.")
            continue
        schema_id = entry.get("id")
        version = entry.get("version")
        path = _record_path(
            entry.get("path"),
            failures,
            context=f"schema {index}",
        )
        if not isinstance(schema_id, str) or not schema_id:
            failures.append(f"Fresh-epoch schema {index} has no ID.")
            continue
        if not isinstance(version, int) or version < 1:
            failures.append(f"Fresh-epoch schema has invalid version: {schema_id}")
            continue
        identity = (schema_id, version)
        if identity in seen:
            failures.append(
                f"Duplicate fresh-epoch schema identity: {schema_id} v{version}"
            )
        seen.add(identity)
        if path is None:
            continue
        observed_schemas[identity] = path
        if path in seen_paths:
            failures.append(f"Fresh-epoch schema path collision: {path}")
        seen_paths.add(path)
        schema = _read_json(root / path, failures, f"fresh-epoch schema {schema_id}")
        expected_id = f"urn:programming-agent-skills:{schema_id}:v{version}"
        if isinstance(schema, dict) and schema.get("$id") != expected_id:
            failures.append(
                f"Fresh-epoch schema $id mismatch: {path} -> {expected_id}"
            )
    for identity, expected_path in REQUIRED_SCHEMAS.items():
        observed_path = observed_schemas.get(identity)
        if observed_path is None:
            failures.append(
                f"Missing required fresh-epoch schema: "
                f"{identity[0]} v{identity[1]}"
            )
        elif observed_path != expected_path:
            failures.append(
                f"Fresh-epoch schema path drift: "
                f"{identity[0]} v{identity[1]} -> {observed_path}"
            )


def _validate_compatibility(
    root: Path,
    payload: dict[str, object],
    failures: list[str],
) -> None:
    compatibility = payload.get("compatibility")
    if not isinstance(compatibility, dict):
        failures.append("Fresh-epoch compatibility must be an object.")
        return
    versions = compatibility.get("campaign_manifest_versions")
    if versions != [1]:
        failures.append("Fresh-epoch compatibility must preserve manifest version 1.")

    fixture = _record_path(
        compatibility.get("legacy_fixture"),
        failures,
        context="legacy manifest fixture",
    )
    if fixture is not None:
        manifest = _read_json(root / fixture, failures, "legacy campaign manifest")
        if isinstance(manifest, dict) and manifest.get("schema_version") != 1:
            failures.append(
                f"Legacy campaign manifest requires schema version 1: {fixture}"
            )

    relationship_index = _record_path(
        compatibility.get("relationship_index"),
        failures,
        context="relationship index",
    )
    if relationship_index is not None:
        path = root / relationship_index
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as error:
            failures.append(
                f"Cannot read compatibility relationship index: "
                f"{relationship_index}: {error}"
            )
        else:
            if not content.strip():
                failures.append(
                    f"Compatibility relationship index is empty: {relationship_index}"
                )


def _validate_privacy(
    root: Path,
    payload: dict[str, object],
    failures: list[str],
) -> None:
    privacy = payload.get("privacy")
    if not isinstance(privacy, dict):
        failures.append("Fresh-epoch privacy must be an object.")
        return
    public_sources = _record_path(
        privacy.get("public_sources"),
        failures,
        context="public source root",
    )
    private_ignore = privacy.get("private_ignore")
    if private_ignore != "sources/":
        failures.append("Fresh-epoch privacy has no compatible private ignore rule.")
    public_unignore = privacy.get("public_unignore")
    expected_unignore = [
        "!docs/research/skill-pack-composition/sources/",
        "!docs/research/skill-pack-composition/sources/**",
    ]
    if public_unignore != expected_unignore:
        failures.append(
            "Fresh-epoch public source root must have the exact narrow unignore rules."
        )
    else:
        try:
            ignore_rules = {
                line.strip()
                for line in (root / ".gitignore").read_text(
                    encoding="utf-8"
                ).splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            }
        except OSError as error:
            failures.append(f"Cannot read .gitignore for private source rule: {error}")
        else:
            if private_ignore not in ignore_rules:
                failures.append(
                    f"Private source root must remain ignored: {private_ignore}"
                )
            for rule in expected_unignore:
                if rule not in ignore_rules:
                    failures.append(
                        f"Public source packet root must remain trackable: {rule}"
                    )

    forbidden = privacy.get("forbidden_authority_keys")
    if not isinstance(forbidden, list) or not all(
        isinstance(item, str) and item for item in forbidden
    ):
        failures.append("Fresh-epoch forbidden authority keys are invalid.")
        return
    if public_sources is None:
        return
    source_root = root / public_sources
    if not source_root.is_dir():
        failures.append(f"Missing public source packet root: {public_sources}")
        return
    for artifact in sorted(source_root.glob("*")):
        if not artifact.is_file() or artifact.name.casefold() == "readme.md":
            continue
        if artifact.suffix not in {".md", ".json"}:
            continue
        try:
            metadata = _artifact_metadata(artifact)
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"Cannot read public source packet: {artifact}: {error}")
            continue
        for key in forbidden:
            if key in metadata:
                failures.append(
                    f"Public source packet has forbidden authority key: {key} -> "
                    f"{artifact.relative_to(root).as_posix()}"
                )


def validate_repository(root: Path) -> list[str]:
    """Return deterministic topology, identity, compatibility, and privacy failures."""

    failures: list[str] = []
    payload = _read_json(
        root / TOPOLOGY_PATH,
        failures,
        "fresh-epoch topology",
    )
    if not isinstance(payload, dict):
        return failures
    if payload.get("format") != 1:
        failures.append("Fresh-epoch topology must use format 1.")

    fingerprint = payload.get("fingerprint")
    if not isinstance(fingerprint, dict):
        failures.append("Fresh-epoch fingerprint contract must be an object.")
    else:
        if fingerprint.get("algorithm") != "sha256":
            failures.append("Fresh-epoch fingerprint algorithm must be sha256.")
        if fingerprint.get("format") != "sha256-v1":
            failures.append("Fresh-epoch fingerprint format must be sha256-v1.")
        if fingerprint.get("pattern") != r"^sha256-v1:[0-9a-f]{64}$":
            failures.append("Fresh-epoch fingerprint pattern is incompatible.")

    _validate_routes(root, payload, failures)
    identities = _validate_identities(payload, failures)
    _validate_owners(root, payload, identities, failures)
    _validate_schema_registry(root, payload, failures)
    _validate_compatibility(root, payload, failures)
    _validate_privacy(root, payload, failures)
    return failures
