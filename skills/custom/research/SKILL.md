---
name: research
description: Research one source question against primary sources into a cited repo-local Markdown note. Use for durable source evidence when the user requests a note or a caller authorizes one note path.
---

# Research

**Research delegates reading, not judgment.**

Lock -> Trace -> Scout -> Classify -> Gate -> Write -> Return.

## Boundary

Research owns one question, source legwork, evidence judgment, a claim ledger, one cited note, and its pointer. The caller owns the supported decision or artifact and all other mutations.

Write exactly one tracked note only at the user's request or a caller-authorized repo-local path. Otherwise leave the repo unchanged and return cited inline evidence or a blocker.

## Process

1. **Lock.** Name the question, supported decision or artifact, scope, freshness requirement, target repo, authorized note path, and write authority.
2. **Trace.** Trace every load-bearing claim to its owning primary source: repo source, tests, config, governing docs, or ADRs; versioned official docs, specifications, tagged source, or release notes; the issuing standards body; or the original paper, dataset, and method. Use secondary sources only for discovery.
3. **Scout.** When independent lanes materially improve breadth or speed, give direct fresh-context read-only scouts with `fork_turns="none"` one complete research contract and one lane. Require claims, citations, authority, version or date, conflicts, and gaps. Scouts never edit files, mutate external state, or spawn; exclude parent conclusions and peer results. The main agent alone judges evidence and writes the note. Minimal recent context supports continuity, not independence.
4. **Classify.** Mark every load-bearing claim `supported`, `conflicted`, or `unknown`; attach its source, authority, and freshness.
5. **Gate.** Stop only when every load-bearing claim is classified, the best authority and version or date are recorded, conflicts and gaps are explicit, and further search repeats evidence or cannot close a documented gap. A blocked note records attempted lanes and missing evidence.
6. **Write.** Use the repo's research-note convention or `docs/research/<slug>.md`. Preserve the contract, ledger, evidence, uncertainty, and next route:

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

7. **Return.** Give the caller the note path, one-paragraph answer, status, uncertainty, and next route. For a no-write result, name the missing gate and return cited inline evidence or a blocker.
