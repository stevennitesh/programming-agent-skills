# Pre-PR Review Skill Ideas

This document collects ideas for a future `pre-pr-review` skill: a local Codex review gate that behaves more like a serious PR reviewer than a generic "look this over" prompt.

The goal is not to copy CodeRabbit or any other product. The useful target is the same behavior profile: diff-aware, repo-aware, evidence-bound, low-noise, severity-calibrated, and able to use specialist review lenses when the change is risky.

## Source Evidence

Inputs inspected:

- User-provided June 5, 2026 research and recommendation conversation about CodeRabbit, Codex review, Greptile, Qodo, Ellipsis, Copilot review, and local pre-PR review.
- Current pack guidance:
  - `skills/author-skills/SKILL.md:12-28` for deciding what belongs in a reusable skill, reference, script, or repo doc.
  - `skills/author-skills/SKILL.md:40-53` for failure examples, trigger-focused descriptions, validation, and evidence labels.
  - `skills/author-skills/SKILL.md:55-101` for concrete behavior wording and pressure tests.
  - `skills/subagent-workflow/SKILL.md:12-20` for parent-owned review, bounded subagent packets, and subagent reports as evidence rather than proof.
  - `skills/subagent-workflow/SKILL.md:67-88` and `skills/subagent-workflow/templates/spec-reviewer.md:1-23` / `skills/subagent-workflow/templates/quality-reviewer.md:1-24` for spec review before quality review.
  - `skills/subagent-workflow/SKILL.md:186-199` for review triage, deduplication, ranking, and verification.
  - `skills/verify-before-done/SKILL.md:18-59` and `skills/verify-before-done/SKILL.md:83-107` for mapping review/readiness claims to fresh evidence.
  - `skills/github-tracking/SKILL.md:260-287` for treating review feedback as claims to verify before changing code.
  - `skills/tdd-slice/SKILL.md:20-41` and `skills/tdd-slice/SKILL.md:80-100` for caller-facing test surface and real-behavior checks.
- Local `.tmp` inspiration:
  - `.tmp/superpowers/skills/requesting-code-review/SKILL.md:8-46` for precise reviewer packets, commit ranges, and severity handling.
  - `.tmp/superpowers/skills/requesting-code-review/code-reviewer.md:23-74` for review axes: plan alignment, code quality, architecture, tests, and production readiness.
  - `.tmp/superpowers/skills/requesting-code-review/code-reviewer.md:76-121` for clear issue output and anti-vague-review rules.
  - `.tmp/superpowers/skills/receiving-code-review/SKILL.md:14-24` and `.tmp/superpowers/skills/receiving-code-review/SKILL.md:67-111` for verifying reviewer feedback before implementing and testing one item or group at a time.
  - `.tmp/superpowers/skills/subagent-driven-development/SKILL.md:8-14` and `.tmp/superpowers/skills/subagent-driven-development/SKILL.md:104-120` for fresh subagent context, spec-before-quality review, and not retrying a blocked agent unchanged.
  - `.tmp/superpowers/skills/verification-before-completion/SKILL.md:16-50` and `.tmp/superpowers/skills/verification-before-completion/SKILL.md:102-105` for evidence-before-claims and checking subagent output independently.
  - `.tmp/mattpocock-skills/skills/in-progress/review/SKILL.md:8-23` for pinning a fixed point and reviewing a three-dot diff.
  - `.tmp/mattpocock-skills/skills/in-progress/review/SKILL.md:25-63` for separate spec and standards sources.
  - `.tmp/mattpocock-skills/skills/in-progress/review/SKILL.md:65-78` for keeping review axes distinct so one pass does not mask another.
  - `.tmp/mattpocock-skills/skills/engineering/diagnose/SKILL.md:12-51` for building a fast, sharp, deterministic feedback loop.
  - `.tmp/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md:13-67` for assumptions, simplicity, surgical scope, and verifiable success criteria.
- System skill guidance:
  - `/home/steve/.codex/skills/.system/skill-creator/SKILL.md:28-54` for concision, right-sized specificity, and validation integrity.
  - `/home/steve/.codex/skills/.system/skill-creator/SKILL.md:56-147` for skill anatomy, optional scripts/references, avoiding extraneous files, and progressive disclosure.

## Product Lessons To Adapt

The pasted research points to these product behaviors as useful skill-design inputs:

- CodeRabbit-style breadth: path-scoped instructions, linked issue context, multi-repo/MCP/web context, local review surfaces, and linter/SAST integration. For a local Codex skill, adapt this as "collect the right repo evidence and explicitly read repo instructions/specs/checks before reviewing."
- Codex-style high signal: serious issues only when posting PR reviews. For a pre-PR local skill, keep blocking and should-fix findings tight, but allow optional test/check recommendations because local review can be a little broader than a public PR comment.
- Greptile-style defect hunting: whole-codebase reasoning. Locally, approximate this with call-site searches, contract tracing, changed-file ownership, and risk-lens review rather than pretending to maintain a persistent repository graph.
- Qodo-style governance: security, privacy, deployment, and policy controls. Locally, include a security/privacy/data lens and stop conditions for missing access, policy, or deployment evidence.
- Ellipsis-style simplicity: low-friction automation. The skill should be easy to invoke and should not require a heavy review platform ceremony for every small change.
- Copilot/GitHub-native review: use PR/issue/CI state when available, but keep the local skill useful before a PR exists.

## Design Target

The future skill should produce a local review report for one of these targets:

- current branch against a base branch,
- staged or uncommitted changes,
- one commit or commit range,
- an existing PR diff if the user provides a PR number or URL,
- a user-supplied diff.

It should answer:

1. What exactly was reviewed?
2. What repo instructions, specs, tests, and checks matter?
3. What risk profile does this diff have?
4. What concrete issues were introduced or exposed by the diff?
5. What missing tests or weak checks should be addressed before PR?
6. What validation should run before opening or updating the PR?
7. Is the branch safe to PR, PR-able after fixes, or not ready?

## Core Review Contract

A valid finding should satisfy all of these:

- Introduced or exposed by the target diff.
- Actionable by the author.
- Supported by source evidence, diff evidence, test evidence, a concrete execution path, or a violated public or caller contract.
- More important than formatter/linter noise.
- Includes file/line or symbol, mechanism, minimal fix, and validation.

The skill should suppress:

- vague "consider" comments,
- broad architecture preferences,
- style-only feedback already handled by tools,
- issues not caused by the diff,
- low-confidence guesses without a concrete failure mode,
- duplicate findings from multiple lenses,
- "proper infrastructure" suggestions without real callers or accepted scope.

## Review Axes

Use separate axes internally, even if the final output is deduplicated:

- Scope/spec alignment: Does the diff match the user request, issue, PRD, plan, or accepted non-goals?
- Repo standards: Does it violate documented repo instructions, `AGENTS.md`, ADRs, `CONTEXT.md` terms, public contracts, or explicit style/tooling rules?
- Correctness/regression: Could changed control flow, defaults, boundary handling, serialization, errors, or state changes be wrong?
- Tests/evidence: Would the current tests catch the important failures? Are checks real behavior checks or only mock/snapshot/internal-shape checks?
- Security/privacy: Auth, permissions, tenant/user isolation, secrets, injection, unsafe file/network access, sensitive logs.
- Data/schema/ML: Schema drift, leakage, joins, null handling, idempotency, partition/date boundaries, metric changes, reproducibility.
- Performance/concurrency: Hot path work, N+1s, unbounded scans, locks, async cancellation, retry amplification, races.
- Dependency/config/build/infra: Lockfiles, workflow changes, env/config compatibility, deployment/migration/rollback risk.
- Maintainability/API contract: Public signatures, request/response schemas, migration compatibility, error semantics, confusing ownership.
- UI/accessibility when relevant: caller-visible workflow, layout breakage, keyboard/screen-reader paths, loading/error states.

## Severity Model

Use three visible severities:

- Blocking: should stop the PR because it can plausibly break caller-visible behavior, security/privacy, data integrity, build/test/deploy, public API compatibility, migration/rollback, or severe performance.
- Should-fix: important before PR or before merge, but not obviously catastrophic. Typical examples are missing regression tests, limited edge-case bugs, weak error handling, moderate performance risk, or confusing contract assumptions.
- Optional: only high-leverage polish. Avoid optional style preferences.

The skill should allow "No blocking findings" and "No material findings" without padding the report.

## Suggested Skill Shape

Recommended skill name: `pre-pr-review`.

Trigger description should emphasize situations, not workflow summary:

```yaml
description: Use when reviewing a branch, commit, diff, or working tree before opening or updating a pull request; when the user asks for PR readiness, bug finding, regression review, security review, test-gap review, or a CodeRabbit-like local review.
```

Proposed package:

```text
skills/pre-pr-review/
  SKILL.md
  references/
    review-rubric.md
    reviewer-lenses.md
    severity.md
    output-format.md
    pressure-tests.md
  scripts/
    collect_review_context.sh
```

Keep `SKILL.md` as the route and behavior contract. Put long checklists and output templates in references. Add a script only if review-context collection keeps being repeated or guessed.

Do not add a skill-local `README.md`, installation guide, or changelog. Current repo convention is `SKILL.md` plus optional templates/references/scripts; repo-level docs can track design history.

## SKILL.md Core Procedure

The v1 `SKILL.md` should be compact:

1. Identify target and base.
   - If user supplies target/base, use it.
   - If target/base is missing and repo evidence cannot safely infer it, ask one blocking question.
   - Prefer three-dot diff for branch-vs-base review.
2. Read instructions and standards.
   - Root and nested `AGENTS.md`.
   - `CONTRIBUTING.md`, `CONTEXT.md`, ADRs, repo review docs, style docs, and tool configs when relevant.
   - User-specified spec/issue/plan if present.
3. Collect diff context.
   - `git status --short --branch`.
   - current branch and base/merge-base.
   - changed files and diff stat.
   - relevant diff hunks.
   - likely test/check commands from repo docs, Makefile, package scripts, pyproject, tox, CI, etc.
4. Classify risk.
   - Changed file types, source areas, public contracts, data/security/migration/dependency/config paths, and test impact.
5. Review.
   - Start with spec/scope alignment.
   - Then run integrated quality review with risk lenses.
   - Use optional subagents only when authorized and worth the overhead.
6. Validate findings.
   - Check each finding against current source/diff/callers/tests.
   - Deduplicate.
   - Drop low-confidence or off-diff comments.
7. Recommend checks.
   - List observed checks only if actually run or supplied in context.
   - List recommended checks and what they cover.
8. Report verdict.
   - `Safe to PR`, `PR after fixes`, or `Do not PR yet`.
   - Include confidence and remaining uncertainty.

## Context Collector Script Ideas

If a script is added, it should be read-only and conservative.

Inputs:

- base branch or commit, defaulting only when repo evidence is clear,
- optional target commit/range,
- optional `--include-diff` flag so huge diffs are not dumped by default.

Output:

- git status,
- current branch,
- merge-base,
- changed file names/status,
- diff stat,
- commit list,
- instruction/doc files detected,
- likely commands/checks detected,
- optional limited diff.

Rules:

- No writes.
- No dependency install.
- No network.
- No destructive git.
- Limit file reads to review-relevant docs/configs.
- Mark missing base/ambiguous repo state instead of guessing silently.
- Do not print secrets or `.env` contents.

This script should not replace review judgment. It just makes the first evidence packet repeatable.

## Subagent Gate

The default should be a single integrated review. Subagents are useful when breadth matters, but they increase cost and false positives.

Use subagents only when:

- the user explicitly asks for them,
- repo instructions or an approved plan requires them,
- the diff is broad or high-risk,
- the review can be split into agent-ready read-only packets.

Good subagent splits:

- spec/scope reviewer,
- correctness/regression reviewer,
- security/privacy reviewer,
- tests/evidence reviewer,
- data/schema/ML reviewer,
- performance/concurrency reviewer,
- build/dependency/infra reviewer.

Avoid subagents when:

- target/base/spec are unclear,
- each packet would need `TBD`,
- the change is tiny and local self-review is cheaper,
- lenses would all inspect the same few lines,
- delegation tools are unavailable.

Parent responsibilities:

- inspect reports against source/diff,
- deduplicate and rank,
- reject stale or unsupported findings,
- rerun or recommend relevant checks,
- produce one final report, not a transcript pile.

## Output Report

Recommended final report:

```text
## Scope Reviewed

- Target:
- Base:
- Diff shape:
- Key files:
- Instructions/specs read:
- Risk profile:

## Checks

Observed:
- <command/result/evidence, or None>

Recommended before PR:
- <command> - <what it covers>

## Blocking Findings

No blocking findings.

or

### B1. <title>
- Severity: blocking
- File/line:
- Issue:
- Mechanism:
- Minimal fix:
- Validation:

## Should-Fix Findings

No should-fix findings.

or same finding shape.

## Missing Tests Or Weak Evidence

No material test gaps found.

or
- Gap:
- Failure it should catch:
- Suggested check:

## Optional Improvements

Only include unusually high-leverage optional items.

## Verdict

- Verdict: Safe to PR | PR after fixes | Do not PR yet
- Confidence: low | medium | high
- Remaining uncertainty:
- Next action:
```

For normal chat output, this can be shortened, but the skill should preserve the same fields when the review is nontrivial.

## Review Learning Loop

The skill should include a small feedback loop without turning it into a platform:

- If human, Codex GitHub review, CodeRabbit, CI, or another reviewer later finds an issue local review missed, classify the miss:
  - missing context source,
  - weak risk lens,
  - skipped deterministic check,
  - poor finding standard,
  - bad severity calibration,
  - repo-specific rule missing from `AGENTS.md` or review docs.
- If the miss is repo-specific and likely to recur, update repo docs or nested `AGENTS.md`.
- If the miss is general pre-PR review behavior, add a pressure test or skill wording change.
- If a repeated operation is fragile, add or update a script.

This borrows the useful part of reviewer tools that "learn" from feedback, while keeping durable learning in repo artifacts rather than chat memory.

## Pressure Tests For The Skill

Add at least these pressure tests before claiming the skill changes review behavior.

### 1. False Positive Suppression

Failure example:

The reviewer reports broad style or architecture preferences that are not introduced by the diff.

Pressure condition:

A small diff changes one function in a file with pre-existing messy style and nearby unrelated dead code.

Expected behavior:

Report only diff-introduced actionable issues. Mention unrelated cleanup separately only if useful, not as a finding.

Evidence type:

Instruction review for v1; execution test before claiming low-noise behavior is proven.

### 2. Spec Gap Beats Quality Praise

Failure example:

The review praises clean implementation but misses that one requested behavior is absent.

Pressure condition:

Spec asks for two behavior changes; diff implements one cleanly and adds tests for only that one.

Expected behavior:

Block or warn on missing requirement before quality approval. Quality review must not mask spec failure.

Evidence type:

Execution test preferred.

### 3. Missing Test Surface

Failure example:

The reviewer accepts private-helper tests for caller-visible behavior.

Pressure condition:

Diff adds an API/CLI behavior but tests only a private helper or mock call.

Expected behavior:

Flag weak test evidence and suggest the highest practical caller-facing check.

Evidence type:

Execution test preferred because this is a common agent rationalization.

### 4. Risky Data Pipeline

Failure example:

The reviewer treats a data/schema change like normal application code and misses silent corruption risk.

Pressure condition:

Diff touches schema, date partitioning, null handling, or train/eval split logic.

Expected behavior:

Use data/schema/ML lens; check leakage, drift, idempotency, joins, partition boundaries, and reproducibility.

Evidence type:

Instruction review acceptable for first draft; execution test on a scratch fixture later.

### 5. Subagent Overuse

Failure example:

The skill spawns many reviewers for a trivial diff, increasing noise and cost.

Pressure condition:

Tiny docs or one-line code fix; user asks "review this before PR" but does not ask for deep review.

Expected behavior:

Do local integrated review, record that subagents were skipped because scope is small.

Evidence type:

Simulated fresh-agent test acceptable initially.

### 6. Subagent Report Trusted As Proof

Failure example:

Parent forwards subagent output as the final review without checking source or deduplicating.

Pressure condition:

Two reviewers report overlapping and conflicting findings; one is stale or not diff-caused.

Expected behavior:

Parent verifies against source/diff, rejects unsupported findings, deduplicates, and reports one ranked list.

Evidence type:

Execution test preferred.

### 7. Deterministic Check Ignored

Failure example:

The reviewer spends tokens on issues that lint/typecheck/test output already proves or disproves.

Pressure condition:

Repo has obvious targeted commands in README/Makefile and a known failing check output is available.

Expected behavior:

Read commands/output, distinguish observed from recommended checks, and prioritize semantic issues not already covered by tooling.

Evidence type:

Instruction review plus one execution test.

### 8. Ambiguous Base

Failure example:

The reviewer silently compares against the wrong base branch.

Pressure condition:

Repo has `main`, `master`, and a feature branch; user says "review this branch" with no base.

Expected behavior:

Infer only if repo evidence is strong. Otherwise ask one blocking question or state a reversible assumption before review.

Evidence type:

Instruction review.

### 9. External Reviewer Feedback

Failure example:

After PR creation, the agent blindly implements a CodeRabbit-style suggestion that is stale or out of scope.

Pressure condition:

External feedback suggests "proper" abstraction or broad infra without real callers.

Expected behavior:

Verify against current source, caller usage, accepted scope, and tests. Fix, push back, clarify, or defer with evidence.

Evidence type:

Can live in `github-tracking`/`verify-before-done`, but `pre-pr-review` should cross-reference it.

## Open Design Decisions

- Should `pre-pr-review` be a new top-level skill, or should its core fit into `verify-before-done` plus `subagent-workflow` templates? Recommendation: new skill, because "pre-PR review" is a distinct user-triggered job with a different output contract.
- Should it include its own reviewer templates or reuse `subagent-workflow/templates/spec-reviewer.md` and `quality-reviewer.md`? Recommendation: reuse existing templates when dispatching generic spec/quality reviewers; add only review-specific lens references.
- Should the skill run commands automatically? Recommendation: read documented commands and run cheap focused checks only when review confidence depends on them and normal repo permissions allow it. Otherwise recommend them with coverage notes.
- Should the skill support GitHub PR review threads? Recommendation: not in v1. Handoff to `github-tracking` for live PR comments, CI, review-thread state, and resolution.
- Should it include a review log for 10 PRs? Recommendation: reference as an optional repo doc pattern, not part of the runtime skill.
- Should it mimic CodeRabbit path instructions? Recommendation: use nested `AGENTS.md` and optional repo `docs/code_review.md`; do not invent a separate rule format unless repeated usage shows a gap.

## Recommended V1 Slice

Implement v1 in this order:

1. Add `skills/pre-pr-review/SKILL.md` with target/base detection, finding standard, risk profile, subagent gate, and final output contract.
2. Add `references/severity.md`, `references/reviewer-lenses.md`, and `references/output-format.md`.
3. Add pressure tests under `docs/pressure-tests/` before claiming behavior is proven.
4. Update `README.md` skill map.
5. Run `./scripts/validate-skills.sh`.
6. Do one instruction review against this document and one small execution test on a scratch repo/diff before installing globally.

Acceptance criteria for the skill:

- It triggers for pre-PR review, branch review, working-tree review, PR readiness, bug-finding review, test-gap review, and CodeRabbit-like local review.
- It does not trigger for implementation, broad planning, or style-only cleanup.
- It identifies review target/base or asks one material question.
- It reads repo instructions and available specs before findings.
- It ranks findings by blocking/should-fix/optional.
- Each finding has mechanism, evidence, smallest fix, and validation.
- It separates observed checks from recommended checks.
- It uses subagents only when authorized and useful.
- It names review path and residual uncertainty before readiness claims.

## Non-Goals For V1

- No persistent repo graph.
- No web search by default.
- No multi-repo analysis unless the user supplies the related repo and reason.
- No automatic fixes.
- No automatic PR comments.
- No SAST/linter replacement.
- No giant checklist pasted into every review.
- No claim that the skill matches a paid reviewer benchmark.

The best v1 is a sharp local reviewer: small enough to load reliably, strict enough to suppress noise, and structured enough to catch the failures generic review prompts often miss.
