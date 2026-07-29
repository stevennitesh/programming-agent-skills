"""Inspect, validate, or atomically update one audit-codebase HTML report."""

from __future__ import annotations

import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Sequence


_RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_SECTION_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_GIT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_KINDS = {
    "system",
    "subsystem-narrative",
    "finding",
    "candidate",
    "candidate-index",
    "summary",
}
_MARKER_PREFIX = "<!-- audit-codebase:"
_UNSAFE_HREF = re.compile(r"(?i)^(?://|[a-z][a-z0-9+.-]*:)")
_UNSAFE_TAGS = {"base", "embed", "form", "iframe", "link", "object", "script", "style"}
_RESOURCE_ATTRS = {"action", "data", "formaction", "poster", "src", "srcset"}
_CANDIDATE_STATES = (
    "presented",
    "decision pending",
    "analyzed",
    "implemented",
    "disproved",
    "blocked",
)
_STRENGTHS = {"Strong", "Worth exploring", "Speculative"}
_SUBSYSTEM_STATES = {"mapped", "incomplete", "audited"}
_FINDING_STATES = ("active", "resolved", "disproved")
_PROGRESS_IDS = {"report-header", "summary-progress", "report-footer"}
_INSERT_KINDS = ("finding-insert", "candidate-index-insert", "candidate-insert")


class ReportUpdateError(ValueError):
    """The requested report update failed before publication."""

    def __init__(
        self,
        message: str,
        *,
        stage: str = "validate",
        mutation_started: bool = False,
        report_unchanged: bool = True,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.mutation_started = mutation_started
        self.report_unchanged = report_unchanged

    def as_dict(self) -> dict[str, object]:
        return {
            "error": str(self),
            "stage": self.stage,
            "mutation_started": self.mutation_started,
            "report_unchanged": self.report_unchanged,
        }


class _MarkupFacts(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: dict[str, int] = {}
        self.fragment_links: list[str] = []
        self.html_count = 0
        self.main_count = 0
        self.unsafe: list[str] = []
        self.report_versions: list[str] = []
        self.candidate_cards: dict[str, list[dict[str, str]]] = {}
        self.candidate_rows: dict[str, list[dict[str, str]]] = {}
        self.candidate_findings: dict[str, list[str]] = {}
        self.subsystems: dict[str, list[dict[str, str]]] = {}
        self.findings: dict[str, list[dict[str, str]]] = {}
        self.retained: dict[str, list[dict[str, str]]] = {}
        self.gaps: dict[str, list[dict[str, str]]] = {}
        self.implementation_results: dict[str, list[dict[str, str]]] = {}
        self.progress: dict[str, list[str]] = {}
        self.finding_progress: dict[str, list[str]] = {}
        self.insertions: dict[tuple[str, str], int] = {}
        self.pickups: dict[str, dict[str, list[str]]] = {}
        self._pickup: tuple[str, str, str, list[str]] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        lowered = tag.lower()
        if lowered == "html":
            self.html_count += 1
        elif lowered == "main":
            self.main_count += 1
        elif lowered in _UNSAFE_TAGS:
            self.unsafe.append(f"{lowered} element")

        values = {
            name.lower(): value
            for name, value in attrs
            if value is not None
        }
        element_id = values.get("id", "")
        if (
            lowered == "meta"
            and values.get("name") == "audit-codebase-report-version"
        ):
            self.report_versions.append(values.get("content", ""))
        if lowered == "article" and element_id.startswith("candidate-"):
            candidate_id = element_id.removeprefix("candidate-")
            self.candidate_cards.setdefault(candidate_id, []).append(values)
        if lowered == "article" and element_id.startswith("finding-"):
            finding_id = element_id.removeprefix("finding-")
            self.findings.setdefault(finding_id, []).append(values)
        if lowered == "section" and element_id.startswith("subsystem-"):
            subsystem_id = element_id.removeprefix("subsystem-")
            self.subsystems.setdefault(subsystem_id, []).append(values)
        if lowered == "tr" and element_id.startswith("candidate-index-"):
            candidate_id = element_id.removeprefix("candidate-index-")
            self.candidate_rows.setdefault(candidate_id, []).append(values)
        if values.get("data-implementation-result") is not None:
            candidate_id = values.get("data-candidate-id", "")
            self.implementation_results.setdefault(candidate_id, []).append(values)
        if "data-candidate-progress" in values:
            self.progress.setdefault(element_id, []).append(
                values["data-candidate-progress"]
            )
        if "data-finding-progress" in values:
            self.finding_progress.setdefault(element_id, []).append(
                values["data-finding-progress"]
            )
        if "data-retained-id" in values:
            self.retained.setdefault(values["data-retained-id"], []).append(values)
        if "data-gap-id" in values:
            self.gaps.setdefault(values["data-gap-id"], []).append(values)
        if "data-candidate-finding" in values:
            candidate_id = values["data-candidate-finding"]
            href = values.get("href", "")
            if href.startswith("#finding-"):
                self.candidate_findings.setdefault(candidate_id, []).append(
                    href.removeprefix("#finding-")
                )
        if "data-candidate-pickup" in values:
            if self._pickup is not None:
                raise ReportUpdateError("candidate pickup elements may not nest")
            self._pickup = (
                lowered,
                values["data-candidate-pickup"],
                values.get("data-pickup-view", ""),
                [],
            )

        for name, value in attrs:
            if value is None:
                continue
            attr = name.lower()
            if attr == "id":
                self.ids[value] = self.ids.get(value, 0) + 1
            if attr == "href" and value.startswith("#"):
                self.fragment_links.append(value[1:])
            if (
                attr in _RESOURCE_ATTRS
                or attr == "style"
                or attr.startswith("on")
                or attr in {"href", "xlink:href"} and _UNSAFE_HREF.match(value)
            ):
                self.unsafe.append(f"unsafe resource or behavior attribute {name}")

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)

    def handle_comment(self, data: str) -> None:
        match = re.fullmatch(
            r"\s*audit-codebase:"
            r"(finding-insert|candidate-index-insert|candidate-insert):"
            r"([a-z0-9]+(?:-[a-z0-9]+)*)\s*",
            data,
        )
        if match:
            key = (match.group(1), match.group(2))
            self.insertions[key] = self.insertions.get(key, 0) + 1

    def handle_data(self, data: str) -> None:
        if self._pickup is not None:
            self._pickup[3].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._pickup is None or tag.lower() != self._pickup[0]:
            return
        _, candidate_id, view, parts = self._pickup
        value = " ".join("".join(parts).split())
        self.pickups.setdefault(candidate_id, {}).setdefault(view, []).append(value)
        self._pickup = None


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _decode(path: Path) -> tuple[bytes, str]:
    data = path.read_bytes()
    try:
        return data, data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ReportUpdateError(f"{path} is not strict UTF-8") from exc


def _canonical_report(repo_root: Path, report: Path) -> Path:
    try:
        root = repo_root.resolve(strict=True)
        resolved = report.resolve(strict=True)
    except OSError as exc:
        raise ReportUpdateError(f"cannot resolve report boundary: {exc}") from exc

    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ReportUpdateError("report resolves outside repository root") from exc

    parts = relative.parts
    if (
        len(parts) != 4
        or parts[0] != ".scratch"
        or parts[1] != "audit-codebase"
        or not _RUN_ID.fullmatch(parts[2])
        or parts[3] != "report.html"
    ):
        raise ReportUpdateError("report is not at the canonical audit-codebase path")

    lexical = Path(os.path.abspath(report))
    expected = Path(os.path.abspath(root / relative))
    if lexical != expected:
        raise ReportUpdateError("report path is redirected or non-canonical")
    return resolved


def _facts(markup: str) -> _MarkupFacts:
    parser = _MarkupFacts()
    try:
        parser.feed(markup)
        parser.close()
        if parser._pickup is not None:
            raise ReportUpdateError("candidate pickup element is not closed")
    except Exception as exc:  # HTMLParser may surface malformed entity state.
        raise ReportUpdateError(f"HTML parse failed: {exc}") from exc
    return parser


def _marker(kind: str, identifier: str, edge: str) -> str:
    return f"<!-- audit-codebase:{kind}:{identifier}:{edge} -->"


def _anchor(kind: str, identifier: str) -> str:
    if kind == "summary" and identifier in {"report-header", "report-footer"}:
        return identifier
    return f"{kind}-{identifier}"


def _required(record: dict[str, str], name: str, label: str) -> str:
    if name not in record:
        raise ReportUpdateError(f"{label} is missing {name}")
    return record[name]


def _validate_candidate_record(
    *, identifier: str, record: dict[str, str], label: str
) -> tuple[str, str, str]:
    if _required(record, "data-candidate-id", label) != identifier:
        raise ReportUpdateError(f"{label} candidate ID does not match its anchor")
    state = _required(record, "data-state", label)
    strength = _required(record, "data-strength", label)
    subsystem_id = _required(record, "data-subsystem-id", label)
    if state not in _CANDIDATE_STATES:
        raise ReportUpdateError(f"{label} has unsupported candidate state {state!r}")
    if strength not in _STRENGTHS:
        raise ReportUpdateError(f"{label} has unsupported strength {strength!r}")
    if not _SECTION_ID.fullmatch(subsystem_id):
        raise ReportUpdateError(f"{label} has unsafe subsystem ID")
    return state, strength, subsystem_id


def _validate_complete_report(
    facts: _MarkupFacts,
) -> tuple[dict[str, str], str, dict[str, str], str]:
    if facts.html_count != 1 or facts.main_count != 1:
        raise ReportUpdateError("report must contain one html and one main element")
    if facts.report_versions != ["4"]:
        raise ReportUpdateError("report must declare audit-codebase version 4")
    duplicate_ids = sorted(
        identifier for identifier, count in facts.ids.items() if count != 1
    )
    if duplicate_ids:
        raise ReportUpdateError(
            f"report contains duplicate IDs: {', '.join(duplicate_ids)}"
        )

    subsystem_ids = set(facts.subsystems)
    for identifier in sorted(subsystem_ids):
        records = facts.subsystems[identifier]
        if len(records) != 1:
            raise ReportUpdateError(
                f"subsystem {identifier!r} must have one static container"
            )
        record = records[0]
        if _required(record, "data-subsystem-id", f"subsystem {identifier!r}") != identifier:
            raise ReportUpdateError(
                f"subsystem {identifier!r} ID does not match its anchor"
            )
        _required(record, "data-state", f"subsystem {identifier!r}")
        _required(record, "data-source-identity", f"subsystem {identifier!r}")
        for kind in _INSERT_KINDS:
            if facts.insertions.get((kind, identifier), 0) != 1:
                raise ReportUpdateError(
                    f"subsystem {identifier!r} requires one {kind} anchor"
                )

    finding_states: dict[str, str] = {}
    finding_counts = {state: 0 for state in _FINDING_STATES}
    for identifier in sorted(facts.findings):
        records = facts.findings[identifier]
        if len(records) != 1 or not _SECTION_ID.fullmatch(identifier):
            raise ReportUpdateError(
                f"finding {identifier!r} must have one safe record"
            )
        record = records[0]
        label = f"finding {identifier!r}"
        if _required(record, "data-finding-id", label) != identifier:
            raise ReportUpdateError(f"{label} ID does not match its anchor")
        subsystem_id = _required(record, "data-subsystem-id", label)
        if subsystem_id not in subsystem_ids:
            raise ReportUpdateError(f"{label} has no matching subsystem")
        state = _required(record, "data-state", label)
        if state not in _FINDING_STATES:
            raise ReportUpdateError(f"{label} has unsupported state {state!r}")
        finding_states[identifier] = state
        finding_counts[state] += 1

    card_ids = set(facts.candidate_cards)
    row_ids = set(facts.candidate_rows)
    if card_ids != row_ids:
        raise ReportUpdateError("candidate cards and index rows do not match")
    if set(facts.implementation_results) - card_ids:
        raise ReportUpdateError("implementation evidence has no matching candidate card")
    if set(facts.pickups) - card_ids:
        raise ReportUpdateError("candidate pickup has no matching candidate card")

    states: dict[str, str] = {}
    counts = {state: 0 for state in _CANDIDATE_STATES}
    for identifier in sorted(card_ids):
        if not _SECTION_ID.fullmatch(identifier):
            raise ReportUpdateError(f"unsafe candidate ID: {identifier}")
        cards = facts.candidate_cards[identifier]
        rows = facts.candidate_rows[identifier]
        if len(cards) != 1 or len(rows) != 1:
            raise ReportUpdateError(
                f"candidate {identifier!r} must have one card and one index row"
            )
        card_values = _validate_candidate_record(
            identifier=identifier,
            record=cards[0],
            label=f"candidate card {identifier!r}",
        )
        row_values = _validate_candidate_record(
            identifier=identifier,
            record=rows[0],
            label=f"candidate index row {identifier!r}",
        )
        if card_values != row_values:
            raise ReportUpdateError(
                f"candidate {identifier!r} card and index projection disagree"
            )

        state = card_values[0]
        subsystem_id = card_values[2]
        if subsystem_id not in subsystem_ids:
            raise ReportUpdateError(
                f"candidate {identifier!r} has no matching subsystem"
            )
        states[identifier] = state
        counts[state] += 1
        member_findings = facts.candidate_findings.get(identifier, [])
        if len(member_findings) != len(set(member_findings)):
            raise ReportUpdateError(
                f"candidate {identifier!r} repeats a finding member"
            )
        for finding_id in member_findings:
            if finding_id not in finding_states:
                raise ReportUpdateError(
                    f"candidate {identifier!r} references unknown finding {finding_id!r}"
                )
            finding_record = facts.findings[finding_id][0]
            if finding_record["data-subsystem-id"] != subsystem_id:
                raise ReportUpdateError(
                    f"candidate {identifier!r} references a foreign finding"
                )
        pickups = facts.pickups.get(identifier, {})
        if set(pickups) - {"card", "index"}:
            raise ReportUpdateError(
                f"candidate {identifier!r} has unsupported pickup view"
            )
        card_pickups = pickups.get("card", [])
        row_pickups = pickups.get("index", [])
        if state in {"presented", "decision pending", "blocked"}:
            if (
                len(card_pickups) != 1
                or len(row_pickups) != 1
                or not card_pickups[0]
                or card_pickups != row_pickups
            ):
                raise ReportUpdateError(
                    f"candidate {identifier!r} requires one matching pickup"
                )
        elif state == "analyzed":
            if card_pickups != row_pickups or len(card_pickups) > 1:
                raise ReportUpdateError(
                    f"candidate {identifier!r} optional pickup projections disagree"
                )
        elif card_pickups or row_pickups:
            raise ReportUpdateError(
                f"candidate {identifier!r} {state} state forbids pickup"
            )
        results = facts.implementation_results.get(identifier, [])
        if state != "implemented":
            if results:
                raise ReportUpdateError(
                    f"candidate {identifier!r} has implementation evidence before implemented"
                )
            continue
        if len(results) != 1:
            raise ReportUpdateError(
                f"implemented candidate {identifier!r} needs one evidence element"
            )
        result = results[0]
        expected = {
            "data-implementation-result": "complete",
            "data-candidate-id": identifier,
            "data-source-status": {"current", "reachable"},
            "data-proof-status": "accepted",
            "data-review-status": "accepted",
            "data-closure-status": "complete",
            "data-blockers": "none",
        }
        for name, value in expected.items():
            observed = _required(result, name, f"implementation result {identifier!r}")
            if isinstance(value, set):
                if observed not in value:
                    raise ReportUpdateError(
                        f"implementation result {identifier!r} has invalid {name}"
                    )
            elif observed != value:
                raise ReportUpdateError(
                    f"implementation result {identifier!r} has invalid {name}"
                )
        for name in ("data-commit-sha", "data-tree-sha"):
            if not _GIT_ID.fullmatch(
                _required(result, name, f"implementation result {identifier!r}")
            ):
                raise ReportUpdateError(
                    f"implementation result {identifier!r} has invalid {name}"
                )
        if not _required(
            result,
            "data-repair-generations",
            f"implementation result {identifier!r}",
        ).isdigit():
            raise ReportUpdateError(
                f"implementation result {identifier!r} has invalid Repair count"
            )

    progress = ",".join(
        f"{state.replace(' ', '-')}:{counts[state]}"
        for state in _CANDIDATE_STATES
    )
    if not _PROGRESS_IDS <= set(facts.progress):
        raise ReportUpdateError("report is missing candidate progress projections")
    for identifier, values in facts.progress.items():
        if len(values) != 1 or values[0] != progress:
            raise ReportUpdateError(
                f"candidate progress projection {identifier!r} is inconsistent"
            )
    finding_progress = ",".join(
        f"{state}:{finding_counts[state]}" for state in _FINDING_STATES
    )
    if not _PROGRESS_IDS <= set(facts.finding_progress):
        raise ReportUpdateError("report is missing finding progress projections")
    for identifier, values in facts.finding_progress.items():
        if len(values) != 1 or values[0] != finding_progress:
            raise ReportUpdateError(
                f"finding progress projection {identifier!r} is inconsistent"
            )
    return states, progress, finding_states, finding_progress


def _validate_report(
    source: str,
) -> tuple[dict[str, str], str, dict[str, str], str]:
    facts = _facts(source)
    result = _validate_complete_report(facts)
    regions: list[tuple[int, int, str]] = []
    for identifier in facts.subsystems:
        regions.append(
            (*_marked_bounds(source, "subsystem-narrative", identifier), "narrative")
        )
    for kind, identifiers in (
        ("finding", facts.findings),
        ("candidate", facts.candidate_cards),
        ("candidate-index", facts.candidate_rows),
    ):
        for identifier in identifiers:
            regions.append((*_marked_bounds(source, kind, identifier), f"{kind}:{identifier}"))
    ordered = sorted(regions)
    for left, right in zip(ordered, ordered[1:]):
        if left[1] > right[0]:
            raise ReportUpdateError(
                f"report has overlapping regions: {left[2]} and {right[2]}"
            )
    return result


def _sync_progress(source: str) -> str:
    facts = _facts(source)
    candidate_counts = {state: 0 for state in _CANDIDATE_STATES}
    for records in facts.candidate_cards.values():
        if len(records) == 1 and records[0].get("data-state") in candidate_counts:
            candidate_counts[records[0]["data-state"]] += 1
    finding_counts = {state: 0 for state in _FINDING_STATES}
    for records in facts.findings.values():
        if len(records) == 1 and records[0].get("data-state") in finding_counts:
            finding_counts[records[0]["data-state"]] += 1
    candidate_progress = ",".join(
        f"{state.replace(' ', '-')}:{candidate_counts[state]}"
        for state in _CANDIDATE_STATES
    )
    finding_progress = ",".join(
        f"{state}:{finding_counts[state]}" for state in _FINDING_STATES
    )

    def replace(name: str, value: str, markup: str) -> str:
        pattern = rf"({name}\s*=\s*)([\"'])[^\"']*\2"
        updated, count = re.subn(
            pattern,
            lambda match: (
                f"{match.group(1)}{match.group(2)}{value}{match.group(2)}"
            ),
            markup,
        )
        if count != len(_PROGRESS_IDS):
            raise ReportUpdateError(f"{name} projections are not derivable")
        return updated

    source = replace("data-candidate-progress", candidate_progress, source)
    return replace("data-finding-progress", finding_progress, source)


def _validate_section(kind: str, identifier: str, fragment: str) -> _MarkupFacts:
    if kind not in _KINDS:
        raise ReportUpdateError(f"unsupported section kind: {kind}")
    if not _SECTION_ID.fullmatch(identifier):
        raise ReportUpdateError(f"unsafe section ID: {identifier}")
    if _MARKER_PREFIX in fragment:
        raise ReportUpdateError("fragment may not inject audit-codebase markers")

    facts = _facts(fragment)
    anchor = _anchor(kind, identifier)
    if facts.ids.get(anchor, 0) != 1:
        raise ReportUpdateError(
            f"fragment must contain exactly one target anchor {anchor!r}"
        )
    if facts.unsafe:
        raise ReportUpdateError("; ".join(sorted(set(facts.unsafe))))
    return facts


def inspect_report(
    *,
    repo_root: Path,
    report: Path,
    candidate_id: str | None = None,
    subsystem_id: str | None = None,
) -> dict[str, object]:
    """Validate one report and return its local navigation facts."""

    try:
        canonical = _canonical_report(repo_root, report)
        source_bytes, source = _decode(canonical)
        if candidate_id is not None and subsystem_id is not None:
            raise ReportUpdateError("inspect accepts one selected ID")
        facts = _facts(source)
        states, progress, finding_states, finding_progress = _validate_report(source)
        candidates = {
            identifier: {
                "id": identifier,
                "subsystem_id": facts.candidate_cards[identifier][0][
                    "data-subsystem-id"
                ],
                "state": states[identifier],
                "strength": facts.candidate_cards[identifier][0]["data-strength"],
                "pickup": (
                    facts.pickups.get(identifier, {}).get("card", [""])[0]
                    if facts.pickups.get(identifier, {}).get("card")
                    else ""
                ),
            }
            for identifier in sorted(states)
        }
        result: dict[str, object] = {
            "report": str(canonical),
            "report_version": "3",
            "run_id": canonical.parent.name,
            "sha256": _sha256(source_bytes),
            "candidate_states": states,
            "candidate_progress": progress,
            "finding_states": finding_states,
            "finding_progress": finding_progress,
            "stage": "inspect",
            "mutation_started": False,
            "report_unchanged": True,
            "capabilities": {
                "update_candidate": True,
                "reaudit_subsystem": all(
                    facts.insertions.get((kind, identifier), 0) == 1
                    for identifier in facts.subsystems
                    for kind in _INSERT_KINDS
                ),
                "close_candidate_findings": True,
            },
        }
        if candidate_id is not None:
            if candidate_id not in candidates:
                raise ReportUpdateError(f"candidate not found: {candidate_id}")
            result["candidate"] = candidates[candidate_id]
        elif subsystem_id is not None:
            if subsystem_id not in facts.subsystems:
                raise ReportUpdateError(f"subsystem not found: {subsystem_id}")
            subsystem = facts.subsystems[subsystem_id][0]
            grouped_findings = {
                state: sorted(
                    identifier
                    for identifier, finding_state in finding_states.items()
                    if finding_state == state
                    and facts.findings[identifier][0]["data-subsystem-id"]
                    == subsystem_id
                )
                for state in _FINDING_STATES
            }
            result["subsystem"] = {
                "id": subsystem_id,
                "state": subsystem["data-state"],
                "source_identity": subsystem["data-source-identity"],
                "findings": grouped_findings,
                "retained_complexity": sorted(
                    identifier
                    for identifier, records in facts.retained.items()
                    if records[0].get("data-subsystem-id") == subsystem_id
                ),
                "gaps": sorted(
                    identifier
                    for identifier, records in facts.gaps.items()
                    if records[0].get("data-subsystem-id") == subsystem_id
                ),
                "candidates": sorted(
                    identifier
                    for identifier, candidate in candidates.items()
                    if candidate["subsystem_id"] == subsystem_id
                ),
                "regions": {
                    "narrative": source.count(
                        _marker("subsystem-narrative", subsystem_id, "start")
                    )
                    == 1,
                    "finding_insert": facts.insertions.get(
                        ("finding-insert", subsystem_id), 0
                    )
                    == 1,
                    "candidate_index_insert": facts.insertions.get(
                        ("candidate-index-insert", subsystem_id), 0
                    )
                    == 1,
                    "candidate_insert": facts.insertions.get(
                        ("candidate-insert", subsystem_id), 0
                    )
                    == 1,
                },
            }
        else:
            result["candidates"] = list(candidates.values())
        return result
    except ReportUpdateError as exc:
        exc.stage = "inspect"
        raise


def _prepare_update(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    sections: Sequence[tuple[str, str, Path]],
) -> dict[str, object]:
    """Build and validate one prospective non-overlapping section update."""

    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ReportUpdateError("expected SHA-256 must be 64 lowercase hex characters")
    if not sections:
        raise ReportUpdateError("at least one section is required")

    report = _canonical_report(repo_root, report)
    source_bytes, source = _decode(report)
    observed_sha256 = _sha256(source_bytes)
    if observed_sha256 != expected_sha256:
        raise ReportUpdateError(
            f"report collision: expected {expected_sha256}, observed {observed_sha256}"
        )
    _validate_report(source)

    replacements: list[tuple[int, int, str, _MarkupFacts, str]] = []
    seen: set[tuple[str, str]] = set()
    for kind, identifier, fragment_path in sections:
        key = (kind, identifier)
        if key in seen:
            raise ReportUpdateError(f"duplicate replacement: {kind}:{identifier}")
        seen.add(key)

        _, fragment = _decode(fragment_path)
        fragment_facts = _validate_section(kind, identifier, fragment)
        start_marker = _marker(kind, identifier, "start")
        end_marker = _marker(kind, identifier, "end")
        if source.count(start_marker) != 1 or source.count(end_marker) != 1:
            raise ReportUpdateError(
                f"report must contain one marker pair for {kind}:{identifier}"
            )
        start = source.index(start_marker)
        end_start = source.find(end_marker, start + len(start_marker))
        if end_start < 0:
            raise ReportUpdateError(f"reversed marker pair for {kind}:{identifier}")
        end = end_start + len(end_marker)
        replacement = f"{start_marker}\n{fragment.strip()}\n{end_marker}"
        replacements.append((start, end, replacement, fragment_facts, f"{kind}:{identifier}"))

    ordered = sorted(replacements, key=lambda item: item[0])
    for left, right in zip(ordered, ordered[1:]):
        if left[1] > right[0]:
            raise ReportUpdateError(
                f"overlapping replacements are not allowed: {left[4]} and {right[4]}"
            )

    updated = source
    for start, end, replacement, _, _ in reversed(ordered):
        updated = updated[:start] + replacement + updated[end:]

    updated = _sync_progress(updated)
    final_facts = _facts(updated)
    candidate_states, progress, finding_states, finding_progress = (
        _validate_report(updated)
    )
    for _, _, _, fragment_facts, label in replacements:
        kind, identifier = label.split(":", 1)
        anchor = _anchor(kind, identifier)
        if final_facts.ids.get(anchor, 0) != 1:
            raise ReportUpdateError(
                f"updated target anchor {anchor!r} does not occur exactly once"
            )
        for changed_id in fragment_facts.ids:
            if final_facts.ids.get(changed_id, 0) != 1:
                raise ReportUpdateError(
                    f"changed ID {changed_id!r} from {label} does not occur exactly once"
                )
        for target in fragment_facts.fragment_links:
            if final_facts.ids.get(target, 0) != 1:
                raise ReportUpdateError(
                    f"changed-fragment link #{target} from {label} does not resolve once"
                )

    updated_bytes = updated.encode("utf-8")
    return {
        "_report_path": report,
        "_source_bytes": source_bytes,
        "_updated_bytes": updated_bytes,
        "report": str(report),
        "sha256": _sha256(updated_bytes),
        "sections": [item[4] for item in replacements],
        "candidate_states": candidate_states,
        "candidate_progress": progress,
        "finding_states": finding_states,
        "finding_progress": finding_progress,
    }


def validate_report_update(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    sections: Sequence[tuple[str, str, Path]],
) -> dict[str, object]:
    """Validate a prospective update without creating or changing files."""

    prepared = _prepare_update(
        repo_root=repo_root,
        report=report,
        expected_sha256=expected_sha256,
        sections=sections,
    )
    return {
        key: value
        for key, value in prepared.items()
        if not key.startswith("_")
    } | {
        "stage": "validate",
        "mutation_started": False,
        "report_unchanged": True,
    }


def _publish_prepared(prepared: dict[str, object]) -> dict[str, object]:
    report = prepared["_report_path"]
    source_bytes = prepared["_source_bytes"]
    updated_bytes = prepared["_updated_bytes"]
    assert isinstance(report, Path)
    assert isinstance(source_bytes, bytes)
    assert isinstance(updated_bytes, bytes)

    sibling: Path | None = None
    try:
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=f"{report.name}.audit-update-",
                suffix=".tmp",
                dir=report.parent,
                delete=False,
            ) as handle:
                sibling = Path(handle.name)
                handle.write(updated_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(sibling, report.stat().st_mode)
            reread_bytes, reread = _decode(sibling)
            if reread_bytes != updated_bytes:
                raise ReportUpdateError(
                    "atomic sibling read-back mismatch",
                    stage="render",
                )
            _validate_report(reread)
        except OSError as exc:
            raise ReportUpdateError(
                f"cannot render atomic sibling: {exc}",
                stage="render",
            ) from exc

        try:
            current_bytes = report.read_bytes()
        except OSError as exc:
            raise ReportUpdateError(
                f"cannot verify report collision: {exc}",
                stage="collision-check",
            ) from exc
        if current_bytes != source_bytes:
            raise ReportUpdateError(
                "report changed concurrently before replacement",
                stage="collision-check",
            )
        try:
            os.replace(sibling, report)
        except OSError as exc:
            try:
                unchanged = report.exists() and report.read_bytes() == source_bytes
            except OSError:
                unchanged = False
            raise ReportUpdateError(
                f"atomic replacement failed: {exc}",
                stage="replace",
                mutation_started=True,
                report_unchanged=unchanged,
            ) from exc
        sibling = None
        try:
            published = report.read_bytes()
        except OSError as exc:
            raise ReportUpdateError(
                f"published report read-back failed: {exc}",
                stage="read-back",
                mutation_started=True,
                report_unchanged=False,
            ) from exc
        if published != updated_bytes:
            raise ReportUpdateError(
                "published report read-back mismatch",
                stage="read-back",
                mutation_started=True,
                report_unchanged=False,
            )
    finally:
        if sibling is not None:
            active_error = sys.exc_info()[0] is not None
            try:
                sibling.unlink(missing_ok=True)
            except OSError as exc:
                if not active_error:
                    raise ReportUpdateError(
                        f"atomic sibling cleanup failed: {exc}",
                        stage="cleanup",
                    ) from exc

    return {
        key: value
        for key, value in prepared.items()
        if not key.startswith("_")
    } | {
        "stage": "read-back",
        "mutation_started": True,
        "report_unchanged": False,
    }


def update_report(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    sections: Sequence[tuple[str, str, Path]],
) -> dict[str, object]:
    """Validate and atomically publish one non-overlapping section update."""

    return _publish_prepared(
        _prepare_update(
            repo_root=repo_root,
            report=report,
            expected_sha256=expected_sha256,
            sections=sections,
        )
    )


def _insert_marker(kind: str, subsystem_id: str) -> str:
    return f"<!-- audit-codebase:{kind}:{subsystem_id} -->"


def _upsert_region(
    source: str,
    *,
    kind: str,
    identifier: str,
    fragment: str,
    insert_kind: str,
    subsystem_id: str,
) -> tuple[str, bool]:
    start_marker = _marker(kind, identifier, "start")
    end_marker = _marker(kind, identifier, "end")
    replacement = f"{start_marker}\n{fragment.strip()}\n{end_marker}"
    if start_marker in source or end_marker in source:
        start, end = _marked_bounds(source, kind, identifier)
        return source[:start] + replacement + source[end:], False
    anchor = _insert_marker(insert_kind, subsystem_id)
    if source.count(anchor) != 1:
        raise ReportUpdateError(
            f"subsystem {subsystem_id!r} has no unique {insert_kind} anchor"
        )
    return source.replace(anchor, f"{replacement}\n{anchor}", 1), True


def _prepared_markup(
    *,
    report: Path,
    source_bytes: bytes,
    updated: str,
    sections: list[str],
) -> dict[str, object]:
    updated = _sync_progress(updated)
    candidate_states, candidate_progress, finding_states, finding_progress = (
        _validate_report(updated)
    )
    updated_bytes = updated.encode("utf-8")
    return {
        "_report_path": report,
        "_source_bytes": source_bytes,
        "_updated_bytes": updated_bytes,
        "report": str(report),
        "sha256": _sha256(updated_bytes),
        "sections": sections,
        "candidate_states": candidate_states,
        "candidate_progress": candidate_progress,
        "finding_states": finding_states,
        "finding_progress": finding_progress,
    }


def reaudit_subsystem(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    subsystem_id: str,
    subsystem_state: str,
    source_identity: str,
    narrative_path: Path,
    findings: Sequence[tuple[str, Path]] = (),
    candidates: Sequence[tuple[str, Path, Path]] = (),
    validate_only: bool = False,
) -> dict[str, object]:
    """Atomically refresh one subsystem and upsert its findings and candidates."""

    if not _SECTION_ID.fullmatch(subsystem_id):
        raise ReportUpdateError(f"unsafe subsystem ID: {subsystem_id}")
    if subsystem_state not in _SUBSYSTEM_STATES:
        raise ReportUpdateError(f"unsupported subsystem state: {subsystem_state}")
    if not source_identity.strip():
        raise ReportUpdateError("source identity must not be empty")
    canonical = _canonical_report(repo_root, report)
    source_bytes, source = _decode(canonical)
    if _sha256(source_bytes) != expected_sha256:
        raise ReportUpdateError(
            f"report collision: expected {expected_sha256}, "
            f"observed {_sha256(source_bytes)}"
        )
    facts = _facts(source)
    _validate_report(source)
    if subsystem_id not in facts.subsystems:
        raise ReportUpdateError(f"subsystem not found: {subsystem_id}")

    section_pattern = re.compile(
        rf"<section\b[^>]*\bid\s*=\s*([\"'])"
        rf"subsystem-{re.escape(subsystem_id)}\1[^>]*>"
    )
    section_match = section_pattern.search(source)
    if section_match is None:
        raise ReportUpdateError(f"subsystem container not found: {subsystem_id}")
    section_tag = section_match.group(0)
    for name, value in (
        ("data-state", subsystem_state),
        ("data-source-identity", source_identity.strip()),
    ):
        section_tag, count = re.subn(
            rf"(\b{re.escape(name)}\s*=\s*)([\"'])[^\"']*\2",
            lambda match, replacement=escape(value, quote=True): (
                f"{match.group(1)}{match.group(2)}{replacement}{match.group(2)}"
            ),
            section_tag,
            count=1,
        )
        if count != 1:
            raise ReportUpdateError(f"subsystem container has no {name}")
    source = source[: section_match.start()] + section_tag + source[section_match.end() :]

    _, narrative = _decode(narrative_path)
    _validate_section("subsystem-narrative", subsystem_id, narrative)
    start, end = _marked_bounds(source, "subsystem-narrative", subsystem_id)
    updated = (
        source[:start]
        + f"{_marker('subsystem-narrative', subsystem_id, 'start')}\n"
        + narrative.strip()
        + f"\n{_marker('subsystem-narrative', subsystem_id, 'end')}"
        + source[end:]
    )
    sections = [f"subsystem-narrative:{subsystem_id}"]
    seen_findings: set[str] = set()
    for identifier, path in findings:
        if identifier in seen_findings:
            raise ReportUpdateError(f"duplicate finding update: {identifier}")
        seen_findings.add(identifier)
        _, fragment = _decode(path)
        fragment_facts = _validate_section("finding", identifier, fragment)
        record = fragment_facts.findings.get(identifier, [])
        if (
            len(record) != 1
            or record[0].get("data-subsystem-id") != subsystem_id
        ):
            raise ReportUpdateError(
                f"finding {identifier!r} does not belong to subsystem {subsystem_id!r}"
            )
        updated, _ = _upsert_region(
            updated,
            kind="finding",
            identifier=identifier,
            fragment=fragment,
            insert_kind="finding-insert",
            subsystem_id=subsystem_id,
        )
        sections.append(f"finding:{identifier}")

    seen_candidates: set[str] = set()
    for identifier, card_path, row_path in candidates:
        if identifier in seen_candidates:
            raise ReportUpdateError(f"duplicate candidate update: {identifier}")
        seen_candidates.add(identifier)
        _, card = _decode(card_path)
        _, row = _decode(row_path)
        card_facts = _validate_section("candidate", identifier, card)
        row_facts = _validate_section("candidate-index", identifier, row)
        card_record = card_facts.candidate_cards.get(identifier, [])
        row_record = row_facts.candidate_rows.get(identifier, [])
        if (
            len(card_record) != 1
            or len(row_record) != 1
            or card_record[0].get("data-subsystem-id") != subsystem_id
            or row_record[0].get("data-subsystem-id") != subsystem_id
        ):
            raise ReportUpdateError(
                f"candidate {identifier!r} does not belong to subsystem "
                f"{subsystem_id!r}"
            )
        updated, _ = _upsert_region(
            updated,
            kind="candidate-index",
            identifier=identifier,
            fragment=row,
            insert_kind="candidate-index-insert",
            subsystem_id=subsystem_id,
        )
        updated, _ = _upsert_region(
            updated,
            kind="candidate",
            identifier=identifier,
            fragment=card,
            insert_kind="candidate-insert",
            subsystem_id=subsystem_id,
        )
        sections.extend(
            (f"candidate-index:{identifier}", f"candidate:{identifier}")
        )

    prepared = _prepared_markup(
        report=canonical,
        source_bytes=source_bytes,
        updated=updated,
        sections=sections,
    )
    if validate_only:
        return {
            key: value
            for key, value in prepared.items()
            if not key.startswith("_")
        } | {
            "stage": "validate",
            "mutation_started": False,
            "report_unchanged": True,
        }
    return _publish_prepared(prepared)


def _load_completion(path: Path) -> dict[str, object]:
    _, source = _decode(path)
    try:
        value = json.loads(source)
    except json.JSONDecodeError as exc:
        raise ReportUpdateError(f"completion packet is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ReportUpdateError("completion packet must be a JSON object")
    return value


def _packet_text(packet: dict[str, object], name: str) -> str:
    value = packet.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ReportUpdateError(f"completion packet requires {name}")
    return value.strip()


def _marked_bounds(source: str, kind: str, identifier: str) -> tuple[int, int]:
    start_marker = _marker(kind, identifier, "start")
    end_marker = _marker(kind, identifier, "end")
    if source.count(start_marker) != 1 or source.count(end_marker) != 1:
        raise ReportUpdateError(
            f"report must contain one marker pair for {kind}:{identifier}"
        )
    start = source.index(start_marker)
    end = source.index(end_marker, start) + len(end_marker)
    return start, end


def _without_pickup(region: str, identifier: str, view: str) -> str:
    pattern = re.compile(
        rf"<code\b(?=[^>]*\bdata-candidate-pickup="
        rf'["\']{re.escape(identifier)}["\'])(?=[^>]*\bdata-pickup-view='
        rf'["\']{view}["\'])'
        r"[^>]*>.*?</code>",
        flags=re.DOTALL,
    )
    updated, count = pattern.subn("", region)
    if count > 1:
        raise ReportUpdateError(
            f"candidate {identifier!r} has multiple {view} pickups"
        )
    return updated


def _implemented_evidence(
    identifier: str,
    packet: dict[str, object],
) -> str:
    commit = _packet_text(packet, "commit_identity")
    tree = _packet_text(packet, "commit_tree_identity")
    source_status = _packet_text(packet, "current_source_result")
    if not _GIT_ID.fullmatch(commit) or not _GIT_ID.fullmatch(tree):
        raise ReportUpdateError("completion packet has invalid commit identity")
    if source_status not in {"current", "reachable"}:
        raise ReportUpdateError("completion packet has invalid current_source_result")
    repairs = packet.get("repair_generations_used")
    if not isinstance(repairs, int) or isinstance(repairs, bool) or repairs < 0:
        raise ReportUpdateError("completion packet has invalid repair_generations_used")

    visible = (
        ("Commit", commit),
        ("Tree", tree),
        ("Current source", source_status),
        ("Accepted proof", _packet_text(packet, "accepted_proof")),
        ("Changed scope", _packet_text(packet, "changed_scope")),
        ("Residual risk", _packet_text(packet, "residual_risk")),
        ("Last verified", _packet_text(packet, "last_verified_identity")),
    )
    items = "".join(
        f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>"
        for label, value in visible
    )
    return (
        f'\n<p data-implemented-banner="{identifier}">'
        "Implemented and verified.</p>\n"
        '<dl data-implementation-result="complete" '
        f'data-candidate-id="{identifier}" '
        f'data-commit-sha="{commit}" data-tree-sha="{tree}" '
        f'data-source-status="{source_status}" data-proof-status="accepted" '
        f'data-review-status="accepted" data-repair-generations="{repairs}" '
        'data-closure-status="complete" data-blockers="none">'
        f"{items}</dl>\n"
    )


def _replace_state(
    region: str,
    tag: str,
    old_state: str,
    new_state: str,
) -> tuple[str, int]:
    pattern = re.compile(
        rf"(<{tag}\b[^>]*\bdata-state\s*=\s*)([\"'])"
        rf"{re.escape(old_state)}\2"
    )
    return pattern.subn(
        lambda match: (
            f"{match.group(1)}{match.group(2)}{new_state}{match.group(2)}"
        ),
        region,
        count=1,
    )


def close_candidate(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    candidate_id: str,
    completion_path: Path,
) -> dict[str, object]:
    """Close one analyzed candidate from a root-admitted completion packet."""

    if not _SECTION_ID.fullmatch(candidate_id):
        raise ReportUpdateError(f"unsafe candidate ID: {candidate_id}")
    canonical = _canonical_report(repo_root, report)
    source_bytes, source = _decode(canonical)
    if _sha256(source_bytes) != expected_sha256:
        raise ReportUpdateError(
            f"report collision: expected {expected_sha256}, "
            f"observed {_sha256(source_bytes)}"
        )
    facts = _facts(source)
    states, _, finding_states, _ = _validate_report(source)
    if states.get(candidate_id) != "analyzed":
        raise ReportUpdateError(
            f"candidate {candidate_id!r} must be analyzed before closeout"
        )

    packet = _load_completion(completion_path)
    required = {
        "implementation_outcome": "complete",
        "run_id": canonical.parent.name,
        "candidate_id": candidate_id,
        "formal_review_decision": "accepted",
        "change_closure": "complete",
    }
    for name, expected in required.items():
        if packet.get(name) != expected:
            raise ReportUpdateError(
                f"completion packet {name} does not match {expected!r}"
            )
    try:
        packet_report = Path(_packet_text(packet, "report")).resolve(strict=True)
    except OSError as exc:
        raise ReportUpdateError(f"completion packet report cannot resolve: {exc}") from exc
    if packet_report != canonical:
        raise ReportUpdateError("completion packet report does not match")
    subsystem_id = _packet_text(packet, "subsystem_id")
    if not _SECTION_ID.fullmatch(subsystem_id):
        raise ReportUpdateError("completion packet has unsafe subsystem_id")
    _packet_text(packet, "accepted_proof")
    _packet_text(packet, "changed_scope")
    _packet_text(packet, "residual_risk")
    _packet_text(packet, "last_verified_identity")
    raw_transitions = packet.get("finding_transitions")
    if not isinstance(raw_transitions, list):
        raise ReportUpdateError("completion packet requires finding_transitions")
    transitions: dict[str, tuple[str, str]] = {}
    for item in raw_transitions:
        if not isinstance(item, dict):
            raise ReportUpdateError("finding transition must be an object")
        finding_id = item.get("finding_id")
        state = item.get("state")
        reason = item.get("reason")
        if (
            not isinstance(finding_id, str)
            or not isinstance(state, str)
            or state not in _FINDING_STATES
            or not isinstance(reason, str)
            or not reason.strip()
            or finding_id in transitions
        ):
            raise ReportUpdateError("completion packet has invalid finding transition")
        transitions[finding_id] = (state, reason.strip())

    member_findings = set(facts.candidate_findings.get(candidate_id, []))
    active_members = {
        identifier
        for identifier in member_findings
        if finding_states.get(identifier) == "active"
    }
    if set(transitions) != active_members:
        raise ReportUpdateError(
            "finding transitions must cover every active candidate finding"
        )

    card_start, card_end = _marked_bounds(source, "candidate", candidate_id)
    row_start, row_end = _marked_bounds(source, "candidate-index", candidate_id)
    card_record = facts.candidate_cards[candidate_id][0]
    row_record = facts.candidate_rows[candidate_id][0]
    if (
        card_record.get("data-subsystem-id") != subsystem_id
        or row_record.get("data-subsystem-id") != subsystem_id
    ):
        raise ReportUpdateError("candidate is not inside the matching subsystem")

    card = source[card_start:card_end]
    row = source[row_start:row_end]
    card, card_count = _replace_state(card, "article", "analyzed", "implemented")
    row, row_count = _replace_state(row, "tr", "analyzed", "implemented")
    if card_count != 1 or row_count != 1:
        raise ReportUpdateError("candidate state projections are not closeable")
    card = _without_pickup(card, candidate_id, "card")
    row = _without_pickup(row, candidate_id, "index")
    closing = card.rfind("</article>")
    if closing < 0:
        raise ReportUpdateError("candidate card has no closing article")
    card = card[:closing] + _implemented_evidence(candidate_id, packet) + card[closing:]

    replacements = [(card_start, card_end, card), (row_start, row_end, row)]
    for finding_id, (state, reason) in transitions.items():
        finding_start, finding_end = _marked_bounds(source, "finding", finding_id)
        finding = source[finding_start:finding_end]
        finding, count = _replace_state(
            finding,
            "article",
            finding_states[finding_id],
            state,
        )
        if count != 1:
            raise ReportUpdateError(
                f"finding {finding_id!r} state is not closeable"
            )
        closing = finding.rfind("</article>")
        if closing < 0:
            raise ReportUpdateError(f"finding {finding_id!r} has no closing article")
        transition = (
            f'\n<p data-finding-transition="{finding_id}" '
            f'data-state="{state}">{escape(reason)}</p>\n'
        )
        finding = finding[:closing] + transition + finding[closing:]
        replacements.append((finding_start, finding_end, finding))

    updated = source
    for start, end, replacement in sorted(replacements, reverse=True):
        updated = updated[:start] + replacement + updated[end:]

    prepared = _prepared_markup(
        report=canonical,
        source_bytes=source_bytes,
        updated=updated,
        sections=[
            f"candidate:{candidate_id}",
            f"candidate-index:{candidate_id}",
            *(f"finding:{identifier}" for identifier in sorted(transitions)),
        ],
    )
    return _publish_prepared(prepared)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    def add_report_args(command: argparse.ArgumentParser) -> None:
        command.add_argument("--repo-root", type=Path, required=True)
        command.add_argument("--report", type=Path, required=True)

    inspect = commands.add_parser("inspect")
    add_report_args(inspect)
    inspect.add_argument("--candidate-id")
    inspect.add_argument("--subsystem-id")

    for name in ("validate", "update"):
        command = commands.add_parser(name)
        add_report_args(command)
        command.add_argument("--expected-sha256", required=True)
        command.add_argument(
            "--section",
            nargs=3,
            action="append",
            metavar=("KIND", "ID", "FRAGMENT"),
            required=True,
        )

    close = commands.add_parser("close-candidate")
    add_report_args(close)
    close.add_argument("--expected-sha256", required=True)
    close.add_argument("--candidate-id", required=True)
    close.add_argument("--completion", type=Path, required=True)

    reaudit = commands.add_parser("reaudit-subsystem")
    add_report_args(reaudit)
    reaudit.add_argument("--expected-sha256", required=True)
    reaudit.add_argument("--subsystem-id", required=True)
    reaudit.add_argument(
        "--subsystem-state",
        required=True,
        choices=sorted(_SUBSYSTEM_STATES),
    )
    reaudit.add_argument("--source-identity", required=True)
    reaudit.add_argument("--narrative", type=Path, required=True)
    reaudit.add_argument(
        "--finding",
        nargs=2,
        action="append",
        default=[],
        metavar=("ID", "FRAGMENT"),
    )
    reaudit.add_argument(
        "--candidate",
        nargs=3,
        action="append",
        default=[],
        metavar=("ID", "CARD", "INDEX"),
    )
    reaudit.add_argument("--validate-only", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_report(
                repo_root=args.repo_root,
                report=args.report,
                candidate_id=args.candidate_id,
                subsystem_id=args.subsystem_id,
            )
        elif args.command in {"validate", "update"}:
            sections = [
                (kind, identifier, Path(fragment))
                for kind, identifier, fragment in args.section
            ]
            operation = (
                validate_report_update
                if args.command == "validate"
                else update_report
            )
            result = operation(
                repo_root=args.repo_root,
                report=args.report,
                expected_sha256=args.expected_sha256,
                sections=sections,
            )
        elif args.command == "close-candidate":
            result = close_candidate(
                repo_root=args.repo_root,
                report=args.report,
                expected_sha256=args.expected_sha256,
                candidate_id=args.candidate_id,
                completion_path=args.completion,
            )
        else:
            result = reaudit_subsystem(
                repo_root=args.repo_root,
                report=args.report,
                expected_sha256=args.expected_sha256,
                subsystem_id=args.subsystem_id,
                subsystem_state=args.subsystem_state,
                source_identity=args.source_identity,
                narrative_path=args.narrative,
                findings=tuple(
                    (identifier, Path(fragment))
                    for identifier, fragment in args.finding
                ),
                candidates=tuple(
                    (identifier, Path(card), Path(index))
                    for identifier, card, index in args.candidate
                ),
                validate_only=args.validate_only,
            )
    except (OSError, ReportUpdateError) as exc:
        error = (
            exc
            if isinstance(exc, ReportUpdateError)
            else ReportUpdateError(str(exc), stage=args.command)
        )
        print(json.dumps(error.as_dict(), sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
