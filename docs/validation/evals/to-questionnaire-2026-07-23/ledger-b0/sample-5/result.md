## Omission

Proceed: yes.
Write: no.

Coverage:
- Named throughput: covered by “What sustained throughput must the system support for a GA go/no-go?”
- SLO feasibility: uncovered.
- Rollback: covered by “What rollback condition should trigger reversing the GA release?”

Required question before Save:
- “Based on the current evidence, is the target SLO feasible for GA?”

Conflict:
- “Finalize” conflicts with the coverage gate. A known needed-back item cannot be omitted, so the draft must not be written until the SLO-feasibility question is added.

## Orphan

Proceed: yes.
Write: no.

Coverage:
- Named throughput: covered by “What sustained throughput must the system support for a GA go/no-go?”
- Rollback: covered by “What rollback condition should trigger reversing the GA release?”
- Dashboard color: no ledger item; remove the question.

Required questions:
- “What sustained throughput must the system support for a GA go/no-go?”
- “What rollback condition should trigger reversing the GA release?”

Conflict:
- The dashboard-color question is unrelated to the locked needed-back ledger. The draft must not be written until that out-of-scope orphan is removed.

## Catch-all

Proceed: yes.
Write: no.

Coverage:
- Named throughput: explicitly covered.
- Rollback: explicitly covered.
- Top production risk: uncovered; “Anything else?” does not cover a known ledger item.

Required question before Save:
- “What is the top production risk that should affect the GA go/no-go?”

Conflict:
- The generic catch-all cannot substitute for the known production-risk question. Keep “Anything else?” only as the final catch-all and add the explicit risk question before writing.

## Hard budget

Proceed: yes.
Write: no.

Coverage:
- Named throughput: required, not yet covered.
- Bottleneck: required, not yet covered.
- SLO feasibility: required, not yet covered.
- Rollback metric: required, not yet covered.
- Rollback threshold: required, not yet covered.
- Evaluation window: required, not yet covered.
- On-call owner: required, not yet covered.
- Runbook validation: required, not yet covered.

Questions required for complete coverage:
1. “What sustained throughput must the system support for a GA go/no-go?”
2. “What is the limiting bottleneck at that throughput?”
3. “Based on the current evidence, is the target SLO feasible for GA?”
4. “Which metric should govern rollback?”
5. “What threshold on that metric should trigger rollback?”
6. “Over what evaluation window should that threshold be measured?”
7. “Who will own the on-call response for GA?”
8. “Has the GA runbook been validated in a representative exercise?”

Conflict:
- Eight distinct material answers plus the minimum answering context cannot be shown to fit the locked two-minute effort budget. Omitting or combining them would violate complete, atomic coverage; exceeding two minutes would violate the hard budget. Do not write. Priya Shah must be given a larger effort budget or the sender must explicitly narrow the needed-back ledger.
