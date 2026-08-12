# Condition-Triggered Review Behavior Evaluation

Date: 2026-08-11

Decision: **accept** the frozen condition-triggered review candidate.

## Registration

- Change type: `defect-correction`
- Expected control deficit: ordinary proved changes require an independent
  reviewer and dormant Repair bookkeeping even when no independent judgment is
  needed; Audit Close rejects an otherwise valid unreviewed implementation.
- Entry predicate: implementation proof and Change Closure are complete, no
  repository or user rule requires review, the final candidate has one mutation
  author, and no material acceptance judgment still needs Change Review as its
  lowest-burden independent decision path.
- Applicability: `common` for the stated personal-project workflow; this is a
  caller-context classification, not an ecosystem-frequency claim.
- Claim: remove review ceremony on the entry-positive path without weakening
  proof, Change Closure, triggered independent review, or bounded repair.

## Frozen Surfaces

The cohort identity is `git hash-object --stdin` over the path/blob records in
the exact table order below. Each record is `<path><space><blob><CRLF>`, encoded
as UTF-8. The order is part of the identity; it is not path-sorted.

| Arm | Identity | Source |
| --- | --- | --- |
| Control | `faae0756f992725ae01dfff4285c122944b18db9` | committed `HEAD` `2a4d5a1c6e4cd9dd2cea314e78a73078c34752e1` |
| Candidate v1 | `205b7b19928a1ab633d7c1eba143449bcae4627e` | entry-positive contribution candidate |
| Candidate v2 | `a5d4694953d8b355fa6fd5d541d1603c16e4d492` | accepted successor with explicit reviewed Close schema and legacy compatibility |

Exact control path/blob manifest:

| Path | Git blob |
| --- | --- |
| `CONTEXT.md` | `9b17ac614e83b419068f5927fd454565093396aa` |
| `README.md` | `0696a91b061b7fc5c6ba5c5c2e75a56f4172f0ef` |
| `AGENTS_PORTABLE_FALLBACK.md` | `4a60f74a72c3558b427c3523f1e9aa6ecb046f7b` |
| `skills/custom/implement/SKILL.md` | `e8211d97a28526fa7de79da98b89845467a7efa0` |
| `skills/custom/parallel-implement/SKILL.md` | `6c31fdf8e427580c8aa865ac9daba914fc59eff6` |
| `skills/custom/change-review/SKILL.md` | `3cf27460e63d4eed47ffeb11b044fbd1baeeb602` |
| `skills/custom/high-assurance-review/SKILL.md` | `443d0b8fa1bab3573a6179150921846ccee4ed20` |
| `skills/custom/audit-codebase/scripts/update_report.py` | `7c3d1f8550a56e21d823c8cfe49e384e98ff5736` |

Exact accepted candidate-v2 path/blob manifest:

| Path | Git blob |
| --- | --- |
| `CONTEXT.md` | `4cc7047bc5a7358b1450d609e3845477884e7258` |
| `README.md` | `05bb06363c0e573179a1e6d93368890a5b54fea0` |
| `AGENTS_PORTABLE_FALLBACK.md` | `1baa9d91e84a21cc69495f47cb96aabfc111f449` |
| `docs/adr/0015-independent-change-review-is-condition-triggered.md` | `30ede6e8f95547a10397708eba4c3bd899c695b4` |
| `skills/custom/implement/SKILL.md` | `06ec722f2ea490f800c14e19d683895d6a4ee1af` |
| `skills/custom/parallel-implement/SKILL.md` | `ae97d8f4314f5b0d51cec4c5d450988c0de2b60d` |
| `skills/custom/change-review/SKILL.md` | `670fedbef33c520713ef574703700d80136cb80e` |
| `skills/custom/high-assurance-review/SKILL.md` | `fc1ab810c67e776b818f7973cea3ebedcdb21b8b` |
| `skills/custom/audit-codebase/scripts/update_report.py` | `cb3da19ccbb5298c032ccf8d441687449335efbf` |

Candidate-v1 used the same manifest except Audit Close blob
`d073b6ec20972510110abe831d07b7af9bdd80f0`. Adding this evidence note changes
none of the listed surfaces.

## Runtime And Authority

Each counted sample was a fresh-context, read-only Codex subagent created with
`fork_turns="none"` on the Windows Codex desktop host in workspace
`E:\GitHub\code\programming-agent-skills`. Model and reasoning settings were
inherited from the root; their exact backend identifiers were unavailable to
the tasks. The available runtime tools were local read-only shell and file
inspection; no network or external provider was used. Control agents could
inspect only committed `HEAD` through `git show`; candidate agents could
inspect only their named working-tree surfaces. Neither arm could inspect the
other arm, prior sample outputs, tests, or evaluations. Root retained the
rubric and made the final judgment. Backend build, token, and latency telemetry
was unavailable.

No sample had mutation, review, commit, synchronization, or publication
authority.

## Fixed Prompt Inputs

The counted C2-C5 control prompt differed only by sample number:

```text
Inspect only committed HEAD 2a4d5a1c... through git show. Do not inspect the
working tree, diff, candidate, tests, evaluations, or peer outputs. Apply the
active Implement, Parallel Implement, Change Review, High-Assurance Review,
CONTEXT, README, and Audit Close instructions to fixed cases A-E. For each,
report review/no-review, specialist/no-specialist, required review/Repair
fields, and completion. Rubric deficit: unnecessary mandatory review or
dormant review/Repair paperwork in any case.
```

C1 received the same A-E inputs and rubric plus the W1-W5 protected cases. The
extra inputs were scored separately and did not alter its A-E judgments.

The counted F1-F5 candidate prompt differed only by sample number:

```text
Inspect only the named candidate working-tree policy surfaces. Do not inspect
history, HEAD, diff, control, tests, evaluations, or peer outputs. Apply the
instructions to the identical fixed cases A-E. For each, report
review/no-review, specialist/no-specialist, required review/Repair fields, and
completion. Pass only if no unnecessary review or dormant review/Repair
paperwork appears and proof, final read-back, and Change Closure remain
mandatory.
```

Candidate-v2 extension F6 used A-E unchanged and added E2: confirm that the
public Close schema can emit the exact accepted-review pair without dormant
fields. F7-F11 used this exact fixed prompt, differing only by sample number:

```text
Inspect only current Audit Close script blob
cb3da19ccbb5298c032ccf8d441687449335efbf. Do not inspect history, HEAD, diff,
control, tests, evaluations, docs, or peer outputs. Evaluate E: valid unreviewed
Close without review/Repair fields while proof and Change Closure remain
required; E2: condition-triggered accepted review has an exact public schema
with the paired review fields and no Repair field; L: legacy v4 manifests and
v10/state-2 reports with a nonnegative repair_generations_used remain readable
while new state/schema omit it. Pass only if all three are explicit and
compatible.
```

The wrong-condition prompts fixed W1-W5 exactly as listed below. Candidate-v2
added W6: preserve condition-triggered accepted-review provenance through the
public `--reviewed` schema branch without a Repair field.

## Entry-Positive Cases And Rubric

| Case | Passing candidate behavior | Control deficit |
| --- | --- | --- |
| A | Proved one-author ordinary change completes without review paperwork | Mandatory fresh reviewer |
| B | One delegated mutation author plus root verification does not count as two authors | Mandatory third actor |
| C | Release, supported risk, or security/production adjacency alone adds no review or specialist | Mandatory ordinary review |
| D | Lower-burden caller-owned migration acceptance avoids independent review | Mandatory review despite the settled decision path |
| E | Audit Close accepts a valid unreviewed result with no review or Repair fields | Close rejects missing review/Repair fields |

Every passing result also had to retain claim-matched proof, final diff and
state read-back, Change Closure, unrelated-state exclusion, and ordinary
touched-contract correctness.

## Entry-Positive Results

Five fresh controls ran before candidate sampling. `D` means the registered
deficit appeared; `P` means the candidate satisfied the complete rubric.

| Arm / sample | A | B | C | D | E | Critical failure |
| --- | --- | --- | --- | --- | --- | --- |
| Control C1 | D | D | D | D | D | no |
| Control C2 | D | D | D | D | D | no |
| Control C3 | D | D | D | D | D | no |
| Control C4 | D | D | D | D | D | no |
| Control C5 | D | D | D | D | D | no |
| Candidate F1 | P | P | P | P | P | no |
| Candidate F2 | P | P | P | P | P | no |
| Candidate F3 | P | P | P | P | P | no |
| Candidate F4 | P | P | P | P | P | no |
| Candidate F5 | P | P | P | P | P | no |

Aggregate: control reproduced the deficit in `25/25` case judgments; candidate
passed `25/25`. Semantic variance was zero on review selection and completion.
One control sample understated the separate Repair field in Audit Close while
still correctly finding Close impossible without review; the other four
controls identified both mandatory review and Repair fields. This did not
affect the registered control deficit.

Audit Close changed after candidate-v1 to expose the reviewed schema branch
and preserve legacy artifact compatibility. A-D retained identical blobs and
reuse their five-sample result. E was resampled against candidate-v2:

| Candidate-v2 sample | E | E2 | L | Critical failure |
| --- | --- | --- | --- | --- |
| F6 | P | P | not scored | no |
| F7 | P | P | P | no |
| F8 | P | P | P | no |
| F9 | P | P | P | no |
| F10 | P | P | P | no |
| F11 | P | P | P | no |

F7-F11 are the five-sample fixed E/E2/L successor cohort and passed `15/15`.
F6 is additional broader-surface evidence and is not part of that fixed cohort.
Candidate-v2 therefore passed `17/17` scored post-gate judgments with zero
semantic variance. Focused execution independently exercised both public
schema branches plus legacy manifest and report compatibility.

## Wrong-Condition Pair

The wrong-condition pair ran only after the candidate cleared the
entry-positive contribution gate.

| Case | Protected behavior | Control | Candidate |
| --- | --- | --- | --- |
| W1 | Retained mutations from two independent authors receive one final review | protected | protected |
| W2 | An explicit repository requirement invokes review | protected | protected |
| W3 | Proved material migration judgment invokes review when review is the lowest-burden independent path | protected | protected |
| W4 | Missing required proof stops before completion | protected, but ordinary Implement may spend a reviewer to rediscover the gap | protected; stops before review |
| W5 | Automatic review repair is bounded | protected by a default two-generation budget | protected by one automatic repair successor, then caller return |
| W6 | Triggered accepted review is representable without dormant Repair state | not applicable to the original policy claim | protected by the explicit `--reviewed` Close schema branch |

The final candidate preserved `6/6` applicable protected cases and removed the control's extra
review-on-known-proof-gap and dormant budget ceremony. Its maximum automatic
review sequence is the initial review plus one repaired successor review.

## Sample Records

- Controls: `review_policy_control_eval`, `review_control_sample_2` through
  `review_control_sample_5`.
- Candidates: `review_candidate_sample_1` through
  `review_candidate_sample_11`.
- Wrong-condition evidence: `review_wrong_control`, `review_wrong_candidate`,
  and final successor `review_wrong_candidate_v2`.

An earlier exploratory candidate task was started before the adaptive control
gate completed and is not counted. Its result agreed with the counted cohort.
The protocol deviation triggered the five-sample post-gate candidate-v2 fixed
cohort F7-F11; F6 is additional broader evidence rather than acceptance at the
five-sample minimum.

## Judgment And Limits

Decision: `accept`.

The control deficit appeared before counted candidate sampling, the candidate
made a material and consistent reduction, and no protected-behavior regression
or critical failure appeared. The result supports exact candidate-v2; it
does not establish general review efficacy or prevalence outside the stated
workflow.

Residual transfer gaps:

- independent mutation authorship and lowest-burden judgment remain semantic
  operator decisions rather than mechanically derived facts;
- the read-only fixtures establish routing judgment, not live provider or Git
  mutations;
- Audit Close records an optional accepted-review decision and provenance, not
  a full review transcript or repair lineage.
