# GitHub review threads

Read when assessing or acting on GitHub PR feedback and thread coverage or
resolution state matters. Use [Review feedback](review-feedback.md) to assess
claims and corrections; choose the available connector, API, or CLI that exposes
the needed state.

## Establish the relevant feedback

Identify the repository, PR, and candidate head. Retrieve actual review threads,
their replies, locations, and resolution state. Follow pagination for the scope
requested; flat comment summaries or a first page cannot establish complete
thread coverage. If access or tooling limits coverage, identify what remains
unread or unavailable.

Keep thread identities associated with the comments and candidate they address.
Assess their relevance to the current code: an outdated location can still
describe an unfixed problem, and a resolved thread can concern behavior changed
again since its resolution. Include relevant review summaries or supplied feedback
outside threads when the request covers them.

## Verify corrections and authorized state changes

Apply the existing feedback assessment before deciding whether a correction or
thread action is warranted. Preserve the distinction between a comment's technical
disposition and its GitHub resolution state.

For authorized replies or resolutions, make the disposition and supporting evidence
clear. Before resolving a thread for a code fix, establish that the PR contains
the verified correction. A local fix alone does not establish that state.

Read back affected threads after a mutation before claiming success. If a call's
outcome is uncertain, inspect current state before retrying. Recheck the PR head
before concluding; if it changed, establish which assessment and verification
still apply and what needs further review.

Report remaining actionable or uncertain items and material coverage limits,
including any mismatch between technical disposition and recorded thread state.
Thread closure alone does not establish candidate correctness. Publication,
merge, and branch cleanup remain with their authorized workflows.
