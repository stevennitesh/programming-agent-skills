# Case: Omission

Recipient: Priya Shah
Downstream decision: GA go/no-go

Proceed to Save: Yes. The supplied draft is revised before Save so that every named needed-back item has an explicit question.

Resulting coverage and questions:

1. Throughput — What sustained production throughput can the system support for GA?
2. 99.9% SLO feasibility — Is the 99.9% SLO feasible at that throughput?
3. Rollback trigger — What exact production condition should trigger a GA rollback?
4. Final catch-all — Is there anything else we should know before making the GA go/no-go decision?

# Case: Orphan

Recipient: Priya Shah
Downstream decision: GA go/no-go

Proceed to Save: Yes. The dashboard-color question is removed because it does not unlock the GA go/no-go decision.

Resulting coverage and questions:

1. Throughput — What sustained production throughput can the system support for GA?
2. Rollback trigger — What exact production condition should trigger a GA rollback?
3. Final catch-all — Is there anything else we should know before making the GA go/no-go decision?

# Case: Catch-all

Recipient: Priya Shah
Downstream decision: GA go/no-go

Proceed to Save: Yes. `Anything else?` remains only as the final catch-all; it does not cover the known top-production-risk ledger item, which receives its own question.

Resulting coverage and questions:

1. Throughput — What sustained production throughput can the system support for GA?
2. Rollback trigger — What exact production condition should trigger a GA rollback?
3. Top production risk — What is the single most important production risk that should affect the GA go/no-go decision?
4. Final catch-all — Is there anything else we should know before making the GA go/no-go decision?

# Case: Hard budget

Recipient: Priya Shah
Downstream decision: GA go/no-go

Proceed to Save: No. No questionnaire is written. The hard two-minute effort budget conflicts with the requirement to obtain eight distinct material facts or judgments through atomic questions, and neither constraint may be relaxed.

Required coverage that cannot be omitted:

1. What sustained production throughput can the system support for GA?
2. What is the limiting production bottleneck at that throughput?
3. Is the 99.9% SLO feasible at that throughput?
4. Which production metric should govern rollback?
5. What threshold on that metric should trigger rollback?
6. Over what evaluation window should the rollback threshold be assessed?
7. Who is the on-call owner for the GA release?
8. Has the GA rollback runbook been validated under production-like conditions?

Conflict requiring resolution before Save: increase the effort budget enough to answer all eight questions, or explicitly reduce the required coverage. Under the locked instructions, completion is not possible.
