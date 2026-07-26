from __future__ import annotations

import json
from pathlib import Path

from scripts import fresh_epoch_contract, validate_skills


ROUTES = {
    "docs/research/README.md": [
        "docs/research/skill-pack-composition/README.md",
        "docs/research/skills/README.md",
    ],
    "docs/research/skill-pack-composition/README.md": [
        "docs/research/skill-pack-composition/cards",
        "docs/research/skill-pack-composition/sources",
    ],
    "docs/research/skills/README.md": ["docs/research/skills"],
    "docs/synthesis/README.md": [
        "docs/synthesis/skill-pack.md",
        "docs/synthesis/skills",
        "docs/synthesis/methods/README.md",
    ],
    "docs/synthesis/methods/README.md": [
        "docs/synthesis/methods/fresh-composition-epoch.md",
        "docs/synthesis/methods/deploy-prompts.md",
    ],
    "docs/validation/README.md": [
        "docs/validation/shared/README.md",
        "docs/validation/skills/README.md",
        "docs/validation/skill-pack/README.md",
    ],
    "docs/validation/shared/README.md": [
        "docs/validation/shared/protocols",
        "docs/validation/shared/fixtures",
        "docs/validation/shared/schemas",
    ],
}


def write_contract_tree(root: Path) -> dict[str, object]:
    for route, targets in ROUTES.items():
        path = root / route
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# {path.stem}\n\n" + "".join(f"- `{target}`\n" for target in targets),
            encoding="utf-8",
        )

    for relative in (
        "docs/research/skill-pack-composition/cards",
        "docs/research/skill-pack-composition/sources",
        "docs/research/skills",
        "docs/synthesis/skills",
        "docs/validation/shared/protocols",
        "docs/validation/shared/fixtures",
        "docs/validation/shared/schemas",
        "docs/validation/skills",
        "docs/validation/skill-pack",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)

    relationship_index = root / "docs/synthesis/skill-context-relationships.md"
    relationship_index.write_text("# Relationship Index\n", encoding="utf-8")
    (root / "docs/synthesis/methods/deploy-prompts.md").write_text(
        "# One-skill Deploy Campaign\n",
        encoding="utf-8",
    )
    legacy_fixture = (
        root / "docs/validation/shared/fixtures/campaign-manifest-v1.json"
    )
    legacy_fixture.write_text(
        json.dumps({"schema_version": 1, "campaign": {"id": "legacy"}}),
        encoding="utf-8",
    )

    schemas = [
        {
            "id": "fresh-epoch-topology",
            "version": 1,
            "path": (
                "docs/validation/shared/schemas/"
                "fresh-epoch-topology-v1.schema.json"
            ),
        },
        {
            "id": "exact-content-fingerprint",
            "version": 1,
            "path": (
                "docs/validation/shared/schemas/"
                "exact-content-fingerprint-v1.schema.json"
            ),
        },
    ]
    schema_registry = root / "docs/validation/shared/schemas/registry.json"
    schema_registry.write_text(
        json.dumps({"format": 1, "schemas": schemas}),
        encoding="utf-8",
    )
    for schema in schemas:
        (root / str(schema["path"])).write_text(
            json.dumps(
                {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "$id": f"urn:programming-agent-skills:{schema['id']}:v1",
                    "type": "object",
                }
            ),
            encoding="utf-8",
        )

    topology: dict[str, object] = {
        "format": 1,
        "fingerprint": {
            "algorithm": "sha256",
            "format": "sha256-v1",
            "pattern": "^sha256-v1:[0-9a-f]{64}$",
        },
        "routes": [
            {"path": path, "targets": targets} for path, targets in ROUTES.items()
        ],
        "owners": [
            {
                "information_class": "research-card",
                "path": "docs/research/skill-pack-composition/cards",
                "route": "docs/research/skill-pack-composition/README.md",
                "required": True,
                "identity_family": "research-card",
            },
            {
                "information_class": "source-record",
                "path": "docs/research/skill-pack-composition/sources",
                "route": "docs/research/skill-pack-composition/README.md",
                "required": True,
                "identity_family": "source-record",
            },
            {
                "information_class": "skill-research-packet",
                "path": "docs/research/skills",
                "route": "docs/research/skills/README.md",
                "required": True,
                "identity_family": "skill-research-packet",
            },
            {
                "information_class": "pack-composition-contract",
                "path": "docs/synthesis/skill-pack.md",
                "route": "docs/synthesis/README.md",
                "required": False,
            },
            {
                "information_class": "per-skill-synthesis",
                "path": "docs/synthesis/skills",
                "route": "docs/synthesis/README.md",
                "required": True,
            },
            {
                "information_class": "fresh-epoch-controller",
                "path": "docs/synthesis/methods/fresh-composition-epoch.md",
                "route": "docs/synthesis/methods/README.md",
                "required": False,
            },
            {
                "information_class": "one-skill-controller",
                "path": "docs/synthesis/methods/deploy-prompts.md",
                "route": "docs/synthesis/methods/README.md",
                "required": True,
            },
            {
                "information_class": "shared-validation-contract",
                "path": "docs/validation/shared",
                "route": "docs/validation/shared/README.md",
                "required": True,
            },
            {
                "information_class": "per-skill-validation",
                "path": "docs/validation/skills",
                "route": "docs/validation/README.md",
                "required": True,
                "identity_family": "evaluation",
            },
            {
                "information_class": "pack-integration-validation",
                "path": "docs/validation/skill-pack",
                "route": "docs/validation/README.md",
                "required": True,
                "identity_family": "composition-epoch",
            },
        ],
        "identity_families": [
            {"name": "composition-epoch", "pattern": "^FCE-[0-9]{8}-[0-9]{2}$"},
            {"name": "research-card", "pattern": "^RC-[0-9]{4}$"},
            {"name": "card-claim", "pattern": "^RC-[0-9]{4}-C[0-9]{2}$"},
            {"name": "source-record", "pattern": "^SRC-[0-9]{4}$"},
            {
                "name": "skill-research-packet",
                "pattern": "^RP-[a-z0-9-]+-[0-9]{8}-[0-9]{2}$",
            },
            {
                "name": "evaluation",
                "pattern": "^EV-[a-z0-9-]+-[a-z0-9-]+-[0-9]{8}-[0-9]{2}$",
            },
            {"name": "migration-entry", "pattern": "^MIG-[0-9]{4}$"},
        ],
        "compatibility": {
            "campaign_manifest_versions": [1],
            "legacy_fixture": (
                "docs/validation/shared/fixtures/campaign-manifest-v1.json"
            ),
            "relationship_index": (
                "docs/synthesis/skill-context-relationships.md"
            ),
        },
        "privacy": {
            "public_sources": "docs/research/skill-pack-composition/sources",
            "private_ignore": "sources/",
            "public_unignore": [
                "!docs/research/skill-pack-composition/sources/",
                "!docs/research/skill-pack-composition/sources/**",
            ],
            "forbidden_authority_keys": [
                "acceptance_decision",
                "adoption",
                "h1",
                "recommendation",
                "rubric_score",
            ],
        },
        "schema_registry": "docs/validation/shared/schemas/registry.json",
    }
    contract = root / "docs/validation/shared/fresh-epoch-topology.json"
    contract.write_text(json.dumps(topology), encoding="utf-8")
    (root / ".gitignore").write_text(
        "sources/\n"
        "!docs/research/skill-pack-composition/sources/\n"
        "!docs/research/skill-pack-composition/sources/**\n",
        encoding="utf-8",
    )
    return topology


def validate(root: Path) -> list[str]:
    validator = getattr(validate_skills, "validate_fresh_epoch_contract", None)
    assert callable(validator), "validate_skills must expose the fresh-epoch seam"
    return validator(root)


def test_exact_content_fingerprint_is_versioned_and_deterministic() -> None:
    assert fresh_epoch_contract.exact_content_fingerprint(b"abc") == (
        "sha256-v1:"
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_fresh_epoch_contract_accepts_current_compatible_topology(
    tmp_path: Path,
) -> None:
    write_contract_tree(tmp_path)

    assert validate(tmp_path) == []


def test_fresh_epoch_contract_rejects_missing_owner_and_owner_collision(
    tmp_path: Path,
) -> None:
    topology = write_contract_tree(tmp_path)
    (tmp_path / "docs/research/skills/README.md").unlink()

    failures = validate(tmp_path)

    assert any("Missing fresh-epoch route" in failure for failure in failures)

    write_contract_tree(tmp_path)
    topology["owners"].append(
        {
            "information_class": "colliding-owner",
            "path": "docs/research/skills",
            "route": "docs/research/skills/README.md",
            "required": True,
        }
    )
    (tmp_path / "docs/validation/shared/fresh-epoch-topology.json").write_text(
        json.dumps(topology),
        encoding="utf-8",
    )

    failures = validate(tmp_path)

    assert any("Owner path collision" in failure for failure in failures)


def test_fresh_epoch_contract_requires_canonical_registry_entries(
    tmp_path: Path,
) -> None:
    topology = write_contract_tree(tmp_path)
    contract = tmp_path / "docs/validation/shared/fresh-epoch-topology.json"
    topology["owners"] = topology["owners"][1:]
    contract.write_text(json.dumps(topology), encoding="utf-8")
    assert any("Missing required fresh-epoch owner" in item for item in validate(tmp_path))

    topology = write_contract_tree(tmp_path)
    topology["routes"] = topology["routes"][1:]
    contract.write_text(json.dumps(topology), encoding="utf-8")
    assert any("Missing required fresh-epoch route" in item for item in validate(tmp_path))

    topology = write_contract_tree(tmp_path)
    topology["identity_families"] = topology["identity_families"][1:]
    contract.write_text(json.dumps(topology), encoding="utf-8")
    assert any("Missing required identity family" in item for item in validate(tmp_path))

    topology = write_contract_tree(tmp_path)
    topology["identity_families"][0]["pattern"] = ".*"
    contract.write_text(json.dumps(topology), encoding="utf-8")
    assert any("Identity family pattern drift" in item for item in validate(tmp_path))

    write_contract_tree(tmp_path)
    registry = tmp_path / "docs/validation/shared/schemas/registry.json"
    payload = json.loads(registry.read_text(encoding="utf-8"))
    payload["schemas"] = payload["schemas"][1:]
    registry.write_text(json.dumps(payload), encoding="utf-8")
    assert any("Missing required fresh-epoch schema" in item for item in validate(tmp_path))

    write_contract_tree(tmp_path)
    assert validate(tmp_path) == []


def test_fresh_epoch_contract_rejects_duplicate_ids(tmp_path: Path) -> None:
    write_contract_tree(tmp_path)
    cards = tmp_path / "docs/research/skill-pack-composition/cards"
    (cards / "one.md").write_text(
        "---\nartifact_id: RC-0001\n---\n", encoding="utf-8"
    )
    (cards / "two.md").write_text(
        "---\nartifact_id: RC-0001\n---\n", encoding="utf-8"
    )

    failures = validate(tmp_path)

    assert any("Duplicate stable ID: RC-0001" in failure for failure in failures)


def test_fresh_epoch_contract_rejects_nested_malformed_and_duplicate_ids(
    tmp_path: Path,
) -> None:
    write_contract_tree(tmp_path)
    research = tmp_path / "docs/research/skills"
    (research / "alpha").mkdir()
    (research / "beta").mkdir()
    (research / "alpha/one.md").write_text(
        "---\nartifact_id: RP-alpha-20260725-01\n---\n",
        encoding="utf-8",
    )
    (research / "beta/two.md").write_text(
        "---\nartifact_id: RP-alpha-20260725-01\n---\n",
        encoding="utf-8",
    )
    (research / "beta/bad.md").write_text(
        "---\nartifact_id: invalid\n---\n",
        encoding="utf-8",
    )

    failures = validate(tmp_path)

    assert any(
        "Duplicate stable ID: RP-alpha-20260725-01" in failure
        for failure in failures
    )
    assert any(
        "artifact ID does not match skill-research-packet" in failure
        for failure in failures
    )

    write_contract_tree(tmp_path)
    validation = tmp_path / "docs/validation/skills"
    for skill in ("alpha", "beta"):
        (validation / skill / "evals/EV-alpha-routing-20260725-01").mkdir(
            parents=True
        )
    (validation / "beta/evals/invalid").mkdir()

    failures = validate(tmp_path)

    assert any(
        "Duplicate stable ID: EV-alpha-routing-20260725-01" in failure
        for failure in failures
    )
    assert any(
        "artifact ID does not match evaluation" in failure
        for failure in failures
    )

    for artifact in (
        research / "alpha/one.md",
        research / "beta/two.md",
        research / "beta/bad.md",
    ):
        artifact.unlink()
    (research / "alpha/one.md").write_text(
        "---\nartifact_id: RP-alpha-20260725-01\n---\n",
        encoding="utf-8",
    )
    (research / "beta/two.md").write_text(
        "---\nartifact_id: RP-beta-20260725-01\n---\n",
        encoding="utf-8",
    )
    (
        validation / "beta/evals/EV-alpha-routing-20260725-01"
    ).rmdir()
    (validation / "beta/evals/invalid").rmdir()
    (validation / "beta/evals/EV-beta-routing-20260725-01").mkdir()

    assert validate(tmp_path) == []


def test_fresh_epoch_contract_rejects_unsafe_paths(tmp_path: Path) -> None:
    topology = write_contract_tree(tmp_path)
    topology["owners"][0]["path"] = "../outside"
    (tmp_path / "docs/validation/shared/fresh-epoch-topology.json").write_text(
        json.dumps(topology),
        encoding="utf-8",
    )

    failures = validate(tmp_path)

    assert any("Unsafe fresh-epoch path" in failure for failure in failures)


def test_fresh_epoch_contract_rejects_windows_drive_paths(tmp_path: Path) -> None:
    for index, unsafe in enumerate(("C:/outside", "C:outside")):
        case = tmp_path / str(index)
        topology = write_contract_tree(case)
        topology["owners"][0]["path"] = unsafe
        (
            case / "docs/validation/shared/fresh-epoch-topology.json"
        ).write_text(json.dumps(topology), encoding="utf-8")

        failures = validate(case)

        assert any("Unsafe fresh-epoch path" in failure for failure in failures)


def test_fresh_epoch_contract_rejects_forbidden_source_authority(
    tmp_path: Path,
) -> None:
    write_contract_tree(tmp_path)
    source = tmp_path / "docs/research/skill-pack-composition/sources/source.md"
    source.write_text(
        "---\nartifact_id: SRC-0001\nadoption: selected\n---\n",
        encoding="utf-8",
    )

    failures = validate(tmp_path)

    assert any("forbidden authority key: adoption" in failure for failure in failures)


def test_fresh_epoch_contract_preserves_private_and_legacy_boundaries(
    tmp_path: Path,
) -> None:
    write_contract_tree(tmp_path)
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")
    legacy = tmp_path / "docs/validation/shared/fixtures/campaign-manifest-v1.json"
    legacy.write_text(
        json.dumps({"schema_version": 2, "campaign": {"id": "future"}}),
        encoding="utf-8",
    )

    failures = validate(tmp_path)

    assert "Private source root must remain ignored: sources/" in failures
    assert any(
        "Public source packet root must remain trackable" in failure
        for failure in failures
    )
    assert any(
        "Legacy campaign manifest requires schema version 1" in failure
        for failure in failures
    )
