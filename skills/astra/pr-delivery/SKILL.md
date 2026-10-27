---
name: pr-delivery
description: Create, update, monitor, or merge pull requests, including status inquiries. Exclude review-only assessment.
---

# PR delivery

Reach the requested PR endpoint and verify its actual remote state using a
connector, API, or CLI that exposes the needed information and effects.

Status inquiries end with one read-only report. Creation or update alone does not
authorize continued monitoring, review fixes, or merge. Carry requested
follow-through to its endpoint under existing authority, including across turns.

For requested end-to-end delivery or preparation for human merge, read
[Delivery endpoints](references/delivery-endpoints.md). For an old PR that needs
rebasing or reassessment against the current base, read
[Refresh an existing PR](references/refresh-existing-pr.md).

## Establish the target and authority

Identify the repository, intended remote, actual base and source branches, local
candidate, published head, and existing PR. Reuse the intended PR. A stale
remote-tracking ref is not current remote evidence.

Establish the requested endpoint and applicable checks, reviews, merge conditions,
and repository policy. Preserve unrelated work and active write custody; delivery
does not grant history-rewrite, cleanup, or residual-risk acceptance authority.

## Prepare and publish the PR

Inspect the candidate and comparison; complete required verification and supported
in-scope repairs. Stage, commit, and push only authorized work. Choose evidence
suited to the changed behavior: mocked checks alone do not establish real UI or
runtime behavior. Delivery does not override test or environment permissions.

Write the title and description for a reviewer without conversation context. Lead
with the concrete problem and resulting behavior; include decisive verification
and material limits. Scale detail to the change and repository conventions, using
a before/after example when useful. Update the prose when scope changes; extra
templates, screenshots, or checklists are needed only when required.

Check public text and attachments for private details. Quantitative benefits and
model/harness attribution must be verified and relevant to the requested format.
Preserve contributor credit during continuation.

Read back the PR's base, head, and changed state before claiming publication.
Inspect remote state before retrying an uncertain mutation. Follow host
requirements for attaching the PR to the chat.

## Carry requested checks and review through

Track required CI and each requested hosted review against the applicable
candidate. Distinguish pending, absent, unavailable, failed, and passed states.
Review completion needs the review system's actual evidence; green CI, silence,
or no comments does not prove a requested review ran or finished.

Assess feedback with [Review feedback](../change-review/references/review-feedback.md).
For GitHub feedback retrieval, comments, replies, or resolution, use
[GitHub review threads](references/github-review-threads.md).
For other forges, preserve the same coverage, identity, technical-disposition,
mutation-readback, and freshness obligations.
Use [change-review](../change-review/SKILL.md) for a needed candidate assessment;
delivery does not automatically require a separate reviewer or review swarm.

Carry supported corrections through the authorized scope. Replies and resolutions
require existing authority and verified remote state; a local fix alone cannot
justify thread resolution.

After head or base changes, reestablish affected verification, requested review,
and integration gates. Retain still-applicable evidence, including across Git-only
changes. Missing infrastructure or access evidence does not justify speculative
code fixes. Do not rebase every behind branch unless policy or behavior requires it.

For waiting on CI, review, or forge state, use
[PR monitoring](references/pr-monitoring.md). Treat new questions and constraints
as steering unless the user cancels or replaces the objective. Repair recoverable failures
within scope; stop dependent work for missing authority, required input, or a
blocker that cannot be resolved within scope. Leave a usable continuation state.

## Merge and verify the endpoint

Merge only with user authority, satisfied current gates and requested checks and
reviews, authorized disposition of remaining actionable or uncertain findings,
and confirmed forge mergeability. A clean review does not satisfy other gates.

Immediately before merging, refresh the PR's base and exact head and confirm that
the gate evidence still applies. Guard the merge with that head when supported.
If it moved, reassess the successor; do not bypass a failed guard. Follow the
authorized merge method and repository protections. Auto-merge enabled or a queued
merge remains pending until the forge confirms it merged. Active conflicts belong to
[resolving-merge-conflicts](../resolving-merge-conflicts/SKILL.md); resolve them only
within the authorized integration endpoint.

Read back the remote PR, target branch, and merged revision before claiming
success; inspect state before retrying an uncertain merge. Requested branch/worktree
cleanup remains with [git-cleanup](../git-cleanup/SKILL.md).

Report the PR, endpoint, candidate or merged revision, decisive checks and reviews,
and remaining blockers or evidence limits. Distinguish local repairs, published
changes, and verified merge state.
