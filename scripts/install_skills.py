"""Transactionally install the custom skill pack without touching unrelated skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pathlib import Path

from scripts.skill_pack_contract import (
    MANIFEST_FORMAT,
    MANIFEST_NAME,
    MANIFEST_SOURCE,
    SHA256_RE,
    SKILL_NAME_RE,
    file_hash,
    lexical_path,
    manifest_bytes,
    parse_managed_manifest_payload,
    payload_hash,
    reject_unsafe_redirect,
    tree_hash,
)

if os.name == "nt":
    import msvcrt
else:
    import fcntl


BOOTSTRAP_HEADING = "## Skill Pack Bootstrap"
LEGACY_BOOTSTRAP_HEADING = "## Skill Pack Guide"
LEGACY_BOUNDARY_HEADING = "## Boundary"
TRANSACTION_PREFIX = ".programming-agent-skills-transaction-"
ACTIVE_TRANSACTION_NAME = f"{TRANSACTION_PREFIX}active"
PREPARING_TRANSACTION_NAME = ".programming-agent-skills-preparing-transaction"
INSTALL_LOCK_NAME = ".programming-agent-skills-install.lock"
OPERATION_CLAIM_NAME = ".programming-agent-skills-operation-claim.json"
TRANSACTION_PLAN_KEYS = (
    "format",
    "skills_dir",
    "global_agents",
    "mutated_skills",
    "skills_dir_existed",
    "manifest_existed",
    "global_agents_existed",
    "previous_hashes",
    "planned_hashes",
    "manifest_sha256",
    "manifest_target_sha256",
    "global_agents_sha256",
    "global_agents_target_sha256",
)
TRANSACTION_STATUSES = frozenset(
    {
        "preparing",
        "prepared",
        "applying",
        "rollback-incomplete",
        "recovery-incomplete",
        "committed",
        "rolled-back",
    }
)


@dataclass(frozen=True)
class InstallPlan:
    skills_dir: Path
    global_agents: Path | None
    mutated_names: tuple[str, ...]
    skills_dir_existed: bool
    manifest_existed: bool
    global_agents_existed: bool
    previous_hashes: dict[str, str]
    planned_hashes: dict[str, str | None]
    manifest_sha256: str | None
    manifest_target_sha256: str
    global_agents_sha256: str | None
    global_agents_target_sha256: str | None

    @property
    def manifest_path(self) -> Path:
        return self.skills_dir / MANIFEST_NAME

    def to_state(self, status: str = "preparing") -> dict[str, object]:
        return {
            "format": 1,
            "status": status,
            "skills_dir": str(self.skills_dir),
            "global_agents": str(self.global_agents) if self.global_agents else None,
            "mutated_skills": list(self.mutated_names),
            "skills_dir_existed": self.skills_dir_existed,
            "manifest_existed": self.manifest_existed,
            "global_agents_existed": self.global_agents_existed,
            "previous_hashes": dict(self.previous_hashes),
            "planned_hashes": dict(self.planned_hashes),
            "manifest_sha256": self.manifest_sha256,
            "manifest_target_sha256": self.manifest_target_sha256,
            "global_agents_sha256": self.global_agents_sha256,
            "global_agents_target_sha256": self.global_agents_target_sha256,
            "rollback_errors": [],
        }

    @classmethod
    def from_state(cls, payload: object, state_path: Path) -> "InstallPlan":
        if not isinstance(payload, dict) or payload.get("format") != 1:
            raise ValueError(f"Transaction state must use format 1: {state_path}")

        skills_value = payload.get("skills_dir")
        mutated_names = payload.get("mutated_skills")
        skills_dir_existed = payload.get("skills_dir_existed")
        manifest_existed = payload.get("manifest_existed")
        global_existed = payload.get("global_agents_existed")
        global_value = payload.get("global_agents")
        status = payload.get("status")
        if not isinstance(skills_value, str) or not skills_value:
            raise ValueError(f"Transaction state has no skills_dir: {state_path}")
        if (
            not isinstance(mutated_names, list)
            or not all(
                isinstance(name, str) and SKILL_NAME_RE.fullmatch(name)
                for name in mutated_names
            )
            or len(mutated_names) != len(set(mutated_names))
        ):
            raise ValueError(f"Transaction state has unsafe mutated_skills: {state_path}")
        if not all(
            isinstance(value, bool)
            for value in (skills_dir_existed, manifest_existed, global_existed)
        ):
            raise ValueError(f"Transaction state has invalid existence flags: {state_path}")
        if global_value is not None and not isinstance(global_value, str):
            raise ValueError(f"Transaction state has invalid global_agents: {state_path}")
        if global_existed and global_value is None:
            raise ValueError(
                "Transaction state records a global snapshot without global_agents: "
                f"{state_path}"
            )
        if status not in TRANSACTION_STATUSES:
            raise ValueError(f"Transaction state has invalid status: {state_path}")

        previous_hashes = payload.get("previous_hashes")
        planned_hashes = payload.get("planned_hashes")
        manifest_sha256 = payload.get("manifest_sha256")
        manifest_target_sha256 = payload.get("manifest_target_sha256")
        global_sha256 = payload.get("global_agents_sha256")
        global_target_sha256 = payload.get("global_agents_target_sha256")
        if not isinstance(previous_hashes, dict) or not all(
            isinstance(name, str)
            and name in mutated_names
            and SKILL_NAME_RE.fullmatch(name)
            and isinstance(value, str)
            and SHA256_RE.fullmatch(value)
            for name, value in previous_hashes.items()
        ):
            raise ValueError(f"Transaction state has invalid previous_hashes: {state_path}")
        if (
            not isinstance(planned_hashes, dict)
            or set(planned_hashes) != set(mutated_names)
            or not all(
                isinstance(name, str)
                and SKILL_NAME_RE.fullmatch(name)
                and (
                    value is None
                    or (isinstance(value, str) and SHA256_RE.fullmatch(value))
                )
                for name, value in planned_hashes.items()
            )
        ):
            raise ValueError(f"Transaction state has invalid planned_hashes: {state_path}")
        if (
            manifest_existed
            and not (
                isinstance(manifest_sha256, str)
                and SHA256_RE.fullmatch(manifest_sha256)
            )
        ) or (not manifest_existed and manifest_sha256 is not None):
            raise ValueError(f"Transaction state has invalid manifest_sha256: {state_path}")
        if not (
            isinstance(manifest_target_sha256, str)
            and SHA256_RE.fullmatch(manifest_target_sha256)
        ):
            raise ValueError(
                f"Transaction state has invalid manifest_target_sha256: {state_path}"
            )
        if (
            global_existed
            and not (
                isinstance(global_sha256, str) and SHA256_RE.fullmatch(global_sha256)
            )
        ) or (not global_existed and global_sha256 is not None):
            raise ValueError(
                f"Transaction state has invalid global_agents_sha256: {state_path}"
            )
        if global_value is None:
            if global_target_sha256 is not None:
                raise ValueError(
                    f"Transaction state has unexpected global target hash: {state_path}"
                )
        elif not (
            isinstance(global_target_sha256, str)
            and SHA256_RE.fullmatch(global_target_sha256)
        ):
            raise ValueError(
                "Transaction state has invalid global_agents_target_sha256: "
                f"{state_path}"
            )

        return cls(
            skills_dir=lexical_path(Path(skills_value)),
            global_agents=lexical_path(Path(global_value)) if global_value else None,
            mutated_names=tuple(mutated_names),
            skills_dir_existed=skills_dir_existed,
            manifest_existed=manifest_existed,
            global_agents_existed=global_existed,
            previous_hashes=dict(previous_hashes),
            planned_hashes=dict(planned_hashes),
            manifest_sha256=manifest_sha256,
            manifest_target_sha256=manifest_target_sha256,
            global_agents_sha256=global_sha256,
            global_agents_target_sha256=global_target_sha256,
        )


@dataclass(frozen=True)
class TransactionPaths:
    root: Path

    @property
    def staged(self) -> Path:
        return self.root / "staged"

    @property
    def backups(self) -> Path:
        return self.root / "previous-skills"

    @property
    def displaced(self) -> Path:
        return self.root / "displaced-skills"

    @property
    def manifest_snapshot(self) -> Path:
        return self.root / "previous-manifest.json"

    @property
    def global_snapshot(self) -> Path:
        return self.root / "previous-global-agents.md"

    @property
    def rollback(self) -> Path:
        return self.root / "rollback-live"


@dataclass(frozen=True)
class FileRollbackTarget:
    label: str
    live: Path
    incoming: Path
    snapshot: Path | None
    prior: str | None
    planned: str
    live_quarantine: Path
    incoming_quarantine: Path
    cleanup_quarantines: bool = False


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def active_skill_dirs(root: Path) -> list[Path]:
    paths = sorted(path for path in (root / MANIFEST_SOURCE).iterdir() if path.is_dir())
    for path in paths:
        if not SKILL_NAME_RE.fullmatch(path.name):
            raise ValueError(f"Source pack has unsafe skill name: {path.name!r}")
    return paths


def transaction_plan(payload: dict[str, object]) -> dict[str, object]:
    return {key: payload.get(key) for key in TRANSACTION_PLAN_KEYS}


def transaction_plan_hash(payload: dict[str, object]) -> str:
    return payload_hash(transaction_plan(payload))


def read_managed_manifest(skills_dir: Path) -> tuple[set[str], dict[str, str]]:
    manifest = skills_dir / MANIFEST_NAME
    if not manifest.is_file():
        return set(), {}
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid installed manifest: {manifest}: {error}") from error
    names, hashes, failures = parse_managed_manifest_payload(payload)
    if failures:
        raise ValueError(f"Invalid installed manifest: {manifest}: {'; '.join(failures)}")
    return names, hashes


def managed_skill_path(skills_dir: Path, name: str) -> Path:
    if not SKILL_NAME_RE.fullmatch(name):
        raise ValueError(f"Unsafe managed skill name: {name!r}")
    root = lexical_path(skills_dir)
    path = skills_dir / name
    if lexical_path(path).parent != root:
        raise ValueError(f"Managed skill path escapes the skills directory: {path}")
    return path


def is_coordination_name(name: str) -> bool:
    exact = {
        INSTALL_LOCK_NAME,
        OPERATION_CLAIM_NAME,
        f".{OPERATION_CLAIM_NAME}.installing",
        ACTIVE_TRANSACTION_NAME,
        PREPARING_TRANSACTION_NAME,
    }
    return name in exact or name.startswith(TRANSACTION_PREFIX)


def validate_target_topology(
    skills_dir: Path,
    global_agents: Path | None,
) -> None:
    reject_unsafe_redirect(skills_dir, "managed skills target")
    skills_dir = lexical_path(skills_dir)
    if any(is_coordination_name(part) for part in skills_dir.parts):
        raise ValueError(
            f"Invalid installer target topology for skills directory: {skills_dir}"
        )
    if global_agents is None:
        return
    reject_unsafe_redirect(global_agents, "global AGENTS target")
    global_agents = lexical_path(global_agents)
    if (
        global_agents == skills_dir
        or skills_dir in global_agents.parents
        or global_agents in skills_dir.parents
    ):
        raise ValueError(
            "Invalid installer target topology: global AGENTS and the managed "
            f"skills tree must not overlap: {global_agents}, {skills_dir}"
        )
    if any(is_coordination_name(part) for part in global_agents.parts):
        raise ValueError(
            "Invalid installer target topology: global AGENTS collides with a "
            f"reserved coordination path: {global_agents}"
        )


@contextmanager
def install_lock(parent: Path):
    reject_unsafe_redirect(parent, "installer lock parent")
    parent = lexical_path(parent)
    parent.mkdir(parents=True, exist_ok=True)
    lock_path = parent / INSTALL_LOCK_NAME
    reject_unsafe_redirect(lock_path, "installer lock")
    handle = lock_path.open("a+b")
    handle.seek(0, os.SEEK_END)
    if handle.tell() == 0:
        handle.write(b"\0")
        handle.flush()
    handle.seek(0)
    try:
        try:
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise RuntimeError(
                "Another install or recovery process owns the skill-pack lock: "
                f"{lock_path}"
            ) from error
        yield
    finally:
        try:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        handle.close()


def operation_lock_parents(
    skills_dir: Path,
    global_agents: Path | None,
) -> list[Path]:
    parents = [lexical_path(skills_dir).parent]
    if global_agents is not None:
        parents.append(lexical_path(global_agents).parent)
    unique = {os.path.normcase(str(parent)): parent for parent in parents}
    return [unique[key] for key in sorted(unique)]


@contextmanager
def install_locks(parents: list[Path]):
    normalized = {
        os.path.normcase(str(lexical_path(parent))): lexical_path(parent)
        for parent in parents
    }
    with ExitStack() as stack:
        for key in sorted(normalized):
            stack.enter_context(install_lock(normalized[key]))
        yield


def operation_claim_path(parent: Path) -> Path:
    return lexical_path(parent) / OPERATION_CLAIM_NAME


def read_operation_claim(path: Path) -> dict[str, object]:
    reject_unsafe_redirect(path, "skill-pack operation claim")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(
            f"Invalid skill-pack operation claim: {path}: {error}"
        ) from error
    if not isinstance(payload, dict) or payload.get("format") != 1:
        raise ValueError(f"Skill-pack operation claim must use format 1: {path}")
    transaction_value = payload.get("transaction")
    plan_sha256 = payload.get("plan_sha256")
    mutation_started = payload.get("mutation_started")
    if not isinstance(transaction_value, str) or not transaction_value:
        raise ValueError(f"Skill-pack operation claim has no transaction: {path}")
    if not isinstance(plan_sha256, str) or not SHA256_RE.fullmatch(plan_sha256):
        raise ValueError(f"Skill-pack operation claim has invalid plan_sha256: {path}")
    if not isinstance(mutation_started, bool):
        raise ValueError(
            f"Skill-pack operation claim has invalid mutation_started: {path}"
        )
    return payload


def write_operation_claim(path: Path, payload: dict[str, object]) -> None:
    reject_unsafe_redirect(path, "skill-pack operation claim")
    temporary = path.with_name(f".{path.name}.installing")
    reject_unsafe_redirect(temporary, "temporary skill-pack operation claim")
    if temporary.exists():
        raise RuntimeError(
            f"Refusing to overwrite temporary operation-claim path: {temporary}"
        )
    with temporary.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def reject_unfinished_operation_claims(parents: list[Path]) -> None:
    for parent in parents:
        claim_path = operation_claim_path(parent)
        if not claim_path.is_file():
            if claim_path.exists():
                raise ValueError(f"Skill-pack operation claim is not a file: {claim_path}")
            continue
        claim = read_operation_claim(claim_path)
        transaction = lexical_path(Path(str(claim["transaction"])))
        if not transaction.is_dir():
            raise RuntimeError(
                "Orphaned skill-pack operation claim found; preserve it and "
                f"repair or inspect the missing transaction before installing: {claim_path}"
            )
        raise RuntimeError(
            "Unfinished skill-pack transaction found. Restore the previous pack "
            "with `python -m scripts.install_skills --recover-transaction "
            f"{transaction}` before installing: {claim_path}"
        )


def write_operation_claims(
    parents: list[Path],
    transaction: Path,
    state: dict[str, object],
) -> None:
    payload = {
        "format": 1,
        "transaction": str(transaction),
        "plan_sha256": transaction_plan_hash(state),
        "mutation_started": False,
    }
    for parent in parents:
        claim_path = operation_claim_path(parent)
        if claim_path.exists():
            raise RuntimeError(f"Skill-pack operation claim already exists: {claim_path}")
        write_operation_claim(claim_path, payload)


def mark_operation_claims_mutation_started(
    parents: list[Path],
    transaction: Path,
    state: dict[str, object],
) -> None:
    expected_plan_hash = transaction_plan_hash(state)
    for parent in parents:
        claim_path = operation_claim_path(parent)
        claim = read_operation_claim(claim_path)
        recorded_transaction = lexical_path(Path(str(claim["transaction"])))
        if (
            recorded_transaction != transaction
            or claim["plan_sha256"] != expected_plan_hash
        ):
            raise RuntimeError(
                "Cannot mark mutation start because the operation claim does not "
                f"match the active transaction: {claim_path}"
            )
        claim["mutation_started"] = True
        write_operation_claim(claim_path, claim)


def verify_operation_claims(
    parents: list[Path],
    transaction: Path,
    state: dict[str, object],
    *,
    required: bool,
) -> bool:
    expected_plan_hash = transaction_plan_hash(state)
    errors: list[str] = []
    mutation_markers: list[bool] = []
    for parent in parents:
        claim_path = operation_claim_path(parent)
        if not claim_path.is_file():
            if required:
                errors.append(f"missing operation claim: {claim_path}")
            continue
        try:
            claim = read_operation_claim(claim_path)
        except ValueError as error:
            errors.append(str(error))
            continue
        recorded_transaction = lexical_path(Path(str(claim["transaction"])))
        if recorded_transaction != transaction:
            errors.append(f"operation claim targets another transaction: {claim_path}")
        if claim["plan_sha256"] != expected_plan_hash:
            errors.append(f"operation claim transaction plan mismatch: {claim_path}")
        mutation_markers.append(bool(claim["mutation_started"]))
    if errors:
        raise RuntimeError(
            "Skill-pack transaction plan or operation claim is invalid; recovery "
            f"snapshot preserved at {transaction}: {'; '.join(errors)}"
        )
    return any(mutation_markers)


def clear_operation_claims(parents: list[Path], transaction: Path) -> list[str]:
    errors: list[str] = []
    for parent in parents:
        claim_path = operation_claim_path(parent)
        temporary = claim_path.with_name(f".{claim_path.name}.installing")
        if temporary.exists() or temporary.is_symlink():
            try:
                temporary_claim = read_operation_claim(temporary)
                temporary_transaction = lexical_path(
                    Path(str(temporary_claim["transaction"]))
                )
                if temporary_transaction != transaction:
                    errors.append(
                        f"preserve unrelated temporary operation claim: {temporary}"
                    )
                else:
                    temporary.unlink()
            except (OSError, ValueError) as error:
                errors.append(
                    f"preserve invalid temporary operation claim {temporary}: {error}"
                )
        if not claim_path.exists():
            continue
        try:
            claim = read_operation_claim(claim_path)
            recorded_transaction = lexical_path(Path(str(claim["transaction"])))
            if recorded_transaction != transaction:
                errors.append(f"preserve unrelated operation claim: {claim_path}")
                continue
            claim_path.unlink()
        except (OSError, ValueError) as error:
            errors.append(f"remove operation claim {claim_path}: {error}")
    return errors


def clear_claims_then_transaction(
    parents: list[Path], transaction: Path, outcome: str
) -> None:
    claim_errors = clear_operation_claims(parents, transaction)
    if claim_errors:
        raise RuntimeError(
            f"{outcome}, but operation-claim cleanup is incomplete; "
            f"snapshot preserved at {transaction}: {'; '.join(claim_errors)}"
        )
    try:
        shutil.rmtree(transaction)
    except OSError as error:
        raise RuntimeError(
            f"{outcome}, but transaction cleanup failed; snapshot preserved at "
            f"{transaction}: {error}"
        ) from error


def claim_transaction(parent: Path, state: dict[str, object]) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    transaction = parent / ACTIVE_TRANSACTION_NAME
    if transaction.exists():
        raise RuntimeError(
            f"Another installer already owns the install transaction: {transaction}"
        )
    preparing = parent / PREPARING_TRANSACTION_NAME
    if preparing.exists():
        raise RuntimeError(
            f"Unfinished preparing transaction found; refusing to remove it: {preparing}"
        )
    preparing.mkdir()
    try:
        write_transaction_state(preparing, state)
        preparing.rename(transaction)
    except BaseException:
        if preparing.exists():
            remove_path(preparing)
        raise
    return transaction


def replace_tree(source: Path, destination: Path, displaced: Path) -> None:
    temporary = destination.parent / f".{destination.name}.installing"
    for path in (temporary, displaced):
        if path.exists() or path.is_symlink():
            raise RuntimeError(
                f"Refusing to overwrite managed-skill coordination path: {path}"
            )
    shutil.copytree(source, temporary)
    if destination.exists():
        displaced.parent.mkdir(parents=True, exist_ok=True)
        destination.rename(displaced)
    try:
        temporary.rename(destination)
    except Exception:
        if displaced.exists() and not destination.exists():
            displaced.rename(destination)
        raise


def retire_tree(path: Path, displaced: Path) -> None:
    if displaced.exists() or displaced.is_symlink():
        raise RuntimeError(
            f"Refusing to overwrite retired-skill quarantine path: {displaced}"
        )
    displaced.parent.mkdir(parents=True, exist_ok=True)
    path.rename(displaced)


def write_manifest(path: Path, payload: dict[str, object]) -> None:
    temporary = path.parent / f".{path.name}.installing"
    reject_unsafe_redirect(temporary, "manifest temporary path")
    if temporary.exists() or temporary.is_symlink():
        raise RuntimeError(f"Refusing to overwrite manifest temporary path: {temporary}")
    with temporary.open("xb") as handle:
        handle.write(manifest_bytes(payload))
    temporary.replace(path)


def native_text_bytes(text: str) -> bytes:
    return text.replace("\n", os.linesep).encode("utf-8")


def global_agents_temporary_path(target: Path) -> Path:
    return target.with_name(f".{target.name}.programming-agent-skills.installing")


def global_agents_rollback_path(target: Path) -> Path:
    return target.with_name(f".{target.name}.programming-agent-skills.rollback")


def global_agents_temporary_rollback_path(target: Path) -> Path:
    return target.with_name(
        f".{target.name}.programming-agent-skills.rollback-installing"
    )


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def reject_coordination_collision(path: Path, label: str) -> None:
    reject_unsafe_redirect(path, label)
    if path.exists() or path.is_symlink():
        raise RuntimeError(f"Refusing to overwrite existing {label}: {path}")


def restore_file(path: Path, snapshot: Path | None) -> None:
    if path.exists() or path.is_symlink():
        raise OSError(f"Refusing to overwrite live path during rollback: {path}")
    if snapshot is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(snapshot.read_bytes())


def restore_tree(snapshot: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        raise OSError(f"Refusing to overwrite live tree during rollback: {destination}")
    shutil.copytree(snapshot, destination)


def quarantine_tree(
    path: Path,
    quarantine: Path,
    expected_hashes: set[str],
) -> None:
    quarantine.parent.mkdir(parents=True, exist_ok=True)
    reject_unsafe_redirect(path, "rollback tree target")
    reject_unsafe_redirect(quarantine, "rollback tree quarantine")
    if quarantine.exists() or quarantine.is_symlink():
        if not quarantine.is_dir() or tree_hash(quarantine) not in expected_hashes:
            raise OSError(f"Rollback tree quarantine is outside the plan: {quarantine}")
        return
    if not path.exists():
        return
    if not path.is_dir():
        raise OSError(f"Rollback tree target has unsupported type: {path}")
    path.rename(quarantine)
    if tree_hash(quarantine) not in expected_hashes:
        if not path.exists():
            quarantine.rename(path)
        raise OSError(f"Rollback tree target changed outside the plan: {path}")


def quarantine_file(
    path: Path,
    quarantine: Path,
    expected_hashes: set[str],
) -> None:
    quarantine.parent.mkdir(parents=True, exist_ok=True)
    reject_unsafe_redirect(path, "rollback file target")
    reject_unsafe_redirect(quarantine, "rollback file quarantine")
    if quarantine.exists() or quarantine.is_symlink():
        if not quarantine.is_file() or file_hash(quarantine) not in expected_hashes:
            raise OSError(f"Rollback file quarantine is outside the plan: {quarantine}")
        return
    if not path.exists():
        return
    if not path.is_file():
        raise OSError(f"Rollback file target has unsupported type: {path}")
    path.replace(quarantine)
    if file_hash(quarantine) not in expected_hashes:
        if not path.exists():
            quarantine.replace(path)
        raise OSError(f"Rollback file target changed outside the plan: {path}")


def rollback_file(target: FileRollbackTarget) -> list[str]:
    errors: list[str] = []
    slots = (
        (target.incoming, target.incoming_quarantine, {target.planned}),
        (
            target.live,
            target.live_quarantine,
            {value for value in (target.prior, target.planned) if value is not None},
        ),
    )
    for path, quarantine, expected in slots:
        try:
            quarantine_file(path, quarantine, expected)
        except (OSError, ValueError) as error:
            errors.append(f"quarantine {path}: {error}")

    already_restored = False
    if target.live.exists() or target.live.is_symlink():
        try:
            already_restored = (
                target.prior is not None
                and target.live.is_file()
                and file_hash(target.live) == target.prior
                and target.live_quarantine.is_file()
            )
        except (OSError, ValueError):
            already_restored = False
        if not already_restored:
            errors.append(
                f"live {target.label} appeared during rollback quarantine: {target.live}"
            )

    if not errors and not already_restored:
        try:
            restore_file(target.live, target.snapshot)
        except OSError as error:
            errors.append(f"restore {target.live}: {error}")
    if not errors:
        try:
            if target.prior is None:
                if target.live.exists():
                    errors.append(f"verify absent {target.live}: path still exists")
            elif not target.live.is_file() or file_hash(target.live) != target.prior:
                errors.append(f"verify restored {target.live}: content mismatch")
        except OSError as error:
            errors.append(f"verify restored {target.live}: {error}")

    if not errors and target.cleanup_quarantines:
        for _, quarantine, _ in slots:
            try:
                remove_path(quarantine)
            except OSError as error:
                errors.append(f"remove rollback quarantine {quarantine}: {error}")
    return errors


def write_transaction_state(transaction: Path, payload: dict[str, object]) -> None:
    state = transaction / "transaction-state.json"
    temporary = transaction / ".transaction-state.json.installing"
    reject_unsafe_redirect(temporary, "temporary transaction state")
    if temporary.exists() or temporary.is_symlink():
        raise RuntimeError(
            f"Refusing to overwrite temporary transaction state: {temporary}"
        )
    with temporary.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(state)


def reconcile_transaction_state_temporary(transaction: Path) -> None:
    state_path = transaction / "transaction-state.json"
    temporary = transaction / ".transaction-state.json.installing"
    reject_unsafe_redirect(state_path, "transaction state")
    reject_unsafe_redirect(temporary, "temporary transaction state")
    if not temporary.exists():
        return
    if not state_path.is_file() or not temporary.is_file():
        raise RuntimeError(
            f"Cannot reconcile incomplete transaction state in {transaction}"
        )
    try:
        current = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Invalid committed transaction state in {transaction}: {error}"
        ) from error
    try:
        pending = json.loads(temporary.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        temporary.unlink()
        return
    except OSError as error:
        raise RuntimeError(
            f"Cannot read incomplete transaction state in {transaction}: {error}"
        ) from error
    if (
        not isinstance(current, dict)
        or not isinstance(pending, dict)
        or current.get("format") != 1
        or pending.get("format") != 1
        or transaction_plan_hash(current) != transaction_plan_hash(pending)
    ):
        raise RuntimeError(
            f"Incomplete transaction state does not match the immutable plan: {temporary}"
        )
    current_status = current.get("status")
    pending_status = pending.get("status")
    allowed = {
        "preparing": {"preparing", "prepared"},
        "prepared": {
            "prepared",
            "applying",
            "rolled-back",
            "recovery-incomplete",
        },
        "applying": {
            "applying",
            "committed",
            "rolled-back",
            "rollback-incomplete",
            "recovery-incomplete",
        },
        "rollback-incomplete": {
            "rollback-incomplete",
            "recovery-incomplete",
            "rolled-back",
        },
        "recovery-incomplete": {"recovery-incomplete", "rolled-back"},
        "committed": {"committed"},
        "rolled-back": {"rolled-back"},
    }
    if pending_status not in allowed.get(str(current_status), set()):
        raise RuntimeError(
            f"Incomplete transaction state has an invalid phase transition: {temporary}"
        )
    temporary.replace(state_path)


def clear_safe_preparing_transaction(
    preparing: Path,
    skills_dir: Path,
    global_agents: Path | None,
) -> None:
    if not preparing.exists():
        return
    reject_unsafe_redirect(preparing, "preparing transaction")
    if not preparing.is_dir():
        raise RuntimeError(f"Preparing transaction is not a directory: {preparing}")
    entries = {path.name for path in preparing.iterdir()}
    if not entries:
        preparing.rmdir()
        return
    candidates = [
        preparing / "transaction-state.json",
        preparing / ".transaction-state.json.installing",
    ]
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1 or entries != {existing[0].name}:
        raise RuntimeError(
            f"Cannot prove preparing transaction is safe to clear: {preparing}"
        )
    try:
        payload = json.loads(existing[0].read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        shutil.rmtree(preparing)
        return
    except OSError as error:
        raise RuntimeError(
            f"Invalid preparing transaction state: {existing[0]}: {error}"
        ) from error
    if (
        not isinstance(payload, dict)
        or payload.get("format") != 1
        or payload.get("status") != "preparing"
        or lexical_path(Path(str(payload.get("skills_dir", "")))) != skills_dir
        or (
            lexical_path(Path(str(payload["global_agents"])))
            if payload.get("global_agents")
            else None
        )
        != global_agents
    ):
        raise RuntimeError(
            f"Preparing transaction does not match the requested targets: {preparing}"
        )
    shutil.rmtree(preparing)


def preparing_transaction_state(
    skills_dir: Path,
    global_agents: Path | None,
    mutated_names: list[str],
    skills_dir_existed: bool,
    *,
    manifest_existed: bool = False,
    global_agents_existed: bool = False,
    previous_hashes: dict[str, str] | None = None,
    planned_hashes: dict[str, str | None] | None = None,
    manifest_sha256: str | None = None,
    manifest_target_sha256: str | None = None,
    global_agents_sha256: str | None = None,
    global_agents_target_sha256: str | None = None,
) -> dict[str, object]:
    return {
        "format": 1,
        "status": "preparing",
        "skills_dir": str(skills_dir),
        "global_agents": str(global_agents) if global_agents else None,
        "mutated_skills": mutated_names,
        "skills_dir_existed": skills_dir_existed,
        "manifest_existed": manifest_existed,
        "global_agents_existed": global_agents_existed,
        "previous_hashes": previous_hashes or {},
        "planned_hashes": planned_hashes or {},
        "manifest_sha256": manifest_sha256,
        "manifest_target_sha256": manifest_target_sha256,
        "global_agents_sha256": global_agents_sha256,
        "global_agents_target_sha256": global_agents_target_sha256,
        "rollback_errors": [],
    }


def snapshot_integrity_errors(
    plan: InstallPlan,
    paths: TransactionPaths,
) -> list[str]:
    backup_dir = paths.backups
    previous_hashes = plan.previous_hashes
    errors: list[str] = []
    try:
        actual_backups = (
            {path.name for path in backup_dir.iterdir()} if backup_dir.is_dir() else set()
        )
    except OSError as error:
        errors.append(f"read previous-skill snapshots: {error}")
        actual_backups = set()
    expected_backups = set(previous_hashes)
    if actual_backups != expected_backups:
        errors.append(
            "previous-skill snapshot set differs: "
            f"expected {sorted(expected_backups)}, actual {sorted(actual_backups)}"
        )
    for name, expected_hash in previous_hashes.items():
        snapshot = backup_dir / name
        try:
            if not snapshot.is_dir() or tree_hash(snapshot) != expected_hash:
                errors.append(f"previous-skill snapshot hash mismatch: {name}")
        except OSError as error:
            errors.append(f"read previous-skill snapshot {name}: {error}")

    for label, path, expected_hash in (
        ("manifest", paths.manifest_snapshot, plan.manifest_sha256),
        ("global AGENTS", paths.global_snapshot, plan.global_agents_sha256),
    ):
        try:
            if expected_hash is None:
                if path.exists():
                    errors.append(f"unexpected {label} snapshot: {path}")
            elif not path.is_file() or file_hash(path) != expected_hash:
                errors.append(f"{label} snapshot hash mismatch: {path}")
        except OSError as error:
            errors.append(f"read {label} snapshot {path}: {error}")
    return errors


def live_target_identity_errors(
    plan: InstallPlan,
    paths: TransactionPaths | None = None,
    *,
    mode: str = "either",
) -> list[str]:
    """Refuse rollback over live content not owned by the immutable plan."""
    skills_dir = plan.skills_dir
    previous_hashes = plan.previous_hashes
    planned_hashes = plan.planned_hashes
    rollback_root = paths.rollback if paths is not None else None
    errors: list[str] = []

    def allowed(previous: str | None, planned: str | None) -> set[str | None]:
        if mode == "previous":
            return {previous}
        if mode == "planned":
            return {planned}
        return {previous, planned}

    for name in plan.mutated_names:
        destination = managed_skill_path(skills_dir, name)
        previous = previous_hashes.get(name)
        planned = planned_hashes[name]
        try:
            reject_unsafe_redirect(destination, f"managed skill {name}")
            if destination.is_dir():
                actual: str | None = tree_hash(destination)
            elif destination.exists():
                errors.append(f"managed skill has unsupported live type: {name}")
                continue
            else:
                actual = None
            permitted = allowed(previous, planned)
            rollback_live = (
                rollback_root / f"{name}-live" if rollback_root is not None else None
            )
            if rollback_live is not None and rollback_live.exists():
                reject_unsafe_redirect(
                    rollback_live, f"rollback live tree for {name}"
                )
                if (
                    not rollback_live.is_dir()
                    or tree_hash(rollback_live)
                    not in {value for value in (previous, planned) if value is not None}
                ):
                    errors.append(
                        f"rollback live tree is outside the plan: {name}"
                    )
                elif actual is None:
                    permitted.add(None)
            if (
                mode == "either"
                and actual is None
                and previous is not None
                and planned is not None
                and rollback_root is not None
            ):
                displaced = rollback_root.parent / "displaced-skills" / name
                incoming = skills_dir / f".{name}.installing"
                reject_unsafe_redirect(
                    displaced, f"managed-skill displaced tree for {name}"
                )
                reject_unsafe_redirect(
                    incoming, f"managed-skill incoming tree for {name}"
                )
                if (
                    displaced.is_dir()
                    and incoming.is_dir()
                    and tree_hash(displaced) == previous
                    and tree_hash(incoming) == planned
                ):
                    permitted.add(None)
            if actual not in permitted:
                errors.append(f"managed skill live state is outside the plan: {name}")
        except (OSError, ValueError) as error:
            errors.append(f"inspect managed skill {name}: {error}")
        for label, coordination, expected in (
            ("incoming", skills_dir / f".{name}.installing", planned),
        ):
            try:
                reject_unsafe_redirect(
                    coordination, f"managed-skill {label} tree for {name}"
                )
                if coordination.is_dir():
                    if expected is None or tree_hash(coordination) != expected:
                        errors.append(
                            f"managed-skill {label} tree is outside the plan: {name}"
                        )
                elif coordination.exists():
                    errors.append(
                        f"managed-skill {label} path has unsupported type: {name}"
                    )
            except (OSError, ValueError) as error:
                errors.append(
                    f"inspect managed-skill {label} tree {name}: {error}"
                )
        if rollback_root is not None:
            applied_displaced = rollback_root.parent / "displaced-skills" / name
            try:
                reject_unsafe_redirect(
                    applied_displaced, f"applied displaced tree for {name}"
                )
                if applied_displaced.exists() and (
                    not applied_displaced.is_dir()
                    or previous is None
                    or tree_hash(applied_displaced) != previous
                ):
                    errors.append(
                        f"applied displaced tree is outside the plan: {name}"
                    )
            except (OSError, ValueError) as error:
                errors.append(f"inspect applied displaced tree {name}: {error}")
            for label, expected in (("incoming", planned),):
                quarantine = rollback_root / f"{name}-{label}"
                try:
                    reject_unsafe_redirect(
                        quarantine, f"rollback {label} tree for {name}"
                    )
                    if quarantine.exists() and (
                        not quarantine.is_dir()
                        or expected is None
                        or tree_hash(quarantine) != expected
                    ):
                        errors.append(
                            f"rollback {label} tree is outside the plan: {name}"
                        )
                except (OSError, ValueError) as error:
                    errors.append(
                        f"inspect rollback {label} tree {name}: {error}"
                    )

    for label, path, previous, planned in (
        (
            "manifest",
            plan.manifest_path,
            plan.manifest_sha256,
            plan.manifest_target_sha256,
        ),
        (
            "global AGENTS",
            plan.global_agents,
            plan.global_agents_sha256,
            plan.global_agents_target_sha256,
        ),
    ):
        if path is None:
            continue
        try:
            reject_unsafe_redirect(path, label)
            if path.is_file():
                actual = file_hash(path)
            elif path.exists():
                errors.append(f"{label} has unsupported live type: {path}")
                continue
            else:
                actual = None
            permitted = allowed(previous, planned)
            if rollback_root is not None and label == "manifest":
                rollback_live = rollback_root / "manifest-live"
                reject_unsafe_redirect(rollback_live, "rollback manifest quarantine")
                if rollback_live.exists():
                    if (
                        not rollback_live.is_file()
                        or file_hash(rollback_live)
                        not in {
                            value
                            for value in (previous, planned)
                            if value is not None
                        }
                    ):
                        errors.append(
                            f"rollback manifest quarantine is outside the plan: {rollback_live}"
                        )
                    elif actual is None:
                        permitted.add(None)
            if label == "global AGENTS":
                rollback_live = global_agents_rollback_path(path)
                reject_unsafe_redirect(
                    rollback_live, "global AGENTS rollback quarantine"
                )
                if rollback_live.exists() and (
                    rollback_live.is_file()
                    and file_hash(rollback_live)
                    in {
                        value
                        for value in (previous, planned)
                        if value is not None
                    }
                ) and actual is None:
                    permitted.add(None)
            if actual not in permitted:
                errors.append(f"{label} live state is outside the plan: {path}")
        except (OSError, ValueError) as error:
            errors.append(f"inspect {label} live state {path}: {error}")
        if label == "global AGENTS":
            temporary = global_agents_temporary_path(path)
            try:
                reject_unsafe_redirect(temporary, "global AGENTS temporary path")
                if temporary.is_file() and (
                    planned is None or file_hash(temporary) != planned
                ):
                    errors.append(
                        f"global AGENTS temporary state is outside the plan: {temporary}"
                    )
                elif temporary.exists() and not temporary.is_file():
                    errors.append(
                        f"global AGENTS temporary path has unsupported type: {temporary}"
                    )
            except (OSError, ValueError) as error:
                errors.append(f"inspect global AGENTS temporary path {temporary}: {error}")
            rollback_live = global_agents_rollback_path(path)
            rollback_temporary = global_agents_temporary_rollback_path(path)
            for quarantine, expected in (
                (
                    rollback_live,
                    {value for value in (previous, planned) if value is not None},
                ),
                (
                    rollback_temporary,
                    {planned} if planned is not None else set(),
                ),
            ):
                try:
                    reject_unsafe_redirect(quarantine, "global AGENTS rollback path")
                    if quarantine.exists() and (
                        not quarantine.is_file()
                        or file_hash(quarantine) not in expected
                    ):
                        errors.append(
                            f"global AGENTS rollback path is outside the plan: {quarantine}"
                        )
                except (OSError, ValueError) as error:
                    errors.append(
                        f"inspect global AGENTS rollback path {quarantine}: {error}"
                    )
        elif label == "manifest":
            temporary = path.parent / f".{path.name}.installing"
            try:
                reject_unsafe_redirect(temporary, "manifest temporary path")
                if temporary.is_file() and file_hash(temporary) != planned:
                    errors.append(
                        f"manifest temporary state is outside the plan: {temporary}"
                    )
                elif temporary.exists() and not temporary.is_file():
                    errors.append(
                        f"manifest temporary path has unsupported type: {temporary}"
                    )
            except (OSError, ValueError) as error:
                errors.append(f"inspect manifest temporary path {temporary}: {error}")
    return errors


def recover_transaction(
    transaction: Path,
    expected_skills_dir: Path,
    expected_global_agents: Path | None,
) -> dict[str, object]:
    reject_unsafe_redirect(transaction, "transaction snapshot")
    reject_unsafe_redirect(expected_skills_dir, "managed skills recovery target")
    if expected_global_agents is not None:
        reject_unsafe_redirect(expected_global_agents, "global AGENTS recovery target")
    transaction = lexical_path(transaction)
    if not transaction.is_dir() or transaction.name != ACTIVE_TRANSACTION_NAME:
        raise ValueError(f"Not a skill-pack transaction snapshot: {transaction}")
    expected_skills_dir = lexical_path(expected_skills_dir)
    expected_global_agents = (
        lexical_path(expected_global_agents)
        if expected_global_agents is not None
        else None
    )
    validate_target_topology(expected_skills_dir, expected_global_agents)
    state_path = transaction / "transaction-state.json"
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid transaction state: {state_path}: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"Transaction state must be an object: {state_path}")
    skills_value = payload.get("skills_dir")
    if not isinstance(skills_value, str) or not skills_value:
        raise ValueError(f"Transaction state has no skills_dir: {state_path}")
    skills_dir = lexical_path(Path(skills_value))
    if skills_dir.parent != transaction.parent:
        raise ValueError(
            "Transaction snapshot is not beside its recorded skills directory: "
            f"{transaction} -> {skills_dir}"
        )
    global_value = payload.get("global_agents")
    if global_value is not None and not isinstance(global_value, str):
        raise ValueError(f"Transaction state has invalid global_agents: {state_path}")
    global_agents = (
        lexical_path(Path(global_value)) if global_value else None
    )
    if skills_dir != expected_skills_dir or global_agents != expected_global_agents:
        raise ValueError(
            "Transaction targets do not match requested recovery targets: "
            f"state=({skills_dir}, {global_agents}), "
            f"requested=({expected_skills_dir}, {expected_global_agents})"
        )
    locked_parents = operation_lock_parents(skills_dir, global_agents)
    with install_locks(locked_parents):
        return _recover_transaction_locked(
            transaction,
            locked_parents,
            expected_skills_dir,
            expected_global_agents,
        )


def _recover_transaction_locked(
    transaction: Path,
    locked_parents: list[Path],
    expected_skills_dir: Path,
    expected_global_agents: Path | None,
) -> dict[str, object]:

    reconcile_transaction_state_temporary(transaction)
    state_path = transaction / "transaction-state.json"
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid transaction state: {state_path}: {error}") from error
    plan = InstallPlan.from_state(payload, state_path)
    status = payload["status"]
    if plan.skills_dir.parent != transaction.parent:
        raise ValueError(
            "Transaction snapshot is not beside its recorded skills directory: "
            f"{transaction} -> {plan.skills_dir}"
        )
    if (
        plan.skills_dir != expected_skills_dir
        or plan.global_agents != expected_global_agents
    ):
        raise ValueError(
            "Transaction targets do not match requested recovery targets: "
            f"state=({plan.skills_dir}, {plan.global_agents}), "
            f"requested=({expected_skills_dir}, {expected_global_agents})"
        )
    if operation_lock_parents(plan.skills_dir, plan.global_agents) != locked_parents:
        raise RuntimeError(
            "Transaction targets changed while recovery locks were acquired; "
            f"snapshot preserved at {transaction}"
        )
    claimed_mutation_started = verify_operation_claims(
        locked_parents,
        transaction,
        payload,
        required=status not in {"preparing", "committed", "rolled-back"},
    )
    if status == "preparing" and claimed_mutation_started:
        raise RuntimeError(
            "Transaction mutation phase does not match its operation claims; "
            f"recovery snapshot preserved at {transaction}"
        )
    if status in {"preparing", "prepared"} and not claimed_mutation_started:
        clear_claims_then_transaction(
            locked_parents,
            transaction,
            "Pre-mutation transaction is safe to clear",
        )
        return {"status": "cleared-preparation", "skills_dir": plan.skills_dir}
    if status in {"applying", "rollback-incomplete", "recovery-incomplete"} and not claimed_mutation_started:
        raise RuntimeError(
            "Transaction mutation phase does not match its operation claims; "
            f"recovery snapshot preserved at {transaction}"
        )

    paths = TransactionPaths(transaction)

    integrity_errors = snapshot_integrity_errors(plan, paths)
    if integrity_errors:
        raise RuntimeError(
            "Transaction snapshot hash mismatch; recovery snapshot preserved at "
            f"{transaction}: {'; '.join(integrity_errors)}"
        )

    live_mode = (
        "planned"
        if status == "committed"
        else "previous" if status == "rolled-back" else "either"
    )
    live_errors = live_target_identity_errors(plan, paths, mode=live_mode)
    if live_errors:
        raise RuntimeError(
            "Live install targets changed outside the claimed transaction plan; "
            f"recovery snapshot preserved at {transaction}: {'; '.join(live_errors)}"
        )
    if status in {"committed", "rolled-back"}:
        clear_claims_then_transaction(
            locked_parents,
            transaction,
            "Terminal transaction state was verified",
        )
        return {
            "status": "cleared-commit" if status == "committed" else "restored",
            "skills_dir": plan.skills_dir,
        }

    errors = rollback_install(plan=plan, paths=paths)
    if errors:
        payload["status"] = "recovery-incomplete"
        payload["recovery_errors"] = errors
        write_transaction_state(transaction, payload)
        raise RuntimeError(
            "Skill-pack recovery is incomplete; snapshot preserved at "
            f"{transaction}: {'; '.join(errors)}"
        )

    payload["status"] = "rolled-back"
    payload["recovery_errors"] = []
    write_transaction_state(transaction, payload)
    clear_claims_then_transaction(
        locked_parents,
        transaction,
        "Previous pack was restored and verified",
    )
    return {"status": "restored", "skills_dir": plan.skills_dir}


def rollback_install(
    plan: InstallPlan,
    paths: TransactionPaths,
) -> list[str]:
    skills_dir = plan.skills_dir
    backup_dir = paths.backups
    previous_hashes = plan.previous_hashes
    planned_hashes = plan.planned_hashes
    errors: list[str] = []
    rollback_root = paths.rollback

    for name in plan.mutated_names:
        destination = managed_skill_path(skills_dir, name)
        previous = previous_hashes.get(name)
        planned = planned_hashes[name]
        slots = (
            (
                skills_dir / f".{name}.installing",
                rollback_root / f"{name}-incoming",
                {planned} if planned is not None else set(),
            ),
            (
                destination,
                rollback_root / f"{name}-live",
                {value for value in (previous, planned) if value is not None},
            ),
        )
        item_errors: list[str] = []
        for path, quarantine, expected in slots:
            try:
                quarantine_tree(path, quarantine, expected)
            except (OSError, ValueError) as error:
                item_errors.append(f"quarantine {path}: {error}")
        already_restored = False
        if destination.exists() or destination.is_symlink():
            try:
                already_restored = (
                    previous is not None
                    and destination.is_dir()
                    and tree_hash(destination) == previous
                    and (rollback_root / f"{name}-live").is_dir()
                )
            except (OSError, ValueError):
                already_restored = False
            if not already_restored:
                item_errors.append(
                    f"live tree appeared during rollback quarantine: {destination}"
                )
        backup = backup_dir / name
        if not item_errors and not already_restored and backup.is_dir():
            try:
                restore_tree(backup, destination)
            except OSError as error:
                item_errors.append(f"restore {destination}: {error}")
        if not item_errors:
            try:
                if previous is None:
                    if destination.exists():
                        item_errors.append(
                            f"verify absent {destination}: path still exists"
                        )
                elif not destination.is_dir() or tree_hash(destination) != previous:
                    item_errors.append(
                        f"verify restored {destination}: tree hash mismatch"
                    )
            except OSError as error:
                item_errors.append(f"verify restored {destination}: {error}")
        errors.extend(item_errors)

    manifest_path = plan.manifest_path
    errors.extend(
        rollback_file(
            FileRollbackTarget(
                label="manifest",
                live=manifest_path,
                incoming=manifest_path.parent / f".{manifest_path.name}.installing",
                snapshot=paths.manifest_snapshot if plan.manifest_existed else None,
                prior=plan.manifest_sha256,
                planned=plan.manifest_target_sha256,
                live_quarantine=rollback_root / "manifest-live",
                incoming_quarantine=rollback_root / "manifest-incoming",
            )
        )
    )

    if plan.global_agents is not None:
        global_target_sha256 = plan.global_agents_target_sha256
        if global_target_sha256 is None:
            errors.append("global AGENTS target hash is missing from the install plan")
        else:
            errors.extend(
                rollback_file(
                    FileRollbackTarget(
                        label="global AGENTS",
                        live=plan.global_agents,
                        incoming=global_agents_temporary_path(plan.global_agents),
                        snapshot=(
                            paths.global_snapshot if plan.global_agents_existed else None
                        ),
                        prior=plan.global_agents_sha256,
                        planned=global_target_sha256,
                        live_quarantine=global_agents_rollback_path(plan.global_agents),
                        incoming_quarantine=global_agents_temporary_rollback_path(
                            plan.global_agents
                        ),
                        cleanup_quarantines=True,
                    )
                )
            )

    if not plan.skills_dir_existed and skills_dir.is_dir():
        try:
            if not any(skills_dir.iterdir()):
                skills_dir.rmdir()
        except OSError as error:
            errors.append(f"remove new skills directory {skills_dir}: {error}")

    return errors


def bootstrap_section(template: Path) -> str:
    text = template.read_text(encoding="utf-8")
    start = text.find(BOOTSTRAP_HEADING)
    if start < 0:
        raise ValueError(f"Template is missing {BOOTSTRAP_HEADING}: {template}")
    return text[start:].strip() + "\n"


def render_global_bootstrap(template: Path, target: Path) -> tuple[str, str]:
    section = bootstrap_section(template)
    if not target.exists():
        return "created", "# Global Codex Instructions\n\n" + section

    text = target.read_text(encoding="utf-8")
    start = text.find(BOOTSTRAP_HEADING)
    if start >= 0:
        next_heading = re.search(
            r"(?m)^##\s+", text[start + len(BOOTSTRAP_HEADING) :]
        )
        end = len(text)
        if next_heading is not None:
            end = start + len(BOOTSTRAP_HEADING) + next_heading.start()
        updated = text[:start].rstrip() + "\n\n" + section
        if end < len(text):
            updated += "\n" + text[end:].lstrip()
        return ("present" if updated == text else "updated"), updated

    legacy_start = text.find(LEGACY_BOOTSTRAP_HEADING)
    if legacy_start >= 0:
        if text.find(LEGACY_BOUNDARY_HEADING, legacy_start) < 0:
            raise ValueError(
                f"Legacy skill-pack block has no {LEGACY_BOUNDARY_HEADING}: {target}"
            )
        boundary_start = text.find(LEGACY_BOUNDARY_HEADING, legacy_start)
        after_boundary = boundary_start + len(LEGACY_BOUNDARY_HEADING)
        next_heading = re.search(r"(?m)^##\s+", text[after_boundary:])
        legacy_end = len(text)
        if next_heading is not None:
            legacy_end = after_boundary + next_heading.start()
        updated = text[:legacy_start].rstrip() + "\n\n" + section
        if legacy_end < len(text):
            updated += "\n" + text[legacy_end:].lstrip()
        return "migrated", updated
    return "merged", text.rstrip() + "\n\n" + section


def preview_global_bootstrap(template: Path, target: Path) -> str:
    status, _ = render_global_bootstrap(template, target)
    return status


def install_global_bootstrap(template: Path, target: Path) -> str:
    status, updated = render_global_bootstrap(template, target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if status != "present":
        temporary = global_agents_temporary_path(target)
        reject_unsafe_redirect(temporary, "global AGENTS temporary path")
        if temporary.exists() or temporary.is_symlink():
            raise RuntimeError(
                f"Refusing to overwrite global AGENTS temporary path: {temporary}"
            )
        with temporary.open("xb") as handle:
            handle.write(native_text_bytes(updated))
        temporary.replace(target)
    return status


def install(
    root: Path,
    skills_dir: Path,
    global_agents: Path | None,
    *,
    dry_run: bool = False,
) -> dict[str, object]:
    reject_unsafe_redirect(root, "skill-pack source root")
    reject_unsafe_redirect(skills_dir, "managed skills target")
    if global_agents is not None:
        reject_unsafe_redirect(global_agents, "global AGENTS target")
    root = root.expanduser().resolve()
    skills_dir = lexical_path(skills_dir)
    global_agents = (
        lexical_path(global_agents) if global_agents is not None else None
    )
    validate_target_topology(skills_dir, global_agents)
    if dry_run:
        return _install_locked(root, skills_dir, global_agents, dry_run=True)
    with install_locks(operation_lock_parents(skills_dir, global_agents)):
        return _install_locked(
            root,
            skills_dir,
            global_agents,
            dry_run=dry_run,
        )


def _install_locked(
    root: Path,
    skills_dir: Path,
    global_agents: Path | None,
    *,
    dry_run: bool = False,
) -> dict[str, object]:
    validate_target_topology(skills_dir, global_agents)
    sources = active_skill_dirs(root)
    transaction_parent = skills_dir.parent
    operation_parents = operation_lock_parents(skills_dir, global_agents)
    for parent in operation_parents:
        reject_unsafe_redirect(
            operation_claim_path(parent), "skill-pack operation claim"
        )
        reject_unsafe_redirect(
            operation_claim_path(parent).with_name(
                f".{OPERATION_CLAIM_NAME}.installing"
            ),
            "temporary skill-pack operation claim",
        )
    if not dry_run:
        reject_unfinished_operation_claims(operation_parents)
        clear_safe_preparing_transaction(
            transaction_parent / PREPARING_TRANSACTION_NAME,
            skills_dir,
            global_agents,
        )
    stale_transactions = sorted(transaction_parent.glob(f"{TRANSACTION_PREFIX}*"))
    if stale_transactions:
        paths = ", ".join(str(path) for path in stale_transactions)
        raise RuntimeError(
            "Unfinished skill-pack transaction found. Restore the previous pack "
            "with `python -m scripts.install_skills --recover-transaction "
            f"<snapshot-path>` before installing: {paths}"
        )

    active_names = {path.name for path in sources}
    source_hashes = {source.name: tree_hash(source) for source in sources}
    previous_names, recorded_hashes = read_managed_manifest(skills_dir)
    retired_names = sorted(previous_names - active_names)

    new_names: list[str] = []
    updated_names: list[str] = []
    unchanged_names: list[str] = []
    for source in sources:
        destination = managed_skill_path(skills_dir, source.name)
        if destination.exists() and not destination.is_dir():
            raise ValueError(f"Managed skill path is not a directory: {destination}")
        if not destination.is_dir():
            new_names.append(source.name)
        else:
            installed_hash = tree_hash(destination)
            if source.name in previous_names:
                if installed_hash != recorded_hashes[source.name]:
                    raise ValueError(
                        f"Refusing to overwrite modified managed skill: {source.name}"
                    )
            else:
                raise ValueError(
                    "Refusing to take over an unmanaged skill path without explicit "
                    f"adoption: {source.name}"
                )
            if source_hashes[source.name] == installed_hash:
                unchanged_names.append(source.name)
            else:
                updated_names.append(source.name)

    for name in retired_names:
        destination = managed_skill_path(skills_dir, name)
        if destination.exists() and not destination.is_dir():
            raise ValueError(f"Managed skill path is not a directory: {destination}")
        if destination.is_dir() and tree_hash(destination) != recorded_hashes[name]:
            raise ValueError(f"Refusing to retire modified managed skill: {name}")

    bootstrap_status = "skipped"
    global_target_text: str | None = None
    if global_agents is not None:
        bootstrap_status, global_target_text = render_global_bootstrap(
            root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
            global_agents,
        )

    if dry_run:
        return {
            "skills": sorted(active_names),
            "new": new_names,
            "updated": updated_names,
            "unchanged": unchanged_names,
            "retired": retired_names,
            "global_bootstrap": bootstrap_status,
        }

    manifest = {
        "format": MANIFEST_FORMAT,
        "source": MANIFEST_SOURCE,
        "skills": sorted(active_names),
        "hashes": source_hashes,
    }

    changed_names = sorted(set(new_names + updated_names))
    mutated_names = sorted(set(changed_names + retired_names))
    for name in mutated_names:
        destination = managed_skill_path(skills_dir, name)
        if destination.exists() and not destination.is_dir():
            raise ValueError(f"Managed skill path is not a directory: {destination}")

    skills_dir_existed = skills_dir.is_dir()
    manifest_path = skills_dir / MANIFEST_NAME
    reject_unsafe_redirect(manifest_path, "installed manifest")
    if manifest_path.exists() and not manifest_path.is_file():
        raise ValueError(f"Installed manifest is not a file: {manifest_path}")
    manifest_existed = manifest_path.is_file()
    manifest_sha256 = file_hash(manifest_path) if manifest_existed else None
    if (
        global_agents is not None
        and global_agents.exists()
        and not global_agents.is_file()
    ):
        raise ValueError(f"Global AGENTS target is not a file: {global_agents}")
    global_agents_existed = global_agents is not None and global_agents.is_file()
    global_sha256 = file_hash(global_agents) if global_agents_existed else None
    previous_hashes = {
        name: tree_hash(managed_skill_path(skills_dir, name))
        for name in mutated_names
        if managed_skill_path(skills_dir, name).is_dir()
    }
    planned_hashes: dict[str, str | None] = {
        name: source_hashes.get(name) for name in mutated_names
    }
    manifest_target_sha256 = hashlib.sha256(manifest_bytes(manifest)).hexdigest()
    global_target_sha256 = (
        hashlib.sha256(native_text_bytes(global_target_text)).hexdigest()
        if global_target_text is not None
        else None
    )
    manifest_is_planned = (
        manifest_existed and file_hash(manifest_path) == manifest_target_sha256
    )
    global_is_planned = (
        global_agents is None
        or (
            global_agents.is_file()
            and global_target_sha256 is not None
            and file_hash(global_agents) == global_target_sha256
        )
    )
    if not mutated_names and manifest_is_planned and global_is_planned:
        return {
            "skills": sorted(active_names),
            "new": new_names,
            "updated": updated_names,
            "unchanged": unchanged_names,
            "retired": retired_names,
            "global_bootstrap": bootstrap_status,
        }
    for name in mutated_names:
        reject_coordination_collision(
            skills_dir / f".{name}.installing",
            f"managed-skill temporary path for {name}",
        )
    reject_coordination_collision(
        skills_dir / f".{MANIFEST_NAME}.installing",
        "manifest temporary path",
    )
    if global_agents is not None:
        for path, label in (
            (global_agents_temporary_path(global_agents), "global AGENTS temporary path"),
            (global_agents_rollback_path(global_agents), "global AGENTS rollback path"),
            (
                global_agents_temporary_rollback_path(global_agents),
                "global AGENTS temporary rollback path",
            ),
        ):
            reject_coordination_collision(path, label)
    for parent in operation_parents:
        temporary_claim = operation_claim_path(parent).with_name(
            f".{OPERATION_CLAIM_NAME}.installing"
        )
        reject_coordination_collision(
            temporary_claim,
            "temporary skill-pack operation claim",
        )
    plan = InstallPlan(
        skills_dir=skills_dir,
        global_agents=global_agents,
        mutated_names=tuple(mutated_names),
        skills_dir_existed=skills_dir_existed,
        manifest_existed=manifest_existed,
        global_agents_existed=global_agents_existed,
        previous_hashes=previous_hashes,
        planned_hashes=planned_hashes,
        manifest_sha256=manifest_sha256,
        manifest_target_sha256=manifest_target_sha256,
        global_agents_sha256=global_sha256,
        global_agents_target_sha256=global_target_sha256,
    )
    transaction_state = plan.to_state()
    transaction = claim_transaction(transaction_parent, transaction_state)
    paths = TransactionPaths(transaction)
    mutation_started = False

    try:
        write_operation_claims(operation_parents, transaction, transaction_state)
        paths.staged.mkdir()
        paths.backups.mkdir()
        paths.displaced.mkdir()
        for source in sources:
            staged = paths.staged / source.name
            shutil.copytree(source, staged)
            if tree_hash(staged) != source_hashes[source.name]:
                raise RuntimeError(f"Staged skill failed hash verification: {source.name}")

        for name in mutated_names:
            destination = managed_skill_path(skills_dir, name)
            if destination.is_dir():
                backup = paths.backups / name
                shutil.copytree(destination, backup)
                if tree_hash(backup) != previous_hashes[name]:
                    raise RuntimeError(
                        f"Previous skill snapshot failed hash verification: {name}"
                    )

        if manifest_existed:
            shutil.copy2(manifest_path, paths.manifest_snapshot)
            if file_hash(paths.manifest_snapshot) != manifest_sha256:
                raise RuntimeError("Previous manifest snapshot failed hash verification")

        if global_agents_existed and global_agents is not None:
            shutil.copy2(global_agents, paths.global_snapshot)
            if file_hash(paths.global_snapshot) != global_sha256:
                raise RuntimeError(
                    "Previous global AGENTS snapshot failed hash verification"
                )

        transaction_state["status"] = "prepared"
        write_transaction_state(transaction, transaction_state)

        mark_operation_claims_mutation_started(
            operation_parents,
            transaction,
            transaction_state,
        )
        transaction_state["status"] = "applying"
        write_transaction_state(transaction, transaction_state)
        mutation_started = True
        skills_dir.mkdir(parents=True, exist_ok=True)
        for name in changed_names:
            destination = managed_skill_path(skills_dir, name)
            replace_tree(paths.staged / name, destination, paths.displaced / name)
            if tree_hash(destination) != source_hashes[name]:
                raise RuntimeError(f"Installed skill failed hash verification: {name}")

        for name in retired_names:
            retired = managed_skill_path(skills_dir, name)
            if retired.is_dir():
                retire_tree(retired, paths.displaced / name)

        write_manifest(manifest_path, manifest)

        if global_agents is not None:
            bootstrap_status = install_global_bootstrap(
                root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
                global_agents,
            )

        try:
            committed_names, committed_hashes = read_managed_manifest(skills_dir)
        except ValueError as error:
            raise RuntimeError(
                "Committed manifest failed post-install verification"
            ) from error
        if committed_names != active_names or committed_hashes != source_hashes:
            raise RuntimeError("Committed manifest failed post-install verification")

        for source in sources:
            destination = managed_skill_path(skills_dir, source.name)
            if (
                not destination.is_dir()
                or tree_hash(destination) != source_hashes[source.name]
            ):
                raise RuntimeError(
                    f"Committed skill failed hash verification: {source.name}"
                )
        for name in retired_names:
            if managed_skill_path(skills_dir, name).exists():
                raise RuntimeError(f"Retired managed skill still exists: {name}")
        if global_agents is not None and preview_global_bootstrap(
            root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
            global_agents,
        ) != "present":
            raise RuntimeError("Global bootstrap failed post-install verification")
        if (
            global_agents is not None
            and file_hash(global_agents) != global_target_sha256
        ):
            raise RuntimeError(
                "Global bootstrap content changed from the claimed install plan"
            )
        transaction_state["status"] = "committed"
        write_transaction_state(transaction, transaction_state)
    except Exception as error:
        rollback_errors: list[str] = []
        rollback_completed = False
        if mutation_started:
            rollback_errors = snapshot_integrity_errors(plan, paths)
            if not rollback_errors:
                rollback_errors = live_target_identity_errors(plan, paths)
            if not rollback_errors:
                rollback_errors = rollback_install(plan=plan, paths=paths)
            rollback_completed = not rollback_errors
            if rollback_completed and transaction.is_dir():
                transaction_state["status"] = "rolled-back"
                transaction_state["failure"] = str(error)
                transaction_state["rollback_errors"] = []
                try:
                    write_transaction_state(transaction, transaction_state)
                except OSError as state_error:
                    rollback_errors.append(
                        f"record verified rollback state: {state_error}"
                    )
        if not rollback_errors:
            try:
                clear_claims_then_transaction(
                    operation_parents,
                    transaction,
                    (
                        "Skill-pack install restored and verified pre-install state"
                        if mutation_started
                        else "Skill-pack install failed before mutation"
                    ),
                )
            except RuntimeError as cleanup_error:
                rollback_errors.append(str(cleanup_error))
        if rollback_errors:
            if mutation_started and not rollback_completed and transaction.is_dir():
                transaction_state["status"] = "rollback-incomplete"
                transaction_state["failure"] = str(error)
                transaction_state["rollback_errors"] = rollback_errors
                try:
                    write_transaction_state(transaction, transaction_state)
                except OSError as state_error:
                    rollback_errors.append(
                        f"record incomplete rollback state: {state_error}"
                    )
            detail = "; ".join(rollback_errors)
            if not mutation_started:
                raise RuntimeError(
                    "Skill-pack install failed before mutation and transaction "
                    "cleanup is incomplete; safe pre-mutation state preserved at "
                    f"{transaction}: {detail}"
                ) from error
            raise RuntimeError(
                "Skill-pack install failed and rollback is incomplete; recovery "
                f"snapshot preserved at {transaction}: {detail}"
            ) from error
        raise

    clear_claims_then_transaction(
        operation_parents,
        transaction,
        "Skill-pack install committed and verified",
    )

    return {
        "skills": sorted(active_names),
        "new": new_names,
        "updated": updated_names,
        "unchanged": unchanged_names,
        "retired": retired_names,
        "global_bootstrap": bootstrap_status,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path.home() / ".agents/skills",
        help="Shared Codex skills directory.",
    )
    parser.add_argument(
        "--global-agents",
        type=Path,
        default=Path.home() / ".codex/AGENTS.md",
        help="Global AGENTS.md that receives the minimal bootstrap section.",
    )
    parser.add_argument("--skip-global-agents", action="store_true")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true")
    action.add_argument(
        "--recover-transaction",
        type=Path,
        metavar="SNAPSHOT_PATH",
        help="Restore and verify the previous managed pack from a transaction snapshot.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.recover_transaction is not None:
        global_agents = None if args.skip_global_agents else args.global_agents.expanduser()
        try:
            result = recover_transaction(
                args.recover_transaction,
                args.skills_dir.expanduser(),
                global_agents,
            )
        except (OSError, ValueError, RuntimeError) as error:
            print(f"Recovery failed: {error}", file=sys.stderr)
            return 1
        if result["status"] == "cleared-preparation":
            print(
                "Cleared a verified pre-mutation transaction in "
                f"{result['skills_dir']}. Rerun the installer to apply current source."
            )
        elif result["status"] == "cleared-commit":
            print(
                "Verified the committed managed pack and finished transaction cleanup in "
                f"{result['skills_dir']}."
            )
        else:
            print(
                "Restored the previous managed pack in "
                f"{result['skills_dir']}. Rerun the installer to apply current source."
            )
        return 0

    root = repo_root()
    global_agents = None if args.skip_global_agents else args.global_agents.expanduser()
    try:
        result = install(
            root,
            args.skills_dir.expanduser(),
            global_agents,
            dry_run=args.dry_run,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"Managed skills: {len(result['skills'])} in {args.skills_dir.expanduser()}")
        if result["new"]:
            print(f"New skills: {', '.join(result['new'])}")
        if result["updated"]:
            print(f"Updated skills: {', '.join(result['updated'])}")
        print(f"Unchanged skills: {len(result['unchanged'])}")
    else:
        print(f"Installed {len(result['skills'])} custom skills into {args.skills_dir.expanduser()}")
    if result["retired"]:
        print(f"Retired managed skills: {', '.join(result['retired'])}")
    print(f"Global bootstrap: {result['global_bootstrap']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
