from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash, compare_payloads, lint_worker_fixture


EPOCH = Path(__file__).resolve().parent
PROMPT4 = EPOCH / "evals" / "prompt4"
M0 = EPOCH / "m0-runtime"
H1 = EPOCH / "h1-runtime"
RESULTS = (
    ROOT
    / "docs/validation/evals/"
    / "writing-great-skills-2026-07-24-7d0da40-prompt4/results-manifest.json"
)
SYNTHESIS = ROOT / "docs/synthesis/skills/writing-great-skills.md"
TRANSCRIPT = (
    ROOT
    / "docs/validation/transcripts/"
    / "2026-07-24-writing-great-skills-7d0da40-prompt4-evaluation.md"
)

M0_HASH = "175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341"
H1_HASH = "95c45d53a6e853bad3a74981634b2bdf8c0e3bc7fc8a11f5a568fc3b0efad577"
PROTOCOL_HASH = "abec7ab79e589900ce22de33db02684c1285ad718b3466e1205f902b3076a36d"
RESULTS_HASH = "ece74b8484a5d3462a4fe84fc8a6d80b5b6c5907c7ca9ff16784e67113dc593a"
CANDIDATE_HASH = "d31949cd53b53a7e4f7b96b4be17ba77266e48ef4bf1c7eac91b78182158fe5f"
SYNTHESIS_MARKER_HASH = "d209216030556da78d90e054de67035d4e3bfc91d1bf6ec4076fbf282c016055"
TRANSCRIPT_CAPSULE_HASH = "10ce4c30f2baa0225d11853bf5f9c751184766ffd005cdf40197d35aea8084b8"
OUTPUT_HASHES = {
    "M0-EP-01.md": "2f6a218d38cc6c22e14987e5a400cc135600e619cc240818d4b0bcaf879e5993",
    "M0-EP-02.md": "73b98a90b8b6faf11bcea06dcdc5facc57f21462c6897cbc43edf2a2a4da3d36",
    "M0-EP-03.md": "7b046fc27987827ed07b9bf83904d160fd9c1a216e8445999910df15b6272c3c",
    "M0-EP-04.md": "ef9da522cf948dafbf67a01c21d8f2c0e996480179d4f44aefb56f71eea70d95",
    "M0-EP-05.md": "180cef0d8f9194c4eeb4b2b519942599d800725d58ccbd1034a9c7e0d0bbf1ed",
}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def marker_hash(path: Path, start: str, end: str) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    bounded = text[text.index(start) : text.index(end) + len(end)]
    return hashlib.sha256(bounded.encode("utf-8")).hexdigest()


assert campaign_tree_hash(M0)["sha256"] == M0_HASH
assert campaign_tree_hash(H1)["sha256"] == H1_HASH
assert file_hash(PROMPT4 / "protocol-manifest.json") == PROTOCOL_HASH
assert file_hash(RESULTS) == RESULTS_HASH
assert file_hash(EPOCH / "candidate.json") == CANDIDATE_HASH
assert marker_hash(
    SYNTHESIS,
    "<!-- WRITING-GREAT-SKILLS-DEPLOY-DECISION:START -->",
    "<!-- WRITING-GREAT-SKILLS-DEPLOY-DECISION:END -->",
) == SYNTHESIS_MARKER_HASH
assert marker_hash(
    TRANSCRIPT,
    "<!-- DEPLOY-STAGE-CAPSULE:prompt4:start -->",
    "<!-- DEPLOY-STAGE-CAPSULE:prompt4:end -->",
) == TRANSCRIPT_CAPSULE_HASH

assert lint_worker_fixture(PROMPT4 / "worker-fixture.json") == {
    "status": "ok",
    "case_count": 2,
}
comparison = compare_payloads(
    PROMPT4 / "worker-fixture.json",
    "EP-01",
    PROMPT4 / "payloads/entry-positive-m0.json",
    PROMPT4 / "payloads/entry-positive-h1.json",
)
assert comparison["shared_payload_sha256"] == (
    "f4ea07177d332bd5734b62179b944fbbbb3d01594b2d7cdb7630b9397bad2852"
)

results = load_json(RESULTS)
assert results["prompt4_decision"] == "accepted"
assert results["h1_disposition"] == "reject-no-control-deficit"
assert results["m0_viability"]["status"] == "passed"
assert len(results["m0_viability"]["proof_coverage"]) == 11
assert all(item["result"] == "pass" for item in results["m0_viability"]["proof_coverage"])
contribution = results["h1_contribution"]
assert contribution["m0"]["scores"] == [8, 8, 8, 8, 8]
assert contribution["m0"]["immediate_inline_count"] == 0
assert contribution["registered_deficit_observed"] is False
assert contribution["h1_gate"] == "closed"
assert contribution["entry_positive_counts"] == {"m0": 5, "h1": 0}
assert contribution["wrong_condition_counts"] == {"m0": 0, "h1": 0}
assert len(contribution["samples"]) == 5
assert all(item["valid"] and item["scores"]["total"] == 8 for item in contribution["samples"])
assert results["final_runtime"]["surviving_h1_units"] == []
assert results["final_runtime"]["v1_tree_sha256"] == M0_HASH

for name, expected in OUTPUT_HASHES.items():
    assert file_hash(PROMPT4 / "outputs" / name) == expected

candidate = load_json(EPOCH / "candidate.json")
assert candidate["decision"] == "prompt4-accepted-v1-equals-m0"
assert candidate["runtime"]["h1"]["evaluation_disposition"] == "reject-no-control-deficit"
assert candidate["runtime"]["surviving_h1_transformations"] == []
assert candidate["runtime"]["v1"]["tree_sha256"] == M0_HASH

m0_skill = (M0 / "SKILL.md").read_text(encoding="utf-8")
package = "\n".join(
    path.read_text(encoding="utf-8") for path in M0.rglob("*") if path.is_file()
)
assert set(re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", m0_skill)) == {
    "GLOSSARY.md",
    "BEHAVIOR-EVALS.md",
}
assert package.count("allow_implicit_invocation: true") == 1
assert "fork_turns" not in package

relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(
    encoding="utf-8"
)
assert "| `writing-great-skills` | implicitly invocable |" in relationships
assert (
    "| `writing-great-skills` | `GLOSSARY.md`: skill-authoring vocabulary; "
    "`BEHAVIOR-EVALS.md`: counterfactual wording evaluation |"
) in relationships
assert "$writing-great-skills` owns semantic quality" in relationships

print("prompt4 M0 viability, adaptive gate, V1, and relationship proof: pass")
