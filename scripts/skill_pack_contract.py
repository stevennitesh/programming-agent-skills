"""Shared identities and manifest rules for the custom skill pack."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections.abc import Callable
from pathlib import Path


MANIFEST_NAME = ".programming-agent-skills-manifest.json"
MANIFEST_FORMAT = 1
MANIFEST_SOURCE = "skills/custom"
EXPERIMENTAL_SOURCE = "skills/experimental"
EXPERIMENTAL_MANIFEST_NAME = "manifest.json"
EXPERIMENTAL_MANIFEST_FORMAT = 1
SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def level_two_heading_spans(text: str) -> list[tuple[str, int, int]]:
    """Return real level-two Markdown headings and spans, excluding fences."""
    headings: list[tuple[str, int]] = []
    offset = 0
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        fence_match = re.match(r"^[ \t]*(`{3,}|~{3,})", content)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
        elif fence is None:
            heading_match = re.fullmatch(r"##[ \t]+(.+?)[ \t]*", content)
            if heading_match:
                headings.append((heading_match.group(1), offset))
        offset += len(line)

    return [
        (title, start, headings[index + 1][1] if index + 1 < len(headings) else len(text))
        for index, (title, start) in enumerate(headings)
    ]


def level_two_section_span(text: str, heading: str) -> tuple[int, int] | None:
    """Return one exact level-two section span or reject duplicate headings."""
    title = heading.removeprefix("## ")
    matches = [
        (start, end)
        for candidate, start, end in level_two_heading_spans(text)
        if candidate == title
    ]
    if len(matches) > 1:
        raise ValueError(f"Markdown must contain exactly one {heading} heading")
    return matches[0] if matches else None


def lexical_path(path: Path) -> Path:
    """Return an absolute path without following links or reparse points."""
    return Path(os.path.abspath(os.fspath(path.expanduser())))


def reject_unsafe_redirect(path: Path, label: str) -> None:
    """Reject links/reparse points in an existing path or any existing ancestor."""
    candidate = lexical_path(path)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    while True:
        try:
            metadata = os.lstat(candidate)
        except FileNotFoundError:
            pass
        except OSError as error:
            raise ValueError(f"Cannot inspect {label}: {candidate}: {error}") from error
        else:
            is_reparse = bool(
                reparse_flag
                and getattr(metadata, "st_file_attributes", 0) & reparse_flag
            )
            if stat.S_ISLNK(metadata.st_mode) or is_reparse:
                raise ValueError(f"Unsafe {label} link/reparse point: {candidate}")
        if candidate.parent == candidate:
            break
        candidate = candidate.parent


def tree_entries(
    directory: Path,
    *,
    ignore: Callable[[Path, bool], bool] | None = None,
) -> dict[str, tuple[str, bytes]]:
    directory = directory.expanduser()
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)

    def classify(path: Path) -> tuple[str, bytes]:
        metadata = os.lstat(path)
        is_reparse = bool(
            reparse_flag and getattr(metadata, "st_file_attributes", 0) & reparse_flag
        )
        if stat.S_ISLNK(metadata.st_mode) or is_reparse:
            raise ValueError(f"Unsafe special tree entry (link/reparse point): {path}")
        if stat.S_ISDIR(metadata.st_mode):
            return "directory", b""
        if stat.S_ISREG(metadata.st_mode):
            return "file", path.read_bytes()
        raise ValueError(f"Unsafe special tree entry (unsupported type): {path}")

    root_kind, _ = classify(directory)
    if root_kind != "directory":
        raise ValueError(f"Skill tree root is not a directory: {directory}")

    entries: dict[str, tuple[str, bytes]] = {}
    for current, directory_names, file_names in os.walk(
        directory,
        topdown=True,
        followlinks=False,
    ):
        directory_names.sort()
        file_names.sort()
        current_path = Path(current)
        kept_directories: list[str] = []
        for name in directory_names:
            path = current_path / name
            relative_path = path.relative_to(directory)
            relative = relative_path.as_posix()
            entry = classify(path)
            if ignore is not None and ignore(relative_path, True):
                continue
            entries[relative] = entry
            kept_directories.append(name)
        directory_names[:] = kept_directories
        for name in file_names:
            path = current_path / name
            relative_path = path.relative_to(directory)
            relative = relative_path.as_posix()
            entry = classify(path)
            if ignore is not None and ignore(relative_path, False):
                continue
            entries[relative] = entry
    return entries


def tree_hash(
    directory: Path,
    *,
    ignore: Callable[[Path, bool], bool] | None = None,
) -> str:
    entries = tree_entries(directory, ignore=ignore)
    names = set(entries)
    digest = hashlib.sha256()
    # Preserve format-1 Path ordering. Existing manifests rely on its
    # platform-specific ordering for ordinary file-only trees.
    for name in sorted(entries, key=Path):
        kind, content = entries[name]
        if kind == "directory":
            prefix = f"{name}/"
            if any(other.startswith(prefix) for other in names):
                continue
            digest.update(b"empty-directory\0")
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def manifest_bytes(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def parse_managed_manifest_payload(
    payload: object,
) -> tuple[set[str], dict[str, str], list[str]]:
    if not isinstance(payload, dict):
        return set(), {}, ["Installed skill manifest must be an object."]

    failures: list[str] = []
    if payload.get("format") != MANIFEST_FORMAT:
        failures.append(f"Installed skill manifest must use format {MANIFEST_FORMAT}.")
    if payload.get("source") != MANIFEST_SOURCE:
        failures.append(f"Installed skill manifest source must be {MANIFEST_SOURCE}.")

    raw_names = payload.get("skills")
    if not isinstance(raw_names, list) or not all(
        isinstance(name, str) for name in raw_names
    ):
        failures.append("Installed skill manifest must contain a string list named skills.")
        names: set[str] = set()
    else:
        names = set(raw_names)
        if len(names) != len(raw_names):
            failures.append("Installed skill manifest skills must be unique.")
        for name in raw_names:
            if not SKILL_NAME_RE.fullmatch(name):
                failures.append(
                    f"Installed skill manifest has unsafe skill name: {name!r}."
                )

    raw_hashes = payload.get("hashes")
    if not isinstance(raw_hashes, dict) or not all(
        isinstance(name, str)
        and isinstance(value, str)
        and SHA256_RE.fullmatch(value)
        for name, value in raw_hashes.items()
    ):
        failures.append(
            "Installed skill manifest hashes must map skill names to lowercase "
            "SHA-256 digests."
        )
        hashes: dict[str, str] = {}
    else:
        hashes = dict(raw_hashes)
        if set(hashes) != names:
            failures.append(
                "Installed skill manifest hash keys must exactly match managed skills."
            )
    return names, hashes, failures
