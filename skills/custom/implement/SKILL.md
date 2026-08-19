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

- Invoke `$tdd` only when the user explicitly requests TDD or repository policy
  requires it. Otherwise implement directly and use ordinary tests as useful
  proof.
- If the user explicitly requests subagents, load
  [Plain Worker Handoff](references/WORKER-HANDOFF.md) and
  [Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md), then
  delegate only a bounded edit that one worker can own. The root inspects the
  returned diff and proof.
- For tracker-backed work, follow the repository's claim and closeout rules.
  Direct work creates no tracker state. Commit only when the user or repository
  requires Git delivery; do not push without separate authority.
- Before a destructive or external mutation, confirm the exact target and
  authority. Read the result back when the operation can partially succeed or
  another writer can change it.

## 4. Prove

Run the nearest useful check that can fail for the behavior you changed. Use an
existing test seam when it is meaningful. Add or change tests when repository
policy requires them or when they are the cheapest durable protection for the
behavior—not to satisfy a ritual. Run broader suites only when policy or shared
impact justifies them.

Inspect the real output or caller path when a unit check cannot establish that
the change works. If safe execution is unavailable, use the strongest safe
proxy and say what remains unproved.

Invoke `$change-review` only when the user or repository requires independent
review, the candidate has changes from two or more independent authors, or a
material shared-contract or irreversible-migration judgment remains after
proof. Keep the candidate fixed while it is reviewed. Review grants no
authority to widen scope.

## 5. Finish

Inspect the complete diff and current repository state. Remove displaced code,
debugging residue, stale comments, and unnecessary complexity. Update
documentation only when the public contract, operator workflow, or a durable
non-obvious decision changed.

Call the item complete only when the requested behavior works, the relevant
proof passes, and the final diff contains only intended changes. Otherwise
preserve useful work and state exactly what remains.

Return a concise summary of what changed, the proof run, and any material gap.
Include commit or tracker state only when applicable. Stop before another item,
deployment, PR creation, merge, or unauthorized push.
