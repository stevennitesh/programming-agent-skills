---
name: high-assurance-review
description: Explicit-only review of one immutable caller-selected candidate through two fresh core reviewers and coordinator-only finding admission, returning one terminal decision. Never selected automatically from release or risk facts.
---

# High-Assurance Review

**Admit -> Pin -> Review -> Converge -> Gate**

## 1. Admit

Load the `change-review` skill's `FINDING-CONTRACT.md`.
Accept only when the user explicitly names High Assurance Review or approves
one exact caller-owned invocation packet for one immutable candidate. That
admission authorizes the two core lanes only. Release status, supported risk,
security or production adjacency, and uncertainty are neither required nor
sufficient for invocation.
Recommend `$audit-codebase` for an immutable
repository-baseline audit, then stop.

Require this invocation to be the top-level root of its review run. That root
is the semantic assurance coordinator. A core reviewer, specialist, or
other nested review lane that invokes this skill returns `incomplete` before
Pin. The coordinator owns
dispatch, finding admission, convergence, and the terminal read-only decision;
it never mutates or substitutes for a reviewer.

Hold a read-only boundary through Gate. Leave repository, dependency, tracker,
PR, external, Repair, and successor state unchanged. If required evidence needs
mutation, return `incomplete` with the blocker and verified partial evidence.

Freeze the caller's accepted request and commitments, commitment boundary, fixed point, candidate,
`Spec required: yes | no`, Source Trace, required proof, skips, supported-risk
facts, carried IDs, coordinator actor and task IDs, and mode.

Use one mode:

- `initial` is the default and judges the selected snapshot; or
- `remediation` is a fresh run for one caller-repaired candidate and inspects
  the carried outcomes, exact repair delta, affected seams, and remaining
  acceptance without reopening untouched scope.

Return `incomplete` before Pin for a missing, contradictory, or ambiguous
decision-bearing field.

## 2. Pin

Resolve the supplied fixed point once; otherwise resolve the repository
default-branch merge base. Capture one nonempty immutable candidate:

- exact commit, tree, and selected diff bytes for a Git-addressed candidate;
- exact base, head, and diff content for a connected PR; or
- `HEAD`, index tree, staged diff, unstaged diff, normalized status, and every
  in-scope untracked path and its bytes for an explicitly selected live candidate.

Record the fixed point, candidate kind, exact identities, selected scope,
captured content, commands, and ref resolutions. Reviewers inspect only captured
bytes. Return `incomplete` when the fixed point or candidate is unavailable,
ambiguous, empty, partial, or mismatched. Do not infer, switch candidates,
mutate to obtain one, or silently narrow scope.

Trace Standards from repository instructions,
`docs/agents/engineering-contract.md`, maintained
configuration, and meaningful nearby conventions. Trace Spec independently in
this precedence:

1. caller-supplied source;
2. captured-commit material;
3. one matching repository source.

A missing, conflicting, unreadable, or unresolved required Spec makes coverage
`incomplete`. An absent optional Spec is skipped, never inferred.

Assign accepted-behavior judgment to the Spec lane and implementation-quality
judgment to the Standards lane. Reuse exact-snapshot proof and run only missing,
invalidated, or repository-required safe checks. Cover semantic branches and
supported interactions, not a blind Cartesian product. Any required source,
proof seam, overlap, or risk trigger left uncovered makes the review
`incomplete`.

## 3. Review

Dispatch exactly two direct core reviewer lanes as fresh read-only collaboration
subagents:

1. `har-spec-reviewer` — accepted meaning, scope, contracts, acceptance, and
   complete replacement or removal.
2. `har-standards-reviewer` — correctness, failure behavior, ownership,
   simplicity, maintainability, and proof proportional to the claim.

Both lanes intentionally overlap on supported risk, failure and recovery paths,
complete replacement or removal, and evidence completeness while retaining
their primary axis.

Add at most one `har-specialist` only when the user or approved invocation
packet explicitly names one bounded specialist objective and its coverage.
Security and production/SRE specialist coverage require those objectives to
be explicit. Supported risk alone never selects a specialist. Without explicit
specialist authority, the two core lanes cover the admitted general scope or
return `incomplete` when required specialist evidence cannot be obtained. The
specialist covers only its assigned objective; risk never becomes a third axis.

Record each lane's actor and task IDs, fresh-context and separation evidence,
assigned objective, and snapshot binding. Give each lane only the immutable
snapshot, factual sources, assigned coverage, read-only boundary, and this
return contract:

```text
status: complete | blocked
lane: har-spec-reviewer | har-standards-reviewer | har-specialist
axis: Spec | Standards
coverage:
finding candidates:
skipped checks:
blockers:
```

Withhold coordinator hypotheses, peer output, the partial ledger, and terminal
cues. Reviewers return finding candidates only; they do not spawn, admit
findings, decide the gate, or authorize Repair.

Verify each return against its lane, snapshot, and required fields. A
contaminated, mutating, out-of-lane, stale, or incomplete return receives no
credit. Permit at most one fresh unbiased replacement per invalid lane while
the snapshot and factual brief remain valid. An evidence blocker or second
invalid return closes that lane `incomplete`; do not create recursive rounds.

Define **valid reviewer quorum** as exactly two valid fresh core returns plus a
valid required specialist, if any. Without quorum, return `incomplete`; the
coordinator never substitutes for a reviewer.

## 4. Converge

Normalize valid lane finding candidates into one coordinator-owned ledger. Give
each item a stable ID, factual origin, axis, and one state:
`candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Preserve
carried IDs through remediation.

The coordinator admits or rejects every finding candidate against the immutable
snapshot and Finding Contract. Required unavailable evidence makes coverage
`incomplete`, not a finding.

Resolve duplicates and disagreements from anchors, supported scenarios,
behavior paths, direct evidence, and contrary evidence. Reviewer count,
agreement, majority, and debate do not establish truth. An unresolved material
dispute is `incomplete`. Close every finding candidate and carried ID before
Gate.

## 5. Gate

Re-read and compare every cell of the pinned candidate identity using its
recorded command and ref resolution. Candidate drift returns `incomplete` with
verified partial evidence. Do not recapture; symbolic baseline movement does
not replace the pinned fixed point.

Derive exactly one decision after the reviewer quorum closes:

- `blocked` when a directly verified admitted finding blocks candidate
  acceptance under the governing caller or repository policy;
- `incomplete` when required source, coverage, finding-candidate disposition,
  dispute, protocol, report, specialist, or drift state remains unresolved and
  no admitted blocker already establishes `blocked`;
- `pass with residual risk` when coverage is complete, no blocker exists, and
  decision-bearing residual risk remains for caller acceptance; or
- `pass` when coverage is complete, no blocker or decision-bearing residual
  risk remains, and drift is clear.

A directly verified admitted blocker takes precedence over unrelated
incomplete coverage; preserve that unresolved coverage in the Return.

Return one caller-bound packet with mode, fixed point, snapshot, candidate,
sources, core and specialist fresh-context evidence, coverage by axis, admitted
findings, carried dispositions, closed finding-candidate states, skipped checks,
residual risk, drift, decision, and blockers. The decision
grants no Repair, candidate acceptance or closeout, or residual-risk acceptance
authority; those remain with the caller. End with:

```text
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires valid reviewer quorum; every applicable axis and risk
trigger to close; every finding candidate and carried ID to be disposed;
drift to pass; and one internally consistent decision to return. Return control
to the caller and stop.
