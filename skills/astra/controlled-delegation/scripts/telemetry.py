"""Bounded, read-only Codex session metadata observations; no billing inference."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

TAIL_BYTES = 2 * 1024 * 1024
HEADER_BYTES = 1024 * 1024
MAX_ENTRIES = 4096
FIELDS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens",
          "output_tokens", "reasoning_output_tokens", "total_tokens")


def locate(root: Path, thread_id: str) -> Path:
    """Walk only the dated layout, with a fixed entry budget and no symlinks."""
    budget = MAX_ENTRIES
    found = []
    def visit(directory: Path, depth: int) -> None:
        nonlocal budget
        with os.scandir(directory) as entries:
            for entry in entries:
                budget -= 1
                if budget < 0:
                    raise ValueError("lookup_limit_use_exact_session_path")
                if depth < 3:
                    if entry.name.isdigit() and entry.is_dir(follow_symlinks=False):
                        visit(Path(entry.path), depth + 1)
                elif entry.is_file(follow_symlinks=False) and entry.name.endswith(f"-{thread_id}.jsonl"):
                    found.append(Path(entry.path))
    # UUIDv7 carries creation time. Try nearby dates first to allow for local
    # directory dates; fall back to the bounded walk for other layouts/IDs.
    identity = UUID(thread_id)
    if identity.version == 7:
        created = datetime.fromtimestamp((identity.int >> 80) / 1000, timezone.utc)
        for offset in (0, -1, 1):
            day = created + timedelta(days=offset)
            directory = root / day.strftime('%Y/%m/%d')
            if directory.is_dir() and not any(p.is_symlink() for p in
                                              (directory, directory.parent, directory.parent.parent)):
                visit(directory, 3)
    if not found:
        visit(root, 0)
    if len(found) != 1:
        raise ValueError("session_not_uniquely_located")
    return found[0]


def observe(path: Path, thread_id: str) -> dict:
    result = {"thread_id": thread_id, "session_path": str(path.absolute()),
              "captured_at": datetime.now(timezone.utc).isoformat(),
              "status": "unavailable", "warnings": [], "context": None, "usage": None}
    try:
        with path.open("rb") as stream:
            stat = os.fstat(stream.fileno())
            cutoff = stat.st_size
            result["file_identity"] = [stat.st_dev, stat.st_ino]
            result["cutoff_bytes"] = cutoff
            header = json.loads(stream.readline(HEADER_BYTES))
            if header.get("type") != "session_meta" or header.get("payload", {}).get("id") != thread_id:
                raise ValueError("session_identity_mismatch")
            start = max(0, cutoff - TAIL_BYTES)
            stream.seek(start - 1 if start else 0)
            preceding = stream.read(1) if start else b"\n"
            data = stream.read(cutoff - start)
            if start:
                if preceding != b"\n":
                    data = data.partition(b"\n")[2]
                result["warnings"].append("bounded_tail_not_full_history")
            for line in data.splitlines(keepends=True):
                if not line.endswith(b"\n"):
                    result["warnings"].append("incomplete_final_record")
                    continue
                try:
                    event = json.loads(line)
                    payload = event.get("payload", {})
                    if not isinstance(payload, dict):
                        raise ValueError()
                    timestamp = event.get("timestamp")
                    timestamp = timestamp if isinstance(timestamp, str) else None
                    if event.get("type") == "turn_context":
                        result["context"] = {k: payload.get(k) if isinstance(payload.get(k), str) else None
                                             for k in ("turn_id", "model", "effort")}
                        result["context"]["timestamp"] = timestamp
                        if any(not value for value in result["context"].values()):
                            result["warnings"].append("incomplete_context_metadata")
                    elif event.get("type") == "event_msg" and payload.get("type") == "token_count":
                        info = payload.get("info")
                        if not isinstance(info, dict):
                            continue
                        counters = {}
                        for key in ("total_token_usage", "last_token_usage"):
                            values = info.get(key)
                            if isinstance(values, dict):
                                counters[key] = {k: v for k, v in values.items()
                                                 if k in FIELDS and type(v) is int and v >= 0}
                        if not any(counters.values()):
                            result["usage"] = None
                            result["warnings"].append("empty_usage_counters")
                        else:
                            result["usage"] = {"timestamp": timestamp, "counters": counters}
                except (ValueError, AttributeError, TypeError):
                    result["warnings"].append("invalid_record")
            if os.fstat(stream.fileno()).st_size < cutoff:
                raise ValueError("session_truncated_during_read")
        for key in ("context", "usage"):
            if result[key] is None:
                result["warnings"].append(f"no_{key}_in_observed_tail")
        result["status"] = "partial" if result["warnings"] else "observed"
    except (OSError, ValueError, AttributeError, TypeError):
        result["context"] = result["usage"] = None
        result["warnings"].append("unreadable_invalid_or_mismatched_session")
    result["warnings"] = sorted(set(result["warnings"]))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread-id", default=os.environ.get("CODEX_THREAD_ID"))
    parser.add_argument("--session", type=Path)
    parser.add_argument("--sessions-root", type=Path,
                        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "sessions")
    args = parser.parse_args()
    try:
        thread_id = str(UUID(args.thread_id))
        path = args.session or locate(args.sessions_root, thread_id)
        result = observe(path, thread_id)
    except (ValueError, TypeError, AttributeError, OSError) as error:
        reason = str(error)
        if reason not in {"lookup_limit_use_exact_session_path", "session_not_uniquely_located"}:
            reason = "provide_valid_thread_id_and_exact_session_path"
        result = {"status": "unavailable", "warnings": [reason]}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
