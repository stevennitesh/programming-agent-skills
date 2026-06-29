---
name: to-slice-plan
description: Create no-babysitting implementation slice plans.
---

# To Slice Plan

## Purpose

Turn an implementation goal or analysis finding into a durable executable
handoff. It can be executed by `$next-slice` one slice at a time or by
`$slice-plan-runner` during an approved unattended run. Use this skill only
when the user explicitly invokes `$to-slice-plan`.

Do not implement code while using this skill. Finish and validate the plan first;
implementation belongs in `$next-slice` or `$slice-plan-runner`.

## Contract

Read these contracts before planning:

- `/home/steve/.codex/skills/_shared/slice-planning-contract.md`
- `/home/steve/.codex/skills/_shared/slice-runtime-contract.md`

If either cannot be read, stop. Use [`TEMPLATE.md`](TEMPLATE.md) as the
authoring shape, but treat the contracts and validator as authoritative: every
hard field is present, conditional impact fields are included only when
relevant, empty values are `None` or `N/A`, and the handoff is executable
without inferred intent.

After saving any `.md` slice plan, validate it with:

```bash
/home/steve/.codex/skills/to-slice-plan/scripts/validate_slice_plan.py <plan-path>
```

Use `--allow-draft` only while authoring an incomplete plan. Strict plan
validation without `--allow-draft` must pass before calling the plan ready.
Validator warnings do not block by themselves, but must be inspected as
possible drift and reported. Non-Markdown plans are outside this contract unless
the user explicitly approves them.

## Workflow

1. Inspect the real current state.
   - Read the relevant repo docs, specs, prior result docs, tests, CLIs, code
     paths, artifacts, current worktree status, and recent commits.
   - Treat review comments, live-data evidence, and validation output as
     plan-changing.
   - Completion criterion: every current-state claim in the plan has an
     inspected evidence pointer.

2. Compare implementation to the goal.
   - Separate what is done, missing, wrong, fragile, duplicated, slow,
     overbuilt, obsolete, or misleading.
   - Identify the Testing seam, validation boundary, and any conditional
     impacts that matter for safety, review, or handoff.
   - Use `Fog of war` only for unresolved decisions that must be resolved
     before implementation. Use `Risks/review traps` for normal implementation
     uncertainty, edge cases, stale assumptions, or things the executor should
     inspect carefully.
   - Recommend grilling when specs, ADRs, domain language, acceptance criteria,
     or intent alignment are uncertain.
   - Completion criterion: the gap analysis is evidence-backed and uncertain
     decisions are isolated instead of hidden inside implementation slices.

3. Choose bounded slices.
   - Prefer real tracer bullets: narrow vertical paths through production-shaped
     code that take a representative input or call, exercise the actual
     boundary/module/CLI/API under change, produce an observable output or
     persisted state, and verify it with a focused test or command.
   - Prefer TDD for behavior-changing code when practical: plan a targeted test
     that can fail before the implementation and pass after it. Do not force
     red-green sequencing when the stronger proof is an existing test update,
     contract validation, CLI/report command, fixture diagnostic, or live-data
     approval gate.
   - Shape the whole plan as real tracer bullets when possible. Use enabling,
     cleanup, or horizontal slices only when a vertical slice is not yet
     possible or would be riskier; explain that tradeoff in `Slice Count
     Rationale`.
   - For code implementation plans, make the first code slice a real tracer
     bullet whenever possible. If the first slice cannot be vertical, make it
     the smallest enabling slice that creates the missing Testing seam or
     contract, and explain why in `Slice Count Rationale`.
   - Plan only enough slices to reduce real uncertainty, prove behavior,
     simplify the code, or create a working path.
   - Merge or remove slices that only add ceremony, rename things, or defer the
     hard part.
   - For workflow-loop or operator-loop plans, identify where agent inference is
     valuable and where deterministic handoff should be fast, scripted, or
     cache-backed. Good slices improve the decision packet, deterministic
     command/artifact handoff, validation visibility, or post-run
     interpretation.
   - When planning operator-loop improvements, name the deterministic handoff
     surface: commands, artifacts, cache files, validators, reports, and tests
     the executor should use instead of rediscovering manually.
   - Keep plans as short as possible while preserving executable handoff
     quality. Prefer precise acceptance criteria, validation, dependencies,
     risks, and handoff notes over long implementation narration.
   - Keep each slice narrow enough to validate, review, and commit alone.
   - Separate live-data/network runs from pure code when approvals, runtime, or
     reproducibility matter.
   - Add a prefactoring slice only when it materially lowers risk or makes the
     main change straightforward; otherwise keep cleanup inside the touched
     slice.
   - Completion criterion: every slice has all hard contract fields,
     justified dependencies, explicit validation, a Review gate, one commit
     boundary, and only relevant conditional impact fields.

4. Save and validate the plan.
   - Use the repo's existing docs/plans location and naming style.
   - Update an active plan index only when the repo has one and this plan should
     become active.
   - Run strict plan validation for `.md` slice plans before calling the plan
     ready; use `--allow-draft` only for intermediate authoring checks.
   - Completion criterion: the plan path exists, all self-check boxes are
     complete, and the final report clearly labels the plan ready or blocked.

## Planning Rules

- Preserve unrelated dirty work.
- Keep generated data, caches, downloaded artifacts, and bulky outputs out of
  tracked source unless explicitly required.
- Do not move into adjacent phases outside the user's requested goal.
- Use `Out of Scope` to fence tempting follow-ons.
- Use shared vocabulary, hard field names, conditional impact field names, and
  Review gate values exactly as defined by the planning and runtime contracts.
- When schema choice is unclear, prefer existing valid vocabulary and explain
  the nuance in `Risks/review traps`, `Feedback loop`, or impact fields rather
  than inventing a new Work type or field.
- Set Execution Handoff `Continuation mode` to `disabled` when repeated
  full-read execution is safer; otherwise use the standard allowed-shortcut
  wording from the planning contract.
- Set Execution Handoff `Runner completion scope` as the plan-authored maximum
  for `$slice-plan-runner`. Choose it intentionally:
  - Use `one-slice` for risky first slices, uncertain architecture, unproven
    contracts, approval boundaries, live/network behavior, destructive work, or
    when the next slice should be reassessed after the first commit.
  - Use `remaining-pending` for normal multi-slice offline implementation when
    slices are fixture-driven, commit-bounded, validation-backed, and have no
    approval boundary.
  - Use `max N slices` or `named slices: ...` when only part of the plan is safe
    to run unattended before a later review, live-data, network, or decision
    boundary.
  - Use `disabled` when `$slice-plan-runner` should not execute the plan.
  - Explain the choice in `Runner safety`, including why the selected scope is
    safe or why it is intentionally narrow.
- If using `Review gate: $review`, name the fixed point or explain where the
  executor can derive it without guessing. A named spec/source is helpful, but
  `$review` may discover the spec or report Spec as unavailable.

## Validator Debugging

- Invalid Work type: use the exact list from the template or contract.
- Non-`None` Fog of war rejected: move normal uncertainty to
  `Risks/review traps`, or use `decision`, `research`, `prototype`, or
  `grilling` only when the slice truly resolves unknowns.
- Leftover placeholder: replace `<...>` with concrete text, `None`, `N/A`, or
  an accepted symbolic token such as `RUN_ROOT`, `PLAN_PATH`, or
  `OBSERVATION_PATH`.
- Feedback loop required: `bug`, `regression`, and `performance` slices need a
  concrete feedback loop.
- Cleanup/deletion impact required: cleanup, deletion, deprecation,
  consolidation, or prefactoring wording triggers it.
- Warning keywords are lexical hints; inspect them for drift, but they may be
  harmless in ordinary prose, fixture descriptions, or validation coverage.

## Completion

End with a planner completion report, not the shared Executor Completion Report:

- saved plan path;
- `Plan Self-Check: satisfied`, or unsatisfied items with blockers;
- strict plan validation command, result, and warnings if any, or why
  validation was not applicable;
- plan state: `ready` only when strict validation passed and no blockers remain,
  otherwise `blocked` with the blocker;
- `Fog of war: None`, or unresolved decisions;
- slice count and first slice to implement next when ready;
- executor readiness only for ready plans: strict validation passed, first
  pending slice is named, and Execution Handoff is complete;
- grilling recommendation;
- blockers, evidence gaps, assumptions, or review gate concerns when present;
- Handoff note in the shape `Changed:`, `Remains:`, `Read next:`, `Next slice:`.
