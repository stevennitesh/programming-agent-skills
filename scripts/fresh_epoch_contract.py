"""Validate the mechanical Fresh Composition Epoch ownership envelope."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
import subprocess
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
        "required": True,
    },
    "per-skill-synthesis": {
        "path": "docs/synthesis/skills",
        "route": "docs/synthesis/README.md",
        "required": True,
    },
    "fresh-epoch-controller": {
        "path": "docs/synthesis/methods/fresh-composition-epoch.md",
        "route": "docs/synthesis/methods/README.md",
        "required": True,
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
    ("pack-composition-contract", 1): (
        "docs/validation/shared/schemas/"
        "pack-composition-contract-v1.schema.json"
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


MIGRATION_DISPOSITIONS = frozenset(
    {
        "preserve-in-place",
        "move",
        "extract-and-preserve",
        "merge-index",
        "supersede",
        "archive",
        "remove",
        "owner-gap",
    }
)
EPOCH_DISPOSITIONS = frozenset(
    {
        "exact-reusable",
        "method-evidence-only",
        "historical-admission-only",
        "superseded",
        "unverifiable",
        "duplicate",
    }
)
CATALOG_QUERY_DISPOSITIONS = frozenset(
    {
        "relevant-evidence",
        "already-represented",
        "not-applicable",
        "counterevidence",
        "unverified-gap",
    }
)
PROOF_REUSE_DISPOSITIONS = frozenset(
    {"exact-reusable", "lane-limited", "invalidated", "missing"}
)
MIGRATION_STATUSES = frozenset(
    {
        "inventoried",
        "prepared",
        "moved",
        "references-reconciled",
        "verified",
        "blocked",
    }
)
UNSAFE_REMOVAL_BASES = frozenset(
    {"age", "old", "verbose", "verbosity", "low-link-count", "non-adoption"}
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")


def _migration_rows(
    payload: dict[str, object],
    *,
    visibility: str,
    failures: list[str],
) -> list[dict[str, object]]:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        failures.append(f"{visibility.title()} migration rows must be a list.")
        return []
    result: list[dict[str, object]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            failures.append(
                f"{visibility.title()} migration row {index} must be an object."
            )
            continue
        result.append(row)
    return result


def _validate_migration_row(
    row: dict[str, object],
    *,
    visibility: str,
    seen_ids: set[str],
    seen_sources: set[str],
    failures: list[str],
) -> None:
    migration_id = row.get("migration_id")
    if (
        not isinstance(migration_id, str)
        or re.fullmatch(r"MIG-[0-9]{4}", migration_id) is None
    ):
        failures.append(f"Invalid migration ID: {migration_id!r}")
    elif migration_id in seen_ids:
        failures.append(f"Duplicate migration ID: {migration_id}")
    else:
        seen_ids.add(migration_id)

    source = row.get("source")
    if not isinstance(source, dict):
        failures.append(f"Migration row has no source: {migration_id}")
        return
    source_key = source.get("key")
    if not isinstance(source_key, str) or not source_key:
        failures.append(f"Migration row has no source key: {migration_id}")
        return
    if source_key in seen_sources:
        failures.append(f"Duplicate migration source: {source_key}")
    else:
        seen_sources.add(source_key)

    state = source.get("state")
    is_private = state in {"private-ignored", "ignored", "local-residue"}
    if visibility == "public" and is_private:
        failures.append(f"Private inventory leaked into public ledger: {migration_id}")

    fingerprint = source.get("fingerprint")
    if fingerprint is None:
        if row.get("status") != "blocked":
            failures.append(f"Unreadable source must be blocked: {migration_id}")
        if source.get("identity") is not None:
            failures.append(
                f"Unreadable source identity must not be inferred: {migration_id}"
            )
    elif (
        not isinstance(fingerprint, str)
        or re.fullmatch(r"sha256-v1:[0-9a-f]{64}", fingerprint) is None
    ):
        failures.append(f"Invalid source fingerprint: {migration_id}")
    if (
        row.get("artifact_class") == "campaign"
        and source.get("identity") is None
    ):
        failures.append(
            f"Campaign member has no applicable identity: {migration_id}"
        )

    axes = (
        ("migration_disposition", MIGRATION_DISPOSITIONS),
        ("epoch_disposition", EPOCH_DISPOSITIONS),
        ("catalog_query_disposition", CATALOG_QUERY_DISPOSITIONS),
        ("proof_reuse_disposition", PROOF_REUSE_DISPOSITIONS),
    )
    if any(row.get(name) not in allowed for name, allowed in axes):
        failures.append(
            f"Migration row requires distinct disposition axes: {migration_id}"
        )

    owner = row.get("owner")
    owner_gap = row.get("owner_gap")
    disposition = row.get("migration_disposition")
    if disposition == "owner-gap":
        if not isinstance(owner_gap, str) or not owner_gap:
            failures.append(f"Owner-gap row must explain the gap: {migration_id}")
    elif not isinstance(owner, str) or not owner:
        failures.append(f"Migration row has no owner: {migration_id}")

    status = row.get("status")
    if status not in MIGRATION_STATUSES:
        failures.append(f"Invalid migration status: {migration_id} -> {status!r}")
    if status == "verified":
        required_proof = row.get("required_proof")
        observed_result = row.get("observed_result")
        if (
            not isinstance(required_proof, list)
            or not required_proof
            or not isinstance(observed_result, dict)
            or observed_result.get("passed") is not True
        ):
            failures.append(f"Migration row verified before proof: {migration_id}")

    recovery = row.get("recovery")
    if not isinstance(recovery, dict) or not recovery.get("pointer"):
        failures.append(f"Migration row has no recovery pointer: {migration_id}")
    elif disposition in {"move", "remove"} and not recovery.get("applicable_lock"):
        failures.append(
            f"Migration move/remove row requires an applicable Lock: {migration_id}"
        )

    basis = row.get("basis")
    if disposition == "remove" and isinstance(basis, list):
        normalized_basis = {
            item.casefold() for item in basis if isinstance(item, str)
        }
        unsafe = sorted(normalized_basis & UNSAFE_REMOVAL_BASES)
        if unsafe:
            failures.append(
                f"Migration row has unsafe removal basis: "
                f"{migration_id} -> {', '.join(unsafe)}"
            )


def validate_migration_control(
    public: dict[str, object],
    private: dict[str, object],
    observed: dict[str, object],
) -> list[str]:
    """Validate one complete public/private migration fixed point."""

    failures: list[str] = []
    if public.get("format") != 1:
        failures.append("Public migration control must use format 1.")
    if private.get("format") != 1:
        failures.append("Private migration control must use format 1.")

    fixed_point = public.get("fixed_point")
    if not isinstance(fixed_point, dict):
        failures.append("Migration control has no fixed point.")
        fixed_point = {}
    source_head = fixed_point.get("source_head")
    if (
        not isinstance(source_head, str)
        or re.fullmatch(r"[0-9a-f]{40}", source_head) is None
    ):
        failures.append("Migration control has no valid source HEAD.")
    private_fixed_point = private.get("fixed_point")
    if (
        not isinstance(private_fixed_point, dict)
        or private_fixed_point.get("source_head") != source_head
    ):
        failures.append("Private migration source HEAD does not match.")
    for key in (
        "public_inventory_fingerprint",
        "private_inventory_fingerprint",
    ):
        if fixed_point.get(key) != observed.get(key):
            failures.append(f"Fixed point drift: {key}")

    public_rows = _migration_rows(
        public,
        visibility="public",
        failures=failures,
    )
    private_rows = _migration_rows(
        private,
        visibility="private",
        failures=failures,
    )
    seen_ids: set[str] = set()
    seen_sources: set[str] = set()
    public_sources: set[str] = set()
    private_sources: set[str] = set()
    for row in public_rows:
        _validate_migration_row(
            row,
            visibility="public",
            seen_ids=seen_ids,
            seen_sources=seen_sources,
            failures=failures,
        )
        source = row.get("source")
        if isinstance(source, dict) and isinstance(source.get("key"), str):
            public_sources.add(str(source["key"]))
    for row in private_rows:
        _validate_migration_row(
            row,
            visibility="private",
            seen_ids=seen_ids,
            seen_sources=seen_sources,
            failures=failures,
        )
        source = row.get("source")
        if isinstance(source, dict) and isinstance(source.get("key"), str):
            private_sources.add(str(source["key"]))

    observed_public = {
        str(item) for item in observed.get("public_source_keys", [])
    }
    observed_private = {
        str(item) for item in observed.get("private_source_keys", [])
    }
    for source_key in sorted(observed_public - public_sources):
        failures.append(f"Missing migration row: {source_key}")
    for source_key in sorted(public_sources - observed_public):
        failures.append(f"Stale migration row: {source_key}")
    for source_key in sorted(observed_private - private_sources):
        failures.append(f"Missing private migration row: {source_key}")
    for source_key in sorted(private_sources - observed_private):
        failures.append(f"Stale private migration row: {source_key}")
    return failures


def _path_fingerprint(path: Path) -> str | None:
    try:
        if path.is_file():
            return exact_content_fingerprint(path.read_bytes())
        if path.is_dir():
            if (path / ".git").exists():
                repository_fingerprint = _repository_fingerprint(path)
                if repository_fingerprint is not None:
                    return repository_fingerprint
            digest = hashlib.sha256()
            for child in sorted(
                (item for item in path.rglob("*") if item.is_file()),
                key=lambda item: item.relative_to(path).as_posix(),
            ):
                relative = child.relative_to(path).as_posix().encode("utf-8")
                content = child.read_bytes()
                digest.update(len(relative).to_bytes(8, "big"))
                digest.update(relative)
                digest.update(len(content).to_bytes(8, "big"))
                digest.update(content)
            return f"sha256-v1:{digest.hexdigest()}"
    except OSError:
        return None
    return None


def _repository_fingerprint(path: Path) -> str | None:
    """Fingerprint a local Git evidence root without hashing unchanged objects."""

    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=path,
            check=True,
            capture_output=True,
        ).stdout.strip()
        diff = subprocess.run(
            ["git", "diff", "--binary", "HEAD", "--"],
            cwd=path,
            check=True,
            capture_output=True,
        ).stdout
        untracked_output = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
            cwd=path,
            check=True,
            capture_output=True,
        ).stdout
        untracked = [
            item
            for item in untracked_output.split(b"\0")
            if item
        ]
        digest = hashlib.sha256()
        for label, content in ((b"HEAD", head), (b"DIFF", diff)):
            digest.update(label)
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
        for encoded_relative in sorted(untracked):
            relative = encoded_relative.decode(
                "utf-8",
                errors="surrogateescape",
            )
            content = (path / relative).read_bytes()
            digest.update(b"UNTRACKED")
            digest.update(len(encoded_relative).to_bytes(8, "big"))
            digest.update(encoded_relative)
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
        return f"sha256-v1:{digest.hexdigest()}"
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return None


def _artifact_identity(path: Path) -> str | None:
    try:
        if path.name == "manifest.json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            campaign = payload.get("campaign") if isinstance(payload, dict) else None
            if isinstance(campaign, dict):
                skill = campaign.get("skill")
                epoch = campaign.get("epoch")
                if isinstance(skill, str) and isinstance(epoch, str):
                    return f"campaign:{skill}:{epoch}"
                campaign_id = campaign.get("id")
                if isinstance(campaign_id, str):
                    return f"campaign:{campaign_id}"
        if path.suffix == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                artifact_id = payload.get("artifact_id")
                if isinstance(artifact_id, str):
                    return artifact_id
        if path.suffix == ".md":
            metadata = _artifact_metadata(path)
            artifact_id = metadata.get("artifact_id")
            if isinstance(artifact_id, str):
                return artifact_id
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return None


def _artifact_class(relative: str, state: str) -> str:
    if state in {"private-ignored", "ignored"}:
        return "private-evidence"
    if state == "local-residue":
        return "local-residue"
    for prefix, artifact_class in (
        (".archive/docs/", "historical-documentation"),
        ("docs/research/", "research"),
        ("docs/synthesis/", "synthesis"),
        ("docs/validation/campaigns/", "campaign"),
        ("docs/validation/evals/", "evaluation"),
        ("docs/validation/transcripts/", "validation-transcript"),
        ("docs/validation/", "validation"),
        ("skills/custom/", "active-runtime"),
        ("skills/experimental/", "experimental-runtime"),
        ("skills/extra/", "optional-runtime"),
        ("skills/.archive/", "retired-runtime"),
        ("docs/agents/", "control-plane"),
        ("docs/adr/", "decision"),
        ("docs/plans/", "control-plane"),
    ):
        if relative.startswith(prefix):
            return artifact_class
    return "control-plane"


def _migration_plan(
    relative: str,
    *,
    state: str,
) -> tuple[str, str | None, str | None, str | None, list[str]]:
    if state in {"private-ignored", "ignored"}:
        return (
            "preserve-in-place",
            "ignored-private-evidence",
            None,
            None,
            ["private-boundary", "preserve-first"],
        )
    if state == "local-residue":
        return (
            "remove",
            "local-residue-cleanup",
            None,
            None,
            ["empty-local-residue", "separately-authorized-cleanup"],
        )
    if relative.startswith("docs/research/skill-facets/"):
        parts = PurePosixPath(relative).parts
        skill = parts[3] if len(parts) > 3 else "unknown"
        return (
            "merge-index",
            f"docs/research/skills/{skill}/README.md",
            None,
            f"docs/research/skills/{skill}/<pending-packet-id>.md",
            ["issue-34-current-to-target-mapping"],
        )
    if relative.startswith("docs/research/language/skill pack ideas/"):
        return (
            "extract-and-preserve",
            "docs/research/skill-pack-composition/README.md",
            None,
            "docs/research/skill-pack-composition/sources/<pending-source-id>.md",
            ["issue-34-current-to-target-mapping"],
        )
    if relative == "docs/research/catalog-contract-research.md":
        return (
            "move",
            "docs/research/skill-pack-composition/README.md",
            None,
            "docs/research/skill-pack-composition/sources/<pending-source-id>.md",
            ["issue-34-current-to-target-mapping"],
        )
    if (
        relative.startswith("docs/research/")
        and len(PurePosixPath(relative).parts) == 3
        and PurePosixPath(relative).name.casefold() != "readme.md"
    ):
        return (
            "move",
            "docs/research/skills/README.md",
            None,
            "docs/research/skills/<owner-gap>/<pending-packet-id>.md",
            ["issue-34-current-to-target-mapping"],
        )
    if relative.startswith("docs/validation/campaigns/"):
        parts = PurePosixPath(relative).parts
        epoch = parts[3] if len(parts) > 3 else "<pending-epoch>"
        skill = epoch.rsplit("-", 3)[0] if "-" in epoch else "<owner-gap>"
        suffix = "/".join(parts[4:])
        target = f"docs/validation/skills/{skill}/campaigns/{epoch}"
        if suffix:
            target += f"/{suffix}"
        return (
            "move",
            f"docs/validation/skills/{skill}/README.md",
            None,
            target,
            ["issue-34-current-to-target-mapping"],
        )
    if relative.startswith(("docs/validation/evals/", "docs/validation/transcripts/")):
        return (
            "owner-gap",
            None,
            "Per-skill versus pack-level validation owner is not yet proved.",
            None,
            ["issue-34-owner-gap-rule"],
        )
    return (
        "preserve-in-place",
        _default_owner(relative),
        None,
        None,
        ["issue-34-preserve-first"],
    )


def _default_owner(relative: str) -> str:
    for prefix, owner in (
        ("docs/research/", "docs/research/README.md"),
        ("docs/synthesis/", "docs/synthesis/README.md"),
        ("docs/validation/", "docs/validation/README.md"),
        ("skills/custom/", "skills/custom"),
        ("skills/experimental/", "skills/experimental"),
        ("skills/extra/", "skills/extra"),
        ("skills/.archive/", "skills/.archive"),
        (".archive/docs/", ".archive/docs"),
        ("docs/agents/", "AGENTS.md"),
        ("docs/adr/", "docs/adr"),
        ("docs/plans/", "docs/plans/README.md"),
    ):
        if relative.startswith(prefix):
            return owner
    return relative


def _current_authority(relative: str) -> bool:
    return (
        relative in {"AGENTS.md", "CONTEXT.md", "README.md", ".gitignore"}
        or relative.startswith(("docs/agents/", "docs/adr/", "docs/plans/"))
        or relative
        in {
            "docs/research/README.md",
            "docs/research/skill-pack-composition/README.md",
            "docs/research/skill-pack-composition/cards/README.md",
            "docs/research/skill-pack-composition/catalog.json",
            "docs/synthesis/README.md",
            "docs/synthesis/skill-context-relationships.md",
            "docs/validation/README.md",
            "docs/validation/shared/README.md",
        }
        or relative.startswith("docs/validation/shared/schemas/")
        or relative.startswith("docs/validation/shared/fixtures/")
        or relative.startswith("docs/synthesis/methods/")
        or relative
        in {
            "scripts/campaign_artifacts.py",
            "scripts/install_skills.py",
            "scripts/skill_pack_contract.py",
            "scripts/validate_skills.py",
        }
    )


def _observation_fingerprint(
    observations: list[dict[str, object]],
) -> str:
    content = json.dumps(
        observations,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return exact_content_fingerprint(content)


def _resolved_markdown_targets(
    referrer: str,
    content: str,
) -> set[str]:
    targets: set[str] = set()
    parent = PurePosixPath(referrer).parent.as_posix()
    for match in MARKDOWN_LINK_RE.finditer(content):
        raw_target = match.group("target").strip()
        if raw_target.startswith("<") and ">" in raw_target:
            raw_target = raw_target[1 : raw_target.index(">")]
        else:
            raw_target = re.split(r"\s+[\"']", raw_target, maxsplit=1)[0]
        raw_target = raw_target.split("#", 1)[0].split("?", 1)[0]
        if (
            not raw_target
            or raw_target.startswith(("/", "#"))
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_target)
        ):
            continue
        resolved = posixpath.normpath(posixpath.join(parent, raw_target))
        if resolved != ".." and not resolved.startswith("../"):
            targets.add(PurePosixPath(resolved).as_posix())
    return targets


def _container_identities(
    root: Path,
    public_paths: list[str],
) -> dict[str, str]:
    identities: dict[str, str] = {}
    for relative in public_paths:
        if (
            relative.startswith("docs/validation/campaigns/")
            and PurePosixPath(relative).name == "manifest.json"
        ):
            identity = _artifact_identity(root / PurePosixPath(relative))
            if identity is not None:
                identities[PurePosixPath(relative).parent.as_posix()] = identity
    return identities


def _container_identity(
    relative: str,
    identities: dict[str, str],
) -> str | None:
    path = PurePosixPath(relative)
    for parent in (path.parent, *path.parents):
        identity = identities.get(parent.as_posix())
        if identity is not None:
            return identity
    return None


def build_migration_control(
    root: Path,
    *,
    public_paths: list[str],
    private_paths: list[str],
    reference_paths: list[str],
    head: str,
    public_states: dict[str, str] | None = None,
    private_states: dict[str, str] | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    """Build deterministic public control and private ignored sidecar payloads."""

    public_states = public_states or {}
    private_states = private_states or {}
    reference_text: dict[str, str] = {}
    reference_targets: dict[str, set[str]] = {}
    for relative in sorted(set(reference_paths)):
        try:
            reference_text[relative] = (root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        reference_targets[relative] = _resolved_markdown_targets(
            relative,
            reference_text[relative],
        )
    container_identities = _container_identities(root, public_paths)

    public_observations: list[dict[str, object]] = []
    private_observations: list[dict[str, object]] = []
    public_rows: list[dict[str, object]] = []
    private_rows: list[dict[str, object]] = []
    next_id = 1
    for visibility, paths, states, observations, rows in (
        (
            "public",
            public_paths,
            public_states,
            public_observations,
            public_rows,
        ),
        (
            "private",
            private_paths,
            private_states,
            private_observations,
            private_rows,
        ),
    ):
        for relative in sorted(set(paths)):
            state = states.get(
                relative,
                "tracked" if visibility == "public" else "private-ignored",
            )
            path = root / PurePosixPath(relative)
            fingerprint = _path_fingerprint(path)
            identity = (
                _artifact_identity(path) or _container_identity(
                    relative,
                    container_identities,
                )
                if fingerprint is not None
                else None
            )
            inbound_references = (
                sorted(
                    reference
                    for reference, content in reference_text.items()
                    if reference != relative
                    and (
                        relative in content
                        or relative in reference_targets.get(reference, set())
                    )
                )
                if visibility == "public"
                else []
            )
            observation = {
                "key": relative,
                "state": state,
                "fingerprint": fingerprint,
                "identity": identity,
                "inbound_references": inbound_references,
            }
            observations.append(observation)
            disposition, owner, owner_gap, target_path, basis = _migration_plan(
                relative,
                state=state,
            )
            changing = disposition in {
                "move",
                "extract-and-preserve",
                "merge-index",
                "supersede",
                "archive",
                "remove",
            }
            status = "inventoried" if fingerprint is not None else "blocked"
            row: dict[str, object] = {
                "migration_id": f"MIG-{next_id:04d}",
                "source": {
                    "key": relative,
                    "state": state,
                    "fingerprint": fingerprint,
                    "identity": identity,
                },
                "artifact_class": _artifact_class(relative, state),
                "inbound_references": inbound_references,
                "owner": owner,
                "owner_gap": owner_gap,
                "migration_disposition": disposition,
                "epoch_disposition": (
                    "exact-reusable"
                    if visibility == "public" and _current_authority(relative)
                    else (
                        "unverifiable"
                        if visibility == "private"
                        else "historical-admission-only"
                    )
                ),
                "catalog_query_disposition": "unverified-gap",
                "proof_reuse_disposition": "missing",
                "target": {"semantic_id": None, "path": target_path},
                "basis": basis,
                "reference_rewrite_set": (
                    inbound_references if changing else []
                ),
                "required_proof": (
                    [
                        "target-read-back",
                        "reference-reconciliation",
                        "owner-routing",
                        "validator-proof",
                        "old-path-disposition",
                    ]
                    if changing
                    else ["fixed-point-identity"]
                ),
                "observed_result": None,
                "status": status,
                "residual_risk": (
                    "source access or hashing failed"
                    if fingerprint is None
                    else (
                        "future migration proof and semantic identity remain pending"
                        if changing
                        else "epoch admission and proof reuse remain unassessed"
                    )
                ),
                "recovery": {
                    "pointer": (
                        f"git:{head}:{relative}@{fingerprint}"
                        if state == "tracked"
                        else relative
                    ),
                    "applicable_lock": (
                        "FCE-pack-lock"
                        if changing and state != "local-residue"
                        else (
                            "authorized-cleanup-lock"
                            if state == "local-residue"
                            else None
                        )
                    ),
                },
            }
            rows.append(row)
            next_id += 1

    public_inventory_fingerprint = _observation_fingerprint(public_observations)
    private_inventory_fingerprint = _observation_fingerprint(private_observations)
    private: dict[str, object] = {
        "format": 1,
        "fixed_point": {
            "source_head": head,
            "private_inventory_fingerprint": private_inventory_fingerprint,
        },
        "rows": private_rows,
    }
    private_bytes = (
        json.dumps(private, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    public: dict[str, object] = {
        "format": 1,
        "fixed_point": {
            "source_head": head,
            "public_inventory_fingerprint": public_inventory_fingerprint,
            "private_inventory_fingerprint": private_inventory_fingerprint,
        },
        "private_sidecar": {
            "path": ".tmp/fresh-composition-epoch/migration-ledger-private.json",
            "fingerprint": exact_content_fingerprint(private_bytes),
        },
        "rows": public_rows,
    }
    observed: dict[str, object] = {
        "current_head": head,
        "public_inventory_fingerprint": public_inventory_fingerprint,
        "private_inventory_fingerprint": private_inventory_fingerprint,
        "public_source_keys": sorted(set(public_paths)),
        "private_source_keys": sorted(set(private_paths)),
    }
    return public, private, observed


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
