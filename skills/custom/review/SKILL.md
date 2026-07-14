---
name: review
description: "Review ordinary branch, WIP, staged, or \"review since X\" diffs read-only from a fixed point. Judge Standards (\"built right?\") and Spec (\"right thing?\") as two separate axes. Hand off local PRs or high-risk local diffs to $convergent-pr-review."
---

# Review

**Pin. Trace. Judge. Report.**

Own one ordinary, read-only fixed-point review.

**Read-only:** Inspect only. Leave the worktree, index, commits, tracker, PR comments or reviews, and external messages unchanged.

- **Standards:** built right, against repository rules, meaningful nearby conventions, and the fallback smell baseline when standards are thin.
- **Spec:** right thing, against the authoritative request, bounded slice, acceptance criteria, and required proof.

Keep the axes separate. Never merge, deduplicate, or rerank findings across them.

**Review route:** For a local PR or high-risk local diff, hand off to `$convergent-pr-review` and stop. Carry the caller-supplied Spec requirement, Source Trace and Spec sources, fixed point, and target inputs; `$convergent-pr-review` owns snapshot capture.

**Spec gate:** The caller supplies `Spec required: yes | no`. Default to `no` for standalone review. When `Spec required: yes`, a missing, conflicting, or unresolved authoritative source makes the review `incomplete`; never skip or replace the Spec axis.

An incomplete review returns:

```text
Review status: incomplete
Review target: <resolved target or unresolved>
Sources: Standards: <sources or not traced>. Spec: <source or unresolved>.
Blocker: <unresolved ref | empty or incomplete target | missing or conflicting Spec>
Skipped: judgment did not run.
```

## 1. Pin

Resolve the supplied fixed point to a commit SHA. Otherwise discover the repository default branch and merge base, record the resolved commit, and ask only when discovery is ambiguous.

Select one target:

- review tree: `git diff <fixed-point> <review-tree>`
- committed branch: `git diff <fixed-point> HEAD`
- working tree: `git diff <fixed-point>`
- explicitly staged only: `git diff --cached`

A supplied review tree wins over every live target. Verify `<review-tree>^{tree}` and inspect its files through `git show`. For staged-only review, record the fixed point but review only the cached diff.

Capture the resolved fixed point, selected diff command, `git status --short`, and relevant commits. Read in-scope untracked files directly for working-tree review.

Fail when a ref does not resolve, the complete target cannot be captured, or the target is empty.

## 2. Trace

Build one **Source Trace** before judgment.

Trace Spec in order:

1. Current request or caller-supplied item, slice, criteria, path, issue, URL, spec, or legacy PRD.
2. Issue or PR references in captured commits, following `docs/agents/issue-tracker.md` when available.
3. A matching source under repository conventions such as `docs/`, `specs/`, or `.scratch/`.

When Spec is required, stop `incomplete` unless one authoritative source resolves without conflict. When optional and absent, report `Skipped: no spec available`.

Trace Standards from `AGENTS.md` and its pointers, contributor or coding guidance, test and tooling configuration, and meaningful nearby conventions. When these are thin, read [SMELL-BASELINE.md](SMELL-BASELINE.md). Repository standards override it; label each smell a `baseline judgement call`; leave tooling-enforced style to tooling.

## 3. Judge

Run **Standards -> lens reset -> Spec**.

Report only actionable findings. Each finding includes severity, location, evidence, risk, and required change. Standards findings also say `documented-standard breach` or `baseline judgement call`.

- **P0:** catastrophic failure, data loss, or exploitable security flaw.
- **P1:** merge-blocking correctness or contract failure.
- **P2:** significant risk or missing required validation.
- **P3:** lower-risk actionable correctness or maintainability problem.

Judge Standards from its traced sources. Set those findings aside, reset to the pinned target and Spec source, then judge Spec for omissions, incorrect behavior, scope creep, and proof gaps through useful interfaces or seams.

## 4. Report

Use exactly:

```markdown
Review status: complete
Review target: <resolved fixed point> | <diff command> | <review tree or live target>
Sources: Standards: <sources>. Spec: <source or skipped>.

## Standards

<findings or "No findings.">

## Spec

<findings or "No findings." / "Skipped: no spec available.">

Summary: Standards: <count>, worst <severity or none>. Spec: <count/skipped>, worst <severity or none>.
```

Complete only when `Pin` and `Trace` pass, both applicable axes run with a lens reset, and the report satisfies the finding contract.
