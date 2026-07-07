#!/usr/bin/env python3
"""Regression checks for validate_slice_plan.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR_PATH = SCRIPT_DIR / "validate_slice_plan.py"
spec = importlib.util.spec_from_file_location("validate_slice_plan", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

SELF_CHECK = """
- [x] The slice planning and runtime contracts were read and the plan is
      grounded in current files, docs, tests, commands, or artifacts.
- [x] Every major claim has an evidence pointer.
- [x] Every slice includes every hard field and required conditional impact field.
- [x] Empty required fields use `None` or `N/A`, and strict validation passes for
      `.md` plans or the user approved a non-Markdown plan.
- [x] Slice count, tracer-bullet shape, fog of war, approvals, live/network or
      destructive work, and Out of Scope boundaries are explicit.
- [x] Validation, Review gate, commit boundary, branch expectations, and Handoff
      note are executable without inferring intent.
- [x] The plan is saved in the repo and any active plan index is updated when
      appropriate.
""".strip()


def base_plan(
    *,
    extra_slice_line: str = "",
    review_gate: str = "none",
    status_target: str = "plan slice status",
    work_type: str = "test",
    objective: str = "Check strict validation behavior.",
    approvals: str = "None",
    continuation_mode: str = (
        "allowed after first clean committed slice when strict validation passes, "
        "only status/handoff changed, and no approval/review/dirty/warning drift exists"
    ),
    runner_completion_scope: str = "one-slice",
) -> str:
    return f"""# Regression Slice Plan

Date: 2026-06-27

Plan status: proposed implementation plan.

## Goal

Exercise validator behavior.

## Out of Scope

Adjacent feature work.

## Current State

Validator and fixture coverage exist in this skill. Markdown autolinks like
<https://example.com> are allowed.

## Evidence Table

| Claim | Evidence | Notes |
| --- | --- | --- |
| Validator behavior is checked | scripts/test_validate_slice_plan.py | Regression coverage |

## Gap Analysis

The validator needs strict regressions.

## Slice Count Rationale

One slice is enough for the fixture.

## Slice Plan

### Slice 1 - Validator Fixture

- Status: `pending`
- Work type: {work_type}
- Objective: {objective}
- Dependencies/prerequisites: None
- Acceptance criteria: Validator accepts the base plan and rejects malformed variants.
- Testing seam: validate_plan()
- Validation: python3 scripts/test_validate_slice_plan.py
- Review gate: `{review_gate}`
- Commit boundary: Validator regression only.
- Branch expectations: Safe feature branch.
- Fog of war: None
- Handoff note:
  - Changed: Validator fixture exercised.
  - Remains: None
  - Read next: Slice Plan
  - Next slice: None
- Risks/review traps: None
{extra_slice_line}
## Recommended First Slice

Slice 1 - Validator Fixture.

## Execution Handoff

- Start command: `Use $next-slice plan.md for Slice 1`
- Runner safety: `$slice-plan-runner` is safe for this one-slice fixture.
- Continuation mode: {continuation_mode}
- Runner completion scope: {runner_completion_scope}
- Slice/run limits: one slice.
- Approvals: {approvals}
- Branch expectations: Safe feature branch.
- Status update target: {status_target}
- Stop conditions: validation failure or dirty overlap.
- Strict validation command: `validate_slice_plan.py plan.md`
- Validation warnings: inspect and report warnings.
- Review gate: `{review_gate}`
- Handoff note shape: `Changed:`, `Remains:`, `Read next:`, `Next slice:`

## Plan Self-Check

{SELF_CHECK}
"""


def validate_text(text: str) -> tuple[list[str], list[str]]:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "plan.md"
        path.write_text(text, encoding="utf-8")
        return validator.validate_plan(path)


def require_valid(name: str, text: str) -> None:
    errors, warnings = validate_text(text)
    if errors or warnings:
        raise AssertionError(
            f"{name} expected valid, got errors={errors} warnings={warnings}"
        )


def require_error(name: str, text: str, expected: str) -> None:
    errors, _warnings = validate_text(text)
    if not any(expected in error for error in errors):
        raise AssertionError(
            f"{name} expected error containing {expected!r}, got {errors}"
        )


def require_warning_only(name: str, text: str, expected: str) -> None:
    errors, warnings = validate_text(text)
    if errors or not any(expected in warning for warning in warnings):
        raise AssertionError(
            f"{name} expected warning containing {expected!r}, "
            f"got errors={errors} warnings={warnings}"
        )


def require_line_aware_error(name: str, text: str, expected: str) -> None:
    errors, _warnings = validate_text(text)
    if not any(expected in error and "line " in error for error in errors):
        raise AssertionError(
            f"{name} expected line-aware error containing {expected!r}, got {errors}"
        )


def main() -> int:
    require_valid("base", base_plan())
    require_valid("review skill", base_plan(review_gate="$convergent-pr-review"))
    require_valid(
        "tracker status target",
        base_plan(status_target="plan slice status; tracker: docs/PLAN.md"),
    )
    require_valid(
        "bug with feedback",
        base_plan(
            work_type="bug",
            extra_slice_line="- Feedback loop: python3 -m pytest tests/test_bug.py\n",
        ),
    )
    require_valid(
        "high-risk with impact",
        base_plan(
            objective="Run a network probe.",
            approvals="Approved network probe.",
            extra_slice_line="- Data/live/network/approval impact: approved probe only\n",
        ),
    )
    require_warning_only(
        "unknown field",
        base_plan(extra_slice_line="- Extra field: tolerated warning\n"),
        "unknown slice field",
    )
    require_warning_only(
        "design hint",
        base_plan(objective="Change the module interface."),
        "Lexical warning: Objective contains 'module'",
    )
    require_error(
        "duplicate field",
        base_plan(extra_slice_line="- Objective: Duplicate\n"),
        "duplicate field 'Objective'",
    )
    require_line_aware_error(
        "duplicate field line",
        base_plan(extra_slice_line="- Objective: Duplicate\n"),
        "duplicate field 'Objective'",
    )
    require_error(
        "duplicate section",
        base_plan().replace("## Goal\n", "## Goal\n## Goal\n", 1),
        "duplicate top-level section",
    )
    require_error(
        "slice outside plan",
        base_plan().replace("## Current State\n", "## Current State\n### Slice 99 - Bad\n", 1),
        "slice headings are only allowed inside '## Slice Plan'",
    )
    require_error(
        "duplicate slice number",
        base_plan().replace("### Slice 1 - Validator Fixture", "### Slice 2 - Bad"),
        "slice numbers must be sequential starting at 1",
    )
    require_error(
        "duplicate slice heading",
        base_plan().replace(
            "## Recommended First Slice",
            "### Slice 1 - Duplicate\n\n- Status: `pending`\n\n## Recommended First Slice",
        ),
        "duplicate Slice 1 headings",
    )
    require_error(
        "bad tracker",
        base_plan(status_target="plan slice status; named tracker"),
        "Status update target",
    )
    require_error(
        "start command missing current plan",
        base_plan().replace(
            "Use $next-slice plan.md for Slice 1",
            "Use $next-slice other-plan.md for Slice 1",
        ),
        "Start command must name the current plan",
    )
    require_error(
        "start command missing concrete slice",
        base_plan().replace(
            "Use $next-slice plan.md for Slice 1",
            "Use $next-slice plan.md for the next pending slice",
        ),
        "Start command must name a concrete Slice number",
    )
    require_error(
        "strict command missing current plan",
        base_plan().replace("validate_slice_plan.py plan.md", "validate_slice_plan.py other.md"),
        "Strict validation command must name the current plan",
    )
    require_error(
        "strict command uses draft",
        base_plan().replace(
            "validate_slice_plan.py plan.md",
            "validate_slice_plan.py --allow-draft plan.md",
        ),
        "must not use --allow-draft",
    )
    require_error(
        "bad continuation mode",
        base_plan(continuation_mode="allowed after the first slice"),
        "Continuation mode missing terms",
    )
    require_valid("disabled continuation mode", base_plan(continuation_mode="disabled"))
    for scope in (
        "disabled",
        "one-slice",
        "remaining-pending",
        "max 3 slices",
        "named slices: Slice 2, Slice 4",
    ):
        require_valid(f"runner scope {scope}", base_plan(runner_completion_scope=scope))
    for scope in ("one slice", "all", "max three slices", "named slices:"):
        require_error(
            f"bad runner scope {scope}",
            base_plan(runner_completion_scope=scope),
            "Runner completion scope",
        )
    require_error(
        "bad review gate",
        base_plan(review_gate="convergent-pr-review"),
        "use '$convergent-pr-review'",
    )
    require_error(
        "missing review gate skill",
        base_plan(review_gate="$not-installed-review"),
        "allowed skill gates",
    )
    require_error(
        "leftover placeholder",
        base_plan().replace("Exercise validator behavior.", "Exercise <placeholder>."),
        "leftover placeholder",
    )
    require_error(
        "handoff sentinel",
        base_plan().replace("- Remains: None\n", "- Remains: None.\n"),
        "use exact 'None'",
    )
    require_error(
        "bug missing feedback",
        base_plan(work_type="bug"),
        "bug slice needs non-N/A Feedback loop",
    )
    require_warning_only(
        "high-risk warning field",
        base_plan().replace(
            "Validation: python3 scripts/test_validate_slice_plan.py",
            "Validation: python3 scripts/test_validate_slice_plan.py # network fixture",
        ),
        "Lexical warning: Validation contains 'network'",
    )
    require_error(
        "high-risk missing impact",
        base_plan(objective="Run a network probe."),
        "Data/live/network/approval impact",
    )
    require_error(
        "high-risk missing approval",
        base_plan(
            objective="Run a network probe.",
            extra_slice_line="- Data/live/network/approval impact: approved probe only\n",
        ),
        "Approvals cannot be None/N/A",
    )
    require_error(
        "cleanup missing impact",
        base_plan(work_type="cleanup"),
        "Cleanup/deletion impact",
    )
    require_error(
        "docs missing impact",
        base_plan(work_type="docs"),
        "Docs/artifacts impact",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "template.md"
        path.write_text(
            validator.DEFAULT_TEMPLATE_PATH.read_text(encoding="utf-8")
            + "\n- Dependencies/prerequisites: `None`\n",
            encoding="utf-8",
        )
        errors = validator.validate_template(path)
        if not any("stale default-biased value" in error for error in errors):
            raise AssertionError(f"stale template expected error, got {errors}")

    schema_output = StringIO()
    with redirect_stdout(schema_output):
        validator.print_schema()
    schema = schema_output.getvalue()
    for expected in (
        "Valid Work type values:",
        "Review gate values:",
        "$review: fixed-point standards/spec conformance; fixed point required",
        "$convergent-pr-review: independent bug/risk convergence with verification",
        "Runner completion scope values:",
        "RUN_ROOT",
        "Plan Self-Check items:",
    ):
        if expected not in schema:
            raise AssertionError(f"schema output missing {expected!r}: {schema}")

    print("validate_slice_plan regression checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
