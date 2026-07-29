---
name: writing-great-skills
description: Create, edit, audit, or test canonical Codex skill behavior. Exclude general prompt editing, ordinary code review, new-package scaffolding, installation, publishing, synchronization, and Git delivery.
---

# Writing Great Skills

Make canonical skill behavior predictable: choose the intended branch, do the
required work, fail safely, and stop at the intended boundary. Optimize behavior
and semantic density, not prose or step count.

## Authority

Choose one operation:

- **Audit:** judge read-only; exact replacement wording is advisory.
- **Author:** when edits are authorized, perform any needed audit and edit only
  the requested canonical skill or skill-design artifact and directly affected
  proof or relationship surfaces.

Behavioral evaluation is a read-only proof branch within either operation, not
a third operation.

New-package scaffolding and metadata belong to the bundled `skill-creator`.
Installation, publishing, synchronization, and Git delivery remain with their
owners. When requested work crosses a foreign boundary, stop with the exact
next-owner handoff.

## Resolve

Resolve the target, operation, canonical source, and allowed writes before
judgment or mutation. Audit allows no writes. Return `blocked` if any boundary
cannot be resolved safely.

## Trace

Inspect only surfaces capable of changing the requested behavior: applicable
intent, the canonical package, affected callers and relationships, gates,
outputs, mutations, failure branches, completion, and the smallest relevant
proof. A whole-skill audit covers the complete package and every behaviorally
affected caller, relationship, proof, and active routing record. Record a
classification only when it changes judgment or handoff.

Inspect an installed mirror only when installation state is explicitly
requested. Report parity or drift; leave repair to the installation owner.

## Shape

Give each behavior one owner for its trigger, authority, action, evidence,
failure Return, and completion. Preserve each relationship's callee, observable
trigger, authority, and Return. Keep the local contract slice and point to
foreign procedure.

Define every term that changes admission, branching, order, pass/fail, or
completion with an observable rule and any applicable counting scope or
invalidation condition.

Use steps for ordered actions or state changes. Use gates for cross-cutting
checks at the boundary they protect. Each gate names its condition, passing
evidence, and safe failure action. Execute a directly checkable invariant before
the judgment or action it protects; do not defer it to review. Recheck only
after a transition could invalidate it. Scope failure to the smallest dependent
action or output unless authority or safety requires a full stop. Never report
a failed branch complete. Preserve independent supported results and calibrate
each to its weakest load-bearing evidence.

Make completion checkable and demanding enough to force the required work.
Treat an implicitly invocable description as a routing predicate: name
observable triggers and the closest exclusions, not runtime procedure.

Prefer an established leading word when it accurately recruits a known practice
and replaces repeated guidance. Define any local deviation, then use the term
consistently where the practice must stay salient. Never let it replace
observable authority, gates, proof, safe failure, Return, or completion.

Keep common behavior inline. Load [GLOSSARY.md](GLOSSARY.md) only when choosing
or defining a leading word, changing invocation or reference-loading behavior,
splitting a skill, promoting a lesson across skills, or specifying derived
state.

## Prune

After behavior is correct, mark each changed or adjacent instruction unit
`Keep`, `Collapse`, `Disclose`, or `Delete`:

- Keep behavior, safety, authority, proof, irreversible order, safe failure,
  Return, and completion.
- Collapse duplicated meaning into one owner.
- Disclose branch-only detail behind an exact condition and target.
- Delete no-ops, stale exposition, and ownerless clauses.

Apply the same removal test to every proposed step, field, artifact, view, and
check.

State the positive target first and pair each necessary guardrail with its safe
action.

## Prove

Match proof to the claim: read back exact bytes and mutations, use focused
structural checks for machine contracts, and trace relationships to their
owners. Bind evidence to the exact candidate and its invalidation boundary.
Structural evidence does not prove live behavior.

For a claim that exact wording changes invocation, judgment, action, context
loading, Return, or completion, load
[BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md).

**Author Lock:** after authorized edits, read back mutations and current work
state, preserve unrelated work, run proportionate canonical proof, and stop
before installation, publishing, synchronization, staging, commit, push, or
other delivery.

## Return

Return `complete`, `partial`, or `blocked` with the operation and coverage.
Use `partial` when safe work completed but admitted coverage or proof remains
incomplete.

- **Audit complete:** requested coverage is inspected; the verdict, supported
  impact-ordered findings, advisory candidates, deliberate non-changes,
  behavior at risk, and material evidence limits are reported.
- **Author complete:** affected contracts have one owner; required differences
  are implemented; exact mutations, proof, preserved unrelated state,
  deliberate non-changes, and residual risk are reported; Author Lock holds.

Name skipped proof or unchanged foreign state only when its omission could be
mistaken for completed scope.
