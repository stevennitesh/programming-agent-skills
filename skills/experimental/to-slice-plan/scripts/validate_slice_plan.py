#!/usr/bin/env python3
"""Validate strict Markdown slice plans for the slice execution skills."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "TEMPLATE.md"

TOP_LEVEL_SECTIONS = [
    "Goal",
    "Out of Scope",
    "Current State",
    "Evidence Table",
    "Gap Analysis",
    "Slice Count Rationale",
    "Slice Plan",
    "Recommended First Slice",
    "Execution Handoff",
    "Plan Self-Check",
]

REQUIRED_FIELDS = [
    "Status",
    "Work type",
    "Objective",
    "Dependencies/prerequisites",
    "Acceptance criteria",
    "Testing seam",
    "Validation",
    "Review gate",
    "Commit boundary",
    "Branch expectations",
    "Fog of war",
    "Handoff note",
    "Risks/review traps",
]
OPTIONAL_FIELDS = [
    "Feedback loop",
    "Design impact",
    "Data/live/network/approval impact",
    "Cleanup/deletion impact",
    "Docs/artifacts impact",
    "Notes/considerations",
]

EXECUTION_HANDOFF_FIELDS = [
    "Start command",
    "Runner safety",
    "Continuation mode",
    "Runner completion scope",
    "Slice/run limits",
    "Approvals",
    "Branch expectations",
    "Status update target",
    "Stop conditions",
    "Strict validation command",
    "Validation warnings",
    "Review gate",
    "Handoff note shape",
]

VALID_STATUSES = {"pending", "completed", "skipped", "blocked"}
VALID_WORK_TYPES = {
    "feature",
    "bug",
    "regression",
    "performance",
    "cleanup",
    "docs",
    "test",
    "research",
    "decision",
    "prototype",
    "grilling",
    "maintenance",
}
FEEDBACK_REQUIRED_WORK_TYPES = {"bug", "regression", "performance"}
FOG_WORK_TYPES = {"decision", "research", "prototype", "grilling"}
PERFORMANCE_INDICATORS = (
    "bug",
    "regression",
    "performance",
    "slow",
    "latency",
    "timeout",
    "flaky",
)
HIGH_RISK_INDICATORS = (
    "live-data",
    "live data",
    "network",
    "credential",
    "destructive",
    "remote-write",
    "remote write",
)
CLEANUP_INDICATORS = (
    "cleanup",
    "consolidat",
    "delete",
    "deletion",
    "deprecat",
    "prefactor",
)
DOCS_INDICATORS = ("docs", "documentation", "artifact", "report", "readme")
DESIGN_INDICATORS = (
    "module",
    "interface",
    "seam",
    "adapter",
    "adr",
    "domain",
    "glossary",
    "architecture",
    "schema",
    "contract",
)
INDICATOR_FIELDS = (
    "Work type",
    "Objective",
    "Dependencies/prerequisites",
    "Acceptance criteria",
    "Validation",
    "Risks/review traps",
    "Notes/considerations",
)
HIGH_RISK_HARD_FIELDS = (
    "Objective",
    "Dependencies/prerequisites",
    "Acceptance criteria",
)
HIGH_RISK_WARNING_FIELDS = (
    "Testing seam",
    "Validation",
    "Risks/review traps",
    "Notes/considerations",
)
SKILL_ROOTS = (
    Path("/home/steve/.codex/skills"),
    Path("/home/steve/.agents/skills"),
)
REVIEW_GATES = {
    "none",
    "local diff review",
    "$review",
    "$convergent-pr-review",
}
RUNNER_COMPLETION_SCOPES = (
    "disabled",
    "one-slice",
    "remaining-pending",
    "max N slices",
    "named slices: ...",
)
SYMBOLIC_TOKENS = ("RUN_ROOT", "PLAN_PATH", "OBSERVATION_PATH")
REVIEW_GATE_GUIDANCE = {
    "none": "tiny docs/test-only slice where focused validation is enough",
    "local diff review": "default local unstaged/staged diff inspection",
    "$review": "fixed-point standards/spec conformance; fixed point required",
    "$convergent-pr-review": "independent bug/risk convergence with verification",
    "repo command: <exact command>": "repo-owned review/check command run literally",
}
HANDOFF_FIELDS = ["Changed", "Remains", "Read next", "Next slice"]
KNOWN_FIELDS = set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)
EXPECTED_SELF_CHECKS = [
    (
        "contract-grounded",
        "The slice planning and runtime contracts were read and the plan is "
        "grounded in current files, docs, tests, commands, or artifacts.",
    ),
    (
        "evidence-backed",
        "Every major claim has an evidence pointer.",
    ),
    (
        "slice-fields",
        "Every slice includes every hard field and required conditional impact field.",
    ),
    (
        "strict-readiness",
        "Empty required fields use `None` or `N/A`, and strict validation passes "
        "for `.md` plans or the user approved a non-Markdown plan.",
    ),
    (
        "boundaries",
        "Slice count, tracer-bullet shape, fog of war, approvals, live/network "
        "or destructive work, and Out of Scope boundaries are explicit.",
    ),
    (
        "executable-handoff",
        "Validation, Review gate, commit boundary, branch expectations, and "
        "Handoff note are executable without inferring intent.",
    ),
    (
        "saved-plan",
        "The plan is saved in the repo and any active plan index is updated "
        "when appropriate.",
    ),
]
EXPECTED_SELF_CHECK_ITEMS = [text for _check_id, text in EXPECTED_SELF_CHECKS]

PLACEHOLDER_RE = re.compile(r"^<[^>]+>$")
LEFTOVER_PLACEHOLDER_RE = re.compile(r"<[A-Za-z][A-Za-z0-9 _./|-]*>")
SENTINEL_PUNCTUATION_VALUES = {"None.", "N/A."}
TEMPLATE_STALE_VALUES = (
    "- Dependencies/prerequisites: `None`",
    "- Feedback loop: `N/A`",
    "- Fog of war: `None`",
    "- Status update target: `plan slice status`",
)
SLICE_HEADING_RE = re.compile(r"^###\s+Slice\s+(\d+)\b.*", re.IGNORECASE)
FIELD_RE = re.compile(r"^- ([^:]+):\s*(.*)$")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
SELF_CHECK_ITEM_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s+(.+?)\s*$")
PREFIX_INDICATORS = {"credential", "consolidat", "deprecat", "prefactor"}


@dataclass(frozen=True)
class SectionBlock:
    name: str
    text: str
    heading_line: int
    content_start_line: int


@dataclass(frozen=True)
class SliceBlock:
    heading: str
    number: int
    line_number: int
    lines: list[str]


def line_number_at(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def normalize_value(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        value = value[1:-1].strip()
    return value


def value_is_blank(value: str) -> bool:
    value = normalize_value(value)
    return not value or PLACEHOLDER_RE.match(value) is not None


def sentinel_punctuation_error(value: str, context: str) -> str | None:
    normalized = normalize_value(value)
    if normalized in SENTINEL_PUNCTUATION_VALUES:
        sentinel = normalized[:-1]
        return f"{context}: use exact '{sentinel}' without punctuation"
    return None


def markdown_h2_names(text: str) -> list[str]:
    return [match.group(1).strip() for match in H2_RE.finditer(text)]


def duplicate_names(names: list[str]) -> list[str]:
    counts = Counter(names)
    return sorted(name for name, count in counts.items() if count > 1)


def parse_top_level_section_blocks(text: str) -> dict[str, SectionBlock]:
    matches = list(H2_RE.finditer(text))
    sections: dict[str, SectionBlock] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.setdefault(
            name,
            SectionBlock(
                name=name,
                text=text[start:end].strip(),
                heading_line=line_number_at(text, match.start()),
                content_start_line=line_number_at(text, match.end()),
            ),
        )
    return sections


def parse_top_level_sections(text: str) -> dict[str, str]:
    return {
        name: section.text for name, section in parse_top_level_section_blocks(text).items()
    }


def parse_slice_blocks(text: str, *, start_line: int = 1) -> list[SliceBlock]:
    slices: list[SliceBlock] = []
    current_heading: str | None = None
    current_number: int | None = None
    current_line: int | None = None
    current_lines: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=start_line):
        match = SLICE_HEADING_RE.match(line)
        if match:
            if current_heading is not None:
                assert current_number is not None and current_line is not None
                slices.append(
                    SliceBlock(
                        heading=current_heading,
                        number=current_number,
                        line_number=current_line,
                        lines=current_lines,
                    )
                )
            current_heading = line.strip()
            current_number = int(match.group(1))
            current_line = line_number
            current_lines = []
        elif current_heading is not None:
            if line.startswith("## ") and not line.startswith("### "):
                assert current_number is not None and current_line is not None
                slices.append(
                    SliceBlock(
                        heading=current_heading,
                        number=current_number,
                        line_number=current_line,
                        lines=current_lines,
                    )
                )
                current_heading = None
                current_number = None
                current_line = None
                current_lines = []
            else:
                current_lines.append(line)
    if current_heading is not None:
        assert current_number is not None and current_line is not None
        slices.append(
            SliceBlock(
                heading=current_heading,
                number=current_number,
                line_number=current_line,
                lines=current_lines,
            )
        )
    return slices


def parse_slices(text: str) -> list[tuple[str, list[str]]]:
    return [(block.heading, block.lines) for block in parse_slice_blocks(text)]


def parse_fields(
    lines: list[str], *, start_line: int = 1
) -> tuple[dict[str, list[str]], list[str], dict[str, int]]:
    fields: dict[str, list[str]] = {}
    seen: Counter[str] = Counter()
    field_lines: dict[str, int] = {}
    current: str | None = None
    for line_number, line in enumerate(lines, start=start_line):
        match = FIELD_RE.match(line)
        if match:
            current = match.group(1).strip()
            seen[current] += 1
            field_lines.setdefault(current, line_number)
            fields.setdefault(current, []).append(match.group(2).strip())
        elif current is not None:
            fields[current].append(line.rstrip())
    return fields, duplicate_names(list(seen.elements())), field_lines


def field_text(fields: dict[str, list[str]], field: str) -> str:
    return "\n".join(fields.get(field, [])).strip()


def field_has_value(fields: dict[str, list[str]], field: str) -> bool:
    text = field_text(fields, field)
    if not text:
        return False
    meaningful = []
    empty_handoff_re = re.compile(r"^- (Changed|Remains|Read next|Next slice):\s*$")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if field == "Handoff note" and empty_handoff_re.match(stripped):
            continue
        meaningful.append(stripped)
    return bool(meaningful) and not value_is_blank(" ".join(meaningful))


def validate_top_level(text: str, sections: dict[str, SectionBlock]) -> list[str]:
    errors: list[str] = []
    for section in duplicate_names(markdown_h2_names(text)):
        errors.append(f"duplicate top-level section '## {section}'")
    for section in TOP_LEVEL_SECTIONS:
        if section not in sections:
            errors.append(f"missing top-level section '## {section}'")
            continue
        block = sections[section]
        nonblank = " ".join(line.strip() for line in block.text.splitlines() if line.strip())
        if value_is_blank(nonblank):
            errors.append(
                f"top-level section '## {section}' is blank (line {block.heading_line})"
            )
    return errors


def review_gate_skill_found_in_local_roots(review_gate: str) -> bool:
    if not review_gate.startswith("$"):
        return True
    skill_name = review_gate[1:]
    return any((root / skill_name / "SKILL.md").exists() for root in SKILL_ROOTS)


def validate_review_gate(value: str, context: str) -> list[str]:
    errors: list[str] = []
    review_gate = normalize_value(value)
    if review_gate == "convergent-pr-review":
        errors.append(f"{context}: use '$convergent-pr-review', not 'convergent-pr-review'")
    elif review_gate.startswith("repo command:"):
        if not review_gate.removeprefix("repo command:").strip():
            errors.append(f"{context}: repo command Review gate needs an exact command")
    elif review_gate and review_gate not in REVIEW_GATES:
        gates = sorted(REVIEW_GATES)
        errors.append(
            f"{context}: Review gate must be one of {gates} "
            "or start with 'repo command:'; only $review and "
            "$convergent-pr-review are allowed skill gates"
        )
    elif not review_gate_skill_found_in_local_roots(review_gate):
        errors.append(
            f"{context}: Review gate skill '{review_gate}' was not found in local skill roots"
        )
    return errors


def validate_continuation_mode(value: str, context: str) -> list[str]:
    errors: list[str] = []
    mode = normalize_value(value).lower()
    if mode == "disabled":
        return errors
    if not mode.startswith("allowed"):
        errors.append(f"{context}: Continuation mode must be 'disabled' or start with 'allowed'")
        return errors
    required_terms = {
        "strict validation": "strict validation",
        "clean committed": "clean committed",
        "status": "status",
        "handoff": "handoff",
        "approval": "approval",
        "review": "review",
        "dirty": "dirty",
        "warning": "warning",
    }
    missing = [label for term, label in required_terms.items() if term not in mode]
    if missing:
        errors.append(
            f"{context}: allowed Continuation mode missing terms: {', '.join(missing)}"
        )
    return errors


def validate_runner_completion_scope(value: str, context: str) -> list[str]:
    errors: list[str] = []
    scope = normalize_value(value).lower()
    if scope in {"disabled", "one-slice", "remaining-pending"}:
        return errors
    if re.match(r"^max\s+\d+\s+slices$", scope):
        return errors
    if scope.startswith("named slices:") and scope.removeprefix("named slices:").strip():
        return errors
    errors.append(
        f"{context}: Runner completion scope must be disabled, one-slice, "
        "remaining-pending, max N slices, or named slices: ..."
    )
    return errors


def command_mentions_plan(command: str, path: Path | None) -> bool:
    if path is None:
        return True
    candidates = {path.name, str(path)}
    try:
        candidates.add(str(path.resolve()))
    except OSError:
        pass
    for candidate in candidates:
        pattern = rf"(?<![\w./-]){re.escape(candidate)}(?![\w./-])"
        if re.search(pattern, command):
            return True
    return False


def approval_is_empty(value: str) -> bool:
    normalized = normalize_value(value).lower()
    return normalized in {"none", "n/a"}


def validate_execution_handoff(
    sections: dict[str, SectionBlock],
    *,
    plan_path: Path | None = None,
    high_risk_requires_approval: bool = False,
) -> list[str]:
    errors: list[str] = []
    section = sections.get("Execution Handoff")
    lines = section.text.splitlines() if section is not None else []
    start_line = section.content_start_line if section is not None else 1
    fields, duplicates, field_lines = parse_fields(lines, start_line=start_line)
    for field in duplicates:
        line = field_lines.get(field, start_line)
        errors.append(f"Execution Handoff has duplicate field '{field}' (line {line})")
    for field in EXECUTION_HANDOFF_FIELDS:
        if field not in fields:
            errors.append(f"Execution Handoff missing field '{field}'")
        elif not field_has_value(fields, field):
            line = field_lines.get(field, start_line)
            errors.append(f"Execution Handoff field '{field}' is blank (line {line})")
        else:
            error = sentinel_punctuation_error(
                field_text(fields, field), f"Execution Handoff field '{field}'"
            )
            if error:
                line = field_lines.get(field, start_line)
                errors.append(f"{error} (line {line})")
    for field in sorted(set(fields) - set(EXECUTION_HANDOFF_FIELDS)):
        line = field_lines.get(field, start_line)
        errors.append(f"Execution Handoff has unexpected field '{field}' (line {line})")

    start_command = field_text(fields, "Start command")
    strict_validation_command = field_text(fields, "Strict validation command")
    if "$next-slice" not in start_command:
        errors.append("Execution Handoff Start command must include '$next-slice'")
    elif not command_mentions_plan(start_command, plan_path):
        errors.append("Execution Handoff Start command must name the current plan")
    if "$next-slice" in start_command and not re.search(
        r"\bSlice\s+\d+\b", start_command, re.IGNORECASE
    ):
        errors.append("Execution Handoff Start command must name a concrete Slice number")
    if "$slice-plan-runner" not in field_text(fields, "Runner safety"):
        errors.append("Execution Handoff Runner safety must mention '$slice-plan-runner'")
    errors.extend(
        validate_continuation_mode(
            field_text(fields, "Continuation mode"), "Execution Handoff"
        )
    )
    errors.extend(
        validate_runner_completion_scope(
            field_text(fields, "Runner completion scope"), "Execution Handoff"
        )
    )
    if "validate_slice_plan.py" not in strict_validation_command:
        errors.append(
            "Execution Handoff Strict validation command must name "
            "validate_slice_plan.py"
        )
    if "--allow-draft" in strict_validation_command:
        errors.append(
            "Execution Handoff Strict validation command must not use --allow-draft"
        )
    elif strict_validation_command and not command_mentions_plan(
        strict_validation_command, plan_path
    ):
        errors.append(
            "Execution Handoff Strict validation command must name the current plan"
        )
    raw_status_target = normalize_value(field_text(fields, "Status update target"))
    status_target = raw_status_target.lower()
    if status_target not in {"none", "n/a"}:
        status_target_re = re.compile(
            r"^plan slice status"
            r"(\s*;\s*tracker\s*:\s*(?!<)[`\w./-]+`?)?$",
            re.IGNORECASE,
        )
        if not status_target_re.match(raw_status_target):
            errors.append(
                "Execution Handoff Status update target must be None, "
                "plan slice status, or plan slice status; tracker: <id/path>"
            )
    errors.extend(validate_review_gate(field_text(fields, "Review gate"), "Execution Handoff"))
    if high_risk_requires_approval and approval_is_empty(field_text(fields, "Approvals")):
        errors.append(
            "Execution Handoff Approvals cannot be None/N/A when a slice objective, "
            "prerequisite, or acceptance criteria includes high-risk live/network, "
            "credentialed, destructive, or remote-write work"
        )
    return errors


def normalize_self_check_item(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def parse_self_check_items(text: str) -> tuple[dict[str, str], list[str]]:
    items: dict[str, str] = {}
    seen: Counter[str] = Counter()
    current_label: str | None = None
    current_state: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_label, current_state, current_parts
        if current_label is not None and current_state is not None:
            label = normalize_self_check_item(" ".join(current_parts))
            seen[label] += 1
            items[label] = current_state
        current_label = None
        current_state = None
        current_parts = []

    for line in text.splitlines():
        match = SELF_CHECK_ITEM_RE.match(line)
        if match:
            flush()
            current_state = match.group(1).lower()
            current_label = match.group(2).strip()
            current_parts = [current_label]
        elif current_label is not None:
            stripped = line.strip()
            if stripped and not stripped.startswith("```"):
                current_parts.append(stripped)
    flush()
    return items, duplicate_names(list(seen.elements()))


def validate_self_check(sections: dict[str, str], allow_draft: bool) -> list[str]:
    text = sections.get("Plan Self-Check", "")
    items, duplicates = parse_self_check_items(text)
    errors: list[str] = []
    for item in duplicates:
        errors.append(f"Plan Self-Check has duplicate item: {item}")
    if not items:
        errors.append("Plan Self-Check must include the expected checklist items")
        return errors

    for expected in EXPECTED_SELF_CHECK_ITEMS:
        if expected not in items:
            errors.append(f"Plan Self-Check missing item: {expected}")
        elif not allow_draft and items[expected] != "x":
            errors.append(f"Plan Self-Check has unchecked item: {expected}")
    return errors


def validate_slice_heading_locations(text: str) -> list[str]:
    errors: list[str] = []
    current_section: str | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        section_match = H2_RE.match(line)
        if section_match:
            current_section = section_match.group(1).strip()
            continue
        if SLICE_HEADING_RE.match(line) and current_section != "Slice Plan":
            errors.append(
                "slice headings are only allowed inside '## Slice Plan': "
                f"{line.strip()} (line {line_number})"
            )
    return errors


def validate_slice_sequence(slices: list[SliceBlock]) -> list[str]:
    errors: list[str] = []
    numbers = [block.number for block in slices]
    counts = Counter(numbers)
    for number in sorted(number for number, count in counts.items() if count > 1):
        lines = [str(block.line_number) for block in slices if block.number == number]
        errors.append(
            f"duplicate Slice {number} headings are not allowed (lines {', '.join(lines)})"
        )
    expected = list(range(1, len(slices) + 1))
    if numbers != expected:
        errors.append(
            "slice numbers must be sequential starting at 1; "
            f"found {numbers}, expected {expected}"
        )
    return errors


def validate_handoff(fields: dict[str, list[str]], heading: str) -> list[str]:
    errors: list[str] = []
    text = field_text(fields, "Handoff note")
    for subfield in HANDOFF_FIELDS:
        subfield_re = rf"^\s*- {re.escape(subfield)}:\s*(.*)$"
        match = re.search(subfield_re, text, re.MULTILINE)
        if not match:
            errors.append(f"{heading}: Handoff note missing subfield '{subfield}'")
        else:
            value = match.group(1)
            if value_is_blank(value):
                errors.append(f"{heading}: Handoff note subfield '{subfield}' is blank")
            else:
                error = sentinel_punctuation_error(
                    value, f"{heading}: Handoff note subfield '{subfield}'"
                )
                if error:
                    errors.append(error)
    return errors


def indicator_regex(indicator: str) -> re.Pattern[str]:
    suffix = "" if indicator in PREFIX_INDICATORS else r"\b"
    return re.compile(rf"\b{re.escape(indicator)}{suffix}", re.IGNORECASE)


def indicator_matches(
    fields: dict[str, list[str]],
    indicators: tuple[str, ...],
    field_names: tuple[str, ...],
) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = []
    for field in field_names:
        text = field_text(fields, field)
        for indicator in indicators:
            if indicator_regex(indicator).search(text):
                matches.append((field, indicator))
    return matches


def has_indicator_in_fields(
    fields: dict[str, list[str]],
    indicators: tuple[str, ...],
    field_names: tuple[str, ...],
) -> bool:
    return bool(indicator_matches(fields, indicators, field_names))


def has_indicator(fields: dict[str, list[str]], indicators: tuple[str, ...]) -> bool:
    return bool(indicator_matches(fields, indicators, INDICATOR_FIELDS))


def describe_indicator_match(matches: list[tuple[str, str]]) -> str:
    if not matches:
        return "matching text"
    field, indicator = matches[0]
    return f"{field} contains '{indicator}'"


def lexical_warning(context: str, match: str, implication: str) -> str:
    return (
        f"{context}: Lexical warning: {match}; this may imply {implication}. "
        "Inspect for drift; ignore if this is ordinary prose, fixture "
        "description, or validation coverage."
    )


def field_missing_or_blank(fields: dict[str, list[str]], field: str) -> bool:
    return field not in fields or not field_has_value(fields, field)


def validate_slice(
    heading: str,
    fields: dict[str, list[str]],
    duplicates: list[str],
    warnings: list[str],
    *,
    field_lines: dict[str, int] | None = None,
    slice_line: int | None = None,
) -> list[str]:
    errors: list[str] = []
    field_lines = field_lines or {}
    context = f"{heading} (line {slice_line})" if slice_line is not None else heading
    for field in duplicates:
        line = field_lines.get(field, slice_line)
        errors.append(f"{context}: duplicate field '{field}' (line {line})")
    for field in REQUIRED_FIELDS:
        if field not in fields:
            errors.append(f"{context}: missing hard field '{field}'")
        elif not field_has_value(fields, field):
            line = field_lines.get(field, slice_line)
            errors.append(f"{context}: hard field '{field}' is blank (line {line})")
        else:
            error = sentinel_punctuation_error(
                field_text(fields, field), f"{context}: field '{field}'"
            )
            if error:
                line = field_lines.get(field, slice_line)
                errors.append(f"{error} (line {line})")

    for field in OPTIONAL_FIELDS:
        if field in fields and not field_has_value(fields, field):
            line = field_lines.get(field, slice_line)
            errors.append(f"{context}: optional field '{field}' is blank (line {line})")
        elif field in fields:
            error = sentinel_punctuation_error(
                field_text(fields, field), f"{context}: field '{field}'"
            )
            if error:
                line = field_lines.get(field, slice_line)
                errors.append(f"{error} (line {line})")

    for field in sorted(set(fields) - KNOWN_FIELDS):
        line = field_lines.get(field, slice_line)
        warnings.append(f"{context}: unknown slice field '{field}' (line {line})")

    status = normalize_value(field_text(fields, "Status"))
    if status and status not in VALID_STATUSES:
        errors.append(f"{context}: invalid Status '{status}'")

    work_type = normalize_value(field_text(fields, "Work type")).lower()
    if work_type and work_type not in VALID_WORK_TYPES:
        errors.append(f"{context}: invalid Work type '{work_type}'")

    errors.extend(validate_review_gate(field_text(fields, "Review gate"), context))

    fog = normalize_value(field_text(fields, "Fog of war"))
    if fog and fog.lower() != "none" and work_type not in FOG_WORK_TYPES:
        errors.append(
            f"{context}: non-None Fog of war requires decision, research, "
            "prototype, or grilling Work type"
        )

    feedback = normalize_value(field_text(fields, "Feedback loop"))
    if work_type in FEEDBACK_REQUIRED_WORK_TYPES:
        if field_missing_or_blank(fields, "Feedback loop") or feedback == "N/A":
            errors.append(f"{context}: {work_type} slice needs non-N/A Feedback loop")
    elif work_type:
        performance_matches = indicator_matches(fields, PERFORMANCE_INDICATORS, INDICATOR_FIELDS)
        if performance_matches:
            match = describe_indicator_match(performance_matches)
            warnings.append(
                lexical_warning(
                    context,
                    match,
                    f"bug/regression/performance work or a Feedback loop for Work type '{work_type}'",
                )
            )

    hard_high_risk_matches = indicator_matches(
        fields, HIGH_RISK_INDICATORS, HIGH_RISK_HARD_FIELDS
    )
    warning_high_risk_matches = indicator_matches(
        fields, HIGH_RISK_INDICATORS, HIGH_RISK_WARNING_FIELDS
    )
    missing_high_risk_impact = field_missing_or_blank(
        fields, "Data/live/network/approval impact"
    )
    if hard_high_risk_matches and missing_high_risk_impact:
        match = describe_indicator_match(hard_high_risk_matches)
        errors.append(
            f"{context}: high-risk live/network work needs "
            f"Data/live/network/approval impact ({match})"
        )
    elif warning_high_risk_matches and missing_high_risk_impact:
        match = describe_indicator_match(warning_high_risk_matches)
        warnings.append(
            lexical_warning(
                context,
                match,
                "Data/live/network/approval impact",
            )
        )

    cleanup_matches = indicator_matches(fields, CLEANUP_INDICATORS, INDICATOR_FIELDS)
    cleanup_needed = work_type == "cleanup" or cleanup_matches
    if cleanup_needed and field_missing_or_blank(fields, "Cleanup/deletion impact"):
        match = describe_indicator_match(cleanup_matches)
        suffix = f" ({match})" if cleanup_matches else ""
        errors.append(
            f"{context}: cleanup/deletion work needs Cleanup/deletion impact{suffix}"
        )
    if work_type == "docs" and field_missing_or_blank(fields, "Docs/artifacts impact"):
        errors.append(f"{context}: docs slice needs Docs/artifacts impact")
    else:
        docs_matches = indicator_matches(fields, DOCS_INDICATORS, INDICATOR_FIELDS)
    if work_type != "docs" and docs_matches and field_missing_or_blank(
        fields, "Docs/artifacts impact"
    ):
        match = describe_indicator_match(docs_matches)
        warnings.append(lexical_warning(context, match, "Docs/artifacts impact"))
    design_matches = indicator_matches(fields, DESIGN_INDICATORS, INDICATOR_FIELDS)
    if design_matches and field_missing_or_blank(
        fields, "Design impact"
    ):
        match = describe_indicator_match(design_matches)
        warnings.append(lexical_warning(context, match, "Design impact"))

    errors.extend(validate_handoff(fields, context))
    return errors


def validate_plan(path: Path, *, allow_draft: bool = False) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    for match in LEFTOVER_PLACEHOLDER_RE.finditer(text):
        errors.append(
            "leftover placeholder text is not allowed: "
            f"{match.group(0)} (line {line_number_at(text, match.start())})"
        )

    section_blocks = parse_top_level_section_blocks(text)
    section_texts = {name: block.text for name, block in section_blocks.items()}
    errors.extend(validate_top_level(text, section_blocks))
    errors.extend(validate_slice_heading_locations(text))
    errors.extend(validate_self_check(section_texts, allow_draft))

    slice_plan = section_blocks.get("Slice Plan")
    slice_text = slice_plan.text if slice_plan is not None else ""
    slice_start_line = slice_plan.content_start_line if slice_plan is not None else 1
    slices = parse_slice_blocks(slice_text, start_line=slice_start_line)
    if not slices:
        errors.append("no slice headings found; expected headings like '### Slice 1 - Name'")
        return errors, warnings
    errors.extend(validate_slice_sequence(slices))
    high_risk_requires_approval = False
    parsed_slices: list[tuple[SliceBlock, dict[str, list[str]], list[str], dict[str, int]]] = []
    for block in slices:
        fields, duplicates, field_lines = parse_fields(
            block.lines, start_line=block.line_number + 1
        )
        high_risk_requires_approval = high_risk_requires_approval or has_indicator_in_fields(
            fields, HIGH_RISK_INDICATORS, HIGH_RISK_HARD_FIELDS
        )
        parsed_slices.append((block, fields, duplicates, field_lines))

    errors.extend(
        validate_execution_handoff(
            section_blocks,
            plan_path=path,
            high_risk_requires_approval=high_risk_requires_approval,
        )
    )
    for block, fields, duplicates, field_lines in parsed_slices:
        errors.extend(
            validate_slice(
                block.heading,
                fields,
                duplicates,
                warnings,
                field_lines=field_lines,
                slice_line=block.line_number,
            )
        )
    return errors, warnings


def validate_template(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    sections = parse_top_level_sections(text)
    errors: list[str] = []
    for stale_value in TEMPLATE_STALE_VALUES:
        if stale_value in text:
            errors.append(
                "template has stale default-biased value; use a replacement "
                f"placeholder instead: {stale_value}"
            )
    for section in duplicate_names(markdown_h2_names(text)):
        errors.append(f"template has duplicate top-level section '## {section}'")
    for section in TOP_LEVEL_SECTIONS:
        if section not in sections:
            errors.append(f"template missing top-level section '## {section}'")

    items, duplicates = parse_self_check_items(sections.get("Plan Self-Check", ""))
    for item in duplicates:
        errors.append(f"template Plan Self-Check has duplicate item: {item}")
    if not items:
        errors.append("template Plan Self-Check must include the expected checklist items")
    else:
        expected = set(EXPECTED_SELF_CHECK_ITEMS)
        found = set(items)
        for item in EXPECTED_SELF_CHECK_ITEMS:
            if item not in found:
                errors.append(f"template Plan Self-Check missing item: {item}")
        for item in sorted(found - expected):
            errors.append(f"template Plan Self-Check has unexpected item: {item}")

    slices = parse_slices(sections.get("Slice Plan", ""))
    if not slices:
        errors.append("template Slice Plan must include a sample slice")
    else:
        heading, lines = slices[0]
        fields, duplicates, _field_lines = parse_fields(lines)
        for field in duplicates:
            errors.append(f"template {heading}: duplicate field '{field}'")
        expected = set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)
        found = set(fields)
        for field in REQUIRED_FIELDS:
            if field not in found:
                errors.append(f"template {heading}: missing hard field '{field}'")
        for field in sorted(found - expected):
            errors.append(f"template {heading}: unexpected field '{field}'")

    handoff_lines = sections.get("Execution Handoff", "").splitlines()
    handoff_fields, duplicates, _field_lines = parse_fields(handoff_lines)
    for field in duplicates:
        errors.append(f"template Execution Handoff has duplicate field '{field}'")
    expected_handoff = set(EXECUTION_HANDOFF_FIELDS)
    found_handoff = set(handoff_fields)
    for field in EXECUTION_HANDOFF_FIELDS:
        if field not in found_handoff:
            errors.append(f"template Execution Handoff missing field '{field}'")
    for field in sorted(found_handoff - expected_handoff):
        errors.append(f"template Execution Handoff has unexpected field '{field}'")
    return errors


def print_schema() -> None:
    print("Slice plan schema")
    print()
    print("Top-level sections:")
    for section in TOP_LEVEL_SECTIONS:
        print(f"- {section}")
    print()
    print("Required slice fields:")
    for field in REQUIRED_FIELDS:
        print(f"- {field}")
    print()
    print("Conditional slice fields:")
    print("- Feedback loop: required for bug, regression, performance")
    print("- Design impact: recommended for domain/schema/module/interface/contract changes")
    print(
        "- Data/live/network/approval impact: required for high-risk "
        "live/network/credentialed/destructive/remote-write work"
    )
    print(
        "- Cleanup/deletion impact: required for "
        "cleanup/deletion/deprecation/consolidation/prefactoring"
    )
    print("- Docs/artifacts impact: required for docs slices; recommended for artifact/report changes")
    print("- Notes/considerations: optional execution-relevant context")
    print()
    print("Valid Status values:")
    for status in sorted(VALID_STATUSES):
        print(f"- {status}")
    print()
    print("Valid Work type values:")
    for work_type in sorted(VALID_WORK_TYPES):
        print(f"- {work_type}")
    print()
    print("Review gate values:")
    for gate, meaning in REVIEW_GATE_GUIDANCE.items():
        print(f"- {gate}: {meaning}")
    print()
    print("Runner completion scope values:")
    for scope in RUNNER_COMPLETION_SCOPES:
        print(f"- {scope}")
    print()
    print("Execution Handoff fields:")
    for field in EXECUTION_HANDOFF_FIELDS:
        print(f"- {field}")
    print()
    print("Accepted symbolic-token convention:")
    for token in SYMBOLIC_TOKENS:
        print(f"- {token}")
    print()
    print("Plan Self-Check items:")
    for item in EXPECTED_SELF_CHECK_ITEMS:
        print(f"- [x] {item}")


def main() -> int:
    epilog = (
        "Maintenance: after changing the contract, template, or validator, run "
        "quick_validate.py for the three skills, --check-template, and "
        "test_validate_slice_plan.py."
    )
    parser = argparse.ArgumentParser(description=__doc__, epilog=epilog)
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Allow unchecked Plan Self-Check items while drafting.",
    )
    parser.add_argument(
        "--check-template",
        nargs="?",
        const=str(DEFAULT_TEMPLATE_PATH),
        type=Path,
        help="Check TEMPLATE.md against the validator schema.",
    )
    parser.add_argument(
        "--print-schema",
        action="store_true",
        help="Print the active validator schema and valid forms.",
    )
    parser.add_argument("plan", nargs="?", type=Path, help="Markdown slice plan to validate")
    args = parser.parse_args()

    if args.print_schema:
        print_schema()
        return 0

    if args.check_template is not None:
        if not args.check_template.exists():
            print(f"ERROR: template not found: {args.check_template}", file=sys.stderr)
            return 2
        errors = validate_template(args.check_template)
        if errors:
            print("Slice plan template validation failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Slice plan template is valid.")
        return 0

    if args.plan is None:
        parser.error("plan is required unless --check-template is used")
    if args.plan.suffix.lower() != ".md":
        print(f"ERROR: validator only accepts .md plans: {args.plan}", file=sys.stderr)
        return 2
    if not args.plan.exists():
        print(f"ERROR: plan not found: {args.plan}", file=sys.stderr)
        return 2

    errors, warnings = validate_plan(args.plan, allow_draft=args.allow_draft)
    if errors:
        print("Slice plan validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if warnings:
        print("Slice plan validation warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"- {warning}", file=sys.stderr)

    print("Slice plan is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
