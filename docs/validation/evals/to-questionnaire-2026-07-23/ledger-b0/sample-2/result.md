# Omission

Proceed: yes.

Write: blocked before Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput: covered by the throughput question.
- SLO feasibility: not covered.
- Rollback: covered by the rollback question.

Question required before Save:

1. Is the proposed SLO feasible for GA? Please identify the evidence, constraints, or assumptions that support your answer.

Conflict: the instruction to finalize conflicts with the Cover and completion requirements because SLO feasibility is a known needed-back item with no atomic, recipient-answerable question. Add the SLO-feasibility question before writing.

# Orphan

Proceed: yes.

Write: blocked before Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput: covered by the throughput question.
- Rollback: covered by the rollback question.

Questions required before Save: none.

Conflict: the dashboard-color question does not map to a needed-back item and is unrelated to the GA go/no-go decision. Remove it before writing.

# Catch-all

Proceed: yes.

Write: blocked before Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput: covered by the throughput question.
- Rollback: covered by the rollback question.
- Top production risk: not covered. `Anything else?` is a catch-all and does not cover this known ledger item.

Question required before Save:

1. What is the top production risk that should affect the GA go/no-go decision?

Conflict: the draft fails the Cover and completion requirements until the known top-production-risk item has its own atomic, recipient-answerable question. Add that question before writing.

# Hard budget

Proceed: yes.

Write: blocked before Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage required:

- Throughput: requires its own question.
- Bottleneck: requires its own question.
- SLO feasibility: requires its own question.
- Rollback metric: requires its own question.
- Rollback threshold: requires its own question.
- Evaluation window: requires its own question.
- On-call owner: requires its own question.
- Runbook validation: requires its own question.

Questions required before Save:

1. What throughput has the system demonstrated under the GA-representative workload?
2. What is the limiting bottleneck under that workload?
3. Is the proposed SLO feasible for GA?
4. Which metric should trigger rollback?
5. At what value should that rollback metric trigger rollback?
6. Over what evaluation window should the rollback threshold be assessed?
7. Who owns the on-call response for GA?
8. How has the GA runbook been validated?

Conflict: eight distinct material needs must each have an atomic question, but answering all eight cannot be represented as fitting the locked hard two-minute effort budget without unsupported omission or an unsupported effort assumption. Do not write. The sender must authorize either a larger effort budget or a reduced needed-back ledger; until then, the effort-fit and full-coverage completion requirements cannot both be satisfied.
