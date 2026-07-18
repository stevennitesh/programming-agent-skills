"""Record, validate, derive, and render a parallel-implement campaign."""

from __future__ import annotations

import argparse
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
    "release",
    "friction",
}
INTENTS = {"dispatch", "land", "review", "repair", "lock", "push", "complete"}
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


def event_path(value: str) -> Path:
    path = Path(value).resolve()
    if path.suffix.lower() != ".jsonl":
        raise ValueError("event stream must use a .jsonl path")
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


def receipt_payload(
    state: dict[str, Any],
    *,
    event_id: str,
    event_number: int,
    intent: str,
    state_event_count: int,
) -> dict[str, Any]:
    requested_errors = intent_errors(state, intent)
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
    release_outcome: str | None = None
    resume_pending = False
    tracker_locked = False
    release_seen = False
    charter_id: str | None = None
    runtime_contract = 1
    repair_generation_budget = 2
    review_invocation_budget = 3
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

    def item_state(item: str) -> dict[str, Any]:
        return items.setdefault(item, {})

    def need(condition: bool, message: str) -> bool:
        if not condition:
            errors.append(message)
        return condition

    for number, event in enumerate(events, 1):
        kind = event["event"]
        item = event["work_item"]
        data = event["data"]
        prefix = f"event {number} {kind} for {item}"
        state = item_state(item)

        if release_seen and kind != "friction":
            errors.append(f"{prefix} occurs after release")

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
                    and candidate_contract in {1, 2},
                    f"{prefix} Charter runtime_contract must be 1 or 2",
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
            resume_pending = True
        elif kind == "reconcile":
            required = {"git", "worktrees", "agents", "tracker"}
            missing = sorted(field for field in required if field not in data)
            need(not missing, f"{prefix} missing reconciliation evidence: {', '.join(missing)}")
            resume_pending = bool(missing)
        elif kind == "lane-create":
            lane_id = data.get("lane_id")
            if need(isinstance(lane_id, str) and bool(lane_id), f"{prefix} requires data.lane_id"):
                lanes[lane_id] = {"work_item": item, "state": "created", **data}
                state["lane_id"] = lane_id
        elif kind == "lane-preflight":
            lane_id = data.get("lane_id")
            if need(lane_id in lanes, f"{prefix} requires lane-create"):
                lanes[lane_id].update(data)
                lanes[lane_id]["state"] = "ready"
                state["preflight"] = True
        elif kind == "dispatch":
            need(not resume_pending, f"{prefix} requires reconciliation after resume")
            lane_id = data.get("lane_id") or state.get("lane_id")
            if need(bool(state.get("preflight")) and lane_id in lanes, f"{prefix} requires lane-preflight"):
                state["dispatched"] = True
                lanes[lane_id]["state"] = "active"
        elif kind == "handoff":
            state["handoff"] = data
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
            lane_id = state.get("lane_id")
            if lane_id in lanes:
                lanes[lane_id]["state"] = "landed"
        elif kind == "graph-drained":
            need(bool(children), f"{prefix} requires an exhaustive scope")
            unfinished = [child for child in children if not item_state(child).get("landed") and not item_state(child).get("disposition")]
            need(not unfinished, f"{prefix} has unfinished children: {', '.join(unfinished)}")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
            graph_drained = True
        elif kind == "review-ready":
            need(graph_drained, f"{prefix} requires graph-drained")
            need(not repair_open, f"{prefix} requires completed Repair")
            need(event.get("integration_sha") == integration_head, f"{prefix} HEAD differs from integration HEAD")
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
        elif kind == "release":
            need(event.get("decision") in {"complete", "partial", "blocked"}, f"{prefix} has invalid outcome")
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
            release_outcome = event.get("decision")
            release_seen = True

    if runtime_contract >= 2 and release_outcome == "complete" and not friction_synthesis:
        errors.append("canonical campaign requires one Workflow Friction synthesis")

    current_head = git_head(repo)
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
        "graph_drained": graph_drained,
        "review_target": review_target,
        "review_decision": review_decision,
        "closeout_head": closeout_head,
        "child_closeouts": child_closeouts,
        "parent_closeout": parent_closeout,
        "pushed_head": pushed_head,
        "release_outcome": release_outcome,
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
    }


def intent_errors(state: dict[str, Any], intent: str) -> list[str]:
    errors = list(state["errors"])
    items = state["items"]
    if state["resume_pending"]:
        errors.append("resume requires reconciled Git, worktree, agent, and tracker evidence")
    if intent == "dispatch":
        if not any(item.get("preflight") and not item.get("dispatched") for item in items.values()):
            errors.append("no reconciled preflighted item is ready to dispatch")
    elif intent == "land":
        if not any(item.get("accepted") and not item.get("landed") for item in items.values()):
            errors.append("no accepted unlanded item is ready to land")
    elif intent == "review":
        if not state["graph_drained"]:
            errors.append("parent graph is not execution-drained")
        if state["repair_open"]:
            errors.append("Repair generation is not complete")
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
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    state = derive_state(events, args.repo)
    return emit(
        not state["errors"],
        operation="resume-status" if args.command == "resume-status" else "status",
        events=str(path),
        campaign_status=state["campaign_status"],
        errors=state["errors"],
        lane_status=state["lane_status"],
        integration_head=state["integration_head"],
        current_head=state["current_head"],
        review_decision_id=state["review_decision_id"],
        repair_generation=state["repair_generation"],
        repair_generation_budget=state["repair_generation_budget"],
        repair_open=state["repair_open"],
        review_invocations_used=state["review_invocations_used"],
        review_invocation_budget=state["review_invocation_budget"],
        review_invocations_completed=state["review_invocations_completed"],
        review_invocations_required=state["review_invocations_required"],
    )


def closeout_actions(state: dict[str, Any]) -> list[dict[str, str]]:
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
    path = event_path(args.events)
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

    lines.extend(["", "## Child Closeout Packets", ""])
    for child in state["children"]:
        packet = state["child_closeouts"].get(child, {})
        lines.extend(
            [
                f"### {child}",
                "",
                f"- State: `{packet.get('state', 'missing')}`",
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
    output.write_text(markdown(state, path.name), encoding="utf-8")
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
