---
name: review
description: "Review ordinary branch, WIP, staged, or \"review since X\" diffs read-only from a fixed point. Judge Standards (\"built right?\") and Spec (\"right thing?\") as two separate axes. Hand off local PRs or high-risk local diffs to $convergent-pr-review."
---

# Review

**Pin. Trace. Judge. Report.**

Review one ordinary diff read-only from a known-good point.

- **Standards:** built right? Judge the diff against documented repo rules, meaningful nearby conventions, and the smell baseline when standards are thin.
- **Spec:** right thing? Judge the diff against the originating request, bounded slice, acceptance criteria, and required proof.

Keep the **two axes** separate. Never merge, deduplicate, rerank, or select a winner across axes; one passing axis cannot hide a failing one.

**Spec gate:** The caller supplies `Spec required: yes | no`. Default to `no` for standalone review. When `yes`, a missing, conflicting, or unresolved Spec source makes the review `incomplete`; never skip or replace the Spec axis.

**Review route:** Hand off to `$convergent-pr-review` and stop for local PRs or high-risk local diffs. Carry the caller-supplied Spec requirement, Source Trace and Spec sources, fixed point, and captured target into the handoff.

## 1. Pin The Target

Use the supplied fixed point. Otherwise discover the repository default branch and merge base, state the resolved baseline, and ask only when discovery is ambiguous.

Select the target:

- immutable tree: `git diff <fixed-point> <review-tree>`
- committed branch: `git diff <fixed-point>...HEAD`
- working tree: `git diff <fixed-point>`
- staged only, when explicitly requested: `git diff --cached`

A supplied `<review-tree>` wins over every live target. Verify it with `git cat-file -e <review-tree>^{tree}` and inspect its files with `git show <review-tree>:<path>`.

For staged-only review, record the fixed point for context; review only `git diff --cached`.

Capture:

- resolved fixed point: `git rev-parse <fixed-point>`
- selected diff command
- `git status --short`
- relevant commits: `git log <fixed-point>..HEAD --oneline`

For a working-tree target, read every in-scope untracked file directly; Git diff omits them.

**Fail fast** when the fixed point or review tree does not resolve, the complete target cannot be captured, or the target is empty.

## 2. Trace The Sources

Build the **Source Trace** before judging the diff.

Trace Spec in this order:

1. The current request or caller-supplied selected item, bounded slice, acceptance criteria, path, issue, URL, spec, or legacy PRD.
2. Issue or PR references in captured commit messages, using `docs/agents/issue-tracker.md` when available.
3. A matching spec, legacy PRD, or issue packet under the repo's documented conventions, including `docs/`, `specs/`, and `.scratch/`.

When `Spec required: yes`, return `incomplete` unless one authoritative source resolves without an unresolved conflict. When `Spec required: no` and none resolves, skip the axis and report `Skipped: no spec available`.

Trace Standards through `AGENTS.md`, `docs/agents/engineering-contract.md`, contributor and coding standards, README guidance, formatter or linter configuration, test documentation, and meaningful nearby conventions.

When Standards are thin, read [SMELL-BASELINE.md](SMELL-BASELINE.md). Repo standards override it; every smell remains a `baseline judgement call`. Leave tooling-enforced style to tooling.

## Finding Contract

Report only actionable findings. Trace every finding to a location and governing source or code evidence.

Every finding includes:

- severity
- location
- evidence
- risk
- required change

Severity:

- **P0:** catastrophic failure, data loss, or exploitable security flaw.
- **P1:** merge-blocking correctness or contract failure.
- **P2:** significant risk or missing required validation.
- **P3:** lower-risk but actionable correctness or maintainability problem.

Standards findings also identify their type: `documented-standard breach` or `baseline judgement call`.

## 3. Judge The Axes

Run single-agent: **Standards -> lens reset -> Spec**.

### Standards

Judge only against the traced Standards sources.

Report documented-standard breaches and meaningful baseline judgement calls. Skip style nits already enforced by tooling unless the diff bypasses or changes that tooling contract.

### Lens Reset

Set Standards findings aside. Start the Spec axis from the pinned target and traced Spec source; do not carry Standards judgments across.

### Spec

Judge only against the traced Spec source.

Report omissions, incorrect behavior, scope creep, and proof gaps, including load-bearing behavior not demonstrated through a useful interface or seam.

Skip this axis only when the Spec gate permits it.

## 4. Report

Begin with:

```markdown
Review target: <resolved fixed point> | <diff command> | <review tree or live target>
Sources: Standards: <sources>. Spec: <source or skipped>.
```

Use exactly these headings:

```markdown
## Standards

<findings or "No findings.">

## Spec

<findings or "No findings." / "Skipped: no spec available.">
```

End with:

```markdown
Summary: Standards: <count>, worst <severity or none>. Spec: <count/skipped>, worst <severity or none>.
```

## Completion Criteria

Complete when the target is pinned and non-empty; Standards sources are named; required Spec resolves or optional Spec is explicitly skipped; both applicable axes run with a lens reset; every finding meets the finding contract; and the read-only report names the target, sources, and per-axis summary.
