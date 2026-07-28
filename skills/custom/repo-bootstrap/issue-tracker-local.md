# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`. This
directory is durable, version-controlled tracker state.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The parent spec is `.scratch/<feature-slug>/SPEC.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
  numbered from `01`
- Triage is recorded with `Category:` and `Status:` lines near the top of each
  issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a
  `## Comments` heading

Example triage header:

```markdown
Category: enhancement
Status: ready-for-agent
```

## When a skill says "publish to the issue tracker"

For a parent spec, create `.scratch/<feature-slug>/SPEC.md` (creating the
directory if needed). For implementation issues, use
`.scratch/<feature-slug>/issues/<NN>-<slug>.md`.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or
the issue number directly.

## Work-item operations

Used by `$to-spec`, `$to-tickets`, `$triage`, `$implement`,
`$parallel-implement`, `$change-review`, and `$high-assurance-review`.

**Implemented items remain as tracked files.**

- **Packet**: `SPEC.md`, issue bodies, `## Comments`, and
  `## Implementation Notes` are the durable packet. Approved implementation
  issues use `Status: ready-for-agent` and one category role when the source
  settles it.
- **Ready-for-agent state**: the configured state marks an item whose producing
  workflow verified its owned packet. The state is navigation metadata, not
  proof of content completeness. `$triage` owns its Codex-ready brief and Ready
  Gate; `$to-tickets` owns its execution packets and graph readiness.
- **Parent / child**: `SPEC.md` is the parent. Its ordered issue list links each
  file, and every issue records `Parent: ../SPEC.md`.
- **Blocking**: put `Blocked by: <NN>, <NN>` near the top of an issue. Normally
  a work item is unblocked when every listed issue has `Status: implemented`.
  During one recorded `$parallel-implement` campaign, a blocker with an accepted
  landing that remains in current integration history with valid proof is
  derived as `landed-awaiting-lock`; it satisfies execution readiness only for
  in-scope dependents in that campaign. The recorded dependency remains until
  Lock. Rollback, invalidation, or failed proof removes the overlay and reblocks
  dependents.
- **Ready query**: list issues with `Status: ready-for-agent`, then drop issues
  with an unresolved blocker or `Claimed by`. Treat a recorded blocker as
  resolved only when the verified same-campaign `landed-awaiting-lock` overlay
  above applies. Preserve the order in `SPEC.md`; without a parent order, choose
  the lowest issue number.
- **Claim**: add `Claimed by: <driver/session>` before implementation dispatch;
  keep the state role unchanged.
- **Release**: remove `Claimed by` when work blocks, is abandoned, or reaches
  closeout.
- **Closeout**: after acceptable review and before Lock, append the final
  closeout packet under `## Implementation Notes`, set `Status: implemented`,
  remove the claim, stage the tracker file with the selected-work diff, and
  apply **Mutation read-back**.
- **Mutation read-back**: after creating or changing tracker files, reread the
  changed files and every affected dependent file; verify the intended file
  bodies, relationships, state, claims, comments, closeout metadata, and
  resulting ready frontier. A partial mutation is blocked; report applied
  operations, failed operations, and the safest recovery action.

## Wayfinding operations

Used by `$wayfinder`. The **map** is one markdown file with child ticket files.

- **Map**: create `.scratch/<feature-slug>/wayfinder/map.md`. Put
  `Status: Open | Complete` near the top and follow the invoking Wayfinder's
  `MAP-FORMAT.md` contract.
- **Child ticket**: create
  `.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md` in approved map
  order. Put `Part of: map.md`,
  `Type: research | prototype | diagnosis | grilling | task`,
  `Participation: HITL | AFK`, `Resolution owner:`, `Resolver:`,
  `Expected return:`, `Re-entry owner: $wayfinder`, and
  `Status: Pending | In Progress | Resolved | Blocked | Waiting | Out Of Scope`
  near the top. Read back exact paths before adding `Blocked by: <NN>, <NN>`.
  Add claim fields only while claimed.
- **Blocking and waiting**: a ticket is unblocked when every ticket in
  `Blocked by` is `Resolved` or `Out Of Scope`. When the last blocker clears,
  change `Status: Blocked` to `Status: Pending`. For `Status: Waiting`, record
  the exact return trigger, return owner, and any artifact pointer and
  durability
  under `## Comments`. Select it through Advance only after attributable
  returned evidence matches the exact trigger; change status only with the
  applied outcome.
- **Frontier query**: list tickets with `Status: Pending`, then drop tickets
  with an unresolved blocker or active `Claim token:`. The remaining tickets in
  map order are the frontier; the first is the default selection.
- **Claim**: Advance first claims the selected ticket for resolver work, then
  claims the map before recording any ticket outcome, edge, fog disposition, or
  other shared map mutation. Closure also requires the map claim. Maintain
  claims the map. Put `Claimed by: codex`,
  `Claim token: codex/<lowercase UUIDv4>`, and
  `Claimed at: <YYYY-MM-DDTHH:MM:SSZ>` on the claimed item; also set a claimed
  Pending ticket to `Status: In Progress`; a claimed Waiting ticket stays
  Waiting until its outcome is applied. Generate one fresh UUIDv4 per Wayfinder
  invocation, reuse it for both claims in that invocation, and never reuse it
  across invocations. Read back the exact token and timestamp; a different
  token owns the item even when the driver is the same.
- **Release**: remove `Claimed by`, `Claim token:`, and `Claimed at:` when
  active work ends.
- **Stale claim**: Elapsed time alone never makes a claim stale. Replace a
  different token only after explicit user approval; first record the prior
  token, claimed-at value, and takeover reason under `## Comments`, then apply
  Mutation read-back to the replacement claim.
- **Outcome**: while the map claim is held, append the canonical resolution
  comment. Set `Resolved` and add its context pointer to `Decisions So Far`; set
  `Blocked` and wire a sharp blocker or return it to fog; set `Waiting` with its
  return record; or set `Out Of Scope` and append its linked scope note. Apply
  map consequences and read back, then release the ticket claim. Keep the map
  claim through eligible Closure; otherwise release it. Read back every final
  claim state. A failed map claim records no ticket outcome or shared mutation.
- **Complete map**: while the map claim is held and no unresolved child, wait,
  blocker, or fog remains, record the compact closing source or decision packet,
  set the map to `Status: Complete`, read back its state and empty frontier,
  release the claim, then read back the claim's absence.

## When a skill says "post a Codex-ready brief"

Append it to the issue file.

If the file already has `## Comments`, add the brief there as a new comment.
Otherwise add `## Codex-Ready Brief` after the triage header.

The brief text, including the AI triage disclaimer when required, comes from
`$triage`.
