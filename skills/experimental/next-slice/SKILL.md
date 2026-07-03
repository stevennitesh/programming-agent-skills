---
name: next-slice
description: Execute one implementation slice from a saved slice plan.
---

# Next Slice

## Purpose

Execute exactly one slice from a saved plan, validate it, commit it when
completed, report any blocker, and stop. Use this skill only when the user
explicitly invokes `$next-slice`.

This is execution, not planning. Do not rewrite the plan, broaden scope, infer
missing hard fields, or continue into later slices unless the user asks for
replanning or a separate run. Status updates are limited to the runtime
contract's definition.

Runner completion scope is ignored by `$next-slice`; this skill executes
exactly one selected pending slice.

Within the selected slice, treat the plan as a boundary, not a script. Adapt
implementation details when current code demands it, as long as the Objective,
Acceptance criteria, safety and approvals, Validation, Review gate, and Commit
boundary remain intact.

## Inputs

- Prefer an explicit plan path and slice name or number.
- If no plan path is provided, use the active plan only when it is unambiguous
  from the current conversation, repo plan index, or repo docs.
- Ask for the plan path when more than one plan is plausible.

## Workflow

1. Load the plan and runtime contract.
   - Read installed `_shared/slice-runtime-contract.md`, the
     selected plan, its Execution Handoff, local `AGENTS.md`, and slice-named
     specs, docs, tests, CLIs, or artifacts.
   - Read installed `_shared/slice-execution-contract.md` or
     `_shared/slice-planning-contract.md` only when
     this is the first slice for the plan in this conversation, strict
     validation warns or fails, the plan changed beyond status/Handoff note, or
     the selected slice touches plan/schema behavior.
   - If the runtime contract cannot be read, stop.
   - Completion criterion: the target slice, execution limits, branch state, and
     dirty baseline are known.

2. Run strict plan validation.
   - Run strict plan validation, without `--allow-draft`, when the plan path ends
     in `.md`:

     ```bash
     python path/to/to-slice-plan/scripts/validate_slice_plan.py <plan-path>
     ```

     Non-Markdown plans are outside the contract unless the user explicitly
     approved them. Validator warnings do not block by themselves; inspect them
     for drift and report them as `Validation warnings: None` or list the
     warnings inspected.
   - Apply the runtime contract's Selection Rules and Stop Conditions.
   - Stop if the selected slice is missing hard fields, is malformed, or
     asks the executor to infer intent.
   - Stop if the selected slice has non-`None` Fog of war; normal
     implementation uncertainty belongs in `Risks/review traps`, not Fog of
     war.
   - Completion criterion: the selected slice is contract-complete before
     editing.

3. Run the shared Single-Slice Execution Cycle once from the validated
   selection.
   - Do not start later slices.
   - Use continuation mode only when the Execution Handoff allows it and every
     runtime-contract continuation condition holds. It may shorten rereading
     for repeated `$next-slice` invocations in the same plan/session, but never
     changes the one-slice execution limit or skips strict validation, dirty
     checks, approvals, Review gate, or commit hygiene.
   - If repeated awkwardness across adjacent slices suggests the plan is
     fighting the code, stop after the selected slice or blocker and recommend
     prefactoring or replanning instead of broadening silently. Examples:
     needing to change acceptance criteria, move work between slices, add a new
     architecture decision, or touch unrelated modules not named by the plan.
   - If the Review gate is `$review` and no fixed point is named or
     unambiguously derivable from the plan, repo docs, or user request, stop
     and ask. Do not invent one.
   - Completion criterion: the selected slice completed and committed, or the
     blocker was reported by the shared cycle.

## Completion Report

End with the shared Executor Completion Report, preceded by the plan path and
slice selected, completed, or blocked.
