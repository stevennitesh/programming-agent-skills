# Attention scan

Use only for a read-only overview of raw intake requiring maintainer attention.

Query the configured tracker and return these disjoint groups, oldest first:

1. items missing or carrying conflicting configured category or state roles;
2. items in `needs-triage`; and
3. items in `needs-info` with reporter activity since the latest attributable
   triage request.

Assign each item to its first matching group. If the tracker cannot establish the
activity boundary, report that uncertainty rather than guessing.

Include external PRs or MRs only when configured as intake and identify their
type. Return counts and concise summaries. Do not verify claims, shape product
meaning, publish handoffs, or mutate tracker state during the scan.
