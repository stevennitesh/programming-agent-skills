# Finding standards

Apply before admitting a review observation. A finding needs:

- An accepted requirement, repository rule, supported behavior, or demonstrated
  maintainability obligation relevant to the selected change.
- A concrete reachable scenario introduced, worsened, or left unsatisfied by that
  candidate, including a required omission.
- Direct evidence from the candidate, its relevant context, or faithful
  verification.
- A consequential failure or avoidable maintenance cost, not a style preference.
- A correction or proof request proportionate to that consequence.

An agent-written plan does not by itself make an added mechanism or gate binding.
Trace a disputed obligation to accepted behavior, repository policy, or a necessary
supported guarantee. Distinguish an unnecessary mechanism from an accepted
guarantee whose revision belongs to its owner.

A smell is a hypothesis. Check whether domain distinctions, independent lifetimes,
external contracts, migration needs, or other current requirements explain it.
Reject disproved claims, speculative hardening, unrelated cleanup, and preferences
for a different but equally valid design.

A maintainability finding need not cause a runtime failure, but it must demonstrate
a concrete cost such as caller burden, duplicated policy, change amplification,
or avoidable operational complexity.

Use one finding per independently actionable obligation and combine duplicate
symptoms when one correction addresses the same cause. Preserve stable finding IDs
when tracking remediation. Identify the reviewed location, trigger, evidence,
impact, and necessary correction or proof. Do not prescribe a larger redesign when
a smaller correction satisfies the obligation.

## Priority and blocking

Calibrate priority from demonstrated impact and reach:

- **P0:** urgent catastrophic production, security, privacy, or data failure.
- **P1:** major supported correctness, contract, or operational failure.
- **P2:** meaningful bounded failure or maintainability cost.
- **P3:** lower-impact actionable problem.

Priority estimates impact; it does not by itself determine whether the candidate
can pass a gate. A P2 can require correction when it violates binding acceptance,
while a nonblocking observation can remain visible at any priority.

Do not inflate severity because a pattern sounds dangerous. Optional suggestions
are not findings unless they satisfy the admission standard; include them only
when requested or materially useful and label them separately.

## Missing proof and gate decisions

Unavailable optional verification is a coverage limit, not automatically a defect.
Missing evidence needed to decide a governing obligation makes the review
incomplete. Omission of required proof can itself be a finding when the admission
conditions above hold. Distinguish both from a verified defect.

When a gate decision is requested, return:

- **blocked:** one or more verified findings require correction before the
  candidate can satisfy applicable behavior or policy;
- **incomplete:** required candidate identity, coverage, source, or evidence
  remains unresolved;
- **pass with residual risk:** required coverage is complete and no required
  correction remains, but a characterized material limitation still belongs to an
  owner's acceptance;
- **pass:** required coverage is complete, no required correction remains, and no
  decision-bearing uncertainty is unresolved.

A verified required correction can block the candidate even when unrelated
coverage remains incomplete; preserve that coverage limit. Do not use residual
risk to disguise missing required proof.

A gate judgment applies to the reviewed candidate. It does not authorize merge,
release, deployment, or acceptance of residual risk.

Distinguish required corrections from nonblocking findings and optional
suggestions. Identify any residual-risk decision and its owner unless acceptance
was already authorized.

For remediation, preserve finding identities and explain each disposition from
current evidence. A missing prior report limits claims about resolving that report
but does not prevent a clearly labeled fresh review of the selected candidate.
