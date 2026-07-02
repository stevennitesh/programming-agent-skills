# Source-To-Skill Flow

Use this flow to build or deepen a skill without turning research into runtime
bloat.

The purpose is to move from current-skill intent and source pressure into
behavior-changing skill language. Each step should become a reusable prompt.

```text
intent
  -> facet map
  -> source search
  -> source extraction
  -> source triage
  -> agent bridge
  -> full behavior synthesis
  -> candidate runtime draft
  -> detailed skill-context draft
  -> plain-language validation candidate
  -> reality validation
  -> final prune
```

## Cadence

Run Prompts 1-2 once for the skill.

Run Prompts 3-7 once per facet. These prompts build facet-specific research,
triage, agent bridge, and full behavior synthesis without editing runtime skill
wording.

Run Prompts 8-12 when you are ready to integrate candidate runtime wording.
That can be:

- `facet integration`: draft candidate runtime lines, assemble a detailed
  skill-context draft, create the plain-language candidate, validate that
  candidate, and prune one facet into a small runtime patch when the facet is
  independent enough; or
- `whole-skill integration`: draft multiple completed facets together so
  overlapping runtime steps, context pointers, and ownership boundaries are
  resolved in one pass.

Default to finishing Prompts 3-7 for enough facets to understand the skill's
shape before applying runtime edits. Use facet integration only when early
runtime feedback is worth the collision risk with later facets.

Each prompt accepts optional revision feedback. Use `none` on the first pass.
When a later prompt loops back, paste the decision and the smallest useful
feedback into the earlier prompt so the rerun addresses the specific failed
gate.

## Feedback Loops

Every prompt should end with a next-step decision, not only a handoff. Use the
smallest loop that fixes the problem:

| Prompt | Continue When | Loop Back When |
| --- | --- | --- |
| 01 Intent | intent, current surface, owner map, preserve inventory, rough facets, collision risks, and search seeds are clear enough for a facet map | user goal, current skill surface, preserve-critical behavior, or related-owner context is missing |
| 02 Facet Map | Step 1 inputs are accounted for, facets have distinct behavior surfaces, collision risks are named, order is clear, and the first facet has an explicit decision | facets overlap, boundaries are unclear, Step 1 owner/preserve inputs are not consumed, or the skill intent needs revision |
| 03 Source Search | Prompt 02 boundaries and lanes are accounted for, source set is verified and accessible enough, rejected/thin lanes are logged, and extraction targets are clear | a source lane is missing, sources are unverified or inaccessible, rejected/thin lanes are unexplained, or the facet boundary appears wrong |
| 04 Extraction | Prompt 03 targets are accounted for, extracted items connect source pressure to agent behavior, gates, misuse risk, and claim strength, and boundary drift is flagged | source coverage is weak, source verification/access fails, extraction targets are skipped without reason, or extracted material does not fit the facet boundary |
| 05 Triage | surviving material has runtime/support/research ownership, owner-conflict severity, bridge translations, runtime priority, duplicate-collapse choices, and rejection reasons | everything is owned elsewhere, bridge material is not executable, priorities are too broad, or extraction/search gaps block judgment |
| 06 Agent Bridge | source language is bridged into agent actions, typed gates, branch exits, stop rules, priority preservation, duplicate-term choices, and owner-severity-aware placement | gates are vague/heavy, branches are fuzzy, priority expands beyond triage, or ownership conflicts require triage/facet revision |
| 07 Full Behavior Synthesis | behavior, trade-offs, typed gates, branch exits, placement, rejected options, runtime budget, repeated-meaning collapse targets, and candidate draft contract are clear | design questions still change the agent bridge, typed gates, branch exits, priority, or ownership decisions |
| 08 Candidate Runtime Draft | candidate runtime lines have stable IDs, placement/merge targets, runtime weights, Prompt 07 handoff accounting, owner-risk notes, and preserve existing behavior | candidate lines lose taste, create no-ops, cannot be placed without duplication, or expose synthesis/bridge gaps |
| 09 Detailed Skill-Context Draft | draft decision is `ready-for-plain-language-candidate`, Prompt 08 lines are assembled into current skill context with full useful detail, repeated runtime meaning removed, and placement/preservation traceability clear | placement cannot preserve behavior, candidate lines are insufficient, wording cannot be assembled cleanly, repeated runtime meaning remains, or an owner/support decision is blocked |
| 10 Plain-Language Candidate | plain-language-candidate decision is `ready-for-reality-validation`, leading words and blunt gates preserve Prompt 09 behavior, repeated runtime meaning is removed, and Prompt 11 can test the actual text that might ship | plain-language wording loses behavior, hides placement, weakens traceability, creates unvalidated behavior, repeats meaning, or exposes Prompt 09/08 gaps |
| 11 Reality Validation | validation decision is `ready-for-final-prune`, Prompt 09/10 traceability is accounted for, and evidence covers the plain-language candidate rather than the explanatory draft or loose candidate lines | `revise-before-prune` loops to Prompt 10, Prompt 09, or earlier based on the failed evidence; `needs-more-validation` stays in Prompt 11; `blocked` resolves the named validation blocker |
| 12 Final Prune | final-prune decision is `plan-ready` or `edit-applied`, final text is validation-backed, non-duplicative, and either patch-shaped or applied in the requested mode | validation is weak, final text introduces unvalidated behavior, support/runtime ownership is unresolved, or Prompt 11 did not decide `ready-for-final-prune` |

Do not skip forward with a known weak gate. A short loop now is cheaper than
validating wording the draft already shows is weak.

## 1. Gather Intent And Preliminary Keywords

Prompt: [`prompts/01-intent-and-keywords.md`](prompts/01-intent-and-keywords.md).

Name the skill's job:

- what behavior should become predictable;
- when the skill should be invoked;
- what current skill, related skills, contracts, and docs already say;
- which behavior is owned here versus elsewhere;
- which existing behaviors must not regress;
- which rough facets are likely to collide and need Prompt 02 decisions;
- what preliminary keywords, terms, and source lanes might matter.

Do this before online search so the search has a target.
Do not decide the final facet map here; record the boundary questions Prompt 02
must resolve.

## 2. Create A Facet Map

Prompt: [`prompts/02-facet-map-and-research-plan.md`](prompts/02-facet-map-and-research-plan.md).

Split the skill into facets before deep research.

Each facet should name:

- the behavior surface it affects;
- the research question;
- likely source lanes;
- likely completion or stop gates;
- what is out of scope for that facet.

The map should also account for Step 1 owner/preserve inputs, record how rough
facets were kept, merged, split, retired, or deferred, and name cross-facet
collision risks before source search begins. This prevents one large vague
research blob without letting Step 2 do the research itself.

## 3. Search For Great Sources Per Facet

Prompt: [`prompts/03-source-search-per-facet.md`](prompts/03-source-search-per-facet.md).

Search by facet, not by the whole skill at once.

Use:

- classic and professional books for taste;
- official manuals and docs for current agent/tool behavior;
- empirical papers for correction and failure modes;
- field practice for operational realism.

Account for the facet map's boundaries, source lanes, avoided lanes, and
collision watchpoints. Record rejected or thin lanes, verify access enough for
extraction, and return to Prompt 02 if the best sources show the facet boundary
is wrong.

## 4. Extract Strong Source Language

Prompt: [`prompts/04-source-extraction.md`](prompts/04-source-extraction.md).

Extract only what can change skill behavior:

- leading words;
- rules;
- failure modes;
- evidence gates;
- stop/ask conditions;
- weak or no-op language to avoid.

Account for Prompt 03's recommended source set, extraction targets, and access
notes. Distinguish direct source claims from cross-source synthesis and agentic
bridge inferences, and flag material that may belong to another facet before
Prompt 05 triage decides ownership.

Do not import summaries for their own sake.

## 5. Triage Source Quality

Prompt: [`prompts/05-source-triage.md`](prompts/05-source-triage.md).

Keep only sources that improve agent behavior.

Reject or demote sources that produce:

- vague slogans;
- generic advice;
- decorative terminology;
- claims without operational gates;
- source pressure already better owned by another skill or contract.

Account for Prompt 04's claim strength, extraction-target coverage, and
boundary-drift notes. Mark owner conflicts by severity, translate bridge-needed
material into plain behavior targets, collapse duplicate terms, and give Prompt
06 a small prioritized runtime pile.

## 6. Bridge Sources Into Agent Behavior

Prompt: [`prompts/06-agent-bridge.md`](prompts/06-agent-bridge.md).

Turn source language into an execution chain:

```text
source taste term
  -> agent execution surface
  -> evidence gate
  -> stop/ask rule
```

Preserve Prompt 05's runtime priorities, bridge translations, duplicate-collapse
choices, and owner-conflict severity. Type gates as hard gates, rechecks,
handoffs, or support cues, and make each branch say whether it rejoins, asks,
hands off, records follow-up, or blocks.

This is where strong words become behavior rather than vocabulary.

## 7. Write Full Behavior Synthesis

Prompt: [`prompts/07-full-behavior-synthesis.md`](prompts/07-full-behavior-synthesis.md).

For a facet run, include that facet's trade-offs, rejected options, design
questions, and why the facet should behave a certain way. For a whole-skill
integration run, include all completed facets being integrated.

Preserve Prompt 06's typed gates, branch exits, priority preservation,
duplicate-term choices, and owner-severity decisions. End with a candidate draft
contract that names what Prompt 08 must preserve, may compress, must demote to
support, must not carry forward, and should collapse as repeated meaning.

Full behavior synthesis may be verbose. It must still end with a candidate
runtime draft handoff.

## 8. Draft Candidate Runtime Lines

Prompt: [`prompts/08-candidate-runtime-draft.md`](prompts/08-candidate-runtime-draft.md).

Turn full behavior synthesis into candidate runtime lines for detailed-draft
assembly.

Start only when Prompt 07 decided `ready-for-candidate-runtime-draft`. If
Prompt 07 did not, return to the owning prompt named by the full behavior
synthesis.

Choose the scope deliberately: draft one facet only when doing facet
integration, or draft multiple completed facets together when runtime wording
needs a whole-skill pass.

Account for Prompt 07's candidate runtime draft handoff before drafting:
preserve required gates, branch exits, leading words, runtime budget, support
demotions, resolved/deferred design questions, and repeated meanings to
collapse.

Scan likely owner conflicts before drafting lines, but leave full placement and
owner-boundary assembly to Prompt 09.

Give every candidate runtime line a stable ID. Draft placement against the
existing `SKILL.md` as `insert`, `replace`, `merge`, `keep existing`, `owned
elsewhere`, `defer to support`, or `cut`, but do not edit the skill yet.

Use Prompt 08's exact runtime-weight labels (`must-runtime`,
`candidate-runtime`, `support-only`, `research-only`, `likely-prune`) and core
classes (`Runtime Core`, `Validation Detail`, `Support`, `Cut`) so Prompt 09
can consume them without translation.

Separate the smallest likely runtime core from fuller detailed-draft material
so Prompt 09 can assemble all useful behavior before plain-language
compression.

Do not convert the wording to plain language yet. Prompt 10 owns that pass
after Prompt 09 has assembled the detailed skill-context draft.

## 9. Assemble A Detailed Skill-Context Draft

Prompt: [`prompts/09-detailed-skill-context-draft.md`](prompts/09-detailed-skill-context-draft.md).

Merge Prompt 08 candidate lines into the current skill context as a detailed
draft. This is where all useful detail gets skill-shaped before any
plain-language compression.

Start only when Prompt 08 decided `ready-for-detailed-skill-context-draft`. If
Prompt 08 did not, return to the owning prompt named by the candidate runtime
draft.

Preserve existing behavior around the candidate lines. Show exact placement,
merge, replacement, support-placeholder, and not-assembled decisions. Keep line
IDs and validation scenario IDs in traceability tables, not in the runtime prose
unless the project explicitly wants them there.

Check owner boundaries before writing the draft: existing skill sections,
engineering contract, tracker docs, related skills, support docs, later skill
steps, and user decisions can provide context or pointers, but Prompt 09 must
not inline their owned procedures.

Do not run the plain-language pass yet. Do not validate against tasks yet.
Do not final-prune. Do not edit `SKILL.md`.

End with a draft decision:

- `ready-for-plain-language-candidate`: continue to Prompt 10;
- `revise-candidate-runtime-draft`: return to Prompt 08;
- `blocked`: resolve the named owner, support-doc, or user decision before
  continuing.

## 10. Create The Plain-Language Validation Candidate

Prompt:
[`prompts/10-plain-language-validation-candidate.md`](prompts/10-plain-language-validation-candidate.md).

Use [`plain-language-pass.md`](plain-language-pass.md).

Collapse the detailed draft into the wording that reality validation will test.
Keep the elite engineering words that recruit useful priors. Convert the gates
to plain language, not the taste.

Make gates blunt:

```text
No proof, no done.
Red must fail for the missing behavior.
Stop, split, or ask.
```

End with a plain-language-candidate decision:

- `ready-for-reality-validation`: continue to Prompt 11;
- `return-to-detailed-skill-context-draft`: return to Prompt 09;
- `blocked`: resolve the named owner, support-doc, or user decision before
  continuing.

## 11. Validate Against Reality

Prompt: [`prompts/11-validate-against-reality.md`](prompts/11-validate-against-reality.md).

Test the plain-language candidate against real tasks, old transcripts, fixtures,
or representative repo work.

Check whether it makes the agent:

- read better context;
- choose a better slice;
- stop at the right boundary;
- prove harder;
- avoid overclaiming;
- report residual risk honestly.

Do not validate loose candidate lines or the explanatory Prompt 09 draft.
Validate the plain-language candidate from Prompt 10 so the actual words that
may ship are part of the evidence.

Start from Prompt 10's plain-language-candidate decision, Prompt 09/10
traceability maps, and validation scenario IDs. If the plain-language-candidate
decision is not `ready-for-reality-validation`, return to Prompt 10 or the
earlier owning prompt instead of validating anyway.

## 12. Prune

Prompt:
[`prompts/12-final-prune-and-runtime-patch.md`](prompts/12-final-prune-and-runtime-patch.md).

Only final-prune after Prompt 11 decides `ready-for-final-prune`. If validation
requires revision, rerun the smallest owning prompt before producing final
runtime text.

Remove:

- no-ops;
- repeated meaning;
- decorative language;
- source explanation that belongs in docs;
- branch-specific reference that should move behind a pointer.

The final runtime skill should keep only behavior-changing wording.

## Prompt Work

Future prompt docs should follow this file one step at a time. Each prompt
should name its input, output, quality bar, and promotion target.
