# GitHub review threads

Read for GitHub PR feedback retrieval, comments, replies, or thread resolution.
Choose a connector, API, or CLI exposing the needed state. Retrieval can support
read-only review; replies and resolutions require existing authority. Technical
assessment stays with the caller; this procedure owns forge interaction and
verified remote state.

## Establish the relevant feedback

Identify the repository, PR, and candidate head. Retrieve actual review threads,
their replies, locations, and resolution state. Follow pagination for the scope
requested; flat comment summaries or a first page cannot establish complete
thread coverage. If access or tooling limits coverage, identify what remains
unread or unavailable.

Return thread identities with the comments, addressed candidate, and resolution
state. Outdated locations and resolved threads do not establish that a technical
issue is fixed. Include review summaries or other supplied feedback when requested.

## Verify corrections and authorized state changes

Before a thread action, require a supported technical disposition against the
current candidate. Keep that disposition separate from GitHub's resolution state.

For authorized replies or resolutions, make the disposition and supporting evidence
clear. Before resolving a thread for a code fix, establish that the PR contains
the verified correction. A local fix alone does not establish that state.

For an authorized comment or reply, lead with the disposition and cite the
relevant code, check, or reproduction. Keep the response concise and distinguish
observation from judgment. Check the complete public text, quotes, and attachments
for secrets or private details and inspect the rendered Markdown when formatting
matters. Use agent attribution when the user or repository requests it, with a
verified public model name or the known harness name if model identity is absent;
do not impose a signature or alter text requested verbatim.

Verify a successful reply through the returned comment identity or URL and
readback before resolving a thread that depends on that response. Technical
disposition alone does not establish that the reply was posted successfully.

Read back affected threads after a mutation before claiming success. If a call's
outcome is uncertain, inspect current state before retrying. Recheck the PR head
before concluding; if it changed, establish which assessment and verification
still apply and what needs further review.

Report remaining actionable or uncertain items and material coverage limits,
including any mismatch between technical disposition and recorded thread state.
Thread closure alone does not establish candidate correctness. Publication,
merge, and branch cleanup remain with their authorized workflows.
