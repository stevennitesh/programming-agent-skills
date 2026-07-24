"""Deterministic pruning proof for review campaign 2026-07-24."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts.skill_pack_contract import tree_hash


BASE = ROOT / ".scratch/deploy-campaigns/2026-07-24-review-f3be70c"
RUNTIME = BASE / "runtime/m0-h1/review"
PROMPT4 = BASE / "evals/prompt4"
EXPECTED_HEAD = "f3be70c31dd8f2ae9f12a75248065ef313790bda"
EXPECTED_TREE = "37a670dbe0748f5f89d7d8e0b61ff30b0241fffd81b1861da5f5838af6dd98c8"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded_sha256(path: Path, begin: bytes, end: bytes) -> str:
    data = path.read_bytes()
    start = data.index(begin) + len(begin)
    stop = data.index(end, start)
    return hashlib.sha256(data[start:stop].replace(b"\r\n", b"\n")).hexdigest()


def normalized_contains(text: str, value: str) -> None:
    assert " ".join(value.split()) in " ".join(text.split()), value


def markdown_gate(path: Path) -> None:
    text = path.read_text("utf-8")
    assert len(re.findall(r"(?m)^```", text)) % 2 == 0, path
    in_fence = False
    table_width: int | None = None
    anchors: set[str] = set()
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            table_width = None
        elif not in_fence and line.startswith("|") and line.endswith("|"):
            width = line.count("|")
            table_width = width if table_width is None else table_width
            assert width == table_width, (path, line)
        else:
            table_width = None
        if not in_fence and line.startswith("#"):
            anchor = re.sub(r"[^a-z0-9 -]", "", line.lstrip("#").strip().lower())
            anchor = re.sub(r"\s+", "-", anchor)
            assert anchor not in anchors, (path, anchor)
            anchors.add(anchor)
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if "://" not in target:
            assert (path.parent / target).resolve().exists(), (path, target)


head = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    cwd=ROOT,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == EXPECTED_HEAD

campaign = json.loads((BASE / "campaign.json").read_text("utf-8"))
candidate = json.loads((BASE / "candidate.json").read_text("utf-8"))
protocol = json.loads((PROMPT4 / "protocol-manifest.json").read_text("utf-8"))
results_path = ROOT / "docs/validation/evals/review-2026-07-24-prompt4/results-manifest.json"
results = json.loads(results_path.read_text("utf-8"))
pruning = campaign["pruning_pass_result"]

assert campaign["campaign"]["pruning_status"] == "complete-pruning-not-needed"
assert campaign["campaign"]["recommended_next_unit"] == "prompt-5"
assert pruning["decision"] == "complete"
assert pruning["disposition"] == "pruning-not-needed"
assert pruning["identity_relationship"] == "current != M0 = H1 = V1 = P1"
assert pruning["complete_cut_audit"] == {
    "instruction_passages_classified": 46,
    "keep": 46,
    "collapse": 0,
    "disclose": 0,
    "delete": 0,
    "clause_map_reused": ".scratch/deploy-campaigns/2026-07-24-review-f3be70c/evals/prompt4/protocol-manifest.json#instruction_passage_map",
}
assert len(pruning["cut_ledger"]) == 2
assert all(item["disposition"].startswith("rejected-") for item in pruning["cut_ledger"])
assert pruning["proof"]["fresh_behavioral_wave"] == "not-run-no-material-cut"

runtime_hash = tree_hash(RUNTIME)
assert runtime_hash == EXPECTED_TREE
for name in ("m0", "h1", "v1", "p1"):
    assert pruning["runtime_identities"][f"{name}_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["p1_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["v1_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["material_cuts"] == []
assert candidate["pruning_pass_result"]["fresh_behavioral_wave"] == (
    "not-run-no-material-cut"
)

assert sha256(BASE / "candidate.json") == pruning["candidate"]["sha256"]
assert sha256(results_path) == campaign["prompt_4_result"]["results"]["sha256"]
assert results["decision"] == "accepted"
assert results["runtime"]["v1_tree_sha256"] == EXPECTED_TREE
assert results["aggregate"]["accepted_case_passes"] == 160
assert results["aggregate"]["accepted_case_outcomes"] == 160
assert results["protected_behavior"]["result"] == "pass"

assert tree_hash(RUNTIME) == protocol["runtime"]["m0_tree_sha256"]
for relative, expected in protocol["runtime"]["files_sha256"].items():
    assert sha256(RUNTIME / relative) == expected
assert len(protocol["instruction_passage_map"]) == 46
for passage in protocol["instruction_passage_map"]:
    path = RUNTIME / passage["surface"].split("#", 1)[0]
    normalized_contains(path.read_text("utf-8"), passage["selector"])

synthesis = ROOT / pruning["synthesis"]["path"]
transcript = ROOT / pruning["transcript"]["path"]
synthesis_hash = bounded_sha256(
    synthesis,
    b"<!-- REVIEW-DEPLOY-DECISION:START -->",
    b"<!-- REVIEW-DEPLOY-DECISION:END -->",
)
assert synthesis_hash == pruning["synthesis"]["bounded_content_sha256"]
assert f"`sha256:{synthesis_hash}`" in synthesis.read_text("utf-8")
assert sha256(synthesis) == pruning["synthesis"]["file_sha256"]
assert sha256(transcript) == pruning["transcript"]["sha256"]

for path in [
    synthesis,
    transcript,
    *sorted(RUNTIME.rglob("*.md")),
]:
    markdown_gate(path)

print(f"head={head}")
print(f"v1_p1_tree_sha256={runtime_hash}")
print("prompt4_acceptance_and_protected_behavior=pass")
print("complete_46_passage_cut_audit=pass")
print("candidate_campaign_synthesis_json_markdown=pass")
