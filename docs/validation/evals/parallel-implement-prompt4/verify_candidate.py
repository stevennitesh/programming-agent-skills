"""Focused Prompt 4 structural, invocation, and relationship proof."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts.skill_pack_contract import tree_hash


CANDIDATE = ROOT / "skills/experimental/parallel-implement"
EXPECTED_TREE = "036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc"
EXPECTED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/CODEX-WORKTREE-LAUNCH.md",
    "references/INTEGRATOR-BRIEF.md",
    "references/RUN-LEDGER.md",
    "references/WORKER-BRIEF.md",
    "scripts/lane_worktree.py",
    "scripts/run_ledger.py",
}


def require(text: str, *needles: str) -> None:
    normalized = " ".join(text.split())
    for needle in needles:
        assert " ".join(needle.split()) in normalized, needle


actual_files = {
    path.relative_to(CANDIDATE).as_posix()
    for path in CANDIDATE.rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
}
assert actual_files == EXPECTED_FILES, (actual_files - EXPECTED_FILES, EXPECTED_FILES - actual_files)
assert tree_hash(CANDIDATE) == EXPECTED_TREE

manifest = json.loads((ROOT / "skills/experimental/manifest.json").read_text("utf-8"))
entry = manifest["skills"]["parallel-implement"]
assert entry["candidate_sha256"] == EXPECTED_TREE

skill = (CANDIDATE / "SKILL.md").read_text("utf-8")
metadata = (CANDIDATE / "agents/openai.yaml").read_text("utf-8")
ledger = (CANDIDATE / "references/RUN-LEDGER.md").read_text("utf-8")
worker = (CANDIDATE / "references/WORKER-BRIEF.md").read_text("utf-8")
integrator = (CANDIDATE / "references/INTEGRATOR-BRIEF.md").read_text("utf-8")

require(
    skill,
    "explicitly requested parent",
    "Root-only",
    "If invocation is delegated, return a routing blocker before mutation.",
    "Return one selected item to `$implement`",
    "return an incomplete, ambiguous, unsettled, or unready graph to `$to-tickets`",
    "recommend\n`$repo-bootstrap` and stop",
    "events.jsonl` is authority",
    "Missing state is not completed state.",
    "semantic ownership",
    "proof seams and scarce proof resources",
    "otherwise dispatch serially",
    "`landed-awaiting-lock`, but it never closes the tracker item",
    "Land accepted commits one at a time at the root.",
    "`$tdd`",
    "`$diagnosing-bugs`",
    "`$review`",
    "`$convergent-pr-review`",
    "`$resolving-merge-conflicts`",
    "Every repaired successor receives fresh formal review.",
    "close every child with mutation read-back, then\nclose the parent",
    "Return `complete` only when",
    "nonterminal `partial` or `blocked` return",
)
require(metadata, "allow_implicit_invocation: false")
require(ledger, "runtime contract 3", "events.jsonl", "checkpoint", "closeout")
require(
    worker,
    "Never spawn, integrate, formally review, mutate trackers, push, or widen scope.",
)
require(
    integrator,
    "Return dispatch, formal review, tracker mutation, push, and run closeout to the orchestrator.",
)

for reference in (
    "references/RUN-LEDGER.md",
    "references/CODEX-WORKTREE-LAUNCH.md",
    "references/WORKER-BRIEF.md",
    "references/INTEGRATOR-BRIEF.md",
):
    assert (CANDIDATE / reference).is_file(), reference

for relative in (
    "agents/openai.yaml",
    "references/CODEX-WORKTREE-LAUNCH.md",
    "scripts/lane_worktree.py",
    "scripts/run_ledger.py",
):
    candidate_bytes = (CANDIDATE / relative).read_bytes()
    canonical_bytes = (ROOT / "skills/custom/parallel-implement" / relative).read_bytes()
    assert candidate_bytes == canonical_bytes, relative

affected_markdown = [
    ROOT / "docs/synthesis/skills/parallel-implement.md",
    ROOT / "docs/validation/transcripts/2026-07-23-parallel-implement-prompt4-behavior-audit.md",
    ROOT / "docs/validation/evals/parallel-implement-prompt4/recovery-raw.md",
    ROOT / "docs/validation/evals/parallel-implement-prompt4/concurrency-raw.md",
    ROOT / "docs/validation/evals/parallel-implement-prompt4/viability-raw.md",
]
for path in affected_markdown:
    text = path.read_text("utf-8")
    assert len(re.findall(r"(?m)^```", text)) % 2 == 0, path
    in_fence = False
    table_width = None
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            table_width = None
            continue
        if in_fence:
            continue
        if line.startswith("|") and line.endswith("|"):
            width = line.count("|")
            if table_width is None:
                table_width = width
            assert width == table_width, (path, line)
        else:
            table_width = None
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if "://" not in target:
            assert (path.parent / target).resolve().exists(), (path, target)

print(f"tree_sha256={EXPECTED_TREE}")
for relative in sorted(EXPECTED_FILES):
    data = (CANDIDATE / relative).read_bytes()
    print(f"{hashlib.sha256(data).hexdigest()}  {relative}")
print("structural_invocation_context_return_completion_relationship=pass")
print("protected_byte_parity=pass")
print("affected_markdown_gate=pass")
