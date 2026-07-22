# Source Distillation Flow

Use this optional method when outside evidence would improve a synthesis,
design decision, or engineering practice. It turns inspected sources into a
small, provenance-backed set of important concepts and usable techniques.

```text
scope question
  -> optional facet map
  -> search and verify sources
  -> extract concepts and techniques
  -> distill source packet
       |-> source-packet-complete
       |-> evidence-gap
       `-> blocked
```

The flow ends at evidence. It does not design agent behavior, draft runtime
instructions, edit a skill, run behavioral evaluation, promote a candidate,
install, or deliver through Git. Return the final source packet to the owner of
the synthesis or decision that requested it.

## Source Standard

Prefer the source closest to the claim:

- official documentation, standards, specifications, original papers, and
  canonical repositories for current facts and defined behavior;
- upstream skill packages for what those packages actually instruct or
  implement;
- inspected books, chapters, and author material for durable concepts,
  techniques, tradeoffs, and professional taste;
- credible secondary synthesis or field practice when it adds comparison,
  adoption evidence, or operational context unavailable from a primary source.

An upstream skill is primary evidence of its own content, not proof that its
advice is correct. A book title, abstract, search snippet, review, or metadata
record proves only what was actually visible there. Label access depth and do
not upgrade an indirect source into a direct claim.

For current or changeable claims, verify the live source and record the check
date. For a checked-out upstream package, record the repository, revision or
commit, worktree state, files inspected, and whether referenced files, scripts,
examples, and explicit exclusions were covered.

## Claim Labels

Keep source claims separate from interpretation:

- `direct`: supported by the inspected source section;
- `corroborated`: independently supported by multiple inspected sources;
- `synthesis`: a comparison or conclusion drawn across sources;
- `inference`: a proposed application beyond what the source directly says;
- `thin`: plausible, but the accessible evidence is incomplete or indirect.

Every retained item names its source, locator, claim label, applicable context,
and limitation. Contradictions remain visible; do not manufacture consensus.

## Cadence

Run Prompt 01 once per bounded source question. Run Prompt 02 only when the
question has multiple genuinely independent facets; a narrow question proceeds
directly to search. Run Prompts 03-05 per facet or for the whole bounded
question.

Use the smallest feedback loop that repairs the evidence:

| Step | Continue when | Return when |
| --- | --- | --- |
| 01 Scope | question, intended use, boundaries, source lanes, and freshness needs are explicit | the requested outcome or evidence boundary is unclear |
| 02 Map | facets are non-duplicative and each has a research question | the map adds ceremony or hides one narrow question |
| 03 Search | the strongest relevant sources are verified, accessible, and queued for exact extraction | coverage, access, freshness, or source quality is insufficient |
| 04 Extract | useful claims, concepts, techniques, context, limits, and disagreements are traceable to inspected sections | extraction depends on unseen text or exposes a source gap |
| 05 Distill | every retained item passes the admission standard and rejected material and gaps are recorded | weak evidence, unresolved contradiction, or missing context prevents a trustworthy packet |

## Steps

1. [Scope the source question](prompts/01-scope-source-question.md). Define the
   question, intended use, exclusions, source lanes, and evidence freshness.
2. [Map research facets](prompts/02-map-research-facets.md) only when useful.
   Split by independent research questions, not future document sections or
   runtime behavior.
3. [Search and verify sources](prompts/03-search-and-verify-sources.md). Record
   queries, rejected lanes, access depth, freshness, and exact extraction
   targets.
4. [Extract concepts and techniques](prompts/04-extract-concepts-and-techniques.md).
   Preserve source meaning, provenance, context, tradeoffs, limitations, and
   disagreement before judging what survives.
5. [Distill the source packet](prompts/05-distill-source-packet.md). Collapse
   duplicates, reject weak or generic material, separate facts from inference,
   and retain only important concepts and usable techniques.

When the bounded question asks what language a skill pack uses, apply the
[skill-pack vocabulary profile](prompts/extract-skill-pack-vocabulary.md)
across Prompts 03-05. It adds whole-package coverage, semantic clustering,
alias and collision analysis, and refresh-in-place output without creating a
second workflow.

## Admission Standard

Retain an item only when it:

- answers the bounded source question;
- is supported at the strength claimed by inspected evidence;
- materially improves understanding, judgment, or technique;
- retains the conditions, tradeoffs, and limitations needed for safe use; and
- adds meaning not already represented by a stronger retained item.

Interesting, famous, memorable, or repeated material does not survive on that
basis alone.

## Final Source Packet

Prompt 05 produces one decision-ready artifact containing:

- question, scope, intended use, and exclusions;
- verified source registry with access depth and freshness;
- important concepts;
- usable techniques and when to use them;
- claim labels, exact provenance, limitations, and disagreements;
- pruned and rejected material with reasons;
- unresolved evidence gaps; and
- applications or adaptations clearly labeled as inference.

Use a caller-authorized path. For general work, default to
`docs/research/source-packets/<topic>.md`; for an existing owned research area,
write inside that area instead of creating a second owner.

Completion is exactly one of:

- `source-packet-complete`: the packet meets the admission and provenance
  standards;
- `evidence-gap`: the packet is usable only with the named missing or weak
  evidence disclosed; or
- `blocked`: access, scope, or verification prevents trustworthy distillation.
