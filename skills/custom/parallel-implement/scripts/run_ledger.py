"""Append and validate the parallel-implement JSONL event stream."""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
EVENT_TYPES = {
    "scope",
    "scope-change",
    "resume",
    "frontier",
    "serial-frontier",
    "parallel-frontier",
    "lane-create",
    "lane-preflight",
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
    "review-decision",
    "closeout-head",
    "child-closeout",
    "parent-closeout",
    "tracker-lock",
    "push",
    "release",
    "friction",
}


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


def append(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    prior = load_events(path)
    validate_events(prior)
    extra = json.loads(args.data_json) if args.data_json else {}
    if not isinstance(extra, dict):
        raise ValueError("data-json must contain an object")
    event = {
        "schema": SCHEMA_VERSION,
        "event_id": args.event_id or str(uuid.uuid4()),
        "timestamp": datetime.now(UTC).isoformat(),
        "event": args.event,
        "work_item": args.work_item,
        "worker_sha": args.worker_sha,
        "integration_sha": args.integration_sha,
        "validation": args.validation,
        "decision": args.decision,
        "risk": args.risk,
        "data": extra,
    }
    validate_events([*prior, event])
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n").encode()
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, encoded)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return emit(True, operation="append", events=str(path), event=event)


def validate(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    return emit(True, operation="validate", events=str(path), count=len(events))


def list_events(args: argparse.Namespace) -> int:
    path = event_path(args.events)
    events = load_events(path)
    validate_events(events)
    return emit(True, operation="list", events=str(path), items=events)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    append_parser = commands.add_parser("append")
    append_parser.add_argument("--events", required=True)
    append_parser.add_argument("--event", required=True, choices=sorted(EVENT_TYPES))
    append_parser.add_argument("--event-id")
    append_parser.add_argument("--work-item", required=True)
    append_parser.add_argument("--worker-sha")
    append_parser.add_argument("--integration-sha")
    append_parser.add_argument("--validation")
    append_parser.add_argument("--decision")
    append_parser.add_argument("--risk")
    append_parser.add_argument("--data-json")
    append_parser.set_defaults(handler=append)

    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("--events", required=True)
    validate_parser.set_defaults(handler=validate)

    list_parser = commands.add_parser("list")
    list_parser.add_argument("--events", required=True)
    list_parser.set_defaults(handler=list_events)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return emit(False, operation=args.command, error=str(error))


if __name__ == "__main__":
    raise SystemExit(main())
