---
name: writing-great-skills
description: Create or edit canonical Codex skill behavior; audit or review skill semantics; or test whether skill wording changes invocation, judgment, action, context loading, Return, or completion. Exclude general prompt rewriting, ordinary code review, new-package scaffolding, installation, and delivery.
---

# Writing Great Skills

Make canonical skill behavior predictable: choose the intended branch, perform
the required legwork, fail safely, and stop at the intended boundary. Optimize
behavior and semantic density, not prose or step count.

## Authority

Select exactly one operation from the request:

- **Audit:** judge read-only; exact replacement wording is advisory.
- **Author:** edit only the requested canonical skill or skill-design artifact
  and directly affected proof or relationship surfaces.

Resolve the target, operation, canonical source, and mutation boundary before
judgment or mutation. Return `blocked` when any cannot be resolved safely.
New-package scaffolding and metadata mechanics belong to the bundled
`skill-creator`. Installation, publishing, synchronization, and Git delivery
remain with their owners; stop with an exact handoff instead of performing their
work.

## Coverage

Inspect only surfaces capable of changing the requested behavior: the canonical
package, applicable intent and decisions, callers, relationships, owned gates,
outputs, mutations, failure branches, completion, and the smallest relevant
proof. Classify each inspected surface as `affected`, `preserve`, `owned
elsewhere`, `historical evidence`, `drift`, or `not applicable`. For a full
audit, classify the complete canonical package and every behaviorally affected
caller, relationship, proof, and publication surface.

Inspect an installed mirror only when installation-state evidence is explicitly
requested. Report observed parity or drift and leave repair to the installation
owner.

## Behavior Shape

Give each behavior one owner for its rule, admission, authority, inputs,
outputs, evidence, failure Return, and completion. Preserve every relationship's
callee, observable trigger, authority, and Return. Keep the local contract slice
and point to foreign procedure.

Make the outcome, applicable branches, authority, action, evidence, safe
failure, Return, and completion discoverable. Use the fewest meaningful state
transitions. A step earns its place only when it changes state, authority,
actor, artifact, or evidence. Put cross-cutting checks in gates at the boundary
they protect. Each gate names its condition, passing evidence, and safe failure
action. Make completion checkable and demanding enough to force the required
legwork.

Treat an implicitly invocable description as the routing predicate: name
observable request or caller triggers and the closest exclusions without runtime
procedure or body-summary detail.

Prefer a strong pretrained leading word when one behavior must stay salient
across decision points. Define it once and reuse only the term. Keep exact
safety, authority, machine, proof, Return, and completion contracts explicit; a
leading word never replaces them.

Keep common behavior inline. Load [GLOSSARY.md](GLOSSARY.md) only when
invocation, behavior shape, information hierarchy, pruning, or completion
vocabulary affects the work. Split only for independent invocation, irreducible
branch load, or an observed persistent early-stop defect after sharpening
completion.

## Prune

After behavior is correct, give each changed or adjacent instruction unit one
pruning disposition: `Keep`, `Collapse`, `Disclose`, or `Delete`. Keep it when
removal changes intended behavior, safety, authority, proof, irreversible order,
safe failure, Return, or completion. Collapse duplicated meaning into one owner
or an earned leading word. Disclose branch-only detail. Delete no-ops, stale
exposition, and ownerless clauses. State the positive target first and pair each
necessary guardrail with its safe action.

## Claim-Matched Proof

Use read-back for exact bytes and mutations, focused structural checks for
machine contracts, and relationship traces for ownership. When a claim
attributes changed invocation, judgment, action, context loading, Return, or
completion to exact wording, load [BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md) and use
uncontaminated direct controls with fixed tasks and rubrics, fresh contexts,
candidate language absent from control inputs, and root-owned judgment.
Structural evidence does not prove wording efficacy.

## Author Lock

After authorized semantic edits, read back exact mutations and current work
state, preserve unrelated work, run proportionate canonical proof, and stop
before installation, publishing, synchronization, staging, commit, push, or
other delivery.

## Return

Return `complete`, `partial`, or `blocked` with the selected operation and
coverage. Audit reports the verdict, impact-ordered findings, useful exact
candidates, deliberate non-changes, behavior at risk, and evidence limits.
Author reports changed canonical surfaces, behavior added, changed, or removed,
proof, preserved unrelated state, deliberate non-changes, and residual risk.
Name every skipped proof, evidence limit, and unchanged foreign state.

Complete only when coverage is classified; every affected trigger, owner,
relationship, pointer, gate, output, mutation boundary, Return, and completion
condition has one home; required differences are decided; proportionate proof
and read-back are recorded; unrelated work is preserved; and execution stops
before installation or delivery.
