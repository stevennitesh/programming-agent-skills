"""Deterministic proof for the writing-great-skills Deploy Pruning Pass."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash

BASE = ROOT / ".scratch/deploy-campaigns/2026-07-24-writing-great-skills-7d0da40"
RUNTIME = BASE / "m0-runtime"
PROTOCOL = BASE / "evals/prompt4/protocol-manifest.json"
PROMPT4 = ROOT / "docs/validation/evals/writing-great-skills-2026-07-24-7d0da40-prompt4/results-manifest.json"
PRUNING = ROOT / "docs/validation/evals/writing-great-skills-2026-07-24-7d0da40-pruning/results-manifest.json"
SYNTHESIS = ROOT / "docs/synthesis/skills/writing-great-skills.md"
TRANSCRIPT = ROOT / "docs/validation/transcripts/2026-07-24-writing-great-skills-7d0da40-pruning.md"
EXPECTED_HEAD = "7d0da40a218114aa138265557ea2454361dcd147"
EXPECTED_TREE = "175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_gate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    assert len(re.findall(r"(?m)^```", text)) % 2 == 0, path
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

campaign = load(BASE / "campaign-manifest.json")
candidate = load(BASE / "candidate.json")
protocol = load(PROTOCOL)
prompt4 = load(PROMPT4)
pruning = load(PRUNING)

assert prompt4["prompt4_decision"] == "accepted"
assert prompt4["h1_contribution"]["decision"] == "reject-no-control-deficit"
assert prompt4["final_runtime"]["v1_tree_sha256"] == EXPECTED_TREE
assert campaign["active_unit"] == "pruning-pass"
assert campaign["decision"] == "complete"
assert campaign["pruning"]["disposition"] == "pruning-not-needed"
assert campaign["runtime_identities"]["P1"]["identity"] == EXPECTED_TREE
assert candidate["pruning_pass_result"]["p1_tree_sha256"] == EXPECTED_TREE
assert pruning["complete_cut_audit"]["v1_instruction_passages"] == 27
assert pruning["complete_cut_audit"]["classifications"] == {
    "keep": 27,
    "collapse": 0,
    "disclose": 0,
    "delete": 0,
}
assert pruning["rejected_or_forbidden"]["material_cuts"] == []
assert pruning["rejected_or_forbidden"]["reintroduced_c0_units"] == []
assert not pruning["rejected_or_forbidden"]["h1_pointer_repair_reintroduced"]
assert len([p for p in protocol["instruction_passage_map"] if p["runtime"] == "M0+H1"]) == 27
assert campaign_tree_hash(RUNTIME)["sha256"] == EXPECTED_TREE
assert TRANSCRIPT.read_text(encoding="utf-8").count("<!-- DEPLOY-STAGE-CAPSULE:pruning:start -->") == 1
assert TRANSCRIPT.read_text(encoding="utf-8").count("<!-- DEPLOY-STAGE-CAPSULE:pruning:end -->") == 1
for path in [SYNTHESIS, TRANSCRIPT, *sorted(RUNTIME.rglob("*.md"))]:
    markdown_gate(path)

print("pruning exact acceptance, identities, cut audit, and boundaries: pass")
