# EP-BORDER-02

- Status: `complete`
- Operation: Audit
- Disposition: `needs-more-evidence`

## Decision

The supplied record supports `needs-more-evidence`. The registered control
defect appeared in all five fresh runs (`B02-F1`), so the defect-correction
comparison is admitted. The candidate corrected the defect in three runs but
reproduced it in two (`B02-F2`). This fails the fixed acceptance requirement
of correction in every matched run, and the rule explicitly sends disagreeing
outcomes without a critical regression to more evidence (`B02-F3`).

Neither a regression disposition nor a protocol explanation is supported:
no new critical or protected-behavior regression appeared (`B02-F4`), and
both failing candidate runs followed protocol (`B02-F5`). The five outcomes
therefore show unresolved contribution variance rather than an admissible
acceptance result or an observed critical regression.

## Coverage and limits

The affected surface is the supplied `EP-BORDER-02` evidence record and its
fixed decision rule. The runtime, fixture, repository, installation, Git, and
external state are preserved. Numeric minimum, maximum, and spread operations
are not applicable because this case supplies categorical run outcomes rather
than numeric observations.

The evidence is sufficient for the terminal recorded disposition
`needs-more-evidence`, but insufficient for `accept`: two of five matched runs
miss the required correction. This judgment is limited to the supplied task,
five matched runs, and fixed execution configuration. It does not establish
behavior under other tasks, models, hosts, configurations, wrong-condition
cohorts, or real-world prevalence.
