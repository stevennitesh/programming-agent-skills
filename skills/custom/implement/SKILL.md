---
name: implement
description: Deliver one explicitly selected bounded ready item through a small, sound implementation and proportionate proof.
---

# Implement

Deliver exactly one caller-selected ready item. Work directly by default. The
caller owns the requested outcome, scope, permissions, and irreversible
external effects. Push requires separate authority.

## 1. Understand

Read the repository instructions and the code that owns the behavior. Trace
the real callers, data flow, and existing proof seam far enough to understand
what must change. Preserve unrelated work and established domain language.
Treat demonstrated caller dependence as compatibility and migration evidence;
do not automatically make it a new commitment or discard it.

Use the caller's selection as the scope fence. If the intended behavior is
unsettled, return the decision to its owner. Ordinary bug investigation stays
here: reproduce the symptom and trace it to its cause. Return
`diagnosis-required` only when the failure needs a dedicated investigation,
such as intermittent, performance, environment-only, production-only, or still
causally ambiguous behavior.

## 2. Choose The Design

Choose the smallest integrated design that makes the requested behavior clear.
Prefer the current behavior owner, small interfaces, and local state. Model the
domain with a clear data shape instead of scattering conditionals. Subtract,
reuse, or replace before adding another path. Use language, framework, and
repository capabilities before adding abstractions or dependencies. Add a
boundary only for a real caller or trust boundary. Fix the cause across
affected callers instead of guarding one symptom.

Within the bounded change, integrate new behavior as a native part of the
design rather than a bolted-on special case. Keep framework, transport, and
storage details at the edge. Pass domain values into core logic and prefer
explicit results over hidden mutation. Derive secondary state from one source
of truth. Add a layer or seam only when it hides meaningful complexity or
supports real variation.

Do not add speculative compatibility, defensive checks, configuration,
abstraction, documentation, or migration machinery. Validate actionable
machine input at its owning trust boundary; ordinary internal values do not
need adversarial treatment.

## 3. Build

Implement the complete requested behavior in the current owner. Follow local
style and keep the diff coherent. Remove code made obsolete by the change when
that removal is safe and in scope.

Use these branches only when their condition is present:

- If Git has an active conflicted operation or unmerged index, stop
  implementation, preserve Git state, and hand off to
  `$resolving-merge-conflicts` with the requested scope plus whether resolution
  and native continuation were requested.
- Invoke `$tdd` for each materially distinct settled behavior and independent
  oracle only when the user explicitly requests TDD, test-first work, or
  RED-GREEN-REFACTOR, or repository policy requires TDD. A material gap returns
  before that behavior is mutated. Otherwise implement directly and use
  ordinary tests as useful proof.
- If the user explicitly requests subagents, load
  [Plain Worker Handoff](references/WORKER-HANDOFF.md), then delegate only a
  bounded edit that one worker can own. Use a fresh capable worker under the
  active runtime unless the user selects a model. The root inspects the
  returned diff and proof.
- For tracker-backed work, read `docs/agents/issue-tracker.md` and
  `docs/agents/triage-labels.md`, then follow the claim and closeout rules. If
  either contract is missing or incompatible, recommend `$repo-bootstrap` and
  stop. Direct work creates no tracker state. Commit only when the user or
  repository requires Git delivery; do not push without separate authority.
- Before a destructive action or durable external mutation, confirm the exact
  target and authority. Read back every durable external mutation. Establish a
  recovery path before an operation that can partially succeed.

## 4. Prove

Run the nearest useful check that can fail for the behavior you changed. Use an
existing test seam when it is meaningful. Add or change tests when repository
policy requires them or when they are the cheapest durable protection for the
behavior—not to satisfy a ritual. Run broader suites only when policy or shared
impact justifies them.

For a bug fix, use proof capable of distinguishing the defect from the repaired
behavior. When the defect depends on a produced result being used later,
exercise the lowest ordinary consuming caller that can expose it.

When an operation has material partial-effect risk or must recover after
interruption, exercise that boundary. Any proxy must be capable of exposing the
same recovery failure.

Inspect the real output or caller path when a unit check cannot establish that
the change works. If safe execution is unavailable, use the strongest safe
proxy and say what remains unproved.

Invoke `$change-review` only when the user or repository requires it, or a
concrete unresolved shared-contract or migration judgment remains after proof.
Pin the clean candidate first and let Change Review own its procedure. Multiple
authors alone do not trigger review.

## 5. Finish

Inspect the complete diff and current repository state. Remove displaced code,
debugging residue, stale comments, and unnecessary complexity. Update
documentation only when the public contract, operator workflow, or a durable
non-obvious decision changed.

Call the item complete only when the requested behavior works, the relevant
proof passes, and the final diff contains only intended changes. Otherwise
preserve useful work and state exactly what remains.

For a completed tracker item, preserve its category, remove readiness roles,
apply `implemented`, and close only when the tracker configuration says to.
Read the result back. Refetch open dependents whose blocker changed; apply
`ready-for-agent` only when the dependent has a complete accepted packet and no
unresolved blocker. Leave other dependents non-ready.

Return a concise summary of what changed, the proof run, and any material gap.
Include commit or tracker state only when applicable. Stop before another item,
deployment, PR creation, merge, or unauthorized push.
