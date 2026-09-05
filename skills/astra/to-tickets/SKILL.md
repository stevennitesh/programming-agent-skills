---
name: to-tickets
description: Draft, publish, or repair delivery tickets from settled work, with acceptance and real dependencies. Use for explicit ticket requests or when multiple owners, sessions, or independently checkable outcomes justify decomposition; exclude ordinary implementation without a ticketing request.
---

# To tickets

Turn a settled outcome into useful delivery boundaries, preserving the meaning
that each implementer needs. Drafting does not require a tracker. Publication is
conditional, and implementation follows the user's original authorization.

## 1. Establish the source and need for decomposition

Read the supplied spec, conversation, or audit direction and its decision-bearing
references. Identify accepted behavior, constraints, acceptance, and remaining
uncertainty. A parent spec is useful but not required. Inspect relevant current
owners, callers, and proof to find practical boundaries; do not survey unrelated
code or re-open settled requirements.

For one coherent outcome without a useful ownership or dependency handoff, return
one bounded work item instead of manufacturing a graph. If the user explicitly
requests one tracker ticket, retain that publication request. Resolve ordinary
technical details within scope. For consequential missing product decisions,
identify the owner and affected work; for a real architecture question, use
`$codebase-design` when available. Draft independent settled work while marking
dependent items blocked. Do not label uncertain work ready or invent decisions
to complete a plan.

## 2. Choose cohesive delivery boundaries

Create the fewest tickets that each deliver a meaningful, independently checkable
outcome. Prefer a narrow path through the affected behavior over separate schema,
API, and UI tickets, but do not force every layer into every slice. Fold setup,
documentation, and tests into the outcome they support.

A technical prerequisite deserves its own ticket when migration, compatibility,
ownership, or an independently verifiable enabling result makes that useful.
Name what it unlocks and how to prove it. An early experiment or thin real path
earns a learning role only when its result changes later work. Do not add a
prefactoring stage to every feature.

For wide changes, cross-ticket integration, or learning that changes later work, read
[Delivery boundaries](references/delivery-boundaries.md). Keep coherent changes
together when splitting would manufacture temporary compatibility or conceal
unfinished integration. Size work so a fresh agent can recover the needed context;
context-window estimates do not replace meaningful boundaries.

## 3. Preserve acceptance and real dependencies

Each ticket needs its outcome, source pointer, settled decisions and scope,
observable acceptance, consequential constraints, and actual blockers. A source
link does not replace the acceptance that this ticket must satisfy. Preserve the
source's distinguishing input, state, result, and evidence class rather than
replacing them with generic instructions to handle edge cases or add tests.

Give each delivery-changing commitment an owning ticket. Repeat acceptance only
at a consumer that can independently lose that meaning. When work produces an
input another ticket needs, make that dependency explicit and prove the consuming
path with the actual produced result. Use stable pointers or a compact accepted
schema when they prevent guessing; leave routine implementation mechanics open.

An edge means a required predecessor outcome, not preferred order or possible
file overlap. Live concurrency and integration coordination belong to execution.
Check for missing commitments, duplicate work, unknown blockers, cycles, and a
truthful starting set. A required human decision or permission is an explicit
prerequisite, not an executable agent ticket. Do not claim a starting set exists
when every item is blocked.

## 4. Deliver the draft or publish

Present the proposed outcomes, acceptance, dependencies, and why the boundaries
are useful. Use one local document or the conversation for a draft unless the
user requests separate files. Revise when feedback changes the breakdown without
silently changing accepted behavior.

When publishing or repairing tracker items is requested, read
[Tracker publication](references/tracker-publication.md). Prepare the concrete
effects, follow existing authorization and repository policy, and verify the
result. Missing tracker setup blocks publication, not the useful draft. Do not
auto-publish merely because the skill is named to-tickets.

Finish with the draft or verified ticket pointers, dependencies, actionable work,
and material limits. Already-authorized implementation can continue; a planning
or ticket-publication request alone does not authorize implementing the graph,
spawning workers, or closing a parent.
