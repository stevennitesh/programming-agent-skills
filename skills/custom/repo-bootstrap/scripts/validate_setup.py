"""Validate the local setup surface required by the custom skill pack."""

from __future__ import annotations

import argparse
import hashlib
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

SETUP_SCHEMA_TOKEN = "<!-- programming-agent-skills setup-schema: 1:57bffed703dc -->"
ENGINEERING_PRIMER_TOKEN = (
    "Explore imaginatively. Converge under proof. Simplify ruthlessly."
)
SETUP_SCHEMA_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-schema: \d+:[0-9a-f]{12} -->"
)
SETUP_FILE_MARKER_RE = re.compile(
    r"<!-- programming-agent-skills setup-file: [a-z0-9./-]+:[0-9a-f]{12} -->"
)

SETUP_FILE_SOURCES = {
    "docs/agents/triage-labels.md": "triage-labels.md",
    "docs/agents/domain.md": "domain.md",
    "docs/agents/engineering-contract.md": "engineering-contract.md",
}

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

CONTRACT_LITERAL_TOKENS = (
    ENGINEERING_PRIMER_TOKEN,
    "## Engineering Taste",
    "**Imagination before commitment.**",
    "**Experiments over speculation.**",
    "**Semantic proof over plausible output.**",
    "**Deep simplicity.**",
    "**Stewardship.**",
    "**Source trace:**",
    "**Bounded slice:**",
    "**Commitment boundary:**",
    "**Load-bearing internal:**",
    "**Semantic correctness:**",
    "**Semantic proof:**",
    "**State-boundary matrix.**",
    "**Proof seam:**",
    "**Proof lane:**",
    "**Evidence:**",
    "**Tracer bullet:**",
    "**Fixed point:**",
    "**Review snapshot:**",
    "**staged worker**",
    "**lane worker**",
    "**Spec / Standards:**",
    "**Residual risk:**",
    "Explore -> Choose -> Prove -> Expand -> Simplify -> Lock",
    ".tmp/",
    ".scratch/",
    "## Lock",
)

WORK_ITEM_TOKENS = (
    "## Work-item operations",
    "**Packet**",
    "**Ready-for-agent contract**",
    "**Mutation read-back**",
    "**Parent / child**",
    "**Blocking**",
    "**Ready query**",
    "**Claim**",
    "**Release**",
    "**Closeout**",
)

WAYFINDER_TOKENS = (
    "## Wayfinding operations",
    "Participation: HITL | AFK",
    "**Frontier query**",
    "**Claim**",
    "Claim token:",
    "Claimed at:",
    "codex/<lowercase UUIDv4>",
    "<YYYY-MM-DDTHH:MM:SSZ>",
    "Maintain claims the map",
    "never reuse it across invocations",
    "Elapsed time alone never makes a claim stale.",
    "explicit user approval",
    "**Release**",
    "**Resolve**",
    "**Block**",
    "**Out of scope**",
    "**Complete map**",
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
    "`wayfinder:grilling`",
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


def require_section_tokens(
    text: str,
    relative: str,
    requirements: tuple[tuple[str, tuple[str, ...]], ...],
    failures: list[str],
) -> None:
    for heading, tokens in requirements:
        for token in tokens:
            if not markdown_section_contains(text, heading, token):
                failures.append(f"{relative} section {heading} is missing {token}")


def markdown_section_contains(text: str, heading: str, signature: str) -> bool:
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}[ \t]*(?:\r?\n|\Z)"
        r"(.*?)(?=^#{1,2}(?:[ \t]+|$)|\Z)"
    )
    return any(signature in match.group(1) for match in pattern.finditer(text))


def portable_owner_failures(agents: str) -> list[str]:
    portable_section_remains = any(
        markdown_section_contains(agents, heading, signature)
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


def tracker_source(text: str) -> str | None:
    lowered = text.lower()
    for provider in ("github", "gitlab", "local markdown"):
        if re.search(rf"(?m)^#\s+issue tracker:\s*{re.escape(provider)}\s*$", lowered):
            suffix = "local" if provider == "local markdown" else provider
            return f"issue-tracker-{suffix}.md"
    return None


def expected_setup_file_marker(relative: str, text: str) -> str:
    source = (
        tracker_source(text)
        if relative == "docs/agents/issue-tracker.md"
        else SETUP_FILE_SOURCES.get(relative)
    )
    if source is None:
        source = "custom-tracker-interface"
        digest = hashlib.sha256(SETUP_SCHEMA_TOKEN.encode()).hexdigest()[:12]
    else:
        template = Path(__file__).resolve().parents[1] / source
        if not template.is_file():
            raise ValueError(f"Missing setup source template: {source}")
        digest = hashlib.sha256(template.read_bytes()).hexdigest()[:12]
    return f"<!-- programming-agent-skills setup-file: {source}:{digest} -->"


def setup_file_marker_failures(
    text: str, relative: str, expected: str
) -> list[str]:
    if SETUP_FILE_MARKER_RE.findall(text) == [expected]:
        return []
    return [
        f"{relative} must contain exactly one current setup-file source marker: "
        f"{expected}"
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

    for relative in REQUIRED_FILES[1:]:
        text = texts[relative]
        if text:
            expected = expected_setup_file_marker(relative, text)
            failures.extend(setup_file_marker_failures(text, relative, expected))

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
        require_tokens(tracker, "docs/agents/issue-tracker.md", WAYFINDER_TOKENS, failures)
        if "post a codex-ready brief" not in tracker.lower():
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
            ("## Tight Engineering Spine", ("**Expand:**", "bounded slice")),
            ("## Proof Discipline", ("command authority",)),
            ("## Work State And Workers", ("**staged worker**", "**lane worker**")),
            ("## Lock", (".tmp/", ".scratch/", "mutation boundary")),
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
