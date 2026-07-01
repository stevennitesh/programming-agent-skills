# Source-To-Skill Prompts

These prompts turn the source-to-skill flow into reusable work steps.

Use one prompt at a time. Each prompt should produce a durable artifact that
feeds the next step without jumping straight to runtime `SKILL.md` edits.

## Prompts

| Prompt | Step | Output |
| --- | --- | --- |
| [`01-intent-and-keywords.md`](01-intent-and-keywords.md) | Gather intent and preliminary keywords | Skill intent, behavior surface, rough facet candidates, preliminary keyword bank, and source-search seeds. |
| [`02-facet-map-and-research-plan.md`](02-facet-map-and-research-plan.md) | Create a facet map | Final facet list, research order, facet boundaries, source lanes, search vocabulary, and first facet recommendation. |
| [`03-source-search-per-facet.md`](03-source-search-per-facet.md) | Search for great sources per facet | Verified ranked source set, search queries, unverified-source notes, source quality notes, extraction targets, coverage check, and next extraction recommendation. |
| [`04-source-extraction.md`](04-source-extraction.md) | Extract strong source language | Leading words, behavior rules, failure modes, evidence gates, stop/ask conditions, bridge language, no-op language, and triage handoff. |
| [`05-source-triage.md`](05-source-triage.md) | Triage source quality | Keep/reject decisions, ownership routing, runtime/support/research candidates, bridge-needed material, rejection log, and behavior-flow handoff. |
| [`06-behavior-flow.md`](06-behavior-flow.md) | Create the behavior flow | Runtime/support inventories, execution sequence, branches, completion criteria, stop/ask rules, placement guidance, risks, and synthesis handoff. |
| [`07-generous-synthesis.md`](07-generous-synthesis.md) | Write generous synthesis | Purpose, source pressure, chosen behavior, leading words, execution surface, gates, control logic, placement, rejected options, design questions, and compression handoff. |
| [`08-compact-language-draft.md`](08-compact-language-draft.md) | Compact into strong plain language | Candidate invocation wording, runtime steps, blunt gates, context-pointer candidates, compression log, compact draft, and audit handoff. |
| [`09-behavior-audit.md`](09-behavior-audit.md) | Run a behavior audit | Line inventory, behavior verdicts, no-op checks, gate strength, ownership, context pointers, leading words, regression check, and validation handoff. |
| [`10-validate-against-reality.md`](10-validate-against-reality.md) | Validate against reality | Validation lane, expected behavior, scenario, line coverage, evidence notes, results, regression risks, decision, and final-prune handoff. |
| [`11-final-prune-and-runtime-patch.md`](11-final-prune-and-runtime-patch.md) | Prune and prepare runtime patch | Validation-driven final decisions, final runtime text, invocation/support decisions, prune log, residual risk, optional applied edit record, and completion summary. |

## Boundary

- Put reusable prompts for the source-to-skill flow here.
- Put research outputs in `../../../research/`.
- Put generous or compact synthesis notes in `../../`.
- Put runtime behavior only in `../../../../skills/current/`.
