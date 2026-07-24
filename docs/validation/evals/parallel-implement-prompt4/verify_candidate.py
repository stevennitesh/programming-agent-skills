"""Deterministic Prompt 3 proof for the frozen parallel-implement candidate."""

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
EVAL = ROOT / "docs/validation/evals/parallel-implement-prompt4"
MANIFEST = json.loads((EVAL / "protocol-manifest.json").read_text("utf-8"))
RUNTIME = MANIFEST["runtime"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_contains(text: str, value: str) -> None:
    assert " ".join(value.split()) in " ".join(text.split()), value


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
worker_text = worker_path.read_text("utf-8").lower()
for forbidden in ("expected_m0_weakness", "candidate_terms", '"rubrics"', '"scoring"'):
    assert forbidden not in worker_text

skill = (CANDIDATE / "SKILL.md").read_text("utf-8")
metadata = (CANDIDATE / "agents/openai.yaml").read_text("utf-8")
ledger = (CANDIDATE / "references/RUN-LEDGER.md").read_text("utf-8")
worker = (CANDIDATE / "references/WORKER-BRIEF.md").read_text("utf-8")
integrator = (CANDIDATE / "references/INTEGRATOR-BRIEF.md").read_text("utf-8")

for required in (
    "explicit request to deliver one parent",
    "exhaustive associated non-empty Ready-for-agent graph",
    "recommend `$repo-bootstrap` and stop",
    "complete repair packet",
    "`events.jsonl` is authority",
    "Missing state is not completed state.",
    "semantic ownership",
    "proof seams and scarce proof resources",
    "Claim each selected item and read back the claim.",
    "Land accepted commits one at a time at the root.",
    "`$resolving-merge-conflicts`",
    "Every repaired successor receives fresh formal review.",
    "close every child with mutation read-back",
    "close the parent only after",
    "nonterminal `partial` or `blocked` return",
    "Publication and Git delivery remain with their separately authorized owners.",
):
    normalized_contains(skill, required)

assert "allow_implicit_invocation: false" in metadata
assert "Continue the same actor once" not in skill
assert "Push only when authorized" not in skill
normalized_contains(
    skill,
    "Continue an actor only while its reconciled lane, authority, and bounded assignment remain current",
)
normalized_contains(
    ledger,
    "publication evidence supplied under separate authority when applicable",
)
normalized_contains(worker, "Never spawn, integrate, formally review, mutate trackers, push, or widen scope.")
normalized_contains(
    integrator,
    "Return dispatch, formal review, tracker mutation, push, and run closeout to the orchestrator.",
)

for mapping in ("runtime_clause_map", "compatibility_map"):
    for surfaces in MANIFEST[mapping].values():
        for surface in surfaces:
            path_text = surface.split("#", 1)[0]
            assert (CANDIDATE / path_text).is_file(), surface
for passage, owners in MANIFEST["instruction_passage_map"].items():
    assert (CANDIDATE / passage.split("#", 1)[0]).is_file(), passage
    assert owners and all(owner.startswith(("M0-", "K-")) for owner in owners), passage

for relative in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", skill):
    assert (CANDIDATE / relative).resolve().is_file(), relative

markdown = list(CANDIDATE.rglob("*.md")) + [
    ROOT / "docs/validation/transcripts/2026-07-24-parallel-implement-prompt3-construction.md"
]
for path in markdown:
    text = path.read_text("utf-8")
    assert len(re.findall(r"(?m)^```", text)) % 2 == 0, path
    in_fence = False
    table_width = None
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            table_width = None
        elif not in_fence and line.startswith("|") and line.endswith("|"):
            width = line.count("|")
            table_width = width if table_width is None else table_width
            assert width == table_width, (path, line)
        elif not in_fence:
            table_width = None
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if "://" not in target:
            assert (path.parent / target).resolve().exists(), (path, target)

experimental_manifest = json.loads(
    (ROOT / "skills/experimental/manifest.json").read_text("utf-8")
)
assert (
    experimental_manifest["skills"]["parallel-implement"]["candidate_sha256"]
    == RUNTIME["tree_sha256"]
)

print(f"tree_sha256={RUNTIME['tree_sha256']}")
print("inventory_hashes_h1_equality=pass")
print("helper_identity=pass")
print("clauses_compatibility_invocation_relationships=pass")
print("fixture_isolation_and_markdown=pass")
