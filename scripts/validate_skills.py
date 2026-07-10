"""Validate the repository-owned contracts of the programming-agent skill pack."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SKILL_ROOTS = ("skills/custom", "skills/experimental", "skills/extra")
CUSTOM_SKILL_ROOT = "skills/custom"
GLOBAL_AGENTS_TEMPLATE = "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md"
INSTALLED_MANIFEST = ".programming-agent-skills-manifest.json"
REQUIRED_AGENT_DOCS = ("AGENTS_PORTABLE_FALLBACK.md", GLOBAL_AGENTS_TEMPLATE)
REQUIRED_REPO_FILES = ("README.md", "scripts/install_skills.py")
GLOBAL_AGENTS_SKILLS = frozenset(("ask-matt", "setup-matt-pocock-skills"))
GLOBAL_AGENTS_TOKENS = (
    "# Global Codex Instructions",
    "## Skill Pack Bootstrap",
    "Repo-local `AGENTS.md` primes.",
    "**Route:**",
    "**Setup:**",
    "**Boundary:**",
)
GLOBAL_AGENTS_FORBIDDEN_TOKENS = ("## Shell Search Safety", "rg -F --")
REQUIRED_SETUP_DOCS = (
    "AGENTS.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
    "docs/plans/README.md",
    "skills/custom/setup-matt-pocock-skills/engineering-contract.md",
)
PUBLISHED_MARKDOWN_ROOTS = (
    "skills",
    "docs/books",
    "docs/agents",
    "docs/plans",
    "docs/language",
    "docs/research",
    "docs/synthesis",
    "docs/validation",
)
LOCAL_IDENTIFIER_RE = re.compile(
    r"DESKTOP-|S-1-5-21|[A-Z]:[\\/]|/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|"
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|"
    r"api[_-]?key[ \t]*[:=]|secret[ \t]*[:=]|token[ \t]*[:=]|"
    r"password[ \t]*[:=]|BEGIN (RSA|OPENSSH|PRIVATE)"
)
RESOURCE_REF_RE = re.compile(r"`([^`]+)`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
FRONTMATTER_FIELD_RE = re.compile(r"(?m)^([a-zA-Z0-9_-]+):\s*(.+?)\s*$")
TRAILING_WHITESPACE_RE = re.compile(r"[ \t]$")
ACTIVE_SURFACE_FILES = (
    "README.md",
    "AGENTS.md",
    "CONTEXT.md",
    GLOBAL_AGENTS_TEMPLATE,
    "docs/agents/engineering-contract.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/synthesis/skill-context-relationships.md",
)
STALE_ACTIVE_TOKENS = (
    "AGENTS_SKILL_PACK_GUIDE",
    "$to-issues",
    "$to-prd",
    "skills/current",
    "skills/matt-pocock",
)


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


def custom_skill_dirs(root: Path) -> list[Path]:
    skill_root = root / CUSTOM_SKILL_ROOT
    if not skill_root.is_dir():
        return []
    return sorted(path for path in skill_root.iterdir() if path.is_dir())


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def skill_frontmatter(skill_file: Path) -> dict[str, str] | None:
    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return None
    return {
        key: unquote_yaml_scalar(value)
        for key, value in FRONTMATTER_FIELD_RE.findall(match.group(1))
    }


def skill_resource_references(skill_file: Path) -> list[str]:
    references: set[str] = set()
    text = skill_file.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK_RE.finditer(text):
        token = match.group(1).strip().split("#", 1)[0]
        if (
            token
            and token != "url-or-path"
            and not token.startswith(("http://", "https://", "mailto:", "#"))
            and "<" not in token
            and ">" not in token
        ):
            references.add(token)
    for match in RESOURCE_REF_RE.finditer(text):
        token = match.group(1)
        if re.match(r"^(templates|references|scripts|examples)/[^`\s]+$", token):
            references.add(token)
    return sorted(references)


def validate_skill_policy(skill_dir: Path) -> list[str]:
    policy_file = skill_dir / "agents/openai.yaml"
    if not policy_file.is_file():
        return [f"Skill missing invocation policy: {skill_dir.name}/agents/openai.yaml"]
    values = re.findall(
        r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$",
        policy_file.read_text(encoding="utf-8"),
    )
    if len(values) != 1:
        return [
            "Skill invocation policy must set allow_implicit_invocation exactly once: "
            f"{policy_file.as_posix()}"
        ]
    return []


def validate_skill_folders(root: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    skill_names: list[str] = []

    if not (root / "skills").is_dir():
        return [], ["Missing skills/ directory."]

    skill_dirs = iter_skill_dirs(root)
    if not skill_dirs:
        failures.append("No skill directories found under skills/.")
    duplicate_names = {
        name
        for name in {path.name for path in skill_dirs}
        if sum(path.name == name for path in skill_dirs) > 1
    }
    for name in sorted(duplicate_names):
        locations = ", ".join(path.as_posix() for path in skill_dirs if path.name == name)
        failures.append(f"Duplicate skill name across roots: {name}: {locations}")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        skill_names.append(skill_dir.name)
        if not skill_file.is_file():
            failures.append(f"Skill folder missing SKILL.md: {skill_dir.name}")
            continue

        frontmatter = skill_frontmatter(skill_file)
        if frontmatter is None:
            failures.append(f"Skill frontmatter is missing or malformed: {skill_file.as_posix()}")
        else:
            name = frontmatter.get("name", "")
            description = frontmatter.get("description", "")
            if name != skill_dir.name:
                failures.append(
                    f"Skill name must match its directory: {skill_file.as_posix()} -> {name!r}"
                )
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
                failures.append(f"Skill name is invalid: {skill_file.as_posix()} -> {name!r}")
            if not description:
                failures.append(f"Skill description is missing: {skill_file.as_posix()}")

        failures.extend(validate_skill_policy(skill_dir))

        for resource_ref in skill_resource_references(skill_file):
            resource_path = (skill_dir / resource_ref).resolve()
            skills_root = (root / "skills").resolve()
            if not resource_path.is_relative_to(skills_root):
                failures.append(
                    "Skill resource reference must stay inside skills/: "
                    f"{skill_file.as_posix()} -> {resource_ref}"
                )
                continue
            if not resource_path.exists():
                failures.append(
                    "Skill resource reference is missing: "
                    f"{skill_file.as_posix()} -> {resource_ref}"
                )

    return sorted(skill_names), failures


def validate_active_surfaces(root: Path) -> list[str]:
    failures: list[str] = []
    paths = {root / relative for relative in ACTIVE_SURFACE_FILES}
    custom_root = root / CUSTOM_SKILL_ROOT
    if custom_root.is_dir():
        paths.update(custom_root.rglob("*.md"))
        paths.update(custom_root.rglob("*.yaml"))
    for path in sorted(paths):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for token in STALE_ACTIVE_TOKENS:
            if token in text:
                failures.append(f"Active surface contains stale token: {relative} -> {token}")
    return failures


def validate_required_docs(root: Path) -> list[str]:
    failures: list[str] = []
    for file in REQUIRED_REPO_FILES:
        if not (root / file).is_file():
            failures.append(f"Missing required repository file: {file}")
    for doc in REQUIRED_AGENT_DOCS:
        if not (root / doc).is_file():
            failures.append(f"Missing required agent instruction document: {doc}")
    for doc in REQUIRED_SETUP_DOCS:
        if not (root / doc).is_file():
            failures.append(f"Missing required setup surface document: {doc}")
    return failures


def validate_setup_surface(root: Path) -> list[str]:
    validator = root / "skills/custom/setup-matt-pocock-skills/scripts/validate_setup.py"
    if not validator.is_file():
        return [f"Missing setup-surface validator: {validator.relative_to(root).as_posix()}"]
    result = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return []
    output = (result.stdout + result.stderr).strip()
    return ["Repo setup surface is invalid:", *indent_lines(output)]


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


def global_agents_template_skill_references(root: Path) -> list[str]:
    template = root / GLOBAL_AGENTS_TEMPLATE
    if not template.is_file():
        return []
    refs: set[str] = set()
    for match in RESOURCE_REF_RE.finditer(template.read_text(encoding="utf-8")):
        token = match.group(1).removeprefix("$")
        if re.match(r"^[a-z0-9][a-z0-9-]*$", token):
            refs.add(token)
    return sorted(refs)


def validate_global_agents_template(root: Path, skill_names: list[str]) -> list[str]:
    names = set(skill_names)
    failures = []
    refs = set(global_agents_template_skill_references(root))
    for skill_name in sorted(refs):
        if skill_name not in names:
            failures.append(
                f"{GLOBAL_AGENTS_TEMPLATE} references missing skill: {skill_name}"
            )
    for skill_name in sorted(GLOBAL_AGENTS_SKILLS - refs):
        failures.append(
            f"{GLOBAL_AGENTS_TEMPLATE} is missing bootstrap skill: {skill_name}"
        )
    for skill_name in sorted(refs - GLOBAL_AGENTS_SKILLS):
        failures.append(
            f"{GLOBAL_AGENTS_TEMPLATE} must leave route maps to ask-matt; "
            f"unexpected skill reference: {skill_name}"
        )

    template = root / GLOBAL_AGENTS_TEMPLATE
    if template.is_file():
        text = template.read_text(encoding="utf-8")
        for token in GLOBAL_AGENTS_TOKENS:
            if token not in text:
                failures.append(f"{GLOBAL_AGENTS_TEMPLATE} is missing {token}")
        for token in GLOBAL_AGENTS_FORBIDDEN_TOKENS:
            if token in text:
                failures.append(
                    f"{GLOBAL_AGENTS_TEMPLATE} must leave environment-specific "
                    f"instructions local; found {token}"
                )
    return failures


def repo_skill_dir(root: Path, skill_name: str) -> Path | None:
    for relative_root in SKILL_ROOTS:
        candidate = root / relative_root / skill_name
        if candidate.is_dir():
            return candidate
    return None


def compare_dirs(expected: Path, actual: Path) -> list[str]:
    failures: list[str] = []
    expected_files = {
        path.relative_to(expected).as_posix(): path
        for path in expected.rglob("*")
        if path.is_file() and not path.name.endswith(":Zone.Identifier")
    }
    actual_files = {
        path.relative_to(actual).as_posix(): path
        for path in actual.rglob("*")
        if path.is_file() and not path.name.endswith(":Zone.Identifier")
    }
    for name in sorted(expected_files.keys() - actual_files.keys()):
        failures.append(f"Only in repo: {expected_files[name]}")
    for name in sorted(actual_files.keys() - expected_files.keys()):
        failures.append(f"Only in installed copy: {actual_files[name]}")
    for name in sorted(expected_files.keys() & actual_files.keys()):
        if expected_files[name].read_bytes() != actual_files[name].read_bytes():
            failures.append(f"Files differ: {expected_files[name]} {actual_files[name]}")
    return failures


def read_installed_manifest(installed_root: Path) -> tuple[set[str], list[str]]:
    manifest_path = installed_root / INSTALLED_MANIFEST
    if not manifest_path.is_file():
        return set(), []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return set(), [f"Installed skill manifest is invalid: {manifest_path}: {error}"]
    names = payload.get("skills") if isinstance(payload, dict) else None
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        return set(), [f"Installed skill manifest must contain a string list named skills: {manifest_path}"]
    return set(names), []


def validate_installed_skills(
    root: Path,
    skill_names: list[str],
    installed_skills_dir: str,
    require_all_installed: bool,
) -> list[str]:
    failures: list[str] = []
    if not installed_skills_dir:
        if require_all_installed:
            return ["Installed skill verification requires --installed-root or AGENT_SKILLS_DIR."]
        return failures

    installed_root = Path(installed_skills_dir).expanduser()
    if not installed_root.is_dir():
        return [f"AGENT_SKILLS_DIR does not exist or is not a directory: {installed_root}"]

    names = set(skill_names)
    manifest_exists = (installed_root / INSTALLED_MANIFEST).is_file()
    managed_names, manifest_failures = read_installed_manifest(installed_root)
    failures.extend(manifest_failures)
    for stale_name in sorted(managed_names - names):
        failures.append(f"Installed manifest contains retired managed skill: {stale_name}")
    for unmanaged_name in sorted(names - managed_names):
        if manifest_exists:
            failures.append(f"Installed manifest is missing active managed skill: {unmanaged_name}")

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
    for name in ("README.md", "AGENTS.md", "AGENTS_PORTABLE_FALLBACK.md", GLOBAL_AGENTS_TEMPLATE):
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
    failures: list[str] = []
    for label, args in (
        ("working tree", ["diff", "--check"]),
        ("staged diff", ["diff", "--cached", "--check"]),
    ):
        diff_check = run_git(args, cwd=root)
        output = (diff_check.stdout + diff_check.stderr).strip()
        if diff_check.returncode != 0 or output:
            failures.append(f"git diff --check failed for {label}:")
            failures.extend(indent_lines(output))
    return failures


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
    parser.add_argument(
        "--installed-root",
        default=os.environ.get("AGENT_SKILLS_DIR", ""),
        help="Shared installed skills directory to compare against skills/custom.",
    )
    parser.add_argument(
        "--require-installed",
        action="store_true",
        default=os.environ.get("AGENT_SKILLS_REQUIRE_ALL", "0") == "1",
        help="Require every custom skill to exist under --installed-root.",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    os.chdir(root)

    validation = Validation()
    skill_names, skill_failures = validate_skill_folders(root)
    custom_skill_names = [path.name for path in custom_skill_dirs(root)]
    validation.extend(skill_failures)
    validation.extend(validate_required_docs(root))
    validation.extend(validate_active_surfaces(root))
    validation.extend(validate_setup_surface(root))
    validation.extend(
        unified_file_diff(
            root / "skills/custom/setup-matt-pocock-skills/engineering-contract.md",
            root / "docs/agents/engineering-contract.md",
            root=root,
        )
    )
    validation.extend(validate_global_agents_template(root, custom_skill_names))
    validation.extend(
        validate_installed_skills(
            root,
            custom_skill_names,
            args.installed_root,
            args.require_installed,
        )
    )
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
