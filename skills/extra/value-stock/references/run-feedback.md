# Valuation Run Feedback

Use this branch only under the exact loading condition in `SKILL.md`. It
evaluates one valuation run; it is not another valuation gate, a user
satisfaction survey, or authority to revise the skill.

## Bind The Run

Run after the canonical valuation or blocked attempt and every applicable review
reach terminal state. Bind the packet to the exact security, as-of date,
information cutoff, depth, final Model Lock version and calculation artifact,
valuation output, review evidence, tools, and authority. If no Lock was
possible, bind it to the identified blocked attempt and its evidence.

The packet records canonical state; it does not change method disposition, the
Lock, gate or review validity, valuation status, or the report. If the root
admits a feedback finding that changes load-bearing valuation content, return to
the main skill, create a new Lock version, recompute its dependent outputs,
rerun required gates and review, recompose the canonical valuation under the
selected return contract, and regenerate feedback against the new final version.
Do not combine packets across versions or evaluate feedback about feedback.

## Classify Findings

Use one classification per finding:

- `execution miss` - an exact current contract observably required the behavior,
  but the run omitted or observably violated it;
- `contract gap candidate` - conforming execution could still miss the behavior
  because its trigger, action, evidence, safe failure, owner, or Return is absent
  or materially ambiguous;
- `evidence limit` - owning evidence is unavailable, conflicting, or
  insufficient and controls precision or status; or
- `forecast judgment` - supported economic assumptions differ and belong in
  causal cases or sensitivities.

An existing-instruction miss is not a contract gap. Evidence limits and forecast
judgments are not errors. A reviewer may find an issue, but only the root may
verify, classify, admit, and assign its valuation or status effect.

## Return The Packet

Omit empty conditional fields.

```text
feedback status: complete | partial | blocked
trigger and requested use:
run:
  security, as-of date, cutoff, and depth:
  final Model Lock version or blocked-attempt identity:
  applicable company and method branches with their triggers:
methods:
  - method, target claim, disposition, and reason:
outcome:
  final status and supported value:
  baseline or pre-review value:  # only when a material correction changed it
verified findings:
  - issue:
    classification:
    valuation or status effect:
    finder and evidence pointer:
    current contract owner and expected behavior:
    disposition: corrected | bounded | rejected | unresolved
    invalidated Lock, output, or review work:  # only when applicable
remaining load-bearing unknowns:
  - unknown, owning evidence or bound, affected output, and status effect:
summary:
  material errors caught before final output (count):
  material errors not caught by applicable gates (count):
  Model Lock versions (count and admitted reasons):
  review packets invalidated (count):
  value change from mechanical corrections:
  value change from economic judgment:
  unresolved items controlling partial or blocked (count):
improvement and fixture assessments:  # only for improvement or fixture use
  - source: finding | standalone request
    source finding or requested behavior:
    decision: nominate | reuse existing | no nomination
    kind: existing-contract regression | existing-contract coverage |
          contract-gap evaluation
    reason:
    entry predicate:
    frozen minimal stable public/shareable input and evidence pointers,
      or safe synthetic recipe:
    expected observable result and safe failure:
    materially different entry-positive family and transfer basis:
    closest wrong-condition:
    existing fixture or duplicate-search boundary:
    reuse scope, invalidation boundary, and evidence limit:
    advisory candidate wording and deliberate non-change:
    proof state and next owner:
```

Set `feedback status` to `complete` when every explicitly requested feedback use
is grounded in the bound run and every reported finding is verified, classified,
and dispositioned, and every explicitly requested fixture assessment has a
supported decision; `partial` when a useful packet is grounded but one requested
component, finding, or assessment remains unverifiable; and `blocked` when the
run or blocked attempt cannot be bound well enough to support any requested
feedback output. Feedback status is independent of valuation status.

Derive summary counts and value bridges from the method, Lock, review, and
finding records; do not create a second source of truth. Count only root-verified
material errors, and count each underlying error once per run regardless of
finders, affected outputs, findings, or Lock versions. A caught error was
detected before an affected value was used in final output; a not-caught error
survived its applicable gate and was verified later against the same Lock. Those
counts are independent and may overlap. Compare value changes only on the same
value definition and identify mechanical correction separately from economic
judgment.

## Nominate, Do Not Self-Edit

Assess fixture eligibility only when the requested feedback use includes
improving `$value-stock` or a reusable valuation fixture. For each root-verified
material `execution miss` or `contract gap candidate`, return one decision for
the distinct behavioral failure family; return one decision for every explicit
standalone fixture request even when no finding exists. Nominate only when the
behavior has an observable entry predicate, expected result and safe failure;
transfers to a materially different entry-positive family; has a closest wrong
condition; can be represented by stable, public or shareable frozen inputs and
evidence, or a safe synthetic recipe; and is not already covered by the same
fixture family. Otherwise return `reuse existing` or `no nomination` with the
reason. Evidence limits, forecast judgments, immaterial accidents, and
ticker-only or sector-only variation do not qualify.

Label an existing-instruction miss an `existing-contract regression` candidate.
Label a gap a `contract-gap evaluation` candidate until the authoring owner
admits the behavior; do not call it a regression fixture before then. A correct
`reuse existing` or `no nomination` decision completes that assessment.
Deduplicate by entry predicate, expected behavior, and invalidation boundary,
not by finder, output, ticker, or company.

One run may establish an observation and transfer hypothesis, not prevalence or
behavioral efficacy. A materially different fixture changes the load-bearing
method, claim, issuer state, or accounting mechanism, not merely the ticker or
sector label. A wrong-condition fixture must show that the proposed behavior
does not add reference loading, research, calculation, review, user-visible
filler, or weaker status beyond a cheap predicate check.

The skill-authoring owner decides whether to admit a reusable lesson or fixture.
Any claim that exact wording changes invocation, judgment, action, context
loading, Return, or completion requires the current behavioral evaluation
contract, including frozen controls and candidates, entry-positive sampling,
and wrong-condition checks. This packet is input to that work, not proof of it.

Do not edit this skill, its references, tests, evaluation corpus, installation,
or any other canonical artifact. Do not invoke authoring, evaluation,
installation, synchronization, or delivery without separate caller authority.
Return the packet and its next-owner handoff.
