"""Record, validate, derive, and render a parallel-implement campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
RUNTIME_CONTRACT = 6
REVIEW_AGENT_IDS = {
    "change-review": "ordinary-reviewer",
    "high-assurance-review": "assurance-coordinator",
}
ASSURANCE_CORE_AGENT_IDS = {
    "har-spec-reviewer",
    "har-standards-reviewer",
}
ASSURANCE_REVIEWER_IDS = {
    *ASSURANCE_CORE_AGENT_IDS,
    "har-specialist",
}
PROVIDER_BINDING_FIELDS = (
    "lane_id",
    "agent_id",
    "runtime_agent_type",
    "task_id",
    "requested_model",
    "requested_effort",
    "environment",
)


def load_runtime_profiles() -> dict[str, tuple[str, str, str]]:
    source = Path(__file__).resolve().parents[1] / "references/RUNTIME-PROFILES.md"
    profiles = {}
    for line in source.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(
            r"\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|",
            line,
        )
        if match:
            profile, agent_type, model, effort = match.groups()
            profiles[profile] = (agent_type, model, effort)
    required = {
        "parallel-root",
        "clear-worker",
        "adaptive-worker",
        "fast-adaptive-worker",
        "demanding-worker",
        "serial-integrator",
        *REVIEW_AGENT_IDS.values(),
        *ASSURANCE_REVIEWER_IDS,
    }
    if set(profiles) != required:
        raise ValueError("runtime profiles are incomplete")
    return profiles


_RUNTIME_PROFILES: dict[str, tuple[str, str, str]] | None = None


def runtime_profiles() -> dict[str, tuple[str, str, str]]:
    global _RUNTIME_PROFILES
    if _RUNTIME_PROFILES is None:
        _RUNTIME_PROFILES = load_runtime_profiles()
    return _RUNTIME_PROFILES


def runtime_profile_matches(
    profile: Any, agent_type: Any, model: Any, effort: Any
) -> bool:
    expected = runtime_profiles().get(profile)
    if expected == (agent_type, model, effort):
        return True
    return (
        profile == "serial-integrator"
        and expected is not None
        and agent_type == expected[0]
        and model == expected[1]
        and effort == "high"
    )


def provider_binding_matches(receipt: Any, binding: dict[str, Any]) -> bool:
    return (
        isinstance(receipt, dict)
        and receipt.get("status") == "accepted"
        and all(receipt.get(field) == binding.get(field) for field in PROVIDER_BINDING_FIELDS)
    )


def canonical_path(value: str) -> str:
    return os.path.normcase(str(Path(value).resolve()))


def commit_identity(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-fA-F]{40,64}", value))


def parsed_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def path_within(child: str, parent: str) -> bool:
    try:
        return os.path.commonpath([canonical_path(child), canonical_path(parent)]) == canonical_path(parent)
    except ValueError:
        return False
EVENT_TYPES = {
    "scope",
    "resume",
    "reconcile",
    "lane-create",
    "lane-preflight",
    "lane-cleanup",
    "dispatch",
    "handoff",
    "accept",
    "reject",
    "land",
    "integration-regression",
    "integration-correction",
    "graph-drained",
    "review-ready",
    "review-invocation",
    "review-decision",
    "repair-plan",
    "repair-complete",
    "closeout-head",
    "child-closeout",
    "parent-closeout",
    "tracker-lock",
    "checkpoint",
    "release",
}
INTENTS = {
    "dispatch",
    "land",
    "correct-integration",
    "review",
    "repair",
    "lock",
    "checkpoint",
    "complete",
}
SAFE_LANE_STATES = {
    "removed",
    "provider-preserved",
    "unregistered-residual-directory",
}
ACCEPTED_REVIEWS = {"pass", "pass with residual risk"}
CLOSEOUT_FIELDS = {
    "delivered",
    "acceptance_evidence",
    "proof",
    "review",
    "reviewed_head",
    "residual_risk",
    "intended_mutation",
    "posted_comment",
    "mutation_readback",
    "claim_release",
    "affected_frontier_readback",
}
WORKER_RETURN_FIELDS = {
    "changed_scope_ids",
    "actual_changed_files",
    "acceptance_proof",
    "test_portfolio_delta",
    "commands_and_results",
    "skipped_checks",
    "risk_or_blocker",
    "next_need",
    "scope_notes",
    "final_status",
}


@contextmanager
def stream_lock(path: Path):
    """Serialize read-validate-append operations across supported platforms."""
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def emit(ok: bool, **data: Any) -> int:
    print(json.dumps({"schema": SCHEMA_VERSION, "ok": ok, **data}, sort_keys=True))
    return 0 if ok else 1


def resolve_profile(args: argparse.Namespace) -> int:
    binding = runtime_profiles().get(args.profile)
    if binding is None:
        return emit(
            False,
            operation="profile",
            code="UNKNOWN_PROFILE",
            profile=args.profile,
        )
    agent_type, model, effort = binding
    spawn = {"agent_type": agent_type}
    if agent_type == "default":
        spawn.update(model=model, reasoning_effort=effort)
    return emit(
        True,
        operation="profile",
        profile=args.profile,
        model=model,
        reasoning=effort,
        spawn=spawn,
    )


def event_path(value: str) -> Path:
    path = Path(value).resolve()
    if path.suffix.lower() != ".jsonl":
        raise ValueError("event stream must use a .jsonl path")
    return path


def run_path(value: str, *, create: bool = False) -> Path:
    path = Path(value).resolve()
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def run_events(value: str, *, create: bool = False) -> Path:
    return run_path(value, create=create) / "events.jsonl"


def run_repo(path: Path) -> str:
    events = load_events(path)
    if not events:
        raise ValueError("run has not been started")
    repo = events[0].get("data", {}).get("repo")
    if not isinstance(repo, str) or not repo:
        raise ValueError("run does not record its repository")
    return repo


def write_derived_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def artifact_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def root_decision_digest(
    action: str,
    subject: str,
    head: str | None,
    data: dict[str, Any],
) -> str:
    decision = {
        "action": action,
        "subject": subject,
        "head": head,
        "data": {key: value for key, value in data.items() if key != "root_receipt"},
    }
    encoded = json.dumps(decision, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def artifact_name(value: str) -> str:
    digest = hashlib.sha256(value.encode()).hexdigest()[:16]
    stem = value if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value) else "item"
    return f"{stem[:48]}-{digest}"


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"blank event at line {number}")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid JSON at line {number}: {error.msg}") from error
        if not isinstance(event, dict):
            raise ValueError(f"event at line {number} is not an object")
        events.append(event)
    return events


def validate_events(events: list[dict[str, Any]]) -> None:
    event_ids: set[str] = set()
    for number, event in enumerate(events, 1):
        if event.get("schema") != SCHEMA_VERSION:
            raise ValueError(f"event {number} has unsupported schema")
        if event.get("event") not in EVENT_TYPES:
            raise ValueError(f"event {number} has unknown type")
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError(f"event {number} has no event_id")
        if event_id in event_ids:
            raise ValueError(f"event {number} duplicates event_id {event_id}")
        event_ids.add(event_id)
        if not isinstance(event.get("timestamp"), str) or not event["timestamp"]:
            raise ValueError(f"event {number} has no timestamp")
        if not isinstance(event.get("work_item"), str) or not event["work_item"]:
            raise ValueError(f"event {number} has no work_item")
        if not isinstance(event.get("data"), dict):
            raise ValueError(f"event {number} data is not an object")


def normalize_event(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("event input must be an object")
    event_type = raw.get("event")
    if event_type not in EVENT_TYPES:
        raise ValueError(f"unknown event type: {event_type}")
    work_item = raw.get("work_item")
    if not isinstance(work_item, str) or not work_item:
        raise ValueError("event input requires work_item")
    data = raw.get("data", {})
    if not isinstance(data, dict):
        raise ValueError("event data must be an object")
    return {
        "schema": SCHEMA_VERSION,
        "event_id": raw.get("event_id") or str(uuid.uuid4()),
        "timestamp": raw.get("timestamp") or datetime.now(UTC).isoformat(),
        "event": event_type,
        "work_item": work_item,
        "worker_sha": raw.get("worker_sha"),
        "integration_sha": raw.get("integration_sha"),
        "validation": raw.get("validation"),
        "decision": raw.get("decision"),
        "risk": raw.get("risk"),
        "data": data,
    }


def append_encoded(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = "".join(
        json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
        for event in events
    ).encode()
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        written = 0
        while written < len(encoded):
            count = os.write(descriptor, encoded[written:])
            if count <= 0:
                raise OSError("event stream write made no progress")
            written += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def semantic_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return the retry identity without generated time or stored receipt."""
    return {
        key: value
        for key, value in event.items()
        if key not in {"timestamp", "receipt"}
    }


def stable_event_id(prefix: str, payload: Any, *, index: int = 0) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()[:16]
    return f"{prefix}-{index + 1}-{digest}"


def append_facade_events(
    path: Path,
    raw_events: list[dict[str, Any]],
    *,
    repo: str | None,
) -> tuple[int, int, list[dict[str, Any]], dict[str, Any]]:
    """Append an idempotent semantic batch and keep the reducer authoritative."""
    with stream_lock(path):
        prior = load_events(path)
        validate_events(prior)
        by_id = {event["event_id"]: event for event in prior}
        appended: list[dict[str, Any]] = []
        replayed = 0
        for raw in raw_events:
            event = normalize_event(raw)
            existing = by_id.get(event["event_id"])
            if existing is not None:
                if "timestamp" not in raw:
                    event["timestamp"] = existing["timestamp"]
                if semantic_event(event) != semantic_event(existing):
                    raise ValueError(
                        f"event_id {event['event_id']} already exists with a different payload"
                    )
                replayed += 1
                continue
            appended.append(event)
            by_id[event["event_id"]] = event
        prospective = [*prior, *appended]
        validate_events(prospective)
        state = derive_state(prospective, repo)
        if state["errors"]:
            raise ValueError(
                "prospective packet is semantically invalid: "
                + "; ".join(state["errors"])
            )
        if appended:
            append_encoded(path, appended)
    return len(appended), replayed, prospective, state


def scope_identifiers(value: Any) -> tuple[list[str], str | None]:
    if not isinstance(value, list) or not value:
        return [], "must be a non-empty list"
    identifiers: list[str] = []
    for entry in value:
        if isinstance(entry, str):
            identifier = entry.strip()
        elif isinstance(entry, dict) and isinstance(entry.get("id"), str):
            identifier = entry["id"].strip()
        else:
            return [], "entries must be nonempty strings or objects with a nonempty id"
        if not identifier:
            return [], "entries must be nonempty strings or objects with a nonempty id"
        identifiers.append(identifier)
    if len(identifiers) != len(set(identifiers)):
        return [], "identifiers must be unique"
    return identifiers, None


def git_head(repo: str | None) -> str | None:
    if not repo:
        return None
    result = subprocess.run(
        ["git", "-C", str(Path(repo).resolve()), "rev-parse", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "cannot resolve repository HEAD")
    return result.stdout.strip()


def git_clean(repo: str | None) -> bool | None:
    if not repo:
        return None
    result = subprocess.run(
        ["git", "-C", str(Path(repo).resolve()), "status", "--porcelain=v1"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "cannot inspect repository status")
    return not bool(result.stdout)


def git_is_ancestor(repo: str | None, ancestor: str, descendant: str) -> bool:
    if not repo:
        return True
    result = subprocess.run(
        [
            "git",
            "-C",
            str(Path(repo).resolve()),
            "merge-base",
            "--is-ancestor",
            ancestor,
            descendant,
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode not in {0, 1}:
        raise ValueError(result.stderr.strip() or "cannot verify integration ancestry")
    return result.returncode == 0


def derive_state(events: list[dict[str, Any]], repo: str | None = None) -> dict[str, Any]:
    lane_agent_ids = (
        set(runtime_profiles())
        - set(REVIEW_AGENT_IDS.values())
        - ASSURANCE_REVIEWER_IDS
        - {"parallel-root"}
    )
    errors: list[str] = []
    children: list[str] = []
    parent_id: str | None = None
    parent_claim: dict[str, Any] | None = None
    items: dict[str, dict[str, Any]] = {}
    lanes: dict[str, dict[str, Any]] = {}
    integration_head: str | None = None
    graph_drained = False
    review_ready = False
    review_target: str | None = None
    review_decision: str | None = None
    closeout_head: str | None = None
    child_closeouts: dict[str, dict[str, Any]] = {}
    parent_closeout: dict[str, Any] | None = None
    checkpoint_outcome: str | None = None
    checkpoint_data: dict[str, Any] | None = None
    checkpoint_active = False
    checkpoint_resume_pending = False
    release_outcome: str | None = None
    resume_pending = False
    resume_timestamp: datetime | None = None
    tracker_locked = False
    release_seen = False
    charter_id: str | None = None
    root_actor_id: str | None = None
    caller_id: str | None = None
    residual_risk_policy: dict[str, Any] | None = None
    repair_generation_budget = 2
    repair_generation = 0
    repair_completed_generation = 0
    repair_open = False
    repair_base: str | None = None
    repair_findings: list[str] = []
    review_findings: list[dict[str, Any]] = []
    review_residual_risks: list[dict[str, Any]] = []
    review_route_mismatches = 0
    review_decision_id: str | None = None
    review_invocation_id: str | None = None
    review_mode: str | None = None
    review_route: str | None = None
    review_actor_id: str | None = None
    review_receipt: dict[str, Any] | None = None
    review_actor_ids_used: set[str] = set()
    review_task_ids_used: set[str] = set()
    integration_regression: dict[str, Any] | None = None
    latest_integration_correction: str | None = None
    current_head = git_head(repo)
    current_clean = git_clean(repo)
    last_integration_number = max(
        (
            number
            for number, candidate in enumerate(events, 1)
            if candidate.get("event") in {"land", "integration-correction"}
        ),
        default=0,
    )
    last_review_ready_number = max(
        (
            number
            for number, candidate in enumerate(events, 1)
            if candidate.get("event") == "review-ready"
        ),
        default=0,
    )

    def item_state(item: str) -> dict[str, Any]:
        return items.setdefault(item, {})

    def implementation_actor_ids() -> set[str]:
        return {
            actor
            for actor in [
                root_actor_id,
                *[lane.get("actor_id") for lane in lanes.values()],
            ]
            if isinstance(actor, str) and actor
        }

    def serial_lane_idle(lane: dict[str, Any]) -> bool:
        return (
            lane.get("environment") == "local"
            and lane.get("state") == "landed"
            and lane.get("lane_clean") is True
            and lane.get("task_state") in {"idle", "completed"}
        )

    def need(condition: bool, message: str) -> bool:
        if not condition:
            errors.append(message)
        return condition

    def require_root_receipt(
        data: dict[str, Any],
        *,
        action: str,
        subject: str,
        head: str | None = None,
        prefix: str,
    ) -> bool:
        receipt = data.get("root_receipt")
        expected_digest = root_decision_digest(action, subject, head, data)
        return need(
            isinstance(receipt, dict)
            and receipt.get("actor_id") == root_actor_id
            and receipt.get("action") == action
            and receipt.get("subject") == subject
            and receipt.get("head") == head
            and bool(receipt.get("receipt_id"))
            and receipt.get("decision_sha256") == expected_digest,
            f"{prefix} requires a root-owned {action} receipt",
        )

    def require_resolved_telemetry(
        data: dict[str, Any], prefix: str, *, review: bool = False
    ) -> bool:
        valid = True
        label = "review " if review else ""
        for resolved_field, status_field, requested_field in (
            ("resolved_model", "resolved_model_status", "requested_model"),
            ("resolved_effort", "resolved_effort_status", "requested_effort"),
        ):
            status_value = data.get(status_field)
            valid &= need(
                status_value in {"matched", "unavailable"},
                f"{prefix} has invalid {label}{status_field}",
            )
            if status_value == "matched":
                valid &= need(
                    data.get(resolved_field) == data.get(requested_field),
                    f"{prefix} {label}{resolved_field} differs from request",
                )
            elif status_value == "unavailable":
                valid &= need(
                    bool(data.get("telemetry_unavailable_reason")),
                    f"{prefix} unavailable {label}telemetry requires a reason",
                )
                valid &= need(
                    data.get(resolved_field) in {None, ""},
                    f"{prefix} unavailable {label}telemetry cannot include {resolved_field}",
                )
        return valid

    for number, event in enumerate(events, 1):
        kind = event["event"]
        item = event["work_item"]
        data = event["data"]
        prefix = f"event {number} {kind} for {item}"
        state = item_state(item)

        if release_seen:
            errors.append(f"{prefix} occurs after release")
        if checkpoint_active and kind != "resume":
            errors.append(f"{prefix} occurs before checkpoint resume")
        if checkpoint_resume_pending and kind != "reconcile":
            errors.append(f"{prefix} occurs before checkpoint reconciliation")

        if kind == "scope":
            visible = data.get("children")
            if parent_id is None:
                parent_id = item
            else:
                need(False, f"{prefix} duplicates the immutable campaign scope")
            valid_children = need(
                isinstance(visible, list)
                and bool(visible)
                and all(isinstance(child, str) and child for child in visible)
                and len(visible) == len(set(visible)),
                f"{prefix} requires nonempty unique data.children",
            )
            if valid_children:
                children = list(visible)
            candidate_root_actor_id = data.get("root_actor_id")
            if need(
                isinstance(candidate_root_actor_id, str)
                and bool(candidate_root_actor_id.strip()),
                f"{prefix} requires data.root_actor_id",
            ):
                root_actor_id = candidate_root_actor_id
            candidate_caller_id = data.get("caller_id")
            if need(
                isinstance(candidate_caller_id, str)
                and bool(candidate_caller_id.strip()),
                f"{prefix} requires data.caller_id",
            ):
                caller_id = candidate_caller_id
            charter = data.get("charter")
            if need(isinstance(charter, dict), f"{prefix} requires data.charter"):
                candidate_id = charter.get("id")
                if need(
                    isinstance(candidate_id, str) and bool(candidate_id),
                    f"{prefix} data.charter requires id",
                ):
                    charter_id = candidate_id
                need(
                    charter.get("runtime_contract") == RUNTIME_CONTRACT,
                    f"{prefix} requires runtime contract {RUNTIME_CONTRACT}",
                )

                candidate_policy = charter.get("residual_risk_policy")
                if candidate_policy is not None:
                    if need(
                        isinstance(candidate_policy, dict)
                        and bool(candidate_policy.get("id"))
                        and bool(candidate_policy.get("evidence")),
                        f"{prefix} residual-risk policy requires id and evidence",
                    ):
                        residual_risk_policy = dict(candidate_policy)

                candidate_repair = charter.get(
                    "repair_generation_budget", repair_generation_budget
                )
                if need(
                    isinstance(candidate_repair, int) and candidate_repair >= 0,
                    f"{prefix} Charter repair_generation_budget must be a nonnegative integer",
                ):
                    repair_generation_budget = candidate_repair
            candidate_parent_claim = data.get("parent_claim")
            if need(
                isinstance(candidate_parent_claim, dict)
                and candidate_parent_claim.get("state") == "retained"
                and candidate_parent_claim.get("work_item") == parent_id
                and candidate_parent_claim.get("owner") == root_actor_id
                and bool(candidate_parent_claim.get("token"))
                and bool(candidate_parent_claim.get("readback")),
                f"{prefix} requires the retained parent claim",
            ):
                parent_claim = dict(candidate_parent_claim)
            scope_head = event.get("integration_sha")
            if need(
                commit_identity(scope_head),
                f"{prefix} requires the exact starting HEAD",
            ):
                integration_head = scope_head
        elif kind == "resume":
            if checkpoint_active:
                checkpoint_active = False
                checkpoint_resume_pending = True
            resume_pending = True
            resume_timestamp = parsed_time(event.get("timestamp"))
        elif kind == "reconcile":
            required = {"git", "worktrees", "tasks", "claims", "tracker"}
            missing = sorted(field for field in required if field not in data)
            need(not missing, f"{prefix} missing reconciliation evidence: {', '.join(missing)}")
            empty = sorted(field for field in required if field in data and data.get(field) is None)
            need(not empty, f"{prefix} empty reconciliation evidence: {', '.join(empty)}")
            invalid_tasks = False
            if not missing and not empty:
                container_contracts = {
                    "git": dict,
                    "worktrees": list,
                    "tasks": list,
                    "claims": list,
                    "tracker": dict,
                }
                for field, expected_type in container_contracts.items():
                    value = data.get(field)
                    invalid_tasks |= not need(
                        isinstance(value, expected_type)
                        and (expected_type is list or bool(value)),
                        f"{prefix} {field} evidence must be a valid {expected_type.__name__}",
                    )
                if "remote" in data:
                    invalid_tasks |= not need(
                        isinstance(data.get("remote"), dict) and bool(data["remote"]),
                        f"{prefix} remote evidence must be a nonempty dict",
                    )
                for field in {"git", "tracker", "remote"} & set(data):
                    observation = data.get(field)
                    if isinstance(observation, dict):
                        observed_at = parsed_time(observation.get("observed_at"))
                        invalid_tasks |= not need(
                            observed_at is not None
                            and resume_timestamp is not None
                            and observed_at > resume_timestamp,
                            f"{prefix} {field} evidence is not post-resume",
                        )
                git_observation = data.get("git")
                if isinstance(git_observation, dict):
                    invalid_tasks |= not need(
                        git_observation.get("head") == integration_head
                        and git_observation.get("status") == "clean"
                        and (
                            not repo
                            or (
                                git_observation.get("head") == current_head
                                and current_clean is True
                            )
                        ),
                        f"{prefix} Git evidence must match clean live integration HEAD",
                    )
                active_lanes = {
                    lane_id: lane
                    for lane_id, lane in lanes.items()
                    if lane.get("state") not in SAFE_LANE_STATES
                }
                claim_lanes = {
                    lane_id: lane
                    for lane_id, lane in lanes.items()
                    if lane_id in active_lanes
                    or (
                        item_state(str(lane.get("work_item"))).get("landed")
                        and child_closeouts.get(str(lane.get("work_item")), {}).get("state")
                        != "verified"
                    )
                }
                expected_claims = {
                    lane_id: {
                        "work_item": lane.get("work_item"),
                        "actor_id": lane.get("actor_id"),
                        "owner": lane.get("claim", {}).get("owner"),
                        "token": lane.get("claim", {}).get("token"),
                    }
                    for lane_id, lane in claim_lanes.items()
                }
                if parent_claim and not parent_closeout:
                    expected_claims["parent"] = {
                        "work_item": parent_id,
                        "actor_id": root_actor_id,
                        "owner": parent_claim.get("owner"),
                        "token": parent_claim.get("token"),
                    }
                worktree_observations = data.get("worktrees")
                if isinstance(worktree_observations, list):
                    observed_lane_ids = []
                    for observation in worktree_observations:
                        valid_worktree = need(
                            isinstance(observation, dict),
                            f"{prefix} worktree observation must be an object",
                        )
                        if not isinstance(observation, dict):
                            invalid_tasks = True
                            continue
                        lane_id = observation.get("lane_id")
                        lane = claim_lanes.get(lane_id, {})
                        observed_lane_ids.append(lane_id)
                        observed_at = parsed_time(observation.get("observed_at"))
                        valid_worktree &= need(
                            lane_id in claim_lanes
                            and observation.get("provider") == lane.get("provider")
                            and observation.get("state")
                            in SAFE_LANE_STATES | {"registered"}
                            and isinstance(observation.get("worktree"), str)
                            and canonical_path(observation["worktree"])
                            == canonical_path(str(lane.get("worktree")))
                            and observed_at is not None
                            and resume_timestamp is not None
                            and observed_at > resume_timestamp,
                            f"{prefix} worktree observation is stale or mismatched",
                        )
                        invalid_tasks |= not valid_worktree
                    invalid_tasks |= not need(
                        set(observed_lane_ids) == set(claim_lanes)
                        and len(observed_lane_ids) == len(set(observed_lane_ids)),
                        f"{prefix} worktree inventory is not exhaustive and unique",
                    )
                claim_observations = data.get("claims")
                if isinstance(claim_observations, list):
                    observed_claim_keys = []
                    for observation in claim_observations:
                        valid_claim = need(
                            isinstance(observation, dict),
                            f"{prefix} claim observation must be an object",
                        )
                        if not isinstance(observation, dict):
                            invalid_tasks = True
                            continue
                        lane_id = observation.get("lane_id")
                        claim_key = (
                            "parent"
                            if observation.get("work_item") == parent_id
                            and lane_id is None
                            else lane_id
                        )
                        expected_claim = expected_claims.get(claim_key, {})
                        observed_claim_keys.append(claim_key)
                        observed_at = parsed_time(observation.get("observed_at"))
                        valid_claim &= need(
                            claim_key in expected_claims
                            and observation.get("work_item")
                            == expected_claim.get("work_item")
                            and observation.get("actor_id")
                            == expected_claim.get("actor_id")
                            and observation.get("state") == "retained"
                            and observation.get("owner")
                            == expected_claim.get("owner")
                            and observation.get("token")
                            == expected_claim.get("token")
                            and observed_at is not None
                            and resume_timestamp is not None
                            and observed_at > resume_timestamp,
                            f"{prefix} claim observation is stale or mismatched",
                        )
                        invalid_tasks |= not valid_claim
                    invalid_tasks |= not need(
                        set(observed_claim_keys) == set(expected_claims)
                        and len(observed_claim_keys)
                        == len(set(observed_claim_keys)),
                        f"{prefix} claim inventory is not exhaustive and unique",
                    )
                task_observations = data.get("tasks")
                invalid_tasks |= not need(
                    isinstance(task_observations, list),
                    f"{prefix} tasks must be a list of observations",
                )
                if isinstance(task_observations, list):
                    observed_task_keys = [
                        (
                            observation.get("lane_id"),
                            observation.get("agent_id"),
                            observation.get("actor_id"),
                            observation.get("task_id"),
                        )
                        for observation in task_observations
                        if isinstance(observation, dict)
                    ]
                    expected_task_keys = {
                        (
                            lane.get("lane_id"),
                            lane.get("agent_id"),
                            lane.get("actor_id"),
                            lane.get("task_id"),
                        )
                        for lane in claim_lanes.values()
                    }
                    invalid_tasks |= not need(
                        set(observed_task_keys) == expected_task_keys
                        and len(observed_task_keys) == len(set(observed_task_keys)),
                        f"{prefix} task inventory is not exhaustive and unique",
                    )
                    for lane in claim_lanes.values():
                        matches = [
                            observation
                            for observation in task_observations
                            if isinstance(observation, dict)
                            and observation.get("lane_id") == lane.get("lane_id")
                            and observation.get("agent_id") == lane.get("agent_id")
                            and observation.get("actor_id") == lane.get("actor_id")
                            and observation.get("task_id") == lane.get("task_id")
                        ]
                        valid_observation = need(
                            len(matches) == 1,
                            f"{prefix} requires one observation for task {lane.get('task_id')}",
                        )
                        if valid_observation:
                            observation = matches[0]
                            for field in {
                                "task_state",
                                "liveness_cursor",
                                "observation_id",
                                "observed_at",
                                "worktree",
                                "head",
                                "status",
                                "processes",
                                "claim_state",
                            }:
                                valid_observation &= need(
                                    observation.get(field) is not None,
                                    f"{prefix} task observation requires {field}",
                                )
                            observed_at = parsed_time(observation.get("observed_at"))
                            valid_observation &= need(
                                observed_at is not None
                                and resume_timestamp is not None
                                and observed_at > resume_timestamp,
                                f"{prefix} task observation is not post-resume",
                            )
                            valid_observation &= need(
                                observation.get("observation_id")
                                != lane.get("observation_id"),
                                f"{prefix} reuses a task observation",
                            )
                            valid_observation &= need(
                                observation.get("task_state")
                                in {
                                    "queued",
                                    "ready",
                                    "running",
                                    "completed",
                                    "failed",
                                    "interrupted",
                                },
                                f"{prefix} task observation has invalid state",
                            )
                            valid_observation &= need(
                                observation.get("status") in {"clean", "dirty"},
                                f"{prefix} task observation has invalid status",
                            )
                            valid_observation &= need(
                                isinstance(observation.get("processes"), list),
                                f"{prefix} task observation processes must be a list",
                            )
                            valid_observation &= need(
                                observation.get("claim_state") == "retained",
                                f"{prefix} active task must retain its claim",
                            )
                            valid_observation &= need(
                                commit_identity(observation.get("head")),
                                f"{prefix} task observation requires commit-shaped HEAD",
                            )
                            handoff = item_state(lane.get("work_item", "")).get("handoff")
                            if isinstance(handoff, dict) and handoff.get("commit"):
                                valid_observation &= need(
                                    observation.get("head") == handoff.get("commit"),
                                    f"{prefix} task observation HEAD differs from Return",
                                )
                            valid_observation &= need(
                                canonical_path(str(observation.get("worktree")))
                                == canonical_path(str(lane.get("worktree"))),
                                f"{prefix} task observation changes worktree",
                            )
                            if valid_observation:
                                lane["task_state"] = observation.get("task_state")
                                lane["liveness_cursor"] = observation.get("liveness_cursor")
                                lane["observation_id"] = observation.get("observation_id")
                        invalid_tasks |= not valid_observation
            resume_pending = bool(missing or empty or invalid_tasks)
            checkpoint_resume_pending = bool(missing or empty or invalid_tasks)
        elif kind == "lane-create":
            lane_id = data.get("lane_id")
            if need(isinstance(lane_id, str) and bool(lane_id), f"{prefix} requires data.lane_id"):
                valid = need(lane_id not in lanes, f"{prefix} reuses a lane ID")
                required = {
                    "agent_id",
                    "actor_id",
                    "runtime_agent_type",
                    "task_id",
                    "transport",
                    "requested_model",
                    "requested_effort",
                    "environment",
                    "task_state",
                    "report_transport",
                    "liveness_cursor",
                    "task_id_state",
                    "resolved_model_status",
                    "resolved_effort_status",
                }
                missing = sorted(
                    field
                    for field in required
                    if not isinstance(data.get(field), str) or not data.get(field)
                )
                valid &= need(not missing, f"{prefix} missing task receipt fields: {', '.join(missing)}")
                valid &= need(
                    data.get("agent_id") in lane_agent_ids,
                    f"{prefix} has invalid worker agent ID",
                )
                valid &= need(
                    data.get("actor_id") != root_actor_id,
                    f"{prefix} root cannot be a worker actor",
                )
                valid &= need(
                    all(lane.get("actor_id") != data.get("actor_id") for lane in lanes.values()),
                    f"{prefix} reuses a worker actor identity",
                )
                assignment_mode = data.get("assignment_mode")
                assignment_ref = data.get("assignment_ref")
                valid &= need(
                    assignment_mode
                    in {"implementation", "integration-correction", "review-repair"},
                    f"{prefix} has invalid assignment mode",
                )
                valid &= need(
                    isinstance(assignment_ref, str) and bool(assignment_ref),
                    f"{prefix} requires assignment identity",
                )
                valid &= require_root_receipt(
                    data,
                    action="assign",
                    subject=item,
                    head=integration_head,
                    prefix=prefix,
                )
                if assignment_mode == "implementation":
                    valid &= need(
                        assignment_ref == item,
                        f"{prefix} implementation assignment differs from work item",
                    )
                elif assignment_mode == "integration-correction":
                    valid &= need(
                        bool(integration_regression)
                        and assignment_ref
                        == integration_regression.get("event_id"),
                        f"{prefix} correction assignment differs from open regression",
                    )
                elif assignment_mode == "review-repair":
                    valid &= need(
                        repair_open
                        and assignment_ref
                        == f"repair-{repair_generation}",
                        f"{prefix} Repair assignment differs from open generation",
                    )
                    valid &= need(
                        data.get("actor_id") not in review_actor_ids_used
                        and data.get("task_id") not in review_task_ids_used,
                        f"{prefix} Repair lane reuses a review actor or task",
                    )
                valid &= need(
                    runtime_profile_matches(
                        data.get("agent_id"),
                        data.get("runtime_agent_type"),
                        data.get("requested_model"),
                        data.get("requested_effort"),
                    ),
                    f"{prefix} agent binding does not match requested model and effort",
                )
                valid &= need(
                    data.get("transport") == "subagent-v2",
                    f"{prefix} requires subagent-v2 transport",
                )
                valid &= need(
                    data.get("environment") in {"local", "worktree"},
                    f"{prefix} has invalid task environment",
                )
                valid &= need(
                    data.get("task_state") in {"ready", "running"},
                    f"{prefix} task is not dispatchable",
                )
                valid &= need(
                    data.get("report_transport") == data.get("transport"),
                    f"{prefix} Return transport differs from task transport",
                )
                valid &= need(
                    data.get("task_id_state") == "canonical",
                    f"{prefix} task ID is not canonical",
                )
                provider_acceptance = data.get("provider_acceptance")
                valid &= need(
                    provider_binding_matches(provider_acceptance, data)
                    and provider_acceptance.get("provider")
                    in {"delegated-custody", "manual-helper"}
                    and isinstance(provider_acceptance.get("worktree"), str)
                    and Path(provider_acceptance["worktree"]).is_absolute(),
                    f"{prefix} requires task-bound provider acceptance receipt",
                )
                valid &= need(
                    data.get("environment_match") is True,
                    f"{prefix} provider did not confirm the requested environment",
                )
                valid &= require_resolved_telemetry(data, prefix)
                task_id = data.get("task_id")
                if isinstance(task_id, str) and task_id:
                    valid &= need(
                        all(
                            lane.get("task_id") != task_id
                            or lane.get("state") in SAFE_LANE_STATES
                            for lane in lanes.values()
                        ),
                        f"{prefix} reuses an active task ID",
                    )
                if valid:
                    lanes[lane_id] = {"work_item": item, "state": "created", **data}
                    state["lane_id"] = lane_id
        elif kind == "lane-preflight":
            lane_id = data.get("lane_id")
            if need(lane_id in lanes, f"{prefix} requires lane-create"):
                valid = True
                lane = lanes[lane_id]
                for field in {
                    "agent_id",
                    "runtime_agent_type",
                    "actor_id",
                    "task_id",
                    "transport",
                    "requested_model",
                    "requested_effort",
                    "environment",
                    "task_state",
                    "report_transport",
                    "liveness_cursor",
                    "assignment_mode",
                    "assignment_ref",
                }:
                    if field in data:
                        valid &= need(
                            data.get(field) == lane.get(field),
                            f"{prefix} changes task receipt field {field}",
                        )
                worktree = data.get("worktree")
                valid &= need(
                    isinstance(worktree, str)
                    and bool(worktree)
                    and Path(worktree).is_absolute(),
                    f"{prefix} requires an absolute worktree",
                )
                valid &= need(
                    commit_identity(data.get("base")),
                    f"{prefix} requires a commit-shaped exact base",
                )
                valid &= need(
                    data.get("observed_head") == data.get("base"),
                    f"{prefix} observed HEAD differs from exact base",
                )
                valid &= need(
                    data.get("base") == integration_head,
                    f"{prefix} lane base differs from current integration HEAD",
                )
                if repo and number == len(events):
                    valid &= need(
                        data.get("base") == current_head,
                        f"{prefix} lane base differs from live repository HEAD",
                    )
                valid &= need(bool(data.get("provider")), f"{prefix} requires a lane provider")
                provider_acceptance = lane.get("provider_acceptance")
                valid &= need(
                    isinstance(provider_acceptance, dict)
                    and provider_acceptance.get("provider") == data.get("provider")
                    and isinstance(worktree, str)
                    and canonical_path(str(provider_acceptance.get("worktree")))
                    == canonical_path(worktree),
                    f"{prefix} preflight differs from provider acceptance receipt",
                )
                route = (
                    lane.get("transport"),
                    lane.get("environment"),
                    data.get("provider"),
                )
                allowed_routes = {
                    ("subagent-v2", "local", "delegated-custody"),
                    ("subagent-v2", "worktree", "manual-helper"),
                }
                valid &= need(
                    route in allowed_routes,
                    f"{prefix} has incompatible transport, environment, and provider",
                )
                if lane.get("environment") == "local":
                    valid &= need(
                        lane.get("transport") == "subagent-v2",
                        f"{prefix} local agent requires subagent-v2 transport",
                    )
                    valid &= need(
                        "root_checkout" not in data,
                        f"{prefix} local lane cannot include a root checkout binding",
                    )
                if lane.get("environment") == "local" and isinstance(worktree, str):
                    valid &= need(bool(repo), f"{prefix} local lane requires repository identity")
                    if repo:
                        valid &= need(
                            canonical_path(worktree) == canonical_path(repo),
                            f"{prefix} local lane must use the repository checkout",
                        )
                    valid &= need(
                        all(
                            other_id == lane_id
                            or other.get("environment") != "local"
                            or other.get("state") in SAFE_LANE_STATES
                            or serial_lane_idle(other)
                            for other_id, other in lanes.items()
                        ),
                        f"{prefix} reuses an active local checkout",
                    )
                if lane.get("environment") == "worktree":
                    root_checkout = data.get("root_checkout")
                    valid &= need(
                        isinstance(root_checkout, dict)
                        and root_checkout.get("access") == "read-only"
                        and root_checkout.get("environment")
                        == "PARALLEL_IMPLEMENT_ROOT_CHECKOUT"
                        and isinstance(root_checkout.get("path"), str)
                        and Path(root_checkout["path"]).is_absolute()
                        and (
                            not repo
                            or canonical_path(root_checkout["path"])
                            == canonical_path(str(repo))
                        )
                        and isinstance(worktree, str)
                        and canonical_path(root_checkout["path"])
                        != canonical_path(worktree),
                        f"{prefix} requires the read-only root checkout binding",
                    )
                valid &= need(data.get("status") == "clean", f"{prefix} requires clean status")
                startup_proof = data.get("startup_proof")
                valid &= need(
                    isinstance(startup_proof, dict)
                    and startup_proof.get("status") in {"passed", "skipped"}
                    and (
                        startup_proof.get("status") == "passed"
                        or bool(startup_proof.get("reason"))
                    ),
                    f"{prefix} requires structured startup proof",
                )
                project_provenance = data.get("project_provenance")
                valid &= need(
                    isinstance(project_provenance, dict)
                    and project_provenance.get("status")
                    in {"verified", "not-applicable"}
                    and (
                        project_provenance.get("status") == "verified"
                        or bool(project_provenance.get("reason"))
                    ),
                    f"{prefix} requires structured project provenance",
                )
                for field in {"temp_root", "pytest_basetemp", "cache_root"}:
                    value = data.get(field)
                    valid &= need(
                        isinstance(value, str)
                        and bool(value)
                        and Path(value).is_absolute()
                        and isinstance(worktree, str)
                        and path_within(value, worktree),
                        f"{prefix} requires lane-contained {field}",
                    )
                if isinstance(worktree, str) and worktree:
                    valid &= need(
                        all(
                            other_id == lane_id
                            or not other.get("worktree")
                            or canonical_path(str(other.get("worktree")))
                            != canonical_path(worktree)
                            or other.get("state") in SAFE_LANE_STATES
                            or serial_lane_idle(other)
                            for other_id, other in lanes.items()
                        ),
                        f"{prefix} reuses an active worktree",
                    )
                if valid:
                    lanes[lane_id].update(data)
                    lanes[lane_id]["state"] = "ready"
                    state["preflight"] = True
        elif kind == "dispatch":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            lane_id = data.get("lane_id") or state.get("lane_id")
            if need(bool(state.get("preflight")) and lane_id in lanes, f"{prefix} requires lane-preflight"):
                valid = True
                lane = lanes[lane_id]
                claim = data.get("claim")
                valid &= need(
                    isinstance(claim, dict)
                    and claim.get("state") == "retained"
                    and claim.get("work_item") == item
                    and claim.get("actor_id") == lane.get("actor_id")
                    and claim.get("owner") == root_actor_id
                    and bool(claim.get("token"))
                    and bool(claim.get("readback")),
                    f"{prefix} requires retained claim receipt and read-back",
                )
                valid &= require_root_receipt(
                    data,
                    action="dispatch",
                    subject=item,
                    head=integration_head,
                    prefix=prefix,
                )
                assignment_sha256 = data.get("assignment_sha256")
                valid &= need(
                    isinstance(assignment_sha256, str)
                    and bool(re.fullmatch(r"[0-9a-f]{64}", assignment_sha256)),
                    f"{prefix} requires the final assignment SHA-256",
                )
                if valid:
                    lane["claim"] = claim
                    lane["assignment_sha256"] = data.get("assignment_sha256")
                if valid:
                    state["dispatched"] = True
                    lanes[lane_id]["state"] = "active"
        elif kind == "handoff":
            lane_id = data.get("lane_id") or state.get("lane_id")
            lane = lanes.get(lane_id, {})
            valid = need(
                lane.get("work_item") == item,
                f"{prefix} handoff lane belongs to another work item",
            )
            for field in {
                "agent_id",
                "runtime_agent_type",
                "actor_id",
                "task_id",
                "transport",
                "worktree",
            }:
                valid &= need(
                    isinstance(data.get(field), str)
                    and data.get(field)
                    and data.get(field) == lane.get(field),
                    f"{prefix} handoff has mismatched {field}",
                )
            feedback = state.get("feedback")
            authorized_assignment_ref = lane.get("assignment_ref")
            if isinstance(feedback, dict):
                authorized_assignment_ref = feedback.get("event_id")
            elif (
                integration_regression
                and integration_regression.get("route") == "original-worker"
                and integration_regression.get("lane_id") == lane_id
            ):
                authorized_assignment_ref = integration_regression.get("event_id")
            valid &= need(
                data.get("assignment_ref") == authorized_assignment_ref,
                f"{prefix} handoff differs from the current assignment",
            )
            expected_base = lane.get("base")
            if (
                integration_regression
                and integration_regression.get("route") == "original-worker"
                and integration_regression.get("lane_id") == lane_id
            ):
                expected_base = integration_regression.get("integration_sha")
            valid &= need(
                data.get("base") == expected_base,
                f"{prefix} handoff has mismatched base",
            )
            valid &= need(
                data.get("assignment_sha256") == lane.get("assignment_sha256"),
                f"{prefix} handoff differs from the final assignment",
            )
            valid &= need(
                data.get("status") in {"done", "blocker", "needs-feedback"},
                f"{prefix} handoff has invalid status",
            )
            missing_return = sorted(
                field for field in WORKER_RETURN_FIELDS if field not in data
            )
            valid &= need(
                not missing_return,
                f"{prefix} handoff missing Return fields: {', '.join(missing_return)}",
            )
            valid &= need(
                isinstance(data.get("changed_scope_ids"), list)
                and isinstance(data.get("actual_changed_files"), list)
                and isinstance(data.get("commands_and_results"), list)
                and isinstance(data.get("skipped_checks"), list),
                f"{prefix} handoff Return collections must be lists",
            )
            if data.get("status") == "done":
                valid &= need(bool(data.get("commit")), f"{prefix} done handoff requires commit")
            prior_handoff = state.get("handoff")
            if isinstance(feedback, dict):
                valid &= need(
                    data.get("assignment_ref") == feedback.get("event_id"),
                    f"{prefix} corrected Return differs from feedback identity",
                )
                valid &= need(
                    isinstance(prior_handoff, dict)
                    and data.get("supersedes_commit") == prior_handoff.get("commit")
                    and data.get("commit") != prior_handoff.get("commit"),
                    f"{prefix} corrected Return must supersede the prior commit",
                )
                if (
                    repo
                    and commit_identity(expected_base)
                    and commit_identity(data.get("commit"))
                ):
                    valid &= need(
                        git_is_ancestor(repo, expected_base, data["commit"]),
                        f"{prefix} successor commit does not descend from its assignment base",
                    )
            if valid:
                state["handoff"] = data
                state["handoff_event_id"] = event.get("event_id")
        elif kind == "accept":
            need(bool(state.get("dispatched")), f"{prefix}: accept requires dispatch")
            need(bool(event.get("worker_sha")), f"{prefix} requires worker_sha")
            require_root_receipt(
                data,
                action="accept-worker-return",
                subject=item,
                head=event.get("worker_sha"),
                prefix=prefix,
            )
            handoff = state.get("handoff")
            feedback = state.get("feedback")
            need(
                isinstance(handoff, dict) and handoff.get("status") == "done",
                f"{prefix} requires one valid done handoff",
            )
            if isinstance(feedback, dict):
                need(
                    state.get("handoff_event_id") != feedback.get("return_event_id")
                    and isinstance(handoff, dict)
                    and handoff.get("assignment_ref") == feedback.get("event_id"),
                    f"{prefix} feedback requires a corrected successor Return",
                )
            if isinstance(handoff, dict):
                need(
                    event.get("worker_sha") == handoff.get("commit"),
                    f"{prefix} worker SHA differs from returned commit",
                )
            state["accepted"] = event.get("worker_sha")
            state.pop("feedback", None)
            state.pop("rejected", None)
        elif kind == "reject":
            need(bool(state.get("dispatched")), f"{prefix}: reject requires dispatch")
            handoff = state.get("handoff")
            decision = event.get("decision")
            require_root_receipt(
                data,
                action="route-correction",
                subject=item,
                head=event.get("worker_sha"),
                prefix=prefix,
            )
            need(
                isinstance(handoff, dict)
                and handoff.get("status") == "done"
                and event.get("worker_sha") == handoff.get("commit"),
                f"{prefix} feedback must bind the returned commit",
            )
            need(
                isinstance(decision, dict)
                and decision.get("return_event_id") == state.get("handoff_event_id")
                and bool(decision.get("feedback"))
                and bool(decision.get("required_proof")),
                f"{prefix} requires bounded worker feedback",
            )
            state["feedback"] = {
                **(decision if isinstance(decision, dict) else {}),
                "event_id": event.get("event_id"),
            }
            state["accepted"] = None
            state["rejected"] = event.get("decision") or True
        elif kind == "land":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(bool(state.get("accepted")), f"{prefix}: land requires acceptance")
            need(not state.get("feedback"), f"{prefix} cannot land while worker feedback is open")
            need(bool(event.get("worker_sha")), f"{prefix} requires worker_sha")
            need(bool(event.get("integration_sha")), f"{prefix} requires integration_sha")
            if state.get("accepted") and event.get("worker_sha"):
                need(
                    state["accepted"] == event["worker_sha"],
                    f"{prefix} worker SHA differs from acceptance",
                )
            landed_head = event.get("integration_sha")
            worker_head = event.get("worker_sha")
            prior_head = integration_head
            require_root_receipt(
                data,
                action="land",
                subject=item,
                head=landed_head,
                prefix=prefix,
            )
            need(commit_identity(worker_head), f"{prefix} worker SHA is not a commit identity")
            need(commit_identity(landed_head), f"{prefix} integration SHA is not a commit identity")
            need(
                data.get("prior_integration_sha") == prior_head,
                f"{prefix} prior integration HEAD differs",
            )
            need(
                data.get("observed_head") == landed_head,
                f"{prefix} observed HEAD differs from integration SHA",
            )
            need(data.get("clean") is True, f"{prefix} requires clean landing read-back")
            if isinstance(worker_head, str) and isinstance(landed_head, str):
                need(
                    git_is_ancestor(repo, worker_head, landed_head),
                    f"{prefix} landed HEAD does not contain the worker commit",
                )
            if isinstance(prior_head, str) and isinstance(landed_head, str):
                need(
                    git_is_ancestor(repo, prior_head, landed_head),
                    f"{prefix} landed HEAD does not descend from prior integration HEAD",
                )
            if repo and number == last_integration_number:
                need(
                    landed_head == current_head,
                    f"{prefix} landed HEAD differs from current repository HEAD",
                )
                need(current_clean is True, f"{prefix} integration checkout is not clean")
            state["landed"] = event.get("integration_sha")
            integration_head = event.get("integration_sha") or integration_head
            lane_id = state.get("lane_id")
            if lane_id in lanes:
                lanes[lane_id]["state"] = "landed"
                need(
                    data.get("lane_head") == event.get("worker_sha"),
                    f"{prefix} worker lane HEAD differs from landed Return",
                )
                need(data.get("lane_clean") is True, f"{prefix} worker lane is not clean")
                need(
                    data.get("task_state") in {"idle", "completed"},
                    f"{prefix} worker task is not idle after landing",
                )
                need(bool(data.get("liveness_cursor")), f"{prefix} requires worker liveness read-back")
                lanes[lane_id].update(
                    {
                        "worker_sha": event.get("worker_sha"),
                        "lane_head": data.get("lane_head"),
                        "lane_clean": data.get("lane_clean"),
                        "task_state": data.get("task_state"),
                        "liveness_cursor": data.get("liveness_cursor"),
                    }
                )
        elif kind == "integration-regression":
            route = data.get("route")
            write_scope_ids, write_scope_error = scope_identifiers(data.get("write_scope"))
            require_root_receipt(
                data,
                action="route-correction",
                subject=item,
                head=integration_head,
                prefix=prefix,
            )
            need(bool(integration_head), f"{prefix} requires an integrated HEAD")
            need(
                event.get("integration_sha") == integration_head,
                f"{prefix} HEAD differs from integration HEAD",
            )
            need(
                review_invocation_id is None,
                f"{prefix} is only valid before formal review",
            )
            need(integration_regression is None, f"{prefix} duplicates an open integration regression")
            need(bool(data.get("red")), f"{prefix} requires a trusted RED")
            allowed_correction_routes = {"original-worker", "serial-integrator"}
            need(route in allowed_correction_routes, f"{prefix} has invalid correction route")
            need(
                isinstance(data.get("owner"), str) and bool(data["owner"].strip()),
                f"{prefix} requires an owner",
            )
            need(not write_scope_error, f"{prefix} write scope {write_scope_error}")
            need(bool(data.get("required_proof")), f"{prefix} requires regression proof")
            if route == "original-worker":
                lane_id = data.get("lane_id")
                lane = lanes.get(lane_id, {})
                need(lane_id in lanes, f"{prefix} requires the original lane")
                need(
                    lane.get("actor_id") == data.get("owner"),
                    f"{prefix} original lane actor differs from the authorized owner",
                )
            integration_regression = {
                **data,
                "event_id": event["event_id"],
                "integration_sha": integration_head,
                "write_scope_ids": write_scope_ids,
            }
            graph_drained = False
            review_ready = False
        elif kind == "integration-correction":
            regression = integration_regression or {}
            route = data.get("route")
            corrected_head = event.get("integration_sha")
            actor_id = data.get("actor_id")
            changed_scope_ids, changed_scope_error = scope_identifiers(data.get("changed_scope"))
            require_root_receipt(
                data,
                action="land-correction",
                subject=item,
                head=corrected_head,
                prefix=prefix,
            )
            need(bool(integration_regression), f"{prefix} requires an open integration regression")
            need(
                data.get("regression_event_id") == regression.get("event_id"),
                f"{prefix} regression identity differs",
            )
            need(
                data.get("prior_integration_sha") == integration_head,
                f"{prefix} prior HEAD differs from integration HEAD",
            )
            need(route == regression.get("route"), f"{prefix} correction route differs")
            need(
                isinstance(actor_id, str) and bool(actor_id.strip()),
                f"{prefix} requires actor_id",
            )
            need(
                actor_id == regression.get("owner"),
                f"{prefix} actor differs from authorized owner",
            )
            need(bool(corrected_head), f"{prefix} requires integration_sha")
            need(corrected_head != integration_head, f"{prefix} requires a successor HEAD")
            need(not changed_scope_error, f"{prefix} changed scope {changed_scope_error}")
            if not changed_scope_error:
                authorized_scope_ids = set(regression.get("write_scope_ids") or [])
                need(
                    set(changed_scope_ids) <= authorized_scope_ids,
                    f"{prefix} changed scope exceeds authorization",
                )
            need(bool(event.get("validation")), f"{prefix} requires correction proof")
            delegated_routes = {"original-worker", "serial-integrator"}
            if route in delegated_routes:
                lane_id = data.get("lane_id")
                worker_sha = data.get("worker_sha")
                landing_method = data.get("landing_method", "direct")
                need(lane_id in lanes, f"{prefix} requires a known correction lane")
                lane_actor = lanes.get(lane_id, {}).get("actor_id")
                need(
                    isinstance(lane_actor, str) and bool(lane_actor),
                    f"{prefix} correction lane lacks preflight actor identity",
                )
                need(
                    lane_actor == actor_id,
                    f"{prefix} lane actor differs from correction actor",
                )
                lane_item = lanes.get(lane_id, {}).get("work_item")
                need(
                    bool(lane_item)
                    and item_state(str(lane_item)).get("accepted") == worker_sha,
                    f"{prefix} requires an accepted correction packet",
                )
                need(
                    data.get("correction_commit") == worker_sha,
                    f"{prefix} correction commit differs from the accepted worker commit",
                )
                if route == "original-worker":
                    need(
                        lane_id == regression.get("lane_id"),
                        f"{prefix} differs from the authorized original lane",
                    )
                else:
                    lane = lanes.get(lane_id, {})
                    need(
                        lane.get("assignment_mode") == "integration-correction"
                        and lane.get("assignment_ref") == regression.get("event_id"),
                        f"{prefix} fresh lane is not assigned to the open regression",
                    )
                    need(
                        lane.get("agent_id") == "serial-integrator",
                        f"{prefix} cross-worker correction requires serial-integrator",
                    )
                need(
                    landing_method
                    in {"direct", "merge", "cherry-pick", "squash", "patch"},
                    f"{prefix} has invalid landing method",
                )
                if landing_method in {"direct", "merge"}:
                    need(
                        git_is_ancestor(repo, worker_sha, corrected_head),
                        f"{prefix} successor HEAD does not contain the accepted correction commit",
                    )
                else:
                    need(
                        bool(data.get("landing_readback")),
                        f"{prefix} transformed landing requires diff read-back",
                    )
                need(
                    data.get("lane_head") == worker_sha,
                    f"{prefix} correction lane HEAD differs from worker commit",
                )
                need(data.get("lane_clean") is True, f"{prefix} correction lane is not clean")
                need(
                    data.get("task_state") in {"idle", "completed"},
                    f"{prefix} correction task is not idle",
                )
                need(bool(data.get("liveness_cursor")), f"{prefix} requires correction liveness read-back")
                lanes[lane_id].update(
                    {
                        "state": "landed",
                        "worker_sha": worker_sha,
                        "lane_head": data.get("lane_head"),
                        "lane_clean": data.get("lane_clean"),
                        "task_state": data.get("task_state"),
                        "liveness_cursor": data.get("liveness_cursor"),
                    }
                )
            if integration_head and corrected_head:
                need(
                    git_is_ancestor(repo, integration_head, corrected_head),
                    f"{prefix} successor HEAD does not descend from integration HEAD",
                )
            integration_head = corrected_head or integration_head
            latest_integration_correction = corrected_head
            integration_regression = None
            graph_drained = False
            review_ready = False
        elif kind == "graph-drained":
            require_root_receipt(
                data,
                action="graph-drained",
                subject=item,
                head=integration_head,
                prefix=prefix,
            )
            need(bool(children), f"{prefix} requires an exhaustive scope")
            unfinished = [child for child in children if not item_state(child).get("landed") and not item_state(child).get("disposition")]
            need(not unfinished, f"{prefix} has unfinished children: {', '.join(unfinished)}")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            graph_drained = True
        elif kind == "review-ready":
            require_root_receipt(
                data,
                action="review-ready",
                subject=item,
                head=integration_head,
                prefix=prefix,
            )
            need(graph_drained, f"{prefix} requires graph-drained")
            need(not repair_open, f"{prefix} requires completed Repair")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            need(
                repair_generation == repair_completed_generation,
                f"{prefix} latest Repair generation lacks completion proof",
            )
            task_receipts = data.get("tasks")
            expected_tasks = {
                (
                    lane_id,
                    lane.get("actor_id"),
                    lane.get("task_id"),
                )
                for lane_id, lane in lanes.items()
            }
            observed_tasks = {
                (
                    receipt.get("lane_id"),
                    receipt.get("actor_id"),
                    receipt.get("task_id"),
                )
                for receipt in task_receipts or []
                if isinstance(receipt, dict)
                and receipt.get("state") in {"idle", "completed"}
            }
            need(
                isinstance(task_receipts, list)
                and len(task_receipts) == len(observed_tasks)
                and observed_tasks == expected_tasks,
                f"{prefix} requires exhaustive idle implementation task evidence",
            )
            if isinstance(task_receipts, list):
                receipts_by_lane = {
                    receipt.get("lane_id"): receipt
                    for receipt in task_receipts
                    if isinstance(receipt, dict)
                }
                for lane_id, lane in lanes.items():
                    receipt = receipts_by_lane.get(lane_id, {})
                    need(
                        receipt.get("head") == lane.get("worker_sha")
                        and receipt.get("clean") is True
                        and bool(receipt.get("liveness_cursor")),
                        f"{prefix} requires current clean idle evidence for lane {lane_id}",
                    )
            integration_receipt = data.get("integration")
            need(
                isinstance(integration_receipt, dict)
                and integration_receipt.get("head") == integration_head
                and integration_receipt.get("clean") is True,
                f"{prefix} requires clean candidate HEAD read-back",
            )
            proof = data.get("final_proof")
            need(
                isinstance(proof, dict)
                and proof.get("head") == integration_head
                and proof.get("status") == "passed"
                and bool(proof.get("receipt")),
                f"{prefix} requires candidate-bound final proof receipt",
            )
            if repo and number == last_review_ready_number:
                need(
                    integration_head == current_head and current_clean is True,
                    f"{prefix} candidate differs from clean current repository HEAD",
                )
            review_ready = True
        elif kind == "review-invocation":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            invocation_id = event["event_id"]
            mode = data.get("mode")
            route = data.get("route")
            actor_id = data.get("actor_id")
            review_agent_id = data.get("agent_id")
            review_lane_id = data.get("lane_id")
            review_task_id = data.get("task_id")
            review_transport = data.get("transport")
            review_model = data.get("requested_model")
            review_effort = data.get("requested_effort")
            review_environment = data.get("environment")
            review_task_state = data.get("task_state")
            review_liveness_cursor = data.get("liveness_cursor")
            review_worktree = data.get("worktree")
            review_provider = data.get("provider")
            target = event.get("integration_sha")
            require_root_receipt(
                data,
                action="select-review",
                subject=item,
                head=target,
                prefix=prefix,
            )
            implementation_actors = implementation_actor_ids()
            valid = True
            allowed_modes = {"initial", "remediation"}
            valid &= need(mode in allowed_modes, f"{prefix} has invalid review mode")
            valid &= need(
                isinstance(root_actor_id, str) and bool(root_actor_id),
                f"{prefix} requires the campaign root actor ID",
            )
            valid &= need(
                route in {"change-review", "high-assurance-review"},
                f"{prefix} has invalid review route",
            )
            route_evidence = data.get("route_evidence")
            valid_route_evidence = need(
                isinstance(route_evidence, dict)
                and route_evidence.get("candidate") == target
                and bool(route_evidence.get("source"))
                and route_evidence.get("basis")
                in {"ordinary", "release", "supported-high-risk"},
                f"{prefix} requires candidate-bound route evidence",
            )
            if valid_route_evidence and isinstance(route_evidence, dict):
                basis = route_evidence.get("basis")
                valid &= need(
                    (route == "change-review" and basis == "ordinary")
                    or (
                        route == "high-assurance-review"
                        and basis in {"release", "supported-high-risk"}
                    ),
                    f"{prefix} route differs from its evidence basis",
                )
                if basis == "supported-high-risk":
                    valid &= need(
                        bool(route_evidence.get("trigger")),
                        f"{prefix} supported-high-risk route requires its trigger",
                    )
            valid &= need(
                isinstance(actor_id, str) and bool(actor_id.strip()),
                f"{prefix} requires a review actor ID",
            )
            if isinstance(actor_id, str) and actor_id:
                valid &= need(
                    actor_id not in implementation_actors,
                    f"{prefix} review actor is an implementation or integration actor",
                )
                valid &= need(
                    actor_id not in review_actor_ids_used,
                    f"{prefix} reuses a prior review actor",
                )
            valid &= need(
                review_agent_id == REVIEW_AGENT_IDS.get(route),
                f"{prefix} review agent ID does not match route",
            )
            valid &= need(
                isinstance(review_lane_id, str) and bool(review_lane_id),
                f"{prefix} requires a review lane ID",
            )
            valid &= need(
                runtime_profile_matches(
                    review_agent_id,
                    data.get("runtime_agent_type"),
                    review_model,
                    review_effort,
                ),
                f"{prefix} review agent binding does not match requested model and effort",
            )
            valid &= need(
                isinstance(review_task_id, str) and bool(review_task_id),
                f"{prefix} requires a review task ID",
            )
            valid &= need(
                review_transport == "subagent-v2",
                f"{prefix} review requires subagent-v2 transport",
            )
            valid &= need(
                review_environment in {"local", "worktree"},
                f"{prefix} has invalid review environment",
            )
            valid &= need(
                isinstance(review_worktree, str)
                and bool(review_worktree)
                and Path(review_worktree).is_absolute(),
                f"{prefix} requires an absolute review worktree",
            )
            valid &= need(
                (review_environment, review_provider)
                == ("local", "delegated-custody"),
                f"{prefix} review requires delegated custody of the local candidate",
            )
            if isinstance(review_worktree, str) and review_worktree:
                valid &= need(
                    all(
                        lane.get("state") in SAFE_LANE_STATES
                        or serial_lane_idle(lane)
                        or not lane.get("worktree")
                        or canonical_path(str(lane.get("worktree")))
                        != canonical_path(review_worktree)
                        for lane in lanes.values()
                    ),
                    f"{prefix} review reuses an implementation worktree",
                )
            valid &= need(
                review_task_state in {"ready", "running", "completed"},
                f"{prefix} has invalid review task state",
            )
            valid &= need(
                isinstance(review_liveness_cursor, str)
                and bool(review_liveness_cursor),
                f"{prefix} requires review liveness cursor",
            )
            valid &= need(
                data.get("task_id_state") == "canonical",
                f"{prefix} review task ID is not canonical",
            )
            provider_acceptance = data.get("provider_acceptance")
            valid &= need(
                provider_binding_matches(provider_acceptance, data)
                and provider_acceptance.get("provider") == review_provider
                and isinstance(provider_acceptance.get("worktree"), str)
                and isinstance(review_worktree, str)
                and canonical_path(provider_acceptance["worktree"])
                == canonical_path(review_worktree),
                f"{prefix} requires task-bound review provider receipt",
            )
            valid &= need(
                data.get("environment_match") is True,
                f"{prefix} provider did not confirm the review environment",
            )
            valid &= require_resolved_telemetry(data, prefix, review=True)
            valid &= need(
                data.get("observed_head") == target,
                f"{prefix} review observed HEAD differs from target",
            )
            valid &= need(data.get("status") == "clean", f"{prefix} review checkout is not clean")
            valid &= need(
                isinstance(data.get("startup_proof"), dict)
                and data["startup_proof"].get("status") == "passed",
                f"{prefix} requires review startup proof",
            )
            valid &= need(
                isinstance(data.get("project_provenance"), dict)
                and data["project_provenance"].get("status") == "verified",
                f"{prefix} requires review project provenance",
            )
            for field in {"temp_root", "pytest_basetemp", "cache_root"}:
                value = data.get(field)
                valid &= need(
                    isinstance(value, str)
                    and bool(value)
                    and Path(value).is_absolute()
                    and isinstance(review_worktree, str)
                    and path_within(value, review_worktree),
                    f"{prefix} requires review-lane-contained {field}",
                )
            implementation_tasks = {
                lane.get("task_id")
                for lane in lanes.values()
                if isinstance(lane.get("task_id"), str) and lane.get("task_id")
            }
            if isinstance(review_task_id, str) and review_task_id:
                valid &= need(
                    review_task_id not in implementation_tasks,
                    f"{prefix} review task is an implementation task",
                )
                valid &= need(
                    review_task_id not in review_task_ids_used,
                    f"{prefix} reuses a prior review task",
                )
            valid &= need(
                target == integration_head,
                f"{prefix} HEAD differs from integration HEAD",
            )
            if review_invocation_id is None:
                valid &= need(
                    review_ready and mode == "initial",
                    f"{prefix} first invocation must be initial and review-ready",
                )
            elif review_decision == "scope-mismatch":
                valid &= need(
                    review_route_mismatches == 1
                    and target == review_target
                    and mode == review_mode
                    and route != review_route,
                    f"{prefix} route-mismatch retry must keep target and mode, select the other route, and occur once",
                )
            elif mode == "remediation":
                valid &= need(review_ready, f"{prefix} remediation requires review-ready")
                valid &= need(
                    repair_completed_generation == repair_generation
                    and repair_generation > 0,
                    f"{prefix} remediation requires completed Repair proof",
                )
                valid &= need(
                    repair_base == review_target,
                    f"{prefix} Repair base differs from prior review target",
                )
                valid &= need(
                    target != review_target,
                    f"{prefix} remediation requires a successor HEAD",
                )
            else:
                valid &= need(
                    False,
                    f"{prefix} initial mode is only valid for the first invocation",
                )
            if valid:
                if target != review_target:
                    review_route_mismatches = 0
                review_invocation_id = invocation_id
                review_mode = mode
                review_route = route if isinstance(route, str) else None
                review_actor_id = actor_id if isinstance(actor_id, str) else None
                if isinstance(review_task_id, str) and review_task_id:
                    review_task_ids_used.add(review_task_id)
                review_receipt = {
                    field: data.get(field)
                    for field in {
                        "agent_id",
                        "runtime_agent_type",
                        "lane_id",
                        "actor_id",
                        "task_id",
                        "transport",
                        "requested_model",
                        "requested_effort",
                        "environment",
                        "worktree",
                        "provider",
                        "resolved_model_status",
                        "resolved_model",
                        "resolved_effort_status",
                        "resolved_effort",
                        "telemetry_unavailable_reason",
                    }
                }
                review_target = target
                review_ready = False
                review_decision = None
                review_decision_id = None
                review_findings = []
                review_residual_risks = []
        elif kind == "review-decision":
            need(bool(review_target), f"{prefix} requires a review invocation")
            need(review_decision is None, f"{prefix} duplicates a decision for the review target")
            need(event.get("integration_sha") == review_target, f"{prefix} HEAD differs from review target")
            if repo and number > last_integration_number:
                need(
                    event.get("integration_sha") == current_head,
                    f"{prefix} reviewed HEAD differs from current HEAD",
                )
                need(current_clean is True, f"{prefix} requires a clean current checkout")
            decision = event.get("decision")
            need(
                decision
                in ACCEPTED_REVIEWS
                | {"blocked", "incomplete", "scope-mismatch"},
                f"{prefix} has unknown decision",
            )
            decision_invocation = data.get("review_invocation_id")
            need(
                decision_invocation == review_invocation_id,
                f"{prefix} review invocation identity differs",
            )
            mode = data.get("mode", review_mode)
            need(mode == review_mode, f"{prefix} review mode differs from invocation")
            if review_invocation_id is not None:
                need(data.get("route") == review_route, f"{prefix} review route differs from invocation")
                implementation_actors = implementation_actor_ids()
                returned_actor_ids = (
                    {review_actor_id}
                    if isinstance(review_actor_id, str) and review_actor_id
                    else set()
                )
                assurance_returns = data.get("assurance_returns", [])
                if review_route == "high-assurance-review":
                    require_quorum = decision in (ACCEPTED_REVIEWS | {"blocked"})
                    valid_returns = need(
                        isinstance(assurance_returns, list)
                        and len(assurance_returns) <= 3
                        and all(isinstance(row, dict) for row in assurance_returns),
                        f"{prefix} assurance returns must contain at most three lanes",
                    )
                    if valid_returns and isinstance(assurance_returns, list):
                        agent_ids = [row.get("agent_id") for row in assurance_returns]
                        assurance_actors = [row.get("actor_id") for row in assurance_returns]
                        assurance_tasks = [row.get("task_id") for row in assurance_returns]
                        assurance_lanes = [row.get("lane_id") for row in assurance_returns]
                        valid_agent_ids = need(
                            all(
                                isinstance(agent_id, str)
                                and agent_id in ASSURANCE_REVIEWER_IDS
                                for agent_id in agent_ids
                            )
                            and len(agent_ids) == len(set(agent_ids)),
                            f"{prefix} assurance returns require unique known agent IDs",
                        )
                        if require_quorum:
                            valid_agent_ids &= need(
                                frozenset(agent_ids)
                                in {
                                    frozenset(ASSURANCE_CORE_AGENT_IDS),
                                    frozenset(ASSURANCE_REVIEWER_IDS),
                                },
                                f"{prefix} requires two core assurance returns and at most one specialist",
                            )
                        valid_identity_fields = valid_agent_ids
                        for field, values in {
                            "actor_id": assurance_actors,
                            "task_id": assurance_tasks,
                            "lane_id": assurance_lanes,
                        }.items():
                            valid_identity_fields &= need(
                                all(isinstance(value, str) and bool(value) for value in values)
                                and len(values) == len(set(values)),
                                f"{prefix} assurance returns require unique nonempty {field} values",
                            )
                        valid_identity_fields &= need(
                            all(
                                row.get("status")
                                in ({"complete"} if require_quorum else {"complete", "blocked"})
                                and row.get("reviewed_head") == review_target
                                for row in assurance_returns
                            ),
                            f"{prefix} assurance returns are incomplete or bound to another snapshot",
                        )
                        valid_bindings = True
                        for row in assurance_returns:
                            agent_id = row.get("agent_id")
                            valid_bindings &= need(
                                runtime_profile_matches(
                                    agent_id,
                                    row.get("runtime_agent_type"),
                                    row.get("requested_model"),
                                    row.get("requested_effort"),
                                ),
                                f"{prefix} assurance reviewer binding does not match {agent_id}",
                            )
                            valid_bindings &= need(
                                row.get("transport") == "subagent-v2"
                                and row.get("task_id_state") == "canonical",
                                f"{prefix} assurance reviewer {agent_id} requires canonical subagent-v2 transport",
                            )
                            provider_acceptance = row.get("provider_acceptance")
                            valid_bindings &= need(
                                isinstance(provider_acceptance, dict)
                                and provider_acceptance.get("status") == "accepted"
                                and provider_binding_matches(provider_acceptance, row)
                                and row.get("environment") in {"local", "worktree"}
                                and (
                                    row.get("environment"),
                                    provider_acceptance.get("provider"),
                                )
                                == ("local", "delegated-custody")
                                and isinstance(row.get("worktree"), str)
                                and Path(row["worktree"]).is_absolute()
                                and provider_acceptance.get("worktree")
                                == row.get("worktree"),
                                f"{prefix} assurance reviewer {agent_id} requires a task-bound provider receipt",
                            )
                            valid_bindings &= require_resolved_telemetry(
                                row,
                                f"{prefix} assurance reviewer {agent_id}",
                                review=True,
                            )
                        valid_identity_fields &= valid_bindings
                        if decision == "scope-mismatch":
                            valid_identity_fields &= need(
                                not assurance_returns,
                                f"{prefix} scope mismatch cannot return assurance lanes",
                            )
                        implementation_tasks = {
                            lane.get("task_id")
                            for lane in lanes.values()
                            if isinstance(lane.get("task_id"), str)
                            and lane.get("task_id")
                        }
                        if valid_identity_fields:
                            need(
                                not (
                                    set(assurance_actors)
                                    & ({review_actor_id} | implementation_actors)
                                ),
                                f"{prefix} assurance reviewer actors overlap the coordinator or implementation actors",
                            )
                            need(
                                not (
                                    set(assurance_tasks)
                                    & (
                                        {review_receipt.get("task_id")}
                                        | implementation_tasks
                                        | review_task_ids_used
                                    )
                                ),
                                f"{prefix} assurance reviewer tasks are not fresh or independent",
                            )
                            returned_actor_ids.update(assurance_actors)
                            review_task_ids_used.update(assurance_tasks)
                else:
                    need(
                        not assurance_returns,
                        f"{prefix} ordinary review cannot return assurance lanes",
                    )
                need(
                    not (returned_actor_ids & implementation_actors),
                    f"{prefix} review actors overlap implementation or integration actors",
                )
                need(
                    not (returned_actor_ids & review_actor_ids_used),
                    f"{prefix} reuses prior review actors",
                )
                review_actor_ids_used.update(returned_actor_ids)
                if isinstance(review_receipt, dict):
                    for field, expected in review_receipt.items():
                        need(
                            data.get(field) == expected,
                            f"{prefix} review Return has mismatched {field}",
                        )
                    need(
                        data.get("terminal_task_state") == "completed",
                        f"{prefix} requires completed review task",
                    )
                    need(
                        isinstance(data.get("liveness_cursor"), str)
                        and bool(data.get("liveness_cursor")),
                        f"{prefix} requires final review liveness cursor",
                    )
                    need(
                        data.get("reviewed_head") == review_target,
                        f"{prefix} reviewed HEAD differs from review target",
                    )
                    need(data.get("clean") is True, f"{prefix} requires clean review lane")
                    need(
                        data.get("lane_state") == "provider-preserved"
                        and bool(data.get("custody")),
                        f"{prefix} requires review lane custody",
                    )
            findings = data.get("findings", [])
            residual_risks = data.get("residual_risks", [])
            need(isinstance(findings, list) and all(isinstance(finding, dict) for finding in findings), f"{prefix} data.findings must be a list of objects")
            need(
                isinstance(residual_risks, list)
                and all(isinstance(risk, dict) for risk in residual_risks),
                f"{prefix} data.residual_risks must be a list of objects",
            )
            if isinstance(findings, list) and isinstance(residual_risks, list):
                finding_ids = [
                    finding.get("id")
                    for finding in findings
                    if isinstance(finding, dict)
                ]
                need(
                    all(isinstance(finding_id, str) and bool(finding_id) for finding_id in finding_ids)
                    and len(finding_ids) == len(set(finding_ids)),
                    f"{prefix} requires unique nonempty finding IDs",
                )
                residual_ids = [
                    risk.get("id")
                    for risk in residual_risks
                    if isinstance(risk, dict)
                ]
                need(
                    all(isinstance(risk_id, str) and bool(risk_id) for risk_id in residual_ids)
                    and len(residual_ids) == len(set(residual_ids)),
                    f"{prefix} requires unique nonempty residual-risk IDs",
                )
                if decision == "pass with residual risk":
                    need(bool(residual_risks), f"{prefix} requires identified residual risks")
                elif decision == "pass":
                    need(not residual_risks, f"{prefix} pass cannot retain residual risk")
                elif decision == "scope-mismatch":
                    need(
                        not findings and not residual_risks,
                        f"{prefix} scope mismatch cannot return review judgment",
                    )
            review_decision = decision
            review_decision_id = event.get("event_id")
            review_findings = findings if isinstance(findings, list) else []
            review_residual_risks = (
                residual_risks if isinstance(residual_risks, list) else []
            )
            if decision == "scope-mismatch":
                review_route_mismatches += 1
        elif kind == "repair-plan":
            generation = data.get("generation")
            finding_ids = data.get("finding_ids")
            blockers = [finding for finding in review_findings if finding.get("blocking") is True]
            blocker_ids = [finding.get("id") for finding in blockers]
            need(review_decision == "blocked", f"{prefix} requires blocked review")
            need(data.get("review_decision_id") == review_decision_id, f"{prefix} review decision identity differs")
            need(data.get("review_target") == review_target, f"{prefix} blocked snapshot differs from review target")
            need(bool(charter_id), f"{prefix} requires a recorded Charter")
            need(data.get("charter_id") == charter_id, f"{prefix} Charter differs from campaign Charter")
            need(isinstance(generation, int) and generation == repair_generation + 1, f"{prefix} has invalid Repair generation")
            need(isinstance(generation, int) and generation <= repair_generation_budget, f"{prefix} exceeds Repair Generation Budget")
            need(bool(blockers), f"{prefix} requires complete blocking findings")
            need(
                all(
                    finding.get("remediation") == "automatic-in-scope"
                    and bool(finding.get("anchor"))
                    and bool(finding.get("evidence"))
                    and bool(finding.get("required_proof"))
                    for finding in blockers
                ),
                f"{prefix} contains an inadmissible or decision-required blocker",
            )
            need(
                isinstance(finding_ids, list)
                and all(isinstance(finding_id, str) and finding_id for finding_id in finding_ids)
                and set(finding_ids) == set(blocker_ids),
                f"{prefix} must batch every blocking finding ID",
            )
            if isinstance(generation, int):
                repair_generation = generation
            repair_findings = list(finding_ids) if isinstance(finding_ids, list) else []
            repair_base = review_target
            repair_open = True
            review_ready = False
        elif kind == "repair-complete":
            require_root_receipt(
                data,
                action="complete-repair",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(repair_open, f"{prefix} requires an open Repair generation")
            need(data.get("generation") == repair_generation, f"{prefix} Repair generation differs from plan")
            need(set(data.get("finding_ids", [])) == set(repair_findings), f"{prefix} finding IDs differ from plan")
            need(bool(event.get("validation")), f"{prefix} requires Repair proof")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            lane_id = data.get("lane_id")
            lane = lanes.get(lane_id, {})
            worker_sha = data.get("worker_sha")
            landing_method = data.get("landing_method", "direct")
            repair_item = lane.get("work_item")
            need(lane_id in lanes, f"{prefix} requires a delegated Repair lane")
            need(
                lane.get("assignment_mode") == "review-repair"
                and lane.get("assignment_ref") == f"repair-{repair_generation}",
                f"{prefix} Repair lane differs from the open generation",
            )
            need(
                data.get("actor_id") == lane.get("actor_id")
                and data.get("task_id") == lane.get("task_id"),
                f"{prefix} Repair worker provenance differs from its lane",
            )
            need(
                lane.get("actor_id") != root_actor_id
                and lane.get("actor_id") not in review_actor_ids_used
                and lane.get("task_id") not in review_task_ids_used,
                f"{prefix} Repair must use a delegated non-review worker",
            )
            need(
                bool(repair_item)
                and item_state(str(repair_item)).get("accepted") == worker_sha,
                f"{prefix} requires the accepted Repair worker commit",
            )
            need(
                data.get("prior_integration_sha") == repair_base
                and data.get("supersedes_candidate") == repair_base
                and event.get("integration_sha") != repair_base,
                f"{prefix} Repair must supersede the blocked candidate",
            )
            need(
                landing_method in {"direct", "merge", "cherry-pick", "squash", "patch"},
                f"{prefix} has invalid Repair landing method",
            )
            if landing_method in {"direct", "merge"}:
                need(
                    git_is_ancestor(repo, worker_sha, event.get("integration_sha")),
                    f"{prefix} repaired HEAD does not contain the accepted worker commit",
                )
            else:
                need(bool(data.get("landing_readback")), f"{prefix} transformed Repair requires diff read-back")
            repair_open = False
            repair_completed_generation = repair_generation
        elif kind == "closeout-head":
            require_root_receipt(
                data,
                action="lock",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(item == parent_id, f"{prefix} work item differs from the frozen parent")
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(review_decision in ACCEPTED_REVIEWS, f"{prefix} requires accepted review")
            if review_decision == "pass with residual risk":
                acceptance = data.get("residual_risk_acceptance")
                need(
                    isinstance(acceptance, dict)
                    and acceptance.get("kind") in {"caller", "frozen-policy"}
                    and isinstance(acceptance.get("source"), str)
                    and bool(acceptance.get("source").strip()),
                    f"{prefix} requires caller or frozen-policy residual-risk acceptance",
                )
                if isinstance(acceptance, dict) and acceptance.get("kind") == "frozen-policy":
                    need(
                        isinstance(residual_risk_policy, dict)
                        and acceptance.get("policy_id")
                        == residual_risk_policy.get("id")
                        and acceptance.get("policy_evidence")
                        == residual_risk_policy.get("evidence"),
                        f"{prefix} frozen-policy acceptance differs from the frozen policy",
                    )
                elif isinstance(acceptance, dict):
                    reviewed_residual_ids = [
                        risk.get("id")
                        for risk in review_residual_risks
                        if isinstance(risk.get("id"), str) and risk.get("id")
                    ]
                    residual_ids = acceptance.get("residual_ids")
                    need(
                        acceptance.get("caller_id") == caller_id
                        and bool(acceptance.get("receipt_id"))
                        and acceptance.get("review_decision_id") == review_decision_id
                        and acceptance.get("review_target") == review_target
                        and isinstance(residual_ids, list)
                        and set(residual_ids) == set(reviewed_residual_ids),
                        f"{prefix} caller acceptance differs from the reviewed residual set",
                    )
            need(event.get("integration_sha") == integration_head, f"{prefix} closeout HEAD differs from integration HEAD")
            need(event.get("integration_sha") == review_target, f"{prefix} closeout HEAD differs from review target")
            closeout_head = event.get("integration_sha")
        elif kind == "child-closeout":
            require_root_receipt(
                data,
                action="close-child",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(bool(state.get("landed") or state.get("disposition")), f"{prefix} requires landed or disposed child")
            if state.get("landed"):
                need(
                    event.get("integration_sha") == closeout_head,
                    f"{prefix} HEAD differs from the reviewed closeout HEAD",
                )
                need(
                    data.get("landed_head") == state["landed"],
                    f"{prefix} landed HEAD differs from the child landing",
                )
                need(
                    git_is_ancestor(repo, state["landed"], closeout_head),
                    f"{prefix} reviewed closeout HEAD omits the child landing",
                )
            closeout_state = data.get("state")
            need(closeout_state in {"draft", "review-final", "posted", "verified"}, f"{prefix} has invalid state")
            if closeout_state == "verified":
                required_closeout = CLOSEOUT_FIELDS
                missing = sorted(
                    field for field in required_closeout if not data.get(field)
                )
                need(not missing, f"{prefix} verified packet missing: {', '.join(missing)}")
                need(data.get("reviewed_head") == closeout_head, f"{prefix} reviewed HEAD differs from closeout HEAD")
                lane = lanes.get(state.get("lane_id"), {})
                claim = lane.get("claim")
                release = data.get("claim_release")
                need(
                    isinstance(claim, dict)
                    and isinstance(release, dict)
                    and release.get("state") == "released"
                    and release.get("token") == claim.get("token")
                    and bool(release.get("readback")),
                    f"{prefix} requires matching claim-release absence read-back",
                )
                need(
                    isinstance(data.get("affected_frontier_readback"), dict)
                    and bool(data["affected_frontier_readback"].get("receipt")),
                    f"{prefix} requires affected-frontier read-back",
                )
            child_closeouts[item] = data
        elif kind == "parent-closeout":
            require_root_receipt(
                data,
                action="close-parent",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(item == parent_id, f"{prefix} work item differs from the frozen parent")
            missing = [child for child in children if child_closeouts.get(child, {}).get("state") != "verified"]
            need(not missing, f"{prefix} requires verified child closeout: {', '.join(missing)}")
            need(data.get("state") == "verified", f"{prefix} requires verified state")
            need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
            release = data.get("claim_release")
            need(
                isinstance(parent_claim, dict)
                and isinstance(release, dict)
                and release.get("state") == "released"
                and release.get("work_item") == parent_id
                and release.get("token") == parent_claim.get("token")
                and bool(release.get("readback")),
                f"{prefix} requires matching parent claim-release absence read-back",
            )
            parent_closeout = data
        elif kind == "lane-cleanup":
            lane_id = data.get("lane_id") or state.get("lane_id")
            if need(lane_id in lanes, f"{prefix} requires known data.lane_id"):
                lane = lanes[lane_id]
                valid = True
                valid &= need(
                    lane.get("work_item") == item,
                    f"{prefix} cleanup lane belongs to another work item",
                )
                for field in {"agent_id", "actor_id", "task_id"}:
                    valid &= need(
                        data.get(field) == lane.get(field),
                        f"{prefix} cleanup has mismatched {field}",
                    )
                cleanup_state = data.get("state")
                valid &= need(
                    cleanup_state in SAFE_LANE_STATES,
                    f"{prefix} has invalid cleanup state",
                )
                valid &= need(
                    data.get("terminal_task_state")
                    in {"completed", "interrupted", "failed"},
                    f"{prefix} requires terminal task state",
                )
                valid &= need(
                    data.get("commit_disposition") in {"integrated", "preserved"},
                    f"{prefix} requires commit disposition",
                )
                returned_commit = (
                    state.get("handoff", {}).get("commit")
                    if isinstance(state.get("handoff"), dict)
                    else None
                ) or state.get("accepted")
                valid &= need(
                    commit_identity(data.get("exact_head"))
                    and data.get("exact_head") == returned_commit,
                    f"{prefix} cleanup HEAD differs from returned commit",
                )
                valid &= need(data.get("clean") is True, f"{prefix} requires clean status")
                if data.get("commit_disposition") == "integrated":
                    valid &= need(
                        bool(state.get("landed")),
                        f"{prefix} integrated disposition requires landing",
                    )
                elif data.get("commit_disposition") == "preserved":
                    valid &= need(
                        isinstance(data.get("preservation"), dict)
                        and bool(data.get("preservation")),
                        f"{prefix} preserved disposition requires evidence",
                    )
                provider = lane.get("provider")
                if cleanup_state == "removed":
                    valid &= need(
                        provider == "manual-helper"
                        and data.get("registered_after") is False
                        and data.get("directory_exists") is False,
                        f"{prefix} removed lane lacks cleanup proof",
                    )
                elif cleanup_state == "provider-preserved":
                    valid &= need(
                        provider == "delegated-custody"
                        and bool(data.get("custody")),
                        f"{prefix} provider-preserved lane lacks custody proof",
                    )
                elif cleanup_state == "unregistered-residual-directory":
                    valid &= need(
                        provider == "manual-helper"
                        and data.get("registered_after") is False
                        and data.get("directory_exists") is True
                        and data.get("intentionally_preserved") is True
                        and bool(data.get("custody")),
                        f"{prefix} residual lane lacks accepted custody proof",
                    )
                if valid:
                    lanes[lane_id].update(data)
                    lanes[lane_id]["state"] = data.get("state")
        elif kind == "tracker-lock":
            require_root_receipt(
                data,
                action="tracker-lock",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(item == parent_id, f"{prefix} work item differs from the frozen parent")
            need(bool(parent_closeout), f"{prefix} requires verified parent closeout")
            need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
            tracker_locked = True
        elif kind == "checkpoint":
            require_root_receipt(
                data,
                action="checkpoint",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            decision = event.get("decision")
            required = {
                "reason",
                "continuation",
                "current_head",
                "actors",
                "integration_state",
                "next_frontier",
                "blockers",
                "claims",
                "tracker",
            }
            missing = sorted(field for field in required if field not in data)
            need(decision in {"partial", "blocked"}, f"{prefix} has invalid outcome")
            need(not missing, f"{prefix} missing checkpoint evidence: {', '.join(missing)}")
            checkpoint_head = data.get("current_head")
            need(
                isinstance(checkpoint_head, str) and bool(checkpoint_head.strip()),
                f"{prefix} requires a nonempty current HEAD",
            )
            need(
                event.get("integration_sha") == checkpoint_head,
                f"{prefix} event HEAD differs from current HEAD",
            )
            need(data.get("actors") == "idle", f"{prefix} requires idle actors")
            need(
                data.get("integration_state") in {"clean", "preserved"},
                f"{prefix} has invalid integration state",
            )
            need(
                isinstance(data.get("next_frontier"), list),
                f"{prefix} next_frontier must be a list",
            )
            need(
                isinstance(data.get("blockers"), list),
                f"{prefix} blockers must be a list",
            )
            need(data.get("claims_complete") is True, f"{prefix} requires complete claim accounting")
            claims = data.get("claims")
            valid_claims = need(
                isinstance(claims, list) and all(isinstance(claim, dict) for claim in claims),
                f"{prefix} claims must be a list of objects",
            )
            claim_items: list[str] = []
            if isinstance(claims, list):
                for claim in claims:
                    claim_item = claim.get("work_item")
                    claim_state = claim.get("state")
                    valid_claims &= need(
                        isinstance(claim_item, str) and bool(claim_item),
                        f"{prefix} claim requires work_item",
                    )
                    if isinstance(claim_item, str):
                        claim_items.append(claim_item)
                    valid_claims &= need(
                        claim_state in {"retained", "released"},
                        f"{prefix} claim has invalid state",
                    )
                    if claim_state == "retained":
                        retained_fields = {
                            "owner",
                            "token",
                            "claimed_at",
                            "recovery_owner",
                        }
                        retained_fields.add("readback")
                        valid_claims &= need(
                            all(claim.get(field) for field in retained_fields),
                            f"{prefix} retained claim lacks custody evidence or read-back",
                        )
                    elif claim_state == "released":
                        valid_claims &= need(
                            bool(claim.get("readback")),
                            f"{prefix} released claim lacks read-back",
                        )
            if valid_claims:
                need(
                    len(claim_items) == len(set(claim_items)),
                    f"{prefix} duplicates claim work items",
                )
                retained_by_item = {
                    claim.get("work_item"): claim
                    for claim in claims
                    if claim.get("state") == "retained"
                }
                required_retained: dict[str, dict[str, Any]] = {}
                if parent_claim and not parent_closeout and parent_id:
                    required_retained[parent_id] = parent_claim
                for child in children:
                    if not item_state(child).get("landed") or child_closeouts.get(
                        child, {}
                    ).get("state") == "verified":
                        continue
                    lane = lanes.get(item_state(child).get("lane_id"), {})
                    if isinstance(lane.get("claim"), dict):
                        required_retained[child] = lane["claim"]
                missing_retained = sorted(set(required_retained) - set(retained_by_item))
                need(
                    not missing_retained,
                    f"{prefix} omits retained custody: {', '.join(missing_retained)}",
                )
                for required_item, recorded_claim in required_retained.items():
                    observed_claim = retained_by_item.get(required_item, {})
                    need(
                        observed_claim.get("owner") == recorded_claim.get("owner")
                        and observed_claim.get("token") == recorded_claim.get("token"),
                        f"{prefix} retained claim identity differs for {required_item}",
                    )
            unsafe = []
            for lane_id, lane in lanes.items():
                lane_state = lane.get("state")
                if lane_state not in SAFE_LANE_STATES or (
                    lane_state == "unregistered-residual-directory"
                    and not lane.get("intentionally_preserved")
                ):
                    unsafe.append(f"{lane_id}:{lane_state}")
            need(not unsafe, f"{prefix} has active lanes: {', '.join(unsafe)}")
            if integration_head:
                need(
                    checkpoint_head == integration_head,
                    f"{prefix} HEAD differs from integration HEAD",
                )
            if integration_regression:
                blocker_ids = {
                    blocker
                    if isinstance(blocker, str)
                    else blocker.get("id")
                    for blocker in data.get("blockers", [])
                    if isinstance(blocker, (str, dict))
                }
                need(
                    decision == "blocked",
                    f"{prefix} open integration regression requires blocked outcome",
                )
                need(
                    integration_regression.get("event_id") in blocker_ids,
                    f"{prefix} blockers omit the open integration regression",
                )
            need(not repair_open, f"{prefix} has an open Repair generation")
            checkpoint_outcome = decision
            checkpoint_data = data
            checkpoint_active = True
        elif kind == "release":
            require_root_receipt(
                data,
                action="release",
                subject=item,
                head=event.get("integration_sha"),
                prefix=prefix,
            )
            need(item == parent_id, f"{prefix} work item differs from the frozen parent")
            need(event.get("decision") == "complete", f"{prefix} requires complete")
            need(tracker_locked, f"{prefix} requires tracker Lock")
            need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
            unsafe = []
            for lane_id, lane in lanes.items():
                lane_state = lane.get("state")
                if lane_state not in SAFE_LANE_STATES or (
                    lane_state == "unregistered-residual-directory"
                    and not lane.get("intentionally_preserved")
                ):
                    unsafe.append(f"{lane_id}:{lane_state}")
            need(not unsafe, f"{prefix} has active lanes: {', '.join(unsafe)}")
            release_outcome = event.get("decision")
            release_seen = True

    if latest_integration_correction is not None and latest_integration_correction == integration_head:
        need(
            current_head == integration_head,
            "corrected integration HEAD differs from current HEAD",
        )
        need(current_clean is not False, "corrected integration checkout is not clean")
    if checkpoint_active and checkpoint_data:
        need(
            checkpoint_data.get("current_head") == current_head,
            "active checkpoint HEAD differs from current HEAD",
        )
        if checkpoint_data.get("integration_state") == "clean":
            need(current_clean is not False, "active checkpoint requires a clean integration checkout")
    lane_status: dict[str, str] = {}
    for lane_id, lane in lanes.items():
        state = str(lane.get("state") or "unknown")
        item = item_state(lane["work_item"])
        if state in SAFE_LANE_STATES:
            if state == "unregistered-residual-directory" and not lane.get("intentionally_preserved"):
                lane_status[lane_id] = "residual"
            else:
                lane_status[lane_id] = state
        elif state == "blocked-dirty":
            lane_status[lane_id] = "dirty-preserved"
        elif item.get("landed"):
            lane_status[lane_id] = "landed"
        elif item.get("accepted"):
            lane_status[lane_id] = "committed-unlanded"
        elif item.get("handoff", {}).get("clean") and not item.get("handoff", {}).get("commit"):
            lane_status[lane_id] = "clean-uncommitted"
        elif item.get("dispatched"):
            lane_status[lane_id] = "active"
        else:
            lane_status[lane_id] = state

    if release_outcome:
        campaign_status = release_outcome
    elif checkpoint_active:
        campaign_status = checkpoint_outcome or "partial"
    elif repair_open:
        campaign_status = "repairing"
    elif review_decision in ACCEPTED_REVIEWS:
        campaign_status = "reviewed"
    elif review_decision in {"blocked", "incomplete"}:
        campaign_status = "review-blocked"
    elif review_decision == "scope-mismatch":
        campaign_status = (
            "review-ready" if review_route_mismatches == 1 else "review-blocked"
        )
    elif review_ready:
        campaign_status = "review-ready"
    elif graph_drained:
        campaign_status = "drained"
    elif any(item.get("landed") for item in items.values()):
        campaign_status = "draining"
    else:
        campaign_status = "open"

    return {
        "errors": errors,
        "children": children,
        "parent_id": parent_id,
        "items": items,
        "lanes": lanes,
        "lane_status": lane_status,
        "integration_head": integration_head,
        "current_head": current_head,
        "current_clean": current_clean,
        "graph_drained": graph_drained,
        "review_ready": review_ready,
        "review_target": review_target,
        "review_decision": review_decision,
        "closeout_head": closeout_head,
        "child_closeouts": child_closeouts,
        "parent_closeout": parent_closeout,
        "release_outcome": release_outcome,
        "checkpoint_outcome": checkpoint_outcome,
        "checkpoint_data": checkpoint_data,
        "checkpoint_active": checkpoint_active,
        "checkpoint_resume_pending": checkpoint_resume_pending,
        "integration_regression": integration_regression,
        "campaign_status": campaign_status,
        "resume_pending": resume_pending,
        "tracker_locked": tracker_locked,
        "charter_id": charter_id,
        "root_actor_id": root_actor_id,
        "caller_id": caller_id,
        "residual_risk_policy": residual_risk_policy,
        "runtime_contract": RUNTIME_CONTRACT,
        "repair_generation_budget": repair_generation_budget,
        "repair_generation": repair_generation,
        "repair_completed_generation": repair_completed_generation,
        "repair_open": repair_open,
        "repair_base": repair_base,
        "repair_findings": repair_findings,
        "review_findings": review_findings,
        "review_residual_risks": review_residual_risks,
        "review_route_mismatches": review_route_mismatches,
        "review_decision_id": review_decision_id,
        "review_invocation_id": review_invocation_id,
        "review_mode": review_mode,
        "review_route": review_route,
        "review_actor_id": review_actor_id,
        "review_actor_ids_used": sorted(review_actor_ids_used),
        "review_task_ids_used": sorted(review_task_ids_used),
    }


def intent_errors(state: dict[str, Any], intent: str) -> list[str]:
    errors = list(state["errors"])
    items = state["items"]
    if state["checkpoint_active"] and intent != "checkpoint":
        errors.append("active checkpoint requires resume before authority reopens")
    if state["resume_pending"]:
        errors.append("resume requires reconciled Git, worktree, agent, and tracker evidence")
    if intent == "dispatch":
        if not any(item.get("preflight") and not item.get("dispatched") for item in items.values()):
            errors.append("no reconciled preflighted item is ready to dispatch")
    elif intent == "land":
        if not any(item.get("accepted") and not item.get("landed") for item in items.values()):
            errors.append("no accepted unlanded item is ready to land")
    elif intent == "correct-integration":
        if not state["integration_regression"]:
            errors.append("no integration regression is open")
        if state["integration_head"] != state["current_head"]:
            errors.append("integration HEAD does not equal current HEAD")
        if state["current_clean"] is False:
            errors.append("integration checkout is not clean")
    elif intent == "review":
        if not state["graph_drained"]:
            errors.append("parent graph is not execution-drained")
        if state["repair_open"]:
            errors.append("Repair generation is not complete")
        if state["integration_regression"]:
            errors.append("integration regression is not corrected")
        if state["integration_head"] != state["current_head"]:
            errors.append("integration HEAD does not equal current HEAD")
        if state["current_clean"] is False:
            errors.append("integration checkout is not clean")
        if state["repair_generation"] != state["repair_completed_generation"]:
            errors.append("latest Repair generation lacks completion proof")
        if state["review_invocation_id"] and state["review_decision"] is None:
            errors.append("current review invocation has no decision")
        if state["review_decision"] == "incomplete":
            errors.append("incomplete review requires a partial checkpoint")
        if (
            state["review_decision"] == "scope-mismatch"
            and state["review_route_mismatches"] > 1
        ):
            errors.append("review routes are exhausted; preserve a partial checkpoint")
        repaired_successor_ready = (
            state["repair_generation"] > 0
            and state["repair_generation"] == state["repair_completed_generation"]
            and state["integration_head"] != state["review_target"]
        )
        if state["review_decision"] == "blocked" and not repaired_successor_ready:
            errors.append("blocked review requires Repair or caller decision")
    elif intent == "repair":
        if not state["charter_id"]:
            errors.append("campaign Charter is not recorded")
        if state["review_decision"] != "blocked":
            errors.append("review is not blocked")
        if not state["repair_open"]:
            errors.append("no Repair plan is open")
        if state["repair_generation"] > state["repair_generation_budget"]:
            errors.append("Repair Generation Budget is exhausted")
        if state["review_target"] != state["current_head"]:
            errors.append("blocked review target does not equal current HEAD")
    elif intent == "lock":
        if state["review_decision"] not in ACCEPTED_REVIEWS:
            errors.append("review has not passed")
        if state["review_target"] != state["current_head"]:
            errors.append("review target does not equal current HEAD")
        if state["repair_open"]:
            errors.append("Repair generation remains open")
    elif intent == "checkpoint":
        if not state["checkpoint_active"]:
            errors.append("no resumable checkpoint is active")
    elif intent == "complete":
        if state["review_decision"] not in ACCEPTED_REVIEWS:
            errors.append("review has not passed")
        if state["closeout_head"] != state["current_head"]:
            errors.append("closeout HEAD does not equal current HEAD")
        if state["current_clean"] is not True:
            errors.append("integration checkout is not clean")
        missing = [child for child in state["children"] if state["child_closeouts"].get(child, {}).get("state") != "verified"]
        if missing:
            errors.append(f"children lack verified closeout: {', '.join(missing)}")
        if not state["parent_closeout"]:
            errors.append("parent closeout is not verified")
        if not state["tracker_locked"]:
            errors.append("tracker Lock is not verified")
        for lane_id, lane_state in state["lane_status"].items():
            if lane_state not in SAFE_LANE_STATES:
                recorded = state["lanes"][lane_id].get("state")
                errors.append(f"lane {lane_id} remains {lane_state} ({recorded})")
    return list(dict.fromkeys(errors))


def status(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    return public_state("status", args, state, events)


def implementation_states(state: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for child in state["children"]:
        item = state["items"].get(child, {})
        closeout = state["child_closeouts"].get(child, {})
        if closeout.get("state") == "verified":
            value = "closed"
        elif item.get("landed"):
            value = "landed-awaiting-lock"
        elif item.get("accepted"):
            value = "accepted"
        elif item.get("dispatched"):
            value = "active"
        elif item.get("preflight"):
            value = "ready"
        elif item.get("disposition"):
            value = f"disposed:{item['disposition']}"
        else:
            value = "pending"
        result[child] = value
    return result


def facade_view(state: dict[str, Any]) -> dict[str, Any]:
    implementations = implementation_states(state)
    active = sorted(
        lane_id
        for lane_id, lane_state in state["lane_status"].items()
        if lane_state in {"active", "committed-unlanded", "dirty-preserved"}
    )
    mechanically_eligible = [
        intent for intent in sorted(INTENTS) if not intent_errors(state, intent)
    ]
    owner = "agent"
    action = "select-frontier"
    subjects = sorted(
        key for key, value in implementations.items() if value == "pending"
    )
    phase = "select"

    if state["errors"]:
        phase, action = "blocked", "reconcile-state"
        subjects = []
    elif state["release_outcome"] == "complete":
        phase, action = "complete", "none"
        owner, subjects = "none", []
    elif state["checkpoint_active"]:
        phase, action = "checkpoint", "resume"
        subjects = []
    elif state["resume_pending"]:
        phase, action = "open", "reconcile"
        subjects = []
    elif state["integration_regression"]:
        phase, action = "drain", "correct-integration"
        subjects = [state["integration_regression"].get("event_id") or "integration"]
    elif any(value == "ready" for value in implementations.values()):
        phase, action = "open", "dispatch"
        subjects = sorted(key for key, value in implementations.items() if value == "ready")
    elif any(value == "accepted" for value in implementations.values()):
        phase, action = "drain", "inspect-land"
        subjects = sorted(key for key, value in implementations.items() if value == "accepted")
    elif any(value == "active" for value in implementations.values()):
        phase, action = "drain", "await-worker"
        owner, subjects = "task", active
    elif not state["graph_drained"]:
        finished = all(
            value.startswith("landed") or value.startswith("disposed") or value == "closed"
            for value in implementations.values()
        ) and bool(implementations)
        if finished:
            phase, action = "review", "record-graph-drained"
            subjects = list(state["children"])
    elif state["review_invocation_id"] and state["review_decision"] is None:
        phase, action = "review", "await-review"
        owner = "task"
        subjects = [state["review_invocation_id"]]
    elif state["review_decision"] == "scope-mismatch":
        phase, action = (
            ("review", "select-review")
            if state["review_route_mismatches"] == 1
            else ("checkpoint", "record-checkpoint")
        )
        subjects = [state["review_target"]] if state["review_target"] else []
    elif state["review_decision"] not in {None, *ACCEPTED_REVIEWS}:
        phase, action = "review", "decide-repair"
        subjects = [
            finding.get("id")
            for finding in state["review_findings"]
            if isinstance(finding, dict) and finding.get("id")
        ]
    elif state["review_decision"] in ACCEPTED_REVIEWS:
        if not state["closeout_head"]:
            phase, action = "lock", "lock"
            subjects = [state["review_target"]] if state["review_target"] else []
        elif not state["tracker_locked"]:
            phase, action = "lock", "closeout"
            subjects = [entry["owner"] for entry in closeout_actions(state)]
        else:
            phase, action = "release", "finish"
            subjects = []
    elif not state["review_ready"]:
        phase, action = "review", "record-review-ready"
        subjects = [state["current_head"]] if state["current_head"] else []
    else:
        phase, action = "review", "select-review"
        subjects = [state["review_target"]] if state["review_target"] else []

    return {
        "phase": phase,
        "unfinished_children": sorted(
            key for key, value in implementations.items() if value != "closed"
        ),
        "recorded_ready": sorted(
            key for key, value in implementations.items() if value == "ready"
        ),
        "active_lanes": active,
        "blockers": state["errors"],
        "mechanically_eligible_intents": mechanically_eligible,
        "items": implementations,
        "awaiting": {
            "owner": owner,
            "action": action,
            "subjects": subjects,
        },
    }


def public_state(
    operation: str,
    args: argparse.Namespace,
    state: dict[str, Any],
    events: list[dict[str, Any]],
    **extra: Any,
) -> int:
    view = facade_view(state)
    projection = {
        "revision": len(events),
        "campaign_status": state["campaign_status"],
        "head": {
            "integration": state["integration_head"],
            "current": state["current_head"],
            "clean": state["current_clean"],
        },
        **view,
    }
    state_path = run_path(args.run) / "state.json"
    write_derived_json(state_path, projection)
    if state["errors"]:
        detail = run_path(args.run) / "failure.json"
        write_derived_json(detail, {"code": "STATE_INVALID", "errors": state["errors"]})
        return emit(
            False,
            operation=operation,
            code="STATE_INVALID",
            revision=len(events),
            effect_started=False,
            changed=False,
            detail=str(detail),
        )
    return emit(
        True,
        operation=operation,
        revision=len(events),
        phase=view["phase"],
        head=state["current_head"],
        awaiting=view["awaiting"],
        state=str(state_path),
        **extra,
    )


def read_object(path_value: str) -> dict[str, Any]:
    value = json.loads(Path(path_value).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path_value} must contain one JSON object")
    return value


def start(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    if load_events(path):
        raise ValueError("start requires an empty event stream; use status to resume")
    packet = read_object(args.scope_file)
    parent = packet.get("parent")
    children = packet.get("children")
    charter = packet.get("charter")
    root_actor_id = packet.get("root_actor_id")
    caller_id = packet.get("caller_id")
    parent_claim = packet.get("parent_claim")
    if not isinstance(parent, str) or not parent:
        raise ValueError("scope packet requires parent")
    if not isinstance(children, list):
        raise ValueError("scope packet requires children")
    if (
        not children
        or not all(isinstance(child, str) and child.strip() for child in children)
        or len(children) != len(set(children))
    ):
        raise ValueError("scope packet requires nonempty unique child IDs")
    if (
        not isinstance(charter, dict)
        or not isinstance(charter.get("id"), str)
        or not charter["id"].strip()
        or not isinstance(charter.get("outcome"), str)
        or not charter["outcome"].strip()
    ):
        raise ValueError("scope packet requires charter.id and charter.outcome")
    if not isinstance(root_actor_id, str) or not root_actor_id.strip():
        raise ValueError("scope packet requires root_actor_id")
    if not isinstance(caller_id, str) or not caller_id.strip():
        raise ValueError("scope packet requires caller_id")
    if not (
        isinstance(parent_claim, dict)
        and parent_claim.get("state") == "retained"
        and parent_claim.get("work_item") == parent
        and parent_claim.get("owner") == root_actor_id
        and bool(parent_claim.get("token"))
        and bool(parent_claim.get("readback"))
    ):
        raise ValueError("scope packet requires the retained parent claim")
    repair_budget = charter.get("repair_generation_budget", 2)
    charter = {
        **charter,
        "runtime_contract": RUNTIME_CONTRACT,
        "repair_generation_budget": repair_budget,
    }
    data = {
        key: value
        for key, value in packet.items()
        if key not in {"parent", "integration_sha"}
    }
    if not args.repo:
        raise ValueError("start requires --repo")
    data["repo"] = canonical_path(args.repo)
    data["charter"] = charter
    raw = {
        "event": "scope",
        "event_id": stable_event_id("scope", {"parent": parent, "data": data}),
        "work_item": parent,
        "integration_sha": git_head(args.repo) if args.repo else packet.get("integration_sha"),
        "data": data,
    }
    applied, replayed, events, state = append_facade_events(path, [raw], repo=args.repo)
    return public_state(
        "start",
        args,
        state,
        events,
        receipt={"applied": applied, "replayed": replayed},
    )


def packet_events(packet: dict[str, Any]) -> list[dict[str, Any]]:
    kind = packet.get("kind")
    work_item = packet.get("work_item")
    identity = {key: value for key, value in packet.items() if key != "event_id"}
    if kind == "lane-ready":
        lane_id = packet.get("lane_id")
        actor_id = packet.get("actor_id")
        task_fields = {
            field: packet.get(field)
            for field in {
                "agent_id",
                "runtime_agent_type",
                "task_id",
                "transport",
                "requested_model",
                "requested_effort",
                "environment",
                "task_state",
                "report_transport",
                "liveness_cursor",
            }
        }
        if not all(
            isinstance(value, str) and value
            for value in (work_item, lane_id, actor_id, *task_fields.values())
        ):
            raise ValueError("lane-ready requires work item, lane, actor, and task receipt")
        create = packet.get("create") if isinstance(packet.get("create"), dict) else {}
        preflight = packet.get("preflight") if isinstance(packet.get("preflight"), dict) else {}
        assignment = (
            packet.get("assignment")
            if isinstance(packet.get("assignment"), dict)
            else {}
        )
        assignment_mode = assignment.get("mode")
        assignment_ref = assignment.get("ref")
        root_receipt = assignment.get("root_receipt")
        if not all(
            isinstance(value, str) and value
            for value in (assignment_mode, assignment_ref)
        ):
            raise ValueError("lane-ready requires a root-recorded assignment mode and ref")
        common = {
            "lane_id": lane_id,
            "actor_id": actor_id,
            "assignment_mode": assignment_mode,
            "assignment_ref": assignment_ref,
            "root_receipt": root_receipt,
            **task_fields,
        }
        return [
            {
                "event": "lane-create",
                "event_id": stable_event_id("lane-create", identity),
                "work_item": work_item,
                "data": {**create, **common},
            },
            {
                "event": "lane-preflight",
                "event_id": stable_event_id("lane-preflight", identity),
                "work_item": work_item,
                "data": {**preflight, **common},
            },
        ]
    if kind == "worker-result":
        required = {
            field: packet.get(field)
            for field in {
                "lane_id",
                "agent_id",
                "runtime_agent_type",
                "actor_id",
                "task_id",
                "transport",
                "worktree",
                "base",
                "assignment_ref",
            }
        }
        if not isinstance(work_item, str) or not work_item or not all(
            isinstance(value, str) and value for value in required.values()
        ):
            raise ValueError("worker-result requires work item and matching lane/task identity")
        report = packet.get("report") if isinstance(packet.get("report"), dict) else {}
        event_identity = {"work_item": work_item, **required}
        return [{"event": "handoff", "event_id": stable_event_id("handoff", event_identity), "work_item": work_item, "data": {**report, **required}}]
    if kind == "events":
        values = packet.get("events")
        if not isinstance(values, list) or not values:
            raise ValueError("events packet requires a non-empty events list")
        facade_owned = {"scope", "lane-create", "lane-preflight", "handoff", "release"}
        result = []
        for index, value in enumerate(values):
            if not isinstance(value, dict):
                raise ValueError("events packet entries must be objects")
            if value.get("event") in facade_owned:
                raise ValueError(
                    f"{value.get('event')} must use its dedicated facade command"
                )
            result.append({**value, "event_id": value.get("event_id") or stable_event_id(str(value.get("event", "event")), identity, index=index)})
        return result
    raise ValueError("unsupported packet kind; use lane-ready, worker-result, or events")


def apply_packet(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    packet = read_object(args.packet_file)
    raw_events = packet_events(packet)
    applied, replayed, events, state = append_facade_events(
        path, raw_events, repo=args.repo
    )
    return public_state(
        "apply",
        args,
        state,
        events,
        receipt={
            "applied": applied,
            "replayed": replayed,
            "event_ids": [event["event_id"] for event in raw_events],
        },
    )


def brief(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    item = state["items"].get(args.work_item, {})
    lane = state["lanes"].get(item.get("lane_id"), {})
    if not item:
        raise ValueError(f"unknown work item: {args.work_item}")
    if not lane or lane.get("state") not in {"ready", "active"}:
        raise ValueError(f"work item is not bound to a ready task lane: {args.work_item}")
    mode = lane.get("assignment_mode")
    if mode not in {"implementation", "integration-correction", "review-repair"}:
        raise ValueError(f"work item has no recorded assignment mode: {args.work_item}")
    lines = [
        "# Parallel Implementation Assignment",
        "",
        f"- Work item: `{args.work_item}`",
        f"- Mode: `{mode}`",
        f"- Agent: `{lane['agent_id']}`",
        f"- Actor: `{lane['actor_id']}`",
        f"- Lane: `{item['lane_id']}`",
        f"- Task: `{lane['task_id']}`",
        f"- Transport: `{lane['transport']}`",
        f"- Environment: `{lane['environment']}`",
        f"- Charter: `{state['charter_id'] or 'not recorded'}`",
        f"- Base: `{lane['base']}`",
        f"- Worktree: `{lane['worktree']}`",
        f"- Temp root: `{lane['temp_root']}`",
        f"- Pytest base: `{lane['pytest_basetemp']}`",
        f"- Cache root: `{lane['cache_root']}`",
        f"- Return transport: `{lane['report_transport']}`",
        f"- Liveness cursor: `{lane['liveness_cursor']}`",
    ]
    if lane["environment"] == "worktree":
        lines.extend(
            [
                f"- Root checkout: `{args.repo}`",
                "- Root checkout access: `read-only`",
                "- Write boundary: `assigned worktree only`",
            ]
        )
    if mode == "integration-correction":
        regression = state.get("integration_regression") or {}
        lines.extend([
            "",
            "## Integration correction",
            "",
            f"- Regression event: `{regression.get('event_id') or 'not recorded'}`",
            f"- Prior integration HEAD: `{regression.get('integration_sha') or 'not recorded'}`",
            f"- Route: `{regression.get('route') or 'not recorded'}`",
            f"- Authorized scope IDs: `{', '.join(regression.get('write_scope_ids') or []) or 'not recorded'}`",
            f"- Required proof: `{regression.get('required_proof') or 'not recorded'}`",
        ])
    elif mode == "review-repair":
        lines.extend([
            "",
            "## Review repair",
            "",
            f"- Generation: `{state['repair_generation']}`",
            f"- Finding IDs: `{', '.join(state['repair_findings']) or 'not recorded'}`",
            f"- Reviewed HEAD: `{state['repair_base'] or 'not recorded'}`",
        ])
    briefs = run_path(args.run) / "briefs"
    output = briefs / f"{artifact_name(args.work_item)}.md"
    if not path_within(str(output), str(briefs)):
        raise ValueError("brief artifact escapes its run directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return emit(
        True,
        operation="brief",
        work_item=args.work_item,
        mode=mode,
        artifact=str(output),
        sha256=artifact_digest(output),
    )


def finish(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    errors = intent_errors(state, "complete")
    if errors:
        detail = run_path(args.run) / "failure.json"
        write_derived_json(detail, {"code": "INCOMPLETE", "errors": errors})
        return emit(
            False,
            operation="finish",
            code="INCOMPLETE",
            effect_started=False,
            changed=False,
            detail=str(detail),
        )
    applied = 0
    replayed = 0
    if state["release_outcome"] != "complete":
        if not args.completion_file:
            raise ValueError("finish requires --in with a root release receipt")
        completion = read_object(args.completion_file) if args.completion_file else {}
        parent = events[0]["work_item"]
        release = {
            "event": "release",
            "event_id": stable_event_id(
                "release-complete",
                {"parent": parent, "head": state["current_head"]},
            ),
            "work_item": parent,
            "integration_sha": state["current_head"],
            "decision": "complete",
            "data": {"root_receipt": completion.get("root_receipt")},
        }
        applied, replayed, events, state = append_facade_events(
            path, [release], repo=args.repo
        )
    output = run_path(args.run) / "LEDGER.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown(state, path.name), encoding="utf-8")
    return emit(
        True,
        operation="finish",
        status="complete",
        head=state["current_head"],
        artifact=str(output),
        sha256=artifact_digest(output),
        receipt={"applied": applied, "replayed": replayed},
    )


def closeout_actions(state: dict[str, Any]) -> list[dict[str, str]]:
    if state["checkpoint_active"]:
        return [
            {
                "owner": "campaign",
                "action": "resume-campaign",
                "state": state["checkpoint_outcome"] or "partial",
            }
        ]
    actions: list[dict[str, str]] = []
    for child in state["children"]:
        child_state = state["child_closeouts"].get(child, {}).get("state")
        if child_state != "verified":
            actions.append({"owner": child, "action": "finalize-child-closeout", "state": child_state or "missing"})
    if not state["parent_closeout"]:
        actions.append({"owner": "parent", "action": "verify-parent-closeout", "state": "missing"})
    for lane_id, lane_state in state["lane_status"].items():
        if lane_state not in SAFE_LANE_STATES:
            actions.append({"owner": lane_id, "action": "reconcile-lane", "state": lane_state})
    return actions


def markdown(state: dict[str, Any], events_name: str) -> str:
    lines = [
        "# Parallel Implement Run Ledger",
        "",
        f"Generated from `{events_name}`; do not edit.",
        "",
        "## Campaign",
        "",
        f"- Status: `{state['campaign_status']}`",
        f"- Charter: `{state['charter_id'] or 'not recorded'}`",
        f"- Integration HEAD: `{state['integration_head'] or 'not reached'}`",
        f"- Reviewed HEAD: `{state['review_target'] or 'not reached'}`",
        f"- Closeout HEAD: `{state['closeout_head'] or 'not reached'}`",
        f"- Runtime contract: `{state['runtime_contract']}`",
        f"- Repair generations: `{state['repair_generation']}/{state['repair_generation_budget']}`",
        f"- Review: `{state['review_mode'] or 'not reached'}` / `{state['review_decision'] or 'not reached'}`",
        f"- Repair state: `{'open' if state['repair_open'] else 'closed'}`",
        f"- Carried findings: {', '.join(state['repair_findings']) or 'none'}",
        f"- Children: {', '.join(state['children']) or 'not recorded'}",
        "",
        "## Lanes",
        "",
        "| Lane | Work item | State |",
        "| --- | --- | --- |",
    ]
    for lane_id, lane_state in sorted(state["lane_status"].items()):
        lines.append(f"| `{lane_id}` | `{state['lanes'][lane_id]['work_item']}` | `{lane_state}` |")
    if not state["lane_status"]:
        lines.append("| none | none | none |")
    lines.extend(["", "## Child Implementation and Tracker Closeout", ""])
    for child in state["children"]:
        packet = state["child_closeouts"].get(child, {})
        item = state["items"].get(child, {})
        if item.get("landed"):
            implementation = f"landed at `{item['landed']}`"
        elif item.get("accepted"):
            implementation = f"committed at `{item['accepted']}`; not landed"
        elif item.get("disposition"):
            implementation = f"disposed: {item['disposition']}"
        elif item.get("dispatched"):
            implementation = "active"
        else:
            implementation = "pending"
        tracker_closeout = packet.get("state")
        if not tracker_closeout:
            tracker_closeout = (
                "deferred by checkpoint" if state["checkpoint_active"] else "not started"
            )
        lines.extend(
            [
                f"### {child}",
                "",
                f"- Implementation: {implementation}",
                f"- Tracker closeout: `{tracker_closeout}`",
                f"- Delivered: {packet.get('delivered', 'not recorded')}",
                f"- Acceptance: {packet.get('acceptance_evidence', 'not recorded')}",
                f"- Validation: {packet.get('proof', 'not recorded')}",
                f"- Review: {packet.get('review', 'not recorded')}",
                f"- Residual risk: {packet.get('residual_risk', 'not recorded')}",
                f"- Mutation read-back: {packet.get('mutation_readback', 'not recorded')}",
                "",
            ]
        )
    lines.extend(["## Closeout Plan", ""])
    actions = closeout_actions(state)
    if actions:
        lines.extend(f"- `{action['owner']}`: {action['action']} ({action['state']})" for action in actions)
    else:
        lines.append("- No remaining closeout actions.")
    lines.extend(["", "## Event Timeline", ""])
    return "\n".join(lines) + "\n"


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def parser() -> argparse.ArgumentParser:
    root = JsonArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    profile_parser = commands.add_parser("profile")
    profile_parser.add_argument("--id", dest="profile", required=True)
    profile_parser.set_defaults(handler=resolve_profile)

    start_parser = commands.add_parser("start")
    start_parser.add_argument("--run", required=True)
    start_parser.add_argument("--repo", required=True)
    start_parser.add_argument("--in", dest="scope_file", required=True)
    start_parser.set_defaults(handler=start)

    status_parser = commands.add_parser("status")
    status_parser.add_argument("--run", required=True)
    status_parser.set_defaults(handler=status)

    apply_parser = commands.add_parser("apply")
    apply_parser.add_argument("--run", required=True)
    apply_parser.add_argument("--in", dest="packet_file", required=True)
    apply_parser.set_defaults(handler=apply_packet)

    brief_parser = commands.add_parser("brief")
    brief_parser.add_argument("--run", required=True)
    brief_parser.add_argument("--item", dest="work_item", required=True)
    brief_parser.set_defaults(handler=brief)

    finish_parser = commands.add_parser("finish")
    finish_parser.add_argument("--run", required=True)
    finish_parser.add_argument("--in", dest="completion_file")
    finish_parser.set_defaults(handler=finish)
    return root


def main() -> int:
    args: argparse.Namespace | None = None
    before_revision = 0
    handler_started = False
    try:
        args = parser().parse_args()
        if args.command == "profile":
            handler_started = True
            return args.handler(args)
        args.events = str(run_events(args.run, create=args.command == "start"))
        before_revision = len(load_events(Path(args.events)))
        if args.command != "start":
            args.repo = run_repo(Path(args.events))
        handler_started = True
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        if args is None:
            return emit(
                False,
                operation=sys.argv[1] if len(sys.argv) > 1 else "parse",
                code="INPUT_INVALID",
                effect_started=False,
                changed=False,
                error=str(error),
            )
        if args.command == "profile":
            return emit(
                False,
                operation="profile",
                code="INPUT_INVALID",
                profile=getattr(args, "profile", None),
                error=str(error),
            )
        events_path = Path(args.events)
        after_revision = before_revision
        changed = False
        if handler_started:
            try:
                after_revision = len(load_events(events_path))
                changed = after_revision != before_revision
            except (OSError, ValueError):
                changed = events_path.exists() and events_path.stat().st_size > 0
        detail = run_path(args.run) / "failure.json"
        write_derived_json(
            detail,
            {
                "code": "INPUT_INVALID",
                "error": str(error),
                "revision": {"before": before_revision, "after": after_revision},
            },
        )
        return emit(
            False,
            operation=args.command,
            code="INPUT_INVALID",
            effect_started=changed,
            changed=changed,
            detail=str(detail),
        )


if __name__ == "__main__":
    raise SystemExit(main())
