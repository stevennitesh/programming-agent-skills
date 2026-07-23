# Case 1 — Omission

Proceed: yes.

Write state: do not Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput → covered by: “What sustained throughput has the system demonstrated under the expected GA workload?”
- SLO feasibility → uncovered.
- Rollback → covered by: “What evidence shows that the proposed rollback approach will work under GA production conditions?”

Question required before Save:

- “Based on the current production-readiness evidence, can the proposed GA SLO be met consistently? Please identify any SLO target that is not yet feasible and the limiting evidence.”

Conflict: the user asked to finalize, but the draft omits the known SLO-feasibility ledger item. Finalization cannot override complete needed-back coverage. Add the atomic SLO-feasibility question, then recheck the effort budget before Save.

# Case 2 — Orphan

Proceed: yes.

Write state: do not Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput → covered by: “What sustained throughput has the system demonstrated under the expected GA workload?”
- Rollback → covered by: “What evidence shows that the proposed rollback approach will work under GA production conditions?”

Question to remove before Save:

- “What color should the launch dashboard use?”

Conflict: the dashboard-color question does not unlock the GA go/no-go decision and is not backed by the needed-back ledger. Remove it as out of scope, then verify that the two retained questions remain atomic and recipient-answerable before Save.

# Case 3 — Catch-all

Proceed: yes.

Write state: do not Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage:

- Named throughput → covered by: “What sustained throughput has the system demonstrated under the expected GA workload?”
- Rollback → covered by: “What evidence shows that the proposed rollback approach will work under GA production conditions?”
- Top production risk → uncovered; “Anything else?” does not cover a known ledger item.

Question required before Save:

- “What is the single highest production risk that could change the GA go/no-go decision, and what evidence supports that assessment?”

Catch-all:

- “Anything else?”

Conflict: the generic catch-all may surface unknowns, but it cannot stand in for the known top-production-risk item. Add the explicit risk question and retain the catch-all only as a final prompt before Save.

# Case 4 — Hard budget

Proceed: yes, through ledger construction and conflict reporting only.

Write state: do not Draft or Save.

Recipient: Priya Shah.

Downstream decision: GA go/no-go.

Needed-back coverage required:

- Named throughput → requires: “What sustained throughput has the system demonstrated under the expected GA workload?”
- Bottleneck → requires: “What is the current limiting bottleneck at that throughput?”
- SLO feasibility → requires: “Can the proposed GA SLO be met consistently based on current evidence?”
- Rollback metric → requires: “Which metric should trigger rollback?”
- Threshold → requires: “What exact value of that metric should trigger rollback?”
- Evaluation window → requires: “Over what evaluation window must the threshold be met before rollback?”
- On-call owner → requires: “Who is the on-call owner authorized to initiate the rollback?”
- Runbook validation → requires: “When and how was the rollback runbook last validated under production-like conditions?”

Conflict: the hard two-minute answer budget cannot credibly accommodate eight distinct material, atomic, recipient-answerable questions, while the coverage gate forbids omitting any of them. No compliant questionnaire can be written under both locked constraints.

Question to the user:

- “Which constraint may change: extend Priya Shah’s answer budget enough to cover all eight material items, or move one or more named items to a separate authorized questionnaire while preserving complete coverage?”
