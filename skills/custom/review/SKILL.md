---
name: review
description: "Run ordinary fixed-point review for branch, WIP, staged, or \"review since X\" diffs. Keep Standards (\"built right?\") and Spec (\"right thing?\") as two axes, never merged. Use convergent-pr-review for local PRs or high-risk local diffs."
---

# Review

Run a read-only review of the selected diff from a known-good point.

This is the default Converge gate for ordinary branch, WIP, staged, and `$implement` closeout review.

- **Standards**: built right? Check documented repo conventions, the local engineering contract, meaningful nearby conventions, and the smell baseline when repo standards are thin.
- **Spec**: right thing? Check the originating request, issue, spec, bounded slice, acceptance criteria, and required proof.

Keep the **two axes, never merged**. One axis passing must not hide the other axis failing, and there is no single winner across axes.

Use `$convergent-pr-review` instead for local PR review or high-risk local-diff review that needs independent reviewer passes, scoped lenses, and a verified finding ledger.

## 1. Pin The Review Target

Use the fixed point the user or caller supplied. Otherwise discover the repository default branch and merge base, state the resolved baseline, and ask only when discovery is ambiguous.

Choose the review target:

- supplied immutable tree: `git diff <fixed-point> <review-tree>`
- committed branch: `git diff <fixed-point>...HEAD`
- uncommitted working tree: `git diff <fixed-point>`
- staged only, when explicitly requested: `git diff --cached`

A supplied `<review-tree>` wins over every live target. Verify it with `git cat-file -e <review-tree>^{tree}` and inspect snapshot content with `git show <review-tree>:<path>`, not the live worktree.

For staged-only review, record the fixed point for context; the reviewed diff remains `git diff --cached`.

Capture:

- fixed point resolution: `git rev-parse <fixed-point>`
- selected diff command
- `git status --short`
- commit list when relevant: `git log <fixed-point>..HEAD --oneline`

For working-tree review, read every in-scope untracked file directly; Git diff omits them. Count those files when deciding whether the target is non-empty.

Confirm the fixed point and any review tree resolve and the selected target is non-empty. Stop otherwise.

Done means the immutable or live review target, diff command, status, and relevant commit range are known, or review stopped with the reason.

## 2. Find The Spec

Find product intent in this order:

1. The current request or a caller-supplied selected item, bounded slice, acceptance criteria, path, issue, URL, spec, or legacy PRD.
2. Issue or PR references in commit messages, fetched through `docs/agents/issue-tracker.md` when available.
3. A matching spec or legacy PRD under `docs/`, `specs/`, `.scratch/`, or the repo's issue-packet convention.

If no Spec exists, skip the Spec axis and report `Skipped: no spec available`.

Done means the Spec axis has a source, or is explicitly skipped.

## 3. Find Standards

Find documented repo rules: `AGENTS.md`, `docs/agents/engineering-contract.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `README.md`, formatter/linter configs, test docs, or local convention docs.

If repo standards are thin, use meaningful nearby conventions and read [SMELL-BASELINE.md](SMELL-BASELINE.md). Repo standards override it; every smell remains a labelled judgement call. Tooling-enforced style stays out.

Done means Standards sources are named, or their absence is reported with the convention or smell baseline used.

## Finding Contract

Every finding needs severity, location, evidence, risk, and required change.

- **P0:** catastrophic failure, data loss, or exploitable security flaw.
- **P1:** merge-blocking correctness or contract failure.
- **P2:** significant risk or missing required validation.
- **P3:** lower-risk but actionable correctness or maintainability problem.

Standards findings also identify their type: `documented-standard breach` or `baseline judgement call`.

## 4. Review Standards

Report only actionable Standards findings. Evidence is the documented rule, meaningful nearby convention, or baseline smell. Location is a file and line, hunk, or affected behavior.

Skip style nits that tooling already enforces unless the diff bypasses tooling or changes the tooling contract.

Done means documented-standard breaches and meaningful baseline judgement calls have been reported, or the axis has no findings.

## 5. Review Spec

Report only actionable Spec findings:

- missing or partially implemented requirements
- acceptance criteria that are not proven
- behavior outside the bounded slice
- requirements that look implemented but are likely wrong
- load-bearing internal behavior not proven through a useful interface or seam
- missing or weak tests where proof is required

Evidence is a spec quote, issue text, acceptance criterion, or code evidence.

Done means Spec gaps, scope creep, semantic risks, and proof gaps have been reported, or the axis has no findings.

## 6. Review Mode

Run **single-agent**: Standards, then a **lens reset**, then Spec. Set Standards findings aside; judge Spec only against the review target and Spec source.

Route requests for independent reviewer subagents to `$convergent-pr-review`.

Done means both axes ran sequentially with a lens reset and remained separate.

## Output

Begin with:

```markdown
Review target: <resolved fixed point> | <diff command> | <review tree or live target>
Sources: Standards: <sources>. Spec: <source or skipped>.
```

Present findings under exactly these headings:

```markdown
## Standards

<findings or "No findings.">

## Spec

<findings or "No findings." / "Skipped: no spec available.">
```

Preserve the **two axes, never merged**: do not merge, deduplicate, rerank, or pick a single winner. The final one-line summary may count both axes; findings stay under their axis.

End with:

```markdown
Summary: Standards: <count>, worst <severity or none>. Spec: <count/skipped>, worst <severity or none>.
```

## Completion Criteria

Complete only when the review target is pinned and non-empty; Standards and Spec sources are named or explicitly skipped; both axes were evaluated with lens separation; every finding satisfies the finding contract; the output names the target and sources; and the review remained read-only.
