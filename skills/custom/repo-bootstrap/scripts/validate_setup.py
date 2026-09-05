"""Validate the local setup configuration required by the custom skill pack."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import tomllib
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

PORTABLE_OWNER_MARKER = (
    "<!-- programming-agent-skills portable-contract-owner: 1 -->"
)
SETUP_FILE_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-file: engineering-contract\.md:[0-9a-f]{12} -->"
)

AGENT_POINTERS = (
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)
TRACKER_HEADINGS = (
    "Issue tracker: GitHub",
    "Issue tracker: GitLab",
    "Issue tracker: Local Markdown",
)
TRACKER_SECTIONS = ("Operations", "Representation", "Mutation read-back")
LABEL_ROLES = (
    "bug",
    "enhancement",
    "needs-triage",
    "needs-info",
    "ready-for-agent",
    "ready-for-human",
    "implemented",
    "wontfix",
)
GITHUB_RELATIONSHIP_MODES = (
    ("Parent / child mode", ("native-sub-issues", "parent-task-list")),
    ("Dependency mode", ("native-dependencies", "body-links")),
)
GITLAB_RELATIONSHIP_MODES = (
    ("Parent / child mode", ("native-links", "body-links")),
    ("Dependency mode", ("native-links", "body-links")),
)
PARALLEL_CONFIG = Path(".codex/config.toml")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Target repository root")
    parser.add_argument("--domain-owner", default="domain-modeling",
                        choices=("domain-modeling", "shape-work"),
                        help="Domain owner required by the selected source contract.")
    parser.add_argument(
        "--repository-owned-contract",
        action="store_true",
        help="Check contract structure without requiring a managed source marker.",
    )
    return parser.parse_args()


def read_required(root: Path, relative: str, failures: list[str]) -> str:
    path = root / relative
    if not path.is_file():
        failures.append(f"Missing required setup file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        failures.append(f"Cannot read required setup file {relative}: {error}")
        return ""


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


def visible_markdown(text: str) -> str:
    return re.sub(r"(?s)<!--.*?-->", "", unfenced_markdown(text))


def portable_owner_failures(agents: str) -> list[str]:
    if PORTABLE_OWNER_MARKER not in agents:
        return []
    return [
        "AGENTS.md still declares the portable engineering-contract owner; "
        "complete portable-fallback adoption through $repo-bootstrap."
    ]


def agents_commands_failures(agents: str) -> list[str]:
    if markdown_headings(agents, 2).count("Commands") == 1:
        return []
    return ["AGENTS.md must contain one unfenced ## Commands heading"]


def agent_pointer_failures(agents: str) -> list[str]:
    return [
        f"AGENTS.md is missing {pointer}"
        for pointer in AGENT_POINTERS
        if pointer not in visible_markdown(agents)
    ]


def relationship_mode_failures(
    tracker: str, provider: str, modes: tuple[tuple[str, tuple[str, ...]], ...]
) -> list[str]:
    if markdown_headings(tracker, 1) != [f"Issue tracker: {provider}"]:
        return []

    failures: list[str] = []
    for field, choices in modes:
        choice_pattern = "|".join(re.escape(choice) for choice in choices)
        if not re.search(
            rf"(?im)^\*\*{re.escape(field)}:\*\*\s*(?:{choice_pattern})"
            rf"\.?(?:\r?\n|\Z)",
            tracker,
        ):
            failures.append(
                "docs/agents/issue-tracker.md must set "
                f"{field} to one configured {provider} mode"
            )
    return failures


def tracker_configuration_failures(tracker: str) -> list[str]:
    failures: list[str] = []
    headings = markdown_headings(tracker, 1)
    if len(headings) != 1 or headings[0] not in TRACKER_HEADINGS:
        return [
            "docs/agents/issue-tracker.md must select GitHub, GitLab, "
            "or Local Markdown"
        ]

    sections = markdown_headings(tracker, 2)
    for section in TRACKER_SECTIONS:
        if sections.count(section) != 1:
            failures.append(
                f"docs/agents/issue-tracker.md must contain one ## {section} section"
            )

    if headings[0] != "Issue tracker: Local Markdown" and not re.search(
        r"(?im)^\*\*Close implemented items:\*\*\s*(?:yes|no)\.?(?:\r?\n|\Z)",
        tracker,
    ):
        failures.append(
            "docs/agents/issue-tracker.md must set Close implemented items to yes or no"
        )
    failures.extend(relationship_mode_failures(tracker, "GitHub", GITHUB_RELATIONSHIP_MODES))
    failures.extend(relationship_mode_failures(tracker, "GitLab", GITLAB_RELATIONSHIP_MODES))
    return failures


def label_configuration_failures(labels: str) -> list[str]:
    roles = {
        role
        for role, value in re.findall(
            r"(?m)^\| `([a-z0-9:-]+)` \| `([^`]+)` \|", visible_markdown(labels)
        )
        if value.strip()
    }
    return [
        f"docs/agents/triage-labels.md is missing the {role} role"
        for role in LABEL_ROLES
        if role not in roles
    ]


def domain_layout_failures(domain: str, *, domain_owner: str = "domain-modeling") -> list[str]:
    match = re.search(
        r"(?im)^\*\*Configured layout:\*\*\s*"
        r"(single-context|multi-context)\.?(?:\r?\n|\Z)",
        domain,
    )
    if match is None:
        return [
            "docs/agents/domain.md must set Configured layout to "
            "single-context or multi-context"
        ]

    failures: list[str] = []
    if markdown_headings(domain, 2).count("Route") != 1:
        failures.append("docs/agents/domain.md must contain one ## Route section")
    visible = visible_markdown(domain)
    if f"${domain_owner}" not in visible:
        failures.append(f"docs/agents/domain.md must point to ${domain_owner}")
    required_path = "CONTEXT.md" if match.group(1) == "single-context" else "CONTEXT-MAP.md"
    if required_path not in visible:
        failures.append(f"docs/agents/domain.md is missing {required_path}")
    if "docs/adr/" not in visible:
        failures.append("docs/agents/domain.md is missing docs/adr/")
    return failures


def engineering_contract_failures(
    text: str, relative: str, *, repository_owned: bool = False
) -> list[str]:
    failures: list[str] = []
    headings = [heading.casefold() for heading in markdown_headings(text, 1)]
    if headings != ["engineering contract"]:
        failures.append(f"{relative} must contain one top-level Engineering Contract heading")

    if not repository_owned:
        try:
            source = Path(__file__).resolve().parents[1] / "engineering-contract.md"
            digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
        except OSError as error:
            failures.append(f"Cannot read canonical engineering-contract.md: {error}")
            return failures

        expected_marker = (
            "<!-- programming-agent-skills setup-file: "
            f"engineering-contract.md:{digest} -->"
        )
        if SETUP_FILE_MARKER_RE.findall(unfenced_markdown(text)) != [expected_marker]:
            failures.append(
                f"{relative} must contain exactly one current source marker: "
                f"{expected_marker}"
            )
    visible = visible_markdown(text)
    sections = re.split(r"(?m)^##[ \t]+.+$", visible)[1:]
    sections = [re.sub(r"(?m)^#{3,6}[ \t]+.*$", "", section) for section in sections]
    if not sections or not any(section.strip() for section in sections):
        failures.append(
            f"{relative} must contain at least one non-empty level-two section"
        )
    return failures


def parallel_package() -> Path:
    return Path(__file__).resolve().parents[2] / "parallel-implement"


def parallel_support_failures(root: Path) -> list[str]:
    try:
        return inspect_parallel_support(root)
    except (OSError, UnicodeError) as error:
        return [f"Cannot inspect optional parallel support: {error}"]


def inspect_parallel_support(root: Path) -> list[str]:
    config_path = root / PARALLEL_CONFIG
    if not config_path.is_file():
        return []

    helper_path = parallel_package() / "scripts/lane_worktree.py"
    if not helper_path.is_file():
        return ["Parallel implementation support requires the installed canonical package"]

    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        return [f".codex/config.toml is invalid: {error}"]

    failures: list[str] = []
    if config.get("default_permissions") != "project-lanes":
        return []
    permissions = config.get("permissions")
    profile = permissions.get("project-lanes") if isinstance(permissions, dict) else None
    if not isinstance(profile, dict) or profile.get("extends") != ":workspace":
        failures.append("project-lanes permissions must extend :workspace")
    roots = profile.get("workspace_roots") if isinstance(profile, dict) else None
    if not isinstance(roots, dict):
        failures.append("project-lanes permissions must declare workspace_roots")
        return failures

    candidates = [
        Path(raw_path).resolve()
        for raw_path, enabled in roots.items()
        if isinstance(raw_path, str)
        and enabled is True
        and Path(raw_path).name.lower() == "wt"
    ]
    if len(candidates) != 1:
        failures.append("project-lanes permissions must contain one parallel wt root")
        return failures

    try:
        candidates[0].relative_to(root.resolve())
    except ValueError:
        pass
    else:
        failures.append("parallel lane root must be outside the repository")
    return failures


def run_git(root: Path, arguments: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, UnicodeError):
        return None


def check_ignore(root: Path, probe: str) -> tuple[bool | None, str]:
    result = run_git(root, ["check-ignore", "-q", "--no-index", probe])
    if result is None:
        return None, "Cannot check Git ignore state"
    if result.returncode == 0:
        return True, ""
    if result.returncode == 1:
        return False, ""
    return None, "Git could not check ignore state"


def git_root_failures(root: Path) -> list[str]:
    result = run_git(root, ["rev-parse", "--show-toplevel"])
    if result is None:
        return ["Cannot find the Git repository root"]
    if result.returncode != 0:
        return ["Target is not a Git repository"]
    try:
        observed_root = Path(result.stdout.strip()).resolve()
    except OSError as error:
        return [f"Cannot resolve the Git repository root: {error}"]
    if observed_root != root:
        return ["Target must be the Git repository root"]
    return []


def validate_setup(root: Path, *, repository_owned_contract: bool = False,
                   domain_owner: str = "domain-modeling") -> list[str]:
    failures = git_root_failures(root)
    if not failures:
        failures.extend(parallel_support_failures(root))

    texts = {
        relative: read_required(root, relative, failures) for relative in REQUIRED_FILES
    }

    agents = texts["AGENTS.md"]
    if agents:
        failures.extend(portable_owner_failures(agents))
        failures.extend(agents_commands_failures(agents))
        failures.extend(agent_pointer_failures(agents))

    tracker = texts["docs/agents/issue-tracker.md"]
    if tracker:
        failures.extend(tracker_configuration_failures(tracker))

    labels = texts["docs/agents/triage-labels.md"]
    if labels:
        failures.extend(label_configuration_failures(labels))

    domain = texts["docs/agents/domain.md"]
    if domain:
        failures.extend(domain_layout_failures(domain, domain_owner=domain_owner))

    contract = texts["docs/agents/engineering-contract.md"]
    if contract:
        failures.extend(
            engineering_contract_failures(
                contract, "docs/agents/engineering-contract.md",
                repository_owned=repository_owned_contract,
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

    if markdown_headings(tracker, 1) == ["Issue tracker: Local Markdown"]:
        ignored, error = check_ignore(root, ".scratch/setup-validation-probe")
        if ignored is None:
            failures.append(error)
        elif ignored:
            failures.append(".scratch/ is ignored; durable local state must remain trackable")

    return failures


def main() -> int:
    args = parse_args()
    try:
        root = Path(args.repo).resolve()
    except OSError as error:
        print(f"Setup surface is incomplete:\n- Cannot resolve repository root: {error}")
        return 1

    failures = validate_setup(root, repository_owned_contract=args.repository_owned_contract,
                              domain_owner=args.domain_owner)
    if failures:
        print("Setup surface is incomplete:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Setup surface is structurally valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
