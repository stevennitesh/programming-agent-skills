---
name: high-assurance-review
description: Thorough read-only review of one fixed code candidate through two fresh independent reviewers and one verified decision. Use only when the user explicitly requests high-assurance, heavy, or final review, commonly for an implemented ticket graph or before merging a PR. Exclude ordinary review, repository-baseline audits, repair, and mutation.
---

# High-Assurance Review

**Fix -> Ground -> Review twice -> Converge -> Gate**

Run as the top-level coordinator. Reviewers do not invoke High-Assurance
Review, delegate, repair, or decide the gate.

Keep the run read-only. The caller retains repair, merge, tracker, release,
residual-risk acceptance, and successor-candidate authority.

## 1. Fix

Accept one user-selected heavy review of one complete code candidate. Do not
activate from PR presence, candidate size, release status, novelty, or risk.
Recommend `$audit-codebase` and stop when the request concerns a repository or
subsystem baseline rather than a change.

Use the comparison point the user names. Otherwise resolve the repository
default-branch merge base. Pin the complete candidate before dispatch:

- for a branch or finished ticket graph, capture its fixed point, ordered
  commit inventory, head commit, tree, and selected diff bytes;
- for a connected PR, capture the exact base, head, and diff; or
- for selected live work, capture `HEAD`, staged and unstaged changes, status,
  and every in-scope untracked path and its bytes.

Return `incomplete` when the candidate is empty, partial, ambiguous, or cannot
be fixed without mutation. Review the pinned candidate, never a later version.
Bind surrounding callers, callees, types, configuration, tests, and proof to
the same repository state so reviewers can judge execution paths beyond the
diff.

## 2. Ground

Load the `change-review` skill, its `FINDING-CONTRACT.md`, repository
instructions, and `docs/agents/engineering-contract.md` when present. Gather
the accepted request, governing issue or specification, durable decisions,
and candidate-bound proof.

For a finished ticket graph, include the accepted parent plus every in-scope
ticket and its disposition. Account for each material commitment in the
integrated candidate or an explicit non-code outcome. Review the combined
behavior and cross-ticket interactions rather than replaying each ticket's
workflow.

For a pre-merge PR, use its accepted description and linked issue or
specification. Commit and tracker references help discover authority; they do
not create it. A missing or conflicting source that prevents accepted-behavior
judgment makes coverage `incomplete`. Skip an optional absent source rather
than inventing intent.

The accepted request is always required. Treat an issue or specification as
required when the caller requests conformance to it or repository and candidate
evidence make it governing; otherwise record why it is optional.

Resolve the accepted request and governing sources before dispatch; apply only
their accepted scope. Treat superseded behavior and historical procedural
material as context. Retain current repository instructions as governing
context and candidate-bound proof as evidence. Cover failure, recovery,
compatibility, or security behavior only when accepted requirements or the
candidate activate it.

When changed behavior affects a handoff across owners or stages, identify each
material handoff that can change accepted caller-visible behavior. Name its
producer, actual returned or persisted representation, lowest real
consuming caller, and terminal effect. Omit unchanged and
non-decision-bearing internals. An untraced material handoff makes coverage
`incomplete`.

Build one factual brief shared by both reviewers. Include the fixed candidate,
governing sources, affected handoffs, relevant repository context, existing
proof, and material evidence limits. Withhold coordinator hypotheses, peer
output, and terminal cues.

Coverage must account for:

- accepted commitments, scope, and observable behavior;
- real entry paths, callers, owners, and cross-ticket or dependency
  interactions;
- replaced behavior and displaced code, configuration, tests, or docs;
- applicable failure, recovery, trust, migration, concurrency, or
  compatibility paths; and
- proof strong enough for each decision-bearing claim.

An uncovered material obligation or interaction makes the review `incomplete`.

## 3. Review twice

Identify the relevant implementation and integration authors before dispatch.
Dispatch exactly two fresh, read-only reviewers against the same pinned
candidate and factual brief. Each must use a fresh task or context, be distinct
from the other reviewer, and be separate from every identified author. If
freshness or required separation cannot be established, return `incomplete`.
Each applies Change Review directly and inspects the whole candidate without
spawning another reviewer.

Give the lanes different primary emphasis without creating blind spots:

1. **Behavior and integration** checks accepted meaning, graph or PR scope,
   caller-visible contracts, cross-ticket interactions, acceptance, and
   complete replacement or removal.
2. **Engineering quality** checks correctness, reachable failure behavior,
   causal ownership, data shape, simplicity, maintainability, and proof
   proportional to the claim.

When accepted behavior changes how an intermediate result requests additional
work or how a later invocation consumes an earlier result, both reviewers
independently trace a supported real-caller journey through the changed
continuation to its terminal effect. Cover each materially
distinct accepted request profile or terminal outcome, including a declared
exhaustion or capacity bound when it changes that effect. Both lanes may inspect
the same candidate-bound artifact; do not rerun the workflow for symmetry.

For each affected handoff, each reviewer challenges whether the proof could
distinguish a consumer that uses the actual result from one that ignores it,
uses stale identity, or ends the transition early, as applicable. Give the
handoff coverage only when the lowest ordinary consuming caller receives the
actual returned or persisted representation and exposes the expected terminal
effect. Direct-helper or producer-only proof does not cover the handoff unless
accepted behavior exposes that helper directly.

Both trace actual execution paths, distinguish reachable failures from
hypotheticals, inspect the canonical owner, challenge unnecessary branches or
dual paths, and prefer real-artifact evidence over summaries or proxies.

Each reviewer returns its identity and independence basis, coverage, material
evidence limits or blockers, and finding candidates under the Finding Contract.
An empty review is valid.

Add at most one specialist only when the user explicitly names one bounded
specialist question. If indispensable specialist judgment is unavailable,
return `incomplete`.

## 4. Converge

Disposition every reviewer finding candidate under the Finding Contract.
Verify every candidate that could be admitted against the pinned sources,
candidate, callers, and contrary evidence. Reviewer agreement raises review
priority but never establishes truth.

Apply the Finding Contract's Reach and Impact gates through a supported real
caller before admitting a behavioral or contract finding or closing coverage
as complete. A direct-helper invocation is diagnostic unless accepted behavior
exposes that helper directly. Return `incomplete` when required reach remains
uncertain.

Deduplicate overlaps. Resolve disagreements from evidence, not votes. Reject
speculation, optional hardening, unrelated cleanup, and preference-only
redesign. Give admitted findings stable IDs when they may enter remediation.
Keep a short rationale for any rejected or disputed material claim that could
change the gate. An unresolved material dispute makes the review `incomplete`.

Run only safe checks needed to settle a material finding, graph-completion
claim, repository requirement, or decision-bearing uncertainty. Reuse valid
candidate-bound proof. Missing required proof may be a finding when the
Finding Contract supports it; unavailable optional proof is a stated limit.

## 5. Gate

Recheck mutable candidate identity using the original resolution. If it moved,
return `incomplete`; do not recapture it inside the run.

Return exactly one decision:

- `blocked` when an admitted `P0` or `P1`, or binding caller or repository
  acceptance policy, rejects the candidate;
- `incomplete` when required source, coverage, evidence, dispute, reviewer, or
  candidate identity remains unresolved and no admitted blocker already
  decides the gate;
- `pass with residual risk` when coverage is complete, no blocker exists, and
  a verified material uncertainty remains for caller acceptance; or
- `pass` when coverage is complete, no blocker or decision-bearing uncertainty
  remains, and drift is clear.

Return the candidate identity, coverage, admitted findings in impact order,
material rejected or disputed claims, checks and evidence limits, residual
risk, reviewer identities and independence basis, applicable drift result, and
decision. Nonblocking findings remain visible but do not decide the gate. A
blocker takes precedence over unrelated incomplete coverage; preserve that
coverage limit in the result.

For a repaired candidate, start a fresh run. Carry prior admitted finding IDs,
inspect the repair delta and affected callers, and recheck remaining
acceptance. If the repair broadens the change materially, review the full new
candidate rather than treating it as bounded remediation.

Completion requires both fresh reviewers to inspect the same fixed candidate;
every applicable commitment and interaction to be covered; every material
finding candidate to be verified or resolved; every reviewer candidate to be
dispositioned; drift to be clear; and one
internally consistent decision to return. Stop without repairing or merging.
