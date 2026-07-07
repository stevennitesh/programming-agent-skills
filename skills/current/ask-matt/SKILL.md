---
name: ask-matt
description: Ask which skill or flow fits your situation. A router skill over the explicit skills in this repo.
---

# Ask Matt

You don't remember every skill, so ask.

This is a **router skill**. Its job is to reduce **cognitive load** by routing the user's situation to one next skill or flow.

## Router Behavior

When invoked, recommend the next skill or flow.

If the route is clear, name one recommended path and why it fits.

If the route is unclear, ask one highest-leverage question.

Do not run the downstream skill unless the user asks.

## First-Time Setup

If this repo has not been configured for the engineering skills, route first to **`$setup-matt-pocock-skills`**.

Recommend **`$setup-matt-pocock-skills`** when `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, or `docs/agents/domain.md` is missing and the route depends on issues, triage labels, or domain docs.

## Main Flow: Idea -> Ship

Route here when the user has an idea and wants it built.

| Situation | Route |
| --- | --- |
| The idea needs sharpening in a codebase | **`$grill-with-docs`** |
| There is no codebase context to preserve | **`$grilling`** |
| Too much fog of war for a PRD | **`$wayfinder`** |
| A runnable answer is needed | **`$prototype`**, bridged by **`$handoff`** |
| Multi-session idea without a durable PRD | **`$to-prd`** then **`$to-issues`** |
| Existing PRD, spec, plan, or parent issue needs slices | **`$to-issues`** |
| One ready issue or slice | **`$implement`** |

Default path:

1. **`$grill-with-docs`** - sharpen the idea by interview and preserve resolved domain language or ADR-worthy decisions.
2. If conversation cannot settle a question, recommend **`$prototype`** and carry the answer back with **`$handoff`**.
3. If the build is multi-session and lacks a durable PRD, recommend **`$to-prd`** then **`$to-issues`**.
4. If a PRD, spec, plan, or parent issue already exists, recommend **`$to-issues`**.
5. If exactly one bounded slice is ready, recommend **`$implement`**.

## Incoming Work

Route here when work arrives raw from outside the planning flow.

| Situation | Route |
| --- | --- |
| Bugs, requests, or external PRs need sorting | **`$triage`** |
| A ticket is already ready-for-agent | **`$implement`** |
| A bug symptom is uncertain | **`$diagnosing-bugs`** |
| A behavior change is clear and testable | **`$tdd`** |

Do not triage issues produced by **`$to-issues`**. They are already intended to be ready-for-agent.

## Codebase Health

Route here for maintenance and design, not direct feature work.

| Situation | Route |
| --- | --- |
| Find architecture deepening opportunities | **`$improve-codebase-architecture`** |
| Design a deeper module or interface | **`$codebase-design`** |
| Resolve domain language or ADR-worthy decisions | **`$domain-modeling`** |
| Review a diff against standards and spec | **`$review`** |

Architecture work often generates an idea. Once the idea is chosen, route back into the main flow at **`$grill-with-docs`**.

## Crossing Sessions

Recommend **`$handoff`** when a fresh session should continue from the current conversation.

Recommend it when:

- the thread is near the edge of the smart zone
- a prototype needs its own session
- a fresh implementation session should start from a compact brief
- the current conversation must be preserved without relying on `/compact`

Prefer `/compact` only when staying in the same conversation is fine and losing verbatim history is acceptable.

`$handoff` forks. `/compact` continues.

## Standalone Routes

| Situation | Route |
| --- | --- |
| Improve or author skills | **`$writing-great-skills`** |

## Tie-Breakers

If the user has a loose idea, prefer **`$grill-with-docs`**.

If the idea has too many unresolved decisions for a PRD, prefer **`$wayfinder`**.

If the user names one ready issue, prefer **`$implement`**.

If the symptom, root cause, or repro is uncertain, prefer **`$diagnosing-bugs`** before **`$tdd`**.

If the behavior is known and testable, prefer **`$tdd`**.

If the user asks what to work on next, prefer **`$triage`** for incoming tracker work and **`$improve-codebase-architecture`** for codebase health.

## Completion Criteria

Done means the user has one recommended next skill or flow, the reason it fits, and any setup or handoff needed before starting it.
