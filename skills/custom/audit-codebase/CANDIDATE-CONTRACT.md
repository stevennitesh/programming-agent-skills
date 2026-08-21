# Candidate analysis

A candidate is a user-selectable improvement boundary supported by at least
one admitted defect or opportunity. It may live inside one subsystem or span
several when the members share one causal owner, repeated policy, improvement
direction, and Proof Seam.

## Present

Record:

```text
Candidate ID:
Title:
Subsystems and causal owner:
Member finding IDs:
Supported behavior:
Current evidence and demonstrated cost:
Affected callers:
Improvement direction:
Behavior and safety floors:
Proof Seam and required proof:
Confidence and evidence limits:
State: presented
```

Keep every member visible. Gap-only hypotheses and retained complexity are not
candidates. Rank candidates across audited evidence, but leave selection to the
user.

## Revalidate

The report is a lead, not current proof. Reread the implicated source, callers,
contracts, decisions, tests, members, and Proof Seams.

- **Confirmed:** the recorded problem and direction still hold.
- **Changed:** update the evidence, scope, members, or direction while a
  coherent supported candidate remains.
- **Disproved:** record the evidence that removed the problem or cost.
- **Blocked:** record the missing evidence or user decision and exact re-entry.

Unrelated drift does not invalidate the candidate. A changed causal owner or
new affected subsystem widens the Source Trace without forcing a full remap.

## Compare

Start with Keep and the smallest sound change. Compare a structural change or
replacement only when it is materially plausible.

```text
Current shape and demonstrated cost:
Smallest sound change:
Other material option and trade-off: <option> | none
Recommended direction:
Affected ownership, interfaces, data, and decisions:
Compatibility or migration need: <evidenced need> | none
Proof:
Residual risk or evidence gap:
State: analyzed | blocked | disproved
```

Prefer subtraction and the current owner. Earn a new boundary through
information hiding, supported variation, or a real external dependency. Bound
fallout and leave unrelated cleanup separate.

When a material user decision remains, state the exact question and viable
consequences. Suggest the natural owner and stop. Analysis does not mutate
domain records, publish tickets, specify an implementation graph, or start
implementation.
