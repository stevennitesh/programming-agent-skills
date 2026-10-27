# Finding standards

Use this standard for fresh findings and assessment of supplied feedback.
A finding must establish:

- An accepted requirement, repository rule, supported behavior, or demonstrated
  maintainability obligation relevant to the selected change.
- A concrete reachable problem the candidate introduces or worsens, or an accepted
  requirement of that change it fails to satisfy.
- Direct evidence of the trigger and consequential failure or maintenance cost.
- A correction or proof request proportionate to the consequence.

An unrelated pre-existing defect is outside ordinary change-review scope. An
unchanged line can still cause a regression activated by the candidate; explain
that connection. Missing required behavior is eligible even without a regression.

Tests and agent-written plans are evidence, not independent acceptance authority;
their agreement does not prove an assumption they share. Trace disputed
obligations to accepted intent, policy, or a necessary supported guarantee.
Preserve domain meaning and compatibility, and check contrary evidence such as
external contracts or migration needs before admitting a finding.

Reject speculative hardening, unrelated cleanup, style preferences, and equally
valid alternative designs. Maintainability findings need a concrete cost, such as
duplicated policy, caller burden, or change amplification. Combine duplicate
symptoms of one cause into one actionable finding. Identify its location, trigger,
evidence, impact, and needed correction or proof; recommend broader repair only
when demonstrated benefits justify its scope and cost.

## Priority and blocking

Calibrate priority from demonstrated impact and reach:

- **P0:** urgent catastrophic production, security, privacy, or data failure.
- **P1:** major supported correctness, contract, or operational failure.
- **P2:** meaningful bounded failure or maintainability cost.
- **P3:** lower-impact actionable problem.

Priority does not determine blocking: a P2 can violate binding acceptance, while
a nonblocking observation may remain at any priority. Low frequency or a different
supported caller does not automatically make a reachable security, data-loss,
compatibility, or concurrency failure a nit. Do not inflate speculative risks or
promote optional suggestions into findings.

## Missing proof and gate decisions

Unavailable optional verification is a coverage limit. Missing evidence needed to
judge a governing obligation makes the review incomplete. Omission of required
proof can itself be a finding when it meets the admission standard; distinguish
that obligation from a verified behavior defect.

When a gate decision is requested, return:

- **blocked:** one or more verified findings require correction before the
  candidate can satisfy applicable behavior or policy;
- **incomplete:** required candidate identity, coverage, source, or evidence
  remains unresolved;
- **needs owner decision:** required coverage is complete and no required
  correction remains, but a characterized material risk still requires its
  owner's acceptance;
- **pass:** required coverage is complete, no required correction or consequential
  decision remains, and any material residual risk has an authorized disposition.

Report blocking findings even when other coverage is incomplete, retaining both
facts. Name required corrections, nonblocking findings, and any risk decision and
its owner. Residual risk cannot substitute for missing required proof. A verdict
applies only to the reviewed candidate and grants no merge, release, deployment,
or risk-acceptance authority.
