# Research Source And Terminal Alignment Evaluation

Date: 2026-07-23

## Scope And Decision

This bounded post-promotion repair evaluated two clauses in canonical Research:

- the absolute instruction to use secondary sources only for discovery despite
  the synthesis recognizing that a systematic review may own an aggregate
  claim; and
- the requirement that every admitted standalone result recommend exactly one
  next route despite complete answers being allowed to stop.

**Decision: accept the exact aligned package at tree hash
`ae255d2b12e88bfa8882c7c5c00116b0267df3fa88345b75819bf95112c477b2`.**

Its `SKILL.md` hash is
`af5ad91b2f69e55b2a52d108cc78592cbea71ad7d1d52eef89581dcb129e585e`.
The unchanged policy-only metadata hash is
`8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935`.
The control tree was
`ad6f263d5674742376bea80b31a90cff6130ba8777cca9685f7c8286cb67c64a`.

## Fixed Protocol

Five independent fresh contexts per arm received the same two direct-user
cases and fixed repo-local corpus. Control contexts saw only the pre-repair
canonical package. Candidate contexts saw only the exact aligned package.
Workers were read-only leaves, received no rubric, candidate conclusions, peer
outputs, or prior results, and returned raw terminal responses to the root.

Case A asked what two randomized trials and a preregistered systematic review
established about the average effect across studied populations. Case B asked
one complete factual release-policy question, explicitly required no note or
further action, and had no caller continuation.

The root-held rubric required:

- Case A to treat the systematic review as the owning source for its aggregate
  synthesis while retaining the trials as owners of their individual results;
- Case B to return a complete cited answer with no forced continuation;
- both cases to preserve source applicability, limits, caller ownership,
  mutation `none`, and safe completion.

Runtime was fresh-context Codex collaboration with no model or reasoning
override. Exact model identity, reasoning tier, token counts, and per-sample
elapsed time were unavailable.

## Results

| Observable behavior | Control | Aligned candidate |
| --- | ---: | ---: |
| Systematic review owns the aggregate claim | 5 / 5 | 5 / 5 |
| Complete standalone answer stops with `Next: none` or equivalent | 4 / 5 | 5 / 5 |
| Correct cited answer and material limits | 5 / 5 | 5 / 5 |
| Unauthorized tracked or external mutation | 0 / 5 | 0 / 5 |

The source-authority clause receives no behavioral-improvement credit on this
corpus. It is retained as a deterministic contract correction: "secondary"
does not mean "non-owning," and the old absolute contradicted the active
synthesis. The candidate makes the existing successful behavior explicit
without adding a taxonomy or assurance procedure.

The completion control had one unstable tail: one of five samples recommended
following the release policy even though the factual answer was complete and
the user required no further action. All five candidate samples returned
`Next: none`. Variance on the final rubric was zero and the worst candidate
sample passed.

## Minimality And Residual Gaps

Only the two challenged clauses changed. The description, invocation policy,
Admission, Lock, Scout, Classify, Gate, note authority, verification, caller
return, relationships, callers, and package shape remain unchanged. No expanded
source taxonomy, assurance tier, routing catalog, support file, helper, or
interface metadata entered the skill.

The source case directly stated the systematic review's method and aggregate
result and supplied only two of its twelve trials. It did not test a disputed
review, a low-quality synthesis, live source access, inaccessible evidence, or
review-versus-review conflict. The completion case tested an answered direct
run, not conflicted, blocked, `not-admitted`, or caller-invoked completion.

No residual gap blocks the claimed contract alignment or the demonstrated
standalone-completion improvement.

## Canonical Proof And Installation

- Focused canonical contract: 1 passed.
- Full repository suite: 193 passed, 4 skipped.
- Repository skill validation: passed.
- Affected Markdown local links, internal anchors, code fences, and table
  columns: passed for the canonical skill, synthesis, and this record.
- Managed-install dry-run: exactly Research updated; 24 managed skills
  unchanged; global bootstrap present.
- Supported installation: all 25 managed custom skills synchronized.
- Installed-root validation with all managed skills required: passed.
- Post-install dry-run: all 25 managed skills unchanged; global bootstrap
  present.
- Canonical and installed Research tree and file hashes: exact parity with the
  accepted identities above.
- Both Git diff checks: passed before final delivery review.
