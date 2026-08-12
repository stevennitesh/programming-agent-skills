# Value-stock conditional-loading quality lift

## Registration

- **Type:** `quality-lift`
- **Entry predicate:** an ordinary Compact valuation uses a caller-owned public
  calculation path and none of the research, review, forward-multiple,
  future-date, Full, feedback, or grilling branches applies.
- **Applicability:** common for repository-backed valuations; fixture frequency
  does not establish prevalence.
- **Expected control deficit:** preload the full runbook and unrelated reference
  sections, then select the bundled gateway despite the caller-owned path.
- **Protected wrong-condition behavior:** an unsupported non-FCFF/RI method
  returns a capability gap without bundled fallback or improvised arithmetic.
- **Authority:** read-only fresh-agent sampling. No sample could mutate the
  control, candidate, repository, or external state.

## Frozen bytes, host, and inputs

- Control commit: `96b7d0fa325b3a8cbffdede6c73d66c97da24ce2`.
- Control Git blobs: `SKILL.md`
  `98aabb135773e303f6cc8e6c893bf69f67b0640c`; runbook
  `914ac992f2c5626338cc945a1a093fc9cbc887fa`.
- Candidate Git blobs: `SKILL.md`
  `5eb064b1ea725da2c8dacc65e58af428ebf31bbe`; runbook
  `b961a98d56f9fb88c24b368f19d10c21e93e456f`.
- Candidate SHA-256: `SKILL.md`
  `3296F3C1CBCC1E1767512B2540A9E7AFBD1A9D0E1A1243B60A2547FEA8EFFB00`;
  runbook
  `6CD652890762CFA7938BE10318C8985052AD2EAC6A9C41DC7BAACE07D482448E`.
- Host/runtime: Codex desktop fresh explorer-agent contexts. Model, reasoning,
  and service-tier telemetry were unavailable. Tools were read-only shell reads
  of the named bytes. Arms ran in waves because six worker slots were available.

Each control sample was instructed to read only the two files from the control
commit with `git show`. Each candidate sample was instructed to read only the
current two candidate files and not inspect the control.

### Entry-positive prompt

```text
You are beginning an ordinary Compact FCFF valuation in a caller repository
that declares its own current calculator contract and public calculation path.
There is no research gap, independent review request, forward P/E/PEG request,
future-date output, Full request, run-feedback request, or grilling request.
Do not perform the valuation. Return exactly: (1) what complete files/sections
the contract requires you to load before company-specific evidence, (2) which
calculation path it requires after Model Lock freeze, (3) which branch-only
references it requires in this scenario.
```

### Wrong-condition prompt

```text
An asset-based NAV method is admitted, no caller-owned calculator path exists,
and the user did not request FCFF, residual income, forward multiples, research,
review, or feedback. Do not perform valuation. Return exactly: calculator path
selected; capability disposition; branch-only references loaded.
```

## Rubric

Entry-positive candidate passes only when it:

1. does not require the complete runbook at startup;
2. names only the phase required before company-specific evidence and defers
   later phase/branch material until its trigger;
3. selects the declared caller-owned FCFF calculation path exclusively; and
4. does not load research, review, forward-multiple, future-date, Full,
   feedback, grilling, or bundled-fallback material.

Wrong-condition candidate passes only when it selects no calculator, returns an
unsupported-method capability gap with an unlock condition, does not use the
bundled FCFF/RI fallback or manual arithmetic, and loads no unrelated branch.
Naming the selected NAV method section is allowed because it is method fit, not
an unrelated conditional branch.

## Per-sample results

| Sample | Arm | Entry-positive disposition |
| --- | --- | --- |
| `/root/eval_control_1` | Control | Full runbook and source protocol; unconditional method/MOS/assertion material; bundled gateway; Compact report. Deficit. |
| `/root/eval_control_2` | Control | Full runbook; source protocol; method/MOS/assertions; bundled gateway; Compact report. Deficit. |
| `/root/eval_control_3` | Control | Full runbook and source protocol; method/MOS/assertions; bundled gateway; Compact report. Deficit. |
| `/root/eval_control_4` | Control | Full invariant and runbook; source protocol; method/MOS/assertions; bundled gateway; Compact report. Deficit. |
| `/root/eval_control_5` | Control | Full runbook; source protocol; method/MOS/assertions; bundled gateway; Compact report. Deficit. |
| `/root/eval_candidate_1` | Candidate | Section 1 before evidence; caller FCFF path only; no conditional branch. Pass. |
| `/root/eval_candidate_2` | Candidate | Sections 1 then 2 at their boundaries; caller FCFF path only; Compact at composition; no unrelated branch. Pass. |
| `/root/eval_candidate_3` | Candidate | Section 1 before evidence; caller FCFF path only; no conditional branch. Pass. |
| `/root/eval_candidate_4` | Candidate | Sections 1 then 2 at their boundaries; caller FCFF path only; selected method/assertions and Compact only when reached. Pass. |
| `/root/eval_candidate_5` | Candidate | Section 1 before evidence; caller FCFF path only; assertions/Compact only when reached. Pass. |

| Sample | Arm | Wrong-condition disposition |
| --- | --- | --- |
| `/root/eval_control_1` through `/root/eval_control_5` | Control | Each selected no calculator, returned an unsupported-method gap, avoided manual arithmetic, and loaded Compact only. Protected. |
| `/root/eval_candidate_1` | Candidate | No calculator; capability gap with public-NAV-path unlock; no branch. Protected. |
| `/root/eval_candidate_2` | Candidate | No calculator; capability gap with public-NAV-path unlock; no bundled/manual path or branch. Protected. |
| `/root/eval_candidate_3` | Candidate | No calculator; capability gap with public-NAV-path unlock; no branch. Protected. |
| `/root/eval_candidate_4` | Candidate | No calculator; capability gap with verified-NAV-path unlock; selected NAV method section only. Protected. |
| `/root/eval_candidate_5` | Candidate | No calculator; capability gap with caller-owned-NAV-path unlock; no branch. Protected. |

## Aggregate and decision

- Entry-positive control deficit: `5/5`.
- Entry-positive candidate contribution: `5/5` pass.
- Wrong-condition protection: control `5/5`; candidate `5/5`.
- Variance: no behavioral variance in path selection, gap policy, or unrelated
  branch loading. Candidate wording varied only in whether later selected-method,
  assertion, and Compact sections were mentioned in the response.
- Worst candidate result: entry-positive sample 4 listed the selected FCFF and
  calculation-assertion sections; wrong-condition sample 4 listed the selected
  NAV method section. Both are permitted by the rubric and loaded no unrelated
  branch.
- Critical failures: none.
- Protocol deviations: none material. Samples were reused after documentation
  repair because frozen bytes, prompts, host, tools, and runtime identity were
  unchanged, as permitted by the evaluation contract.
- **Decision:** `accept`.
- **Residual transfer gap:** the evaluation proves the frozen Compact FCFF and
  unsupported-NAV routes, not every issuer, method, or reference combination.
