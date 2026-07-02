---
name: review
description: "Run ordinary fixed-point review for branch, WIP, or \"review since X\" diffs. Keep Standards and Spec separate: documented repo conventions, and whether the diff satisfies the originating issue, PRD, spec, or acceptance criteria. For local PR or high-risk convergence review, use convergent-pr-review."
---

# Review

Run a read-only fixed-point review of the current diff.

This is the default Converge gate for ordinary branch, WIP, and `$implement` closeout review. It checks two axes separately:

- **Standards**: whether the diff follows documented repo conventions and the local engineering contract.
- **Spec**: whether the diff satisfies the originating issue, PRD, spec, bounded slice, and acceptance criteria.

Keep the axes separate. Do not merge, deduplicate, or rerank findings across axes. One axis passing must not hide the other axis failing.

Use `$convergent-pr-review` instead for local PR review or high-risk local-diff review that needs independent reviewer passes, scoped lenses, and a verified finding ledger.

Do not edit files.

## 1. Pin The Fixed Point

Use the fixed point the user supplied: commit SHA, branch, tag, `main`, `HEAD~5`, or similar. If none was supplied, ask.

Capture:

- fixed point resolution: `git rev-parse <fixed-point>`
- diff command: `git diff <fixed-point>...HEAD`
- commit list: `git log <fixed-point>..HEAD --oneline`

Confirm the fixed point resolves and the diff is non-empty before reviewing. Stop if the fixed point does not resolve or the diff is empty.

Done means the fixed point, diff command, and commit range are known, or the review is stopped with the reason.

## 2. Find The Spec

Find the source of product intent:

1. Issue or PR references in commit messages, fetched through `docs/agents/issue-tracker.md` when available.
2. A path, issue, URL, PRD, spec, or acceptance criteria the user passed.
3. A PRD/spec file under `docs/`, `specs/`, `.scratch/`, or the repo's issue-packet convention matching the branch or feature.

If no Spec exists, skip the Spec axis and report `Skipped: no spec available`.

Done means the Spec axis has a source, or is explicitly skipped.

## 3. Find Standards

Find documented repo rules: `AGENTS.md`, `docs/agents/engineering-contract.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `README.md`, formatter/linter configs, test docs, or local convention docs.

If no Standards source exists, say so. Report only clear nearby-convention mismatches, and label them as convention findings rather than documented-standard violations.

Do not invent standards.

Done means Standards sources are named, or their absence is reported.

## 4. Review Standards

Report only actionable Standards findings.

Each finding needs severity, location, evidence, risk, and required change.

Evidence is the documented rule or nearby convention. Location is file/line, hunk, or affected behavior.

Skip style nits that tooling already enforces unless the diff bypasses tooling or changes the tooling contract.

Done means documented-standard violations and meaningful convention findings have been reported, or the axis has no findings.

## 5. Review Spec

Report only actionable Spec findings:

- missing or partially implemented requirements
- acceptance criteria that are not proven
- behavior outside the bounded slice
- requirements that look implemented but are likely wrong
- load-bearing internal behavior not proven through a useful interface or seam
- missing or weak tests where proof is required

Each finding needs severity, location, evidence, risk, and required change.

Evidence is a spec quote, issue text, PRD section, acceptance criterion, or code evidence.

Done means Spec gaps, scope creep, semantic risks, and proof gaps have been reported, or the axis has no findings.

## 6. Subagent Boundary

Default to sequential review in the current agent context: Standards first, then Spec.

A delegated parent task, including `$implement`, is not a request for delegated review.

Only run Standards and Spec in separate subagents when the user explicitly asks for review subagents, delegated review, parallel review, or multi-agent review for this review step.

Done means the chosen review mode matches the user's review request, not an inherited execution context.

## Output

Present findings under exactly these headings:

```markdown
## Standards

<findings or "No findings.">

## Spec

<findings or "No findings." / "Skipped: no spec available.">
```

Do not merge, deduplicate, or rerank findings across axes. The final one-line summary may count both axes, but findings stay under their axis.

End with:

```markdown
Summary: Standards: <count>, worst <severity or none>. Spec: <count/skipped>, worst <severity or none>.
```

## Completion Criteria

Done means the fixed point was verified, the diff was reviewed read-only, Standards and Spec were evaluated separately, findings are actionable and evidenced, missing sources are reported explicitly, and the output preserves the two-axis boundary.
