---
name: change-review
description: Review a selected diff, branch, PR, or working-tree candidate for introduced or worsened correctness, contract, and maintainability problems. Exclude whole-codebase audits.
---

# Change review

Review a fixed candidate against its accepted outcome and relevant engineering
obligations. Admit only evidence-backed findings attributable to that candidate.

Review is complete when the candidate identity is known, material obligations in
scope have been assessed, admitted findings meet the finding standard, and
remaining coverage limits are explicit.

A review-only request does not authorize product edits, external comments, merge,
release, or risk acceptance. For an already-authorized review-and-fix request,
establish the review conclusion before continuing into repair.

Use ordinary review by default. Read
[Impact analysis](references/impact-analysis.md) when the user asks for blast
radius or candidate safety depends on consequential behavior outside the diff and
direct callers. Read [Review feedback](references/review-feedback.md) when the
input is existing reviewer comments or requested corrections that must be judged
against the current candidate.

Only when the user explicitly requests high assurance or multiple independent
reviewers, read [High assurance](references/high-assurance.md). A large diff, a PR,
or the phrase "final review" does not activate that mode.

## 1. Fix the candidate and obligations

Use the target and comparison the user names. Otherwise resolve the relevant
current work in scope, including staged, unstaged, and applicable untracked
content. For a named branch or PR, use its actual base and head rather than
assuming a conventional branch or silently substituting another comparison.

An empty selection means there is no change to review, not that an imagined
candidate is clean.

Record the candidate identity and comparison. For mutable work, capture the
selected content or hold review custody so the conclusion remains attached to the
state actually examined. Bind supplied proof and decisive context to that same
candidate.

A diff alone is insufficient when callers, configuration, persisted
representations, or external contracts determine the changed behavior.

Read the accepted request, applicable repository guidance, and relevant decisions.
Use tests and implementation as evidence of behavior, not substitutes for missing
accepted intent. If intent is insufficient for a conformance claim, state that
coverage limit while continuing correctness checks that have independent support.

When independent review is required, use the high-assurance path and report any
independence limitation.

## 2. Review the changed behavior

Check the requested outcome and scope before implementation quality. Attractive
structure cannot compensate for incomplete behavior, and a working happy path
does not excuse a demonstrated design or maintainability cost.

Challenge the assumptions connecting the chosen approach to the accepted outcome.
Agreement among a plan, implementation, and tests does not independently validate
an assumption they share.

Review against accepted behavior and binding constraints, not an unnecessary
implementation mechanism merely because a plan proposed it. If a plan-level
assumption is wrong, identify that decision rather than demanding additional
machinery to satisfy it.

Trace the changed behavior far enough through real owners and consumers to verify
the property the change can lose. When a boundary changes, prefer the actual
produced or persisted representation and real consumer over a hand-constructed
substitute.

For numerical or data changes, check semantics capable of making a plausible
result wrong: identity, units, time and availability alignment, missing-value
meaning, precision, aggregation, and consequential method assumptions. Use an
independent reference, invariant, or analytic case when implementation and tests
could share the same mistake.

Inspect only risks activated by the change or required behavior. Do not manufacture
hardening findings for risks the supported workflow does not have.

When behavior is removed or replaced, follow its real consumers and registrations
far enough to identify displaced code or required compatibility. Do not demand
deletion while a real migration still requires coexistence.

Report design or maintainability findings only when they demonstrate concrete
caller burden, duplicated policy, change amplification, or another real cost.
Preference, unfamiliarity, line count, or the existence of one adapter is not a
finding by itself. Keep unrelated baseline-improvement discovery with
[audit-codebase](../audit-codebase/SKILL.md).

## 3. Admit findings under evidence

Before reporting an observation, apply
[Finding standards](references/finding-standards.md).

Seek evidence capable of disproving the finding and distinguish a problem
introduced or worsened by the candidate from unrelated baseline code. An unchanged
line can still be the causal location of a regression activated by the change;
explain that connection rather than restricting review to modified hunks.

Reuse candidate-bound proof while its relevant code, inputs, dependencies,
configuration, environment, and candidate identity remain valid. Run additional
checks only when they can settle a material question or repository policy requires
them. A substitute proves only properties it preserves.

## 4. Conclude on the same candidate

Recheck mutable candidate identity before returning the conclusion. If the
candidate moved, identify what remains reviewed and what requires re-review rather
than attaching the old verdict to the new state.

For a repair review, preserve prior finding identities, re-evaluate each against
the successor, and inspect the repair's affected behavior. Broaden only when the
repair materially expands the candidate.

Return findings under Finding standards in impact order, together with the reviewed
identity, decisive evidence, and material coverage limits. If no findings are
admitted, say so without implying coverage beyond what was actually established.

When the caller requests a gate verdict, use the gate semantics in Finding
standards.

For review-only work, stop with the conclusion. For already-authorized
review-and-fix work, continue within the active workflow's ownership and custody
rules. Review does not grant publication, merge, release, deployment, or residual
risk authority.
