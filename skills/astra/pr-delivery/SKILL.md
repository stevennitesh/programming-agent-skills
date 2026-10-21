---
name: pr-delivery
description: Create, update, monitor, or merge pull requests, including status inquiries. Exclude review-only assessment.
---

# PR delivery

Deliver the requested pull request outcome with a clear description and evidence
for its actual remote state. Use the available connector, API, or CLI that exposes
the needed information and effects; no particular forge or tool is required.

Match the endpoint to the user's request. A status inquiry is read-only and ends
with one current report. Creating or updating a PR does not by itself authorize
continued monitoring, review fixes, or merge. When follow-through is requested,
continue through its authorized effects without stopping at each intermediate
green check or status update. Existing user authority persists across turns.

## Establish the target and authority

Identify the repository and intended remote, base branch, source branch, local
candidate, published PR head, and existing PR before creating one. Reuse the
intended existing PR rather than creating a duplicate. Do not assume a default
branch name or treat a stale remote-tracking ref as current remote evidence.

Read applicable repository delivery rules and the user's requested endpoint,
checks, reviews, and merge conditions. Distinguish those requirements from optional
suggestions. Preserve unrelated dirty work and active write ownership. A delivery
request does not authorize discarding work, rewriting shared history, accepting
residual risk, or unrelated cleanup.

## Prepare and publish the PR

Inspect the actual candidate and comparison before describing or publishing it.
Complete the required verification and supported in-scope repairs. Stage, commit,
and push only work covered by existing authority and repository policy; do not
absorb unrelated changes to make publication convenient.

Write a concise, human-readable title and description for a reviewer who has not
seen the conversation. Lead with the concrete problem and resulting behavior;
include the evidence needed to assess the change and material verification limits.
Use a before/after example when useful. Scale detail to the change and repository
conventions; a fixed template, screenshots, or a lengthy checklist is not required
unless the repository or user requires them. Update stale PR prose when scope
changes so it describes the final implementation.

Read back the created or updated PR, including its base and head, before reporting
publication. If a mutation has an uncertain outcome, inspect current remote state
before retrying it. Follow host requirements for attaching the PR to the chat.

## Carry requested checks and review through

Track required CI and each explicitly requested hosted review, including Codex
review where requested, against the applicable candidate. Distinguish pending,
absent, unavailable, failed, and passed outcomes. Establish review completion from
the review system's actual completion evidence; green CI, silence, or no comments
does not establish that a requested review ran or finished.

Assess feedback with [Review feedback](../change-review/references/review-feedback.md).
For GitHub thread coverage, replies, or resolution, use
[GitHub review threads](../change-review/references/github-review-threads.md).
For another forge, preserve the same coverage, identity, technical-disposition,
mutation-readback, and freshness obligations using its available review surface.
Use [change-review](../change-review/SKILL.md) for a needed candidate assessment;
delivery does not automatically require a separate reviewer or review swarm.

Treat automated and human comments as technical claims. Verify them against the
current candidate, requirements, and affected behavior before fixing or rejecting
them. Apply supported corrections within the original authorized scope, grouping
related fixes when useful. Reviewer preference does not override settled user
decisions or authorize broader work. Replies and thread resolutions require their
own existing authority; a local correction alone cannot justify remote resolution.

After a head change, reestablish affected verification and requested review
evidence for the successor. Retain evidence only where its relevant inputs remain
valid, and account for base changes that affect the gates. Distinguish code or
configuration failures from infrastructure, access, and unavailable evidence;
unsupported speculative code changes do not repair an evidence outage.

Wait through the requested finish line, using useful updates while work continues.
Treat new questions and constraints as steering unless the user cancels or replaces
the objective. Retry recoverable failures within scope; stop dependent work for
missing authority, required input, or an operational blocker that cannot be
resolved within scope. Report the blocker and next useful action rather than
creating a new approval gate or retrying indefinitely.

## Merge and verify the endpoint

Merge only with existing user authority, satisfied current repository gates and
requested checks and reviews, an authorized disposition of remaining actionable
or uncertain findings, and confirmed forge mergeability. A completed review with
no findings is evidence for that review, not a substitute for another required gate.

Immediately before merging, refresh the PR's base and exact head and confirm that
the gate evidence still applies. Guard the merge with that head when supported.
If it moved, reassess the successor; do not bypass a failed guard. Follow the
authorized merge method and repository policy. Active conflicts belong to
[resolving-merge-conflicts](../resolving-merge-conflicts/SKILL.md); resolve them only
within the authorized integration endpoint.

Read back remote PR and target-branch state after the merge, including the merged
revision, before claiming success. For an uncertain merge response, inspect state
before retrying. Branch and worktree disposition remains with
[git-cleanup](../git-cleanup/SKILL.md) when requested.

Report the PR link, endpoint reached, candidate or merged revision, decisive check
and review results, and any remaining blocker or evidence limit. Distinguish local
repairs, published changes, and verified merge state. Keep status-only reports
bounded to their inquiry; leave unfinished requested delivery with a usable
continuation state when an actual blocker prevents completion.
