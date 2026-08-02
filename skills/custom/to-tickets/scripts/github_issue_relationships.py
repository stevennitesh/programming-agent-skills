"""Mutate and verify GitHub issue relationships through ``gh api``.

The helper keeps GitHub's database IDs behind a small issue-number interface
and returns deterministic, bidirectional relationship snapshots for recovery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol


class GitHubApiError(RuntimeError):
    """The GitHub API boundary failed or returned an unusable payload."""


class RelationshipConflictError(RuntimeError):
    """The requested relationship conflicts with observed durable state."""


class RelationshipVerificationError(RuntimeError):
    """A mutation did not appear in its bidirectional read-back."""

    def __init__(self, result: dict[str, Any]) -> None:
        self.result = result
        super().__init__(json.dumps(result, sort_keys=True))


class GitHubApi(Protocol):
    """The narrow REST seam consumed by relationship operations."""

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        fields: dict[str, int] | None = None,
        paginate: bool = False,
        allow_not_found: bool = False,
    ) -> Any:
        """Return one decoded REST response."""


class GhApiClient:
    """Authenticated GitHub REST adapter backed by the ``gh`` CLI."""

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        fields: dict[str, int] | None = None,
        paginate: bool = False,
        allow_not_found: bool = False,
    ) -> Any:
        command = ["gh", "api", "--method", method.upper()]
        if paginate:
            command.extend(["--paginate", "--slurp"])
        for key, value in (fields or {}).items():
            command.extend(["-F", f"{key}={value}"])
        command.append(endpoint)

        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            error = completed.stderr.strip() or completed.stdout.strip()
            if allow_not_found and "HTTP 404" in error:
                return None
            raise GitHubApiError(
                f"gh api failed for {method.upper()} {endpoint}: {error}"
            )

        raw = completed.stdout.strip()
        if not raw:
            return None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as error:
            raise GitHubApiError(
                f"gh api returned invalid JSON for {method.upper()} {endpoint}"
            ) from error

        if (
            paginate
            and isinstance(payload, list)
            and all(isinstance(page, list) for page in payload)
        ):
            return [item for page in payload for item in page]
        return payload


def _repository(value: str) -> str:
    parts = value.split("/")
    if (
        len(parts) != 2
        or not parts[0]
        or not parts[1]
        or any(part in {".", ".."} for part in parts)
    ):
        raise ValueError("repository must be OWNER/REPO")
    return value


def _positive_issue_number(value: int) -> int:
    if isinstance(value, bool) or value <= 0:
        raise ValueError("issue numbers must be positive integers")
    return value


def _issue_endpoint(repository: str, issue_number: int, suffix: str = "") -> str:
    base = f"repos/{repository}/issues/{issue_number}"
    return f"{base}/{suffix}" if suffix else base


def _normalize_issue(payload: Any) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise GitHubApiError("GitHub issue response must be an object")
    required = ("number", "id", "state")
    missing = [field for field in required if field not in payload]
    if missing:
        raise GitHubApiError(
            f"GitHub issue response is missing: {', '.join(missing)}"
        )
    try:
        number = int(payload["number"])
        database_id = int(payload["id"])
    except (TypeError, ValueError) as error:
        raise GitHubApiError("GitHub issue number and id must be integers") from error
    return {
        "number": number,
        "id": database_id,
        "state": str(payload["state"]),
        "state_reason": payload.get("state_reason"),
        "html_url": payload.get("html_url"),
    }


def _normalize_many(payload: Any) -> list[dict[str, object]]:
    if not isinstance(payload, list):
        raise GitHubApiError("GitHub relationship response must be a list")
    return sorted(
        (_normalize_issue(item) for item in payload),
        key=lambda item: int(item["number"]),
    )


def _normalize_issue_packet(payload: Any) -> dict[str, object]:
    issue = _normalize_issue(payload)
    if not isinstance(payload, dict):
        raise GitHubApiError("GitHub issue response must be an object")
    for field in ("title", "body", "labels", "assignees"):
        if field not in payload:
            raise GitHubApiError(f"GitHub issue response is missing: {field}")
    labels = payload["labels"]
    assignees = payload["assignees"]
    if not isinstance(labels, list) or not all(isinstance(row, dict) for row in labels):
        raise GitHubApiError("GitHub issue labels must be objects")
    if not isinstance(assignees, list) or not all(
        isinstance(row, dict) for row in assignees
    ):
        raise GitHubApiError("GitHub issue assignees must be objects")
    return {
        **issue,
        "title": str(payload["title"]),
        "body": str(payload["body"] or ""),
        "labels": sorted(str(row.get("name") or "") for row in labels),
        "assignees": sorted(str(row.get("login") or "") for row in assignees),
    }


def _normalize_comments(payload: Any) -> list[dict[str, object]]:
    if not isinstance(payload, list):
        raise GitHubApiError("GitHub comments response must be a list")
    result = []
    for row in payload:
        if not isinstance(row, dict) or "id" not in row or "body" not in row:
            raise GitHubApiError("GitHub comment response is incomplete")
        result.append(
            {
                "id": int(row["id"]),
                "body": str(row["body"] or ""),
                "author": str((row.get("user") or {}).get("login") or ""),
                "created_at": row.get("created_at"),
                "updated_at": row.get("updated_at"),
            }
        )
    return result


def _contains(
    issues: Sequence[dict[str, object]],
    issue_number: int,
) -> bool:
    return any(int(issue["number"]) == issue_number for issue in issues)


def inspect_issue(
    client: GitHubApi,
    repository: str,
    issue_number: int,
) -> dict[str, object]:
    """Return one normalized issue and all native relationship directions."""

    repository = _repository(repository)
    issue_number = _positive_issue_number(issue_number)
    base = _issue_endpoint(repository, issue_number)
    issue = _normalize_issue(client.request("GET", base))
    parent_payload = client.request(
        "GET",
        f"{base}/parent",
        allow_not_found=True,
    )
    parent = (
        _normalize_issue(parent_payload)
        if parent_payload is not None
        else None
    )
    return {
        "repository": repository,
        "issue": issue,
        "parent": parent,
        "children": _normalize_many(
            client.request("GET", f"{base}/sub_issues", paginate=True)
        ),
        "blocked_by": _normalize_many(
            client.request(
                "GET",
                f"{base}/dependencies/blocked_by",
                paginate=True,
            )
        ),
        "blocking": _normalize_many(
            client.request(
                "GET",
                f"{base}/dependencies/blocking",
                paginate=True,
            )
        ),
    }


def snapshot_campaign(
    client: GitHubApi,
    repository: str,
    parent_number: int,
    output: Path,
) -> dict[str, object]:
    """Write one complete immutable parent-graph snapshot and return its receipt."""

    repository = _repository(repository)
    parent_number = _positive_issue_number(parent_number)
    parent_endpoint = _issue_endpoint(repository, parent_number)
    raw_children = client.request("GET", f"{parent_endpoint}/sub_issues", paginate=True)
    if not isinstance(raw_children, list) or not raw_children:
        raise GitHubApiError("campaign parent must have at least one sub-issue")
    children = [_normalize_issue(row) for row in raw_children]
    child_numbers = [int(row["number"]) for row in children]
    if len(child_numbers) != len(set(child_numbers)):
        raise GitHubApiError("campaign sub-issues must be unique")
    child_set = set(child_numbers)
    child_packets = {
        int(row["number"]): row for row in raw_children if isinstance(row, dict)
    }
    nodes: list[dict[str, object]] = []
    for number in [parent_number, *child_numbers]:
        endpoint = _issue_endpoint(repository, number)
        payload = (
            client.request("GET", endpoint)
            if number == parent_number
            else child_packets[number]
        )
        packet = _normalize_issue_packet(payload)
        packet["comments"] = _normalize_comments(
            client.request("GET", f"{endpoint}/comments", paginate=True)
        )
        nodes.append(packet)

    blocked_by_edges: set[tuple[int, int]] = set()
    for child_number in child_numbers:
        endpoint = _issue_endpoint(repository, child_number)
        parent_payload = client.request("GET", f"{endpoint}/parent", allow_not_found=True)
        parent = _normalize_issue(parent_payload) if parent_payload is not None else None
        if not isinstance(parent, dict) or int(parent["number"]) != parent_number:
            raise RelationshipVerificationError(
                {
                    "operation": "snapshot",
                    "status": "mismatch",
                    "verified": False,
                    "error": f"issue #{child_number} does not read back parent #{parent_number}",
                }
            )
        blockers = _normalize_many(
            client.request(
                "GET",
                f"{endpoint}/dependencies/blocked_by",
                paginate=True,
            )
        )
        for blocker in blockers:
            blocker_number = int(blocker["number"])
            if blocker_number not in child_set:
                raise GitHubApiError(
                    f"dependency #{blocker_number} -> #{child_number} leaves the campaign graph"
                )
            blocked_by_edges.add((blocker_number, child_number))

    blocking_edges: set[tuple[int, int]] = set()
    for blocker_number in child_numbers:
        endpoint = _issue_endpoint(repository, blocker_number)
        blocking = _normalize_many(
            client.request(
                "GET",
                f"{endpoint}/dependencies/blocking",
                paginate=True,
            )
        )
        blocking_edges.update(
            (blocker_number, int(dependent["number"]))
            for dependent in blocking
            if int(dependent["number"]) in child_set
        )
    if blocked_by_edges != blocking_edges:
        raise RelationshipVerificationError(
            {
                "operation": "snapshot",
                "status": "mismatch",
                "verified": False,
                "error": "dependency directions differ",
                "blocked_by_only": sorted(blocked_by_edges - blocking_edges),
                "blocking_only": sorted(blocking_edges - blocked_by_edges),
            }
        )
    parent_children = [
        int(row["number"])
        for row in client.request("GET", f"{parent_endpoint}/sub_issues", paginate=True)
    ]
    if parent_children != child_numbers:
        raise RelationshipVerificationError(
            {
                "operation": "snapshot",
                "status": "mismatch",
                "verified": False,
                "error": "parent sub-issue read-back differs from the ordered campaign graph",
            }
        )

    artifact = {
        "schema": 1,
        "tracker": "github",
        "repository": repository,
        "observed_at": datetime.now(UTC).isoformat(),
        "parent": parent_number,
        "children": child_numbers,
        "nodes": nodes,
        "edges": [
            {"blocker": blocker, "dependent": dependent}
            for blocker, dependent in sorted(blocked_by_edges)
        ],
    }
    encoded = (json.dumps(artifact, indent=2, sort_keys=True) + "\n").encode()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise GitHubApiError("snapshot output already exists")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_bytes(encoded)
    temporary.replace(output)
    return {
        "schema": 1,
        "operation": "snapshot",
        "status": "complete",
        "verified": True,
        "path": str(output),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "repository": repository,
        "parent": parent_number,
        "children": child_numbers,
    }


def attach_child(
    client: GitHubApi,
    repository: str,
    parent_number: int,
    child_number: int,
) -> dict[str, object]:
    """Attach one native child once, then verify parent and child directions."""

    repository = _repository(repository)
    parent_number = _positive_issue_number(parent_number)
    child_number = _positive_issue_number(child_number)
    if parent_number == child_number:
        raise ValueError("an issue cannot be its own parent")

    child_endpoint = _issue_endpoint(repository, child_number)
    current_parent_payload = client.request(
        "GET",
        f"{child_endpoint}/parent",
        allow_not_found=True,
    )
    current_parent = (
        _normalize_issue(current_parent_payload)
        if current_parent_payload is not None
        else None
    )
    if current_parent is not None and int(current_parent["number"]) != parent_number:
        raise RelationshipConflictError(
            f"issue #{child_number} already has parent "
            f"#{current_parent['number']}"
        )

    status = "reused"
    if current_parent is None:
        child = _normalize_issue(client.request("GET", child_endpoint))
        client.request(
            "POST",
            _issue_endpoint(repository, parent_number, "sub_issues"),
            fields={"sub_issue_id": int(child["id"])},
        )
        status = "created"

    children_observed = _normalize_many(
        client.request(
            "GET",
            _issue_endpoint(repository, parent_number, "sub_issues"),
            paginate=True,
        )
    )
    if status == "created":
        parent_payload = client.request(
            "GET",
            f"{child_endpoint}/parent",
            allow_not_found=True,
        )
        parent_for_child = (
            _normalize_issue(parent_payload)
            if parent_payload is not None
            else None
        )
    else:
        parent_for_child = current_parent
    parent_observed = {
        "repository": repository,
        "issue_number": parent_number,
        "children": children_observed,
    }
    child_observed = {
        "repository": repository,
        "issue_number": child_number,
        "parent": parent_for_child,
    }
    verified = (
        _contains(children_observed, child_number)
        and parent_for_child is not None
        and int(parent_for_child["number"]) == parent_number
    )
    result: dict[str, object] = {
        "operation": "attach-child",
        "status": status if verified else "mismatch",
        "verified": verified,
        "repository": repository,
        "parent_number": parent_number,
        "child_number": child_number,
        "parent": parent_observed,
        "child": child_observed,
    }
    if not verified:
        raise RelationshipVerificationError(result)
    return result


def add_blocker(
    client: GitHubApi,
    repository: str,
    issue_number: int,
    blocker_number: int,
) -> dict[str, object]:
    """Add one native blocker once, then verify both dependency directions."""

    repository = _repository(repository)
    issue_number = _positive_issue_number(issue_number)
    blocker_number = _positive_issue_number(blocker_number)
    if issue_number == blocker_number:
        raise ValueError("an issue cannot block itself")

    blocked_by_endpoint = _issue_endpoint(
        repository,
        issue_number,
        "dependencies/blocked_by",
    )
    current_blockers = _normalize_many(
        client.request("GET", blocked_by_endpoint, paginate=True)
    )
    status = "reused"
    if not _contains(current_blockers, blocker_number):
        blocker = _normalize_issue(
            client.request("GET", _issue_endpoint(repository, blocker_number))
        )
        client.request(
            "POST",
            blocked_by_endpoint,
            fields={"issue_id": int(blocker["id"])},
        )
        status = "created"

    if status == "created":
        blocked_by_observed = _normalize_many(
            client.request("GET", blocked_by_endpoint, paginate=True)
        )
    else:
        blocked_by_observed = current_blockers
    blocking_observed = _normalize_many(
        client.request(
            "GET",
            _issue_endpoint(
                repository,
                blocker_number,
                "dependencies/blocking",
            ),
            paginate=True,
        )
    )
    issue_observed = {
        "repository": repository,
        "issue_number": issue_number,
        "blocked_by": blocked_by_observed,
    }
    blocker_observed = {
        "repository": repository,
        "issue_number": blocker_number,
        "blocking": blocking_observed,
    }
    verified = (
        _contains(blocked_by_observed, blocker_number)
        and _contains(blocking_observed, issue_number)
    )
    result: dict[str, object] = {
        "operation": "add-blocker",
        "status": status if verified else "mismatch",
        "verified": verified,
        "repository": repository,
        "issue_number": issue_number,
        "blocker_number": blocker_number,
        "issue": issue_observed,
        "blocker": blocker_observed,
    }
    if not verified:
        raise RelationshipVerificationError(result)
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Mutate GitHub issue relationships and return normalized "
            "bidirectional read-back."
        )
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--repo", required=True)
    inspect_parser.add_argument("--issue", type=int, required=True)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("--repo", required=True)
    snapshot_parser.add_argument("--parent", type=int, required=True)
    snapshot_parser.add_argument("--out", type=Path, required=True)

    child_parser = subparsers.add_parser("attach-child")
    child_parser.add_argument("--repo", required=True)
    child_parser.add_argument("--parent", type=int, required=True)
    child_parser.add_argument("--child", type=int, required=True)

    blocker_parser = subparsers.add_parser("add-blocker")
    blocker_parser.add_argument("--repo", required=True)
    blocker_parser.add_argument("--issue", type=int, required=True)
    blocker_parser.add_argument("--blocker", type=int, required=True)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    client: GitHubApi | None = None,
) -> int:
    """Run one relationship operation and print exactly one JSON result."""

    args = _parser().parse_args(argv)
    api = client or GhApiClient()
    try:
        if args.operation == "inspect":
            result = inspect_issue(api, args.repo, args.issue)
        elif args.operation == "snapshot":
            result = snapshot_campaign(api, args.repo, args.parent, args.out)
        elif args.operation == "attach-child":
            result = attach_child(api, args.repo, args.parent, args.child)
        else:
            result = add_blocker(api, args.repo, args.issue, args.blocker)
    except RelationshipVerificationError as error:
        print(json.dumps(error.result, indent=2, sort_keys=True))
        return 2
    except (GitHubApiError, RelationshipConflictError, ValueError) as error:
        print(
            json.dumps(
                {
                    "verified": False,
                    "status": "error",
                    "error": str(error),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
