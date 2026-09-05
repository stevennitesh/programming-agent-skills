# Finding standards

Apply before admitting a review observation. A finding needs:

- An accepted requirement, repository rule, supported behavior, or demonstrated
  maintainability obligation relevant to the change.
- A concrete reachable scenario introduced, worsened, or left unsatisfied by the
  selected change, including a required omission.
- Direct evidence from the candidate, its relevant context, or faithful verification.
- A consequential failure or avoidable maintenance cost, not a style preference.
- A correction or proof request proportionate to that consequence.

A smell is a hypothesis. Check whether domain distinctions, independent lifetimes,
external contracts, or migration needs explain it. Reject disproved claims,
speculative hardening, and unrelated cleanup. An unfamiliar design is not faulty
merely because another is possible. A material design issue need not cause a
runtime failure, but must demonstrate caller burden, duplicated policy, change
amplification, or another concrete cost.

Use one finding per independently actionable obligation; combine duplicate
symptoms when one correction addresses the same cause. Give stable IDs when
tracking remediation. Identify the exact reviewed location, trigger, evidence,
impact, and necessary correction or check. Avoid prescribing a full redesign
when a smaller correction would meet the obligation.

Calibrate priority from demonstrated impact and reach:

- **P0:** urgent catastrophic production, security, privacy, or data failure.
- **P1:** major supported correctness, contract, or operational failure.
- **P2:** meaningful bounded failure or maintainability cost.
- **P3:** lower-impact actionable problem.

Do not inflate severity because a pattern sounds dangerous. Optional suggestions
are not blockers; include them only when requested or materially useful and label
them separately from admitted findings.

## Missing proof and gate decisions

Unavailable optional verification is a stated limit, not automatically a defect.
Missing evidence needed to decide a governing obligation makes that coverage
incomplete. Omission of required proof can itself be a finding when the admission
conditions above hold. Distinguish both from a verified defect.

When a gate decision is requested, return:

- **blocked:** a verified P0/P1 or binding acceptance policy rejects the candidate;
- **incomplete:** required identity, coverage, source, or evidence remains unresolved;
- **pass with residual risk:** required coverage is complete and no blocker exists,
  but a characterized material limitation remains for the owner's acceptance;
- **pass:** required coverage is complete and no blocker or decision-bearing
  uncertainty remains.

A verified blocker can decide the gate despite unrelated incomplete coverage;
preserve that coverage limit. Do not use residual risk to disguise missing required
proof. Nonblocking findings remain visible even when policy permits a pass. A gate
judgment is about the reviewed candidate, not permission to merge or accept risk.

For remediation, preserve finding identities and explain each disposition from
current evidence. A missing prior report limits claims of having resolved that
report, but does not prevent a clearly labeled fresh review of the selected change.
