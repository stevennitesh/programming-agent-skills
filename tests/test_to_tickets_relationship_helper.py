from __future__ import annotations

import importlib.util
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest


ROOT = Path(__file__).resolve().parents[1]
HELPER = (
    ROOT
    / "skills"
    / "custom"
    / "to-tickets"
    / "scripts"
    / "github_issue_relationships.py"
)
LEDGER = ROOT / "skills/custom/parallel-implement/scripts/run_ledger.py"


def load_helper() -> ModuleType:
    assert HELPER.is_file(), "to-tickets must bundle the GitHub relationship helper"
    spec = importlib.util.spec_from_file_location(
        "to_tickets_github_issue_relationships",
        HELPER,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior
    return module


def issue(number: int, *, state: str = "open") -> dict[str, object]:
    return {
        "number": number,
        "id": number * 100,
        "state": state,
        "state_reason": "completed" if state == "closed" else None,
        "html_url": f"https://github.com/acme/widgets/issues/{number}",
    }


class FakeGitHubApi:
    """In-memory substitute for GitHub's issue-relationship REST boundary."""

    def __init__(
        self,
        numbers: list[int],
        *,
        parents: dict[int, int] | None = None,
        blockers: dict[int, set[int]] | None = None,
        apply_mutations: bool = True,
    ) -> None:
        self.issues = {
            number: {
                **issue(number),
                "title": f"Issue {number}",
                "body": f"Body {number}",
                "labels": [{"name": "agent-ready"}],
                "assignees": [{"login": "worker"}],
            }
            for number in numbers
        }
        self.parents = dict(parents or {})
        self.blockers = {
            number: set(values) for number, values in (blockers or {}).items()
        }
        self.apply_mutations = apply_mutations
        self.calls: list[dict[str, object]] = []

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        fields: dict[str, int] | None = None,
        paginate: bool = False,
        allow_not_found: bool = False,
    ) -> Any:
        self.calls.append(
            {
                "method": method,
                "endpoint": endpoint,
                "fields": fields,
                "paginate": paginate,
                "allow_not_found": allow_not_found,
            }
        )
        parts = endpoint.split("/")
        issue_number = int(parts[4])
        suffix = "/".join(parts[5:])

        if method == "GET" and not suffix:
            return self.issues[issue_number]
        if method == "GET" and suffix == "comments":
            assert paginate
            return [
                {
                    "id": issue_number * 1000,
                    "user": {"login": "author"},
                    "body": f"Comment {issue_number}",
                    "created_at": "2026-08-02T00:00:00Z",
                    "updated_at": "2026-08-02T00:00:00Z",
                    "html_url": f"https://github.com/acme/widgets/issues/{issue_number}#issuecomment-1",
                }
            ]
        if method == "GET" and suffix == "parent":
            parent = self.parents.get(issue_number)
            if parent is None:
                assert allow_not_found
                return None
            return self.issues[parent]
        if method == "GET" and suffix == "sub_issues":
            assert paginate
            children = [
                self.issues[child]
                for child, parent in self.parents.items()
                if parent == issue_number
            ]
            return list(reversed(children))
        if method == "GET" and suffix == "dependencies/blocked_by":
            assert paginate
            return [
                self.issues[blocker]
                for blocker in reversed(
                    sorted(self.blockers.get(issue_number, set()))
                )
            ]
        if method == "GET" and suffix == "dependencies/blocking":
            assert paginate
            return [
                self.issues[dependent]
                for dependent, blockers in sorted(
                    self.blockers.items(),
                    reverse=True,
                )
                if issue_number in blockers
            ]
        if method == "POST" and suffix == "sub_issues":
            assert fields is not None
            child_id = fields["sub_issue_id"]
            child = next(
                number
                for number, payload in self.issues.items()
                if payload["id"] == child_id
            )
            if self.apply_mutations:
                self.parents[child] = issue_number
            return self.issues[child]
        if method == "POST" and suffix == "dependencies/blocked_by":
            assert fields is not None
            blocker_id = fields["issue_id"]
            blocker = next(
                number
                for number, payload in self.issues.items()
                if payload["id"] == blocker_id
            )
            if self.apply_mutations:
                self.blockers.setdefault(issue_number, set()).add(blocker)
            return self.issues[blocker]
        raise AssertionError((method, endpoint, fields))


def test_inspect_normalizes_all_relationship_directions() -> None:
    helper = load_helper()
    api = FakeGitHubApi(
        [10, 20, 30, 40, 50],
        parents={20: 10, 30: 20},
        blockers={20: {40}, 50: {20}},
    )

    observed = helper.inspect_issue(api, "acme/widgets", 20)

    assert observed == {
        "repository": "acme/widgets",
        "issue": issue(20),
        "parent": issue(10),
        "children": [issue(30)],
        "blocked_by": [issue(40)],
        "blocking": [issue(50)],
    }


def test_snapshot_campaign_writes_one_complete_verified_graph(tmp_path: Path) -> None:
    helper = load_helper()
    api = FakeGitHubApi(
        [10, 20, 30],
        parents={20: 10, 30: 10},
        blockers={30: {20}},
    )
    output = tmp_path / "run" / "tracker-snapshot.json"

    receipt = helper.snapshot_campaign(api, "acme/widgets", 10, output)

    snapshot = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["schema"] == 1
    assert receipt["path"] == str(output.resolve())
    assert receipt["sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    assert snapshot["children"] == [30, 20]
    assert [node["number"] for node in snapshot["nodes"]] == [10, 30, 20]
    assert snapshot["nodes"][1]["body"] == "Body 30"
    assert snapshot["nodes"][1]["comments"][0]["body"] == "Comment 30"
    assert snapshot["edges"] == [{"blocker": 20, "dependent": 30}]
    assert len(api.calls) == 12


def test_snapshot_receipt_directly_starts_the_parallel_ledger(tmp_path: Path) -> None:
    helper = load_helper()
    api = FakeGitHubApi([10, 20], parents={20: 10})
    run = tmp_path / "run"
    receipt = helper.snapshot_campaign(
        api, "acme/widgets", 10, run / "tracker-snapshot.json"
    )
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Skill Tests"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "skills@example.test"], cwd=repo, check=True)
    (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
    subprocess.run(["git", "add", "tracked.txt"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    scope = tmp_path / "scope.json"
    scope.write_text(
        json.dumps(
            {
                "root_actor_id": "root-agent",
                "caller_id": "caller",
                "parent_claim": {
                    "state": "retained",
                    "work_item": "10",
                    "owner": "root-agent",
                    "token": "claim-10",
                    "readback": "retained",
                },
                "tracker_snapshot": receipt,
                "charter": {"id": "charter", "outcome": "deliver"},
            }
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(LEDGER),
            "start",
            "--run",
            str(run),
            "--repo",
            str(repo),
            "--in",
            str(scope),
        ],
        text=True,
        capture_output=True,
    )
    packet = json.loads(result.stdout)
    assert result.returncode == 0, packet
    assert packet["awaiting"]["action"] == "select-frontier"


def test_snapshot_campaign_never_overwrites_frozen_output(tmp_path: Path) -> None:
    helper = load_helper()
    api = FakeGitHubApi([10, 20], parents={20: 10})
    output = tmp_path / "snapshot.json"
    helper.snapshot_campaign(api, "acme/widgets", 10, output)
    frozen = output.read_bytes()
    with pytest.raises(helper.GitHubApiError, match="already exists"):
        helper.snapshot_campaign(api, "acme/widgets", 10, output)
    assert output.read_bytes() == frozen


def test_snapshot_campaign_rejects_native_child_order_drift(tmp_path: Path) -> None:
    helper = load_helper()

    class ReorderedApi(FakeGitHubApi):
        reads = 0

        def request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
            value = super().request(method, endpoint, **kwargs)
            if method == "GET" and endpoint.endswith("/10/sub_issues"):
                self.reads += 1
                if self.reads == 2:
                    return list(reversed(value))
            return value

    api = ReorderedApi([10, 20, 30], parents={20: 10, 30: 10})
    with pytest.raises(helper.RelationshipVerificationError, match="ordered campaign graph"):
        helper.snapshot_campaign(api, "acme/widgets", 10, tmp_path / "snapshot.json")


@pytest.mark.parametrize("hidden_direction", ("blocked_by", "blocking"))
def test_snapshot_campaign_rejects_asymmetric_dependencies(
    tmp_path: Path,
    hidden_direction: str,
) -> None:
    helper = load_helper()

    class AsymmetricApi(FakeGitHubApi):
        def request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
            if method == "GET" and endpoint.endswith(
                f"/dependencies/{hidden_direction}"
            ):
                super().request(method, endpoint, **kwargs)
                return []
            return super().request(method, endpoint, **kwargs)

    api = AsymmetricApi(
        [10, 20, 30],
        parents={20: 10, 30: 10},
        blockers={30: {20}},
    )
    with pytest.raises(helper.RelationshipVerificationError, match="directions differ"):
        helper.snapshot_campaign(api, "acme/widgets", 10, tmp_path / "snapshot.json")


def test_attach_child_is_idempotent_and_verifies_both_directions() -> None:
    helper = load_helper()
    api = FakeGitHubApi([10, 20])

    created = helper.attach_child(api, "acme/widgets", 10, 20)
    reused = helper.attach_child(api, "acme/widgets", 10, 20)

    assert created["status"] == "created"
    assert reused["status"] == "reused"
    assert created["verified"] is True
    assert created["parent"]["children"] == [issue(20)]
    assert created["child"]["parent"] == issue(10)
    posts = [
        call
        for call in api.calls
        if call["method"] == "POST"
        and str(call["endpoint"]).endswith("/sub_issues")
    ]
    assert posts == [
        {
            "method": "POST",
            "endpoint": "repos/acme/widgets/issues/10/sub_issues",
            "fields": {"sub_issue_id": 2000},
            "paginate": False,
            "allow_not_found": False,
        }
    ]
    assert len(api.calls) <= 8


def test_add_blocker_is_idempotent_and_verifies_both_directions() -> None:
    helper = load_helper()
    api = FakeGitHubApi([20, 40])

    created = helper.add_blocker(api, "acme/widgets", 20, 40)
    reused = helper.add_blocker(api, "acme/widgets", 20, 40)

    assert created["status"] == "created"
    assert reused["status"] == "reused"
    assert created["verified"] is True
    assert created["issue"]["blocked_by"] == [issue(40)]
    assert created["blocker"]["blocking"] == [issue(20)]
    posts = [
        call
        for call in api.calls
        if call["method"] == "POST"
        and str(call["endpoint"]).endswith("/dependencies/blocked_by")
    ]
    assert posts == [
        {
            "method": "POST",
            "endpoint": "repos/acme/widgets/issues/20/dependencies/blocked_by",
            "fields": {"issue_id": 4000},
            "paginate": False,
            "allow_not_found": False,
        }
    ]
    assert len(api.calls) <= 8


@pytest.mark.parametrize(
    ("operation", "args"),
    (
        ("attach_child", ("acme/widgets", 10, 20)),
        ("add_blocker", ("acme/widgets", 20, 40)),
    ),
)
def test_mutation_mismatch_returns_normalized_recovery_state(
    operation: str,
    args: tuple[object, ...],
) -> None:
    helper = load_helper()
    api = FakeGitHubApi([10, 20, 40], apply_mutations=False)

    with pytest.raises(helper.RelationshipVerificationError) as caught:
        getattr(helper, operation)(api, *args)

    assert caught.value.result["verified"] is False
    assert caught.value.result["status"] == "mismatch"
    assert caught.value.result["repository"] == "acme/widgets"


def test_gh_adapter_uses_typed_fields_and_flattens_paginated_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    helper = load_helper()
    calls: list[list[str]] = []

    def run(
        command: list[str],
        **_: object,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps([[issue(20)], [issue(30)]]),
            stderr="",
        )

    monkeypatch.setattr(helper.subprocess, "run", run)
    client = helper.GhApiClient()

    observed = client.request(
        "POST",
        "repos/acme/widgets/issues/10/sub_issues",
        fields={"sub_issue_id": 2000},
        paginate=True,
    )

    assert observed == [issue(20), issue(30)]
    assert calls == [
        [
            "gh",
            "api",
            "--method",
            "POST",
            "--paginate",
            "--slurp",
            "-F",
            "sub_issue_id=2000",
            "repos/acme/widgets/issues/10/sub_issues",
        ]
    ]


def test_cli_prints_one_normalized_json_result(capsys: pytest.CaptureFixture[str]) -> None:
    helper = load_helper()
    api = FakeGitHubApi([20, 40], blockers={20: {40}})

    status = helper.main(
        ["inspect", "--repo", "acme/widgets", "--issue", "20"],
        client=api,
    )

    assert status == 0
    assert json.loads(capsys.readouterr().out) == helper.inspect_issue(
        api,
        "acme/widgets",
        20,
    )
