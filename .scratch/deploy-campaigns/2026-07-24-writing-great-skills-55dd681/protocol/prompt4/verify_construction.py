from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash, compare_payloads, lint_worker_fixture


CAMPAIGN = ROOT / ".scratch/deploy-campaigns/2026-07-24-writing-great-skills-55dd681"
PROTOCOL = CAMPAIGN / "protocol/prompt4/protocol-manifest.json"
M0 = CAMPAIGN / "runtime/m0/writing-great-skills"
H1 = CAMPAIGN / "runtime/h1/writing-great-skills"
WORKER = CAMPAIGN / "fixtures/prompt4/worker-fixture.json"
ROOT_EVALUATOR = CAMPAIGN / "fixtures/prompt4/root-evaluator.json"
M0_PAYLOAD = CAMPAIGN / "payloads/prompt4/EP-CLEAR-01-m0.json"
H1_PAYLOAD = CAMPAIGN / "payloads/prompt4/EP-CLEAR-01-h1.json"
TRANSCRIPT = ROOT / "docs/validation/transcripts/2026-07-24-writing-great-skills-prompt3-construction.md"
INVENTORY = ["BEHAVIOR-EVALS.md", "GLOSSARY.md", "SKILL.md", "agents/openai.yaml"]


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(path: Path) -> list[str]:
    return sorted(item.relative_to(path).as_posix() for item in path.rglob("*") if item.is_file())


def markdown_gate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    if len(re.findall(r"^```", text, flags=re.MULTILINE)) % 2:
        failures.append(f"{path}: unbalanced code fences")
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)", text):
        if "://" not in target and not (path.parent / target).exists():
            failures.append(f"{path}: missing local link {target}")
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("|") and line.endswith("|"):
            columns = len(line.split("|")) - 2
            if columns < 2:
                failures.append(f"{path}:{line_number}: malformed table row")
    return failures


def main() -> int:
    protocol = load(PROTOCOL)
    root_evaluator = load(ROOT_EVALUATOR)
    failures: list[str] = []

    for label, path in (("m0", M0), ("h1", H1)):
        if files(path) != INVENTORY:
            failures.append(f"{label}: inventory mismatch")
        expected = protocol["runtime"][label]
        actual_tree = campaign_tree_hash(path)["sha256"]
        if actual_tree != expected["tree_sha256"]:
            failures.append(f"{label}: tree hash mismatch")
        for name, expected_sha in expected["files_sha256"].items():
            if sha(path / name) != expected_sha:
                failures.append(f"{label}:{name}: file hash mismatch")

    changed = [name for name in INVENTORY if (M0 / name).read_bytes() != (H1 / name).read_bytes()]
    if changed != ["BEHAVIOR-EVALS.md"]:
        failures.append(f"arm delta mismatch: {changed}")

    for passage in protocol["instruction_passage_map"]:
        surface = passage["surface"].split("#", 1)[0]
        if passage["selector"] not in (M0 / surface).read_text(encoding="utf-8"):
            failures.append(f"missing M0 passage {passage['id']}")
    for passage in protocol["h1_delta_passage_map"]:
        surface = passage["surface"].split("#", 1)[0]
        if passage["selector"] not in (H1 / surface).read_text(encoding="utf-8"):
            failures.append(f"missing H1 passage {passage['id']}")

    required = {f"M0-U{number:02d}" for number in range(1, 10)} | {"H1-UNCERTAINTY-01"}
    if set(protocol["semantic_trace"]) != required:
        failures.append("semantic trace IDs are incomplete")
    proof_ids = {
        item["id"]
        for group in (
            protocol["proof_registration"]["m0_viability_suite"],
            protocol["proof_registration"]["protected_behavior"],
            protocol["proof_registration"]["relationships"],
            protocol["proof_registration"]["invocation"],
            protocol["proof_registration"]["context"],
            protocol["proof_registration"]["machine"],
        )
        for item in group
    }
    proof_ids.add(protocol["proof_registration"]["h1_contribution_control"]["id"])
    for semantic_id, trace in protocol["semantic_trace"].items():
        if not trace["owner"] or not trace["passages"] or not trace["proof_ids"]:
            failures.append(f"{semantic_id}: empty owner, passage, or proof")
        if any(proof_id not in proof_ids for proof_id in trace["proof_ids"]):
            failures.append(f"{semantic_id}: unregistered proof ID")

    combined = {
        label: "\n".join((path / name).read_text(encoding="utf-8") for name in INVENTORY)
        for label, path in (("m0", M0), ("h1", H1))
    }
    forbidden_patterns = {
        "FORBID-AUDIT-WRITE": r"Audit[^\n]*(?:edit|mutat(?:e|ion)|write)",
        "FORBID-SCAFFOLD-INSTALL-DELIVERY": r"(?:install_skills|git\s+(?:commit|push)|publish\s+command|scaffold\s+command)",
        "FORBID-SKILL-OWNED-DISPATCH": r"(?:fork_turns|spawn_agent|dispatch\s+(?:a\s+)?worker)",
        "FORBID-NAMED-SURFACE-FIXED-ORDER": r"(?:required headings|mandatory headings|always follow (?:this|the) sequence)",
        "FORBID-LENGTH-AS-SEMANTIC-VERDICT": r"(?:line count|word count|token count|shorter is better)",
        "FORBID-NEGATION-CAUSALITY": r"(?:negation|prohibition) activates",
        "FORBID-CONCEPTUAL-LEADING-WORD-EFFICACY": r"(?:leading word|leitwort|recruits? (?:the )?model priors)",
        "FORBID-FAILURE-FORM-WITHOUT-DEFICIT": r"(?:Failure\s*\|\s*Instruction form|failure taxonomy)",
    }
    for semantic_id, pattern in forbidden_patterns.items():
        for label, text in combined.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                failures.append(f"{semantic_id}: forbidden match in {label}")

    for path in (M0, H1):
        skill = (path / "SKILL.md").read_text(encoding="utf-8")
        behavior = (path / "BEHAVIOR-EVALS.md").read_text(encoding="utf-8")
        policy = (path / "agents/openai.yaml").read_text(encoding="utf-8")
        description = skill.split("---", 2)[1]
        if policy.strip() != "policy:\n  allow_implicit_invocation: true":
            failures.append(f"{path}: implicit policy mismatch")
        if len(re.findall(r"\[[^\]]+\]\([^)]+\.md\)", skill)) != 2:
            failures.append(f"{path}: expected exactly two Markdown references")
        if any(token in description for token in ("## ", "Select exactly", "Return `complete`")):
            failures.append(f"{path}: body-summary routing leak")
        if "requested canonical skill or skill-design artifact and directly affected proof or relationship surfaces" not in skill:
            failures.append(f"{path}: Author scope missing")
        if "observed persistent early-stop defect after sharpening its" not in skill:
            failures.append(f"{path}: automatic split guard missing")
        if "minimum floor, not an automatic\nsufficiency rule" not in behavior:
            failures.append(f"{path}: five-sample sufficiency guard missing")

    forbidden_ids = {item["semantic_id"] for item in protocol["forbidden_absence_checks"]}
    expected_forbidden = {
        "FORBID-EXPLICIT-ONLY-CONVERSION", "FORBID-BODY-SUMMARY-ROUTING",
        "FORBID-AUDIT-WRITE", "FORBID-AUTHOR-SCOPE-EXPANSION",
        "FORBID-SCAFFOLD-INSTALL-DELIVERY", "FORBID-SKILL-OWNED-DISPATCH",
        "FORBID-NAMED-SURFACE-FIXED-ORDER", "FORBID-LENGTH-AS-SEMANTIC-VERDICT",
        "FORBID-NEGATION-CAUSALITY", "FORBID-CONCEPTUAL-LEADING-WORD-EFFICACY",
        "FORBID-AUTOMATIC-CONTEXT-SPLIT", "FORBID-FIVE-SAMPLE-SUFFICIENCY",
        "FORBID-FAILURE-FORM-WITHOUT-DEFICIT", "FORBID-NEW-HELPER-WITHOUT-FAILURE",
        "FORBID-HISTORICAL-LIFECYCLE-REUSE",
    }
    if forbidden_ids != expected_forbidden:
        failures.append("forbidden semantic coverage mismatch")

    lint_worker_fixture(WORKER)
    comparison = compare_payloads(WORKER, "EP-CLEAR-01", M0_PAYLOAD, H1_PAYLOAD)
    if comparison["shared_payload_sha256"] != protocol["fixture_identity"]["resolved_pair"]["shared_payload_sha256"]:
        failures.append("resolved payload identity mismatch")

    worker = load(WORKER)
    worker_text = json.dumps(worker, sort_keys=True)
    for forbidden in ("hypothesis", "expected_weakness", "rubric", "candidate_terms", "prior_outputs", "conclusions"):
        if f'"{forbidden}"' in worker_text:
            failures.append(f"worker fixture root cue: {forbidden}")
    fact_ids = {
        fact["id"]
        for case in worker["cases"]
        for fact in case["facts"]
    }
    lint_map = root_evaluator["fixture_lint_map"]
    for section in ("criteria", "decision_inputs", "required_output_semantics"):
        for entry in lint_map[section]:
            ids = entry.get("worker_fact_ids", [])
            operations = entry.get("observable_operations", [])
            if not ids and not operations:
                failures.append(f"fixture lint map empty: {section}")
            if any(item not in fact_ids for item in ids):
                failures.append(f"fixture lint map unknown fact: {section}")

    for markdown in list(M0.rglob("*.md")) + list(H1.rglob("*.md")) + ([TRANSCRIPT] if TRANSCRIPT.exists() else []):
        failures.extend(markdown_gate(markdown))

    if failures:
        print(json.dumps({"status": "failed", "failures": failures}, indent=2))
        return 1
    print(json.dumps({
        "status": "ok",
        "m0_tree_sha256": campaign_tree_hash(M0)["sha256"],
        "h1_tree_sha256": campaign_tree_hash(H1)["sha256"],
        "passage_count": len(protocol["instruction_passage_map"]),
        "h1_delta_passage_count": len(protocol["h1_delta_passage_map"]),
        "forbidden_absence_count": len(forbidden_ids),
        "fixture_case_count": len(worker["cases"]),
        "resolved_shared_payload_sha256": comparison["shared_payload_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
