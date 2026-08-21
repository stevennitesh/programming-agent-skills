# Plain Worker Handoff

Send a fresh implementation worker only the task context needed to begin:

- **Ticket and desired outcome:** the selected work item and observable result.
- **Fixed decisions and relevant context:** settled choices plus precise source,
  repository, and symbol references worth reading.
- **Acceptance criteria:** every behavior the worker must satisfy, including any
  real caller or runtime entry-to-output path that must be proven.
- **Owned write scope:** allowed files or directories, exclusions, and protected
  areas.
- **Repository base and working directory:** the exact starting commit and the
  checkout in which every command and write must occur.
- **Required validation:** focused commands and evidence through the claimed
  runtime path; component proof counts only when that path exercises the
  component.
- **Stop and escalation conditions:** new authority, contradictory repository
  evidence, overlapping ownership, or an unplanned public-contract decision.
- **Expected evidence return:** changed scope, task commit when requested,
  commands and observed results, acceptance evidence, and any material gap.

Do not include the coordinator's planning transcript. The worker implements only
the assigned scope and does not edit the authoritative spec or ticket graph,
integrate, push, review, close tickets, or spawn another worker. It may create
one task-scoped commit when the assignment requests one.

Return concise prose. If work remains, name the exact blocker and next safe
action. The coordinator inspects the diff, commit, and evidence before granting
completion or issuing one bounded correction.
