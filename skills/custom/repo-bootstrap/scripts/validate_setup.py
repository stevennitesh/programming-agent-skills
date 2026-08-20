"""Validate the local setup surface required by the custom skill pack."""

from __future__ import annotations

import argparse
import errno
import hashlib
import re
import subprocess
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TypeAlias


REQUIRED_FILES = (
    "AGENTS.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

SETUP_SCHEMA_TOKEN = "<!-- programming-agent-skills setup-schema: 1:d8b501d28404 -->"
SETUP_SCHEMA_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-schema: \d+:[0-9a-f]{12} -->"
)
SETUP_FILE_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-file: engineering-contract\.md:[0-9a-f]{12} -->"
)

PORTABLE_OWNER_MARKER = (
    "<!-- programming-agent-skills portable-contract-owner: 1 -->"
)

AGENT_POINTERS = (
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

DOMAIN_TOKENS = (
    "**single-context:**",
    "**multi-context:**",
    "CONTEXT-MAP.md",
    "<context-root>/docs/adr/",
    "$domain-modeling",
)

WORK_ITEM_TOKENS = (
    "## Operations",
    "## Work-item representation",
    "**Packet:**",
    "**Parent / child:**",
    "**Blocking:**",
    "**Ready query:**",
    "**Claim:**",
    "**Closeout:**",
    "## Mutation read-back",
)
WAYFINDER_TOKENS = (
    "Participation:",
    "Resolution owner:",
    "Resolver:",
    "Expected return:",
    "Mutation boundary:",
    "Re-entry owner: $wayfinder",
    "Claim token:",
    "Claimed at:",
)

HOSTED_WAYFINDER_TOKENS = (
    "docs/agents/triage-labels.md",
    "Blocked: waiting - <gist>",
)
LOCAL_WAYFINDER_TOKENS = (
    "Status: Pending | In Progress | Resolved | Blocked | Waiting | Out Of Scope",
    "waiting return records",
)

GITHUB_RELATIONSHIP_MODES = (
    (
        "Parent / child mode",
        ("native-sub-issues", "parent-task-list"),
    ),
    (
        "Dependency mode",
        ("native-dependencies", "body-links"),
    ),
)

LABEL_TOKENS = (
    "`bug`",
    "`enhancement`",
    "`needs-triage`",
    "`needs-info`",
    "`ready-for-agent`",
    "`ready-for-human`",
    "`implemented`",
    "`wontfix`",
    "`wayfinder:map`",
    "`wayfinder:research`",
    "`wayfinder:prototype`",
    "`wayfinder:diagnosis`",
    "`wayfinder:grilling`",
    "`wayfinder:questionnaire`",
    "`wayfinder:task`",
)

PARALLEL_CONFIG = Path(".codex/config.toml")
PARALLEL_AGENT = Path(".codex/agents/luna_max.toml")


class FailureKind(str, Enum):
    FILESYSTEM_IO = "filesystem-io"
    TEXT_DECODING = "text-decoding"
    GIT_UNAVAILABLE = "git-unavailable"
    GIT_INVOCATION = "git-invocation"
    GIT_COMMAND = "git-command"


@dataclass(frozen=True)
class ValidationFailure:
    kind: FailureKind
    operation: str
    path: str | None = None

    def render(self) -> str:
        context = f" for {self.path}" if self.path is not None else ""
        return f"[{self.kind.value}] {self.operation} failed{context}"


Failure: TypeAlias = str | ValidationFailure


def render_failure(failure: Failure) -> str:
    if isinstance(failure, ValidationFailure):
        return failure.render()
    return failure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Target repository root")
    return parser.parse_args()


def read_required(root: Path, relative: str, failures: list[Failure]) -> str:
    path = root / relative
    try:
        if not path.is_file():
            failures.append(f"Missing required setup file: {relative}")
            return ""
        return path.read_text(encoding="utf-8")
    except UnicodeError:
        failures.append(
            ValidationFailure(FailureKind.TEXT_DECODING, "decode setup file", relative)
        )
        return ""
    except OSError:
        failures.append(
            ValidationFailure(FailureKind.FILESYSTEM_IO, "read setup file", relative)
        )
        return ""


def require_tokens(
    text: str, relative: str, tokens: tuple[str, ...], failures: list[str]
) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{relative} is missing {token}")


def wayfinder_contract_failures(text: str, relative: str) -> list[str]:
    failures: list[str] = []
    provider_tokens = (
        LOCAL_WAYFINDER_TOKENS
        if "issue tracker: local markdown" in text.lower()
        else HOSTED_WAYFINDER_TOKENS
    )
    require_section_tokens(
        text,
        relative,
        (("## Wayfinding representation", WAYFINDER_TOKENS + provider_tokens),),
        failures,
    )
    return failures


def domain_contract_failures(text: str, relative: str) -> list[str]:
    failures: list[str] = []
    require_tokens(text, relative, DOMAIN_TOKENS, failures)
    return failures


def require_section_tokens(
    text: str,
    relative: str,
    requirements: tuple[tuple[str, tuple[str, ...]], ...],
    failures: list[str],
) -> None:
    for heading, tokens in requirements:
        section = markdown_section(text, heading, include_fenced_content=False)
        for token in tokens:
            if section is None or token not in section:
                failures.append(f"{relative} section {heading} is missing {token}")


def markdown_section(
    text: str,
    heading: str,
    *,
    include_fenced_content: bool = True,
) -> str | None:
    lines = text.splitlines(keepends=True)
    outside_fence: list[bool] = []
    fence_char = ""
    fence_length = 0

    for line in lines:
        outside_fence.append(not fence_char)
        stripped = line.rstrip("\r\n")
        if fence_char:
            if re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*",
                stripped,
            ):
                fence_char = ""
                fence_length = 0
            continue
        opening = re.match(r"[ \t]{0,3}(`{3,}|~{3,})", stripped)
        if opening:
            fence_char = opening.group(1)[0]
            fence_length = len(opening.group(1))

    matches = [
        index
        for index, line in enumerate(lines)
        if outside_fence[index] and line.rstrip().rstrip("\r\n") == heading
    ]
    if len(matches) != 1:
        return None

    start = matches[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if outside_fence[index] and re.match(r"^#{1,2}(?:[ \t]+|$)", lines[index]):
            end = index
            break
    section = "".join(
        line
        for index, line in enumerate(lines[start:end], start)
        if include_fenced_content or outside_fence[index]
    )
    return section


def markdown_headings(text: str, level: int) -> list[str]:
    headings: list[str] = []
    fence_char = ""
    fence_length = 0
    pattern = re.compile(rf"^{'#' * level}[ \t]+(.+?)[ \t]*$")

    for line in text.splitlines():
        stripped = line.rstrip()
        if fence_char:
            if re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*",
                stripped,
            ):
                fence_char = ""
                fence_length = 0
            continue
        opening = re.match(r"[ \t]{0,3}(`{3,}|~{3,})", stripped)
        if opening:
            fence_char = opening.group(1)[0]
            fence_length = len(opening.group(1))
            continue
        match = pattern.fullmatch(stripped)
        if match:
            headings.append(match.group(1))
    return headings


def unfenced_markdown(text: str) -> str:
    lines: list[str] = []
    fence_char = ""
    fence_length = 0

    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        if fence_char:
            if re.fullmatch(
                rf"[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*",
                stripped,
            ):
                fence_char = ""
                fence_length = 0
            continue
        opening = re.match(r"[ \t]{0,3}(`{3,}|~{3,})", stripped)
        if opening:
            fence_char = opening.group(1)[0]
            fence_length = len(opening.group(1))
            continue
        lines.append(line)
    return "".join(lines)


def engineering_contract_failures(text: str, relative: str) -> list[Failure]:
    failures: list[Failure] = []
    if markdown_headings(text, 1) != ["Engineering Contract"]:
        failures.append(f"{relative} must contain one top-level Engineering Contract heading")
    try:
        source = Path(__file__).resolve().parents[1] / "engineering-contract.md"
        digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    except OSError:
        failures.append(
            ValidationFailure(
                FailureKind.FILESYSTEM_IO,
                "read canonical setup file",
                "engineering-contract.md",
            )
        )
        return failures
    expected_marker = (
        "<!-- programming-agent-skills setup-file: "
        f"engineering-contract.md:{digest} -->"
    )
    if SETUP_FILE_MARKER_RE.findall(unfenced_markdown(text)) != [expected_marker]:
        failures.append(
            f"{relative} must contain exactly one current engineering-contract source marker: "
            f"{expected_marker}"
        )
    level_two = markdown_headings(text, 2)
    has_content = any(
        re.sub(
            r"(?s)<!--.*?-->",
            "",
            unfenced_markdown(markdown_section(text, f"## {heading}") or ""),
        ).strip()
        for heading in level_two
    )
    if not has_content:
        failures.append(
            f"{relative} must contain at least one unfenced level-two section "
            "with non-comment content"
        )
    return failures


def portable_owner_failures(agents: str) -> list[str]:
    if PORTABLE_OWNER_MARKER in agents:
        return [
            "AGENTS.md still declares the portable engineering-contract owner; "
            "complete portable-fallback adoption through $repo-bootstrap."
        ]
    return []


def setup_schema_marker_failures(agents: str) -> list[str]:
    if SETUP_SCHEMA_MARKER_RE.findall(unfenced_markdown(agents)) == [SETUP_SCHEMA_TOKEN]:
        return []
    return [
        "AGENTS.md must contain exactly one current programming-agent-skills "
        "setup-schema marker"
    ]


def agents_commands_failures(agents: str) -> list[str]:
    if markdown_section(agents, "## Commands") is not None:
        return []
    return ["AGENTS.md must contain one unfenced ## Commands heading"]


def github_relationship_mode_failures(tracker: str) -> list[str]:
    if "issue tracker: github" not in tracker.lower():
        return []

    failures: list[str] = []
    for field, choices in GITHUB_RELATIONSHIP_MODES:
        choice_pattern = "|".join(re.escape(choice) for choice in choices)
        if not re.search(
            rf"(?im)^\*\*{re.escape(field)}:\*\*\s*(?:{choice_pattern})"
            rf"\.?(?:\r?\n|\Z)",
            tracker,
        ):
            failures.append(
                "docs/agents/issue-tracker.md must set "
                f"{field} to one configured GitHub mode"
            )
    return failures


def parallel_package() -> Path:
    return Path(__file__).resolve().parents[2] / "parallel-implement"


def parallel_support_failures(root: Path) -> list[Failure]:
    try:
        return inspect_parallel_support(root)
    except UnicodeError:
        return [
            ValidationFailure(
                FailureKind.TEXT_DECODING,
                "decode parallel configuration",
                PARALLEL_CONFIG.as_posix(),
            )
        ]
    except OSError:
        return [
            ValidationFailure(
                FailureKind.FILESYSTEM_IO,
                "inspect parallel support",
                ".codex",
            )
        ]


def inspect_parallel_support(root: Path) -> list[Failure]:
    config_path = root / PARALLEL_CONFIG
    agent_path = root / PARALLEL_AGENT
    if not config_path.is_file() and not agent_path.is_file():
        return []

    failures: list[Failure] = []
    package = parallel_package()
    helper_path = package / "scripts/lane_worktree.py"
    template_path = package / "assets/luna_max.toml"
    if not helper_path.is_file() or not template_path.is_file():
        return ["Parallel implementation support requires the installed canonical package"]

    if not config_path.is_file():
        failures.append("Parallel implementation support is missing .codex/config.toml")
    if not agent_path.is_file():
        failures.append(
            "Parallel implementation support is missing .codex/agents/luna_max.toml"
        )
    elif agent_path.read_bytes() != template_path.read_bytes():
        failures.append(".codex/agents/luna_max.toml does not match the current template")
    if not config_path.is_file():
        return failures

    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        failures.append(f".codex/config.toml is invalid: {error}")
        return failures

    if config.get("default_permissions") != "project-lanes":
        failures.append(".codex/config.toml must select the project-lanes permission profile")
    permissions = config.get("permissions")
    profile = permissions.get("project-lanes") if isinstance(permissions, dict) else None
    if not isinstance(profile, dict) or profile.get("extends") != ":workspace":
        failures.append("project-lanes permissions must extend :workspace")
    roots = profile.get("workspace_roots") if isinstance(profile, dict) else None
    if not isinstance(roots, dict):
        failures.append("project-lanes permissions must declare workspace_roots")
        return failures

    candidates: list[Path] = []
    for raw_path, enabled in roots.items():
        if not isinstance(raw_path, str) or enabled is not True:
            continue
        lane_root = Path(raw_path).resolve()
        if lane_root.name.lower() == "wt":
            candidates.append(lane_root)
    if len(candidates) != 1:
        failures.append("project-lanes permissions must contain one parallel wt root")
        return failures

    lane_root = candidates[0]
    try:
        lane_root.relative_to(root.resolve())
    except ValueError:
        pass
    else:
        failures.append("parallel lane root must be outside the repository")
    return failures


def git_invocation_failure(operation: str, error: OSError) -> ValidationFailure:
    kind = (
        FailureKind.GIT_UNAVAILABLE
        if isinstance(error, FileNotFoundError) or error.errno == errno.ENOENT
        else FailureKind.GIT_INVOCATION
    )
    return ValidationFailure(kind, operation)


def run_git(root: Path, arguments: list[str], operation: str) -> tuple[
    subprocess.CompletedProcess[str] | None, ValidationFailure | None
]:
    try:
        return (
            subprocess.run(
                ["git", *arguments],
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            None,
        )
    except OSError as error:
        return None, git_invocation_failure(operation, error)
    except UnicodeError:
        return None, ValidationFailure(
            FailureKind.TEXT_DECODING,
            f"decode Git output from {operation}",
        )


def check_ignore(root: Path, probe: str) -> tuple[bool | None, Failure]:
    result, failure = run_git(
        root,
        ["check-ignore", "-q", "--no-index", probe],
        "check Git ignore state",
    )
    if failure is not None:
        return None, failure
    assert result is not None
    if result.returncode == 0:
        return True, ""
    if result.returncode == 1:
        return False, ""
    return None, ValidationFailure(FailureKind.GIT_COMMAND, "check Git ignore state")


def git_root_failures(root: Path) -> list[Failure]:
    result, failure = run_git(root, ["rev-parse", "--show-toplevel"], "find Git root")
    if failure is not None:
        return [failure]
    assert result is not None
    if result.returncode != 0:
        return ["Target is not a Git repository"]
    try:
        observed_root = Path(result.stdout.strip()).resolve()
    except OSError:
        return [ValidationFailure(FailureKind.FILESYSTEM_IO, "resolve Git root")]
    if observed_root != root:
        return ["Target must be the Git repository root"]
    return []


def main() -> int:
    raw_root = Path(parse_args().repo)
    try:
        root = raw_root.resolve()
    except OSError:
        failure = ValidationFailure(
            FailureKind.FILESYSTEM_IO,
            "resolve repository root",
            "repository root",
        )
        print("Setup surface is incomplete:")
        print(f"- {failure.render()}")
        return 1
    failures: list[Failure] = []

    repository_failures = git_root_failures(root)
    failures.extend(repository_failures)
    if not repository_failures:
        failures.extend(parallel_support_failures(root))

    texts = {
        relative: read_required(root, relative, failures) for relative in REQUIRED_FILES
    }

    agents = texts["AGENTS.md"]
    if agents:
        failures.extend(portable_owner_failures(agents))
        failures.extend(agents_commands_failures(agents))
        failures.extend(setup_schema_marker_failures(agents))
        require_tokens(agents, "AGENTS.md", AGENT_POINTERS, failures)

    tracker = texts["docs/agents/issue-tracker.md"]
    if tracker:
        require_tokens(tracker, "docs/agents/issue-tracker.md", WORK_ITEM_TOKENS, failures)
        failures.extend(
            wayfinder_contract_failures(tracker, "docs/agents/issue-tracker.md")
        )
        if "**comment or brief:**" not in tracker.lower():
            failures.append(
                "docs/agents/issue-tracker.md is missing Codex-ready brief transport"
            )
        local_tracker = "issue tracker: local markdown" in tracker.lower()
        if not local_tracker and not re.search(
            r"(?im)^\*\*Close implemented items:\*\*\s*(?:yes|no)\.?(?:\r?\n|\Z)",
            tracker,
        ):
            failures.append(
                "docs/agents/issue-tracker.md must set Close implemented items to yes or no"
            )
        failures.extend(github_relationship_mode_failures(tracker))
    else:
        local_tracker = False

    labels = texts["docs/agents/triage-labels.md"]
    require_tokens(labels, "docs/agents/triage-labels.md", LABEL_TOKENS, failures)

    domain = texts["docs/agents/domain.md"]
    if domain and not re.search(
        r"(?im)^\*\*Configured layout:\*\*\s*(?:single-context|multi-context)\.?(?:\r?\n|\Z)",
        domain,
    ):
        failures.append(
            "docs/agents/domain.md must set Configured layout to single-context or multi-context"
        )
    failures.extend(domain_contract_failures(domain, "docs/agents/domain.md"))

    contract = texts["docs/agents/engineering-contract.md"]
    failures.extend(
        engineering_contract_failures(
            contract, "docs/agents/engineering-contract.md"
        )
    )

    for relative, text in texts.items():
        if "<single-context | multi-context>" in text or "<yes | no>" in text:
            failures.append(f"{relative} still contains an unresolved setup placeholder")

    ignored, error = check_ignore(root, ".tmp/setup-validation-probe")
    if ignored is None:
        failures.append(error)
    elif not ignored:
        failures.append(".tmp/ contents are not ignored")

    ignored, error = check_ignore(root, ".scratch/setup-validation-probe")
    if ignored is None:
        failures.append(error)
    elif ignored:
        failures.append(".scratch/ is ignored; durable local state must remain trackable")

    if failures:
        print("Setup surface is incomplete:")
        for failure in failures:
            print(f"- {render_failure(failure)}")
        return 1

    print(f"Setup surface is valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
