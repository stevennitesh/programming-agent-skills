# Pre-PR Review Evidence Plan

Use this plan to gather enough real evidence before creating the `pre-pr-review` skill.

The goal is to learn where a local Codex review gate actually needs structure: target/base detection, repo context collection, spec-first review, finding quality, subagent gating, command discovery, and readiness reporting.

## Evidence Questions

Collect evidence that answers these questions:

1. What does plain Codex review already catch without a new skill?
2. What does it miss when using only the current repo instructions?
3. Which findings are noisy, stale, off-diff, or style-only?
4. Which repo evidence sources matter most: `AGENTS.md`, review docs, issue/PRD, tests, Makefile, CI, config, callers, or fixtures?
5. Which deterministic checks should run before or after review?
6. Which review lenses add real value for high-risk changes?
7. When do subagents improve coverage, and when do they only add cost/noise?
8. Which repeated misses should become skill rules, reference checklists, or scripts?

## Sample Set

Gather at least six samples before writing the skill.

### Real Repo Samples

Use 3-5 real diffs from different projects or risk types:

- Normal application behavior change.
- Data/ML/schema/pipeline change.
- Config/build/CI/dependency/infra change.
- Security/auth/permission-sensitive change, if available.
- Small low-risk change to test false-positive suppression.

Prefer samples where later evidence exists, such as human review, CI, CodeRabbit, Codex GitHub review, or a bug found after review.

### Fixture Samples

Create 3 scratch fixture diffs later, after the real samples show the most common failure modes:

- Clean implementation that misses one spec requirement.
- Caller-visible behavior tested only through a private helper or mock call.
- Risky data/schema diff with one true issue and several tempting false positives.

Do not build fixtures first unless no real samples are available.

## Review Modes To Compare

For each sample, run at least two modes:

1. Baseline local review:
   - Current Codex behavior without the future skill.
   - Use only normal repo instructions and the user prompt.

2. Structured local review prompt:
   - Use the proposed contract from `docs/2026-06-05-pre-pr-review-skill-ideas.md`.
   - Ask for target/base, risk profile, blocking findings, should-fix findings, missing tests, recommended checks, and verdict.

For high-risk samples only, add:

3. Selective subagent review:
   - Use separate read-only lenses only when the diff is broad or risky.
   - Deduplicate findings manually in the parent report.

If a repo already has external review evidence, also capture:

4. External comparison:
   - Human review, CI/check failures, Codex GitHub review, CodeRabbit, or another review bot.

## Standard Review Prompt

Use this prompt for structured local review runs:

```text
Review this target as a pre-PR review.

Target:
Base:
Spec or request:

Use repo instructions, relevant docs, current source, tests, and diff evidence.

Report only findings that are:
- introduced or exposed by this diff,
- actionable by the author,
- supported by source/diff/test evidence or a concrete execution path,
- more important than formatter/linter noise.

Prioritize correctness, security/privacy, data integrity, public or caller contracts, missing tests, dependency/config risk, migration/rollback risk, performance/concurrency, and CI/build risk.

Return:
1. Scope reviewed
2. Checks observed
3. Checks recommended before PR
4. Blocking findings
5. Should-fix findings
6. Missing tests or weak evidence
7. Optional improvements only if high leverage
8. Verdict: Safe to PR / PR after fixes / Do not PR yet
9. Confidence and remaining uncertainty
```

## Subagent Prompt

Use only for high-risk samples:

```text
Review this target against the base as a pre-PR review.

Use separate read-only review lenses where useful:
- spec/scope alignment,
- correctness/regression,
- security/privacy,
- tests/evidence,
- data/schema/ML,
- performance/concurrency,
- build/dependency/infra.

Each reviewer must report only issues introduced or exposed by the diff and must include evidence, mechanism, minimal fix, and validation.

Parent synthesis must:
- verify findings against source/diff,
- deduplicate,
- reject unsupported or off-diff findings,
- rank blocking / should-fix / optional,
- include one final verdict.
```

## Miss And Noise Taxonomy

Use these labels in the ledger and sample template.

### Miss Types

- `wrong-base`: review compared against the wrong target or base.
- `missed-spec-gap`: implementation missed a requirement or added scope creep.
- `missed-contract-risk`: public API, CLI, UI, config, schema, or caller contract drift.
- `missed-correctness`: logic, boundary, state, error path, serialization, or compatibility bug.
- `missed-security-data`: security, privacy, permission, data loss, leakage, or tenant isolation issue.
- `missed-test-gap`: weak or missing test/check for changed behavior.
- `missed-check-output`: command, CI, linter, typecheck, or test output was ignored or misread.
- `missed-performance-concurrency`: hot path, N+1, unbounded work, race, lock, async, or retry risk.
- `missed-context-source`: important repo instruction, issue, PRD, ADR, `CONTEXT.md`, or caller was not read.

### Noise Types

- `off-diff`: issue is not introduced or exposed by the diff.
- `style-only`: formatter/linter or preference-level comment.
- `speculative`: no concrete failure mechanism.
- `broad-rewrite`: suggests architecture or infrastructure beyond accepted scope.
- `duplicate`: same finding repeated across reviewers.
- `stale`: contradicted by current source or latest diff.
- `wrong-severity`: real issue ranked too high or too low.
- `unsupported`: no file/line, symbol, execution path, or contract evidence.

## Command Discovery Notes

For each repo, record where review-relevant checks came from:

- root or nested `AGENTS.md`,
- README or contributing docs,
- Makefile, justfile, npm scripts, pyproject, tox, cargo, go, etc.,
- CI workflow,
- prior PR body or issue,
- observed developer convention.

Record whether commands were:

- actually run,
- not run because too slow,
- not run because dependencies/access missing,
- not run because unrelated to the diff.

## Decision Rules After Evidence

Convert evidence into the skill this way:

- Repeated wrong-base or ambiguous-base issues -> add explicit target/base detection and one-question stop rule.
- Repeated missed spec gaps -> make spec/scope review the first review step.
- Repeated noisy findings -> tighten the finding standard and "do not report" list.
- Repeated test-surface misses -> add a tests/evidence lens and caller-facing check rule.
- Repeated command-discovery mistakes -> add `collect_review_context.sh`.
- Repeated high-risk blind spots -> add targeted lenses in `references/reviewer-lenses.md`.
- Repeated subagent noise -> strengthen subagent gate and parent deduplication rule.
- Repeated repo-specific misses -> update that repo's `AGENTS.md` or `docs/code_review.md`, not the portable skill.

## Done Criteria Before Skill Creation

Start the skill only after:

- At least 3 real samples are captured.
- At least 1 high-risk sample is captured.
- At least 1 low-risk sample is captured to test noise suppression.
- At least 2 review modes are compared for most samples.
- The ledger has repeated misses/noise summarized.
- The proposed v1 rules trace to observed evidence or an explicit pressure test.

If evidence is thin, create the fixture samples before writing the skill body.
