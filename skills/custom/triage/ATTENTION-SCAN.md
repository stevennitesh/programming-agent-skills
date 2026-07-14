# Attention Scan

Query the configured tracker and present these disjoint buckets oldest first:

1. **Role drift:** unlabeled items and items with missing or conflicting category or state roles.
2. **`needs-triage`:** evaluation in progress.
3. **`needs-info` with reporter activity:** reporter activity since the latest triage note.

Assign each item to its first matching bucket. When PR triage is enabled, include configured external PRs and tag every line `[PR]` or `[issue]`.

Show counts and one-line summaries, make no mutations, and let the maintainer choose.

Complete when all three buckets were evaluated, PR policy was respected, counts and summaries were returned, and tracker state stayed unchanged.
