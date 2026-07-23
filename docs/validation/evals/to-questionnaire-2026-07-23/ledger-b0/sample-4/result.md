## Case 1 — Omission

Recipient: Priya Shah
Downstream decision: GA go/no-go
Proceed to Save: No
Write state: Do not write the questionnaire.

Needed-back coverage:

- Throughput → covered by the draft’s throughput question.
- SLO feasibility → uncovered.
- Rollback → covered by the draft’s rollback question.

Required question before Save:

> Is the GA SLO feasible under the expected production load?

Conflict: “Finalize” cannot override the coverage requirement. The known SLO-feasibility ledger item has no atomic, recipient-answerable question. Add the question, recheck the three-item ledger, and only then proceed to Save.

## Case 2 — Orphan

Recipient: Priya Shah
Downstream decision: GA go/no-go
Proceed to Save: Yes, after removing the orphan question.
Write state: Do not write yet; this is the pre-Save correction.

Needed-back coverage:

- Throughput → covered by the draft’s throughput question.
- Rollback → covered by the draft’s rollback question.

Question to remove:

> What color should the dashboard be?

Conflict: The dashboard-color question maps to no needed-back ledger item and is unrelated to the GA go/no-go decision. Remove it; no replacement question is needed.

## Case 3 — Catch-all

Recipient: Priya Shah
Downstream decision: GA go/no-go
Proceed to Save: No
Write state: Do not write the questionnaire.

Needed-back coverage:

- Throughput → covered by the draft’s throughput question.
- Rollback → covered by the draft’s rollback question.
- Top production risk → uncovered; `Anything else?` does not cover a known ledger item.

Required question before the final catch-all:

> What is the single highest production risk that should affect the GA go/no-go decision?

Conflict: The generic catch-all cannot substitute for the explicit top-production-risk question. Add the atomic question, retain `Anything else?` only as the final catch-all, and recheck all three ledger items before Save.

## Case 4 — Hard budget

Recipient: Priya Shah
Downstream decision: GA go/no-go
Proceed to Save: No
Write state: Do not write the questionnaire.

Required needed-back coverage and questions:

- Throughput → “What sustained production throughput must the system support for GA?”
- Bottleneck → “What is the most likely production bottleneck at that throughput?”
- SLO feasibility → “Is the GA SLO feasible under the expected production load?”
- Rollback metric → “Which production metric should govern rollback?”
- Threshold → “What value of that metric should trigger rollback?”
- Evaluation window → “Over what evaluation window must the rollback threshold be assessed?”
- On-call owner → “Who is the on-call owner for the GA launch?”
- Runbook validation → “Has the GA runbook been validated in a production-like exercise?”

Conflict: Eight distinct material needs require eight atomic answers. A hard two-minute effort budget cannot credibly cover all eight without either exceeding the budget or omitting material coverage. Neither is permitted.

Required sender resolution:

> Can the answering-effort budget be increased enough for Priya Shah to answer all eight atomic questions?

Until the budget is increased, the send cannot satisfy both Cover and effort fit, so Save is blocked.
