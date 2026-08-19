# Implement Lean-Pilot Behavior Evaluation

## Registration

- Evaluation type: `quality-lift`
- Expected control deficit: ordinary implementation work retains sound coding
  choices but carries review, closure, tree, tracker, commit, and fixed Return
  protocol when none of those branches is active.
- Entry predicate: one settled, bounded implementation item with no explicit
  TDD, delegation, tracker, Git-delivery, review, deployment, or destructive
  mutation trigger.
- Applicability: `common`. This is the pack's intended normal coding path and
  the five fixtures cover feature, defect, refactor, external-boundary, and
  already-satisfied work. The cohort does not establish population frequency.
- Rubric: preserve the smallest sound design, current owner, real caller,
  proportionate proof, subtractive cleanup, and truthful completion; minimize
  workflow and artifacts that do not affect the result. Coding quality and
  ceremony were each scored from 1 to 5; for ceremony, 1 is leanest.
- Authority: read-only evaluation. No sample could edit the repository, invoke
  a workflow, publish, commit, or mutate external state.

## Fixed Points

- Control: commit `ffad06982a3aac1666bcd9433de33a540f532daf`, Git blob
  `baee2bd61e92eb91aa087df8fbed007688342036`, reconstructed-content SHA-256
  `47a59f2c81b3caf0770e2fbddc8f6a44cd7a7b884bd16d78c65fbd8d18ffd219`.
- Candidate: `skills/custom/implement/SKILL.md`, SHA-256
  `a706cdd33a6b3077b191535550aa2622f89f1bc4ce79bc36707fd9719e38528d`.
- Size: 1,447 control words and 604 candidate words, a 58% reduction.
- Host: Codex desktop fresh-context subagents on 2026-08-19.
- Model and reasoning: inherited `default` agent runtime. Exact backend build,
  reasoning configuration, token counts, latency, and cost were unavailable.
- Tools: control samples could read only the pinned Git object; candidate
  samples could read only the frozen candidate file. No sample had mutation
  authority.

## Entry-Positive Cohort

The five fixed inputs were:

1. Add a settled `--compact` CLI flag through the existing renderer.
2. Fix a confirmed numeric `Retry-After` parser defect.
3. Move a duplicate normalizer to its named existing owner and delete the copy.
4. Use a configured upload target and validate the provider result before a
   local manifest update, without a live upload.
5. Recognize that `.yaml` support and its production-path test already exist.

| Sample | Control result | Candidate result |
| --- | --- | --- |
| F1 feature | Quality 5, ceremony 2; sound direct change, but prescribed Change Closure and structured Return. | Quality 5, ceremony 1; direct flag threading, focused formatting proof, concise Return. |
| F2 known bug | Quality 5, ceremony 2; correct narrow exception handling, plus closure and fixed status fields. | Quality 5, ceremony 1; catches only conversion failures and adds proof only if missing. |
| F3 refactor | Quality 5, ceremony 2; correct owner and deletion, plus closure/tree protocol. | Quality 5, ceremony 1; one owner, duplicate removed, existing caller tests only. |
| F4 external boundary | Quality 5, ceremony 1; correctly validates response and avoids unauthorized live upload. | Quality 5, ceremony 1; same boundary behavior and explicit unproved live-provider gap. |
| F5 already satisfied | Quality 5, ceremony 1; no change and one existing focused check. | Quality 5, ceremony 1; no change and one existing focused check. |

Control tasks:
`/root/implement_control_feature`, `/root/implement_control_bug`,
`/root/implement_control_refactor`, `/root/implement_control_external`, and
`/root/implement_control_noop`.

Candidate tasks:
`/root/implement_candidate_feature`, `/root/implement_candidate_bug`,
`/root/implement_candidate_refactor`, `/root/implement_candidate_external`,
and `/root/implement_candidate_noop`.

Aggregate coding-quality mean was 5.0 in both arms, with no variance. Ceremony
mean improved from 1.6 to 1.0; the candidate had no variance and its worst
result was quality 5, ceremony 1. No critical failure appeared.

## Wrong-Condition Pairs

Three situational pairs ran only after the contribution gate passed:

- Explicit TDD: both arms invoked `$tdd`. Both leave RED ordering to the TDD
  owner rather than duplicating it in Implement. No regression.
- Explicit subagent request: both arms delegated the bounded edit and required
  root inspection. The candidate loads the existing handoff and runtime-profile
  references only on this branch. No regression.
- Two-author irreversible migration: both arms triggered independent review,
  kept the candidate fixed, preserved caller authority for the external
  mutation, and required result read-back. The candidate leaves review-result
  mechanics to `$change-review`. No regression.

Control tasks were `/root/implement_wrong_control_tdd`,
`/root/implement_wrong_control_delegate`, and
`/root/implement_wrong_control_review`. Candidate tasks used the same names
with `candidate` in place of `control`.

## Decision

- Critical failures: none.
- Protocol deviations: arm order was control then candidate because the
  adaptive gate requires confirming the control deficit first. No context was
  reused between samples. Only one candidate sample explicitly reported
  recomputing the supplied SHA-256; the root froze and rechecked it before and
  after the cohorts.
- Unavailable telemetry: exact model build, reasoning effort, token use,
  latency, cost, and live repository-edit behavior.
- Evaluation decision: `accept`.
- Residual transfer gap: these are semantic coding vignettes, not longitudinal
  measurements of production defects or maintenance cost. Use the rewritten
  Implement skill as the bounded pilot before applying the pattern to the rest
  of the pack.
