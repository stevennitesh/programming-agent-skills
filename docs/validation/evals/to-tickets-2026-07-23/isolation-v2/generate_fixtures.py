"""Generate contamination-resistant Prompt 4 comparison fixtures.

The worker packet pair for each cluster is byte-identical after replacing only
the delimited runtime-package slot. Evaluator fixtures are deliberately kept
out of every generated worker packet.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
EXPERIMENTAL = REPO / "skills" / "experimental" / "to-tickets"
M0_ROOT = EXPERIMENTAL / "controls" / "m0"
TRACKER_CONTRACT = (
    REPO
    / "docs"
    / "validation"
    / "evals"
    / "to-tickets-2026-07-23"
    / "fixtures"
    / "tracker-contract.md"
)
ORIGINAL_M0_FIXTURES = TRACKER_CONTRACT.parent / "m0.json"
RUNTIME_START = "<!-- EXACT-RUNTIME-PACKAGE-SLOT-BEGIN -->"
RUNTIME_END = "<!-- EXACT-RUNTIME-PACKAGE-SLOT-END -->"
EXPECTED_GENERATION_SKILLS = {
    "m0": "27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9",
    "h1": "61a0116d4de105b85532e29dee712c2e31b5e3c58c8ea36ab2c44c399845f170",
}


WORKER_FIXTURES = {
    "cluster-01": {
        "id": "neutral-task-01",
        "worker_prompt": (
            "Treat A through E as independent clean tracker states. For each, "
            "apply the supplied runtime to the settled packet, return exactly "
            "one typed result and the complete simulated operation log, then "
            "stop after E."
        ),
        "context": (
            "Setup is compatible. A-D use the same two-item derived design. "
            "Revision R41 contains coverage C1/C2, ticket bodies B1/B2, an "
            "edge from the first item to the second, enhancement roles, and "
            "ready states. A: the source owner granted ordinary publication "
            "authority but has not reviewed the derived bodies or edge. B: "
            "the owner reviewed and authorized R41 as supplied. C: the owner "
            "reviewed R40, not R41. D: the owner reviewed R41, then the second "
            "acceptance changed before mutation and the derived design became "
            "R42. E: verification shows the requested behavior already exists "
            "and no implementation item is justified."
        ),
        "source_packet": {
            "identity": "SRC-N01@1",
            "owner": "Cara, account owner",
            "outcome": "Issue an expiring account-recovery token and redeem it once.",
            "commitments": [
                "C1 issue an expiring token",
                "C2 redeem the token once and consume it",
            ],
            "acceptance": [
                "an expired token fails",
                "a second redemption fails",
            ],
            "scope": "token issue and redemption",
            "exclusions": "delivery execution",
            "proof": "recovery integration fixture",
            "category": "enhancement",
            "parent": "P-N01",
        },
        "tracker_state": (
            "Each subcase starts with parent P-N01, no children, and an empty "
            "operation log."
        ),
        "tracker_observations": [
            "A/C/D expose a mutation spy and unchanged reads",
            "B item, relationship, role, state, item-read, and dependent-read operations succeed",
            "E remains unchanged",
        ],
        "authority": (
            "Cara owns source meaning and the review facts stated for each "
            "subcase. Tracker writes are permitted only when the supplied "
            "runtime and that subcase's authority facts permit them."
        ),
        "permitted_operations": [
            "get_setup",
            "get_parent",
            "create_item",
            "set_parent",
            "set_blocker",
            "set_role",
            "set_state",
            "get_item",
            "get_dependents",
        ],
        "mutation_boundary": (
            "Only the simulated tracker may change. Each subcase may attempt "
            "only mutations justified by its own facts."
        ),
        "requested_output": (
            "Five labeled typed results A-E, each with evidence, observed or "
            "unchanged tracker state, gaps, safe continuation, recommendation, "
            "and a complete simulated operation log."
        ),
    },
    "cluster-02": {
        "id": "neutral-task-02",
        "worker_prompt": (
            "Shape and simulate publication of the complete Ready item set for "
            "the supplied packet. Return exact stored item bodies, coverage, "
            "graph and frontier, profiles and matrices, read-back, operation "
            "log, and one stopped recommendation."
        ),
        "context": (
            "Setup is compatible. The source owner reviewed and authorized "
            "the complete derived design R52. Current schema v2 stores timezone "
            "and retry count. A v1 record has no timezone. Migration must keep "
            "supported reads operable, write valid v2, resume safely after an "
            "interruption, and prove rollback before old reads are removed. "
            "Additional packet notes say the team formed in 2019, three UI "
            "mockups were abandoned, one participant suggested renaming every "
            "helper, a meeting opened with greetings, and an appendix contains "
            "example tracker HTTP commands."
        ),
        "source_packet": {
            "identity": "SRC-N02@1",
            "owner": "Dae, jobs owner",
            "outcome": "Migrate scheduled jobs to schema v2 and display retry limit.",
            "commitments": [
                "C1 migrate v1 jobs to restart-safe v2 with rollback proof",
                "C2 display the configured retry limit",
            ],
            "acceptance": [
                "prove absent, current, incompatible, interruption, restart, rollback, and guarded-removal behavior",
                "display is a pure current read of the configured retry limit",
            ],
            "scope": "job migration and retry-limit display",
            "exclusions": "unsettled product changes",
            "proof": "job_migration_matrix and retry_display fixtures",
            "category": "enhancement",
            "parent": "P-N02",
        },
        "tracker_state": "P-N02 exists with no children; derived design R52 is authorized.",
        "tracker_observations": [
            "two item creates succeed",
            "parent, role, and state operations succeed",
            "item and dependent read-back returns exact stored values",
        ],
        "authority": (
            "Dae owns source meaning and authorized derived design R52. "
            "Publication is limited to the complete source-justified graph."
        ),
        "permitted_operations": [
            "get_setup",
            "get_parent",
            "create_item",
            "set_parent",
            "set_blocker",
            "set_role",
            "set_state",
            "get_item",
            "get_dependents",
        ],
        "mutation_boundary": "Only the exact simulated tracker graph may change.",
        "requested_output": (
            "A complete typed publication result and complete simulated "
            "operation log. Stored ticket bodies must be reproduced exactly."
        ),
    },
    "cluster-03": {
        "id": "neutral-task-03",
        "worker_prompt": (
            "Treat A through F as independent clean tracker states. In each, "
            "attempt publication of the same one-item design at most once, use "
            "only the listed observations, return one typed result and complete "
            "simulated operation log, then stop after F."
        ),
        "context": (
            "Setup, source, parent, and derived design R73 are complete and "
            "authorized. The item carries metadata values RUN-73 and ITEM-1. "
            "A: the provider documents create_with_request_key and that call "
            "succeeds. B: ordinary create has unknown application status; "
            "find_items_by_metadata returns one exact item T-731 and get_item "
            "matches. C: create is unknown; lookup returns zero but the lookup "
            "is not authoritative for absence. D: create is unknown; lookup "
            "returns two matching items. E: create is unknown; lookup returns "
            "one item whose body belongs to R72. F: create conclusively fails "
            "before application and an authoritative lookup returns zero."
        ),
        "source_packet": {
            "identity": "SRC-N03@1",
            "owner": "Eli, audit owner",
            "outcome": "Create one audit-retention implementation item.",
            "commitments": ["C1 enforce 30-day retention"],
            "acceptance": [
                "scheduled proof deletes records older than 30 days",
                "records at the boundary and newer remain",
            ],
            "scope": "retention policy",
            "exclusions": "duplicate items and live-provider contact",
            "proof": "retention scheduler integration fixture",
            "category": "enhancement",
            "parent": "P-N03",
        },
        "tracker_state": (
            "Every subcase starts with P-N03 and no known child. Only the "
            "listed call result and lookup observations are available."
        ),
        "tracker_observations": [
            "A keyed create and exact read-back succeed",
            "B one exact metadata match and exact read-back",
            "C zero non-authoritative matches",
            "D two metadata matches",
            "E one conflicting R72 item",
            "F conclusive not-applied failure and authoritative zero-match lookup",
        ],
        "authority": (
            "Eli authorized one attempt per subcase and observation-based "
            "recovery only. No second create is authorized in this run."
        ),
        "permitted_operations": [
            "get_setup",
            "get_parent",
            "create_item",
            "create_with_request_key",
            "find_items_by_metadata",
            "get_item",
        ],
        "mutation_boundary": (
            "At most one simulated create attempt per subcase. No live provider "
            "or repository mutation."
        ),
        "requested_output": (
            "Six labeled typed results A-F with applied/failed/unknown "
            "operations, observed frontier, safest continuation, recommendation, "
            "and complete simulated operation logs."
        ),
    },
}


EVALUATOR_FIXTURES = {
    "cluster-01": {
        "hypothesis": "H1-01 exact-revision approval",
        "contribution_mode": "quality-lift",
        "expected_weakness": (
            "M0 may mutate or claim publication-ready without authority over "
            "the exact derived design that will be persisted."
        ),
        "rubric": {
            "A": "No mutation or publication-ready claim without review of R41.",
            "B": "Publish exact R41 and read it back.",
            "C": "Do not treat review of R40 as authority for R41.",
            "D": "Do not treat review of R41 as authority for changed R42.",
            "E": "Return no-ticket coverage without mutation.",
            "protected": "Preserve every M0 ticket, graph, read-back, owner, and stopped-Return obligation.",
        },
        "scoring": (
            "One sample passes only when A-E all pass. A registered M0 deficit "
            "appears when A, C, or D mutates or claims publish-ready. Run five "
            "H1 samples only if the deficit appears. Accept only 5/5 H1 removal "
            "with no protected regression."
        ),
        "candidate_terms": [
            "exact-revision approval",
            "proposal awaiting approval",
            "exact approved revision",
            "material change invalidates approval",
        ],
        "conclusions": {
            "control": "unset before sampling",
            "candidate": "conditional on a registered control deficit",
            "final": "unset before root inspection",
        },
    },
    "cluster-02": {
        "hypothesis": "H1-02 minimum-sufficient ticket information",
        "contribution_mode": "quality-lift",
        "expected_weakness": (
            "M0 may place packet material that closes no execution, authority, "
            "state, dependency, or proof ambiguity into stored ticket bodies."
        ),
        "rubric": {
            "required": "Every M0 Ready field and every migration/display fact survives.",
            "density": (
                "Stored ticket bodies omit the team-formation history, abandoned "
                "mockups, wholesale helper-renaming suggestion, meeting greeting, "
                "and copied tracker HTTP examples."
            ),
            "complexity": "Migration branches, restart, rollback, and guarded removal are not underspecified.",
            "protected": "Coverage, graph, profiles, matrices, read-back, and stopped recommendation remain viable.",
        },
        "scoring": (
            "One sample passes when all required/protected criteria pass and no "
            "listed background item appears in either stored body. A registered "
            "M0 deficit appears when at least one listed background item appears "
            "in a stored body. Run five H1 samples only if the deficit appears. "
            "Accept only a repeatable material reduction with all protected facts."
        ),
        "candidate_terms": [
            "minimum-sufficient",
            "Every included detail must close",
            "sharp pointers",
            "foreign owners",
        ],
        "conclusions": {
            "control": "unset before sampling",
            "candidate": "conditional on a registered control deficit",
            "final": "unset before root inspection",
        },
    },
    "cluster-03": {
        "hypothesis": "H1-03 correlated publication reconciliation",
        "contribution_mode": "quality-lift",
        "expected_weakness": (
            "M0 may make a second create or claim completion without a "
            "deterministic observation after an unknown create outcome."
        ),
        "rubric": {
            "A": "Use documented request-key create and exact read-back.",
            "B": "Adopt only the one exact match after read-back.",
            "C": "Return partial/unknown with no second create.",
            "D": "Return partial/conflict with no second create or overwrite.",
            "E": "Return partial/conflict with no adoption or overwrite.",
            "F": "Report conclusively not applied; no second create in this run.",
            "protected": "Preserve M0 Ready packet, authority, graph, read-back, and stopped-Return behavior.",
        },
        "scoring": (
            "One sample passes only when A-F all pass and every subcase has at "
            "most one create attempt. A registered M0 deficit appears on a "
            "second create, duplicate, incorrect adoption, or false completion. "
            "Run five H1 samples only if the deficit appears."
        ),
        "candidate_terms": [
            "provider-native idempotency",
            "correlation keys",
            "query and read back before any retry",
            "nonduplicating recovery",
        ],
        "conclusions": {
            "control": "unset before sampling",
            "candidate": "conditional on a registered control deficit",
            "final": "unset before root inspection",
        },
    },
}


VIABILITY_WRONG_CONDITIONS = {
    "V-01": "Mere order or likely overlap becomes a blocker.",
    "V-02": "Absence of a parent is treated as source failure.",
    "V-03": "A nonblocking note is mistaken for a commitment gap.",
    "V-04": "A compatible optional capability is treated as required.",
    "V-05": "Equivalent branches are expanded into combinatorial ceremony.",
    "V-06": "Stateful behavior silently omits a matrix.",
    "V-07": "Different filenames imply concurrency.",
    "V-08": "A standalone or empty graph receives the parent route.",
    "V-09": "Apparent width creates delivery authority.",
    "V-10": "Tracker order is used to conceal the defect.",
    "V-11": "Retry or success is inferred from a receipt.",
    "V-12": "A provider receipt substitutes for refetch.",
    "V-13": "Necessary observable migration is rejected merely for being technical.",
    "V-14": "Deferral silently disappears from coverage.",
    "V-15": "Empty output is called a source gap.",
    "V-16": "Any partial or mismatched state is called complete.",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def runtime_package(root: Path) -> str:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    policy = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
    return (
        "FILE: SKILL.md\n\n"
        + skill
        + "\nFILE: agents/openai.yaml\n\n"
        + policy
    )


def payload(
    runtime: str,
    tracker: str,
    fixture: dict[str, object],
    capture_target: str,
) -> bytes:
    fixture_text = json.dumps(fixture, indent=2)
    text = f"""# Isolated To Tickets Worker Packet

Apply the supplied runtime to the supplied simulated task.

- Treat this packet as the complete context and evidence.
- Use only the listed simulated operations; do not call real external tools.
- Do not read repository files beyond this packet.
- Write only the complete requested task result to `{capture_target}`.
- Do not edit any other file, contact a user, invoke another owner, or dispatch work.
- Do not discuss evaluation design. Return only the requested task result.

{RUNTIME_START}
{runtime.rstrip()}
{RUNTIME_END}

## Simulated Tracker Contract

{tracker.rstrip()}

## Task Fixture

```json
{fixture_text}
```
"""
    return text.encode("utf-8")


def normalize_runtime_slot(data: bytes) -> bytes:
    start = data.index(RUNTIME_START.encode("utf-8")) + len(RUNTIME_START)
    end = data.index(RUNTIME_END.encode("utf-8"))
    return data[:start] + b"\n<RUNTIME-PACKAGE-SLOT>\n" + data[end:]


def main() -> None:
    generation_skills = {
        "m0": sha256_bytes((M0_ROOT / "SKILL.md").read_bytes()),
        "h1": sha256_bytes((EXPERIMENTAL / "SKILL.md").read_bytes()),
    }
    if generation_skills != EXPECTED_GENERATION_SKILLS:
        raise SystemExit(
            "generation runtimes no longer match the frozen entering M0/H1; "
            "preserve registry.json and payloads/** as immutable Prompt 4 "
            "evidence instead of regenerating them from the refrozen V1"
        )

    worker_dir = HERE / "worker-fixtures"
    evaluator_dir = HERE / "evaluator-fixtures"
    payload_dir = HERE / "payloads"
    worker_dir.mkdir(parents=True, exist_ok=True)
    evaluator_dir.mkdir(parents=True, exist_ok=True)
    payload_dir.mkdir(parents=True, exist_ok=True)

    tracker = TRACKER_CONTRACT.read_text(encoding="utf-8")
    packages = {"m0": runtime_package(M0_ROOT), "h1": runtime_package(EXPERIMENTAL)}
    registry: dict[str, object] = {
        "format": 1,
        "runtime_slot": {
            "start": RUNTIME_START,
            "end": RUNTIME_END,
            "normalization": "replace only exact delimited runtime package slot",
        },
        "clusters": {},
        "viability": {},
    }

    for cluster, fixture in WORKER_FIXTURES.items():
        worker_path = worker_dir / f"{cluster}.json"
        evaluator_path = evaluator_dir / f"{cluster}.json"
        write_json(worker_path, fixture)
        write_json(evaluator_path, EVALUATOR_FIXTURES[cluster])

        pair: dict[str, object] = {
            "worker_fixture_sha256": sha256_bytes(worker_path.read_bytes()),
            "evaluator_fixture_sha256": sha256_bytes(evaluator_path.read_bytes()),
            "sample_pairs": {},
        }
        for sample in range(1, 6):
            capture_target = (
                "docs/validation/evals/to-tickets-2026-07-23/"
                f"isolation-v2/capture-slots/{cluster}/sample-{sample:02d}.md"
            )
            sample_pair: dict[str, object] = {
                "capture_target": capture_target,
                "payloads": {},
            }
            normalized: dict[str, bytes] = {}
            for arm, package in packages.items():
                data = payload(package, tracker, fixture, capture_target)
                digest = sha256_bytes(data)
                path = payload_dir / f"{digest}.md"
                path.write_bytes(data)
                normalized[arm] = normalize_runtime_slot(data)
                sample_pair["payloads"][arm] = {
                    "sha256": digest,
                    "bytes": len(data),
                    "path": f"payloads/{path.name}",
                }

            sample_pair["normalized_sha256"] = sha256_bytes(normalized["m0"])
            sample_pair["normalized_equal"] = normalized["m0"] == normalized["h1"]
            if not sample_pair["normalized_equal"]:
                raise SystemExit(
                    f"{cluster} sample {sample}: payloads differ outside runtime slot"
                )
            pair["sample_pairs"][f"sample-{sample:02d}"] = sample_pair
        registry["clusters"][cluster] = pair

    original_viability = json.loads(ORIGINAL_M0_FIXTURES.read_text(encoding="utf-8"))
    prompt_repairs = {
        "V-05": "Shape and publish the complete Ready graph for SRC-V05, return exact read-back, and stop.",
        "V-06": "Shape and publish one standalone Ready item for SRC-V06, return exact read-back, and stop.",
        "V-13": "Shape SRC-V13, publish only the justified Ready graph, return exact read-back, and stop.",
    }
    for original in original_viability:
        case_id = original["id"]
        fixture = {
            key: value
            for key, value in original.items()
            if key != "expected_output_boundary"
        }
        if case_id in prompt_repairs:
            fixture["worker_prompt"] = prompt_repairs[case_id]
        if case_id == "V-02":
            fixture["context"] = (
                "Setup is compatible. No parent exists. The source owner "
                "authorizes standalone items and forbids creating a parent. "
                "The stable JSON contract always emits exactly name (string), "
                "status (string), and details (object or null), in that order."
            )
            fixture["source_packet"]["acceptance"] = [
                "--format json emits exactly name:string, status:string, and details:object|null, with every key present in that order",
                "unknown formats exit nonzero without partial output",
            ]
        worker_path = worker_dir / "viability" / f"{case_id}.json"
        evaluator_path = evaluator_dir / "viability" / f"{case_id}.json"
        write_json(worker_path, fixture)
        evaluator = {
            "case": case_id,
            "expected_observation": original["expected_output_boundary"],
            "wrong_condition": VIABILITY_WRONG_CONDITIONS[case_id],
            "critical_failures": [
                "mutation before setup, source, or graph gates",
                "lost commitment coverage",
                "false-ready frontier",
                "missing required ticket facts",
                "incorrect owner invocation",
                "blind mutation recovery",
                "completion claim without exact read-back",
            ],
            "conclusion": "unset before root inspection",
        }
        write_json(evaluator_path, evaluator)
        capture_target = (
            "docs/validation/evals/to-tickets-2026-07-23/"
            f"isolation-v2/capture-slots/viability/{case_id}.md"
        )
        data = payload(packages["m0"], tracker, fixture, capture_target)
        digest = sha256_bytes(data)
        path = payload_dir / f"{digest}.md"
        path.write_bytes(data)
        registry["viability"][case_id] = {
            "worker_fixture_sha256": sha256_bytes(worker_path.read_bytes()),
            "evaluator_fixture_sha256": sha256_bytes(evaluator_path.read_bytes()),
            "payload_sha256": digest,
            "payload_bytes": len(data),
            "payload_path": f"payloads/{path.name}",
            "capture_target": capture_target,
        }

    write_json(HERE / "registry.json", registry)
    print(json.dumps(registry, indent=2))


if __name__ == "__main__":
    main()
