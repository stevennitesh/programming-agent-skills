from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import (
    campaign_tree_hash,
    compare_payloads,
    lint_worker_fixture,
)


EPOCH = Path(__file__).resolve().parent
PROTOCOL_DIR = EPOCH / "evals" / "prompt4"
M0 = EPOCH / "m0-runtime"
H1 = EPOCH / "h1-runtime"
EXPECTED_INVENTORY = {
    "BEHAVIOR-EVALS.md",
    "GLOSSARY.md",
    "SKILL.md",
    "agents/openai.yaml",
}
M0_HASH = "175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341"
H1_HASH = "95c45d53a6e853bad3a74981634b2bdf8c0e3bc7fc8a11f5a568fc3b0efad577"
CHECKPOINT_HASH = "33b6bb9b9e4a5571f92552ada39870588b4272a62d4111bfaef0b1b00c8d0aac"
H1_EXPRESSION = (
    "When observed runs miss must-have branch material behind a weak pointer, "
    "sharpen it to name the target, condition, and load/apply action; inline "
    "only if a fresh entry-positive check still misses."
)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path: Path) -> set[str]:
    return {
        item.relative_to(path).as_posix()
        for item in path.rglob("*")
        if item.is_file()
    }


def normalized(text: str) -> str:
    return " ".join(text.split())


def marker_hash(path: Path, start_marker: str, end_marker: str) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    start = text.index(start_marker)
    end = text.index(end_marker, start) + len(end_marker)
    return hashlib.sha256(text[start:end].encode("utf-8")).hexdigest()


def check_runtime(path: Path, expected_hash: str) -> None:
    assert inventory(path) == EXPECTED_INVENTORY
    assert campaign_tree_hash(path)["sha256"] == expected_hash
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    package = "\n".join(
        item.read_text(encoding="utf-8")
        for item in path.rglob("*")
        if item.is_file()
    )
    links = set(re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", skill))
    assert links == {"GLOSSARY.md", "BEHAVIOR-EVALS.md"}
    assert all((path / link).is_file() for link in links)
    assert package.count("allow_implicit_invocation: true") == 1
    assert "fork_turns" not in package
    skill_flat = normalized(skill)
    for semantic in (
        "Choose exactly one operation",
        "Before judgment or mutation, resolve the target, canonical source, operation, and mutation boundary",
        "Inspect and classify every surface capable of changing the requested behavior",
        "Give each behavior and relationship one owner",
        "Keep common guidance inline",
        "Keep clauses that change intended behavior",
        "Use exact read-back and deterministic checks",
        "Return `complete`, `partial`, or `blocked`",
        "Complete only when every affected semantic and surface has one home",
    ):
        assert semantic in skill_flat


assert file_hash(EPOCH / "m0-checkpoint.json") == CHECKPOINT_HASH
check_runtime(M0, M0_HASH)
check_runtime(H1, H1_HASH)

freeze = load_json(EPOCH / "m0-freeze.json")
assert freeze["package"]["sha256"] == M0_HASH
assert freeze["sole_construction_authority"]["sha256"] == CHECKPOINT_HASH
assert not any(freeze["construction_boundary"].values())

changed_files = []
for relative in sorted(EXPECTED_INVENTORY):
    if (M0 / relative).read_bytes() != (H1 / relative).read_bytes():
        changed_files.append(relative)
assert changed_files == ["GLOSSARY.md"]
m0_glossary = normalized((M0 / "GLOSSARY.md").read_text(encoding="utf-8"))
h1_glossary = normalized((H1 / "GLOSSARY.md").read_text(encoding="utf-8"))
assert H1_EXPRESSION not in m0_glossary
assert h1_glossary.count(H1_EXPRESSION) == 1
assert len(H1_EXPRESSION.split()) == 30
assert h1_glossary.index("**Information hierarchy:**") < h1_glossary.index(H1_EXPRESSION)
assert h1_glossary.index(H1_EXPRESSION) < h1_glossary.index("**Pruning:**")

protocol = load_json(PROTOCOL_DIR / "protocol-manifest.json")
assert protocol["behavioral_evaluation_status"] == "not-started"
assert protocol["runtime"]["m0"]["tree_sha256"] == M0_HASH
assert protocol["runtime"]["h1"]["tree_sha256"] == H1_HASH
semantic_trace = protocol["semantic_trace"]
assert set(semantic_trace) == {
    *(f"M0-{number:02d}" for number in range(1, 11)),
    "H1-POINTER-REPAIR-01",
}
passages = {item["id"]: item for item in protocol["instruction_passage_map"]}
for semantic_id, trace in semantic_trace.items():
    assert trace["owner"]
    assert trace["passages"]
    assert trace["proof_ids"]
    assert all(passage in passages for passage in trace["passages"])
for passage in passages.values():
    runtime = H1 if passage["runtime"] == "H1" else M0
    surface = passage["surface"].split("#", 1)[0]
    assert passage["selector"] in normalized(
        (runtime / surface).read_text(encoding="utf-8")
    ), (
        passage["id"],
        passage["selector"],
    )

registration = protocol["proof_registration"]
assert len(registration["m0_viability_suite"]) == 11
cluster = registration["h1_cluster"]
assert cluster["minimum_m0_entry_positive_samples"] >= 5
assert cluster["minimum_h1_entry_positive_samples_if_opened"] >= 5
assert cluster["wrong_condition_pairs_after_entry_gate"] >= 1
assert "Fewer than four of five M0 controls score 8" in cluster["open_h1_gate"]
assert protocol["prior_evidence"]["predecessor_c0_g04"] == "historical-admission-only"
assert protocol["prior_evidence"]["reuse_for_prompt4_sampling"] == "forbidden"
assert set(protocol["forbidden_absence_checks"]) == {
    "FORBID-DIRECT-C0-G04-BYTE-RESTORE",
    "FORBID-INLINE-BEFORE-PERSISTENT-MISS",
    "FORBID-WORKING-POINTER-CHURN",
    "FORBID-SECOND-H1-CANDIDATE",
    "FORBID-HISTORICAL-EVIDENCE-AS-CURRENT-PROOF",
    "FORBID-FOREIGN-AUTHORITY-EXPANSION",
}

worker_path = PROTOCOL_DIR / "worker-fixture.json"
root_path = PROTOCOL_DIR / "root-only-evaluation.json"
lint_map_path = PROTOCOL_DIR / "fixture-lint-map.json"
assert lint_worker_fixture(worker_path) == {"status": "ok", "case_count": 2}
worker = load_json(worker_path)
root_only = load_json(root_path)
lint_map = load_json(lint_map_path)
worker_text = worker_path.read_text(encoding="utf-8")
for forbidden_key in (
    '"hypothesis"',
    '"expected_m0_weakness"',
    '"candidate_terms"',
    '"entry_positive_rubric"',
    '"conclusions"',
):
    assert forbidden_key not in worker_text
fact_ids = {
    fact["id"]
    for case in worker["cases"]
    for fact in case["facts"]
}
for rubric in (
    root_only["entry_positive_rubric"]["criteria"],
    root_only["wrong_condition_rubric"]["criteria"],
):
    for criterion in rubric:
        assert criterion["worker_sources"]
        assert set(criterion["worker_sources"]) <= fact_ids
        assert lint_map["criterion_grounding"][criterion["id"]]
for requested in worker["fixed_execution"]["requested_output"]:
    assert lint_map["requested_output_grounding"][requested]

payloads = PROTOCOL_DIR / "payloads"
entry = compare_payloads(
    worker_path,
    "EP-01",
    payloads / "entry-positive-m0.json",
    payloads / "entry-positive-h1.json",
)
wrong = compare_payloads(
    worker_path,
    "WC-01",
    payloads / "wrong-condition-m0.json",
    payloads / "wrong-condition-h1.json",
)
assert entry["shared_payload_sha256"] == (
    "f4ea07177d332bd5734b62179b944fbbbb3d01594b2d7cdb7630b9397bad2852"
)
assert wrong["shared_payload_sha256"] == (
    "0d56d2fff56eb70e90844f71de33604fe8c1d8039e3e79e8ef3ffdced67ce120"
)

for payload_path in payloads.glob("*.json"):
    payload = load_json(payload_path)
    runtime = payload["runtime"]
    resolved = (payload_path.parent / runtime["path"]).resolve()
    assert resolved in {M0.resolve(), H1.resolve()}
    assert campaign_tree_hash(resolved)["sha256"] == runtime["tree_sha256"]

candidate = load_json(EPOCH / "candidate.json")
assert candidate["decision"] == "ready-for-prompt-4"
assert candidate["runtime"]["m0"]["tree_sha256"] == M0_HASH
assert candidate["runtime"]["h1"]["tree_sha256"] == H1_HASH
assert [item["id"] for item in candidate["runtime"]["h1_transformations"]] == [
    "H1-POINTER-REPAIR-01"
]
assert candidate["candidate_specific_proof_plan"]["behavioral_evaluation_status"] == "not-started"

manifest = load_json(EPOCH / "campaign-manifest.json")
assert manifest["active_unit"] == "prompt-3"
assert manifest["decision"] == "ready-for-prompt-4"
assert manifest["runtime_identities"]["M0"]["identity"] == M0_HASH
assert manifest["runtime_identities"]["H1"]["identity"] == H1_HASH
assert manifest["recommended_next_unit"] == "Deploy Prompt 4"
assert manifest["successor_started"] is False
identities = manifest["artifact_identities"]
assert identities["m0_checkpoint"]["sha256"] == file_hash(EPOCH / "m0-checkpoint.json")
assert identities["m0_freeze"]["sha256"] == file_hash(EPOCH / "m0-freeze.json")
assert identities["candidate_record"]["sha256"] == file_hash(EPOCH / "candidate.json")
assert identities["prompt4_protocol"]["sha256"] == file_hash(
    PROTOCOL_DIR / "protocol-manifest.json"
)
assert identities["prompt3_verifier"]["sha256"] == file_hash(Path(__file__))
transcript = ROOT / manifest["stage_capsule"]["path"]
assert identities["prompt3_transcript"]["sha256"] == file_hash(transcript)
assert identities["prompt3_transcript"]["stage_capsule_sha256"] == marker_hash(
    transcript,
    manifest["stage_capsule"]["start_marker"],
    manifest["stage_capsule"]["end_marker"],
)
assert manifest["stage_capsule"]["sha256"] == identities["prompt3_transcript"][
    "stage_capsule_sha256"
]

print("prompt3 candidate-aware compatibility preflight: pass")
