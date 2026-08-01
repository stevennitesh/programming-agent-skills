"""Validate the local setup surface required by the custom skill pack."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

SETUP_SCHEMA_TOKEN = "<!-- programming-agent-skills setup-schema: 1:8113e40631ff -->"
ENGINEERING_PRIMER_TOKEN = (
    "Explore imaginatively. Converge under proof. Simplify ruthlessly."
)
SETUP_SCHEMA_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-schema: \d+:[0-9a-f]{12} -->"
)

PORTABLE_OWNER_TOKENS = (
    "# Portable Engineering Contract",
    "This contract owns engineering taste, gates, and completion.",
)

PORTABLE_SECTION_HEADINGS = (
    "## North Star",
    "## Engineering Taste",
    "## Working Loop",
    "## Hard Gates",
    "## Shape Before Build",
    "## Implementation Taste",
    "## Review And Report",
)

PORTABLE_SECTION_SIGNATURES = (
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
        "## Review And Report",
        "Review every nontrivial diff from a fixed point on separate axes:",
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

CONTRACT_LITERAL_TOKENS = (
    ENGINEERING_PRIMER_TOKEN,
    "not a workflow, checklist, review gate",
    "Skills own procedures, checks, stopping",
    "## How To Read This Contract",
    "**Must** marks a correctness, safety, integrity, or honesty floor.",
    "**Prefer** marks the default engineering choice.",
    "**Method** names a practice triggered by a stated condition.",
    "## Shared Concepts",
    "**Bounded slice:**",
    "**Commitment boundary:**",
    "**Proof seam:**",
    "**Proof lane:**",
    "**Change closure:**",
    "**Residual risk:**",
    "## Keep Faith With The Work",
    "### Preserve Commitments And Domain Truth",
    "### Make Correctness Robust",
    "### Respect Trust And Data Boundaries",
    "### Keep Evidence Honest",
    "### Practice Stewardship",
    "## Shape Code For Understanding",
    "### Deep Simplicity",
    "### Local Readability",
    "### Fit Before Novelty",
    "### Build Only What Is Needed",
    "### Keep Tests Lean And Meaningful",
    "YAGNI",
    "DRY",
    "## Methods When The Condition Applies",
    "### Reason Across State Boundaries",
    "### Use A Negative Control",
    "### Close Displaced Paths",
    "### Measure Consequential Claims",
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


def portable_owner_failures(agents: str) -> list[str]:
    portable_section_remains = any(
        signature in (markdown_section(agents, heading) or "")
        for heading, signature in PORTABLE_SECTION_SIGNATURES
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

    failures.extend(git_root_failures(root))

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
    require_tokens(
        contract,
        "docs/agents/engineering-contract.md",
        CONTRACT_LITERAL_TOKENS,
        failures,
    )
    require_section_tokens(
        contract,
        "docs/agents/engineering-contract.md",
        (
            (
                "## How To Read This Contract",
                (
                    "Methods are not",
                    "responsible task or skill owns the procedure and evidence",
                    "No generic rule overrides",
                ),
            ),
            (
                "## Keep Faith With The Work",
                (
                    "operational definition or exact authoritative owner",
                    "not merely a successful happy path",
                    "Validate untrusted or contract-sensitive input",
                    "A focused check",
                    "Preserve unrelated behavior, work, and durable decisions",
                ),
            ),
            (
                "## Shape Code For Understanding",
                (
                    "supported variation, repeated policy, or a real external",
                    "Apply YAGNI",
                    "Apply DRY to shared meaning and policy",
                    "Consolidation must preserve coverage and diagnostic clarity",
                    "Test count is not a goal",
                ),
            ),
            (
                "## Methods When The Condition Applies",
                (
                    "not a blind Cartesian",
                    "controlled violation fails for the intended reason",
                    "Retain an older path only for a supported",
                    "measure before claiming improvement",
                ),
            ),
        ),
        failures,
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
