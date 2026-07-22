# Source-To-Skill Prompts

> Archived: these prompts document the retired source-to-runtime pipeline. Use
> [`docs/synthesis/methods/prompts/`](../../../../../docs/synthesis/methods/prompts/)
> for the active source-distillation prompts.

These optional prompts support outside-source discovery and pruning of books,
context, and engineering best practices. They produce evidence for synthesis;
they are not the default skill-development or deployment route.

Use only the prompts needed for the evidence or pruning question. Each selected
prompt should produce a durable artifact without jumping to runtime edits.

## Cadence

- Prompts 1-7 may structure outside-source research and synthesis evidence.
- Prompts 8-12 may help shape, test, and prune candidate evidence before it
  returns to whole-skill synthesis.
- Once a whole-skill synthesis exists, use
  [`docs/synthesis/methods/deploy-prompts.md`](../../../../../docs/synthesis/methods/deploy-prompts.md)
  for deployment.
- Every prompt accepts optional revision feedback. Use `none` on the first
  pass; when looping back, paste the decision and the smallest useful feedback
  from the later prompt or user.
- Each prompt should end with a next-step decision. If the decision says to
  revise, rerun the smallest earlier prompt that owns the problem before moving
  forward.

## Deployment Boundary

This prompt set produces design artifacts and evidence, not runtime authority.
Return selected evidence and pruning decisions to the whole-skill synthesis.
Deploy Prompts own experimental extraction, behavioral acceptance, canonical
promotion, installation, and optional Git delivery.

## Prompts

| Prompt | Step | Output |
| --- | --- | --- |
| [`01-intent-and-keywords.md`](01-intent-and-keywords.md) | Gather intent and preliminary keywords | Skill intent, behavior surface, rough facet candidates, preliminary keyword bank, source-search seeds, and intent decision. |
| [`02-facet-map-and-research-plan.md`](02-facet-map-and-research-plan.md) | Create a facet map | Final facet list, research order, facet boundaries, source lanes, search vocabulary, first facet recommendation, and facet-map decision. |
| [`03-source-search-per-facet.md`](03-source-search-per-facet.md) | Search for great sources per facet | Verified ranked source set, search queries, unverified-source notes, source quality notes, extraction targets, coverage check, next extraction recommendation, and source-search decision. |
| [`04-source-extraction.md`](04-source-extraction.md) | Extract strong source language | Leading words, behavior rules, failure modes, evidence gates, stop/ask conditions, bridge language, no-op language, triage handoff, and extraction decision. |
| [`05-source-triage.md`](05-source-triage.md) | Triage source quality | Keep/reject decisions, ownership routing, runtime/support/research candidates, bridge-needed material, rejection log, agent-bridge handoff, and triage decision. |
| [`06-agent-bridge.md`](06-agent-bridge.md) | Bridge sources into agent behavior | Runtime/support inventories, execution sequence, branches, completion criteria, stop/ask rules, placement guidance, risks, full-synthesis handoff, and agent-bridge decision. |
| [`07-full-behavior-synthesis.md`](07-full-behavior-synthesis.md) | Write full behavior synthesis | Purpose, source pressure, chosen behavior, leading words, execution surface, gates, control logic, placement, rejected options, design questions, repeated-meaning collapse targets, candidate draft handoff, and synthesis decision. |
| [`08-candidate-runtime-draft.md`](08-candidate-runtime-draft.md) | Draft candidate runtime lines | Synthesis-decision gate, candidate invocation wording, runtime steps, gate consequences, owner-boundary scan, context-pointer candidates, candidate log, candidate runtime draft, detailed-draft handoff, and candidate-draft decision. |
| [`09-detailed-skill-context-draft.md`](09-detailed-skill-context-draft.md) | Assemble detailed skill-context draft | Candidate-draft intake gate, owner-boundary check, candidate input, placement/merge map, preserved behavior, integrated detailed draft, traceability map, support placeholders, repetition check, and draft decision. |
| [`10-plain-language-validation-candidate.md`](10-plain-language-validation-candidate.md) | Create plain-language validation candidate | Leading-word and gate plan, plain-language candidate text, preservation check, repetition removal, reality-validation handoff, and plain-language-candidate decision. |
| [`11-validate-against-reality.md`](11-validate-against-reality.md) | Validate against reality | Validation lane, expected behavior, scenario, plain-language-candidate coverage, evidence notes, results, regression risks, decision, and final-prune handoff. |
| [`12-final-prune-and-runtime-patch.md`](12-final-prune-and-runtime-patch.md) | Prune candidate evidence | Validation-driven residual decisions, candidate text, invocation/support evidence, prune log, residual risk, and a synthesis handoff. |

## Boundary

- Put reusable prompts for the source-to-skill flow here.
- Put research outputs in `../../../research/`.
- Put facet synthesis artifacts in `../../facets/`.
- Put whole-skill or legacy synthesis notes in `../../skills/` or `../../families/`.
- Put runtime behavior only in `../../../../skills/custom/`.
- Return evidence to synthesis; do not extract, promote, install, synchronize,
  publish, stage, commit, or push runtime skill changes from this prompt set.
