# Matt Pocock Skills v1.1 Upstream Audit

Durable source and reconstruction: [UPSTREAM-SOURCE.md](UPSTREAM-SOURCE.md).

Snapshot before updating `.tmp/mattpocock-skills`.

## Update Window

- Local checkout: `.tmp/mattpocock-skills`
- Remote: `https://github.com/mattpocock/skills.git`
- Branch: `main`
- Before fetch/update: `66f92b61f5b1434a1c7422f6fbd8efc5ee0c0214` (`66f92b6`, merge PR #456)
- Incoming `origin/main`: `d574778` (`v1.1.0`, merge PR #353)
- Working tree before update: clean
- Incoming diff size: 57 files, 428 insertions, 374 deletions

Fetch also surfaced these new remote branches:

- `fix/wayfinder-self-grilling`
- `fix/wayfinder-tracker-indirection`
- `negative-space-prompting`
- `release/v1.1`
- `to-issues-sub-issues-and-prototype`
- `to-issues/wide-refactor-expand-contract`
- `wayfinder-no-fog-early-exit`
- `wayfinder/plan-not-execute`

## High-Signal Changes

### Planning Vocabulary

The main planning chain changed from:

`idea -> /to-prd -> /to-issues -> /implement`

to:

`idea -> /to-spec -> /to-tickets -> /implement`

The notable move is not just a rename. "Spec" becomes the through-line artifact term, while "tickets" becomes the implementation-slice term. That reduces the overloaded issue/PRD vocabulary and makes the router easier to read.

Possible lesson: our pack should keep artifact names boring and literal where possible. If users already say "ticket" for work items and "spec" for intent, skill names should probably follow that instead of defending bespoke terms.

### `to-tickets`

`to-issues` was deleted and replaced with `to-tickets`.

New behavior emphasizes:

- tracer-bullet vertical slices;
- explicit blocking edges on every ticket;
- local-file and real-tracker modes as the same conceptual artifact;
- native tracker features, especially sub-issues and blocking links, when available;
- wide-refactor handling through expand-contract sequencing instead of forcing every change into a vertical slice.

Possible lesson: dependency shape deserves first-class language. "Blocked by" and "frontier" are stronger than a plain ordered issue list because they support parallel agent work without hiding sequencing assumptions.

### `to-spec`

`to-prd` was renamed to `to-spec`.

The new skill keeps the "you may know this as a PRD" bridge, but centers the output as a spec. It also asks the agent to sketch testing seams before writing/publishing, then confirm them with the user.

Possible lesson: a spec-writing skill can do more than summarize product intent. It can force the earliest testability conversation while the feature shape is still cheap to change.

### `wayfinder`

`wayfinder` moved from `skills/in-progress/` into `skills/engineering/`, was added to plugin metadata, and became a user-invoked engineering skill.

The strongest design changes:

- it is framed as planning by default, not execution;
- it uses a `Destination` to set scope before tickets exist;
- the map is an index, not a store, so decisions live in tickets and the map only points at them;
- it separates in-scope fog (`Not yet specified`) from `Out of scope`;
- it prefers issue-tracker child issues and native blocking relationships;
- a session claims a ticket by assignment rather than by a claim label;
- ticket types distinguish HITL and AFK work, preventing an agent from "grilling" itself;
- it has an early exit when there is no real fog and the work fits one session.

Possible lesson: for large ambiguous efforts, the useful artifact may be a decision map rather than an implementation plan. The map should not duplicate ticket content; it should preserve orientation and scope.

### Router And Docs

`ask-matt` now routes through:

`/grill-with-docs -> /to-spec -> /to-tickets -> /implement`

It also adds `wayfinder` as a situational on-ramp for greenfield or huge-feature efforts that are too foggy for one session. The README and engineering docs now list `implement` and `wayfinder` under user-invoked engineering skills.

Possible lesson: routers need maintenance whenever the skill graph changes. A router should describe the main happy path, then name situational on-ramps without making every new skill the default front door.

### Writing-Great-Skills

The writing guide added `Negation` as a failure mode: steering by prohibition can make the forbidden behavior more salient, so positive target behavior should be preferred, with prohibitions reserved for hard guardrails.

Possible lesson: our skill review rubric should explicitly look for "don't do X" language that can be rewritten as the desired behavior. This matches our existing preference for strong leading words and positive routing.

### Setup Skill

`setup-matt-pocock-skills` updated its explainer language from `to-issues` / `to-prd` to `to-tickets` / `to-spec`.

Possible lesson: setup docs are a dependency surface. Renames in the skill graph need to be chased into bootstrap text, not just README tables.

## Review Questions For Our Pack

- Should our public docs use `spec` / `tickets` more consistently where we currently say `PRD` / `issues`?
- Should worker packets or issue templates make `Blocked by` explicit even in local-file trackers?
- Should wide refactors get their own expand-contract guidance in our planning or implementation skills?
- Should our wayfinding / route-choice language distinguish "decision map" from "implementation plan" more sharply?
- Should the writing-review checklist add a negation pass: rewrite prohibitions into positive target behaviors when possible?
- Should setup or bootstrap docs be included in rename checks whenever a skill is added, removed, or renamed?
