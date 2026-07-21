"""Record, validate, derive, and render a parallel-implement campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
EVENT_TYPES = {
    "scope",
    "scope-change",
    "resume",
    "reconcile",
    "frontier",
    "serial-frontier",
    "parallel-frontier",
    "lane-create",
    "lane-preflight",
    "lane-stall",
    "lane-recovery",
    "lane-cleanup",
    "integrator-ready",
    "dispatch",
    "handoff",
    "accept",
    "reject",
    "stale-base",
    "conflict",
    "land",
    "integration-regression",
    "integration-correction",
    "feedback",
    "wave-validation",
    "graph-drained",
    "review-ready",
    "review-target",
    "review-invocation",
    "review-decision",
    "repair-plan",
    "repair-complete",
    "closeout-head",
    "child-closeout",
    "parent-closeout",
    "tracker-lock",
    "push",
    "checkpoint",
    "release",
    "friction",
}
INTENTS = {
    "dispatch",
    "land",
    "correct-integration",
    "review",
    "repair",
    "lock",
    "push",
    "checkpoint",
    "complete",
}
SAFE_LANE_STATES = {
    "removed",
    "provider-preserved",
    "unregistered-residual-directory",
}
ACCEPTED_REVIEWS = {"pass", "pass with residual risk"}
LEGACY_REVIEW_DECISIONS = {"pass-with-residual-risk": "pass with residual risk"}
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
}
FRONTIER_REASONS = {
    "serial-default",
    "serial-tripwire",
    "serial-backpressure",
    "parallel-independent",
    "widen-after-clean-wave",
    "downshift-correctness",
    "downshift-overlap",
    "downshift-stale",
    "downshift-contention",
    "downshift-backpressure",
    "serial-after-downshift",
    "reset-after-external-change",
}
PROOF_LEVELS = {"slice", "wave", "candidate", "correction", "repair"}
PROOF_FIELDS = {
    "level",
    "command_identity",
    "exit_code",
    "duration_seconds",
    "counts",
    "environment_identity",
    "log_digest",
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


def event_path(
    value: str,
    *,
    require_absolute: bool = False,
    require_existing: bool = False,
) -> Path:
    supplied = Path(value)
    if require_absolute and not supplied.is_absolute():
        raise ValueError(f"event stream path must be absolute: {value}")
    path = supplied.resolve()
    if path.suffix.lower() != ".jsonl":
        raise ValueError("event stream must use a .jsonl path")
    if require_existing and not path.is_file():
        raise ValueError(f"event stream does not exist: {path}")
    return path


def absolute_file_path(
    value: str,
    *,
    label: str,
    require_existing: bool = False,
) -> Path:
    supplied = Path(value)
    if not supplied.is_absolute():
        raise ValueError(f"{label} path must be absolute: {value}")
    path = supplied.resolve()
    if require_existing and not path.is_file():
        raise ValueError(f"{label} does not exist: {path}")
    return path


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
        os.write(descriptor, encoded)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def input_event(args: argparse.Namespace) -> dict[str, Any]:
    if args.stdin:
        value = json.loads(sys.stdin.read())
        if not isinstance(value, dict):
            raise ValueError("stdin must contain one JSON object")
        return value
    extra = json.loads(args.data_json) if args.data_json else {}
    return {
        "event": args.event,
        "event_id": args.event_id,
        "work_item": args.work_item,
        "worker_sha": args.worker_sha,
        "integration_sha": args.integration_sha,
        "validation": args.validation,
        "decision": args.decision,
        "risk": args.risk,
        "data": extra,
    }


def append(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    with stream_lock(path):
        prior = load_events(path)
        validate_events(prior)
        event = normalize_event(input_event(args))
        validate_events([*prior, event])
        append_encoded(path, [event])
    return emit(True, operation="append", events=str(path), event=event)


def read_batch(args: argparse.Namespace) -> list[dict[str, Any]]:
    raw = (
        Path(args.from_file).read_text(encoding="utf-8")
        if args.from_file
        else sys.stdin.read()
    )
    value = json.loads(raw)
    if not isinstance(value, list) or not value:
        raise ValueError("batch input must be a non-empty JSON array")
    return [normalize_event(event) for event in value]


def append_batch(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    with stream_lock(path):
        prior = load_events(path)
        validate_events(prior)
        events = read_batch(args)
        validate_events([*prior, *events])
        append_encoded(path, events)
    return emit(True, operation="append-batch", events=str(path), count=len(events))


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
) -> tuple[int, int, list[dict[str, Any]]]:
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
    return len(appended), replayed, prospective


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


def proof_evidence_errors(value: Any, *, expected_level: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{expected_level} proof evidence must be an object"]
    errors: list[str] = []
    missing = sorted(field for field in PROOF_FIELDS if field not in value)
    if missing:
        errors.append(f"{expected_level} proof evidence missing: {', '.join(missing)}")
    level = value.get("level")
    if level != expected_level or level not in PROOF_LEVELS:
        errors.append(f"{expected_level} proof evidence has invalid level")
    if not isinstance(value.get("command_identity"), str) or not value.get(
        "command_identity", ""
    ).strip():
        errors.append(f"{expected_level} proof evidence requires command_identity")
    exit_code = value.get("exit_code")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        errors.append(f"{expected_level} proof evidence requires integer exit_code")
    duration = value.get("duration_seconds")
    if (
        not isinstance(duration, (int, float))
        or isinstance(duration, bool)
        or duration < 0
    ):
        errors.append(f"{expected_level} proof evidence requires nonnegative duration_seconds")
    if not isinstance(value.get("counts"), dict):
        errors.append(f"{expected_level} proof evidence requires counts")
    for field in ("environment_identity", "log_digest"):
        if not isinstance(value.get(field), str) or not value.get(field, "").strip():
            errors.append(f"{expected_level} proof evidence requires {field}")
    if isinstance(exit_code, int) and exit_code != 0:
        excerpt = value.get("failure_excerpt")
        if not isinstance(excerpt, str) or not excerpt.strip():
            errors.append(
                f"{expected_level} failed proof evidence requires failure_excerpt"
            )
        elif len(excerpt) > 2000:
            errors.append(f"{expected_level} proof failure_excerpt exceeds 2000 characters")
    return errors


def receipt_payload(
    state: dict[str, Any],
    *,
    event_id: str,
    event_number: int,
    intent: str,
    state_event_count: int,
) -> dict[str, Any]:
    requested_errors = intent_errors(state, intent)
    regression = state.get("integration_regression") or {}
    correction_authorization = None
    if intent == "correct-integration" and regression:
        correction_authorization = {
            "regression_event_id": regression.get("event_id"),
            "prior_integration_sha": regression.get("integration_sha"),
            "route": regression.get("route"),
            "owner": regression.get("owner"),
            "write_scope": regression.get("write_scope"),
            "write_scope_ids": regression.get("write_scope_ids"),
            "required_proof": regression.get("required_proof"),
        }
    authorized = [
        candidate
        for candidate in sorted(INTENTS)
        if not intent_errors(state, candidate)
    ]
    return {
        "operation": "append-receipt",
        "committed": True,
        "event_id": event_id,
        "event_number": event_number,
        "state_event_count": state_event_count,
        "receipt_fresh": event_number == state_event_count,
        "requested_intent": {"name": intent, "allowed": not requested_errors},
        "correction_authorization": correction_authorization,
        "authorized_intents": authorized,
        "next_actions": next_actions(requested_errors, intent),
        "counters": {
            "repairs_used": state["repair_generation"],
            "repairs_remaining": max(
                0, state["repair_generation_budget"] - state["repair_generation"]
            ),
            "reviews_used": state["review_invocations_used"],
            "reviews_remaining": max(
                0,
                state["review_invocation_budget"]
                - state["review_invocations_used"],
            ),
            "reviews_required_remaining": max(
                0,
                state["review_invocations_required"]
                - state["review_invocations_completed"],
            ),
        },
        "candidate_sha": state["integration_head"],
        "reviewed_sha": state["review_target"],
        "released_sha": (
            state["closeout_head"] if state["release_outcome"] else None
        ),
    }


def append_receipt(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    raw = input_event(args)
    supplied_id = raw.get("event_id")
    if supplied_id and supplied_id != args.event_id:
        return emit(
            False,
            operation="append-receipt",
            committed=False,
            event_id=args.event_id,
            error="stdin event_id differs from --event-id",
        )
    raw["event_id"] = args.event_id
    if args.intent == "checkpoint" and not args.repo:
        return emit(
            False,
            operation="append-receipt",
            committed=False,
            event_id=args.event_id,
            error="checkpoint receipt requires repository-backed Git evidence",
            errors=["checkpoint receipt requires repository-backed Git evidence"],
        )

    with stream_lock(path):
        prior = load_events(path)
        validate_events(prior)
        existing_number = next(
            (
                number
                for number, event in enumerate(prior, 1)
                if event["event_id"] == args.event_id
            ),
            None,
        )
        if existing_number is not None:
            existing = prior[existing_number - 1]
            if "timestamp" not in raw:
                raw["timestamp"] = existing["timestamp"]
            candidate = normalize_event(raw)
            if semantic_event(candidate) != semantic_event(existing):
                return emit(
                    False,
                    operation="append-receipt",
                    committed=False,
                    event_id=args.event_id,
                    event_number=existing_number,
                    error="event_id already exists with a different payload",
                )
            stored = existing.get("receipt")
            if isinstance(stored, dict) and existing_number == len(prior):
                return emit(True, **stored)
            state = derive_state(prior, args.repo)
            if state["errors"]:
                return emit(
                    False,
                    operation="append-receipt",
                    committed=False,
                    event_id=args.event_id,
                    error="existing event prefix is semantically invalid",
                    errors=state["errors"],
                )
            receipt = receipt_payload(
                state,
                event_id=args.event_id,
                event_number=existing_number,
                intent=args.intent,
                state_event_count=len(prior),
            )
            return emit(True, **receipt)

        event = normalize_event(raw)
        prospective = [*prior, event]
        validate_events(prospective)
        state = derive_state(prospective, args.repo)
        if state["errors"]:
            return emit(
                False,
                operation="append-receipt",
                committed=False,
                event_id=args.event_id,
                error="prospective event is semantically invalid",
                errors=state["errors"],
            )
        receipt = receipt_payload(
            state,
            event_id=args.event_id,
            event_number=len(prospective),
            intent=args.intent,
            state_event_count=len(prospective),
        )
        event["receipt"] = receipt
        append_encoded(path, [event])
    return emit(True, **receipt)


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


def git_common_dir(repo: str) -> str:
    resolved_repo = Path(repo).resolve()
    result = subprocess.run(
        ["git", "-C", str(resolved_repo), "rev-parse", "--git-common-dir"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or "cannot resolve Git common directory")
    value = Path(result.stdout.strip())
    return str((value if value.is_absolute() else resolved_repo / value).resolve())


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
    errors: list[str] = []
    children: list[str] = []
    push_required = False
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
    pushed_head: str | None = None
    checkpoint_outcome: str | None = None
    checkpoint_data: dict[str, Any] | None = None
    checkpoint_active = False
    checkpoint_resume_pending = False
    release_outcome: str | None = None
    resume_pending = False
    tracker_locked = False
    release_seen = False
    charter_id: str | None = None
    runtime_contract = 1
    repair_generation_budget = 4
    review_invocation_budget = 5
    review_invocations_required = 1
    review_invocations_used = 0
    review_invocations_completed = 0
    repair_generation = 0
    repair_completed_generation = 0
    repair_open = False
    repair_base: str | None = None
    repair_findings: list[str] = []
    review_findings: list[dict[str, Any]] = []
    review_decision_id: str | None = None
    review_invocation_id: str | None = None
    review_mode: str | None = None
    review_invocation_canonical = False
    review_invocation_ids: set[str] = set()
    friction_observations: dict[str, dict[str, Any]] = {}
    friction_synthesis: dict[str, Any] | None = None
    integration_regression: dict[str, Any] | None = None
    latest_integration_correction: str | None = None
    integration_checkout: dict[str, Any] | None = None
    frontier_width = 1
    peak_authorized_width = 1
    frontier_reason = "serial-default"
    selected_frontier: list[str] = []
    frontier_recorded = False
    last_wave_clean = False
    serial_latch: dict[str, Any] | None = None
    latch_just_reset = False
    downshift_required: str | None = None
    downshift_last_cause: dict[str, Any] | None = None
    downshift_last_release: dict[str, Any] | None = None
    proof_records: list[dict[str, Any]] = []

    def item_state(item: str) -> dict[str, Any]:
        return items.setdefault(item, {})

    def need(condition: bool, message: str) -> bool:
        if not condition:
            errors.append(message)
        return condition

    def record_proof(value: Any, *, expected_level: str, prefix: str) -> bool:
        proof_errors = proof_evidence_errors(value, expected_level=expected_level)
        for proof_error in proof_errors:
            errors.append(f"{prefix} {proof_error}")
        if proof_errors:
            return False
        proof_records.append(dict(value))
        return True

    for number, event in enumerate(events, 1):
        kind = event["event"]
        item = event["work_item"]
        data = event["data"]
        prefix = f"event {number} {kind} for {item}"
        state = item_state(item)

        if release_seen and kind != "friction":
            errors.append(f"{prefix} occurs after release")
        if checkpoint_active and kind not in {"friction", "resume"}:
            errors.append(f"{prefix} occurs before checkpoint resume")
        if checkpoint_resume_pending and kind not in {"friction", "reconcile"}:
            errors.append(f"{prefix} occurs before checkpoint reconciliation")

        if kind in {"scope", "scope-change"}:
            visible = data.get("children")
            if kind == "scope":
                need(
                    isinstance(visible, list)
                    and all(isinstance(child, str) and child for child in visible),
                    f"{prefix} requires data.children",
                )
            elif visible is not None:
                need(
                    isinstance(visible, list)
                    and all(isinstance(child, str) and child for child in visible),
                    f"{prefix} data.children must be a list of IDs",
                )
            if isinstance(visible, list) and all(
                isinstance(child, str) and child for child in visible
            ):
                children = list(dict.fromkeys(visible))
                dispositions = data.get("dispositions", {})
                if isinstance(dispositions, dict):
                    for child, disposition in dispositions.items():
                        if child in children and disposition:
                            item_state(child)["disposition"] = disposition
            push_required = bool(data.get("push_required", push_required))
            checkout = data.get("integration_checkout")
            if checkout is not None:
                valid_checkout = need(
                    isinstance(checkout, dict),
                    f"{prefix} integration_checkout must be an object",
                )
                if isinstance(checkout, dict):
                    mode = checkout.get("mode")
                    valid_checkout &= need(
                        mode in {"existing-checkout", "managed-integration-worktree"},
                        f"{prefix} integration checkout has invalid mode",
                    )
                    valid_checkout &= need(
                        all(
                            isinstance(checkout.get(field), str)
                            and bool(checkout[field])
                            for field in ("path", "git_common_dir", "starting_head")
                        ),
                        f"{prefix} integration checkout lacks identity",
                    )
                    expected_authority = (
                        "none" if mode == "existing-checkout" else "managed"
                    )
                    valid_checkout &= need(
                        checkout.get("cleanup_authority") == expected_authority,
                        f"{prefix} integration checkout cleanup authority differs from mode",
                    )
                    if valid_checkout:
                        if integration_checkout is not None:
                            need(
                                checkout == integration_checkout,
                                f"{prefix} changes integration checkout ownership",
                            )
                        else:
                            integration_checkout = dict(checkout)
            charter = data.get("charter")
            if isinstance(charter, dict):
                candidate_id = charter.get("id")
                if need(isinstance(candidate_id, str) and bool(candidate_id), f"{prefix} data.charter requires id"):
                    if charter_id:
                        need(candidate_id == charter_id, f"{prefix} changes the campaign Charter")
                    else:
                        charter_id = candidate_id
                candidate_contract = charter.get("runtime_contract", runtime_contract)
                if need(
                    isinstance(candidate_contract, int)
                    and candidate_contract in {1, 2, 3},
                    f"{prefix} Charter runtime_contract must be 1, 2, or 3",
                ):
                    if kind == "scope-change":
                        need(
                            candidate_contract >= runtime_contract,
                            f"{prefix} cannot lower runtime_contract",
                        )
                    runtime_contract = max(runtime_contract, candidate_contract)

                legacy_repair = charter.get("repair_budget")
                canonical_repair = charter.get("repair_generation_budget")
                if legacy_repair is not None and canonical_repair is not None:
                    need(
                        legacy_repair == canonical_repair,
                        f"{prefix} has conflicting repair budget aliases",
                    )
                candidate_repair = (
                    canonical_repair
                    if canonical_repair is not None
                    else legacy_repair
                    if legacy_repair is not None
                    else repair_generation_budget
                )
                candidate_review_budget = charter.get(
                    "review_invocation_budget",
                    candidate_repair + 1
                    if kind == "scope"
                    else review_invocation_budget,
                )
                candidate_required = charter.get(
                    "review_invocations_required", review_invocations_required
                )
                budget_values_valid = True
                budget_values_valid &= need(
                    isinstance(candidate_repair, int) and candidate_repair >= 0,
                    f"{prefix} Charter repair_generation_budget must be a nonnegative integer",
                )
                budget_values_valid &= need(
                    isinstance(candidate_review_budget, int)
                    and candidate_review_budget > 0,
                    f"{prefix} Charter review_invocation_budget must be a positive integer",
                )
                budget_values_valid &= need(
                    isinstance(candidate_required, int) and candidate_required > 0,
                    f"{prefix} Charter review_invocations_required must be a positive integer",
                )
                if budget_values_valid:
                    need(
                        candidate_review_budget >= candidate_required,
                        f"{prefix} review budget is below required invocations",
                    )
                    if kind == "scope-change" and any(
                        key in charter
                        for key in {
                            "repair_budget",
                            "repair_generation_budget",
                            "review_invocation_budget",
                            "review_invocations_required",
                        }
                    ):
                        change = data.get("budget_change")
                        valid_change = need(
                            isinstance(change, dict),
                            f"{prefix} budget changes require data.budget_change",
                        )
                        if isinstance(change, dict):
                            valid_change &= need(
                                bool(change.get("source")),
                                f"{prefix} budget change requires caller source",
                            )
                            valid_change &= need(
                                bool(change.get("reason")),
                                f"{prefix} budget change requires reason",
                            )
                            prior = change.get("prior")
                            expected_prior = {
                                "repair_generation_budget": repair_generation_budget,
                                "review_invocation_budget": review_invocation_budget,
                                "review_invocations_required": review_invocations_required,
                            }
                            valid_change &= need(
                                prior == expected_prior,
                                f"{prefix} budget change prior values do not match state",
                            )
                        valid_change &= need(
                            candidate_repair >= repair_generation,
                            f"{prefix} repair budget is below consumed generations",
                        )
                        valid_change &= need(
                            candidate_review_budget >= review_invocations_used,
                            f"{prefix} review budget is below consumed invocations",
                        )
                        valid_change &= need(
                            candidate_review_budget >= candidate_required,
                            f"{prefix} review budget is below required invocations",
                        )
                        valid_change &= need(
                            candidate_required >= review_invocations_required,
                            f"{prefix} cannot lower required review invocations",
                        )
                        budget_values_valid &= valid_change
                    if budget_values_valid:
                        repair_generation_budget = candidate_repair
                        review_invocation_budget = candidate_review_budget
                        review_invocations_required = candidate_required
        elif kind == "resume":
            if checkpoint_active:
                checkpoint_active = False
                checkpoint_resume_pending = True
            resume_pending = True
        elif kind == "reconcile":
            required = {
                "git",
                "worktrees",
                "agents",
                "tracker",
                "claims",
                "remote",
                "integration_checkout",
            }
            missing = sorted(field for field in required if field not in data)
            need(not missing, f"{prefix} missing reconciliation evidence: {', '.join(missing)}")
            resume_pending = bool(missing)
            checkpoint_resume_pending = bool(missing)
        elif kind == "frontier" and runtime_contract >= 3 and (
            "width" in data or "reason" in data
        ):
            width = data.get("width")
            reason = data.get("reason")
            selected = data.get("selected")
            valid = True
            valid &= need(
                isinstance(width, int) and not isinstance(width, bool) and 1 <= width <= 5,
                f"{prefix} width must be between 1 and 5",
            )
            valid &= need(
                reason in FRONTIER_REASONS,
                f"{prefix} has invalid frontier reason",
            )
            valid &= need(
                isinstance(selected, list)
                and all(isinstance(value, str) and value for value in selected),
                f"{prefix} selected frontier must be a list of work items",
            )
            if (
                isinstance(selected, list)
                and all(isinstance(value, str) and value for value in selected)
                and isinstance(width, int)
                and not isinstance(width, bool)
            ):
                valid &= need(
                    len(selected) == width and len(selected) == len(set(selected)),
                    f"{prefix} selected frontier must match width without duplicates",
                )
                valid &= need(
                    set(selected) <= set(children),
                    f"{prefix} selected frontier contains work outside campaign scope",
                )
            queued = [
                work_item
                for work_item, work_state in items.items()
                if work_state.get("handoff")
                and not work_state.get("accepted")
                and not work_state.get("rejected")
            ]
            if reason == "reset-after-external-change":
                valid &= need(serial_latch is not None, f"{prefix} requires an active serial latch")
                valid &= need(width == 1, f"{prefix} latch reset must remain width one")
                valid &= need(
                    isinstance(data.get("release_evidence"), str)
                    and bool(data["release_evidence"].strip()),
                    f"{prefix} requires serial latch release evidence",
                )
                if valid:
                    downshift_last_release = {
                        "event_id": event["event_id"],
                        "evidence": data.get("release_evidence"),
                    }
                    serial_latch = None
                    latch_just_reset = True
                    downshift_required = None
            elif isinstance(reason, str) and reason.startswith("downshift-"):
                valid &= need(width == 1, f"{prefix} Downshift must select width one")
                if valid:
                    serial_latch = {
                        "cause": reason,
                        "event_id": event["event_id"],
                    }
                    downshift_last_cause = dict(serial_latch)
                    latch_just_reset = False
                    downshift_required = None
            elif serial_latch is not None:
                valid &= need(width == 1, f"{prefix} serial latch permits only width one")
                valid &= need(
                    reason == "serial-after-downshift",
                    f"{prefix} active serial latch requires serial-after-downshift",
                )
            elif isinstance(width, int) and width > 1:
                valid &= need(not queued, f"{prefix} cannot widen with an uninspected result queue")
                for field in (
                    "substantial",
                    "semantic_independence",
                    "proof_isolated",
                    "root_capacity",
                ):
                    valid &= need(data.get(field) is True, f"{prefix} requires {field}")
                if not frontier_recorded:
                    valid &= need(
                        width == 2 and data.get("cold_start") is True,
                        f"{prefix} cold start may open only two proved-independent lanes",
                    )
                    valid &= need(
                        reason == "parallel-independent",
                        f"{prefix} cold start requires parallel-independent",
                    )
                elif latch_just_reset:
                    valid &= need(width == 2, f"{prefix} reset may reopen only at width two")
                    valid &= need(
                        reason == "parallel-independent",
                        f"{prefix} reset reopening requires parallel-independent",
                    )
                elif width > frontier_width:
                    valid &= need(
                        width == frontier_width + 1,
                        f"{prefix} width may increase by only one",
                    )
                    valid &= need(last_wave_clean, f"{prefix} widening requires a clean prior wave")
                    valid &= need(
                        reason == "widen-after-clean-wave",
                        f"{prefix} widening requires widen-after-clean-wave",
                    )
                else:
                    valid &= need(
                        width == frontier_width,
                        f"{prefix} parallel width may hold or increase by one",
                    )
                    valid &= need(
                        reason == "parallel-independent",
                        f"{prefix} held parallel width requires parallel-independent",
                    )
            elif reason in {"parallel-independent", "widen-after-clean-wave"}:
                valid &= need(False, f"{prefix} parallel reason requires width above one")
            if valid:
                frontier_width = int(width)
                peak_authorized_width = max(peak_authorized_width, frontier_width)
                frontier_reason = str(reason)
                selected_frontier = list(selected)
                frontier_recorded = True
                last_wave_clean = False
                if reason != "reset-after-external-change":
                    latch_just_reset = False
        elif kind == "lane-create":
            lane_id = data.get("lane_id")
            if need(isinstance(lane_id, str) and bool(lane_id), f"{prefix} requires data.lane_id"):
                if data.get("role") == "integration":
                    need(
                        integration_checkout is not None
                        and integration_checkout.get("mode")
                        == "managed-integration-worktree",
                        f"{prefix} integration lane requires managed integration checkout ownership",
                    )
                    if integration_checkout and data.get("worktree"):
                        need(
                            str(Path(data["worktree"]).resolve())
                            == str(Path(integration_checkout["path"]).resolve()),
                            f"{prefix} integration lane path differs from campaign checkout",
                        )
                lanes[lane_id] = {"work_item": item, "state": "created", **data}
                state["lane_id"] = lane_id
        elif kind == "lane-preflight":
            lane_id = data.get("lane_id")
            if need(lane_id in lanes, f"{prefix} requires lane-create"):
                lanes[lane_id].update(data)
                lanes[lane_id]["state"] = "ready"
                state["preflight"] = True
        elif kind == "dispatch":
            valid = need(
                not resume_pending,
                f"{prefix} requires reconciliation after resume",
            )
            lane_id = data.get("lane_id") or state.get("lane_id")
            valid &= need(
                bool(state.get("preflight")) and lane_id in lanes,
                f"{prefix} requires lane-preflight",
            )
            if runtime_contract >= 3:
                repair_dispatch = repair_open and item not in children
                valid &= need(
                    frontier_recorded or repair_dispatch,
                    f"{prefix} requires a recorded selected frontier",
                )
                valid &= need(
                    item in selected_frontier or repair_dispatch,
                    f"{prefix} work item is outside the selected frontier",
                )
                if repair_dispatch:
                    valid &= need(
                        frontier_width == 1,
                        f"{prefix} Repair dispatch must remain serial",
                    )
                valid &= need(
                    not state.get("dispatched"),
                    f"{prefix} work item is already dispatched",
                )
                pending_results = [
                    work_item
                    for work_item, work_state in items.items()
                    if work_state.get("handoff")
                    and not work_state.get("accepted")
                    and not work_state.get("rejected")
                ]
                accepted_unlanded = [
                    work_item
                    for work_item, work_state in items.items()
                    if work_state.get("accepted") and not work_state.get("landed")
                ]
                active = [
                    work_item
                    for work_item, work_state in items.items()
                    if work_state.get("dispatched")
                    and not work_state.get("handoff")
                    and not work_state.get("accepted")
                    and not work_state.get("rejected")
                    and not work_state.get("landed")
                ]
                valid &= need(
                    not pending_results,
                    f"{prefix} cannot open behind an uninspected result queue",
                )
                valid &= need(
                    not accepted_unlanded,
                    f"{prefix} cannot open behind accepted unlanded work",
                )
                valid &= need(
                    len(active) < frontier_width,
                    f"{prefix} exceeds authorized frontier width {frontier_width}",
                )
                valid &= need(
                    downshift_required is None,
                    f"{prefix} requires Downshift before dispatch",
                )
            if valid:
                state["dispatched"] = True
                lanes[lane_id]["state"] = "active"
        elif kind == "handoff":
            if runtime_contract >= 3 and data.get("status") == "done":
                record_proof(data.get("proof"), expected_level="slice", prefix=prefix)
            state["handoff"] = data
        elif kind in {"stale-base", "conflict"}:
            need(bool(state.get("dispatched")), f"{prefix} requires dispatch")
            need(bool(state.get("handoff")), f"{prefix} requires a returned packet")
            state[kind.replace("-", "_")] = data
            state["rejected"] = True
            last_wave_clean = False
            downshift_required = (
                "downshift-stale" if kind == "stale-base" else "downshift-overlap"
            )
        elif kind == "wave-validation" and runtime_contract >= 3 and "outcome" in data:
            outcome = data.get("outcome")
            valid = need(
                outcome in {"pass", "fail"},
                f"{prefix} wave outcome must be pass or fail",
            )
            valid &= need(bool(event.get("validation")), f"{prefix} requires wave proof")
            valid &= record_proof(
                data.get("proof"), expected_level="wave", prefix=prefix
            )
            if integration_head:
                valid &= need(
                    event.get("integration_sha") == integration_head,
                    f"{prefix} HEAD differs from integration HEAD",
                )
            if valid:
                last_wave_clean = outcome == "pass"
                if outcome == "fail":
                    downshift_required = "downshift-correctness"
        elif kind == "accept":
            need(bool(state.get("dispatched")), f"{prefix}: accept requires dispatch")
            need(bool(event.get("worker_sha")), f"{prefix} requires worker_sha")
            state["accepted"] = event.get("worker_sha")
        elif kind == "reject":
            need(bool(state.get("dispatched")), f"{prefix}: reject requires dispatch")
            state["rejected"] = True
        elif kind == "land":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(bool(state.get("accepted")), f"{prefix}: land requires acceptance")
            need(bool(event.get("worker_sha")), f"{prefix} requires worker_sha")
            need(bool(event.get("integration_sha")), f"{prefix} requires integration_sha")
            if state.get("accepted") and event.get("worker_sha"):
                need(
                    state["accepted"] == event["worker_sha"],
                    f"{prefix} worker SHA differs from acceptance",
                )
            state["landed"] = event.get("integration_sha")
            integration_head = event.get("integration_sha") or integration_head
            last_wave_clean = False
            lane_id = state.get("lane_id")
            if lane_id in lanes:
                lanes[lane_id]["state"] = "landed"
        elif kind == "integration-regression":
            route = data.get("route")
            write_scope_ids, write_scope_error = scope_identifiers(data.get("write_scope"))
            need(runtime_contract >= 3, f"{prefix} requires runtime contract 3")
            need(bool(integration_head), f"{prefix} requires an integrated HEAD")
            need(
                event.get("integration_sha") == integration_head,
                f"{prefix} HEAD differs from integration HEAD",
            )
            need(
                review_invocations_used == 0,
                f"{prefix} is only valid before formal review",
            )
            need(integration_regression is None, f"{prefix} duplicates an open integration regression")
            need(bool(data.get("red")), f"{prefix} requires a trusted RED")
            need(
                route in {"original-worker", "fresh-lane", "root-tiny"},
                f"{prefix} has invalid correction route",
            )
            need(
                isinstance(data.get("owner"), str) and bool(data["owner"].strip()),
                f"{prefix} requires an owner",
            )
            need(not write_scope_error, f"{prefix} write scope {write_scope_error}")
            need(bool(data.get("required_proof")), f"{prefix} requires regression proof")
            if route == "root-tiny":
                need(
                    data.get("root_authorized") is True,
                    f"{prefix} tiny root correction requires explicit authorization",
                )
            integration_regression = {
                **data,
                "event_id": event["event_id"],
                "integration_sha": integration_head,
                "write_scope_ids": write_scope_ids,
            }
            graph_drained = False
            review_ready = False
            last_wave_clean = False
            downshift_required = "downshift-correctness"
        elif kind == "integration-correction":
            regression = integration_regression or {}
            route = data.get("route")
            corrected_head = event.get("integration_sha")
            actor_id = data.get("actor_id")
            changed_scope_ids, changed_scope_error = scope_identifiers(data.get("changed_scope"))
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
            need(
                data.get("correction_commit") == corrected_head,
                f"{prefix} correction commit differs from successor HEAD",
            )
            need(not changed_scope_error, f"{prefix} changed scope {changed_scope_error}")
            if not changed_scope_error:
                authorized_scope_ids = set(regression.get("write_scope_ids") or [])
                need(
                    set(changed_scope_ids) <= authorized_scope_ids,
                    f"{prefix} changed scope exceeds authorization",
                )
            need(bool(event.get("validation")), f"{prefix} requires correction proof")
            if runtime_contract >= 3:
                record_proof(
                    data.get("proof"), expected_level="correction", prefix=prefix
                )
            if route in {"original-worker", "fresh-lane"}:
                lane_id = data.get("lane_id")
                worker_sha = data.get("worker_sha")
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
            need(bool(children), f"{prefix} requires an exhaustive scope")
            unfinished = [child for child in children if not item_state(child).get("landed") and not item_state(child).get("disposition")]
            need(not unfinished, f"{prefix} has unfinished children: {', '.join(unfinished)}")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            if runtime_contract >= 3:
                need(last_wave_clean, f"{prefix} requires passing current wave proof")
            graph_drained = True
        elif kind == "review-ready":
            need(graph_drained, f"{prefix} requires graph-drained")
            need(not repair_open, f"{prefix} requires completed Repair")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            if runtime_contract >= 3:
                need(
                    bool(event.get("validation")),
                    f"{prefix} requires current candidate proof",
                )
                record_proof(
                    data.get("proof"), expected_level="candidate", prefix=prefix
                )
            need(
                repair_generation == repair_completed_generation,
                f"{prefix} latest Repair generation lacks completion proof",
            )
            review_ready = True
        elif kind == "review-target":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(review_ready, f"{prefix} requires review-ready")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            need(
                review_invocations_used < review_invocation_budget,
                f"{prefix} exceeds review invocation budget",
            )
            legacy_mode = "initial" if repair_generation == 0 else "remediation"
            if legacy_mode == "remediation" and review_target:
                need(
                    repair_completed_generation == repair_generation,
                    f"{prefix} successor Review requires Repair proof",
                )
                need(
                    repair_base == review_target,
                    f"{prefix} Repair base differs from prior review target",
                )
                need(
                    integration_head != review_target,
                    f"{prefix} successor Review requires a new HEAD",
                )
            review_invocation_id = event["event_id"]
            review_mode = legacy_mode
            review_invocation_canonical = False
            review_invocation_ids.add(review_invocation_id)
            review_invocations_used += 1
            review_target = event.get("integration_sha")
            review_ready = False
            review_decision = None
            review_decision_id = None
            review_findings = []
        elif kind == "review-invocation":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            invocation_id = event["event_id"]
            mode = data.get("mode")
            target = event.get("integration_sha")
            valid = True
            valid &= need(
                invocation_id not in review_invocation_ids,
                f"{prefix} duplicates review invocation identity",
            )
            valid &= need(
                mode in {"initial", "remediation", "assurance"},
                f"{prefix} has invalid review mode",
            )
            reason = data.get("reason")
            valid &= need(
                isinstance(reason, str) and bool(reason.strip()),
                f"{prefix} requires a reason",
            )
            valid &= need(
                target == integration_head,
                f"{prefix} HEAD differs from integration HEAD",
            )
            valid &= need(
                review_invocations_used < review_invocation_budget,
                f"{prefix} exceeds review invocation budget",
            )
            if review_invocation_id is None:
                valid &= need(
                    review_ready and mode == "initial",
                    f"{prefix} first invocation must be initial and review-ready",
                )
            elif review_decision == "incomplete":
                valid &= need(
                    target == review_target and mode == review_mode,
                    f"{prefix} incomplete retry must keep target and mode",
                )
            elif mode == "assurance":
                valid &= need(
                    review_decision in ACCEPTED_REVIEWS,
                    f"{prefix} assurance requires an accepted review",
                )
                valid &= need(
                    target == review_target,
                    f"{prefix} assurance requires the accepted immutable target",
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
                    review_ready and review_invocation_id is None,
                    f"{prefix} initial mode is only valid for the first invocation or incomplete retry",
                )
            if valid:
                review_invocation_ids.add(invocation_id)
                review_invocation_id = invocation_id
                review_mode = mode
                review_invocation_canonical = True
                review_invocations_used += 1
                review_target = target
                review_ready = False
                review_decision = None
                review_decision_id = None
                review_findings = []
        elif kind == "review-decision":
            need(bool(review_target), f"{prefix} requires a review invocation")
            need(review_decision is None, f"{prefix} duplicates a decision for the review target")
            need(event.get("integration_sha") == review_target, f"{prefix} HEAD differs from review target")
            raw_decision = event.get("decision")
            decision = LEGACY_REVIEW_DECISIONS.get(raw_decision, raw_decision)
            need(decision in ACCEPTED_REVIEWS | {"blocked", "incomplete", "fail"}, f"{prefix} has unknown decision")
            decision_invocation = data.get("review_invocation_id")
            if review_invocation_canonical:
                need(
                    decision_invocation == review_invocation_id,
                    f"{prefix} review invocation identity differs",
                )
            mode = data.get("mode", review_mode)
            need(mode == review_mode, f"{prefix} review mode differs from invocation")
            findings = data.get("findings", [])
            need(isinstance(findings, list) and all(isinstance(finding, dict) for finding in findings), f"{prefix} data.findings must be a list of objects")
            review_decision = decision
            review_decision_id = event.get("event_id")
            review_findings = findings if isinstance(findings, list) else []
            if decision != "incomplete":
                review_invocations_completed += 1
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
            need(
                review_invocations_used < review_invocation_budget,
                f"{prefix} requires one remaining successor review invocation",
            )
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
            need(repair_open, f"{prefix} requires an open Repair generation")
            need(data.get("generation") == repair_generation, f"{prefix} Repair generation differs from plan")
            need(set(data.get("finding_ids", [])) == set(repair_findings), f"{prefix} finding IDs differ from plan")
            need(bool(event.get("validation")), f"{prefix} requires Repair proof")
            if runtime_contract >= 3:
                record_proof(
                    data.get("proof"), expected_level="repair", prefix=prefix
                )
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            repair_open = False
            repair_completed_generation = repair_generation
        elif kind == "closeout-head":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(review_decision in ACCEPTED_REVIEWS, f"{prefix} requires accepted review")
            need(
                review_invocations_completed >= review_invocations_required,
                f"{prefix} requires {review_invocations_required} completed review invocations",
            )
            need(event.get("integration_sha") == integration_head, f"{prefix} closeout HEAD differs from integration HEAD")
            need(event.get("integration_sha") == review_target, f"{prefix} closeout HEAD differs from review target")
            closeout_head = event.get("integration_sha")
        elif kind == "child-closeout":
            need(bool(state.get("landed") or state.get("disposition")), f"{prefix} requires landed or disposed child")
            if state.get("landed"):
                need(event.get("integration_sha") == state["landed"], f"{prefix} integration SHA differs from landed SHA")
            closeout_state = data.get("state")
            need(closeout_state in {"draft", "review-final", "posted", "verified"}, f"{prefix} has invalid state")
            if closeout_state == "verified":
                missing = sorted(field for field in CLOSEOUT_FIELDS if not data.get(field))
                need(not missing, f"{prefix} verified packet missing: {', '.join(missing)}")
                need(data.get("reviewed_head") == closeout_head, f"{prefix} reviewed HEAD differs from closeout HEAD")
            child_closeouts[item] = data
        elif kind == "parent-closeout":
            missing = [child for child in children if child_closeouts.get(child, {}).get("state") != "verified"]
            need(not missing, f"{prefix} requires verified child closeout: {', '.join(missing)}")
            need(data.get("state") == "verified", f"{prefix} requires verified state")
            need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
            parent_closeout = data
        elif kind == "push":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            need(bool(closeout_head), f"{prefix} requires closeout-head")
            need(event.get("integration_sha") == closeout_head, f"{prefix} pushed HEAD differs from closeout HEAD")
            pushed_head = event.get("integration_sha")
        elif kind == "lane-cleanup":
            lane_id = data.get("lane_id") or state.get("lane_id")
            if need(lane_id in lanes, f"{prefix} requires known data.lane_id"):
                lanes[lane_id].update(data)
                lanes[lane_id]["state"] = data.get("state")
                if (
                    lanes[lane_id].get("role") == "integration"
                    and integration_checkout is not None
                ):
                    integration_checkout = {
                        **integration_checkout,
                        "final_disposition": data.get("state"),
                        "registered_after": data.get("registered_after"),
                        "directory_exists": data.get("directory_exists"),
                        "intentionally_preserved": data.get(
                            "intentionally_preserved", False
                        ),
                    }
        elif kind == "tracker-lock":
            need(bool(parent_closeout), f"{prefix} requires verified parent closeout")
            need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
            tracker_locked = True
        elif kind == "friction":
            friction_kind = data.get("kind")
            if friction_kind == "observation":
                need(
                    friction_synthesis is None,
                    f"{prefix} observation occurs after friction synthesis",
                )
                required = {"surface", "source", "evidence", "impact", "suggestion"}
                missing = sorted(field for field in required if not data.get(field))
                if need(
                    not missing,
                    f"{prefix} observation missing: {', '.join(missing)}",
                ):
                    friction_observations[event["event_id"]] = data
            elif friction_kind == "synthesis":
                need(
                    friction_synthesis is None,
                    f"{prefix} duplicates friction synthesis",
                )
                observation_ids = data.get("observations")
                themes = data.get("deduplicated_themes")
                none_observed = data.get("none_observed")
                valid_synthesis = True
                valid_synthesis &= need(
                    isinstance(observation_ids, list)
                    and all(isinstance(value, str) and value for value in observation_ids),
                    f"{prefix} synthesis observations must be IDs",
                )
                valid_synthesis &= need(
                    isinstance(themes, list)
                    and all(isinstance(value, str) and value for value in themes),
                    f"{prefix} synthesis themes must be strings",
                )
                valid_synthesis &= need(
                    isinstance(none_observed, bool),
                    f"{prefix} synthesis requires none_observed",
                )
                if isinstance(observation_ids, list):
                    valid_synthesis &= need(
                        set(observation_ids) == set(friction_observations),
                        f"{prefix} synthesis must reference every friction observation exactly once",
                    )
                    valid_synthesis &= need(
                        len(observation_ids) == len(set(observation_ids)),
                        f"{prefix} synthesis duplicates an observation ID",
                    )
                if none_observed is True:
                    valid_synthesis &= need(
                        not friction_observations and not observation_ids and not themes,
                        f"{prefix} none_observed conflicts with recorded friction",
                    )
                else:
                    valid_synthesis &= need(
                        bool(friction_observations),
                        f"{prefix} synthesis requires observations or none_observed true",
                    )
                if valid_synthesis:
                    friction_synthesis = data
            else:
                need(False, f"{prefix} friction kind must be observation or synthesis")
        elif kind == "checkpoint":
            decision = event.get("decision")
            required = {
                "reason",
                "continuation",
                "current_head",
                "actors",
                "lanes",
                "integration_state",
                "integration_checkout",
                "next_frontier",
                "blockers",
                "serial_latch",
                "result_queue",
                "proof_state",
                "open_work",
                "claims",
                "tracker",
                "remote",
            }
            missing = sorted(field for field in required if field not in data)
            need(runtime_contract >= 3, f"{prefix} requires runtime contract 3")
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
            need(isinstance(data.get("lanes"), dict), f"{prefix} lanes must be an object")
            checkpoint_checkout = data.get("integration_checkout")
            need(
                isinstance(checkpoint_checkout, dict)
                and checkpoint_checkout.get("mode")
                in {"existing-checkout", "managed-integration-worktree"}
                and bool(checkpoint_checkout.get("path")),
                f"{prefix} integration_checkout requires mode and path",
            )
            if integration_checkout and isinstance(checkpoint_checkout, dict):
                need(
                    checkpoint_checkout.get("mode") == integration_checkout.get("mode")
                    and checkpoint_checkout.get("path") == integration_checkout.get("path"),
                    f"{prefix} integration checkout identity differs from campaign",
                )
            need(
                isinstance(data.get("next_frontier"), list),
                f"{prefix} next_frontier must be a list",
            )
            need(
                isinstance(data.get("blockers"), list),
                f"{prefix} blockers must be a list",
            )
            need(
                data.get("serial_latch") == serial_latch,
                f"{prefix} serial_latch differs from canonical state",
            )
            queued = sorted(
                work_item
                for work_item, work_state in items.items()
                if work_state.get("handoff")
                and not work_state.get("accepted")
                and not work_state.get("rejected")
            )
            need(
                isinstance(data.get("result_queue"), list)
                and sorted(data.get("result_queue", [])) == queued,
                f"{prefix} result_queue differs from canonical state",
            )
            need(
                isinstance(data.get("proof_state"), dict),
                f"{prefix} proof_state must be an object",
            )
            open_work = data.get("open_work")
            need(
                isinstance(open_work, dict)
                and "integration_regression" in open_work
                and "repair" in open_work,
                f"{prefix} open_work must account for correction and Repair",
            )
            if isinstance(open_work, dict):
                need(
                    open_work.get("integration_regression")
                    == (
                        integration_regression.get("event_id")
                        if integration_regression
                        else None
                    ),
                    f"{prefix} open_work integration regression differs from canonical state",
                )
                need(
                    open_work.get("repair")
                    == (repair_generation if repair_open else None),
                    f"{prefix} open_work Repair differs from canonical state",
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
                        valid_claims &= need(
                            all(claim.get(field) for field in ("owner", "token", "claimed_at", "recovery_owner")),
                            f"{prefix} retained claim lacks owner or recovery evidence",
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
            need(event.get("decision") in {"complete", "partial", "blocked"}, f"{prefix} has invalid outcome")
            if runtime_contract >= 3:
                need(
                    event.get("decision") == "complete",
                    f"{prefix} runtime contract 3 reserves release for complete",
                )
            if event.get("decision") == "complete":
                need(tracker_locked, f"{prefix} requires tracker Lock")
                need(event.get("integration_sha") == closeout_head, f"{prefix} HEAD differs from closeout HEAD")
                need(not push_required or pushed_head == closeout_head, f"{prefix} requires approved push")
                unsafe = []
                for lane_id, lane in lanes.items():
                    lane_state = lane.get("state")
                    if lane_state not in SAFE_LANE_STATES or (
                        lane_state == "unregistered-residual-directory"
                        and not lane.get("intentionally_preserved")
                    ):
                        unsafe.append(f"{lane_id}:{lane_state}")
                need(not unsafe, f"{prefix} has active lanes: {', '.join(unsafe)}")
                if (
                    integration_checkout
                    and integration_checkout.get("mode")
                    == "managed-integration-worktree"
                ):
                    disposition = integration_checkout.get("final_disposition")
                    need(
                        disposition in SAFE_LANE_STATES,
                        f"{prefix} managed integration checkout lacks a safe final disposition",
                    )
                    if disposition == "unregistered-residual-directory":
                        need(
                            integration_checkout.get("intentionally_preserved") is True,
                            f"{prefix} managed integration checkout residual is not intentionally preserved",
                        )
            release_outcome = event.get("decision")
            release_seen = True

    if runtime_contract >= 2 and release_outcome == "complete" and not friction_synthesis:
        errors.append("canonical campaign requires one Workflow Friction synthesis")

    current_head = git_head(repo)
    current_clean = git_clean(repo)
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
    elif review_decision in {"blocked", "incomplete", "fail"}:
        campaign_status = "review-blocked"
    elif graph_drained:
        campaign_status = "review-ready"
    elif any(item.get("landed") for item in items.values()):
        campaign_status = "draining"
    else:
        campaign_status = "open"

    return {
        "errors": errors,
        "children": children,
        "push_required": push_required,
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
        "pushed_head": pushed_head,
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
        "runtime_contract": runtime_contract,
        "repair_generation_budget": repair_generation_budget,
        "review_invocation_budget": review_invocation_budget,
        "review_invocations_required": review_invocations_required,
        "review_invocations_used": review_invocations_used,
        "review_invocations_completed": review_invocations_completed,
        "repair_generation": repair_generation,
        "repair_completed_generation": repair_completed_generation,
        "repair_open": repair_open,
        "repair_base": repair_base,
        "repair_findings": repair_findings,
        "review_findings": review_findings,
        "review_decision_id": review_decision_id,
        "review_invocation_id": review_invocation_id,
        "review_mode": review_mode,
        "friction_observations": friction_observations,
        "friction_synthesis": friction_synthesis,
        "integration_checkout": integration_checkout,
        "width": frontier_width,
        "peak_width": peak_authorized_width,
        "frontier_reason": frontier_reason,
        "selected_frontier": selected_frontier,
        "last_wave_clean": last_wave_clean,
        "serial_latch": serial_latch,
        "downshift_required": downshift_required,
        "downshift_last_cause": downshift_last_cause,
        "downshift_last_release": downshift_last_release,
        "proof_records": proof_records,
    }


def intent_errors(state: dict[str, Any], intent: str) -> list[str]:
    errors = list(state["errors"])
    items = state["items"]
    if state["checkpoint_active"] and intent != "checkpoint":
        errors.append("active checkpoint requires resume before authority reopens")
    if state["resume_pending"]:
        errors.append("resume requires reconciled Git, worktree, agent, and tracker evidence")
    if intent == "dispatch":
        pending_results = [
            work_item
            for work_item, item in items.items()
            if item.get("handoff")
            and not item.get("accepted")
            and not item.get("rejected")
        ]
        if pending_results:
            errors.append(
                "uninspected worker result queue: " + ", ".join(sorted(pending_results))
            )
        if state.get("downshift_required"):
            errors.append(
                "Downshift must be recorded: " + str(state["downshift_required"])
            )
        if pending_results and state.get("width", 1) > 1 and not state.get("serial_latch"):
            errors.append("parallel width requires Downshift before new dispatch")
        accepted_unlanded = [
            work_item
            for work_item, item in items.items()
            if item.get("accepted") and not item.get("landed")
        ]
        if accepted_unlanded:
            errors.append(
                "accepted unlanded work requires Drain: "
                + ", ".join(sorted(accepted_unlanded))
            )
        ready = [
            work_item
            for work_item, item in items.items()
            if item.get("preflight") and not item.get("dispatched")
        ]
        if not ready:
            errors.append("no reconciled preflighted item is ready to dispatch")
        elif state.get("runtime_contract", 1) >= 3:
            selected_ready = set(ready) & set(state.get("selected_frontier", []))
            if not selected_ready:
                errors.append("no preflighted item belongs to the selected frontier")
            active = sum(
                bool(item.get("dispatched"))
                and not item.get("handoff")
                and not item.get("accepted")
                and not item.get("rejected")
                and not item.get("landed")
                for item in items.values()
            )
            if active >= state.get("width", 1):
                errors.append("authorized frontier width is fully occupied")
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
        if state["review_invocations_used"] >= state["review_invocation_budget"]:
            errors.append("Review Invocation Budget is exhausted")
        if state["review_invocation_id"] and state["review_decision"] is None:
            errors.append("current review invocation has no decision")
        repaired_successor_ready = (
            state["repair_generation"] > 0
            and state["repair_generation"] == state["repair_completed_generation"]
            and state["integration_head"] != state["review_target"]
        )
        if state["review_decision"] in {"blocked", "fail"} and not repaired_successor_ready:
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
        if state["review_invocations_used"] >= state["review_invocation_budget"]:
            errors.append("no successor review invocation remains")
        if state["review_target"] != state["current_head"]:
            errors.append("blocked review target does not equal current HEAD")
    elif intent == "lock":
        if state["review_decision"] not in ACCEPTED_REVIEWS:
            errors.append("review has not passed")
        if state["review_target"] != state["current_head"]:
            errors.append("review target does not equal current HEAD")
        if state["repair_open"]:
            errors.append("Repair generation remains open")
        if (
            state["review_invocations_completed"]
            < state["review_invocations_required"]
        ):
            errors.append("required review invocations are incomplete")
    elif intent == "push":
        if not state["closeout_head"]:
            errors.append("closeout HEAD is not approved")
        if state["closeout_head"] != state["current_head"]:
            errors.append("closeout HEAD does not equal current HEAD")
        if state["repair_open"]:
            errors.append("Repair generation remains open")
    elif intent == "checkpoint":
        if not state["checkpoint_active"]:
            errors.append("no resumable checkpoint is active")
    elif intent == "complete":
        if state["release_outcome"] != "complete":
            errors.append("release outcome is not complete")
        if state["review_decision"] not in ACCEPTED_REVIEWS:
            errors.append("review has not passed")
        if state["closeout_head"] != state["current_head"]:
            errors.append("closeout HEAD does not equal current HEAD")
        missing = [child for child in state["children"] if state["child_closeouts"].get(child, {}).get("state") != "verified"]
        if missing:
            errors.append(f"children lack verified closeout: {', '.join(missing)}")
        if not state["parent_closeout"]:
            errors.append("parent closeout is not verified")
        if not state["tracker_locked"]:
            errors.append("tracker Lock is not verified")
        if state["push_required"] and state["pushed_head"] != state["closeout_head"]:
            errors.append("approved closeout HEAD was not pushed")
        for lane_id, lane_state in state["lane_status"].items():
            if lane_state not in SAFE_LANE_STATES:
                recorded = state["lanes"][lane_id].get("state")
                errors.append(f"lane {lane_id} remains {lane_state} ({recorded})")
    return list(dict.fromkeys(errors))


def next_actions(errors: list[str], intent: str) -> list[str]:
    if not errors:
        return [f"authorized:{intent}"]
    return [f"reconcile:{error}" for error in errors]


def validate_state_command(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    errors = intent_errors(state, args.intent)
    allowed = not errors
    return emit(
        allowed,
        operation="validate-state",
        events=str(path),
        intent=args.intent,
        allowed=allowed,
        campaign_status=state["campaign_status"],
        errors=errors,
        next_action=next_actions(errors, args.intent),
        lane_status=state["lane_status"],
        current_head=state["current_head"],
        integration_head=state["integration_head"],
        checkpoint_active=state["checkpoint_active"],
        approved_head=state["closeout_head"],
        review_decision_id=state["review_decision_id"],
        repair_generation=state["repair_generation"],
        repair_generation_budget=state["repair_generation_budget"],
        repair_open=state["repair_open"],
        review_invocations_used=state["review_invocations_used"],
        review_invocation_budget=state["review_invocation_budget"],
        review_invocations_completed=state["review_invocations_completed"],
        review_invocations_required=state["review_invocations_required"],
    )


def validate(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    return emit(True, operation="validate", events=str(path), count=len(events))


def status(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    facade = facade_view(state)
    return emit(
        not state["errors"],
        operation="resume-status" if args.command == "resume-status" else "status",
        events=str(path),
        campaign_status=state["campaign_status"],
        errors=state["errors"],
        lane_status=state["lane_status"],
        integration_head=state["integration_head"],
        current_head=state["current_head"],
        checkpoint_active=state["checkpoint_active"],
        review_decision_id=state["review_decision_id"],
        repair_generation=state["repair_generation"],
        repair_generation_budget=state["repair_generation_budget"],
        repair_open=state["repair_open"],
        review_invocations_used=state["review_invocations_used"],
        review_invocation_budget=state["review_invocation_budget"],
        review_invocations_completed=state["review_invocations_completed"],
        review_invocations_required=state["review_invocations_required"],
        **facade,
    )


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
        elif item.get("rejected"):
            value = "rejected"
        elif item.get("handoff"):
            value = "returned"
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
    result_queue = sorted(
        key for key, value in implementations.items() if value == "returned"
    )
    active = sorted(
        lane_id
        for lane_id, lane_state in state["lane_status"].items()
        if lane_state in {"active", "committed-unlanded", "dirty-preserved"}
    )
    authorized = [
        intent for intent in sorted(INTENTS) if not intent_errors(state, intent)
    ]
    action = "select-frontier"
    evidence = "reconciled dependencies, scope, proof, slots, and review bandwidth"
    suggested = "record a serial or parallel frontier packet with apply"
    phase = "select"
    decision_required = False
    repaired_successor_ready = (
        state["repair_generation"] > 0
        and state["repair_generation"] == state["repair_completed_generation"]
        and not state["repair_open"]
        and state["integration_head"] != state["review_target"]
    )
    required_downshift = state.get("downshift_required")
    if result_queue and state.get("width", 1) > 1 and not state.get("serial_latch"):
        required_downshift = "downshift-backpressure"

    if state["errors"]:
        phase, action = "blocked", "reconcile-state"
        evidence = state["errors"]
        suggested = "inspect status errors and repair the canonical event stream"
    elif state["release_outcome"] == "complete":
        phase, action = "complete", "none"
        evidence, suggested = "terminal release is recorded", "no campaign action remains"
    elif state["checkpoint_active"]:
        phase, action = "checkpoint", "resume"
        evidence = "fresh Git, worktree, actor, claim, tracker, remote, and integration-checkout observations"
        suggested = "append resume, then apply one reconciliation packet"
    elif state["resume_pending"]:
        phase, action = "open", "reconcile"
        evidence = "Git, worktrees, actors, claims, tracker, remote, and integration checkout"
        suggested = "apply a reconciliation packet before dispatch or landing"
    elif state["integration_regression"]:
        phase, action = "drain", "correct-integration"
        evidence = state["integration_regression"]
        suggested = "open the authorized correction route and apply its accepted result"
    elif required_downshift:
        phase, action = "downshift", "downshift"
        evidence = {
            "reason": required_downshift,
            "result_queue": result_queue,
            "current_width": state.get("width", 1),
        }
        suggested = "apply one width-one frontier with the required Downshift reason"
    elif result_queue:
        phase, action = "drain", "inspect-result"
        evidence = result_queue
        suggested = "inspect and classify the oldest queued worker result"
    elif any(value == "accepted" for value in implementations.values()):
        phase, action = "drain", "land"
        evidence = sorted(key for key, value in implementations.items() if value == "accepted")
        suggested = "inspect and serially land one accepted packet"
    elif any(value == "ready" for value in implementations.values()):
        phase, action = "open", "dispatch"
        evidence = sorted(key for key, value in implementations.items() if value == "ready")
        suggested = "dispatch the preflighted lane with its generated brief"
    elif any(value == "active" for value in implementations.values()):
        phase, action = "drain", "await-worker"
        evidence, suggested = active, "classify each worker return when it arrives"
    elif not state["graph_drained"]:
        finished = all(
            value.startswith("landed") or value.startswith("disposed") or value == "closed"
            for value in implementations.values()
        ) and bool(implementations)
        if finished:
            phase, action = "drain", "record-graph-drained"
            evidence = "every child is landed or explicitly disposed"
            suggested = "apply graph-drained at the current integration HEAD"
    elif (
        state["review_decision"] is None or repaired_successor_ready
    ) and not state["review_ready"]:
        phase, action = "review", "record-review-ready"
        evidence = "broad loop-close proof and idle lanes"
        suggested = "apply review-ready at the immutable integration HEAD"
    elif state["review_decision"] is None or repaired_successor_ready:
        phase, action = "review", "invoke-review"
        evidence = "Charter, Source Trace, fixed point, and immutable target"
        suggested = "invoke the selected formal review route"
    elif state["review_decision"] not in ACCEPTED_REVIEWS:
        phase, action, decision_required = "review", "repair-or-decide", True
        evidence = state["review_findings"]
        suggested = "apply one complete eligible Repair plan or return the decision packet"
    elif not state["closeout_head"]:
        phase, action = "lock", "lock"
        evidence = "accepted reviewed HEAD equals current integration HEAD"
        suggested = "record closeout-head, then execute the generated closeout plan"
    elif not state["tracker_locked"]:
        phase, action = "lock", "closeout"
        evidence = closeout_actions(state)
        suggested = "complete child-first tracker mutations with read-back"
    elif state["push_required"] and state["pushed_head"] != state["closeout_head"]:
        phase, action = "lock", "push"
        evidence = state["closeout_head"]
        suggested = "push and verify the approved closeout SHA"
    else:
        phase, action = "release", "release"
        evidence = "safe lanes, complete closeout, and friction synthesis"
        suggested = "append terminal complete release, then run finish"

    return {
        "phase": phase,
        "frontier": sorted(
            key for key, value in implementations.items() if value in {"pending", "ready"}
        ),
        "active_lanes": active,
        "blockers": state["errors"],
        "decision_required": decision_required,
        "authorized_actions": authorized,
        "implementation_state": implementations,
        "result_queue": result_queue,
        "width": state.get("width", 1),
        "peak_width": state.get("peak_width", 1),
        "frontier_reason": state.get("frontier_reason", "serial-default"),
        "serial_latch": state.get("serial_latch"),
        "downshift_last_cause": state.get("downshift_last_cause"),
        "downshift_last_release": state.get("downshift_last_release"),
        "proof_records": state.get("proof_records", []),
        "integration_checkout": state.get("integration_checkout"),
        "next_action": {
            "action": action,
            "evidence": evidence,
            "suggested": suggested,
        },
    }


def read_object(path_value: str) -> dict[str, Any]:
    value = json.loads(Path(path_value).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path_value} must contain one JSON object")
    return value


def start(args: argparse.Namespace) -> int:
    path = event_path(args.events, require_absolute=True)
    if path.exists():
        raise ValueError(f"start requires a missing event stream; use status to resume: {path}")
    packet = read_object(args.scope_file)
    parent = packet.get("parent")
    children = packet.get("children")
    charter = packet.get("charter")
    if not isinstance(parent, str) or not parent:
        raise ValueError("scope packet requires parent")
    if not isinstance(children, list):
        raise ValueError("scope packet requires children")
    if not isinstance(charter, dict) or not charter.get("id"):
        raise ValueError("scope packet requires charter.id")
    repair_budget = charter.get("repair_generation_budget", 4)
    charter = {
        **charter,
        "runtime_contract": 3,
        "repair_generation_budget": repair_budget,
        "review_invocation_budget": charter.get(
            "review_invocation_budget", repair_budget + 1
        ),
        "review_invocations_required": charter.get("review_invocations_required", 1),
    }
    data = {
        key: value
        for key, value in packet.items()
        if key not in {"parent", "integration_sha"}
    }
    data["charter"] = charter
    if "integration_checkout" not in data:
        if not args.repo:
            raise ValueError(
                "scope packet requires integration_checkout when --repo is unavailable"
            )
        starting_head = git_head(args.repo)
        data["integration_checkout"] = {
            "mode": "existing-checkout",
            "path": str(Path(args.repo).resolve()),
            "git_common_dir": git_common_dir(args.repo),
            "starting_head": starting_head,
            "cleanup_authority": "none",
        }
    raw = {
        "event": "scope",
        "event_id": stable_event_id("scope", {"parent": parent, "data": data}),
        "work_item": parent,
        "integration_sha": git_head(args.repo) if args.repo else packet.get("integration_sha"),
        "data": data,
    }
    applied, replayed, events = append_facade_events(path, [raw], repo=args.repo)
    state = derive_state(events, args.repo)
    return emit(
        True,
        operation="start",
        events=str(path),
        applied=applied,
        replayed=replayed,
        **facade_view(state),
    )


def stream_snapshot(path: Path, events: list[dict[str, Any]]) -> dict[str, Any]:
    encoded = "".join(
        json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n"
        for event in events
    ).encode()
    return {
        "path": str(path),
        "event_count": len(events),
        "last_event_id": events[-1]["event_id"] if events else None,
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def terminal_packet_identity(packet: dict[str, Any]) -> str:
    basis = {
        "step": packet.get("step"),
        "stream": packet.get("stream"),
        "prefilled": packet.get("prefilled"),
        "required_fields": packet.get("required_fields"),
    }
    return stable_event_id(f"terminal-{packet.get('step')}", basis)


def review_packet_spec(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[str]]:
    errors = intent_errors(state, "review")
    if errors:
        raise ValueError("review packet is not applicable: " + "; ".join(errors))
    if not state["review_ready"]:
        raise ValueError("review packet requires recorded review-ready candidate proof")
    if not events:
        raise ValueError("review packet requires a campaign scope")
    return (
        {
            "parent": events[0]["work_item"],
            "target": state["integration_head"],
            "charter_id": state["charter_id"],
            "graph_drained": state["graph_drained"],
            "review_ready": state["review_ready"],
            "candidate_proof": next(
                (
                    proof
                    for proof in reversed(state["proof_records"])
                    if proof.get("level") == "candidate"
                ),
                None,
            ),
            "repair_generation": state["repair_generation"],
            "prior_review_invocation_id": state["review_invocation_id"],
            "review_invocations_used": state["review_invocations_used"],
            "review_invocations_remaining": max(
                0,
                state["review_invocation_budget"]
                - state["review_invocations_used"],
            ),
        },
        [
            "invocation_id",
            "mode",
            "reason",
            "route",
            "findings",
            "decision",
            "residual_risk",
        ],
    )


def closeout_packet_spec(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[str]]:
    errors = intent_errors(state, "lock")
    if errors:
        raise ValueError("closeout packet is not applicable: " + "; ".join(errors))
    if not events:
        raise ValueError("closeout packet requires a campaign scope")
    pending = [
        child
        for child in state["children"]
        if state["child_closeouts"].get(child, {}).get("state") != "verified"
    ]
    return (
        {
            "parent": events[0]["work_item"],
            "approved_head": state["review_target"],
            "pending_children": pending,
            "expected_child_mutations": [
                {"work_item": child, "intended_mutation": "close child after verified evidence"}
                for child in pending
            ],
            "child_verified_fields": sorted(CLOSEOUT_FIELDS),
            "push_required": state["push_required"],
            "closeout_head_recorded": state["closeout_head"],
        },
        ["child_readbacks"],
    )


def release_packet_spec(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[str]]:
    errors = [
        error
        for error in intent_errors(state, "complete")
        if error != "release outcome is not complete"
    ]
    if errors:
        raise ValueError("release packet is not applicable: " + "; ".join(errors))
    if not events:
        raise ValueError("release packet requires a campaign scope")
    return (
        {
            "parent": events[0]["work_item"],
            "approved_head": state["closeout_head"],
            "proof_state": state["proof_records"],
            "review_state": {
                "decision": state["review_decision"],
                "target": state["review_target"],
                "completed": state["review_invocations_completed"],
                "required": state["review_invocations_required"],
            },
            "closeout_state": {
                "children": state["child_closeouts"],
                "parent": state["parent_closeout"],
                "tracker_locked": state["tracker_locked"],
            },
            "lane_state": state["lane_status"],
            "integration_checkout": state["integration_checkout"],
            "push_state": {
                "required": state["push_required"],
                "pushed_head": state["pushed_head"],
            },
            "efficiency_state": efficiency_result(events, state),
            "friction_observation_ids": sorted(state["friction_observations"]),
            "friction_recorded": bool(state["friction_synthesis"]),
        },
        ["friction_synthesis", "disposition", "residual_risk"],
    )


def repair_packet_spec(
    state: dict[str, Any], events: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[str]]:
    if not events:
        raise ValueError("repair packet requires a campaign scope")
    if state["repair_open"]:
        return (
            {
                "phase": "complete",
                "parent": events[0]["work_item"],
                "target": state["integration_head"],
                "generation": state["repair_generation"],
                "finding_ids": state["repair_findings"],
                "review_target": state["repair_base"],
            },
            ["finding_ids", "successor_head", "proof", "changed_scope"],
        )
    if state["review_decision"] != "blocked":
        raise ValueError("repair plan requires a blocked review")
    if state["review_target"] != state["current_head"]:
        raise ValueError("repair plan target differs from current HEAD")
    if state["repair_generation"] >= state["repair_generation_budget"]:
        raise ValueError("Repair Generation Budget is exhausted")
    if state["review_invocations_used"] >= state["review_invocation_budget"]:
        raise ValueError("repair plan requires a successor review invocation")
    blockers = [
        finding
        for finding in state["review_findings"]
        if finding.get("blocking") is True
    ]
    if not blockers or any(
        finding.get("remediation") != "automatic-in-scope"
        or not finding.get("id")
        or not finding.get("anchor")
        or not finding.get("evidence")
        or not finding.get("required_proof")
        for finding in blockers
    ):
        raise ValueError("repair plan contains an inadmissible or decision-required blocker")
    return (
        {
            "phase": "plan",
            "parent": events[0]["work_item"],
            "target": state["review_target"],
            "charter_id": state["charter_id"],
            "generation": state["repair_generation"] + 1,
            "review_decision_id": state["review_decision_id"],
            "findings": blockers,
            "prior_owners": {
                work_item: lane.get("actor_id")
                for work_item, item in state["items"].items()
                for lane in [state["lanes"].get(item.get("lane_id"), {})]
                if lane.get("actor_id")
            },
            "prior_scopes": {
                work_item: lane.get("assignment", {}).get("expected_scope")
                for work_item, item in state["items"].items()
                for lane in [state["lanes"].get(item.get("lane_id"), {})]
                if isinstance(lane.get("assignment"), dict)
            },
        },
        ["finding_ids", "assignments"],
    )


def prepare(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    output = absolute_file_path(args.output, label="terminal packet output")
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    if state["errors"]:
        raise ValueError("canonical state is invalid: " + "; ".join(state["errors"]))
    if args.step == "review":
        prefilled, required_fields = review_packet_spec(state, events)
    elif args.step == "repair":
        prefilled, required_fields = repair_packet_spec(state, events)
    elif args.step == "closeout":
        prefilled, required_fields = closeout_packet_spec(state, events)
    elif args.step == "release":
        prefilled, required_fields = release_packet_spec(state, events)
    else:
        raise ValueError(f"terminal step is not implemented: {args.step}")
    packet = {
        "schema": SCHEMA_VERSION,
        "kind": "terminal",
        "step": args.step,
        "stream": stream_snapshot(path, events),
        "prefilled": prefilled,
        "required_fields": required_fields,
        "values": {},
    }
    packet["packet_id"] = terminal_packet_identity(packet)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return emit(
        True,
        operation="prepare",
        events=str(path),
        output=str(output),
        step=args.step,
        packet_id=packet["packet_id"],
        required_fields=required_fields,
        **facade_view(state),
    )


def terminal_review_events(packet: dict[str, Any]) -> list[dict[str, Any]]:
    prefilled = packet.get("prefilled")
    values = packet.get("values")
    required = packet.get("required_fields")
    if not isinstance(prefilled, dict) or not isinstance(values, dict):
        raise ValueError("terminal packet requires prefilled and values objects")
    if not isinstance(required, list) or not all(
        isinstance(field, str) and field for field in required
    ):
        raise ValueError("terminal packet requires required_fields")
    missing = [field for field in required if field not in values]
    if missing:
        raise ValueError("terminal packet values missing: " + ", ".join(missing))
    invocation_id = values.get("invocation_id")
    if not isinstance(invocation_id, str) or not invocation_id:
        raise ValueError("review invocation_id must be a nonempty string")
    findings = values.get("findings")
    if not isinstance(findings, list) or not all(
        isinstance(finding, dict) for finding in findings
    ):
        raise ValueError("review findings must be a list of objects")
    parent = prefilled.get("parent")
    target = prefilled.get("target")
    mode = values.get("mode")
    decision = values.get("decision")
    packet_id = packet.get("packet_id")
    return [
        {
            "event": "review-invocation",
            "event_id": invocation_id,
            "work_item": parent,
            "integration_sha": target,
            "data": {
                "mode": mode,
                "reason": values.get("reason"),
                "route": values.get("route"),
                "packet_id": packet_id,
            },
        },
        {
            "event": "review-decision",
            "event_id": stable_event_id("review-decision", {"packet_id": packet_id}),
            "work_item": parent,
            "integration_sha": target,
            "decision": decision,
            "risk": values.get("residual_risk"),
            "data": {
                "review_invocation_id": invocation_id,
                "mode": mode,
                "route": values.get("route"),
                "findings": findings,
                "residual_risk": values.get("residual_risk"),
                "packet_id": packet_id,
            },
        },
    ]


def terminal_values(packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    prefilled = packet.get("prefilled")
    values = packet.get("values")
    required = packet.get("required_fields")
    if not isinstance(prefilled, dict) or not isinstance(values, dict):
        raise ValueError("terminal packet requires prefilled and values objects")
    if not isinstance(required, list) or not all(
        isinstance(field, str) and field for field in required
    ):
        raise ValueError("terminal packet requires required_fields")
    missing = [field for field in required if field not in values]
    if missing:
        raise ValueError("terminal packet values missing: " + ", ".join(missing))
    return prefilled, values


def terminal_closeout_events(packet: dict[str, Any]) -> list[dict[str, Any]]:
    prefilled, values = terminal_values(packet)
    parent = prefilled.get("parent")
    approved_head = prefilled.get("approved_head")
    packet_id = packet.get("packet_id")
    child_readbacks = values.get("child_readbacks")
    if not isinstance(child_readbacks, list) or not all(
        isinstance(value, dict) for value in child_readbacks
    ):
        raise ValueError("closeout child_readbacks must be a list of objects")
    work_items = [value.get("work_item") for value in child_readbacks]
    if any(not isinstance(item, str) or not item for item in work_items):
        raise ValueError("each closeout child read-back requires work_item")
    if len(work_items) != len(set(work_items)):
        raise ValueError("closeout child read-backs duplicate work_item")
    pending_children = set(prefilled.get("pending_children") or [])
    if not work_items and pending_children:
        raise ValueError("closeout packet requires at least one pending child read-back")
    if not set(work_items) <= pending_children:
        raise ValueError("closeout packet contains a child outside the pending set")
    events: list[dict[str, Any]] = []
    if not prefilled.get("closeout_head_recorded"):
        events.append(
            {
                "event": "closeout-head",
                "event_id": stable_event_id("closeout-head", {"packet_id": packet_id}),
                "work_item": parent,
                "integration_sha": approved_head,
                "data": {"packet_id": packet_id},
            }
        )
    for readback in child_readbacks:
        work_item = readback["work_item"]
        data = {key: value for key, value in readback.items() if key != "work_item"}
        data["packet_id"] = packet_id
        events.append(
            {
                "event": "child-closeout",
                "event_id": stable_event_id(
                    "child-closeout", {"packet_id": packet_id, "work_item": work_item}
                ),
                "work_item": work_item,
                "integration_sha": approved_head,
                "data": data,
            }
        )
    closes_every_pending_child = set(work_items) == pending_children and all(
        readback.get("state") == "verified" for readback in child_readbacks
    )
    if not closes_every_pending_child:
        for field in ("parent_readback", "tracker_lock", "push"):
            if values.get(field) is not None:
                raise ValueError(
                    f"partial closeout must leave {field} null until every child is verified"
                )
        return events
    parent_readback = values.get("parent_readback")
    if not isinstance(parent_readback, dict):
        raise ValueError("closeout parent_readback must be an object")
    events.append(
        {
            "event": "parent-closeout",
            "event_id": stable_event_id("parent-closeout", {"packet_id": packet_id}),
            "work_item": parent,
            "integration_sha": approved_head,
            "data": {**parent_readback, "packet_id": packet_id},
        }
    )
    tracker_lock = values.get("tracker_lock")
    if not isinstance(tracker_lock, dict) or not tracker_lock.get("readback"):
        raise ValueError("closeout tracker_lock requires readback")
    events.append(
        {
            "event": "tracker-lock",
            "event_id": stable_event_id("tracker-lock", {"packet_id": packet_id}),
            "work_item": parent,
            "integration_sha": approved_head,
            "data": {**tracker_lock, "packet_id": packet_id},
        }
    )
    push = values.get("push")
    if prefilled.get("push_required"):
        if not isinstance(push, dict) or push.get("verified_head") != approved_head:
            raise ValueError("closeout push requires verified approved HEAD")
        events.append(
            {
                "event": "push",
                "event_id": stable_event_id("push", {"packet_id": packet_id}),
                "work_item": parent,
                "integration_sha": approved_head,
                "data": {**push, "packet_id": packet_id},
            }
        )
    elif push is not None:
        raise ValueError("closeout push must be null when push is not required")
    return events


def terminal_release_events(packet: dict[str, Any]) -> list[dict[str, Any]]:
    prefilled, values = terminal_values(packet)
    parent = prefilled.get("parent")
    approved_head = prefilled.get("approved_head")
    packet_id = packet.get("packet_id")
    disposition = values.get("disposition")
    if disposition != "complete":
        raise ValueError("runtime-contract-3 release disposition must be complete")
    events: list[dict[str, Any]] = []
    synthesis = values.get("friction_synthesis")
    if not prefilled.get("friction_recorded"):
        if not isinstance(synthesis, dict):
            raise ValueError("release friction_synthesis must be an object")
        if set(synthesis.get("observations", [])) != set(
            prefilled.get("friction_observation_ids") or []
        ):
            raise ValueError("release friction synthesis must reference every observation")
        events.append(
            {
                "event": "friction",
                "event_id": stable_event_id("friction", {"packet_id": packet_id}),
                "work_item": parent,
                "data": {**synthesis, "kind": "synthesis", "packet_id": packet_id},
            }
        )
    elif synthesis is not None:
        raise ValueError("release friction synthesis is already recorded")
    events.append(
        {
            "event": "release",
            "event_id": stable_event_id("release", {"packet_id": packet_id}),
            "work_item": parent,
            "integration_sha": approved_head,
            "decision": "complete",
            "risk": values.get("residual_risk"),
            "data": {
                "disposition": disposition,
                "residual_risk": values.get("residual_risk"),
                "packet_id": packet_id,
            },
        }
    )
    return events


def terminal_repair_events(packet: dict[str, Any]) -> list[dict[str, Any]]:
    prefilled, values = terminal_values(packet)
    parent = prefilled.get("parent")
    packet_id = packet.get("packet_id")
    finding_ids = values.get("finding_ids")
    if not isinstance(finding_ids, list) or not all(
        isinstance(finding_id, str) and finding_id for finding_id in finding_ids
    ):
        raise ValueError("repair finding_ids must be a list of IDs")
    expected_ids = (
        [finding.get("id") for finding in prefilled.get("findings", [])]
        if prefilled.get("phase") == "plan"
        else prefilled.get("finding_ids", [])
    )
    if set(finding_ids) != set(expected_ids) or len(finding_ids) != len(
        set(finding_ids)
    ):
        raise ValueError("repair packet must carry every admitted finding exactly once")
    if prefilled.get("phase") == "plan":
        assignments = values.get("assignments")
        if not isinstance(assignments, list) or not assignments or not all(
            isinstance(assignment, dict)
            and assignment.get("owner")
            and assignment.get("scope")
            and assignment.get("required_proof")
            for assignment in assignments
        ):
            raise ValueError("repair plan requires complete assignments")
        return [
            {
                "event": "repair-plan",
                "event_id": stable_event_id("repair-plan", {"packet_id": packet_id}),
                "work_item": parent,
                "integration_sha": prefilled.get("target"),
                "data": {
                    "charter_id": prefilled.get("charter_id"),
                    "generation": prefilled.get("generation"),
                    "review_decision_id": prefilled.get("review_decision_id"),
                    "review_target": prefilled.get("target"),
                    "finding_ids": finding_ids,
                    "assignments": assignments,
                    "packet_id": packet_id,
                },
            }
        ]
    successor = values.get("successor_head")
    if successor != prefilled.get("target"):
        raise ValueError("repair successor_head differs from current integration HEAD")
    proof = values.get("proof")
    proof_errors = proof_evidence_errors(proof, expected_level="repair")
    if proof_errors:
        raise ValueError("; ".join(proof_errors))
    changed_scope = values.get("changed_scope")
    if not isinstance(changed_scope, list) or not changed_scope:
        raise ValueError("repair completion requires changed_scope")
    return [
        {
            "event": "repair-complete",
            "event_id": stable_event_id("repair-complete", {"packet_id": packet_id}),
            "work_item": parent,
            "integration_sha": successor,
            "validation": str(proof.get("command_identity")),
            "data": {
                "generation": prefilled.get("generation"),
                "finding_ids": finding_ids,
                "changed_scope": changed_scope,
                "proof": proof,
                "packet_id": packet_id,
            },
        }
    ]


def validate_terminal_stream(
    packet: dict[str, Any],
    path: Path,
    events: list[dict[str, Any]],
    state: dict[str, Any],
) -> None:
    if packet.get("schema") != SCHEMA_VERSION:
        raise ValueError("terminal packet has unsupported schema")
    if packet.get("packet_id") != terminal_packet_identity(packet):
        raise ValueError("terminal packet identity differs from generated content")
    expected_stream = stream_snapshot(path, events)
    if packet.get("stream") != expected_stream:
        raise ValueError("terminal packet stream is stale or belongs to another campaign")
    prefilled = packet.get("prefilled")
    if not isinstance(prefilled, dict):
        raise ValueError("terminal packet requires prefilled evidence")
    packet_head = prefilled.get("target") or prefilled.get("approved_head")
    if packet_head != state["integration_head"]:
        raise ValueError("terminal packet target differs from current integration HEAD")


def packet_events(
    packet: dict[str, Any], *, state: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    kind = packet.get("kind")
    work_item = packet.get("work_item")
    identity = {key: value for key, value in packet.items() if key != "event_id"}
    if kind == "lane-ready":
        lane_id = packet.get("lane_id")
        actor_id = packet.get("actor_id")
        if not all(isinstance(value, str) and value for value in (work_item, lane_id, actor_id)):
            raise ValueError("lane-ready requires work_item, lane_id, and actor_id")
        create = packet.get("create") if isinstance(packet.get("create"), dict) else {}
        preflight = packet.get("preflight") if isinstance(packet.get("preflight"), dict) else {}
        assignment = (
            packet.get("assignment")
            if isinstance(packet.get("assignment"), dict)
            else {}
        )
        existing_actors = {
            lane.get("actor_id")
            for lane in (state or {}).get("lanes", {}).values()
            if lane.get("actor_id")
        }
        recorded_lane = (state or {}).get("lanes", {}).get(lane_id, {})
        role = packet.get("role") or recorded_lane.get("role") or (
            "primary" if not existing_actors else "additional"
        )
        return [
            {
                "event": "lane-create",
                "event_id": stable_event_id("lane-create", identity),
                "work_item": work_item,
                "data": {
                    **create,
                    "lane_id": lane_id,
                    "actor_id": actor_id,
                    "role": role,
                    "assignment": assignment,
                },
            },
            {
                "event": "lane-preflight",
                "event_id": stable_event_id("lane-preflight", identity),
                "work_item": work_item,
                "data": {**preflight, "lane_id": lane_id, "actor_id": actor_id},
            },
        ]
    if kind == "worker-result":
        if not isinstance(work_item, str) or not work_item:
            raise ValueError("worker-result requires work_item")
        report = packet.get("report")
        if not isinstance(report, dict):
            raise ValueError("worker result missing: report")
        if state is not None and state.get("runtime_contract", 1) >= 3:
            required = {
                "status",
                "changed_scope_summary",
                "proof_outcome",
                "proof_log_path",
                "skipped_checks",
                "risks",
                "report_path",
                "final_status",
            }
            missing = sorted(
                key
                for key in required
                if key not in report or report[key] is None or report[key] == ""
            )
            if report.get("status") == "done" and not report.get("commit"):
                missing.append("commit")
            if report.get("status") == "done" and not report.get("proof"):
                missing.append("proof")
            if missing:
                raise ValueError("worker result missing: " + ", ".join(missing))
            if report.get("status") not in {"done", "blocker", "needs-feedback"}:
                raise ValueError(
                    "worker result status must be done, blocker, or needs-feedback"
                )
            if not isinstance(report.get("skipped_checks"), list):
                raise ValueError("worker result skipped_checks must be a list")
            if not isinstance(report.get("risks"), list):
                raise ValueError("worker result risks must be a list")
            for field in ("proof_log_path", "report_path"):
                absolute_file_path(
                    str(report[field]), label=f"worker result {field}"
                )
            if report.get("status") == "done":
                proof_errors = proof_evidence_errors(
                    report.get("proof"), expected_level="slice"
                )
                if proof_errors:
                    raise ValueError("; ".join(proof_errors))
        return [
            {
                "event": "handoff",
                "event_id": stable_event_id("handoff", identity),
                "work_item": work_item,
                "data": report,
            }
        ]
    if kind == "events":
        values = packet.get("events")
        if not isinstance(values, list) or not values:
            raise ValueError("events packet requires a non-empty events list")
        result = []
        for index, value in enumerate(values):
            if not isinstance(value, dict):
                raise ValueError("events packet entries must be objects")
            result.append({**value, "event_id": value.get("event_id") or stable_event_id(str(value.get("event", "event")), identity, index=index)})
        return result
    if kind == "terminal":
        if state is None:
            raise ValueError("terminal packet requires current reducer state")
        step = packet.get("step")
        if step == "review":
            return terminal_review_events(packet)
        if step == "repair":
            return terminal_repair_events(packet)
        if step == "closeout":
            return terminal_closeout_events(packet)
        if step == "release":
            return terminal_release_events(packet)
        raise ValueError(f"unsupported terminal step: {step}")
    raise ValueError(
        "unsupported packet kind; use lane-ready, worker-result, events, or terminal"
    )


def apply_packet(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    packet_path = absolute_file_path(
        args.packet_file, label="packet", require_existing=True
    )
    packet = read_object(str(packet_path))
    prior = load_events(path)
    validate_events(prior)
    state = derive_state(prior, args.repo)
    raw_events = packet_events(packet, state=state)
    existing_ids = {event["event_id"] for event in prior}
    if packet.get("kind") == "terminal" and not all(
        event["event_id"] in existing_ids for event in raw_events
    ):
        validate_terminal_stream(packet, path, prior, state)
    applied, replayed, events = append_facade_events(path, raw_events, repo=args.repo)
    state = derive_state(events, args.repo)
    return emit(
        True,
        operation="apply",
        events=str(path),
        applied=applied,
        replayed=replayed,
        event_ids=[event["event_id"] for event in raw_events],
        **facade_view(state),
    )


def brief(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    item = state["items"].get(args.work_item, {})
    lane = state["lanes"].get(item.get("lane_id"), {})
    if not item:
        raise ValueError(f"unknown work item: {args.work_item}")
    assignment = (
        lane.get("assignment") if isinstance(lane.get("assignment"), dict) else {}
    )
    assignment_fields = {
        "source_trace",
        "dependencies",
        "acceptance",
        "expected_scope",
        "exclusions",
        "public_proof_seam",
        "proof_command_file",
        "report_path",
        "claim",
        "temp_roots",
        "liveness_checkpoint",
        "state_boundary_matrix",
    }
    missing_assignment = sorted(
        field
        for field in assignment_fields
        if field not in assignment
        or assignment[field] is None
        or assignment[field] == ""
    )
    if missing_assignment:
        raise ValueError(
            "brief assignment missing: " + ", ".join(missing_assignment)
        )
    for field in ("proof_command_file", "report_path"):
        absolute_file_path(str(assignment[field]), label=f"brief {field}")
    claim = assignment.get("claim")
    if not isinstance(claim, dict) or not all(
        claim.get(field) for field in ("owner", "token", "readback")
    ):
        raise ValueError("brief assignment claim requires owner, token, and readback")
    temp_roots = assignment.get("temp_roots")
    if not isinstance(temp_roots, dict) or not all(
        temp_roots.get(field) for field in ("temp", "pytest", "cache")
    ):
        raise ValueError("brief assignment temp_roots requires temp, pytest, and cache")
    for field, value in temp_roots.items():
        absolute_file_path(str(value), label=f"brief temp root {field}")
    preflight_fields = {
        "base",
        "worktree",
        "actor_id",
        "proof_startup",
        "python_provenance",
        "temp_root",
        "pytest_basetemp",
        "cache_root",
    }
    missing_preflight = sorted(
        field
        for field in preflight_fields
        if field not in lane or lane[field] is None or lane[field] == ""
    )
    if missing_preflight:
        raise ValueError("brief preflight missing: " + ", ".join(missing_preflight))
    for field in ("worktree", "temp_root", "pytest_basetemp", "cache_root"):
        absolute_file_path(str(lane[field]), label=f"brief preflight {field}")

    def compact(value: Any, fallback: str = "not recorded") -> str:
        if isinstance(value, list):
            return ", ".join(str(item) for item in value) or fallback
        if value is None or value == "":
            return fallback
        return str(value)

    lines = [
        "# Parallel Implementation Assignment",
        "",
        f"- Work item: `{args.work_item}`",
        f"- Mode: `{args.mode}`",
        f"- Actor: `{lane.get('actor_id') or 'unassigned'}`",
        f"- Role: `{lane.get('role') or 'additional'}`",
        f"- Charter: `{state['charter_id'] or 'not recorded'}`",
        f"- Base: `{lane.get('base') or state['current_head'] or 'not recorded'}`",
        f"- Worktree: `{lane.get('worktree') or 'not recorded'}`",
        f"- Source Trace: `{compact(assignment.get('source_trace'))}`",
        f"- Dependencies: `{compact(assignment.get('dependencies'))}`",
        f"- Acceptance: `{compact(assignment.get('acceptance'))}`",
        f"- Expected scope: `{compact(assignment.get('expected_scope'))}`",
        f"- Exclusions: `{compact(assignment.get('exclusions'))}`",
        f"- Public proof seam: `{compact(assignment.get('public_proof_seam'))}`",
        f"- Proof command file: `{compact(assignment.get('proof_command_file'))}`",
        f"- Report path: `{compact(assignment.get('report_path'))}`",
        f"- Claim owner: `{claim.get('owner')}`",
        f"- Claim token: `{claim.get('token')}`",
        f"- Claim read-back: `{claim.get('readback')}`",
        f"- Preflight proof startup: `{compact(lane.get('proof_startup'))}`",
        f"- Python import provenance: `{compact(lane.get('python_provenance'))}`",
        f"- Stable temp root: `{lane.get('temp_root')}`",
        f"- Stable pytest root: `{lane.get('pytest_basetemp')}`",
        f"- Stable cache root: `{lane.get('cache_root')}`",
        f"- Liveness checkpoint: `{compact(assignment.get('liveness_checkpoint'))}`",
        f"- State-boundary matrix: `{compact(assignment.get('state_boundary_matrix'))}`",
        "",
        "A warm actor receives a new isolated lane, reconciled base, and complete assignment every time; actor reuse never means checkout reuse.",
        "Implement only the assigned acceptance slice in this lane. Do not integrate, review, mutate trackers, push, spawn agents, or widen scope.",
        "Communicate only for a blocker, required decision, or assigned liveness checkpoint; keep routine detail in the report.",
        "Return one clean commit with criterion-to-proof evidence, or an exact blocker/needs-feedback packet.",
    ]
    if args.mode == "integration-correction":
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
    elif args.mode == "review-repair":
        lines.extend([
            "",
            "## Review repair",
            "",
            f"- Generation: `{state['repair_generation']}`",
            f"- Finding IDs: `{', '.join(state['repair_findings']) or 'not recorded'}`",
            f"- Reviewed HEAD: `{state['repair_base'] or 'not recorded'}`",
        ])
    lines.extend([
        "",
        "## Compact receipt",
        "",
        "Write detailed criterion evidence and command output to the report and proof-log paths. Return one worker-result packet containing status, commit when done, changed_scope_summary, proof_outcome, proof_log_path, structured slice proof evidence, skipped_checks, risks, report_path, and final_status.",
        "The receipt is evidence only; root acceptance and serial landing remain separate.",
    ])
    output = absolute_file_path(args.output, label="brief output")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return emit(True, operation="brief", events=str(path), output=str(output), mode=args.mode, work_item=args.work_item)


def finish(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    friction = "already-recorded"
    if not state["friction_synthesis"]:
        if state["friction_observations"]:
            return emit(
                False,
                operation="finish",
                events=str(path),
                state="decision-required",
                error="friction observations require a deliberate synthesis",
                observations=sorted(state["friction_observations"]),
                **facade_view(state),
            )
        parent = events[0]["work_item"] if events else "campaign"
        raw = {
            "event": "friction",
            "event_id": stable_event_id("friction-none", {"parent": parent}),
            "work_item": parent,
            "data": {
                "kind": "synthesis",
                "observations": [],
                "deduplicated_themes": [],
                "none_observed": True,
            },
        }
        _, _, events = append_facade_events(path, [raw], repo=args.repo)
        state = derive_state(events, args.repo)
        friction = "none-observed-recorded"
    errors = intent_errors(state, "complete")
    if errors:
        return emit(
            False,
            operation="finish",
            events=str(path),
            state="blocked-incomplete",
            errors=errors,
            friction=friction,
            **facade_view(state),
        )
    output = absolute_file_path(args.output, label="finish output")
    output.parent.mkdir(parents=True, exist_ok=True)
    result = efficiency_result(events, state)
    output.write_text(markdown(state, path.name, result), encoding="utf-8")
    return emit(
        True,
        operation="finish",
        events=str(path),
        output=str(output),
        friction=friction,
        efficiency_result=result,
        **facade_view(state),
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
    if state["push_required"] and state["pushed_head"] != state["closeout_head"]:
        actions.append({"owner": "parent", "action": "push-approved-head", "state": state["closeout_head"] or "unapproved"})
    for lane_id, lane_state in state["lane_status"].items():
        if lane_state not in SAFE_LANE_STATES:
            actions.append({"owner": lane_id, "action": "reconcile-lane", "state": lane_state})
    return actions


def closeout_plan(args: argparse.Namespace) -> int:
    path = event_path(
        args.events, require_absolute=True, require_existing=True
    )
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    return emit(
        not state["errors"],
        operation="closeout-plan",
        events=str(path),
        errors=state["errors"],
        actions=closeout_actions(state),
    )


def efficiency_result(
    events: list[dict[str, Any]], state: dict[str, Any]
) -> dict[str, Any]:
    def timestamp(event: dict[str, Any]) -> datetime:
        return datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))

    lock_events = [
        event for event in events if event["event"] in {"tracker-lock", "push"}
    ]
    elapsed_seconds: float | None = None
    if events and lock_events:
        elapsed_seconds = max(
            0.0, (timestamp(lock_events[-1]) - timestamp(events[0])).total_seconds()
        )
    excluded_wait = 0.0
    wait_start: datetime | None = None
    for event in events:
        if event["event"] == "checkpoint":
            wait_start = timestamp(event)
        elif event["event"] == "resume" and wait_start is not None:
            excluded_wait += max(0.0, (timestamp(event) - wait_start).total_seconds())
            wait_start = None

    lane_actors: dict[str, str] = {}
    active: set[str] = set()
    returned: set[str] = set()
    actors: set[str] = set()
    peak_width = 0
    maximum_queue = 0
    proof_invocations = len(state.get("proof_records", []))
    proof_duration = sum(
        float(proof.get("duration_seconds", 0.0))
        for proof in state.get("proof_records", [])
        if isinstance(proof.get("duration_seconds"), (int, float))
        and not isinstance(proof.get("duration_seconds"), bool)
    )
    terminal_packets: set[str] = set()
    for event in events:
        data = event.get("data", {})
        packet_id = data.get("packet_id")
        if isinstance(packet_id, str) and packet_id:
            terminal_packets.add(packet_id)
        lane_id = data.get("lane_id")
        actor_id = data.get("actor_id")
        if event["event"] == "lane-preflight" and isinstance(lane_id, str):
            if isinstance(actor_id, str) and actor_id:
                lane_actors[lane_id] = actor_id
                actors.add(actor_id)
        item = state["items"].get(event["work_item"], {})
        item_lane = item.get("lane_id") or lane_id
        item_actor = lane_actors.get(str(item_lane))
        if event["event"] == "dispatch" and item_actor:
            active.add(item_actor)
        elif event["event"] == "handoff" and item_actor:
            active.discard(item_actor)
            returned.add(event["work_item"])
        elif event["event"] in {"accept", "reject"}:
            if item_actor:
                active.discard(item_actor)
            returned.discard(event["work_item"])
        peak_width = max(peak_width, len(active))
        maximum_queue = max(maximum_queue, len(returned))
    rework_types = {
        "reject",
        "stale-base",
        "conflict",
        "integration-regression",
        "integration-correction",
        "repair-plan",
    }
    return {
        "outcome": state["release_outcome"] or state["checkpoint_outcome"],
        "elapsed_to_verified_lock_seconds": elapsed_seconds,
        "excluded_wait_seconds": excluded_wait,
        "agent_controlled_elapsed_seconds": (
            max(0.0, elapsed_seconds - excluded_wait)
            if elapsed_seconds is not None
            else None
        ),
        "total_tokens": "unavailable",
        "fresh_implementation_contexts": len(actors),
        "peak_implementation_width": peak_width,
        "proof_invocations": proof_invocations,
        "proof_duration_seconds": proof_duration,
        "maximum_uninspected_result_queue": maximum_queue,
        "rework_events": sum(event["event"] in rework_types for event in events),
        "root_authored_terminal_packets": len(terminal_packets),
        "compatibility_fallbacks": sum("receipt" in event for event in events),
        "canonical_event_count": len(events),
        "correctness_result": (
            "accepted"
            if state.get("review_decision") in ACCEPTED_REVIEWS
            else state.get("review_decision") or "not-reviewed"
        ),
        "downshift_latch_cause": state.get("downshift_last_cause"),
        "downshift_latch_release": state.get("downshift_last_release"),
        "repair_generations": {
            "used": state["repair_generation"],
            "budget": state["repair_generation_budget"],
        },
        "review_invocations": {
            "used": state["review_invocations_used"],
            "budget": state["review_invocation_budget"],
            "completed": state["review_invocations_completed"],
            "required": state["review_invocations_required"],
        },
        "measurement_gaps": ["platform token telemetry unavailable"],
    }


def markdown(
    state: dict[str, Any],
    events_name: str,
    result: dict[str, Any] | None = None,
) -> str:
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
        f"- Review invocations: `{state['review_invocations_used']}/{state['review_invocation_budget']}` used; `{state['review_invocations_completed']}/{state['review_invocations_required']}` required complete",
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
    lines.extend(["", "## Workflow Friction", ""])
    if state["friction_observations"]:
        for observation_id, observation in state["friction_observations"].items():
            lines.extend(
                [
                    f"### {observation_id}",
                    "",
                    f"- Surface: {observation['surface']}",
                    f"- Source: {observation['source']}",
                    f"- Evidence: {observation['evidence']}",
                    f"- Impact: {observation['impact']}",
                    f"- Suggestion: {observation['suggestion']}",
                    "",
                ]
            )
    elif state["friction_synthesis"] and state["friction_synthesis"].get(
        "none_observed"
    ):
        lines.append("- None observed.")
    else:
        lines.append("- Synthesis not recorded.")
    if state["friction_synthesis"] and not state["friction_synthesis"].get(
        "none_observed"
    ):
        themes = state["friction_synthesis"].get("deduplicated_themes", [])
        lines.append(f"- Themes: {', '.join(themes) or 'none'}")

    if result is not None:
        lines.extend(
            [
                "",
                "## Efficiency Result",
                "",
                f"- Outcome: `{result['outcome']}`",
                f"- Elapsed to verified Lock: `{result['elapsed_to_verified_lock_seconds']}` seconds",
                f"- Excluded wait: `{result['excluded_wait_seconds']}` seconds",
                f"- Agent-controlled elapsed: `{result['agent_controlled_elapsed_seconds']}` seconds",
                f"- Total tokens: `{result['total_tokens']}`",
                f"- Fresh implementation contexts: `{result['fresh_implementation_contexts']}`",
                f"- Peak implementation width: `{result['peak_implementation_width']}`",
                f"- Proof invocations / duration: `{result['proof_invocations']}` / `{result['proof_duration_seconds']}` seconds",
                f"- Maximum uninspected result queue: `{result['maximum_uninspected_result_queue']}`",
                f"- Rework events: `{result['rework_events']}`",
                f"- Root-authored terminal packets / generated events: `{result['root_authored_terminal_packets']}` / `{result['canonical_event_count']}`",
                f"- Compatibility fallbacks: `{result['compatibility_fallbacks']}`",
                f"- Correctness result: `{result['correctness_result']}`",
                f"- Downshift latch cause: `{result['downshift_latch_cause']}`",
                f"- Downshift latch release: `{result['downshift_latch_release']}`",
                f"- Repair generations: `{result['repair_generations']}`",
                f"- Review invocations: `{result['review_invocations']}`",
                f"- Measurement gaps: {', '.join(result['measurement_gaps']) or 'none'}",
            ]
        )

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


def render(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        markdown(state, path.name, efficiency_result(events, state)),
        encoding="utf-8",
    )
    return emit(
        not state["errors"],
        operation="render",
        events=str(path),
        output=str(output),
        errors=state["errors"],
    )


def list_events(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    return emit(True, operation="list", events=str(path), items=events)


def init(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    if path.exists():
        raise ValueError(f"event stream already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return emit(True, operation="init", events=str(path))


def add_event_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--events", required=True)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--event", choices=sorted(EVENT_TYPES))
    parser.add_argument("--event-id")
    parser.add_argument("--work-item")
    parser.add_argument("--worker-sha")
    parser.add_argument("--integration-sha")
    parser.add_argument("--validation")
    parser.add_argument("--decision")
    parser.add_argument("--risk")
    parser.add_argument("--data-json")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init")
    init_parser.add_argument("--events", required=True)
    init_parser.set_defaults(handler=init)

    start_parser = commands.add_parser("start")
    start_parser.add_argument("--events", required=True)
    start_parser.add_argument("--scope-file", required=True)
    start_parser.add_argument("--repo")
    start_parser.set_defaults(handler=start)

    apply_parser = commands.add_parser("apply")
    apply_parser.add_argument("--events", required=True)
    apply_parser.add_argument("--packet-file", required=True)
    apply_parser.add_argument("--repo")
    apply_parser.set_defaults(handler=apply_packet)

    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--events", required=True)
    prepare_parser.add_argument(
        "--step", required=True, choices=["review", "repair", "closeout", "release"]
    )
    prepare_parser.add_argument("--output", required=True)
    prepare_parser.add_argument("--repo")
    prepare_parser.set_defaults(handler=prepare)

    brief_parser = commands.add_parser("brief")
    brief_parser.add_argument("--events", required=True)
    brief_parser.add_argument("--work-item", required=True)
    brief_parser.add_argument(
        "--mode",
        required=True,
        choices=["implementation", "integration-correction", "review-repair"],
    )
    brief_parser.add_argument("--output", required=True)
    brief_parser.add_argument("--repo")
    brief_parser.set_defaults(handler=brief)

    finish_parser = commands.add_parser("finish")
    finish_parser.add_argument("--events", required=True)
    finish_parser.add_argument("--output", required=True)
    finish_parser.add_argument("--repo")
    finish_parser.set_defaults(handler=finish)

    append_parser = commands.add_parser("append")
    add_event_arguments(append_parser)
    append_parser.set_defaults(handler=append)

    receipt_parser = commands.add_parser("append-receipt")
    add_event_arguments(receipt_parser)
    receipt_parser.add_argument("--intent", required=True, choices=sorted(INTENTS))
    receipt_parser.add_argument("--repo")
    receipt_parser.set_defaults(handler=append_receipt)

    batch_parser = commands.add_parser("append-batch")
    batch_parser.add_argument("--events", required=True)
    source = batch_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--from-file")
    source.add_argument("--stdin", action="store_true")
    batch_parser.set_defaults(handler=append_batch)

    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("--events", required=True)
    validate_parser.set_defaults(handler=validate)

    state_parser = commands.add_parser("validate-state")
    state_parser.add_argument("--events", required=True)
    state_parser.add_argument("--intent", required=True, choices=sorted(INTENTS))
    state_parser.add_argument("--repo")
    state_parser.set_defaults(handler=validate_state_command)

    for name in ("status", "resume-status"):
        status_parser = commands.add_parser(name)
        status_parser.add_argument("--events", required=True)
        status_parser.add_argument("--repo")
        status_parser.set_defaults(handler=status)

    plan_parser = commands.add_parser("closeout-plan")
    plan_parser.add_argument("--events", required=True)
    plan_parser.add_argument("--repo")
    plan_parser.set_defaults(handler=closeout_plan)

    render_parser = commands.add_parser("render")
    render_parser.add_argument("--events", required=True)
    render_parser.add_argument("--output", required=True)
    render_parser.add_argument("--repo")
    render_parser.set_defaults(handler=render)

    list_parser = commands.add_parser("list")
    list_parser.add_argument("--events", required=True)
    list_parser.set_defaults(handler=list_events)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "append" and not args.stdin:
            if not args.event or not args.work_item:
                raise ValueError("flag input requires --event and --work-item")
        if args.command == "append-receipt":
            if not args.stdin:
                raise ValueError("append-receipt requires --stdin")
            if not args.event_id:
                raise ValueError("append-receipt requires --event-id")
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return emit(
            False,
            operation=args.command,
            state="blocked-input",
            recoverable=True,
            error=str(error),
            next_action={"command": args.command, "repair": "correct input and retry"},
        )


if __name__ == "__main__":
    raise SystemExit(main())
