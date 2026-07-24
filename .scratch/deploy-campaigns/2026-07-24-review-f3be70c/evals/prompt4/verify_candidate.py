"""Deterministic Deploy Prompt 3 proof for review campaign 2026-07-24."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from scripts.skill_pack_contract import tree_hash


BASE = ROOT / ".scratch/deploy-campaigns/2026-07-24-review-f3be70c"
RUNTIME = BASE / "runtime/m0-h1/review"
EVAL = BASE / "evals/prompt4"
CAMPAIGN = json.loads((BASE / "campaign.json").read_text("utf-8"))
P3 = CAMPAIGN["prompt_3_construction"]
PROTOCOL = json.loads((EVAL / "protocol-manifest.json").read_text("utf-8"))
CANDIDATE = json.loads((BASE / "candidate.json").read_text("utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def bounded_sha256(path: Path, begin: bytes, end: bytes) -> str:
    data = path.read_bytes()
    start = data.index(begin) + len(begin)
    stop = data.index(end, start)
    return hashlib.sha256(data[start:stop].replace(b"\r\n", b"\n")).hexdigest()


def normalized_contains(text: str, value: str) -> None:
    assert " ".join(value.split()) in " ".join(text.split()), value


assert tree_hash(ROOT / "skills/custom/review") == PROTOCOL["inputs"][
    "current_runtime_tree_sha256"
]
assert canonical_sha256(CAMPAIGN["m0_checkpoint"]) == PROTOCOL["inputs"][
    "m0_checkpoint_sha256"
]
assert canonical_sha256(CAMPAIGN["prompt_2_decision"]) == PROTOCOL["inputs"][
    "prompt2_manifest_sha256"
]
assert canonical_sha256(
    CAMPAIGN["prompt_2_decision"]["m0_runtime_specification"]
) == PROTOCOL["inputs"]["specification_sha256"]
for source in CAMPAIGN["m0_checkpoint"]["local_source_identity_manifest"]:
    assert sha256(ROOT / source["path"]) == source["sha256"], source["path"]
assert sha256(ROOT / CAMPAIGN["prompt_2_decision"]["research"]["path"]) == PROTOCOL[
    "inputs"
]["research_sha256"]
prompt2_transcript = ROOT / PROTOCOL["inputs"]["prompt2_transcript_path"]
assert prompt2_transcript == ROOT / CAMPAIGN["prompt_2_decision"]["transcript"]
assert sha256(prompt2_transcript) == PROTOCOL["inputs"]["prompt2_transcript_sha256"]
prompt2_record = prompt2_transcript.read_text("utf-8")
prompt2_content_sha256 = PROTOCOL["inputs"]["prompt2_content_sha256"]
assert (
    CAMPAIGN["prompt_2_decision"]["synthesis"]["content_sha256"]
    == prompt2_content_sha256
)
assert f"`sha256:{prompt2_content_sha256}`" in prompt2_record
assert "Decision: ready-for-prompt-3" in prompt2_record
transcript = ROOT / P3["transcript"]
transcript_hash = bounded_sha256(
    transcript,
    b"<!-- REVIEW-PROMPT3-DECISION:START -->",
    b"<!-- REVIEW-PROMPT3-DECISION:END -->",
)
assert transcript_hash == P3["transcript_content_sha256"]
assert f"Content fingerprint: `{transcript_hash}`" in transcript.read_text("utf-8")
assert canonical_sha256(P3) == CAMPAIGN["prompt_3_manifest_fingerprint"].removeprefix(
    "sha256:"
)

actual_inventory = sorted(
    path.relative_to(RUNTIME).as_posix()
    for path in RUNTIME.rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
)
runtime = PROTOCOL["runtime"]
assert actual_inventory == runtime["inventory"] == P3["runtime"]["inventory"]
assert tree_hash(RUNTIME) == runtime["m0_tree_sha256"]
assert (
    runtime["m0_tree_sha256"]
    == runtime["h1_tree_sha256"]
    == P3["runtime"]["m0_tree_sha256"]
    == P3["runtime"]["h1_tree_sha256"]
    == CANDIDATE["runtime"]["m0_tree_sha256"]
    == CANDIDATE["runtime"]["h1_tree_sha256"]
)
assert runtime["h1_transformations"] == runtime["h1_contribution_arms"] == []
assert CANDIDATE["runtime"]["h1_transformations"] == []
for relative, expected in runtime["files_sha256"].items():
    assert sha256(RUNTIME / relative) == expected == P3["runtime"]["files_sha256"][
        relative
    ]
for relative in runtime["compatibility_byte_identity"]:
    assert (RUNTIME / relative).read_bytes() == (
        ROOT / "skills/custom/review" / relative
    ).read_bytes(), relative

assert sha256(EVAL / "protocol-manifest.json") == P3["proof_registration"][
    "protocol_sha256"
]
assert P3["candidate_record"]["sha256"] == (
    "b5669778fb0a4e9878af6705f9bb6219e60995737d9b9473f1462f5e9c1ee48b"
)
assert sha256(BASE / "candidate.json") == CAMPAIGN["prompt_4_result"]["candidate"][
    "sha256"
]
worker_ref = PROTOCOL["proof_registration"]["viability_suite"]["worker_fixture"]
root_ref = PROTOCOL["proof_registration"]["viability_suite"]["root_evaluator"]
assert sha256(EVAL / worker_ref["path"]) == worker_ref["sha256"]
assert sha256(EVAL / root_ref["path"]) == root_ref["sha256"]
worker = json.loads((EVAL / worker_ref["path"]).read_text("utf-8"))
evaluator = json.loads((EVAL / root_ref["path"]).read_text("utf-8"))
assert worker["visibility"] == "worker-visible"
assert evaluator["visibility"] == "root-only"
worker_lower = (EVAL / worker_ref["path"]).read_text("utf-8").lower()
for forbidden in (
    '"hypothesis"',
    "expected_m0_weakness",
    "candidate_terms",
    "sample_expectations",
    "critical_failures",
    "conclusions_before_sampling",
):
    assert forbidden not in worker_lower
sample_ids = [sample["id"] for sample in worker["samples"]]
assert len(sample_ids) == len(set(sample_ids)) == 32
assert set(sample_ids) == set(evaluator["sample_expectations"])
assert all(sample["facts"] and sample["family"] for sample in worker["samples"])
assert set(sample["family"] for sample in worker["samples"]) == set(
    PROTOCOL["proof_registration"]["viability_suite"]["families"]
)
assert evaluator["hypothesis"] is None
assert evaluator["expected_m0_weakness"] is None
assert evaluator["candidate_terms"] == evaluator["contribution_arms"] == []
assert PROTOCOL["evaluation_status"] == evaluator["evaluation_status"] == "not-started"

passages = PROTOCOL["instruction_passage_map"]
assert len(passages) == P3["passage_map"]["entry_count"] == 46
assert canonical_sha256(passages) == P3["passage_map"]["sha256"]
assert len({passage["id"] for passage in passages}) == len(passages)
for passage in passages:
    path = RUNTIME / passage["surface"].split("#", 1)[0]
    assert path.is_file(), passage
    normalized_contains(path.read_text("utf-8"), passage["selector"])
    assert passage["origin"] in {
        "frozen-checkpoint",
        "permitted-required-compatibility",
        "permitted-foreign-compatibility",
    }
required = set(CAMPAIGN["prompt_2_decision"]["required_semantic_ids"])
assert required == set(PROTOCOL["semantic_trace"]) == set(P3["semantic_trace"])
for semantic_id in required:
    protocol_passages = PROTOCOL["semantic_trace"][semantic_id]["passages"]
    assert protocol_passages == P3["semantic_trace"][semantic_id]
    assert protocol_passages and PROTOCOL["semantic_trace"][semantic_id]["proof_ids"]
    assert all(
        semantic_id in passage["semantic_ids"]
        for passage in passages
        if passage["id"] in protocol_passages
    )
assert set(PROTOCOL["forbidden_absence_checks"]) == set(
    CAMPAIGN["prompt_2_decision"]["forbidden_semantic_ids"]
) == set(P3["forbidden_absence_proof"]["ids"])

skill = (RUNTIME / "SKILL.md").read_text("utf-8")
finding = (RUNTIME / "FINDING-CONTRACT.md").read_text("utf-8")
metadata = (RUNTIME / "agents/openai.yaml").read_text("utf-8")
all_runtime = "\n".join(
    path.read_text("utf-8") for path in sorted(RUNTIME.rglob("*")) if path.is_file()
)
assert "ADVISORY-CONTRACT" not in skill and "Advisory ID:" not in skill
assert "Keep this ledger in context only" in skill
assert not any("ledger" in path.name.lower() for path in RUNTIME.rglob("*"))
assert "Do not recapture or continue on the changed state." in skill
for phrase in (
    "evidence ladder",
    "major-first",
    "exhaustive-tail",
    "parallel reviewer",
    "fresh reviewer",
    "copied review package",
    "ponytail",
    "removable-line",
):
    assert phrase not in all_runtime.lower()
severity = re.findall(r"(?m)^- `(P[0-9])`:", finding)
assert severity == ["P0", "P1", "P2", "P3"]
assert not any(word in finding for word in ("Critical:", "Important:", "Minor:"))
for literal in (
    "Return boundary: caller",
    "Mutation authority: none",
    "Successor snapshot authority: none",
):
    assert skill.count(literal) == 2
assert "allow_implicit_invocation: true" in metadata
assert "[SMELL-BASELINE.md](SMELL-BASELINE.md) only when" in skill
assert "[FINDING-CONTRACT.md](FINDING-CONTRACT.md)." in skill

blocks = re.findall(r"```text\n(.*?)```", skill, flags=re.DOTALL)
assert len(blocks) == 2
complete_fields = [line.split(":", 1)[0] for line in blocks[0].splitlines() if ":" in line]
incomplete_fields = [
    line.split(":", 1)[0] for line in blocks[1].splitlines() if ":" in line
]
assert complete_fields[0] == "Review status"
assert "Standards findings" in complete_fields and "Spec findings" in complete_fields
assert incomplete_fields == [
    "Review status",
    "Review mode",
    "Fixed point",
    "Snapshot identity",
    "Target",
    "Sources",
    "Covered work",
    "Verified findings",
    "Carried dispositions",
    "Blocker",
    "Skipped work",
    "Residual risk",
    "Drift",
    "Return boundary",
    "Mutation authority",
    "Successor snapshot authority",
]
finding_block = re.search(r"```text\n(ID:.*?)```", finding, flags=re.DOTALL)
assert finding_block
assert [line.rstrip(":") for line in finding_block.group(1).splitlines()] == [
    "ID",
    "Axis",
    "Severity",
    "Location",
    "Anchor",
    "Supported scenario",
    "Evidence",
    "Impact",
    "Blocking: yes | no",
    "Remediation: automatic-in-scope | decision-required | residual-hardening",
    "Required proof",
]

relationships = PROTOCOL["proof_registration"]["relationships"]
relationship_text = {
    "REL-01": (ROOT / "skills/custom/skill-router/SKILL.md").read_text("utf-8"),
    "REL-02": (ROOT / "skills/custom/implement/SKILL.md").read_text("utf-8"),
    "REL-03": (ROOT / "skills/custom/parallel-implement/SKILL.md").read_text("utf-8"),
    "REL-04": skill,
    "REL-05": skill,
}
for relationship in relationships:
    text = relationship_text[relationship["id"]]
    assert "$review" in text or relationship["caller"] == "review"
assert "$convergent-pr-review" in skill and "$audit-codebase" in skill

for path in list(RUNTIME.rglob("*.md")) + [
    ROOT / "docs/validation/transcripts/2026-07-24-review-prompt3-construction.md"
]:
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

print(f"tree_sha256={runtime['m0_tree_sha256']}")
print("input_fingerprints_inventory_hashes_h1_equality=pass")
print("passage_semantic_forbidden_maps=pass")
print("fixtures_isolation_grounding_registration=pass")
print("invocation_relationship_context_machine_contracts=pass")
print("markdown_json_candidate_manifest=pass")
