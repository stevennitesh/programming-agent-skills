"""Validate the local setup surface required by the custom skill pack."""

from __future__ import annotations

import argparse
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

SETUP_SCHEMA_TOKEN = "<!-- programming-agent-skills setup-schema: 1:9caab4908050 -->"
ENGINEERING_PRIMER_TOKEN = (
    "Explore imaginatively. Converge under proof. Simplify ruthlessly."
)
SETUP_SCHEMA_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-schema: \d+:[0-9a-f]{12} -->"
)

PORTABLE_OWNER_TOKENS = (
    "# Portable Engineering Contract",
    "Use this as your global `AGENTS.md` when the skill pack is not installed.",
)

PORTABLE_LEGACY_SECTION_SIGNATURES = (
    (
        "## North Star",
        "Explore imaginatively. Converge under proof. Simplify ruthlessly.",
    ),
    ("## Engineering Taste", "**Imagination before commitment.**"),
    (
        "## Working Loop",
        "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock",
    ),
    ("## Hard Gates", "**No evidence, no done.**"),
    ("## Shape Before Build", "**Interview:** when intent is unsettled"),
    ("## Implementation Taste", "Order tracer-bullet slices by dependency."),
    (
        "## Check, Conditional Review, And Report",
        "Inspect every owned diff and final repository state.",
    ),
)

PORTABLE_CURRENT_SECTION_SIGNATURES = (
    (
        "## Authority And State",
        "Diagnosis, research, design, explanation, and review are read-only unless",
    ),
    ("## Ground Or Route", "If expected behavior, symptom, or cause is uncertain"),
    (
        "## Implement The Smallest Integrated Change",
        "Trace each acceptance commitment through the real caller or entry path",
    ),
    (
        "## Activate Heavier Methods Only When Triggered",
        "Use RED-GREEN-REFACTOR only when the user or repository explicitly requires",
    ),
    (
        "## Prove, Close, And Report",
        "Run the smallest fresh check capable of disproving each claim",
    ),
)

AGENT_POINTERS = (
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

DOMAIN_TOKENS = (
    "## Route",
    "## Preserve The Model",
    "**single-context:**",
    "**multi-context:**",
    "CONTEXT-MAP.md",
    "<context-root>/docs/adr/",
    "$domain-modeling",
)

DOMAIN_PROSE_TOKENS = (
    "Missing records are not setup gaps.",
    "setup neither creates nor recommends them.",
    "invariants",
    "Do not flatten different meanings across contexts.",
    "return the exact gap",
    "never silently override them",
    "decision owner",
)

CONTRACT_STRUCTURAL_TOKENS = (
    ENGINEERING_PRIMER_TOKEN,
    "# Engineering Contract",
)

CONTRACT_LEVEL_TWO_HEADINGS = (
    "Correctness And Evidence — Must",
    "Design Defaults — Prefer",
    "Methods When The Condition Applies",
)

CONTRACT_METHOD_HEADINGS = (
    "Reason Across State And Lifecycle Boundaries",
    "Use A Negative Control",
    "Prove Durable Artifacts Proportionally",
    "Measure Consequential Claims",
    "Invoke Heavier Owners Only From Their Trigger",
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
WORK_ITEM_PROSE_TOKENS = (
    "navigation metadata",
    "agent and human frontiers separately",
    "false-ready",
    "do not retry blindly",
    "unverified partial mutation",
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
    "exact return record",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Target repository root")
    return parser.parse_args()


def read_required(root: Path, relative: str, failures: list[str]) -> str:
    path = root / relative
    if not path.is_file():
        failures.append(f"Missing required setup file: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(
    text: str, relative: str, tokens: tuple[str, ...], failures: list[str]
) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{relative} is missing {token}")


def require_prose_tokens(
    text: str, relative: str, tokens: tuple[str, ...], failures: list[str]
) -> None:
    normalized_text = " ".join(text.split())
    for token in tokens:
        if " ".join(token.split()) not in normalized_text:
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
    require_prose_tokens(text, relative, DOMAIN_PROSE_TOKENS, failures)
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


def engineering_contract_failures(text: str, relative: str) -> list[str]:
    failures: list[str] = []
    require_tokens(text, relative, CONTRACT_STRUCTURAL_TOKENS, failures)
    if markdown_headings(text, 1) != ["Engineering Contract"]:
        failures.append(f"{relative} must contain one top-level Engineering Contract heading")
    if markdown_headings(text, 2) != list(CONTRACT_LEVEL_TWO_HEADINGS):
        failures.append(
            f"{relative} must contain the exact engineering-contract section outline"
        )
    if markdown_headings(text, 3) != list(CONTRACT_METHOD_HEADINGS):
        failures.append(
            f"{relative} must contain the exact condition-triggered method outline"
        )
    methods = markdown_section(text, "## Methods When The Condition Applies")
    if methods is None or markdown_headings(methods, 3) != list(
        CONTRACT_METHOD_HEADINGS
    ):
        failures.append(
            f"{relative} must own every condition-triggered method under its method section"
        )
    return failures


def portable_owner_failures(agents: str) -> list[str]:
    portable_section_remains = any(
        signature in (markdown_section(agents, heading) or "")
        for heading, signature in (
            PORTABLE_LEGACY_SECTION_SIGNATURES + PORTABLE_CURRENT_SECTION_SIGNATURES
        )
    )
    if any(token in agents for token in PORTABLE_OWNER_TOKENS) or portable_section_remains:
        return [
            "AGENTS.md still declares the portable engineering-contract owner; "
            "complete portable-fallback adoption through $repo-bootstrap."
        ]
    return []


def setup_schema_marker_failures(agents: str) -> list[str]:
    if SETUP_SCHEMA_MARKER_RE.findall(agents) == [SETUP_SCHEMA_TOKEN]:
        return []
    return [
        "AGENTS.md must contain exactly one current programming-agent-skills "
        "setup-schema marker"
    ]


def engineering_primer_failures(agents: str) -> list[str]:
    pattern = re.compile(
        rf"(?m)\A# Repository Instructions[ \t]*\r?\n"
        rf"(?:[ \t]*\r?\n)*{re.escape(SETUP_SCHEMA_TOKEN)}[ \t]*\r?\n"
        rf"(?:[ \t]*\r?\n)*{re.escape(ENGINEERING_PRIMER_TOKEN)}[ \t]*\r?\n"
        rf"(?:[ \t]*\r?\n)*## Commands[ \t]*$"
    )
    if pattern.search(agents):
        return []
    return [
        "AGENTS.md must place the engineering primer between the current "
        "setup-schema marker and ## Commands"
    ]


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


def parallel_support_failures(root: Path) -> list[str]:
    config_path = root / PARALLEL_CONFIG
    agent_path = root / PARALLEL_AGENT
    if not config_path.is_file() and not agent_path.is_file():
        return []

    failures: list[str] = []
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
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
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


def check_ignore(root: Path, probe: str) -> tuple[bool | None, str]:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--no-index", probe],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return True, ""
    if result.returncode == 1:
        return False, ""
    return None, result.stderr.strip() or "git check-ignore failed"


def git_root_failures(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        return [f"Git root check failed: {error}"]
    if result.returncode != 0:
        return ["Target is not a Git repository"]
    if Path(result.stdout.strip()).resolve() != root:
        return ["Target must be the Git repository root"]
    return []


def main() -> int:
    root = Path(parse_args().repo).resolve()
    failures: list[str] = []

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
        if not re.search(r"(?m)^## Commands\s*$", agents):
            failures.append("AGENTS.md is missing a ## Commands primer")
        failures.extend(setup_schema_marker_failures(agents))
        failures.extend(engineering_primer_failures(agents))
        require_tokens(agents, "AGENTS.md", AGENT_POINTERS, failures)
        if not re.search(
            r"(?im)^(?:[-*]\s*)?(?:before|for)\s+nontrivial coding[^\n]*"
            r"docs/agents/engineering-contract\.md[^\n]*$",
            agents,
        ):
            failures.append(
                "AGENTS.md must tell agents to read the engineering contract before nontrivial coding"
            )

    tracker = texts["docs/agents/issue-tracker.md"]
    if tracker:
        require_tokens(tracker, "docs/agents/issue-tracker.md", WORK_ITEM_TOKENS, failures)
        require_prose_tokens(
            tracker,
            "docs/agents/issue-tracker.md",
            WORK_ITEM_PROSE_TOKENS,
            failures,
        )
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
            print(f"- {failure}")
        return 1

    print(f"Setup surface is valid: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
