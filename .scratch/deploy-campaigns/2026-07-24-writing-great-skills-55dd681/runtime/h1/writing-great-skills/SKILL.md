---
name: writing-great-skills
description: Create or edit canonical Codex skill behavior; audit or review skill semantics; or test whether skill wording changes invocation, judgment, action, context loading, Return, or completion. Exclude general prompt rewriting, ordinary code review, new-package scaffolding, installation, and delivery.
---

# Writing Great Skills

## Authority

Select exactly one operation from the request:

- **Audit:** judge read-only; exact replacement wording is advisory.
- **Author:** edit only the requested canonical skill or skill-design artifact and directly affected proof or relationship surfaces.

A direct behavior test is read-only; a persisted artifact requires Author
authority. Resolve the target, operation, canonical source, and mutation
boundary before judgment or mutation. Return `blocked` when any cannot be
resolved safely.

The bundled `skill-creator` owns new-package scaffolding and metadata
mechanics. Writing Great Skills owns semantic quality through canonical proof.
Installation, publishing, synchronization, and Git delivery remain with their
owners; stop with an exact handoff instead of performing their work.

## Coverage

Inspect only surfaces capable of changing the requested behavior: the
canonical package, applicable intent and decisions, callers, relationships,
owned gates, outputs, mutations, failure branches, completion, and the
smallest relevant proof. Classify each inspected surface as `affected`,
`preserve`, `owned elsewhere`, `historical evidence`, `drift`, or
`not applicable`. For a full audit, classify the complete canonical package
and every behaviorally affected caller, relationship, proof, and publication
surface.

Inspect an installed mirror only when installation-state evidence is
explicitly requested. Report observed parity or drift and leave repair to the
installation owner.

## Semantic Contract

Give each behavior one owner for its rule, admission, authority, inputs,
outputs, evidence, failure Return, and completion. Preserve every
relationship's callee, observable trigger, authority, and Return. Keep the
local contract slice and point to foreign procedure instead of copying it.

Make the applicable outcome, trigger, authority, action or branch, Return, and
completion discoverable without requiring a named surface, mandatory heading,
or universal step order.

Treat an implicitly invocable description as the routing predicate. Name
observable request or caller triggers and the closest exclusions. Keep
explicit-name reach, runtime procedure, and body-summary detail out of that
predicate.

Keep common behavior inline. Put branch-only reference behind a pointer that
names both its target and loading condition. Load [GLOSSARY.md](GLOSSARY.md)
when invocation, information hierarchy, pruning, or completion vocabulary
affects the work. Split only for independent invocation, irreducible branch
load, or an observed persistent early-stop defect after sharpening its
completion criterion.

## Behavior-Preserving Cuts

Keep clauses that change intended behavior, safety, authority, proof,
irreversible order, safe failure, Return, or completion. For each proposed
cut, ask: "If I cut this, what behavior changes?" Restore one owner; remove
no-ops, duplicated meaning, stale exposition, and clauses without an intent or
local-contract owner. State the positive target first and pair every necessary
guardrail with its safe action.

## Claim-Matched Proof

Use read-back for exact bytes and mutations, focused structural checks for
machine contracts, and relationship traces for ownership. When a claim says
wording changes invocation, judgment, action, context loading, Return, or
completion, load [BEHAVIOR-EVALS.md](BEHAVIOR-EVALS.md) and use uncontaminated
direct controls. Keep fixed tasks and rubrics, fresh contexts, candidate
language out of control inputs, and judgment with the root. Ambient
collaboration policy owns dispatch mechanics.

## Return

Return `complete`, `partial`, or `blocked` with the selected operation and
coverage. Audit adds the verdict, impact-ordered findings, useful exact
candidates, deliberate non-changes, behavior at risk, and evidence limits.
Author adds changed canonical surfaces, behavior added, changed, or removed,
proof, preserved unrelated state, deliberate non-changes, and residual risk.

Use `partial` when useful bounded judgment exists but admitted coverage or
current proof is incomplete. Use `blocked` when authority or mutation safety
cannot be established. Name every skipped proof, evidence limit, unchanged
foreign state, and residual risk.

Complete only when coverage is classified; every affected invocation surface,
owner, relationship, pointer, gate, output, mutation boundary, Return, and
completion condition has one home; required differences are decided; current
proportionate proof passes or skips are named; exact mutations and work state
are read back; unrelated work is preserved; and execution stops before
installation or delivery.
