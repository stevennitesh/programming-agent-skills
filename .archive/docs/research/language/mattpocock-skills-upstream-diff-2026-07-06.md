# Matt Pocock Skills Upstream Diff - 2026-07-06

Durable source and reconstruction: [UPSTREAM-SOURCE.md](UPSTREAM-SOURCE.md).

## Scope

Compared the copied old repo at `.tmp/mattpocock-skills` against the freshly fetched upstream `origin/main`.

- Old/local commit: `43ea0884b07a3e67a5a07f025ce92aefa983177b`
- New upstream commit: `66f92b61f5b1434a1c7422f6fbd8efc5ee0c0214`
- Range inspected: `HEAD..origin/main`
- Package version stayed `1.0.1`.

The copied repo had three local dirty files before fetch. They were not included in the upstream comparison:

- `scripts/link-skills.sh`
- `scripts/list-skills.sh`
- `skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh`

## Top-Level Shape

The update is broad but coherent: promoted skills now have human-facing docs pages, `ask-matt` becomes a fuller router, `review` is promoted and renamed to `code-review`, `decision-mapping` is replaced by `wayfinder`, and `tdd` is rewritten as a tighter red-green reference.

Diff size:

- 59 files changed
- 1329 insertions
- 229 deletions

## Skill Inventory Changes

### Added Or Promoted

- `skills/engineering/research/SKILL.md`
  - New model-invoked skill.
  - Delegates reading to a background agent.
  - Requires primary sources and a cited Markdown file saved in the repo.

- `skills/engineering/code-review/SKILL.md`
  - Promoted from `skills/in-progress/review/SKILL.md`.
  - Renamed from `review` to `code-review`.
  - Runs a two-axis review: `Standards` and `Spec`.
  - Uses parallel sub-agents and adds an always-on Fowler smell baseline for Standards.

- `skills/in-progress/wayfinder/SKILL.md`
  - Replaces `decision-mapping`.
  - Plans work too large for one session as a shared issue-tracker map.
  - Introduces `destination`, `map`, `frontier`, `fog of war`, `not yet specified`, and `out of scope` as core vocabulary.
  - Claims tickets by assigning them, prefers native tracker blocking, and resolves one ticket per session.

- `skills/in-progress/claude-handoff/SKILL.md`
  - New in-progress skill for handing a conversation to a fresh background Claude agent with a named handoff summary.

### Removed Or Renamed

- `skills/in-progress/decision-mapping/SKILL.md` was deleted.
- `skills/in-progress/review/SKILL.md` was renamed/promoted to `skills/engineering/code-review/SKILL.md`.
- `skills/engineering/tdd/refactoring.md` was deleted.

## Behavior Changes By Skill

### `ask-matt`

`ask-matt` now maps the full skill set, not only user-invoked skills. It explicitly threads:

- `implement` driving `tdd` internally.
- `implement` ending with `code-review`.
- `diagnosing-bugs` as the "something is broken" on-ramp.
- `domain-modeling` and `codebase-design` as vocabulary layers underneath other skills.
- `research` as a standalone background-agent reading lane.

Migration watchpoint: our environment-wide guide already has a custom suggestion index. If we ingest this, keep one router as the source of truth rather than duplicating route logic in several places.

### `tdd`

`tdd` was substantially rewritten:

- It is now framed as a red-green reference, not a full workflow.
- It requires tests only at pre-agreed seams.
- It keeps the good-test rule: public interfaces, behavior, independent expected values.
- It calls implementation-coupled, tautological, and horizontal-slicing tests the main anti-patterns.
- It explicitly says refactoring belongs to `code-review`, not the red-green loop.

Migration watchpoint: our local `tdd` skill may already use tracer-bullet language. The upstream change is sharper around `pre-agreed seams` and may be worth folding in, but only if it does not weaken our repo-local engineering contract.

### `code-review`

The promoted `code-review` skill reviews `HEAD` against a fixed point supplied by the user:

- Uses `git diff <fixed-point>...HEAD`.
- Finds spec sources from commits, user paths, docs/spec files, or asks the user.
- Finds standards sources from repo docs.
- Adds a built-in Fowler smell baseline even when repo standards are missing.
- Runs Standards and Spec as parallel sub-agents and reports them separately.

Migration watchpoint: our pack currently has `review` and `convergent-pr-review`. Do not blindly rename unless we want to align with upstream terminology and update every router, guide, and skill that says `review`.

### `implement`

Only one direct change:

- Close-out review changed from `/review` to `/code-review`.

Migration watchpoint: if we do not rename our review skill, do not ingest this line verbatim.

### `grilling`

Small but important boundary change:

- Description now uses the leading word `Grill`.
- Adds: do not enact the plan until the user confirms shared understanding.

Migration watchpoint: low-risk and aligned with our approval-gate taste.

### `research`

New skill shape:

- Spin up a background agent.
- Investigate against primary sources.
- Save a cited Markdown file where the repo already keeps notes.

Migration watchpoint: this reading lane overlaps with source distillation but
is much smaller and more general. Use it only when that narrower lane answers
the source question.

### `wayfinder`

Large new in-progress direction:

- Replaces decision mapping with a tracker-backed map.
- Starts by naming the `destination`.
- Creates a map issue labelled `wayfinder:map`.
- Creates child tickets by type: `research`, `prototype`, `grilling`, `task`.
- Uses native issue dependencies where possible.
- Defines the `frontier` as open, unblocked, unclaimed child tickets.
- Keeps unclear future work in `Not yet specified`.
- Keeps excluded work in `Out of scope`.
- Resolves only one ticket per session.

Migration watchpoint: this is conceptually close to our `parallel-implement`, tracker packets, and current-work router ideas. Treat it as research input, not a drop-in replacement.

## Setup And Tracker Changes

`setup-matt-pocock-skills` tracker templates gained `Wayfinding operations` sections for GitHub, GitLab, and local markdown trackers.

New tracker concepts:

- `wayfinder:map`
- `wayfinder:<type>`
- child tickets
- native blocking/dependency links
- frontier query
- claim by assignment or local `Status: claimed`
- resolution comment plus map context pointer

Migration watchpoint: if `wayfinder` is not adopted, these template additions are extra tracker surface area. If adopted, this should be the single source of truth for map mechanics.

## Docs And Packaging Changes

Promoted skills now get human-facing docs pages under:

- `docs/engineering/*.md`
- `docs/productivity/*.md`

The update adds `.agents/writing-docs.md`, which says docs pages:

- are not copies of `SKILL.md`;
- explain why and when to reach for the skill;
- use absolute published links;
- include `What it does`, `When to reach for it`, and `Where it fits`;
- expose leading words without reproducing the runbook.

Plugin manifest changes:

- Adds `implement`.
- Adds `research`.
- Adds `code-review`.
- Removes `misc` skills from promoted/public docs.

Migration watchpoint: our repo deliberately keeps boot docs tiny and avoids docs sprawl. If we adopt upstream docs pages, keep them clearly outside the active agent boot path.

## High-Value Candidate Imports

These are the upstream changes most likely to improve our pack with low risk:

- Add the `grilling` confirmation gate.
- Consider `tdd`'s `pre-agreed seams` language.
- Consider the `research` skill as a small, general primary-source reading lane.
- Borrow `code-review`'s fixed-point plus Standards/Spec split only if it improves our existing `review` skill without colliding with `convergent-pr-review`.
- Keep `.agents/writing-docs.md` as a reference for human-facing docs only if we decide public docs pages are in scope.

## Do Not Blindly Ingest

- Do not rename `review` to `code-review` without updating routers, guides, and every skill reference.
- Do not add wayfinder tracker labels/templates unless adopting `wayfinder`.
- Do not copy upstream docs pages into the active boot path.
- Do not treat upstream `to-prd` docs as authoritative for our local `to-prd`; our local skill now has stricter source trace and approval gates.
