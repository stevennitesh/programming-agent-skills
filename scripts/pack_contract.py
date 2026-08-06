"""Pure Pack Composition Contract parsing, validation, and projection."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

CONTRACT_BEGIN = "<!-- pack-composition-contract:v1:begin -->"
CONTRACT_END = "<!-- pack-composition-contract:v1:end -->"
FINGERPRINT_PREFIX = "sha256-v1:"
FINGERPRINTED_SOURCE_RE = re.compile(r".+#sha256-v1:[0-9a-f]{64}$")
ROLES = {"router", "executable-aggregate", "leaf"}
RELATIONSHIP_VERBS = {
    "Load",
    "Invoke",
    "Compose",
    "Hand off",
    "Suggest only",
    "Recommend and stop",
}
RESULT_DECISIONS = {
    "integration-accepted",
    "needs-more-evidence",
    "blocked",
}
COLLISION_CLASSES = {
    "capability",
    "vocabulary",
    "authority",
    "mutation",
    "invocation",
    "completion",
    "Return/completion",
    "relationship",
    "context-load",
}
REQUIRED_COLLISION_CLASSES = {
    "invocation",
    "capability",
    "authority",
    "mutation",
    "vocabulary",
    "Return/completion",
    "relationship",
    "context-load",
}
FORBIDDEN_SEMANTIC_FIELDS = {
    "h1",
    "admission",
    "admission_decision",
    "adoption",
    "recommendation",
    "rubric_score",
    "validation_judgment",
}


class PackContractError(ValueError):
    """Raised when canonical Pack Contract bytes cannot be parsed."""


def exact_fingerprint(payload: object) -> str:
    content = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"{FINGERPRINT_PREFIX}{hashlib.sha256(content).hexdigest()}"


def create_draft() -> dict[str, object]:
    """Return an inactive schema-shaped draft without selecting composition."""

    return {
        "epoch_header": {
            "schema_version": 1,
            "composition_epoch_id": None,
            "contract_revision": 0,
            "status": "draft",
            "fixed_point": {
                "repository_tree": None,
                "environment": None,
                "timestamp": None,
            },
            "intended_pack_outcome": None,
            "scope": [],
            "exclusions": [],
            "research_bound": {
                "independent_passes": 1,
                "catalog_reconciliation_passes": 1,
                "named_gap_passes": 1,
            },
            "source_pointers": [],
            "acceptance_scenarios": [],
            "load_budget_policy": {
                "metric": None,
                "ceiling_or_class": None,
                "status": "gap",
            },
            "campaign_proof_graph": [],
            "integration_result": {
                "decision": None,
                "evidence_pointer": None,
            },
            "epoch_lock": None,
        },
        "capabilities": [],
        "selected_skills": [],
        "relationships": [],
        "exclusions_collisions_gaps": [],
    }


def render_contract(
    contract: dict[str, object],
    *,
    introduction: str = "# Pack Composition Contract\n",
) -> str:
    prefix = introduction.rstrip() + "\n\n"
    payload = json.dumps(
        contract,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    return (
        f"{prefix}{CONTRACT_BEGIN}\n"
        "```json\n"
        f"{payload}\n"
        "```\n"
        f"{CONTRACT_END}\n"
    )


def parse_contract(content: str) -> dict[str, object]:
    if content.count(CONTRACT_BEGIN) != 1 or content.count(CONTRACT_END) != 1:
        raise PackContractError("Pack Contract markers must occur exactly once")
    start = content.index(CONTRACT_BEGIN) + len(CONTRACT_BEGIN)
    end = content.index(CONTRACT_END)
    if start >= end:
        raise PackContractError("Pack Contract markers are reversed")
    bounded = content[start:end].strip()
    if not bounded.startswith("```json\n") or not bounded.endswith("\n```"):
        raise PackContractError("Pack Contract must contain one bounded JSON fence")
    try:
        payload = json.loads(bounded[len("```json\n") : -len("\n```")])
    except json.JSONDecodeError as error:
        raise PackContractError(f"Pack Contract JSON is invalid: {error}") from error
    if not isinstance(payload, dict):
        raise PackContractError("Pack Contract payload must be an object")
    return payload


def semantic_fingerprint(content: str) -> str:
    """Fingerprint decision-bearing content only, excluding commentary."""

    return exact_fingerprint(parse_contract(content))


def _schema_failures(contract: object) -> list[str]:
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "docs/validation/shared/schemas/"
        "pack-composition-contract-v1.schema.json"
    )
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError, TypeError) as error:
        return [f"Pack Contract schema is unavailable or invalid: {error}"]
    return [
        "Pack Contract schema failure at "
        f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(contract),
            key=lambda item: list(item.absolute_path),
        )
    ]


def validate_contract(contract: object, *, for_freeze: bool = False) -> list[str]:
    if not isinstance(contract, dict):
        return ["Pack Contract must be an object"]
    expected = {
        "epoch_header",
        "capabilities",
        "selected_skills",
        "relationships",
        "exclusions_collisions_gaps",
    }
    failures: list[str] = []
    if set(contract) != expected:
        failures.append("Pack Contract must expose exactly its five settled parts")
    schema_failures = _schema_failures(contract)
    failures.extend(schema_failures)
    header = contract.get("epoch_header")
    if not isinstance(header, dict):
        failures.append("Pack Contract has no epoch header")
        return failures
    if header.get("schema_version") != 1:
        failures.append("Pack Contract schema_version must be 1")
    if header.get("status") not in {
        "draft",
        "frozen",
        "integration-accepted",
    }:
        failures.append("Pack Contract status is invalid")
    for ledger in (
        "capabilities",
        "selected_skills",
        "relationships",
        "exclusions_collisions_gaps",
    ):
        if not isinstance(contract.get(ledger), list):
            failures.append(f"{ledger} must be a list")
    failures.extend(_forbidden_field_failures(contract))
    if all(isinstance(contract.get(key), list) for key in expected - {"epoch_header"}):
        try:
            failures.extend(_ledger_failures(contract))
        except (AttributeError, TypeError, ValueError) as error:
            failures.append(f"Pack Contract ledgers are malformed: {error}")
    if for_freeze:
        if header.get("status") != "draft":
            failures.append("Only a draft can be frozen")
        if not header.get("composition_epoch_id"):
            failures.append("Freeze requires composition_epoch_id")
        if not header.get("intended_pack_outcome"):
            failures.append("Freeze requires intended_pack_outcome")
        if not contract.get("selected_skills"):
            failures.append("Freeze requires selected skills")
        if header.get("integration_result") != {
            "decision": None,
            "evidence_pointer": None,
        }:
            failures.append("Freeze requires a pending integration result")
        if header.get("epoch_lock") is not None:
            failures.append("Freeze rejects a premature epoch Lock")
        fixed_point = header.get("fixed_point")
        if not isinstance(fixed_point, dict) or any(
            not fixed_point.get(key)
            for key in ("repository_tree", "environment", "timestamp")
        ):
            failures.append("Freeze requires a complete fixed point")
        if header.get("contract_revision") != 1:
            failures.append("Initial freeze requires contract_revision 1")
        research_bound = header.get("research_bound")
        if research_bound != {
            "independent_passes": 1,
            "catalog_reconciliation_passes": 1,
            "named_gap_passes": 1,
        }:
            failures.append("Freeze requires the settled bounded research policy")
        if not header.get("acceptance_scenarios"):
            failures.append("Freeze requires acceptance scenarios")
        source_pointers = header.get("source_pointers")
        if (
            not isinstance(source_pointers, list)
            or not source_pointers
            or any(
                not isinstance(pointer, str)
                or FINGERPRINTED_SOURCE_RE.fullmatch(pointer) is None
                for pointer in source_pointers
            )
        ):
            failures.append("Freeze requires content-addressed source pointers")
        load_budget = header.get("load_budget_policy")
        if not isinstance(load_budget, dict) or load_budget.get("status") != "set":
            failures.append("Freeze requires a set load budget policy")
        issues = contract.get("exclusions_collisions_gaps", [])
        represented_collision_classes = {
            issue.get("class")
            for issue in issues
            if isinstance(issue, dict)
        }
        missing_collision_classes = sorted(
            REQUIRED_COLLISION_CLASSES - represented_collision_classes
        )
        if missing_collision_classes:
            failures.append(
                "Freeze requires every collision class: "
                + ", ".join(missing_collision_classes)
            )
        for collision_class in sorted(REQUIRED_COLLISION_CLASSES):
            resolved_rows = [
                issue
                for issue in issues
                if isinstance(issue, dict)
                and issue.get("class") == collision_class
                and issue.get("status") == "resolved"
            ]
            if not any(
                isinstance(issue.get("resolution"), str)
                and bool(issue["resolution"].strip())
                and isinstance(
                    issue.get("negative_control_scenario_id"), str
                )
                and bool(issue["negative_control_scenario_id"].strip())
                for issue in resolved_rows
            ):
                failures.append(
                    "Freeze requires substantive resolved evidence for "
                    f"{collision_class} collision"
                )
        for issue in issues:
            if not isinstance(issue, dict):
                continue
            if issue.get("status") != "resolved" and (
                issue.get("essential")
                or issue.get("class") in COLLISION_CLASSES
            ):
                failures.append(
                    f"Freeze rejects unresolved {issue.get('class')} issue "
                    f"{issue.get('issue_id')}"
                )
            if (
                issue.get("status") == "deferred"
                and not issue.get("essential")
                and (
                    not issue.get("future_owner_or_stopping_condition")
                    or not issue.get("nondependency_proof_ids")
                )
            ):
                failures.append(
                    f"Deferred issue {issue.get('issue_id')} requires a future "
                    "owner or stopping condition and nondependency proof"
                )
        try:
            campaign_order(contract)
        except PackContractError as error:
            failures.append(str(error))
    return failures


def freeze_contract(contract: dict[str, object]) -> dict[str, object]:
    failures = validate_contract(contract, for_freeze=True)
    if failures:
        return {
            "status": "contract-invalid",
            "contract": deepcopy(contract),
            "failures": failures,
        }
    frozen = deepcopy(contract)
    frozen["epoch_header"]["status"] = "frozen"  # type: ignore[index]
    return {
        "status": "contract-frozen",
        "contract": frozen,
        "fingerprint": contract_fingerprint(frozen),
        "failures": [],
    }


def contract_fingerprint(contract: dict[str, object]) -> str:
    """Fingerprint frozen composition semantics, excluding runtime progress."""

    projection = deepcopy(contract)
    header = projection.get("epoch_header")
    if isinstance(header, dict):
        header["status"] = "frozen"
        header["integration_result"] = {
            "decision": None,
            "evidence_pointer": None,
        }
        header["epoch_lock"] = None
    return exact_fingerprint(projection)


def _forbidden_field_failures(value: object, path: str = "$") -> list[str]:
    failures: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.casefold() in FORBIDDEN_SEMANTIC_FIELDS:
                failures.append(f"forbidden semantic field at {child_path}")
            failures.extend(_forbidden_field_failures(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            failures.extend(_forbidden_field_failures(child, f"{path}[{index}]"))
    return failures


def _unique_ids(
    rows: list[object],
    *,
    field: str,
    prefix: str,
    ledger: str,
) -> tuple[set[str], list[str]]:
    identifiers: set[str] = set()
    failures: list[str] = []
    pattern = re.compile(rf"^{re.escape(prefix)}-\d{{3}}$")
    for row in rows:
        if not isinstance(row, dict):
            failures.append(f"{ledger} rows must be objects")
            continue
        identifier = row.get(field)
        if not isinstance(identifier, str) or not pattern.fullmatch(identifier):
            failures.append(f"{ledger} has invalid {field}")
            continue
        if identifier in identifiers:
            failures.append(f"{ledger} has duplicate {field} {identifier}")
        identifiers.add(identifier)
    return identifiers, failures


def _ledger_failures(contract: dict[str, object]) -> list[str]:
    capabilities = contract["capabilities"]
    skills = contract["selected_skills"]
    relationships = contract["relationships"]
    issues = contract["exclusions_collisions_gaps"]
    assert isinstance(capabilities, list)
    assert isinstance(skills, list)
    assert isinstance(relationships, list)
    assert isinstance(issues, list)

    capability_ids, failures = _unique_ids(
        capabilities,
        field="capability_id",
        prefix="CAP",
        ledger="capabilities",
    )
    skill_ids, more = _unique_ids(
        skills,
        field="skill_id",
        prefix="SK",
        ledger="selected_skills",
    )
    failures.extend(more)
    relationship_ids, more = _unique_ids(
        relationships,
        field="relationship_id",
        prefix="REL",
        ledger="relationships",
    )
    failures.extend(more)
    _, more = _unique_ids(
        issues,
        field="issue_id",
        prefix="ECG",
        ledger="exclusions_collisions_gaps",
    )
    failures.extend(more)

    skill_by_id = {
        row.get("skill_id"): row for row in skills if isinstance(row, dict)
    }
    header = contract["epoch_header"]
    assert isinstance(header, dict)
    scenario_rows = header.get("acceptance_scenarios", [])
    scenario_ids: set[str] = set()
    for scenario in scenario_rows:
        if not isinstance(scenario, dict):
            continue
        scenario_id = scenario.get("scenario_id")
        if scenario_id in scenario_ids:
            failures.append(f"duplicate acceptance scenario {scenario_id}")
        elif isinstance(scenario_id, str):
            scenario_ids.add(scenario_id)
        if scenario.get("expected_owner_skill_id") not in skill_ids:
            failures.append(
                f"acceptance scenario {scenario_id} has unknown expected owner"
            )
    owner_claims: dict[str, list[str]] = defaultdict(list)
    for row in skills:
        if not isinstance(row, dict):
            continue
        skill_id = row.get("skill_id")
        if row.get("primary_role") not in ROLES:
            failures.append(f"skill {skill_id} has invalid primary role")
        if not isinstance(row.get("contract_order"), int):
            failures.append(f"skill {skill_id} requires integer contract order")
        for capability_id in row.get("owned_capability_ids", []):
            if capability_id not in capability_ids:
                failures.append(
                    f"skill {skill_id} references unknown capability {capability_id}"
                )
            owner_claims[capability_id].append(str(skill_id))
        for relationship_id in row.get("relationship_ids", []):
            if relationship_id not in relationship_ids:
                failures.append(
                    f"skill {skill_id} references unknown relationship "
                    f"{relationship_id}"
                )
        for scenario_id in row.get("acceptance_scenario_ids", []):
            if scenario_id not in scenario_ids:
                failures.append(
                    f"skill {skill_id} references unknown acceptance scenario "
                    f"{scenario_id}"
                )

    for row in capabilities:
        if not isinstance(row, dict):
            continue
        capability_id = row.get("capability_id")
        owner = row.get("primary_owner_skill_id")
        if row.get("disposition") == "selected":
            if owner not in skill_ids:
                failures.append(
                    f"capability {capability_id} has no selected primary ownership"
                )
            claims = owner_claims.get(str(capability_id), [])
            if claims != [owner]:
                failures.append(
                    f"capability {capability_id} ownership must be claimed "
                    "exactly once by its primary owner"
                )
        if row.get("essential") and row.get("disposition") != "selected":
            failures.append(
                f"essential capability {capability_id} cannot be deferred or excluded"
            )
        for contributor in row.get("allowed_contributor_skill_ids", []):
            if contributor not in skill_ids:
                failures.append(
                    f"capability {capability_id} references unknown contributor"
                )
        for scenario_id in row.get("acceptance_scenario_ids", []):
            if scenario_id not in scenario_ids:
                failures.append(
                    f"capability {capability_id} references unknown acceptance "
                    f"scenario {scenario_id}"
                )

    relationship_by_id = {
        row.get("relationship_id"): row
        for row in relationships
        if isinstance(row, dict)
    }
    for row in relationships:
        if not isinstance(row, dict):
            continue
        relationship_id = row.get("relationship_id")
        caller = row.get("caller_skill_id")
        target = row.get("target_skill_id")
        verb = row.get("verb")
        if verb not in RELATIONSHIP_VERBS:
            failures.append(
                f"relationship verb {verb!r} is invalid for {relationship_id}"
            )
        if caller not in skill_ids or target not in skill_ids:
            failures.append(
                f"relationship {relationship_id} references an unknown skill"
            )
        caller_row = skill_by_id.get(caller)
        if (
            isinstance(caller_row, dict)
            and relationship_id not in caller_row.get("relationship_ids", [])
        ):
            failures.append(
                f"relationship {relationship_id} is not owned by caller {caller}"
            )
        target_row = skill_by_id.get(target)
        explicit_target_authority = row.get("explicit_target_authority")
        if (
            isinstance(target_row, dict)
            and target_row.get("invocation_mode") == "explicit-only"
            and verb != "Recommend and stop"
            and explicit_target_authority != "exact-user-approved-packet"
        ):
            failures.append(
                f"explicit-only target {target} requires Recommend and stop"
            )
        if explicit_target_authority is not None and (
            not isinstance(target_row, dict)
            or target_row.get("invocation_mode") != "explicit-only"
            or verb == "Recommend and stop"
        ):
            failures.append(
                f"relationship {relationship_id} has inapplicable "
                "explicit_target_authority"
            )
        for capability_id in row.get("affected_capability_ids", []):
            if capability_id not in capability_ids:
                failures.append(
                    f"relationship {relationship_id} references unknown capability"
                )
        for owner_field in (
            "resume_owner_skill_id",
            "combined_exit_owner_skill_id",
        ):
            if row.get(owner_field) not in skill_ids:
                failures.append(
                    f"relationship {relationship_id} has invalid {owner_field}"
                )
        ordering = row.get("ordering_impact")
        if ordering not in {
            "callee-before-caller",
            "caller-before-callee",
            "none",
        }:
            failures.append(
                f"relationship {relationship_id} has invalid ordering impact"
            )
        else:
            graph_edges = {
                (
                    edge.get("predecessor_skill_id"),
                    edge.get("successor_skill_id"),
                )
                for edge in contract["epoch_header"].get(
                    "campaign_proof_graph", []
                )
                if isinstance(edge, dict)
            }
            required_edge = {
                "callee-before-caller": (target, caller),
                "caller-before-callee": (caller, target),
                "none": None,
            }[ordering]
            if required_edge is not None and required_edge not in graph_edges:
                failures.append(
                    f"relationship ordering for {relationship_id} is missing "
                    "from campaign proof graph"
                )

    for row in issues:
        if not isinstance(row, dict):
            continue
        issue_id = row.get("issue_id")
        if row.get("class") not in {
            "exclusion",
            "gap",
            *COLLISION_CLASSES,
        }:
            failures.append(f"issue {issue_id} has invalid class")
        for skill_id in row.get("involved_skill_ids", []):
            if skill_id not in skill_ids:
                failures.append(f"issue {issue_id} references unknown skill")
        for capability_id in row.get("involved_capability_ids", []):
            if capability_id not in capability_ids:
                failures.append(f"issue {issue_id} references unknown capability")
        negative_scenario = row.get("negative_control_scenario_id")
        if (
            negative_scenario is not None
            and negative_scenario not in scenario_ids
        ):
            failures.append(
                f"issue {issue_id} references unknown negative-control scenario"
            )

    # A relationship row must not exist without the caller's ownership claim.
    for relationship_id, row in relationship_by_id.items():
        caller = row.get("caller_skill_id")
        if relationship_id not in skill_by_id.get(caller, {}).get(
            "relationship_ids", []
        ):
            failures.append(
                f"relationship {relationship_id} lacks caller ownership"
            )
    return failures


def _graph(contract: dict[str, object]) -> tuple[dict[str, set[str]], dict[str, int]]:
    header = contract.get("epoch_header", {})
    skills = contract.get("selected_skills", [])
    if not isinstance(header, dict) or not isinstance(skills, list):
        raise PackContractError("campaign graph requires a valid contract")
    skill_ids = {
        row.get("skill_id")
        for row in skills
        if isinstance(row, dict) and isinstance(row.get("skill_id"), str)
    }
    successors = {skill_id: set() for skill_id in skill_ids}
    indegree = {skill_id: 0 for skill_id in skill_ids}
    edges = header.get("campaign_proof_graph")
    if not isinstance(edges, list):
        raise PackContractError("campaign proof graph must be a list")
    seen: set[tuple[str, str]] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise PackContractError("campaign proof graph edges must be objects")
        predecessor = edge.get("predecessor_skill_id")
        successor = edge.get("successor_skill_id")
        if predecessor not in skill_ids or successor not in skill_ids:
            raise PackContractError("campaign proof graph references unknown skill")
        if predecessor == successor:
            raise PackContractError("campaign proof graph has a self cycle")
        pair = (str(predecessor), str(successor))
        if pair in seen:
            raise PackContractError("campaign proof graph has duplicate edge")
        seen.add(pair)
        successors[str(predecessor)].add(str(successor))
        indegree[str(successor)] += 1
    return successors, indegree


def campaign_order(contract: dict[str, object]) -> list[str]:
    """Return the deterministic, dependency-respecting campaign order."""

    successors, indegree = _graph(contract)
    skills = contract.get("selected_skills", [])
    assert isinstance(skills, list)
    metadata = {
        row["skill_id"]: (
            {"leaf": 0, "executable-aggregate": 1, "router": 2}.get(
                row.get("primary_role"), 3
            ),
            row.get("contract_order", 0),
            row["skill_id"],
        )
        for row in skills
        if isinstance(row, dict) and isinstance(row.get("skill_id"), str)
    }
    ready = sorted(
        (skill_id for skill_id, degree in indegree.items() if degree == 0),
        key=metadata.__getitem__,
    )
    ordered: list[str] = []
    while ready:
        skill_id = ready.pop(0)
        ordered.append(skill_id)
        for successor in sorted(successors[skill_id], key=metadata.__getitem__):
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
                ready.sort(key=metadata.__getitem__)
    if len(ordered) != len(indegree):
        raise PackContractError("campaign proof graph contains a hard cycle")
    return ordered


def contract_slice(
    contract: dict[str, object],
    skill_id: str,
) -> dict[str, object]:
    """Project an immutable skill-local admission packet from a frozen contract."""

    header = contract.get("epoch_header")
    if (
        not isinstance(header, dict)
        or header.get("status") != "frozen"
        or header.get("epoch_lock") is not None
    ):
        return {"status": "contract-not-frozen"}
    skills = contract.get("selected_skills", [])
    skill = next(
        (
            row
            for row in skills
            if isinstance(row, dict) and row.get("skill_id") == skill_id
        ),
        None,
    )
    if skill is None:
        return {"status": "skill-not-selected", "skill_id": skill_id}
    predecessors = {
        edge.get("predecessor_skill_id")
        for edge in header.get("campaign_proof_graph", [])
        if isinstance(edge, dict) and edge.get("successor_skill_id") == skill_id
    }
    capabilities = [
        deepcopy(row)
        for row in contract.get("capabilities", [])
        if isinstance(row, dict)
        and row.get("primary_owner_skill_id") == skill_id
    ]
    relationships = [
        deepcopy(row)
        for row in contract.get("relationships", [])
        if isinstance(row, dict)
        and skill_id
        in {
            row.get("caller_skill_id"),
            row.get("target_skill_id"),
            row.get("resume_owner_skill_id"),
            row.get("combined_exit_owner_skill_id"),
        }
    ]
    issues = [
        deepcopy(row)
        for row in contract.get("exclusions_collisions_gaps", [])
        if isinstance(row, dict)
        and (
            skill_id in row.get("involved_skill_ids", [])
            or any(
                capability.get("capability_id")
                in row.get("involved_capability_ids", [])
                for capability in capabilities
            )
        )
    ]
    proof_edges = [
        deepcopy(edge)
        for edge in header.get("campaign_proof_graph", [])
        if isinstance(edge, dict)
        and skill_id
        in {
            edge.get("predecessor_skill_id"),
            edge.get("successor_skill_id"),
        }
    ]
    epoch_id = header.get("composition_epoch_id")
    revision = header.get("contract_revision")
    scenario_ids = set(skill.get("acceptance_scenario_ids", []))
    for capability in capabilities:
        scenario_ids.update(capability.get("acceptance_scenario_ids", []))
    scenario_ids.update(
        issue.get("negative_control_scenario_id")
        for issue in issues
        if issue.get("negative_control_scenario_id") is not None
    )
    scenarios = [
        deepcopy(scenario)
        for scenario in header.get("acceptance_scenarios", [])
        if isinstance(scenario, dict)
        and (
            scenario.get("scenario_id") in scenario_ids
            or scenario.get("expected_owner_skill_id") == skill_id
        )
    ]
    projection = {
        "slice_id": f"{epoch_id}:r{revision}:{skill_id}",
        "composition_epoch_id": epoch_id,
        "contract_revision": revision,
        "contract_fingerprint": contract_fingerprint(contract),
        "fixed_point": deepcopy(header.get("fixed_point")),
        "research_bound": deepcopy(header.get("research_bound")),
        "source_pointers": deepcopy(header.get("source_pointers")),
        "acceptance_scenarios": scenarios,
        "load_budget_policy": deepcopy(header.get("load_budget_policy")),
        "skill": deepcopy(skill),
        "capabilities": capabilities,
        "relationships": relationships,
        "issues": issues,
        "campaign_proof_edges": proof_edges,
    }
    return {
        "status": "contract-slice",
        "slice": projection,
        "slice_fingerprint": exact_fingerprint(projection),
    }


def contract_blueprint(
    contract: dict[str, object],
    skill_id: str,
) -> dict[str, object]:
    """Project one immutable slice before its predecessors are campaign-ready."""

    header = contract.get("epoch_header")
    if (
        not isinstance(header, dict)
        or header.get("status") != "frozen"
        or header.get("epoch_lock") is not None
    ):
        return {"status": "contract-not-frozen"}
    predecessors = sorted(
        str(edge["predecessor_skill_id"])
        for edge in header.get("campaign_proof_graph", [])
        if isinstance(edge, dict)
        and edge.get("successor_skill_id") == skill_id
        and isinstance(edge.get("predecessor_skill_id"), str)
    )
    projected = contract_slice(contract, skill_id)
    if projected.get("status") != "contract-slice":
        return projected
    return {
        "status": "contract-slice-blueprint",
        "slice": projected["slice"],
        "slice_fingerprint": projected["slice_fingerprint"],
        "predecessor_skill_ids": predecessors,
    }




def _descendants(contract: dict[str, object], roots: Iterable[str]) -> set[str]:
    successors, _ = _graph(contract)
    affected = set(roots)
    pending = list(roots)
    while pending:
        for successor in successors.get(pending.pop(), set()):
            if successor not in affected:
                affected.add(successor)
                pending.append(successor)
    return affected


def assess_amendment(
    frozen: dict[str, object],
    proposed: dict[str, object],
    *,
    proof_registry: dict[str, list[str]],
) -> dict[str, object]:
    """Describe semantic blast radius without mutating either contract."""

    current_header = frozen.get("epoch_header", {})
    proposed_header = proposed.get("epoch_header", {})
    if not isinstance(current_header, dict) or not isinstance(proposed_header, dict):
        return {"status": "contract-incompatible", "failures": ["missing header"]}
    if current_header.get("epoch_lock") is not None:
        return {
            "status": "contract-incompatible",
            "failures": ["a locked epoch cannot be amended"],
        }
    if proposed_header.get("epoch_lock") is not None:
        return {
            "status": "contract-incompatible",
            "failures": ["an amendment cannot inject an epoch Lock"],
        }
    if current_header.get("status") not in {
        "frozen",
        "integration-accepted",
    }:
        return {
            "status": "contract-incompatible",
            "failures": ["amendment source must be frozen"],
        }
    if proposed_header.get("composition_epoch_id") != current_header.get(
        "composition_epoch_id"
    ):
        return {
            "status": "contract-incompatible",
            "failures": ["amendment must preserve composition epoch identity"],
        }
    required_revision = current_header.get("contract_revision", 0) + 1
    if proposed_header.get("contract_revision") != required_revision:
        return {
            "status": "contract-incompatible",
            "required_contract_revision": required_revision,
            "failures": ["amendment must increment contract revision by exactly one"],
        }
    proposal_failures = validate_contract(proposed)
    if proposal_failures:
        return {
            "status": "contract-incompatible",
            "required_contract_revision": required_revision,
            "failures": proposal_failures,
        }

    current_skills = {
        row["skill_id"]: row
        for row in frozen.get("selected_skills", [])
        if isinstance(row, dict) and isinstance(row.get("skill_id"), str)
    }
    proposed_skills = {
        row["skill_id"]: row
        for row in proposed.get("selected_skills", [])
        if isinstance(row, dict) and isinstance(row.get("skill_id"), str)
    }
    direct = {
        skill_id
        for skill_id in set(current_skills) | set(proposed_skills)
        if current_skills.get(skill_id) != proposed_skills.get(skill_id)
    }
    row_bound_stale: set[str] = set()
    current_capabilities = {
        row.get("capability_id"): row
        for row in frozen.get("capabilities", [])
        if isinstance(row, dict)
    }
    proposed_capabilities = {
        row.get("capability_id"): row
        for row in proposed.get("capabilities", [])
        if isinstance(row, dict)
    }
    current_relationships = {
        row.get("relationship_id"): row
        for row in frozen.get("relationships", [])
        if isinstance(row, dict)
    }
    proposed_relationships = {
        row.get("relationship_id"): row
        for row in proposed.get("relationships", [])
        if isinstance(row, dict)
    }

    def recruit_capabilities(capability_ids: Iterable[object]) -> None:
        identifiers = {
            value for value in capability_ids if isinstance(value, str)
        }
        for capability_id in identifiers:
            for row in (
                current_capabilities.get(capability_id),
                proposed_capabilities.get(capability_id),
            ):
                if not isinstance(row, dict):
                    continue
                owner = row.get("primary_owner_skill_id")
                if isinstance(owner, str):
                    direct.add(owner)
                direct.update(
                    value
                    for value in row.get("allowed_contributor_skill_ids", [])
                    if isinstance(value, str)
                )
        for row in [
            *current_relationships.values(),
            *proposed_relationships.values(),
        ]:
            if identifiers & set(row.get("affected_capability_ids", [])):
                direct.update(
                    value
                    for field in (
                        "caller_skill_id",
                        "target_skill_id",
                        "resume_owner_skill_id",
                        "combined_exit_owner_skill_id",
                    )
                    if isinstance((value := row.get(field)), str)
                )
    broad_header = {
        "fixed_point",
        "intended_pack_outcome",
        "scope",
        "exclusions",
        "research_bound",
        "source_pointers",
        "load_budget_policy",
    }
    if any(current_header.get(key) != proposed_header.get(key) for key in broad_header):
        direct.update(current_skills)

    current_scenarios = {
        row.get("scenario_id"): row
        for row in current_header.get("acceptance_scenarios", [])
        if isinstance(row, dict)
    }
    proposed_scenarios = {
        row.get("scenario_id"): row
        for row in proposed_header.get("acceptance_scenarios", [])
        if isinstance(row, dict)
    }
    changed_scenarios = {
        scenario_id
        for scenario_id in set(current_scenarios) | set(proposed_scenarios)
        if current_scenarios.get(scenario_id) != proposed_scenarios.get(scenario_id)
    }
    for skill_id, row in {**current_skills, **proposed_skills}.items():
        owned_scenario_ids = set(row.get("acceptance_scenario_ids", []))
        for capability_id in row.get("owned_capability_ids", []):
            for capability in (
                current_capabilities.get(capability_id),
                proposed_capabilities.get(capability_id),
            ):
                if isinstance(capability, dict):
                    owned_scenario_ids.update(
                        capability.get("acceptance_scenario_ids", [])
                    )
        expected_owner_ids = {
            scenario_id
            for scenario_id in changed_scenarios
            if (
                current_scenarios.get(scenario_id, {}).get(
                    "expected_owner_skill_id"
                )
                == skill_id
                or proposed_scenarios.get(scenario_id, {}).get(
                    "expected_owner_skill_id"
                )
                == skill_id
            )
        }
        if changed_scenarios & owned_scenario_ids or expected_owner_ids:
            direct.add(skill_id)
    for issue in [
        *(
            row
            for row in frozen.get("exclusions_collisions_gaps", [])
            if isinstance(row, dict)
        ),
        *(
            row
            for row in proposed.get("exclusions_collisions_gaps", [])
            if isinstance(row, dict)
        ),
    ]:
        if issue.get("negative_control_scenario_id") in changed_scenarios:
            direct.update(
                value
                for value in issue.get("involved_skill_ids", [])
                if isinstance(value, str)
            )
            recruit_capabilities(issue.get("involved_capability_ids", []))
            row_bound_stale.update(
                value
                for value in issue.get("nondependency_proof_ids", [])
                if isinstance(value, str)
            )

    current_edges = {
        (
            row.get("predecessor_skill_id"),
            row.get("successor_skill_id"),
        )
        for row in current_header.get("campaign_proof_graph", [])
        if isinstance(row, dict)
    }
    proposed_edges = {
        (
            row.get("predecessor_skill_id"),
            row.get("successor_skill_id"),
        )
        for row in proposed_header.get("campaign_proof_graph", [])
        if isinstance(row, dict)
    }
    for edge in current_edges ^ proposed_edges:
        direct.update(value for value in edge if isinstance(value, str))

    for ledger, id_field, owner_fields in (
        ("capabilities", "capability_id", ("primary_owner_skill_id",)),
        (
            "relationships",
            "relationship_id",
            (
                "caller_skill_id",
                "target_skill_id",
                "resume_owner_skill_id",
                "combined_exit_owner_skill_id",
            ),
        ),
        ("exclusions_collisions_gaps", "issue_id", ()),
    ):
        current_rows = frozen.get(ledger, [])
        proposed_rows = proposed.get(ledger, [])
        if current_rows == proposed_rows:
            continue
        current_by_id = {
            row.get(id_field): row
            for row in current_rows
            if isinstance(row, dict)
        }
        proposed_by_id = {
            row.get(id_field): row
            for row in proposed_rows
            if isinstance(row, dict)
        }
        changed_ids = {
            row_id
            for row_id in set(current_by_id) | set(proposed_by_id)
            if current_by_id.get(row_id) != proposed_by_id.get(row_id)
        }
        changed_rows = [
            row
            for row_id in changed_ids
            for row in (current_by_id.get(row_id), proposed_by_id.get(row_id))
            if isinstance(row, dict)
        ]
        if ledger == "capabilities":
            recruit_capabilities(changed_ids)
        for row in changed_rows:
            if not isinstance(row, dict):
                continue
            for owner_field in owner_fields:
                owner = row.get(owner_field)
                if isinstance(owner, str):
                    direct.add(owner)
            direct.update(
                value
                for value in row.get("involved_skill_ids", [])
                if isinstance(value, str)
            )
            if ledger == "exclusions_collisions_gaps":
                recruit_capabilities(row.get("involved_capability_ids", []))
                row_bound_stale.update(
                    value
                    for value in row.get("nondependency_proof_ids", [])
                    if isinstance(value, str)
                )
            elif ledger == "relationships":
                recruit_capabilities(row.get("affected_capability_ids", []))
                row_bound_stale.update(
                    value
                    for value in row.get("required_proof_ids", [])
                    if isinstance(value, str)
                )
    affected = _descendants(frozen, direct)
    ordered = [skill_id for skill_id in campaign_order(frozen) if skill_id in affected]
    stale = [
        proof_id
        for skill_id in ordered
        for proof_id in proof_registry.get(skill_id, [])
    ]
    stale.extend(
        proof_id for proof_id in sorted(row_bound_stale) if proof_id not in stale
    )
    return {
        "status": "behavior-decision-gap",
        "required_contract_revision": required_revision,
        "affected_skill_ids": ordered,
        "stale_proof_ids": stale,
    }


def validate_result(contract: dict[str, object]) -> dict[str, object]:
    """Validate a human-recorded integration result; never make the decision."""

    header = contract.get("epoch_header")
    result = header.get("integration_result") if isinstance(header, dict) else None
    if not isinstance(result, dict):
        return {"status": "result-invalid", "failures": ["missing result record"]}
    decision = result.get("decision")
    pointer = result.get("evidence_pointer")
    structural_failures = validate_contract(contract)
    if structural_failures:
        return {"status": "result-invalid", "failures": structural_failures}
    if decision is None and pointer is None:
        if (
            isinstance(header, dict)
            and header.get("status") in {"draft", "frozen"}
            and header.get("epoch_lock") is None
        ):
            return {"status": "result-pending"}
        return {
            "status": "result-invalid",
            "failures": ["pending result is incompatible with lifecycle state"],
        }
    if decision not in RESULT_DECISIONS:
        return {"status": "result-invalid", "failures": ["invalid result decision"]}
    if not isinstance(pointer, str) or not pointer.strip():
        return {"status": "result-invalid", "failures": ["missing evidence pointer"]}
    if decision == "integration-accepted":
        failures: list[str] = []
        if not isinstance(header, dict) or header.get("status") != (
            "integration-accepted"
        ):
            failures.append("accepted result requires integration-accepted status")
        if failures:
            return {"status": "result-invalid", "failures": failures}
    elif (
        not isinstance(header, dict)
        or header.get("status") != "frozen"
        or header.get("epoch_lock") is not None
    ):
        return {
            "status": "result-invalid",
            "failures": [
                "blocked or needs-more-evidence result requires an unlocked "
                "frozen contract"
            ],
        }
    return {"status": "result-valid", "decision": decision}


def validate_completion(contract: dict[str, object]) -> dict[str, object]:
    """Validate the Lock recorded after an accepted integration result."""

    result = validate_result(contract)
    if result.get("status") != "result-valid" or result.get("decision") != (
        "integration-accepted"
    ):
        return {
            "status": "completion-invalid",
            "failures": ["completion requires a valid accepted integration result"],
        }
    header = contract["epoch_header"]
    assert isinstance(header, dict)
    lock = header.get("epoch_lock")
    if lock is None:
        return {"status": "completion-pending"}
    if (
        not isinstance(lock, dict)
        or not isinstance(lock.get("lock_id"), str)
        or not lock["lock_id"].strip()
        or not isinstance(lock.get("evidence_pointer"), str)
        or not lock["evidence_pointer"].strip()
    ):
        return {
            "status": "completion-invalid",
            "failures": ["completion requires an evidence-bound epoch Lock"],
        }
    return {
        "status": "completion-valid",
        "lock_id": lock["lock_id"],
        "evidence_pointer": lock["evidence_pointer"],
    }


def validate_repository(root: Path) -> list[str]:
    """Validate the canonical owner state and its registered schema."""

    failures: list[str] = []
    owner = root / "docs/synthesis/skill-pack.md"
    schema_path = (
        root
        / "docs/validation/shared/schemas/"
        "pack-composition-contract-v1.schema.json"
    )
    registry_path = root / "docs/validation/shared/schemas/registry.json"
    method = root / "docs/synthesis/methods/fresh-composition-epoch.md"
    try:
        canonical = parse_contract(owner.read_text(encoding="utf-8"))
    except (OSError, PackContractError) as error:
        failures.append(f"Canonical Pack Contract cannot be read: {error}")
        return failures
    header = canonical.get("epoch_header")
    status = header.get("status") if isinstance(header, dict) else None
    if status == "draft" and canonical != create_draft():
        failures.append("Canonical draft must remain the exact inactive v1 draft")
    if status == "frozen" and header.get("contract_revision") == 1:
        freeze_input = deepcopy(canonical)
        freeze_input["epoch_header"]["status"] = "draft"  # type: ignore[index]
        refrozen = freeze_contract(freeze_input)
        if (
            refrozen.get("status") != "contract-frozen"
            or refrozen.get("contract") != canonical
        ):
            failures.append(
                "Canonical frozen Pack Contract cannot be reproduced from "
                "its revision draft"
            )
    failures.extend(
        f"Canonical Pack Contract: {failure}"
        for failure in validate_contract(canonical)
    )
    try:
        schema_bytes = schema_path.read_bytes()
        schema = json.loads(schema_bytes)
        Draft202012Validator.check_schema(schema)
        schema_errors = sorted(
            Draft202012Validator(schema).iter_errors(canonical),
            key=lambda error: list(error.absolute_path),
        )
        failures.extend(
            "Canonical Pack Contract schema failure at "
            f"{'/'.join(str(part) for part in error.absolute_path) or '$'}: "
            f"{error.message}"
            for error in schema_errors
        )
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError) as error:
        failures.append(f"Pack Contract schema or registry cannot be read: {error}")
        return failures
    expected_path = (
        "docs/validation/shared/schemas/"
        "pack-composition-contract-v1.schema.json"
    )
    expected_fingerprint = (
        f"{FINGERPRINT_PREFIX}{hashlib.sha256(schema_bytes).hexdigest()}"
    )
    entries = [
        row
        for row in registry.get("schemas", [])
        if isinstance(row, dict)
        and row.get("id") == "pack-composition-contract"
        and row.get("version") == 1
    ]
    if len(entries) != 1:
        failures.append("Registry requires exactly one Pack Contract v1 entry")
    elif entries[0].get("path") != expected_path:
        failures.append("Pack Contract registry path drift")
    elif entries[0].get("fingerprint") != expected_fingerprint:
        failures.append("Pack Contract schema fingerprint drift")
    fixture_path = (
        root
        / "docs/validation/shared/fixtures/"
        "pack-composition-contract-v1/contract.json"
    )
    try:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"Pack Contract positive fixture cannot be read: {error}")
    else:
        fixture_errors = sorted(
            Draft202012Validator(schema).iter_errors(fixture),
            key=lambda error: list(error.absolute_path),
        )
        failures.extend(
            f"Pack Contract fixture schema failure: {error.message}"
            for error in fixture_errors
        )
        frozen = freeze_contract(fixture)
        if frozen.get("status") != "contract-frozen":
            failures.extend(
                f"Pack Contract fixture: {failure}"
                for failure in frozen.get("failures", [])
            )
        else:
            frozen_contract = frozen["contract"]
            if campaign_order(frozen_contract) != ["SK-001"]:
                failures.append("Pack Contract fixture order drift")
            if contract_slice(frozen_contract, "SK-001").get("status") != (
                "contract-slice"
            ):
                failures.append("Pack Contract fixture slice failure")
    try:
        method_text = method.read_text(encoding="utf-8")
    except OSError as error:
        failures.append(f"Fresh Composition Epoch method cannot be read: {error}")
    else:
        for token in (
            "docs/synthesis/skill-pack.md",
            "docs/synthesis/methods/deploy-prompts.md",
            "behavior-decision-gap",
            "integration-accepted",
            "needs-more-evidence",
            "Recommend and stop",
        ):
            if token not in method_text:
                failures.append(f"Fresh Composition Epoch method misses {token}")
    return failures
