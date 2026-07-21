# Skill Synthesis Deployment Prompts

Use these prompts after a whole-skill synthesis exists. Change only the final
`Skill name:` value.

Invoke one with, for example:

```text
Run Deploy Prompt 3 for grilling.
```

The default sequence is `2 -> 3 -> 4 -> 5`. Use Prompt 1 only when material
decisions remain and Prompt 6 only when Git delivery is wanted.

## Deploy Prompt 1: Debate The Synthesis

Optional.

```text
First use $writing-great-skills in Audit mode to pressure-test the named skill's complete synthesis. Read the full synthesis and required skill-authoring references; headings, searches, or truncated excerpts are not complete coverage.

Explicitly classify every category below, even when no finding exists:

1. Ambiguity — contradictions, overloaded terms, unclear gates, and normal, edge, and failure boundary cases.
2. Ownership — rule, authority, evidence, mutation, Return, relationship, and completion owners.
3. Simplification — duplication, no-ops, scattered meaning, and behavior-preserving cuts.
4. Navigation — authority trace, normative homes, pointers, layer boundaries, and stale or competing surfaces.
5. Leading words — steering value, invocation fit, conflicting anchors, invented terms, and harmful negation.
6. Unnecessary complexity — each mechanism's behavior gained versus runtime, caller, proof, and maintenance load.

Do not treat `selected`, `normative`, `exhaustive`, rationale, tests, or polished structure as proof that a decision is correct. Challenge the design by inversion, counterexample, ownership trace, and cut test.

Before asking the user anything, produce an internal category ledger containing evidence, verdict, and every unresolved material decision. A category is not closed merely because another category found one obvious issue.

Then use $grill-with-docs to resolve the material decision frontier one question at a time. Recommend an answer and state the decisive tradeoff. After each answer, relay its domain consequence before continuing.

Use domain context `render only` and ADR action `offer only`. Do not edit files or start downstream execution.

Acceptance of one recommendation confirms only that decision. After every category is closed, present the complete decisions, deferrals, evidence limits, and category ledger, and obtain explicit confirmation of the whole packet.

Return the confirmed decision packet, the six-category coverage ledger, and Domain Delta. If any category lacks complete evidence, return `Blocked` or `Evidence gap`; never claim full confirmation.

Skill name: CHANGE_ME
```

## Deploy Prompt 2: Finalize The Synthesis

```text
Use $writing-great-skills in Author mode to apply our confirmed decisions to the named skill's synthesis and any directly affected synthesis or relationship documents.

Preserve useful exhaustive research while simplifying its presentation. Finish with a readiness decision for experimental extraction. Do not edit runtime skills.

Skill name: CHANGE_ME
```

## Deploy Prompt 3: Create The Experimental Skill

```text
Use $writing-great-skills in Author mode to create a complete experimental candidate for the named skill from its ready synthesis and current canonical baseline.

Update directly affected experimental proof and relationship surfaces. Prove the candidate and stop before behavioral evaluation, promotion, installation, or Git delivery.

Skill name: CHANGE_ME
```

## Deploy Prompt 4: Audit, Repair, And Evaluate

```text
Use $writing-great-skills in Author mode to audit the named experimental candidate against its synthesis and our confirmed decisions, then repair any omissions or unnecessary complexity.

After repairs, enter Prove and run behavioral evaluation when warranted by the claims. Refresh the synthesis and directly affected evidence or relationship documents with what was learned. Return an acceptance decision and stop before promotion.

Skill name: CHANGE_ME
```

## Deploy Prompt 5: Promote And Install

```text
Promote the accepted experimental candidate for the named skill.

First use $writing-great-skills in Author mode to update the canonical skill and directly affected proof, relationship, and synthesis surfaces, stopping after canonical proof.

After that Return, complete the experimental-promotion lifecycle and use the repository's managed installer to update the global installed skill and verify parity. Do not perform Git delivery.

Skill name: CHANGE_ME
```

## Deploy Prompt 6: Git Delivery

Optional.

```text
Deliver the completed named-skill changes through Git.

Include only the bounded synthesis, evaluation, canonical, relationship, test, and experimental-lifecycle changes belonging to this skill. Preserve unrelated work. Commit the verified result, but do not push unless explicitly requested.

Skill name: CHANGE_ME
```
