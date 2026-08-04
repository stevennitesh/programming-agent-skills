# Plain Worker Handoff

Send a fresh implementation worker only the task context needed to begin:

- **Ticket and desired outcome:** the selected work item and observable result.
- **Fixed decisions and relevant context:** settled choices plus precise source,
  repository, and symbol references worth reading.
- **Acceptance criteria:** every behavior the worker must satisfy.
- **Owned write scope:** allowed files or directories, exclusions, and protected
  areas.
- **Repository base and working directory:** the exact starting commit and the
  checkout in which every command and write must occur.
- **Required validation:** focused commands and the evidence they must produce.
- **Stop and escalation conditions:** new authority, contradictory repository
  evidence, overlapping ownership, or an unplanned public-contract decision.
- **Expected evidence return:** the result described below.

Do not include the coordinator's planning transcript. The worker implements only
the assigned scope and does not edit the authoritative spec or ticket graph,
integrate, push, review, close tickets, or spawn another worker. It may create
one task-scoped commit when the assignment requests one.

Return:

- status: `completed | partial | blocked`;
- changed files and task commit when requested;
- commands run and observed results;
- acceptance-criterion evidence;
- assumptions, deviations, or remaining risk; and
- the exact blocker or recommended next action.

The return is provisional. The coordinator inspects the diff, commit, and
evidence before granting completion or issuing one bounded correction.
