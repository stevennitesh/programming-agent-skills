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
_KINDS = {"system", "subsystem", "candidate", "summary"}
_MARKER_PREFIX = "<!-- audit-codebase:"
_UNSAFE_HREF = re.compile(r"(?i)^(?://|[a-z][a-z0-9+.-]*:)")
_UNSAFE_TAGS = {"base", "embed", "form", "iframe", "link", "object", "script", "style"}
_RESOURCE_ATTRS = {"action", "data", "formaction", "poster", "src", "srcset"}


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
    except Exception as exc:  # HTMLParser may surface malformed entity state.
        raise ReportUpdateError(f"HTML parse failed: {exc}") from exc
    return parser


def _marker(kind: str, identifier: str, edge: str) -> str:
    return f"<!-- audit-codebase:{kind}:{identifier}:{edge} -->"


def _validate_section(kind: str, identifier: str, fragment: str) -> _MarkupFacts:
    if kind not in _KINDS:
        raise ReportUpdateError(f"unsupported section kind: {kind}")
    if not _SECTION_ID.fullmatch(identifier):
        raise ReportUpdateError(f"unsafe section ID: {identifier}")
    if _MARKER_PREFIX in fragment:
        raise ReportUpdateError("fragment may not inject audit-codebase markers")

    facts = _facts(fragment)
    anchor = f"{kind}-{identifier}"
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
    if final_facts.html_count != 1 or final_facts.main_count != 1:
        raise ReportUpdateError("updated report must contain one html and one main element")
    for _, _, _, fragment_facts, label in replacements:
        kind, identifier = label.split(":", 1)
        anchor = f"{kind}-{identifier}"
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
        if reread_facts.html_count != 1 or reread_facts.main_count != 1:
            raise ReportUpdateError("atomic sibling failed final structure check")

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
