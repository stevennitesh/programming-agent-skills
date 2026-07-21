# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`. This directory is durable, version-controlled tracker state.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The parent spec is `.scratch/<feature-slug>/SPEC.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Triage is recorded with `Category:` and `Status:` lines near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

Example triage header:

```markdown
Category: enhancement
Status: ready-for-agent
```

## When a skill says "publish to the issue tracker"

For a parent spec, create `.scratch/<feature-slug>/SPEC.md` (creating the directory if needed). For implementation issues, use `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`, `$parallel-implement`, and `$review`.

**Implemented items remain as tracked files.**

- **Packet**: `SPEC.md`, issue bodies, `## Comments`, and `## Implementation Notes` are the durable packet. Approved implementation issues use `Status: ready-for-agent` and one category role when the source settles it.
- **Ready-for-agent contract**: every ready item names one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. `$triage` owns incoming classification and verification; `$to-tickets` owns slicing and dependency order. Both produce this contract.
- **Parent / child**: `SPEC.md` is the parent. Its ordered issue list links each file, and every issue records `Parent: ../SPEC.md`.
- **Blocking**: put `Blocked by: <NN>, <NN>` near the top of an issue. Normally a work item is unblocked when every listed issue has `Status: implemented`. During one recorded `$parallel-implement` campaign, a blocker with an accepted landing that remains in current integration history with valid proof is derived as `landed-awaiting-lock`; it satisfies execution readiness only for in-scope dependents in that campaign. The recorded dependency remains until Lock. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.
- **Ready query**: list issues with `Status: ready-for-agent`, then drop issues with an unresolved blocker or `Claimed by`. Treat a recorded blocker as resolved only when the verified same-campaign `landed-awaiting-lock` overlay above applies. Preserve the order in `SPEC.md`; without a parent order, choose the lowest issue number.
- **Claim**: add `Claimed by: <driver/session>` before implementation dispatch; keep the state role unchanged.
- **Release**: remove `Claimed by` when work blocks, is abandoned, or reaches closeout.
- **Closeout**: after acceptable review and before Lock, append the final closeout packet under `## Implementation Notes`, set `Status: implemented`, remove the claim, stage the tracker file with the selected-work diff, and apply **Mutation read-back**.
- **Mutation read-back**: after creating or changing tracker files, reread them and verify the intended body, relationships, state, claim, comments, and closeout metadata. A partial mutation is blocked; report applied operations, failed operations, and the safest recovery action.

## Wayfinder tracker mapping

This section maps Wayfinder's provider-neutral objects and primitives to Local Markdown. Wayfinder owns identity rules, fields, state, claims, recovery, sequencing, and completion.

- **Map object**: `.scratch/<feature-slug>/wayfinder/map.md`, containing the fields defined by Wayfinder's `MAP-FORMAT.md`. Candidate lookup searches open and closed maps beneath `.scratch/`.
- **Ticket object**: ordered files at `.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md` with `Part of:` pointing to the map.
- **Resolver type mapping**: `Type: research | prototype | diagnosis | questionnaire | grilling | design | task`; Local Markdown creates no hosted labels.
- **Parent and blocking mapping**: map order plus `Part of:` and `Blocked by:` repository-relative paths.
- **Claim storage**: the map file stores Wayfinder's campaign-claim block; ticket files carry no independent claim.
- **Claim capability**: `unavailable` until the target records an exact atomic create or compare-and-swap guard against a captured revision. A configured primitive must fail a losing actor or changed revision; record its invocation and losing-race result here.
- **Claim release mapping**: remove the configured guard and map claim block, then reread their absence.
- **Revision token**: repository-relative path, Git blob id when tracked or SHA-256 content hash otherwise, file size, and modification timestamp.
- **Read-back primitive**: reread every changed file and affected relationship; return filesystem errors and observed fields to the owning skill.

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment. Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from `$triage`.
