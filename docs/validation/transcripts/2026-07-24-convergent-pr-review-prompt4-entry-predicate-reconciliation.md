# Convergent PR Review Prompt 4 Entry-Predicate Reconciliation

- Authorized unit: bounded Prompt 4 reconciliation only
- Fixed Git `HEAD`: `f3be70c31dd8f2ae9f12a75248065ef313790bda`
- Decision: `accepted`
- Pruning, promotion, installation, canonical edits, test edits, and Git
  delivery: not performed

## Protocol

H1-03 and H1-05 were preregistered independently under the current
`writing-great-skills/BEHAVIOR-EVALS.md` entry-predicate contract. Each used a
separate worker-visible fixture, root-only hypothesis/rubric fixture, five
entry-positive M0 controls, and separate wrong-condition M0/H1 pairs.

Both worker fixtures passed `python -m scripts.campaign_artifacts
lint-fixture`. Every sampled case had resolved M0 and H1 JSON envelopes.
`compare-payloads` passed for all 17 case pairs after removing only
`/runtime`; all source, authority, isolation, and fixture-fidelity checks
passed. Exact runtime packages were the only arm delta. Candidate language,
rubrics, conclusions, and prior outputs remained root-only.

The first M0 control in each independent unit was inspected before the
remaining controls. Every evaluator used `fork_turns="none"` and received only
one exact runtime plus one resolved factual envelope. Exact service model,
reasoning effort, temperature, and seed were unavailable.

## Results

H1-03 applicability is `situational` from independent method evidence. Its M0
controls showed the registered deficit in `0/5`; no entry-positive H1 wave ran.
Two wrong-condition pairs passed. Decision:
`reject-no-control-deficit`.

H1-05 applicability is `situational` from independent method evidence and the
observed original Q03-03 behavior. Its M0 controls showed the registered
deficit in `3/5`, below the frozen `4/5` release gate; no entry-positive H1
wave ran. Five wrong-condition pairs covered contaminated briefs, consumed
recovery, broad search, drift, and a new invocation. H1 false-fired on drift
by authorizing field completion after the unchanged-snapshot predicate failed.
Decision: `reject-regression`.

Fixture frequencies were not used to infer prevalence. Conditional efficacy,
applicability, and permanent runtime load were judged separately.

## V1

Preserved H1-01, H1-02, and H1-04 decisions remain unchanged. No H1 unit
survives. V1 remains exact M0 at
`6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280`.
No reconciled package copy was needed.

The prior pruning and Prompt 5 chronology remains historical and unchanged.
Because V1 identity did not change, neither affected pruning nor Prompt 5 is
required.

```text
Authorized unit completed: Deploy Prompt 4 entry-predicate reconciliation
Decision: accepted
Campaign shape: hypothesis-candidate
Runtime identities: M0=V1=package-tree-sha256:6c419036d5cb8000d47666f2e02d414330c2369933a75654bac786bd8cff7280; H1=package-tree-sha256:379474917dc540ef9704a74628af11e123db11fc9e800a94b797278c1ab05c82 (H1-03 reject-no-control-deficit; H1-05 reject-regression)
Artifacts changed: reconciliation-entry-predicate/**; campaign manifest/results/candidate/synthesis reconciliation state; this transcript
Evidence used or reused: exact frozen M0/H1; preserved 25/25 M0 viability and H1-01/02/04 decisions; 10 fresh entry-positive M0 controls; 14 fresh wrong-condition M0/H1 samples; exact envelope lint/comparison/hash evidence
Residual gaps: exact service model/reasoning/temperature/seed unavailable; conditional fixture transfer only; applicability remains situational and independently sourced
Recommended next unit: none
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: both reevaluated H1 units were rejected and reconciled V1 remains exact M0, so no affected pruning or Prompt 5 rerun is required
```
