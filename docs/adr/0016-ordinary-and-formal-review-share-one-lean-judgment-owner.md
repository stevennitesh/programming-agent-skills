# Ordinary And Formal Review Share One Lean Judgment Owner

**Status**: accepted

## Context

ADR-0015 correctly made independent review condition-triggered, but the runtime
still made actor IDs, model and reasoning bindings, transport states, coverage
ledgers, and formal report fields part of every Change Review. That machinery
could block an otherwise valid review without improving judgment of the code.
Direct review and formal delivery need the same evidence discipline but not the
same orchestration or Return surface.

## Decision

Keep one Change Review judgment owner. Its ordinary path identifies the selected
code change, traces accepted behavior and engineering quality through real
callers, verifies concrete finding candidates, checks mutable-candidate drift,
and returns findings or no findings.

Load formal-review procedure only when the caller supplies `Formal review: yes`.
Formal review requires one fixed candidate and adds required-Spec handling,
reviewer independence when claimed, bounded remediation review, and a terminal
decision. Implement and Parallel Implement retain ADR-0015's activation
triggers and own reviewer dispatch, repair, proof reruns, and successor
candidates. High Assurance Review remains explicit-only and owns its fresh
multi-lane coordination.

Fresh reviewer separation remains required when independence is claimed.
`ordinary-reviewer`, `integration-reviewer`, and High Assurance lane names are
semantic roles, not model or reasoning assignments. Runtime transport does not
establish code-review correctness and cannot invalidate an otherwise correctly
separated review.

Findings require an accepted requirement or repository rule, a reachable
scenario, direct candidate evidence, concrete impact, and a proportionate
correction. Review grants no mutation, repair, release, acceptance, or successor
authority.

This decision supersedes ADR-0015 and retains its condition-triggered activation
policy. ADR-0014 remains accepted.

## Consequences

- Ordinary review carries no formal-delivery packet or status taxonomy.
- Formal review remains fixed-candidate and read-only.
- Reviewer dispatchers prove fresh separation without model receipts.
- Worker runtime profiles remain available for implementation delegation; they
  no longer define reviewer correctness.
- Historical review evaluations and superseded ADRs remain unchanged evidence.
