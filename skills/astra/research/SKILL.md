---
name: research
description: Research or compare options by synthesizing and evaluating sources. Exclude quick factual lookups and runnable experiments.
---

# Research

Use evidence that can establish the class of claim being made. Do not promote
documentation into observed behavior, implementation into effectiveness,
association into causation, current evidence into historical availability, or a
recommendation into established fact.

## 1. Frame the decisive claims

Establish the question, intended use, and constraints that can change the answer,
such as version, date, jurisdiction, repository state, audience, source limits, or
comparison criteria. Reuse settled context; do not reopen it merely to make the
research process complete.

Identify the claims that could change the conclusion and distinguish their
evidence class:

- contract, definition, or published position;
- implementation mechanics;
- observed runtime behavior;
- empirical effectiveness or causality;
- historical availability at a cutoff;
- quantitative result or method; and
- comparative judgment or recommendation.

Evidence for one class does not establish a stronger one. If a simple factual
lookup settles the request, answer it directly instead of expanding this workflow.

## 2. Use the evidence method the claim requires

Prefer the source capable of establishing the claim: operative or authoritative
text for a contract or obligation, exact code for mechanics, applicable
observation or data for behavior, and appropriate empirical evidence for
effectiveness. Use secondary material to find primary evidence when useful, but
state the available source's actual evidentiary limit when the owner cannot be
inspected.

Load a specialist reference only when its trigger is present:

- Comparing options, causal/effectiveness claims, reliability, generalization, or
  a body of studies:
  [Comparison and empirical evidence](references/comparison-and-empirical.md).
- Quantities, benchmarks, or quantitative methods:
  [Quantitative evidence](references/quantitative.md).
- What was available, known, published, or effective at a cutoff:
  [Historical evidence](references/historical.md).
- Legal/policy meaning or non-public evidence:
  [Source boundaries](references/source-boundaries.md).
- Mapping a requirement, definition, method, or named behavior through a target
  artifact or repository, or researching why code exists:
  [Repository mapping](references/repository-mapping.md).

## 3. Test the conclusion

Separate observations from inference and state material premises. Resolve apparent
disagreement by scope, version, authority, population, method, or state before
calling it a true contradiction. Absence from a bounded search is not proof of
absence.

Seek counterevidence when it could materially change the conclusion. For
empirical, comparative, contested, or incentive-driven claims, use an independent
evidence path capable of exposing the likely error. Independence means different
underlying evidence or method relevant to that error, not a quota of URLs,
articles, or subagents.

Stop when the decisive claims are supported to the strength the answer requires
or their specific limits are established, material counterevidence has been
considered, and further credible search is unlikely to change the conclusion. A
time or source budget may stop research; it does not convert uncertainty into
support.

## 4. Deliver the supported result

Lead with the supported answer or requested recommendation. Include the decisive
tradeoffs, assumptions, conflicts, and evidence limits that change how the answer
should be used. A conditional recommendation, tie, or unknown is preferable to a
stronger conclusion the evidence does not support.

Check that decisive citations support the adjacent claim and apply to the relevant
version, date, population, repository state, or other governing condition. Do not
combine evidence from incompatible states into one apparently verified result.

Return inline findings unless a durable artifact was requested. A recommendation
does not itself authorize adoption or implementation.

Research evaluates existing evidence. When a decisive claim requires a new
observation, identify that missing observation; use
[prototype](../prototype/SKILL.md) only when an experiment is authorized.
[shape-work](../shape-work/SKILL.md) owns unsettled product meaning and
[codebase-design](../codebase-design/SKILL.md) owns unresolved architecture or
integration design.
