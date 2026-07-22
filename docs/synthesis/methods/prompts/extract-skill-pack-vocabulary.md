# Prompt Profile: Extract Skill-Pack Vocabulary

Use this specialization of Prompts 03-05 in
[`../source-distillation-flow.md`](../source-distillation-flow.md) when one
bounded source question asks what language or vocabulary a skill pack uses.

```markdown
We are extracting the meaningful vocabulary of one skill pack into a
provenance-backed research packet.

Scope packet: `<path or Prompt 01 output>`
Pack name: `<human-readable name>`
Source location: `<checkout path, repository, archive, or URL>`
Requested revision: `<commit, tag, version, or current checked state>`
Included surfaces: `<whole pack or explicit subset>`
Existing vocabulary owners to compare: `<paths or "none">`
Output path: `<authorized path or docs/research/language/<pack-slug>-vocabulary.md>`
Revision feedback: `<feedback or "none">`

Treat the skill pack as primary evidence only for its own language and
behavior. Do not treat its terminology as correct, universal, or suitable for
local adoption merely because it appears upstream.

Freeze the source identity before extraction. Record repository or origin,
revision, worktree state when applicable, verification date, and every package
surface in scope. Inspect all relevant `SKILL.md` files, descriptions and
metadata, disclosed references, routing or relationship docs, templates,
examples, tests, and human-facing docs. Inspect scripts only when their names,
interfaces, output, or comments define pack vocabulary. Classify every
discovered surface as `inspected`, `skipped`, or `not-applicable`, with a
reason for anything skipped.

Build any raw token list, phrase concordance, or frequency report only as
scratch work under an ignored `.tmp/` location. Do not copy the source corpus,
raw concordance, or private source notes into the durable research packet.
Frequency is a discovery signal, never an admission rule.

Find candidate terms from:

- explicit definitions, glossaries, headings, named practices, and repeated
  phrases;
- invocation, routing, ownership, and handoff language;
- workflow actions, branches, states, gates, and stopping conditions;
- artifacts, packets, maps, ledgers, reports, and other named outputs;
- evidence, evaluation, review, completion, and failure language;
- domain, design, debugging, implementation, and planning concepts;
- warnings, exclusions, contrasts, and terms used to name failure modes; and
- distinctive verbs or nouns whose meaning is distributed across several
  package surfaces.

Classify retained terms with one or more of:

- `candidate-leading-word`;
- `invocation-routing`;
- `workflow-control`;
- `artifact-state`;
- `evidence-completion`;
- `domain-design`;
- `relationship-handoff`;
- `failure-exclusion`;
- `pack-specific`.

For every candidate, determine:

- the term and meaningful variants;
- its meaning in this pack, not a dictionary definition;
- the behavior, distinction, or decision the term recruits;
- exact file and heading or line provenance;
- spread across distinct skills or supporting surfaces;
- whether it is explicitly defined, consistently implied, or used
  inconsistently;
- aliases that share its meaning;
- collisions where the same word carries different meanings;
- whether it is established professional language or pack-specific jargon;
- relevant conditions, exclusions, or misuse risks; and
- any comparison with local vocabulary, labeled `synthesis` or `inference`.

Use the source-distillation claim labels exactly: `direct`, `corroborated`,
`synthesis`, `inference`, and `thin`. A repeated upstream use may corroborate
the pack-wide meaning; it does not corroborate the term's external validity.

Retain a term only when it has a traceable pack-specific meaning and materially
improves understanding of how the pack routes, acts, decides, communicates, or
finishes. Prefer one semantic owner for aliases. Keep a deliberately defined
one-off term when it names an important distinction. Reject generic prose,
boilerplate verbs, incidental filenames, framework syntax, unexplained
acronyms, and terms admitted only because they are frequent, memorable, or
unusual.

Return one durable artifact with:

## Question And Boundary

State the vocabulary question, intended use, included and excluded surfaces,
comparison boundary, and freshness target.

## Source Identity

| Pack | Origin | Revision | Worktree State | Verified | Authority | Limitation |
| --- | --- | --- | --- | --- | --- | --- |

## Coverage

| Surface | Inspected / Skipped / Not Applicable | Files Or Count | Consequence |
| --- | --- | --- | --- |

Include enough inventory detail to prove whole-pack or declared-subset
coverage without copying the source tree into the packet.

## Vocabulary Clusters

Group related terms by semantic function, not by source folder or alphabetical
order. Explain the shared concept and important distinctions in each cluster.

## Retained Vocabulary

| Term | Variants | Class | Meaning In This Pack | Behavior Or Distinction Recruited | Spread | Claim Label | Best Provenance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Techniques Encoded By The Language

| Vocabulary | Technique | Essential Mechanics | Use Context In The Pack | Failure / Misuse Risk | Claim Label | Provenance |
| --- | --- | --- | --- | --- | --- | --- |

## Aliases, Collisions, And Inconsistencies

| Terms | Relationship | Evidence | Consequence For Interpretation |
| --- | --- | --- | --- |

## Inferred Applications

Keep upstream meaning separate from proposed local use. Label every local
comparison or possible adoption `synthesis` or `inference`, name the assumption
that would need validation, and make no runtime or vocabulary-owner edit.

## Prune Log

| Removed Or Merged Material | Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |

Cluster ordinary rejected words instead of producing a stop-word inventory.

## Evidence Gaps

Name skipped surfaces, ambiguous meanings, inconsistent uses, inaccessible
references, revision uncertainty, and any term whose external origin or local
fit was not verified.

## Final Decision

Choose exactly one:

- `source-packet-complete`;
- `evidence-gap`, naming what remains usable and what cannot be claimed;
- `blocked`, naming the access, scope, or verification blocker.

When the output path already exists, reconcile it in place against the new
revision. Preserve still-supported meanings, update provenance, remove stale
terms, and rely on Git history rather than creating a new dated audit unless
the caller explicitly requests a historical comparison.
```

Complete when the declared package surface is accounted for; every retained
term has semantic meaning, exact provenance, honest breadth, and one cluster;
aliases and collisions are resolved or disclosed; generic material is pruned;
scratch source data remains ignored; and the terminal decision matches the
evidence. The prompt stops at research evidence and does not select canonical
vocabulary, draft runtime wording, or edit a skill.
