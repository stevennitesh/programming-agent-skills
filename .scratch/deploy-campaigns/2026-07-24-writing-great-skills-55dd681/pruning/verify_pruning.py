"""Deterministic pruning proof for writing-great-skills campaign."""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash


BASE = ROOT / ".scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681"
RUNTIME = BASE / "runtime/m0/writing-great-skills"
PROTOCOL = BASE / "protocol/prompt4/protocol-manifest.json"
PROMPT4_RESULTS = (
    ROOT
    / "docs/validation/evals/writing-great-skills-2026-07-24-prompt4/results-manifest.json"
)
PRUNING_RESULTS = (
    ROOT
    / "docs/validation/evals/writing-great-skills-2026-07-24-pruning/results-manifest.json"
)
SYNTHESIS = ROOT / "docs/synthesis/skills/writing-great-skills.md"
TRANSCRIPT = (
    ROOT
    / "docs/validation/transcripts/2026-07-24-writing-great-skills-pruning.md"
)
EXPECTED_HEAD = "55dd6818182caf75e85de713a13ed76996336a27"
EXPECTED_TREE = "559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bounded_sha(path: Path, begin: str, end: str) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index(begin) + len(begin)
    stop = text.index(end, start)
    return hashlib.sha256(text[start:stop].replace("\r\n", "\n").encode()).hexdigest()


def normalized_contains(text: str, value: str) -> None:
    assert " ".join(value.split()) in " ".join(text.split()), value


def markdown_gate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
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

campaign = load(BASE / "campaign.json")
candidate = load(BASE / "candidate.json")
protocol = load(PROTOCOL)
prompt4 = load(PROMPT4_RESULTS)
results = load(PRUNING_RESULTS)
pruning = campaign["pruning_pass_result"]

assert campaign["active_unit"] == "pruning-pass"
assert campaign["decision"]["status"] == "complete"
assert campaign["decision"]["disposition"] == "pruning-not-needed"
assert campaign["decision"]["recommended_next_unit"] == "prompt-5"
assert pruning["decision"] == "complete"
assert pruning["disposition"] == "pruning-not-needed"
assert pruning["complete_cut_audit"] == {
    "instruction_passages_classified": 41,
    "keep": 41,
    "collapse": 0,
    "disclose": 0,
    "delete": 0,
    "clause_map_reused": (
        ".scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681/"
        "protocol/prompt4/protocol-manifest.json#instruction_passage_map"
    ),
}
assert len(pruning["cut_ledger"]) == 3
assert all(item["disposition"].startswith("rejected-") for item in pruning["cut_ledger"])
assert pruning["proof"]["fresh_behavioral_wave"] == "not-run-no-material-cut"

runtime_hash = campaign_tree_hash(RUNTIME)["sha256"]
assert runtime_hash == EXPECTED_TREE
for name in ("m0", "rederived_h1", "v1", "p1"):
    assert pruning["runtime_identities"][f"{name}_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["v1_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["p1_tree_sha256"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["material_cuts"] == []
assert results["runtime"]["v1_tree_sha256"] == EXPECTED_TREE
assert results["runtime"]["p1_tree_sha256"] == EXPECTED_TREE
assert results["passage_classification"]["total"] == 41
assert sha(BASE / "candidate.json") == pruning["candidate"]["sha256"]
assert sha(PRUNING_RESULTS) == pruning["results"]["sha256"]
assert sha(ROOT / pruning["decision_record"]["path"]) == pruning["decision_record"]["sha256"]
assert sha(SYNTHESIS) == pruning["synthesis"]["file_sha256"]
assert bounded_sha(
    SYNTHESIS,
    "<!-- WRITING-GREAT-SKILLS-DEPLOY-DECISION:START -->",
    "<!-- WRITING-GREAT-SKILLS-DEPLOY-DECISION:END -->",
) == pruning["synthesis"]["bounded_content_sha256"]
assert sha(TRANSCRIPT) == pruning["transcript"]["sha256"]
assert bounded_sha(
    TRANSCRIPT,
    "<!-- BEGIN PRUNING DECISION -->",
    "<!-- END PRUNING DECISION -->",
) == pruning["transcript"]["decision_capsule_sha256"]
manifest_for_hash = dict(campaign)
manifest_for_hash.pop("artifact_identities")
manifest_hash = hashlib.sha256(
    json.dumps(
        manifest_for_hash,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
).hexdigest()
assert manifest_hash == campaign["artifact_identities"]["campaign_manifest"]["sha256"]

assert prompt4["prompt4_decision"] == "accepted"
assert prompt4["final_runtime"]["v1_tree_sha256"] == EXPECTED_TREE
assert prompt4["m0_viability"]["valid_count"] == 3
assert prompt4["h1_contribution"]["entry_positive_counts"]["m0"] == 6
assert prompt4["h1_contribution"]["paired_effect"]["protected_behavior_regressions"] == 0

assert protocol["runtime"]["m0"]["tree_sha256"] == EXPECTED_TREE
assert len(protocol["instruction_passage_map"]) == 41
for passage in protocol["instruction_passage_map"]:
    path = RUNTIME / passage["surface"].split("#", 1)[0]
    normalized_contains(path.read_text(encoding="utf-8"), passage["selector"])

assert TRANSCRIPT.read_text(encoding="utf-8").count("<!-- BEGIN PRUNING DECISION -->") == 1
assert TRANSCRIPT.read_text(encoding="utf-8").count("<!-- END PRUNING DECISION -->") == 1
for path in [SYNTHESIS, TRANSCRIPT, ROOT / "docs/validation/evals/writing-great-skills-2026-07-24-pruning/decision.md", *sorted(RUNTIME.rglob("*.md"))]:
    markdown_gate(path)

print(f"head={head}")
print(f"v1_p1_tree_sha256={runtime_hash}")
print("prompt4_acceptance_and_protected_behavior=pass")
print("complete_41_passage_cut_audit=pass")
print("candidate_campaign_synthesis_json_markdown=pass")
