"""Repo-specific skill-pack validation.

Skill frontmatter/schema validation is intentionally delegated to the Codex
internal skill validator. This module checks repo-specific integrity and is the
Windows-native entrypoint for the checks formerly owned only by
scripts/validate-skills.sh.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import re
import subprocess
import sys
from pathlib import Path


SKILL_ROOTS = ("skills/current", "skills/experimental", "skills/extra")
REQUIRED_AGENT_DOCS = ("AGENTS_PORTABLE_FALLBACK.md", "AGENTS_SKILL_PACK_GUIDE.md")
REQUIRED_SETUP_DOCS = (
    "AGENTS.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
    "docs/plans/README.md",
    "skills/current/setup-matt-pocock-skills/engineering-contract.md",
)
PUBLISHED_MARKDOWN_ROOTS = (
    "skills",
    "docs/books",
    "docs/agents",
    "docs/plans",
    "docs/language",
)
LOCAL_IDENTIFIER_RE = re.compile(
    r"DESKTOP-|S-1-5-21|[A-Z]:\\|"
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|"
    r"api[_-]?key[ \t]*[:=]|secret[ \t]*[:=]|token[ \t]*[:=]|"
    r"password[ \t]*[:=]|BEGIN (RSA|OPENSSH|PRIVATE)"
)
RESOURCE_REF_RE = re.compile(r"`([^`]+)`")
TRAILING_WHITESPACE_RE = re.compile(r"[ \t]$")


class Validation:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def extend(self, messages: list[str]) -> None:
        self.failures.extend(messages)


def run_git(args: list[str], *, cwd: Path, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def repo_root() -> Path:
    result = run_git(["rev-parse", "--show-toplevel"], cwd=Path.cwd())
    if result.returncode != 0:
        print("Not inside a Git repository.", file=sys.stderr)
        raise SystemExit(1)
    return Path(result.stdout.strip())


def iter_skill_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for relative_root in SKILL_ROOTS:
        skill_root = root / relative_root
        if not skill_root.is_dir():
            continue
        dirs.extend(sorted(path for path in skill_root.iterdir() if path.is_dir()))
    return dirs


def skill_resource_references(skill_file: Path) -> list[str]:
    references: set[str] = set()
    text = skill_file.read_text(encoding="utf-8")
    for match in RESOURCE_REF_RE.finditer(text):
        token = match.group(1)
        if re.match(r"^(templates|references|scripts|examples)/[^`\s]+$", token):
            references.add(token)
    return sorted(references)


def validate_skill_folders(root: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    skill_names: list[str] = []

    if not (root / "skills").is_dir():
        return [], ["Missing skills/ directory."]

    skill_dirs = iter_skill_dirs(root)
    if not skill_dirs:
        failures.append("No skill directories found under skills/.")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        skill_names.append(skill_dir.name)
        if not skill_file.is_file():
            failures.append(f"Skill folder missing SKILL.md: {skill_dir.name}")
            continue

        for resource_ref in skill_resource_references(skill_file):
            resource_path = Path(resource_ref)
            if resource_path.is_absolute() or ".." in resource_path.parts:
                failures.append(
                    "Skill resource reference must stay inside the skill directory: "
                    f"{skill_file.as_posix()} -> {resource_ref}"
                )
                continue
            if not (skill_dir / resource_path).exists():
                failures.append(
                    "Skill resource reference is missing: "
                    f"{skill_file.as_posix()} -> {resource_ref}"
                )

    return sorted(skill_names), failures


def validate_required_docs(root: Path) -> list[str]:
    failures: list[str] = []
    if not (root / "README.md").is_file():
        failures.append("Missing README.md.")
    for doc in REQUIRED_AGENT_DOCS:
        if not (root / doc).is_file():
            failures.append(f"Missing required agent instruction document: {doc}")
    for doc in REQUIRED_SETUP_DOCS:
        if not (root / doc).is_file():
            failures.append(f"Missing required setup surface document: {doc}")
    return failures


def unified_file_diff(expected: Path, actual: Path, *, root: Path) -> list[str]:
    if not expected.is_file() or not actual.is_file():
        return []
    if expected.read_bytes() == actual.read_bytes():
        return []
    try:
        result = subprocess.run(
            ["git", "diff", "--no-index", "--", str(expected), str(actual)],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        diff = result.stdout or result.stderr
    except OSError:
        diff = f"{expected} differs from {actual}"
    return ["docs/agents/engineering-contract.md differs from setup template:", *indent_lines(diff)]


def guide_skill_references(root: Path) -> list[str]:
    guide = root / "AGENTS_SKILL_PACK_GUIDE.md"
    if not guide.is_file():
        return []
    refs: set[str] = set()
    for match in RESOURCE_REF_RE.finditer(guide.read_text(encoding="utf-8")):
        token = match.group(1)
        if re.match(r"^[a-z0-9][a-z0-9-]*$", token):
            refs.add(token)
    return sorted(refs)


def validate_guide_refs(root: Path, skill_names: list[str]) -> list[str]:
    names = set(skill_names)
    failures = []
    for skill_name in guide_skill_references(root):
        if skill_name not in names:
            failures.append(f"AGENTS_SKILL_PACK_GUIDE.md references missing skill: {skill_name}")
    return failures


def repo_skill_dir(root: Path, skill_name: str) -> Path | None:
    for relative_root in SKILL_ROOTS:
        candidate = root / relative_root / skill_name
        if candidate.is_dir():
            return candidate
    return None


def compare_dirs(expected: Path, actual: Path) -> list[str]:
    failures: list[str] = []
    comparison = filecmp.dircmp(expected, actual, ignore=["*:Zone.Identifier"])

    for name in sorted(comparison.left_only):
        failures.append(f"Only in repo: {expected / name}")
    for name in sorted(comparison.right_only):
        if name.endswith(":Zone.Identifier"):
            continue
        failures.append(f"Only in installed copy: {actual / name}")
    for name in sorted(comparison.diff_files):
        failures.append(f"Files differ: {expected / name} {actual / name}")
    for name in sorted(comparison.funny_files):
        failures.append(f"Could not compare: {expected / name} {actual / name}")
    for subdir, subcomparison in comparison.subdirs.items():
        failures.extend(compare_dirs(expected / subdir, actual / subdir))
    return failures


def validate_installed_skills(root: Path, skill_names: list[str]) -> list[str]:
    installed_skills_dir = os.environ.get("AGENT_SKILLS_DIR", "")
    require_all_installed = os.environ.get("AGENT_SKILLS_REQUIRE_ALL", "0") == "1"
    failures: list[str] = []
    if not installed_skills_dir:
        return failures

    installed_root = Path(installed_skills_dir).expanduser()
    if not installed_root.is_dir():
        return [f"AGENT_SKILLS_DIR does not exist or is not a directory: {installed_root}"]

    names = set(skill_names)
    for installed_skill_dir in sorted(path for path in installed_root.iterdir() if path.is_dir()):
        if installed_skill_dir.name not in names:
            failures.append(
                f"Installed AGENT_SKILLS_DIR contains unknown or stale skill: {installed_skill_dir.name}"
            )

    for skill_name in skill_names:
        source_dir = repo_skill_dir(root, skill_name)
        if source_dir is None:
            failures.append(f"Repo skill path not found for installed skill comparison: {skill_name}")
            continue
        installed_dir = installed_root / skill_name
        if not installed_dir.is_dir():
            if require_all_installed:
                failures.append(f"Installed skill missing from AGENT_SKILLS_DIR: {skill_name}")
            continue
        diffs = compare_dirs(source_dir, installed_dir)
        if diffs:
            failures.append(f"Installed skill differs from repo: {skill_name}")
            failures.extend(indent_lines("\n".join(diffs)))
    return failures


def published_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in ("README.md", "AGENTS.md", "AGENTS_PORTABLE_FALLBACK.md", "AGENTS_SKILL_PACK_GUIDE.md"):
        path = root / name
        if path.is_file():
            files.append(path)
    for relative_root in PUBLISHED_MARKDOWN_ROOTS:
        directory = root / relative_root
        if directory.is_dir():
            files.extend(sorted(directory.rglob("*.md")))
    return files


def validate_trailing_whitespace(root: Path) -> list[str]:
    failures: list[str] = []
    for path in published_markdown_files(root):
        relative = path.relative_to(root).as_posix()
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if TRAILING_WHITESPACE_RE.search(line):
                failures.append(f"{relative}:{line_number}:{line}")
    if failures:
        return ["Trailing whitespace found:", *indent_lines("\n".join(failures))]
    return []


def validate_public_mode(root: Path) -> list[str]:
    failures: list[str] = []

    tracked = run_git(["ls-files"], cwd=root)
    if tracked.returncode != 0:
        failures.append(f"git ls-files failed: {tracked.stderr.strip()}")
    elif not tracked.stdout.strip():
        failures.append("No tracked files found.")

    ignored = run_git(["ls-files", "-ci", "--exclude-standard"], cwd=root)
    if ignored.returncode != 0:
        failures.append(f"git ls-files ignored scan failed: {ignored.stderr.strip()}")
    elif ignored.stdout.strip():
        failures.append("Tracked files match ignore rules:")
        failures.extend(indent_lines(ignored.stdout))

    grep = run_git(["grep", "-n", "-I", "-E", LOCAL_IDENTIFIER_RE.pattern, "--", "."], cwd=root)
    if grep.returncode == 0:
        for hit in grep.stdout.splitlines():
            if hit.startswith("scripts/validate-skills.sh:") or hit.startswith("scripts/validate_skills.py:"):
                continue
            if "example.com" in hit or "EXAMPLE.COM" in hit or "correct-horse-battery-staple" in hit:
                continue
            failures.append(f"Potential local identifier or secret pattern: {hit}")
    elif grep.returncode != 1:
        failures.append(f"git grep local identifier scan failed: {grep.stderr.strip()}")

    return failures


def validate_git_diff_check(root: Path) -> list[str]:
    diff_check = run_git(["diff", "--check"], cwd=root)
    output = (diff_check.stdout + diff_check.stderr).strip()
    if diff_check.returncode != 0 or output:
        return ["git diff --check reported whitespace or diff issues:", *indent_lines(output)]
    return []


def indent_lines(text: str) -> list[str]:
    if not text:
        return []
    return [f"  {line}" for line in text.rstrip().splitlines()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate repo-specific skill-pack integrity.",
        prog="python -m scripts.validate_skills",
    )
    parser.add_argument("--public", "--release", action="store_true", dest="public_mode")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    os.chdir(root)

    validation = Validation()
    skill_names, skill_failures = validate_skill_folders(root)
    validation.extend(skill_failures)
    validation.extend(validate_required_docs(root))
    validation.extend(
        unified_file_diff(
            root / "skills/current/setup-matt-pocock-skills/engineering-contract.md",
            root / "docs/agents/engineering-contract.md",
            root=root,
        )
    )
    validation.extend(validate_guide_refs(root, skill_names))
    validation.extend(validate_installed_skills(root, skill_names))
    validation.extend(validate_trailing_whitespace(root))
    if args.public_mode:
        validation.extend(validate_public_mode(root))
    validation.extend(validate_git_diff_check(root))

    if args.verbose:
        tracked = run_git(["ls-files"], cwd=root)
        if tracked.returncode == 0:
            print(f"Tracked files: {len([line for line in tracked.stdout.splitlines() if line])}")
        print(f"Skill folders: {len(skill_names)}")

    if validation.failures:
        for failure in validation.failures:
            print(f"- {failure}")
        print("Public readiness check failed." if args.public_mode else "Skill validation failed.")
        return 1

    print("Public readiness check passed." if args.public_mode else "Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
