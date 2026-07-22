# Prompt 05: Distill The Source Packet

Use this as Step 5 of
[`../source-distillation-flow.md`](../source-distillation-flow.md).

```markdown
We are pruning extracted evidence into a decision-ready source packet.

Scope packet: `<path or Prompt 01 output>`
Facet map: `<path or "not needed">`
Source-search packet(s): `<paths or Prompt 03 outputs>`
Extraction packet(s): `<paths or Prompt 04 outputs>`
Output path: `<caller-authorized path>`
Revision feedback: `<feedback or "none">`

Do not search or extract new material except to identify a precise gap. Do not
draft skill instructions or prescribe a downstream design. Retain an item only
when it answers the question, is supported at the strength claimed, materially
improves understanding or technique, preserves necessary limits, and is not
duplicated by a stronger item.

Return one artifact with:

## Question And Boundary

State the question, intended use, inclusions, exclusions, and freshness target.

## Verified Source Registry

Carry forward the sources actually used, their access depth, revision or check
date, exact locators, authority, and limitations.

## Important Concepts

| Concept | Concise Meaning | Why It Matters | Claim Label | Best Provenance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- |

## Usable Techniques

| Technique | Purpose | Essential Mechanics | Use When | Avoid / Adapt When | Claim Label | Best Provenance |
| --- | --- | --- | --- | --- | --- | --- |

## Disagreements And Context

Preserve material source conflicts and explain contextual differences only at
the strength supported. Do not force consensus.

## Inferred Applications

Keep source facts separate from proposed uses. Label each adaptation
`inference` and name the assumption that downstream work must validate.

## Prune Log

| Removed / Merged Material | Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |

Reasons include duplicate, generic, decorative, off-question, indirect, stale,
unsupported, source-specific without transfer value, or superseded by stronger
evidence.

## Evidence Gaps

Name missing access, thin claims, unresolved contradictions, freshness risk,
and questions the packet cannot answer.

## Final Decision

Choose exactly one:

- `source-packet-complete`;
- `evidence-gap`, naming what remains usable and what cannot be claimed;
- `blocked`, naming the access, scope, or verification blocker.
```

Complete when every retained concept and technique earns its place, exact
provenance and limitations remain visible, duplicate and weak material is
logged, and the terminal decision matches the evidence.
