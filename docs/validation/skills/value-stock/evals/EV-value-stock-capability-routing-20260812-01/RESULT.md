# Value-Stock Capability Routing Evaluation

Decision: `accept`

## Registration

- Change class: `defect-correction`
- Expected control deficit: operation capability is resolved after dependent
  evidence, gates, forecasting, and freezing; catalog `blocked` can be mistaken
  for `no_match`; an unsupported optional reverse operation can be treated as a
  required Compact/Full failure.
- Entry predicate: security identity and method fit are settled, an intrinsic
  operation is supported, and a distinct optional or requested operation is not.
- Applicability: `situational`. The stock-valuation caller currently supports a
  residual-income intrinsic spine without a compatible reverse operation; this
  fixture establishes relevance, not prevalence.
- Authority: stock-valuation reconciliation ticket 04, the canonical
  `value-stock` skill, and its analyst-runbook and return-contract owners.
- Host and tools: Codex fresh-context subagents with read-only shell/file access.
  Model, reasoning, and runtime identity telemetry were unavailable.

## Frozen Entry-Positive Cohort

Task facts: identity settled; residual income selected on fit; caller-owned
residual-income calculate/report supported; reverse unsupported; authoritative
price present; catalog state `blocked`; ordinary Compact valuation; reverse not
explicitly requested. Extension samples fixed the catalog question as
non-load-bearing to intrinsic residual income so its routing effect could be
separated from the independent gate-status rule.

Rubric:

1. resolve exact operation capability before dependent method work;
2. preserve `blocked` and do not initiate new research;
3. do not improvise or execute unsupported reverse arithmetic; and
4. keep the optional adjunct gap separate from otherwise-complete intrinsic
   status.

Frozen control commit: `064dda7c67ca7ee8cee3bfb0c185ebd578cf946c`.

| File | Control blob | Candidate blob |
| --- | --- | --- |
| `skills/extra/value-stock/SKILL.md` | `5eb064b1ea725da2c8dacc65e58af428ebf31bbe` | `88602ddb6a40f2614cad3d05efa0a3825e8443bf` |
| `skills/extra/value-stock/references/analyst-runbook.md` | `b961a98d56f9fb88c24b368f19d10c21e93e456f` | `597b16d312630256579ccc54e1e3546239563e6b` |
| `skills/extra/value-stock/references/compact-report.md` | `94b8f7d83fbad4e33c1f470ac188138966f17146` | `fd2851663d73e16ec0b6503967a25c27acf24aa4` |
| `skills/extra/value-stock/references/report-contract.md` | `86d5e3bf313f4e611b1a9e453d7e9d605a638a6c` | `2211e6cca6810c7f0b27e89366af44070b6524e4` |

## Entry-Positive Results

Each cell scores rubric items 1-4 above as `P` or `F`. The disposition column
records the observed action, ambiguity, or qualification. Sample IDs are the
fresh-context task suffixes used during execution.

| Control sample | 1 | 2 | 3 | 4 | Critical | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `control1` | F | F | P | F | yes | Capability followed Gates 1-3 and freeze; `blocked` remained ambiguous; reverse was not executed; overall status was narrowed. |
| `control2` | F | P | P | F | yes | Capability was late and research was withheld, but non-downgrade was only a safest-reading inference, not an owned rule. |
| `control3` | F | F | P | P | yes | Capability was late and `blocked` was mapped to new research; unsupported arithmetic was refused and intrinsic status was preserved. |
| `control4` | F | P | P | F | yes | Capability was late; no research from `blocked` alone; reverse refused; Compact was narrowed to `partial`. |
| `control5` | F | F | P | P | yes | Capability was late and `blocked` was treated as no eligible answer; reverse refused; intrinsic result preserved. |
| `ext-control6` | F | P | P | F | yes | Evaluator marked 1 and 4 pass by inference; root adjudication failed both because the cited calculation boundary follows forecast/freeze and no explicit status-protection rule exists. |
| `ext-control7` | F | P | P | F | yes | Exact late-order and unconditional reverse/status conflict identified; no research for the fixed non-load-bearing question. |
| `ext-control8` | F | P | P | F | no | Same two rubric failures; evaluator classified them non-critical because safe arithmetic and research boundaries still held. |

Control aggregate: item 1 `0/8`, item 2 `5/8`, item 3 `8/8`, and item 4
`2/8`. The extended samples disposed the initial variance: safe non-execution
was stable, while early ordering and explicit status ownership consistently
failed when judged from owned wording rather than favorable inference. The
single evaluator-score disagreement is preserved above with root adjudication.

| Candidate sample | 1 | 2 | 3 | 4 | Critical | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate1` | P | P | P | P | no | Bound before dependent work; `blocked` retained; reverse stopped; intrinsic status preserved with independent load-bearing qualification. |
| `candidate2` | P | P | P | P | no | All four actions explicit; report contract loaded only at composition. |
| `candidate3` | P | P | P | P | no | All four actions explicit; catalog status distinguished from valuation status. |
| `candidate4` | P | P | P | P | no | All four actions explicit; re-resolution limited to changed operation identity. |
| `candidate5` | P | P | P | P | no | All four actions explicit; price evidence did not create reverse capability. |
| `ext-candidate6` | P | P | P | P | no | Four-row rubric returned all pass from the frozen commit. |
| `ext-candidate7` | P | P | P | P | no | Four-row rubric returned all pass and preserved the non-load-bearing qualification. |
| `ext-candidate8` | P | P | P | P | no | Four-row rubric returned all pass; no research, reverse execution, or status contamination. |

Candidate aggregate: every item `8/8`; no critical failure. Variance was limited
to explanatory detail and whether the already-resolved reverse binding was
described before or after the supported intrinsic branch. Every candidate also
preserved the independent rule that inaccessible required primary evidence or
an unbounded load-bearing intrinsic input can still narrow or block intrinsic
status for its own reason.

## Frozen Wrong-Condition Pairs

Countercondition facts: FCFF selected on fit; caller-owned calculate, compatible
reverse, report, and audit supported; authoritative price present; catalog state
`no_match` for one material bounded question without a full-effect bound;
ordinary Compact valuation.

| Pair sample | Research | Reverse | One path | Conditional loading | Critical | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `wrong-control1` | P | P | P | P | no | At most one handoff; reverse after dependency readiness; caller path only; unrelated branches excluded. |
| `wrong-candidate1` | P | P | P | P | no | Protected actions preserved; deterministic audit did not trigger independent review. |
| `wrong-control2` | P | P | P | P | no | One handoff; supported reverse; caller path; Compact-only composition. |
| `wrong-candidate2` | P | P | P | P | no | Protected actions preserved; selected-section-only return loading made explicit. |

Wrong-condition aggregate: each protected item `4/4`; no critical failure and
no regression. Candidate samples additionally scoped return-time loading to the
source and method sections already selected by the runbook.

## Judgment

The candidate materially corrects the registered routing defect in all eight
entry-positive samples without a protected-behavior regression in the two
wrong-condition pairs. Structural tests are corroboration only; the decision is
based on the fresh action simulations above.

The initial five-sample arms were grouped so committed control bytes could
remain isolated from candidate language. Because that protocol deviation and
material control variance required extension, three more fresh samples per arm
were run as alternating fixed-commit pairs where slot availability allowed.
Their explicit non-load-bearing fact isolated catalog routing from intrinsic
gate status, and their per-rubric format exposed one favorable control inference
that the root conservatively adjudicated as failure. No sample was reused, no
evaluator edited the repository, and control prompts excluded candidate text
and conclusions. This extension disposes the protocol deviation and variance;
no further material variance remains.

Residual transfer gap: the evaluation is synthetic and does not establish how
often callers expose partially supported operation sets. Live valuations must
still resolve the caller's declared operation contract.
