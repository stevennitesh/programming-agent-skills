"""Deterministic Prompt 3 proof for parallel-implement correction epoch r2."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts.skill_pack_contract import tree_hash


CANDIDATE = ROOT / "skills/experimental/parallel-implement"
EVAL = ROOT / "docs/validation/evals/parallel-implement-prompt4-r2"
MANIFEST = json.loads((EVAL / "protocol-manifest.json").read_text("utf-8"))
RUNTIME = MANIFEST["runtime"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_sha256(path: Path) -> str:
    data = path.read_bytes()
    begin = b"<!-- DECISION-CONTENT-BEGIN -->"
    end = b"<!-- DECISION-CONTENT-END -->"
    start = data.index(b"\n", data.index(begin)) + 1
    stop = data.index(end, start)
    return hashlib.sha256(data[start:stop]).hexdigest()


def normalized_contains(text: str, value: str) -> None:
    assert " ".join(value.split()) in " ".join(text.split()), value


inputs = MANIFEST["inputs"]
assert content_sha256(
    ROOT / "docs/validation/transcripts/2026-07-24-parallel-implement-prompt1-m0-r2.md"
) == inputs["m0_checkpoint_content_sha256"]
assert content_sha256(
    ROOT / "docs/research/parallel-implement-2026-07-24-r2.md"
) == inputs["research_r2_content_sha256"]
assert content_sha256(
    ROOT / "docs/research/parallel-implement-2026-07-24.md"
) == inputs["research_carried_content_sha256"]
assert content_sha256(
    ROOT / "docs/synthesis/skills/parallel-implement.md"
) == inputs["prompt2_content_sha256"]
assert tree_hash(ROOT / "skills/custom/parallel-implement") == inputs[
    "current_canonical_tree_sha256"
]
prior_protocol = json.loads(
    (
        ROOT
        / "docs/validation/evals/parallel-implement-prompt4/protocol-manifest.json"
    ).read_text("utf-8")
)
assert prior_protocol["runtime"]["tree_sha256"] == inputs[
    "failed_candidate_tree_sha256"
]

actual_inventory = sorted(
    path.relative_to(CANDIDATE).as_posix()
    for path in CANDIDATE.rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
)
assert actual_inventory == RUNTIME["inventory"]
assert tree_hash(CANDIDATE) == RUNTIME["tree_sha256"]
assert RUNTIME["m0_sha256"] == RUNTIME["h1_sha256"] == RUNTIME["tree_sha256"]
for relative, expected in RUNTIME["files_sha256"].items():
    assert sha256(CANDIDATE / relative) == expected, relative

for helper in ("scripts/lane_worktree.py", "scripts/run_ledger.py"):
    assert (CANDIDATE / helper).read_bytes() == (
        ROOT / "skills/custom/parallel-implement" / helper
    ).read_bytes(), helper

worker_path = EVAL / MANIFEST["evaluation"]["worker_fixture"]["path"]
root_path = EVAL / MANIFEST["evaluation"]["root_fixture"]["path"]
assert sha256(worker_path) == MANIFEST["evaluation"]["worker_fixture"]["sha256"]
assert sha256(root_path) == MANIFEST["evaluation"]["root_fixture"]["sha256"]
worker_data = json.loads(worker_path.read_text("utf-8"))
root_data = json.loads(root_path.read_text("utf-8"))
worker_text = worker_path.read_text("utf-8").lower()
for forbidden in (
    "expected_m0_weakness",
    "candidate_terms",
    '"rubrics"',
    '"scoring"',
    "conclusions_before_sampling",
):
    assert forbidden not in worker_text
assert [sample["id"] for sample in worker_data["samples"]] == [
    "O-01",
    "O-02",
    "O-03",
    "H-01",
    "H-02",
]
assert [capture["id"] for capture in MANIFEST["evaluation"]["expected_captures"]] == [
    "O-01",
    "O-02",
    "O-03",
    "H-01",
    "H-02",
]
assert set(root_data["rubrics"]) == {"ordinary", "high-risk"}
for family, template_name in (("ordinary", "ordinary"), ("high-risk", "high_risk")):
    fixture = worker_data["templates"][template_name]
    blockers = {
        finding["id"]
        for finding in fixture["pre_admission"]["complete_review_report"]
        if finding["severity"] == "blocking"
    }
    assert blockers == set(fixture["post_decision_admission"]["admitted_ids"]) == {
        "F1",
        "F2",
    }
    assert set(fixture["post_decision_admission"]["classifications"]) == blockers
    assert all(
        value == "automatic-in-scope"
        for value in fixture["post_decision_admission"]["classifications"].values()
    )
    assert set(fixture["post_decision_admission"]["charter_evidence"]) == blockers
    assert fixture["post_decision_admission"]["repair_generation_budget_remaining"] == 1
    assert fixture["post_decision_admission"]["successor_review_budget_remaining"] == 1
    assert fixture["successor"]["target_type"]
    assert fixture["successor"]["risk"]
    assert fixture["successor"]["risk_evidence"]
    assert len(root_data["rubrics"][family]) == 5

skill = (CANDIDATE / "SKILL.md").read_text("utf-8")
metadata = (CANDIDATE / "agents/openai.yaml").read_text("utf-8")
worker = (CANDIDATE / "references/WORKER-BRIEF.md").read_text("utf-8")
integrator = (CANDIDATE / "references/INTEGRATOR-BRIEF.md").read_text("utf-8")
for required in (
    "explicit request to deliver one parent",
    "exhaustive associated non-empty Ready-for-agent graph",
    "recommend `$repo-bootstrap` and stop",
    "`events.jsonl` is authority",
    "Claim each selected item and read back the claim.",
    "Land accepted commits one at a time at the root.",
    "`$resolving-merge-conflicts`",
    "preserving and returning the complete blocking report intact",
    "Open no Repair plan, assignment, mutation, or successor snapshot before the caller admits the complete blocking set.",
    "require the admitted IDs to equal every blocking ID",
    "individually Charter-preserving",
    "both the frozen Repair-generation and successor-review budgets",
    "identity-matched proof and fresh formal review",
    "close every child with mutation read-back",
    "Publication and Git delivery remain with their separately authorized owners.",
):
    normalized_contains(skill, required)
assert "allow_implicit_invocation: false" in metadata
assert "Continue the same actor once" not in skill
assert "the original worker once" not in skill
assert "one narrow continuation" not in worker
assert "Push only when authorized" not in skill
normalized_contains(
    skill,
    "a reconciled existing lane whose authority and bounded assignment remain current",
)
normalized_contains(
    worker,
    "only while the root-recorded route, reconciled lane, authority, and bounded assignment remain current",
)
normalized_contains(worker, "caller admission record")
normalized_contains(worker, "admitted IDs equal every blocking ID")
normalized_contains(integrator, "complete blocking set")
normalized_contains(integrator, "both frozen budgets permit the successor")

for mapping in ("runtime_clause_map", "compatibility_map"):
    for surfaces in MANIFEST[mapping].values():
        for surface in surfaces:
            assert (CANDIDATE / surface.split("#", 1)[0]).is_file(), surface
for passage, owners in MANIFEST["instruction_passage_map"].items():
    assert (CANDIDATE / passage.split("#", 1)[0]).is_file(), passage
    assert owners and all(owner.startswith(("M0-", "K-")) for owner in owners)

for relative in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", skill):
    assert (CANDIDATE / relative).resolve().is_file(), relative

markdown = list(CANDIDATE.rglob("*.md")) + [
    ROOT
    / "docs/validation/transcripts/2026-07-24-parallel-implement-prompt3-construction-r2.md"
]
for path in markdown:
    text_value = path.read_text("utf-8")
    assert len(re.findall(r"(?m)^```", text_value)) % 2 == 0, path
    in_fence = False
    table_width = None
    for line in text_value.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            table_width = None
        elif not in_fence and line.startswith("|") and line.endswith("|"):
            width = line.count("|")
            table_width = width if table_width is None else table_width
            assert width == table_width, (path, line)
        elif not in_fence:
            table_width = None
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text_value):
        if "://" not in target:
            assert (path.parent / target).resolve().exists(), (path, target)

experimental_manifest = json.loads(
    (ROOT / "skills/experimental/manifest.json").read_text("utf-8")
)
assert experimental_manifest["skills"]["parallel-implement"]["candidate_sha256"] == (
    RUNTIME["tree_sha256"]
)
construction = markdown[-1]
declared_fingerprint = re.search(
    r"(?m)^Content fingerprint: `([0-9a-f]{64})`$",
    construction.read_text("utf-8"),
)
assert declared_fingerprint is not None
assert content_sha256(construction) == declared_fingerprint.group(1)

print(f"tree_sha256={RUNTIME['tree_sha256']}")
print("input_fingerprints_inventory_hashes_h1_equality=pass")
print("helper_identity_and_compatibility=pass")
print("clauses_relationships_repair_authority=pass")
print("five_fixture_isolation_and_grounding=pass")
print("markdown_json_manifest=pass")
