---
name: writing-for-agents
description: Write or audit agent-facing skills, AGENTS.md, guides, specs, prompts, and continuation handoffs. Exclude product discovery, ordinary prose, minor wording edits, and app task transfers.
---

# Writing for agents

Write guidance that helps a capable agent make the intended decisions with the
context it will actually receive. Preserve the user's settled choices and the
document's authority. For an audit, return findings without editing.

## 1. Identify the reader and the decision

Establish what the receiving agent must accomplish, what it will already know,
and how this document enters its context. Read the relevant caller or pointer
and the source that owns the rules. Resolve consequential gaps from those
sources; surface any remaining product or policy decision to its owner.

For a worker assignment, include the bounded task, necessary context, and
expected return. Keep orchestration decisions with the caller.

When preparing a continuation handoff for another agent or fresh context, read
[Continuation handoffs](references/continuation-handoffs.md). That reference owns
the packet and its checks; do not turn a request to write a handoff into executing
the next step or transferring a task. Ordinary progress reports do not require it.

When creating a skill or assessing or changing its discovery, structure, or
packaging, read
[Skill authoring](references/skill-authoring.md) for discovery and packaging.

## 2. Put information where it belongs

Keep common instructions together. Put substantial conditional detail behind
a link that says when to read it and where it lives. If agents miss a reference,
clarify its trigger before copying the material into the main document.

Use ordered steps for a procedure, lookup structure for reference, and reasons
and tradeoffs for explanation. A guide need not become a workflow. Split material
when readers need it at different times, rather than to satisfy a file-size rule.

Give each rule one authoritative home and link to procedures owned elsewhere.
Prefer current configuration, command help, and code over copied facts unless
the document adds a convention, reason, or costly-to-discover detail.

When changing an authoritative instruction, inspect directly affected callers and
competing current guidance. Reconcile useful material and retire obsolete pointers
within scope; distinguish historical evidence from instructions still in force.
For replacing specs or plans, follow
[Document reconciliation](../shape-work/references/durable-decisions.md#reconcile-competing-documents).
Keep this check bounded to the affected guidance.

## 3. Write concrete instructions, then prune

Put conditions and prerequisites before the actions they govern. Name the actor
when ownership could be confused, and make "only," "unless," and "after" attach
to one clear obligation. Prefer direct positive actions; retain prohibitions for
concrete boundaries. Name the observable outcome. Keep terminology
consistent and define local terms where they affect a decision. Match the form
to the ambiguity:

- For a required output shape, show its parts or one useful example.
- For an easily omitted requirement, put it in the relevant step or template.
- For conditional behavior, name an observable trigger, such as "If the task
  supplies a brief, read it." Preserve the owning policy when clarifying its
  conditions.
- For a hard boundary, state the prohibited action and the permitted next step.

Read each obligation as something the agent may enforce literally. Preserve
the distinction between requirements, recommendations, and examples. Avoid
turning a past incident or a local preference into a universal rule.

Delete repeated defaults, stale facts, and instructions with no identifiable
decision or failure to address. Retain non-obvious constraints and useful reasons.
Aim for sufficient guidance, without prescribing ordinary mechanics the agent
can choose from its tools and repository.

## 4. Check the behavior the document asks for

Read the result as a future agent with only the expected context. Check whether
it introduces an unnecessary stop, question, delegation, artifact, or test.
Resolve conflicting rules and missing prerequisites. Confirm that the intended
outcome and the user's choices survived the edit.

For changed triggers or conditional guidance, trace a representative applicable
case and a nearby excluded case through the entry pointer and relevant branches.
Confirm required guidance is encountered before the decision it governs without
activating unrelated procedures. This is an editorial walkthrough, not a required
agent run or behavioral test.

Check affected links and machine-read structure. For executable recipes, run
the changed path when authorized and practical, checking its observable result.
If execution is unavailable, identify the unverified part. Structural checks
do not establish that wording improves agent behavior; use a scoped behavioral
comparison when the user requests evidence of that effect.

Finish when the receiving agent can identify when the guidance applies, follow
it with the available context, and recognize completion without inventing
missing policy. Report the change and any material verification gap concisely.
