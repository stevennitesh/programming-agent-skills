"""Atomically replace marked regions in one audit-codebase HTML report."""

from __future__ import annotations

import argparse
import hashlib
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
_KINDS = {"system", "subsystem", "candidate", "candidate-index", "summary"}
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
_PROGRESS_IDS = {"report-header", "summary-progress", "report-footer"}


class ReportUpdateError(ValueError):
    """The requested report update failed before publication."""


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
        self.implementation_results: dict[str, list[dict[str, str]]] = {}
        self.progress: dict[str, list[str]] = {}
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
) -> tuple[str, str]:
    if _required(record, "data-candidate-id", label) != identifier:
        raise ReportUpdateError(f"{label} candidate ID does not match its anchor")
    state = _required(record, "data-state", label)
    strength = _required(record, "data-strength", label)
    if state not in _CANDIDATE_STATES:
        raise ReportUpdateError(f"{label} has unsupported candidate state {state!r}")
    if strength not in _STRENGTHS:
        raise ReportUpdateError(f"{label} has unsupported strength {strength!r}")
    return state, strength


def _validate_complete_report(
    facts: _MarkupFacts,
) -> tuple[dict[str, str], str]:
    if facts.html_count != 1 or facts.main_count != 1:
        raise ReportUpdateError("report must contain one html and one main element")
    if facts.report_versions != ["3"]:
        raise ReportUpdateError("report must declare audit-codebase version 3")
    duplicate_ids = sorted(
        identifier for identifier, count in facts.ids.items() if count != 1
    )
    if duplicate_ids:
        raise ReportUpdateError(
            f"report contains duplicate IDs: {', '.join(duplicate_ids)}"
        )

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
        states[identifier] = state
        counts[state] += 1
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
    return states, progress


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


def update_report(
    *,
    repo_root: Path,
    report: Path,
    expected_sha256: str,
    sections: Sequence[tuple[str, str, Path]],
) -> dict[str, object]:
    """Validate and atomically publish one non-overlapping section update."""

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
    _validate_complete_report(_facts(source))

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

    final_facts = _facts(updated)
    candidate_states, progress = _validate_complete_report(final_facts)
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
    sibling: Path | None = None
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
            raise ReportUpdateError("atomic sibling read-back mismatch")
        reread_facts = _facts(reread)
        _validate_complete_report(reread_facts)

        current_bytes = report.read_bytes()
        if _sha256(current_bytes) != expected_sha256:
            raise ReportUpdateError("report changed concurrently before replacement")
        os.replace(sibling, report)
        sibling = None
    finally:
        if sibling is not None:
            sibling.unlink(missing_ok=True)

    return {
        "report": str(report),
        "sha256": _sha256(updated_bytes),
        "sections": [item[4] for item in replacements],
        "candidate_states": candidate_states,
        "candidate_progress": progress,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument(
        "--section",
        nargs=3,
        action="append",
        metavar=("KIND", "ID", "FRAGMENT"),
        required=True,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    sections = [
        (kind, identifier, Path(fragment))
        for kind, identifier, fragment in args.section
    ]
    try:
        result = update_report(
            repo_root=args.repo_root,
            report=args.report,
            expected_sha256=args.expected_sha256,
            sections=sections,
        )
    except (OSError, ReportUpdateError) as exc:
        print(f"report update failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
