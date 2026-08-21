# Issue tracker: Local Markdown

Tracker state is durable, version-controlled Markdown under
`.scratch/<feature-slug>/`. This guide maps skill-owned tracker actions to that
representation. Skills own packet content, readiness judgment, authorization,
workflow order, claim lifecycle, review, and completion.

## Operations

- **Parent:** `.scratch/<feature-slug>/SPEC.md`.
- **Issues:** `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from
  `01`.
- **Publish:** create the applicable parent or issue file.
- **Fetch:** read the referenced file.
- **Comment or brief:** append under `## Comments`, or add
  `## Codex-Ready Brief` when comments do not exist. `$triage` owns the brief
  and disclaimer.

Put `Category:` and `Status:` near the top. Append closeout evidence under
`## Implementation Notes`. Implemented items remain tracked files and accompany
the selected-work commit.

## Work-item representation

- **Packet:** parent, issue body, comments, and implementation notes.
- **State:** `Status: ready-for-agent | ready-for-human | implemented |
  <mapped non-ready state>` plus the applicable mapped `Category:`. Ready states
  are navigation metadata, not proof that a packet or transition is valid.
- **Parent / child:** the parent links issues in order; each issue stores
  `Parent: ../SPEC.md`.
- **Blocking:** `Blocked by: <NN>, <NN>`; a blocker clears when its status is
  `implemented`.
- **Ready query:** derive agent and human frontiers separately from mapped ready
  states, then exclude unresolved blockers and `Claimed by:`. Preserve parent
  order; otherwise use the lowest issue number.
- **Claim:** `Claimed by: <driver/session>`.
- **Closeout:** append the skill-owned packet under implementation notes, set
  `Status: implemented`, and remove the claim.

Closing or superseding a blocker must not expose a false-ready dependent.

## Wayfinding representation

Use `.scratch/<feature-slug>/wayfinder/map.md` with
`Status: Open | Complete` and
`.scratch/<feature-slug>/wayfinder/tickets/<NN>-<slug>.md` in map order.

Each ticket stores `Part of: map.md`, `Type:`, `Decision owner:`,
`Accept when:`, and any applicable `Mutation boundary:`, plus
`Status: Pending | In Progress | Resolved | Blocked | Waiting | Out Of Scope`.
Store edges in `Blocked by:`, waiting return records under comments, and active
claims in `Claimed by:` and `Claim token:`. Store resolution and
scope notes under comments and decision pointers in the map. `$wayfinder` owns
frontier selection, claim lifecycle, outcomes, and map completion.

## Mutation read-back

After a mutation, reread changed files and affected dependents and verify every
intended body, relationship, state, claim, comment, closeout field, and
resulting frontier. When recovery is required, do not retry blindly. Treat any
unverified partial mutation as blocked and report applied, failed, and unknown
effects plus the safest recovery.
