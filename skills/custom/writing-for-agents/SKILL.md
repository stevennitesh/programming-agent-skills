---
name: writing-for-agents
description: Create, edit, or audit instructions agents consume, including skills, AGENTS.md, prompts, guides, specs, tickets, handoffs, and subagent assignments used in orchestration. Exclude ordinary human-facing prose, application code, and orchestration mechanics such as worker selection, scheduling, or integration.
---

# Writing for agents

Write documents that help an agent take the intended process reliably without
forcing identical output. Work directly on the requested document and its
affected pointers. Preserve the user's decisions, authority, and scope.

## 1. Understand the reader

Identify the agent that will read the document, what it must accomplish, the
source of truth for its decisions, and how the document enters context. Trace
the real prompt, pointer, caller, or workflow far enough to know what the text
must change.

When orchestrating subagents, use this skill to make each assignment bounded,
include only context that changes the worker's task, and state what the worker
returns. Preserve any worker contract owned by the orchestrating workflow. This
skill improves the assignment text; it does not choose workers, schedule
dependencies, integrate results, or verify the combined outcome.

For an audit, make no edits. For an authorized edit, change only the requested
document and directly affected links or metadata. Do not invent missing product
or domain decisions.

When the target is a skill, read
[Skill mechanics](references/SKILL-MECHANICS.md) before changing invocation,
frontmatter, package structure, or routing.

## 2. Organize the information

Separate ordered steps from reference material. Keep instructions every run
needs inline. Put substantial branch-only material behind a pointer that names
both when to read it and where it lives.

A context pointer is text already in view that tells the agent when to load
other material. Skill descriptions and links in `AGENTS.md` are context
pointers. Their wording controls discovery, so state the distinct trigger
branches first and avoid repeating synonyms for one branch. When required
material is missed, sharpen the pointer before moving the material inline.

Balance two costs. Context load is material the agent sees whether it needs it
or not. Cognitive load is what a person must remember to invoke or find. Spend
context on common behavior and cognitive load where human judgment should
choose the route.

Give each consequential step a completion criterion the agent can check. When
its scope is enumerable, require every relevant item to be accounted for. Do
not add a checklist when one clear sentence defines done.

If agents repeatedly rush a step, sharpen its completion criterion first. Split
the sequence only when a real context boundary can hide the later work.

## 3. Write the instructions

State the desired action first. Use prohibitions only for concrete failure or
authority boundaries, and pair each one with the safe action.

Use a leading word when a familiar term such as TDD, YAGNI, seam, or vertical
slice carries the intended practice more precisely than repeated explanation.
Define local terms where they first affect a decision. Keep exact API, domain,
and repository language when it carries required meaning.

Keep related rules together. Say each instruction once at its owning location.
Point to foreign procedures instead of copying them.

## 4. Prune

Delete material that does not change the receiving agent's behavior. Remove
duplicate meaning, stale explanation, inactive branches from the common path,
and instructions the agent already follows by default.

Treat the environment as a source of truth. A document that restates an easy
lookup from configuration, scripts, directory layout, or command help is a
cache. Keep that copy only when the lookup is costly or the document adds a
reason, convention, or warning the environment cannot show.

Prefer deleting a no-op sentence to polishing it. Shortness is not the goal;
every remaining line earning its place is.

## 5. Check the result

Read the final document as the receiving agent. Confirm that its pointers lead
to the right material, its steps end at the requested outcome, and the original
meaning survived the edit. Run the nearest useful syntax, link, metadata, or
consumer check when the document has a machine-read contract.

Only when the user explicitly asks to test, compare, or measure the document's
effect on agent behavior, read
[Behavioral evaluation](references/BEHAVIOR-EVALS.md). Otherwise do not run
behavioral cohorts, spawn evaluation agents, or create an evaluation report.

Return a concise account of what changed or, for an audit, the supported
findings. Include proof or a material gap when it affects the claim. Perform
installation, publishing, staging, or commit only when the user requests it.
Publishing and push require separate authority. Stop before unrelated edits.
