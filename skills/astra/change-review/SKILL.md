---
name: change-review
description: Review a selected diff, branch, PR, or working-tree candidate for introduced or worsened problems. Exclude whole-codebase audits.
---

# Change review

Review the selected change against accepted requirements, supported behavior, and
applicable repository guidance. Deliver actionable findings with evidence, the
candidate reviewed, and material coverage limits.

Choose the investigation and verification needed to reach a defensible conclusion.
Review is complete when material obligations in scope have been assessed and the
result distinguishes established problems from unresolved questions.

A review-only request authorizes assessment, not product edits or external effects.
For already-authorized review-and-fix work, establish the conclusion and continue
into repair under the active workflow's ownership and custody rules. A review
verdict does not itself authorize publication, merge, release, or risk acceptance.

## Review contract

Use the user's target and comparison, including the actual base and head for a
named branch or PR. Otherwise resolve the current work in scope, including staged,
unstaged, and applicable untracked content. An empty selection is no change to
review, not a clean verdict on an imagined candidate.

Bind the review and its evidence to an identified candidate. For mutable work,
capture the selected content or hold review custody, and recheck identity before
concluding. If it moves, state what remains reviewed and what needs re-review.

Apply [Finding standards](references/finding-standards.md): concrete, reachable
problems introduced, worsened, or left unsatisfied by the candidate, including
missing required behavior and demonstrated maintenance costs. Tests and plans are
evidence, not substitutes for accepted intent; their agreement does not establish
an assumption they share. Preserve domain meaning and supported compatibility.

When shared validation or persisted-input acceptance changes, check the affected
callers and compatibility obligations. If existing fixtures are migrated to a
stricter contract, determine whether they represent previously supported persisted
inputs. Require a distinguishing compatibility regression case using the previous
input where that workflow remains supported; passing only migrated fixtures does
not establish compatibility.

For a repair review, preserve prior finding identities, re-evaluate each against
the successor, and assess the correction's affected behavior, including expanded
impact from changed ownership, interfaces, or persisted-input acceptance.

## Choose the review arrangement

The lead chooses the arrangement according to difficulty, uncertainty, the value
of isolated context, and budget. Honor explicit user requirements and host
constraints. A large diff or "final review" does not by itself require delegation.

- **Direct review:** review in the current context when additional reviewers
  would not materially improve the result.
- **Independent review:** use a fresh read-only reviewer when context isolation
  would materially help. Read [Independent review](references/independent-review.md).
- **High assurance:** use multiple independent reviewers with complementary scopes
  when added coverage warrants the cost. The lead chooses the count and scopes.
  Read [High assurance](references/high-assurance.md).

Keep model selection with the active model policy. The lead assesses returned
findings and coverage and retains final acceptance.

Read [Impact analysis](references/impact-analysis.md) when asked for blast radius
or when consequential assumptions extend beyond the diff and direct callers.
Read [Review feedback](references/review-feedback.md) when assessing or applying
existing reviewer comments. Unrelated baseline-improvement discovery belongs to
[audit-codebase](../audit-codebase/SKILL.md).

## Output

Use this structure, adapting its rendering to a caller-required schema or review
interface. Order findings by severity and use precise, clickable locations.

```text
Findings

[P1] Specific, actionable title — path:line
Trigger or affected workflow, what goes wrong, and why it matters.
Decisive evidence and the correction needed, where established.

Reviewed: candidate identity and comparison
Coverage: material areas assessed and verification used
Limits: consequential uncertainty or missing evidence
```

If none qualify, say "No actionable findings." Keep evidence gaps and optional
suggestions separate from established defects. Preserve stable finding IDs and
report their dispositions across correction rounds. Include a gate verdict only
when requested or required, using the semantics in Finding standards. State
coverage limits without implying that unreviewed behavior is correct.
