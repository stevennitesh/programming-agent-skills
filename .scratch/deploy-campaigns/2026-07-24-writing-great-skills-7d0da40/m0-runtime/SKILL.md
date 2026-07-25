---
name: writing-great-skills
description: Create or edit canonical Codex skill behavior; audit or review skill semantics; or test whether skill wording changes invocation, judgment, action, context loading, Return, or completion. Exclude general prompt rewriting, ordinary code review, package scaffolding, installation, and delivery.
---

# Writing Great Skills

## Authority

Choose exactly one operation from the request:

- **Audit:** judge read-only; exact replacement wording may be advisory.
- **Author:** edit only the requested canonical skill or skill-design artifact
  and directly affected proof or relationship surfaces.

Before judgment or mutation, resolve the target, canonical source, operation,
and mutation boundary. Return `blocked` when any cannot be resolved safely.
Point to the owners of scaffolding, installation, publishing,
synchronization, Git delivery, and foreign domain or engineering decisions;
do not perform or copy their procedures.

## Coverage

Inspect and classify every surface capable of changing the requested behavior:
the complete requested canonical package and each affected caller,
relationship, proof, output, mutation, failure, completion, and publication
surface. Return `partial` when admitted coverage is incomplete and `blocked`
when safe coverage cannot be resolved.

## Semantic Contract

Give each behavior and relationship one owner for its trigger, authority,
inputs, action, output, failure Return, and completion. Keep the local
contract slice and point to foreign procedures.

Keep common guidance inline. Load [GLOSSARY.md](GLOSSARY.md) only when
invocation, information hierarchy, pruning, or completion vocabulary affects
the work. Load [BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md) only when claiming that
exact wording changes invocation, judgment, action, context loading, Return,
or completion. When required branch guidance is unavailable, return `partial`;
otherwise do not load irrelevant support.

## Behavior-Preserving Cuts

Keep clauses that change intended behavior, safety, authority, proof,
irreversible order, safe failure, Return, or completion. Remove only clauses
without a local intent or contract owner, duplicated meaning, stale
presentation, or no-op prose. When a behavior-changing cut is not proved safe,
return `partial` with the behavior at risk and exact candidate wording.

## Claim-Matched Proof

Use exact read-back and deterministic checks for structural, relationship, and
mutation claims. For claims that exact wording changes observable behavior,
use uncontaminated direct controls under [BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md).
Do not present a structural proxy as behavioral proof. When required safe proof
cannot run, return `partial` with the skipped proof and evidence limits, or
`blocked` when the work cannot proceed safely.

## Return

Return `complete`, `partial`, or `blocked` with the selected operation,
coverage, operation-specific findings or changes, deliberate non-changes,
proof, preserved unrelated state, behavior at risk, evidence limits, and
residual risk. Name every skipped proof and unchanged foreign state.

Complete only when every affected semantic and surface has one home and
proportionate proof, exact mutations and work state are read back, unrelated
work is preserved, and execution stops before installation or delivery.
