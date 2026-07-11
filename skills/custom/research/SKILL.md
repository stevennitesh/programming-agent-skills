---
name: research
description: Research one source question into a cited repo-local Markdown note. Use when the user requests durable source evidence or a caller supplies an approved note path for source legwork.
---

# Research

**Research delegates reading, not judgment.**

Question -> source lanes -> claim ledger -> evidence gate -> one cited note -> pointer.

## Ownership

- **Research:** Own the question, read-only source legwork, claim ledger, one cited note, and handoff pointer.
- **Workers:** Own assigned source lanes and return evidence. The main agent owns synthesis and the final note.
- **Caller:** Own the decision and every tracker, spec, ADR, domain, source, config, or implementation mutation.
- **Write gate:** A user request for a repo-local research note, or a caller packet that authorizes one note path, permits exactly that tracked mutation. Otherwise leave the repo unchanged and return cited inline evidence or a blocker.

## Process

1. **Lock the research contract.** Name one question, the decision or artifact it supports, scope, freshness requirement, target repo, note path, and write authority.
2. **Pass the write and artifact gates.** Confirm authorization, a writable repo, and one note path. When any is unavailable, leave the repo unchanged and return cited inline evidence or a blocker.
3. **Open source lanes.** Match each claim to the source that owns it:
   - repo behavior -> source, tests, config, governing docs, and ADRs;
   - APIs and libraries -> versioned official docs, specifications, tagged source, and release notes;
   - standards -> the issuing body's standard;
   - empirical claims -> the original paper, dataset, and method.

   Use secondary sources for discovery; trace load-bearing claims to primary sources.
4. **Delegate independent lanes when it materially improves breadth or speed.** Give each worker one lane and require claims, evidence, authority, version or date, conflicts, and gaps. Workers return evidence; the main agent judges it.
5. **Build the claim ledger.** Classify every load-bearing claim as `supported`, `conflicted`, or `unknown`; attach its source, authority, and freshness.
6. **Pass the evidence gate.** Continue until every load-bearing claim is classified, the best available authority and version or date are recorded, conflicts and gaps are explicit, and further searching only repeats evidence or cannot close a documented gap.
7. **Write one note.** Use the repo's research-note convention or `docs/research/<slug>.md`. Preserve the contract, ledger, evidence, uncertainty, and next route in the note shape below.
8. **Hand back the pointer.** Return the note path, one-paragraph answer, status, uncertainty, and next route.

## Note Shape

```markdown
# <Question>

Status: answered | conflicted | blocked
Supports: <decision or artifact>
Scope: <bounds>
Freshness: <as-of date or version>

## Answer

<one-paragraph answer>

## Findings

- <claim> - <supported | conflicted | unknown> ([source](url-or-path))

## Conflicts and Uncertainty

- <conflict, unknown, freshness risk, or blocker>

## Source Trace

| Source | Authority | Version or date | Supports |
| --- | --- | --- | --- |
| <source> | <why it owns the claim> | <version or date> | <claim> |

## Next

- <recommended skill, ticket, spec, or decision>
```

## Completion Criteria

Complete with a note only when write authority, the research contract, and note path are locked; exactly one cited note exists; every load-bearing claim is classified and source-traced; authority, freshness, conflicts, and unknowns are explicit; the note is the only repo mutation; and the caller receives the pointer, answer, status, uncertainty, and next route.

A no-write fallback is complete only when it records the missing authority or artifact gate, returns cited inline evidence or a blocker, and leaves the repo unchanged.

A blocked note is complete only when it records the attempted source lanes and missing evidence.
