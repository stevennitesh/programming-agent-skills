# Pre-PR Review Sample Template

Copy this file for each review sample. Suggested path:

```text
docs/pre-pr-review-samples/<sample-id>-<repo-or-topic>.md
```

Keep raw review transcripts short. Link or summarize long outputs instead of pasting everything.

## Sample Metadata

Sample ID:

Repo:

Date captured:

Reviewer:

Sample type: real | fixture

Risk profile:

Target:

Base:

Comparison command:

Spec, issue, PRD, or user request:

External evidence available:

## Repo Evidence Read

Instructions and standards:

- `AGENTS.md`:
- nested `AGENTS.md`:
- review docs:
- `CONTEXT.md` or ADRs:
- README/contributing:
- tool configs:

Source evidence:

- changed files:
- callers checked:
- tests/fixtures checked:
- CI/check output checked:

Command discovery:

- source of commands:
- commands found:
- commands run:
- commands skipped and why:

## Known Ground Truth

Use this when a sample has external evidence or an intentional fixture bug.

Known true issues:

1. TODO

Known non-issues / tempting false positives:

1. TODO

Expected verdict:

Remaining uncertainty:

## Review Mode: Baseline

Prompt used:

```text

```

Observed checks:

- TODO

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  | yes/no/partial |  | strong/weak/none |  |

Missed issues:

- TODO

False positives/noise:

- TODO

Verdict:

## Review Mode: Structured Prompt

Prompt used:

```text

```

Observed checks:

- TODO

Findings:

| Finding | Severity reported | True positive? | Miss/noise label | Evidence quality | Notes |
| --- | --- | --- | --- | --- | --- |
|  |  | yes/no/partial |  | strong/weak/none |  |

Missed issues:

- TODO

False positives/noise:

- TODO

Verdict:

## Review Mode: Selective Subagents

Use only when the diff is high-risk or broad.

Subagent gate:

- Authorized by:
- Why fan-out was useful:
- Lenses used:
- Lenses skipped:

Findings before parent deduplication:

- TODO

Parent synthesis:

- accepted findings:
- rejected findings:
- duplicate findings:
- final verdict:

Did subagents add unique value?

Did subagents add noise?

## External Review Comparison

External source: human | Codex GitHub | CodeRabbit | CI | other

External findings:

- TODO

Local review caught:

- TODO

Local review missed:

- TODO

Local review found valid issue external review missed:

- TODO

## Classification

Miss labels:

- [ ] wrong-base
- [ ] missed-spec-gap
- [ ] missed-contract-risk
- [ ] missed-correctness
- [ ] missed-security-data
- [ ] missed-test-gap
- [ ] missed-check-output
- [ ] missed-performance-concurrency
- [ ] missed-context-source

Noise labels:

- [ ] off-diff
- [ ] style-only
- [ ] speculative
- [ ] broad-rewrite
- [ ] duplicate
- [ ] stale
- [ ] wrong-severity
- [ ] unsupported

## Skill Implications

Rules to add or strengthen:

- TODO

Reference checklist items:

- TODO

Script/context collection needs:

- TODO

Subagent gate implications:

- TODO

Repo-specific guidance needed instead:

- TODO

## Summary For Ledger

One-line summary:

Best evidence:

Biggest miss:

Worst noise:

Decision implication:
