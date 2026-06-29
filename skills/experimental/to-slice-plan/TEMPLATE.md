# <Plan Title>

Date: <YYYY-MM-DD>

Plan status: proposed implementation plan.

## Authoring Notes

Before strict validation, replace all angle-bracket placeholders with concrete
text, `None`, `N/A`, or an accepted symbolic token. Accepted symbolic-token
convention: `RUN_ROOT`, `PLAN_PATH`, and `OBSERVATION_PATH`; do not wrap them
in angle brackets.

Common valid forms:

- Work type: `feature`, `bug`, `regression`, `performance`, `cleanup`, `docs`,
  `test`, `research`, `decision`, `prototype`, `grilling`, `maintenance`
- Review gate: `none`, `local diff review`, `$review`,
  `$convergent-pr-review`, `repo command: <exact command>`
- Runner completion scope: `disabled`, `one-slice`, `remaining-pending`,
  `max N slices`, `named slices: ...`
- Continuation mode: `disabled`, or the standard allowed-shortcut wording from
  the planning contract
- Status update target: `None`, `plan slice status`,
  `plan slice status; tracker: <id/path>`
- Fog-of-war value: `None`, unless unresolved decision/research/prototype/grilling
  work must be resolved before implementation

Work type examples: live validation or an approved experiment run is
`research`; a fix from observed failing behavior is `bug`; an output, report,
or CLI contract change is `feature`; a measurable latency improvement is
`performance`; documentation-only operator guidance is `docs`.

Review gate meanings: `none` is for tiny slices where validation is enough;
`local diff review` is the normal default; `$review` checks fixed-point
standards/spec conformance; `$convergent-pr-review` coordinates independent
bug/risk convergence; `repo command: ...` runs a repo-owned check literally.

## Goal

<Concrete goal.>

## Out of Scope

<Adjacent phases, tempting follow-ons, or explicitly excluded work.>

## Current State

<What exists now, with file/doc/test/artifact references.>

## Evidence Table

| Claim | Evidence | Notes |
| --- | --- | --- |
| <claim> | <file/doc/test/artifact/command> | <why it matters> |

## Gap Analysis

<What is done, missing, wrong, fragile, duplicated, slow, overbuilt, obsolete,
or misleading. Include design, cleanup, domain, ADR, or grilling notes only when
relevant.>

## Slice Count Rationale

<Why this is the right number of real tracer-bullet slices. For code plans,
explain how the first code slice runs a representative input or call through
production-shaped code to an observable output, or why a smaller enabling slice
must come first. Explain any non-tracer-bullet enabling, cleanup, or horizontal
slice. Mention dependencies, risk, prefactoring needs, Testing seams, and
live-data or review boundaries.>

## Slice Plan

### Slice 1 - <Name>

- Status: `pending`
- Work type: <feature|bug|regression|performance|cleanup|docs|test|research|decision|prototype|grilling|maintenance>
- Objective:
- Dependencies/prerequisites: <requirements, approvals, artifacts, or exact None>
- Acceptance criteria:
- Testing seam: <existing public interface or command>
- Validation: <focused test or command; prefer TDD when practical>
- Review gate: <none|local diff review|$review|$convergent-pr-review|repo command: exact command>
- Commit boundary:
- Branch expectations: <slice commit-safety expectations>
- Fog of war: <unresolved decision work, or None with reason>
- Handoff note:
  - Changed: Pending; slice not yet executed.
  - Remains: <specific remaining work or None>
  - Read next: <specific files/docs/tests/artifacts>
  - Next slice: <next slice name or None>
- Risks/review traps:

<!-- Add only when relevant: Feedback loop; Design impact;
     Data/live/network/approval impact; Cleanup/deletion impact;
     Docs/artifacts impact; Notes/considerations. -->
<!-- Repeat for each slice. Hard fields are required. Use `None` or `N/A`;
     do not omit hard fields. -->

## Recommended First Slice

<The first slice to implement next and why. For code plans, prefer the first
real tracer bullet through the target path.>

## Execution Handoff

- Start command: `Use $next-slice <plan-path> for Slice 1`
- Runner safety: `<whether $slice-plan-runner is safe, why, and scope rationale>`
- Continuation mode: <disabled|allowed after first clean committed slice when
  strict validation passes, only status/handoff changed, and no
  approval/review/dirty/warning drift exists>
- Runner completion scope: <disabled|one-slice|remaining-pending|max N slices|named slices: ...>
- Slice/run limits: `<slice count, time, network, or approval limits>`
- Approvals: `<required approvals or None>`
- Branch expectations: `<run-level branch setup and safety expectations>`
- Status update target: <None|plan slice status|plan slice status; tracker: <id/path>>
- Stop conditions: `<conditions that stop execution or continuation>`
- Strict validation command: `validate_slice_plan.py <plan-path>`
- Validation warnings: `<how validator warnings are handled>`
- Review gate: `<final Review gate value>`
- Handoff note shape: `Changed:`, `Remains:`, `Read next:`, `Next slice:`

## Plan Self-Check

Strict plan validation requires every Plan Self-Check item to be checked. Use
`--allow-draft` only while authoring an incomplete plan.

```bash
/home/steve/.codex/skills/to-slice-plan/scripts/validate_slice_plan.py <plan-path>
/home/steve/.codex/skills/to-slice-plan/scripts/validate_slice_plan.py --allow-draft <plan-path>
```

- [ ] The slice planning and runtime contracts were read and the plan is
      grounded in current files, docs, tests, commands, or artifacts.
- [ ] Every major claim has an evidence pointer.
- [ ] Every slice includes every hard field and required conditional impact field.
- [ ] Empty required fields use `None` or `N/A`, and strict validation passes for
      `.md` plans or the user approved a non-Markdown plan.
- [ ] Slice count, tracer-bullet shape, fog of war, approvals, live/network or
      destructive work, and Out of Scope boundaries are explicit.
- [ ] Validation, Review gate, commit boundary, branch expectations, and Handoff
      note are executable without inferring intent.
- [ ] The plan is saved in the repo and any active plan index is updated when
      appropriate.
