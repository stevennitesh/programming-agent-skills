---
name: change-review
description: Review a selected diff, branch, PR, or working-tree candidate for introduced or worsened problems. Exclude whole-codebase audits.
---

# Change review

Assess the selected change against accepted requirements, supported behavior, and
repository guidance. Choose the investigation and verification needed to return
actionable findings, the reviewed candidate, and material coverage limits.

Review-only work authorizes assessment. For authorized review-and-fix work,
continue into supported repairs under the execution owner's custody rules.
A verdict grants no publication, merge, deployment, or risk-acceptance authority.

## Establish the candidate

Resolve the user's target and comparison, including actual base and head for a
branch or PR. For working-tree review, include staged, unstaged, and applicable
untracked content. An empty selection means there is no change to review.
Capture mutable inputs or hold review custody, bind evidence to that candidate,
and recheck identity before concluding. If it moves, identify what needs re-review.

Read [Finding standards](references/finding-standards.md) for admission, priority,
missing evidence, and requested gate decisions. Unrelated baseline-improvement
discovery belongs to [audit-codebase](../audit-codebase/SKILL.md).

## Review the change in the codebase

Use the request and supported behavior to establish what the change should do.
Follow affected entry points, callers, state transitions, and failure paths as
far as needed to judge that behavior. Check whether an existing owner already
supplies the rule, data, or operation. Flag duplication when it creates a concrete
risk of divergent behavior, unnecessary execution, or maintenance cost.

For consequential behavior, judge whether existing or changed tests would catch
a plausible regression through the affected mechanism. Choose the depth and
evidence that fit the risk.

## Choose the needed branches

Review directly when that is sufficient. For independent or multiple-reviewer
assessment, read [Independent review](references/independent-review.md). The lead
chooses the arrangement for difficulty, isolation, coverage, and budget, honoring
user requirements and the active model policy; size alone does not require
delegation. The lead retains final acceptance.

Read [Impact analysis](references/impact-analysis.md) for requested blast radius,
shared validation, persisted-input acceptance, or supported compatibility changes.
Use it also for consequential assumptions beyond direct callers or when types,
runtime values, or test coverage need closer inspection.

Read [Review feedback](references/review-feedback.md) for supplied findings,
repair reviews, or a requested bounded review-and-repair loop.

## Return the assessment

Order findings by priority with precise, clickable locations, the affected
workflow, consequence, and decisive evidence. Identify the candidate and comparison,
material coverage, verification, and limits using the caller's schema or a concise
readable format. If none qualify, say "No actionable findings" while making any
incomplete required coverage explicit. Keep optional suggestions separate.
Include a gate verdict only when requested or required.
