---
name: review
description: "Review one ordinary branch, WIP, staged, or \"review since X\" diff read-only from a fixed snapshot. Judge Standards (\"built right?\") and Spec (\"right thing?\") separately, then return one terminal report. Hand off local PRs or high-risk local diffs once to $convergent-pr-review."
---

# Review

**Pin. Trace. Admit. Judge. Return.**

Own one ordinary, read-only fixed-snapshot review.

**Terminal:** judge one immutable snapshot and return. Start no remediation, dispatch, tracker mutation, successor review, or snapshot recapture. The report grants no mutation or new-snapshot authority.

**Read-only:** Inspect only. Leave the worktree, index, commits, tracker, PR comments or reviews, and external messages unchanged.

- **Standards:** built right, against repository rules, meaningful nearby conventions, and the fallback smell baseline when standards are thin.
- **Spec:** right thing, against the authoritative request, bounded slice, acceptance criteria, and required proof.

**Lens reset:** keep the axes separate. Never merge, deduplicate, or rerank findings across them.

**Review route:** For a local PR or high-risk local diff, hand off once to `$convergent-pr-review` and stop. Carry the caller-supplied Charter, review mode, Spec requirement, Source Trace, fixed point, target inputs, and any carried finding IDs; `$convergent-pr-review` owns snapshot capture. Do not resume this skill when it returns.

**Spec gate:** The caller supplies `Spec required: yes | no`. Default to `no` for standalone review. When `Spec required: yes`, a missing, conflicting, or unresolved authoritative source makes the review `incomplete`; never skip or replace the Spec axis.

An incomplete review returns:

```text
Review status: incomplete
Review target: <resolved target or unresolved>
Sources: Standards: <sources or not traced>. Spec: <source or unresolved>.
Blocker: <unresolved ref | empty or incomplete target | missing or conflicting Spec>
Skipped: judgment did not run.
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

## 1. Pin

Resolve the supplied fixed point to a commit SHA. Otherwise discover the repository default branch and merge base, record the resolved commit, and ask only when discovery is ambiguous.

Select one target:

- review tree: `git diff <fixed-point> <review-tree>`
- committed branch: `git diff <fixed-point> HEAD`
- working tree: `git diff <fixed-point>`
- explicitly staged only: `git diff --cached`

A supplied review tree wins over every live target. Verify `<review-tree>^{tree}` and inspect its files through `git show`. For staged-only review, record the fixed point but review only the cached diff.

Capture the resolved fixed point, selected diff command, `git status --short`, and relevant commits. Read in-scope untracked files directly for working-tree review. Record `Review mode: initial | remediation`; default to `initial`. Remediation mode requires the original Charter, prior snapshot, carried finding IDs, and repair delta.

Return `incomplete` when a ref does not resolve, the complete target cannot be captured, or the target is empty.

## 2. Trace

Build one **Source Trace** before judgment.

Trace Spec in order:

1. Current request or caller-supplied item, slice, criteria, path, issue, URL, spec, or legacy PRD.
2. Issue or PR references in captured commits, following `docs/agents/issue-tracker.md` when available.
3. A matching source under repository conventions such as `docs/`, `specs/`, or `.scratch/`.

When Spec is optional and absent, report `Skipped: no spec available`.

Trace Standards from `AGENTS.md` and its pointers, contributor or coding guidance, test and tooling configuration, and meaningful nearby conventions. When these are thin, read [SMELL-BASELINE.md](SMELL-BASELINE.md). Repository standards override it; label each smell a `baseline judgement call`; leave tooling-enforced style to tooling.

## 3. Admit

Read [FINDING-CONTRACT.md](FINDING-CONTRACT.md). Apply its Anchor, Reach, Evidence, Impact, and Proportion gates before severity. Preserve the caller's Charter; when none is supplied for standalone review, use the requested slice and resolved Source Trace as the boundary.

## 4. Judge

Run **Standards -> lens reset -> Spec**.

Report only admitted findings through the shared finding interface. Standards findings also say `documented-standard breach` or `baseline judgement call`.

Judge Standards from its traced sources, then reset to the pinned target and Spec source. Judge Spec for omissions, incorrect behavior, scope creep, and proof gaps through useful interfaces or seams.

## 5. Return

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
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

**Complete:** Pin and Trace pass; every reported finding passes Admit; both applicable axes run with a lens reset; the report satisfies the finding contract; and control returns without mutation or successor review.
