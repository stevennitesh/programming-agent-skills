---
name: slice-plan-runner
description: Run a saved slice plan through multiple committed slices.
---

# Slice Plan Runner

## Purpose

Run a saved slice plan unattended, one slice at a time, committing each completed
slice and stopping on ambiguity, contract failure, failed validation, unsafe
scope, or user-judgment needs. Use this skill only when the user explicitly
invokes `$slice-plan-runner`.

This is an execution loop, not planning. Do not invent a plan, broaden scope,
infer missing contract fields, or replace acceptance criteria. Status updates
are limited to the runtime contract's definition.

## Inputs

- Prefer an explicit plan path, slice limit, and run constraints.
- If no plan path is provided, find the active plan from the current
  conversation, repo plan index, or repo docs. Ask for the path if more than one
  plan is plausible.
- Use Runner completion scope as the plan-authored maximum. The effective run
  limit is the strictest limit from the user request, Runner completion scope,
  Slice/run limits, approvals, runtime contract, local safety policy, and stop
  conditions. If no explicit limit exists, run all remaining slices only when
  the user clearly asked for a full unattended run and Runner completion scope
  allows it; otherwise stop and ask for a limit.
- Treat constraints such as `max 3 slices`, `no network`, `stop before live
  data`, or approval requirements as hard limits.

## Loop Rules

- Read `/home/steve/.codex/skills/_shared/slice-runtime-contract.md` before
  selecting the first slice. If it cannot be read, stop.
- Read `/home/steve/.codex/skills/_shared/slice-execution-contract.md` or
  `/home/steve/.codex/skills/_shared/slice-planning-contract.md` only when
  starting a fresh plan, validation warns or fails, the plan changed beyond
  allowed status/Handoff-note updates, or the selected slice touches
  plan/schema behavior.
- Run strict plan validation, without `--allow-draft`, before the first slice and
  after status updates when the plan path ends in `.md`:

  ```bash
  /home/steve/.codex/skills/to-slice-plan/scripts/validate_slice_plan.py <plan-path>
  ```

  Non-Markdown plans are outside the contract unless the user explicitly
  approved them. Validator warnings do not block by themselves; inspect them for
  drift and report them.
- Honor the Execution Handoff, user constraints, and runtime contract before each
  slice.
- Run validation commands sequentially when they may share temp directories,
  caches, ports, databases, global CLI state, generated outputs, environment
  variables, or live service state. Parallelize only clearly independent checks.
- Execute slices sequentially in plan order unless the plan explicitly permits a
  different order.
- Re-check current state and record a fresh dirty baseline before every slice.
- For each selected slice, run the shared Single-Slice Execution Cycle.
- Use continuation mode after a clean committed slice only when the Execution
  Handoff allows it and every runtime-contract continuation condition holds.
  Continuation shortens rereading; it never skips strict validation, dirty
  checks, approvals, Review gate, or commit hygiene.
- Stop after review findings, failed validation, missing Review gate skills, or
  status update conflicts unless the fix is clearly local to the current or
  just-completed slice.
- Do not batch slices, skip malformed slices, or continue after a blocker that
  needs user judgment.

## Continuation Check

After each committed slice:

1. Re-read the updated plan, next slice, and Execution Handoff.
2. Continue only when validation passed, validator warnings were inspected and
   do not indicate drift, the commit succeeded, remaining slices are
   contract-complete, dirty-work boundaries are intact, Continuation mode and
   Runner completion scope allow the next pass, and no stricter limit or
   approval boundary is reached.
3. Stop before network, live-data, credentialed, destructive, or remote-write
   work without explicit approval.
4. Stop and recommend prefactoring or replanning when repeated awkwardness
   across adjacent slices shows the plan is fighting the code.

Completion criterion: continuing is justified by the plan, runtime contract,
handoff, and current repo state.

## Completion Report

End with the shared Executor Completion Report, preceded by the plan path,
requested or inferred slice limit, completed slices, encountered skipped
slices, and blocked slices. Include any slice the run stopped before starting.

If the run stops early, make the stopping reason the headline. Do not describe a
partial run as complete.
