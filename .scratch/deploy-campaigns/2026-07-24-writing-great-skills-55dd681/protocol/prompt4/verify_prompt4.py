from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash


CAMPAIGN = ROOT / ".scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681"
M0 = CAMPAIGN / "runtime/m0/writing-great-skills"
H1 = CAMPAIGN / "runtime/h1/writing-great-skills"
EVALUATED_H1_PATH = CAMPAIGN / "runtime/evaluated-h1/writing-great-skills"
RESULTS = (
    ROOT
    / "docs/validation/evals/writing-great-skills-2026-07-24-prompt4/results-manifest.json"
)
TRANSCRIPT = (
    ROOT
    / "docs/validation/transcripts/2026-07-24-writing-great-skills-prompt4-behavior-audit.md"
)
EXPECTED_V1 = "559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032"
EVALUATED_H1 = "1021d8c5d9d20a81e4ab33a0b014cf71826b818a02153041b7845aac245cf553"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    campaign = load(CAMPAIGN / "campaign.json")
    candidate = load(CAMPAIGN / "candidate.json")
    results = load(RESULTS)

    m0_hash = campaign_tree_hash(M0)["sha256"]
    h1_hash = campaign_tree_hash(H1)["sha256"]
    if m0_hash != EXPECTED_V1:
        failures.append("M0 identity mismatch")
    if h1_hash != EXPECTED_V1:
        failures.append("rederived H1 does not equal M0")
    if campaign_tree_hash(EVALUATED_H1_PATH)["sha256"] != EVALUATED_H1:
        failures.append("evaluated H1 frozen package mismatch")
    if sorted(p.relative_to(M0).as_posix() for p in M0.rglob("*") if p.is_file()) != sorted(
        p.relative_to(H1).as_posix() for p in H1.rglob("*") if p.is_file()
    ):
        failures.append("rederived H1 inventory mismatch")
    for path in M0.rglob("*"):
        if path.is_file() and path.read_bytes() != (H1 / path.relative_to(M0)).read_bytes():
            failures.append(f"rederived H1 byte mismatch: {path.relative_to(M0)}")

    decision = campaign["prompt_4_decision"]
    if campaign["active_unit"] != "prompt4" or campaign["decision"]["status"] != "accepted":
        failures.append("campaign active decision mismatch")
    if decision["v1"]["tree_sha256"] != EXPECTED_V1:
        failures.append("campaign V1 mismatch")
    if decision["h1"]["evaluated_tree_sha256"] != EVALUATED_H1:
        failures.append("evaluated H1 identity lost")
    if decision["h1"]["decision"] != "reject-insufficient-contribution":
        failures.append("H1 disposition mismatch")
    if decision["h1"]["surviving_transformations"]:
        failures.append("rejected H1 transformation survived")

    if candidate["decision"] != "pre-registered-not-sampled":
        failures.append("frozen Prompt 3 candidate mutated")
    if candidate["runtime"]["h1_tree_sha256"] != EVALUATED_H1:
        failures.append("frozen candidate evaluated H1 identity mismatch")
    if sha(CAMPAIGN / "candidate.json") != "d9f14f8ec62781fc1d35c7758c0e289d8cb6c9c6c18269011a455a0edac0a811":
        failures.append("frozen Prompt 3 candidate byte identity mismatch")

    if results["decision"] != "reject-insufficient-contribution":
        failures.append("results disposition mismatch")
    if results["m0_viability"]["valid_count"] != 3:
        failures.append("M0 viability sample count mismatch")
    contribution = results["h1_contribution"]
    if contribution["entry_positive_counts"] != {"m0": 6, "h1": 6}:
        failures.append("entry-positive counts mismatch")
    if contribution["wrong_condition_counts"] != {"m0": 0, "h1": 0}:
        failures.append("wrong-condition counts mismatch")
    if contribution["wrong_condition_gate"] != "not-opened-candidate-rejected-before-gate":
        failures.append("wrong-condition gate mismatch")

    m0_scores = [sample["m0_scores"]["total"] for sample in contribution["samples"]]
    h1_scores = [sample["h1_scores"]["total"] for sample in contribution["samples"]]
    deltas = [h1 - m0 for m0, h1 in zip(m0_scores, h1_scores)]
    if m0_scores != [7, 7, 7, 7, 8, 7] or h1_scores != [8, 8, 7, 7, 8, 8]:
        failures.append("per-sample score mismatch")
    if deltas != [1, 1, 0, 0, 0, 1]:
        failures.append("paired effect mismatch")
    if abs(statistics.pvariance(m0_scores) - contribution["m0"]["population_variance"]) > 0.000001:
        failures.append("M0 variance mismatch")
    if abs(statistics.pvariance(h1_scores) - contribution["h1"]["population_variance"]) > 0.000001:
        failures.append("H1 variance mismatch")

    for sample in contribution["samples"]:
        case_id = sample["case_id"]
        for arm in ("m0", "h1"):
            path = CAMPAIGN / f"evals/prompt4/disposable/{arm}/{case_id}.md"
            if not path.is_file() or sha(path) != sample[f"{arm}_output_sha256"]:
                failures.append(f"{arm} capture mismatch: {case_id}")
    for sample in results["m0_viability"]["samples"]:
        path = ROOT / sample["output"]
        if not path.is_file() or sha(path) != sample["output_sha256"]:
            failures.append(f"M0 viability capture mismatch: {sample['case_id']}")

    if any(path.name.startswith("WC-") for path in (CAMPAIGN / "evals/prompt4/disposable").rglob("*.md")):
        failures.append("wrong-condition capture exists despite closed gate")

    transcript = TRANSCRIPT.read_text(encoding="utf-8")
    if transcript.count("<!-- BEGIN PROMPT4 DECISION -->") != 1:
        failures.append("Prompt 4 capsule start mismatch")
    if transcript.count("<!-- END PROMPT4 DECISION -->") != 1:
        failures.append("Prompt 4 capsule end mismatch")

    if failures:
        print(json.dumps({"status": "failed", "failures": failures}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "status": "ok",
                "m0_tree_sha256": m0_hash,
                "rederived_h1_tree_sha256": h1_hash,
                "v1_tree_sha256": EXPECTED_V1,
                "m0_viability_samples": 3,
                "m0_entry_positive_samples": 6,
                "h1_entry_positive_samples": 6,
                "wrong_condition_samples": 0,
                "h1_decision": "reject-insufficient-contribution",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
