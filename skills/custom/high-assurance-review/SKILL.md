---
name: high-assurance-review
description: Explicit-only review of one immutable caller-selected candidate through two fresh core reviewers and coordinator-only finding admission, returning one terminal decision. Never selected automatically from release or risk facts.
---

# High-Assurance Review

**Admit -> Pin -> Review -> Converge -> Gate**

## 1. Admit

Load the `change-review` skill's `FINDING-CONTRACT.md` and the shared
[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md).
Accept only when the user explicitly invokes High Assurance Review for one
caller-bounded immutable candidate. Release status and supported-risk triggers
may shape coverage but are neither required nor sufficient for invocation.
Recommend `$audit-codebase` for an immutable
repository-baseline audit, then stop.

Require this invocation to be the `assurance-coordinator`, the root of its
review run. A core reviewer, specialist, or other nested review lane that
invokes this skill returns `incomplete` before Pin. For the coordinator, record
runtime agent type, requested and observed-or-unavailable model and reasoning,
and accepted-request or telemetry proof; a missing or mismatched binding returns `transport-invalid`
before Pin. The coordinator owns
dispatch, finding admission, convergence, and the terminal read-only decision;
it never mutates or substitutes for a reviewer.

Hold a read-only boundary through Gate. Leave repository, dependency, tracker,
PR, external, Repair, and successor state unchanged. If required evidence needs
mutation, return `incomplete` with the blocker and verified partial evidence.

Freeze the caller's Charter, commitment boundary, fixed point, candidate,
`Spec required: yes | no`, Source Trace, required proof, skips, supported-risk
facts, carried IDs, coordinator actor and task IDs, and mode.

Use one mode:

- `initial` is the default and judges the selected snapshot; or
- `remediation` is a fresh run for one caller-repaired candidate and applies
  the Finding Contract's remediation packet and coverage boundary.

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
configuration, and meaningful nearby conventions. Load
`change-review/SMELL-BASELINE.md` only when Standards are thin. Trace Spec
independently in this precedence:

1. caller-supplied source;
2. captured-commit material;
3. one matching repository source.

A missing, conflicting, unreadable, or unresolved required Spec makes coverage
`incomplete`. An absent optional Spec is skipped, never inferred.

Freeze one compact row per semantic change unit:

```text
change -> governing commitment -> actual behavior path
       -> applicable Finding Contract classes -> proof -> disposition
```

Assign each applicable Spec and Standards class to exactly one core lane. Reuse
exact-snapshot proof and run only missing, invalidated, or repository-required safe checks. Mark
inapplicable classes `N/A` with a reason; cover semantic branches and supported
interactions, not a blind Cartesian product. Any required source, class, proof
seam, overlap, or risk trigger left uncovered makes the review `incomplete`.

## 3. Review

Dispatch exactly two direct core reviewer lanes as fresh read-only collaboration
subagents using their exact semantic agent, model, and reasoning bindings:

1. `har-spec-reviewer` — Commitment Fidelity, Scope and Contracts, and
   Acceptance and Change Closure.
2. `har-standards-reviewer` — Semantic Correctness, Robustness and Operability,
   Code Quality and Design, Proof Discipline, and Stewardship.

Both lanes intentionally overlap on supported risk, failure and recovery paths,
Change Closure, and evidence completeness while retaining their primary axis
and classes.

Add at most one `har-specialist` when a frozen supported risk requires a distinct
security, migration, concurrency, model, data, or performance evidence lane the
two core lanes cannot responsibly cover. The specialist covers only its
assigned classes and risk; Risk never becomes a third axis.

Record each lane's semantic agent ID, runtime agent type, actor ID, task ID,
requested and observed-or-unavailable model and reasoning, accepted-request or telemetry
proof, fresh-context proof, and snapshot binding. Give each lane only the
immutable snapshot, factual sources, assigned coverage, read-only boundary,
and this return contract:

```text
status: complete | blocked
lane: har-spec-reviewer | har-standards-reviewer | har-specialist
axis: Spec | Standards
classes:
coverage:
finding candidates:
skipped checks:
blockers:
```

Withhold coordinator hypotheses, peer output, the partial ledger, and terminal
cues. Reviewers return finding candidates only; they do not spawn, admit
findings, decide the gate, or authorize Repair.

Verify each return against its dispatch binding and required fields. A
contaminated, mutating, out-of-lane, stale, or incomplete return receives no
credit. Permit at most one fresh unbiased replacement per invalid lane while
the snapshot and factual brief remain valid. An evidence blocker or second
invalid return closes that lane `incomplete`; do not create recursive rounds.

Define **valid reviewer quorum** as exactly two valid fresh core returns plus a
valid required specialist, if any. Without quorum, return `incomplete`; the
coordinator never substitutes for a reviewer.

## 4. Converge

Normalize valid lane finding candidates into one coordinator-owned ledger. Give
each item a stable ID, factual origin, axis, primary class, and one state:
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

- `incomplete` when required source, coverage, finding-candidate disposition,
  dispute, protocol, report, specialist, or drift state remains unresolved;
- `blocked` when a directly verified admitted finding blocks release;
- `pass with residual risk` when coverage is complete, no blocker exists, and
  decision-bearing residual risk remains for caller acceptance; or
- `pass` when coverage is complete, no blocker or decision-bearing residual
  risk remains, and drift is clear.

Return one caller-bound packet with mode, fixed point, snapshot, candidate,
sources, coordinator, core, and specialist requested and
observed-or-unavailable runtime bindings plus their proof, coverage by axis and
class, admitted findings, carried dispositions, closed finding-candidate
states, skipped checks, residual risk, drift, decision, and blockers. The decision
grants no Repair, Lock, or residual-risk acceptance authority; those remain
with the caller. End with:

```text
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires valid reviewer quorum; every applicable axis, class, and
risk trigger to close; every finding candidate and carried ID to be disposed;
drift to pass; and one internally consistent decision to return. Return control
to the caller and stop.
