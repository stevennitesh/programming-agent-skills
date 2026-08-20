# Formal Review

Load this reference only when the caller declares `Formal review: yes` for one
fixed implementation candidate. Ordinary direct review does not load it.

## Admit

Require the accepted request and commitments, fixed point, exact candidate,
required proof and material skips, `Spec required: yes | no`, and
`Mode: initial | remediation`. If independence is claimed, require evidence
that the reviewer was dispatched in a fresh task or context and is distinct
from every implementation and integration author. The caller owns reviewer
dispatch and candidate selection; model choice and runtime transport are not
review evidence.

A required specification that is missing, unreadable, conflicting, or
unresolved makes the review `incomplete`. When it is optional and absent, skip
that source and do not reconstruct intent from the candidate.

Give every admitted formal finding a stable ID. `Remediation` requires the
prior formal Return and candidate identity, fixed successor identity, exact
repair delta, all carried IDs, and remaining acceptance. A partial remediation
packet is `incomplete`; do not reinterpret it as an initial review. Inspect the
carried outcomes, affected callers and dependencies, and acceptance exercised
there. Dispose each carried ID as resolved, still admitted, disproved, or
incomplete without reopening untouched scope for general cleanup.

## Decide

After the main skill's final identity check, return exactly one decision:

- `blocked` when an admitted `P0` or `P1`, or binding repository policy, rejects
  the candidate;
- `incomplete` when required source, evidence, finding disposition, or candidate
  identity remains unresolved and no admitted blocker already decides the gate;
- `pass with residual risk` when no blocker remains but a verified material
  uncertainty still needs caller acceptance; or
- `pass` when no blocker or decision-bearing uncertainty remains.

A directly verified blocker takes precedence over unrelated incomplete
coverage; preserve the unresolved coverage as a material limit.

## Return

Return the fixed point and candidate identity, mode, independence evidence when
required, sources used or skipped, behavior covered, material checks and skips,
admitted findings, carried dispositions when applicable, residual risk, drift,
and decision. The report grants no repair, acceptance, mutation, release, or
successor authority. Return control to the caller and stop.
