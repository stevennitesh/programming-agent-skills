---
name: review
description: "Review changes since a fixed point along two separate axes: Standards, for documented repo conventions, and Spec, for whether the diff implements the originating issue, PRD, or spec. Use when the user asks to review a branch, PR, or work-in-progress diff, including \"review since X\"."
---

# Review

Review the diff between `HEAD` and a fixed point. This is a read-only review skill: do not edit code.

In the convergence loop, this is the Converge gate: verify that the chosen approach still satisfies Spec and Standards before the work is locked.

Run two axes separately:

- **Standards** — does the diff follow this repo's documented standards?
- **Spec** — does the diff faithfully implement the originating issue, PRD, or spec?

Keep the axes separate so one cannot hide the other. Do not merge or rerank findings across axes.

## Process

### 1. Pin The Fixed Point

Use the fixed point the user supplied: commit SHA, branch, tag, `main`, `HEAD~5`, or similar. If none was supplied, ask.

Capture:

- diff command: `git diff <fixed-point>...HEAD`
- commit list: `git log <fixed-point>..HEAD --oneline`

Confirm the fixed point resolves with `git rev-parse <fixed-point>` and the diff is non-empty before reviewing.

### 2. Find The Spec Source

Look for the originating spec in this order:

1. Issue or PR references in commit messages, fetched using `docs/agents/issue-tracker.md` when available.
2. A path, issue, URL, or PRD/spec the user passed.
3. A PRD/spec file under `docs/`, `specs/`, `.scratch/`, or the repo's issue packet convention matching the branch or feature.
4. If none is found, ask where the spec is. If there is no spec, skip the Spec axis and report `no spec available`.

If `docs/agents/issue-tracker.md` is missing and tracker fetch is needed, run `$setup-matt-pocock-skills`. If no tracker fetch is needed, continue.

### 3. Find Standards Sources

Find repo documentation for coding standards and contribution rules: `AGENTS.md`, `docs/agents/engineering-contract.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `README.md`, formatter/linter configs, test docs, or local docs that describe conventions.

If no standards docs exist, say so. Then report only clear local-convention mismatches visible in nearby code, and label them as convention findings rather than documented-standard violations. Do not invent new standards.

### 4. Review Both Axes

If the user explicitly requested subagents, delegation, or parallel agent work, run the two axes in separate Codex subagents. Otherwise, run them sequentially and keep notes separate.

#### Standards Axis

Report documented-standard violations. If no standards docs exist, report only clear local-convention mismatches as convention findings.

Include:

- documented rule or nearby convention being violated
- file/line or hunk evidence when possible
- risk created by the violation
- required change

Skip style nits that tooling already enforces unless the diff bypasses tooling or changes tool configuration.

#### Spec Axis

Report:

- requirements that are missing or only partially implemented
- whether the diff completes the intended bounded slice; for tracer-bullet issues, one narrow behavior through the real system; for support issues, the unblocker, migration, harness, config, or operational change with observable validation
- behavior in the diff that was not asked for, including unrelated tracer bullets, support slices, or adjacent cases that widen the slice
- requirements that look implemented but are likely wrong
- load-bearing internal behavior whose semantics affect the requested result but are not proven through a meaningful seam
- missing or weak tests when an acceptance criterion is not proven through the highest useful interface or seam

Quote or cite the spec line, issue text, or PRD section for each finding.

## Finding Rules

Report only actionable issues: bugs, missing requirements, scope creep, documented-standard violations, convention findings, or test gaps that create real risk.

Each finding must include:

- severity: `Blocker`, `Major`, or `Minor`
- location: file/line or hunk when possible; for cross-cutting behavior, cite the affected behavior
- evidence: spec quote, standard citation, convention evidence, or code evidence
- risk: why it matters
- required change: what would make it pass

Do not pad the review. If an axis has no findings, say so.

## Output

Present findings under two headings:

```markdown
## Standards

<findings or "No findings.">

## Spec

<findings or "No findings." / "Skipped: no spec available.">
```

Do not merge, deduplicate, or rerank across axes.

End with a one-line summary: total findings per axis and the worst severity within each axis.

## Completion Criteria

Done means the fixed point was verified, the diff was reviewed read-only, Standards and Spec were evaluated separately, findings are actionable and evidenced, and missing spec or standards sources are reported explicitly.
