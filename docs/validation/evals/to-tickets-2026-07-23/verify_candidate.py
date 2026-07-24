"""Deterministic Prompt 3 structural checks for the To Tickets candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_FIXTURE_HASHES = {
    "runtime.json": "1da11d50b70313f8f04c16ab40699a90b8fd6a0cad602ae60dfccde39cb6d8fe",
    "tracker-contract.md": "5a860ffb76f82965ca19ad2ad763f8e2db31a12d70540b3e6fe527993898683a",
    "m0.json": "b3cfc9863f2fa8d7c6a0eaa912fa2d6c398eb429eb7a02444c7bf5e29df8e3e7",
    "h1.json": "3e7604d1bb279f0928b524bd5d23348121716e4d8e92e7f470ae975f481ae675",
}
REQUIRED_FIXTURE_FIELDS = {
    "id",
    "worker_prompt",
    "context",
    "source_packet",
    "tracker_state",
    "tracker_observations",
    "source_owner",
    "publication_authority",
    "permitted_tools",
    "permitted_mutations",
    "expected_output_boundary",
}
REQUIRED_SOURCE_FIELDS = {
    "identity",
    "owner",
    "outcome",
    "commitments",
    "acceptance",
    "scope",
    "exclusions",
    "proof",
    "category",
    "parent",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(text: str, tokens: tuple[str, ...], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"{label} missing: {missing}")


def reject(text: str, tokens: tuple[str, ...], label: str) -> None:
    present = [token for token in tokens if token in text]
    if present:
        raise SystemExit(f"{label} unexpectedly contains: {present}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--eval-root", type=Path, required=True)
    parser.add_argument("--m0-skill-sha256", required=True)
    parser.add_argument("--h1-skill-sha256", required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    eval_root = args.eval_root.resolve()
    m0_skill = root / "controls" / "m0" / "SKILL.md"
    h1_skill = root / "SKILL.md"
    m0_policy = root / "controls" / "m0" / "agents" / "openai.yaml"
    h1_policy = root / "agents" / "openai.yaml"

    if sha256(m0_skill) != args.m0_skill_sha256:
        raise SystemExit("M0 SKILL.md identity mismatch")
    if sha256(h1_skill) != args.h1_skill_sha256:
        raise SystemExit("H1 SKILL.md identity mismatch")
    if m0_policy.read_bytes() != h1_policy.read_bytes():
        raise SystemExit("M0/H1 metadata differs")

    m0 = m0_skill.read_text(encoding="utf-8")
    h1 = h1_skill.read_text(encoding="utf-8")
    common = (
        "explicit request to slice settled source",
        "commitment ledger",
        "vertical behavior slice",
        "Ready-for-agent",
        "execution profile",
        "state-boundary matrix",
        "Publish only",
        "then apply parent and dependency relationships",
        "Refetch every created or changed item",
        "$repo-bootstrap",
        "$implement",
        "$parallel-implement",
        "Recommend and stop",
    )
    require(m0, common, "M0")
    require(h1, common, "H1")
    reject(
        m0,
        (
            "proposal awaiting approval",
            "correlation keys",
            "provider-native idempotency",
            "Every included detail must close",
        ),
        "M0",
    )
    require(
        h1,
        (
            "Every included detail must close",
            "proposal awaiting approval",
            "exact approved",
            "provider-native idempotency",
            "correlation keys",
            "before any retry",
        ),
        "H1",
    )
    policy = h1_policy.read_text(encoding="utf-8")
    require(policy, ("allow_implicit_invocation: false",), "metadata")

    fixture_root = eval_root / "fixtures"
    for name, expected in EXPECTED_FIXTURE_HASHES.items():
        path = fixture_root / name
        if sha256(path) != expected:
            raise SystemExit(f"fixture identity mismatch: {name}")

    runtime = json.loads((fixture_root / "runtime.json").read_text(encoding="utf-8"))
    if runtime["model"] != "gpt-5.6-sol" or runtime["reasoning_effort"] != "high":
        raise SystemExit("runtime model/reasoning identity mismatch")
    require(
        json.dumps(runtime),
        ("fresh-context worker", "selected fixture packet", "Root judges"),
        "runtime fixture",
    )

    suites = {
        "m0.json": {f"V-{index:02d}" for index in range(1, 17)},
        "h1.json": {"H1-01", "H1-02", "H1-03"},
    }
    for name, expected_ids in suites.items():
        packets = json.loads((fixture_root / name).read_text(encoding="utf-8"))
        ids = {packet.get("id") for packet in packets}
        if ids != expected_ids or len(packets) != len(expected_ids):
            raise SystemExit(f"fixture ID inventory mismatch: {name}")
        for packet in packets:
            missing = REQUIRED_FIXTURE_FIELDS - set(packet)
            if missing:
                raise SystemExit(f"{packet.get('id')} missing fixture fields: {missing}")
            source_missing = REQUIRED_SOURCE_FIELDS - set(packet["source_packet"])
            if source_missing:
                raise SystemExit(
                    f"{packet['id']} missing source fields: {source_missing}"
                )
            for field in ("commitments", "acceptance"):
                value = packet["source_packet"][field]
                if not isinstance(value, list) or not value:
                    raise SystemExit(f"{packet['id']} has empty source {field}")
            if "rubric" in packet or "expected_weakness" in packet:
                raise SystemExit(f"{packet['id']} leaks root-held evaluator material")
            for field in (
                "worker_prompt",
                "context",
                "tracker_state",
                "source_owner",
                "publication_authority",
                "permitted_mutations",
                "expected_output_boundary",
            ):
                if not isinstance(packet[field], str) or not packet[field].strip():
                    raise SystemExit(f"{packet['id']} has empty {field}")
            for field in ("tracker_observations", "permitted_tools"):
                if not isinstance(packet[field], list) or not packet[field]:
                    raise SystemExit(f"{packet['id']} has empty {field}")

    protocol = (eval_root / "protocol.md").read_text(encoding="utf-8")
    require(
        protocol,
        tuple(EXPECTED_FIXTURE_HASHES.values())
        + ("gpt-5.6-sol", "fresh-context workers", "root-held"),
        "protocol",
    )
    print("to-tickets Prompt 3 candidate structure: PASS")


if __name__ == "__main__":
    main()
