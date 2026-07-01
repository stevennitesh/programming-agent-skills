# Source-To-Skill Flow

Use this flow to build or deepen a skill without turning research into runtime
bloat.

The purpose is to move from intent and source pressure into compact,
behavior-changing skill language. Each step should become a reusable prompt.

```text
intent
  -> facet map
  -> source search
  -> source extraction
  -> source triage
  -> behavior flow
  -> generous synthesis
  -> compact language
  -> behavior audit
  -> validation
  -> prune
```

## 1. Gather Intent And Preliminary Keywords

Prompt: [`prompts/01-intent-and-keywords.md`](prompts/01-intent-and-keywords.md).

Name the skill's job:

- what behavior should become predictable;
- when the skill should be invoked;
- what current skill, related skills, contracts, and docs already say;
- what preliminary keywords, terms, and source lanes might matter.

Do this before online search so the search has a target.

## 2. Create A Facet Map

Prompt: [`prompts/02-facet-map-and-research-plan.md`](prompts/02-facet-map-and-research-plan.md).

Split the skill into facets before deep research.

Each facet should name:

- the behavior surface it affects;
- the research question;
- likely source lanes;
- likely completion or stop gates;
- what is out of scope for that facet.

This prevents one large vague research blob.

## 3. Search For Great Sources Per Facet

Prompt: [`prompts/03-source-search-per-facet.md`](prompts/03-source-search-per-facet.md).

Search by facet, not by the whole skill at once.

Use:

- classic and professional books for taste;
- official manuals and docs for current agent/tool behavior;
- empirical papers for correction and failure modes;
- field practice for operational realism.

## 4. Extract Strong Source Language

Prompt: [`prompts/04-source-extraction.md`](prompts/04-source-extraction.md).

Extract only what can change skill behavior:

- leading words;
- rules;
- failure modes;
- evidence gates;
- stop/ask conditions;
- weak or no-op language to avoid.

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

## 6. Create The Behavior Flow

Prompt: [`prompts/06-behavior-flow.md`](prompts/06-behavior-flow.md).

Turn source language into an execution chain:

```text
source taste term
  -> agent execution surface
  -> evidence gate
  -> stop/ask rule
```

This is where strong words become behavior rather than vocabulary.

## 7. Write Generous Synthesis

Prompt: [`prompts/07-generous-synthesis.md`](prompts/07-generous-synthesis.md).

Use [`../GENEROUS-TEMPLATE.md`](../GENEROUS-TEMPLATE.md).

Include all facets, trade-offs, rejected options, design questions, and why the
skill should behave a certain way.

Generous synthesis may be verbose. It must still end with a compression
handoff.

## 8. Compact Into Strong Plain Language

Prompt: [`prompts/08-compact-language-draft.md`](prompts/08-compact-language-draft.md).

Use [`../TEMPLATE.md`](../TEMPLATE.md) and
[`controlled-language-pass.md`](controlled-language-pass.md).

Turn generous synthesis into candidate runtime wording.

Keep elite engineering words. Plain-language the gates.

Do not flatten the taste. Keep `tracer bullet`, `red-green-refactor`, `seam`,
`fixed-point review`, and other strong terms when they recruit useful priors.

Make gates blunt:

```text
No proof, no done.
Red must fail for the missing behavior.
Stop, split, or ask.
```

## 9. Run A Behavior Audit

Prompt: [`prompts/09-behavior-audit.md`](prompts/09-behavior-audit.md).

After compaction, test every proposed runtime line or rule:

- What behavior does this change?
- What failure mode does it prevent?
- What proof does it require?
- Is this already owned by another skill or the engineering contract?
- Is this a leading word, a gate, or a no-op?
- Is it duplicated, too long, or better moved behind a context pointer?

## 10. Validate Against Reality

Prompt: [`prompts/10-validate-against-reality.md`](prompts/10-validate-against-reality.md).

Test the compact wording against real tasks, old transcripts, fixtures, or
representative repo work.

Check whether it makes the agent:

- read better context;
- choose a better slice;
- stop at the right boundary;
- prove harder;
- avoid overclaiming;
- report residual risk honestly.

## 11. Prune

Prompt: [`prompts/11-final-prune-and-runtime-patch.md`](prompts/11-final-prune-and-runtime-patch.md).

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
