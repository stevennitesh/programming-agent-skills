# Attention scan

Query the configured tracker and show these disjoint groups oldest first:

1. items missing or conflicting configured category or state roles;
2. items in `needs-triage`;
3. items in `needs-info` with reporter activity since the latest attributable
   triage request.

Assign each item to its first matching group. If the tracker cannot establish
the activity boundary, report that uncertainty instead of guessing. Include
external PRs or MRs only when configured and identify their type.

Return counts and one-line summaries. Complete after evaluating every group
without changing tracker state.
