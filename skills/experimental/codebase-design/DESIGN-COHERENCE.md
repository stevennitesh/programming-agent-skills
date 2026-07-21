# Design Coherence

Apply this reference read-only when a caller needs design framing or coherence checking without a design recommendation. The caller supplies the bounded artifact, accepted constraints, evidence, mutation boundary, and use of the result.

This reference never selects architecture, invokes another skill, mutates caller state, or converts a gap into a ticket, blocker, fog item, or route. A real design decision remains one bounded `$codebase-design` Direct Design pass.

## Criteria

| Criterion | Coherent evidence | Typed gap |
| --- | --- | --- |
| **Responsibility** | Each material behavior, invariant, decision, and failure policy has one appropriate owner | Ownership is missing, duplicated, circular, or forces callers to coordinate hidden policy |
| **Interface** | Material operations, inputs, outputs, invariants, ordering, errors, configuration, performance, and behavior are explicit | Dependent decisions assume incompatible or underspecified caller contracts |
| **Dependency** | Direction preserves domain ownership and locality; transport and vendor concerns remain outside domain decisions | Dependencies invert ownership, leak transport, or create cycles and cross-layer coordination |
| **Seam** | Every seam is earned by locality, isolation, domain ownership, real variation, or testability | A seam is hypothetical, misplaced, duplicative, or shallow |
| **Migration** | First step, compatibility, cutover, rollback, and preservation obligations are explicit when commitments change | Settled decisions cannot evolve safely or disagree about compatibility and transition |
| **Proof** | Observable behavior is provable through the caller-facing interface; enforced boundaries include allowed and forbidden callers plus a red-capable check | Proof depends on implementation detail, omits a material caller, or cannot demonstrate the boundary |

Mark a criterion `not applicable` only with evidence that the bounded artifact creates or changes none of that concern.

## Frame

Use while design-relevant meaning is not yet settled. Give every applicable criterion exactly one disposition:

- **Constraint:** accepted source fixes the boundary.
- **Question:** one sharp design decision is required.
- **Evidence gap:** the concern is material but needs named evidence or another decision before its question is sharp.
- **Not applicable:** evidence proves the criterion does not bear on the artifact.

Frame answers no Question and fills no Evidence gap. It completes when every criterion has one disposition, every Constraint cites accepted source, every Question fits one Direct Design pass, and every Evidence gap names its sharpening source.

## Check

Use only with settled decisions, constraints, evidence, and the bounded current or proposed shape.

For each applicable criterion, identify affected responsibilities, interfaces, dependencies, seams, migration commitments, callers, and proofs; compare the settled statements; then record `pass` with evidence or return a typed gap. Preserve missing material evidence as a gap.

Return `coherent` only when every applicable criterion passes and no material incompatibility or missing proof remains.

## Typed Gap

```text
Criterion:
Affected decisions, interfaces, dependencies, callers, or proofs:
Conflicting or missing source:
Caller-facing consequence:
Why material to the bounded artifact:
Required owner or evidence:
Proof needed to close:
```

## Return And Completion

```text
Mode: Frame | Check
Artifact and scope:
Criteria results:
Constraints and source pointers:
Questions or typed gaps:
Evidence gaps and sharpening sources, when framing:
Verdict: framed | coherent | gaps
Caller retains: artifact, disposition, mutation, and completion authority
```

Complete when every applicable criterion has evidence or an exact gap, the packet is internally consistent, and no caller or foreign state changed.
