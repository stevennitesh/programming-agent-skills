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
Use $grill-with-docs to resolve anything material worth debating in the named skill's synthesis: ambiguity, ownership, simplification, navigation, leading words, or unnecessary complexity.

Use domain context `render only` and ADR action `offer only`. Return the confirmed decision packet without editing or downstream execution.

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
