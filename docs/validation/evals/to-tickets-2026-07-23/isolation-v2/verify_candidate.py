"""Focused structural and evidence checks for To Tickets Prompt 4 V1."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from scripts.skill_pack_contract import tree_hash


EVAL_ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / "skills" / "experimental" / "to-tickets"
M0 = CANDIDATE / "controls" / "m0"
EXPECTED_PACKAGE = "c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9"
EXPECTED_SKILL = "27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9"
EXPECTED_POLICY = "a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94"
EXPECTED_WORKSPACE = "e8d7e55ba09a7174aad65e4e5b4add539cb029d3e3753dee35c366de402f0c05"
EVALUATOR_ONLY = {
    "hypothesis",
    "expected_weakness",
    "rubric",
    "scoring",
    "candidate_terms",
    "conclusions",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_runtime_slot(data: bytes, start: bytes, end: bytes) -> bytes:
    start_index = data.index(start) + len(start)
    end_index = data.index(end)
    return (
        data[:start_index]
        + b"\n<RUNTIME-PACKAGE-SLOT>\n"
        + data[end_index:]
    )


assert tree_hash(M0) == EXPECTED_PACKAGE
assert sha256(M0 / "SKILL.md") == EXPECTED_SKILL
assert sha256(M0 / "agents" / "openai.yaml") == EXPECTED_POLICY
assert sha256(CANDIDATE / "SKILL.md") == EXPECTED_SKILL
assert sha256(CANDIDATE / "agents" / "openai.yaml") == EXPECTED_POLICY
assert (CANDIDATE / "SKILL.md").read_bytes() == (M0 / "SKILL.md").read_bytes()
assert (
    CANDIDATE / "agents" / "openai.yaml"
).read_bytes() == (M0 / "agents" / "openai.yaml").read_bytes()
assert tree_hash(CANDIDATE) == EXPECTED_WORKSPACE

skill = (CANDIDATE / "SKILL.md").read_text(encoding="utf-8")
for rejected in (
    "proposal awaiting approval",
    "provider-native idempotency",
    "correlation keys",
    "Every included detail must close",
):
    assert rejected not in skill, rejected

manifest = json.loads(
    (ROOT / "skills" / "experimental" / "manifest.json").read_text(
        encoding="utf-8"
    )
)
assert (
    manifest["skills"]["to-tickets"]["candidate_sha256"] == EXPECTED_WORKSPACE
)

registry = json.loads((EVAL_ROOT / "registry.json").read_text(encoding="utf-8"))
start = registry["runtime_slot"]["start"].encode()
end = registry["runtime_slot"]["end"].encode()
assert set(registry["clusters"]) == {"cluster-01", "cluster-02", "cluster-03"}
for name, cluster in registry["clusters"].items():
    worker = EVAL_ROOT / "worker-fixtures" / f"{name}.json"
    evaluator = EVAL_ROOT / "evaluator-fixtures" / f"{name}.json"
    assert sha256(worker) == cluster["worker_fixture_sha256"]
    assert sha256(evaluator) == cluster["evaluator_fixture_sha256"]
    worker_data = json.loads(worker.read_text(encoding="utf-8"))
    evaluator_data = json.loads(evaluator.read_text(encoding="utf-8"))
    assert not EVALUATOR_ONLY.intersection(worker_data)
    assert EVALUATOR_ONLY.issubset(evaluator_data)
    assert set(cluster["sample_pairs"]) == {
        f"sample-{index:02d}" for index in range(1, 6)
    }
    for pair in cluster["sample_pairs"].values():
        m0_path = EVAL_ROOT / pair["payloads"]["m0"]["path"]
        h1_path = EVAL_ROOT / pair["payloads"]["h1"]["path"]
        assert sha256(m0_path) == pair["payloads"]["m0"]["sha256"]
        assert sha256(h1_path) == pair["payloads"]["h1"]["sha256"]
        normalized_m0 = normalize_runtime_slot(m0_path.read_bytes(), start, end)
        normalized_h1 = normalize_runtime_slot(h1_path.read_bytes(), start, end)
        assert pair["normalized_equal"] is True
        assert normalized_m0 == normalized_h1
        assert hashlib.sha256(normalized_m0).hexdigest() == pair["normalized_sha256"]

assert set(registry["viability"]) == {
    f"V-{index:02d}" for index in range(1, 17)
}
for case, entry in registry["viability"].items():
    worker = EVAL_ROOT / "worker-fixtures" / "viability" / f"{case}.json"
    evaluator = EVAL_ROOT / "evaluator-fixtures" / "viability" / f"{case}.json"
    payload = EVAL_ROOT / entry["payload_path"]
    capture = ROOT / Path(entry["capture_target"])
    assert sha256(worker) == entry["worker_fixture_sha256"]
    assert sha256(evaluator) == entry["evaluator_fixture_sha256"]
    assert sha256(payload) == entry["payload_sha256"]
    assert capture.is_file() and capture.stat().st_size > 0
    assert not EVALUATOR_ONLY.intersection(
        json.loads(worker.read_text(encoding="utf-8"))
    )

credited = {
    "cluster-01": EVAL_ROOT / "raw" / "current" / "cluster-01",
    "cluster-02-m0": EVAL_ROOT / "raw" / "current" / "cluster-02" / "m0",
    "cluster-02-h1": EVAL_ROOT / "raw" / "current" / "cluster-02" / "h1",
    "cluster-03": EVAL_ROOT / "raw" / "current" / "cluster-03" / "m0",
}
for directory in credited.values():
    captures = sorted(directory.glob("sample-*.md"))
    assert len(captures) == 5
    assert all(path.stat().st_size > 0 for path in captures)

assert (
    EVAL_ROOT
    / "raw"
    / "deviations"
    / "viability-fixture-defect"
    / "V-02-under-specified-source.md"
).is_file()
assert (
    EVAL_ROOT / "raw" / "deviations" / "pre-viability" / "cluster-01"
).is_dir()

results = (EVAL_ROOT / "results.md").read_text(encoding="utf-8")
for token in (
    "Decision: `accepted`",
    "`rejected-no-control-deficit`",
    "`rejected-regression`",
    EXPECTED_PACKAGE,
    EXPECTED_WORKSPACE,
):
    assert token in results, token

print(f"v1_package_sha256={EXPECTED_PACKAGE}")
print(f"v1_skill_sha256={EXPECTED_SKILL}")
print(f"workspace_sha256={EXPECTED_WORKSPACE}")
print("clean_viability_inventory=16")
print("credited_comparison_inventory=20")
print("prompt4_v1_structure_and_evidence=pass")
