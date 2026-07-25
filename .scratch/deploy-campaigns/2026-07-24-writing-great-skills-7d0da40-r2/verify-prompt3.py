from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.campaign_artifacts import campaign_tree_hash, lint_worker_fixture


EXPECTED_INVENTORY = {
    "BEHAVIOR-EVALS.md",
    "GLOSSARY.md",
    "SKILL.md",
    "agents/openai.yaml",
}
TERMINAL = {
    "accept",
    "reject-no-control-deficit",
    "reject-insufficient-contribution",
    "reject-regression",
    "needs-more-evidence",
    "blocked",
}


def normalized(value: str) -> str:
    return " ".join(value.split()).lower()


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        text,
    )
    assert match is not None, f"missing heading: {heading}"
    return normalized(match.group(1))


def inventory(path: Path) -> set[str]:
    return {
        item.relative_to(path).as_posix()
        for item in path.rglob("*")
        if item.is_file()
    }


def require_all(haystack: str, needles: tuple[str, ...]) -> None:
    for needle in needles:
        assert normalized(needle) in haystack, needle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", required=True, type=Path)
    parser.add_argument("--expected-tree-sha256", required=True)
    args = parser.parse_args()
    candidate = args.candidate_root.resolve()
    observed = campaign_tree_hash(candidate)
    assert observed["sha256"] == args.expected_tree_sha256
    assert inventory(candidate) == EXPECTED_INVENTORY

    skill = (candidate / "SKILL.md").read_text(encoding="utf-8")
    glossary = (candidate / "GLOSSARY.md").read_text(encoding="utf-8")
    behavior = (candidate / "BEHAVIOR-EVALS.md").read_text(encoding="utf-8")
    policy = (candidate / "agents/openai.yaml").read_text(encoding="utf-8")
    package = normalized("\n".join((skill, glossary, behavior, policy)))

    links = set(re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", skill))
    assert links == {"GLOSSARY.md", "BEHAVIOR-EVALS.md"}
    assert all((candidate / link).is_file() for link in links)
    assert normalized(policy) == "policy: allow_implicit_invocation: true"
    assert "fork_turns" not in package

    require_all(section(skill, "## Authority"), (
        "Select exactly one operation",
        "Audit",
        "Author",
        "target, operation, canonical source, and mutation boundary",
        "Return `blocked`",
        "skill-creator",
        "installation, publishing, synchronization, and Git delivery",
    ))
    require_all(section(skill, "## Coverage"), (
        "Inspect only surfaces capable of changing the requested behavior",
        "affected",
        "preserve",
        "owned elsewhere",
        "historical evidence",
        "drift",
        "not applicable",
        "full audit",
    ))
    require_all(section(skill, "## Semantic Contract"), (
        "Give each behavior one owner",
        "relationship's callee, observable trigger, authority, and Return",
        "implicitly invocable description as the routing predicate",
        "common behavior inline",
        "GLOSSARY.md",
        "persistent early-stop defect",
    ))
    require_all(section(skill, "## Behavior-Preserving Cuts"), (
        "intended behavior, safety, authority, proof",
        "safe failure, Return, or completion",
        "no-ops",
        "duplicated meaning",
        "stale exposition",
        "ownerless clauses",
    ))
    require_all(section(skill, "## Claim-Matched Proof"), (
        "read-back for exact bytes and mutations",
        "focused structural checks",
        "relationship traces",
        "BEHAVIOR-EVALS.md",
        "uncontaminated direct controls",
        "fixed tasks and rubrics",
        "fresh contexts",
        "Structural evidence does not prove wording efficacy",
    ))
    require_all(section(skill, "## Author Lock"), (
        "read back exact mutations and current work state",
        "preserve unrelated work",
        "stop before installation, publishing, synchronization, staging, commit, push",
    ))
    require_all(section(skill, "## Return"), (
        "complete",
        "partial",
        "blocked",
        "Audit reports",
        "Author reports",
        "Complete only when coverage is classified",
    ))

    require_all(section(behavior, "## Register the control"), (
        "defect-correction",
        "quality-lift",
        "Fix the task",
        "meaningful rubric deficit",
        "observable entry predicate",
        "common",
        "situational",
        "rare",
        "unknown",
        "reject-no-control-deficit",
    ))
    require_all(section(behavior, "## Freeze the cohorts"), (
        "separate entry-positive and wrong-condition cohorts",
        "candidate language, conclusions, and prior outputs out of control contexts",
        "fresh contexts",
        "evidence judgment stays with the root",
    ))
    require_all(section(behavior, "## Apply the adaptive gate"), (
        "at least five fresh M0 entry-positive controls",
        "at least five fresh H1 entry-positive samples only when",
        "wrong-condition M0/H1 pairs only after H1 clears",
        "non-triggering cases",
        "material variance",
        "borderline effect",
        "protocol deviation",
        "minimum floor, not automatic evidence sufficiency",
    ))
    require_all(section(behavior, "## Judge conditional efficacy"), (
        "Strings, headings, and template echoes are structural evidence only",
        "M0 demonstrates the registered defect or meaningful quality deficit",
        "H1 materially improves it",
        "no critical or protected-behavior regression",
        "Judge conditional efficacy on entry-positive cases",
        "applicability",
        "do not infer prevalence from fixture frequency",
    ))
    record = section(behavior, "## Record the result")
    assert set(re.findall(
        r"`(accept|reject-no-control-deficit|reject-insufficient-contribution|reject-regression|needs-more-evidence|blocked)`",
        behavior,
    )) == TERMINAL
    require_all(record, (
        "Complete with exactly one of",
        "residual transfer gap",
        "Reserve `reject-regression` for an observed critical or protected-behavior regression",
    ))

    require_all(normalized(glossary), (
        "Implicitly invocable",
        "Description",
        "Common behavior",
        "Branch-only reference",
        "Completion criterion",
        "Persistent early-stop defect",
        "Single owner",
        "No-op",
    ))

    forbidden = (
        "When observed runs miss must-have branch material behind a weak pointer",
        "sharpen it to name the target, condition, and load/apply action",
        "inline only if a fresh entry-positive check still misses",
    )
    assert not any(normalized(item) in package for item in forbidden)

    router = (ROOT / "skills/custom/skill-router/SKILL.md").read_text(encoding="utf-8")
    relationships = (ROOT / "docs/synthesis/skill-context-relationships.md").read_text(encoding="utf-8")
    assert "| Create, edit, or review Codex skills | `$writing-great-skills` |" in router
    relationship_flat = normalized(relationships)
    require_all(relationship_flat, (
        "writing-great-skills",
        "GLOSSARY.md",
        "BEHAVIOR-EVALS.md",
        "skill-creator",
        "new-package scaffolding and metadata mechanics",
        "stops after canonical proof",
        "does not absorb installation or delivery",
    ))

    epoch = Path(__file__).resolve().parent
    protocol = json.loads((epoch / "evals/prompt4/protocol-manifest.json").read_text(encoding="utf-8"))
    assert protocol["runtime"]["m0"]["tree_sha256"] == observed["sha256"]
    assert protocol["runtime"]["h1"]["tree_sha256"] == observed["sha256"]
    assert protocol["runtime"]["h1"]["equals"] == "M0"
    assert protocol["h1_contribution"]["status"] == "not-applicable"
    assert len(protocol["m0_viability_suite"]) == 13
    assert lint_worker_fixture(epoch / "evals/prompt4/worker-fixture.json") == {
        "status": "ok",
        "case_count": 2,
    }

    result = {
        "status": "pass",
        "candidate_root": str(candidate),
        "expected_tree_sha256": args.expected_tree_sha256,
        "independently_recomputed_tree_sha256": observed["sha256"],
        "algorithm": observed["algorithm"],
        "file_count": observed["file_count"],
        "identity_binding": "explicit-candidate-root",
        "canonical_runtime_resolved": False,
        "semantic_scope": ["M0-01..M0-10", "V01..V13", "M0-07", "M0-10", "F-01..F-07"],
        "relationship_scope": ["skill-router", "skill-creator", "GLOSSARY.md", "BEHAVIOR-EVALS.md", "installation-and-delivery-owners"],
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
