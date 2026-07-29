from __future__ import annotations

import importlib.util
import json
import subprocess
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


def load_helper() -> ModuleType:
    assert HELPER.is_file(), "to-tickets must bundle the GitHub relationship helper"
    spec = importlib.util.spec_from_file_location(
        "to_tickets_github_issue_relationships",
        HELPER,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
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
        self.issues = {number: issue(number) for number in numbers}
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
