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

SETUP_SCHEMA_TOKEN = "<!-- programming-agent-skills setup-schema: 1:236234b74983 -->"

AGENT_POINTERS = (
    "docs/agents/issue-tracker.md",
    "docs/agents/triage-labels.md",
    "docs/agents/domain.md",
    "docs/agents/engineering-contract.md",
)

CONTRACT_TOKENS = (
    "**Source trace:**",
    "**Bounded slice:**",
    "**Commitment boundary:**",
    "**Load-bearing internal:**",
    "**Semantic correctness:**",
    "**Semantic proof:**",
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
    "Orient -> Explore -> Decide -> Prove -> Cover -> Converge -> Simplify -> Lock",
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


def main() -> int:
    root = Path(parse_args().repo).resolve()
    failures: list[str] = []

    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if git_root.returncode != 0:
        failures.append("Target is not a Git repository")

    texts = {
        relative: read_required(root, relative, failures) for relative in REQUIRED_FILES
    }

    agents = texts["AGENTS.md"]
    if agents:
        if not re.search(r"(?m)^## Commands\s*$", agents):
            failures.append("AGENTS.md is missing a ## Commands primer")
        if SETUP_SCHEMA_TOKEN not in agents:
            failures.append(
                "AGENTS.md is missing the current programming-agent-skills setup-schema marker"
            )
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
        CONTRACT_TOKENS,
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
