# Skill Synthesis Deployment Prompts

Use these prompts after a whole-skill synthesis exists. Change only the final
`Skill name:` value.

Invoke one with, for example:

```text
Run Deploy Prompt 3 for grilling.
```

The default sequence is `1 -> 2 -> 3 -> 4 -> 5`. Skip Prompt 1 only when the
synthesis already contains a current simplest-baseline comparison, a complete
mechanism-admission ledger, and no material decision frontier. Use Prompt 6
only when Git delivery is wanted.

## Deploy Prompt 1: Debate The Synthesis

Conditionally skippable only under the gate above.

```text
First use $writing-great-skills in Audit mode to pressure-test the named skill's complete synthesis. Read the full synthesis and required skill-authoring references; headings, searches, or truncated excerpts are not complete coverage.

Before judging the proposed design, inspect every checked-out upstream below as a mandatory baseline candidate:

- Matt Pocock under `.tmp/mattpocock-skills`;
- Superpowers under `.tmp/superpowers`; and
- Ponytail under `.tmp/ponytail`.

Search ignored paths explicitly, such as with `rg -uu`. For each upstream, locate and completely read the matching or equivalent package when one exists, plus any directly named upstream exclusion or change record capable of changing its interpretation. Record each upstream HEAD, worktree state, and freshness limit independently. Record an absent checkout or missing match as a gap rather than implying coverage.

Also completely inspect the current canonical skill. Compare all available upstream candidates and canonical, then select the simplest credible version that still expresses the core outcome; use a minimal scratch outline only when none does. Treat the selected baseline as a design control, not runtime authority.

Build a mechanism-admission ledger for every behavior beyond that baseline:

<mechanism-admission-ledger>
Mechanism:
Baseline failure or required caller contract:
Evidence:
Owner:
Cheaper alternative:
Runtime, caller, proof, and maintenance load:
Admission: admit | disclose | caller-owned | non-runtime | defer | reject
</mechanism-admission-ledger>

Admit a mechanism only when it cures a demonstrated failure, satisfies a required caller contract, or protects a non-intuitive safety boundary. A conceivable edge case, confirmed recommendation, polished rationale, or existing test is not sufficient evidence by itself.

Explicitly classify every category below, even when no finding exists:

1. Ambiguity — contradictions, overloaded terms, unclear gates, and normal, edge, and failure boundary cases.
2. Ownership — rule, authority, evidence, mutation, Return, relationship, and completion owners.
3. Simplification — duplication, no-ops, scattered meaning, and behavior-preserving cuts.
4. Navigation — authority trace, normative homes, pointers, layer boundaries, and stale or competing surfaces.
5. Leading words — steering value, invocation fit, conflicting anchors, invented terms, and harmful negation.
6. Unnecessary complexity — each mechanism's behavior gained versus runtime, caller, proof, and maintenance load.

For unnecessary complexity, judge common-path versus branch-only load and the aggregate design versus the simplest baseline, not only each mechanism in isolation.

Do not treat `selected`, `normative`, `exhaustive`, rationale, tests, or polished structure as proof that a decision is correct. Challenge the design by inversion, counterexample, ownership trace, and cut test.

Before asking the user anything, produce an internal category ledger containing evidence, verdict, and every unresolved material decision. A category is not closed merely because another category found one obvious issue.

Then use $grill-with-docs to resolve the material decision frontier one question at a time. Recommend an answer and state the decisive tradeoff. After each answer, relay its domain consequence before continuing.

Use domain context `render only` and ADR action `offer only`. Do not edit files or start downstream execution.

Acceptance of one recommendation confirms only that decision. After every category is closed, reconstruct the smallest coherent runtime from the baseline plus admitted mechanisms and re-evaluate the aggregate design. Individual admissions do not justify aggregate complexity. Present that minimum runtime, complete decisions, rejected or deferred machinery, evidence limits, category ledger, and mechanism-admission ledger, then obtain explicit confirmation of the whole packet.

Return the confirmed decision packet, minimum runtime, six-category coverage ledger, mechanism-admission ledger, and Domain Delta. If any category or admitted mechanism lacks complete evidence, return `Blocked` or `Evidence gap`; never claim full confirmation.

Skill name: CHANGE_ME
```

## Deploy Prompt 2: Finalize The Synthesis

```text
Use $writing-great-skills in Author mode to apply our confirmed decisions to the named skill's synthesis and any directly affected synthesis or relationship documents.

Preserve useful exhaustive research as evidence, not automatic runtime authority. Make the normative design name the simplest credible baseline, minimum viable runtime, admitted mechanism deltas, caller-owned or disclosed behavior, rejected and deferred hypotheses, and residual unavoidable complexity. A confirmed decision enters runtime only through its admitted destination.

Before readiness, dry-read the synthesis as Prompt 3 input. Verify that Prompt 3 can classify every behavior and surface without inventing a decision: make the exact baseline, platform-specific vocabulary or adaptations, admitted destination, inline versus disclosed versus caller-owned classification, and proof phase and owner unambiguous. Reconcile competing prose, tables, historical evidence, and current-runtime evidence. Block when extraction would have to choose between instructions, create an unadmitted surface, or encode semantic behavior as Prompt 3 structural proof.

Finish with a readiness decision for experimental extraction. Block readiness when a runtime mechanism lacks admission evidence, a branch-specific contract remains inline without justification, or the aggregate design has not been compared with the simplest baseline. Do not edit runtime skills.

Skill name: CHANGE_ME
```

## Deploy Prompt 3: Create The Experimental Skill

```text
Use $writing-great-skills in Author mode to create a complete experimental candidate for the named skill from its ready synthesis and simplest credible baseline.

Inventory the complete experimental package and every owned or disclosed runtime surface, including `SKILL.md`, metadata, references, scripts, templates, assets, and machine-consumed schemas. Classify every instruction-bearing paragraph, list item, table row, schema field, and distinct clause; do not silently scope the pass to the main skill file.

Start from the baseline's smallest coherent core. Reconcile every synthesis behavior, confirmed decision, guardrail, authority boundary, Return, and completion condition before adding it. Record each as `Baseline`, `Add`, `Disclose`, `Caller-owned`, `Non-runtime`, `Deferred`, or `Rejected`, with its destination, admission evidence, and cheaper alternative. Do not create behavior and hope later pruning removes it; do not continue while any item is unclassified.

Assemble the behavior-complete candidate only from the baseline plus admitted additions. Keep the common path inline. Disclose caller-specific or irreducible branch contracts when their inline load outweighs their common-path value, unless current behavior evidence shows disclosure loses the contract.

Only after coverage is complete, Shape the runtime semantic surface and Prune every instruction-bearing unit with the cut test: "If I cut this, what behavior changes?" Record a `Keep`, `Collapse`, `Disclose`, or `Delete` ledger with enough source and destination detail for Prompt 4 to reconstruct the decision. Retain behavior-changing guidance, protected contracts, and the minimum context or pointer needed to execute them; collapse repeated meaning and disclose branch-only detail. Treat word count as a diagnostic, not proof, and every Prompt 3 prune decision as provisional until Prompt 4 behavior proof.

Record the baseline delta, mechanism-admission ledger, pruning ledger, and residual unavoidable sprawl in one named experimental extraction and pruning evidence record under `docs/validation/`. Update structural proof only for machine-consumed contracts, and update relationship documents only when an invocation, caller, ownership, or Return edge actually changes. Read back and mechanically prove the candidate, then stop before behavioral evaluation, promotion, installation, or Git delivery.

Skill name: CHANGE_ME
```

## Deploy Prompt 4: Audit, Repair, And Evaluate

```text
Use $writing-great-skills in Author mode to audit the named experimental candidate against its synthesis and our confirmed decisions. Refresh the simplest credible baseline, complete-package inventory, baseline delta, and mechanism-admission ledger from Prompt 3, including every owned or disclosed runtime surface and instruction-bearing unit.

Before repairing omissions, challenge every added mechanism against its admission predicate, owner, evidence, cheaper alternative, and aggregate load. A missing synthesis item is an omission only when its admitted runtime destination still holds. Remove unadmitted machinery; move caller-owned and branch-only behavior to its owner or disclosed surface. If this would reverse a confirmed material decision rather than enforce its recorded admission, stop and return the bounded minimality decision frontier instead of silently repairing it.

Only after scope minimality passes, repair genuine omissions and reconstruct a behavior-complete package relative to the admitted runtime surface.

Freeze an exact hash-identified snapshot of that admitted, repaired pre-prune package in an isolated evaluation fixture. Then reperform the Prune audit; do not merely accept the candidate's existing ledger. Classify every instruction-bearing unit as `Keep`, `Collapse`, `Disclose`, or `Delete` using the cut test. Block acceptance until every retained unit changes runtime behavior, preserves a protected contract, or supplies the minimum context or pointer needed to execute one; collapse repeated meaning and disclose branch-only detail. Record residual unavoidable sprawl and compare aggregate runtime load with the baseline; raw word count alone neither passes nor fails the candidate.

After repairs, enter Prove and match proof to the claim. For every added mechanism or behavioral claim, use the simplest credible baseline that can expose its claimed failure; use the current canonical skill only when it is that baseline or the claim specifically changes canonical behavior. Reject guidance when the selected baseline does not exhibit the claimed failure. For every pruning-equivalence claim, use the admitted repaired pre-prune snapshot as the control and the final pruned package as the candidate; reject any wording prune that regresses admitted behavior. Do not require scope cuts of unadmitted machinery to preserve the behavior being removed; instead prove the required outcome, caller contracts, and safety boundaries still hold. A no-guidance arm may diagnose defaults but cannot justify candidate wording. Run fresh behavioral samples for behavioral claims, grouping claims only when one fixed scenario and rubric genuinely tests them; use read-back, mechanical checks, and relationship traces for nonbehavioral claims.

Before dispatch, minimize evaluation cost without weakening evidence. Build one claim-to-proof matrix and deduplicate fixed cases that genuinely share inputs and a root-held rubric. Keep expected behaviors, candidate language, conclusions, and peer outputs out of the neutral worker protocol. Run and judge control locks first; do not dispatch a candidate arm for guidance whose selected control does not exhibit the claimed failure.

Reuse an arm only when its assigned package or surface hash, neutral protocol and fixed inputs, model and reasoning settings, tools, authority, evidence, and runtime are unchanged and the arm remains uncontaminated. Record every reuse and deviation. A fresh worker may lock a metadata-only routing result before seeing its assigned body, then continue in that same context through compatible full-package cases. The exact final-candidate arm may serve both baseline-delta and pruning-equivalence comparisons when one fixed suite and rubric genuinely tests both and the candidate bytes do not change. After a repair, preserve unchanged controls and rerun only behaviorally affected candidate arms. Each unique context counts once per claim it actually exercises; never duplicate a wave merely to rename the comparison.

Keep worker returns compact: one action-and-Return packet per fixed case, plus detail for failures or rubric ambiguity. The root still inspects every result, records per-sample outcomes, variance, worst result, critical failures, unavailable telemetry, and residual gaps. The sampling floor and contamination rules in `BEHAVIOR-EVALS.md` remain unchanged.

Refresh the synthesis and directly affected evidence or relationship documents with what was learned, keeping evaluation ledgers in `docs/validation/` and relationship documents limited to actual edges and ownership boundaries. Return an acceptance decision and stop before promotion.

Skill name: CHANGE_ME
```

## Deploy Prompt 5: Promote And Install

```text
Promote the accepted experimental candidate for the named skill.

First use $writing-great-skills in Author mode to update the canonical skill and directly affected proof, relationship, and synthesis surfaces, stopping after canonical proof.

Reuse the accepted behavioral evidence when the candidate bytes and affected behavioral claims are unchanged; do not run another behavioral-evaluation wave solely for promotion. If either changed, stop and return to behavioral evaluation before promotion.

After that Return, complete the experimental-promotion lifecycle: delete only the promoted skill's entire experimental directory and remove only its manifest entry, preserving every other experimental candidate. Then use the repository's managed installer to update the global installed skill and verify parity. Do not perform Git delivery.

Skill name: CHANGE_ME
```

## Deploy Prompt 6: Git Delivery

Optional.

```text
Deliver the completed named-skill changes through Git.

Include only the bounded synthesis, evaluation, canonical, relationship, test, and experimental-lifecycle changes belonging to this skill. Preserve unrelated work. Commit the verified result, but do not push unless explicitly requested.

Skill name: CHANGE_ME
```
