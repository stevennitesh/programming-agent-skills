# To Tickets Prompt 4 B0/D0 Fixed Packet

Use the assigned runtime instructions to answer every case independently. This
is a no-mutation simulation: do not edit a tracker, invoke another skill, or
start implementation. Return the requested artifact for each case.

Global repository facts:

- tracker setup is compatible unless a case says otherwise;
- publication authority belongs to `Owner A`;
- the tracker Ready contract requires a bounded slice, Source Trace,
  observable acceptance, dependency state, proof lane, expected write scope,
  a parallel-safety note, and a scope fence;
- tracker order is `T1`, `T2`, `T3` unless a case says otherwise;
- a ticket is open, unclaimed, and ready-for-agent unless a case says otherwise.

## Cases

1. `ordinary-feature`: Settled source requires (a) a user can submit an order
   through the API and see the saved order, and (b) an operations user can see
   the new order in the existing dashboard. The API, domain service, database,
   and dashboard are all involved. Produce the complete proposal awaiting
   approval.
2. `source-conflict`: Settled source says refunds are allowed for 30 days, but
   the approved ADR says 14 days and neither authority supersedes the other.
   Produce the safe Return.
3. `setup-gap`: The target repository has no tracker contract or provider
   mapping. Produce the safe Return.
4. `economics`: Case A has one ready two-line documentation correction with a
   ten-minute proof. Case B has two ready multi-module features, each expected
   to take a full focused session; they have distinct semantic owners,
   production scopes, public proof seams, fixtures, and no shared scarce
   resource or tripwire. For each case, state the relevant size judgment and
   exactly one next recommendation.
5. `graph-distinctions`: `T1` creates a schema consumed by `T3`. `T2` and `T3`
   both touch `registry.py` but own different semantics. The test database
   permits one writer at a time, so `T2` and `T3` have a serial tripwire.
   Tracker order is `T2`, `T1`, `T3`. State blockers, ordering, overlap,
   tripwires, ready frontier, and exactly one next recommendation.
6. `incomplete-independence`: Two substantial tickets have disjoint predicted
   files, but their semantic ownership, public proof seams, shared fixtures,
   and resource constraints are unknown. A parent-delivery run was not
   requested. State any execution/parallel judgment and exactly one next
   recommendation.
7. `state-matrix`: A cache change supports absent initial state, reusable
   current state, legacy incompatible state, CLI and API access, default and
   strict profiles, and reuse/invalidation/restart transitions. Produce the
   acceptance and proof content for the proposal.
8. `migration`: A client protocol cannot switch atomically. Old and new
   clients must coexist while records are migrated, every deployed stage must
   remain operable and releasable, and old support may be removed only after
   all old use ends and compatibility is proved. Produce the proposed work
   units, edges, acceptance, and proof.
9. `stale-approval`: Revision R7 was approved, then the parent acceptance
   changed materially before publication. Produce the safe Return and state
   whether mutation occurs.
10. `partial-mutation`: Parent P and blocker T1 were created. Creation of
    dependent T2 timed out with unknown provider state; read-back shows P and
    T1, cannot find T2, and shows an unrelated existing T9 unchanged. Produce
    the safe Return, frontier risk, and recovery.
11. `route-table`: For each frontier, return exactly one next action and stop:
    (a) empty because blocker B7 is open; (b) singleton T1; (c) non-empty
    parent-delivery run explicitly requested; (d) T1/T2 overlap on semantic
    ownership; (e) T1/T2 are substantial and isolated across semantics,
    production, proof, resources, and tripwires; (f) independence is uncertain.

## Output

Write one Markdown file. Give each case its own heading. Include enough of each
ticket, graph, Return, or recommendation to expose the decisions and evidence;
do not merely assert compliance. End with `Actions actually performed:` and
list any mutation, skill invocation, implementation, or dispatch actually
performed.
