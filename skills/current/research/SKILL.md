---
name: research
description: Use when the user wants a topic researched, docs/API/library facts checked, primary-source evidence gathered, or source legwork delegated before a decision, PRD, issue, diagnosis, or architecture recommendation; save one cited repo-local Markdown note.
---

# Research

Use this when a question needs source legwork before a decision, PRD, issue, diagnosis, or architecture recommendation.

Research answers with **primary sources**: official docs, specs, standards, source code, first-party APIs, release notes, papers, or repo-local documents. Secondary write-ups can help discover sources, but they do not own claims.

## Process

1. **Frame the question.** Name the exact question, why it matters, and what decision or artifact the answer will support.
2. **Find primary sources.** Prefer repo-local docs and source for repo behavior; use official external sources for external APIs, libraries, standards, or product behavior. Browse when freshness or source attribution matters.
3. **Trace claims.** Follow every load-bearing claim back to the source that owns it. If sources conflict, record the conflict instead of smoothing it over.
4. **Write one note.** Save the findings as a Markdown file where the repo keeps research notes. If no convention exists, use `docs/research/<slug>.md`.
5. **Hand back the pointer.** Report the note path, the answer in one paragraph, and any uncertainty, blocker, or next route.

Use a subagent for broad reading when available and useful. If no subagent is available, do the research inline. Either way, the output is the same: one cited note in the repo.

## Note Shape

```markdown
# <Question>

## Answer

<short answer>

## Findings

- <claim> ([source](url-or-path))

## Source Trace

- <source>: <why it is authoritative>

## Uncertainty

- <unknown, conflict, freshness risk, or blocker>

## Next

- <recommended next skill, issue, PRD, or decision>
```

## Boundaries

- Do not publish tracker comments or mutate issues unless the invoking workflow explicitly asks.
- Do not turn research into implementation. Hand back the note and next route.
- Do not cite secondary sources for load-bearing claims when a primary source exists.
- Do not paste long source excerpts; cite and summarize.

## Completion Criteria

Done means one Markdown note exists in the repo, every load-bearing claim has a source trace, and the user has the note path plus the decision or next route it supports.
