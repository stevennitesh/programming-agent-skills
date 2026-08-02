# Review Agent Binding Behavioral Evaluation

Date: 2026-08-02

Registration: defect-correction

Decision: accept

## Scope

Verify that standalone Implement and Parallel Implement create formal-review
tasks with explicit model and reasoning bindings, Change Review remains a
non-delegating leaf, and High Assurance alone creates its two core reviewer
tasks. Exercise missing, mismatched, inherited, and unproved bindings at the
formal-review boundary.

## Frozen control

Repository `HEAD`: `c0d45be1de53edb21ce27737552df83c14d5897d`.

- Implement: `5f6fa4bbbd36ffd93e079cf67fb81a4a696ad784`
- Change Review: `84c0213aa989fc53c63d0fc2c499788012758d37`
- High Assurance Review: `b6a3d59eafc11e1d182488619573dc47afd8eb76`
- Parallel task lanes: `8cfb3af4491829ab081aff07e2460bde6f146c1f`

Five fresh-context read-only evaluators traced ordinary Implement, high-risk
Implement, standalone Change Review, direct High Assurance, and Parallel
Implement. The control left model and reasoning undefined for review tasks
created outside Parallel Implement. Change Review correctly spawned no task.

## Final candidate

- Implement: `0b76cc8d63e37c573fd5193e9ce86adf50bab9ed`
- Change Review: `1506d5fd6e5d29f4e5f5f10179ec28a6237fe7a9`
- Review bindings: `12bcb97bffb8760e62efec36475034921f8c55ca`
- High Assurance Review: `69449a06afea0c1ebd89840d3bc7cf591c6e4191`
- Parallel task lanes: `d23dee781c2742af10080ff10151e069453daeda`
- Run-ledger contract: `38f0baa1e86ad5eccaa47c251fcafd2e99f4ccd9`
- Run-ledger helper: `afe0a89c68c9a57e0c110b78018a969693edcc5f`

Fresh-context candidate and adversarial waves challenged the same practical
paths. They found and drove repairs for inconsistent transport status,
coordinator and core provenance gaps, the ledger's stale single-table loader,
and assertion-only core receipts. The terminal evaluator replayed the repaired
negative controls and found no remaining defect.

## Required behavior

| Case | Expected | Result |
| --- | --- | --- |
| Ordinary Implement | `ordinary-reviewer`, Sol High, fresh read-only task | pass |
| High-risk Implement | Sol High coordinator; two Sol Extra High core tasks | pass |
| Formal Change Review | exact ordinary binding; no delegation | pass |
| Standalone Change Review | current runtime provenance; no spawned review | pass |
| Parallel formal review | shared review bindings; worker bindings unchanged | pass |
| Binding mismatch | `transport-invalid`; no review credit | pass |
| Nested reviewer invocation | stop without recursive review | pass |

## Practical negative controls

The final run-ledger candidate rejected missing task receipts, arbitrary
environment/provider pairs, wrong requested effort, and unavailable telemetry
that still carried a resolved value. A valid matched two-core receipt passed.
The ledger trusts the root-recorded accepted task receipt; cryptographic
provider attestation is outside this contract.

## Proof

- Affected suites: `108 passed`.
- Skill-pack validation: passed.
- Whitespace and diff checks: passed.

The evaluation was read-only apart from the authorized canonical and proof
changes. No evaluator mutated repository state.
